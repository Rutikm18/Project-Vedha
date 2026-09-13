"""
test_exposure_analytics.py — the dashboard's Protocol Risk + Zone Health panels.

services/analytics.compute_exposure had no coverage at all (test_exposure.py
guards a different module, app.discovery.exposure). These tests pin the two
behaviours the panels were getting wrong: charging a host's worst finding to
every protocol it exposes, and averaging a zone's worst asset out of existence.
"""
from __future__ import annotations

from types import SimpleNamespace

from app.services.analytics import compute_exposure


def _asset(aid, environment=None):
    return SimpleNamespace(id=aid, environment=environment)


def _service(aid, port, name):
    return SimpleNamespace(asset_id=aid, port=port, service_name=name)


def _finding(aid, severity, port=None, evidence=None):
    if evidence is None:
        evidence = {"port": port} if port is not None else {}
    return SimpleNamespace(asset_id=aid, severity=severity, evidence=evidence)


def _protocol(out, name):
    return next(p for p in out["protocols"] if p["name"] == name)


# ── Protocol risk: attribution ────────────────────────────────────────────────

def test_a_critical_on_one_port_does_not_incriminate_the_others():
    """The defect this panel existed to stop reporting.

    Burden used to be computed PER ASSET and then handed to every service that
    asset exposed, so a host with a critical web RCE showed SSH at maximum risk
    and an operator reading the panel would go and harden SSH.
    """
    out = compute_exposure(
        assets=[_asset("a1", "prod")],
        services=[_service("a1", 80, "http"), _service("a1", 22, "ssh")],
        findings=[_finding("a1", "critical", port=80)],
    )
    http, ssh = _protocol(out, "HTTP"), _protocol(out, "SSH")
    assert http["severity"] == "critical" and http["findings"] == 1
    assert ssh["severity"] is None and ssh["findings"] == 0
    assert ssh["value"] == 0


def test_worst_severity_wins_per_service():
    out = compute_exposure(
        assets=[_asset("a1")],
        services=[_service("a1", 445, "smb")],
        findings=[
            _finding("a1", "low", port=445),
            _finding("a1", "critical", port=445),
            _finding("a1", "medium", port=445),
        ],
    )
    smb = _protocol(out, "SMB")
    assert smb["severity"] == "critical"
    assert smb["findings"] == 3


def test_same_port_on_different_assets_aggregates():
    out = compute_exposure(
        assets=[_asset("a1"), _asset("a2")],
        services=[_service("a1", 22, "ssh"), _service("a2", 22, "ssh")],
        findings=[_finding("a2", "high", port=22)],
    )
    ssh = _protocol(out, "SSH")
    assert ssh["severity"] == "high"
    assert ssh["assets"] == 2       # exposed on both
    assert ssh["findings"] == 1     # but only one finding


def test_clean_services_are_listed_not_hidden():
    """"Exposed and nothing wrong with it" is information. Hiding clean rows
    would make an empty panel ambiguous between "no services" and "no findings"."""
    out = compute_exposure(
        assets=[_asset("a1")],
        services=[_service("a1", 22, "ssh")],
        findings=[],
    )
    assert _protocol(out, "SSH")["severity"] is None
    assert out["unattributed_findings"] == 0


def test_findings_with_no_port_are_counted_not_smeared():
    """A host-level finding names no service, so it must not raise every
    protocol on the box — but it must not vanish silently either."""
    out = compute_exposure(
        assets=[_asset("a1")],
        services=[_service("a1", 22, "ssh"), _service("a1", 443, "https")],
        findings=[_finding("a1", "critical")],           # no port in evidence
    )
    assert all(p["severity"] is None for p in out["protocols"])
    assert out["unattributed_findings"] == 1


def test_port_is_read_from_a_host_colon_port_target():
    out = compute_exposure(
        assets=[_asset("a1")],
        services=[_service("a1", 3389, "ms-wbt-server")],
        findings=[_finding("a1", "high", evidence={"target": "10.0.0.5:3389"})],
    )
    assert _protocol(out, "MS-WBT-SERVER")["severity"] == "high"
    assert out["unattributed_findings"] == 0


