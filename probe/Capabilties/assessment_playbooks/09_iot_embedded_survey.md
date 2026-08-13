# 09 — IoT / Embedded Device Survey (Core-Level Playbook)

> **Goal:** Discover and assess consumer/enterprise IoT and embedded devices (cameras, printers,
> NAS, smart-building gear, routers, VoIP phones, medical/embedded appliances) on a network. These
> devices are numerous, long-lived, rarely patched, and ship with weak defaults — a top source of
> real-world compromise (Mirai and successors).

---

## 1. Core theory: embedded devices announce themselves and trust the LAN

Two properties define the IoT surface:

1. **Discovery protocols leak everything.** IoT devices are built to be *found* on a LAN, so they
   broadcast/multicast rich self-descriptions:
   - **SSDP/UPnP** (UDP 1900) — `M-SEARCH` multicast → devices reply with an XML **device
     description URL** (`/rootDesc.xml`) exposing make/model/firmware/services. UPnP also offers
     **port-mapping** (WANIPConnection) — historically abusable to open holes through NAT.
   - **mDNS / DNS-SD** (UDP 5353, `_services._dns-sd._udp`) — Bonjour/Avahi: printers, Chromecasts,
     HomeKit, etc. announce service types and TXT records (model, capabilities).
   - **WS-Discovery** (UDP 3702) — ONVIF cameras, printers.
   - **SNMP** (UDP 161) — see `12_snmp_exposure.md`; huge info disclosure with `public` community.
   - **CoAP** (UDP 5683) — constrained-device REST; `.well-known/core` lists resources.
   - **MQTT** (TCP 1883 / 8883 TLS) — pub/sub broker; often no auth → subscribe to `#` reads all
     telemetry/commands.

2. **They trust the local network.** Weak/no auth, default creds, cleartext protocols (telnet 23,
   HTTP admin), old TLS, and firmware full of N-day CVEs. The device assumes anyone on the LAN is
   friendly.

Common ports: 23 (telnet), 80/443/8080/8443 (embedded web admin), 554 (RTSP cameras), 5000
(UPnP/synology), 1883/8883 (MQTT), 5683 (CoAP), 9100 (raw printing), 631 (IPP), 37777 (Dahua),
7547 (TR-069 CWMP), 8291 (MikroTik), 49152+ (UPnP dynamic).

---

## 2. Approach from a single system (methodology + commands)

**Step 1 — passive + multicast discovery (cheap, rich):**
```bash
# SSDP/UPnP
python3 -c "import socket,struct;..."           # or:
nmap -sU -p1900 --script upnp-info <cidr>
# mDNS / DNS-SD
avahi-browse -art            # or: dns-sd -B _services._dns-sd._udp
nmap -sU -p5353 --script dns-service-discovery <cidr>
# WS-Discovery (cameras/printers)
nmap -sU -p3702 --script broadcast-ws-discovery
```

**Step 2 — active fingerprint of the web/admin surface:**
```bash
nmap -sS -p 23,80,81,443,554,631,1883,5000,7547,8080,8443,9100,37777 \
     -sV --script "http-title,http-headers,rtsp-methods,mqtt-subscribe,banner" \
     -iL live.txt -oX iot.xml
# Grab UPnP device description
curl -s http://<host>:PORT/rootDesc.xml
```

**Step 3 — identify make/model/firmware:** from UPnP XML, mDNS TXT, HTTP titles/favicons, SNMP
sysDescr, RTSP `OPTIONS`/`DESCRIBE`, and banner strings. Model+firmware → CVE lookup.

**Step 4 — default-credential & known-CVE checks (in scope):**
- Try documented default creds (admin/admin, root/root, vendor-specific) — **single, careful
  attempts**, respecting lockout.
- Camera-specific: RTSP stream access without auth, ONVIF unauthenticated, known backdoors
  (e.g., historical Dahua/Hikvision auth-bypass CVEs).
- MQTT: subscribe to `#` (wildcard) → if it returns data, broker is unauthenticated (finding).
- CoAP: `GET /.well-known/core` → resource enumeration.

---

## 3. Vulnerability logic

- **Default / hardcoded credentials** — the #1 IoT issue (Mirai's entire propagation method).
- **Unauthenticated services** — open MQTT broker, open RTSP camera, UPnP exposing internal LAN,
  CoAP without DTLS.
- **N-day firmware CVEs** — model+firmware → known RCE/auth-bypass (routers, cameras, NAS).
- **Cleartext admin** — telnet/HTTP admin, credentials sniffable.
- **UPnP exposure** — internal UPnP reachable from WAN, or port-mapping abuse.
- **TR-069 (CWMP 7547)** exposure — ISP management protocol; historically mass-exploited.
- **Weak crypto / no TLS** — telemetry and control in cleartext.
- **Amplification participants** — SSDP/SNMP/CoAP as DDoS reflectors (`11_udp_service_exposure.md`).

---

## 4. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Fragile devices crash on scan | Minimal stacks (like OT-lite) | Gentle timing, `-sT` over `-sX/-sN`, avoid aggressive NSE; treat medical/critical IoT like OT (`06`) |
| Non-standard ports/protocols | Vendor idiosyncrasy | Broad `-sV --version-all`; parse UPnP/mDNS for the real service map |
| Model/firmware hard to pin | Sparse banners | Combine UPnP XML + mDNS TXT + SNMP sysDescr + favicon hash + RTSP DESCRIBE |
| Default-cred testing risks lockout/DoS | Weak devices, aggressive brute | One or two documented defaults only; no mass brute; watch device health |
| Huge device count | Consumer-scale networks | Cluster by OUI/model; sample per model; prioritize internet-reachable |
| Devices on separate VLAN/SSID | Segmentation | Note reachability; pivot only within scope |
| Encrypted/proprietary control | Vendor cloud tunnels | Passive traffic analysis; correlate to cloud endpoints |
| Ephemeral / mobile IoT | Phones, wearables come and go | Combine with mDNS/passive continuous capture |
| Legal sensitivity (cameras, medical) | Privacy/safety | Never view/stream personal camera feeds beyond proving access; treat medical as safety-critical |

---

## 5. Considerations & guardrails

- **Some IoT is safety- or privacy-critical** (medical devices, cameras, building controls). Treat
  medical/industrial IoT with **OT-level caution** (`06`). Prove access without viewing private
  feeds or altering device behavior.
- **Default-cred and firmware exploits can brick devices** — validate exposure conservatively.
- **UPnP/SSDP probing is broadcast-noisy** — coordinate on production networks.
- **Amplification testing** must never actually flood a third party — measure the amplification
  factor safely, don't weaponize.

---

## 6. References

- UPnP Device Architecture (Open Connectivity Foundation); RFC 6762 (mDNS), RFC 6763 (DNS-SD),
  RFC 7252 (CoAP), OASIS MQTT 3.1.1/5.0, RFC 2326 (RTSP), TR-069/CWMP (Broadband Forum).
- OWASP **IoT Top 10** and OWASP IoT Security Testing Guide; ENISA IoT security baselines.
- NIST **IR 8259 / SP 800-213** (IoT device cybersecurity); ETSI EN 303 645 (consumer IoT).
- Mirai botnet analysis (default-credential telnet propagation) — canonical IoT-threat case study.
- Nmap NSE: `upnp-info`, `broadcast-*`, `mqtt-subscribe`, `rtsp-*`, `coap-resources`, `snmp-*`.
