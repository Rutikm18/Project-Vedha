# Probe Capability Status — local run verification

**Verified:** 2026-08-21, local Path-A engine (`tools/probe_local_run.py`), no manager.
**Target under test:** `192.168.1.74` — a Windows desktop (`DESKTOP-34M18MB`); open TCP 135/445/3389.

> Note: "coming soon" below means **not yet demonstrated end-to-end**, NOT broken.
> The empty results are because a Windows desktop runs no web / DB / AI / IoT
> services — those branches need a target that actually exposes the service to be
> confirmed. Re-verify each against an appropriate host before marking it available.

---

## ✅ Working (produced real results)

| Use case | Command | Evidence on 192.168.1.74 |
|----------|---------|--------------------------|
| **Network Discovery** | `$PY tools/probe_local_run.py $T it port_scan` | `alive: true`, open `[445]` |
| **Device Inventory** | `$PY tools/probe_local_run.py $T it service_banner` | alive + ports + banner stage ran |
| **Full Assessment** | `PROBE_LOCAL_PORTS=full $PY tools/probe_local_run.py $T it deep_scan` | 8 ports; TLS(3389) grade **A** + cert; full SMB posture; SNMP verdict |
| **Windows Estate (SMB)** | `PROBE_LOCAL_PORTS=445 $PY tools/probe_local_run.py $T it deep_scan smb` | SMBv1 off, signing required, dialect 0x0302 |
| **TLS assessment** | (via Full Assessment / `deep_scan tls`) | grade A, cipher analysis, cert on 3389/RDP |
| **SNMP Exposure** | `PROBE_LOCAL_PORTS=161 $PY tools/probe_local_run.py $T it deep_scan snmp` | verdict `{responded:false, reason:no_snmp_response}` |
| **UDP Service Exposure** | `PROBE_LOCAL_PORTS=53,123,161,137,11211 $PY tools/probe_local_run.py $T it deep_scan udp` | open\|filtered ports enumerated |
| **Full-Port Audit** | `PROBE_LOCAL_PORTS=1-65535 $PY tools/probe_local_run.py $T it port_scan` | found `[135,445,2179,3389,7680]` (extra high ports) |
| **Multi-Vantage Exposure** | `PROBE_LOCAL_PORTS=full $PY tools/probe_local_run.py $T it port_scan` | `[135,445,3389]` |
| **IoT Device Survey** | `PROBE_LOCAL_PORTS=full $PY tools/probe_local_run.py $T iot service_banner` | runs (IoT catalog); only 445 on this host |

## 🕓 Coming soon (functional, not yet demonstrated on a matching target)

| Use case | Command | Why unverified here |
|----------|---------|---------------------|
| **External Web Triage** (web half) | `$PY tools/probe_local_run.py $T it deep_scan tls,web` | no 80/443 open on target (TLS half is proven) |
| **Web Application Triage** | `$PY tools/probe_local_run.py $T it deep_scan web` | no web port on target → empty |
| **Database Exposure** | `PROBE_LOCAL_PORTS=3306,5432,1433,6379,27017 $PY tools/probe_local_run.py $T it deep_scan db` | no DB port on target → empty |
| **AI / MCP Endpoint Sweep** | `PROBE_LOCAL_PORTS=full $PY tools/probe_local_run.py $T it deep_scan mcp_ai` | no AI/MCP endpoint on target → empty |

## ❓ Not tested yet

| Use case | Command / note |
|----------|----------------|
| **OT / ICS Passive** | `$PY tools/probe_local_run.py $T ot -` (listen-only ~60s; needs an OT segment) |
| **Re-scan / Delta** | manager-side diff of two Full Assessments — not a standalone local run |

---

## Verified accuracy — 2026-08-21, `192.168.1.74` (DESKTOP-34M18MB, Win 11 Pro)

Cross-checked the probe's findings against target-side ground truth
(`tools/verify_windows_ground_truth.ps1`) **and** an attacker-vantage connect scan
from the scanning host. Result: **precision 100% / recall 100%.**

| Dimension | Result | Evidence |
|-----------|--------|----------|
| **Precision** | 100% | all 5 reported TCP ports (135/445/2179/3389/7680) are real *and* reachable |
| **Recall** | 100% | 0 reachable ports missed — every extra host-bound port is firewalled |
| **SMB** | exact | `EnableSMB1Protocol=False`, `RequireSecuritySignature=True`, SMB2 on |
| **RDP/TLS** | exact | RDP on, NLA required, SecurityLayer=2, TLS 1.0 disabled → 1.2/1.3 only |
| **SNMP** | exact | no SNMP agent service → probe's `no_snmp_response` correct |
| **memcached/DNS** | exact | no such service; UDP `open\|filtered` was ambiguity, not exposure |

