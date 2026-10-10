#!/usr/bin/env python3
"""Localhost mini weak-lab: the REAL probe workflow against emulated weak services, then the
REAL manager detection engine on the facts it produced.

Why: unit tests prove each piece; this proves they work together the way a scan does — a
service the probe now reaches (IoT/mobile branches, TLS on a non-table port, an unidentified
port, SNMPv3 noAuth) must come out the other end as the right finding.

    sudo python3 probe/tests/rig/localhost_lab_e2e.py        # binds standard ports on 127.0.0.1

Needs root (ports 21/161/554/1883 ...) and the repo's backend dependencies. SNMP needs
`pip install pysnmp==4.4.12 'pyasn1<0.5'`; without it the SNMP rows are skipped, not faked.
It prints a findings table and exits non-zero if an expected finding is missing.
"""
from __future__ import annotations

import asyncio
import json
import os
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBE = HERE.parent.parent
REPO = PROBE.parent
sys.path.insert(0, str(PROBE))
sys.path.insert(0, str(REPO / "manager" / "backend"))
H = "127.0.0.1"
EMU = HERE / "ubuntu-weak-lab" / "lab_emulators.py"

# (rule id, port) pairs a correct pipeline must raise on this lab.
EXPECTED = {
    ("POSTURE-IPMI-CIPHER-ZERO", 623), ("POSTURE-MQTT-UNAUTHENTICATED", 1883),
    ("POSTURE-ADB-UNAUTHENTICATED", 5555), ("POSTURE-RTSP-EXPOSED", 554),
    ("POSTURE-CWMP-EXPOSED", 7547), ("POSTURE-UDP-AMPLIFIER", 123),
    ("POSTURE-SIP-EXPOSED", 5060), ("POSTURE-TLS-SELF-SIGNED", 8444),
    ("POSTURE-UNIDENTIFIED-SERVICE", 6100), ("POSTURE-FTP-ANONYMOUS-LOGIN", 21),
    ("POSTURE-EXPOSED-REMOTE_ACCESS", 4786),              # catalogued, so named — not "unidentified"
}
EXPECTED_SNMP = {("POSTURE-SNMP-DEFAULT-COMMUNITY", 161), ("POSTURE-SNMPV3-NOAUTH-USER", 161)}
MUST_NOT = {("POSTURE-UNIDENTIFIED-SERVICE", 1883),      # MQTT is explained by iot_scan
            ("POSTURE-UNIDENTIFIED-SERVICE", 4786)}      # named by the exposure catalog


def _tcp_server(port, handler, ctx=None):
    srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((H, port)); srv.listen(16)

    def loop():
        while True:
            try:
                c, _ = srv.accept()
            except OSError:
                return

            def one(c=c):
                try:
                    if ctx:
                        c = ctx.wrap_socket(c, server_side=True)
                    handler(c)
                except Exception:       # noqa: BLE001 — a probe hanging up is normal here
                    pass
                finally:
                    try:
                        c.close()
                    except OSError:
                        pass
            threading.Thread(target=one, daemon=True).start()
    threading.Thread(target=loop, daemon=True).start()


def _ftp(port=21):
    """Anonymous FTP; one scripted session per connection."""
    def session(c):
        f = c.makefile("rwb", buffering=0)
        say = lambda s: f.write(s.encode() + b"\r\n")      # noqa: E731
        say("220 lab ftpd")
        pasv = None
        while True:
            line = f.readline().decode().strip()
            if not line:
                return
            cmd = line.split(" ", 1)[0]
            if cmd == "USER": say("331 pass")
            elif cmd == "PASS": say("230 ok")
            elif cmd == "PASV":
                pasv = socket.socket(); pasv.bind((H, 0)); pasv.listen(1)
                p = pasv.getsockname()[1]
                say(f"227 Entering Passive Mode (127,0,0,1,{p >> 8},{p & 255})")
            elif cmd == "LIST":
                say("150 here"); d, _ = pasv.accept(); d.close(); say("226 done")
            elif cmd == "QUIT": say("221 bye"); return
            else: say("500 ?")
    _tcp_server(port, session)


