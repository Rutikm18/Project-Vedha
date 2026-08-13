# 11 — UDP Service Exposure (Core-Level Playbook)

> **Goal:** Reliably enumerate UDP-based services — the perennially under-scanned, high-value
> surface hiding DNS, SNMP, NTP, TFTP, VPN (IKE), SIP, DHCP, mDNS, SSDP, and the amplification
> vectors used in DDoS. UDP scanning is *hard and slow* for reasons rooted in the protocol; this
> playbook explains why and how to do it right.

---

## 1. Core theory: UDP is connectionless, so "no reply" is ambiguous

TCP gives you a handshake: SYN→SYN/ACK (open) or SYN→RST (closed). UDP has **no handshake**. When
you send a UDP datagram to a port, three things can happen (see Nmap's exact logic,
`fresh_implement.md §5.8`):

1. **The service replies with a UDP packet** → **open** (unambiguous, but many services stay
   silent unless spoken to in their own protocol).
2. **The host replies with ICMP port-unreachable (type 3, code 3)** → **closed**.
3. **Silence** → **open|filtered** — you *cannot distinguish* an open service that simply didn't
   answer your (wrong) payload from a firewall dropping the packet.

This is why UDP scans are dominated by `open|filtered` noise unless you send the *right* payload.

### 1.1 The two hard problems
- **The silent-open problem:** a DNS server won't answer garbage on 53; it answers a **valid DNS
  query**. So generic empty UDP probes miss most services. **Solution: protocol-specific
  payloads.** Nmap ships these (`payload.cc`, `nmap-payloads`): a real DNS query to 53, SNMP
  get-request to 161, NTP query to 123, etc. A correct payload turns silent-open into a clear reply.
- **The ICMP rate-limit problem:** RFC 1812 tells routers/hosts to **rate-limit ICMP error
  generation** (e.g., 1/sec). Since "closed" is proven by an ICMP port-unreachable, rate limiting
  means Nmap can't tell "closed" from "dropped" fast enough, so it must **slow down and wait** — the
  root cause of UDP scans taking hours. Linux default is ~1 ICMP dest-unreachable/sec, which is
  brutal for scanning 65k ports. Nmap's congestion control (`fresh_implement.md §7`) adapts, and
  `--defeat-icmp-ratelimit` trades accuracy for speed by treating silence as `closed|filtered`.

---

## 2. High-value UDP services (what you're hunting)

| Port | Service | Why it matters |
|------|---------|----------------|
| 53 | DNS | Zone transfer, recursion (amplification), cache poisoning, version leak |
| 67/68 | DHCP | Rogue server, option leakage, starvation |
| 69 | TFTP | No auth; config/firmware download (routers, phones) |
| 123 | NTP | `monlist` (CVE-2013-5211) → huge amplification + host list leak |
| 137/138 | NetBIOS | Name/service leakage on Windows |
| 161 | SNMP | Massive info disclosure / write access — see `12_snmp_exposure.md` |
| 500/4500 | IKE/IPsec | VPN fingerprint, aggressive-mode PSK capture |
| 514 | Syslog | Log injection / info |
| 623 | IPMI/RMCP | BMC — cipher-0 auth bypass, hash disclosure (server lights-out) |
| 1194 | OpenVPN | VPN exposure |
| 1900 | SSDP/UPnP | Amplification + internal LAN exposure (`09`) |
| 5060 | SIP | VoIP enumeration, toll fraud |
| 5353 | mDNS | Device/service discovery leak |
| 11211 | memcached | Unauth data + record-breaking amplification (`04`) |

Amplification vectors (DNS, NTP monlist, SSDP, memcached, CLDAP, chargen) are both a **DDoS-reflector
finding** and an exposure to report.

---

## 3. Approach from a single system (methodology + commands)

**Step 1 — scan the *right* ports with payloads, not all 65k:**
```bash
# Top UDP ports with version/payload probes (fast, high-yield)
nmap -sU -sV --top-ports 100 -T4 --min-rate 100 -iL live.txt -oX udp.xml
# Targeted high-value set
nmap -sU -sV -p 53,67,69,123,137,161,500,623,1900,5060,5353,11211 <hosts>
```
`-sV` is important on UDP: it drives Nmap to send the protocol-specific payloads that elicit
replies, resolving `open|filtered` into `open`.

