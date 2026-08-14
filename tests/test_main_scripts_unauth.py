"""
test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive
P1 findings), from the collected banner. Pure classifier + findings rule.
"""
from __future__ import annotations

from main_scripts import findings as F
from main_scripts.unauth_access import classify_unauth_access, is_rce_capable


# ── classifier: True (unauth) / False (protected) / None (unknown) ───────────
def test_redis_unauth_info_leak_is_true():
    assert classify_unauth_access("redis", "# Server\r\nredis_version:7.2.0\r\nrun_id:ab") is True
    assert classify_unauth_access("redis", "+PONG\r\n") is True


def test_redis_noauth_is_protected():
    assert classify_unauth_access("redis", "-NOAUTH Authentication required.\r\n") is False


def test_redis_silent_is_unknown():
    assert classify_unauth_access("redis", "") is None
    assert classify_unauth_access("redis", "some unrelated bytes") is None


def test_elasticsearch_unauth_vs_secured():
    assert classify_unauth_access("elasticsearch",
                                  '{"name":"n1","cluster_name":"es","tagline":"You Know, for Search"}') is True
    assert classify_unauth_access("elasticsearch",
                                  '{"error":{"type":"security_exception"},"status":401}') is False


def test_couchdb_and_memcached_and_mongodb():
    assert classify_unauth_access("couchdb", '{"couchdb":"Welcome","version":"3.3.2"}') is True
    assert classify_unauth_access("memcached", "STAT pid 1234\r\nSTAT version 1.6.9\r\n") is True
    assert classify_unauth_access("mongodb", '{"ismaster":true,"maxWireVersion":21,"ok":1}') is True


def test_non_datastore_service_is_unknown():
    assert classify_unauth_access("http", "HTTP/1.1 200 OK") is None
    assert classify_unauth_access("ssh", "SSH-2.0-OpenSSH_9.6") is None
    assert classify_unauth_access(None, "anything") is None


def test_rce_capability_flag():
    assert is_rce_capable("redis") is True
    assert is_rce_capable("mongodb") is False


# ── findings rule ────────────────────────────────────────────────────────────
def _run(*facts):
    return F.run_findings(list(facts))


def test_unauth_redis_is_critical_and_rce_flagged():
    fs = _run({"scanner": "service_banner", "target": "10.0.0.9", "port": 6379, "status": "open",
               "data": {"service": "redis", "banner": "# Server\r\nredis_version:7.2.0"}})
    hit = next(f for f in fs if f.rule_id == "SVC-UNAUTH-DATASTORE-ACCESS")
    assert hit.severity == F.SEV_CRITICAL and hit.confidence == F.CONF_HIGH
    assert hit.data["rce_capable"] is True and "code execution" in hit.evidence.lower()


def test_unauth_elasticsearch_is_high():
    fs = _run({"scanner": "service_banner", "target": "t", "port": 9200, "status": "open",
               "data": {"service": "elasticsearch",
                        "banner": '{"cluster_name":"es","tagline":"You Know, for Search"}'}})
    hit = next(f for f in fs if f.rule_id == "SVC-UNAUTH-DATASTORE-ACCESS")
    assert hit.severity == F.SEV_HIGH and hit.data["rce_capable"] is False


def test_protected_redis_raises_no_unauth_finding():
    fs = _run({"scanner": "service_banner", "target": "t", "port": 6379, "status": "open",
               "data": {"service": "redis", "banner": "-NOAUTH Authentication required."}})
    assert "SVC-UNAUTH-DATASTORE-ACCESS" not in {f.rule_id for f in fs}
