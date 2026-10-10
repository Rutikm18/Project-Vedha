#!/usr/bin/env python3
"""Fidelity check: do the lab EMULATORS look weak to the REAL Vedha probe scanners?

selftest.sh proves the emulators match the lab's own verifier. This proves they match
what the shipped scanners actually parse, so an "emulated" scenario really exercises the
scanner code. Run from anywhere; needs only the repo (no root, binds 127.0.0.1).

    python3 probe/tests/rig/ubuntu-weak-lab/selftest_vs_scanners.py
"""
import asyncio
import os
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))      # .../probe
sys.path.insert(0, PROBE_ROOT)
EMU = os.path.join(HERE, "lab_emulators.py")
H = "127.0.0.1"
ENV = dict(os.environ, VEDHA_LAB_ROOTDESC_PORT="18500")

EMULATORS = [
    ("rtsp", ["--tcp", "18554"]), ("cwmp", ["--tcp", "18547"]), ("adb", ["--tcp", "18556"]),
    ("ollama", ["--tcp", "18434"]), ("ssdp", ["--udp", "18900"]), ("ntp", ["--udp", "18123"]),
    ("sip", ["--tcp", "18060", "--udp", "18060"]), ("ipmi", ["--udp", "18623"]),
]

results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name:36} {detail}")


def udp_once(port, payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)
    try:
        s.sendto(payload, (H, port))
        return s.recvfrom(65535)[0]
    finally:
        s.close()


def main():
    try:
        from scanner import iot_scanner as iot
        from scanner import ipmi_scanner as ipmi
        from scanner import mobile_scanner as mob
        from scanner import udp_scanner as udp
    except Exception as exc:                                    # missing optional deps etc.
        print(f"cannot import the probe scanners ({exc!r}); run inside the probe venv")
        return 2
    procs = [subprocess.Popen([sys.executable, EMU, "serve", n, "--bind", H, *a], env=ENV,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
             for n, a in EMULATORS]
    time.sleep(1.5)
    try:
        async def tcp_probes():
            rtsp = await iot._probe_rtsp(H, 18554, 4)
            check("iot._probe_rtsp (T19)", bool(rtsp and rtsp.get("public_methods")), rtsp)
            cw = await iot._probe_cwmp(H, 18547, 4)
            check("iot._probe_cwmp (T20)", bool(cw and cw.get("cwmp_indicators")), cw)
            adb = await mob._probe_adb(H, 18556, 4)
            check("mobile._probe_adb (T21)", bool(adb and adb.get("adb_command") == "CNXN"), adb)
        asyncio.run(tcp_probes())

        ssdp = iot._probe_ssdp_sync(H, 18900, 4)
        check("iot._probe_ssdp_sync (G02)", bool(ssdp), ssdp)

        mon = udp_once(18123, udp._ntp_monlist_probe())
        check("udp.interpret_ntp_monlist (G04)", udp.interpret_ntp_monlist(mon), f"{len(mon)} bytes")
        sip = udp.interpret_sip(udp_once(18060, udp._sip_probe(H)))
        check("udp.interpret_sip (G09)", sip.get("sip_response", "").startswith("SIP/2.0 200"), sip)
        resp = udp_once(18623, ipmi.build_open_session_request())
        parsed = ipmi.parse_open_session_response(resp)
        check("ipmi.parse_open_session (T05)", bool(parsed and parsed.get("cipher_zero")), parsed)
    finally:
        for p in procs:
            p.terminate()
        for p in procs:
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
    print(f"\nscanner fidelity: {sum(results)} passed, {len(results) - sum(results)} failed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
