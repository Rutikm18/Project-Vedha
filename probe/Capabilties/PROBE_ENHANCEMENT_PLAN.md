# Probe Enhancement & Optimization Plan

> **Purpose:** A grounded, prioritized roadmap for making the Vedha probe faster, more
> accurate, and more complete — building everything from core protocol logic, no
> dependency on nmap/masscan/etc. Every item below references the *actual* current
> state of the code and states the target, the technique, and the tradeoff.

**Status legend:** ✅ done · 🟡 partial · ❌ missing
**Effort:** S (hours) · M (1–2 days) · L (multi-day)

---

## 0. Current state (honest baseline)

| Scanner | Covers | Gap |
|---|---|---|
| `port_scanner.py` | TCP **connect** scan (asyncio) | 🟡 full 3-way handshake per port — slow, logged, no SYN/stateless |
| `host_discovery.py` | TCP probe + ARP fusion, OUI, MAC-random | 🟡 no ICMP echo/timestamp, no TTL fingerprint, no OS guess |
| `service_banner.py` | banner grab (speak/client-first) | 🟡 no probe-ladder (nmap-style intensity), no soft-match |
| `web_scanner.py` | HTTP fingerprint, headers, OPTIONS | ❌ no route discovery, JWT, injection surface, favicon hash |
| `tls_scanner.py` | per-version handshake, cert parse | 🟡 negotiated cipher only, no full cipher enum, no JARM |
| `snmp_scanner.py` | ✅ full MIB walk + amplification + v3 | — |
| `udp_scanner.py` | ✅ 12 ports incl. IKE/SIP/TFTP/IPMI | 🟡 **blocking sockets in thread pool** (not true async) |
| `db_scanner.py` | 6 DB wire protocols | 🟡 no auth-required-vs-present classification for all |
| `smb_scanner.py` | dialect / SMBv1 | 🟡 no signing-required, null-session, MS17-010 tell |
| `mcp_ai_scanner.py` | MCP/AI discovery | 🟡 **blocking `urllib`** — serializes the loop |
| `passive_collector.py` | listen-only OT/broadcast | 🟡 no active-safe OT probes (Modbus/EIP/BACnet) |
| `iot_scanner.py` | ✅ SSDP/mDNS/RTSP/MQTT/CoAP/TR-069 | — |
| `delta_scanner.py` | ✅ rescan/delta engine | — |
| `mobile_scanner.py` | ✅ ADB/iOS/mDNS | — |
| `detection_engine/` | version→CVE, EPSS/KEV, AI-normalize | 🟡 scanner→detection handoff is manual |

**The three structural weaknesses** (biggest leverage, fix first):
1. **Scan engine is connect-only + thread-pool UDP** → speed and stealth ceiling.
2. **No per-host funnel orchestration** → scanners re-probe the same host independently.
3. **Fingerprinting is shallow** → OS, JARM, full-cipher, favicon all missing → weaker asset ID and correlation.

---

## Tier 1 — Scan engine core *(highest leverage)*

