# Vedha Network VA — Volume II: Core-Level Deep Dives

**Status:** Research / design-only. *No code is changed by this document.* This is
the engineering-depth companion to
[`2026-10-03-network-va-usecases-technical-research.md`](./2026-10-03-network-va-usecases-technical-research.md)
(Volume I). Where Volume I mapped every use-case to a method and a gap, Volume II
goes to **the wire**: the exact algorithms, packet structures, hash constructions,
accuracy figures, and concrete (design-only) implementation sketches tied to
Vedha's real modules.

**Date:** 2026-10-03 · **Branch:** `claude/serene-bardeen-1uqxzq`

> **Sourcing note.** The session's egress proxy allows package registries and
> GitHub raw content but blocks direct fetches of arxiv.org / usenix.org /
> nmap.org (org network policy — not something a connector changes). So the
> primary-source extraction below combines: (a) GitHub-hosted reference specs
> fetched directly (FoxIO JA4), (b) server-side web search that returns the
> papers' own figures, and (c) Vedha's own code, which already encodes several of
> these algorithms exactly (`ja4s.py`, `ja4x.py`, `syn_scanner.py`). Every
> numeric claim is attributed. If you want me to pull a specific PDF verbatim,
> allow its domain in the environment's network policy and I'll fetch it.

**Contents**
1. Stateless scanning core — SYN cookies, address permutation, rate-as-ceiling
2. LZR — expected-service confirmation in ≤5 handshakes (the #1 ROI item)
3. GPS — all-port service prediction
4. TCP state machine & firewall-analysis scans (ACK/FIN/NULL/Xmas/Window/Maimon)
5. Service/version fingerprinting — the nmap probe-DB model
6. TLS fingerprinting family — JARM, JA4/JA4S/JA4X byte-level
7. OS/stack fingerprinting — the feature vector and its ceilings
8. CVE correlation & prioritization — CPE match, OSV ranges, EPSS v4, SSVC
9. IPv6 discovery at scale — ND + hitlist + target-generation algorithms
10. OT/ICS passive depth — SPAN/TAP, DPI, function-code classification
11. Accuracy validation — the number you can defend to a client
12. Consolidated design roadmap

---

## 1. Stateless scanning core (ZMap / masscan)

### 1.1 Why stateless

A stateful scanner (nmap, connect scan) keeps a table entry per outstanding probe;
at a /16 that table and its timers dominate cost. The stateless model keeps **zero
per-probe state** and recovers all needed context *from the reply itself*. This is
what lets masscan/ZMap sweep enormous ranges in minutes
([ZMap, USENIX Sec '13](https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_durumeric.pdf)).

### 1.2 The SYN-cookie trick (the heart of it)

A stateless SYN scan must distinguish a *legitimate* SYN/ACK (reply to a SYN we
sent) from a stray/forged packet, without a table. It encodes the probe identity in
the TCP **Initial Sequence Number (ISN)**:

```
ISN  =  MAC_k( dst_ip, dst_port, src_port )        # keyed hash, k = per-scan secret
```

The target's SYN/ACK acknowledges our ISN+1, so on receipt we recompute the cookie
from the reply's own 4-tuple and check:

```
reply.ack_number - 1  ==  MAC_k( reply.src_ip, reply.src_port, reply.dst_port )
```

A match proves "this is a reply to a SYN *we* sent to *that* (ip,port)"—validated
with no stored state and robust against injected/forged replies. Vedha implements
exactly this: `scanner/syn_scanner.py` → `syn_cookie()` / `verify_reply_cookie()`,
with `reply.ack - 1 == cookie(reply addressing)`.

### 1.3 Address-space permutation (don't hammer, don't miss)

ZMap iterates the (IP,port) space as a **cyclic multiplicative group mod p** (p a
prime just above 2³²): pick a primitive root g, and the sequence `a·gⁱ mod p`
visits every address exactly once in a statistically random order. Benefits:
no target gets a burst, the scan is resumable from an index, and work shards
cleanly across probes (probe *n* of *N* takes indices ≡ n mod N). Vedha's scalable
design already adopts the "randomize the (IP,port) space and shard
deterministically" principle (`docs/research/2026-09-23-scalable-large-subnet-scanning.md` §2.5).

### 1.4 Accuracy reality: one probe ≈ 98 %

- A single SYN per host detects **~98 %** of instantaneously-listening hosts; the
  missing ~2 % matches the Internet's background single-packet loss rate (ZMap).
- ZMap defaults to **one** probe and *sacrifices* that ~2 % for speed; nmap
  retransmits adaptively and recovers it at a large time cost.
- **The correct product behaviour** (and Vedha's) is in between: definitive replies
  (SYN/ACK, RST) are never retried; only *silence* gets a **bounded retransmit**,
  because a single dropped SYN is a false negative the scanner manufactured.
  (`port_scanner.py` retransmit-on-silence; `adaptive_timeout.py` SRTT+4·RTTVAR.)
- **A requested rate is a safety ceiling, not a coverage guarantee.** At N pps,
  packet loss and target rate-limits mean *useful* coverage < N. Coverage must be
  measured and reported, not assumed — `port_scanner.ScanMetrics`
  (`requested / classified / missing / duplicate` → `complete()`/`degraded()`) is
  that honesty instrument.

### 1.5 Design sketch (already largely present)

Vedha already has the three pieces (SYN cookies in `syn_scanner`, masscan wrap +
async fallback in `mass_scan`, metrics in `port_scanner`). The one design
addition worth proposing is a **resumable, sharded campaign scheduler** (phase/
shard/attempt model from the scalable-subnet research) so a /16 can run across
multiple probes with deterministic, non-overlapping coverage and at-least-once
idempotent result ingestion. Design-only; the engine primitives exist.

---

## 2. LZR — expected-service confirmation in ≤5 handshakes *(the #1 accuracy ROI)*

**Primary:** Izhikevich et al., *LZR: Identifying Unexpected Internet Services*,
USENIX Security '21 ([arXiv:2301.04841](https://arxiv.org/abs/2301.04841); reference
impl: [github.com/stanford-esrg/lzr](https://github.com/stanford-esrg/lzr)).

### 2.1 The problem it solves

Routing a deep scanner by **port number** is wrong twice: (a) a service often runs
on an *unexpected* port (HTTPS on 8443, Redis on 6380, SSH on 2222) and gets
missed, and (b) a port can be open with *nothing meaningful* behind it, wasting a
full deep handshake. LZR confirms *what actually speaks* before committing.

### 2.2 The mechanism (wire-level)

1. Complete (or half-complete) the TCP handshake to an open port.
2. **Send application-layer data riding on the ACK** — the first-packet handshake
   bytes of the *expected* protocol for that port (e.g. an HTTP `GET`, a TLS
   ClientHello).
3. Observe the response class:
   - **Any L7 data back** → fingerprint it, identify the protocol, **close**. Done
     in effectively one extra round-trip.
   - **ACKs the data but sends nothing** / **zero window** → keep the connection,
     escalate.
   - **Neither ACKs the data nor closes** → **retransmit the data with the PUSH
     flag** (forces delivery up the stack).
   - **RST / closes** → not a real L7 service on that port.
4. The key empirical lever: **~40 % of hosts that send a SYN/ACK never acknowledge
   application data** — none of them can complete an L7 handshake, so they are
   *safely ignored*. That single filter is where most of the speed-up comes from.

### 2.3 The numbers

- **99 % of identifiable unexpected services identified in ≤5 handshakes.**
- Dramatic reduction in application-layer scan time/bandwidth vs. trying a full
  protocol handshake on every open port.

### 2.4 Design sketch for Vedha (`workflow/router.py`)

Today `router.py` routes an open port to a deep scanner by port→branch table
(`_BRANCH_PORT_TABLE`) and even *skips* TLS on ports "observed not to speak TLS."
Proposal (collection-only, no new offensive capability):

```
for each open port:
    send expected-protocol first-bytes on the ACK   # LZR probe
    classify response → {protocol, speaks_tls, none}
    route to the deep scanner for the CONFIRMED protocol, not the port number
    if no L7 response in ≤5 handshakes: mark 'open, no service' and skip deep pass
```

Impact: recovers services on non-standard ports (recall ↑) *and* stops wasting deep
handshakes on empty opens (speed ↑). It also fixes the status-#3 blind spot
honestly — a port that *does* speak TLS inside another protocol would be detected
by the confirmation step rather than hard-skipped. This is the single
highest-accuracy, lowest-risk upgrade in the whole surface.

---

## 3. GPS — predicting IPv4 services across all ports

**Primary:** *GPS: Predicting IPv4 Services Across All Ports*
([arXiv:2303.00895](https://arxiv.org/pdf/2303.00895)).

- **Problem:** exhaustive all-port service scanning (65 535 ports × app-layer
  handshake) is infeasible at scale.
- **Core idea:** services are *correlated* across ports and hosts — knowing what
  runs on some (IP,port) pairs predicts likely (IP,port,service) elsewhere. GPS
  bootstraps with a four-phase process, learns these correlations, and scans only
  the high-probability pairs.
- **Numbers:** finds **92.5 % of services across all ports** with **131× less
  bandwidth** and **204× more precision** than exhaustive scanning; computes
  predictions in **~13 minutes**.
- **Relation to LZR:** LZR makes *each* open-port confirmation cheap (≤5
  handshakes); GPS decides *which* (IP,port) pairs are worth probing at all. They
  compose: GPS for all-port *breadth* prediction, LZR for per-port *confirmation*.
- **Where Vedha would use it:** only at large multi-/16 external scale. For an
  enterprise /24–/22 the `enterprise` (~2,500-port) and `full` profiles already
  finish in the job ceiling, so GPS is a *future* lever, not a near-term gap.

---

## 4. TCP state machine & firewall-analysis scans

Vedha ships Connect + stateless SYN. The six **firewall-analysis** techniques are
not implemented. Here is the exact behaviour that governs them and why their copy
must be carefully caveated.

### 4.1 The RFC-793 response matrix

| Scan | Flags sent | Open port | Closed port | Filtered |
|---|---|---|---|---|
| Connect | full handshake | SYN/ACK → ACK (est.) | RST | timeout |
| SYN | SYN | SYN/ACK (then we RST) | RST | timeout / ICMP unreach |
| **ACK** | ACK | **RST** (`unfiltered`) | **RST** (`unfiltered`) | no reply / ICMP type 3 code 13 (`filtered`) |
| **Window** | ACK | RST, **window > 0** | RST, **window = 0** | no reply |
| **FIN** | FIN | *no reply* | RST | no reply (→ `open\|filtered`) |
| **NULL** | *(none)* | *no reply* | RST | no reply |
| **Xmas** | FIN+PSH+URG | *no reply* | RST | no reply |
| **Maimon** | FIN+ACK | *(RFC: RST always)*; **BSD drops if open** | RST | no reply |

Two deductions a client report must state plainly:

- **ACK scan never finds open ports.** Its job is to map the **firewall**: a RST
  back = the firewall let the ACK through (port `unfiltered`); silence or
  ICMP-admin-prohibited = `filtered`. It tells you *whether a stateful firewall
  exists and which ports it blocks* — intelligence Connect/SYN cannot produce. This
  is the one of the six to foreground.
- **FIN/NULL/Xmas/Maimon are stack-dependent.** They exploit the RFC-793 rule that
  a *closed* port RSTs and an *open* port stays silent — but **Windows, Cisco IOS,
  and many modern stacks send RST for every probe regardless of state**, so on a
  Windows estate they report *every* port `closed`. They are evasion/diagnostic
  tools for specific (often BSD/Unix, stateless-firewall) environments, **not**
  general open-port finders. Maimon specifically relies on the BSD quirk of
  dropping a FIN/ACK to an open port.

### 4.2 Design sketch

All six are raw-packet sends with no handshake completion → pure collection, same
privilege gate as `syn_scanner` (`CAP_NET_RAW`, Linux). Implementation reuses
`syn_scanner`'s `build_ip_header` / `build_tcp_*` / `parse_packet` — **only the TCP
flag field and the reply-interpretation table change.** Expose under
**Advanced → Firewall / Filtering Analysis**, disabled by default, each card
carrying the Windows/modern-stack caveat so we never present a FIN-scan "all
closed" as authoritative. The Window-scan variant reads the RST window field per
§4.1 to leak open/closed on stacks that still exhibit it (a diminishing set — note
it as best-effort).

---

## 5. Service/version fingerprinting — the nmap probe-DB model

**Reference:** nmap's `nmap-service-probes` + version-detection algorithm (the
field standard; Vedha's `OSS_CORE_STUDY.md` already resolves the license question —
learn the model, re-derive the data clean).

### 5.1 The probe-DB grammar

```
Probe <proto> <name> q|<escaped-probe-string>|      # the bytes to send ("" = NULL probe)
rarity <1-9>                                         # how uncommon → gated by intensity
ports <list>                                         # ports this probe is normally tried on
sslports <list>                                      # try this probe inside TLS on these ports
match <svc> m|<regex>|<flags> [p/vendorproductname/] [v/version/] [i/info/] [cpe:/.../]
softmatch <svc> m|<regex>|                           # tentative: narrows to this service's probes
fallback <probe>                                     # if no match, try these probes' match lines
```

### 5.2 The matching flow

1. Fire the **NULL probe** first (read what a speak-first service volunteers).
2. For each candidate probe in rarity order (bounded by `--version-intensity`
   0–9, default 7; a probe fires if its rarity ≤ intensity **or** the port is in
   the probe's `ports`), send the probe string, read the response.
3. Test the response against that probe's `match` lines → on a hit, extract
   `service / product / version / cpe` from the regex capture groups and **stop**.
4. A **softmatch** gives a tentative protocol ID with *no* version; subsequent
   probes are then restricted to that service's probes (narrowing), until a hard
   `match` yields the version. (`--version-all` ignores the stop and tries every
   probe.)
5. `fallback` lets a probe borrow another's match lines (e.g. TLS-wrapped probes
   fall back to the plaintext HTTP matches inside the tunnel).

### 5.3 Vedha today & the gap

`service_banner.py` implements the shape (NULL-probe read → soft-match regex table
→ one TLS-fallback handshake → repeat inside tunnel → structured HTTP head). The
**gap is corpus depth**: product/version capture is null on many services
(`usecases-networkva.md` SB-03/04 `✗`), which directly caps Level-6 CVE accuracy
(no version → no CVE match). **Design proposal:** grow a license-clean probe/match
corpus (rarity + ports + cpe), keyed to the services Vedha already routes, and
add **banner sanitisation** (strip non-printable bytes before storing). This is
data work behind the existing engine, not a new scanner.

---

## 6. TLS fingerprinting family — JARM, JA4 / JA4S / JA4X (byte-level)

### 6.1 JARM (active, 2020) — what Vedha computes today

`tls_fingerprint.py` sends **10** deliberately-varied ClientHellos (varying TLS
version, cipher list + ordering, GREASE, ALPN, extension order) and hashes the
server's *selection behaviour*: a 62-char digest = 30 chars encoding the
(cipher,version) chosen per probe (`000` = no reply) + 32-char truncated SHA-256 of
the cumulative server extensions. **Why it's fading:** under TLS 1.3/QUIC the
server's selection surface shrank, so **JARM fingerprints now collide heavily**,
reducing discriminative power (FoxIO's own motivation for JA4S/JA4Scan).

### 6.2 JA4 (client ClientHello) — exact construction

From the [FoxIO reference](https://github.com/FoxIO-LLC/ja4):
```
JA4 = (proto)(tls_ver)(sni)(cipher_count)(ext_count)(alpn_first)(alpn_last)
      _ (sha256(sorted ciphers)[:12])
      _ (sha256(sorted exts)+"_"+sig_algs [:12])
```
- proto: `t` TCP / `q` QUIC / `d` DTLS
- tls_ver: `13/12/11/10/s3/s2/d1/d2/d3/00` (highest offered)
- sni: `d` if SNI present (domain) / `i` if none (IP)
- cipher_count / ext_count: two-digit decimals, **GREASE excluded**
- alpn: first+last alnum char of first ALPN (hex if non-alnum), else `00`
- cipher hash: 4-hex-lowercase ciphers, **sorted**, comma-joined, SHA-256[:12]
  (`000000000000` if empty)
- ext hash: extensions **excluding 0x0000 SNI and 0x0010 ALPN**, sorted,
  comma-joined, then `_` + signature-algorithms **in order (not sorted)**,
  SHA-256[:12]

The decisive improvement over JA3: **extensions are sorted by type**, so browser
extension-shuffling no longer randomises the fingerprint — JA4 is stable where JA3
churned.

### 6.3 JA4S (server ServerHello) & JA4X (certificate) — already in Vedha

Vedha ships both (`ja4s.py`, `ja4x.py`), byte-compatible with the FoxIO reference:

```
JA4S = (proto)(tls_ver)(ext_count)(alpn) _ (chosen_cipher_4hex) _ sha256(ext_types_in_order)[:12]
       e.g.  t130200_1301_234ea6891581
JA4X = sha256(issuer_RDN_OIDs)[:12] _ sha256(subject_RDN_OIDs)[:12] _ sha256(ext_OIDs)[:12]
       # each OID hex-encoded by DER content octets: 2.5.4.6 -> 550406 ; empty list -> 000000000000
```
JA4X is computed from the certificate `tls_scanner` **already collects** — zero
extra probing — and clusters certs minted by the same tooling/CA (incl. malware C2
cert generators) even when field values differ.

### 6.4 The cited research — what each adds

- **[arXiv:2602.09606](https://arxiv.org/abs/2602.09606)** (2026) — bad-bot
  detection by **JA4 + gradient-boosting**: the JA4 fingerprint is a strong
  *feature* for a classifier, not just a lookup key.
- **[arXiv:2410.03817](https://arxiv.org/abs/2410.03817)** (2024) — **feature
  expansion + similarity mapping** (MinHash-style) to surface *unknown* malicious
  infra from fingerprint *neighbourhoods*, not exact matches — important because
  exact-match fingerprint DBs miss novel infrastructure.
- **[arXiv:2405.07848](https://arxiv.org/abs/2405.07848)** — **positional-unigram
  byte models**: model the ClientHello/handshake as a byte distribution per
  position → generalises across minor variations better than a brittle exact hash.
- **[arXiv:2009.01939](https://arxiv.org/abs/2009.01939)** — **destination-context**
  TLS fingerprinting: the *same* client fingerprint means different things to
  different destinations; adding (SNI/destination) context sharply raises accuracy.

### 6.5 Design takeaway

JA4S/JA4X are shipped — **promote them to the primary TLS-stack identity** (Level 6)
and the MAC-less host-identity key for delta (Level 7), demoting JARM to a legacy
corroborator per the collision findings. For *classification* (benign vs
suspicious infra) the research direction is **fingerprint-as-feature +
similarity**, not exact-match blocklists — a manager-side analytics opportunity,
not a probe change.

---

## 7. OS / stack fingerprinting — the feature vector and its ceilings

### 7.1 The signal set

Active/passive OS inference reads TCP/IP stack idiosyncrasies the OS vendor fixed:

| Feature | Why it discriminates |
|---|---|
| **Initial TTL** (round observed up to 64/128/255) | Linux/Unix/macOS 64, Windows 128, many net devices 255 |
| **TCP window size** + **window scale** | stack/tuning specific |
| **MSS** | path/stack specific |
| **TCP options order** (MSS, SACK, TS, NOP, WScale) | *ordering* is a strong per-stack signature |
| **DF bit**, **IP ID** behaviour, **TCP timestamp** presence, **SACK permitted** | implementation tells |

p0f encodes these as a signature string
(`ver:ittl:olen:mss:wsize,scale:olayout:quirks:pclass`) and matches against a DB.

### 7.2 Accuracy ceilings (be honest to the client)

- **p0f v3:** ~**92.8 %** OS-name accuracy but only ~**64 %** precision / ~**49 %**
  recall — TTL/window alone are limited; many stacks share values.
- **ML on headers:** nPrintML and tabular-transformer approaches
  ([arXiv:2502.09084](https://arxiv.org/pdf/2502.09084)) beat p0f's recall with
  *smaller* packet samples and expose fine-grained OS differences.
- **Conclusion:** OS family is a **confidence-scored hint, not a verdict** — exactly
  how `os_fingerprint.py` scores it (TTL rounding + window/MSS heuristic + a 0–1
  confidence), and why `device_classifier.py` caps role confidence by the number of
  *independent* agreeing signals.

### 7.3 JA4T / TCP-SYN stack fingerprint (adjacent capability)

The JA4+ suite includes a **TCP** fingerprint (JA4T) built from SYN window size +
TCP options + MSS + window scale — the same features above, hashed into a stable
string. Since `syn_scanner` *already harvests* the TCP stack fields on a SYN/ACK
(`_harvest_tcp_stack`), a JA4T-style digest is **almost free** and would strengthen
both OS inference and host identity. Design-only proposal; feeds Levels 6–7.

---

## 8. CVE correlation & prioritization (manager side)

### 8.1 Identity: product → CPE 2.3

A banner-derived `{product, version}` becomes a CPE 2.3 string
(`cpe:2.3:a:openbsd:openssh:9.5:...`). Vedha: `scanner/cpe.py` (+`cpe_unmapped`
when a product is named but unmapped — measurable blind-spot). Accuracy here gates
everything downstream; version quality (Level 5/§5.3) is the limiter.

### 8.2 The version-range match and its #1 false-positive source

OSV/NVD express "affected" as ranges: `{introduced, fixed}`. The matcher treats
`introduced` with no `fixed` as "vulnerable from X onward" (OSV convention). **The
FP (status #4, confirmed):** Debian/Ubuntu OSV records for *unfixed* CVEs are
`introduced: 0, fixed: (none)` → the range is `[0, ∞)` and matches **every**
upstream banner version (e.g. vsftpd 3.0.3, OpenSSH 9.5 flagged wrongly). Two
compounding realities:
- **Distro backports:** distros patch without bumping the upstream version, so a
  version match ≠ vulnerable (a backport marker in the banner —
  `+deb`, `.elN`, `ubuntu`, `raspbian` — already downgrades Vedha findings to
  `low`).
- **Unparseable versions** are skipped, not matched (so "defaults to match-all" is
  *not* what the code does — the `[0,∞)` records are the real cause).

**Design fix:** mark open-ended / distro-unfixed matches as **suspected** (not
confirmed), and bound them with upstream NVD `versionEndExcluding` data before they
reach the queue. Confirmed status should require the range match **and** an
authoritative/credentialed source — banner-inferred stays "suspected,
backport-possible," which is already Vedha's stated contract (confidence `medium`
max for banner-derived).

### 8.3 Prioritization: KEV → EPSS → CVSS, with the two confirmed bugs

- **CISA KEV** = *known-exploited* → always first. **Bug (status #5):** KEV links
  are not OS-gated, so `RDP-NO-NLA` links BlueKeep on Windows 11. **Fix:** an
  applicability field (OS family + version range) per KEV link.
- **EPSS v4** (FIRST, released **2025-03-17**): an **XGBoost** gradient-boosted
  model over **~2,850 features in 5 groups** (exploit code/tooling, CVE metadata,
  temporal, threat-intel feeds, references) emitting a **0–1 probability of
  exploitation in 30 days**. v4 added malware-activity + endpoint-detection +
  Shodan-scan + HackerOne signals, observes ~12 000 exploited CVEs/month (vs ~2 000
  in v3), groups weaknesses under the top-22 CWE, and excludes REJECTED CVEs.
  Efficiency: remediating **EPSS ≥ 0.1** addresses ~2.7 % of CVEs but catches
  ~63 % of exploited ones — ~20× more efficient than "CVSS ≥ 7." **Bug (status
  #6):** EPSS alone promotes a 30 %-confidence DoS to Critical. **Fix:** cap EPSS
  promotion by *match confidence* and *impact*.
- **CVSS** = severity, last — only ~2.3 % of CVSS-7+ CVEs are ever observed in
  exploitation, so CVSS alone massively over-alerts.
- **SSVC** (stakeholder-specific, CISA decision tree: Exploitation × Automatable ×
  Technical-impact × Mission/Well-being → Track/Track*/Attend/Act) is the
  *decision* layer worth proposing on top of the KEV/EPSS/CVSS signals — it turns
  scores into an action, which is what a client report should carry.

Vedha keeps **confidence and risk orthogonal** (a low-confidence finding can still
be critical-risk: "high impact *if* real — verify patch level"), which is the
correct model; the three fixes above make the *priority* field trustworthy.

---

## 9. IPv6 discovery at scale

### 9.1 Why brute force is impossible, and ND is the answer

A /64 holds 2⁶⁴ addresses — unsweepable. But **RFC 4861** ND means every live host
on a segment subscribes to `ff02::1` (all-nodes multicast): one ICMPv6 echo to
`ff02::1` makes them reply, populating the kernel neighbour cache, which you then
read (Linux `ip -6 neigh`, BSD `ndp -an`). Vedha: `ipv6_discovery.py` does exactly
this, no /64 enumeration (a hard guardrail). Discovered addresses feed the existing
dual-stack connect scanner.

### 9.2 Beyond the local segment: target-generation algorithms (TGAs)

For *routed* IPv6 (an enterprise /48 with many /64s, or external ranges), ND
doesn't reach — you need **seeds** (known active addresses) + a **TGA** that learns
address structure and generates likely-active candidates:

- **Entropy/IP** (Foremski 2016): compute **per-nybble entropy** across seed
  addresses (each of the 32 hex digits is a dimension), group adjacent nybbles of
  similar entropy into **segments**, learn a **Bayesian network** of inter-segment
  dependencies, then sample it to generate targets.
- **6Graph:** split the space by structural region, map each region's addresses to
  an undirected graph, do **density-based graph cutting** to cluster address
  patterns and discard outliers iteratively.
- **6Gen / 6Tree / 6GAN / 6Rover:** densest-address-region expansion, dynamic
  space-tree discovery, GAN + RL multi-pattern generation, and RL pattern-mining
  for *unseeded* space respectively.
- **Seeds** come from the IPv6 **Hitlist Service** (10 yrs of responsive-prefix
  data), NTP/DNS, and — for an enterprise — the client's own DNS/AAAA, DHCPv6
  leases, logs, and the probe's neighbour cache.

### 9.3 Design sketch

Near-term Vedha stays correct with **ND on-segment**. For an enterprise /48 the
design is: **(1)** harvest seeds (neighbour cache + client DNS/AAAA + DHCPv6 +
logs), **(2)** run a lightweight TGA (Entropy/IP is the simplest high-value one —
pure statistics, no GPU), **(3)** connect-scan the generated candidates with the
existing dual-stack engine. Pure collection; the hard guardrail (never a blind /64
sweep) is preserved because we only probe *generated/seeded* addresses.

---

## 10. OT / ICS passive depth

### 10.1 The rule, restated at protocol level

Active probing crashes fragile controllers — a single unsolicited connection or
malformed packet has rebooted PLCs and tripped physical processes. **NIST SP
800-82** and **IEC 62443** both mandate passive-first. Vedha's `ot` profile is
*structurally* passive-only (`gate_0_is_passive_profile` routes exclusively to
`PassiveCollector`; no active gate is reachable) — a guarantee, not a setting.

### 10.2 Passive asset ID: what you can learn without sending a packet

From a **SPAN port / network TAP** feed (a copy of traffic; nothing injected), deep
packet inspection of OT protocols yields vendor/model/role and a behavioural
baseline:

- **Protocols to dissect:** Modbus/TCP, DNP3, IEC 60870-5-104, EtherNet/IP (CIP),
  PROFINET, BACnet/IP, Siemens S7comm, OPC-UA, IEC 61850 (MMS/GOOSE), HART-IP.
- **Device identity:** MAC-OUI → vendor; protocol-specific identity objects (CIP
  Identity Object, S7 module ID, Modbus device-ID FC43) seen *in existing traffic*;
  announcement broadcasts.
- **Function-code baselining** = the security signal: learn which codes each device
  pair uses. **Read** Modbus codes (FC01 coils, FC02 discrete, FC03 holding, FC04
  input) are normal; **write** codes (FC05, FC06, FC15, FC16, FC23) from an
  unexpected source are the anomaly. Same for DNP3 objects, S7 read/write.

### 10.3 Vedha today & design

`passive_collector.py` is **host-stack receive-only**: it binds broadcast
announcement ports (NetBIOS 137, BACnet/IP 47808, EtherNet/IP 2222) and records
self-announcements; it deliberately does **not** join multicast (IP_ADD_MEMBERSHIP
emits IGMP — not passive), so mDNS/SSDP/LLMNR are reported as *unavailable
coverage*. **Design proposal:** add a **receive-only SPAN/TAP packet-capture
backend** with the protocol dissectors above — this recovers mDNS/SSDP/LLMNR and
unlocks real OT device/role identification + function-code baselining, while still
transmitting **zero** packets. This is the single capability that would make the OT
use-case a differentiator rather than a broadcast listener.

---

## 11. Accuracy validation — the number you can defend to a client

The thing that lets Vedha *claim* accuracy honestly is already built:

- **`accuracy.py`** scores precision / recall / F1 for findings and OPEN
  precision/recall + state accuracy for ports, against a labelled corpus.
- **`accuracy_gate.py`** turns that into a **merge gate**: a corpus on disk,
  thresholds, and a non-zero exit when a change lowers the numbers.
- **The provenance rule:** only an **independently-labelled ground-truth** corpus
  (nmap from the same vantage, a second probe, hand verification) counts toward
  thresholds; a **regression** corpus (labelled by what the engine produces today)
  catches drift but *cannot* prove correctness. Conflating the two is the classic
  way a scanner "proves" accuracy it doesn't have.
- **Ground-truth discipline:** labels must be the **remote-validated** state from
  the scanner's vantage, never a local `ss -ltn` dump — bind-to-`0.0.0.0` ≠
  reachable.
- **Per-path tagging:** `syn_scanner` stamps `method = syn | connect_fallback` so
  accuracy is measured *per path*.

**Every proposal in §12 must pass this gate on an independently-labelled corpus
before it is promoted from *Coming soon* to *enabled*.** That is precisely what
lets us put a precision/recall figure in front of a client and stand behind it —
and it is already the product's policy (verified use-cases enabled, the rest gated).

---

## 12. Consolidated design roadmap (design-only, by accuracy ROI)

| # | Capability | Core technique (this doc) | Vedha touch-point | Risk |
|---|---|---|---|---|
| 1 | **LZR expected-service confirmation** | §2 ACK-with-data, 40 % filter, ≤5 handshakes | `workflow/router.py` | collection-only |
| 2 | **Version→CVE FP fixes** | §8.2–8.3 bound `[0,∞)`, OS-gate KEV, EPSS×confidence | manager `cve/`, `detection_engine/` | analysis-only |
| 3 | **TLS-inside-RDP / SCHANNEL** | §6 + §4 RDP sec-layer then inner TLS per version | `rdp_scanner`, `tls_scanner`, `router.py` | collection-only |
| 4 | **Firewall-analysis bundle** | §4 RFC-793 matrix, ACK first, caveated copy | reuse `syn_scanner` raw machinery | collection-only, CAP_NET_RAW |
| 5 | **JA4S/JA4X as primary identity** + JA4T | §6.3, §7.3 | `delta_scanner`, `device_classifier` | analysis-only (JA4T reuses SYN harvest) |
| 6 | **Service/version corpus depth** | §5 nmap probe-DB model, banner sanitisation | `service_banner.py`, `cpe.py` | data work |
| 7 | **SSVC decision layer** | §8.3 CISA decision tree over KEV/EPSS/CVSS | manager reporting | analysis-only |
| 8 | **Resumable sharded campaign** | §1.3 permutation + phase/shard/attempt | scheduler | infra |
| 9 | **IPv6 TGA for routed ranges** | §9.2 Entropy/IP seed→generate→connect | `ipv6_discovery.py` | collection-only, seeded |
| 10 | **OT SPAN/TAP pcap backend** | §10.2 DPI + function-code baseline | `passive_collector.py` | **zero-transmit** |

None crosses the collection-only / anonymous / read-only line. Every item is a
*design*, not a build — this document exists so the build, when authorised, starts
from the real wire-level mechanism and a measurable accuracy target, not a README
claim.

---

## 13. Sources

Fetched / searched this round (adds to Volume I §11):

- LZR (USENIX Sec '21; arXiv:2301.04841; ref impl github.com/stanford-esrg/lzr):
  https://arxiv.org/abs/2301.04841 · https://github.com/stanford-esrg/lzr
- GPS — Predicting IPv4 Services Across All Ports (arXiv:2303.00895): https://arxiv.org/pdf/2303.00895
- FoxIO JA4+ technical spec (fetched): https://github.com/FoxIO-LLC/ja4
- TLS-FP research: arXiv:2602.09606 · 2410.03817 · 2405.07848 · 2009.01939
- OS-FP (tabular transformer, arXiv:2502.09084): https://arxiv.org/pdf/2502.09084 · p0f v3 reference: https://lcamtuf.coredump.cx/p0f3/
- EPSS v4 (FIRST / Empirical Security, 2025-03-17): https://research.empiricalsecurity.com/research/introducing-epss-version-4
- CISA KEV · CISA SSVC decision guide
- IPv6 TGAs: Entropy/IP (Foremski 2016), 6Graph, 6Gen (zakird.com/papers/imc17-6gen.pdf), 6GAN (arXiv:2204.09839), IPv6 Hitlist Service (arXiv:2609.11475)
- OT/ICS: NIST SP 800-82, IEC 62443; passive ICS discovery (arXiv:1904.04271)

Internal: as Volume I, plus `scanner/{syn_scanner,ja4s,ja4x,os_fingerprint,cpe}.py`,
`scanner/{accuracy,accuracy_gate}.py`, `workflow/router.py`,
`docs/research/2026-09-23-scalable-large-subnet-scanning.md`.
