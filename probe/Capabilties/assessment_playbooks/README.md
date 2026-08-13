# Assessment Playbooks — Core-Level Scanning & Vulnerability Discovery

A set of deep, protocol/packet-level playbooks for scanning a network and finding vulnerabilities
**from a single foothold system**, one file per assessment area. Each playbook is grounded in how
the protocols and stacks actually behave on the wire, and cross-references the Nmap engine
internals documented in [`../fresh_implement.md`](../fresh_implement.md).

> ⚠️ **Authorized use only.** These techniques are for assessing networks you own or are
> contractually/written-scoped to test. Discovery and scanning are logged, can disrupt fragile
> systems, and may be illegal without authorization. Every playbook assumes explicit consent,
> defined scope, and a safety-first posture.

---

## How the playbooks fit together

```
              ┌─────────────────────────────────────────────┐
              │ 02  FULL ASSESSMENT (orchestration/funnel)   │
              └───────────────────┬─────────────────────────┘
                                  │ sequences ↓
   01 Network Discovery ──► live hosts ──► port/service/OS ──► specialized playbooks:
                                  │
   ┌──────────────┬──────────────┼───────────────┬──────────────┬───────────────┐
   ▼              ▼              ▼               ▼              ▼               ▼
 03 External    04 Database    05 Windows      06 OT/ICS     07 AI/MCP        11 UDP
 Web Triage     Exposure       Estate          (PASSIVE)     Endpoints        Exposure
   │              │              │               │              │               │
   ▼              ▼              ▼               ▼              ▼               ▼
 10 Web App     (RCE/data)    (AD paths)     (safety-first)  (unauth AI)     12 SNMP
 Triage                                                                       Exposure
                                  │
   09 IoT/Embedded Survey    13 Mobile Device      08 Re-scan/Delta (continuous monitoring)
   (device LAN surface)      (client + backend)    (diff every scan over time)
```

- **Start** with `01` (know what's alive) and `02` (the master funnel: discovery → ports →
  services → OS → vulns).
- **Branch** into the specialized playbook for each surface you find.
- **Loop** with `08` to turn point-in-time scans into continuous attack-surface monitoring.
- **`06` OT/ICS is passive-first** — never run the aggressive techniques from the other playbooks
  against industrial/medical/safety-critical gear.

---

## Index

| # | Playbook | Focus | Key ports/protocols |
|---|----------|-------|---------------------|
| 01 | [Network Discovery](01_network_discovery.md) | Host liveness, L2/L3 | ARP, NDP, ICMP, TCP-SYN/ACK ping |
| 02 | [Full Assessment](02_full_assessment.md) | End-to-end orchestration | (all) |
| 03 | [External Web Triage](03_external_web_triage.md) | Internet web surface | DNS, TLS, HTTP, CT logs |
| 04 | [Database Exposure](04_database_exposure.md) | Exposed DBs | 3306,5432,1433,27017,6379,9200 |
| 05 | [Windows Estate](05_windows_estate.md) | AD/Windows | SMB,RPC,LDAP,Kerberos (445,389,88) |
| 06 | [OT / ICS Passive Discovery](06_ot_ics_passive.md) | Industrial (passive) | Modbus,DNP3,S7,EtherNet/IP,BACnet |
| 07 | [AI / MCP Endpoint Sweep](07_ai_mcp_endpoint_sweep.md) | AI infra & MCP | 11434,MCP/JSON-RPC,vector DBs |
| 08 | [Re-scan / Delta Assessment](08_rescan_delta.md) | Change over time | ndiff / XML diffing |
| 09 | [IoT / Embedded Survey](09_iot_embedded_survey.md) | Embedded devices | SSDP,mDNS,CoAP,MQTT,telnet |
| 10 | [Web Application Triage](10_web_app_triage.md) | App-layer vulns | HTTP, OWASP classes |
| 11 | [UDP Service Exposure](11_udp_service_exposure.md) | UDP services | 53,123,161,500,1900,11211 |
| 12 | [SNMP Exposure Check](12_snmp_exposure.md) | SNMP | UDP 161, MIB/OID |
| 13 | [Mobile Device](13_mobile_device.md) | Phones & app backends | ADB 5555, mDNS, app APIs |

---

## The common method (every playbook shares this spine)

1. **Least-intrusive first.** Passive → unauthenticated active → authenticated → exploitation.
   Stop at the least-invasive step that proves the finding.
2. **Multiple stimuli, because one probe is never reliable.** (Nmap's ping cocktail and scan-type
   logic — `../fresh_implement.md §5-6` — is the archetype.)
3. **The response *or its absence* is the evidence.** Interpret RST/SYN-ACK/ICMP-unreachable/
   silence per protocol and per scan type.
4. **Fingerprint before you attack.** Handshake/banner → product+version → known-vuln mapping.
5. **Prove, don't detonate.** Enumerate exposure with metadata; never exfiltrate real data, never
   weaponize amplification, never brick fragile devices.
6. **Prioritize by Exploitability × Exposure × Impact**, then report with reproducible evidence.
7. **Record everything as structured output (Nmap XML)** so `08` can diff it forever.

---

## Universal challenges (recur in every area)

| Challenge | Cross-cutting tackle |
|-----------|----------------------|
| Firewalls/IDS drop or flag probes | Multiple probe types; slow timing; randomize; pivot to internal foothold; ACK-scan to map rules |
| Fragile hosts crash under scanning | Passive-first for OT/medical/IoT; gentle timing; `-sT` over exotic scans |
| Banners/versions lie | Prefer behavioral checks (NSE/nuclei/native clients) over banner→CVE |
| UDP ambiguity (open|filtered) | Protocol payloads + native clients; accept honest uncertainty |
| Scope/ownership on shared IPs & CDNs | Verify ownership per asset, not per IP; explicit include/exclude lists |
| Volume & reproducibility | Funnel the pipeline; fixed commands; XML → DB; delta-only alerting |
| Legal/safety/privacy | Written authorization, change windows, safety contacts, no data exfiltration |

---

## Reference spine

- **Nmap internals (this repo):** [`../fresh_implement.md`](../fresh_implement.md) — packet-level
  mechanics behind all active scanning.
- **Methodology:** NIST SP 800-115, PTES, MITRE ATT&CK, OWASP (WSTG/MASTG/IoT/LLM Top 10).
- **Safety-critical:** NIST SP 800-82 & IEC 62443 (OT), CISA ICS-CERT advisories.
- Per-area RFCs, protocol specs, and tooling are listed in each playbook's References section.
