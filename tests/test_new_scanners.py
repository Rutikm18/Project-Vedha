"""
test_new_scanners.py — unit tests for the five new/enhanced scanner modules.

Tests are network-free: all probes that require sockets are tested only for
their packet construction, response parsing, and data-model logic.
No network connections are made; scanners are not instantiated.
"""

from __future__ import annotations

import json
import os
import struct
import tempfile
from pathlib import Path

import pytest


# ══════════════════════════════════════════════════════════════════════════════
# SNMP scanner — BER utilities, PDU builders, response parsing
# ══════════════════════════════════════════════════════════════════════════════

class TestSNMPBerUtilities:
    from scanner.snmp_scanner import (
        _encode_oid, _decode_oid, _ber_len, _ber_parse, _decode_value,
        _build_get, _build_getnext, _build_getbulk_v2c, _SYSDESCR_OID,
    )

    def test_encode_sysdescr_oid(self):
        from scanner.snmp_scanner import _encode_oid
        enc = _encode_oid("1.3.6.1.2.1.1.1.0")
        assert enc == b"\x2b\x06\x01\x02\x01\x01\x01\x00"

    def test_oid_roundtrip_sysdescr(self):
        from scanner.snmp_scanner import _encode_oid, _decode_oid
        for oid in ["1.3.6.1.2.1.1.1.0", "1.3.6.1.2.1.4.22.1.2",
                    "1.3.6.1.2.1.25.4.2.1.2", "1.3.6.1.2.1.2.2.1.2"]:
            assert _decode_oid(_encode_oid(oid)) == oid

    def test_ber_len_short_form(self):
        from scanner.snmp_scanner import _ber_len
        assert _ber_len(0) == b"\x00"
        assert _ber_len(1) == b"\x01"
        assert _ber_len(127) == b"\x7f"

    def test_ber_len_long_form_one_byte(self):
        from scanner.snmp_scanner import _ber_len
        assert _ber_len(128) == b"\x81\x80"
        assert _ber_len(255) == b"\x81\xff"

    def test_ber_len_long_form_two_bytes(self):
        from scanner.snmp_scanner import _ber_len
        assert _ber_len(256) == b"\x82\x01\x00"
        assert _ber_len(512) == b"\x82\x02\x00"

    def test_ber_parse_two_tlvs(self):
        from scanner.snmp_scanner import _ber_parse
        data = b"\x02\x01\x01\x04\x06public"
        tlvs = _ber_parse(data)
        assert len(tlvs) == 2
        assert tlvs[0] == (0x02, b"\x01")   # INTEGER 1
        assert tlvs[1] == (0x04, b"public")  # OCTET STRING

    def test_ber_parse_empty(self):
        from scanner.snmp_scanner import _ber_parse
        assert _ber_parse(b"") == []

    def test_decode_value_ip_address(self):
        from scanner.snmp_scanner import _decode_value
        assert _decode_value(0x40, b"\xc0\xa8\x01\x01") == "192.168.1.1"
        assert _decode_value(0x40, b"\x0a\x00\x00\x01") == "10.0.0.1"

    def test_decode_value_counter32(self):
        from scanner.snmp_scanner import _decode_value
        assert _decode_value(0x41, b"\x00\x01\x00\x00") == "65536"

    def test_decode_value_timeticks(self):
        from scanner.snmp_scanner import _decode_value
        assert _decode_value(0x43, b"\x00\x00\x27\x10") == "10000"

    def test_decode_value_end_of_mib_view(self):
        from scanner.snmp_scanner import _decode_value
        assert _decode_value(0x82, b"") == "endOfMibView"
        assert _decode_value(0x80, b"") == "noSuchObject"
        assert _decode_value(0x81, b"") == "noSuchInstance"

    def test_decode_value_octet_string(self):
        from scanner.snmp_scanner import _decode_value
        assert _decode_value(0x04, b"Linux router") == "Linux router"

    def test_get_pdu_outer_tag(self):
        from scanner.snmp_scanner import _build_get, _SYSDESCR_OID
        pkt = _build_get("public", _SYSDESCR_OID)
        assert pkt[0] == 0x30   # outer SEQUENCE
        assert 0xa0 in pkt      # GET-request PDU tag

    def test_getnext_pdu_tag(self):
        from scanner.snmp_scanner import _build_getnext, _SYSDESCR_OID
        pkt = _build_getnext("public", _SYSDESCR_OID)
        assert 0xa1 in pkt      # GetNextRequest PDU

    def test_getbulk_pdu_tag_and_version(self):
        from scanner.snmp_scanner import _build_getbulk_v2c, _SYSDESCR_OID
        pkt = _build_getbulk_v2c("public", _SYSDESCR_OID)
        assert 0xa5 in pkt             # GetBulkRequest PDU
        assert b"\x02\x01\x01" in pkt  # version = v2c (INTEGER 1)

    def test_oid_in_subtree(self):
        from scanner.snmp_scanner import _oid_in_subtree
        assert _oid_in_subtree("1.3.6.1.2.1.1.1.0", "1.3.6.1.2.1.1.1") is True
        assert _oid_in_subtree("1.3.6.1.2.1.2.2.1.2.1", "1.3.6.1.2.1.2.2.1.2") is True
        assert _oid_in_subtree("1.3.6.1.2.1.4.0", "1.3.6.1.2.1.1.1") is False
        assert _oid_in_subtree("1.3.6.1.2.1.1.1", "1.3.6.1.2.1.1.1") is False  # same prefix, not child


