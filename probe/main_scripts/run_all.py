#!/usr/bin/env python3
"""
run_all.py — sequential orchestrator for the main_scripts scanners.

Runs every scanner against ONE target, host-discovery first, and saves each
scanner's JSONL output into a timestamped directory. Wide->narrow: the TCP scan
discovers OPEN ports, and only those are fed to the port-specific scanners
(service_banner / tls / web / db), so nothing re-scans the whole host.

    python -m main_scripts.run_all -t 192.168.1.70
    python -m main_scripts.run_all -t 192.168.1.70 --profile full
    python -m main_scripts.run_all -t 192.168.1.70 --profile top1000 --outdir /tmp/scan70

Read-only and scope-enforced (each scanner loads the same ScopeGuard allowlist,
which this runner writes from -t). No exploitation, no brute force. A scanner that
errors is logged and the run continues — one failed stage never aborts the rest.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Directory that contains the main_scripts package (so `-m main_scripts.X` works).
_PKG_ROOT = Path(__file__).resolve().parent.parent

# Port-specific scanners only fire on OPEN ports that plausibly speak their
# protocol — discovered from the TCP scan, never assumed from a fixed list.
_TLS_CANDIDATES = {443, 8443, 993, 995, 465, 636, 989, 990, 5061, 3389}
_HTTP_CANDIDATES = {80, 81, 443, 591, 8000, 8008, 8080, 8081, 8443, 8888, 9000}
_DB_CANDIDATES = {1433, 1521, 3306, 5432, 5984, 6379, 9042, 11211, 27017}
_SSH_CANDIDATES = {22, 2222}
_LDAP_CANDIDATES = {389, 636, 3268, 3269}
_DNS_CANDIDATES = {53}
_NFS_CANDIDATES = {111, 2049}
_FTP_CANDIDATES = {21}
_RSYNC_CANDIDATES = {873}
_VNC_CANDIDATES = {5900, 5901}
_SMTP_CANDIDATES = {25, 587}
_MSRPC_CANDIDATES = {135}
_PRINTER_CANDIDATES = {9100, 631}


def _log(outdir: Path, msg: str) -> None:
    line = f"{datetime.now().strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True)
    with (outdir / "run.log").open("a") as fh:
        fh.write(line + "\n")


def _run_stage(outdir: Path, name: str, module: str, extra: list[str]) -> Path | None:
    """Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl."""
    out_file = outdir / f"{name}.jsonl"
    argv = [sys.executable, "-m", f"main_scripts.{module}", *extra, "-o", str(out_file)]
    _log(outdir, f"[{name}] $ {' '.join(argv[2:])}")
    try:
        proc = subprocess.run(argv, cwd=_PKG_ROOT, capture_output=True,
                              text=True, timeout=1800)
        if proc.returncode != 0:
            _log(outdir, f"[{name}] EXIT {proc.returncode}: "
                          f"{proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else '?'}")
        else:
            _log(outdir, f"[{name}] done -> {out_file.name}")
    except subprocess.TimeoutExpired:
        _log(outdir, f"[{name}] TIMEOUT after 1800s")
        return None
    return out_file if out_file.exists() else None


def _read_jsonl(path: Path | None) -> list[dict]:
    if not path or not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def _open_tcp_ports(records: list[dict]) -> list[int]:
    return sorted({r["port"] for r in records
                   if r.get("proto") == "tcp" and r.get("status") == "open"
                   and r.get("port") is not None})


def _ports_arg(ports) -> str:
    return ",".join(str(p) for p in sorted(ports))


def main() -> None:
    ap = argparse.ArgumentParser(description="Run all main_scripts scanners on one target")
    ap.add_argument("-t", "--target", required=True, help="single target IP/host")
    ap.add_argument("--profile", default="top1000",
                    choices=["quick", "top100", "top1000", "full"],
                    help="TCP coverage profile (default top1000)")
    ap.add_argument("--outdir", default=None, help="output directory (default: ./scans/...)")
    ap.add_argument("--rate", default="300")
    ap.add_argument("--concurrency", default="200")
    ap.add_argument("--timeout", default="2.0")
    ap.add_argument("--vuln-db", default=None,
                    help="offline CVE mirror (SQLite) to correlate facts against; "
                         "if given and present, writes cve_findings.jsonl")
    ap.add_argument("--exposed", action="store_true",
                    help="treat this target as internet-exposed (adds the exposure "
                         "weight to CVE risk scores). Default: internal — no boost. "
                         "An internal enterprise scan should NOT pass this.")
    args = ap.parse_args()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = args.target.replace(".", "_").replace(":", "_")
    outdir = Path(args.outdir) if args.outdir else _PKG_ROOT / "scans" / f"scan_{safe}_{stamp}"
    outdir.mkdir(parents=True, exist_ok=True)

    # Scope file authorizing exactly this target — the safety control every
    # scanner enforces before touching the wire.
    scope = outdir / "scope.txt"
    scope.write_text(args.target + "\n")
    common = ["-t", args.target, "-s", str(scope), "--rate", args.rate,
              "--concurrency", args.concurrency, "--timeout", args.timeout]

    _log(outdir, f"=== run_all target={args.target} profile={args.profile} outdir={outdir} ===")

    # ── Stage 1: host discovery (informational — we scan regardless, since a
    #    live Windows host commonly blocks ICMP and would look 'down'). ──
    disc = _read_jsonl(_run_stage(outdir, "01_host_discovery", "host_discovery", common))
    alive = any(r.get("status") in ("open", "reachable", "up", "alive")
                or (r.get("data") or {}).get("alive") for r in disc)
    _log(outdir, f"host_discovery: {'appears LIVE' if alive else 'no positive liveness (continuing anyway)'}")

    # ── Stage 2: TCP port scan (discovers the OPEN set that gates later stages) ──
    tcp = _read_jsonl(_run_stage(outdir, "02_port_scan", "port_scanner",
                                 common + ["--profile", args.profile, "--report-closed"]))
    open_tcp = _open_tcp_ports(tcp)
    _log(outdir, f"open TCP ports: {open_tcp or '(none)'}")

    # ── Stages 3-6: host-wide scanners that don't need a port list ──
    _run_stage(outdir, "03_udp", "udp_scanner", common)
    _run_stage(outdir, "04_os_fingerprint", "os_fingerprint", common)
    _run_stage(outdir, "05_snmp", "snmp_scanner", ["-t", args.target, "-s", str(scope),
                                                   "--timeout", args.timeout])
    _run_stage(outdir, "05b_ipmi", "ipmi_scanner", ["-t", args.target, "-s", str(scope),
                                                    "--timeout", args.timeout])
    if 445 in open_tcp or 139 in open_tcp:
        _run_stage(outdir, "06_smb", "smb_scanner", common)
        if 445 in open_tcp:
            _run_stage(outdir, "06b_smb_enum", "smb_enum_scanner", common)
    else:
        _log(outdir, "[06_smb] skipped (445/139 not open)")

    # ── Stages 7-9: port-specific scanners, fed only the relevant OPEN ports ──
    if open_tcp:
        _run_stage(outdir, "07_service_banner", "service_banner",
                   common + ["-p", _ports_arg(open_tcp)])
        tls_ports = sorted(set(open_tcp) & _TLS_CANDIDATES)
        if tls_ports:
            _run_stage(outdir, "08_tls", "tls_scanner", common + ["-p", _ports_arg(tls_ports)])
        http_ports = sorted(set(open_tcp) & _HTTP_CANDIDATES)
        if http_ports:
            _run_stage(outdir, "09_web", "web_scanner", common + ["-p", _ports_arg(http_ports)])
        db_ports = sorted(set(open_tcp) & _DB_CANDIDATES)
        if db_ports:
            _run_stage(outdir, "10_db", "db_scanner", common + ["-p", _ports_arg(db_ports)])
        ssh_ports = sorted(set(open_tcp) & _SSH_CANDIDATES)
        if ssh_ports:
            _run_stage(outdir, "11_ssh", "ssh_scanner", common + ["-p", _ports_arg(ssh_ports)])
        ldap_ports = sorted(set(open_tcp) & _LDAP_CANDIDATES)
        if ldap_ports:
            _run_stage(outdir, "12_ldap", "ldap_scanner", common + ["-p", _ports_arg(ldap_ports)])
        if 53 in open_tcp:
            _run_stage(outdir, "13_dns", "dns_scanner", common)
        if 2049 in open_tcp or 111 in open_tcp:
            _run_stage(outdir, "14_nfs", "nfs_scanner", common)
        if 21 in open_tcp:
            _run_stage(outdir, "15_ftp", "ftp_scanner", common + ["-p", "21"])
        if 873 in open_tcp:
            _run_stage(outdir, "16_rsync", "rsync_scanner", common + ["-p", "873"])
        vnc_ports = sorted(set(open_tcp) & _VNC_CANDIDATES)
        if vnc_ports:
            _run_stage(outdir, "17_vnc", "vnc_scanner", common + ["-p", _ports_arg(vnc_ports)])
        smtp_ports = sorted(set(open_tcp) & _SMTP_CANDIDATES)
        if smtp_ports:
            _run_stage(outdir, "18_smtp", "smtp_scanner", common + ["-p", _ports_arg(smtp_ports)])
        if 135 in open_tcp:
            _run_stage(outdir, "19_msrpc", "msrpc_scanner", common + ["-p", "135"])
        printer_ports = sorted(set(open_tcp) & _PRINTER_CANDIDATES)
        if printer_ports:
            _run_stage(outdir, "20_printer", "printer_scanner",
                       common + ["-p", _ports_arg(printer_ports)])
    else:
        _log(outdir, "no open TCP ports — skipping service/tls/web/db stages")

    # ── Inference layer: fuse everything into a device-role guess ──
    from main_scripts.device_classifier import classify_from_results
    from main_scripts.scanner_base import ScanResult

    all_records = (tcp + _read_jsonl(outdir / "03_udp.jsonl")
                   + _read_jsonl(outdir / "04_os_fingerprint.jsonl")
                   + _read_jsonl(outdir / "07_service_banner.jsonl"))
    shaped = [ScanResult(scanner=r.get("scanner", "?"), target=r.get("target", args.target),
                         port=r.get("port"), proto=r.get("proto"),
                         status=r.get("status"), data=r.get("data") or {})
              for r in all_records]
    device = classify_from_results(shaped)

    # ── Findings layer: turn every collected fact into vulnerability findings ──
    # Interpretation only (no wire access). Config/hygiene/exposure findings —
    # never CVE claims (CVE detection needs the manager's pinned vuln DB).
    from main_scripts.findings import run_findings, summarize as summarize_findings

    all_facts: list[dict] = []
    for jf in sorted(outdir.glob("*.jsonl")):
        if jf.name in ("findings.jsonl", "cve_findings.jsonl"):  # never re-ingest our own output
            continue
        all_facts.extend(_read_jsonl(jf))
    findings = run_findings(all_facts)
    findings_path = outdir / "findings.jsonl"
    with findings_path.open("w") as fh:
        for fnd in findings:
            fh.write(json.dumps(fnd.to_dict(), default=str) + "\n")
    findings_summary = summarize_findings(findings)
    _log(outdir, f"findings: {findings_summary['total']} total, "
                 f"{findings_summary['actionable']} actionable -> {findings_path.name}")
    for fnd in findings[:10]:
        loc = f"{fnd.target}:{fnd.port}" if fnd.port else fnd.target
        _log(outdir, f"  [{fnd.severity.upper():8}] {loc:22} {fnd.title}")

    # ── CVE correlation (optional, manager-side): if an offline vuln mirror is
    #    supplied, map the CPE identities the probe emitted to prioritized CVEs.
    #    This is a SEPARATE layer — the probe itself asserted no CVE; findings
    #    here are banner-derived (confidence 'medium', "verify patch level"). ──
    cve_summary = None
    if args.vuln_db:
        db_path = Path(args.vuln_db)
        if not db_path.exists():
            _log(outdir, f"[cve] --vuln-db {db_path} not found — skipping correlation")
        else:
            from cve.vulndb import VulnDB
            from cve.correlator import (correlate, mirror_age_note,
                                        summarize as summarize_cves)
            db = VulnDB(str(db_path))
            # Exposure is an operator assertion, not an assumption: only boost risk
            # when --exposed is set. Blanket-marking every scanned host as exposed
            # made the weight uniform (i.e. carry no signal) on internal scans.
            exposed = {args.target} if args.exposed else set()
            try:
                # Surface mirror age up front — a stale mirror misses new CVEs.
                _log(outdir, f"[cve] {mirror_age_note(db)}")
                cve_findings = correlate(all_facts, db, exposed_targets=exposed)
            finally:
                db.close()
            cve_path = outdir / "cve_findings.jsonl"
            with cve_path.open("w") as fh:
                for cf in cve_findings:
                    fh.write(json.dumps(cf.to_dict(), default=str) + "\n")
            cve_summary = summarize_cves(cve_findings)
            _log(outdir, f"cve: {cve_summary['total']} candidate CVEs, "
                         f"{cve_summary['kev']} KEV -> {cve_path.name}")
            for cf in cve_findings[:10]:
                loc = f"{cf.target}:{cf.port}" if cf.port else cf.target
                kev = " KEV" if cf.kev else ""
                _log(outdir, f"  [{cf.risk_band.upper():8}] {loc:22} "
                             f"{cf.cve_id} (risk {cf.risk_score}{kev})")

    summary = {
        "target": args.target,
        "profile": args.profile,
        "started": stamp,
        "host_alive_hint": alive,
        "open_tcp_ports": open_tcp,
        "device_classification": device,
        "findings_summary": findings_summary,
        "top_findings": [f.to_dict() for f in findings[:10]],
        "cve_summary": cve_summary,
        "outputs": sorted(p.name for p in outdir.glob("*.jsonl")),
    }
    (outdir / "SUMMARY.json").write_text(json.dumps(summary, indent=2, default=str))
    _log(outdir, f"device: {device['device_type']} (conf {device['confidence']}) "
                 f"role_detail={device['role_detail']}")
    _log(outdir, f"=== done. results in {outdir} ===")
    print("\n" + json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
