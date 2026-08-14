# 01 — Network Discovery (Core-Level Playbook)

> **Goal:** From a single foothold system, enumerate *which hosts exist* on the reachable
> network(s) before spending effort on port/service/vuln work. Discovery is the foundation:
> everything downstream is wasted if your host inventory is wrong.
>
> **Authorized use only.** Everything here assumes you own the network or have written scope.

---

## 1. The core problem (why "ping the subnet" is naive)

Host liveness is **not** a single fact — it is a probabilistic inference from how a target's
network stack (and every device between you and it) reacts to a stimulus. A host can be:

- **Up but silent** to ICMP (firewall drops echo requests — extremely common on Windows/enterprise).
- **Up and answering only on L2** (responds to ARP but drops all IP-layer pings).
- **Down but impersonated** (a firewall or load balancer answers on its behalf).
- **Up but behind NAT/PAT** (you see one IP, many hosts).

So discovery = **send multiple stimulus types and treat *any* proof-of-life as "up."** This is
exactly the logic Nmap encodes in `nexthost()` / `pingtype` (see `fresh_implement.md §6`): the
default privileged ping is a *cocktail* — ICMP echo **+** TCP SYN to 443 **+** TCP ACK to 80 **+**
ICMP timestamp — precisely because no single probe is reliable.

---

## 2. Layer-by-layer core theory

### 2.1 Layer 2 (same broadcast domain) — ARP / NDP is ground truth
If your foothold is on the **same subnet** as the target, ARP (IPv4) or ICMPv6 Neighbor
Discovery (IPv6) is the single most reliable discovery method, and it is **unspoofably tied to
presence**:

- To send *any* IP packet to a local host, your kernel **must** resolve its MAC via ARP first.
- ARP operates below IP, so **L3 firewalls cannot filter it** — a host that ignores every ping
  still must answer ARP to function on the LAN.
- Nmap uses this automatically on Ethernet (`implicitARPPing`, `PING_SCAN_ARP`); any ARP reply =
  `HOST_UP`. `arp-scan --localnet` does the same standalone.

**Core mechanic:** you broadcast `who-has <IP> tell <you>` to `ff:ff:ff:ff:ff:ff`; a live host
unicasts `<IP> is-at <MAC>`. The MAC's first 3 bytes (OUI) also give you a free vendor
fingerprint (`nmap-mac-prefixes`) — VMware/Cisco/Apple/etc. before you send a single TCP packet.

**IPv6 twist:** there is no ARP and no broadcast. You use ICMPv6 Neighbor Solicitation to the
solicited-node multicast address, plus `ping6 ff02::1` (all-nodes). Sweeping a /64 by brute force
is impossible (2^64 addresses) — you must rely on multicast, Neighbor Discovery cache scraping,
DNS, and passive capture instead.

### 2.2 Layer 3 (routed / remote subnets) — ICMP + TCP/UDP probes
Once a router is between you and the target, ARP no longer reaches it. Now you rely on IP-layer
stimuli, each with different firewall-evasion properties:

| Probe | Nmap flag | Why it can succeed where others fail |
|-------|-----------|--------------------------------------|
| ICMP echo | `-PE` | Classic ping; blocked on many enterprise nets |
| ICMP timestamp | `-PP` | Older ACLs forget to block type 13 |
| ICMP addr-mask | `-PM` | Rarely blocked, rarely answered |
| TCP SYN 443/80 | `-PS443,80` | Firewalls that permit web traffic answer |
| TCP ACK 80 | `-PA80` | Slips stateless filters; RST proves host up |
| UDP 40125 | `-PU` | ICMP port-unreachable proves host up |
| SCTP INIT | `-PY` | Rarely filtered on telco nets |

The inference: a **SYN/ACK or RST** back proves the host's stack processed your packet → up.
An **ICMP unreachable** from the *target itself* also proves it is up (see Nmap's ICMP-code
table in `fresh_implement.md §5.6b`).

### 2.3 Passive discovery — the zero-packet method
You can enumerate hosts without sending anything by **listening**:
- ARP/NDP chatter, DHCP requests, mDNS/LLMNR/NBNS broadcasts, SSDP announcements, spanning-tree,
  gratuitous ARP — every host that boots or talks announces itself.
- Tools: `tcpdump`/`Zeek`/`p0f`; `netdiscover -p` (passive mode); `responder -A` (analyze-only).
- Passive `p0f` also **fingerprints OS from real traffic** (TTL, window size, options) — the same
  signals Nmap's active OS detection uses (`fresh_implement.md §9`), but invisible.

