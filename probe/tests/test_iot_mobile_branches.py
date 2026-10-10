"""
test_iot_mobile_branches.py — the IoT and mobile collectors must run on a real job.

THE DEFECT THIS PINS. iot_scanner (RTSP, MQTT, CWMP, SSDP, mDNS, CoAP) and
mobile_scanner (ADB, iOS lockdownd) existed in both scanner trees with their own
unit tests, and the manager carried four rules that read their facts:
POSTURE-MQTT-UNAUTHENTICATED, POSTURE-CWMP-EXPOSED, POSTURE-RTSP-EXPOSED and the
CRITICAL POSTURE-ADB-UNAUTHENTICATED. But no workflow stage ever constructed
either scanner — not in the `it` profile, not even in the `iot` profile — so on
every job those rules could not fire. The weak-lab scan of 2026-10-10 proved it:
an anonymous MQTT broker and an unauthenticated ADB shell were both reported
clean.

THE TRAP THE FIX HAD TO AVOID. `_port_candidates` used to add SMB_PORTS for EVERY
host-level branch, because smb was the only one. Registering iot/mobile as
host-level branches without fixing that would have swept 139/445 instead of
1883/5555 — the branch gate (open port ∩ trigger table) would then never pass and
the fix would have silently done nothing. TestSweep pins the general invariant.

The end-to-end test runs the REAL scanners through the REAL engine against tiny
in-test devices on 127.0.0.1, takes the facts exactly as the agent uploads them
(the workflow cache), and pushes them through the manager's real ingest and rules.
"""
from __future__ import annotations

import asyncio
import json
import socket
import sys
import threading
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pytest

import workflow.workflow_engine as we
from scanner import iot_scanner, mobile_scanner
from scanner.scanner_base import ScanResult, ScopeGuard
from workflow.asset import Asset, PortFact, _MERGE_DISPATCH
from workflow.branches import BRANCH_BY_NAME, BRANCHES
from workflow.cache import FACT_CERTAINTY, WorkflowCache, classify_certainty
from workflow.gates import (
    IOT_SERVICE_PORTS, MOBILE_SERVICE_PORTS, PROFILE_DEEP_BRANCHES,
    _BRANCH_PORT_TABLE, gate_5_branch_eligible,
)

_ENGINE = Path(__file__).resolve().parents[2] / "manager" / "detection_engine"


# ── registry ─────────────────────────────────────────────────────────────────

class TestRegistry:
    @pytest.mark.parametrize("branch,component", [("iot", "iot_scan"),
                                                  ("mobile", "mobile_scan")])
    def test_registered_as_host_level_branches(self, branch, component):
        spec = BRANCH_BY_NAME[branch]
        assert spec.component == component
        # Each scanner probes its own fixed protocol set per HOST; it takes no
        # `ports` argument, so it must be host-level (one run per host).
        assert spec.host_level

    def test_every_branch_scanner_emits_its_component_name(self):
        """The manager keys its rules on ScanResult.scanner. If a spec's
        component and its scanner class's `name` ever disagree, the trace and
        plan say one thing while the facts arrive under another name."""
        for spec in BRANCHES:
            cls = getattr(we, spec.scanner)
            assert cls.name == spec.component, (spec.branch, cls.name, spec.component)

    def test_trigger_tables_match_what_the_scanners_probe(self):
        """The gate fires on these ports; they must be exactly the TCP ports the
        scanner itself connects to, or the gate and the scanner drift apart."""
        assert IOT_SERVICE_PORTS == set(iot_scanner._RTSP_PORTS
                                        + iot_scanner._MQTT_PORTS
                                        + iot_scanner._CWMP_PORTS)
        assert MOBILE_SERVICE_PORTS == {5555, mobile_scanner._IOS_LOCKDOWND_PORT}
        assert _BRANCH_PORT_TABLE["iot"] == IOT_SERVICE_PORTS
        assert _BRANCH_PORT_TABLE["mobile"] == MOBILE_SERVICE_PORTS

    def test_standalone_funnel_routes_match_the_gate_tables(self):
        """The CLI/campaign path (scan_funnel, both trees) must trigger on the
        same ports as the agent's job path, or the two orchestrators disagree
        about which hosts get IoT/mobile handshakes."""
        from scanner.scan_funnel import DEFAULT_PORT_ROUTES, build_default_funnel
        assert set(DEFAULT_PORT_ROUTES["iot"]) == IOT_SERVICE_PORTS
        assert set(DEFAULT_PORT_ROUTES["mobile"]) == MOBILE_SERVICE_PORTS
        funnel = build_default_funnel(ScopeGuard.from_list(["10.0.0.0/8"]))
        assert funnel.deep_scanner_factories["iot"]([1883]).name == "iot_scan"
        assert funnel.deep_scanner_factories["mobile"]([5555]).name == "mobile_scan"