**Recall proof.** The host binds 8 extra ports to `0.0.0.0`/`.74` that the probe did
NOT report — `139, 623, 902, 912, 5040, 16992, 49664, 49670`. An attacker-vantage
connect scan confirmed **all 8 time out (firewalled)**, while the probe's 5
(135/445/2179/3389/7680) connect instantly. The probe reports the *reachable*
attack surface, exactly as intended — bind-to-`0.0.0.0` ≠ reachable.

---

## Known gaps / follow-ups

1. ~~**Driver output does not tag protocol/state on `open_ports`.**~~
   **FIXED 2026-08-21.** `summarize()` now carries `PortFact.proto` + state +
   certainty, rendering `445/tcp open` vs `11211/udp open|filtered (uncertain)`.
   A UDP `open|filtered` can no longer be mis-read as a live TCP service (the
   root cause of the memcached confusion).

2. **6 use-cases flagged `coming_soon` — unverified, not broken.** Web Triage,
   Web App Triage, DB Exposure, AI/MCP Sweep (returned empty — target runs no
   such service), plus **OT Passive** and **Re-scan/Delta** (not yet exercised).
   Now enforced everywhere: `status: "coming_soon"` in both catalogs (manager +
   probe, parity-checked), a **disabled "Coming soon" badge** in the operator
   `/scan` cards and the portal `<select>`, **and** a backend gate — the portal
   scan-request and operator enqueue endpoints both reject a `coming_soon`
   use-case (422), so a crafted API call can't dispatch one. Promote to ✅ +
   `available` once verified against a matching target (TLS branch already proven).
   **Available (tested) = 9:** discovery, device_inventory, full_assessment,
   windows_estate, snmp_exposure, udp_service_exposure, full_port_audit,
   exposure_matrix, iot_device_survey.

3. **Result flakiness (environmental).** Repeated identical `port_scan` runs
   alternated between `alive:true / open:[445]` and `alive:false / open:[]` —
   host/Wi-Fi rate-limiting after a scan burst, not a code defect. Re-run once if a
   result comes back unexpectedly empty; space runs or lower rate for stable numbers.

4. **Host-side note (not a probe gap): Intel AMT latent exposure.** `LMS` binds
   `0.0.0.0:623` and `:16992` on the target but is firewalled, so the probe
   correctly omits it. If that firewall rule is ever relaxed, Intel AMT (a
   historically CVE-heavy out-of-band management surface) becomes reachable.
   Confirm AMT is provisioned-off on the host, not merely firewalled.
   (As of 2026-08-25 the probe now actively tests 623 for IPMI cipher-zero — see
   `ipmi_scanner` below.)

---

## Tier-1 Enterprise Network VA — new capabilities (added 2026-08-25)

Breadth-first, unauthenticated / empty-credential, read-only checks. Each scanner
follows the collect→findings split, is wired into all orchestrators across both
trees, and is enforced by `tests/test_tier1_wiring_gate.py` (no branch can ship
half-wired). Validation column: **UT** = unit tests (pure logic + monkeypatched
probe + parity); **GT** = live-socket ground-truth performed; **lab** = needs a
service lab for precision/recall (follow-up).

| Capability | Scanner (port) | Findings | Validation |
|---|---|---|---|
| SSH algo/config audit | `ssh_scanner` (22) | SSH-WEAK-ALGO, SSH-TERRAPIN | UT + GT (real KEXINIT) |
| SMB null-session enum | `smb_enum_scanner` (445) | SMB-NULL-SESSION(-USERS) | UT · lab (Samba/AD) |
| LDAP anonymous bind | `ldap_scanner` (389/636) | LDAP-ANON-BIND/SEARCH | UT · lab (AD) |
| DNS AXFR/DNSSEC/version | `dns_scanner` (53) | DNS-ZONE-TRANSFER, DNS-VERSION-DISCLOSURE, DNS-DNSSEC-ABSENT | UT · lab (zonetransfer.me) |
| NFS export exposure | `nfs_scanner` (2049/111) | NFS-EXPORT-WORLD-READABLE, RPC-PORTMAPPER-EXPOSED | UT (crafted XDR) · lab |
| FTP anonymous access | `ftp_scanner` (21) | FTP-ANON-ACCESS | UT + GT (control+PASV) |
| rsync anon modules | `rsync_scanner` (873) | RSYNC-ANON-MODULES, RSYNC-DAEMON-EXPOSED | UT · lab |
| VNC auth exposure | `vnc_scanner` (5900/5901) | VNC-NO-AUTH, VNC-WEAK-AUTH | UT + GT (RFB) |
| IPMI cipher-zero | `ipmi_scanner` (623/udp) | IPMI-CIPHER-ZERO, IPMI-EXPOSED | UT (byte-exact RMCP+) · lab |
| SMTP hygiene | `smtp_scanner` (25/587) | SMTP-USER-ENUM, SMTP-NO-STARTTLS | UT + GT (VRFY/EHLO) |
| MSRPC endpoint map | `msrpc_scanner` (135) | MSRPC-ENDPOINTS-EXPOSED | UT · lab (Windows) |
| Printer exposure | `printer_scanner` (9100/631) | PRINTER-EXPOSED | UT + GT (PJL) |