This is essential in **fragile networks (OT/ICS)** where active probing can crash devices
(see `06_ot_ics_passive.md`).

---

## 3. Approach from a single system in the network (methodology)

**Phase 0 — Situational awareness of your own host (do this first):**
```
ip a ; ip route ; ip neigh          # your interfaces, subnets, existing ARP cache
cat /etc/resolv.conf                 # DNS servers = often domain controllers
ip route get 8.8.8.8                 # which iface/gateway reaches the internet
```
Your **ARP/neighbor cache and routing table already list live hosts for free.** The default
gateway, DNS server, and DHCP server are guaranteed-live, high-value hosts.

**Phase 1 — Local subnet (L2):**
```
arp-scan --localnet --retry=3         # or: nmap -sn -PR 10.0.0.0/24
```
`-PR` forces ARP-only. Fast, reliable, gives MAC+vendor.

**Phase 2 — Remote subnets (L3):** enumerate routes you can reach, then sweep each:
```
nmap -sn -PE -PP -PS443,80,22 -PA80 -PU40125 --source-port 53 10.20.0.0/16
```
Multiple probe types + a trusted source port (53) to slip naive egress ACLs.

**Phase 3 — Reconcile with passive + DNS:**
- Reverse-DNS sweep the range (`nmap -sL` = list scan, no packets to targets, just PTR lookups).
- Pull DNS zone data / do reverse lookups against the discovered DNS server.
- Correlate DHCP leases, AD computer objects (`06`/`05` playbooks) if you have any credentials.

**Output artifact:** a canonical live-host list (IP, MAC, vendor, OS-hint, discovery-method)
feeding every other playbook. Save as Nmap XML so `08_rescan_delta.md` can diff it later.

---

## 4. Vulnerability-relevant signal you extract *during* discovery

Discovery is not just "up/down" — the *manner* of response leaks findings:

- **MAC OUI** → device class (printer, camera, PLC, hypervisor) → which downstream playbook.
- **TTL of replies** → OS family (64=Linux/Unix, 128=Windows, 255=network gear/Cisco).
- **IP-ID behavior** → predictable IP-ID = idle-scan zombie candidate + weak host (see Nmap
  IP-ID classes, `fresh_implement.md §9`).
- **Hosts answering ARP but not IP pings** → likely host-based firewall = a target worth deeper
  scanning, not skipping.
- **Rogue/unexpected hosts** → the finding itself (shadow IT, unmanaged device).

---

## 5. Challenges & how to tackle them (low-level)

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Hosts drop ICMP | Enterprise default-deny for ICMP | Add TCP SYN/ACK + UDP + SCTP probes; treat RST as "up" |
| Switched network hides hosts | Unicast traffic isn't flooded to your port | Use active ARP sweep (broadcast) or a SPAN/mirror port for passive |
| ARP cache poisoning risk | Your active ARP can be logged/detected | Rate-limit, randomize, or go passive on sensitive segments |
| IPv6 space too large to sweep | 2^64 hosts per /64 | Multicast (`ff02::1`), NDP cache scraping, DNS, passive only |
| NAC / 802.1X quarantine | Your foothold may be in a restricted VLAN | Discover the VLAN you're really in; look for voice/native VLAN hopping |
| Rate limiting / IDS triggers | Bursty sweeps look like a scan | Slow timing (`-T2`), randomize host order (`--randomize-hosts`), spread over time |
| False "up" from middleboxes | Load balancer/firewall answers for absent hosts | Corroborate with a second probe type + later port scan; a host that's "up" but has zero ports may be a phantom |
| Asymmetric routing / no return path | Reply routed elsewhere | Verify your source IP is routable back; use the correct egress interface (`-e`) |
| Duplicate/overlapping subnets (VPN) | Same RFC1918 range on two sides | Bind to specific interface; track by MAC not just IP |

---

## 6. Considerations & guardrails

- **Discovery *is* reconnaissance and is logged.** Do it under scope; note timestamps.
- **Be gentle on fragile networks** — see OT/ICS playbook; passive-first is the safe default.
- **Don't trust a single "down."** Absence of reply ≠ absence of host. Re-probe with alternate
  methods before excluding.
- **Inventory hygiene:** every downstream playbook consumes this host list — errors here
  multiply.

---

## 8. State-of-the-art: what the research literature actually proves

The following are the load-bearing findings from the top measurement/security-research groups
(Michigan/Stanford/Censys, TU Munich, MIT/ICSI/Berkeley-Paxson lineage). Each carries an
engineering lesson you must internalize before building a serious tool. *(Citations verified
against USENIX/ACM/SIGCOMM primary sources — see §11.)*

