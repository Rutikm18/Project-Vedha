# 08 — Re-scan / Delta Assessment (Core-Level Playbook)

> **Goal:** Detect *change* in a network's exposure over time — new hosts, new open ports, new
> services, disappeared services, version drift — rather than re-deriving the whole picture from
> scratch. Delta assessment turns point-in-time scanning into **continuous attack-surface
> monitoring** and validates remediation.

---

## 1. Core theory: security is a time-series, not a snapshot

A network's exposure changes constantly: hosts spin up/down (cloud autoscaling, DHCP), services
get deployed, firewall rules change, patches land. A single scan is a **frame**; security posture
is the **film**. What matters operationally is the **diff between frames**:

- **New open port / service** = new attack surface (possibly a shadow deployment or a regression).
- **Version change** = patch applied (good) or software rolled back/replaced (investigate).
- **Host appeared/disappeared** = inventory drift.
- **State transition** filtered→open = a firewall change exposed something.

The enabling insight: **scan output must be a stable, structured, machine-diffable artifact.**
Nmap's XML (`-oX`) is designed for exactly this, and Nmap ships **`ndiff`** (in this repo:
`nmap/ndiff/ndiff.py`) whose entire purpose is to compare two XML scans and emit the delta.

---

## 2. The data model that makes deltas possible

To diff reliably you need a **stable identity key** for each finding and a **normalized record**:

```
identity  = (host_id, protocol, port)         where host_id is stable across scans
record    = { state, service, product, version, reason, script_output, timestamp }
```

Pitfalls in choosing `host_id`:
- **IP is unstable** in DHCP/cloud environments (same host, new IP tomorrow).
- Prefer **MAC** (L2, from ARP) on local nets, or **hostname/asset-id** where available, or a
  **hardware/cert/JARM fingerprint** for internet hosts. Falling back to IP is fine for static
  infrastructure but must be a conscious choice.

Normalization matters: sort ports, canonicalize service names, strip volatile fields (scan
timestamps, session IDs) before diffing, or every scan looks "changed."

---

## 3. Approach from a single system (methodology + commands)

**Step 1 — baseline (identical, reproducible command; save XML):**
```bash
nmap -sS -sV -O -p- -T4 -iL scope.txt -oX baseline_2024-06-01.xml
```
Fix everything that affects output: port set, timing, scripts, tool version. **Reproducibility is
the whole game** — a different `--top-ports` or `-sV` intensity produces spurious deltas.

**Step 2 — periodic re-scan (same command, new date):**
```bash
nmap -sS -sV -O -p- -T4 -iL scope.txt -oX scan_2024-07-01.xml
```

**Step 3 — diff:**
```bash
ndiff baseline_2024-06-01.xml scan_2024-07-01.xml           # human-readable delta
ndiff --xml baseline.xml scan.xml > delta.xml               # machine-readable for pipelines
```
`ndiff` reports per-host: ports added/removed, state changes, service/version changes, host
up/down changes — exactly the security-relevant events.

**Step 4 — for large/continuous programs:** load scans into a DB (or a tool like `nmap-did-what`,
Faraday, or an ASM platform) keyed on `(host_id, port)`; compute deltas with set operations; alert
on **new exposure** and **remediation-regression** classes.

**Step 5 — remediation validation:** after a fix, a targeted re-scan of just the affected
`(host, port)` confirms the service is now closed/patched — the delta *is* the proof of fix.

---

## 4. Vulnerability logic (which deltas are findings)

| Delta | Interpretation | Priority |
|-------|----------------|----------|
| New open port on internet-facing host | New attack surface / shadow deploy | High |
| filtered/closed → open | Firewall change exposed a service | High |
| New service version with known CVE | Regression or vulnerable deploy | High |
| Version increased (patched) on a prev-vuln service | Remediation confirmed | Info (good) |
| Host newly appeared in scope | Unmanaged/rogue asset | Medium-High |
| open → closed on a service that should exist | Outage or intended decommission | Investigate |
| New host with DB/RDP/SMB exposed | High-value new surface | High |

The key automation: **alert only on deltas**, not on the full (noisy) scan — this is how ASM
programs stay signal-rich.

---

## 5. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Everything looks "changed" | Non-deterministic scans (timing, DHCP IP churn, random port order) | Pin exact command; key on stable host_id (MAC/hostname), not IP; normalize/sort before diff |
| Flapping ports | Load balancers, autoscaling, transient services | Require N consecutive scans to confirm; smooth with a debounce window |
| IP reuse across hosts | DHCP hands same IP to a different device | Use MAC/asset-id as identity; correlate, don't assume IP=host |
| Version string noise | Minor banner formatting differences | Canonicalize product/version fields; diff on normalized tuples |
| Scope drift | scope.txt changed between runs | Version-control the scope file; diff scope too |
| Huge diffs after infra change | Mass migration/re-IP | Re-baseline deliberately; annotate the change event |
| Cloud ephemerality | Hosts live minutes | Shorten scan cadence; integrate with cloud inventory APIs, not just active scans |
| Missed change between scans | Coarse cadence | Increase frequency for critical assets; combine with passive/continuous monitoring |
| Tool/DB version changed output | New Nmap or nuclei templates alter results | Record tool + DB versions per scan; treat tool upgrades as re-baseline events |

---

## 6. Considerations & guardrails

- **Reproducibility is non-negotiable.** Same command, recorded tool versions, version-controlled
  scope. Otherwise deltas are noise.
- **Store raw XML immutably** (timestamped, hashed) — it is the evidence trail and the diff source.
- **Delta ≠ cause.** A new open port could be legitimate; the delta flags it for human triage, it
  doesn't judge it.
- **Cadence matches asset criticality** — daily/continuous for internet-facing, weekly/monthly for
  stable internal.

---

## 7. References

- Nmap `ndiff` (in this repo: `nmap/ndiff/ndiff.py`, `nmap/ndiff/docs/`), Nmap XML DTD.
- NIST SP 800-137 (Information Security Continuous Monitoring / ISCM).
- Attack Surface Management concept (Gartner ASM/EASM/CAASM); continuous-monitoring literature.
- Tooling: ndiff, nmap-did-what, Faraday, RustScan+ndiff pipelines, commercial ASM platforms.
- Nmap XML rationale: `../fresh_implement.md §12` (output formats).
