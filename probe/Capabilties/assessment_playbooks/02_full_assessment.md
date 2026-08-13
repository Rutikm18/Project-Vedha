# 02 — Full Assessment (Core-Level Playbook)

> **Goal:** From a single foothold, run an end-to-end, defensible assessment of a network:
> discovery → port state → service/version → OS → vuln enumeration → (optional) auth checks,
> producing a prioritized, reproducible findings set. This is the *orchestration* playbook —
> it sequences all the others.

---

## 1. Core principle: assessment is a pipeline of narrowing inference

Each stage **reduces uncertainty and cost** for the next. You never run everything against
everything — you funnel:

```
All addresses in scope
   │  (discovery — cheap, broad)                    → live hosts        [01]
   ▼
Live hosts
   │  (port scan — SYN, top-ports first)            → open ports
   ▼
Open ports
   │  (service/version detection)                   → software + versions
   ▼
Software + versions
   │  (OS detection, NSE, CVE mapping, auth checks) → vulnerabilities
   ▼
Prioritized findings (exploitability × exposure × impact)
```

The reason for the funnel is **combinatorial cost**: scanning 65535 TCP + 65535 UDP ports ×
service detection × NSE across a /16 is astronomically expensive and noisy. The pipeline spends
budget only where prior evidence justifies it — the same "spend probes where evidence warrants"
logic Nmap's congestion control uses at the packet level (`fresh_implement.md §7`).

---

## 2. The stages in depth

### Stage A — Discovery (see `01_network_discovery.md`)
Produce the authoritative live-host list. Everything else keys off it.

### Stage B — Port state enumeration
Core decision: **SYN scan (`-sS`) when privileged, connect scan (`-sT`) otherwise.** Why SYN is
default: half-open, faster, fuller control, and it distinguishes filtered from closed reliably
(`fresh_implement.md §5.3`). Strategy:

1. **Top-ports first** (`--top-ports 1000`) — `nmap-services` frequency-ranked ports find ~93%
   of real services for a fraction of the cost of `-p-`.
2. **Then full sweep** (`-p-`) on hosts that matter, to catch services on odd ports.
3. **UDP selectively** (`-sU --top-ports 100`) — UDP is slow (`11_udp_service_exposure.md`); scan
   the high-value UDP ports (53,161,123,500,1900,5353…) rather than all 65k.

### Stage C — Service & version detection (`-sV`)
Turns "port 8080 open" into "Apache Tomcat 9.0.30." This is what makes vuln mapping possible —
you match *product + version* to CVEs. Engine detail in `fresh_implement.md §8`. Add `-sV
--version-all` on high-value hosts; keep intensity moderate elsewhere for speed.

### Stage D — OS detection (`-O`)
Fingerprints the stack (`fresh_implement.md §9`). Feeds prioritization (EOL OSes), tool
selection, and lateral-movement planning. Needs one open + one closed port for accuracy.

### Stage E — Vulnerability enumeration
Two complementary approaches:
- **Version → CVE mapping** (unauthenticated, low-risk): correlate detected versions against
  CVE/NVD, vendor advisories, and NSE `vuln` category scripts (`--script vuln`). Beware version
  banners that lie (backported patches) — see challenges.
- **Active NSE / template checks:** `nmap --script "default,safe,vuln"`, plus `nuclei` templates
  for web (`03`/`10`), protocol-specific checks (`04`,`05`,`12`). These *probe behavior*, not just
  banners — far fewer false positives.
- **Optional authenticated checks:** with in-scope creds, run authenticated scans (config audits,
  patch levels) — highest fidelity, lowest false-positive rate.

### Stage F — Correlation, prioritization, reporting
Score = **Exploitability × Exposure × Impact**:
- Exploitability: public exploit? auth required? complexity? (map to EPSS / exploit-DB).
- Exposure: internet-facing vs internal-only; reachable from where?
- Impact: crown-jewel host? DC? database? OT controller?

Use CVSS as a *base*, then adjust with EPSS (probability of exploitation) and your environment.

---

## 3. Concrete single-host workflow (commands)

```bash
# A. Discovery
nmap -sn -PR 10.0.0.0/24 -oX disc.xml                       # local
nmap -sn -PE -PS443,80,22 -PA80 -PU40125 10.20.0.0/22       # routed

# B. Ports (funnel)
nmap -sS --top-ports 1000 -T4 -iL live.txt -oX ports_fast.xml
nmap -sS -p- -T4 <high_value_hosts> -oX ports_full.xml
nmap -sU --top-ports 100 <high_value_hosts> -oX udp.xml

# C-E. Service+OS+vuln on what we found open
nmap -sV -O --version-all -sC --script "default,safe,vuln" \
     -p <open_ports> -iL live.txt -oX deep.xml

# Web + specialized handoffs (see dedicated playbooks)
httpx -l webhosts.txt | nuclei -severity medium,high,critical   # 03/10
```

Always emit **XML** (`-oX`) — it is the machine-readable substrate for delta assessment (`08`),
reporting, and tool chaining.

---

## 4. Challenges & how to tackle them (low-level)

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Scan takes days | 65k×2 ports × services × NSE across many hosts | Funnel: top-ports → full only on interesting hosts; parallel host groups; UDP sparingly |
| IDS/IPS blocks you mid-scan | Bursty, signature-matching traffic | `-T2/-T3`, `--max-rate`, randomize host+port order, split over time/sources |
| Version banners lie | Backported security patches keep old version string | Prefer behavioral checks (NSE/nuclei) over banner→CVE; note "version-based, needs confirmation" |
| False positives flood report | Banner-only CVE matching | Tier findings by confidence: confirmed (behavioral) > version-based > inferred |
| Stateful firewall shows all-filtered | Default-deny perimeter | Pivot to internal foothold; use ACK scan to map the ruleset (`fresh_implement.md §5.6`) |
| Rate-limited UDP misleads | RFC1812 ICMP throttling | See `11_udp_service_exposure.md`; slow down, use payload probes |
| Fragile hosts crash (printers, OT, old IoT) | Malformed/aggressive probes | Exclude OT (`06`), use `-sT` not `-sS` on delicate hosts, avoid `-sX/-sN/-sF` on unknown gear |
| Credential-required depth | Unauth scan misses config/patch issues | Coordinate authenticated scans where scope allows |
| Data volume unmanageable | Big estate, many artifacts | Normalize to XML→DB; dedupe by (host,port,service); track deltas (`08`) |
| Scope creep / hitting out-of-scope hosts | CIDR mistakes, third-party CDNs | Maintain explicit include/exclude lists (`--excludefile`), verify ownership of every /24 |

---

## 5. Considerations & guardrails

- **Blast radius:** a full assessment is the noisiest, most disruptive activity here. Get written
  authorization, a change window, and emergency contacts. Know which hosts are fragile.
- **Reproducibility:** fixed commands + XML output = defensible, re-runnable results. Record
  tool versions and DB (NVD, nuclei-templates) dates.
- **Least intrusive that answers the question:** start passive/unauth; escalate to active/auth
  only as needed and permitted.
- **Chain of custody for findings:** every finding needs evidence (the probe, the response,
  the reason) — Nmap's `--reason` and raw NSE output are your proof.

---

## 6. References

- MITRE ATT&CK (Reconnaissance TA0043, Discovery TA0007) for technique framing.
- NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment) — the
  canonical assessment methodology reference.
- PTES (Penetration Testing Execution Standard) — phased engagement model.
- FIRST CVSS v3.1/v4.0 spec; EPSS (first.org/epss) for exploitation likelihood.
- Nmap internals: `../fresh_implement.md` (whole document).