# ══════════════════════════════════════════════════════════════════════════════
# UDP scanner — probe construction and response interpretation
# ══════════════════════════════════════════════════════════════════════════════

class TestUDPProbeConstruction:

    def test_ike_probe_length_field_matches_actual(self):
        from scanner.udp_scanner import _ike_probe
        pkt = _ike_probe()
        length_field = struct.unpack("!I", pkt[24:28])[0]
        assert length_field == len(pkt)

    def test_ike_probe_header_fields(self):
        from scanner.udp_scanner import _ike_probe
        pkt = _ike_probe()
        assert pkt[16] == 33   # Next Payload = SA
        assert pkt[17] == 0x20  # IKEv2 version
        assert pkt[18] == 34   # IKE_SA_INIT
        assert pkt[19] == 0x08  # initiator flag

    def test_ike_probe_init_spi_not_zero(self):
        from scanner.udp_scanner import _ike_probe
        pkt = _ike_probe()
        assert pkt[:8] != b"\x00" * 8   # initiator SPI must not be zero

    def test_ike_probe_resp_spi_zero(self):
        from scanner.udp_scanner import _ike_probe
        pkt = _ike_probe()
        assert pkt[8:16] == b"\x00" * 8  # responder SPI = zeros (initiation)

    def test_interpret_ike_v2(self):
        from scanner.udp_scanner import interpret_ike
        hdr = bytearray(28)
        hdr[17] = 0x20   # IKEv2 version byte
        hdr[18] = 34     # IKE_SA_INIT
        result = interpret_ike(bytes(hdr))
        assert result["version"] == "IKEv2.0"

    def test_interpret_ike_v1(self):
        from scanner.udp_scanner import interpret_ike
        hdr = bytearray(28)
        hdr[17] = 0x10   # IKEv1
        result = interpret_ike(bytes(hdr))
        assert result["version"] == "IKEv1.0"

    def test_interpret_ike_short_data(self):
        from scanner.udp_scanner import interpret_ike
        assert interpret_ike(b"short")["version"] == "unknown"

    def test_sip_probe_starts_with_options(self):
        from scanner.udp_scanner import _sip_probe
        pkt = _sip_probe("192.168.1.100")
        text = pkt.decode()
        assert text.startswith("OPTIONS sip:")
        assert "CSeq: 1 OPTIONS" in text
        assert "Content-Length: 0" in text

    def test_sip_probe_target_in_headers(self):
        from scanner.udp_scanner import _sip_probe
        text = _sip_probe("10.0.0.50").decode()
        assert "10.0.0.50" in text

    def test_interpret_sip_parses_server(self):
        from scanner.udp_scanner import interpret_sip
        resp = b"SIP/2.0 200 OK\r\nServer: Asterisk PBX\r\nContent-Length: 0\r\n\r\n"
        info = interpret_sip(resp)
        assert info["server"] == "Asterisk PBX"
        assert "200" in info["sip_response"]

    def test_tftp_probe_opcode_rrq(self):
        from scanner.udp_scanner import _tftp_probe
        pkt = _tftp_probe()
        assert struct.unpack(">H", pkt[:2])[0] == 1  # opcode 1 = RRQ
        assert b"octet" in pkt

    def test_ipmi_probe_length_and_version(self):
        from scanner.udp_scanner import _ipmi_probe
        pkt = _ipmi_probe()
        assert len(pkt) == 12
        assert pkt[0] == 0x06    # RMCP version
        assert pkt[3] == 0x06    # ASF class

    def test_ipmi_probe_iana_enterprise(self):
        from scanner.udp_scanner import _ipmi_probe
        pkt = _ipmi_probe()
        iana = struct.unpack("!I", pkt[4:8])[0]
        assert iana == 0x000011BE  # ASF/IPMI IANA number

    def test_ipmi_probe_presence_ping_type(self):
        from scanner.udp_scanner import _ipmi_probe
        assert _ipmi_probe()[8] == 0x80  # Presence Ping message type

    def test_interpret_ipmi_supported_flag(self):
        from scanner.udp_scanner import interpret_ipmi
        pong = bytearray(12)
        pong[10] = 0x20   # bit 5 = IPMI supported
        result = interpret_ipmi(bytes(pong))
        assert result["ipmi_supported"] is True
        assert result["rmcp_pong"] is True

    def test_interpret_ipmi_not_supported(self):
        from scanner.udp_scanner import interpret_ipmi
        pong = bytearray(12)
        pong[10] = 0x10   # bit 4 only, not IPMI
        result = interpret_ipmi(bytes(pong))
        assert result["ipmi_supported"] is False

    def test_ntp_monlist_mode7_detection(self):
        from scanner.udp_scanner import interpret_ntp_monlist
        # 0x97 = 1001 0111: MSB set (response), low 3 bits = 7 (mode 7)
        assert interpret_ntp_monlist(bytes([0x97])) is True
        assert interpret_ntp_monlist(b"") is False

    def test_memcached_unauth_stat(self):
        from scanner.udp_scanner import interpret_memcached_stats
        assert interpret_memcached_stats(b"STAT pid 12345\r\n") is True
        assert interpret_memcached_stats(b"ERROR\r\n") is False

    def test_udp_probes_has_all_playbook_ports(self):
        from scanner.udp_scanner import UDP_PROBES
        required = {53, 69, 123, 137, 161, 500, 623, 1900, 4500, 5060, 5353, 11211}
        missing = required - set(UDP_PROBES)
        assert not missing, f"Missing ports: {missing}"


