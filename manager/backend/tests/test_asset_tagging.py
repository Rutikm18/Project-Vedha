"""
test_asset_tagging.py — the pure evidence-based asset tagger (app/intel/tagging.py).

Every tag must carry evidence; a host we know nothing about gets no tags rather
than guesses. Covers each rule namespace, BFSI sector signatures, derived
compliance scope / data sensitivity, dedupe, and the manual-tag-preserving merge.
"""
from __future__ import annotations

from app.intel.tagging import (
    AssetFacts,
    ServiceFact,
    derive_tags,
    merge_tags,
    tag_strings,
)


def _tags(facts: AssetFacts) -> set[str]:
    return {f"{t.key}:{t.value}" for t in derive_tags(facts)}


def _svc(port: int, name: str | None = None, **kw) -> ServiceFact:
    return ServiceFact(port=port, service_name=name, **kw)


# ── no evidence, no tags ─────────────────────────────────────────────────────

def test_bare_private_host_only_gets_its_zone():
    tags = _tags(AssetFacts(ip="10.20.30.40"))
    assert tags == {"zone:10.20.30.0/24"}


def test_default_server_asset_type_is_not_a_host_type_claim():
    # asset_type=server is the historical default when nothing classified the host.
    tags = _tags(AssetFacts(ip="10.0.0.1", asset_type="server"))
    assert not any(t.startswith("host_type:") for t in tags)


def test_every_tag_carries_rule_confidence_and_evidence():
    facts = AssetFacts(ip="10.0.0.5", os="Windows Server 2019",
                       services=(_svc(1433, "ms-sql-s"),))
    for tag in derive_tags(facts):
        assert tag.rule and tag.evidence
        assert 0.0 < tag.confidence <= 1.0
        assert tag.source == "auto"


# ── host_type / os_family ────────────────────────────────────────────────────

def test_host_type_from_classifier_role_uses_its_confidence():
    tags = derive_tags(AssetFacts(ip="10.0.0.2", device_role="network_device",
                                  role_confidence=0.8))
    host = [t for t in tags if t.key == "host_type"]
    assert [(t.value, t.confidence) for t in host] == [("network", 0.8)]


def test_os_family_detection():
    assert "os_family:windows" in _tags(AssetFacts(ip="10.0.0.1", os="Microsoft Windows 10"))
    assert "os_family:linux" in _tags(AssetFacts(ip="10.0.0.1", os="Ubuntu 22.04"))
    assert "os_family:network_os" in _tags(AssetFacts(ip="10.0.0.1", os="Cisco IOS 15.2"))
    assert "os_family:macos" in _tags(AssetFacts(ip="10.0.0.1", os="macOS 14"))


def test_os_family_falls_back_to_banner_with_lower_confidence():
    tags = derive_tags(AssetFacts(ip="10.0.0.1", services=(
        _svc(22, "ssh", banner="SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"),)))
    os_tags = [t for t in tags if t.key == "os_family"]
    assert [t.value for t in os_tags] == ["linux"]
    assert os_tags[0].confidence < 0.8


# ── roles from services ──────────────────────────────────────────────────────

def test_service_roles():
    facts = AssetFacts(ip="10.0.0.9", services=(
        _svc(443, "https"), _svc(5432, "postgresql"), _svc(25, "smtp"),
        _svc(53, "domain"), _svc(3389, "ms-wbt-server"), _svc(2049, "nfs"),
        _svc(6443), _svc(502), _svc(5060, "sip"),
    ))
    tags = _tags(facts)
    for role in ("web", "database", "mail", "dns", "remote_access", "file_share",
                 "container_platform", "ics", "voip"):
        assert f"role:{role}" in tags, role


def test_service_name_matches_on_nonstandard_port():
    assert "role:database" in _tags(AssetFacts(ip="10.0.0.9",
                                               services=(_svc(15432, "postgresql"),)))


def test_domain_controller_from_classifier_detail():
    assert "role:domain_controller" in _tags(
        AssetFacts(ip="10.0.0.5", role_detail="domain_controller"))


def test_domain_controller_from_kerberos_ldap_smb_triad():
    tags = _tags(AssetFacts(ip="10.0.0.5", services=(
        _svc(88, "kerberos-sec"), _svc(389, "ldap"), _svc(445, "microsoft-ds"))))
    assert {"role:domain_controller", "role:directory"} <= tags


def test_kerberos_alone_is_not_a_domain_controller():
    assert "role:domain_controller" not in _tags(
        AssetFacts(ip="10.0.0.5", services=(_svc(88, "kerberos-sec"),)))


# ── exposure / zone / domain ─────────────────────────────────────────────────

def test_external_service_exposure_marks_internet_facing():
    tags = _tags(AssetFacts(ip="10.0.0.5", services=(_svc(443, "https", exposure="external"),)))
    assert "exposure:internet_facing" in tags


def test_all_internal_exposure_marks_internal_only():
    tags = _tags(AssetFacts(ip="10.0.0.5", services=(
        _svc(443, "https", exposure="internal_only"), _svc(22, "ssh", exposure="not_exposed"))))
    assert "exposure:internal_only" in tags
    assert "exposure:internet_facing" not in tags


