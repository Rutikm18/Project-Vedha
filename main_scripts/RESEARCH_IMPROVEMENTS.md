# main_scripts — Accuracy Research & Improvement Plan

**Author:** engineering review (Claude, Opus 4.8), 2026-08-15
**Scope:** the 34 scanner modules under `probe/main_scripts/` (~10,400 LoC).
**Goal (user):** make these scripts best-in-class and give *accurate, expected*
results. This is the project's core collection layer.
**Method:** full read of the accuracy-critical core (scanner_base, port_scanner,
syn_scanner, tls_scanner, host_discovery, service_banner, os_fingerprint,
accuracy) + targeted review of the protocol scanners, benchmarked against how
top-class tools solve the same problems (nmap, masscan, ZMap, RustScan/naabu,
p0f, testssl.sh, FoxIO JA4+).

---

## 0. Honest overall assessment

This code is **already well above typical scanner quality.** It gets the hard,
often-skipped things right:

- A canonical nmap-style state model — `open / closed / filtered / open|filtered
  / unreachable / error` — with `state` and `reason` always separate
  (`scanner_base.py:49-95`).
- An **errno→state classifier** so a scanner-side failure (fd exhaustion, no
  route) is never mislabeled as a target "filtered" (`scanner_base.py:70-111`) —
  a subtle correctness win most scanners miss.
- **Set-based completeness** metrics that can't be fooled by a skip+dup pair, so
  a clean-empty result is provably distinct from a degraded one
  (`port_scanner.py:152-247`).
- **Retransmit-on-silence** for the connect path — directly attacks
  scanner-manufactured false negatives (`port_scanner.py:346-364`).
- **Graded-confidence host discovery** fusing TCP endpoint evidence with kernel
  NUD neighbor freshness — a genuinely sophisticated design
  (`host_discovery.py:304-385`).
- **Stateless SYN cookies** (masscan technique) with reply validation
  (`syn_scanner.py:131-147`).
- Correct hand-crafted UDP protocol payloads (SNMP BER, NTP monlist, SSDP, mDNS)
  and honest tri-state UDP with ICMP-unreachable detection
  (`scanner_base.py:516-564`, `udp_scanner.py`).
- Confidence that is **capped by corroboration** and never claims 1.0 from a
  single spoofable signal (`os_fingerprint.py:171-182`).

So the work below is **not** "rewrite this." It is three things, in order:
1. **Wire the sophistication that already exists into the main path** (it's
   built but disconnected — highest ROI).
2. **Arm the accuracy harness with real ground truth** (it can't currently
   *measure* accuracy, only claim it).
3. **Close depth gaps** versus nmap-class tools (service/OS identification).

---

## TIER 1 — Highest ROI: connect the tools you already built

These are the biggest accuracy wins because the hard code already exists and is
simply **not wired into the primary TCP scan path.** Verified by grep:
`AdaptiveRateController` is used only by `udp_scanner`; `AdaptiveTimeout` is used
by *nobody*; `accuracy.py` is imported by *nobody* in the pipeline.

### 1.1 — Wire `AdaptiveTimeout` (SRTT/RTTVAR) into the TCP scanners  ★★★
- **Now:** `port_scanner`/`syn_scanner` use a **fixed** `self.timeout` (default
  3.0s, `scanner_base.py:735`). `adaptive_timeout.py` implements the exact
  Jacobson/Karels SRTT+RTTVAR estimator nmap uses for its RTO (RFC 6298) — and
  **nothing imports it.**
- **Why it hurts accuracy:** a fixed 3s is wrong in *both* directions. On a LAN
  it's ~100× too long (slow, and lets one slow host stall a worker). On a
  high-latency WAN/VPN it's too short → real services time out → **false
  `filtered`**. This is precisely the "results not as expected" failure mode.
- **Fix:** per-host `AdaptiveTimeout`. Seed it from the RTT the connect scan
  *already measures* (`port_scanner.py:307 rtt_ms`) and from `host_discovery`'s
  probe RTTs; use `timeout()` per port instead of the constant. nmap calls this
  its single most important timing lever.