# ══════════════════════════════════════════════════════════════════════════════
# IoT scanner — protocol construction and response parsing
# ══════════════════════════════════════════════════════════════════════════════

class TestIoTScanner:

    def test_ssdp_header_parsing_location(self):
        from scanner.iot_scanner import _parse_ssdp_headers
        resp = (b"HTTP/1.1 200 OK\r\n"
                b"LOCATION: http://192.168.1.1:49152/rootDesc.xml\r\n"
                b"SERVER: Linux UPnP/1.0\r\nST: ssdp:all\r\n\r\n")
        headers = _parse_ssdp_headers(resp)
        assert headers["location"] == "http://192.168.1.1:49152/rootDesc.xml"
        assert "Linux" in headers["server"]
        assert headers["st"] == "ssdp:all"

    def test_mqtt_remaining_length_encoding(self):
        from scanner.iot_scanner import _mqtt_remaining_len
        assert _mqtt_remaining_len(0) == b"\x00"
        assert _mqtt_remaining_len(127) == b"\x7f"
        assert _mqtt_remaining_len(128) == b"\x80\x01"
        assert _mqtt_remaining_len(16383) == b"\xff\x7f"

    def test_mqtt_connect_packet_structure(self):
        from scanner.iot_scanner import _mqtt_connect
        pkt = _mqtt_connect()
        assert pkt[0] == 0x10        # CONNECT packet type
        assert b"MQTT" in pkt        # protocol name
        assert b"vedha-probe" in pkt  # client ID

    def test_mqtt_connect_clean_session_flag(self):
        from scanner.iot_scanner import _mqtt_connect
        pkt = _mqtt_connect()
        # Connect flags byte = 0x02 (clean session)
        assert b"\x04\x02" in pkt   # protocol level 4, connect flags 0x02

    def test_coap_get_wellknown_header(self):
        from scanner.iot_scanner import _coap_get_wellknown_core
        pkt = _coap_get_wellknown_core()
        assert pkt[0] == 0x40   # Ver=1, T=CON, TKL=0
        assert pkt[1] == 0x01   # Code GET

    def test_coap_get_wellknown_path(self):
        from scanner.iot_scanner import _coap_get_wellknown_core
        pkt = _coap_get_wellknown_core()
        assert b".well-known" in pkt
        assert b"core" in pkt

    def test_coap_response_parse_205(self):
        from scanner.iot_scanner import _parse_coap_response
        resp = bytes([0x60, 0x45, 0x00, 0x01]) + b"\xff" + b'</>;rt="core"'
        parsed = _parse_coap_response(resp)
        assert parsed["coap_response_code"] == "2.05"
        assert "core" in parsed["core_resources"]

    def test_coap_response_parse_404(self):
        from scanner.iot_scanner import _parse_coap_response
        resp = bytes([0x60, 0x84, 0x00, 0x01])
        parsed = _parse_coap_response(resp)
        assert parsed["coap_response_code"] == "4.04"

    def test_coap_response_parse_short(self):
        from scanner.iot_scanner import _parse_coap_response
        assert _parse_coap_response(b"ab") == {}


