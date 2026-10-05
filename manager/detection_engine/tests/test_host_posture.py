"""
test_host_posture.py — credentialed host posture & IOA detection (host_posture.py).

Drives the real detectors against realistic WinRM Format-List/Format-Table and
ss/netstat output, then the full detect_host_posture_traced path (state, risk,
traces, coverage). The guiding invariant under test: a detector NEVER accuses on
absent / errored / truncated input.
"""
from __future__ import annotations

import host_posture as H
from models import Asset, Fact, SourceConfidence
from posture_rules import OUTCOME_NO_EVIDENCE, detect_posture_traced


def _win_fact(inventory: dict) -> Fact:
    return Fact(scanner="windows_inventory", target="10.0.0.9",
                timestamp="2026-09-01T00:00:00Z", port=5985, proto="tcp",
                status="observed", data={"transport": "winrm", "inventory": inventory},
                evidence=None, error=None,
                source_confidence=SourceConfidence.authoritative,
                source_file="corpus.jsonl", source_line=1)


def _ssh_fact(inventory: dict) -> Fact:
    return Fact(scanner="ssh_inventory", target="10.0.0.9",
                timestamp="2026-09-01T00:00:00Z", port=22, proto="tcp",
                status="observed", data={"inventory": inventory},
                evidence=None, error=None,
                source_confidence=SourceConfidence.authoritative,
                source_file="corpus.jsonl", source_line=2)


def _asset(*facts: Fact) -> Asset:
    a = Asset(ip="10.0.0.9")
    for f in facts:
        a.add_fact(f)
    return a


# ── AV disabled ───────────────────────────────────────────────────────────────
_DEFENDER_OFF = (
    "AMServiceEnabled              : True\n"
    "RealTimeProtectionEnabled     : False\n"
    "AntivirusSignatureLastUpdated : 1/2/2026 3:04:05 AM\n")
_DEFENDER_OK = (
    "AMServiceEnabled              : True\n"
    "RealTimeProtectionEnabled     : True\n")


def test_av_realtime_disabled_fires():
    ev = H.detect_av_disabled(_win_fact({"defender_status": _DEFENDER_OFF}))
    assert ev and "real-time protection disabled" in ev["disabled"]


def test_av_healthy_clean():
    assert H.detect_av_disabled(_win_fact({"defender_status": _DEFENDER_OK})) is None


def test_av_cmdlet_errored_silent():
    # Defender absent / command failed -> never accuse
    assert H.detect_av_disabled(_win_fact({"defender_status": "__error__: not recognized"})) is None
    assert H.detect_av_disabled(_win_fact({})) is None


# ── service binary paths ───────────────────────────────────────────────────────
_SERVICES = (
    "Name        StartMode State   PathName\n"
    "----        --------- -----   --------\n"
    "Spooler     Auto      Running C:\\Windows\\System32\\spoolsv.exe\n"
    "GoodSvc     Auto      Running \"C:\\Program Files\\Vendor App\\svc.exe\" -k\n"
    "EvilSvc     Auto      Running C:\\Users\\Public\\update.exe\n"
    "Unquoted    Auto      Running C:\\Program Files\\Foo Bar\\agent.exe\n")


def test_service_in_writable_dir_fires():
    evs = H.detect_service_writable_path(_win_fact({"services": _SERVICES}))
    paths = {e["image_path"] for e in evs}
    assert "C:\\Users\\Public\\update.exe" in paths
    # the clean System32 and quoted Program Files services must NOT be flagged here
    assert not any("System32" in p for p in paths)


def test_unquoted_service_path_fires():
    evs = H.detect_unquoted_service_path(_win_fact({"services": _SERVICES}))
    paths = {e["image_path"] for e in evs}
    assert "C:\\Program Files\\Foo Bar\\agent.exe" in paths
    # quoted path and no-space System32 path are not unquoted-vulnerable
    assert not any("Vendor App" in p for p in paths)
    assert not any("System32" in p for p in paths)


def test_truncated_service_line_not_accused():
    truncated = ("Name   StartMode State   PathName\n"
                 "----   --------- -----   --------\n"
                 "Weird  Auto      Running C:\\Users\\Public\\reallylongpath\\thing th…\n")
    assert H.detect_service_writable_path(_win_fact({"services": truncated})) == []


