"""CVE finding text: what a client reads first on a version-matched CVE."""
from __future__ import annotations

from types import SimpleNamespace

from app.detection.cve_text import (
    cve_description, cve_remediation, is_engine_notes_description, product_name,
)
from app.services.remediation_kb import classify_finding

_BANNER = {
    "cve_id": "CVE-2024-6387", "cpe": "cpe:2.3:a:openbsd:openssh:9.6p1:*:*:*:*:*:*:*",
    "product": "openssh", "matched_version": "9.6p1", "port": 22, "ports": [22],
    "proto": "tcp", "source_confidence": "inferred", "version_scheme": "upstream",
    "fixed_version": "9.8p1", "fixed_version_raw": "1:9.8p1-1",
    "matched_range": "[1:8.5p1-1, 1:9.8p1-1)", "asset_ip": "10.0.0.5",
}


def test_banner_cve_description_names_product_port_and_backport_caveat():
    text = cve_description(_BANNER)
    assert text.startswith("OpenSSH 9.6p1 was observed on port 22/tcp (from the service banner)")
    assert "CVE-2024-6387" in text and "backported" in text
    assert "not recorded" not in text


def test_banner_cve_remediation_names_the_upstream_fix_and_the_port():
    text = cve_remediation(_BANNER)
    assert "Upgrade OpenSSH to 9.8p1 or later" in text
    assert "1:9.8p1-1" not in text                      # never the raw Debian bound
    assert "restrict access to port 22/tcp" in text


def test_package_scheme_remediation_names_the_package_version():
    d = {**_BANNER, "version_scheme": "package", "fixed_version": "1:9.2p1-2+deb12u3",
         "matched_version": "9.2p1"}
    text = cve_remediation(d)
    assert "brings the OpenSSH package to 1:9.2p1-2+deb12u3" in text
    assert "backported" not in cve_description(d)


def test_no_fix_recorded_points_to_the_advisory_and_keeps_no_placeholder():
    d = {**_BANNER, "fixed_version": None, "port": None, "ports": []}
    text = cve_remediation(d)
    assert "No upstream release that fixes CVE-2024-6387" in text
    assert "restrict access" not in text and "not recorded" not in text
    assert "port" not in cve_description(d).split("(")[0]


def test_several_ports_are_listed():
    d = {**_BANNER, "ports": [21, 2121], "port": 21, "product": "vsftpd"}
    assert "on ports 21/tcp, 2121/tcp" in cve_description(d)


def test_hostile_values_cannot_write_the_prose():
    d = {**_BANNER, "product": "x<script>alert(1)</script>",
         "matched_version": "9.6p1\n<img src=x>", "cve_id": "CVE-2024-6387<b>"}
    text = cve_description(d) + cve_remediation(d)
    assert "<" not in text and ">" not in text and "\n" not in text
    assert "this vulnerability" in text                 # bad CVE id is not echoed


def test_product_name_falls_back_to_cpe():
    assert product_name({"cpe": "cpe:2.3:a:apache:http_server:2.4.41:*:*:*:*:*:*:*"}) \
        == "Apache HTTP Server"
    assert product_name({}) == "The affected product"


def test_only_old_engine_notes_count_as_replaceable():
    assert is_engine_notes_description(
        "service banner: openssh 9.6p1 | matched range [0, unbounded); version-inferred")
    assert not is_engine_notes_description("Patched by ops on 3 Oct, see ticket 42")
    assert not is_engine_notes_description(None)


def test_version_matched_cve_is_a_missing_patch_whatever_its_title_says():
    f = SimpleNamespace(title="CVE-2024-6387 — openssh", cve_ids=["CVE-2024-6387"],
                        description=cve_description(_BANNER),
                        remediation=cve_remediation({**_BANNER, "port": 3389, "ports": [3389]}),
                        evidence=_BANNER)
    assert classify_finding(f) == "missing_patch"
    # A posture finding keeps its keyword class.
    p = SimpleNamespace(title="OpenSSH weak ciphers offered", cve_ids=None,
                        description="", remediation="", evidence={"rule_id": "POSTURE-SSH-X"})
    assert classify_finding(p) == "outdated_ssh"


def test_ssvc_decision_is_named_in_the_description():
    d = {**_BANNER, "ssvc": {"decision": "Track*", "exploitation": "poc",
                             "automatable": "no", "technical_impact": "total"}}
    assert ("CISA SSVC: Track* (exploitation poc, automatable no, technical impact total)."
            in cve_description(d))


def test_unknown_ssvc_decision_is_not_echoed():
    d = {**_BANNER, "ssvc": {"decision": "<b>Now</b>", "exploitation": "poc"}}
    assert "SSVC" not in cve_description(d)
