# Probe Findings Engine — Research, Design & USPs

> The first step toward "the best vulnerability scanner": turn the probe's rich,
> evidence-backed **facts** into vulnerability **findings**. Scope: `probe/main_scripts/`
> (the reference scanner tree). Status: **v1 implemented + verified** (2026-08-13).
> Module: `probe/main_scripts/findings.py`. Tests: `probe/tests/test_main_scripts_findings.py`
> (27 tests). Wired into `run_all.py`.

---

## 1. Problem & first-principles research

### 1.1 What a "finding" is (and isn't) here

A **vulnerability scanner** is only as good as the *findings* it produces — not the packets
it sends. The `main_scripts` tree is already a strong **collection** engine: every scanner
emits a pure, evidence-backed `ScanResult` and, by explicit invariant, *no verdicts*
("No vulnerability conclusions in collection modules", `plan.md` Step 29). That keeps
collection measurable and false-positive-auditable — but it means the tool, as shipped,
**found facts, not findings**. Closing that gap is the highest-leverage single step toward a
best-in-class scanner.

**The boundary that makes this safe and correct:** there are two kinds of finding.

| Kind | Needs | Where it belongs |
|------|-------|------------------|
| **Config / hygiene / exposure** (SMBv1 on, weak TLS, readable SNMP community, exposed Redis, NTP monlist, Telnet) | only what the probe directly observed | **the probe** — no database required |
| **CVE match** ("host runs OpenSSL 1.0.1 → CVE-2014-0160") | the pinned vulnerability DB + version matching | **the manager** (the probe never emits a CVE) |

The engine here produces the **first kind only**. That is a deliberate architectural
boundary, not a limitation: it means the findings layer is deterministic, offline, and
requires no vuln DB — while CVE detection stays on the manager where the pinned DB lives.

### 1.2 What separates a *best-in-class* findings layer from a noisy one

Research across the incumbents' failure modes (Nessus/OpenVAS/Qualys) points at four things
that decide whether analysts trust a scanner:

1. **Evidence or it didn't happen.** Every finding must cite the exact observed fact
   (scanner, field, value) that produced it. No inference without an observation.
2. **Ambiguity must not become a finding.** The #1 source of scanner false positives is
   treating "no response" or "maybe open" as "open/vulnerable." A finding on an *unproven*
   port is a false positive waiting to happen.
3. **Confidence ≠ severity.** "Redis port answered" is a *high-severity* exposure but only
   *medium-confidence* that it's exploitable (auth may be enforced). Collapsing the two is
   how scanners cry wolf.
4. **Explainable + deterministic.** A reviewer must be able to reconstruct every verdict.
   No black box, no model, no randomness.

These four principles are the design contract below, and they are exactly the properties the
`main_scripts` collection layer already fought for (vantage-relative, ambiguity-as-output) —
the findings engine extends that discipline one layer up.

---

## 2. Design

### 2.1 Architecture

```
scanners (collection, pure facts)        findings.py (interpretation)
  port_scan / smb_scan / tls_scan     ─┐
  snmp_scan / udp_scan / web_scan      ├─▶  run_findings(facts) ─▶ [Finding]  ─▶ findings.jsonl
  service_banner ...                  ─┘        (pure, deterministic,           + SUMMARY.json
                                                 no wire access)
```

`findings.py` is a **separate module** from every collector — collection stays pure and
auditable; judgement lives in one reviewable place. It accepts `ScanResult` objects *or* raw
JSONL dicts (so it works both in-process and over saved scan output).

### 2.2 The `Finding` record

```
rule_id, title, severity, confidence, category, target, port, proto,
evidence (human, cites the fact), recommendation, data (structured trigger), source_scanner
```

- **severity** ∈ critical | high | medium | low | info
- **confidence** ∈ high | medium | low  — *how sure we are it's real AND matters as stated*
- **category** ∈ weak_crypto | misconfiguration | exposure | cleartext_protocol |
  amplification | information_disclosure | default_credentials
- **no `cve_id`** — by design (§1.1).

### 2.3 Rule catalog (v1)

| rule_id | Trigger (observed fact) | Sev | Conf | Category |
|---------|-------------------------|-----|------|----------|
| TLS-OBSOLETE-PROTO | SSLv2/SSLv3 accepted | high | high | weak_crypto |
| TLS-LEGACY-PROTO | TLS 1.0/1.1 accepted | medium | high | weak_crypto |
| TLS-WEAK-CIPHER | cipher_analysis[].weak | high | high | weak_crypto |
| TLS-CERT-EXPIRED | certificate.expired | medium | high | misconfiguration |
| TLS-CERT-SELF-SIGNED | certificate.self_signed | low | high | misconfiguration |
| SMB-V1-ENABLED | smbv1_enabled | high | high | misconfiguration |
| SMB-SIGNING-NOT-REQUIRED | signing_required == false | medium | high | misconfiguration |
| SNMP-COMMUNITY-READABLE | community found (high if default) | high/med | high | default_credentials |
| SNMP-AMPLIFICATION | amplification_factor ≥ 5 | medium | high | amplification |
| UDP-NTP-MONLIST | monlist_enabled | medium | high | amplification |
| UDP-DNS-OPEN-RESOLVER | open_recursion | medium | high | amplification |
| UDP-AMPLIFIER-EXPOSED | known amplifier service answered | low | medium | amplification |
| SVC-TELNET-CLEARTEXT | tcp/23 **open** | high | high | cleartext_protocol |
| SVC-FTP-CLEARTEXT | tcp/21 **open** | medium | medium | cleartext_protocol |
| SVC-RDP-EXPOSED | tcp/3389 **open** | medium | medium | exposure |
| SVC-DATASTORE-EXPOSED | tcp/{6379,27017,9200,5984,11211,9042,3306,5432,1433,1521} **open** | high/med | medium | exposure |
| WEB-DANGEROUS-METHODS | PUT/DELETE/TRACE/CONNECT | medium | high | misconfiguration |
| WEB-SERVER-VERSION-DISCLOSURE | Server header w/ version | info | high | information_disclosure |

