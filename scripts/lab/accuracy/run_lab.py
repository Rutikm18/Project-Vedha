#!/usr/bin/env python3
"""
run_lab.py — scan the accuracy lab with the probe's real scanners, run the manager's
detection engine on the facts, and grade the findings against ground_truth.json.

    python scripts/lab/accuracy/run_lab.py                 # up, scan all, grade, down
    python scripts/lab/accuracy/run_lab.py --only tls-weak tls-strong --keep

Needs: Docker (compose v2), a Python with the probe's requirements (--probe-python,
default: this interpreter), and one with the manager engine's (--engine-python,
default: this interpreter). Writes results/<stamp>/ with the raw facts per target,
findings.json and report.md. Exit code 1 when any expectation fails.

Grading (ground_truth.json): per target, `expect` lists rule ids / CVE ids that must
be reported, `absent` lists ones that must not be, `absent_prefixes` whole families
that must not appear, and `cve_max` caps the customer-facing CVE count (a clean
control's guard against version-match noise), `known_gaps` names a true weakness the
pipeline is known to miss and who owns the fix (reported, not counted as a failure,
and flagged if it starts being reported). Every expectation is about the
customer-facing finding set (posture + `cve`), never the product-presence bucket.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROBE = REPO / "probe"
ENGINE = REPO / "manager" / "detection_engine"


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, **kw)


def wait_port(ip: str, port: int, timeout: float = 90.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((ip, port), timeout=2):
                return True
        except OSError:
            time.sleep(1)
    return False


def scan(target: dict, outdir: Path, probe_python: str) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [probe_python, "-m", "scanner.run_all", "-t", target["ip"], "--outdir", str(outdir),
           "--profile", "full", "--rate", "4000", "--concurrency", "800", "--timeout", "1.5"]
    with (outdir / "run_all.out").open("w") as log:
        subprocess.run(cmd, cwd=PROBE, stdout=log, stderr=subprocess.STDOUT, check=False,
                       timeout=900)
    return sorted(p for p in outdir.glob("*.jsonl") if p.stat().st_size)


_DETECT = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
from pipeline import run_full_detection
res = run_full_detection(sys.argv[3:])
out = {
  "posture": [{"id": f.rule_id, "severity": f.severity, "state": f.state,
               "port": f.port, "title": f.title} for f in res["posture"]],
  "cve": [{"id": f.cve_id, "state": f.state.value, "basis": f.match_basis,
           "version": f.matched_version, "port": f.port, "fixed": f.fixed_version,
           "priority": f.priority} for f in res["cve"]],
  "presence": [{"id": f.cve_id, "basis": f.match_basis} for f in res["cve_product_presence"]],
  "assets": res["counts"]["assets"],
}
open(sys.argv[2], "w").write(json.dumps(out, indent=1, default=str))
"""


def detect(paths: list[Path], out: Path, engine_python: str) -> dict:
    sh([engine_python, "-c", _DETECT, str(ENGINE), str(out), *map(str, paths)])
    return json.loads(out.read_text())


def grade(name: str, spec: dict, res: dict) -> list[str]:
    reported = {f["id"] for f in res["posture"]} | {f["id"] for f in res["cve"]}
    fails = []
    for rid in spec.get("expect", []):
        if rid not in reported:
            fails.append(f"{name}: expected {rid}, not reported")
    for rid in spec.get("absent", []):
        if rid in reported:
            fails.append(f"{name}: {rid} reported but must not be")
    for prefix in spec.get("absent_prefixes", []):
        hits = sorted(r for r in reported if r.startswith(prefix))
        if hits:
            fails.append(f"{name}: {prefix}* must not appear, got {hits}")
    cap = spec.get("cve_max")
    if cap is not None and len(res["cve"]) > cap:
        fails.append(f"{name}: {len(res['cve'])} customer CVE findings > cap {cap}")
    for sev_rule, sev in (spec.get("severity") or {}).items():
        got = {f["severity"] for f in res["posture"] if f["id"] == sev_rule}
        if got and sev not in got:
            fails.append(f"{name}: {sev_rule} severity {sorted(got)} != {sev}")
    for rid in spec.get("known_gaps", {}):
        if rid in reported:
            fails.append(f"{name}: known gap {rid} is now reported — move it to expect")
    if res.get("assets", 0) == 0:
        fails.append(f"{name}: no asset ingested (scan produced nothing usable)")
    return fails


def report(stamp: str, results: dict, fails: list[str], truth: dict) -> str:
    lines = [f"# Accuracy lab run {stamp}", "",
             f"**{'PASS' if not fails else 'FAIL'}** — {len(results)} targets, "
             f"{len(fails)} failed expectation(s).", ""]
    for name, res in results.items():
        spec = truth[name]
        lines += [f"## {name} ({spec['ip']}) — {spec['role']}", "",
                  f"_{spec['why']}_", ""]
        lines += [f"- posture `{f['id']}` {f['severity']}/{f['state']} port {f['port']}: {f['title']}"
                  for f in res["posture"]] or ["- no posture findings"]
        lines += [f"- CVE `{f['id']}` {f['state']} ({f['basis']}) {f['version']} → fix {f['fixed']}"
                  f" priority {f['priority']}" for f in res["cve"]]
        if res["presence"]:
            lines.append(f"- product presence only (not findings): {len(res['presence'])} CVE(s)")
        lines += [f"- **known gap** `{rid}` — {why}" for rid, why in spec.get("known_gaps", {}).items()]
        own = [x for x in fails if x.startswith(f"{name}:")]
        lines += ["", *(f"**FAIL** {x}" for x in own)] if own else ["", "All expectations met."]
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*", help="target names (default: all)")
    ap.add_argument("--keep", action="store_true", help="leave the lab running")
    ap.add_argument("--no-up", action="store_true", help="the lab is already running")
    ap.add_argument("--probe-python", default=sys.executable)
    ap.add_argument("--engine-python", default=sys.executable)
    args = ap.parse_args()

    truth = json.loads((HERE / "ground_truth.json").read_text())
    names = args.only or list(truth)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outroot = HERE / "results" / stamp
    compose = ["docker", "compose", "-f", str(HERE / "docker-compose.yml")]

    if not args.no_up:
        if not (HERE / "certs" / "weak.crt").exists():
            sh([args.probe_python, str(HERE / "gen_certs.py")])
        sh(compose + ["up", "-d", *names])
    results, fails = {}, []
    try:
        for name in names:
            spec = truth[name]
            if not wait_port(spec["ip"], spec["port"]):
                fails.append(f"{name}: {spec['ip']}:{spec['port']} never came up")
                continue
            time.sleep(spec.get("settle", 2))
            paths = scan(spec, outroot / name, args.probe_python)
            res = detect(paths, outroot / name / "findings.json", args.engine_python)
            results[name] = res
            fails += grade(name, spec, res)
            print(f"{name:20} posture={len(res['posture'])} cve={len(res['cve'])} "
                  f"presence={len(res['presence'])} "
                  f"{'ok' if not [f for f in fails if f.startswith(name + ':')] else 'FAIL'}",
                  flush=True)
    finally:
        if not args.keep and not args.no_up:
            subprocess.run(compose + ["down", "-v"], check=False)
    outroot.mkdir(parents=True, exist_ok=True)
    (outroot / "report.md").write_text(report(stamp, results, fails, truth))
    print("\n".join(fails) or "all expectations met")
    print(f"report: {outroot / 'report.md'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