# ── profiles ─────────────────────────────────────────────────────────────────

class TestProfiles:
    @pytest.mark.parametrize("profile", ["it", "iot"])
    def test_allowed_on_active_profiles(self, profile):
        assert {"iot", "mobile"} <= PROFILE_DEEP_BRANCHES[profile]

    def test_never_on_the_passive_ot_profile(self):
        assert not ({"iot", "mobile"} & PROFILE_DEEP_BRANCHES["ot"])


# ── the port sweep must reach every branch's trigger ports ───────────────────

class TestSweep:
    @pytest.mark.parametrize("profile", ["it", "iot"])
    @pytest.mark.parametrize("override", [None, [80, 443]])   # [80,443] ≈ an intensity override
    def test_every_allowed_tcp_branch_trigger_port_is_swept(self, profile, override):
        """A branch gated on 'trigger port is open' can only ever run if the
        sweep puts that port on the wire — for every branch, not just iot."""
        swept = set(we._port_candidates(profile, None, port_override=override))
        for spec in BRANCHES:
            if spec.branch not in PROFILE_DEEP_BRANCHES[profile] or spec.datagram:
                continue
            missing = set(_BRANCH_PORT_TABLE[spec.branch]) - swept
            assert not missing, (profile, override, spec.branch, sorted(missing))

    @pytest.mark.parametrize("branch,ports", [("mobile", MOBILE_SERVICE_PORTS),
                                              ("iot", IOT_SERVICE_PORTS),
                                              ("smb", {139, 445})])
    def test_host_level_branch_sweeps_its_own_ports(self, branch, ports):
        """Regression for the trap: a host-level branch used to contribute
        SMB_PORTS whatever it was. A mobile-only job must sweep 5555/62078."""
        assert set(we._port_candidates("it", {branch})) == set(ports)


# ── the gate: probe only hosts that show the service ─────────────────────────

def _asset(*ports: int) -> Asset:
    now = datetime.now(timezone.utc)
    return Asset(host="10.0.0.9", last_seen_alive=now,
                 open_ports={p: PortFact(proto="tcp", status="open", last_scan_time=now)
                             for p in ports})


class TestGate:
    def test_open_mqtt_triggers_iot(self):
        assert gate_5_branch_eligible("iot", _asset(22, 1883), "it", None)

    def test_open_rtsp_triggers_iot(self):
        assert gate_5_branch_eligible("iot", _asset(554), "it", None)

    def test_open_adb_triggers_mobile(self):
        assert gate_5_branch_eligible("mobile", _asset(5555), "it", None)

    def test_an_ordinary_server_is_not_probed(self):
        """No IoT/mobile handshakes against a host that shows none of their
        ports — the fix must not add noise or packets to every server."""
        plain = _asset(22, 80, 443, 3306)
        assert not gate_5_branch_eligible("iot", plain, "it", None)
        assert not gate_5_branch_eligible("mobile", plain, "it", None)

    def test_ot_profile_never_probes(self):
        assert not gate_5_branch_eligible("iot", _asset(1883), "ot", None)


