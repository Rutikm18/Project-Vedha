"""
Tests for ai_normalizer.py — 0% prior coverage.

Covers:
  - extract_raw_text: per-scanner text extraction logic
  - FakeAIClient: fixed lookup-table test double
  - AINormalizerCache: get/put/persistence
  - propose_candidates: caching, client failure fallback,
    malformed response handling, ai_assisted flag propagation
  - validate=False used throughout — tests must never make real NVD network calls.
"""
from __future__ import annotations

import json

import pytest

import ai_normalizer as ai_mod
from ai_normalizer import (
    AINormalizerCache,
    FakeAIClient,
    extract_raw_text,
    propose_candidates,
)
from models import Fact, SourceConfidence


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fact(scanner: str, data: dict, target: str = "10.0.0.1") -> Fact:
    return Fact(
        scanner=scanner, target=target,
        timestamp="2026-01-01T00:00:00Z",
        port=80, proto="tcp", status="open",
        data=data, evidence=None, error=None,
        source_confidence=SourceConfidence.inferred,
        source_file="test.jsonl", source_line=1,
    )


# ---------------------------------------------------------------------------
# C2-1: extract_raw_text
# ---------------------------------------------------------------------------

class TestExtractRawText:
    def test_service_banner_uses_first_line(self):
        fact = _fact("service_banner", {"first_line": "SSH-2.0-OpenSSH_8.4p1 Debian-5"})
        assert extract_raw_text(fact) == "SSH-2.0-OpenSSH_8.4p1 Debian-5"

    def test_service_banner_falls_back_to_banner(self):
        fact = _fact("service_banner", {"banner": "OpenSSH_8.4p1"})
        assert extract_raw_text(fact) == "OpenSSH_8.4p1"

    def test_service_banner_first_line_takes_priority_over_banner(self):
        fact = _fact("service_banner",
                     {"first_line": "first", "banner": "fallback"})
        assert extract_raw_text(fact) == "first"

    def test_service_banner_no_text_returns_none(self):
        fact = _fact("service_banner", {})
        assert extract_raw_text(fact) is None

    def test_web_scan_server_only(self):
        fact = _fact("web_scan", {"server": "nginx/1.18.0"})
        assert "nginx/1.18.0" in extract_raw_text(fact)

    def test_web_scan_tech_hints_only(self):
        fact = _fact("web_scan", {"tech_hints": ["PHP/7.4", "WordPress"]})
        result = extract_raw_text(fact)
        assert "PHP/7.4" in result
        assert "WordPress" in result

    def test_web_scan_server_and_hints_combined(self):
        fact = _fact("web_scan", {"server": "Apache/2.4", "tech_hints": ["PHP"]})
        result = extract_raw_text(fact)
        assert "Apache/2.4" in result
        assert "PHP" in result

    def test_web_scan_empty_data_returns_none(self):
        fact = _fact("web_scan", {})
        assert extract_raw_text(fact) is None

    def test_db_scan_with_engine_and_version(self):
        fact = _fact("db_scan", {"engine": "postgresql", "server_version": "14.2"})
        result = extract_raw_text(fact)
        assert "postgresql" in result
        assert "14.2" in result

    def test_db_scan_without_engine_returns_none(self):
        fact = _fact("db_scan", {"server_version": "14.2"})
        assert extract_raw_text(fact) is None

    def test_ssh_inventory_returns_none(self):
        """ssh_inventory facts have no banner-style text for the AI to normalise."""
        fact = _fact("ssh_inventory", {"inventory": {"dpkg_packages": "nginx 1.18.0\n"}})
        assert extract_raw_text(fact) is None

    def test_port_scan_returns_none(self):
        fact = _fact("port_scan", {"port": 443})
        assert extract_raw_text(fact) is None


# ---------------------------------------------------------------------------
# C2-2: FakeAIClient
# ---------------------------------------------------------------------------

class TestFakeAIClient:
    def test_returns_registered_response(self):
        client = FakeAIClient({"nginx/1.18": [{"vendor": "nginx", "product": "nginx"}]})
        assert client.propose_cpe("nginx/1.18") == [{"vendor": "nginx", "product": "nginx"}]

    def test_returns_empty_for_unknown_text(self):
        client = FakeAIClient({})
        assert client.propose_cpe("something unknown") == []


# ---------------------------------------------------------------------------
# C2-3: AINormalizerCache
# ---------------------------------------------------------------------------

class TestAINormalizerCache:
    def test_get_returns_none_on_miss(self, tmp_path):
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        assert cache.get("some text") is None

    def test_put_and_get_roundtrip(self, tmp_path):
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        candidates = [{"vendor": "nginx", "product": "nginx"}]
        cache.put("nginx/1.18", candidates)
        assert cache.get("nginx/1.18") == candidates

    def test_cache_persists_across_instances(self, tmp_path):
        p = tmp_path / "cache.json"
        cache1 = AINormalizerCache(path=p)
        cache1.put("nginx/1.18", [{"vendor": "nginx", "product": "nginx"}])
        cache2 = AINormalizerCache(path=p)
        assert cache2.get("nginx/1.18") == [{"vendor": "nginx", "product": "nginx"}]

    def test_key_is_content_hash_not_plaintext(self, tmp_path):
        p = tmp_path / "cache.json"
        cache = AINormalizerCache(path=p)
        cache.put("raw text", [])
        stored = json.loads(p.read_text())
        assert "raw text" not in stored  # stored by sha256 key, not plaintext