1. **Stateless scanning changes the cost model** — *Durumeric, Wustrow, Halderman, "ZMap: Fast
   Internet-Wide Scanning and Its Security Applications," USENIX Security 2013.* The entire IPv4
   space is scannable from **one machine in <45 min** at gigabit line rate, in userspace, by
   **eliminating per-connection state**. This reframes discovery: memory, not bandwidth, was the
   old bottleneck, and statelessness removes it. Follow-up *"Zippier ZMap" (WOOT 2014)* pushed to
   10 GbE.

2. **A port does NOT tell you the service** — *Izhikevich, Teixeira, Durumeric, "LZR: Identifying
   Unexpected Internet Services," USENIX Security 2021.* Only ~3% of HTTP and ~6% of TLS run on
   80/443; services are smeared across non-standard ports, and **services on unexpected ports are
   more likely insecure**. Consequence: any tool that maps "port → service" by IANA assignment
   *systematically under-reports risk*. You must confirm the service by **speaking its protocol**,
   and LZR shows you can identify 99% of services in ≤5 handshakes.

3. **Liveness is probabilistic and probe-dependent** — *Bano, Richter, Javed, Sundaresan,
   Durumeric, Murdoch, Mortier, Paxson, "Scanning the Internet for Liveness," ACM SIGCOMM CCR
   2018.* Running ICMP + 5 TCP + 2 UDP probes concurrently, they show **no single probe type sees
   all live hosts**, responsiveness across protocols is correlated, and "up/down" depends on probe,
   stack cross-layer effects, and filtering. This is the empirical justification for §1's
   "multiple stimuli, any proof-of-life = up."

4. **IPv6 cannot be brute-forced — you generate targets** — *Murdock, Li, Matthews, et al., "Target
   Generation for Internet-wide IPv6 Scanning" (6Gen), IMC 2017; Foremski, Plonka, Berger,
   "Entropy/IP," IMC 2016; Gasser et al., "Clusters in the Expanse: Understanding and Unbiasing
   IPv6 Hitlists," IMC 2018.* You learn address structure from seed sets (hitlists, rDNS, CT logs,
   passive) and **predict dense regions** rather than sweep 2^64. Modern work extends this with
   RL/GAN target generators. Any credible tool needs an IPv6 *target-generation* module, not a
   sweeper.

5. **Kernel bypass is how you go fast** — *Rizzo, "netmap: A Novel Framework for Fast Packet I/O,"
   USENIX ATC 2012 (Best Paper).* The three costs that kill packet rates are **per-packet
   allocation, syscall overhead, and copies**; netmap removes them via preallocated buffers,
   batching, and kernel/user shared memory. This is the theory behind PF_RING ZC, DPDK, and
   AF_XDP — the substrate of any line-rate engine.

6. **Passive monitoring is a first-class discovery method** — *Paxson, "Bro/Zeek: A System for
   Detecting Network Intruders in Real-Time," USENIX Security 1998 / Computer Networks 1999.* The
   founding work of network security monitoring: protocol-aware passive analysis. Combined with
   *Zalewski's p0f* (passive TCP/IP OS fingerprinting; book *Silence on the Wire*), you inventory
   and fingerprint hosts **without emitting a packet** — essential for fragile/OT nets (`06`).

7. **Fingerprint the stack, not the banner** — active TLS/SSH fingerprints resist banner spoofing:
   *JA3/JA3S (Althouse et al., Salesforce)* hash the TLS ClientHello/ServerHello; *JARM* actively
   fingerprints a TLS server; *HASSH* fingerprints SSH. Favicon **mmh3** hashing pivots across
   hosts (Shodan). These are the L7 analog of Nmap's OS fingerprint (`../fresh_implement.md §9`).

8. **Prioritize by probability of exploitation, not just severity** — *Jacobs, Romanosky, et al.,
   "Exploit Prediction Scoring System (EPSS)," FIRST.* CVSS measures worst-case severity; **EPSS
   predicts likelihood of exploitation in the wild**, and *CISA KEV* lists what is *actually* being
   exploited. A strong tool ranks findings by Exploitability(EPSS/KEV) × Exposure × Impact, not raw
   CVSS.

9. **You are scanning a noisy, adversarial Internet** — *Richter & Berger, "Scanning the Scanners,"
   IMC 2019; GreyNoise (Morris).* Background scan traffic is enormous; distinguishing your signal
   from noise, and being a good citizen (blocklists, abuse contact, rate governance — ZMap's
   published best practices), is part of correct engineering, not an afterthought.

---