# ══════════════════════════════════════════════════════════════════════════════
# Delta scanner — stable host ID, diff logic, classification
# ══════════════════════════════════════════════════════════════════════════════

def _make_scan_record(**overrides) -> dict:
    base = {
        "scanner": "port_scan", "target": "10.0.0.1",
        "port": 22, "proto": "tcp", "status": "open",
        "data": {}, "evidence": "", "timestamp": "2026-01-01T00:00:00Z",
    }
    base.update(overrides)
    return base


@pytest.fixture
def delta_engine():
    from scanner.delta_scanner import DeltaEngine
    return DeltaEngine()


class TestStableHostId:

    def test_mac_takes_priority(self):
        from scanner.delta_scanner import _stable_host_id
        rec = {"data": {"mac_address": "AA:BB:CC:DD:EE:FF"}, "target": "10.0.0.1"}
        assert _stable_host_id(rec) == "mac:aa:bb:cc:dd:ee:ff"

    def test_mac_normalises_dashes(self):
        from scanner.delta_scanner import _stable_host_id
        rec = {"data": {"mac_address": "AA-BB-CC-DD-EE-FF"}, "target": "10.0.0.1"}
        assert _stable_host_id(rec) == "mac:aa:bb:cc:dd:ee:ff"

    def test_hostname_second_priority(self):
        from scanner.delta_scanner import _stable_host_id
        rec = {"data": {"inventory": {"hostname": "web01"}}, "target": "10.0.0.1"}
        assert _stable_host_id(rec) == "host:web01"

    def test_ip_fallback(self):
        from scanner.delta_scanner import _stable_host_id
        rec = {"data": {}, "target": "10.0.0.5"}
        assert _stable_host_id(rec) == "ip:10.0.0.5"

    def test_zero_mac_skipped(self):
        from scanner.delta_scanner import _stable_host_id
        rec = {"data": {"mac_address": "00:00:00:00:00:00"}, "target": "10.0.0.1"}
        # zero MAC should fall through to IP
        result = _stable_host_id(rec)
        assert not result.startswith("mac:00:00")


class TestVersionChange:

    def test_different_versions(self):
        from scanner.delta_scanner import _significant_version_change
        assert _significant_version_change("1.18.0", "1.19.0") is True

    def test_same_version(self):
        from scanner.delta_scanner import _significant_version_change
        assert _significant_version_change("1.0", "1.0") is False

    def test_empty_old_version(self):
        from scanner.delta_scanner import _significant_version_change
        assert _significant_version_change("", "1.0") is False

    def test_whitespace_normalised(self):
        from scanner.delta_scanner import _significant_version_change
        assert _significant_version_change("nginx  1.18", "nginx  1.18") is False


