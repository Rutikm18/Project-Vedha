#!/usr/bin/env python3
"""
push_results.py — push local scan facts to the manager via probe bootstrap.

Usage:
    python3 push_results.py \
        --manager http://13.127.147.205:18080 \
        --bootstrap-key <PROBE_BOOTSTRAP_KEY> \
        --facts /tmp/vedha_full_facts.jsonl \
        --targets 192.168.1.0/24

The script:
  1. Self-registers as a probe using the bootstrap key
  2. Creates an engagement for the target scope
  3. Marks the scan job as complete and submits the collected facts
  4. Triggers the detection engine to produce CVE findings
  5. Prints a summary of findings
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import httpx

def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_facts(path: str) -> list[dict]:
    facts = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            facts.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return facts


def main() -> None:
    ap = argparse.ArgumentParser(description="Push local probe facts to the manager")
    ap.add_argument("--manager", default="http://13.127.147.205:18080", help="Manager API base URL")
    ap.add_argument("--bootstrap-key", required=True, help="PROBE_BOOTSTRAP_KEY value set on the manager")
    ap.add_argument("--facts", required=True, help="Path to .jsonl facts file from pipeline.py")
    ap.add_argument("--targets", required=True, help="CIDR that was scanned (becomes engagement scope)")
    ap.add_argument("--name", default="mac-probe-01", help="Probe name to register as")
    ap.add_argument("--no-verify-tls", action="store_true", help="Skip TLS verification")
    ap.add_argument("--engagement-name", default="", help="Engagement name (default: auto)")
    args = ap.parse_args()

    verify = not args.no_verify_tls
    base = args.manager.rstrip("/")
    client = httpx.Client(base_url=base, timeout=30.0, verify=verify)

    facts = load_facts(args.facts)
    print(f"Loaded {len(facts)} fact records from {args.facts}")

    # ── 1. Bootstrap — register probe ─────────────────────────────────────────
    print(f"\n[1/4] Registering probe '{args.name}' via bootstrap key...")
    r = client.post("/agents/bootstrap", json={
        "bootstrap_key": args.bootstrap_key,
        "name": args.name,
        "capabilities": ["assessment", "discovery", "host_discovery", "port_scan",
                         "service_banner", "tls_scan", "web_scan", "db_fingerprint",
                         "smb_enum", "snmp_scan", "udp_scan"],
        "network_segments": [args.targets],
    })
    if r.status_code == 403:
        die("Bootstrap disabled on manager — set PROBE_BOOTSTRAP_KEY in the manager's .env")
    if r.status_code == 401:
        die("Wrong bootstrap key")
    r.raise_for_status()
    reg = r.json()
    agent_id = reg["agent_id"]
    agent_token = reg["token"]
    agent_headers = {"Authorization": f"Bearer {agent_token}"}
    print(f"  Registered as agent_id={agent_id}")

    # Need operator token to create engagement — try with an admin login
    # OR we use the agent token (it's a manager-issued JWT, try as-is)

    # ── 2. Create engagement ───────────────────────────────────────────────────
    print(f"\n[2/4] Creating engagement for scope {args.targets}...")
    eng_name = args.engagement_name or f"Mac Probe — {args.targets} — {time.strftime('%Y-%m-%d %H:%M')}"

    # Try with agent token first (the bootstrap agent has "agent" role)
    # Engagements require admin/manager role, so we need an operator login.
    # Prompt for it if not available.
    op_token = ""

    # Try: see if manager exposes a no-auth engagement create for probes
    r_eng = client.post(
        "/engagements",
        headers=agent_headers,
        json={"name": eng_name, "scope_cidrs": [args.targets]},
    )
    if r_eng.status_code in (401, 403):
        print("  Agent token can't create engagements (needs admin role).")
        print("  Enter manager admin credentials to create the engagement:")
        email = input("  Email: ").strip()
        password = input("  Password: ").strip()
        r_login = client.post("/auth/login", json={"email": email, "password": password})
        if r_login.status_code != 200:
            die(f"Login failed: {r_login.text}")
        op_token = r_login.json()["access_token"]
        r_eng = client.post(
            "/engagements",
            headers={"Authorization": f"Bearer {op_token}"},
            json={"name": eng_name, "scope_cidrs": [args.targets]},
        )
    r_eng.raise_for_status()
    eid = r_eng.json()["id"]
    print(f"  Engagement id={eid}")

    # ── 3. Submit facts as job result ──────────────────────────────────────────
    print(f"\n[3/4] Submitting {len(facts)} facts to manager...")

    op_hdr = {"Authorization": f"Bearer {op_token}"} if op_token else agent_headers

    # Create a discovery job for this engagement
    r_job = client.post(
        "/agents/jobs",
        headers=op_hdr,
        json={
            "engagement_id": eid,
            "job_type": "discovery",
            "params": {
                "scan_type": "assessment",
                "targets": [args.targets],
                "scope_cidrs": [args.targets],
            },
        },
    )
    r_job.raise_for_status()
    job_id = r_job.json()["id"]
    print(f"  Created job_id={job_id}")

    # Claim the job (mark it running)
    r_claim = client.post(
        f"/agents/{agent_id}/jobs",
        headers=agent_headers,
        params={"limit": 1},
    )
    r_claim.raise_for_status()

    # Build result bundle
    live_hosts = list({f["target"] for f in facts if f.get("target") and f.get("status") == "open"})
    services = [f for f in facts if f.get("status") == "open" and f.get("port")]

    result_bundle = {
        "scan_type": "assessment",
        "targets": [args.targets],
        "scope_cidrs": [args.targets],
        "hosts": [
            {"ip": ip, "alive": True, "open_ports": [
                f["port"] for f in services if f.get("target") == ip
            ]}
            for ip in live_hosts
        ],
        "services": services,
        "raw_facts": facts,
        "host_count": len(live_hosts),
        "service_count": len(services),
        "scanner_version": "probe-push-1.0",
    }

    r_result = client.post(
        f"/agents/{agent_id}/jobs/{job_id}/result",
        headers=agent_headers,
        json={"success": True, "result": result_bundle},
    )
    r_result.raise_for_status()
    print(f"  Facts submitted. Response: {r_result.json()}")

    # ── 4. Poll for findings ───────────────────────────────────────────────────
    print(f"\n[4/4] Waiting for detection engine to produce findings...")
    for attempt in range(12):
        time.sleep(5)
        r_findings = client.get(
            f"/findings",
            headers=op_hdr,
            params={"engagement_id": eid, "limit": 100},
        )
        if r_findings.status_code == 200:
            findings = r_findings.json()
            count = len(findings) if isinstance(findings, list) else findings.get("total", 0)
            if count:
                print(f"\n  {count} finding(s) detected!")
                items = findings if isinstance(findings, list) else findings.get("items", [])
                for f in items[:20]:
                    sev = f.get("severity", "?").upper()
                    cve = f.get("cve_id", f.get("title", "?"))
                    host = f.get("host", f.get("asset", {}).get("ip", "?"))
                    cvss = f.get("cvss_score", "")
                    print(f"    [{sev}] {cve}  host={host}  cvss={cvss}")
                break
            print(f"  Attempt {attempt+1}/12 — detection pending...", end="\r")
        else:
            print(f"  Findings poll: HTTP {r_findings.status_code}")
    else:
        print("\n  Detection still running — check the dashboard at http://13.127.147.205:3000")

    print(f"\nDone. Dashboard: http://13.127.147.205:3000")
    print(f"Engagement ID: {eid}")


if __name__ == "__main__":
    main()
