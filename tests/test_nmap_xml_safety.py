"""
test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injection.

CWE-611 (XXE) / CWE-776 (entity expansion). nmap's own output never declares an
<!ENTITY>, so refusing any entity declaration is a zero-false-positive guard that
blocks a malicious/targeted payload from ever reaching the expat parser.
"""
from __future__ import annotations

import pytest

from scanner import nmap_wrapper as nw

# A well-formed nmap run: DOCTYPE present (as real nmap emits), NO entity decl.
_CLEAN = (
    '<?xml version="1.0"?><!DOCTYPE nmaprun>'
    '<nmaprun scanner="nmap"><runstats>'
    '<finished exit="success"/></runstats></nmaprun>'
)
# Same shell, but with an internal entity definition (billion-laughs seed / XXE).
_ENTITY = (
    '<?xml version="1.0"?><!DOCTYPE nmaprun [<!ENTITY x "boom">]>'
    '<nmaprun scanner="nmap"><host>&x;</host></nmaprun>'
)


class TestNmapEntityGuard:
    def test_entity_declaration_is_refused(self):
        with pytest.raises(nw.NmapExecutionError) as ei:
            nw._parse_nmap_xml(_ENTITY, "quick")
        assert ei.value.code == "unsafe_xml"

    def test_entity_guard_is_case_insensitive(self):
        payload = _ENTITY.replace("<!ENTITY", "<!eNtItY")
        with pytest.raises(nw.NmapExecutionError):
            nw._parse_nmap_xml(payload, "quick")

    def test_legitimate_doctype_output_still_parses(self):
        # A real nmap DOCTYPE must NOT be mistaken for an attack.
        assert nw._parse_nmap_xml(_CLEAN, "quick") == []