**Step 2 — protocol-specific validation (turn open|filtered into fact):**
```bash
dig @<host> version.bind chaos txt      # DNS version + recursion test
snmpwalk -v2c -c public <host> system   # SNMP (12)
ntpq -c rv <host> ; ntpdc -c monlist <host>   # NTP monlist / amplification
ike-scan <host>                          # IKE/IPsec VPN fingerprint + aggressive mode
tftp <host> -c get <known_file>          # TFTP read test
```

**Step 3 — measure amplification safely:** compare response size vs request size (bandwidth
amplification factor) — **measure, do not weaponize**; a single request proves the vector.

**Step 4 — accept residual ambiguity honestly:** report `open|filtered` ports as "potentially
exposed — could not confirm closed," not as clean.

---

## 4. Vulnerability logic

- **Unauth info disclosure:** SNMP `public`, NTP `monlist`, DNS version, mDNS/NetBIOS leakage.
- **Amplification/reflection participant:** open resolver, NTP monlist, SSDP, memcached, chargen —
  the host can be abused for DDoS (report + measure BAF).
- **No-auth file/config access:** TFTP (router/phone configs with credentials), IPMI/BMC (cipher-0).
- **VPN weaknesses:** IKE aggressive mode PSK capture → offline crack.
- **VoIP:** SIP enumeration → toll fraud, credential harvest.

---

## 5. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Scans take hours/days | ICMP rate-limiting (RFC 1812) makes "closed" slow to confirm | Scan only high-value ports (`--top-ports`), tune `--min-rate`/`--max-retries`, or `--defeat-icmp-ratelimit` (accepts less certainty) |
| Everything shows open|filtered | Silent-open + generic probes | Use `-sV` and protocol payloads (`nmap-payloads`); validate with native clients (dig/snmpwalk/ike-scan) |
| Reliability: dropped UDP replies | UDP is lossy, no retransmit | Increase `--max-retries`; re-scan uncertain ports; corroborate with protocol clients |
| Spoofing/source confusion | Stateless — replies may be forged | Verify replies come from the target IP; sanity-check payload contents |
| Firewalls silently drop | UDP heavily filtered at perimeter | Pivot to internal foothold; note perimeter posture |
| False amplification test = real DDoS | Repeated large requests flood victims | One measurement request only; never loop; never spoof a victim source |
| IPMI/BMC fragility | Lights-out controllers are delicate | Gentle probing; these are OT-adjacent (`06`) |
| NAT hides UDP services | Stateful NAT mapping | Test from the correct network position; short-lived UDP mappings expire fast |

---

## 6. Considerations & guardrails

- **Amplification vectors are dual-use.** Prove existence and measure the factor with a *single*
  request. Never source-spoof or loop — that is launching a DDoS.
- **UDP results are inherently less certain** than TCP; report confidence honestly
  (open vs open|filtered).
- **Some UDP services are fragile** (IPMI, embedded) — treat like IoT/OT.
- **Budget time deliberately** — full UDP `-p-` across many hosts is rarely worth it; prioritize.

---

## 7. References

- RFC 768 (UDP), RFC 1122 (host requirements), RFC 1812 (router requirements — **ICMP rate
  limiting**, the root cause of slow UDP scans), RFC 792 (ICMP unreachable codes).
- Nmap UDP internals: `../fresh_implement.md §5.8`; payloads: `nmap/payload.cc`, `nmap-payloads`.
- US-CERT/CISA alert TA14-017A (UDP-based amplification attacks) — DNS/NTP/SNMP/SSDP/chargen BAFs.
- CVE-2013-5211 (NTP monlist amplification); memcached amplification (2018 record DDoS).
- Tools: `nmap -sU -sV`, `dig`, `snmpwalk`, `ntpq`/`ntpdc`, `ike-scan`, `responder`, `unicornscan`.
