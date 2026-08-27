# Implementation Risks & Core-Level Approach

> Companion to the gap analysis. Part 1 = concrete errors/challenges you will hit
> while implementing the new capabilities (ssh_scanner, SMB/LDAP via impacket,
> manager-side CVE, DNS AXFR/DNSSEC, TLS depth). Part 2 = what has to exist at the
> core for this to grow from "a scanner" into a platform.

---

## Part 1 — Challenges & errors per capability

### Cross-cutting (these bite *every* new scanner)

| Risk | Why it happens here | Mitigation |
|---|---|---|
| **Nuitka sealed-build breaks that dev never sees** | onefile compiles every dep; dynamic/lazy imports (impacket, cryptography backends) get dropped → `ImportError` **only in the sealed binary** | Extend the runtime-parity CI to build+run the *sealed* binary on every new dep; add explicit `--include-module` for impacket submodules |
| **Blocking calls in the asyncio loop** | new scanners often use sync libs (impacket, paramiko) inside async funnel → whole event loop stalls | Wrap every sync call in `asyncio.to_thread` (as `service_enum.netbios_name` already does) |
| **Scope/rate/anti-attribution bypass** | raw-socket or subprocess paths can skip `BaseScanner` guards | Route ALL new I/O through `BaseScanner`; reuse `user_agent()`, `probe_payload()`, `jittered_delay()`; never open a raw socket outside a scanner |
| **Result-schema drift** | adding fields to `ScanResult`/findings can break the manager's `jsonb` insert or older parsers | Only append fields; bump `result_schema_version`; keep NUL-stripping (`transport._strip_nul`) in mind for new banner bytes |
| **Accuracy regression** | a new check with no ground truth silently erodes the 100%/100% precision/recall you documented | Every scanner ships with a ground-truth test target + precision/recall numbers before it's marked `available` |
| **IPv6 / non-standard ports** | checks hardcoded to v4 or port 22/443 miss real surface | Take port from the funnel route, not a constant; test v6 parity |
| **Privilege tiers** | raw sockets need root; field probes often run unprivileged | Graceful degrade (you already do this for ICMP/SYN) — never crash, emit `error/permission_denied` |

### `ssh_scanner.py` (port ssh-audit's logic + data)

- **Raw SSH binary-packet protocol.** You must send a client version string
  (CRLF-terminated), read the server banner, then parse the `SSH_MSG_KEXINIT`
  packet (packet_length / padding_length / payload framing) *before* any
  encryption. Partial reads and servers that wait for the client's KEXINIT first
  are the two common failure modes.
- **LICENSING (verified 2026-08).** ssh-audit is **MIT** — you MAY vendor its
  algorithm database (`ssh2.py` `SSH2_KexDB`) and even its code into the sealed
  binary **with attribution + the MIT notice**. This is the cleanest port on the
  list. ⚠️ Do NOT do the same with **testssl.sh (GPL-2.0)** or **sslyze/nassl
  (AGPL-3.0)** — copyleft contaminates a commercial sealed binary; for those,
  reference only the public/RFC facts and re-derive the mapping. See the verified
  license table in `GAP_INTEGRATION_PLAN` / below.
- **False positives:** `ssh-rsa` host-key algorithm ≠ weak if it's actually
  `rsa-sha2-256/512` signatures — distinguish host-key algo vs signature algo.
