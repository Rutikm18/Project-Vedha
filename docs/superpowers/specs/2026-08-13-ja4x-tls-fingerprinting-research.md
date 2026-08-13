# Advanced Capability: JA4X Certificate Fingerprinting — arXiv Research → Implementation

> Research-driven scanner enhancement for `probe/main_scripts/`. Question: what
> recent (arXiv, cs.CR) technique is both *advanced* and *implementable* in a
> pure-Python, safe, read-only probe? Answer: **JA4-family TLS fingerprinting**,
> implemented here as **JA4X (X.509 certificate fingerprint)**.
> Status: **implemented + verified** (2026-08-13). Module: `main_scripts/ja4x.py`.

## 1. arXiv research (what's current in network fingerprinting / scanning)

Searched `cat:cs.CR` (arXiv API; the recent listing skews to ML-IDS, so category +
phrase queries were used). The **TLS-fingerprinting** cluster is the live,
implementable line of work:

| Paper | arXiv | Yr | Technique |
|-------|-------|----|-----------|
| Detecting Web Bad Bots via TLS Fingerprints | 2602.09606 | 2026 | **JA4** handshake features + gradient-boosted classifier to separate bots from users |
| A novel TLS-based Fingerprinting… feature expansion + similarity mapping | 2410.03817 | 2024 | Enrich TLS fingerprints, **MinHash/LSH** similarity to surface *unknown* malicious domains |
| Positional-Unigram Byte Models for Generalized TLS Fingerprinting | 2405.07848 | 2024 | Byte-position statistical model of ClientHello; **resists cipher randomisation** |
| Accurate TLS Fingerprinting using Destination Context + Knowledge Bases | 2009.01939 | 2020 | Fingerprint + destination context via weighted naive Bayes |

By contrast, the "port scanning" cluster in cs.CR is almost entirely *defensive*
(detecting/mitigating scans: IDS, SmartNICs, honeypots) — not techniques a
collector implements.

**Takeaway:** the modern, high-signal, implementable direction is JA4-family
fingerprinting. The scanner already ships the *older* active TLS fingerprint
(JARM, 2020, `tls_fingerprint.py`); JA4+ (FoxIO, 2023) is its successor and the
subject of the 2024–2026 academic work above.

## 2. Why JA4X (of the JA4+ suite)

- **Zero extra probing / zero new risk.** JA4S needs raw ServerHello parsing;
  JA4X is computed from the **certificate the `tls_scanner` already collects** —
  pure, offline, read-only.
- **High identification value.** JA4X fingerprints the certificate's *structure*
  (ordered issuer/subject/extension OIDs), independent of field *values*. Certs
  minted by the same tooling/CA share a JA4X even with different names — strong
  for spotting auto-generated C2 certs and correlating infrastructure across a
  fleet or across runs (feeds the manager's delta/threat-intel).
- **Interoperable.** Byte-exact with the FoxIO reference (`2.5.4.6` → `550406`),
  so fingerprints match public JA4X intelligence.

## 3. Algorithm (as implemented, FoxIO-interoperable)

```
for each ordered OID list  L ∈ { issuerRDN, subjectRDN, extensions }:
    hex_i   = DER-content-octets(OID_i) in hex        # 2.5.4.6 -> "550406"
    hash(L) = sha256(",".join(hex_i))[:12]            # empty L -> "000000000000"
JA4X = f"{hash(issuer)}_{hash(subject)}_{hash(extensions)}"
```

## 4. What was implemented

| File | Change |
|------|--------|
| `main_scripts/ja4x.py` **(new)** | `oid_to_hex` (DER OID encoder), `ja4x_from_oid_lists` (pure), `ja4x_from_cert` / `ja4x_from_der` (lazy `cryptography` adapter), `SUSPICIOUS_JA4X` registry + `match_suspicious` |
| `main_scripts/tls_scanner.py` | certificate output now carries `ja4x` (computed from the already-parsed cert) |
| `main_scripts/findings.py` | self-signed finding enriched with `ja4x`; new rule `TLS-SUSPICIOUS-CERT-FINGERPRINT` fires only on a curated threat-intel match |
| `tests/test_main_scripts_ja4x.py` **(new)** | 10 tests: OID/DER correctness, format/determinism/order-sensitivity, empty sentinel, cert adapter, real-DER round-trip (cryptography), threat-intel match + finding |

**Verification:** 10 JA4X tests pass (incl. real self-signed-cert DER round-trip);
full `main_scripts` subset **92 passed, no regression**. OID encoding validated
against the reference (`550406`, `2a864886f70d010901`).

**Boundary preserved:** JA4X is *identification/hygiene*, not a CVE claim — it
stays on the probe; the manager still owns CVE detection. The scanner does not
invent malware attributions: `SUSPICIOUS_JA4X` ships empty and is populated from
vetted feeds; the match *mechanism* is what's tested.

## 5. Roadmap (further research-backed capabilities)

- **JA4S** (ServerHello fingerprint) — reuse the raw TLS parsing already in
  `tls_fingerprint.py` (JARM) to also emit JA4S. Higher effort (raw handshake).
- **JA4-similarity (arXiv:2410.03817)** — MinHash/LSH over fingerprints on the
  manager to cluster look-alike infrastructure and surface unknown-malicious.
- **HASSH** — the SSH analogue (client/server KEX fingerprint) from banner data.
- **Favicon hashing** — Shodan-style web-app identity for `web_scanner`.
