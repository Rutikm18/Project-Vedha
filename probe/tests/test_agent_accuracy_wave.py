"""Agent-side items of the 2026-10-10 accuracy plan (A1-A6): collection that used to be
silently skipped, each proven against the real code path (and, for SNMPv3 and FTP write,
against a protocol-level peer rather than a mock of our own parser)."""
from __future__ import annotations

import asyncio
import socket
import threading

import pytest

import workflow.workflow_engine as we
from scanner.ftp_scanner import FTPScanner
from scanner.scanner_base import ScanResult, ScopeGuard
from scanner import snmp_scanner as snmp
from scanner.udp_scanner import UDP_PROBES
from workflow import gates
from workflow.asset import Asset, PortFact
from workflow.branches import BRANCH_BY_NAME
from workflow.router import looks_like_tls, route_branches
from datetime import datetime, timezone


def _asset(open_ports, services=None):
    now = datetime.now(timezone.utc)
    return Asset(host="10.0.0.1", last_seen_alive=now,
                 open_ports={p: PortFact(proto="tcp", status="open", last_scan_time=now)
                             for p in open_ports},
                 services=services or {})


# ── A1: TLS on any port, driven by what the banner stage observed ────────────

def test_a1_tls_is_routed_by_observed_handshake_not_port_number():
    assert 8444 not in gates.TLS_PORTS and 8445 not in gates.TLS_PORTS
    asset = _asset([8444, 8445], services={8444: {"tls": True, "tls_probed": True},
                                           8445: {"tls": True, "tls_probed": True}})
    routed = route_branches(asset)
    assert routed[8444] >= {"tls"} and routed[8445] >= {"tls"}
    # …and the gate then lets the tls branch run for them although they are not in TLS_PORTS.
    assert gates.gate_5_branch_eligible("tls", asset, "it", None, dynamically_routed=True)


def test_a1_failed_handshake_is_negative_evidence():
    assert looks_like_tls(445, {"tls_probed": True, "banner": None}) is False


# ── A2: IoT / mobile checks are reachable on an IT scan, only when triggered ──

@pytest.mark.parametrize("branch,port", [("iot", 1883), ("iot", 554), ("iot", 7547),
                                         ("mobile", 5555), ("mobile", 62078)])
def test_a2_trigger_port_makes_the_branch_eligible_on_an_it_profile(branch, port):
    assert gates.gate_5_branch_eligible(branch, _asset([port]), "it", None)


def test_a2_without_a_trigger_port_neither_branch_runs():
    asset = _asset([22, 80])
    assert not gates.gate_5_branch_eligible("iot", asset, "it", None)
    assert not gates.gate_5_branch_eligible("mobile", asset, "it", None)


def test_a2_trigger_ports_are_actually_swept():
    for port in gates.IOT_TRIGGER_PORTS | gates.MOBILE_TRIGGER_PORTS:
        assert port in gates.IT_PORTS, port


def test_a2_branches_run_through_the_engine_and_store_facts(monkeypatch):
    calls: list[str] = []

    def fake(cid, port=None, data=None):
        class Scanner:
            def __init__(self, *a, **k): pass
            async def scan_target(self, host):
                calls.append(cid)
                return [ScanResult(scanner=cid, target=host, port=port,
                                   proto="tcp" if port else None, status="open",
                                   data=data if data is not None else {"alive": True})]
        return Scanner

    monkeypatch.setattr(we, "HostDiscoveryScanner", fake("host_discovery"))
    monkeypatch.setattr(we, "PortScanner", fake("port_scan", 1883, {}))
    monkeypatch.setattr(we, "ServiceBannerScanner", fake("service_banner", 1883, {}))
    monkeypatch.setattr(we, "OSFingerprintScanner", fake("os_fingerprint", data={}))
    monkeypatch.setattr(we, "IoTScanner",
                        fake("iot_scan", 1883, {"mqtt_connack": True, "unauthenticated_access": True}))
    assets = asyncio.run(we.run_engagement(["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
                                           service_filter={"iot"}))
    assert "iot_scan" in calls
    assert assets["10.0.0.1"].iot_facts[1883]["unauthenticated_access"] is True


def test_a2_branch_specs_do_not_pass_a_ports_kwarg_the_scanners_cannot_take():
    assert BRANCH_BY_NAME["iot"].kwargs(_asset([1883]), [1883]) == [{}]
    assert BRANCH_BY_NAME["mobile"].kwargs(_asset([5555]), [5555]) == [{}]


# ── A4: an open port nothing identified is said out loud ─────────────────────

def _banner_scanner(port):
    from scanner.service_banner import ServiceBannerScanner
    return ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]), ports=[port],
                                rate=1000, concurrency=4, timeout=1.0)


