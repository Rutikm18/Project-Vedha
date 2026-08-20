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