## 9. Core techniques distilled (with the actual mechanisms)

### 9.1 Stateless asynchronous scanning (ZMap / Masscan)
The design that decouples throughput from memory:

- **Split send and receive into independent loops/threads.** The sender blasts SYNs as fast as the
  NIC allows; a separate receiver matches replies. There is **no connection table**.
- **Statelessness via a keyed hash in the packet.** ZMap sets the TCP **initial sequence number to
  a keyed hash (secret) over (dst IP, dst port)**. When a SYN-ACK returns, its **ACK = seq+1**, so
  the receiver recomputes the hash and validates the reply *without any stored state*. Masscan does
  the equivalent with SYN-cookie-style validation. Memory is O(1) in targets.
- **Address-space permutation without a shuffle table.** ZMap iterates the multiplicative group of
  integers mod a **prime p just above 2³²**, using a randomly chosen **primitive root g**: the
  sequence `x ← g·x mod p` visits every address exactly once in pseudo-random order, in constant
  memory (skip values ≥ 2³²). Masscan uses **BlackRock**, a Feistel/format-preserving-encryption
  permutation over the index space. Randomized order spreads load off any single destination
  network — both a politeness and an accuracy property.
- **Escape the host kernel's TCP stack.** When you inject raw SYNs, the kernel receives the
  SYN-ACKs for connections it never opened and **replies with RST**, corrupting results. Fixes:
  (a) an iptables/pf rule dropping outbound RST on the scan's source-port range, (b) a dedicated
  source-port range the kernel ignores, or (c) Masscan's approach — **ship your own userland
  TCP/IP stack** and don't involve the kernel at all.