# ---------------------------------------------------------------------------
# C2-4: propose_candidates
# ---------------------------------------------------------------------------

class TestProposeCandidates:
    def test_client_failure_returns_empty(self, tmp_path):
        """Any exception from the AI client yields [] — never raises, never
        blocks the pipeline from running in rule-based-only mode."""
        class _BrokenClient:
            def propose_cpe(self, text):
                raise RuntimeError("API down")

        fact = _fact("service_banner", {"first_line": "nginx/1.18"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        result = propose_candidates(fact, "nginx/1.18", _BrokenClient(),
                                    cache=cache, validate=False)
        assert result == []

    def test_cache_hit_bypasses_client(self, tmp_path):
        """When the cache already has an answer, the client must not be called."""
        class _ForbiddenClient:
            def propose_cpe(self, text):
                raise AssertionError("client was called despite a cache hit")

        p = tmp_path / "cache.json"
        seed_cache = AINormalizerCache(path=p)
        seed_cache.put("nginx/1.18", [{"vendor": "nginx", "product": "nginx"}])

        fact = _fact("service_banner", {"first_line": "nginx/1.18"})
        cache = AINormalizerCache(path=p)
        result = propose_candidates(fact, "nginx/1.18", _ForbiddenClient(),
                                    cache=cache, validate=False)
        assert len(result) == 1
        assert result[0].product == "nginx"

    def test_malformed_response_missing_product_skipped(self, tmp_path):
        """A candidate dict without a 'product' key must be silently skipped."""
        client = FakeAIClient({"apache": [{"vendor": "apache"}]})  # no "product"
        fact = _fact("service_banner", {"first_line": "apache"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        result = propose_candidates(fact, "apache", client,
                                    cache=cache, validate=False)
        assert result == []

    def test_malformed_response_not_a_list_returns_empty(self, tmp_path):
        """If the client returns something that isn't a list, return []."""
        class _BadClient:
            def propose_cpe(self, text):
                return {"oops": "not a list"}

        fact = _fact("service_banner", {"first_line": "something"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        result = propose_candidates(fact, "something", _BadClient(),
                                    cache=cache, validate=False)
        assert result == []

    def test_ai_assisted_flag_set_on_candidates(self, tmp_path):
        """Every candidate produced by propose_candidates must be tagged
        ai_assisted=True so downstream code can distinguish AI-derived
        findings from rule-based ones."""
        client = FakeAIClient({"nginx/1.18": [{"vendor": "nginx", "product": "nginx",
                                               "version": "1.18"}]})
        fact = _fact("service_banner", {"first_line": "nginx/1.18"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        candidates = propose_candidates(fact, "nginx/1.18", client,
                                        cache=cache, validate=False)
        assert candidates
        assert all(c.ai_assisted for c in candidates)

    def test_source_confidence_propagated_from_fact(self, tmp_path):
        """source_confidence on the resulting CPECandidate must match the
        originating Fact's source_confidence — not hardcoded."""
        client = FakeAIClient({"nginx/1.18": [{"vendor": "nginx",
                                               "product": "nginx"}]})
        fact = _fact("service_banner", {"first_line": "nginx/1.18"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        candidates = propose_candidates(fact, "nginx/1.18", client,
                                        cache=cache, validate=False)
        assert candidates
        assert all(c.source_confidence == SourceConfidence.inferred for c in candidates)

    def test_version_propagated_when_present(self, tmp_path):
        """When the AI response includes a version, it lands on the candidate."""
        client = FakeAIClient({"nginx/1.18": [{"vendor": "nginx",
                                               "product": "nginx",
                                               "version": "1.18.0"}]})
        fact = _fact("service_banner", {"first_line": "nginx/1.18"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        candidates = propose_candidates(fact, "nginx/1.18", client,
                                        cache=cache, validate=False)
        assert candidates
        assert candidates[0].version_raw == "1.18.0"

    def test_version_none_when_absent(self, tmp_path):
        """A candidate without a version key produces version_raw=None."""
        client = FakeAIClient({"curl": [{"vendor": "haxx", "product": "curl"}]})
        fact = _fact("service_banner", {"first_line": "curl"})
        cache = AINormalizerCache(path=tmp_path / "cache.json")
        candidates = propose_candidates(fact, "curl", client,
                                        cache=cache, validate=False)
        assert candidates
        assert candidates[0].version_raw is None

    def test_result_is_cached_after_first_call(self, tmp_path):
        """The result of a first successful client call must be stored in the
        cache so that a second call with the same text skips the client."""
        call_count = {"n": 0}

        class _CountingClient:
            def propose_cpe(self, text):
                call_count["n"] += 1
                return [{"vendor": "nginx", "product": "nginx"}]

        p = tmp_path / "cache.json"
        fact = _fact("service_banner", {"first_line": "nginx/1.18"})
        cache = AINormalizerCache(path=p)
        propose_candidates(fact, "nginx/1.18", _CountingClient(),
                           cache=cache, validate=False)
        propose_candidates(fact, "nginx/1.18", _CountingClient(),
                           cache=cache, validate=False)
        assert call_count["n"] == 1  # second call was served from cache
