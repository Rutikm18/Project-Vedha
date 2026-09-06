"""finding_compliance — every finding maps to all five frameworks with real controls.

The mappings are curated trusted-source data; these tests pin completeness (no
finding is left with an empty framework) and a few anchor controls so an accidental
edit that guts a mapping is caught.
"""
from __future__ import annotations

from types import SimpleNamespace

from app.services.finding_compliance import FRAMEWORKS, compliance_for


def _f(**kw):
    base = dict(title="", description="", remediation="", cve_ids=[])
    base.update(kw)
    return SimpleNamespace(**base)


def test_every_finding_maps_to_all_five_frameworks():
    refs = compliance_for(_f(title="SSLv3 weak cipher"))
    assert [r["framework"] for r in refs] == list(FRAMEWORKS)
    assert len(refs) == 5


def test_each_ref_has_controls_and_a_rationale():
    for r in compliance_for(_f(title="RDP exposed on 3389")):
        assert r["controls"], r["framework"]
        assert r["rationale"].strip(), r["framework"]


def test_weak_tls_maps_to_pci_transmission_control():
    refs = {r["framework"]: r for r in compliance_for(_f(title="TLS 1.0 weak cipher"))}
    assert any("4.2.1" in c for c in refs["PCI DSS 4.0"]["controls"])


def test_default_creds_maps_to_pci_default_accounts():
    refs = {r["framework"]: r for r in compliance_for(_f(title="default password on admin"))}
    assert any("2.2.2" in c for c in refs["PCI DSS 4.0"]["controls"])


def test_missing_patch_maps_to_nist_flaw_remediation():
    refs = {
        r["framework"]: r
        for r in compliance_for(_f(title="missing security update", cve_ids=["CVE-2017-0144"]))
    }
    assert any("SI-2" in c for c in refs["NIST SP 800-53 Rev.5"]["controls"])


def test_default_creds_maps_to_hipaa_authentication():
    refs = {r["framework"]: r for r in compliance_for(_f(title="default credentials"))}
    hipaa = " ".join(refs["HIPAA Security Rule"]["controls"])
    assert "164.312" in hipaa


def test_generic_and_empty_findings_still_map_all_frameworks_nonempty():
    for finding in (_f(title="genuinely weird thing"), _f(title="")):
        refs = compliance_for(finding)
        assert len(refs) == 5
        for r in refs:
            assert len(r["controls"]) >= 1