### 9.2 Kernel-bypass packet I/O (the line-rate substrate)
To exceed ~1 Mpps you bypass the socket API (netmap's three-cost analysis, §8.5):
- **AF_XDP / XDP (eBPF)** — modern, in-tree Linux zero-copy path; the pragmatic default today.
- **DPDK** — poll-mode drivers, hugepages, dedicated cores; highest throughput, heaviest ops.
- **PF_RING ZC / netmap** — zero-copy rings, batching.
- Techniques throughout: **preallocated packet buffers, batched TX/RX, RSS multiqueue across cores,
  NUMA-aware memory, busy-poll instead of interrupts.**

### 9.3 Multi-probe liveness fusion (Bano et al.)
Do not treat discovery as a single ping. Fire **ICMP echo + ICMP timestamp + TCP SYN(443,80) +
TCP ACK(80) + UDP(53,161,123) + SCTP-INIT + ARP/NDP (local)** concurrently, and treat **any**
positive OR negative-but-host-sourced reply (RST, ICMP unreachable *from the target*) as "up."
Maintain a per-host **liveness vector** across probe types — it is itself a fingerprint (firewall
posture, OS) and a seed for correlated re-probing.

### 9.4 Application-layer confirmation (LZR)
After a port is open, **run the real handshake** to learn the true service (don't trust the port).
Send a battery of protocol openers (TLS ClientHello, HTTP GET, SSH banner read, DB greetings), and
identify from the response — the ZGrab2/LZR model, which is exactly Nmap's `-sV` probe/match engine
(`../fresh_implement.md §8`) generalized and sped up. This is where "scanning" becomes "attack
surface truth."

### 9.5 IPv6 target generation (not sweeping)
Feed a **seed hitlist** (public IPv6 hitlists, rDNS walking, CT logs, passive capture, DHCPv6/NDP
caches), learn address structure (Entropy/IP nibble distributions; 6Gen Hamming-distance clusters),
**generate candidate targets in dense regions**, then actively probe only those. Continuously fold
newly-found live addresses back into the seed set.

### 9.6 Passive fusion + spoof-resistant fingerprinting
- **Passive first where fragile** (`06`): Zeek + p0f over a SPAN/TAP inventory and OS-fingerprint
  with zero emitted packets.
- **Active fingerprints that survive lies:** JARM (TLS server), JA3S (TLS), HASSH (SSH), favicon
  mmh3, Nmap OS-fp. Prefer behavioral/structural fingerprints over banner strings, which are
  trivially forged.

### 9.7 Adaptive stateful depth (Nmap)
Breadth is stateless; **depth is stateful.** For version/OS/NSE, you want Nmap's RFC-2581-style
congestion control and RTT estimation (`../fresh_implement.md §7`) so deep probing self-tunes to
each host/link and doesn't melt fragile targets. The strongest tool uses **stateless for breadth,
stateful for depth.**

### 9.8 Vulnerability correlation & prioritization
- **Identify:** service+version → **CPE** → CVE (NVD), plus vendor advisories.
- **Confirm behaviorally:** run non-destructive checks (Nmap `vuln` NSE, nuclei templates) so a
  finding is *observed behavior*, not a version guess (versions lie — backported patches).
- **Prioritize:** score = **EPSS/KEV (likelihood) × exposure (reachability, internet-facing) ×
  impact (asset criticality)**, not raw CVSS.
- **Optional authenticated depth:** with in-scope creds, config/patch audits give the lowest
  false-positive rate.

---

## 10. Blueprint — architecture of a best-in-class scanner + vuln engine

Design principle: **separate the four concerns** so each can scale and be swapped independently.
Most tools conflate them and get stuck. The pipeline:

```
        ┌───────────────────────────────────────────────────────────────────┐
        │ (0) ORCHESTRATION / SCHEDULER  — scope, rate governance, sharding  │
        └───────────────────────────────────────────────────────────────────┘
             │            │                 │                    │
   ┌─────────▼──┐  ┌──────▼─────────┐  ┌────▼──────────┐  ┌──────▼───────────┐
   │ (1) TARGET │  │ (2) PACKET      │  │ (3) ANALYSIS  │  │ (4) INTELLIGENCE  │
   │ GENERATION │→ │ ENGINE (probe)  │→ │ (interpret)   │→ │ (correlate/score) │
   │ v4 perm +  │  │ stateless SYN + │  │ liveness,     │  │ CPE→CVE, EPSS/KEV,│
   │ v6 hitlist │  │ AF_XDP/DPDK,    │  │ svc-ID (LZR), │  │ behavioral checks,│
   │ + passive  │  │ stateful depth, │  │ fingerprints, │  │ risk ranking,     │
   │ seeds      │  │ passive sensors │  │ OS-fp         │  │ delta/ASM (08)    │
   └────────────┘  └─────────────────┘  └───────────────┘  └───────────────────┘
                                  │
                         ┌────────▼─────────┐
                         │ NORMALIZED STORE │  immutable, time-series, XML/JSON,
                         │ keyed (host,proto,port) → diffable (see 08)          │
                         └──────────────────┘
```

### Layer 0 — Orchestration & safety (build this FIRST, not last)
- **Scope engine:** authoritative include/exclude (CIDR, ASN, hostname), ownership verification,
  hard **do-not-scan lists** (OT/medical/fragile — `06`,`09`,`13`).
- **Rate governor:** global + per-/24 + per-host token buckets; ICMP-rate-aware for UDP (`11`).
- **Politeness:** blocklist honoring, reverse-DNS + abuse-contact on scan source, opt-out handling
  (ZMap best practices).
- **Distribution:** shard the address permutation across N source hosts by index range (each node
  owns a coprime stride), coordinate via a work queue; enables horizontal scale-out.

### Layer 1 — Target generation (decouple "what" from "how")
- IPv4: primitive-root permutation (§9.1) — no target list in memory.
- IPv6: hitlist + Entropy/IP/6Gen generator (§9.5), continuously seeded from results, passive, CT,
  rDNS.
- Feedback loop: live hosts and correlated-liveness seeds (§9.3) refine future target sets.

### Layer 2 — Probe engine (two engines behind one interface)
- **Breadth engine:** stateless async SYN/UDP/ICMP over AF_XDP/DPDK, keyed-hash statelessness,
  own userland stack (§9.1-9.2). Job: find open ports fast, at scale.
- **Depth engine:** stateful, congestion-controlled (Nmap-style) for service/OS/NSE on the reduced
  set (§9.7). Job: truth, gently.
- **Passive sensor:** Zeek/p0f tap feed merged as a probe-less source (§9.6).
- **Pluggable protocol probes** (module registry): each probe declares `{L3/L4, payload,
  match-logic}` — the LZR/ZGrab2 and Nmap-`service-probes` model, data-driven so new protocols ship
  as config, not code (`../fresh_implement.md §8`).

### Layer 3 — Analysis (interpret responses into facts)
- Liveness vector per host (§9.3); port state with **reason** (SYN-ACK/RST/ICMP-code/silence —
  `../fresh_implement.md §5`).
- Service identification by handshake (§9.4), not port; OS-fp; JARM/JA3S/HASSH/favicon fingerprints
  (§9.6).
- Emit **normalized records** `(host_id, proto, port) → {state, service, product, version, reason,
  fingerprints, evidence, ts}`. Stable `host_id` (MAC/cert/JARM/asset-id, not just IP) so deltas
  work (`08`).

### Layer 4 — Intelligence (turn facts into ranked risk)
- CPE→CVE mapping + vendor advisories; **behavioral vuln checks** (NSE/nuclei-style templates) for
  confirmation.
- **Prioritize with EPSS + CISA KEV + exposure + asset value** (§9.8), not raw CVSS.
- Feed the time-series store → **delta/ASM** (`08`) for continuous monitoring and remediation
  validation. Every finding ships with reproducible evidence (the probe + the response).

### Cross-cutting engineering choices
- **Data-driven everything:** probes, matches, fingerprints, and vuln checks are text/templates
  (Nmap's `-services`/`-service-probes`/`-os-db` philosophy) — community-updatable, no recompile.
- **Statelessness where possible, state where necessary.** Breadth stateless; depth stateful.
- **Immutable structured output** (XML/JSON) as the single substrate for diffing, reporting, and
  tool-chaining.
- **Safety as a feature:** fragile-host awareness, gentle timing modes, passive fallback, and
  "prove don't detonate" wired into the engine, not bolted on.

### Suggested build order (MVP → strong)
1. Orchestration + scope + rate governor + normalized store (the skeleton).
2. Stateless IPv4 SYN breadth engine on AF_XDP with keyed-hash statelessness.
3. Handshake-based service ID (start by wrapping ZGrab2/Nmap `-sV`).
4. CPE→CVE + EPSS/KEV prioritization; XML/JSON output.
5. Delta/ASM loop (`08`).
6. Passive sensor fusion (Zeek/p0f) + fingerprint layer (JARM/JA3S).
7. IPv6 target generation.
8. Behavioral vuln templates (nuclei/NSE) + authenticated checks.
9. Distribution/sharding for scale.

**Reality check / don't-reinvent:** the strongest *practical* tool today is usually an
**orchestrated pipeline** of proven components — `masscan`/`zmap` (breadth) → `zgrab2`/`nmap -sV`
(depth/service) → `nuclei` (behavioral vulns) → EPSS/KEV scoring → `ndiff`/ASM store — rather than a
monolith. Build the orchestration, data model, target generation, and prioritization (the parts
that don't exist off-the-shelf); wrap the battle-tested engines for the parts that do.

---

## 11. The verified best method (network scanning, core level) — evidence-backed

> This section is the payoff: the **single best-supported method** for core-level network
> discovery/scanning, with every claim **verified against primary sources** (ZMap USENIX Sec 2013;
> Zippier ZMap WOOT 2014; *Ten Years of ZMap* arXiv 2024; Bano et al. SIGCOMM CCR 2018; netmap ATC
> 2012; AF_XDP LPC 2018→). Numbers are quoted from those papers. See §12 for links.

### 11.1 The decision that dominates everything: stateless breadth, stateful depth
Do **not** pick one engine. The verified-optimal architecture is **two-phase scanning**
(*Ten Years of ZMap*, 2024, explicitly endorses this and warns against monoliths — "build small,
simple… tools that can be creatively assembled, rather than complex applications"):

- **Phase 1 — stateless L4 discovery** (ZMap/Masscan-class): find live hosts + open ports at line
  rate, O(1) memory.
- **Phase 2 — stateful L7 interrogation** (ZGrab2 / Nmap `-sV`/`-O`/NSE): confirm service, version,
  OS, vuln on the *reduced* set, gently, with congestion control.

This is not opinion — it is the design the ZMap authors converged on after a decade, and it
matches the LZR finding (§8.2) that **you must speak the protocol to know the service**.

### 11.2 Best method for accuracy (the counter-intuitive, verified parts)

1. **One well-formed probe is ~97–98% complete. Do NOT retransmit from the same host.**
   - Original ZMap: hosts **plateau after ~8 SYNs; a single SYN already achieves ~98% coverage.**
   - *Ten Years of ZMap* (2024): a single-probe scan misses only **~2.7% of HTTP(S) hosts.**
   - **Verified best practice:** the right fix for that last ~2% is **NOT** more probes from one
     scanner (correlated loss — "both probes are oftentimes lost"), but **2–3 geographically and
     topologically diverse vantage points.** *Path diversity beats probe repetition.*

2. **Make your SYN look real — carry TCP options.** *Ten Years of ZMap* (2024): including TCP
   options (**SACK-permitted, Timestamp, Window Scale, MSS**) yields a **+1.5–2.0% hit-rate**
   increase on TCP/80 vs an option-less SYN. Naked SYNs are dropped/filtered more. (Cost: throughput
   drops from **1.488 Mpps to ~1.276 Mpps on 1 GbE** with full option layouts — a worthwhile trade
   for accuracy.)

3. **Rate does not reveal more hosts — but too much rate loses them to YOUR upstream.**
   - Original ZMap: **no correlation between hit rate and scan rate** up to gigabit — *slower
     scanning does not find more hosts.*
   - Zippier ZMap: hit rate is **stable up to ~4 Mpps, then declines linearly**, and the cause is
     **upstream network congestion (your side), not the targets.**
   - **Verified best practice:** scan as fast as your *upstream* cleanly sustains; the accuracy
     knee is ~4 Mpps on a single well-provisioned 10 GbE path. Beyond that you lose hosts to your
     own congestion, not gain speed. Full IPv4 single-port ≈ **45 min at 1 GbE, ≈4.5 min at 10 GbE
     (~15 Mpps).**

4. **Multi-protocol liveness, not single ping.** Bano et al. (2018): no single probe sees all live
   hosts; responsiveness is correlated across protocols. **Best method:** fire ICMP-echo +
   ICMP-timestamp + TCP-SYN(443,80) + TCP-ACK(80) + UDP(53/161/123) + SCTP-INIT concurrently, and
   on-LAN prefer **ARP/NDP** (unfilterable, ground truth). Any positive *or* host-sourced negative
   (RST / ICMP-unreachable-from-target) = up.

### 11.3 Best method for the engine internals (core mechanics)

5. **Statelessness via keyed hash in the packet** (ZMap): put a secret keyed hash of
   `(dst IP, dst port)` in the TCP **sequence number**; validate returning SYN-ACKs by
   `ACK = seq+1`. No connection table → O(1) memory. Suppress the host kernel's stray **RSTs**
   (firewall the source-port range) or run your **own userland stack** (Masscan).

6. **Address permutation with zero state:** iterate the multiplicative group mod a prime just above
   2³² via a **primitive root** (`x ← g·x mod p`) to visit every IPv4 address once in random order.

7. **Sharding = "pizza," not "interleaved."** *Ten Years of ZMap* (2024): pizza sharding (contiguous
   ranges of the cyclic group) **superseded interleaved sharding in 2017** because it is "easier to
   reason about and implement without off-by-one errors or infinite loops." Use it to split work
   mutex-free across senders/threads.

8. **Deduplicate blowback with a bounded window.** Hosts resend responses "in some cases
   indefinitely." *Ten Years of ZMap*: a **window of 10⁷ entries filters nearly all duplicates**
   (smaller at lower rates). Budget this ring buffer in the receiver.

9. **Kernel-bypass I/O for line rate** (netmap's 3-cost analysis — allocation, syscalls, copies):
   today's pragmatic best is **AF_XDP zero-copy with busy-poll** (in-tree Linux; reached
   **DPDK-parity when the packet is touched**, per Karlsson/Töpel), with **DPDK** as the ceiling for
   pure forwarding and **PF_RING ZC** as ZMap's classic 10 GbE path. Preallocate buffers, batch
   TX/RX, use RSS multiqueue, pin to NUMA-local cores.

### 11.4 Best method for correctness of results & citizenship (verified guidance)
- **Reuse before you scan:** *Ten Years of ZMap* (2024) — first check whether **Censys Research
  Access / Rapid7 Open Data** already answer the question; don't add Internet load needlessly.
- **Signal intent:** reverse-DNS + WHOIS on your scan source, an **opt-out** mechanism, and
  validate how your handshakes appear in target logs. Honor blocklists; randomized order (§6)
  spreads load.

### 11.5 The distilled recommendation (what "best" concretely is)
```
BREADTH (find):  stateless SYN with realistic TCP options (SACK/TS/WScale/MSS),
                 keyed-hash statelessness, pizza-sharded, primitive-root address order,
                 AF_XDP zero-copy, ≤ ~4 Mpps per clean 10GbE path, 10^7 dedup window,
                 8 s cool-down for late replies.  ONE probe/host.
ACCURACY (2%):   add 2–3 diverse vantage points — NOT extra probes from one host.
LIVENESS:        multi-protocol concurrent (ICMP+TCP-SYN/ACK+UDP+SCTP; ARP/NDP on-LAN).
DEPTH (know):    hand open (host,port) to stateful ZGrab2 / Nmap -sV/-O/NSE; congestion-controlled.
IDENTIFY SVC:    speak the protocol (LZR/ZGrab) — never trust port==service.
PRIORITIZE:      CPE→CVE, then rank by EPSS + CISA-KEV × exposure × asset value (not raw CVSS).
STORE/DIFF:      normalized (host_id, proto, port) records → time-series → ndiff/ASM (08).
CITIZENSHIP:     reuse Censys/Rapid7 first; signal intent; opt-out; honor blocklists.
```
Net: **the strongest core-level network tool is a two-phase, multi-vantage, stateless-then-stateful
pipeline** — verified by a decade of Internet-measurement research, not a single monolithic scanner.

---

## 12. References (canonical, verifiable)

**RFCs / protocols**
- RFC 826 (ARP), RFC 4861 (IPv6 Neighbor Discovery), RFC 792 / 4443 (ICMP / ICMPv6),
  RFC 1122 (host requirements), RFC 1812 (router requirements — ICMP rate limiting).

**Research papers (venue/year verified against primary sources)**
- Durumeric, Wustrow, Halderman. *ZMap: Fast Internet-Wide Scanning and Its Security
  Applications.* USENIX Security 2013 — statelessness, primitive-root address order, single-SYN
  ≈98% coverage, no hit-rate/scan-rate correlation.
- Adrian, Durumeric, Mori, Halderman. *Zippier ZMap: Internet-Wide Scanning at 10 Gbps.* USENIX
  WOOT 2014 — ~15 Mpps, full IPv4 in ~4.5 min; **hit rate stable to ~4 Mpps then declines linearly
  from upstream congestion**; PF_RING ZC zero-copy; address-generation sharding.
- Izhikevich, Durumeric, et al. *Ten Years of ZMap.* arXiv:2406.15585, 2024 — **authoritative
  retrospective**: single-probe misses ~2.7% of HTTP(S); TCP options give +1.5–2.0% hit rate;
  prefer 2–3 diverse vantages over repeat probes; **pizza sharding**; 10⁷ dedup window; two-phase
  (L4/L7) scanning philosophy; citizenship guidance.
- (+ Censys, ACM CCS 2015; *ZBanner: Fast Stateless Scanning Capable of Obtaining Responses over
  TCP*, arXiv:2405.07409, 2024 — stateless banner grabbing.)
- Karlsson, Töpel. *The Path to DPDK Speeds for AF_XDP.* Linux Plumbers Conf 2018 (+ subsequent
  busy-poll work) — AF_XDP zero-copy reaching DPDK-parity when the packet is touched.
- Izhikevich, Teixeira, Durumeric. *LZR: Identifying Unexpected Internet Services.* USENIX
  Security 2021.
- Bano, Richter, Javed, Sundaresan, Durumeric, Murdoch, Mortier, Paxson. *Scanning the Internet
  for Liveness.* ACM SIGCOMM CCR 2018.
- Murdock, Li, Matthews, et al. *Target Generation for Internet-wide IPv6 Scanning* (6Gen). IMC
  2017. Foremski, Plonka, Berger. *Entropy/IP.* IMC 2016. Gasser et al. *Clusters in the Expanse:
  Understanding and Unbiasing IPv6 Hitlists.* IMC 2018.
- Rizzo. *netmap: A Novel Framework for Fast Packet I/O.* USENIX ATC 2012 (Best Paper).
- Paxson. *Bro/Zeek: A System for Detecting Network Intruders in Real-Time.* USENIX Security 1998 /
  Computer Networks 1999.
- Richter, Berger. *Scanning the Scanners: Sensing the Internet from a Massively Distributed
  Network Telescope.* IMC 2019.
- Jacobs, Romanosky, et al. *Exploit Prediction Scoring System (EPSS).* FIRST (first.org/epss).

**Practitioner work / blogs / tools**
- Robert Graham — **Masscan** (own userland TCP/IP stack, BlackRock address permutation).
- Michal Zalewski (lcamtuf) — **p0f v3**, book *Silence on the Wire* (passive fingerprinting).
- John Althouse et al. (Salesforce) — **JA3/JA3S**, **JARM**, **HASSH** fingerprinting.
- Salvatore Sanfilippo (antirez) — **idle scan / IP-ID side channel** (hping), original concept.
- Gordon Lyon (Fyodor) — *Nmap Network Scanning*; *Remote OS Detection via TCP/IP Stack
  Fingerprinting*.
- ProjectDiscovery — **nuclei/zgrab-style** behavioral templating; CISA **KEV** catalog.
- Andrew Morris — **GreyNoise** (internet background-noise characterization).

**This repo**
- Nmap engine internals: `../fresh_implement.md` (esp. §5 scan logic, §6 discovery, §7 timing,
  §8 version detection, §9 OS detection). Nmap source: `targets.cc`, `nmap.h:216-229`.
- Related playbooks: UDP nuance `11`, delta/ASM `08`, OT-safe passive `06`, full orchestration `02`.
