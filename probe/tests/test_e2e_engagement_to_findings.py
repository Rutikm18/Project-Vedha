"""
test_e2e_engagement_to_findings.py — the whole pipeline in one place.

    manager engagement + scope
        → ScanJob {use_case_id, scope, targets}
        → probe (TaskRunner → engine.run_scan → REAL sockets)
        → result "POSTed" to manager (captured submit)
        → manager correlation (main_scripts.findings.run_findings)
        → vulnerabilities (base + correlated attack paths)

Only the HTTP transport and the /scope endpoint are stubbed (network plumbing);
the scan and the correlation are the real code paths. A companion runnable demo
lives at scratchpad/e2e_demo.py.
"""
from __future__ import annotations

import socket
import threading

import pytest

from agent.task_runner import TaskRunner
from main_scripts import findings as F


# ── scannable-address helper ─────────────────────────────────────────────────
# NOT loopback. agent/job_admission.drop_denied puts 127/8 on the probe's
# PERMANENT denylist (loopback / link-local / multicast / reserved / broadcast /
# the manager itself), and TaskRunner applies it as the last gate before a
# packet leaves. These tests predate that control (written 2026-08-15, denylist
# landed 2026-09-12) and have been failing ever since — they asked the probe to
# scan a target it is designed to refuse.
#
# The fix is to test against an address the probe may legitimately scan, not to
# weaken the gate. This host's own primary interface address is not denied, so
# the full path — real sockets, real scan, real correlation — still runs.
# tests/test_job_admission.py covers the denylist itself.


def _scannable_local_ip() -> str | None:
    """This host's primary non-loopback IPv4, or None if it has none.

    No packet is sent: connecting a UDP socket only asks the kernel which
    source address it WOULD use for that route.
    """
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("198.51.100.1", 9))     # TEST-NET-2, never routed
        return probe.getsockname()[0]
    except OSError:
        return None
    finally:
        probe.close()


# ── service helper ───────────────────────────────────────────────────────────
def _accept_loop(s: socket.socket) -> None:
    while True:
        try:
            conn, _ = s.accept()
            conn.close()
        except OSError:
            break


def _plant(ports: list[int], host: str) -> list[socket.socket]:
    servers: list[socket.socket] = []
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, p))
            s.listen(16)
            servers.append(s)
            threading.Thread(target=_accept_loop, args=(s,), daemon=True).start()
        except OSError:
            s.close()
    return servers


def _manager(scope_cidrs: list[str]):
    """Return (http_get, submit_result, captured) simulating the manager side."""
    captured: dict = {}

    def http_get(_url: str):
        return {"scope_cidrs": scope_cidrs, "excluded_cidrs": []}

    def submit_result(job_id: str, payload: dict) -> bool:
        captured["job_id"] = job_id
        captured["payload"] = payload
        return True

    return http_get, submit_result, captured


# ── the pipeline: engagement → probe scan → manager ingest ───────────────────
@pytest.fixture
def target() -> str:
    ip = _scannable_local_ip()
    if ip is None:
        pytest.skip("host has no non-loopback IPv4 to scan")
    return ip


def test_engagement_dispatch_reaches_probe_and_enforces_scope(target):
    http_get, submit_result, captured = _manager([f"{target}/32"])
    runner = TaskRunner(http_get=http_get, submit_result=submit_result)

    job = {
        "job_id": "job-scope",
        "engagement_id": "eng-1",
        "params": {"use_case_id": "uc_device_inventory", "targets": [target]},
    }
    result = runner.run_job(job, agent_id="probe-1")

    assert result.success is True
    res = captured["payload"]["result"]
    enforced = res["run_stats"]["scope_enforced"]
    assert enforced["allow"] == [f"{target}/32"]
    assert enforced["targets_authorized"] == [target]
    assert res["scan_type"] == "device_inventory"
    assert res["run_stats"]["applied_tuning"]["intensity"] == "standard"
    assert isinstance(res["facts"], list)


