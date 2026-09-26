"""Similar-finding grouping.

Findings are deduped per (engagement, asset, title), so one issue shows up once
per host — and the CVE track writes one row per CVE per host, the posture track
one row per port. Grouping collapses those into "one fix" units:

  rule    — same posture rule, any port, any host
  product — same vulnerable product + version (one upgrade fixes every CVE row)
  cve     — same CVE set when no product was identified
  title   — same normalised title (imports, seed data, anything else)
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from app.services.finding_groups import GroupRow, build_groups, group_identity

_NOW = datetime(2026, 9, 27, tzinfo=timezone.utc)
_ASSETS = [uuid.uuid4() for _ in range(4)]


def _row(title, *, severity="medium", status="open", asset=0, ip=None, port=None,
         rule_id=None, cpe=None, cves=(), risk=100.0, cvss=None, kev=False,
         validated=False, seen=0):
    return GroupRow(
        id=uuid.uuid4(), title=title, severity=severity, status=status,
        cvss=cvss, risk=risk, epss=None, cve_ids=tuple(cves),
        asset_id=_ASSETS[asset] if asset is not None else None,
        asset_ip=ip or (f"10.0.0.{asset + 1}" if asset is not None else None),
        asset_hostname=None, port=port, rule_id=rule_id, cpe=cpe, kev=kev,
        exploit_validated=validated,
        first_seen=_NOW - timedelta(days=seen), last_seen=_NOW - timedelta(days=seen),
    )


_SSH74 = "cpe:2.3:a:openbsd:openssh:7.4:*:*:*:*:*:*:*"
_SSH82 = "cpe:2.3:a:openbsd:openssh:8.2:*:*:*:*:*:*:*"


# ── identity ──────────────────────────────────────────────────────────────────

def test_identity_rule_ignores_port_suffix():
    key, kind, label = group_identity(_row("SMB signing not required (port 445)", rule_id="SMB-SIGNING-01"))
    assert (key, kind, label) == ("rule:smb-signing-01", "rule", "SMB signing not required")


def test_identity_product_includes_version():
    key, kind, label = group_identity(_row("CVE-2018-15473 — openssh", cves=["CVE-2018-15473"], cpe=_SSH74))
    assert (key, kind) == ("product:openbsd:openssh:7.4", "product")
    assert label == "openssh 7.4 — known vulnerabilities"


def test_identity_product_without_version():
    key, _, label = group_identity(_row("x", cves=["CVE-1"], cpe="cpe:2.3:a:apache:http_server:*:*:*:*:*:*:*:*"))
    assert key == "product:apache:http_server"
    assert label == "http server — known vulnerabilities"


def test_identity_cve_without_cpe_uses_sorted_cves():
    key, kind, _ = group_identity(_row("x", cves=["cve-2021-2", "CVE-2021-1"]))
    assert (key, kind) == ("cve:CVE-2021-1,CVE-2021-2", "cve")


def test_identity_title_is_normalised():
    a = group_identity(_row("Weak  TLS 1.0 enabled (port 443)"))
    b = group_identity(_row("weak tls 1.0 ENABLED"))
    assert a[0] == b[0] == "title:weak tls 1.0 enabled"
    assert a[1] == "title"
    assert a[2] == "Weak  TLS 1.0 enabled".replace("  ", " ")


def test_malformed_cpe_falls_back_to_cve():
    key, kind, _ = group_identity(_row("x", cves=["CVE-9"], cpe="not-a-cpe"))
    assert (key, kind) == ("cve:CVE-9", "cve")


# ── aggregation ───────────────────────────────────────────────────────────────

def test_seed_shape_collapses_to_one_group_per_issue():
    rows = [_row("SMB signing not required", asset=i) for i in range(3)]
    rows += [_row("Outdated OpenSSH 7.4 with known CVEs", severity="high", asset=i) for i in range(3)]
    rows += [_row("RDP exposed without Network Level Authentication", severity="critical", asset=3)]
    groups = build_groups(rows)
    assert [g["finding_count"] for g in groups] == [1, 3, 3]
    assert groups[0]["severity"] == "critical"
    smb = next(g for g in groups if g["label"] == "SMB signing not required")
    assert smb["host_count"] == 3
    assert smb["kind"] == "title"


def test_rule_on_two_ports_and_two_hosts():
    rows = [
        _row("SMBv1 enabled (port 139)", rule_id="SMB1", port=139, asset=0),
        _row("SMBv1 enabled (port 445)", rule_id="SMB1", port=445, asset=0),
        _row("SMBv1 enabled (port 445)", rule_id="SMB1", port=445, asset=1),
    ]
    [g] = build_groups(rows)
    assert g["finding_count"] == 3
    assert g["host_count"] == 2
    assert g["ports"] == [139, 445]
    assert {h["ip"] for h in g["hosts"]} == {"10.0.0.1", "10.0.0.2"}


def test_product_group_collects_cves_across_hosts():
    rows = [
        _row(f"{cve} — openssh", cves=[cve], cpe=_SSH74, asset=a, severity=sev, cvss=cv)
        for a in (0, 1)
        for cve, sev, cv in (("CVE-2018-15473", "medium", 5.3),
                             ("CVE-2016-10009", "high", 7.3),
                             ("CVE-2023-38408", "critical", 9.8))
    ]
    [g] = build_groups(rows)
    assert g["kind"] == "product"
    assert g["finding_count"] == 6
    assert g["host_count"] == 2
    assert g["cve_count"] == 3
    assert g["cves"] == ["CVE-2016-10009", "CVE-2018-15473", "CVE-2023-38408"]
    assert g["severity"] == "critical"
    assert g["severity_counts"] == {"critical": 2, "high": 2, "medium": 2}
    assert g["max_cvss"] == 9.8


def test_different_versions_stay_separate():
    rows = [_row("a", cves=["CVE-1"], cpe=_SSH74), _row("b", cves=["CVE-2"], cpe=_SSH82)]
    assert len(build_groups(rows)) == 2


def test_open_groups_rank_above_fully_closed_ones():
    rows = [
        _row("Old critical", severity="critical", status="remediated"),
        _row("Live medium", severity="medium", status="open"),
    ]
    assert [g["label"] for g in build_groups(rows)] == ["Live medium", "Old critical"]


def test_severity_tier_beats_kev_and_risk():
    rows = [
        _row("KEV high", severity="high", kev=True, risk=990),
        _row("Plain critical", severity="critical", risk=10),
    ]
    assert [g["label"] for g in build_groups(rows)] == ["Plain critical", "KEV high"]


def test_within_tier_kev_then_validated_then_risk():
    rows = [
        _row("A high risky", severity="high", risk=900),
        _row("B high kev", severity="high", kev=True, risk=100),
        _row("C high validated", severity="high", validated=True, risk=100),
    ]
    assert [g["label"] for g in build_groups(rows)] == ["B high kev", "C high validated", "A high risky"]


def test_status_counts_and_open_count():
    rows = [_row("X", status="open"), _row("X", status="confirmed", asset=1),
            _row("X", status="remediated", asset=2), _row("X", status="fp", asset=3)]
    [g] = build_groups(rows)
    assert g["open_count"] == 2
    assert g["status_counts"] == {"open": 1, "confirmed": 1, "remediated": 1, "fp": 1}


def test_members_sorted_and_capped():
    rows = [_row("X", severity="low", risk=1, asset=0), _row("X", severity="critical", risk=5, asset=1),
            _row("X", severity="critical", risk=50, asset=2)]
    [g] = build_groups(rows, member_cap=2)
    assert [m["severity"] for m in g["members"]] == ["critical", "critical"]
    assert g["members"][0]["risk"] == 50
    assert g["members_truncated"] is True
    assert g["top_finding_id"] == g["members"][0]["id"]


def test_findings_without_asset_are_counted_separately():
    rows = [_row("X", asset=None), _row("X", asset=0)]
    [g] = build_groups(rows)
    assert g["host_count"] == 1
    assert g["unassigned_count"] == 1


def test_first_and_last_seen_span():
    rows = [_row("X", seen=10), _row("X", seen=2, asset=1)]
    [g] = build_groups(rows)
    assert g["first_seen"] == _NOW - timedelta(days=10)
    assert g["last_seen"] == _NOW - timedelta(days=2)


def test_empty_input():
    assert build_groups([]) == []
