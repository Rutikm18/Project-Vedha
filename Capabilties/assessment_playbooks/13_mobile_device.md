# 13 — Mobile Device Assessment (Core-Level Playbook)

> **Goal:** Assess mobile devices (iOS/Android phones, tablets) as **network participants** — the
> services they expose on Wi-Fi, the debug/management interfaces they leave open, and the backend
> APIs their apps talk to. Also covers using a mobile device as a *scanning platform*. This is
> distinct from full mobile-app pentesting (static/dynamic binary analysis), which is noted but not
> the focus.

---

## 1. Core theory: modern phones are hardened clients but leaky peers

A stock, locked-down phone exposes very little — it is a **client**, initiating connections, rarely
listening. But real-world exposure comes from four places:

1. **Debug/dev interfaces left enabled:**
   - **Android Debug Bridge (ADB) over TCP** — port **5555**. If a developer enabled `adb tcpip
     5555`, *anyone on the network* can `adb connect` with **no authentication** and get a shell,
     install apps, read data. This is the single highest-impact mobile network finding (the
     "ADB.Miner" worm mass-exploited it).
   - iOS: `lockdownd` (62078/tcp) is present but pairing-record protected; jailbroken devices may
     run SSH on 22 with the infamous default root password `alpine`.
2. **Service-discovery chatter:** phones broadcast **mDNS/Bonjour** (5353), **AirDrop/AWDL**,
   **AirPlay**, **Google Cast**, **UPnP** — leaking device name, model, owner name (often "John's
   iPhone"), and capabilities. Great for inventory and social-engineering intel.
3. **App backend APIs:** the real attack surface is usually **server-side** — the REST/GraphQL APIs
   the mobile app consumes. These are assessed like web APIs (`10_web_app_triage.md`) but often
   have weaker auth because devs assume "only our app calls this."
4. **MDM / enterprise management:** MDM enrollment endpoints, and on-device MDM agents.

Additionally, phones are prime **AitM / rogue-AP targets** (they auto-join known SSIDs, and
certificate/transport security in apps varies).

---

## 2. Approach from a single system on the same network

**Step 1 — discover mobile devices (they're on Wi-Fi/DHCP):**
```bash
# OUI + mDNS reveal make/model/owner without touching the device much
nmap -sn -PR 192.168.1.0/24                      # ARP sweep; Apple/Samsung/Google OUIs
avahi-browse -art                                # Bonjour: "Johns-iPhone", model, services
nmap -sU -p5353 --script dns-service-discovery 192.168.1.0/24
```

**Step 2 — find exposed services:**
```bash
nmap -sS -p 22,62078,5555,5353,7000,8080,49152-49170 -sV <mobile_ip>
# ADB exposure (the big one)
nmap -p5555 --script adb-detect <mobile_ip>      # or: adb connect <ip>:5555 ; adb shell
# iOS jailbreak SSH
nmap -p22 --script ssh-auth-methods <ios_ip>     # test default alpine only if in scope
```

**Step 3 — app backend API assessment (the productive path):**
- Put the phone behind an **intercepting proxy** (Burp/mitmproxy) — configure device Wi-Fi proxy,
  install the CA cert (test device you own). Capture the app↔server traffic.
- **Certificate pinning** will block interception on hardened apps → bypass with Frida
  (`objection`, `frida-multiple-unpinning`) on a rooted/jailbroken test device (only your own
  device, in scope).
- Enumerate the API endpoints, auth (JWT/OAuth/API keys hardcoded in the app), and test the
  server-side vuln classes exactly as in `10_web_app_triage.md` (IDOR, broken auth, injection).

**Step 4 — (optional) app binary triage:** pull the APK/IPA, run `MobSF` for static analysis
(hardcoded secrets, insecure storage, exported components, weak crypto). This is app-layer, not
network — noted for completeness.

---

## 3. Vulnerability logic

- **Exposed ADB (5555)** → unauthenticated remote shell = full device compromise. Critical.
- **Jailbroken iOS SSH with default creds** → root shell.
- **Weak app-backend API** → IDOR/broken-auth/injection against server data (highest business
  impact; often the real prize).
- **No certificate pinning / accepts user CAs** → traffic interception, credential/token theft.
- **Insecure local storage** (secrets/tokens in plaintext) → data theft if device compromised.
- **Exported Android components** (activities/services/content providers) → local privilege/data
  issues (app-layer).
- **Info leakage via mDNS/Bonjour** → owner identity, device model → targeted phishing.
- **MDM misconfig** → enrollment abuse, policy bypass.

---

## 4. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Phones expose almost nothing | Hardened clients, no listening services | Focus on app-backend APIs + debug interfaces (ADB) + service-discovery intel |
| Certificate pinning blocks interception | App validates server cert | Frida/objection unpinning on your own rooted/jailbroken test device; patch APK; use a test build |
| Client IP churns (DHCP/Wi-Fi roaming) | Mobility | Track by MAC (note: MAC randomization complicates this); short scan windows |
| MAC randomization | iOS/Android privacy feature | Correlate via mDNS names, DHCP hostnames, traffic patterns rather than MAC |
| No root/jailbreak available | Can't bypass pinning or inspect storage | Assess server APIs directly (they're the real surface); static-analyze the binary (MobSF) |
| ADB test risk | `adb shell` on someone's phone is intrusive | Only on authorized/owned test devices; prove exposure via `adb connect` banner, don't rummage |
| Encrypted app traffic everywhere | TLS by default | Proxy + CA on test device; pinning bypass; or analyze API from a legit account |
| App-specific transports (QUIC/HTTP3, gRPC, MQTT) | Non-HTTP APIs | Use protocol-aware proxies; capture with pcap and dissect |
| Privacy/legal sensitivity | Personal device & data | Test only owned/authorized devices; never access personal data beyond proof |

---

## 5. Using a mobile device *as* the scanning platform (brief)

- Rooted Android runs Nmap, Termux (full Linux toolchain), and can do on-network recon from within
  a target Wi-Fi — useful for walk-around/wireless assessments.
- Constraints: battery/thermal, no raw-socket without root (falls back to connect scan —
  `fresh_implement.md §3b`), NIC limitations. Treat as a convenient sensor, not a workstation.

---

## 6. Considerations & guardrails

- **Only your own or explicitly authorized devices.** Mobile devices hold intensely personal data;
  scope and consent are paramount. Prove exposure (e.g., ADB reachable) without browsing private
  content.
- **The backend API is usually the real target** — that's where impactful, in-scope findings live,
  and it's assessed with web methods.
- **Pinning bypass and rooting are for test devices you control**, never a third party's phone.
- **MAC randomization + mobility** make inventory tracking harder — rely on multiple signals.

---

## 7. References

- **OWASP MASVS** (Mobile Application Security Verification Standard) and **OWASP MASTG** (Mobile
  Application Security Testing Guide) — the definitive mobile methodology.
- OWASP Mobile Top 10.
- Android ADB documentation (developer.android.com); ADB.Miner worm analysis (port 5555 mass abuse).
- Tools: Nmap, mitmproxy/Burp, Frida + objection, MobSF, apktool/jadx, `avahi-browse`.
- Cross-refs: server APIs → `10_web_app_triage.md`; service discovery → `09_iot_embedded_survey.md`;
  scanning internals → `../fresh_implement.md`.
