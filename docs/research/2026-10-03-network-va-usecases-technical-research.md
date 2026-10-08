# Vedha Network VA — Use-Case Technical Research (Levels 1–7)

**Status:** Research / proposal only. *No code is changed by this document.* It
is the technical backing for the client-facing use-case catalogue — the
core-level logic of every capability we propose, the best-accuracy method known
in the literature, and an honest map of where Vedha's shipping code already does
it versus where it is a gap.

**Date:** 2026-10-03 · **Branch:** `claude/serene-bardeen-1uqxzq` ·
**Author:** research pass over the probe scanner tree + current (2024–2026)
measurement literature.

> How to read this. The request was a 7-level taxonomy (Discovery → Port scan →
> State → Service fingerprint → Deep scanners → Intelligence → Exposure) plus a
> list of scan **modes**, TCP **techniques**, and port **presets**. This document
> walks every item of that taxonomy and answers four questions for each:
>
> 1. **Core logic** — what actually happens on the wire, at the protocol level.
> 2. **Best method / accuracy** — the state-of-the-art technique and its
>    measured accuracy, cited to primary sources (arXiv / USENIX / vendor
>    reference), so a claim we make to a client is defensible.
> 3. **Vedha today** — the shipping module (file path) and what it really does.
> 4. **Gap / proposal** — what to expose now, what to mark *Coming soon*, and the
>    single highest-accuracy improvement worth proposing.
>
> The governing constraint, unchanged: the **probe collects raw facts only**
> (unauthenticated, read-only, dial-out-only); the **manager** does all
> detection, CVE correlation and scoring. Nothing below proposes crossing that
> line. "Accuracy" here means *measured precision/recall against remote-validated
> ground truth*, never a local listener dump — the discipline already enforced by
> `scanner/accuracy.py` and `scanner/accuracy_gate.py`.

---

## 0. Executive summary — what to propose, and why

The product-policy rule is: **enable only what we have verified against a live
target; show the rest as "Coming soon" and refuse to dispatch it** (already
enforced in `agent/use_cases.py` via `status: "coming_soon"` + a backend 422
gate). This document keeps that rule and tells the client *exactly* what each
enabled use-case does.

The three things worth saying up front:

1. **Vedha's accuracy moat is architectural, not just algorithmic.** Every
   scanner emits a *state + machine-readable reason + confidence*, not a boolean,
   and a ground-truth gate (`accuracy_gate.py`) blocks any change that lowers
   measured precision/recall. That is rarer than the scan techniques themselves
   and is the strongest thing to put in front of a client.

2. **The biggest *honest* technical gaps are three, and they are all on the
   roadmap, not the core:** (a) no raw-packet firewall-analysis scans
   (ACK/FIN/NULL/Xmas/Window/Maimon); (b) TLS/SCHANNEL config *behind* RDP/SMB is
   never measured; (c) version→CVE false positives from open-ended OSV ranges.
   Sections 3, 5.2 and 6 give the fix for each.