### 2.4 Invariants (enforced + tested)

- **`open|filtered` never raises an exposure finding** — only a definitively `open` port does.
  (`test_open_filtered_never_raises_exposure`.)
- **Every finding is evidence-backed** — non-empty `evidence` + `data`. (`test_every_finding_is_evidence_backed`.)
- **No finding carries a `cve_id`.** (`test_no_finding_carries_a_cve_id`.)
- **Deduped** by (rule_id, target, port); **sorted** most-severe first.
- **Pure & safe** — no sockets, no state, no AI. Interpretation only.

---

## 3. USPs — what makes this the basis of the best scanner

1. **Evidence-backed findings, always.** Every finding cites the exact fact and method that
   produced it. Not "you might be vulnerable" — *"the SMB server negotiated dialect 0x0202 with
   `smbv1_enabled=true`."* This is the credibility the incumbents lose to false positives.
2. **Anti-false-positive by construction.** Ambiguity (`open|filtered`, no-response, unproven
   port) never becomes a finding. Confidence is separated from severity, so an exposure is never
   over-claimed as an exploit. This is the moat: analysts stop discarding the tool's output.
3. **Zero-dependency, offline, air-gap-ready.** Config/hygiene/exposure findings need no vuln
   DB, no internet, no cloud. The probe can produce actionable findings inside an isolated OT
   segment — where cloud scanners can't reach and appliance scanners can't be placed.
4. **Deterministic + explainable.** Pure functions over facts; a reviewer (or an auditor)
   reconstructs every verdict. No black-box scoring.
5. **Clean architectural boundary.** Config findings on the probe; CVE findings on the manager.
   Each runs where its data lives — the probe never ships or needs the CVE database.
6. **Safe by design.** Interpretation-only layer; the collectors underneath never brute-force,
   authenticate, or exploit. Fit for production and OT networks.
7. **Composable output.** `findings.jsonl` is a clean, typed stream that feeds the manager's
   detection/lifecycle/risk-rank pipeline directly — the probe pre-classifies, the manager
   enriches with CVE/KEV/EPSS.

---

## 4. Validation evidence

- **27 unit tests** (`test_main_scripts_findings.py`) — positive + negative per rule, plus the
  invariants above. Full `main_scripts` subset: **66 passed, no regression.**
- **Real scan data:** run against a captured `192.168.1.70` scan → correctly surfaced the one
  genuine exposure (RDP/3389 open) and stayed silent where collection data was empty (SMB fact
  `{}`, no TLS results) — no fabricated findings.
- **Synthetic vulnerable host:** 14 findings across all 7 categories, correctly severity-sorted;
  a duplicate `open|filtered` Redis fact produced **no** second finding (dedup + ambiguity both
  holding).

---

## 5. Roadmap (next iterations toward "best")

Prioritised, each an independent, testable rule/collector addition:

1. **EOL / obsolete-software findings** from `service_banner` product+version (e.g. OpenSSH < 7,
   IIS 6, Apache 2.2) — hygiene, not CVE. Medium.
2. **Anonymous-access proofs** (FTP anonymous login result, SMB null session, Redis `PING`/`INFO`
   without auth) — upgrades exposure findings from medium→high *confidence* with a real proof.
   Requires the collectors to record the (safe, read-only) probe result.
3. **RDP/RPC collectors** (`plan.md` Steps 19/20) → feed `SVC-RDP-EXPOSED` a security-layer
   detail (NLA on/off) and RPC endpoint inventory.
4. **HTTP security-header findings** (missing HSTS/CSP/X-Frame-Options) from `web_scan`.
5. **Correlation findings** (e.g. SMBv1 + signing-not-required + exposed = domain takeover path).
6. **Severity calibration hook** so the manager can re-rank probe findings with asset criticality
   + KEV/EPSS (ties into the P4 `risk_rank` work already on the manager).
7. **Accuracy harness** (`plan.md` Steps 25/26): findings TP/FP vs a labeled corpus — turn the
   anti-FP claim into a published number.

---

## 6. Files

| File | Role |
|------|------|
| `probe/main_scripts/findings.py` | the engine + rule catalog + CLI (`python -m main_scripts.findings *.jsonl`) |
| `probe/tests/test_main_scripts_findings.py` | 27 tests |
| `probe/main_scripts/run_all.py` | wired: emits `findings.jsonl` + `findings_summary`/`top_findings` in `SUMMARY.json` |