def _serve_once(payload: bytes | None):
    srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(8)
    port = srv.getsockname()[1]

    def run():
        srv.settimeout(6)
        try:
            while True:
                c, _ = srv.accept()
                try:
                    if payload:
                        c.sendall(payload)
                    c.settimeout(0.6)
                    try:
                        c.recv(256)
                    except OSError:
                        pass
                finally:
                    c.close()
        except OSError:
            pass
    threading.Thread(target=run, daemon=True).start()
    return port, srv


def test_a4_silent_listener_is_reported_unidentified():
    port, srv = _serve_once(None)
    try:
        res = asyncio.run(_banner_scanner(port).scan_target("127.0.0.1"))
    finally:
        srv.close()
    assert res and res[0].data["identified"] is False and "raw_hex" in res[0].data


def test_a4_recognised_service_is_identified_and_carries_no_raw_bytes():
    port, srv = _serve_once(b"SSH-2.0-OpenSSH_9.6\r\n")
    try:
        res = asyncio.run(_banner_scanner(port).scan_target("127.0.0.1"))
    finally:
        srv.close()
    assert res[0].data["identified"] is True and "raw_hex" not in res[0].data


# ── A5: structured SSH buckets ───────────────────────────────────────────────

def test_a5_ssh_facts_carry_fail_warn_buckets_per_family():
    from scanner.ssh_scanner import evaluate_algorithms
    out = evaluate_algorithms({
        "kex_algorithms": ["diffie-hellman-group1-sha1", "curve25519-sha256"],
        "server_host_key_algorithms": ["ssh-rsa", "rsa-sha2-512"],
        "encryption_s2c": ["aes128-cbc", "aes256-gcm@openssh.com"], "encryption_c2s": ["arcfour"],
        "mac_s2c": ["hmac-sha1"], "mac_c2s": ["hmac-sha2-256"],
    })
    b = out["buckets"]
    assert set(b) == {"kex", "ciphers", "macs", "host_key"}
    assert "diffie-hellman-group1-sha1" in b["kex"]["fail"]
    assert "arcfour" in b["ciphers"]["fail"] and "hmac-sha1" in b["macs"]["fail"]
    assert "curve25519-sha256" not in b["kex"]["fail"]
    assert "rsa-sha2-512" not in b["host_key"]["fail"] and "ssh-rsa" in b["host_key"]["fail"]


# ── A3: SNMPv3 discovery is well-formed; the noAuth probe parses real replies ─

def test_a3_the_v3_discovery_message_is_well_formed():
    """The hand-written byte string it replaced declared 58 body bytes but held 56, so no real
    agent ever answered it (found by running against a real pysnmp agent)."""
    d = snmp._SNMPv3_DISCOVERY
    assert d[0] == 0x30 and d[1] == len(d) - 2
    outer = snmp._ber_parse(d)
    assert len(outer) == 1 and outer[0][0] == 0x30
    assert [t for t, _ in snmp._ber_parse(outer[0][1])] == [0x02, 0x30, 0x04, 0x30]


