"""
Field gap (testing round 1, #2): one service produced 3-6 findings (FTP x3, Telnet x3).
Re-checked on 17 Oct: the posture track is now the only exposed-cleartext producer and
each exposed-service finding carries a condition-level dedup key, so a Telnet port is
ONE finding and an anonymous FTP port is TWO distinct conditions (anonymous login, and
cleartext protocol), each with its own fix. This pins those counts.
"""
from __future__ import annotations

import json
from collections import Counter

from pipeline import run_full_detection

T = "10.0.0.20"


def _row(scanner, port, data):
    return {"scanner": scanner, "target": T, "timestamp": "2026-10-17T00:00:00Z",
            "port": port, "proto": "tcp", "status": "open", "evidence": None,
            "error": None, "data": data}


def test_ftp_and_telnet_host_findings_per_port(tmp_path):
    rows = [
        _row("port_scan", 21, {"state": "open"}),
        _row("port_scan", 23, {"state": "open"}),
        _row("service_banner", 21, {"first_line": "220 (vsFTPd 3.0.3)", "service": "ftp",
                                    "product": "vsftpd", "version": "3.0.3"}),
        _row("service_banner", 23, {"first_line": "\xff\xfd\x18", "service": "telnet"}),
        _row("ftp_scan", 21, {"ftp": True, "software": "(vsFTPd 3.0.3)",
                              "anonymous_login": True, "anon_read": True}),
    ]
    p = tmp_path / "f.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    res = run_full_detection([str(p)])

    keys = [(f.to_dict().get("evidence") or {}).get("dedup_key") for f in res["posture"]]
    assert all(keys), "every exposed-service finding carries a dedup key"
    assert len(keys) == len(set(keys)), "no two findings share a condition"
    per_port = Counter(k.rsplit(":", 1)[-1] for k in keys)
    assert per_port == {"23": 1, "21": 2}
    rules = sorted(f.rule_id for f in res["posture"])
    assert rules == ["POSTURE-EXPOSED-CLEARTEXT", "POSTURE-EXPOSED-CLEARTEXT",
                     "POSTURE-FTP-ANONYMOUS-LOGIN"]
