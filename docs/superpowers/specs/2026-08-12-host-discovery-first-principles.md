# Vedha Host-Discovery Engine — First-Principles Design

**Date:** 2026-08-12
**Status:** Design reference. Complements the approved build spec
`2026-08-10-native-host-discovery-engine-design.md` (tiered A–D engine). This
document is the *why* at packet/OS level; that document is the *what to build*.
**Scope of the code change shipped alongside this doc:** the unprivileged
Tier-D slice in `probe/scanner/host_discovery.py` was upgraded from a boolean
`alive` to a **freshness-graded, confidence-scored state model** (see §17).

> Guiding claim, stated plainly and defended below: **for a vulnerability
> scanner, a false negative in host discovery is the worst possible error** —
> a missed asset is silently excluded from the entire assessment. Every design
> choice below biases toward "never drop a real host" while still *labelling*
> how trustworthy each liveness claim is, so we don't turn that bias into a pile
> of unverified noise.

---

## 1. What "host alive" actually means

Liveness is not one predicate. Precise definitions:

| Term | Definition | Evidence that establishes it |
|---|---|---|
| **alive** | A network stack at this IP is powered and processing packets *now*. | A response the target itself generated. |
| **reachable (from vantage V)** | Packets from V can elicit a response from the target *along the current path*. | Any reply reaching V. Path-dependent. |
| **observed** | Some system saw traffic attributable to this IP at some time. | Passive capture, a log, a cache entry. |
| **recently observed** | Observed within a freshness window (seconds–minutes). | Timestamped observation < window. |
| **filtered** | Something is dropping our stimulus; we cannot conclude up or down. | Silence, or an ICMP *admin-prohibited* from a middlebox. |
| **unreachable (from V)** | The network told us the target cannot be reached from V. | ICMP host/net unreachable; ARP `FAILED` on-LAN. |
| **unknown / inconclusive** | No signal either way. | Silence with no corroborating cache/passive data. |
| **stale neighbor** | A MAC was learned once but is not currently confirmed. | ARP/NDP entry in `STALE` (or unknown-freshness) state. |
| **locally reachable** | Reachable at L2 on the same broadcast domain. | ARP/NDP resolves; no L3 routing involved. |
| **remotely reachable** | Reachable across ≥1 router. | Reply with decremented TTL / from a routed subnet. |

**Why "no response ≠ host is dead":** silence is produced by *at least five*
distinct causes that are indistinguishable from a single probe — (a) host down,
(b) host up but firewall `DROP` (not `REJECT`), (c) packet loss/congestion,
(d) rate-limiting/tarpit, (e) our own scanner exhausted (fd limits, buffer
pressure). Only (a) means "dead." Collapsing all five to `alive=false` is the
root false-negative generator.

**Host liveness ≠ port state.** "Host is up" is an L3/L2 fact about the machine.
"Port 443 is open" is an L4 fact about one service *as seen from this vantage*.
A host with every port filtered is still alive (Condition E). A port shown
`open` proves the host is alive, but a port shown `filtered` proves nothing
about the host. Vedha must never let "all probed ports filtered" imply "host
down" — that conflation is exactly what the old engine risked.

*Example.* A hardened Linux box: `iptables -P INPUT DROP`, only a WireGuard UDP
port open to specific peers. ICMP: dropped. All TCP: dropped. It is unambiguously
alive and, being on-LAN, answers ARP. A TCP-only scanner reports it down. ARP
freshness reports it up. That single example is the thesis of this design.

---

## 2. Discovery at packet level — the analysis frame

For every technique we answer the same ten questions: (1) packet sent, (2)
expected response, (3) what a response *proves*, (4) what silence means, (5) what
firewall/NAT changes, (6) same-subnet vs routed, (7) privilege required, (8)
false-positive risk, (9) false-negative risk, (10) recommended confidence.
Sections 2–7 apply that frame.

### Layer 2 — ARP (IPv4, same broadcast domain only)

```
Who has 192.168.1.68?  Tell 192.168.1.74      (broadcast, ff:ff:ff:ff:ff:ff)
192.168.1.68 is-at 34:f3:9a:a1:a9:8c          (unicast reply)
```

1. **Sent:** ARP request (broadcast) or, for us, an implicit one triggered by a
   `connect()` to an on-LAN IP.