def _snmp_agent():
    from pysnmp.entity import config, engine
    from pysnmp.entity.rfc3413 import cmdrsp, context
    from pysnmp.carrier.asyncore.dgram import udp
    eng = engine.SnmpEngine()
    config.addTransport(eng, udp.domainName, udp.UdpTransport().openServerMode((H, 161)))
    config.addV1System(eng, "my-area", "public")
    config.addVacmUser(eng, 2, "my-area", "noAuthNoPriv", (1, 3, 6, 1, 2, 1), (1, 3, 6, 1, 2, 1))
    config.addV3User(eng, "initial")                                  # noAuthNoPriv
    config.addVacmUser(eng, 3, "initial", "noAuthNoPriv", (1, 3, 6, 1, 2, 1), (1, 3, 6, 1, 2, 1))
    cmdrsp.GetCommandResponder(eng, context.SnmpContext(eng))
    eng.transportDispatcher.jobStarted(1)
    eng.transportDispatcher.runDispatcher()


def main() -> int:
    if os.geteuid() != 0:
        print("needs root to bind the standard service ports on 127.0.0.1")
        return 2
    procs = []
    emu = lambda name, *a: procs.append(subprocess.Popen(   # noqa: E731
        [sys.executable, str(EMU), "serve", name, "--bind", H, *a],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    emu("rtsp", "--tcp", "554"); emu("cwmp", "--tcp", "7547"); emu("adb", "--tcp", "5555")
    emu("ssdp", "--udp", "1900"); emu("ntp", "--udp", "123")
    emu("sip", "--tcp", "5060", "--udp", "5060"); emu("ipmi", "--udp", "623")

    _tcp_server(1883, lambda c: (c.settimeout(2), c.recv(256), c.sendall(b"\x20\x02\x00\x00")))
    _tcp_server(4786, lambda c: (c.settimeout(1.5), c.recv(64)))             # catalogued, silent
    _tcp_server(6100, lambda c: (c.settimeout(1.5), c.recv(64)))             # opens, says nothing, unknown
    tmp = tempfile.mkdtemp()
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout",
                    f"{tmp}/k.pem", "-out", f"{tmp}/c.pem", "-days", "2", "-subj", "/CN=weak.lab"],
                   check=True, capture_output=True)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(f"{tmp}/c.pem", f"{tmp}/k.pem")
    _tcp_server(8444, lambda c: (c.settimeout(1.5), c.recv(256)), ctx)       # TLS, not in TLS_PORTS
    _ftp(21)
    have_snmp = True
    try:
        threading.Thread(target=_snmp_agent, daemon=True).start()
    except Exception:       # noqa: BLE001
        have_snmp = False
    time.sleep(2.5)

    from scanner.scanner_base import ScopeGuard
    import workflow.workflow_engine as we
    from workflow import gates
    from workflow.cache import WorkflowCache

    cache = WorkflowCache()
    ports = sorted(set(gates.IT_PORTS) | {8444, 6100})       # operator-added ports
    asyncio.run(we.run_engagement([H], ScopeGuard.from_list(["127.0.0.0/8"]), profile="it",
                                  rate=500, concurrency=100, timeout=2.0, disc_timeout=1.5,
                                  port_override=ports, cache=cache))
    for p in procs:
        p.terminate()
    facts = [{k: getattr(e.result, k) for k in ("scanner", "target", "timestamp", "port", "proto",
                                                 "status", "data", "evidence", "error")}
             for e in cache._store.values()]

    from app.detection.engine_bridge import detect_all_from_facts_traced
    _cve, posture, meta = detect_all_from_facts_traced(json.loads(json.dumps(facts, default=str)))
    got = {(p["rule_id"], p["port"]) for p in posture}
    print(f"{len(facts)} facts from {sorted({f['scanner'] for f in facts})}")
    for p in sorted(posture, key=lambda p: (p["port"] or 0, p["rule_id"])):
        print(f"{str(p['port']):>5} {p['severity']:8} {p['state']:10} {p['rule_id']}")
    cov = meta["coverage"]
    print(f"coverage: {cov.get('rules_assessed')}/{cov.get('rules_total')} assessed, "
          f"{cov.get('rules_blind')} blind {cov.get('blind_rule_ids')}")

    want = EXPECTED | (EXPECTED_SNMP if have_snmp else set())
    missing, unexpected = sorted(want - got), sorted(MUST_NOT & got)
    print("MISSING:", missing or "none"); print("MUST NOT APPEAR:", unexpected or "none")
    os._exit(1 if (missing or unexpected) else 0)


if __name__ == "__main__":
    sys.exit(main())