# ── merge + cache: facts must reach the upload set ───────────────────────────

class TestMergeAndCache:
    @pytest.mark.parametrize("component", ["iot_scan", "mobile_scan"])
    def test_has_a_merge_handler_and_certainty(self, component):
        assert component in _MERGE_DISPATCH
        assert component in FACT_CERTAINTY

    def test_udp_answers_stay_recheckable(self):
        """iot_scan mixes TCP handshakes with single UDP datagrams (SSDP, mDNS,
        CoAP). Silence on UDP is ambiguous, so those must stay uncertain."""
        udp = ScanResult("iot_scan", "10.0.0.9", port=1900, proto="udp",
                         status="open", data={"location": "x"})
        tcp = ScanResult("iot_scan", "10.0.0.9", port=1883, proto="tcp",
                         status="open", data={"mqtt_connack": True})
        assert classify_certainty(udp) == "uncertain"
        assert classify_certainty(tcp) == "deterministic"

    def test_facts_merge_per_port(self):
        a = _asset(1883, 5555)
        a.merge_result(ScanResult("iot_scan", "10.0.0.9", port=1883, proto="tcp",
                                  status="open", data={"mqtt_connack": True}))
        a.merge_result(ScanResult("mobile_scan", "10.0.0.9", port=5555, proto="tcp",
                                  status="open", data={"unauthenticated_shell": True}))
        assert a.iot_facts[1883]["mqtt_connack"] is True
        assert a.mobile_facts[5555]["unauthenticated_shell"] is True


def test_non_branch_producers_match_the_manager_guard():
    """manager/detection_engine/tests/test_branch_rule_coverage.py keeps a literal
    NON_BRANCH_PRODUCERS set (it cannot import the whole engine in CI). Pin it
    here against the classes the engine really constructs, so a rename on either
    side fails instead of quietly exempting a dead rule."""
    constructed = {we.HostDiscoveryScanner.name, we.PortScanner.name, we.SynScanner.name,
                   we.OSFingerprintScanner.name, we.ServiceBannerScanner.name,
                   we.UDPScanner.name}
    credentialed_and_passive = {"ssh_inventory", "windows_inventory", "passive_collect"}
    if not _ENGINE.exists():
        pytest.skip("manager tree not present")
    # The guard module imports posture_rules from the engine directory itself.
    added = [str(_ENGINE), str(_ENGINE / "tests")]
    sys.path[:0] = added
    try:
        import test_branch_rule_coverage as guard
    except ImportError as exc:      # a probe-only CI image without manager deps
        pytest.skip(f"manager detection engine not importable here: {exc}")
    finally:
        for p in added:
            sys.path.remove(p)
    assert guard.NON_BRANCH_PRODUCERS == constructed | credentialed_and_passive


# ── end to end: real scanners → real engine → upload set → manager rules ─────

def _adb(conn: socket.socket) -> None:
    hdr = conn.recv(24)
    if len(hdr) < 24:
        return
    body = b"device::ro.product.name=lab;features=shell_v2\x00"
    cnxn = 0x4E584E43
    conn.sendall(cnxn.to_bytes(4, "little") + (0x01000000).to_bytes(4, "little")
                 + (256 * 1024).to_bytes(4, "little") + len(body).to_bytes(4, "little")
                 + (sum(body) & 0xFFFFFFFF).to_bytes(4, "little")
                 + (cnxn ^ 0xFFFFFFFF).to_bytes(4, "little") + body)


def _mqtt(conn: socket.socket) -> None:
    if conn.recv(64):
        conn.sendall(b"\x20\x02\x00\x00")          # CONNACK, return code 0 = accepted


def _rtsp(conn: socket.socket) -> None:
    if conn.recv(512):
        conn.sendall(b"RTSP/1.0 200 OK\r\nCSeq: 1\r\nServer: LabCam/1.0\r\n"
                     b"Public: OPTIONS, DESCRIBE, SETUP, PLAY\r\n\r\n")