- **Effort:** small (the estimator is done; wire `observe()`/`timeout()` into
  `_attempt`). **Impact:** large (fewer false filtered + faster).

### 1.2 — Wire `AdaptiveRateController` (AIMD) into the TCP paths  ★★★
- **Now:** TCP `port_scanner`/`syn_scanner` pace with the fixed `RateLimiter`
  (constant token bucket). The AIMD congestion controller
  (`scanner_base.py:330-393`) — which grows in-flight while replies arrive and
  multiplicatively backs off on loss, the ZMap/masscan approach to RFC-1812 ICMP
  rate limits — is used **only by `udp_scanner`.**
- **Why it hurts accuracy:** when a target or path starts dropping SYNs (its own
  ICMP error budget is saturated), a constant rate keeps hammering → more drops
  → more **false `filtered`**. AIMD detects the loss signal and slows down,
  *raising* recall.
- **Fix:** gate the TCP per-port probes through `AdaptiveRateController.acquire()`
  + `report_success/loss()`; treat `no_response`-after-retries as loss.
- **Effort:** medium. **Impact:** large under load / on fragile networks.

### 1.3 — Arm `accuracy.py` with a real ground-truth corpus  ★★★
- **Now:** `accuracy.py` computes precision/recall/F1 and OPEN precision/recall
  against a labeled corpus — the right instrument. But there is **no corpus**
  (find for `*corpus*/*ground*truth*/*fixture*` = nothing) and nothing in the
  pipeline calls it. The "credibility moat" (its own docstring) is **unbuilt**;
  accuracy is asserted, never measured.
- **Fix:**
  1. Stand up a **known-truth lab** (a handful of hosts/containers with an
     *independently verified* remote state map: which ports are truly
     open/closed/filtered *from the scanner's vantage*, and which services/
     versions run). Note the discipline the file already calls out: ground truth
     must be **remote-validated**, not a local `ss -ltn` listener list
     (`accuracy.py:14-18`).
  2. Freeze that as a JSON corpus; run `accuracy.py` in CI on every scanner
     change and gate merges on precision/recall thresholds.
  3. In the field, build a rolling corpus from a second probe (the
     `vantage_matrix` already models multi-vantage) as the independent validator.
- **Effort:** medium (mostly lab + labeling). **Impact:** this is what *proves*
  "accurate and expected results" instead of claiming it — and it will surface
  the real FP/FN hotspots to fix next.

---

## TIER 2 — SYN scanner accuracy asymmetry (fast path is the weak path)

The connect scanner is careful; the *faster* SYN path is not — so switching to
SYN (which the engine does above 1024 ports, `engine.py:_SYN_PORT_THRESHOLD`)
currently **trades accuracy for speed** in ways masscan/ZMap do not.

### 2.1 — SYN path has NO retransmit on silence  ★★★
- **Now:** `_syn_scan_blocking` sends exactly one SYN per port and collects
  within one deadline (`syn_scanner.py:255-304`). A single dropped SYN or SYN/ACK
  → permanent **false `filtered`**. Meanwhile the *connect* path retransmits on
  silence (`port_scanner.py:346-364`). So the fast path has *more* false
  negatives than the slow one — backwards.
- **Reference:** masscan `--retries` (default 1) sends multiple rounds spaced in
  time; ZMap resends the probe cohort.
- **Fix:** after the first collection window, re-SYN only the still-silent ports
  for N bounded rounds; first definitive SYN-ACK/RST wins. Mirror the connect
  path's "retry silence only, never a definitive answer" rule.

### 2.2 — SYN sends are unpaced (burst → self-inflicted drops)  ★★
- **Now:** the send loop blasts every SYN as fast as the CPU allows
  (`syn_scanner.py:256-262`); `limiter.wait()` is called once *before* the whole
  target, not per packet. A `/24 × top1000` is a multi-thousand-packet burst that
  trips RFC-1812 ICMP rate limits and switch buffers → drops → false filtered.