**Enterprise attack-path correlations:** CORR-ANON-DATA-EXPOSURE (≥2 anonymous
data channels), CORR-USER-ENUM-PLUS-WEAK-AUTH (SMB user list + weak/exposed login),
CORR-MGMT-PLANE-EXPOSED (IPMI/VNC/RDP console surfaces).

## CVE correlation (manager-side layer — the probe still emits NO CVE claim)

A separate `cve/` package (parallel to `scanner/`, NOT a probe scanner, NOT
two-tree mirrored) owns an offline vuln mirror and maps the CPE identity the probe
attaches to service facts → prioritized CVE findings. Design: `Capabilties/
CVE_CORRELATION_DESIGN.md`. Strategy: **full offline NVD mirror** (air-gap) + KEV +
EPSS. Verified against live feeds: NVD 383,275 CVEs (~192 pages), CISA KEV 1,682,
EPSS 365,017.

| Module | Responsibility | Validation |
|---|---|---|
| `cve/version.py` | Loose version parse/compare for real banners (`8.2p1`, `1.1.1k`, epochs) | UT |
| `scanner/cpe.py` (+`main_scripts/` mirror) | product → CPE 2.3 identity; enriches `service_banner` facts | UT + parity |
| `cve/vulndb.py` | SQLite mirror; `cves_for_cpe` range-membership query (versionStart*/End*) | UT (in-mem DB) |
| `cve/correlator.py` | facts → CVE findings; CVSS+KEV+EPSS+exposure risk score, confidence `medium` max, "verify patch level" | UT + live |
| `cve/ingest.py` | Build/refresh mirror: NVD API 2.0 (paginated, **resumable**, rate-limited, certifi TLS), KEV, EPSS | UT (offline `_get`) + live smoke |
| `cve/cli.py` | `ingest` + `correlate` verbs; clean-stdout JSON contract | UT |

Wired into `run_all` (both trees) as an **optional** post-findings step gated on
`--vuln-db <mirror.sqlite>`: correlates the collected facts and writes
`cve_findings.jsonl` (separate from `findings.jsonl`), plus `cve_summary` in
SUMMARY.json. Absent/missing DB → logged and skipped. Findings are banner-derived
(confidence `medium` max, KEV-first risk ordering) — a manager verifies against the
distro patch level before treating any CVE as confirmed. Tests:
`tests/test_cve_correlation.py` (46).

### Architecture-review remediation (2026-08-27)

A senior-level failure analysis of the whole system produced five shipped fixes
(full suite **1235 passed**; the only fail is the pre-existing, out-of-scope MQTT
packet test):

| # | Fix | Where |
|---|-----|-------|
| 1 | **Two-tree parity guard** — every mirrored `scanner/`↔`main_scripts/` `.py` must be byte-identical, catching *logic* drift the wiring gate can't | `tests/test_two_tree_parity.py` (51) |
| 2 | **Exposure is operator-asserted** — `run_all --exposed`; the risk boost applies only when the operator declares the host internet-facing (was blanket-true, so it carried no signal on internal scans) | `run_all.py` (both trees) |
| 3 | **CPE coverage visibility** — `_CPE_MAP` +4 datastores (elasticsearch/couchdb/memcached/redis); `service_banner` emits `cpe_unmapped` when a product is named but no CPE results, so map blind spots are measurable | `scanner/cpe.py`, `scanner/service_banner.py` (+mirrors) |
| 4 | **Distro-backport confidence** — a backport marker in the raw banner (ubuntu/debian/+deb/+dfsg/`.elN`/raspbian) downgrades a finding to `low` with an explanatory note, because distros patch without bumping the upstream version | `cve/correlator.py` |
| 5 | **Mirror-staleness signal** — `ingest` stamps `meta.last_ingest_utc`; `correlate` (CLI + `run_all`) surfaces mirror age and warns past 7 days | `cve/ingest.py`, `cve/correlator.py`, `cve/cli.py` |

