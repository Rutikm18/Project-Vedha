# Vedha — Network Vulnerability Assessment at a Glance

**See everything on your network. Know what an attacker can reach. Prove what changed.**

Vedha deploys a single lightweight probe inside your network. It **dials out
only** — no inbound ports, no agent on every machine, nothing new for an attacker
to target. The probe looks; our platform thinks. It inventories what you have,
grades how exposed each service is, and prioritises the handful of findings that
actually matter — ranked by what attackers are exploiting *today*, not by raw
severity scores.

Every result is **evidence-backed**: for each finding you see what we observed,
how confident we are, and why. No unverifiable "trust us" verdicts.

---

## Available now

Scans you can run today, each validated against live targets.

| Scan | What it does | What you get |
|---|---|---|
| **Network Discovery** | A fast, no-impact sweep of what is alive and what ports each device exposes. | A live inventory of your network — the baseline everything else builds on. *2–5 min per /24.* |
| **Device Identification** | Classifies each live device — workstation, server, network gear, printer, hypervisor, IoT — from its operating system, open ports and service banners. | An evidence-based asset list, never a hostname guess. *5–15 min per /24.* |
| **Full Security Assessment** | The complete one-run sweep: hosts → services → operating system → TLS, web, Windows/SMB, database and SNMP exposure. | Your baseline security posture in a single picture. *15–60 min per /24.* |
| **Network Vulnerability Assessment** *(full campaign)* | The flagship end-to-end run, with live per-stage progress: discovery → device classification → deep service assessment → Windows/SMB → SNMP/UDP → internet-exposure → prioritised CVE candidates. | A complete network VA in one job you can watch happen. *30–90 min per /24.* |
| **Windows & File-Sharing (SMB) Security** | Confirms the legacy SMBv1 protocol is off and SMB signing is enforced. | Closes the EternalBlue / NTLM-relay class of attacks — with proof of the current setting. *5–15 min.* |
| **SNMP Weak-Credential Check** | Tests routers, switches, printers and appliances for default or weak SNMP community strings. | Finds the devices answering "public"/"private" — a classic config-read and lateral-movement foothold. *2–8 min.* |
| **UDP & Amplification Exposure** | Probes UDP services (DNS, NTP, SNMP, memcached, NetBIOS, SSDP) for open-resolver and amplification weaknesses. | Flags the services an attacker could abuse to turn your network into a DDoS reflector. *2–8 min.* |
| **Full-Port Audit** | Scans every one of the 65,535 TCP ports on a host, with a built-in completeness self-check. | Catches services hiding on non-standard ports — and proves a clean result is genuinely clean, not just an incomplete scan. *20–90 min per host.* |
| **Internet-Exposure Mapping** | With two or more probes, compares what each vantage point can reach. | Separates *truly internet-exposed* services from internal-only ones — answers "what can an outside attacker actually reach?" *5–15 min per /24.* |
| **Deep Port Sweep** *(few hosts)* | Every TCP port plus the full assessment on a small set of your most critical hosts. | A crown-jewel deep dive, budgeted so it always finishes. *20–90 min per host, up to 3 hosts.* |
| **IoT & Embedded Device Discovery** | Surfaces cameras (RTSP), MQTT brokers, printers, DVRs and Telnet-exposed gear, with service banners. | Inventories the unmanaged corner of the network most tools miss. *3–10 min per /24.* |
| **Re-scan & Change Detection** | Re-runs an assessment and highlights *what changed* since last time — new hosts, newly opened ports, configuration drift, certificate and version changes. | Turns a point-in-time scan into a watch: shows the drift between runs, not just today's state. *15–60 min per /24.* |

---

## In validation *(coming soon)*

Built and working — being verified against live targets before we switch them on
for customers. We enable a scan only once we have proven it; nothing ships on a
promise.

| Scan | What it will do |
|---|---|
| **Web & TLS/SSL Security Check** | Grades TLS/SSL configuration on your web servers — protocol versions, cipher strength, certificate health. |
| **Web Application Security Check** | Fingerprints web applications — supported methods, security headers, server technology — a read-only pre-flight before a full web-app penetration test. |
| **Database Exposure Check** | Checks whether MySQL, PostgreSQL, SQL Server, Redis or MongoDB are reachable on the network and accept unauthenticated connections. |
| **AI & MCP Endpoint Discovery** | Discovers exposed AI inference endpoints and Model Context Protocol (MCP) servers — a fast-growing, often-unmonitored attack surface. |
| **OT / ICS Passive Discovery** | Listen-only inventory for industrial networks — **zero active packets**, so fragile operational-technology equipment is never probed. |

---

## Why Vedha

- **Collect-only probe, zero inbound footprint.** The sensor dials out over one
  encrypted channel. It adds no attack surface and holds no vulnerability data —
  all analysis happens on our platform, not in your network.
- **Evidence over assertion.** Every finding carries what we saw, our confidence,
  and the reasoning. A firewalled port is never sold to you as "open"; an
  unverifiable guess is never sold as a fact.
- **Prioritised by real-world risk.** Findings are ranked by what attackers are
  *actively exploiting* (CISA KEV and exploit-prediction data) ahead of raw
  severity — so you fix the handful that matter first, not the hundreds that don't.
- **Change-aware.** Security is a moving target. Vedha is built to tell you what is
  *newly* exposed since your last scan, not just re-print the same list.
- **Safe for sensitive networks.** Industrial (OT/ICS) networks are handled
  passively — the probe listens and never sends a packet that could disturb
  fragile control equipment.

---

*Legend — **Available now:** validated against live targets and ready to run.
**In validation:** built and functional; enabled per customer once verified on a
matching live target. We enable only what we have proven.*