- **Fix:** pace sends through the (now-wired, 1.2) AIMD controller or the rate
  limiter; this is the core of why masscan is both fast *and* accurate.

### 2.3 — SYN receive busy-polls and can miss replies  ★★
- **Now:** the recv loop does non-blocking `recv` + `time.sleep(0.005)`
  (`syn_scanner.py:267-273`). Under reply bursts this can drop packets between
  sleeps and wastes CPU.
- **Fix:** `select`/`epoll` on `recv_sock` with the remaining deadline as the
  timeout — event-driven, no polling, no missed replies.

### 2.4 — SYN path is IPv4-only  ★
- Documented (`syn_scanner.py:240-242`) and it falls back, but a dual-stack
  estate silently gets connect-scanned over v6. Acceptable now; note for later.

---

## TIER 3 — Identification depth (accuracy of *what*, not just *open*)

### 3.1 — Service/version matching is ~25 patterns vs nmap's ~12,000  ★★★
- **Now:** `service_banner._PATTERNS` has ~25 soft-match regexes
  (`service_banner.py:43-79`). nmap-service-probes ships ~12,000 match lines.
  Great coverage of the top services; everything else returns a raw banner with
  no `service/product/version`.
- **Fix (choose one, incremental):**
  - Adopt a **curated subset** of nmap-service-probes (it's a documented text
    DB) for the top ~200 services — biggest single lever for "what is this."
  - Add the missing **probe rungs** the ladder lacks (e.g. TLS-wrapped probe,
    see 3.2; a few more DB/appliance greetings).
- **Also:** `_CLIENT_FIRST` lists 443/8443 (`service_banner.py:32`) but the
  scanner sends a **plaintext** `GET` there — an HTTPS server returns nothing, so
  443 gets `open, no banner`. Either exclude TLS ports here (they're covered by
  `tls_scanner`+`web_scanner`) or add a TLS-wrap rung so the banner grabber IDs
  HTTPS servers too.

### 3.2 — OS fingerprint is TTL-only; the TCP-hint plumbing is dead  ★★
- **Now:** `fingerprint_os` accepts `tcp_window`/`mss` hints
  (`os_fingerprint.py:127-182`), but **no TCP scanner harvests them** (grep for
  `tcp_window|TCP_INFO|getsockopt` in port/syn/funnel = nothing), and
  `scan_funnel` never chains window hints into `os_fingerprint`. So OS ID runs on
  TTL alone → only 3 coarse families.
- **Reference:** p0f signatures (TTL + window + options order + MSS + DF) give
  OS/version with no extra packets; nmap's 16-probe stack FP is the gold standal
  but needs raw sockets.
- **Fix (cheap → strong):**
  1. Harvest the peer **TCP window** (and MSS via `TCP_MAXSEG`/`TCP_INFO` on
     Linux) in the connect scan and pass it as the `tcp_hints` os_fingerprint
     already expects. That alone lifts OS ID from 3 families to p0f-class on
     Linux without a single extra packet.
  2. On the raw SYN path, capture the SYN/ACK's window + options ordering for a
     p0f-style signature match.

### 3.3 — Default port set is too thin for discovery  ★★
- **Now:** `BaseScanner`/`TOP_TCP_PORTS` = **35 ports** (`scanner_base.py:605`),
  and `port_scanner` defaults to that when no `-p` is given
  (`port_scanner.py:260`). A default discovery that only looks at 35 ports will
  *miss real services* → "results not as expected."
- **Fix:** default to **top100** (already defined, `port_scanner.py:108-117`) for
  a no-arg scan; keep `quick`(15) as an explicit fast mode. Cheap, immediate
  recall win.

---

## TIER 4 — Robustness / correctness (lower severity)

### 4.1 — `resolve()` uses only `getaddrinfo()[0]`  ★
- `scanner_base.py:460-472` takes the first result. A dual-stack host whose v6 is
  returned first but is unreachable won't fall back to v4. **Fix:** iterate
  `infos` and try each family until one connects (nmap does this).

