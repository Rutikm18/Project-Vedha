"""
test_network_va_accuracy.py — end-to-end accuracy of the network_va use case.

Everything here drives the REAL agent path (`agent.engine.run_scan("network_va")`)
against REAL listeners on loopback, then asserts on what the probe actually put on
the wire and what it concluded. No scanner is monkeypatched: the point is to catch
the class of bug where every unit test passes and the real scan still misses the
service, which is what happened with the risk-port catalog.

Kept deliberately small and fast — a handful of loopback sockets and one bounded
port set — so it can run in the normal suite rather than being a manual rig step.
"""
from __future__ import annotations

import json
import socket
import threading
import time

import pytest

from agent.engine import run_scan
from workflow.gates import IT_PORTS, VA_RISK_PORTS


class _Listener:
    """A real TCP listener that optionally speaks first."""

    def __init__(self, port: int, payload: bytes = b""):
        self.port = port
        self.payload = payload
        self.sock: socket.socket | None = None
        self.hits = 0

    def start(self) -> bool:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", self.port))
            s.listen(16)
        except OSError:
            s.close()
            return False               # privileged or already taken — caller skips
        self.sock = s
        threading.Thread(target=self._loop, daemon=True).start()
        return True

    def _loop(self) -> None:
        try:
            while True:
                conn, _ = self.sock.accept()
                self.hits += 1
                threading.Thread(target=self._serve, args=(conn,), daemon=True).start()
        except OSError:
            pass

    def _serve(self, conn: socket.socket) -> None:
        try:
            if self.payload:
                conn.sendall(self.payload)
            else:
                conn.settimeout(0.3)
                try:
                    conn.recv(64)
                except OSError:
                    pass
        except OSError:
            pass
        finally:
            conn.close()

    def stop(self) -> None:
        if self.sock:
            self.sock.close()


@pytest.fixture(scope="module")
def va_scan():
    """One real network_va against loopback with risk-catalog services listening."""
    wanted = {
        4444: b"",                                              # Metasploit handler
        31337: b"bash-5.1$ ",                                   # backdoor by protocol
        6667: b":irc.local NOTICE AUTH :*** Looking up your hostname\r\n",
        2379: b"HTTP/1.1 404 Not Found\r\nX-Etcd-Cluster-Id: cdf818194e3a8c32\r\n\r\n",
    }
    listeners = {}
    for port, payload in wanted.items():
        lis = _Listener(port, payload)
        if lis.start():
            listeners[port] = lis
    if not listeners:
        pytest.skip("could not bind any risk-catalog port on loopback")
    time.sleep(0.3)
    try:
        result = run_scan(
            "network_va",
            {"targets": ["127.0.0.1"], "intensity": "standard",
             "scope_cidrs": ["127.0.0.0/8"]},
            validated_scope=["127.0.0.0/8"],
        )
    finally:
        for lis in listeners.values():
            lis.stop()
    facts = result.get("facts") or []
    return {
        "ports": sorted(listeners),
        "facts": facts,
        "result": result,
        "open": sorted({f["port"] for f in facts
                        if f["scanner"] == "port_scan" and f["status"] == "open"}),
        "banners": {f["port"]: f["data"] for f in facts
                    if f["scanner"] == "service_banner"},
        "runs": {r["id"]: r for r in (result.get("scanner_runs") or [])},
    }


# ── the sweep actually reaches the risk catalog ──────────────────────────────

def test_every_planted_risk_port_is_found(va_scan):
    """The regression this guards: these ports were outside the 40-port catalog,
    so a network_va could not see them at all however loudly they listened."""
    missed = [p for p in va_scan["ports"] if p not in va_scan["open"]]
    assert not missed, f"network_va did not find planted risk ports {missed}"


def test_scan_completed_without_errors(va_scan):
    assert va_scan["result"].get("ok") is not False
    for name, run in va_scan["runs"].items():
        assert run.get("error_count", 0) == 0, f"{name} reported errors"


# ── identification quality on those ports ────────────────────────────────────

def test_shell_prompt_is_identified_as_a_shell(va_scan):
    if 31337 not in va_scan["ports"]:
        pytest.skip("31337 unavailable")
    assert va_scan["banners"][31337].get("service") == "shell"


def test_irc_is_identified_by_protocol_not_port(va_scan):
    """Positive protocol evidence turns the botnet-C2 port guess into an
    observation, which is what the manager records as corroboration."""
    if 6667 not in va_scan["ports"]:
        pytest.skip("6667 unavailable")
    assert va_scan["banners"][6667].get("service") == "irc"


def test_etcd_is_identified_and_cpe_mapped(va_scan):
    if 2379 not in va_scan["ports"]:
        pytest.skip("2379 unavailable")
    data = va_scan["banners"][2379]
    assert data.get("service") == "etcd"
    assert data.get("http_status") == 404          # structured HTTP head extracted


def test_silent_port_reports_no_banner_honestly(va_scan):
    """4444 says nothing. The scanner must record that, not invent a service."""
    if 4444 not in va_scan["ports"]:
        pytest.skip("4444 unavailable")
    data = va_scan["banners"][4444]
    assert data.get("banner") is None
    assert data.get("service") is None
    assert data.get("tls_probed") is True          # and it did try TLS


# ── branch routing stays disciplined on a busy host ──────────────────────────

def test_no_branch_runs_without_evidence(va_scan):
    """Every deep branch that ran must have produced facts or have had a port to
    justify it — the check for 'unnecessary scanners are running'."""
    runs = va_scan["runs"]
    for name in ("ldap_scan", "dns_scan", "nfs_scan", "ftp_scan", "rsync_scan",
                 "vnc_scan", "smtp_scan", "printer_scan"):
        run = runs.get(name)
        if run and run["status"] != "skipped":
            assert run.get("fact_count", 0) > 0, (
                f"{name} ran but produced nothing — it should have been skipped")


def test_tls_branch_is_not_routed_by_silence(va_scan):
    """service_banner now proves non-TLS by attempting a handshake, so silent
    binary ports must not be speculatively re-probed by tls_scan."""
    for port, data in va_scan["banners"].items():
        if data.get("banner") is None and data.get("tls_probed"):
            assert not data.get("tls"), f"port {port} unexpectedly negotiated TLS"


def test_post_stages_ran(va_scan):
    """network_va composes device classification and the exposure matrix."""
    scanners = {f["scanner"] for f in va_scan["facts"]}
    assert "device_classify" in scanners or "exposure_matrix" in scanners


# ── catalog invariants that make the above possible ──────────────────────────

def test_risk_ports_are_in_the_it_catalog():
    assert set(VA_RISK_PORTS) <= set(IT_PORTS)


@pytest.mark.parametrize("port", [4444, 31337, 6667, 2379, 6000, 9092, 2181])
def test_named_risk_port_in_catalog(port):
    assert port in IT_PORTS
