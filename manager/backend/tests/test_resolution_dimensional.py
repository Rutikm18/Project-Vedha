"""
test_resolution_dimensional.py — a finding accrues a clean miss only when this run
proved it re-ran the SAME check against the SAME asset.

Host-level coverage is not enough. A deep scan finds a weakness on port 8443; a
later light scan never probes 8443 but does complete a port scan of the host, so
the host is "covered". The 8443 finding is absent because nothing looked, and a
host-level gate counts that as clean and auto-closes the customer's live risk.

Each finding is covered along its own dimension:
  posture      -> (rule_id, ip, port) was evaluated to match/no_match this run
  CVE          -> the finding's vendor:product was re-identified on the ip
  correlation  -> never (derived; there is no direct re-check)
  anything else, or no evidence at all -> not covered (fail closed).
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge
from app.detection.resolution import (
    evaluate_resolutions,
    finding_coverage,
    normalize_port,
    product_key,
)
from app.models.enums import FindingSeverity, FindingStatus

_NOW = datetime(2026, 9, 24, tzinfo=timezone.utc)
X = "10.0.0.5"
R = "POSTURE-TLS-DEPRECATED-PROTOCOL"
R2 = "POSTURE-TLS-WEAK-CIPHER"
APACHE_CPE = "cpe:2.3:a:apache:http_server:2.4.49:*:*:*:*:*:*:*"


def _finding(**kw):
    base = dict(
        id=uuid.uuid4(),
        severity=FindingSeverity.medium, status=FindingStatus.open,
        resolution_miss_count=0, detected_db_version="v1",
        resolved_at=None, resolution_method=None, resolution_run_id=None,
        evidence=None, cve_ids=None,
    )
    base.update(kw)
    return SimpleNamespace(**base)


def _posture(port, rule_id=R, **kw):
    return _finding(evidence={"rule_id": rule_id, "asset_ip": X, "port": port}, **kw)


def _cve(**kw):
    return _finding(cve_ids=["CVE-2021-41773"],
                    evidence={"asset_ip": X, "cpe": APACHE_CPE,
                              "cve_id": "CVE-2021-41773"}, **kw)


def _correlation(**kw):
    return _finding(evidence={"rule_id": "PATH-NTLM-RELAY", "correlation": True}, **kw)


def _db_returning(rows):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(all=lambda: rows))
    db.flush = AsyncMock()
    return db


def _run():
    return SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v1")


async def _evaluate(findings, *, covered=(X,), checks=(), products=None, skips=None):
    db = _db_returning([(f, X) for f in findings])
    return await evaluate_resolutions(
        db, uuid.uuid4(), _run(), {"assets": list(covered)}, _NOW,
        evaluated_checks=set(checks), identified_products=products or {},
        skips=skips)


# ── the defect ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_rule_not_rechecked_on_its_port_is_skipped_not_a_clean_miss():
    """The false-clean this file exists for: host X is covered, this rule WAS run
    on X (port 22) and another rule WAS run on 8443 — but THIS rule was never run
    on 8443. Nothing proves the 8443 weakness is gone."""
    f = _posture(8443)
    skips: dict = {}

    resolved = await _evaluate(
        [f], checks={(R, X, 22), (R2, X, 8443)}, skips=skips)

    assert resolved == 0
    assert f.resolution_miss_count == 0, "an unproven absence must not advance the streak"
    assert f.status == FindingStatus.open
    assert f.resolution_method is None
    assert skips == {"rule not re-evaluated on this port": 1}


@pytest.mark.asyncio
async def test_rule_not_rechecked_never_closes_a_high_on_its_second_miss():
    """Same gap on a high finding already one miss in: counting it would close it."""
    f = _posture(8443, severity=FindingSeverity.high, resolution_miss_count=1)

    resolved = await _evaluate([f], checks={(R, X, 22), (R2, X, 8443)})

    assert resolved == 0
    assert f.resolution_miss_count == 1
    assert f.status == FindingStatus.open


@pytest.mark.asyncio
async def test_rule_rechecked_clean_on_its_port_pends_then_resolves_at_threshold():
    """With the rule evaluated no_match on 8443 the old lifecycle applies: a high
    finding needs two consecutive proven-clean runs."""
    f = _posture(8443, severity=FindingSeverity.high)
    checks = {(R, X, 8443)}

    first = await _evaluate([f], checks=checks)
    assert first == 0
    assert f.resolution_miss_count == 1
    assert f.status == FindingStatus.open

    second = await _evaluate([f], checks=checks)
    assert second == 1
    assert f.resolution_miss_count == 2
    assert f.status == FindingStatus.remediated
    assert f.resolution_method == "auto"


@pytest.mark.asyncio
async def test_host_level_posture_finding_is_covered_by_a_portless_evaluation():
    f = _posture(None)

    resolved = await _evaluate([f], checks={(R, X, None)})

    assert resolved == 1
    assert f.status == FindingStatus.remediated


@pytest.mark.asyncio
async def test_host_level_posture_finding_is_not_covered_by_a_port_evaluation():
    f = _posture(None)

    resolved = await _evaluate([f], checks={(R, X, 445)})

    assert resolved == 0
    assert f.resolution_miss_count == 0


@pytest.mark.asyncio
async def test_cve_finding_resolves_when_its_product_was_reidentified():
    f = _cve()

    resolved = await _evaluate([f], products={X: {"apache:http_server"}})

    assert resolved == 1
    assert f.status == FindingStatus.remediated
    assert f.resolution_miss_count == 1


@pytest.mark.asyncio
async def test_cve_finding_is_skipped_when_its_product_was_not_reidentified():
    f = _cve()
    skips: dict = {}

    resolved = await _evaluate(
        [f], products={X: {"openbsd:openssh"}, "10.0.0.9": {"apache:http_server"}},
        skips=skips)

    assert resolved == 0
    assert f.resolution_miss_count == 0
    assert f.status == FindingStatus.open
    assert skips == {"product not re-identified": 1}


@pytest.mark.asyncio
async def test_correlation_finding_is_never_auto_resolved():
    """A derived attack path has no direct re-check. It carries a rule_id, so an
    evaluation under that id must still not cover it."""
    f = _correlation()
    skips: dict = {}

    resolved = await _evaluate([f], checks={("PATH-NTLM-RELAY", X, None)},
                               products={X: {"apache:http_server"}}, skips=skips)

    assert resolved == 0
    assert f.resolution_miss_count == 0
    assert skips == {"derived finding; no direct re-check": 1}


@pytest.mark.asyncio
async def test_empty_evidence_sets_resolve_nothing_even_on_covered_hosts():
    """Every engine fallback path hands over empty sets. The host is covered, yet
    no finding of any kind may accrue a miss."""
    findings = [_posture(8443), _posture(None), _cve(), _correlation(),
                _finding(evidence={"note": "unknown shape"}), _finding()]
    skips: dict = {}

    resolved = await _evaluate(findings, skips=skips)

    assert resolved == 0
    assert all(f.resolution_miss_count == 0 for f in findings)
    assert all(f.status == FindingStatus.open for f in findings)
    assert skips == {
        "rule not re-evaluated on this port": 2,
        "product not re-identified": 1,
        "derived finding; no direct re-check": 1,
        "no coverage dimension for this finding": 2,
    }


@pytest.mark.asyncio
async def test_omitting_the_evidence_sets_fails_closed():
    """A caller that never passes the evidence gets no auto-resolution at all."""
    f = _posture(8443)
    db = _db_returning([(f, X)])

    resolved = await evaluate_resolutions(db, uuid.uuid4(), _run(), {"assets": [X]}, _NOW)

    assert resolved == 0
    assert f.resolution_miss_count == 0


@pytest.mark.asyncio
async def test_uncovered_host_keeps_the_first_gate_and_its_reason():
    f = _posture(8443)
    skips: dict = {}

    resolved = await _evaluate([f], covered=("10.0.0.99",), checks={(R, X, 8443)},
                               skips=skips)

    assert resolved == 0
    assert f.resolution_miss_count == 0
    assert skips == {"asset not re-observed": 1}


@pytest.mark.asyncio
async def test_db_version_change_is_counted_under_its_own_reason():
    f = _cve(detected_db_version="v0")
    skips: dict = {}

    resolved = await _evaluate([f], products={X: {"apache:http_server"}}, skips=skips)

    assert resolved == 0
    assert f.resolution_miss_count == 0
    assert list(skips) == ["absent under a changed vuln-DB basis; not a confirmed fix"]


@pytest.mark.parametrize("outcome", ["no_evidence", "missing_input", "unparseable", "error"])
@pytest.mark.asyncio
async def test_blind_or_unassessed_trace_never_counts_as_evaluated(outcome):
    traces = [{"rule_id": R, "scanner": "tls_scan", "outcome": outcome,
               "asset_ip": X, "port": 8443, "reason": "x"}]
    checks = engine_bridge._evaluated_checks(traces)
    assert checks == set()

    f = _posture(8443)
    resolved = await _evaluate([f], checks=checks)
    assert resolved == 0
    assert f.resolution_miss_count == 0


# ── pure pieces ───────────────────────────────────────────────────────────────

def test_only_match_and_no_match_traces_are_evaluated_checks():
    traces = [
        {"rule_id": R, "outcome": "no_match", "asset_ip": X, "port": 8443},
        {"rule_id": R2, "outcome": "match", "asset_ip": X, "port": "443"},
        {"rule_id": "R3", "outcome": "no_match", "asset_ip": X, "port": None},
        {"rule_id": "R4", "outcome": "no_evidence", "asset_ip": X, "port": None},
        {"rule_id": "R5", "outcome": "missing_input", "asset_ip": X, "port": 22},
        {"rule_id": "R6", "outcome": "unparseable", "asset_ip": X, "port": 22},
        {"rule_id": "R7", "outcome": "error", "asset_ip": X, "port": 22},
        {"rule_id": "R8", "outcome": "no_match", "asset_ip": X, "port": "not-a-port"},
        {"rule_id": "R9", "outcome": "no_match", "asset_ip": "", "port": 22},
        {"outcome": "no_match", "asset_ip": X, "port": 22},
        "not a row",
    ]
    assert engine_bridge._evaluated_checks(traces) == {
        (R, X, 8443), (R2, X, 443), ("R3", X, None),
    }


def test_evaluated_checks_key_on_the_host_the_asset_row_stores():
    """_resolve_asset stores host_of(target); the trace carries the raw target."""
    traces = [{"rule_id": R, "outcome": "no_match", "asset_ip": f"{X}:8443", "port": 8443}]
    assert engine_bridge._evaluated_checks(traces) == {(R, X, 8443)}


def test_evaluated_outcomes_match_the_engine_constants():
    if not engine_bridge._ensure_importable():
        pytest.skip("detection_engine not importable in this environment")
    from posture_rules import OUTCOME_MATCH, OUTCOME_NO_MATCH  # type: ignore
    assert engine_bridge._EVALUATED_OUTCOMES == frozenset({OUTCOME_MATCH, OUTCOME_NO_MATCH})


def test_identified_products_become_sets_keyed_by_host():
    raw = {X: ["apache:http_server"], f"{X}:443": ["openbsd:openssh"],
           "10.0.0.9": ["Nginx:Nginx"], "10.0.0.10": "not-a-list"}
    assert engine_bridge._identified_products(raw) == {
        X: {"apache:http_server", "openbsd:openssh"},
        "10.0.0.9": {"nginx:nginx"},
    }
    assert engine_bridge._identified_products(None) == {}


@pytest.mark.parametrize("value,expected", [
    (None, None), (8443, 8443), ("8443", 8443), (" 22 ", 22), (443.0, 443),
])
def test_normalize_port_accepts(value, expected):
    assert normalize_port(value) == expected


@pytest.mark.parametrize("value", [True, "", "443/tcp", 443.5, [443], {"p": 1}])
def test_normalize_port_rejects(value):
    with pytest.raises(ValueError):
        normalize_port(value)


@pytest.mark.parametrize("cpe,expected", [
    (APACHE_CPE, "apache:http_server"),
    ("cpe:2.3:a:Apache:HTTP_Server:*:*:*:*:*:*:*:*", "apache:http_server"),
    ("cpe:2.3:a:*:http_server:2.4:*:*:*:*:*:*:*", None),
    ("cpe:/a:apache:http_server:2.4.49", None),
    ("cpe:2.3:a:apache", None),
    ("", None),
    (None, None),
])
def test_product_key(cpe, expected):
    assert product_key(cpe) == expected


def _cov(**kw):
    base = dict(ip=X, evidence=None, cve_ids=None, host_covered=True,
                evaluated_checks=set(), identified_products={})
    base.update(kw)
    return finding_coverage(**base)


def test_coverage_host_gate_comes_first():
    assert _cov(host_covered=False, evidence={"rule_id": R, "port": 22},
                evaluated_checks={(R, X, 22)}) == (False, "asset not re-observed")


def test_coverage_posture_port_given_as_string_matches_an_int_trace():
    covered, _ = _cov(evidence={"rule_id": R, "port": "8443"},
                      evaluated_checks={(R, X, 8443)})
    assert covered is True


def test_coverage_posture_with_an_unparseable_port_is_not_covered():
    assert _cov(evidence={"rule_id": R, "port": "8443/tcp"},
                evaluated_checks={(R, X, 8443), (R, X, None)}) == \
        (False, "rule not re-evaluated on this port")


def test_coverage_uses_the_asset_ip_not_the_evidence_ip():
    """Findings are joined to Asset.ip_address; a check on another host is not
    evidence for this one, whatever the evidence dict says."""
    assert _cov(ip="10.0.0.6", evidence={"rule_id": R, "asset_ip": X, "port": 22},
                evaluated_checks={(R, X, 22)}) == \
        (False, "rule not re-evaluated on this port")


def test_coverage_cve_requires_both_cve_ids_and_cpe():
    products = {X: {"apache:http_server"}}
    assert _cov(cve_ids=["CVE-1"], evidence={"cpe": APACHE_CPE},
                identified_products=products)[0] is True
    assert _cov(cve_ids=None, evidence={"cpe": APACHE_CPE},
                identified_products=products) == \
        (False, "no coverage dimension for this finding")
    assert _cov(cve_ids=["CVE-1"], evidence={"cve_id": "CVE-1"},
                identified_products=products) == \
        (False, "no coverage dimension for this finding")


def test_coverage_cve_with_an_unreadable_cpe_is_not_covered():
    assert _cov(cve_ids=["CVE-1"], evidence={"cpe": "garbage"},
                identified_products={X: {"apache:http_server"}}) == \
        (False, "product not re-identified")


def test_coverage_non_dict_evidence_has_no_dimension():
    assert _cov(evidence=["not", "a", "dict"]) == \
        (False, "no coverage dimension for this finding")


# ── engine_bridge carries the evidence ────────────────────────────────────────

_ENGINE = pytest.mark.skipif(not engine_bridge._ensure_importable(),
                             reason="detection_engine not importable in this environment")
_TS = "2026-09-02T11:03:50.208953+00:00"
_FACTS = [
    {"scanner": "smb_scan", "target": "10.0.0.10", "timestamp": _TS, "port": 445,
     "proto": "tcp", "status": "open",
     "data": {"smbv1_enabled": False, "smb2_supported": True,
              "signing_required": True, "negotiated_dialect": "0x0311"}},
    {"scanner": "service_banner", "target": "10.0.0.11", "timestamp": _TS, "port": 22,
     "proto": "tcp", "status": "open",
     "data": {"first_line": "SSH-2.0-OpenSSH_8.4p1 Debian-5"}},
]


@_ENGINE
def test_full_run_meta_carries_evaluated_checks_and_identified_products():
    _cve_d, _posture_d, meta = engine_bridge.detect_all_from_facts_traced(_FACTS)

    checks = meta["evaluated_checks"]
    smb_host = {(rid, port) for rid, ip, port in checks if ip == "10.0.0.10"}
    assert any(rid.startswith("POSTURE-SMB") for rid, _port in smb_host), \
        "smb_scan facts must evaluate smb rules"
    assert all(port == 445 for _rid, port in smb_host)
    # The banner host ran no smb_scan: those rules are no_evidence there, not evaluated.
    assert not any(rid.startswith("POSTURE-SMB") and ip == "10.0.0.11"
                   for rid, ip, _port in checks)
    assert meta["identified_products"] == {"10.0.0.11": {"openbsd:openssh"}}


@_ENGINE
def test_posture_only_retry_keeps_its_own_evaluated_checks_but_no_products(monkeypatch):
    import pipeline  # type: ignore

    def _boom(*_a, **_kw):
        raise RuntimeError("CVE snapshot unavailable")

    monkeypatch.setattr(pipeline, "run_full_detection", _boom)
    _cve_d, _posture_d, meta = engine_bridge.detect_all_from_facts_traced(_FACTS)

    assert any(ip == "10.0.0.10" and port == 445 for _rid, ip, port in meta["evaluated_checks"])
    assert meta["identified_products"] == {}


@_ENGINE
def test_older_engine_fallback_carries_empty_evidence(monkeypatch):
    import pipeline  # type: ignore

    def _old(*_a, **_kw):
        raise ImportError("no run_full_detection")

    monkeypatch.setattr(pipeline, "run_full_detection", _old)
    _cve_d, _posture_d, meta = engine_bridge.detect_all_from_facts_traced(_FACTS)

    assert meta["evaluated_checks"] == set()
    assert meta["identified_products"] == {}


def test_unavailable_engine_carries_empty_evidence(monkeypatch):
    monkeypatch.setattr(engine_bridge, "_ensure_importable", lambda: False)
    _cve_d, _posture_d, meta = engine_bridge.detect_all_from_facts_traced(_FACTS)

    assert meta["evaluated_checks"] == set()
    assert meta["identified_products"] == {}


@pytest.mark.asyncio
async def test_create_findings_wires_the_evidence_and_records_skip_reasons():
    engagement_id = uuid.uuid4()
    result = {
        "facts": [{"scanner": "tls_scan", "target": f"{X}:8443", "status": "open"}],
        "scanner_runs": [{"id": "tls_scan", "status": "completed"}],
    }
    checks = {(R, X, 22)}
    products = {X: {"apache:http_server"}}
    meta = {"coverage": {}, "verdicts": {}, "evaluated_checks": checks,
            "identified_products": products}

    async def _fake_eval(db, eid, run, coverage, now, *, evaluated_checks,
                         identified_products, skips):
        assert evaluated_checks == checks
        assert identified_products == products
        skips["rule not re-evaluated on this port"] = 3
        return 0

    added = []
    db = MagicMock()
    db.add = MagicMock(side_effect=lambda o: added.append(o))
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_all_from_facts_traced",
                      return_value=([], [], meta)), \
         patch.object(engine_bridge, "evaluate_resolutions",
                      new=AsyncMock(side_effect=_fake_eval)) as mock_eval:
        await engine_bridge.create_findings_from_facts(db, engagement_id, result)

    mock_eval.assert_awaited_once()
    run = added[0]
    assert run.stats["coverage"]["assets"] == [X]
    assert run.stats["coverage"]["resolution_skips"] == {
        "rule not re-evaluated on this port": 3}
    # The evidence sets are in-memory only: never persisted, and stats stays JSON.
    blob = json.dumps(run.stats)
    assert "evaluated_checks" not in blob and "identified_products" not in blob


@pytest.mark.asyncio
async def test_create_findings_with_meta_lacking_evidence_passes_empty_sets():
    """A detector stub (or older bridge meta) with no evidence keys must reach
    resolution as EMPTY sets — never as a reason to fall back to host coverage."""
    result = {
        "facts": [{"scanner": "tls_scan", "target": X, "status": "open"}],
        "scanner_runs": [{"id": "tls_scan", "status": "completed"}],
    }
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_all_from_facts_traced",
                      return_value=([], [], {"coverage": {}, "verdicts": {}})), \
         patch.object(engine_bridge, "evaluate_resolutions",
                      new=AsyncMock(return_value=0)) as mock_eval:
        await engine_bridge.create_findings_from_facts(db, uuid.uuid4(), result)

    kwargs = mock_eval.await_args.kwargs
    assert kwargs["evaluated_checks"] == set()
    assert kwargs["identified_products"] == {}


# ── exposed-service findings (the Wave E follow-up) ───────────────────────────
_EXPOSED = "POSTURE-EXPOSED-BACKDOOR"


@pytest.mark.asyncio
async def test_exposed_service_finding_resolves_when_its_port_is_rechecked_clean():
    """A POSTURE-EXPOSED-* finding now carries a trace, so a re-scan that shows its
    port clean (no_match on that exact port) auto-resolves it — before this it
    could never satisfy finding_coverage and stayed open forever."""
    f = _posture(4444, rule_id=_EXPOSED)          # medium → one proven-clean run closes it
    resolved = await _evaluate([f], checks={(_EXPOSED, X, 4444)})
    assert resolved == 1
    assert f.status == FindingStatus.remediated
    assert f.resolution_method == "auto"


@pytest.mark.asyncio
async def test_exposed_service_finding_stays_open_without_its_own_port_recheck():
    """A trace for the same category on a DIFFERENT port proves nothing about 4444."""
    f = _posture(4444, rule_id=_EXPOSED)
    skips: dict = {}
    resolved = await _evaluate([f], checks={(_EXPOSED, X, 9999)}, skips=skips)
    assert resolved == 0
    assert f.status == FindingStatus.open
    assert f.resolution_miss_count == 0
    assert skips == {"rule not re-evaluated on this port": 1}