def test_unmatched_port_and_missing_asset_count_as_unattributed():
    out = compute_exposure(
        assets=[_asset("a1")],
        services=[_service("a1", 22, "ssh")],
        findings=[
            _finding("a1", "high", port=9999),   # no service on that port
            _finding(None, "critical", port=22),  # no asset at all
            _finding("a1", "high", evidence={"port": "not-a-number"}),
            _finding("a1", "high", evidence=None),
        ],
    )
    assert _protocol(out, "SSH")["severity"] is None
    assert out["unattributed_findings"] == 4


def test_protocols_sort_worst_first_then_by_breadth():
    out = compute_exposure(
        assets=[_asset("a1"), _asset("a2")],
        services=[
            _service("a1", 22, "ssh"), _service("a2", 22, "ssh"),
            _service("a1", 445, "smb"),
            _service("a1", 80, "http"),
        ],
        findings=[_finding("a1", "medium", port=22), _finding("a1", "critical", port=445)],
    )
    names = [p["name"] for p in out["protocols"]]
    assert names[0] == "SMB"      # critical
    assert names[1] == "SSH"      # medium
    assert names[2] == "HTTP"     # clean, least urgent


# ── Zone health ───────────────────────────────────────────────────────────────

def test_one_critical_host_does_not_hide_behind_a_healthy_zone():
    """The zone score used to be a plain mean of per-asset burden, so a single
    critical host among ninety-nine clean ones scored 99 and read "Healthy" —
    averaging away the one thing the panel exists to surface."""
    assets = [_asset(f"a{i}", "prod") for i in range(100)]
    out = compute_exposure(
        assets=assets,
        services=[],
        findings=[_finding("a0", "critical")],
    )
    prod = out["zones"][0]
    assert prod["name"] == "PROD"
    assert prod["score"] < 60, prod        # below the "Watch" band, i.e. visible
    assert prod["affected"] == 1 and prod["assets"] == 100


def test_a_worse_zone_still_scores_below_a_less_bad_one():
    """Surfacing the worst asset must not flatten every affected zone onto one
    value — the panel's job is to RANK zones."""
    one_bad = compute_exposure(
        assets=[_asset(f"a{i}", "prod") for i in range(100)],
        services=[], findings=[_finding("a0", "critical")],
    )["zones"][0]
    many_bad = compute_exposure(
        assets=[_asset(f"a{i}", "prod") for i in range(100)],
        services=[], findings=[_finding(f"a{i}", "critical") for i in range(50)],
    )["zones"][0]
    assert many_bad["score"] < one_bad["score"]


def test_clean_zone_scores_full_marks_and_zones_sort_weakest_first():
    out = compute_exposure(
        assets=[_asset("a1", "corp"), _asset("a2", "dmz")],
        services=[],
        findings=[_finding("a2", "high")],
    )
    assert [z["name"] for z in out["zones"]] == ["DMZ", "CORP"]
    assert out["zones"][1]["score"] == 100
    assert out["zones"][1]["affected"] == 0


def test_untagged_assets_fall_into_one_unzoned_bucket():
    out = compute_exposure(
        assets=[_asset("a1"), _asset("a2", "   ")],
        services=[], findings=[],
    )
    assert [z["name"] for z in out["zones"]] == ["UNZONED"]
    assert out["zones"][0]["assets"] == 2


# ── Truncation ────────────────────────────────────────────────────────────────

def test_top_n_is_high_enough_for_the_ui_disclosure_to_do_something():
    """The backend used to cap at 6 while the panel also capped at 6, so its
    "Show all N" control could never reveal a row and protocols 7+ were
    unreachable. The server cap must sit well above the panel's."""
    assets = [_asset("a1")]
    services = [_service("a1", 1000 + i, f"svc{i:02d}") for i in range(30)]
    out = compute_exposure(assets=assets, services=services, findings=[])
    assert len(out["protocols"]) == 25            # default top_n
    assert len(out["protocols"]) > 6              # the panel's own CAP