def test_a3_noauth_request_round_trips_through_the_report_parser():
    engine = {"engine_id": bytes.fromhex("8000000001020304"), "boots": 5, "time": 100}
    usm = snmp._seq(snmp._octet(engine["engine_id"]) + snmp._int_tlv(5) + snmp._int_tlv(100)
                    + snmp._octet(b"") + snmp._octet(b"") + snmp._octet(b""))
    glob = snmp._seq(snmp._int_tlv(1) + snmp._int_tlv(1500) + snmp._octet(b"\x00") + snmp._int_tlv(3))

    def reply(pdu_tag):
        return snmp._seq(snmp._int_tlv(3) + glob + snmp._octet(usm)
                         + snmp._seq(snmp._octet(engine["engine_id"]) + snmp._octet(b"")
                                     + bytes([pdu_tag, 0])))
    assert snmp.parse_v3_engine(reply(0xA8)) == engine
    assert snmp.classify_v3_reply(reply(0xA2)) == "response"
    assert snmp.classify_v3_reply(reply(0xA8)) == "report"
    assert snmp.classify_v3_reply(b"junk") == "unknown"
    req = snmp.build_v3_noauth_get(engine, "initial")
    assert req[1] == len(req) - 2                      # declared length matches


def test_a3_noauth_probe_distinguishes_a_response_from_a_report(monkeypatch):
    sc = snmp.SNMPScanner(ScopeGuard.from_list(["127.0.0.0/8"]), rate=1000, concurrency=2, timeout=0.5)
    engine = {"engine_id": b"\x80\x00\x00\x01", "boots": 1, "time": 2}
    usm = snmp._seq(snmp._octet(engine["engine_id"]) + snmp._int_tlv(1) + snmp._int_tlv(2)
                    + snmp._octet(b"") + snmp._octet(b"") + snmp._octet(b""))
    glob = snmp._seq(snmp._int_tlv(1) + snmp._int_tlv(1500) + snmp._octet(b"\x00") + snmp._int_tlv(3))

    def msg(tag):
        return snmp._seq(snmp._int_tlv(3) + glob + snmp._octet(usm)
                         + snmp._seq(snmp._octet(engine["engine_id"]) + snmp._octet(b"")
                                     + bytes([tag, 0])))

    def udp(target, payload, recvbuf=8192):
        if payload == snmp._SNMPv3_DISCOVERY:
            return msg(0xA8)
        # answer only for user "admin"
        return msg(0xA2) if b"admin" in payload else msg(0xA8)
    monkeypatch.setattr(sc, "_udp", udp)
    assert sc._snmpv3_noauth_user("127.0.0.1") == (True, "admin")
    monkeypatch.setattr(sc, "_udp", lambda t, p, recvbuf=8192: msg(0xA8))
    assert sc._snmpv3_noauth_user("127.0.0.1") == (True, None)
    monkeypatch.setattr(sc, "_udp", lambda t, p, recvbuf=8192: None)
    assert sc._snmpv3_noauth_user("127.0.0.1") == (False, None)


class _FakeFtp:
    """A tiny FTP server: anonymous login; `writable` decides whether STOR is accepted."""

    def __init__(self, writable: bool, deletable: bool = True):
        self.writable, self.deletable = writable, deletable
        self.files: list[str] = []
        self.srv = socket.socket(); self.srv.bind(("127.0.0.1", 0)); self.srv.listen(4)
        self.port = self.srv.getsockname()[1]
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self):
        self.srv.settimeout(8)
        try:
            c, _ = self.srv.accept()
        except OSError:
            return
        f = c.makefile("rwb", buffering=0)
        pasv = None
        send = lambda s: f.write(s.encode() + b"\r\n")   # noqa: E731
        send("220 fake ftpd")
        while True:
            line = f.readline().decode().strip()
            if not line:
                break
            cmd, _, arg = line.partition(" ")
            if cmd == "USER": send("331 need pass")
            elif cmd == "PASS": send("230 ok")
            elif cmd == "PASV":
                pasv = socket.socket(); pasv.bind(("127.0.0.1", 0)); pasv.listen(1)
                p = pasv.getsockname()[1]
                send(f"227 Entering Passive Mode (127,0,0,1,{p >> 8},{p & 255})")
            elif cmd == "LIST":
                send("150 here"); d, _ = pasv.accept(); d.close(); send("226 done")
            elif cmd == "STOR":
                if not self.writable:
                    send("550 permission denied"); continue
                send("150 ok"); d, _ = pasv.accept(); d.recv(256); d.close()
                self.files.append(arg); send("226 stored")
            elif cmd == "DELE":
                if self.deletable and arg in self.files:
                    self.files.remove(arg); send("250 deleted")
                else:
                    send("550 cannot delete")
            elif cmd == "QUIT": send("221 bye"); break
            else: send("500 ?")
        c.close()


