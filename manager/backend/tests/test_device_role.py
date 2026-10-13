"""M10 — one dominant role with a confidence; only a high-confidence role drives anything."""
from __future__ import annotations

from app.detection import attack_paths
from app.intel.device_role import HIGH_CONFIDENCE, drives_amplifier, resolve_role
from app.intel.tagging import AssetFacts, ServiceFact, derive_tags


def test_linux_server_with_router_ports_is_not_network_gear():
    v = resolve_role("network_device", 0.9, "Ubuntu 22.04.3 LTS")
    assert v.role == "server" and not v.high_confidence and v.downgraded_from == "network_device"


def test_dedicated_os_corroborates_the_claim():
    v = resolve_role("network_device", 0.6, "Cisco IOS XE 17.3")
    assert v.role == "network_device" and v.confidence >= 0.85 and v.high_confidence


def test_unrated_and_ambiguous_claims_do_not_clear_the_bar():
    assert not resolve_role("printer", 0.5, None).high_confidence      # tie-capped classifier
    assert resolve_role("printer", 0.8, None).high_confidence
    assert resolve_role(None, None, "Linux").role is None


def test_host_type_tag_only_for_high_confidence():
    base = dict(os="Ubuntu 22.04", services=(ServiceFact(port=179, service_name="bgp"),))
    weak = derive_tags(AssetFacts(device_role="network_device", role_confidence=0.9, **base))
    keys = {(t.key, t.value) for t in weak}
    assert ("host_type", "network") not in keys
    assert ("host_type_candidate", "server") in keys                    # visible, but not driving
    ok = derive_tags(AssetFacts(device_role="network_device", role_confidence=0.9, os="Cisco IOS"))
    assert ("host_type", "network") in {(t.key, t.value) for t in ok}


def test_legacy_role_without_confidence_still_amplifies():
    assert drives_amplifier("network_device", None, None) is True
    assert drives_amplifier("network_device", 0.4, None) is False
    assert drives_amplifier("network_device", 0.95, "Debian GNU/Linux 12") is False
    assert drives_amplifier(None, 0.99, None) is False
    assert HIGH_CONFIDENCE == 0.7


def _snmp_fact(ip):
    return {"scanner": "snmp_scan", "target": ip, "port": 161, "status": "open",
            "data": {"community": "public"}}


def test_attack_path_amplifier_ignores_an_untrusted_network_role():
    facts = [_snmp_fact("10.0.0.5")]
    trusted = attack_paths.attack_path_findings(
        facts, {"10.0.0.5": {"device_role": "network_device", "role_confidence": 0.9, "os": "Cisco IOS"}})
    untrusted = attack_paths.attack_path_findings(
        facts, {"10.0.0.5": {"device_role": "network_device", "role_confidence": 0.9, "os": "Ubuntu 22.04"}})
    legacy = attack_paths.attack_path_findings(facts, {"10.0.0.5": {"device_role": "network_device"}})
    sev = lambda out: [str(f["severity"]) for f in out]                 # noqa: E731
    assert sev(trusted) == sev(legacy)                                  # same as before for trusted/legacy
    assert sev(untrusted) != sev(trusted)                               # contradicted role no longer amplifies