# ── excessive local admins ─────────────────────────────────────────────────────
def test_excessive_local_admins_fires():
    rows = ["Name            PrincipalSource", "----            ---------------"]
    rows += [f"CORP\\user{i}   ActiveDirectory" for i in range(12)]
    ev = H.detect_excessive_local_admins(_win_fact({"local_admins": "\n".join(rows)}))
    assert ev and ev["admin_count"] == 12


def test_few_local_admins_clean():
    text = ("Name            PrincipalSource\n----            ---------------\n"
            "Administrator   Local\nCORP\\Domain Admins ActiveDirectory\n")
    assert H.detect_excessive_local_admins(_win_fact({"local_admins": text})) is None


# ── Linux malicious process ────────────────────────────────────────────────────
def test_malicious_process_fires():
    procs = "bash\nsshd\n/tmp/.x/xmrig\nnginx\nkdevtmpfsi\n"
    evs = H.detect_malicious_process(_ssh_fact({"processes": procs}))
    matched = {e["process"] for e in evs}
    assert "/tmp/.x/xmrig" in matched and "kdevtmpfsi" in matched


def test_dualuse_tools_not_flagged():
    # nc / socat / python are dual-use — presence is not compromise evidence
    procs = "bash\nnc\nsocat\npython3\nncat\n"
    assert H.detect_malicious_process(_ssh_fact({"processes": procs})) == []


# ── Linux backdoor listener ────────────────────────────────────────────────────
_SS_TCP = (
    "State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n"
    "LISTEN 0      128    0.0.0.0:22         0.0.0.0:*         users:((\"sshd\",pid=800))\n"
    "LISTEN 0      1      0.0.0.0:4444       0.0.0.0:*         users:((\"nc\",pid=1337))\n"
    "LISTEN 0      5      127.0.0.1:6379     0.0.0.0:*         users:((\"redis\",pid=900))\n")


def test_backdoor_listener_fires():
    evs = H.detect_backdoor_listener(_ssh_fact({"listening_tcp": _SS_TCP}))
    ports = {e["port"] for e in evs}
    assert 4444 in ports
    # 22 and loopback-bound 6379 are not backdoor ports here
    assert 22 not in ports and 6379 not in ports


# ── end-to-end via detect_posture_traced (wiring, state, coverage) ────────────
def test_credentialed_findings_are_confirmed_and_traced():
    asset = _asset(
        _win_fact({"defender_status": _DEFENDER_OFF, "services": _SERVICES,
                   "local_admins": "Name\n----\nAdministrator  Local\n"}),
        _ssh_fact({"processes": "bash\nxmrig\n", "listening_tcp": _SS_TCP}),
    )
    findings, traces = detect_posture_traced(asset)
    by_id: dict[str, list] = {}
    for f in findings:
        by_id.setdefault(f.rule_id, []).append(f)
    assert "HOST-AV-DISABLED" in by_id
    assert "HOST-SERVICE-WRITABLE-PATH" in by_id
    assert "HOST-MALICIOUS-PROCESS" in by_id
    assert "HOST-BACKDOOR-LISTENER" in by_id
    # credentialed source -> CONFIRMED, highest confidence tier
    av = by_id["HOST-AV-DISABLED"][0]
    assert av.state == "confirmed"
    assert av.precision_factors.get("base", {}).get("tier") == "authoritative_credentialed"
    # the miner process is critical
    assert by_id["HOST-MALICIOUS-PROCESS"][0].severity == "critical"


def test_no_credentialed_scan_reports_no_evidence_not_clean():
    # a host with only a network scan must show host-posture rules as NO_EVIDENCE,
    # never silently absent (so 'not assessed' != 'checked clean')
    netfact = Fact(scanner="smb_scan", target="10.0.0.9", timestamp="2026-09-01T00:00:00Z",
                   port=445, proto="tcp", status="open",
                   data={"smbv1_enabled": False, "smb2_supported": True, "signing_required": True},
                   evidence=None, error=None, source_confidence=SourceConfidence.inferred,
                   source_file="c.jsonl", source_line=1)
    _findings, traces = detect_posture_traced(_asset(netfact))
    host_rule_outcomes = {(t.rule_id, t.outcome) for t in traces if t.rule_id.startswith("HOST-")}
    assert ("HOST-AV-DISABLED", OUTCOME_NO_EVIDENCE) in host_rule_outcomes
    assert ("HOST-MALICIOUS-PROCESS", OUTCOME_NO_EVIDENCE) in host_rule_outcomes
