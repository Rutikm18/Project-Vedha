"""
test_db_posture_rules.py — the database rule pack.

WHY IT EXISTS. db_scan was the only deep branch that ran on every network_va,
shipped facts to the manager, and had ZERO posture rules. An open Redis and a
hardened one produced identical output: a fact, a trust tier, an evidence
record, and no finding. The only thing that ever surfaced was the generic
"database port reachable" from the port catalog, which is a much weaker claim
than "this server handed us its data without being asked for a password".

Every fixture below is a REAL capture from tests/fixtures/probe_corpus/db_scan.json
(Redis 7.4.10, MongoDB 7.0.40, MySQL 8.4.11 on loopback), so these tests fail if
the probe's emitted shape drifts away from what the rules read.

THE TRAP THIS PINS. MongoDB answers isMaster WITHOUT credentials even when
authorization is fully enforced. A rule keyed on "isMaster succeeded" would flag
every MongoDB in an estate as unauthenticated. The signal must be a command the
server actually gates — hence serverStatus.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from models import Asset, Fact, SourceConfidence
import posture_rules as P

CORPUS = Path(__file__).parent / "fixtures" / "probe_corpus"


def _fact(scanner, data, port=None, status="open", target="10.0.0.5"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred, source_file="s", source_line=1)


def _captured(port):
    """The real db_scan fact for one port, straight from the probe corpus."""
    for e in json.loads((CORPUS / "db_scan.json").read_text()):
        if e["port"] == port:
            return e["data"]
    raise AssertionError(f"no captured db_scan fact for port {port}")


def _fire(rule_id, data, port=None):
    rule = next(r for r in P.RULES if r.rule_id == rule_id)
    return rule.detect(_fact("db_scan", data, port=port))


UNAUTH = "POSTURE-DB-UNAUTHENTICATED-ACCESS"
CLEAR = "POSTURE-DB-CLEARTEXT-TRANSPORT"


class TestUnauthenticatedAccess:
    def test_fires_on_real_open_redis(self):
        ev = _fire(UNAUTH, _captured(6379), port=6379)
        assert ev is not None
        assert ev["engine"] == "redis"
        assert ev["server_version"] == "7.4.10"

    def test_fires_on_real_open_mongodb(self):
        ev = _fire(UNAUTH, _captured(27017), port=27017)
        assert ev is not None
        assert ev["engine"] == "mongodb"

    def test_silent_when_auth_is_enforced(self):
        data = dict(_captured(6379), auth_required=True, unauthenticated_read=False)
        assert _fire(UNAUTH, data, port=6379) is None

    def test_silent_on_ismaster_only_shape(self):
        """The trap: identification alone must never imply exposure. MongoDB
        answers isMaster without credentials even when authorization is on."""
        data = {"db": True, "engine": "mongodb", "wire_reply_opcode": 1,
                "server_version": "7.0.40"}
        assert _fire(UNAUTH, data, port=27017) is None

    def test_silent_on_mysql_which_never_reports_unauth_read(self):
        assert _fire(UNAUTH, _captured(3306), port=3306) is None

    def test_requires_the_db_marker(self):
        """Without the discriminator the rule must not fire on a foreign fact."""
        assert _fire(UNAUTH, {"unauthenticated_read": True}) is None

    def test_severity_is_critical(self):
        rule = next(r for r in P.RULES if r.rule_id == UNAUTH)
        assert rule.severity == "critical"
        assert rule.cwe == "CWE-306"


class TestCleartextTransport:
    def test_fires_when_server_says_it_cannot_encrypt(self):
        data = {"db": True, "engine": "microsoft sql server",
                "ssl_supported": False, "encryption_mode": "not_supported",
                "server_version": "15.0.2000"}
        ev = _fire(CLEAR, data, port=1433)
        assert ev is not None
        assert ev["encryption_mode"] == "not_supported"

    def test_silent_on_real_tls_capable_mysql(self):
        """MySQL 8.4.11 advertises CLIENT_SSL — must not be reported."""
        assert _captured(3306)["ssl_supported"] is True
        assert _fire(CLEAR, _captured(3306), port=3306) is None

    def test_silent_when_the_probe_never_learned_it(self):
        """Absent evidence is not a cleartext finding — a short read would
        otherwise manufacture a report against a hardened server."""
        data = {"db": True, "engine": "mysql/mariadb", "server_version": "8.4.11"}
        assert _fire(CLEAR, data, port=3306) is None

    def test_auth_enforced_is_not_applied(self):
        """Authentication in front does not protect a cleartext channel — it
        just means credentials are what crosses it. De-escalating here would
        under-rank the finding."""
        rule = next(r for r in P.RULES if r.rule_id == CLEAR)
        assert rule.auth_enforced is None


class TestContract:
    @pytest.mark.parametrize("rule_id", [UNAUTH, CLEAR])
    def test_requires_names_only_universal_paths(self, rule_id):
        """`requires` must name ONLY paths that EVERY db_scan fact carries.

        This is the bug a live run caught. The engine-specific fields are split
        across engines — Redis and MongoDB report `unauthenticated_read` and no
        TLS capability; MySQL, Postgres and MSSQL report `ssl_supported` and no
        auth signal. Declaring either one made three of six trace rows report
        schema_drift against perfectly healthy hosts, which drowns the drift
        signal that exists to catch a real probe regression.
        """
        rule = next(r for r in P.RULES if r.rule_id == rule_id)
        assert rule.requires == ("db",)

    @pytest.mark.parametrize("rule_id", [UNAUTH, CLEAR])
    def test_declared_inputs_exist_in_the_real_corpus(self, rule_id):
        """Guards the failure no unit test catches: a rule reading a path the
        probe does not emit can never fire, and the host silently looks clean."""
        emitted = set()
        for e in json.loads((CORPUS / "db_scan.json").read_text()):
            emitted.update((e.get("data") or {}).keys())
        rule = next(r for r in P.RULES if r.rule_id == rule_id)
        for path in rule.requires:
            assert path in emitted, f"{rule_id} requires {path}, corpus lacks it"

    def test_every_captured_engine_carries_the_marker(self):
        """The marker is the one thing all engines must agree on — if a probe
        refactor drops it, both rules go silent estate-wide."""
        for e in json.loads((CORPUS / "db_scan.json").read_text()):
            assert e["data"].get("db") is True, f"port {e['port']} lacks the db marker"
