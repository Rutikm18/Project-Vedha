# Vedha VA — Client Pre-Engagement Prerequisites

Please complete the items below **before the assessment start date**. They let our scanning
probe reach the systems in scope and return accurate results. Fields in `<…>` are filled in
jointly during scoping.

**How it works (1 line):** we deploy a lightweight **probe** inside your network. It dials
**out only** to our platform and scans **only** the addresses you authorize. It opens standard
TCP connections to your hosts — nothing is installed on the targets.

---

## 1. Probe host (you provide one host inside the network to be assessed)

| Item | Requirement |
|---|---|
| Placement | A host on the **same network segment / VLAN** that can reach the in-scope targets (no client/AP isolation between it and the targets). |
| OS | Linux (Ubuntu/Debian/RHEL) with **Docker** installed. A small VM is fine. |
| Resources | **1–2 vCPU, 2 GB RAM, 5 GB disk.** |
| Inbound to the probe | **None.** The probe needs no open inbound ports. |
| Access for us | Either (a) you run our one-line install command, or (b) SSH access for our engineer to deploy the probe container. |

*(For remote/SaaS assessments we can also ship the probe as a signed container image or `.tar`.)*

---

## 2. Outbound connectivity — probe → our platform

Allow the probe host **outbound** to our manager:

| From | To | Port | Protocol |
|---|---|---|---|
| Probe host | `<manager-hostname e.g. vedha.vendor.com>` | **443** | HTTPS (TLS) |

- No other outbound is required. If you use an egress proxy, allow `CONNECT` to the host above.
- Your targets **do not** talk to our platform.

---

## 3. Scan reachability — probe → in-scope targets (the important part)

The probe connects **from the probe host's IP** to your targets. On the targets / network
firewalls, **allow inbound TCP from the probe host IP** to the ports below.

**a) Host must answer discovery** (or it is treated as "down" and skipped):
- Allow **ICMP echo (ping)** from the probe host, **or** leave at least one common TCP port responding.

**b) Ports that must be reachable to produce vulnerability findings:**

| Target port | Service | Result |
|---|---|---|
| **22/tcp** | SSH (OpenSSH) | OpenSSH CVEs |
| **80/tcp** | HTTP (nginx / Apache) | Web-server CVEs |
| **443/tcp** | HTTPS + TLS | TLS/cert findings + web-server CVEs |
| **3306 / 5432 / 6379 /tcp** | MySQL/MariaDB · PostgreSQL · Redis | Database CVEs |
| 445, 139, 161(udp), 21 | SMB · SNMP · FTP | Service enumeration (limited CVE coverage) |

> At minimum, open **inbound from the probe host to 22 and/or 80/443 and/or a DB port** on the
> hosts you want assessed. Hosts exposing none of these will be enumerated but yield few/no CVEs.

**c) No blocking in the path:**
- No IPS/IDS, rate-limiter, or WAF that **silently drops or throttles** the probe's connections.
- If you must keep IPS on, **allow-list the probe host IP** for the engagement window.

---

## 4. Keep service versions visible

Findings are matched from the **version in each service's banner**. Please confirm the in-scope
services are in their **normal (version-exposing) configuration** for the engagement:
- nginx: `server_tokens on` (default)
- Apache: `ServerTokens Full/OS` (default)
- SSH: standard banner (default)

Version-hiding hardening (e.g. `server_tokens off`) will suppress findings for that service.

---

## 5. Authorization (Rules of Engagement)

- **Authorized scope (CIDRs / IPs):** `<AUTHORIZED_CIDR_1>`, `<AUTHORIZED_CIDR_2>` …
- **Explicit exclusions:** `<any host/range that must NOT be scanned>`
- **Assessment window:** `<start> – <end>`, timezone `<tz>`
- **Signed written authorization** for the scope above **before** any scanning begins. The probe
  enforces this list and refuses anything outside it.
- **Point of contact** (name / phone / email) reachable during the window.

---

## 6. Optional — deeper (authenticated) results

Credentialed inventory (SSH/WinRM read-only) produces far richer, version-accurate findings.
**This is not required for the current engagement** and is arranged separately if desired; do
**not** place credentials in scope requests. If in future you want authenticated coverage,
provide a **read-only** account per platform:
- Linux: an audit SSH user (key-based) that can run `dpkg -l` / `rpm -qa`.
- Windows: a read-only WinRM account for installed-update inventory.

---

## 7. Pre-flight verification (run before the start date)

From the **probe host**, confirm it can reach a representative target and our platform:

```bash
# reach our platform (expect: 200)
curl -s -o /dev/null -w "manager %{http_code}\n" https://<manager-hostname>/health

# reach a representative in-scope target on the ports above (expect: succeeded)
for p in 22 80 443 3306 5432; do nc -z -w3 <TARGET_IP> $p && echo "$p open"; done
```
If the manager returns `200` and at least one target port shows open, you're ready.

---

### Summary checklist
- [ ] Probe host provisioned (Linux + Docker, same segment as targets)
- [ ] Outbound **443** from probe host to `<manager-hostname>` allowed
- [ ] **Inbound from the probe host IP** to targets on **22 / 80 / 443 / DB ports** allowed
- [ ] Discovery allowed (ICMP or a responding TCP port)
- [ ] IPS/WAF/rate-limit allow-lists the probe host for the window
- [ ] Service version banners left at default
- [ ] Signed authorization, scope CIDRs, exclusions, window, and contact confirmed