3. **The best single accuracy upgrade in the whole surface** is adopting the
   **LZR "expected-service" handshake discipline** (USENIX Sec '21,
   [arXiv:2301.04841](https://arxiv.org/abs/2301.04841)) in the deep-scan router:
   confirm *what actually speaks* on a port in ≤5 handshakes instead of trusting
   the port number. It raises service-identification recall on non-standard ports
   dramatically and it is pure collection. Section 4 details it.

---

## LEVEL 1 — Discovery (host liveness)

**Client value:** "What is actually alive on this network?" — the inventory every
other level filters down from. A missed host is a missed asset, so here a false
*negative* is the expensive error.

### 1.1 Core logic

A host is "alive" if *anything* it controls answers a stimulus. Four independent
signals, strongest first:

| Signal | Stimulus | Positive proof | Privilege |
|---|---|---|---|
| **ARP** (same L2 segment) | ARP `who-has` / any on-LAN IP packet | ARP reply with the target's MAC = host exists at L2 | raw L2, or kernel neighbour cache (unpriv.) |
| **ICMP** echo | echo request | echo reply (and the reply's TTL is an OS hint) | raw/dgram ICMP socket |
| **TCP liveness** | SYN (or full connect) to common ports | SYN/ACK **or** RST — *both* prove a live stack | unprivileged (connect) |
| **UDP liveness** | protocol-valid datagram | any reply, or ICMP port-unreachable | unprivileged |

The subtlety that separates a good discovery engine from a bad one: **a RST (port
closed) still proves the host is alive.** Collapsing "alive" to "has an open port"
under-counts assets. And on a LAN, **ARP cannot be refused** — a host that drops
all ICMP/TCP (hardened workstations, phones, IoT) must still ARP to use the
network, so ARP/neighbour freshness is the catch-all.

### 1.2 Best method / accuracy

- **Stateless L3 discovery at scale** is the ZMap model: send one probe per host,
  no per-target state, randomized address order. ZMap reaches **~98% of listening
  hosts with a single packet**, the ~2% gap matching the Internet's background
  packet-loss rate ([ZMap, USENIX Sec '13](https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_durumeric.pdf)).
  The lesson for accuracy: **one probe ≈ 98%; the last ~2% needs a retransmit.**
- **Discovery is a *filter*, not proof of absence.** Silence never proves a host
  is down — it can be a firewall drop or a lost packet. The correct model grades
  confidence rather than asserting "dead" (ZMap/`masscan` both document this).
- **ARP-freshness beats ARP-cache.** A *fresh, kernel-confirmed* neighbour entry
  (Linux NUD `REACHABLE`) is high proof; a `STALE` cache entry is weak. Treating
  them identically is the classic over-count bug.
- **Multi-signal fusion** (ICMP + TCP + ARP), each with its own weight, is what
  modern engines (nmap `-PE -PS -PA -PR`) do; fusing beats any single signal.

### 1.3 Vedha today

- `scanner/host_discovery.py` — **fuses TCP-connect liveness with
  neighbour/ARP-freshness**, graded by Linux NUD state
  (`REACHABLE/PERMANENT`→high, `DELAY/PROBE`→medium, `STALE`→low,
  `FAILED`→negative), plus a UDP-liveness path. Emits `confirmed_alive /
  probably_alive / recently_observed / inconclusive / unreachable_from_vantage`
  each with a 0–1 confidence, while keeping the legacy `alive` boolean biased to
  *candidate* (a VA scanner must not drop a possible asset). This is exactly the
  "fuse signals, grade confidence, never collapse silence to dead" model the
  literature prescribes — and it is unprivileged (no raw socket needed).
- `scanner/os_fingerprint.py` — raw/dgram **ICMP** echo (+ optional
  timestamp/addr-mask), TTL harvest.
- `scanner/nmap_wrapper.py` — raw **ICMP/ARP/SYN** discovery when nmap + privilege
  are present.
- **IPv4/IPv6:** `port_scanner` resolves with `getaddrinfo(AF_UNSPEC)` and records
  the address family per observation, so v4 and v6 are never conflated.

### 1.4 Gap / proposal

- **ARP sweep is neighbour-cache-derived, not an active raw-ARP sweep**, in the
  unprivileged path. For a LAN segment where we hold `CAP_NET_RAW`, an *active*
  broadcast ARP sweep would catch silent L2-only hosts in one pass instead of
  relying on a connect() to prime each neighbour entry. Propose as a
  privilege-gated enhancement to `host_discovery` (falls back to today's
  behaviour).
- **MAC capture + OUI vendor lookup** (`usecases-networkva.md` HD-07/08 are `✗`):
  on-LAN, the neighbour entry already carries the MAC — surfacing it gives a free
  vendor hint and a stable `host_id` for delta (Level 7). High ROI, pure
  collection.
- **Single-probe retransmit discipline** is already present for TCP
  (`port_scanner` retransmits on silence); make the same explicit for the
  discovery sweep so we can state a measured coverage number (~98% + retransmit)
  to clients.

**Expose now:** *Network Discovery* (uc_discovery_only, code 1) — verified.
**Propose:** active ARP sweep + MAC/OUI as a LAN-privileged add-on.

---

## LEVEL 2 — Port scanning (breadth)

**Client value:** "Which doors are open, from where I'm standing?" The breadth
decision (how many ports) and the technique decision (how we knock) are
orthogonal and both belong in the UI.

### 2.1 Core logic — the two-stage model

Every scalable scanner is **two-stage**: a cheap, stateless, breadth-first sweep
finds open ports fast; expensive stateful work (banner/TLS/version) runs *only* on
the opens.

```
stage 1: find open ports FAST   →   stage 2: deep probe only the opens
(stateless SYN / connect sweep)      (service/version/TLS/DB/...)
```

- **TCP Connect** — full `connect()` via the OS stack. Completes the 3-way
  handshake. Unprivileged, works everywhere, but slow and heavily logged (one
  socket per port). This is the only thing that proves *reachability from this
  vantage* without root.
- **TCP SYN (half-open)** — send a lone SYN, read the reply (SYN/ACK=open,
  RST=closed, silence=filtered), never send the final ACK. Needs raw sockets
  (root/`CAP_NET_RAW`). Faster, quieter, one packet each way.
- **Stateless SYN (masscan/ZMap technique)** — keep *no* per-probe table; encode
  the probe key in the TCP initial sequence number (a "SYN cookie") so a genuine
  SYN/ACK validates itself (`reply.ack-1 == cookie(reply addressing)`). This is
  what lets a /16 finish in minutes instead of hours.

### 2.2 Best method / accuracy

- **Breadth = stateless; depth = stateful.** ZMap/masscan are stateless and
  sacrifice a little accuracy for enormous speed; nmap is stateful, adaptively
  retransmits, and is more accurate per host but slow at scale
  ([Zippier ZMap, WOOT '14](https://www.usenix.org/system/files/conference/woot14/woot14-adrian.pdf);
  [Ten Years of ZMap, arXiv:2406.15585](https://arxiv.org/pdf/2406.15585)). A
  product should use **stateless for the sweep and stateful for the deep pass** —
  precisely the funnel.
- **A requested rate is a safety ceiling, not a completion guarantee.** Firing at
  N pps does not mean N pps of *useful* coverage; packet loss and target rate
  limits mean the honest rate is lower. Coverage must be *measured and reported*,
  not assumed (this is Vedha's `ScanMetrics` completeness record — section 2.3).
- **Randomize the (IP, port) space and shard deterministically** so one target
  isn't hammered and a scan can be resumed/parallelised across probes without
  overlap (ZMap's address permutation; see also the scalable-subnet research in
  `docs/research/2026-09-23-scalable-large-subnet-scanning.md`).
- **Retransmit only on silence.** A definitive RST/refused is never retried; only
  `no_response` gets a bounded retransmit, because a single dropped SYN is a
  *scanner-manufactured* false negative.

### 2.3 Vedha today

- `scanner/port_scanner.py` — **TCP connect** engine with an evidence-based state
  machine (section 3), per-host `ScanMetrics` (requested vs classified vs missing
  vs duplicate ports → `complete()` / `degraded()` self-health), adaptive timeout
  (Jacobson/Karels SRTT+4·RTTVAR, `adaptive_timeout.py`), bounded retransmit on
  silence, and an adaptive rate controller. IPv4/IPv6 independent.
- `scanner/syn_scanner.py` — **stateless SYN with SYN-cookie validation**
  (masscan technique), gated by `syn_scan_supported()` (Linux + usable raw
  socket); **transparently falls back to the connect scanner** elsewhere, tagging
  `data["method"] = "syn" | "connect_fallback"` so accuracy is measurable per
  path.
- `scanner/mass_scan.py` — wraps the `masscan` **binary** when present, normalises
  its JSON into the same `ScanResult` schema; **pure-stdlib high-concurrency
  async connect sweep fallback** when masscan is absent. (Licensing note in the
  module: masscan is AGPL-3.0 — invoke, don't bundle.)
- **Port presets** (`port_scanner.resolve_profile` + `workflow/intensity.py`):
  `quick` (~15), `top100` (nmap canonical), `top1000` (1–1024 ∪ top100 ∪ Windows
  high-ports), `enterprise` (~2,500 curated — the `deep` intensity breadth),
  `full` (1–65535), `custom` (explicit `-p`/range). UDP: `narrow`
  (53/123/137/161/11211) vs `wide` (every catalogued UDP probe).

### 2.4 Gap / proposal — mapping to the requested catalogue

| Requested mode | Vedha mapping | State |
|---|---|---|
| TCP Connect | `port_scanner` | ✅ shipped |
| TCP SYN | `syn_scanner` (Linux+root) → connect fallback | ✅ shipped (fallback by design elsewhere) |
| Top 100 / Top 1,000 / All 1-65535 / Custom | `resolve_profile` presets | ✅ shipped |
| Top 20 / Top 10,000 | **not a named preset** | ⬜ add two presets (trivial) |
| UDP common/top/custom | `udp_scanner` + narrow/wide | ✅ common/wide; custom list ⬜ |
| TCP + UDP combined | funnel runs both when profile includes UDP | ✅ via campaign |
| Previously-discovered ports | delta feeds a port set | 🟡 via `delta_scanner` identity, not yet a one-click preset |
| Service-specific / org port profile | `custom` + branch port tables | 🟡 data exists, no saved-profile UI |

**Proposal:** add `top20` and `top10000` presets and a **"previously discovered
ports"** preset (feed last scan's open set as the candidate list — turns a
re-scan into a fast confirmation pass). All are data/config, not new scan engines.

---

## LEVEL 3 — State inference (open / closed / filtered / open|filtered)

**Client value:** the single most abused word in scanning is "open." Vedha's
differentiator is that it reports *why* it believes a state, with a confidence,
so a firewall drop is never silently sold as a closed port.

### 3.1 Core logic — what each state actually means

| State | TCP evidence | UDP evidence | Certainty |
|---|---|---|---|
| **open** | SYN/ACK (or completed connect) | protocol-valid reply | high |
| **closed** | RST | ICMP type 3 code 3 (port-unreachable) | high |
| **filtered** | silence within timeout, or ICMP admin-prohibited | silence + no ICMP | **medium** — silence has many causes |
| **open\|filtered** | — (connect can't produce this) | silence (no reply, no ICMP) | inherent UDP ambiguity |
| **unreachable** | ICMP host/net-unreachable (EHOSTUNREACH/ENETUNREACH) | same | high |
| **error** | local fault (fd exhaustion, DNS, policy) | same | diagnostic, not a target fact |

The two mistakes that wreck accuracy:

1. **Collapsing every OSError to "filtered."** A scanner-side "too many open
   files" or a routing "no route to host" is *not* a target firewall. Classify by
   errno instead.
2. **Treating UDP silence as closed (or open).** UDP has no handshake; silence is
   genuinely `open|filtered`. Only an ICMP port-unreachable proves `closed`.

### 3.2 Best method / accuracy

- **State is vantage-relative.** "Open" means *reachable from this probe*, which
  is a different fact from "the host has a socket in LISTEN." A host binding 20
  ports to `0.0.0.0` may expose 5 remotely; the other 15 are firewalled. Ground
  truth for accuracy scoring must therefore be the *remote-validated* state, never
  a local `ss -ltn` dump (RFC-793 behaviour + the ZMap vantage lesson; enforced in
  `accuracy.py`).
- **Timeout is not proof.** Label silence `filtered / no_response` with
  `confidence: medium` and retransmit once, rather than asserting a firewall.
- **UDP `closed` via ICMP is the accuracy win** — surfacing the ICMP
  port-unreachable removes a port from the ambiguous pile honestly.

### 3.3 Vedha today

`scanner/port_scanner.py` ships exactly this model. Its module docstring
enumerates the state→reason table verbatim: `open/connect_success`,
`closed/connection_refused|connection_reset`,
`filtered/no_response|connection_aborted`,
`unreachable/host_unreachable|network_unreachable|host_down`, and an `error` class
with `dns_error/local_resource_error/address_unavailable/permission_denied/os_error`
(errno-classified, not collapsed). Every observation carries `proto`, `state`, a
machine-readable `reason`, and a `confidence`. `scanner/udp_scanner.py` maps ICMP
port-unreachable → `closed` and otherwise reports `open|filtered` with the
ambiguity explicit. This is **best-practice, already shipped** — and the 2026-08
ground-truth run (`PROBE_CAPABILITY_STATUS.md`) measured **precision 100% / recall
100%** on a Windows 11 host precisely because bind-to-`0.0.0.0` ≠ reachable was
handled correctly.

### 3.4 Gap / proposal

- Status-gap #10 (`docs/STATUS.md`) — a report once showed a RST ("closed") as
  `error`. Code check says the connect path already maps refused→`closed`; the
  open item is to **locate whichever producer mislabels it** and confirm live.
  Worth a verification pass, not a redesign.
- **Filtered-reason enrichment:** when we hold a raw socket, an ICMP
  *admin-prohibited* (type 3 code 13) distinguishes "firewall actively dropping"
  from "silent timeout" — a higher-confidence `filtered`. Propose as a
  privilege-gated signal on `syn_scanner`.

---

## LEVEL 3b — TCP technique options (firewall / filtering analysis)

The requested "Advanced / Firewall Analysis" techniques — **ACK, FIN, NULL, Xmas,
Window, Maimon** — are a distinct capability class from Connect/SYN, and Vedha
does **not** ship them today (verified: no implementation in `probe/scanner`).
They belong in the proposal as a *Firewall Analysis* bundle, clearly scoped.

### Core logic & what each is *for*

| Technique | Packet | Open port | Closed port | What it tells you |
|---|---|---|---|---|
| **ACK** | lone ACK | RST (`unfiltered`) | RST (`unfiltered`) | **Maps firewall rules** — silence/ICMP-prohibited = *filtered*; it never finds open ports, it finds whether a **stateful** firewall sits in front. |
| **Window** | lone ACK | RST with **non-zero** window | RST with zero window | ACK-scan variant: some stacks leak open/closed via the RST window size. |
| **FIN** | lone FIN | *no response* | RST | RFC-793 stealth: open ports stay silent. |
| **NULL** | no flags | *no response* | RST | same RFC-793 trick, zero flags. |
| **Xmas** | FIN+PSH+URG | *no response* | RST | same, "lit up like a Christmas tree." |
| **Maimon** | FIN+ACK | *(RFC: RST always; many BSD drop if open)* | RST | finds open|filtered on BSD-derived stacks. |

### Best method / accuracy — the honest limits

These lean on **RFC-793** response behaviour, and the single most important thing
to tell a client is the reliability caveat from nmap's own documentation
([nmap: scan methods](https://nmap.org/book/scan-methods-maimon-scan.html),
[firewall subversion](https://nmap.org/book/firewall-subversion.html)):

- **Windows, Cisco IOS, and many modern stacks send RST for every probe
  regardless of port state**, which makes FIN/NULL/Xmas/Maimon report *all* ports
  as `closed` on those targets. They are therefore **diagnostic/evasion tools for
  specific environments, not general-purpose open-port finders.**
- **ACK scan's value is orthogonal and real:** it is the canonical way to learn
  whether a firewall is **stateful vs stateless** and which ports it filters —
  intelligence a Connect/SYN scan cannot produce. This is the one of the six worth
  foregrounding.

### Proposal

Expose these under an explicit **"Advanced → Firewall / Filtering Analysis"**
group, **disabled by default**, with per-technique card copy that states the
Windows/modern-stack caveat so we never sell FIN-scan results as authoritative on
a Windows estate. All require `CAP_NET_RAW` (same gate as `syn_scanner`) and are
pure collection (no handshake completion). Implementation reuses
`syn_scanner`'s raw-packet build/parse machinery — the flag field is the only
change — so this is a contained, high-credibility addition. Keep Connect + SYN as
the two prominent enterprise defaults, exactly as the request specifies.

---

## LEVEL 4 — Service fingerprinting (what actually speaks on a port)

**Client value:** "A port is open — but is it *really* SSH, and which SSH?" The
port number is a hint, not an answer.

### 4.1 Core logic

Two families:

- **Speak-first services** (SSH, SMTP, FTP, VNC, Telnet, many DBs): just read the
  banner the server volunteers.
- **Speak-when-spoken-to services** (HTTP, TLS, binary DB protocols): send a
  minimal, benign, protocol-valid probe and read the structured response. If
  plaintext reveals nothing, attempt **one TLS handshake** and repeat inside the
  tunnel — so HTTPS/IMAPS/SMTPS on any port yields a real banner plus a positive
  "this port speaks TLS" fact.

### 4.2 Best method / accuracy

- **nmap's probe model is the reference**: a library of probes each carrying a
  **rarity** (1–9) and a list of likely ports; `--version-intensity` (0–9,
  default 7) bounds which probes fire; **softmatch** gives a tentative protocol ID
  that narrows subsequent probes
  ([nmap vscan technique](https://nmap.org/book/vscan-technique.html)). The
  accuracy principle: *send the cheapest probe that disambiguates, escalate only on
  miss.*
- **LZR (USENIX Sec '21, [arXiv:2301.04841](https://arxiv.org/abs/2301.04841))**
  is the state-of-the-art for *unexpected* services: it identifies **99% of
  identifiable unexpected services in ≤5 handshakes**, because many services don't
  run on their "expected" port. The takeaway for Vedha: **confirm the real
  protocol per open port before routing to a deep scanner**, rather than routing
  by port number.
- **GPS ([Predicting IPv4 Services Across All Ports](https://arxiv.org/pdf/2303.00895))**
  finds **92.5% of services across all ports with 131× less bandwidth** than
  exhaustive scanning by *predicting* likely (port, service) pairs — relevant when
  we eventually do all-port service ID at scale.

### 4.3 Vedha today

- `scanner/service_banner.py` — banner grab + benign HTTP probe + **one-shot TLS
  fallback** handshake; soft-match regex table → `{service, product, version}`;
  structured HTTP head extraction (status, Server, X-Powered-By, WWW-Authenticate,
  title). Emits `cpe_unmapped` when a product is named but no CPE maps (blind-spot
  visibility).
- `scanner/service_enum.py` — reverse-DNS/mDNS/NetBIOS hostnames, version, OS
  hint, **role tags**, weak/legacy flags, mgmt/auth tags, local topology.
- **Protocol-confirming scanners** (port number is *not* trusted):
  `ssh_scanner` (RFC-4253 ident + KEXINIT), `rdp_scanner` (real X.224 handshake —
  confirms RDP ≠ "3389 open"), `smb_scanner` (SMB1/SMB2 negotiate), `db_scanner`
  (binary handshakes for MySQL/Postgres/MSSQL/Redis/Mongo/Oracle), `tls_scanner`,
  `dns_scanner`, `smtp_scanner`, `ftp_scanner`, `vnc_scanner`, `snmp_scanner`,
  `msrpc_scanner`, `printer_scanner`, `ldap_scanner`, `nfs_scanner`,
  `rsync_scanner`, `ipmi_scanner`, `mcp_ai_scanner`.
- The requested Level-4 protocol list maps cleanly: generic banner ✅, SSH ✅,
  HTTP ✅, TLS ✅, FTP ✅, SMTP ✅, DNS ✅, SMB ✅, RDP ✅, RPC/MSRPC ✅, WinRM ✅
  (port+banner tag, no deep WinRM auth probe), databases ✅, Redis ✅, SNMP ✅,
  VNC ✅.

### 4.4 Gap / proposal

- **Adopt the LZR discipline in `workflow/router.py`:** before routing a port to
  its deep scanner, use the ≤5-handshake confirmation so a service on a
  non-standard port (e.g. HTTPS on 8443, Redis on 6380, SSH on 2222) is still
  deep-scanned, and a mislabelled port isn't. This is the **highest-accuracy,
  lowest-risk** fingerprinting upgrade available and is pure collection. *Propose
  as the flagship Level-4 improvement.*
- **Version-string extraction** is the weak rung (`usecases-networkva.md` SB-03/04
  are `✗` on many services): product/version is often null. A richer probe/response
  pattern DB (nmap-style, re-derived license-clean per `OSS_CORE_STUDY.md`) raises
  recall; version quality directly gates Level 6 CVE accuracy.
- **Banner sanitisation** (SB-08): strip non-printable bytes before storing, so a
  `\x00\x00\x01` banner is evidence, not noise.

---

## LEVEL 5 — Deep scanners (configuration-grade inspection)

**Client value:** the move from "a service is here" to "this service is
**misconfigured** here" — the findings a client pays for. All read-only,
unauthenticated, anonymous/null/default-community only (never credential
guessing).

### 5.1 SMB configuration

- **Core logic:** SMB1 `SMB_COM_NEGOTIATE` listing `NT LM 0.12` → a valid reply
  proves SMBv1 *enabled* (EternalBlue transport). SMB2 `NEGOTIATE` → security-mode
  byte reveals **signing enabled/required**. Null-session (`smb_enum_scanner`):
  anonymous tree/user enumeration. NTLMSSP challenge leaks the Windows build.
- **Best method/accuracy:** nmap `smb-protocols`/`smb-security-mode` are the
  reference; the fact to assert is *dialect + signing posture*, which is
  deterministic from the negotiate response (no auth needed). Vedha's 2026-08
  run matched ground truth exactly (`EnableSMB1Protocol=False`,
  `RequireSecuritySignature=True`).
- **Vedha:** `smb_scanner.py` + `smb_enum_scanner.py` ✅. Findings:
  `SMB-V1-ENABLED`, SMB-signing-not-required, `SMB-NULL-SESSION(-USERS)`.

### 5.2 TLS configuration

- **Core logic:** per TLS port, attempt a handshake at each protocol version
  (1.0/1.1/1.2/1.3), record the negotiated cipher, and DER-parse the certificate
  (subject/issuer/validity/SAN). Grade: deprecated version, weak cipher
  (NULL/EXPORT/RC4/DES/anon), self-signed, expired.
- **Best method/accuracy:** sslyze/testssl.sh define the field reality
  (`OSS_CORE_STUDY.md` notes both are copyleft — learn from, don't embed;
  `tlsx` is the MIT-clean reference). The accuracy rule: **enumerate per-version
  by actually offering each**, don't infer from one handshake.
- **Vedha:** `tls_scanner.py` ✅ (version enumeration, cipher classify, cert parse
  via `cryptography`, `grade_tls_posture`).
- **Gap (status #3, confirmed):** `tls_scan` is deliberately **never run on RDP
  3389 / SMB 445 / MSRPC 135** (`workflow/router.py` skips ports observed not to
  speak plaintext TLS, and RDP wraps TLS in its own protocol). So the **SCHANNEL**
  protocol/cipher set behind those listeners is never measured — RDP only gets
  `POSTURE-RDP-NO-TLS`. **Proposal:** a *TLS-inside-RDP* probe — negotiate the RDP
  security layer, then drive the inner TLS handshake per version/cipher — plus
  SCHANNEL measurement on SMB/LDAP where the protocol tunnels TLS. This is the
  single most-requested missing deep check from the test round.

### 5.3 HTTP / web

- **Core logic:** one benign GET per web port; record status, redirect, response +
  security headers (HSTS/CSP/X-Frame-Options presence), `<title>`, server-tech
  hints, and the auth surface (Basic-over-cleartext). **No** fuzzing, dir-brute, or
  injection — fingerprinting, not attacking (whatweb/httpx observe-mode parity).
- **Best method/accuracy:** the ProjectDiscovery httpx model (MIT) — deterministic
  header/metadata extraction — is the clean reference.
- **Vedha:** `web_scanner.py` (+ HTTP facts in `service_banner.py`) ✅.
  Use-cases `uc_external_web_triage`/`uc_web_app_triage` are **Coming soon** (TLS
  half proven; web half needs live-target verification).

### 5.4 Database exposure

- **Core logic:** each DB speaks a binary protocol, not a text banner. Send the
  minimal valid handshake/greeting and read the version the protocol volunteers;
  for Redis/Mongo, the unauthenticated `INFO`/`isMaster` read is itself the
  exposure finding. No credentials, no queries, no data.
- **Vedha:** `db_scanner.py` ✅ (MySQL/MariaDB, Postgres, MSSQL TDS pre-login,
  Redis, Mongo, Oracle TNS). Finding: `unauth database read` (critical for
  Redis/Mongo no-auth). `uc_db_exposure` is **Coming soon** pending live-target
  verification.

### 5.5 SNMP

- **Core logic:** v1 GET `sysDescr.0` with each candidate community → first reply
  establishes it; then a targeted GETNEXT MIB walk (system/interface/ARP/IP/proc/
  TCP-conn tables); a single GETBULK to **measure amplification** (response/request
  bytes, never looped/spoofed); a USM discovery msg to detect v3.
- **Best method/accuracy:** default-community (`public`/`private`) detection is the
  high-value, deterministic check; the MIB walk turns one open UDP port into a full
  device/topology inventory without scanning. Amplification factor is the
  DDoS-reflector risk signal.
- **Vedha:** `snmp_scanner.py` ✅ (`uc_snmp_exposure`, verified). **Gap (status
  #12):** cannot distinguish a *write* (`private`/RW) community from read — the
  scanner never sends a SET by design. Proposal: a controlled, reversible SET probe
  **or** word the finding "community named `private`; write access not tested"
  (product + authorization decision).

### 5.6 AI / MCP exposure

- **Core logic:** unauthenticated GET of well-known discovery endpoints — Ollama
  `/api/tags`,`/api/version`; OpenAI-compatible `/v1/models` (vLLM/LM Studio/TGI);
  MCP `/sse`,`/mcp`. Record whether auth appears required. **Read list/discovery
  endpoints only** — never call a tool, send a prompt, or load a model.
- **Best method/accuracy — the anti-FP design is the hard part and Vedha already
  has it:** a bare 401/403 on an AI-shaped path is *not* evidence (macOS AirPlay
  403s on every path). Qualifying signals: RFC-7235 `WWW-Authenticate`;
  **MCP-specific RFC-9728** `WWW-Authenticate` referencing OAuth Protected-Resource
  Metadata (`.well-known/oauth-protected-resource`) = near-certain real MCP server;
  or a JSON-shaped model list. This is current (MCP Authorization spec, 2025-03+)
  and a genuine differentiator — AI/MCP is a fast-growing, unmonitored surface.
- **Vedha:** `mcp_ai_scanner.py` ✅ (logic shipped). `uc_ai_endpoint_sweep` is
  **Coming soon** pending live-target verification.

### 5.7 OT / ICS

- **Core logic:** **passive only.** Transmit nothing to any target. Bind
  broadcast/announcement UDP ports receive-only (NetBIOS 137, BACnet/IP 47808,
  EtherNet/IP 2222) and record hosts that announce themselves. **No multicast
  join** (IP_ADD_MEMBERSHIP emits IGMP — not passive), so mDNS/SSDP/LLMNR are
  reported as *unavailable coverage* until a receive-only SPAN/TAP backend is
  configured.
- **Best method/accuracy:** this is the categorical OT rule, not a preference —
  **active scanning crashes fragile PLCs/RTUs**; a single unsolicited connection or
  malformed probe has rebooted controllers and tripped physical processes. **NIST
  SP 800-82** is the governing guidance: *do not run active IT scanners on the
  plant floor; identify devices by listening.* Protocol-aware passive monitoring
  (Modbus/DNP3/EtherNet-IP/PROFINET) + behavioural baselining is the state of the
  art.
- **Vedha:** `passive_collector.py` + `ot` profile is **structurally passive-only**
  (`gate_0_is_passive_profile` routes to `PassiveCollector` exclusively; zero
  active-probe gates reachable). `uc_ot_passive` is **Coming soon** (needs an OT
  segment to verify). This architectural guarantee — the OT profile *cannot* emit
  an active packet — is a strong, defensible claim to a client. **Proposal:** add
  a receive-only SPAN/TAP packet-capture backend to recover mDNS/SSDP/LLMNR + deep
  protocol dissection, still transmit-nothing.

---

## LEVEL 6 — Intelligence (service → product → version → OS/device → confidence/evidence)

**Client value:** the inference layer that turns facts into an identity — *and*
tells you how much to trust it. This is the manager-side correlation territory.

### 6.1 Core logic

- **Service/product/version:** from banners, HTTP headers, TLS certs, protocol
  version fields → a CPE 2.3 identity.
- **OS/device hints:** TTL rounded to initial {64,128,255} + TCP window/MSS +
  ICMP behaviour → OS family (`os_fingerprint.py`); fused with open-port signature
  → device role (`device_classifier.py`).
- **Confidence + evidence:** every inference carries a calibrated confidence, the
  signals that drove it, and whether independent signals corroborate.

### 6.2 Best method / accuracy

- **OS fingerprinting ceilings:** classic **p0f v3** reaches ~92.8% OS-name
  accuracy but only ~64% precision / ~49% recall — passive TTL/window/options
  alone are limited. **ML on TCP/IP headers** (tabular transformers,
  [arXiv:2502.09084](https://arxiv.org/pdf/2502.09084); nPrintML) pushes recall
  well past p0f with smaller packet samples. The honest client message: **OS family
  from TTL is a *hint* with a confidence, not a verdict** — which is exactly how
  `os_fingerprint.py` scores it.
- **TLS-stack identity:** **JARM** (Salesforce 2020) is the active 10-probe digest
  Vedha computes, but JARM collisions have grown under TLS 1.3/QUIC. **JA4+** (FoxIO)
  is the modern successor — **JA4S** (ServerHello) and **JA4X** (certificate
  structure) are stable, sort extensions by type, and need no extra probing (JA4X
  is computed from the cert `tls_scanner` already collects). JA4-family fingerprints
  are the current research approach for actor/infra identification
  ([arXiv:2602.09606](https://arxiv.org/abs/2602.09606) TLS bad-bot detection;
  [arXiv:2410.03817](https://arxiv.org/abs/2410.03817) similarity mapping;
  [FoxIO JA4+ reference](https://github.com/FoxIO-LLC/ja4)).
- **CVE correlation accuracy** (Level 6→7 bridge): a **version match does not prove
  exposure** — distros backport fixes without bumping the version, the dominant
  false-positive source. Prioritise with **KEV** (actually-exploited) first, then
  **EPSS** (EPSS v4, March 2025; EPSS≥0.1 catches ~63% of exploited CVEs while
  flagging only ~2.7% of all CVEs — ~20× more efficient than "CVSS≥7"), then CVSS.
  Only ~2.3% of CVSS-7+ CVEs are ever observed in exploitation, so CVSS alone
  over-alerts.

### 6.3 Vedha today

- `os_fingerprint.py` (TTL+window+MSS heuristic, confidence), `device_classifier.py`
  (role with **confidence capped by number of agreeing signals** — one open port is
  ≤0.5, never certainty), `service_banner.py`/`cpe.py` (product→CPE 2.3 + EOL
  catalogue), `tls_fingerprint.py` (JARM-style), **`ja4s.py` + `ja4x.py` already
  shipped** (modern successor).
- **Manager CVE track** (`manager/.../cve/` + `detection_engine/`): CPE match →
  offline NVD/OSV range match (dpkg/epoch-aware) → **KEV+EPSS+CVSS** join
  (precedence KEV > EPSS≥0.5 > EPSS≥0.1 > CVSS) → confidence `medium` max for
  banner-derived, **distro-backport marker downgrades to `low`**, mirror-staleness
  surfaced past 7 days. Confidence and risk are kept **orthogonal** (a low-confidence
  finding can still be critical-risk, "verify patch level").

### 6.4 Gap / proposal

- **Version→CVE false positives (status #4, confirmed):** Debian OSV records for
  *unfixed* CVEs are `[0, unbounded)` and match every upstream banner version.
  **Proposal:** mark open-ended / distro-unfixed matches as *suspected* and bound
  them with upstream NVD data before they reach the queue.
- **KEV not OS-gated (status #5, confirmed):** `_KEV_LINKS` maps a rule to CVEs
  with no OS applicability, so `POSTURE-RDP-NO-NLA` links BlueKeep on Windows 11.
  **Proposal:** an applicability field (OS family + version range) per KEV link.
- **EPSS over-promotion (status #6):** a DoS at 30% confidence shouldn't be
  Critical. **Proposal:** cap EPSS promotion by match-confidence and impact.
- **JA4+ over JARM:** JA4S/JA4X are shipped — **make them the primary host-identity
  key** for delta (section 7) and deprecate JARM's role to a legacy corroborator,
  matching the literature's collision findings.
- **Confidence surfaced to the user** (status #8): show the role/OS confidence in
  the UI so a workstation-running-VMware mis-call reads as "hypervisor (0.4)", not a
  silent wrong verdict.

---

## LEVEL 7 — Exposure (change over time & reachability)

**Client value:** a VA is a snapshot; security is the *delta*. "What is newly
exposed since last time, and what can an outsider actually reach?"

### 7.1 Core logic

- **Change detection:** diff two scan snapshots on a **stable host identity** and
  classify each change: *new service / service gone / version change / state change
  (filtered↔open) / host appeared / host gone*. The hard part is the identity key:
  IP churns (DHCP), so key on the richest stable identifier available —
  **MAC > hostname > IP** (and, for internet hosts with no MAC, a TLS-stack
  fingerprint).
- **Reachability / vantage:** exposure is path-dependent. 445 can be open from the
  LAN, filtered from guest Wi-Fi, unreachable from the internet — all true at once.
  Never average or overwrite vantages; a port is "external" only if a vantage we
  treat as external actually saw it open.

### 7.2 Best method / accuracy

- **Identity-stable diffing** is the correct model (continuous attack-surface
  monitoring); keying on IP alone manufactures false new/gone churn on DHCP
  networks. Using a **fingerprint** (JA4S/JA4X or JARM) as the identity for
  MAC-less internet hosts is the research-backed approach and feeds directly from
  Level 6.
- **Multi-vantage reconciliation** is the honest way to answer "internet-exposed vs
  internal-only" — a single probe can't, and silence from one vantage never
  disproves reachability confirmed from another.
- **Significance filtering:** not every version-string wobble is a real change;
  grade severity (new *service* > version bump > cosmetic banner change) so the
  delta report is signal, not noise.

### 7.3 Vedha today

- `scanner/delta_scanner.py` ✅ — JSONL snapshot diff, `host_id = MAC > hostname >
  IP`, the six change classes above, `_new_service_severity` +
  `_significant_version_change` filtering. (Playbook 08.)
- `scanner/vantage_matrix.py` ✅ — pure-logic per-vantage reconciliation,
  external/internal/nowhere, never collapses vantages. Feeds `uc_exposure_matrix`
  (code 81, verified) and the multi-probe story.
- Requested Level-7 items map directly: new port ✅, closed port ✅, service
  changed ✅, version changed ✅, unexpected service ✅ (new_service), internet/LAN
  reachable ✅ (vantage_matrix), previous-scan comparison ✅ (delta_scanner).

### 7.4 Gap / proposal

- `uc_rescan_delta` (code 11) is **Coming soon** — the engine exists; it needs the
  manager-side two-snapshot orchestration + a verified live run to promote.
- **Use JA4S/JA4X as the MAC-less identity** in `delta_scanner` so internet-facing
  hosts get stable diffing (today it falls back to IP for them).
- **"Previously discovered ports" → fast re-scan preset** (Level 2 proposal) closes
  the loop: delta identifies the interesting ports, the next scan confirms them
  cheaply.

---

## 8. Scan-mode / technique / preset coverage matrix (the requested lists)

**Core scan modes**

| Mode | Vedha | State |
|---|---|---|
| TCP Default / common | `quick`/`it` profile | ✅ |
| TCP Top 100 | `top100` | ✅ |
| TCP Top 1,000 | `top1000` | ✅ |
| TCP All 1-65535 | `full` / `uc_full_port_audit` (80) / `uc_deep_port_sweep` (82) | ✅ |
| TCP Custom (`22,80,443,8000-9000`) | `custom` + `parse_ports` | ✅ |
| UDP Default / common | `udp_scanner` narrow | ✅ |
| UDP Top | narrow/wide | ✅ (wide) |
| UDP All 1-65535 | — | ⬜ (UDP is per-protocol-probe, not blind all-port by design) |
| UDP Custom | — | 🟡 engine supports a port list; no preset UI |
| TCP + UDP combined | campaign / profile includes UDP | ✅ |

**TCP techniques**

| Technique | Vedha | State |
|---|---|---|
| Connect | `port_scanner` | ✅ prominent default |
| SYN | `syn_scanner` (Linux+root→fallback) | ✅ prominent default |
| ACK | — | ⬜ propose (Firewall Analysis — highest-value of the six) |
| FIN / NULL / Xmas | — | ⬜ propose (Advanced; Windows caveat) |
| Window | — | ⬜ propose (Advanced) |
| Maimon | — | ⬜ propose (Advanced; BSD-specific) |

**Port-selection presets**

| Preset | Vedha | State |
|---|---|---|
| Common / Top 100 / Top 1,000 / All / Custom list / Custom range | `resolve_profile` + `parse_ports` | ✅ |
| Top 20 | — | ⬜ trivial add |
| Top 10,000 | — | ⬜ add (between `enterprise` ~2,500 and `full`) |
| Previously discovered ports | delta identity exists | 🟡 wire as a preset |
| Service-specific ports | branch port tables (`_BRANCH_PORT_TABLE`) | 🟡 internal, not a user preset |
| Organization-defined profile | `custom` | 🟡 no saved-profile UI |

---

## 9. Use-case catalogue cross-walk (the 15 field use-cases ↔ Levels ↔ code)

| # | Field use-case | Levels exercised | Catalog id (code) | Verified? |
|---|---|---|---|---|
| 1 | Network Liveness Sweep | 1 | `uc_discovery_only` (1) | ✅ enable |
| 2 | Device Identification | 1,4,6 | `uc_device_inventory` (2) | ✅ enable |
| 3 | Full Assessment | 1–6 | `uc_full_assessment` (10) | ✅ enable |
| 4 | Re-scan / Delta | 7 | `uc_rescan_delta` (11) | 🟡 Coming soon |
| 5 | External Web + TLS | 4,5 | `uc_external_web_triage` (20) | 🟡 Coming soon (TLS half proven) |
| 6 | Web App Triage | 4,5 | `uc_web_app_triage` (21) | 🟡 Coming soon |
| 7 | Database Exposure | 4,5 | `uc_db_exposure` (40) | 🟡 Coming soon |
| 8 | Windows / SMB | 4,5 | `uc_windows_estate` (30) | ✅ enable |
| 9 | SNMP Exposure | 4,5 | `uc_snmp_exposure` (50) | ✅ enable |
| 10 | UDP / Amplification | 2,3,5 | `uc_udp_service_exposure` (51) | ✅ enable |
| 11 | Full-Port Audit | 2,3 | `uc_full_port_audit` (80) | ✅ enable |
| 12 | Multi-Vantage Exposure | 7 | `uc_exposure_matrix` (81) | ✅ enable |
| 13 | AI / MCP Sweep | 4,5 | `uc_ai_endpoint_sweep` (61) | 🟡 Coming soon |
| 14 | IoT / Embedded Survey | 1,4 | `uc_iot_device_survey` (60) | ✅ enable |
| 15 | OT / ICS Passive | 1 (passive) | `uc_ot_passive` (70) | 🟡 Coming soon |
| — | Network VA (full campaign) | 1–7 | `uc_network_va` (12) | ✅ enable |
| — | Deep Port Sweep (≤3 hosts) | 2–6 | `uc_deep_port_sweep` (82) | ✅ enable |

**Enable now (verified, 9 + 2 campaign/deep):** 1, 2, 3, 8, 9, 10, 11, 12, 14 +
`uc_network_va` + `uc_deep_port_sweep`. **Coming soon (logic shipped, needs a
matching live target to verify):** 4, 5 (web half), 6, 7, 13, 15. This matches the
current `agent/use_cases.py` + backend 422 gate exactly — the policy is already
code-enforced, which is itself a client-credibility point ("we only enable what we
have proven").

---

## 10. Prioritised proposal (what to build after this research, by accuracy ROI)

Ordered by accuracy/credibility gain per unit of work; none crosses the
collection-only line:

1. **LZR expected-service confirmation in the router** (Level 4) — biggest recall
   gain on non-standard ports; ≤5 handshakes; pure collection.
2. **Version→CVE FP fixes** (Level 6: open-ended OSV bounding, OS-gated KEV,
   EPSS×confidence cap) — directly removes the most visible false positives from
   client reports.
3. **TLS-inside-RDP / SCHANNEL measurement** (Level 5.2) — closes the top
   confirmed deep-scan gap.
4. **Firewall-Analysis technique bundle** (Level 3b: ACK first, then
   FIN/NULL/Xmas/Window/Maimon) — new capability class, reuses `syn_scanner`
   raw-packet machinery, caveated copy.
5. **JA4S/JA4X as primary host identity** for delta (Levels 6→7) — stable diffing
   for MAC-less internet hosts.
6. **Preset completeness** (Top 20, Top 10,000, previously-discovered-ports, saved
   org profiles) — cheap, high perceived value.
7. **Discovery LAN upgrades** (active ARP sweep + MAC/OUI) — better asset recall on
   L2.
8. **OT receive-only SPAN/TAP backend** — recovers mDNS/SSDP/LLMNR, still passive.

Each should go through the **accuracy gate** (`accuracy_gate.py`) with an
independently-labelled ground-truth corpus before it is promoted from *Coming
soon* to *enabled* — that gate is the thing that lets us put precision/recall
numbers in front of a client honestly.

---

## 11. Sources

Primary / measurement literature:

- ZMap — Fast Internet-Wide Scanning (USENIX Security '13): https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_durumeric.pdf
- Zippier ZMap — 10 Gbps (WOOT '14): https://www.usenix.org/system/files/conference/woot14/woot14-adrian.pdf
- Ten Years of ZMap (arXiv:2406.15585): https://arxiv.org/pdf/2406.15585
- LZR — Identifying Unexpected Internet Services (USENIX Security '21; arXiv:2301.04841): https://arxiv.org/abs/2301.04841
- GPS — Predicting IPv4 Services Across All Ports (arXiv:2303.00895): https://arxiv.org/pdf/2303.00895
- Nmap — service/version detection technique: https://nmap.org/book/vscan-technique.html
- Nmap — Maimon scan & firewall subversion: https://nmap.org/book/scan-methods-maimon-scan.html · https://nmap.org/book/firewall-subversion.html
- Tabular-transformer OS fingerprinting (arXiv:2502.09084): https://arxiv.org/pdf/2502.09084
- p0f (passive TCP/IP fingerprinting) — reference: https://lcamtuf.coredump.cx/p0f3/
- JA4+ reference (FoxIO JA4/JA4S/JA4X): https://github.com/FoxIO-LLC/ja4
- TLS fingerprinting for bad-bot detection (arXiv:2602.09606): https://arxiv.org/abs/2602.09606
- TLS fingerprint feature-expansion + similarity (arXiv:2410.03817): https://arxiv.org/abs/2410.03817
- Positional-unigram byte models for TLS fingerprinting (arXiv:2405.07848): https://arxiv.org/abs/2405.07848
- Accurate TLS fingerprinting using destination context (arXiv:2009.01939): https://arxiv.org/abs/2009.01939
- IPv6 Hitlist Service — 10 years (arXiv:2609.11475): https://arxiv.org/pdf/2609.11475
- NIST SP 800-82 (OT/ICS security) — governing passive-first guidance.
- EPSS v4 / KEV / CVSS prioritisation (FIRST EPSS; CISA KEV).

Internal (this repo):

- `probe/agent/use_cases.py` · `probe/scanner/*` (port_scanner, syn_scanner,
  host_discovery, os_fingerprint, ipv6_discovery, udp_scanner, service_banner,
  service_enum, tls_scanner, tls_fingerprint, ja4s, ja4x, smb_scanner,
  smb_enum_scanner, db_scanner, snmp_scanner, rdp_scanner, ssh_scanner,
  mcp_ai_scanner, passive_collector, delta_scanner, vantage_matrix,
  device_classifier, accuracy, accuracy_gate, mass_scan)
- `probe/workflow/{gates,intensity,router}.py` · `probe/PROBE_CAPABILITY_STATUS.md`
- `NETWORK_VA_USE_CASES.md` · `usecases-networkva.md` · `docs/STATUS.md`
- `docs/research/2026-09-23-scalable-large-subnet-scanning.md`
- `probe/Capabilties/{OSS_CORE_STUDY,IMPLEMENTATION_RISKS_AND_CORE_APPROACH,TIER1_ENTERPRISE_VA_PLAN}.md`
