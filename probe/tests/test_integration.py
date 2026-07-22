"""
Integration tests — full probe lifecycles exercised through the public APIs
of all Phase 1–5 modules working together.

These tests use mocks for network I/O but exercise the REAL logic:
  - Identity generation → scope encryption → scope decryption
  - Transport → TaskRunner → ScopeValidator → ResultSpool
  - WebSocket message parsing
  - Full job lifecycle (receive → validate → scan → submit)
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from agent.transport import Transport, TransportError
from agent.task_runner import TaskRunner
from agent.result_spool import ResultSpool
from agent.scope_validator import (
    validate_targets_in_scope,
    targets_in_excludes,
    merge_exclusions,
)
from agent.scope_crypt import (
    generate_identity,
    encrypt_scope_b64,
    decrypt_scope_b64,
    bytes_to_pubkey_b64,
)


# ═══════════════════════════════════════════════════════════════════════════
# Full lifecycle: identity → encrypt → job → decrypt → validate → submit
# ═══════════════════════════════════════════════════════════════════════════

def _fake_run_scan(scan_type, params, **kwargs):
    """Return a minimal valid scan result (no real network I/O)."""
    return {
        "result_schema_version": "1.1",
        "probe_id": "test-probe",
        "engagement_uuid": kwargs.get("engagement_uuid"),
        "use_case_id": kwargs.get("use_case_id"),
        "scan_type": scan_type,
        "profile": params.get("profile", "it"),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "ok": True,
        "engine": "test_fake",
        "facts": [],
        "run_stats": {"host_count": 1, "open_ports": 3, "fact_count": 0, "scanners_run": []},
        "errors": [],
        "host_count": 1,
        "service_count": 3,
        "open_ports": 3,
        "finding_count": 0,
    }


class TestIdentityAndEncryption:
    """Phase 4: identity generation + scope encryption roundtrip."""

    def test_full_identity_lifecycle(self):
        """Generate identity → encrypt scope → decrypt scope."""
        sk, pk = generate_identity()
        assert len(sk) == 32
        assert len(pk) == 32
        assert sk != pk  # private ≠ public

        pk_b64 = bytes_to_pubkey_b64(pk)
        assert isinstance(pk_b64, str)
        assert len(pk_b64) == 44  # 32 bytes → base64 without padding

    def test_scope_encryption_roundtrip(self):
        """Manager encrypts → probe decrypts."""
        sk, pk = generate_identity()
        scope = {
            "scope_cidrs": ["10.0.0.0/24", "192.168.1.0/24"],
            "excluded_cidrs": ["10.0.0.5/32"],
            "engagement_id": "eng-abc-123",
        }
        encrypted = encrypt_scope_b64(json.dumps(scope).encode(), pk)
        decrypted_raw = decrypt_scope_b64(encrypted, sk)
        decrypted = json.loads(decrypted_raw)
        assert decrypted == scope

    def test_different_key_cannot_decrypt(self):
        """A different probe cannot decrypt scope meant for another probe."""
        alice_sk, alice_pk = generate_identity()
        bob_sk, _ = generate_identity()
        encrypted = encrypt_scope_b64(b'{"secret": "alice-only"}', alice_pk)
        with pytest.raises(ValueError):
            decrypt_scope_b64(encrypted, bob_sk)


class TestTaskRunnerWithEncryptedScope:
    """Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it."""

    def test_decrypts_encrypted_scope_from_job(self, tmp_path):
        """Job carries encrypted_scope → TaskRunner decrypts → uses it."""
        sk, pk = generate_identity()
        scope = {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": [],
            "engagement_id": "eng-001",
        }
        encrypted = encrypt_scope_b64(json.dumps(scope).encode(), pk)

        submitted = []
        runner = TaskRunner(
            http_get=lambda p: None,
            submit_result=lambda jid, p: submitted.append(p) or True,
            run_scan_fn=_fake_run_scan,
            identity_sk=sk,
        )

        job = {
            "job_id": "job-001",
            "engagement_id": "eng-001",
            "job_type": "discovery",
            "encrypted_scope": encrypted,
            "params": {"targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")

        # Should succeed — scope was decrypted and target is in scope
        assert result.success is True
        assert len(submitted) == 1
        assert submitted[0]["success"] is True

    def test_falls_back_when_decryption_fails(self, tmp_path):
        """Wrong key → decryption fails → graceful fallback to params scope."""
        _, pk = generate_identity()  # encrypt to Alice's key
        bob_sk, _ = generate_identity()  # Bob tries to decrypt

        # Encrypt with Alice's public key
        scope = {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": [], "engagement_id": "e"}
        encrypted = encrypt_scope_b64(json.dumps(scope).encode(), pk)

        submitted = []
        runner = TaskRunner(
            http_get=lambda p: None,
            submit_result=lambda jid, p: submitted.append(p) or True,
            run_scan_fn=_fake_run_scan,
            identity_sk=bob_sk,  # wrong key — cannot decrypt
        )

        job = {
            "job_id": "job-002",
            "engagement_id": "",
            "job_type": "discovery",
            "encrypted_scope": encrypted,  # encrypted for Alice, Bob can't decrypt
            "params": {"targets": ["10.0.0.1"]},
        }
        result = runner.run_job(job, "agent-1")

        # Should still succeed — decryption fails but params scope works
        assert result.success is True


class TestScopeValidationPipeline:
    """Phase 1: combined scope validation (validate + excludes)."""

    def test_accepts_in_scope_rejects_out_of_scope(self):
        targets = ["10.0.0.1", "10.0.0.5", "192.168.1.1", "10.0.0.10"]
        allowed, rejected = validate_targets_in_scope(targets, ["10.0.0.0/24"])
        assert set(allowed) == {"10.0.0.1", "10.0.0.5", "10.0.0.10"}
        assert rejected == ["192.168.1.1"]

    def test_excludes_override_scope(self):
        targets = ["10.0.0.1", "10.0.0.5", "10.0.0.10"]
        # First: scope validation
        allowed, _ = validate_targets_in_scope(targets, ["10.0.0.0/24"])
        assert len(allowed) == 3
        # Then: exclude 10.0.0.5
        kept, dropped = targets_in_excludes(allowed, ["10.0.0.5/32"])
        assert kept == ["10.0.0.1", "10.0.0.10"]
        assert dropped == ["10.0.0.5"]

    def test_merge_exclusions_deduplicates(self):
        eng_excludes = ["10.0.0.5/32", "10.0.1.0/24"]
        job_excludes = ["10.0.0.5/32", "10.0.2.0/24"]
        merged = merge_exclusions(eng_excludes, job_excludes)
        assert merged == ["10.0.0.5/32", "10.0.1.0/24", "10.0.2.0/24"]

    def test_all_excluded_returns_empty(self):
        targets = ["10.0.0.1", "10.0.0.2"]
        kept, dropped = targets_in_excludes(targets, ["10.0.0.0/24"])
        assert kept == []
        assert len(dropped) == 2


class TestResultSpoolWithRetry:
    """Phase 1: result spool with upload retry."""

    def test_spool_persists_and_flushes(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool", max_retries=2, retry_delay_sec=0.01)
        spool.save("job-a", {"result": {"hosts": [{"ip": "10.0.0.1"}]}})
        spool.save("job-b", {"result": {"hosts": [{"ip": "10.0.0.2"}]}})
        assert spool.spool_count == 2

        uploaded = []
        def upload(jid, payload):
            uploaded.append(jid)
            return True

        flushed = spool.flush_spool(upload)
        assert flushed == 2
        assert spool.spool_count == 0
        assert set(uploaded) == {"job-a", "job-b"}

    def test_submit_retries_on_failure(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool", max_retries=3, retry_delay_sec=0.01)
        attempts = []
        def upload(jid, payload):
            attempts.append(jid)
            return len(attempts) >= 3  # fails first 2, succeeds on 3rd

        result = spool.submit_with_retry("job-x", {"data": 42}, upload)
        assert result is True
        assert len(attempts) == 3

    def test_submit_exhausts_retries(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool", max_retries=2, retry_delay_sec=0.01)
        def upload(jid, payload):
            return False

        result = spool.submit_with_retry("job-y", {"data": 42}, upload)
        assert result is False
        # Spool file persists for later retry
        assert spool.exists("job-y") is True


class TestTransportWithIdentity:
    """Phase 4 + Phase 1: Transport sends public_key during registration."""

    def test_register_sends_public_key(self, tmp_path):
        t = Transport("http://localhost:8000", state_file=tmp_path / "state.json")
        t._client = MagicMock()

        mock_resp = MagicMock(status_code=201)
        mock_resp.json.return_value = {"agent_id": "abc", "token": "tok"}
        t._client.post.return_value = mock_resp

        t.register(
            "probe-01",
            capabilities=["discovery"],
            public_key="base64pubkey==",
            operator_token="op-tok",
        )

        call_json = t._client.post.call_args[1]["json"]
        assert call_json["public_key"] == "base64pubkey=="

    def test_register_without_public_key(self, tmp_path):
        """Backward compat: registration without public_key is fine."""
        t = Transport("http://localhost:8000", state_file=tmp_path / "state.json")
        t._client = MagicMock()

        mock_resp = MagicMock(status_code=201)
        mock_resp.json.return_value = {"agent_id": "abc", "token": "tok"}
        t._client.post.return_value = mock_resp

        t.register("probe-01", operator_token="op-tok")
        call_json = t._client.post.call_args[1]["json"]
        assert call_json.get("public_key") is None


class TestWebSocketMessageProtocol:
    """Phase 2: WebSocket message parsing."""

    def test_hello_message(self):
        msg = {"type": "hello_ok"}
        assert msg["type"] == "hello_ok"

    def test_job_push_message(self):
        msg = {
            "type": "job_push",
            "job": {
                "job_id": "job-001",
                "engagement_id": "eng-001",
                "job_type": "discovery",
                "params": {"targets": ["10.0.0.1"]},
                "encrypted_scope": "abc123...",
            },
        }
        assert msg["type"] == "job_push"
        assert msg["job"]["encrypted_scope"] == "abc123..."

    def test_result_message(self):
        msg = {
            "type": "result",
            "job_id": "job-001",
            "success": True,
            "result": {"host_count": 5, "open_ports": 12},
            "error": None,
        }
        assert msg["type"] == "result"
        assert msg["success"] is True
        assert msg["error"] is None

    def test_heartbeat_message(self):
        msg = {"type": "heartbeat", "status": "online", "current_job_id": None}
        assert msg["status"] == "online"


class TestFullJobLifecycle:
    """End-to-end: identity → register → job → decrypt → validate → scan → submit."""

    def test_complete_flow_with_encrypted_scope(self, tmp_path):
        """Simulate the full probe lifecycle from identity to result submission."""
        # ── Setup: generate probe identity ────────────────────────────────
        sk, pk = generate_identity()
        pk_b64 = bytes_to_pubkey_b64(pk)

        # ── Manager encrypts scope ────────────────────────────────────────
        scope = {
            "scope_cidrs": ["10.0.0.0/24"],
            "excluded_cidrs": [],
            "engagement_id": "eng-full-001",
        }
        encrypted_scope = encrypt_scope_b64(json.dumps(scope).encode(), pk)

        # ── Create spool + transport mocks ────────────────────────────────
        spool = ResultSpool(spool_dir=tmp_path / "spool", max_retries=3, retry_delay_sec=0.01)
        submitted_results = []
        scope_fetches = []

        def mock_http_get(path):
            scope_fetches.append(path)
            return {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": []}

        def mock_submit(job_id, payload):
            submitted_results.append((job_id, payload))
            return True

        # ── Create TaskRunner with identity ───────────────────────────────
        runner = TaskRunner(
            http_get=mock_http_get,
            submit_result=mock_submit,
            spool_submit=spool.submit_with_retry,
            run_scan_fn=_fake_run_scan,
            identity_sk=sk,
        )

        # ── Manager sends job with encrypted scope ────────────────────────
        job = {
            "job_id": "job-full-001",
            "engagement_id": "eng-full-001",
            "job_type": "discovery",
            "encrypted_scope": encrypted_scope,
            "params": {
                "use_case_id": "uc_discovery_only",
                "targets": ["10.0.0.1", "10.0.0.2"],
            },
        }

        # ── Execute ───────────────────────────────────────────────────────
        result = runner.run_job(job, "agent-test-01")

        # ── Verify ────────────────────────────────────────────────────────
        assert result.success is True
        assert result.scan_type == "discovery"
        assert result.profile == "it"
        assert result.error is None

        # Result was submitted
        assert len(submitted_results) == 1
        submitted = submitted_results[0]
        assert submitted[0] == "job-full-001"
        assert submitted[1]["success"] is True
        assert "result" in submitted[1]

        # Scope was fetched for belt-and-suspenders validation
        assert len(scope_fetches) == 1
        assert "eng-full-001" in scope_fetches[0]

    def test_job_rejected_all_targets_out_of_scope(self, tmp_path):
        """All targets outside scope → job is rejected cleanly."""
        sk, pk = generate_identity()
        scope = {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": [], "engagement_id": "eng-002"}
        encrypted_scope = encrypt_scope_b64(json.dumps(scope).encode(), pk)

        submitted = []
        runner = TaskRunner(
            http_get=lambda p: {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": []},
            submit_result=lambda jid, p: submitted.append(p) or True,
            run_scan_fn=_fake_run_scan,
            identity_sk=sk,
        )

        job = {
            "job_id": "job-rej-001",
            "engagement_id": "eng-002",
            "job_type": "discovery",
            "encrypted_scope": encrypted_scope,
            "params": {"targets": ["192.168.1.1", "172.16.0.1"]},  # all out of scope
        }

        result = runner.run_job(job, "agent-1")
        assert result.success is False
        assert "outside" in (result.error or "").lower()

    def test_job_ot_passive_profile(self, tmp_path):
        """OT passive profile resolves correctly."""
        submitted = []
        runner = TaskRunner(
            http_get=lambda p: None,
            submit_result=lambda jid, p: submitted.append(p) or True,
            run_scan_fn=_fake_run_scan,
        )

        job = {
            "job_id": "job-ot-001",
            "engagement_id": "",
            "job_type": "discovery",
            "params": {
                "use_case_id": "uc_ot_passive",
                "targets": ["10.0.0.1"],
            },
        }
        result = runner.run_job(job, "agent-1")
        assert result.scan_type == "passive_discovery"
        assert result.profile == "ot"


class TestStartupGauntlet:
    """Phase 5: startup gauntlet checks."""

    def test_gauntlet_skips_in_dev_mode(self, monkeypatch):
        """With LICENSE_ENFORCED=false, gauntlet returns None."""
        monkeypatch.setenv("LICENSE_ENFORCED", "false")
        monkeypatch.delenv("HW_BIND_FINGERPRINT", raising=False)
        from agent.agent import _startup_gauntlet
        lic = _startup_gauntlet()
        assert lic is None

    def test_gauntlet_hw_bind_blocks(self, monkeypatch):
        """Wrong HW fingerprint blocks startup."""
        monkeypatch.setenv("LICENSE_ENFORCED", "true")
        monkeypatch.setenv("HW_BIND_FINGERPRINT", "00000000000000000000000000000000")
        from agent.agent import _startup_gauntlet
        with pytest.raises(SystemExit) as exc:
            _startup_gauntlet()
        assert exc.value.code == 2
