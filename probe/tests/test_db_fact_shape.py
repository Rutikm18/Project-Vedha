"""
test_db_fact_shape.py — the db_scan fact CONTRACT, not its protocol parsing.

WHY THIS EXISTS. db_scan was the only deep branch whose facts reached the
manager and were never assessed: it ran on every network_va, emitted engine and
version data, and had ZERO posture rules. The structural reason was the fact
shape — every sibling scanner emits a boolean discriminator (`ftp`, `dns`,
`nfs`, `ldap`, `vnc`) that the manager's detectors gate on, and db_scan emitted
none, so no rule could follow the house pattern.

These tests pin the marker so it cannot be dropped by a future refactor, which
would silently un-fire every DB rule while the scanner still looked healthy.
"""
from __future__ import annotations

from scanner.db_scanner import interpret_redis_info, stamp_db_fact


def test_marker_is_stamped():
    assert stamp_db_fact({"engine": "redis"})["db"] is True


def test_existing_facts_are_preserved():
    out = stamp_db_fact({"engine": "postgresql", "ssl_supported": True})
    assert out["engine"] == "postgresql"
    assert out["ssl_supported"] is True


def test_probe_output_never_overrides_the_marker():
    """A probe returning its own `db` key must not be able to unset the marker
    the manager gates on — every detector reads `d.get("db") is True`, so a
    False here would silently disable the whole DB rule pack for that host."""
    assert stamp_db_fact({"db": False, "engine": "mysql/mariadb"})["db"] is True


def test_redis_unauth_shape_survives_stamping():
    """The one high-value DB signal already collected today must keep its shape
    once the marker is added — this is what POSTURE-DB-UNAUTHENTICATED-ACCESS
    will read."""
    out = stamp_db_fact(
        interpret_redis_info("$100\r\n# Server\r\nredis_version:7.2.4\r\n"))
    assert out["db"] is True
    assert out["unauthenticated_read"] is True
    assert out["auth_required"] is False
    assert out["engine"] == "redis"