- **Banner floods / tarpits:** cap bytes read (reuse the tarpit heuristic pattern).
- **Data drift:** you now own the weak-algorithm table; version it and schedule
  reviews (you lose ssh-audit's upstream updates).

### SMB null-session / share enum + LDAP anonymous bind (via impacket you already ship)

- **Policy line to decide first.** Your invariant is "NO brute-force / credential
  spray." A null session / anonymous bind sends *empty* credentials — it's
  read-only enumeration, but it **is** a (null) auth attempt and **will trip IDS**.
  Decide + document that this is in-policy before shipping. Keep "no *guessed*
  credentials" intact.
- **impacket bloat + Nuitka fragility.** impacket pulls pyasn1/pycryptodome, uses
  dynamic dispatch → biggest onefile-build risk on this list. Prototype the sealed
  build *early*, not at the end.
- **impacket is synchronous** → must run under `asyncio.to_thread`.
- **Unbounded results:** LDAP anonymous bind can return huge trees / hang → size +
  time caps mandatory.
- **Version skew:** impacket API isn't stable across releases (you pin `>=0.11`) —
  pin exactly and test on upgrade.

### Manager-side CVE / nuclei / KEV / CVSS

- **⚠️ Vantage problem (architectural).** nuclei run *on the manager* needs a
  network path to targets. Your probe is **inside** the customer network; the
  manager is often in the cloud → **it cannot reach internal hosts.** Options:
  (a) probe-side nuclei-lite (breaks "thin/no-DB probe"), (b) probe streams enough
  facts for offline CVE correlation, (c) manager pushes nuclei templates *to the
  probe* to execute. Pick deliberately — this is the hardest call.
- **Version→CVE false positives (the #1 accuracy complaint in this whole domain).**
  Distro backports patch without bumping the banner version (Debian/RHEL) →
  naive "OpenSSH 7.4 = vulnerable" is wrong. CPE matching is fuzzy. Confidence
  must reflect this; never assert a CVE from a banner alone.
- **Feed pipeline:** NVD + KEV + EPSS need an ingestion job, an offline mirror, and
  a freshness SLA. CVSS environmental scoring is opinionated — don't fake precision.

### DNS AXFR / DNSSEC / version.bind

- **AXFR is TCP/53** — different transport from your UDP/53 probes; needs a TCP DNS
  path + streaming with a size cap for large zones.
- **Mostly negative results** (most servers refuse AXFR) — low signal except on the
  rare misconfig; set expectations.
- **DNSSEC done right is hard** (DS/DNSKEY/RRSIG chain of trust). Decide scope: a
  shallow "DNSSEC present?" is cheap; full validation is a project.

### TLS depth (key-size / chain / renegotiation)

- **⚠️ stdlib `ssl` can't test what OpenSSL removed.** Python's `ssl` links the
  system OpenSSL; if that build dropped SSLv3/RC4/EXPORT, **you literally cannot
  offer them to test for them.** This is why testssl/sslyze craft raw handshakes.
  To match them you may need raw TLS ClientHello crafting, not stdlib `ssl`.
- **Chain validation needs a trust store.** Embed `certifi` in the sealed binary and
  keep the roots fresh (they expire). Keep chain validation **separate** from your
  existing `CERT_NONE` observation path — don't break "observe, don't fail."
- **Renegotiation / some cipher probes can hang or add load** — strict timeouts.

---

## Part 2 — Core-level approach to become a "big one"

What separates a scanner from a platform (Nessus / Qualys / Tenable / Rapid7 /
runZero class). Ordered by leverage. Several of these you have *seeds* of already.

### The non-negotiable foundations (build these into the core, not bolt on later)

1. **Content/engine separation — the single biggest structural decision.**
   Today detections are hardcoded Python in `findings.py` `_RULES`. That does not
   scale: you can't ship a new check without shipping code. Split into an **engine**
   (stable) + **versioned, signed detection content** (ships independently, like
   nuclei templates / Nessus plugins). This is what lets you add hundreds of checks
   without a release, and lets the *manager* own CVE content while the probe stays
   thin. **Do this before the catalog grows.**

2. **Asset identity & dedup substrate.** A platform tracks *assets over time*, not
   scans. Merge observations of the same host across vantages/scans/time into a
   stable asset ID (by MAC / cert fingerprint / JA4 / hostname). You have the seeds
   — `device_classifier.py`, `vantage_matrix.py`, `delta_scanner.py` — formalize
   them into one identity graph. (This is literally runZero's moat.)

3. **Findings as immutable events, not overwrites.** Store every finding as a
   time-stamped event → you get history, drift, "first seen / last seen", MTTR, and
   trend reporting for free. Delta becomes a query, not a special scan.

4. **Accuracy as a measured, gated discipline.** You already run precision/recall
   with ground truth (`PROBE_CAPABILITY_STATUS.md`) — make it a **CI gate**: no
   check reaches `available` without ground-truth numbers, and a regression fails
   the build. This measured-accuracy culture is the real moat; every incumbent
   loses trust on false positives.

5. **Risk prioritization, not raw severity.** The market winner is whoever turns
   10,000 findings into the 20 that matter. Combine **KEV + EPSS + internet-exposure
   (you have vantage data!) + asset criticality** into one risk score. Severity
   alone is 2010-era.

6. **Safety / authorization as product features (your differentiator).** You already
   have scope crypto, scope re-validation, rate limiting, OT passive mode,
   anti-attribution, TOFU enrollment, mTLS. Package these as guarantees:
   blast-radius controls, kill switch, "OT-safe / do-no-harm" mode. This wins
   fragile/OT/regulated buyers that Nessus scares.

### The enterprise-sales table stakes (needed to sell, not to scan)

7. **Multi-tenancy + RBAC + full audit trail + SSO.** Tenant isolation is a
   from-day-one data-model decision, painful to retrofit.
8. **Compliance mappings.** Map findings → PCI-DSS / CIS / NIST 800-53 / ISO 27001 /
   HIPAA. This is what buyers actually pay for.
9. **API-first + integrations.** Findings must flow out: Jira/ServiceNow tickets,
   SIEM export, webhooks, Slack. A finding that can't leave the tool is worthless to
   an enterprise SOC.
10. **Reporting.** Exec summary + technical detail + remediation + retest, generated,
    branded, exportable.

### Scale & operations

11. **Fleet architecture.** Many probes ↔ one manager: enrollment (have), heartbeat
    (have), result spooling with backpressure (have `result_spool.py`), job queue,
    probe health/coverage telemetry. Harden for hundreds of probes.
12. **Scan-completeness self-proof.** Extend the full-port-audit self-health idea
    everywhere: a "clean" result must be *provably complete*, not just empty.
13. **AI-native triage layer (grounded, not generative).** Your existing plans fit
    here: LLM for FP suppression, remediation guidance, natural-language query over
    findings — but strictly on top of the fact substrate, **never inventing a
    finding**. Keep the "probe emits facts, never guesses" invariant end-to-end.

### Sequencing advice
Go **deep on network/infra** (your current strength) before sprawling into web-app
and cloud. Breadth without the accuracy discipline (#4) and content/engine split
(#1) creates a false-positive machine that destroys trust — the one thing you can't
buy back.

### The five that must exist at the core
1. Content/engine separation (updatable, signed detections)
2. Asset-identity + immutable finding-events data model
3. Accuracy regression harness as a CI gate
4. Risk prioritization (KEV/EPSS/exposure), not raw severity
5. Multi-tenancy + audit + API-first (retrofitting these is the expensive mistake)
