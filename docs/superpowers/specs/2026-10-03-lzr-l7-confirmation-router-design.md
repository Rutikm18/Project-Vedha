# LZR-derived L7 Confirmation Stage → Router — Design Spec

**Status:** Design / spec only. *This document changes no scanner code.* It
specifies a new collection-only pipeline stage and its integration with
`workflow/router.py`, to the level an implementer can build from. Grounded in the
real Vedha interfaces (`scanner/service_banner.py`, `workflow/router.py`,
`workflow/branches.py`, `workflow/asset.py`, `scanner/scanner_base.py::ScanResult`)
and in the LZR paper (Izhikevich et al., USENIX Security '21,
[arXiv:2301.04841](https://arxiv.org/abs/2301.04841); reference impl
[github.com/stanford-esrg/lzr](https://github.com/stanford-esrg/lzr)).

**Date:** 2026-10-03 · **Branch:** `claude/serene-bardeen-1uqxzq` ·
**Companion to:** Volume I §4 and Volume II §2 of the network-VA research.

---

## 1. Goal (one paragraph)

Replace *port-number / absence inference* in deep-scan routing with *positive L7
confirmation*: for every open TCP port, learn what protocol actually speaks there
(and whether anything speaks at all) in a bounded number of handshakes, then route
the correct deep scanner by **confirmed protocol**, not by the port number or by a
"nothing came back, so guess TLS" fallback. Simultaneously detect and suppress
**ACKing-firewall / HyperACKtive** false-open ports — middleboxes that SYN-ACK on
behalf of absent services and inflate the open-port count. All additions are
collection-only, unauthenticated, read-only.

**Measured target (from LZR):** identify **88%** of identifiable services in a
single packet, **99%** of *unexpected* services within **5 handshakes**; filter
the ~**40%** of SYN/ACK ports that never acknowledge L7 data and the ~**65%** of
apparently-identifiable "services" that are middlebox artifacts (HyperACKtive
filter removes **99.9%** of ACKing-firewall hosts).

---

## 2. Why — what is wrong today

Vedha's router (`workflow/router.py`) is already ahead of most scanners: it routes
by *observed banner content* (`looks_like_http/tls/db/ssh`) rather than purely by
port. But three weaknesses remain, all of which LZR's method addresses:

1. **Absence inference for TLS.** `looks_like_tls()` falls back to
   `banner_fact.get("banner") is None` — "an open port that returned nothing and
   isn't a known web port *probably* speaks TLS, and tls_scan is cheap to try." That
   is a *guess*. On a real estate it means speculative TLS handshakes against
   silent binary services, and — worse — it cannot tell a genuinely-silent service
   apart from a dead/filtered middlebox port.
2. **No middlebox / ACKing-firewall filter.** `port_scanner` reports a port OPEN on
   a completed TCP handshake. An ACKing firewall completes that handshake *on behalf
   of* a service that may not exist, then RSTs/stalls at L7. Today those ports are
   carried as open and routed to deep scanners, producing empty facts and inflated
   exposure counts. LZR shows this is not an edge case: a large share of apparent
   services are these artifacts.
3. **Limited positive protocol coverage.** `service_banner` sends only three probe
   shapes (`_HTTP_PROBE`, `_GENERIC_PROBE b"\r\n"`, and a TLS fallback). Protocols
   that speak-first (SSH, SMTP, FTP, many DBs) are caught; protocols that need the
   *right* first packet to volunteer a fingerprint (and those that emit a
   recognizable error to a *wrong* first packet) are under-covered, so
   product/version is often null (`usecases-networkva.md` SB-03/04 `✗`), which caps
   CVE accuracy downstream.

LZR's contribution is exactly a disciplined answer to all three: send the expected
protocol's first bytes, watch how the peer reacts, and use the *reaction class*
(acks data? sends L7 data? RSTs? zero-window?) to (a) filter non-services, (b)
filter middleboxes, and (c) fingerprint the real protocol — in ≤5 handshakes.

---

## 3. LZR mechanism (precise, as it will be adapted)

From the paper and reference implementation:

- **Data-on-ACK.** After the TCP SYN/ACK, LZR sends application-layer data (the
  expected protocol's first-packet handshake) *with the ACK*. `-pushDataOnly`
  attaches to PSH instead.
- **The non-acknowledging filter.** ~**40%** of hosts that send a SYN/ACK never
  acknowledge the data; none can complete an L7 handshake → **safely ignored**.
- **Response ladder.** If the peer returns *any* L7 data → fingerprint it and
  close (done, often in one packet: **8 of 30** protocols speak first, **+10**
  emit fingerprintable data in response to a *wrong* handshake → **16 of 30**
  identifiable in a single packet; **88%** of identifiable services in one packet).
  If the peer ACKs the data but sends nothing / advertises a **zero window** →
  keep the connection and escalate to the next candidate handshake. If it neither
  ACKs nor closes → **retransmit with PUSH**. Up to **5 handshakes** → **99%** of
  unexpected services.
- **HyperACKtive / ACKing-firewall filter (`-haf`).** Middleboxes SYN-ACK (and
  sometimes ACK data) for *every* port. LZR sends SYNs/data to **N random
  ephemeral ports** on the same host; if the host "answers" there too, it is marked
  as an ACKing firewall and its opens are discounted. This filters **99.9%** of such
  hosts and removes ~**65%** of the apparent-but-fake identifiable services.
  `-forceAllHandshakes` disables the HyperACKtive short-circuit.
- **30-protocol handshake library.** LZR ships per-protocol first-packet probes and
  response fingerprints (http, tls, ssh, and ~27 more).

---

## 4. Adapting LZR to Vedha's architecture (the key design decision)

LZR is a *stateless raw-packet* scanner (ZMap-class): it crafts the ACK+data itself.
Vedha is **unprivileged-connect-first** (`port_scanner` uses `connect()`;
`syn_scanner` uses raw packets only on Linux+`CAP_NET_RAW`, else falls back).
The LZR *concept* does not require raw packets — only the kernel-completed handshake
followed by an immediate, bounded, protocol-aware probe/response exchange. So:

- **Primary path — connect (unprivileged).** After a `connect()` succeeds (kernel
  did SYN→SYN/ACK→ACK), the stage immediately writes the candidate protocol's
  first bytes and reads with a short deadline. The "does it ack data" signal is
  obtained at the socket layer as: *did the peer return any bytes, or FIN/RST,
  within the deadline, versus accept the bytes and stay silent.* This reproduces
  LZR's three response classes without raw sockets. This is the path that runs on
  every platform and in `cap_drop ALL` containers.
- **Scale path — raw (optional, Linux+CAP_NET_RAW).** When `syn_scanner` is active,
  the same probe bytes can ride the ACK exactly as LZR does, giving the true
  single-packet efficiency at /16 scale. Same output schema, tagged
  `method="lzr_raw"` vs `method="lzr_connect"` so accuracy is measured per path
  (mirrors `syn_scanner`'s existing `method` tag).

**Placement.** A new stage **`l7_confirm`** runs in the funnel *after* `port_scan`
and *before/merged-with* `service_banner`, feeding `asset.services[port]` the
confirmed-protocol fields the router reads. Two implementation options:

- **Option A (recommended): a dedicated `scanner/l7_confirm.py` module** (a
  `BaseScanner`), reusing `service_banner`'s `match_service`/`parse_http_head` for
  fingerprinting. Rationale: it is independently measurable against ground truth
  (its own precision/recall), it is cache-keyable, and it keeps `service_banner`'s
  diff small. It supersedes the absence-inference in the router.
- **Option B: extend `service_banner.py`** with the probe ladder + ack-data signal.
  Smaller surface, but mixes two concerns (banner grab vs L7 confirmation) and makes
  the accuracy of each hard to isolate.

This spec describes **Option A**; §12 notes what changes if Option B is chosen.

---

## 5. Stage data model (new, backward-compatible fields)

`l7_confirm` writes a `ScanResult` per open port whose `data` carries:

| field | type | meaning |
|---|---|---|
| `l7_protocol` | str \| null | confirmed protocol (`http`,`tls`,`ssh`,`mysql`,`redis`,`smb`,`rdp`,…) or `null` if none spoke |
| `l7_confirmed` | bool | a positive L7 observation was made (not an inference) |
| `acks_data` | bool | peer accepted our probe bytes (TCP-level) |
| `l7_responded` | bool | peer returned application bytes |
| `probes_used` | int | handshakes spent (≤5) |
| `probe_ladder` | list[str] | which candidate probes were tried, in order |
| `ack_firewall` | bool | host flagged HyperACKtive (see §7) — **host-level** |
| `zero_window` | bool | peer advertised zero receive window (raw path only) |
| `evidence` | str | the bytes/first-line that identified the protocol (truncated) |
| `method` | str | `lzr_connect` \| `lzr_raw` |

These are **additive**: existing `service_banner` fields (`banner`, `first_line`,
`tls`, `tls_probed`, `service`) remain. `asset.services[port]` already merges
`r.data` (`asset.py` lines 160/245), so no Asset schema change is required — the new
keys simply appear alongside the old. `ack_firewall` is stored host-level (under the
null-port convention `branches.py` already uses for host-level facts).

---

## 6. The protocol probe ladder

The ladder is the heart of the stage: an ordered, bounded set of candidate
first-packet probes, chosen per port by likelihood (the nmap "rarity + probable
ports" idea, Volume II §5), capped at **5**. Each entry = {probe bytes, expected
response signature, confidence tier, which deep-scan branch it confirms}. The table
below is the *initial* ladder; it is data, extensible without engine changes, and it
deliberately reuses probes Vedha already sends.

| order | probe (first bytes) | positive signature | confirms → branch | tier |
|---|---|---|---|---|
| speak-first read | *(send nothing, read)* | `SSH-2.0` → ssh; `220 ` → ftp/smtp; `+OK`/`* OK` → pop/imap; RFB `RFB 00` → vnc; MySQL greeting; Postgres `E`/`R`; Redis on INFO | ssh/ftp/smtp/vnc/db | high (positive, first bytes) |
| 1 | `GET / HTTP/1.0\r\nHost: <t>\r\n\r\n` (reuse `_HTTP_PROBE`) | `HTTP/1.` or `HTTP/2` status line | web | high |
| 2 | TLS ClientHello (reuse `tls_scanner` ClientHello) | ServerHello / TLS alert record | tls | high |
| 3 | DB handshakes (reuse `db_scanner`: MySQL greeting read, Postgres startup, Redis `PING`, Mongo `isMaster`, MSSQL prelogin) | protocol-specific greeting/version | db | high |
| 4 | `\r\n` generic (reuse `_GENERIC_PROBE`) | any fingerprintable error (e.g. HTTP 400 `HTTP/1.x`, SMTP `500`, Redis `-ERR`) | web/db/generic | medium |
| 5 | protocol-specific binary (SMB2 negotiate, RDP X.224, SNMP is datagram → excluded here) | SMB2 `\xfeSMB`; RDP X.224 confirm | smb/rdp | high |

Ladder-ordering rules (per port):
- **Port hint first.** If the port is in a branch's `*_PORTS` table
  (`gates.py`), that branch's probe is tried **first** (so 443→TLS, 3306→MySQL,
  22→SSH-read) — the common case resolves in one packet.
- **Speak-first read is always probe 0** (free: costs no bytes out), matching LZR's
  "8/30 speak first."
- **Wrong-handshake fingerprint.** Even a *failed* probe is informative if the error
  is recognizable (LZR's "+10/30"): the classifier records those signatures too.
- **Stop on first high-confidence positive.** Medium-confidence (generic error)
  continues the ladder up to the 5-probe cap (`--version-all`-style exhaustion is a
  deep-mode option only).

The 5-probe cap and the per-port ordering are what bound cost; the budget is an
**intensity knob** (`workflow/intensity.py`): `light`→port-hint probe only (1),
`standard`→≤3, `deep`→≤5 + wrong-handshake fingerprinting.

---

## 7. The response-classification state machine

Per open port (pseudocode is **design-level**, not committed code):

```
confirm_port(target, port) -> dict:
    ladder = order_ladder(port)              # §6, bounded to intensity budget
    used = 0
    for probe in ladder:
        used += 1
        rsp = exchange(target, port, probe)  # connect→write probe→read(deadline)
        cls = classify(rsp)
        if cls.l7_data:                      # peer spoke application bytes
            proto = fingerprint(rsp.bytes)   # reuse match_service / parse_http_head
            return positive(proto, used, acks_data=True, l7_responded=True)
        if cls.rst or cls.closed:            # not a real L7 service on this port
            if used >= budget: break
            continue                         # try next candidate
        if cls.acked_no_data or cls.zero_window:
            retry_push_if_raw(rsp)           # LZR PUSH retransmit (raw path)
            if used >= budget: break
            continue
    # ladder exhausted with no L7 data:
    return negative(acks_data=any_ack, l7_responded=False, l7_protocol=None)
```

`classify(rsp)` buckets:
- **l7_data** — ≥1 application byte returned → fingerprint + stop (confidence high).
- **acked_no_data** — connect succeeded, probe accepted, deadline hit with no bytes
  (connect path) / data-ACK with zero app data (raw path).
- **zero_window** — raw path only: peer advertised win=0 (keep-alive, escalate).
- **rst / closed** — FIN/RST → not a service for this probe.
- **timeout** — no TCP progress → inherit `port_scanner`'s `filtered` semantics.

**HyperACKtive host filter (runs once per host, before trusting any open):**

```
detect_ack_firewall(target, sample_ports=5) -> bool:
    eph = choose_random_high_ports(sample_ports)   # ports NOT in the scan's open set
    hits = 0
    for p in eph:
        if connect(target, p) succeeds AND (probe_accepted OR l7_data):
            hits += 1
    return hits >= threshold        # e.g. >=2 of 5 "open" random ephemerals
```

If `ack_firewall` is true, every "open" port on that host is downgraded: it is kept
in the record but tagged `ack_firewall=True`, deep-scan routing is **suppressed**
unless a port returned *real L7 data* (which a middlebox cannot fake), and the
manager treats bare opens on that host as low-confidence. This is the single biggest
false-positive reduction (~65% of apparent services per LZR).

> **Scope invariant (critical).** The random ephemeral ports are still ports **on
> the authorized target IP**. They must pass `ScopeGuard` exactly like any probe.
> This is in-scope by construction (same host, the engagement authorizes the host),
> but the implementation MUST route them through the existing `ScopeGuard`
> allowlist and rate limiter — no exception path. Document this explicitly so a
> reviewer can verify the HyperACKtive probes cannot leave scope.

---

## 8. Router integration (`workflow/router.py`)

The router's job is unchanged (return `{port: {branches}}`); its *evidence source*
upgrades. Order of evidence becomes:

1. **Confirmed L7 protocol** (`fact["l7_confirmed"] and fact["l7_protocol"]`) →
   route to that protocol's branch directly. This is the new, strongest signal and
   is checked first in each `looks_like_*`.
2. Existing positive banner signals (`service`, `first_line`, `SSH-`, DB
   signatures) — unchanged, now corroborating.
3. **Absence inference is removed / demoted.** `looks_like_tls()`'s final
   `return banner_fact.get("banner") is None` is replaced by: if the port was
   L7-confirmed as *not* TLS → `False`; if confirmed TLS → `True`; only if the port
   was *never confirmed* (older probe build / `--no-l7-confirm`) does the legacy
   absence guess apply, behind a flag. This directly fixes the status-#3 class of
   speculative TLS handshakes against silent binary services.
4. **ACK-firewall suppression.** If `asset`'s host-level `ack_firewall` is true, a
   port with no `l7_responded` yields **no** branches.

Design-level diff shape (illustrative, not committed):

```python
def looks_like_tls(port, fact, host_ack_firewall=False):
    if fact is None: return False
    if host_ack_firewall and not fact.get("l7_responded"): return False
    if fact.get("l7_confirmed"):
        return fact.get("l7_protocol") == "tls"      # authoritative
    if fact.get("tls") or fact.get("service") == "tls": return True
    if fact.get("tls_probed"): return False
    if port in _CLIENT_FIRST: return False
    return fact.get("banner") is None                 # legacy guess, now last resort
```

`route_branches()` gains a host-level `ack_firewall` read and passes it to each
`looks_like_*`. `branches.py` is unchanged — the same `dynamic="tls|web|db|ssh"`
keys receive better-qualified ports. (Extending dynamic routing to more branches —
ssh already; add rdp/smb/smtp/ftp/vnc from `l7_protocol` — is a follow-on, since
the confirmation now produces those labels.)

---

## 9. Workflow wiring

- **Funnel order:** `host_discovery → port_scan → l7_confirm → service_banner →
  route_branches → deep branches`. `l7_confirm` consumes the open-port set and
  writes `asset.services`; `service_banner` still runs (banner/version capture) but
  no longer needs its TLS-absence fallback for routing.
- **Gating:** add an `l7_confirm` gate analogous to the existing gates — skip on the
  `ot` passive profile (hard), skip ports already deep-confirmed by cache.
- **Caching:** cache key `(host_id, port, "l7_confirm")` with the same
  `force_recheck_after` TTL the other branches use (`workflow/cache.py` +
  `_split_cached`), so a re-scan reuses a stable confirmation.
- **Intensity:** probe budget per §6 from `intensity.py` (`light`/`standard`/`deep`
  → 1/3/5 probes; `deep` also enables wrong-handshake fingerprinting and the raw
  path when available).
- **Two-tree parity:** the module and its wiring must be **byte-identical** in
  `scanner/` and `main_scripts/` (enforced by `tests/test_two_tree_parity.py`), and
  wired in `run_all` + `scan_funnel` + `workflow` (enforced by the tier-1 wiring
  gate) — same discipline as every other scanner.

---

## 10. Collection-only / safety invariants (must hold)

- **Read-only, benign probes.** Every ladder probe is a normal client first-packet
  (HTTP GET, TLS ClientHello, protocol greeting read). No auth, no credential, no
  payload that changes target state, no exploitation. Identical posture to
  `service_banner`/`db_scanner` today.
- **Scope.** All probes — including HyperACKtive random-ephemeral probes — go
  through `ScopeGuard` and the rate limiter. No bypass path. (See §7 box.)
- **No new outbound reach.** Probes target only the engagement's authorized host:port
  space. The random ephemeral ports are on the same authorized host.
- **OT.** `l7_confirm` is active probing → structurally excluded from the `ot`
  profile (same gate-0 guarantee as every active scanner).
- **Fail-closed.** On any ambiguity the stage records `l7_protocol=null,
  l7_confirmed=false` and lets the legacy path decide — it never *fabricates* a
  protocol.

---

## 11. Accuracy validation plan (the gate that lets us claim numbers)

The stage is distrusted until measured (`accuracy.py` / `accuracy_gate.py`):

- **Corpus:** build an independently-labelled ground-truth corpus (service on an
  expected port, service on an *unexpected* port, a dead/filtered port, and a
  simulated ACK-firewall host) — labels from an independent observer (nmap `-sV`
  from the same vantage, hand verification), `provenance: ground_truth`.
- **Metrics:**
  - *Protocol-ID precision/recall* per protocol (did `l7_protocol` match truth).
  - *Open-port FP reduction*: opens suppressed by the ACK-firewall filter that were
    truly fake vs truly real (must not suppress real services).
  - *Probes-to-identify* distribution (target: median 1, ≤5 at p99).
  - *Per-method* (`lzr_connect` vs `lzr_raw`) scored separately.
- **Thresholds (initial, from LZR, tune on corpus):** single-packet identify ≥ 0.85
  of identifiable; ≤5-packet identify ≥ 0.95 of unexpected; ACK-firewall
  real-service suppression rate = 0 (never suppress a port that returned real L7
  data). The `accuracy_gate` fails a change that regresses these.
- **Promotion:** ships `coming_soon`; promoted to enabled only after the gate passes
  on the ground-truth corpus **and** a live-target verification run — the exact
  policy already used for the other use-cases.

---

## 12. Test plan

- **Unit (no network, monkeypatched exchange):** `classify()` buckets for each
  response shape; ladder ordering by port hint + intensity budget; `fingerprint()`
  reuse of `match_service`/`parse_http_head`; the 5-probe cap; the HyperACKtive
  threshold logic with a fake that "answers" random ephemerals.
- **Ground-truth (live socket):** against a local multi-service rig (an HTTP, a TLS,
  an SSH-on-2222, a Redis-on-6380, a dead port, and a mock ACKing responder) →
  assert `l7_protocol` correctness and FP suppression.
- **Router tests:** `looks_like_*` now prefers `l7_confirmed`; absence guess only
  fires without confirmation; `ack_firewall` suppresses bare opens. Extend the
  existing router unit tests.
- **Parity:** `test_two_tree_parity.py` (byte-identical mirror) and the tier-1
  wiring gate (no half-wired branch).
- **Scope:** a test asserting HyperACKtive ephemeral probes are refused by
  `ScopeGuard` when the host is out of scope (proves no bypass).

If **Option B** (extend `service_banner`) is chosen instead: the probe ladder +
ack-data signal fold into `ServiceBannerScanner.scan_target`, the new fields attach
to the existing banner fact, and the router change is identical — but the accuracy
corpus can no longer isolate confirmation from banner-grab, so Option A is
preferred for measurability.

---

## 13. Rollout & sequencing

1. **Module + unit tests** (`l7_confirm.py`, both trees) — classify + ladder +
   HyperACKtive, no wiring yet. *Collection-only, fully offline-testable.*
2. **Funnel wiring + cache + intensity** — stage runs, writes `asset.services`,
   emits `ScanResult`s; `coming_soon`, not yet feeding the router.
3. **Router integration** — `looks_like_*` prefer `l7_confirmed`; absence guess
   behind a flag; `ack_firewall` suppression. Router tests.
4. **Ground-truth corpus + accuracy gate thresholds** — measure; iterate the ladder.
5. **Raw path** (`lzr_raw` via `syn_scanner` integration) — optional, Linux+root, for
   scale; same schema + `method` tag.
6. **Promote** to enabled per protocol as the corpus proves each.

Each step is independently shippable and leaves the pipeline green (the stage is a
no-op for routing until step 3, and router behaviour is flag-guarded).

---

## 14. Risks & mitigations

| Risk | Mitigation |
|---|---|
| A probe perturbs a fragile service | Probes are standard client first-packets; `ot` excluded; rate-limited; same posture as today's banner grab |
| HyperACKtive probes look like scanning noise | Bounded (≤5 ephemerals/host), rate-limited, in-scope; documented; disable-able (`--no-haf`) |
| Suppressing a *real* service as middlebox FP | Never suppress a port that returned real L7 data; gate threshold enforces zero real-service suppression |
| Added latency per host | Budgeted by intensity (1/3/5 probes); port-hint-first resolves the common case in one packet; cached across re-scans |
| Raw path unavailable (non-Linux / no CAP_NET_RAW) | Connect path is primary and complete; raw is a scale optimization only |
| Ladder drift between trees | `test_two_tree_parity.py` byte-identical guard |

---

## 15. Decisions for the owner

1. **Option A (dedicated module) vs B (extend service_banner).** Spec recommends A
   for measurability. *Decision needed.*
2. **HyperACKtive default on or off** for standard intensity. Recommend **on** at
   standard+ (it is the biggest FP win) and off at `light`.
3. **Random-ephemeral count** (default 5 per LZR) and the "is-firewall" threshold
   (recommend ≥2/5).
4. **Keep the legacy TLS absence-guess** behind `--legacy-tls-guess` for probes
   without the confirmation stage, or remove it once the stage is universal.
5. **Raw path priority** — build now for scale, or defer until external/large-subnet
   scanning is on the roadmap.

---

## 16. Sources

- LZR — Izhikevich et al., USENIX Security '21 (arXiv:2301.04841): https://arxiv.org/abs/2301.04841 · ref impl: https://github.com/stanford-esrg/lzr
- Vedha code: `workflow/router.py`, `workflow/branches.py`, `workflow/asset.py`,
  `scanner/service_banner.py`, `scanner/db_scanner.py`, `scanner/tls_scanner.py`,
  `scanner/scanner_base.py` (ScanResult), `workflow/{gates,intensity,cache}.py`,
  `tests/test_two_tree_parity.py`, `scanner/accuracy.py`, `scanner/accuracy_gate.py`
- Volume I §4 and Volume II §2: `docs/research/2026-10-03-network-va-*.md`