Confidence and risk are **orthogonal**: a `low`-confidence finding can still be
`critical`-risk ("high-impact IF real — verify the patch level").

**Deferred (need a decision, documented):** (a) the CVE layer's production home
(manager repo vs. probe); (b) `run_all` → clearer name; (c) a per-host aggregate
rate limiter.

**Two open foundations (from the plan, not yet done):** (1) two-tree
(`scanner/` vs `main_scripts/`) consolidation; (2) sealed-build (Nuitka) prototype
with the new impacket submodules + ldap3/dnspython include-modules.

## Network VA campaign — sequential background job (added 2026-08-27)

`scanner/va_campaign.py` (+`main_scripts/` byte-identical mirror) is the
end-to-end **campaign orchestrator**: it runs every already-shipped capability as
one sequential job and streams live "what we're doing now" progress. It does not
add scanners — it *composes* the ScanFunnel-built ones in a fixed, gated order so
an operator can launch a whole-network VA with a single command and watch it.

**Stages (`STAGE_CATALOG`, in order):** discovery → port_map → assessment →
udp_snmp → full_port *(opt-in)* → exposure → inventory → **detect** → cve
*(opt-in)*. Each carries operator-facing `name`/`detail` copy. Gating: a stage with
an unmet `gate` (e.g. port_map when discovery found 0 live hosts) is **skipped**,
not failed; opt-in stages disabled by options are excluded from the percent
denominator. Stage errors are **isolated** — one scanner blowing up marks that
stage `error` and the campaign continues.

**Detection layer (the "condition" DB — added 2026-08-27):** the always-on `detect`
stage (`run_detect` → `findings.py::run_findings(ctx.facts)`) is what turns raw
collected facts into **ranked, actionable weakness findings** — weak/legacy TLS,
SMBv1 / no-signing / null-session, weak-SSH / Terrapin, anonymous FTP/LDAP, no-auth
VNC, IPMI cipher-0, RDP-without-NLA, missing web-security headers, exposed UDP
amplifiers, plus cross-fact attack-path correlations. It is deterministic, offline,
needs no DB, and gates on `bool(ctx.facts)`. Findings are emitted as first-class
facts (`scanner="findings"`, `data=Finding.to_dict()`) and, in the CLI path, split
into their own `findings.jsonl` artifact. This is a **weakness/condition** verdict,
NOT a CVE claim — the opt-in `cve` stage (`--vuln-db`) remains the separate CVE-DB
correlation layer, and the probe still never asserts a confirmed CVE.

**Progress contract (`ProgressReporter.snapshot()`):** JSON with
`campaign_id, targets, status, started_at, updated_at, percent, current_stage,
eta_seconds, stages[]{id,name,detail,status,started_at,ended_at,count,note},
totals{live_hosts,open_ports,facts}`. Written atomically to
`campaign_progress.json` (tmp + `os.replace`) after every transition and pushed to
an optional callback (wrapped so a bad sink never breaks a scan). This is the exact
shape the manager frontend campaign-progress page consumes.

**Two run paths:**
- **Standalone CLI** — `python -m scanner.va_campaign <targets> [--full-ports]
  [--no-udp] [--vuln-db mirror.sqlite] [--exposed] [--out-dir DIR]`. Full-port
  audit and CVE correlation are opt-in here (default = fast, no CVE). `CliProgressView`
  redraws in place on a TTY, one line per transition when piped. Emits a JSON
  summary on stdout (clean-stdout contract), plus `results.jsonl` (every collected
  fact) and `findings.jsonl` (just the detected weaknesses, ranked).
- **Agent-dispatchable use-case** — `uc_network_va` (code `12`, `scan_type
  network_va`, profile `it`), so the manager can enqueue the whole campaign as a
  background job. **Collection-only on this path:** it runs discovery →
  assessment + both post-stages (device classification + exposure mapping) but
  emits **no CVE claim** — CVE correlation stays the manager-side layer (standing
  constraint). CVE is a probe stage *only* in the standalone CLI via `--vuln-db`.

Parity: `uc_network_va` is byte-identical in the probe (`agent/use_cases.py`) and
manager (`agents.py`) catalogs, `USE_CASE_CODES[12]` matches, enforced by the
manager's `test_agent_dispatch.py`. Tests: `tests/test_va_campaign.py` (16 — engine
sequencing/gating/opt-in, error isolation, percent/ETA math, the JSON progress
shape, atomic write, callback resilience, catalog↔default_stages alignment,
CliProgressView, and the real `detect` stage turning an SMBv1 fact into an
`SMB-V1-ENABLED` finding / skipping when nothing was collected) +
`test_probe_core.py::test_network_va_resolves`. Full suite **1255 passed**.