class TestDeltaEngine:

    def _write_jsonl(self, records: list[dict]) -> str:
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
        for r in records:
            f.write(json.dumps(r) + "\n")
        f.close()
        return f.name

    def test_load_jsonl_basic(self, delta_engine):
        path = self._write_jsonl([_make_scan_record(port=22)])
        try:
            index = delta_engine.load_jsonl(path)
            assert len(index) == 1
        finally:
            os.unlink(path)

    def test_load_jsonl_skips_error_status(self, delta_engine):
        path = self._write_jsonl([
            _make_scan_record(port=22, status="open"),
            _make_scan_record(port=80, status="error"),
        ])
        try:
            index = delta_engine.load_jsonl(path)
            assert len(index) == 1  # error record skipped
        finally:
            os.unlink(path)

    def test_load_jsonl_missing_file(self, delta_engine):
        with pytest.raises(FileNotFoundError):
            delta_engine.load_jsonl("/nonexistent/path.jsonl")

    def test_diff_detects_new_service(self, delta_engine):
        base_path = self._write_jsonl([_make_scan_record(port=22)])
        curr_path = self._write_jsonl([
            _make_scan_record(port=22),
            _make_scan_record(port=80),
        ])
        try:
            base = delta_engine.load_jsonl(base_path)
            curr = delta_engine.load_jsonl(curr_path)
            deltas = delta_engine.diff(base, curr)
            new_svc = [d for d in deltas if d.kind == "new_service" and d.port == 80]
            assert new_svc, f"Expected new_service for port 80, got: {deltas}"
        finally:
            os.unlink(base_path)
            os.unlink(curr_path)

    def test_diff_detects_service_gone(self, delta_engine):
        base_path = self._write_jsonl([
            _make_scan_record(port=22),
            _make_scan_record(port=23),  # telnet disappears
        ])
        curr_path = self._write_jsonl([_make_scan_record(port=22)])
        try:
            base = delta_engine.load_jsonl(base_path)
            curr = delta_engine.load_jsonl(curr_path)
            deltas = delta_engine.diff(base, curr)
            gone = [d for d in deltas if d.kind == "service_gone" and d.port == 23]
            assert gone, f"Expected service_gone for port 23, got: {deltas}"
        finally:
            os.unlink(base_path)
            os.unlink(curr_path)

    def test_diff_detects_state_change_to_open(self, delta_engine):
        base_path = self._write_jsonl([_make_scan_record(port=3389, status="filtered")])
        curr_path = self._write_jsonl([_make_scan_record(port=3389, status="open")])
        try:
            base = delta_engine.load_jsonl(base_path)
            curr = delta_engine.load_jsonl(curr_path)
            deltas = delta_engine.diff(base, curr)
            sc = [d for d in deltas if d.kind == "state_change"]
            assert sc and sc[0].severity_hint == "high"
        finally:
            os.unlink(base_path)
            os.unlink(curr_path)

    def test_diff_no_change_produces_no_service_delta(self, delta_engine):
        base_path = self._write_jsonl([_make_scan_record(port=22)])
        curr_path = self._write_jsonl([_make_scan_record(port=22)])
        try:
            base = delta_engine.load_jsonl(base_path)
            curr = delta_engine.load_jsonl(curr_path)
            deltas = delta_engine.diff(base, curr)
            service_deltas = [d for d in deltas
                              if d.kind in ("new_service", "service_gone", "version_change")]
            assert not service_deltas, f"Expected no service changes: {deltas}"
        finally:
            os.unlink(base_path)
            os.unlink(curr_path)

    def test_diff_high_severity_port_heuristic(self, delta_engine):
        # Port 3306 (MySQL) appearing is a high-severity finding
        base_path = self._write_jsonl([])
        curr_path = self._write_jsonl([_make_scan_record(port=3306, status="open")])
        try:
            base = delta_engine.load_jsonl(base_path)
            curr = delta_engine.load_jsonl(curr_path)
            deltas = delta_engine.diff(base, curr)
            new = [d for d in deltas if d.kind == "new_service"]
            assert new and new[0].severity_hint == "high"
        finally:
            os.unlink(base_path)
            os.unlink(curr_path)

    def test_summary_counts(self, delta_engine):
        base_path = self._write_jsonl([_make_scan_record(port=22)])
        curr_path = self._write_jsonl([
            _make_scan_record(port=22),
            _make_scan_record(port=80),
        ])
        try:
            base = delta_engine.load_jsonl(base_path)
            curr = delta_engine.load_jsonl(curr_path)
            deltas = delta_engine.diff(base, curr)
            summary = delta_engine.summary(deltas)
            assert summary["total"] >= 1
            assert "new_service" in summary["by_kind"]
        finally:
            os.unlink(base_path)
            os.unlink(curr_path)

    def test_load_jsonl_skips_invalid_json(self, delta_engine):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
        f.write("not json\n")
        f.write(json.dumps(_make_scan_record(port=22)) + "\n")
        f.close()
        try:
            index = delta_engine.load_jsonl(f.name)
            assert len(index) == 1  # invalid line skipped
        finally:
            os.unlink(f.name)