def _ftp(fake, **kw):
    sc = FTPScanner(ScopeGuard.from_list(["127.0.0.0/8"]), ports=[fake.port], rate=1000,
                    concurrency=2, timeout=2.0, **kw)
    return asyncio.run(sc.scan_target("127.0.0.1"))[0].data


def test_a3_ftp_never_writes_by_default():
    fake = _FakeFtp(writable=True)
    data = _ftp(fake)
    assert data["anonymous_login"] is True and data["anon_write"] is None
    assert fake.files == []                              # nothing was uploaded


def test_a3_ftp_write_test_proves_write_and_cleans_up():
    fake = _FakeFtp(writable=True)
    data = _ftp(fake, write_test=True)
    assert data["anon_write"] is True and "anon_write_leftover" not in data
    assert fake.files == []                              # the test file was deleted again


def test_a3_ftp_write_test_reports_a_leftover_it_could_not_delete():
    fake = _FakeFtp(writable=True, deletable=False)
    data = _ftp(fake, write_test=True)
    assert data["anon_write"] is True and data["anon_write_leftover"].startswith("vedha-write-test-")


def test_a3_ftp_write_refused_is_false():
    fake = _FakeFtp(writable=False)
    assert _ftp(fake, write_test=True)["anon_write"] is False


def test_a3_udp_replies_carry_a_measured_amplification_factor():
    from scanner.udp_scanner import UDPScanner
    import scanner.udp_scanner as U
    reply = b"HTTP/1.1 200 OK\r\nST: upnp:rootdevice\r\n\r\n" + b"x" * 300

    async def fake_probe(*a, **k):
        return reply
    sc = UDPScanner(ScopeGuard.from_list(["127.0.0.0/8"]), ports=[1900], rate=1000, concurrency=2,
                    timeout=0.5)
    sc._gated_probe = lambda target, port, payload: fake_probe()      # type: ignore[assignment]
    res = asyncio.run(sc.scan_target("127.0.0.1"))[0]
    req = len(U.UDP_PROBES[1900][1])
    assert res.data["request_bytes"] == req
    assert res.data["amplification_factor"] == round(len(reply) / req, 2)


# ── A6: the default sets cover every branch and every UDP probe ──────────────

def test_a6_every_branch_port_is_swept_by_the_it_profile():
    for branch, ports in gates._BRANCH_PORT_TABLE.items():
        if branch == "snmp":
            continue                                   # UDP; probed by the datagram branch
        missing = set(ports) - set(gates.IT_PORTS)
        assert not missing, f"{branch} ports never swept: {sorted(missing)}"


def test_a6_the_named_gaps_are_closed():
    for port in (873, 631, 9100, 88, 11434):
        assert port in gates.IT_PORTS, port


def test_a6_default_udp_set_is_every_probe():
    assert gates.UDP_PORTS == set(UDP_PROBES)


def test_a6_standard_intensity_udp_covers_every_service_the_manager_has_a_rule_for():
    from workflow.intensity import intensity_udp_ports
    standard = set(intensity_udp_ports("standard") or [])
    assert {53, 123, 137, 161, 500, 623, 1900, 5060, 5353, 11211} <= standard
