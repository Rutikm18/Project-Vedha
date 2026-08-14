"""
test_main_scripts_datastore_probe.py — safe read-only datastore probes make the
unauthenticated-access proof fire in the field.

Covers: service identification from Redis INFO / Memcached version / Elasticsearch
& CouchDB HTTP bodies (correct labels, not generic 'http'), the ladder wiring, and
the end-to-end memcached unauth finding. Pattern/parse logic — no live network.
"""
from __future__ import annotations

from main_scripts import findings as F
from main_scripts.service_banner import PROBE_LADDER, match_service


def _svc(banner: bytes):
    m = match_service(banner)
    return m["service"] if m else None


# ── identification from the new probes/bodies ────────────────────────────────
def test_redis_info_and_noauth_identify_as_redis():
    assert _svc(b"$1234\r\n# Server\r\nredis_version:7.2.0\r\nrun_id:ab") == "redis"
    assert _svc(b"-NOAUTH Authentication required.\r\n") == "redis"


def test_memcached_version_and_stat_identify_as_memcached():
    assert _svc(b"VERSION 1.6.21\r\n") == "memcached"
    assert _svc(b"STAT pid 1234\r\nSTAT uptime 99\r\n") == "memcached"


def test_elasticsearch_and_couchdb_win_over_generic_http():
    es = b'HTTP/1.1 200 OK\r\n\r\n{"cluster_name":"prod","tagline":"You Know, for Search"}'
    assert _svc(es) == "elasticsearch"
    # CouchDB sets `Server: CouchDB/x` — the body match must win over generic http.
    couch = b'HTTP/1.1 200 OK\r\nServer: CouchDB/3.3.2\r\n\r\n{"couchdb":"Welcome","version":"3.3.2"}'
    assert _svc(couch) == "couchdb"


# ── ladder wiring (safe, read-only commands) ─────────────────────────────────
def test_ladder_includes_safe_datastore_probes():
    d = dict(PROBE_LADDER)
    assert d["redis"] == b"INFO\r\n"
    assert d["memcached"] == b"version\r\n"
    # cheaper rungs still come first (identify-and-stop keeps datastore probes last)
    names = [n for n, _ in PROBE_LADDER]
    assert names.index("null") < names.index("redis")
    assert names.index("generic") < names.index("memcached")


# ── end-to-end: probe response -> unauth finding ─────────────────────────────
def test_memcached_probe_response_yields_unauth_finding():
    # What a real scan would record after the memcached `version` rung.
    fs = F.run_findings([{
        "scanner": "service_banner", "target": "10.0.0.9", "port": 11211, "status": "open",
        "data": {"service": "memcached", "banner": "VERSION 1.6.21"}}])
    hit = next(f for f in fs if f.rule_id == "SVC-UNAUTH-DATASTORE-ACCESS")
    assert hit.severity == F.SEV_HIGH and hit.data["service"] == "memcached"