### 4.2 — `RateLimiter` serializes all tasks through one lock  ★
- `scanner_base.py:294-310` — a single `_next` under one asyncio lock. Fine at
  200/s; at high rates the lock is the bottleneck. Superseded once AIMD (1.2) is
  the pacing authority.

### 4.3 — `expand_targets` materializes the full host list (≤200k)  ★
- `scanner_base.py:399-457` builds the whole list in memory. The sliding window
  bounds *tasks*, not the list. For big ranges route through `mass_scan` (already
  the documented guidance) or make it a generator.

### 4.4 — SMB/DB/SMB2 raw framing fragility  ★
- `smb_scanner.py` hand-rolls SMBv1/SMB2 negotiate framing (its own docstring
  flags this as fiddly). Correct today; add negative/edge fixtures to the corpus
  (Tier 1.3) so a framing regression is caught by measured recall, not in the
  field.

---

## Prioritized roadmap (do in this order)

| # | Change | File(s) | Effort | Accuracy impact | Status |
|---|--------|---------|:------:|:---------------:|:------:|
| 1 | Wire `AdaptiveTimeout` into TCP scan | adaptive_timeout, port_scanner | S | ★★★ | ✅ done (2026-08-15) |
| 2 | SYN retransmit on silence | syn_scanner | S | ★★★ | ✅ done (2026-08-15) |
| 3 | Default no-arg scan → top100 | port_scanner, syn_scanner | XS | ★★ | ✅ done (2026-08-15) |
| 4 | Stand up ground-truth corpus + run `accuracy.py` in CI | new corpus, CI | M | ★★★ (measures everything) | next |
| 5 | Wire AIMD into TCP paths + pace SYN sends | scanner_base, port_scanner, syn_scanner | M | ★★★ | |
| 6 | Harvest TCP window/MSS → feed os_fingerprint | port_scanner, scan_funnel, os_fingerprint | M | ★★ | |
| 7 | Expand service-ID patterns (nmap-service-probes subset) + TLS-wrap rung | service_banner | M/L | ★★★ (what-is-this) | |
| 8 | `select`/epoll SYN receive | syn_scanner | S | ★★ | |
| 9 | `resolve()` multi-family fallback | scanner_base | XS | ★ | |

### Progress log
- **2026-08-15 — items 1–3 shipped.** `port_scanner`: per-host `AdaptiveTimeout`
  (SRTT+4·RTTVAR, fed by completed-handshake/RST RTTs; `--fixed-timeout` opts
  out) + default port set now nmap top-100. `syn_scanner`: retransmit-on-silence
  (`retries`, default 2 — silent ports only, SYN-ACK/RST ends a port early) +
  top-100 default. Synced to `scanner/`. New proof tests: adaptive estimator
  shares+adapts, `--fixed-timeout` disables it, top-100 defaults, SYN silent
  ports retried N+1×, answered ports sent once. Full suite 921 green.

**Sequencing rationale:** #1–3 are small, high-impact, and independently
shippable. **#4 comes early on purpose** — once accuracy is *measured* against
real ground truth, it tells you exactly which of #5–9 move the FP/FN numbers most
for *your* environment, so the rest is data-driven instead of guessed.

---

## Appendix — top-class references mapped to each area

- **Port state model & retransmit:** nmap (host/port state machine, RTT-based
  retransmit), masscan `--retries`.
- **Rate/congestion:** ZMap & masscan (send-rate as first-class; AIMD-style
  backoff to respect RFC-1812 ICMP limits).
- **Adaptive timeout:** nmap timing (SRTT/RTTVAR RTO), RFC 6298.
- **Service/version ID:** nmap-service-probes (the reference match DB).
- **OS fingerprint:** p0f (passive TTL+window+options signatures), nmap OS FP
  (active 16-probe stack).
- **TLS posture & JA4:** testssl.sh (protocol/cipher grading), FoxIO JA4+ (JA4S
  server + JA4X cert fingerprints — already implemented here).
- **Host discovery:** nmap `-PE/-PS/-PA/-PR` fused liveness (this module's
  TCP+neighbor fusion is the unprivileged analog, done well).
