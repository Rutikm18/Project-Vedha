"""test_remediation_context.py — the facts a remediation plan is grounded in.

Every fact carries its provenance (scan / asset_record / not_recorded) so a plan
can say "not recorded" instead of inventing a value.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.remediation import context as rc


def _finding(evidence=None, cve_ids=None, severity="high", exploit_validated=False, epss=None):
    return SimpleNamespace(
        id="f1", title="t", evidence=evidence or {}, cve_ids=cve_ids or [],
        severity=SimpleNamespace(value=severity), exploit_validated=exploit_validated,
        epss_score=epss,
    )


def _asset(**kw):
    base = dict(ip_address="10.0.0.5", hostname="FS01", fqdn=None, os="Windows",
                os_version="Windows Server 2012 R2", asset_type=SimpleNamespace(value="server"),
                criticality=SimpleNamespace(value="high"), environment=None, tags=None)
    base.update(kw)
    return SimpleNamespace(**base)


def _service(**kw):
    base = dict(port=445, protocol="tcp", service_name="microsoft-ds", product="Samba",
                version="4.15.2", cpe=None, banner=None, exposure=None)
    base.update(kw)
    return SimpleNamespace(**base)


class TestProvenance:
    def test_service_facts_are_scan_and_asset_facts_are_records(self):
        ctx = rc.build_context(_finding({"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445}),
                               _asset(), _service())
        assert ctx.product == rc.Fact("Samba", "scan")
        assert ctx.host == rc.Fact("FS01", "asset_record")
        assert ctx.rule_id == "POSTURE-SMB-V1-ENABLED"
        assert ctx.port.value == 445

    def test_absent_fact_reads_not_recorded(self):
        ctx = rc.build_context(_finding(), None, None)
        assert ctx.version.source == "not_recorded"
        assert ctx.text("version") == "not recorded"
        assert "version" not in ctx.facts_used()

    def test_facts_used_lists_only_recorded(self):
        ctx = rc.build_context(_finding({"port": 445}), _asset(), _service())
        used = ctx.facts_used()
        assert "product" in used and "host" in used
        assert "banner_excerpt" not in used

    def test_evidence_product_used_when_no_service(self):
        ctx = rc.build_context(_finding({"product": "openssh", "matched_version": "8.2p1"}), _asset(), None)
        assert ctx.product == rc.Fact("openssh", "scan")
        assert ctx.version == rc.Fact("8.2p1", "scan")


class TestExposure:
    @pytest.mark.parametrize("value,expected", [
        ("external", "internet"), ("internal_only", "internal"),
        ("not_exposed", "internal"), ("ambiguous", "unknown"),
    ])
    def test_service_exposure_mapping(self, value, expected):
        ctx = rc.build_context(_finding({"port": 445}), _asset(), _service(exposure=value))
        assert ctx.exposure == expected

    def test_falls_back_to_evidence_internet_facing(self):
        ctx = rc.build_context(_finding({"internet_facing": True}), _asset(), _service())
        assert ctx.exposure == "internet"

    def test_falls_back_to_environment(self):
        ctx = rc.build_context(_finding(), _asset(environment="DMZ"), None)
        assert ctx.exposure == "internet"


class TestOsFamily:
    @pytest.mark.parametrize("os_name,os_version,asset_type,expected", [
        ("Windows", "Windows Server 2012 R2", "server", "windows"),
        ("Linux", "Ubuntu 22.04", "server", "linux"),
        ("macOS", "Darwin 23", "workstation", "macos"),
        (None, None, "printer", "network"),
        (None, None, "server", "unknown"),
    ])
    def test_family(self, os_name, os_version, asset_type, expected):
        a = _asset(os=os_name, os_version=os_version, asset_type=SimpleNamespace(value=asset_type))
        assert rc.build_context(_finding(), a, None).os_family == expected


class TestServicePick:
    def test_picks_service_on_evidence_port(self):
        svcs = [_service(port=22, product="OpenSSH"), _service(port=445)]
        assert rc.pick_service(_finding({"port": 445}), svcs).port == 445

    def test_nested_posture_evidence_port(self):
        svcs = [_service(port=3389, product="rdp")]
        assert rc.pick_service(_finding({"evidence": {"port": 3389}}), svcs).port == 3389

    def test_none_when_no_port(self):
        assert rc.pick_service(_finding(), [_service()]) is None


class TestSignals:
    def test_banner_truncated(self):
        ctx = rc.build_context(_finding({"port": 445}), _asset(), _service(banner="x" * 500))
        assert len(ctx.banner_excerpt.value) == 200

    def test_kev_and_fixed_version_from_evidence(self):
        ctx = rc.build_context(_finding({"kev": True, "fixed_version": "9.8p1"}, cve_ids=["CVE-2024-6387"]),
                               _asset(), None)
        assert ctx.kev is True
        assert ctx.fixed_version == "9.8p1"
        assert ctx.cve_ids == ("CVE-2024-6387",)

    def test_fragile_from_tags(self):
        a = _asset(tags={"v": 1, "auto": [{"key": "sector_fn", "value": "hsm"}], "manual": []})
        ctx = rc.build_context(_finding(), a, None)
        assert ctx.fragile is True
        assert ctx.fragile_reason

    def test_epss_float(self):
        from decimal import Decimal
        ctx = rc.build_context(_finding(epss=Decimal("0.7123")), _asset(), None)
        assert ctx.epss == pytest.approx(0.7123)