def test_public_ip_is_internet_facing():
    assert "exposure:internet_facing" in _tags(AssetFacts(ip="34.120.10.5"))


def test_ipv6_zone_is_a_64():
    assert "zone:2001:db8:1:2::/64" in _tags(AssetFacts(ip="2001:db8:1:2::10"))


def test_domain_from_fqdn():
    assert "domain:corp.bank.local" in _tags(AssetFacts(ip="10.0.0.5", fqdn="dc01.corp.bank.local"))
    assert "domain:example.co.in" in _tags(AssetFacts(ip="10.0.0.5", hostname="www.example.co.in"))


def test_single_label_hostname_has_no_domain():
    assert not any(t.startswith("domain:") for t in _tags(AssetFacts(ip="10.0.0.5", hostname="dc01")))


def test_malformed_ip_does_not_crash():
    assert _tags(AssetFacts(ip="not-an-ip")) == set()


# ── BFSI sector signatures ───────────────────────────────────────────────────

def test_core_banking_banner_is_high_confidence():
    tags = derive_tags(AssetFacts(ip="10.1.0.5", services=(
        _svc(8443, "https", product="Infosys Finacle Core Banking"),)))
    core = [t for t in tags if (t.key, t.value) == ("sector_fn", "core_banking")]
    assert core and core[0].confidence >= 0.8
    names = {f"{t.key}:{t.value}" for t in tags}
    assert "compliance_scope:critical_financial_system" in names
    assert "data_sensitivity:restricted" in names


def test_swift_port_is_heuristic_and_scopes_cscf():
    tags = derive_tags(AssetFacts(ip="10.1.0.6", services=(_svc(48002),)))
    swift = [t for t in tags if (t.key, t.value) == ("sector_fn", "swift")]
    assert swift and swift[0].confidence <= 0.6
    assert "compliance_scope:swift_cscf_scope" in {f"{t.key}:{t.value}" for t in tags}


def test_hsm_banner_scopes_pci():
    tags = _tags(AssetFacts(ip="10.1.0.7", services=(_svc(1500, banner="Thales payShield 10K"),)))
    assert {"sector_fn:hsm", "compliance_scope:pci_cde_candidate",
            "data_sensitivity:restricted"} <= tags


def test_payment_hostname_is_low_confidence():
    tags = derive_tags(AssetFacts(ip="10.1.0.8", hostname="upi-switch-01"))
    pay = [t for t in tags if (t.key, t.value) == ("sector_fn", "payments")]
    assert pay and pay[0].confidence <= 0.5


def test_generic_hostname_words_do_not_trigger_sector():
    assert not any(t.startswith("sector_fn:")
                   for t in _tags(AssetFacts(ip="10.1.0.8", hostname="core-switch-01")))


def test_fix_protocol_banner_is_trading():
    assert "sector_fn:trading" in _tags(AssetFacts(ip="10.1.0.9", services=(
        _svc(9876, banner="8=FIX.4.4|9=65|35=A"),)))


def test_database_is_confidential_without_sector():
    tags = _tags(AssetFacts(ip="10.0.0.9", services=(_svc(3306, "mysql"),)))
    assert "data_sensitivity:confidential" in tags
    assert "data_sensitivity:restricted" not in tags


# ── dedupe + merge ───────────────────────────────────────────────────────────

def test_duplicate_tags_keep_highest_confidence():
    tags = derive_tags(AssetFacts(ip="10.0.0.5", os="Ubuntu 22.04", services=(
        _svc(22, "ssh", banner="SSH-2.0-OpenSSH_8.9p1 Ubuntu"),)))
    linux = [t for t in tags if (t.key, t.value) == ("os_family", "linux")]
    assert len(linux) == 1 and linux[0].rule == "os.string"


def test_merge_replaces_auto_and_keeps_manual():
    existing = {"v": 1,
                "auto": [{"key": "role", "value": "web", "source": "auto"}],
                "manual": [{"key": "owner_team", "value": "payments", "source": "manual"}]}
    auto = derive_tags(AssetFacts(ip="10.0.0.9", services=(_svc(3306, "mysql"),)))
    merged = merge_tags(existing, auto)
    assert merged["v"] == 1
    assert merged["manual"] == existing["manual"]
    assert {"key": "role", "value": "web", "source": "auto"} not in merged["auto"]
    assert any(t["value"] == "database" for t in merged["auto"])


def test_merge_tolerates_legacy_or_missing_tags():
    auto = derive_tags(AssetFacts(ip="10.0.0.9"))
    assert merge_tags(None, auto)["manual"] == []
    assert merge_tags({"env": "prod"}, auto)["manual"] == []  # legacy free-form dict


def test_tag_strings_include_manual():
    merged = merge_tags({"manual": [{"key": "owner_team", "value": "cards"}]},
                        derive_tags(AssetFacts(ip="10.0.0.9")))
    assert set(tag_strings(merged)) == {"zone:10.0.0.0/24", "owner_team:cards"}