### 1.1 Stateless SYN scan (half-open) — **L** — ✅ DONE
- **Done:** `scanner/syn_scanner.py` — hand-built IPv4+TCP SYN with one's-complement checksums, raw `SOCK_RAW`/`IP_HDRINCL` send + `IPPROTO_TCP` raw recv. **Stateless**: the ISN is a keyed HMAC-SHA256 "SYN cookie" over `(dst_ip, dst_port, src_port)`; a genuine SYN/ACK's `ack-1` must recompute to that cookie, so replies validate with zero per-probe state and stray/forged packets are rejected. Classification: SYN/ACK→open, RST→closed, silence→filtered.
- **Fallback:** `syn_scan_supported()` gates on **Linux + a usable raw socket** (BSD/macOS raw sockets can't receive TCP, so the SYN path is Linux-only in practice); otherwise `SynScanner` transparently delegates to the connect scan. Results carry `data["method"] = "syn" | "connect_fallback"` so each path's accuracy is measurable. Also degrades gracefully if privileges drop mid-run.
- **Wired in:** `build_default_funnel()`'s port stage is now `SynScanner` — production Linux gets the SYN upgrade automatically; dev/unprivileged is unchanged.
- **Tests:** `tests/test_syn_scanner.py` (checksums, cookie, packet round-trip, flag classification, capability/fallback decision, real-loopback fallback open-detection).
- **Tradeoff/limit:** IPv4-only raw path (v6 targets take the fallback); the raw send/recv layer is not unit-tested on macOS (can't be) — its pure components are fully covered and it runs on prod Linux.

### 1.2 True async UDP — **M** — ✅ DONE
- **Was:** `udp_scanner.py` ran blocking `socket.recvfrom` inside `run_in_executor` — throughput capped by the thread pool, not the network.
- **Done:** added `async_udp_probe` + `_UDPProbeProtocol` (`asyncio.DatagramProtocol`) to `scanner_base.py`; `udp_scanner.py` now probes fully on the event loop. Bonus: **tri-state accuracy** — `error_received(ConnectionRefusedError)` (ICMP port-unreachable) now yields a definitive `closed` status, distinct from the timeout `filtered` (resolves playbook 11's open|filtered ambiguity where the OS tells us).
- **Tests:** `tests/test_async_udp.py` (real loopback echo/sink servers, concurrency, tri-state).

### 1.3 Adaptive congestion / ICMP-rate handling — **M** — ✅ DONE
- **Done (retransmit):** `async_udp_probe_retry` in `scanner_base.py` + `UDPScanner(max_retries=2, ...)` and CLI `--max-retries`. Returns on the first *definitive* result (reply=open, ICMP-unreachable=closed) and retries only on silence — so a lossy UDP drop or an RFC-1812 rate-limited ICMP-unreachable gets another chance instead of being mislabelled `open|filtered`.
- **Done (congestion control):** `AdaptiveRateController` in `scanner_base.py` — AIMD in-flight window (TCP-style slow-start → congestion-avoidance, halve-on-loss, bounded [min,max]). `UDPScanner(adaptive=True)` / CLI `--adaptive` swaps the fixed semaphore for this window, so it self-tunes to loss and a host's ICMP-error rate limit instead of a constant token bucket.
- **Tests:** `tests/test_adaptive_rate.py` (window state machine, async gating, retransmit call-counts incl. dropped-reply recovery, adaptive UDPScanner on real loopback).
- **Win realised:** `open|filtered` now resolves to `closed` far more reliably (verified on loopback), fragile hosts aren't hammered, and throughput self-adjusts per network.

### 1.4 Per-host scan funnel orchestrator — **M** — ✅ DONE
- **Was:** each scanner invoked independently, re-deriving liveness/open-ports.
- **Done:** `scanner/scan_funnel.py` — `ScanFunnel` runs **discovery → port scan → routed deep scanners** per host. A dead host is never port-scanned (unless `--force`); each deep scanner is constructed scoped to *only* the open ports routed to it (`DEFAULT_PORT_ROUTES`: tls/db/smb/web/ai), so it can't re-probe the whole host. Dependency-injected factories make the gating/routing unit-testable; `build_default_funnel()` wires the real scanners; optional `--with-udp`.
- **Tests:** `tests/test_scan_funnel.py` (routing, dead-host gating, open-port scoping, aggregation, real-scanner wiring).
- **Note:** used per-host `asyncio.Semaphore` for host-level concurrency; a single *global* budget shared with each scanner's internal fan-out is a further optimization (ties into 1.3).

---

## Tier 2 — Accuracy & fingerprinting — ✅ COMPLETE

### 2.1 Active OS fingerprinting — **M** — ✅ DONE
- `scanner/os_fingerprint.py`: `fingerprint_os(ttl, tcp_window, mss)` — multi-signal scoring (initial TTL rounded to 64/128/255 → Linux/Windows/Network, plus OS-typical TCP windows) → OS-family guess + confidence + hop estimate. Consumes TCP hints from prior SYN/connect results.
- **Tests:** `tests/test_os_fingerprint.py` (TTL inference, family mapping, multi-signal scoring).

### 2.2 ICMP multi-probe discovery + TTL harvest — **S/M** — ✅ DONE
- `os_fingerprint.py`: ICMP echo/timestamp/address-mask builders (+ checksum), reply parser that harvests TTL from the IP header (raw) or copes without it (datagram-ICMP). `OSFingerprintScanner` sends an echo, harvests TTL, infers OS; uses unprivileged datagram-ICMP where possible (macOS/ping-perms), raw otherwise, and degrades to TCP-hint-only when neither is available.
- **Win:** finds hosts that drop TCP but answer ICMP; feeds OS guess + delta identity.

### 2.3 JARM active TLS fingerprint — **M** — ✅ DONE
- `scanner/tls_fingerprint.py`: raw ClientHello builder (SNI, cipher list/order, GREASE, ALPN, supported_versions, key_share) + ServerHello parser (negotiated version/cipher/extensions) + JARM-shaped 62-char digest (10×3 cipher/version codes + 32-char SHA-256 of stable ServerHello extension *types* — not the ephemeral key_share). Verified against a live loopback TLS server: crafted ClientHello accepted, ServerHello parsed, fingerprint non-zero and deterministic.
- **Win:** stable host-identity signal for `delta_scanner` on internet hosts without MAC. *(Caveat: JARM-methodology; validate byte-parity vs the reference tool before cross-database matching.)*
- **Tests:** `tests/test_tls_fingerprint.py` + live check in `tests/test_tls_integration.py`.

### 2.4 Full cipher-suite & TLS posture enumeration — **S/M** — ✅ DONE
- `tls_scanner.py`: `classify_cipher()` (PFS/AEAD/CBC + weak flags: RC4/NULL/DES/3DES/EXPORT/MD5/anon) and `grade_tls_posture()` (A/B/C/F from protocols + ciphers). The scan now emits `cipher_analysis` + `posture{grade,findings}`; evidence leads with the grade. Verified live against a loopback TLS server.
- **Win:** real "weak crypto / deprecated protocol" findings, not just version facts.
- **Tests:** `tests/test_tls_posture.py` + live check in `tests/test_tls_integration.py`.

### 2.5 Service-probe ladder + soft-match — **M** — ✅ DONE
- `service_banner.py`: `PROBE_LADDER` (read-only NULL rung → HTTP → generic, escalating only when unmatched so speak-first services still cost one connection) + `match_service()` regex table → `{service, product, version}` on bytes (text banners *and* binary handshakes like MySQL). Results now carry service/product/version and the matching rung.
- **Win:** identifies services on non-standard ports and silent-until-spoken services.
- **Tests:** `tests/test_service_match.py` (incl. loopback: SSH identified on a non-standard port).

---

## Tier 3 — Coverage completion (from playbooks)

### 3.1 OT active-safe probes (opt-in) — **M** *(Playbook 06)*
- `passive_collector.py` is listen-only. Add **explicitly opt-in, gentle** identity reads: Modbus FC43 Read Device ID, EtherNet/IP List Identity, BACnet Who-Is, S7comm ID. Hard-gated behind a flag; safety > availability.
- **Win:** inventories PLCs/RTUs that never broadcast.

### 3.2 LDAP scanner — **S/M** *(Playbook 05)*
- New `ldap_scanner.py`: anonymous bind + rootDSE read (naming contexts, DC/forest/domain functional level, supported SASL). Non-intrusive.
- **Win:** AD recon finding; complements `smb_scanner`.

### 3.3 SMB depth — **M** *(Playbook 05)*
- Extend `smb_scanner.py`: SMB2 signing-required flag, null-session enumeration, MS17-010 (EternalBlue) safe tell, SMBGhost (CVE-2020-0796) compression flag.

### 3.4 Web app triage depth — **L** *(Playbook 10)*
- `web_scanner.py` is fingerprint-only. Add: content/route discovery (curated wordlist), parameter discovery, `robots.txt`/sitemap/swagger/`.git`/`.env` exposure, **JWT decode + `alg:none`/weak-HMAC/RS256→HS256 checks**, favicon mmh3 hash, security-header grading. Read-only PoCs only.

### 3.5 CT-log passive subdomain enum — **S** *(Playbook 03)*
- Query crt.sh / CT logs for a domain → passive subdomain inventory before any active touch. **External call — needs authorization/rate awareness.**

---

## Tier 4 — Intelligence, correlation & optimization

### 4.1 Confidence scoring on every finding — **S/M**
- Attach a `confidence` (0–1) + evidence-quality tier to each `ScanResult` (banner-confirmed > behavior-confirmed > port-only). Drives FP-rate measurement the architecture was designed for.

### 4.2 Automatic scanner → detection handoff — **M**
- Wire scanner version output straight into `detection_engine/pipeline.py` (CVE match + EPSS/KEV) so a scan run emits prioritized findings end-to-end, no manual step.

### 4.3 Cross-scanner result cache & dedup — **S/M**
- Per-run host cache so liveness/open-ports/TLS are computed once and shared; dedup identical findings across scanners before writing JSONL.

### 4.4 Per-scanner metrics — **S**
- Emit timing, probe count, reply rate, FP-suspect count per scanner → measure accuracy in isolation (the stated design goal in `scanner/__init__.py`).

---

## Recommended sequence

1. **Tier 1.4 funnel** + **1.2 async UDP** — structural wins, unblock everything else, no privilege needed.
2. **Tier 1.1 SYN scan** (with connect fallback) — the headline speed/stealth upgrade.
3. **Tier 2.1/2.2 OS + ICMP fingerprint**, **2.3 JARM** — accuracy + identity for delta.
4. **Tier 1.3 adaptive timing** — correctness under rate limits.
5. **Tier 3** coverage modules by customer priority.
6. **Tier 4** correlation to close the scan→finding loop.

**Guiding constraints (unchanged):** pure Python stdlib (`socket`/`asyncio`/`struct`), scope-guarded before any packet, read-only/collection-only, normalized `ScanResult` JSONL out, tests per module (RED→GREEN), automatic graceful fallback when a privilege/feature is unavailable.