def _cwmp(conn: socket.socket) -> None:
    if conn.recv(512):
        body = b"<html>CWMP connection-request endpoint</html>"
        conn.sendall(b"HTTP/1.1 200 OK\r\nServer: gSOAP/2.8\r\nContent-Length: "
                     + str(len(body)).encode() + b"\r\nConnection: close\r\n\r\n" + body)


class _Device:
    """A one-protocol fake device on 127.0.0.1:port, served from a thread."""

    def __init__(self, port: int, handler):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", port))     # raises OSError when the port is busy
        self.sock.listen(8)
        self.sock.settimeout(0.2)
        self.handler = handler
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self) -> None:
        while not self.stop.is_set():
            try:
                conn, _ = self.sock.accept()
            except (socket.timeout, OSError):
                continue
            with conn:
                conn.settimeout(2)
                try:
                    self.handler(conn)
                except OSError:
                    pass

    def close(self) -> None:
        self.stop.set()
        self.thread.join(timeout=2)
        self.sock.close()


@pytest.fixture
def lab_devices():
    """ADB 5555, MQTT 1883, RTSP 8554, CWMP 7547 — all unprivileged ports. Skips
    (never fails) when a port is busy, so a developer's own broker does not break
    the suite."""
    devices = []
    try:
        for port, handler in ((5555, _adb), (1883, _mqtt), (8554, _rtsp), (7547, _cwmp)):
            devices.append(_Device(port, handler))
    except OSError as exc:
        for d in devices:
            d.close()
        pytest.skip(f"a lab port is busy on this machine: {exc}")
    yield
    for d in devices:
        d.close()


def _alive_discovery():
    class _Discovery:
        name = "host_discovery"

        def __init__(self, *a, **k):
            pass

        async def scan_target(self, target):
            return [ScanResult("host_discovery", target, status="up", data={"alive": True})]

        async def run(self, targets):
            out = []
            for t in targets:
                out.extend(await self.scan_target(t))
            return out
    return _Discovery


def test_mqtt_rtsp_cwmp_and_adb_are_detected_end_to_end(lab_devices, monkeypatch):
    # Liveness is not what this test is about; everything after it is real.
    monkeypatch.setattr(we, "HostDiscoveryScanner", _alive_discovery())
    cache = WorkflowCache()
    asyncio.run(we.run_engagement(
        ["127.0.0.1"], ScopeGuard.from_list(["127.0.0.1/32"]),
        service_filter={"iot", "mobile"}, cache=cache, timeout=2.0))

    # Exactly what agent/engine.py uploads to the manager.
    uploaded = [asdict(entry.result) for entry in cache._store.values()]
    scanners = {f["scanner"] for f in uploaded}
    assert {"iot_scan", "mobile_scan"} <= scanners, sorted(scanners)

    if not _ENGINE.exists():
        pytest.skip("manager tree not present")
    sys.path.insert(0, str(_ENGINE))
    try:
        import ingest
        import posture_rules
    except ImportError as exc:      # the probe half above has already been proven
        pytest.skip(f"manager detection engine not importable here: {exc}")
    finally:
        sys.path.remove(str(_ENGINE))
    path = Path(__file__).parent / ".tmp_iot_mobile_facts.jsonl"
    try:
        path.write_text("\n".join(json.dumps(f) for f in uploaded) + "\n")
        result = ingest.ingest_file(path)
        assert not result.quarantined, [q.reason for q in result.quarantined]
        rule_ids = {f.rule_id for f in posture_rules.detect_all(result)}
    finally:
        path.unlink(missing_ok=True)

    assert {"POSTURE-ADB-UNAUTHENTICATED", "POSTURE-MQTT-UNAUTHENTICATED",
            "POSTURE-RTSP-EXPOSED", "POSTURE-CWMP-EXPOSED"} <= rule_ids, sorted(rule_ids)