2. **Expected:** unicast ARP reply carrying the MAC.
3. **Proves:** a device owning that IP is powered and on this L2 segment *right
   now* — the host's own NIC answered. This is the strongest on-LAN proof and is
   **unfilterable by L3 firewalls** (ARP is below IP; host firewalls filter IP,
   not the kernel's ARP responder).
4. **Silence:** on-LAN, a genuinely absent/off host does not answer → after
   retries the kernel marks the neighbor `FAILED`/`INCOMPLETE` (negative signal).
5. **Firewall/NAT:** cannot suppress a host's own ARP without breaking its LAN
   connectivity. *Proxy ARP* (§8-H) and *ARP suppression* on some fabrics/Wi-Fi
   change this — see below.
6. **Subnet:** ARP is **same-subnet only**. Across a router you never see the
   target's MAC, only the gateway's. Useless for routed discovery.
7. **Privilege:** sending a *raw* ARP frame needs `CAP_NET_RAW`/root
   (AF_PACKET). **Reading** the kernel neighbor cache is **unprivileged** — this
   is the lever Vedha's Tier-D uses.
8. **False positive:** proxy ARP; a router answering for absent hosts; a
   security appliance/tarpit answering for a whole range (§8-M). Duplicate IP
   (§8-N).
9. **False negative:** target on another VLAN; Wi-Fi client isolation; ARP
   suppression fabric; stale entry mistaken for fresh (the bug we fixed).
10. **Confidence:** fresh solicited reply **0.95**; unknown-freshness cache
    **0.5–0.55**; `FAILED` → negative.

**ACTIVE_ARP_REPLY vs ARP_CACHE_OBSERVED — the crux.** These are *not* the same
fact and must never share a confidence value:

- **ACTIVE_ARP_REPLY**: a reply solicited *by our probe*, confirmed by the kernel
  now → NUD `REACHABLE`. The host is up this second.
- **ARP_CACHE_OBSERVED**: a MAC the kernel learned earlier and has not
  re-confirmed → NUD `STALE` (Linux) or any resolved BSD entry (macOS gives no
  state). The host *was* here; it may have since powered off, roamed, or the IP
  may have been reassigned. Aging (`base_reachable_time` ≈ 30 s on Linux, then
  `STALE`) means a `STALE` entry can be up to `gc_stale_time` (default **60 s**,
  often minutes) old.

Vedha distinguishes them by reading the **NUD state**, unprivileged, per target,
*after* probing (so our own `connect()` has refreshed it). See §17 and the
shipped code.

Related L2 phenomena and how they bear on confidence:

- **Gratuitous ARP** (host announces its own IP↔MAC, e.g. on boot / failover):
  strong *passive* liveness + duplicate-IP detection input.
- **Proxy ARP:** a router answers for hosts it can route to → false positives if
  we treat the reply as endpoint proof (§8-H).
- **ARP suppression** (EVPN/VXLAN, some Wi-Fi controllers): fabric answers from a
  cache; you get a reply even when the host is momentarily silent — inflates
  freshness confidence, so on such fabrics treat ARP as MEDIUM, not HIGH.
- **VLAN boundaries / Wi-Fi client isolation:** you simply never see the frame →
  false negative unless you have a vantage in that segment (§15).
- **Virtualized/cloud:** often no real broadcast domain; ARP is emulated or
  absent. On cloud, L2 discovery is largely meaningless (§8-L).

---

## 3. ICMP discovery

| Message | Sent → Expected | Does receiving it prove the host exists? |
|---|---|---|
| **Echo request/reply (8/0)** | echo → echo reply | **Yes**, if the reply's source is the target. Many hosts (Windows default firewall, hardened Linux) drop echo yet are alive → echo silence is a weak negative. |
| **Timestamp (13/14)** | timestamp req → reply | Yes, and it catches ACLs that filter type 8 but forget type 13. Rare but a cheap extra. |
| **Address mask (17/18)** | mask req → reply | Mostly obsolete; a few embedded/IoT stacks answer. Low yield, keep as opportunistic. |
| **Dest Unreachable (3)** | — (elicited) | Depends on code & source: *port unreachable* (3/3) **from the target** proves the target is up (its stack generated it — very useful for UDP, §5). *Host unreachable* (3/1) **from a router** proves the router exists and the target does not answer — that is about the target being *unreachable*, not up. |
| **Admin Prohibited (3/13, 3/9, 3/10)** | — | Generated by a **firewall/router**, not the target. Proves an *enforcement point* exists on the path; says nothing definitive about the target. Confidence about the target: low. |
| **Time Exceeded (11)** | — (TTL=0) | From an intermediate router (traceroute mechanic). Maps the path/enforcement hop; not target liveness. |

**Key discriminator:** *who sourced the ICMP?* An ICMP error from the **target's
own IP** (e.g. port-unreachable) is endpoint proof of life. The same message
type from a **router/firewall IP** is proof about the *path*, not the host. Vedha
must compare the ICMP source address to the probed target before scoring.

Privilege: crafting/reading raw ICMP normally needs `CAP_NET_RAW`. Linux offers
an **unprivileged echo** path via `SOCK_DGRAM`+`IPPROTO_ICMP` gated by
`net.ipv4.ping_group_range` (Tier C in the build spec). Timestamp/error parsing
needs raw.

---

## 4. TCP-based discovery

### TCP SYN discovery (half-open)
```
SYN →   SYN/ACK  = host up + port OPEN        (conf ~0.97)
        RST/ACK  = host up + port CLOSED       (conf ~0.93; but see middlebox)
        (nothing) = filtered / lossy — AMBIGUOUS
        ICMP unreach from router = path says unreachable
```
- SYN/ACK: the target's stack completed half the handshake → alive + open.
- RST: the target's stack refused → **alive** + closed. Caveat: some firewalls
  emit RST *on behalf of* the host (`reject-with tcp-reset`). A stateful host RST
  and a middlebox RST look identical from one packet; TTL analysis (the RST's TTL
  vs. the host's known TTL, or vs. neighboring open-port TTLs) can *sometimes*
  separate the enforcement hop from the endpoint. Hence RST < SYN/ACK confidence.
- SYN vs full connect: SYN never completes the handshake (stealthier, faster, no
  app-layer state) but needs `CAP_NET_RAW`. Full connect completes the handshake
  (visible in target logs, slower) but is **unprivileged** — Vedha's default.

### TCP ACK discovery
```
ACK (to an unsolicited port) →  RST
```
A bare ACK matches no connection, so a live host's stack replies RST. Because the
ACK carries no SYN, **stateless** firewalls that only block "new" (SYN) flows may
pass it, and the resulting RST reveals the host. It distinguishes *stateful* vs
*stateless* filtering and can find hosts behind simple ACLs. Needs raw sockets.
Confidence of the RST as liveness: ~0.9 (again, middlebox-RST ambiguity).

### TCP connect discovery — what `asyncio.open_connection()` actually does
Underneath it calls `socket()` → `connect()` and awaits the kernel's non-blocking
handshake. The OS sends the SYN and the *kernel* interprets the result; Python
sees only the outcome:

| Outcome | errno | Proves about host |
|---|---|---|
| connected | — | **alive + open** (handshake done). |
| `ConnectionRefusedError` | `ECONNREFUSED` | **alive + closed** (RST received). |
| `TimeoutError` (our `wait_for`) | — | **filtered/ambiguous** — silence, not death. |
| reset mid-stream | `ECONNRESET` | alive (host RST). |
| `EHOSTUNREACH` | `EHOSTUNREACH` | router says host unreachable — *not* proof of death, path/ARP-fail. |
| `ENETUNREACH` | `ENETUNREACH` | network unreachable — routing problem, not host state. |
| `EHOSTDOWN` | `EHOSTDOWN` | on-LAN ARP failed — strong "down/absent" *from here*. |
| `EACCES`/`EMFILE`/… | local | **scanner-side** failure — must NOT be read as target state. |

`port_scanner.py:classify_os_error` already does this errno→state mapping
correctly; host_discovery reuses the same philosophy (silence = filtered, not
dead).

**FIN / NULL / Xmas scans:** these probe *port state* on RFC-793-compliant
stacks (closed port → RST, open port → silence). They are **firewall/port-state
inference tools, not host-discovery tools** — Windows/many stacks don't follow
the RFC, and "open|filtered" ambiguity makes them poor liveness signals. Do not
use them for discovery.

---

## 5. UDP discovery

UDP is hard because it is connectionless: an open UDP port that has nothing to
say to your payload stays **silent**, which is indistinguishable from filtered or
down. Two things break the tie:

```
UDP probe →  application reply           = host up + service up   (strong)
             ICMP port-unreachable (3/3) = host up, port closed   (strong! host's stack sent it)
             (nothing)                    = open|filtered|down     (useless alone)
```

**ICMP port-unreachable is the gem:** it is generated by the *target's own IP
stack*, so it proves liveness even when no service answers. But it is
**rate-limited** by most kernels (Linux `net.ipv4.icmp_ratelimit`), so a UDP
sweep gets only a trickle of them — pace accordingly.

**Protocol-aware probes only** (never random bytes — random UDP rarely elicits a
reply and can trip IDS):

| Port | Probe |
|---|---|
| 53 DNS | a real query (e.g. `A` for a root/`version.bind` CHAOS) |
| 123 NTP | mode-3 client / monlist-safe read |
| 161 SNMP | `GetRequest` for `sysDescr.0` with `public` (read-only) |
| 137 NBNS | node-status `*` query |
| 1900 SSDP | `M-SEARCH` ssdp:discover |
| 5353 mDNS | `_services._dns-sd._udp.local` PTR |
| 500/4500 IKE | IKE SA init (no payload commitment) |
| 67/68 DHCP | INFORM/DISCOVER (careful: broadcast, can disturb) — passive-preferred |
| 443 QUIC | QUIC Initial (v1) — modern, increasingly worth it |

Reply=unprivileged; catching the ICMP port-unreachable needs raw. Confidence:
app reply 0.9; port-unreachable 0.9; silence contributes nothing.

---

## 6. Passive discovery (observation, not stimulus)

Separate **active discovery** (we send packets) from **passive observation** (we
listen). Passive is zero-noise, safe on fragile/OT networks, and often reveals
hosts active discovery misses — but it only sees hosts that *happen to talk*.

Sources: ARP/gratuitous-ARP sightings, DHCP leases + `DISCOVER/REQUEST`
broadcasts, mDNS/LLMNR/NBNS name chatter, SSDP announcements, IPv6 NDP/RA,
router neighbor tables, switch CAM/MAC tables (via SNMP `dot1dTpFdb`),
NetFlow/IPFIX, DNS query logs, firewall logs, WLAN-controller client lists, raw
packet capture, endpoint/EDR telemetry.

- **Strengths:** unfilterable by target host firewalls (you observe its
  legitimate traffic), catches silent/privacy hosts, safe for OT (Vedha's `ot`
  profile is passive-only by design).
- **Limits:** only sees talkers; timing-dependent; some sources need infra access
  (SNMP to switches, NetFlow collectors).

**Confidence impact:** a *single* passive sighting is weaker than an active
endpoint reply (it can be replay/stale) → MEDIUM at best. **Multiple correlated**
passive sources (e.g. DHCP lease + mDNS + CAM entry within the window) raise
confidence toward HIGH. Passive evidence should *decay* with age (§11).

---

## 7. IPv6 host discovery — a different game

Brute-forcing a `/64` is **impossible**: 2⁶⁴ ≈ 1.8×10¹⁹ addresses. IPv6
discovery is therefore *observation- and multicast-driven*, not sweep-driven.

- **On-LAN is easy and strong:** ICMPv6 **Neighbor Solicitation** to the
  target's **solicited-node multicast** (`ff02::1:ffXX:XXXX`) →
  **Neighbor Advertisement** carrying the MAC = fresh L2 proof (the v6 analog of
  ARP; equally unfilterable). The **all-nodes multicast `ff02::1`** ping reveals
  many on-LAN hosts at once.
- **Router Advertisements / `ff02::2`** find routers; RAs also tell you the
  prefix(es) in use.
- **Off-LAN enumeration** relies on: DHCPv6 server leases, DNS (AAAA + reverse),
  passive capture, and *pattern heuristics* (many hosts use SLAAC EUI-64 →
  MAC-derived, or low-byte manual addresses like `::1`, `::53`). **Privacy
  extensions (RFC 4941)** and stable-privacy addresses defeat EUI-64 guessing —
  another reason on-LAN NDP + passive dominate.
- **Link-local (`fe80::/10`)** is per-interface and requires a scope id; useful
  only from a directly-attached vantage.

Practical strategy: **on-LAN → NDP + `ff02::1`**; **off-LAN → DNS + DHCPv6 +
passive + targeted heuristics**, never a blind sweep. Vedha should read the v6
neighbor cache the same unprivileged way it reads ARP (Linux `ip -6 neigh`).

---

## 8. Difficult / hidden host scenarios

| # | Scenario | How to discover / classify |
|---|---|---|
| **A** | ICMP blocked, TCP 443 open | TCP SYN/connect to 443 → SYN/ACK = **confirmed_alive**. Trivial; TCP path already covers it. |
| **B** | ICMP blocked, all tested TCP closed | If *any* port RSTs → alive (closed≠down). If truly all silent, fall to on-LAN ARP/NDP; if routed, **inconclusive** — widen port set / UDP. |
| **C** | ICMP + TCP silently dropped, same subnet | **ARP/NDP is the answer.** The host must ARP to use the LAN; our connect() elicits a fresh `REACHABLE` neighbor entry → confirmed_alive despite total L3 silence. (Our shipped fix.) |
| **D** | Phone asleep, Wi-Fi power-save | Intermittent. It still periodically wakes to renew DHCP / send mDNS / answer ARP. **Passive listening + retries over time** + ARP freshness catch it; a single-shot active probe often misses. |
| **E** | Host firewall drops all unsolicited packets | On-LAN: ARP/NDP proves liveness. Routed: cannot prove alive actively → **inconclusive**, lean on passive. Cannot prove *down* either. |
| **F** | Server on another VLAN, all probes filtered | From this vantage: **unreachable/filtered**, confidence about existence = low. Correct classification is *"not reachable from V"*, not "down." Needs a vantage in that VLAN (§15). |
| **G** | Gateway sends ICMP admin-prohibited | Proves a **firewall on the path** exists; about the target it's inconclusive. Record the enforcement hop; do not score the target up or down. |
| **H** | Proxy ARP answers for an absent host | Risk of false positive. Detect: the same MAC answering for many IPs (router's MAC), or ARP reply with no corroborating L3/UDP/passive signal. **Downgrade** ARP-only when the MAC is shared across a range. |
| **I** | Stale ARP entry | Read **NUD state**: `STALE`/unknown-freshness ⇒ `recently_observed`, not confirmed. Re-solicit (our connect() does) and re-check: `REACHABLE` ⇒ upgrade, `FAILED` ⇒ it's gone. (Shipped.) |
| **J** | NAT / load balancer / VIP | You are discovering a **service front**, not an individual host. One IP may fan out to many backends, or many IPs to one box. Label as `service_endpoint`, don't assert host cardinality. |
| **K** | Randomized-MAC mobile | Classify as *mobile/privacy device*; the locally-administered bit flags it (already implemented). Don't rely on OUI (randomized) — rely on behavior + fresh ARP. |
| **L** | Cloud instances / security groups | No real broadcast domain → ARP/NDP mostly meaningless; security groups default-deny → silence is the norm. Discovery shifts to **cloud API / metadata / passive flow logs**, not LAN sweeps. |
| **M** | IPS/tarpit answers for many addresses | Deception. Detect: implausibly uniform replies across a whole range, identical TTL/window fingerprints, every address "up," sticky RTTs. Flag `possible_deception`, lower confidence. |
| **N** | Duplicate IP conflict | Two MACs answer for one IP (ARP reply flapping / gratuitous-ARP storms). Detect conflicting `is-at` for the same IP; flag `duplicate_ip`. |
| **O** | Very slow / rate-limited host | Fixed short timeout false-negatives it. Use **adaptive timeout + limited retries with backoff**; treat rate-limit ICMP as a *presence* hint. |

---

## 9. Evidence hierarchy (critiqued, not accepted blindly)

The user's draft was close. Corrections: **ICMP port-unreachable belongs in VERY
HIGH** (it's endpoint-sourced, same class as RST). **ICMP echo reply is HIGH, not
top**, because some middleboxes proxy it and it's easily spoofed on a hostile
segment. **A lone passive sighting is MEDIUM-LOW**, not MEDIUM, unless
corroborated. Each signal is scored on five axes:

| Signal | Proof strength | Spoofable | Freshness | Same-subnet only | Routed OK | Weight |
|---|---|---|---|---|---|---|
| TCP SYN/ACK (from target) | endpoint, port-open | hard (needs path MITM) | now | no | yes | **0.97** |
| ICMP port-unreachable (from target) | endpoint | hard | now | no | yes | **0.95** |
| Fresh ARP/NDP reply (`REACHABLE`) | L2 endpoint | on-LAN only | now | **yes** | no | **0.95** |
| TCP RST (from target) | endpoint | middlebox may forge | now | no | yes | **0.93** |
| IPv6 Neighbor Advertisement (fresh) | L2 endpoint | on-LAN only | now | **yes** | no | **0.93** |
| ICMP echo reply | endpoint | moderate | now | no | yes | **0.88** |
| Multiple correlated passive obs | inferential | replay-able | window | varies | yes | **0.6–0.75** |
| ARP entry `DELAY/PROBE` | revalidating | on-LAN | ~now | yes | no | **0.75** |
| Single passive observation | inferential | yes | window | varies | yes | **0.5** |
| ARP `STALE` / unknown-freshness cache | historical | yes | up to minutes | yes | no | **0.5** |
| Silence | none | — | — | — | — | **~0.1 (inconclusive)** |
| ARP `FAILED`/`INCOMPLETE` on-LAN | negative | — | now | yes | no | **↓ down-ish** |

Spoofability matters for *trust*, freshness for *currency*, subnet-scope for
*where the claim is valid*. A production engine stores all three, not just the
scalar weight.

---

## 10. Confidence-based host-state model

Binary `alive` is insufficient. States:

- `confirmed_alive` — endpoint reply or fresh L2 proof (conf ≥ 0.90)
- `probably_alive` — corroborating-but-indirect / mid-revalidation (0.70–0.90)
- `recently_observed` — cache/passive only, unconfirmed now (0.30–0.70)
- `inconclusive` — silence, no corroboration (< 0.30, no negative proof)
- `unreachable_from_vantage` — network said unreachable / on-LAN ARP `FAILED`

Schema (superset of what `host_discovery.py` now emits; the extra `first_seen`/
`vantage`/multi-source aggregation is the store layer's job, §11/§15):

```jsonc
{
  "ip": "192.168.1.68",
  "state": "confirmed_alive",
  "confidence": 0.95,
  "alive": true,                       // legacy boolean, preserved
  "vantage": "probe-lan-01",
  "first_seen": "2026-08-12T09:00:01Z",
  "last_seen":  "2026-08-12T09:03:44Z",
  "reason": "syn_ack",
  "method": "tcp+arp",
  "mac": "34:f3:9a:a1:a9:8c",
  "arp_state": "reachable",
  "vendor": "Apple",
  "device_hint": "apple-mobile (iphone/ipad — lockdownd)",
  "evidence": [
    {"method": "tcp_connect", "port": 445, "result": "syn_ack",
     "confidence": 0.97, "observed_at": "…"},
    {"method": "arp_neighbor", "result": "reachable", "nud": "REACHABLE",
     "mac": "34:f3:9a:a1:a9:8c", "confidence": 0.95, "observed_at": "…"}
  ]
}
```

---

## 11. Freshness — avoiding stale-host false positives

The single most important anti-false-positive control. Rules:

1. **Every observation carries a timestamp.** Confidence *decays* with age.
2. **Grade neighbor entries by NUD**, don't treat "has a MAC" as "up." (Shipped:
   `REACHABLE` fresh, `STALE` old, `FAILED` gone.)
3. **Revalidate before asserting.** Our connect() re-solicits ARP so the entry
   we read is post-probe, not a random-age snapshot.
4. **Windowed decay** (recommended defaults): active endpoint reply full weight
   for ~30 s, then decay; ARP `STALE`/passive halved beyond ~60 s; drop to
   `inconclusive` beyond a few minutes without re-confirmation.
5. **`last_seen` drives the state machine**, not `first_seen`. An asset seen once
   an hour ago is `recently_observed` at best until re-probed.

Concretely: *fresh ARP reply 5 s ago* → `confirmed_alive` 0.95. *ARP cache entry
15 min old* → `recently_observed` ~0.4, flagged `revalidate`. Never the same.

---

## 12. Tiered discovery engine — pipeline (challenged)

The proposed Tier 0→6 ordering is sound with two refinements: **(a) run cheap
concurrent probes in parallel within a tier rather than strictly serial across
tiers**, and **(b) make Tier 0/1 (passive + on-LAN L2) authoritative enough to
short-circuit L3 probing on the LAN.**

```
Tier 0  Passive/cache read (neighbor cache, DHCP, mDNS)      [0 packets]
Tier 1  On-LAN: active ARP/NDP (or connect-elicited refresh)  [1 pkt/host]
Tier 2  ICMP echo/timestamp                                   [1–2/host]
Tier 3  TCP SYN to a few high-yield ports                     [n/host]
Tier 4  TCP ACK / full-connect fallback (unprivileged path)   [n/host]
Tier 5  Protocol-aware UDP (DNS/SNMP/NTP/…)                    [few/host]
Tier 6  Deeper retry/backoff for still-unresolved             [adaptive]
```

Decision flow per target:
```
on-LAN?
 ├─ yes → Tier 0 read; probe (connect/ARP); re-read neighbor.
 │         REACHABLE → confirmed_alive, EARLY-EXIT (skip ICMP/UDP).
 │         FAILED    → unreachable_from_vantage.
 │         else      → continue Tier 2–5, fuse.
 └─ no  → Tier 2 (ICMP if privileged) + Tier 3/4 (TCP) + Tier 5 (UDP) concurrently;
          any endpoint reply → confirmed_alive, early-exit;
          all silent → inconclusive (NOT down).
Privilege downgrade: raw tiers absent → Tier C/D unprivileged, logged, never fatal.
Profile gates: ot → passive only; iot → gentle small set, low rate.
```

Optimize for coverage first, then noise/speed. The refinement that matters most:
**on-LAN, L2 freshness is both cheaper and stronger than L3 probing**, so it
should gate everything else.

---

## 13. Early-exit strategy

- **Fresh ARP/NDP `REACHABLE` on-LAN ⇒ host proven up ⇒ cancel remaining L3
  discovery** for *liveness*. (Still run port/service scanning later if the job
  wants it — that's a different question.)
- **TCP RST/SYN-ACK ⇒ host proven up ⇒ cancel remaining discovery probes** for
  that host. The shipped code already cancels sibling port probes on first
  proof-of-life.
- **When NOT to early-exit:** if you also want the *fingerprint* yield (TTL→OS,
  MAC→vendor, which ports answer), one more probe may be worth it. Keep
  early-exit for the *liveness* decision but let a job opt into "gather full
  evidence vector" for asset intelligence.

---

## 14. Packet budget

Order-of-magnitude, hosts-in-range (not all live):

| Strategy | /24 (254) | /22 (1022) | /16 (65 534) |
|---|---|---|---|
| ARP-only (on-LAN) | ~254 | ~1 022 | n/a (not one L2 domain) |
| ICMP-only | ~254 | ~1 022 | ~65 k |
| TCP multi-port (k=9, no early-exit) | ~2 286 | ~9 198 | ~590 k |
| Hybrid tiered **with early-exit** | ~300–600 | ~1.2–2.5 k | ~80–150 k |

Early-exit collapses the multi-port cost toward one-probe-per-live-host plus a
bounded probe set for the silent remainder. Governors: **rate-limit** (token
bucket, the existing `RateLimiter`), **concurrency cap** (`sem`), **jitter** to
avoid synchronized bursts / IDS signatures, **adaptive timeout** (start ~1 s LAN
/ higher WAN), **≤2 retries** with **exponential backoff** for the unresolved
tail only. Never retry the whole range — retry only ambiguous silences.

---

## 15. Multi-vantage discovery — first-class

**Host existence** and **reachability from vantage V** are different facts. A VIP
reachable from Corp LAN, filtered from Guest VLAN, and unreachable from the
Internet is *one host with three vantage-scoped truths*. Store the cross product:

```
observation = (vantage_id, target_ip, timestamp) → {state, confidence, evidence[]}
```

Aggregate to an asset-level view: `exists = OR over vantages` (any vantage seeing
it proves existence); `reachability = per-vantage map` (never collapse — the
differences are the security signal, e.g. "this admin port is reachable from
Guest"). The shipped code already stamps `data.vantage`; the store must key on
`(vantage, target, time)`.

---

## 16. Compare with Nmap — as benchmark, not crutch

| Nmap flag | Mechanism | Vedha stance |
|---|---|---|
| `-Pn` | skip discovery, assume up | A *mode* (treat-as-up), not discovery. Support as an option. |
| `-sn` | ping scan, no ports | Our whole discovery engine. |
| `-PR` | ARP ping (on-LAN) | **Implement natively** (raw ARP for Tier A; neighbor-freshness for Tier D). Highest LAN value. |
| `-PE` | ICMP echo | **Implement natively** (raw + Tier-C unpriv echo). |
| `-PP` | ICMP timestamp | **Implement natively** (cheap ACL-bypass add-on). |
| `-PM` | ICMP address-mask | Low priority; opportunistic only. |
| `-PS` | TCP SYN ping | **Implement natively** (raw SYN; connect fallback exists). |
| `-PA` | TCP ACK ping | **Implement natively** (slips stateless filters). |
| `-PU` | UDP ping | **Implement natively** (protocol-aware + ICMP-unreach). |
| `-PO` | IP-protocol ping | **Useful fallback to nmap**; low incremental value to build. |
| `-O`, `-sV`, NSE | OS/version/scripts | **Fallback to nmap** as an enrichment oracle; not core discovery. |

Split:
- **Must implement natively:** ARP/NDP freshness, ICMP echo/timestamp, TCP
  SYN/ACK/connect, protocol-aware UDP + ICMP-unreach detection, multi-vantage
  state. (These are the discovery core and the FN-reducers.)
- **Useful nmap fallback:** deep `-sV`/`-O`, NSE, IP-protocol ping — enrichment,
  behind `if shutil.which("nmap")`, as an accuracy *oracle* for our own numbers.
- **Not worth building:** FIN/NULL/Xmas for discovery (§4); exotic ICMP types.

---

## 17. Current Vedha implementation — review & the fix

**What it did well:** unprivileged; multi-port so a RST-only host counts; ARP
fusion to catch silent phones; MAC→vendor + randomized-MAC mobile detection;
early-exit on first proof-of-life; clean scope/rate governance.

**Problems in the old design:**
- **`ARP_CACHE_ENTRY == ALIVE` (the headline bug).** A resolved MAC — however
  old — was fused as equal to a live TCP reply. Stale entries (host powered off,
  IP reassigned, roamed) → **false positives**. *Not valid.*
- **No freshness.** The bulk cache was read once and memoized; freshness of any
  given entry was unknown and ignored.
- **Binary `alive`** discarded all confidence nuance.
- **Silence handling** was acceptable (`filtered`) but not distinguished from
  `inconclusive` vs `unreachable`.
- Routed-network & privilege limits acknowledged but not surfaced in state.

**The fix shipped in `host_discovery.py`:**
1. `alive` boolean **kept** (FN-averse: any positive signal, incl. stale, stays a
   *candidate*), plus new `state` + `confidence` + structured `evidence[]`.
2. **Per-target, post-probe neighbor read** (`read_neighbor`) instead of a
   memoized bulk snapshot — freshness reflects what our own probe just elicited.
3. **NUD grading** (`parse_neighbor_line`): `REACHABLE`→0.95, `DELAY/PROBE`→0.75,
   `STALE`→0.50, macOS unknown-freshness→0.55, `FAILED/INCOMPLETE`→negative.
4. **`fuse_liveness`**: strongest signal sets the headline; corroboration nudges
   up (≤0.99); `STALE`/cache-only can only reach `recently_observed`, never
   `confirmed_alive`.
5. `status` mapping (`open`/`filtered`) and `responding_ports`, `method`,
   `device_hint()` **preserved** — zero downstream wiring change.

**Answer to "is `ARP_CACHE_ENTRY = ALIVE` valid?":** No. It is valid only as
`recently_observed` at ~0.5 confidence pending revalidation. A *fresh, solicited*
ARP reply (`REACHABLE`) is `confirmed_alive`; a cache entry is not. That is now
exactly how the code behaves.

---

## 18. Proposed production architecture

Matches the approved build spec's `probe/scanner/discovery/` package:

```
host_discovery/
  orchestrator.py     # tier selection, per-target flow, early-exit, fusion call
  capabilities.py     # root/CAP_NET_RAW, unpriv-ICMP, on-LAN vs routed detection
  neighbor_cache.py   # unprivileged ARP/NDP read + NUD freshness (shipped logic)
  arp_probe.py        # raw ARP (Tier A)
  ipv6_ndp.py         # raw NDP / solicited-node multicast (Tier A, v6)
  icmp_probe.py       # echo/timestamp (raw + Tier-C DGRAM)
  tcp_syn_probe.py    # raw SYN/ACK (Tier A/B)
  tcp_ack_probe.py    # raw ACK (stateless-filter bypass)
  tcp_connect_probe.py# unprivileged connect (Tier D, shipped)
  udp_probe.py        # protocol-aware payloads + ICMP-unreach capture
  passive_observer.py # listen-only sources (feeds Tier 0)
  evidence.py         # Signal/ProbeOutcome dataclasses, timestamps
  confidence.py       # weights, decay, fuse() (shipped fuse_liveness logic)
  dedup.py            # (vantage,ip,time) keying, VIP/NAT + duplicate-IP handling
```

Uniform probe interface: `async def probe(ctx, target) -> ProbeOutcome`; the
orchestrator fuses outcomes via `confidence.fuse`. `host_discovery.py` becomes a
thin re-export shim (per the build spec) once the package lands.

---

## 19. Pseudocode

```python
def discover_host(target, ctx):
    caps = capabilities.detect(ctx, target)          # tier + on-LAN?
    outcomes = []

    if caps.on_lan:
        outcomes += passive.read(target)             # Tier 0, 0 pkts
    # fire the tier-appropriate active probes CONCURRENTLY
    probes = select_probes(caps, ctx.profile)        # honors ot/iot gates
    for out in run_concurrent(probes, target,
                              rate=ctx.limiter, sem=ctx.sem,
                              timeout=adaptive(caps)):
        outcomes.append(out)
        if out.is_endpoint_positive():               # SYN/ACK, RST, port-unreach
            cancel_remaining()                       # early-exit (liveness)
            break

    if caps.on_lan:                                  # post-probe freshness read
        nb = neighbor_cache.read(target)             # NUD-graded, unprivileged
        outcomes.append(nb.as_outcome())
        if nb.fresh == REACHABLE:
            cancel_remaining()

    verdict = confidence.fuse(outcomes)              # state, confidence, evidence[]
    for attempt in range(ctx.max_retries):           # only the ambiguous tail
        if verdict.state != INCONCLUSIVE: break
        sleep(backoff(attempt) + jitter())
        outcomes += reprobe(target, caps)
        verdict = confidence.fuse(outcomes)

    return verdict.with_vantage(ctx.vantage, now())

def discover_subnet(cidr, ctx):
    targets = expand(cidr)
    if same_l2_domain(cidr, ctx):                    # on-LAN /24-ish
        prime_arp(targets, ctx)                      # Tier 1 sweep to fill cache
    results = bounded_gather(                         # sem + rate governed
        (discover_host(t, ctx) for t in targets if ctx.scope.in_scope(t)),
        concurrency=ctx.concurrency)
    return dedup.by_vantage_ip_time(results)         # VIP/NAT + duplicate-IP aware
```

---

## 20. Validation laboratory

For each fixture: **setup → expected packets → expected Vedha state → nmap
reference → PASS/FAIL.**

| Fixture | Setup | Expected packet behavior | Expected Vedha | Nmap reference | PASS if |
|---|---|---|---|---|---|
| Windows 11 (default FW) | LAN, no ports forwarded | echo dropped; 445/3389 may RST or open; ARP answers | `confirmed_alive` (arp/tcp) | `nmap -sn -PR 10.0.0.5` | up via ARP or TCP, not via echo |
| Linux server | 22/80 open | SYN/ACK; echo maybe on | `confirmed_alive`, reason syn_ack | `nmap -sn -PE -PS22,80` | up via TCP |
| macOS laptop | firewall on | ARP answers; TCP mostly filtered | `confirmed_alive` via fresh ARP | `nmap -sn -PR` | up via ARP freshness |
| iPhone | Wi-Fi, lockdownd | 62078 sometimes open; randomized MAC; ARP answers | `confirmed/probably`, device_hint mobile | `nmap -sn -PR` | detected + mobile hint |
| Android | Wi-Fi | mDNS chatter; ARP answers; TCP filtered | `confirmed_alive` via ARP + passive | `nmap -sn -PR` | up via ARP/passive |
| Router/AP | gateway | ARP + often 80/443/53 | `confirmed_alive` | `nmap -sn` | up |
| IoT (Espressif) | LAN | tiny stack; ARP; maybe 80 | `confirmed_alive` via ARP | `nmap -sn -PR` | up, gentle profile respected |
| ICMP-blocked host | drop type 8 | echo silent; TCP/ARP work | up via non-ICMP path | `nmap -sn -PE` (misses) vs `-PS` | up **without** echo |
| TCP-blocked host | drop all TCP | ARP works; TCP silent | `confirmed_alive` via ARP | `nmap -sn -PR` | up via ARP only |
| Drops all unsolicited | host FW DROP | on-LAN ARP only proof | on-LAN `confirmed`; routed `inconclusive` | `nmap -sn -PR` | correct per vantage |
| Powered-off IP | nothing there | ARP `FAILED`; all silent | `unreachable_from_vantage`/`inconclusive` | `nmap -sn` (down) | **not** confirmed_alive |
| Stale ARP entry | note MAC, power off, don't flush | pre-probe `STALE`; post-probe `FAILED` | `recently_observed`→ decays; not confirmed | manual `ip neigh` | never `confirmed_alive` |
| Proxy ARP | router proxies a range | one MAC for many IPs | ARP-only downgraded, flag shared-MAC | `nmap -sn -PR` (false-ups) | Vedha avoids the false positive |
| Filtered VLAN host | different VLAN | no frames seen | `unreachable_from_vantage` | `nmap -sn` (down) | classified reachability, not "down" |
| IPv6 host | on-LAN v6 | NS→NA on solicited-node mcast | `confirmed_alive` via NDP | `nmap -6 -sn` | up via NDP |

The **stale-ARP** and **powered-off** fixtures are the regression guards for the
bug this work fixed.

---

## 21. Accuracy metrics

- **TP:** engine says alive **and** host is alive.
- **FP:** engine says alive **and** host is not (stale ARP, proxy ARP, tarpit).
- **TN:** engine says not-alive **and** host is down.
- **FN:** engine says not-alive **and** host is alive. *The dangerous one.*

Derived: **Recall = TP/(TP+FN)**, **Precision = TP/(TP+FP)**, **FPR =
FP/(FP+TN)**, **FNR = FN/(FN+TP)**, **coverage = fraction of truly-live hosts
discovered by ≥1 method**.

**Confirmed:** your intuition is correct. For a vulnerability scanner **recall
(minimize FN) is the primary metric** — a missed asset is never scanned, never
assessed, and becomes an invisible hole; the whole downstream pipeline inherits
the gap. Precision still matters (FPs waste scan budget and erode trust), but the
right posture is **maximize recall, then manage precision via
confidence/freshness** — which is exactly why the shipped model keeps
stale-evidence hosts as low-confidence *candidates* (`alive=true`,
`recently_observed`) rather than dropping them: we'd rather revalidate a
maybe-stale host than silently exclude a real one.

---

## 22. Prioritized implementation plan

Each item: security value / discovery gain / FN reduction / complexity /
privilege / portability / noise / priority.

**P0 — now (mostly shipped):**
- **Neighbor-freshness state model** (NUD grading, per-target post-probe read,
  confidence/state). *High value; large FN/FP correction; low complexity;
  unprivileged; Linux-rich/macOS-degraded; near-zero extra noise.* **DONE.**
- **Preserve `alive`/`status` contract** while adding `state`/`confidence`.
  *Prevents pipeline regressions; trivial; done.* **DONE.**
- **Unit tests for `fuse_liveness` + `parse_neighbor_line`** golden vectors.
  *Locks the fix; low complexity; portable.* **Next.**

**P1 — important next:**
- **Unprivileged ICMP echo** (Tier C, `ping_group_range`). *Catches ICMP-only
  hosts; medium value; low-medium complexity; unpriv on Linux; medium FN
  reduction; low noise.*
- **Protocol-aware UDP probes** (DNS/SNMP/NTP/mDNS) + reply parsing. *Finds
  UDP-only services; medium complexity; unpriv for replies; medium noise.*
- **IPv6 neighbor-cache read** (`ip -6 neigh`) mirroring the ARP path. *v6 on-LAN
  coverage; low complexity; unpriv.*
- **Multi-vantage `(vantage,ip,time)` store keying.** *Turns reachability into a
  first-class security signal; medium complexity; store-layer.*

**P2 — later (needs `CAP_NET_RAW`):**
- **Raw ARP/NDP active probes** (Tier A). *Strongest LAN proof independent of
  connect(); medium complexity; privileged; Linux.*
- **Raw TCP SYN/ACK + TTL/window OS-hint** (Tier A/B). *Speed + fingerprint;
  privileged.*
- **ICMP port-unreachable capture for UDP.** *Endpoint UDP liveness; privileged.*
- **Proxy-ARP / duplicate-IP / tarpit detection heuristics.** *Precision;
  medium complexity.*
- **Freshness decay + revalidation scheduler.** *Long-run FP control.*

**P3 — optional:**
- ICMP timestamp/address-mask probes (ACL-bypass edge cases).
- IP-protocol ping / exotic techniques → prefer nmap fallback oracle.
- Cloud-API / flow-log discovery adapters (separate integration surface).

**North star:** *Vedha produces an evidence-backed, confidence-scored,
multi-vantage statement about whether an asset exists and whether it is reachable
from a given network position* — not merely a ping sweep. The shipped change is
the first concrete step: liveness is now graded and freshness-aware, and stale
cache no longer masquerades as proof.
