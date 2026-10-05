# Network VA — Research Addendum (roadmap #3, QUIC/ECH, LZR follow-ons)

**Status:** Research only. *No code changed.* Extends Volumes I & II and the LZR
confirmation spec with depth on three areas the earlier docs flagged but did not
drill into: the RDP/SCHANNEL inner-TLS gap (roadmap item #3), the QUIC/HTTP-3
coverage gap and what ECH does to TLS fingerprinting, and the post-LZR service-ID
literature. **Date:** 2026-10-03 · **Branch:** `claude/serene-bardeen-1uqxzq`.

---

## 1. RDP / SCHANNEL inner-TLS measurement (roadmap #3 — the confirmed deep gap)

**The gap (restated, from `docs/STATUS.md` #3):** `tls_scan` is deliberately never
run on 3389/445/135, so the SCHANNEL protocol/cipher set behind an RDP listener is
never measured. `rdp_scanner` confirms RDP and NLA posture but stops before the
crypto. Yet RDP, when it negotiates the SSL/HYBRID security layer, runs a **real
TLS handshake inside its own protocol** — the exact surface a TLS audit should grade.

### 1.1 The RDP security-layer negotiation (what to drive)

RDP's X.224 Connection Request carries an **RDP Negotiation Request** advertising
the client's supported security protocols; the server's Connection Confirm selects
one. The selectable protocols (the set nmap's `rdp-enum-encryption` and
CiscoCXSecurity's `rdp-sec-check` cycle through):

| Selected protocol | Meaning | Crypto surface |
|---|---|---|
| `PROTOCOL_RDP` (Native/Standard) | legacy RDP security | **RC4** 40/56/128-bit, "FIPS" (3DES) — the weak, MITM-able class |
| `PROTOCOL_SSL` (TLS) | RDP over a TLS tunnel | standard TLS: versions + ciphers + cert ← **this is where SCHANNEL lives** |
| `PROTOCOL_HYBRID` / `HYBRID_EX` (CredSSP / NLA, +Early User Auth) | TLS + CredSSP (NTLM/Kerberos) pre-auth | TLS tunnel **and** an NTLMSSP exchange |
| `PROTOCOL_RDSTLS` | RDS gateway TLS | TLS tunnel |

### 1.2 The measurement method (collection-only design)

To grade SCHANNEL behind RDP, extend `rdp_scanner`'s existing X.224 handshake:

1. Send the X.224 Connection Request advertising **SSL** (and separately HYBRID) in
   the RDP Negotiation Request.
2. Read the Connection Confirm → which protocol the server selected (already parsed
   by `rdp_scanner.parse_connection_confirm` / `_posture_from_selected`).
3. **If SSL/HYBRID selected:** the server now expects a TLS ClientHello on the same
   socket. Drive a TLS handshake **per protocol version** (1.0/1.1/1.2/1.3) and the
   cipher probes — reusing `tls_scanner`'s `_try_version` / `classify_cipher` /
   cert-parse machinery — *inside* the post-negotiation socket. Record exactly the
   same facts `tls_scanner` records for a normal TLS port (accepted versions, cipher,
   cert), tagged `transport: "rdp"`.
4. **If Native RDP selected:** record the legacy encryption level (RC4 40/56/128 /
   FIPS-3DES) as a weak-crypto finding — no inner TLS exists to grade.

The same inner-TLS pattern applies to **LDAP StartTLS (389)**, **SMTP STARTTLS
(25/587)** and **WinRM-over-HTTPS (5986)**; RDP is the highest-value because it is
ubiquitous on Windows estates and the legacy RC4 path is a real MITM exposure. This
is purely additional *reading* — one handshake per version/cipher — no auth, no
exploitation; it fits `rdp_scanner`'s stated "read-only, one handshake" posture
extended to "a few handshakes to enumerate the crypto."

### 1.3 Bonus, already partly present

An **incomplete CredSSP/NTLM request with null credentials** makes the server
return an NTLMSSP CHALLENGE that discloses NetBIOS/DNS/OS-build (the `rdpscan`
technique). Vedha's `smb_scanner` already parses exactly this NTLM challenge for the
Windows build (`ntlm_os_build`, `windows_release_from_build`); the same parser can be
reused on the RDP/HYBRID path to add an OS-build fact from 3389 with no new parsing
code. Collection-only (null credentials elicit a public challenge; nothing is
authenticated).

**References:** nmap `rdp-enum-encryption.nse`
(https://github.com/nmap/nmap/blob/master/scripts/rdp-enum-encryption.nse);
CiscoCXSecurity `rdp-sec-check`; CyberRoute `rdpscan` (null-cred NTLMSSP disclosure);
MS-RDPBCGR negotiation. Maps to Vedha `scanner/rdp_scanner.py`, `tls_scanner.py`,
`smb_scanner.py`, `workflow/router.py`.

---

## 2. QUIC / HTTP-3 coverage gap and ECH's effect on TLS fingerprinting

### 2.1 The gap

Vedha scans **TCP** (connect/SYN) and a fixed UDP-service probe set
(`udp_scanner`). **QUIC (UDP/443, and other ports) is not probed.** Since QUIC now
carries **>30% of web requests** (Cloudflare, 2024) and an endpoint can serve
HTTP/3 **only** over QUIC, a TCP-only web assessment can *miss a live web service
entirely* on a QUIC-first host, and will always miss the QUIC attack surface.

### 2.2 The core logic of a QUIC discovery probe (collection-only)

QUIC is UDP; a client opens with an **Initial packet** containing a TLS 1.3
ClientHello inside a CRYPTO frame (version-negotiation long-header packet). A probe:

1. Send a QUIC Initial (long header, a supported version e.g. `0x00000001` for
   QUICv1) with a minimal ClientHello (ALPN `h3`) to UDP/443.
2. A **version-negotiation** or **Initial/Retry** response = QUIC is live here →
   record "speaks QUIC/HTTP-3," the negotiated version, and (from the ServerHello)
   a **JA4S/JA4 over QUIC** fingerprint (JA4 already encodes `q` as the transport —
   Vedha's `ja4s.py` supports the `q` proto marker today).
3. No data beyond the handshake → fingerprint-only, read-only, same posture as the
   TLS probe.

This is a natural extension of the `uc_external_web_triage` / `uc_web_app_triage`
use-cases (currently *Coming soon*) and of `udp_scanner`'s protocol-probe model.

### 2.3 ECH — what it changes for fingerprinting

**Encrypted Client Hello (ECH)** encrypts the inner ClientHello (including SNI) to
the server; an on-path observer sees only the outer "ClientHelloOuter." Implications
for Vedha's TLS-stack identity (Volume II §6):

- **SNI-based inference degrades** where ECH is deployed — but ECH adoption on the
  *server* side is still limited, and this is an **active** scanner (we *are* the
  client), so we control the ClientHello and are not trying to recover someone
  else's SNI. ECH mainly matters for *passive* observation, which Vedha only does in
  the OT path (no TLS there).
- **JA4S/JA4X still work** against an active probe: the server's response behaviour
  and certificate structure are still observable. The research direction
  (fingerprint-as-feature + similarity, Volume II §6.4) is the robust answer as
  ClientHello contents get more uniform/encrypted.
- **Takeaway:** add a QUIC discovery probe for *coverage*; keep JA4S/JA4X (not
  SNI/JARM) as the durable identity signal; treat ECH as a reason to prefer
  server-response and certificate fingerprints over ClientHello-derived ones.

**References:** QUIC adoption (Cloudflare 2024); TLS 1.3/QUIC handshake
(RFC 9000/9001); ECH drafts; JA4+ QUIC support
(https://github.com/FoxIO-LLC/ja4); QUIC measurement surveys 2024–2025.

---

## 3. Post-LZR service-identification literature (where the confirmation stage goes next)

LZR (2021) is the baseline the confirmation spec builds on. The 2023–2026 direction
is **learned** identification layered on the same cheap-handshake collection:

- **Richer handshake-feature classification.** A 2024 ACM IMC pipeline classifies
  the device/software behind a flow from **62 attributes extracted from handshake
  messages** at **>96% accuracy** — i.e., once you have the handshake LZR already
  collects, a feature model identifies far more than a regex match. For Vedha this is
  a *manager-side* analytics layer over the probe's confirmation facts, not a probe
  change (keeps the collection/analysis split).
- **Autoencoder unknown-device detection.** Deep-autoencoder approaches detect
  *unknown* devices (not in the training set) at ~**98.6%** with 100 known classes —
  the open-set problem a fixed fingerprint DB can't solve. This is the ML analogue
  of JA4 *similarity* mapping (Volume II §6.4): surface "this doesn't match anything
  known" instead of silently mislabelling.
- **Fingerprint-as-feature, not exact-match** (the TLS-FP papers in Volume I/II):
  the consistent finding is that exact-hash blocklists miss novel infrastructure;
  modelling the fingerprint as features (gradient boosting) or neighbourhoods
  (MinHash/similarity) generalises.

**Design implication:** the LZR confirmation stage (probe spec) is the right
*collection* foundation; the next accuracy tier is **manager-side**: feed the
confirmation/handshake facts into (a) a feature classifier for product/device ID and
(b) an open-set/similarity model for "unknown but suspicious." Both respect the
probe-collects / manager-analyses split and both are gated by the same
ground-truth accuracy discipline.

**References:** LZR (arXiv:2301.04841); ACM IMC 2024 handshake-classification
(conferences.sigcomm.org/imc/2024); autoencoder unknown-device detection; TLS-FP
feature/similarity papers (arXiv:2602.09606, 2410.03817, 2405.07848, 2009.01939).

---

## 4. Net additions to the roadmap (Volume II §12)

| Item | This addendum | Class | Note |
|---|---|---|---|
| **3. TLS-inside-RDP / SCHANNEL** | §1 — drive RDP SSL/HYBRID then per-version/cipher inner TLS; reuse `tls_scanner` + NTLM parser | collection-only | highest confirmed deep gap; extends `rdp_scanner` |
| **+ QUIC/HTTP-3 discovery** | §2 — UDP/443 QUIC Initial probe; JA4S-over-QUIC | collection-only | closes a real >30%-of-web coverage blind spot for the web use-cases |
| **+ ECH-aware identity** | §2.3 — prefer JA4S/JA4X over SNI/JARM | analysis-only | durability as ClientHellos encrypt |
| **+ ML service/device ID** | §3 — handshake-feature classifier + open-set model | manager-side analysis | next accuracy tier atop LZR confirmation facts |

All collection-side items stay unauthenticated, read-only, scope-guarded, and must
pass the ground-truth accuracy gate before promotion — same discipline as every
other capability.