# ══════════════════════════════════════════════════════════════════════════════
# Mobile scanner — ADB message construction and parsing
# ══════════════════════════════════════════════════════════════════════════════

class TestMobileScanner:

    def test_adb_cnxn_command_field(self):
        from scanner.mobile_scanner import _build_adb_cnxn, A_CNXN
        cnxn = _build_adb_cnxn()
        cmd = struct.unpack("<I", cnxn[:4])[0]
        assert cmd == A_CNXN

    def test_adb_cnxn_magic_invariant(self):
        from scanner.mobile_scanner import _build_adb_cnxn, A_CNXN
        cnxn = _build_adb_cnxn()
        _, _, _, _, _, magic = struct.unpack("<IIIIII", cnxn[:24])
        assert magic == (A_CNXN ^ 0xFFFFFFFF)

    def test_adb_cnxn_checksum_matches(self):
        from scanner.mobile_scanner import _build_adb_cnxn, _adb_checksum
        cnxn = _build_adb_cnxn()
        _, _, _, dlen, csum, _ = struct.unpack("<IIIIII", cnxn[:24])
        data = cnxn[24:]
        assert _adb_checksum(data) == csum

    def test_parse_adb_header_cnxn(self):
        from scanner.mobile_scanner import _parse_adb_header, A_CNXN
        hdr = struct.pack("<IIIIII",
            A_CNXN, 0x01000000, 256 * 1024, 0, 0, A_CNXN ^ 0xFFFFFFFF)
        parsed = _parse_adb_header(hdr)
        assert parsed is not None
        assert parsed["command"] == "CNXN"
        assert parsed["arg0"] == 0x01000000

    def test_parse_adb_header_auth(self):
        from scanner.mobile_scanner import _parse_adb_header, A_AUTH
        hdr = struct.pack("<IIIIII", A_AUTH, 1, 0, 0, 0, A_AUTH ^ 0xFFFFFFFF)
        parsed = _parse_adb_header(hdr)
        assert parsed is not None
        assert parsed["command"] == "AUTH"

    def test_parse_adb_header_invalid_magic(self):
        from scanner.mobile_scanner import _parse_adb_header, A_CNXN
        bad = struct.pack("<IIIIII", A_CNXN, 0, 0, 0, 0, 0xDEADBEEF)
        assert _parse_adb_header(bad) is None

    def test_parse_adb_header_too_short(self):
        from scanner.mobile_scanner import _parse_adb_header
        assert _parse_adb_header(b"too short") is None

    def test_mdns_query_transaction_id_zero(self):
        from scanner.mobile_scanner import _build_mdns_query
        q = _build_mdns_query("_airdrop._tcp.local")
        assert q[:2] == b"\x00\x00"

    def test_mdns_query_one_question(self):
        from scanner.mobile_scanner import _build_mdns_query
        q = _build_mdns_query("_airdrop._tcp.local")
        assert q[4:6] == b"\x00\x01"  # QDCOUNT = 1

    def test_mdns_query_contains_service_labels(self):
        from scanner.mobile_scanner import _build_mdns_query
        q = _build_mdns_query("_airdrop._tcp.local")
        assert b"_airdrop" in q
        assert b"_tcp" in q
        assert b"local" in q

    def test_mdns_query_googlecast(self):
        from scanner.mobile_scanner import _build_mdns_query
        q = _build_mdns_query("_googlecast._tcp.local")
        assert b"_googlecast" in q

    def test_adb_checksum_empty(self):
        from scanner.mobile_scanner import _adb_checksum
        assert _adb_checksum(b"") == 0

    def test_adb_checksum_known_value(self):
        from scanner.mobile_scanner import _adb_checksum
        # sum of b"AB" = 65 + 66 = 131
        assert _adb_checksum(b"AB") == 131
