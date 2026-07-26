# How to Run the Probe — Operations Guide

Practical, copy-paste guide to running the probe: the different production methods,
every `showcase.sh` command, and the **step-by-step path to an actual vulnerability
assessment (VA) output**.

---

## 0. The mental model (read this first)

The probe is **collection only**. It produces **facts** ("port 53 is an open DNS
resolver", "SMBv1 is enabled") — it never emits a CVE (`finding_count: 0` by design).

```
  PROBE (facts)  ─────►  MANAGER detection engine (facts → CVEs)  ─────►  findings + risk
       │                                                                      ▲
       └── config findings (open resolver, SMBv1…) come straight from facts ──┘
       └── AUTHENTICATED inventory (SSH/WinRM) = the accurate version of everything
```

**A complete VA = probe facts + manager CVE correlation + (ideally) authenticated
inventory.** Running the probe alone gives you an exposure map and config findings, not
a full CVE assessment. Section 5 walks the full pipeline.

### ⚠️ Authorization
`scope` is the authorization boundary. Put **only ranges you own or are explicitly
authorized to test** in it. The probe refuses everything outside scope — but *you* set
scope. Never point it at third-party IPs.

---

## 1. Ways to run the probe

| Method | Manager needed? | Best for | Tool |
|---|---|---|---|
| **A. Showcase runner** | No | quick real scans, learning, demos | `showcase.sh` (§3) |
| **B. Standalone CLI** | No | scripted scans on a client host | `pipeline.py`, `dev.sh`, `workflow.cli`, `run_scan.py` (§2) |
| **C. Full production** | **Yes** | deployed appliance → findings in dashboard | `install.sh` + agent + manager (§4) |

All three run the **same scanning engine**. A/B print facts locally; C ships facts to the
manager for CVE detection.

---

## 2. Method B — Standalone CLI (no manager)

Runs on **pure stdlib** — any host with `python3 3.10+`, no `pip install` needed. Run it
on a host inside (or with routing access to) the target network.

```bash
cd probe

# Define the AUTHORIZED scope (one CIDR / IP / host per line)
echo "10.0.0.0/24" > scope.txt

# ── pipeline.py — the profile-aware funnel (recommended standalone tool) ──
python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile it            # full funnel
python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile it -o out.jsonl
python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile iot           # gentle (fragile devices)
python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile ot --listen-seconds 120  # PASSIVE only
python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile it --scanners host_discovery port_scan

# ── dev.sh — quick one-liners (auto-scopes to the target) ──
./dev.sh check 10.0.0.5      # reachability
./dev.sh scan  10.0.0.5      # full assessment → /tmp/probe_result.json
./dev.sh facts 10.0.0.5      # scan + pretty fact table
./dev.sh web   10.0.0.5      # only the web branch

# ── workflow.cli — explicit mode control ──
python3 -m workflow.cli -t 10.0.0.0/24 -s scope.txt --mode assessment -o result.json
python3 -m workflow.cli -t 10.0.0.0/24 -s scope.txt --mode service-specific --services web tls

# ── run_scan.py — flat orchestrator (per-scanner FP measurement) ──
python3 run_scan.py -t 10.0.0.0/24 -s scope.txt --all -o results.jsonl
python3 run_scan.py -t 10.0.0.0/24 -s scope.txt --scanners host_discovery port_scan web_scan --split-output ./runs/

# ── a single scanner in isolation ──
python3 -m scanner.tls_scanner -t 10.0.0.5 -s scope.txt
```

**Profiles** (the safety control): `it` = normal-speed active; `iot` = gentle (low rate,
long timeouts, no SMB/DB probing); `ot` = **passive only, zero active packets** (ICS/SCADA).

---

## 3. Method A — `showcase.sh` (all commands)

The demo/dev runner. Drives the **real engine** (`agent.engine.run_scan`) with use-cases,
scope, and excludes, and prints a readable summary. Run from the `probe/` directory.

| Command | What it does |
|---|---|
| `./showcase.sh --selftest` | **Live self-test**: stands up a fixture, scans it, asserts every function PASS/FAIL |
| `./showcase.sh --demo` | Scripted 7-step tour (capabilities + scope-safety refusals) on localhost |
| `./showcase.sh --list` | List all use-cases + raw scan types |
| `./showcase.sh` | Interactive menu: pick a use-case, enter target/scope/excludes |
| `./showcase.sh --use-case <id> --targets <t> --scope <s>` | Run one use-case directly |
| `./showcase.sh --use-case <id> --targets <t> --scope <s> --exclude <e>` | …with exclusions |
| `./showcase.sh --scan-type <type> --targets <t> --scope <s>` | Run a raw scan type |
| `… --raw` | Print the full JSON result bundle instead of the summary |
| `… --profile it\|iot\|ot` | Override the profile |

Examples:
```bash
./showcase.sh --use-case uc_full_assessment --targets 10.0.0.0/24 --scope 10.0.0.0/24
./showcase.sh --use-case uc_udp_service_exposure --targets 10.0.0.5 --scope 10.0.0.0/24
./showcase.sh --scan-type web_scan --targets 10.0.0.5 --scope 10.0.0.0/24 --exclude 10.0.0.1/32
./showcase.sh --use-case uc_windows_estate --targets 10.0.0.5 --scope 10.0.0.0/24 --raw
```
If `./showcase.sh` errors on permissions: `bash showcase.sh --selftest`.

### The 12 use-cases (`--list`)

| Use-case | Scan | Answers |
|---|---|---|
| `uc_discovery_only` | discovery/it | What's alive? |
| `uc_full_assessment` | assessment/it | Full funnel across all service branches |
| `uc_external_web_triage` | web_tls_scan/it | Exposed web + TLS surface |
| `uc_db_exposure` | db_fingerprint/it | Which DBs are exposed / unauthenticated? |
| `uc_windows_estate` | smb_enum/it | SMBv1? SMB signing required? |
| `uc_ot_passive` | passive_discovery/ot | OT/ICS — passive, zero packets |
| `uc_ai_endpoint_sweep` | mcp_discovery/it | Exposed AI / MCP endpoints |
| `uc_rescan_delta` | assessment/it | Re-assess (manager diffs vs prior) |
| `uc_iot_device_survey` | service_fingerprint/iot | IoT device inventory + banners |
| `uc_web_app_triage` | web_scan/it | HTTP methods, headers, tech stack |
| `uc_udp_service_exposure` | udp_scan/it | UDP + amplification (monlist, open recursion, memcached) |
| `uc_snmp_exposure` | snmp_scan/it | Default/weak SNMP communities |

---

## 4. Method C — Full production (agent + manager)

Deployed-appliance topology: the probe sits **inside the client network**, dials **out only**
to the manager, gets scoped jobs, scans, and ships facts back for CVE detection. Full detail
in `../PROBE_RUNBOOK.md`; the essentials:

```bash
# ── Vendor (one-time, on a trusted machine) ──
cd probe
python3 tools/issue_license.py keygen                       # signing keypair (keep private key secret)
docker build -f Dockerfile.sealed -t registry.example.com/vedha-probe:1.0 \
  --build-arg PROBE_LICENSE_PUBKEY=<hex> .
docker push registry.example.com/vedha-probe:1.0

# ── Client host gets its Host ID → vendor issues a license bound to it ──
docker run --rm registry.example.com/vedha-probe:1.0 hostid
python3 tools/issue_license.py issue --hostid <id> --customer "Acme" --days 365

# ── Client installs (Docker; use install.sh --native for systemd hosts) ──
curl -fsSL https://YOUR_HOST/install.sh -o install.sh && less install.sh   # inspect first
PROBE_IMAGE=registry.example.com/vedha-probe:1.0 \
PLATFORM_URL=https://manager.example.com \
OPERATOR_EMAIL=ops@acme.com OPERATOR_PASSWORD=*** \
PROBE_LICENSE=<token> sh install.sh
docker logs -f vedha-probe                                  # watch it register + poll
```

**Try the whole stack locally first** (manager + probe on one machine):
```bash
cd "$(git rev-parse --show-toplevel)"
make up        # postgres + redis + migrate + API + dashboard
#   then follow Probe_testing.md §3–§10
```

---

## 5. Step-by-step: getting an actual VA output

The desired end state is **prioritized findings**, not raw facts. Do it in this order.

### Stage 1 — Scope & discovery (what exists)
```bash
cd probe
echo "10.0.0.0/24" > scope.txt
python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile it --scanners host_discovery port_scan
```
→ live hosts + open ports. Confirms scope and reachability before you go deep.

### Stage 2 — Full collection (facts)
```bash
./showcase.sh --use-case uc_full_assessment --targets 10.0.0.0/24 --scope 10.0.0.0/24
# or: python3 pipeline.py -t 10.0.0.0/24 -s scope.txt --profile it -o facts.jsonl
```
→ services, banners, TLS/web/SMB/DB/SNMP/UDP facts. **Config findings already appear here**
(e.g. `open_recursion=True` = open DNS resolver, `smbv1_enabled=True`, `unauthenticated_read=True`).

### Stage 3 — Authenticated inventory (accurate versions) — *biggest quality jump*
For real patch-level CVEs, give credentials so the probe reads installed packages/KBs:
- **Windows** hosts (135/445 open): `windows_collector` over WinRM.
- **Linux** hosts (22 open): `ssh_collector`.
This is the only reliable source of version data for CVE matching. Runs via the agent/manager
job params (`ssh_creds` / `win_creds`) or the collectors directly.

### Stage 4 — Detection (facts → CVE findings)
Push the facts through the manager's detection engine:
```bash
cd "$(git rev-parse --show-toplevel)"
make up                                    # bring up the manager
# then (PROBE_RUNBOOK.md §C): login → create engagement (scope) → enqueue job → probe scans
# → detection_engine correlates facts → CVEs (CVSS / KEV / EPSS) → findings
curl -s "https://manager/findings?engagement_id=$EID" -H "Authorization: Bearer $TOKEN"
```

### Stage 5 — Triage & prioritize (the VA report)
Findings ranked by CVSS + KEV (known-exploited) + EPSS (exploit likelihood), plus the config
findings from Stage 2. That ranked list **is** the vulnerability assessment output.

```
Stage 1 discovery ─► Stage 2 facts ─► Stage 3 auth inventory ─► Stage 4 CVE detection ─► Stage 5 prioritized findings
   (what's here)       (+ config          (accurate               (facts → CVEs)            (the VA report)
                        findings)          versions)
```

---

## 6. Reading the output

| You see | It means | Is it a "vuln"? |
|---|---|---|
| `status: open`, a port, a banner | exposure / inventory | No — surface only |
| `open_recursion`, `smbv1_enabled`, `unauthenticated_read`, `signing_required=False`, weak SNMP | **config finding** (direct observation) | **Yes** — reportable now, no CVE engine needed |
| `finding_count: 0` on the probe | probe never emits CVEs by design | — CVEs come from the manager |
| manager `findings[]` with `cve_id`, `cvss`, `kev` | **CVE finding** | **Yes** — the full assessment |

---

## 7. Quick reference

```bash
# fastest "is it working" check
./showcase.sh --selftest

# fastest real scan of a network you own
python3 pipeline.py -t <cidr> -s scope.txt --profile it -o facts.jsonl

# full pipeline to a VA report
#   pipeline.py/showcase (facts) → auth inventory → make up + engagement/job (CVEs) → findings
```

> A probe-side **Triage stage** (in design) will summarize the Stage-2 config findings +
> recommended next actions directly in the probe output — see
> `docs/superpowers/specs/` once it lands.
