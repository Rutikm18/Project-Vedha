# 06 — OT / ICS Passive Discovery (Core-Level Playbook)

> **Goal:** Inventory and assess Operational Technology / Industrial Control Systems (PLCs, RTUs,
> HMIs, SCADA, DCS) **without disrupting physical processes.** The overriding rule: in OT,
> availability and safety dominate — **active scanning can crash controllers and endanger people.**
> Default posture is **passive**.

---

## 1. Core theory: why OT is different (and why active scanning is dangerous)

IT security prioritizes Confidentiality → Integrity → Availability. **OT inverts this: Safety and
Availability come first.** The reasons are physical and protocol-level:

1. **Fragile stacks.** Many PLCs run minimal, decades-old TCP/IP stacks with tiny resource
   budgets. A single malformed packet, an aggressive SYN scan, or even a benign full-connect scan
   has historically **hung or reset PLCs** (documented for many vendors). A crashed PLC can stop a
   turbine, open a valve, or halt a production line.
2. **Real-time determinism.** Control loops run on millisecond cycles. Extra traffic introduces
   jitter that can trip safety systems.
3. **No authentication by design.** Legacy OT protocols (Modbus, DNP3, S7, EtherNet/IP, Profinet)
   were built for isolated networks and often have **no authentication, no encryption, no
   integrity** — reading and even *writing* control values requires no credentials. The exposure
   itself is the vulnerability.
4. **Cannot patch freely.** Uptime requirements and vendor certification mean systems run
   unpatched for years; you can't "just update."

**Consequence:** discovery is **passive-first**. You listen; you do not probe. Active testing, if
ever done, happens only on offline/test rigs with engineering sign-off.

---

## 2. The protocols and ports (what you're listening for)

| Protocol | Port | Purpose / core fact |
|----------|------|---------------------|
| Modbus/TCP | 502 | Simplest SCADA protocol; function codes read/write coils & registers; **no auth** |
| DNP3 | 20000 | Utilities/SCADA; more robust; secure-auth variant rarely enabled |
| EtherNet/IP (CIP) | 44818/tcp, 2222/udp | Rockwell/Allen-Bradley; `List Identity` reveals device details |
| S7comm / S7comm-plus | 102 (COTP/TPKT) | Siemens PLCs; ISO-on-TCP; function-level device info |
| PROFINET | (L2, DCP) | Siemens fieldbus; discovery via L2 DCP frames |
| BACnet | 47808/udp | Building automation (HVAC); Who-Is/I-Am broadcasts |
| OPC-UA | 4840 | Modern, *can* be secured (certs); often left unauthenticated |
| IEC 60870-5-104 | 2404 | Power grid telecontrol |
| FINS (Omron), MELSEC (Mitsubishi), Niagara Fox (1911/4911) | various | Vendor PLC/BMS protocols |
| HMI / historian | 80/443/1433/... | Windows-based HMIs and historians (assess as IT, carefully) |

Passive discovery keys off **broadcast/multicast announcements** (Profinet DCP, BACnet Who-Is,
EtherNet/IP List Identity responses to periodic polls) and **normal cyclic traffic** between HMI
and PLC.

---

## 3. Approach from a single system (passive methodology)

**Step 1 — get a passive vantage point (the hard part):**
- **SPAN/mirror port** on the OT switch, or a **network TAP**, feeding a monitoring NIC on your
  host in **promiscuous, receive-only** mode (ideally a data-diode / RX-only cable so you
  *physically cannot transmit*).
- Never plug into the control LAN as an active node without engineering approval.

**Step 2 — capture and parse:**
```bash
# Receive-only capture
tcpdump -i eth0 -w ot_capture.pcap        # (interface in promisc, no active probes)
# Deep protocol analysis
zeek -r ot_capture.pcap                    # with ICS protocol analyzers/packages
# Wireshark dissectors understand modbus, dnp3, s7comm, cip, bacnet, iec104...
```

