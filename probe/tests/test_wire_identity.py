"""
test_wire_identity.py — the scanner must NOT sign its own packets.

A brand string on the wire (User-Agent, ICMP/UDP payload, client id) lets a blue
team grep one log line, attribute the whole engagement, and one-line-block the tool.
These assert the default identity is generic and env-overridable, and that the
import-time probe constants carry no tool signature.
"""
from __future__ import annotations

from scanner import scanner_base as sb

# Case-insensitive substrings that would attribute traffic to this tool.
_BRANDS = ("vedha", "va-scanner")


class TestUserAgent:
    def test_default_is_generic_browser_no_brand(self):
        ua = sb.user_agent().lower()
        assert "mozilla" in ua
        assert not any(b in ua for b in _BRANDS)

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("VEDHA_SCAN_UA", "curl/8.0")
        assert sb.user_agent() == "curl/8.0"


class TestProbePayload:
    def test_default_carries_no_brand(self):
        payload = sb.probe_payload().lower()
        assert not any(b.encode() in payload for b in _BRANDS)

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("VEDHA_SCAN_PAYLOAD", "xyz")
        assert sb.probe_payload() == b"xyz"


class TestChooseSourcePort:
    """Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs."""

    def test_uses_configured_valid_port(self):
        assert sb.choose_source_port(53) == 53
        assert sb.choose_source_port(88) == 88

    def test_none_gives_random_ephemeral(self):
        assert 40000 <= sb.choose_source_port(None) <= 60000

    def test_out_of_range_falls_back_to_random(self):
        assert 40000 <= sb.choose_source_port(0) <= 60000
        assert 40000 <= sb.choose_source_port(99999) <= 60000

    def test_boundary_ports_are_valid(self):
        assert sb.choose_source_port(1) == 1
        assert sb.choose_source_port(65535) == 65535


class TestModuleConstantsUnbranded:
    """Import-time probe constants built from user_agent() must be signature-free."""

    def test_service_banner_http_probe(self):
        from scanner import service_banner as sbn
        assert not any(b.encode() in sbn._HTTP_PROBE.lower() for b in _BRANDS)

    def test_iot_rtsp_options(self):
        from scanner import iot_scanner as iot
        assert not any(b.encode() in iot._RTSP_OPTIONS.lower() for b in _BRANDS)