def test_out_of_scope_target_is_refused_end_to_end():
    # Manager authorizes only 10.0.0.0/24; the job asks for 8.8.8.8.
    http_get, submit_result, captured = _manager(["10.0.0.0/24"])
    runner = TaskRunner(http_get=http_get, submit_result=submit_result)

    job = {
        "job_id": "job-oos",
        "engagement_id": "eng-2",
        "params": {"use_case_id": "uc_device_inventory", "targets": ["8.8.8.8"]},
    }
    result = runner.run_job(job, agent_id="probe-1")

    assert result.success is False
    # Rejected at scope validation BEFORE the scan engine ran at all — the
    # strongest guarantee: no scan, no facts, no packet left the host.
    payload = captured["payload"]
    assert payload["success"] is False
    assert payload["result"] == {}
    assert "outside engagement scope" in (payload["error"] or "")


def test_real_scan_of_open_datastore_yields_manager_finding(target):
    servers = _plant([3306], target)   # MySQL — in the IT port catalog + a findings rule
    if not servers:
        pytest.skip("could not bind :3306 on this host (in use / restricted)")
    try:
        http_get, submit_result, captured = _manager([f"{target}/32"])
        runner = TaskRunner(http_get=http_get, submit_result=submit_result)
        job = {
            "job_id": "job-ds",
            "engagement_id": "eng-3",
            "params": {"use_case_id": "uc_device_inventory", "targets": [target]},
        }
        result = runner.run_job(job, agent_id="probe-1")
    finally:
        for s in servers:
            s.close()

    assert result.success is True
    facts = captured["payload"]["result"]["facts"]
    open_ports = {f.get("port") for f in facts if f.get("status") == "open"}
    assert 3306 in open_ports, "probe did not observe the planted datastore port"

    # Manager runs correlation/analytics over the REAL probe facts.
    findings = F.run_findings(facts)
    assert "SVC-DATASTORE-EXPOSED" in {f.rule_id for f in findings}


# ── manager correlation surfaces the desired attack paths ────────────────────
def _vulnerable_host_facts(target: str = "10.20.0.10") -> list[dict]:
    """Exactly what the probe's smb/port scanners emit for a vulnerable host."""
    return [
        {"scanner": "smb_scan", "target": target, "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": False, "signing_supported": True}},
        {"scanner": "port_scan", "target": target, "port": 3389, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": target, "port": 23, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": target, "port": 21, "proto": "tcp", "status": "open"},
    ]


def test_manager_correlation_finds_all_three_attack_paths():
    findings = F.run_findings(_vulnerable_host_facts())
    ids = {f.rule_id for f in findings}

    # base findings the probe's facts justify
    assert {"SMB-V1-ENABLED", "SMB-SIGNING-NOT-REQUIRED", "SVC-RDP-EXPOSED",
            "SVC-TELNET-CLEARTEXT", "SVC-FTP-CLEARTEXT"} <= ids
    # the correlated attack paths — the "desired vulns"
    assert "CORR-NTLM-RELAY-PATH" in ids
    assert "CORR-LEGACY-WINDOWS-SURFACE" in ids
    assert "CORR-CLEARTEXT-CLUSTER" in ids


def test_correlated_findings_cite_their_base_findings():
    findings = F.run_findings(_vulnerable_host_facts())
    for f in findings:
        if f.rule_id.startswith("CORR-"):
            assert f.data.get("correlated_findings")
            assert "correlated:" in f.evidence.lower()


def test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise():
    high = F.run_findings(_vulnerable_host_facts())
    relay_high = next(f for f in high if f.rule_id == "CORR-NTLM-RELAY-PATH")
    assert relay_high.severity == F.SEV_HIGH

    signing_only = F.run_findings([
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": False, "signing_required": False, "signing_supported": True}},
    ])
    relay_med = next(f for f in signing_only if f.rule_id == "CORR-NTLM-RELAY-PATH")
    assert relay_med.severity == F.SEV_MEDIUM