**Step 3 — passive asset inventory (purpose-built OT tools):**
- **GRASSMARLIN** (NSA, open-source) — passive ICS network mapper: builds a topology and device
  inventory from captured traffic alone.
- **Malcolm / Zeek + ICS plugins**, **Wireshark** ICS dissectors.
- Commercial passive OT monitoring (Nozomi, Claroty, Dragos, Tenable.ot) — deep protocol
  awareness and vuln matching without active probes.

**Step 4 — build the model:** device (vendor/model/firmware) ↔ role (PLC/HMI/historian) ↔
protocol ↔ communication peers ↔ zone/conduit (Purdue level). Map against **IEC 62443**
zones-and-conduits.

**Step 5 — vuln correlation (offline):** match passively-observed vendor/model/firmware against
ICS-CERT advisories and CVE DBs — **no active probing of the device required.**

---

## 4. Vulnerability logic (what "finding" means in OT)

- **Exposure = vulnerability.** A Modbus PLC reachable from the IT network (flat network, no
  segmentation) is itself the critical finding — anyone can read/write control registers unauthenticated.
- **Missing Purdue segmentation / IT-OT bridge** (dual-homed HMI, engineering laptop on both nets).
- **Legacy protocols with no auth/crypto** in use.
- **Outdated firmware** with published ICS-CERT advisories.
- **Remote-access exposure** (VPNs, vendor dial-in, exposed HMIs to internet — Shodan finds these).
- **Default credentials on HMIs/engineering workstations.**

---

## 5. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Can't actively scan | Devices crash under probes | Passive-only: SPAN/TAP + Zeek/GRASSMARLIN; active only on offline test rigs with sign-off |
| No visibility without a tap | Switched, no mirror configured | Work with plant engineers to enable SPAN or insert a TAP during a maintenance window |
| Proprietary/undocumented protocols | Vendor-specific fieldbus | Use commercial OT dissectors; correlate byte patterns to vendor docs; consult ICS-CERT |
| Passive misses silent devices | A device that never talks isn't seen | Longer capture windows spanning full process cycles; correlate with engineering asset lists |
| Fragile even to passive mistakes | Accidentally transmitting on RX port | Use hardware data-diode / RX-only cable; disable NIC TX; no DHCP/IPv6 chatter from your host |
| Firmware version not in traffic | Not all protocols announce it | Cross-reference with asset management, nameplate data, vendor portals |
| IT tools misidentify OT | Nmap/`-sV` probes can hang PLCs | **Exclude OT ranges from all IT scanners**; maintain a hard do-not-scan list |
| Air-gapped myth | "It's isolated" but isn't | Trace actual L2/L3 paths; find the dual-homed bridge that breaks the gap |

---

## 6. Considerations & guardrails (safety-critical)

- **Safety of people and process is paramount.** When in doubt, do less. A findings report is
  worthless if the assessment tripped a safety system.
- **Coordinate with OT/plant engineers at every step.** They know which devices are fragile.
- **Physically prevent transmission** on control segments (RX-only). Assume any packet you send
  could be the one that crashes a controller.
- **Active scanning, if ever authorized, is done on identical offline/spare hardware**, never on
  live production, and never without an engineer present and a rollback plan.

---

## 7. References

- IEC 62443 (Industrial Automation and Control Systems Security) — zones/conduits model.
- NIST SP 800-82 (Guide to Operational Technology Security) — the canonical OT security guide.
- Purdue Enterprise Reference Architecture (levels 0-5) for segmentation modeling.
- CISA ICS-CERT advisories (vulnerability source for OT devices).
- Protocol specs: Modbus Application Protocol, DNP3 (IEEE 1815), IEC 60870-5-104,
  ODVA CIP/EtherNet-IP, Siemens S7comm (reverse-engineered), OPC-UA (IEC 62541).
- Tools: GRASSMARLIN, Zeek + ICS analyzers, Wireshark ICS dissectors, Malcolm.
