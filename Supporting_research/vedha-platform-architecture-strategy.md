# Vedha — Platform Architecture & Strategy

**Date:** 2026-08-30
**Question:** what does the best network vulnerability assessment platform look like in 2026, and where is the opening?
**Companion:** `vedha-pipeline-hardening.md` (pipeline correctness) — this document is the layer above it.

---

## 0. The short version

Four things happened in the last six months that, taken together, invalidate how essentially every network VA platform is built:

1. **NVD stopped enriching most CVEs** (April 15, 2026). CPE data — the mechanism scanners use to match a CVE to a product — now exists for a minority of new vulnerabilities. Any platform whose detection logic is *"match NVD CPE against fingerprint"* is going structurally blind.
2. **CISA replaced KEV deadlines with a four-variable risk model** (BOD 26-04, June 10, 2026), and one of those four variables is asset exposure — something only *your* scan data can answer.
3. **AI-driven discovery went superlinear.** Forrester's read: *"The limiting factor in security is no longer the ability and knowledge to find problems — it's the ability to absorb, prioritize, and act on them."*
4. **The industry's false-negative problem got measured.** In a controlled 167-environment benchmark, the market-leading scanner claimed detection coverage for 67% of remotely detectable vulnerabilities and actually found 23%.

The consequence for you is unusually specific:

> **The scanner is a commodity. The evidence store is the product.**

Your existing architecture — probe emits verbatim facts, manager performs 100% of detection — is, accidentally, the single most valuable structural decision available in this market right now. Your work log treats it as an implementation detail. It is the moat. Everything below is about recognising that and building on it deliberately.

---

## Part 1 — What actually changed in the market

### 1.1 The CVE data supply chain broke

NIST enriched more than 42,000 CVEs in 2025, and early-2026 submissions ran roughly a third higher year over year. On April 15, 2026 it gave up on universal coverage. Going forward it enriches only CVEs that are in CISA's KEV catalog, affect federal government software, or fall under EO 14028 critical software. Everything else is marked lowest priority and receives no CVSS, no CPE, no CWE — potentially indefinitely. The entire pre-March-2026 unenriched backlog was reclassified as "Not Scheduled" in bulk.

Industry estimates put the enriched share at **15–20% of anticipated CVE volume**.

The load-bearing loss is CPE. A CVE record without CPE cannot be matched against an asset inventory by conventional tooling, so the alert that should trigger remediation never fires. This was already worse than most teams assumed: VulnCheck's analysis of 2024 data found NVD supplied CPE identifiers for **41.35%** of published CVEs, against 76.95% for its own enrichment. The April decision widens that gap deliberately.

CVE volume itself keeps climbing — 48,171 in 2025, with a forecast around 70,000 for 2026, and that forecast predates the current generation of AI-assisted discovery.

**Architectural consequence.** A platform that resolves *fingerprint → CPE → NVD → CVE* has just had its middle two hops deleted for most vulnerabilities. A platform that resolves *raw observation → hand-written or vendor-advisory-derived rule → finding* is unaffected. You are already the second kind. Most incumbents are the first, and cannot cheaply become the second, because they didn't keep the evidence.

### 1.2 Prioritization became a per-asset decision

BOD 26-04 supersedes BOD 19-02 and BOD 22-01, drops CVSS as the scheduling mechanism, and sets remediation urgency from four binary variables evaluated **per vulnerability, per asset**: asset exposure, KEV status, exploit automation, technical impact. Sixteen combinations map to five tiers, from 3 days with mandatory forensic triage down to fix-at-next-upgrade.

CISA's Vulnrichment supplies three of the four. **Asset exposure is determined by the organisation, from its own scanner and asset data.**

That is the whole ballgame for a network VA vendor. Three inputs are free and public; the fourth is exactly what a network scanner is for. You are one join away from producing the current federal prioritization model natively, with evidence for the variable nobody else can source.

Worth noting how badly the old model is performing: only **26% of KEV vulnerabilities were fully remediated in 2025**, down from 38% the prior year, with a median resolution time of 43 days. The problem was never finding them.

### 1.3 The market renamed itself around validation

Gartner's CTEM frame — Scoping, Discovery, Prioritization, **Validation**, Mobilization — is now how buyers think, and "Adversarial Exposure Validation" is a distinct Gartner market. Validation is where programs are documented to stall, and it is where the value is: one commonly cited figure has 63% of vulnerabilities initially rated high or critical dropping to 10% after validation, an 84% reduction in false urgency.

The pitch has shifted from *"we found 4,000 vulnerabilities"* to *"we proved 40 of them are reachable and exploitable, and here's the evidence."*

### 1.4 The false-negative problem, finally quantified

The 2024 Pentest-Tools benchmark ran seven scanners against 167 vulnerable environments from vulhub, of which 128 were remotely detectable.

| Scanner | Claims detection for | Actually detected |
|---|---|---|
| Nessus (all environments) | 55.09% | **18.56%** |
| Nessus (remotely detectable) | 67.19% | **22.66%** |
| Qualys, Nuclei | — | ~25% below claimed |

Misses included Shellshock, Drupalgeddon 2, and the Confluence OGNL RCE — not obscure bugs.

Sit with that. The market leader has a **3x gap between its advertised plugin coverage and its actual detection rate**, and it ships no signal that would let a customer notice. Sonatype separately documented 167,286 instances of exploitable components going entirely unflagged.

**This is the opening.** Every vendor competes on claimed coverage. Nobody reports measured coverage, and nobody reports what they could not check. A platform that says *"we assessed 847 of 903 applicable checks; here are the 56 we couldn't, and why"* is making a claim no competitor can match without rebuilding their data model.

### 1.5 What the AI research actually supports

This is where careful reading matters, because the marketing and the literature disagree sharply.

**Autonomous offensive agents are far weaker than the discourse suggests.** A June 2026 survey of 81 Agent4Pentest papers reports that as benchmarks moved from CTF puzzles to realistic full-scope and CVE tasks, average best-reported success rates **fell from 30% (2023) to 25% (2024) to below 15% (2025–2026)**. The capability didn't regress; the evaluations got honest.

**Agent unreliability is itself a security defect.** Princeton's SAGE group argues that uncompromised agents pose integrity risks through ordinary inconsistency: the same agent, the same task, identical conditions, different outcomes across runs — plus brittleness to trivial rephrasing and poor self-knowledge. They note larger models can *reduce* consistency. Separately, one evaluation found 94.4% of state-of-the-art LLM agents vulnerable to prompt injection and 100% to inter-agent trust exploits.

**Where AI is demonstrably strong: bounded generation with verifiable rewards.** DARPA's AIxCC (2023–2025, won by Team Atlanta) had autonomous cyber reasoning systems finding and patching real vulnerabilities in open-source C and Java at roughly **$152 per task**, versus bug bounties in the hundreds to hundreds of thousands. All seven finalist systems were open-sourced. The distinguishing feature of that setting is that every output was mechanically verifiable — a crashing input either crashes or it doesn't; a patch either passes the test suite or it doesn't.

The synthesis is clean and it should govern your entire AI strategy:

> **AI is excellent where output is cheaply verifiable and terrible where it is not.** Vulnerability detection in a customer environment is the second kind. Detection *content authoring*, evaluated against a fixture corpus, is the first kind.

Put an LLM in the runtime decision path and you have built a scanner whose answers change between runs, which is unshippable in security. Put it in the authoring path, gated by deterministic tests, and you get a large multiple on your content velocity — which is precisely the constraint the NVD collapse just created.

---

## Part 2 — How the leaders are actually built

Stripped of marketing, there are four architectural species.

**Plugin-executor scanners** (Nessus, OpenVAS/Greenbone, Nexpose). Thousands of scripts, each performing a check and emitting a verdict. Evidence is transient; the plugin decides and discards its inputs. Strength: enormous accumulated coverage. Weakness: no retroactive answering — a new CVE means a new plugin and a full rescan — and the claimed/actual gap in §1.4 is invisible from inside the model, because a plugin that fails to fire is indistinguishable from a plugin that found nothing.

**Template engines** (Nuclei, and Nuclei embedded in others). Detection as declarative, community-authored YAML. Strength: content velocity and auditability — the check is readable. Weakness: still verdict-oriented, and template quality varies.

**Fingerprint-and-query platforms** (runZero is the clearest example). Unauthenticated active scanning plus passive discovery plus integrations, profiling each asset against roughly **1,000 attributes**, with vulnerability detection expressed as *queries over the stored fingerprint data*, supplemented by embedded Nuclei with templates selected dynamically per matched service. This buys the capability they market as responding to emerging threats **without rescanning**, and it is only possible because they kept the observations.

Their own illustration of why fingerprint depth matters: a leading vulnerability scanner identified a device as CentOS Linux; it was an F5 load balancer running CentOS-based firmware. Superficially accurate, and the shallow detail led the team to deprioritize the wrong thing.

**Aggregators and prioritizers** (Nucleus, Vulcan, Brinqa, ArmorCode, Zafran). No scanning; they ingest everyone else's findings and re-rank. Structurally dependent on upstream scanners' recall, which §1.4 says is roughly 20%. They cannot fix a false negative they never received.

**Where you are.** Your probe emits facts, your manager decides, your `scan_results` table is append-only JSONB. That is the third species, which is the right one, and you got there for pipeline-hygiene reasons rather than strategic ones. The gap between you and runZero is not architecture — it's fingerprint depth, identity resolution, and the query layer.

---

## Part 3 — The core architectural thesis

### 3.1 Three layers most platforms collapse into one

The deepest problem in your last debugging session, and in this product category generally, is that three genuinely different kinds of statement get stored in the same shape:

| Layer | Statement | Truth conditions | Mutability |
|---|---|---|---|
| **Observation** | "at 14:03 UTC, port 22 returned these bytes" | true by construction | **immutable, forever** |
| **Assertion** | "this service is OpenSSH 7.4 on this asset" | true given a parser and an identity model | revisable when parsers improve |
| **Finding** | "this asset is vulnerable to CVE-X" | true given assertions and a rule | recomputed whenever rules change |

A finding is a *function* of assertions; an assertion is a *function* of observations. Store all three separately, with the function recorded, and every question becomes answerable: why does this finding exist, why doesn't that one, what changed, what did we believe last Tuesday.

Collapse them — which is what a plugin that returns a verdict and discards its input does — and you get a system where "no finding" has no explanation, which is exactly the wall you hit.

Your `scan_results` is the observation layer and it is already correct. **The assertion layer is what you're missing.** Right now you go straight from raw facts to findings, which is why detection rules end up reaching into raw payload paths like `smb.data.smbv1_enabled` and why an agent-side rename silently breaks them.

A fourth provenance class matters too: **imported conclusions**. When you ingest Nuclei output or an EDR export, that is a third party's opinion, not your evidence. Laundering it into first-party fact is how platforms end up unable to explain their own findings. Keep it tagged and adjudicate it separately.

### 3.2 Asset identity is the load-bearing wall

Everything downstream — dedup, trend lines, SLA clocks, remediation verification, the exposure variable in BOD 26-04 — depends on correctly answering "is this the same machine I saw last week?"

Almost everyone keys on IP. **IP-keyed identity isn't imprecise, it's wrong in both directions**, and I built it out to be sure. From `evidence_store.py`, three real machines observed over 30 days with ordinary DHCP behaviour:

```
1. ASSET IDENTITY -- 3 real machines, 30 days, ordinary DHCP churn
  fingerprint identity : 3 assets, 0 conflicts
  IP-keyed identity    : 3 buckets
  ...but HOST_A's 34 observations land in 2 different IP buckets (one machine, split)
  ...and IP bucket 10.0.0.9 contains 2 different real machines (merged)
  Every SLA clock and trend line built on IP identity is measuring noise.
```

The bucket count happens to be right. The groupings are wrong. One machine is split across two buckets, and two machines are merged into one because a DHCP lease got reused.

The correct algorithm is not "prefer better keys." It is:

> **Strong identity keys must both MERGE and SEPARATE.** Two observations sharing an IP but disagreeing on SSH host key are different machines. Two observations with different IPs but the same host key are one machine.

Key strength order: `machine_id` (agent, authoritative) → `ssh_host_key` / `tls_cert_sha256` (survive IP change, survive reimage-preserving-keys) → `mac` (stable per NIC, but VM clones collide) → `hostname` (a label humans reuse) → `ip` (a location, not an identity). Hostname may only link observations that carry no strong key at all, and must be marked low-confidence. Identity confidence should be a first-class field, surfaced in the UI, because an asset resolved by hostname alone deserves less trust than one resolved by machine ID.

### 3.3 What the evidence store buys you

Three capabilities that competitors cannot retrofit without keeping evidence they threw away:

**Retroactive detection.** A CVE drops. You write the rule and answer for the whole fleet across your full retention window, in milliseconds, with zero packets sent:

```
2. RETROACTIVE DETECTION -- a CVE drops today, no rescan
  as of today       : vulnerable=0  clean=3  unknown=0
  as of 15 days ago : vulnerable=1  clean=0  unknown=2
  as of 25 days ago : vulnerable=1  clean=0  unknown=2
```

Under the plugin model this is a rescan: hours to days, customer coordination, change windows. Under the evidence model it is a query. In a world where time-to-exploit is measured in hours, **time-to-answer is the competitive metric**, and it is an architectural property, not an optimisation.

**Honest coverage.** Every check has three possible answers, not two:

```
3. HONEST COVERAGE -- the number nobody reports
  SMBv1 check: 1 vulnerable, 0 clean, 2 UNANSWERABLE
  Honest coverage: 33.3% of assets
```

A dashboard reporting "1 finding" here is technically true and operationally a lie: two thirds of the fleet was never assessed. Given §1.4, this is not a hypothetical failure mode — it is the industry's normal operating state, unreported.

**Evidence-verified remediation.** A closed ticket is a claim. A state transition backed by observations is a fact:

```
4. REMEDIATION VERIFIED BY EVIDENCE, NOT BY A CLOSED TICKET
  2026-07-30  vulnerable
  2026-08-19  not_vulnerable
```

This is CTEM's mobilization stage with actual proof attached, and it's the artifact an auditor wants.

**A bug worth naming, because I hit it building this.** My first implementation OR-ed the answer over history: any past match meant currently vulnerable. Two tests failed, and the failure is a real defect that ships in production systems — a host patched last week stays "vulnerable" forever and no finding ever closes. It looks like diligence and it is a broken close-loop. **Current state must come from the latest qualifying observation; history is preserved separately as `first_seen_vulnerable` and the timeline.** There's now a regression test named for it.

---

## Part 4 — Target architecture

```
L0  COLLECTION      probe / agent — deliberately stupid, emits verbatim facts,
                    versioned collectors, zero detection logic
                          │
L1  OBSERVATION     immutable, append-only, provenance-tagged, tenant-scoped,
                    retained. THE PRODUCT.
                          │
L2  IDENTITY &      entity resolution (fingerprint keys, merge+separate),
    ASSERTION       normalization to product identity, confidence scores
                          │
L3  DETECTION       versioned rules with declared input contracts, executed
                    deterministically, full per-evaluation trace  ← prior doc
                          │
L4  VALIDATION      safe proof-of-exposure, evidence-producing, non-destructive
                          │
L5  PRIORITIZATION  BOD 26-04 / SSVC tiers + EPSS + reachability + business context
                          │
L6  MOBILIZATION    tickets, owner routing, evidence-verified closure
                          │
L7  ATTESTATION     coverage reports, provenance chains, VEX export, audit trail
```

### L0 — Keep the probe stupid

Every line of detection logic in the agent is a line you cannot fix without a fleet redeploy, and a decision whose inputs you did not keep. Your log already states this intent. Enforce it: the probe emits facts and nothing else, tagged with `collector_name` and `collector_version` on every observation, because collector version is what lets you explain why an assertion changed six months later.

**Do not rebuild ten thousand checks.** Embed Nuclei and nmap NSE as *fact producers*, capturing raw request/response as evidence, and let the manager adjudicate. This is what runZero does and it is correct. The impedance mismatch is real — those tools emit verdicts, you want facts — and the resolution is the `imported` provenance class: keep their conclusion, keep the raw exchange, adjudicate separately, never merge the two.

### L1 — Observations are the product

Immutable. Append-only. Tenant-scoped. Provenance-tagged. Retained long enough to be useful — 90 days minimum, ideally a year, because retention window *is* retroactive-answering window.

Cost concern is real and manageable: compress, tier to object storage after 30 days, deduplicate identical consecutive fact blobs by fingerprint (your log already computes one). Most observations are unchanged from the previous scan; store the delta and the fingerprint.

Design constraint: **an observation is never edited, never deleted except by retention policy, and never interpreted at write time.** Interpretation happens at L2 and is always recomputable.

### L2 — The layer you're missing

```python
@dataclass(frozen=True)
class Assertion:
    asset_key:      str          # from identity resolution
    subject:        str          # "service:22/tcp"
    predicate:      str          # "product_identity"
    value:          dict         # {"vendor":"openbsd","product":"openssh","version":"7.4"}
    confidence:     float
    method:         str          # "banner_regex_v3" | "tls_ja3" | "agent_report"
    observation_id: int          # provenance -- always resolvable to raw bytes
    asserted_at:    datetime
```

Detection rules read **assertions**, not raw fact paths. This is the fix for the schema-drift class of bug from the previous document, moved from detection to prevention: when the agent renames a field, exactly one parser breaks, and the parser has its own tests. Today a rename breaks every rule that reads that path, silently.

The normalization layer is also where you replace what NVD stopped giving you. `banner → {vendor, product, version}` is the job CPE was doing. Own it, version it, test it against a fixture corpus, and you're independent of the enrichment collapse.

### L4 — Validation, done safely

CTEM's validation stage, with a constraint that matters commercially: **prove exposure, don't exploit it.** For most vulnerability classes there's a safe observable that distinguishes "version looks vulnerable" from "actually exploitable here" — protocol negotiation reaching the vulnerable code path, an authentication requirement absent, a mitigating configuration missing, a service reachable from an untrusted segment. Record it as evidence attached to the finding.

The 84% false-urgency reduction figure is the business case. The safety constraint is the moat against BAS vendors, who need change-control approval that a read-only validator does not.

### L5 — Prioritization from your own data

You can natively produce all four BOD 26-04 variables:

| Variable | Source |
|---|---|
| KEV status | CISA KEV feed |
| Exploit automation | CISA Vulnrichment SSVC (`Automatable`) |
| Technical impact | Vulnrichment SSVC (`Technical Impact`) |
| **Asset exposure** | **your own reachability data — nobody else has this** |

Plus EPSS as a tiebreak *within* tier — note EPSS v5 began publishing 2026-06-15, and bulk consumers should pull the daily CSV rather than hammering the per-CVE API. Transcribe the real 16-row table from Appendix A; my implementation marks the interpolated middle rows explicitly and has a monotonicity property test that will catch a transcription error.

### L7 — Attestation as a product surface

Ship the coverage numbers. Ship the provenance chain. Ship VEX output (OpenVEX or CSAF 2.0) so "not affected, because the vulnerable code path is unreachable in this configuration, here is the evidence" becomes machine-readable and exportable to customers' own supply-chain tooling.

This is the piece that converts an engineering property into a sales weapon. When a prospect runs you head-to-head against Nessus and you both report 12 findings, you also report *"and here are the 47 checks Nessus silently could not perform on this fleet."* Given §1.4, that number will not be small.

---

## Part 5 — AI, placed where the evidence supports it

The governing rule, derived from §1.5:

> **AI proposes. Deterministic code disposes. Evidence adjudicates.**
> Every AI-touched artifact must reduce to a deterministic, replayable rule a human approved.

### Where AI belongs

**1. Detection-content compilation — the highest-value use by far.**
Advisory or CVE record in; candidate rule, input contract, and test fixtures out; human review; deterministic execution forever after. This directly attacks the constraint the NVD collapse created — you now need to generate your own enrichment, and rule authoring is the bottleneck. It is also exactly the AIxCC shape: generation with mechanical verification. The rule either fires correctly on the fixture corpus or it doesn't, and the model never touches the customer's answer.

Target metric: **time from advisory publication to tested detection in production.** Days to hours is a defensible, measurable claim.

**2. Fact normalization and entity resolution (L2).** Messy banners into structured product identity; ambiguous fingerprints into asset identity. Constraints: emit confidence, allow "unknown" as a legitimate output, and always cache the deterministic mapping so the same input yields the same assertion. Never let the model re-decide at query time.

**3. Triage narration, strictly grounded.** The model explains a verdict the rule engine produced; it never produces the verdict. Input is the detection trace. If the trace says `missing_input: smb.data.smbv1_enabled`, the model writes the sentence a human wants to read. It cannot invent a finding because it isn't asked for one.

**4. Adversarial testing of your own content.** Generate fact payloads designed to make a rule misfire; mutation-test the detection corpus. This is the mutation-testing discipline from the previous document, scaled. Verifiable rewards, safe failure mode.

**5. Remediation authoring.** Config diffs, patch instructions, rollback plans — human-reviewed, and the *verification* is always the next observation, never the model's say-so.

### Where AI does not belong

**The runtime detection decision.** Non-negotiable. Inconsistency across identical runs is a security defect; a scanner that answers differently on Tuesday is unshippable and, in a regulated setting, indefensible.

**Autonomous exploitation as a core loop.** Under 15% success on realistic tasks, and the failure modes are unbounded. Fine as a research track, not as the product.

**Anything that ingests collected banners as instructions.** Your probe collects text from hosts an attacker may control. That is a prompt-injection channel straight into your platform, and 94.4% of agent systems tested were vulnerable. **All collected facts are untrusted data, never instructions**, at every layer. Structure the boundary so that violating this requires deliberate effort.

### The uncomfortable strategic question

Forrester's Project Glasswing analysis argues AI-driven discovery will break the vulnerability management playbook and that signature-based network scanners will give way to AI-based tools. Read carefully, that threat lands on the **content-supply** model, not on the evidence model. If vulnerability discovery accelerates by an order of magnitude, the platform that can turn a new advisory into a tested detection in an hour and answer retroactively across 90 days of stored evidence gets *stronger*, while the platform waiting on NVD enrichment and quarterly rescans gets buried.

Their conclusion — that the limiting factor is now absorbing and acting rather than finding — is an argument for exactly the architecture in Part 4.

---

## Part 6 — Areas of improvement, ranked

Ranked by (leverage × structural advantage) ÷ effort. The first four are cheap because your data model already supports them.

### Tier 0 — Do these; they're nearly free given what you have

| # | Gap | Why it matters | Effort |
|---|---|---|---|
| 1 | **No assertion layer** | Rules read raw payload paths, so agent renames break detection silently. This is the root cause of the drift class from the prior doc, and the replacement for NVD's CPE. | M |
| 2 | **No asset identity resolution** | Findings don't dedupe, trend lines are noise, SLA clocks are wrong, remediation can't be verified. Load-bearing for everything else. | M |
| 3 | **Retroactive detection not exposed** | You already store the facts. This is a query layer over data you have, and it's a headline capability. | S |
| 4 | **Coverage attestation not shipped** | §1.4 says this is the industry's unreported failure. Highest differentiation per unit of work in the whole list. | S |

### Tier 1 — Differentiation

| # | Gap | Why | Effort |
|---|---|---|---|
| 5 | **Fingerprint depth** | runZero profiles ~1,000 attributes; the F5-as-CentOS example shows shallow fingerprinting misleads triage. Depth compounds: every attribute is a future detection you can answer retroactively. | L |
| 6 | **No exposure/reachability model** | BOD 26-04 variable one. The one input no competitor can source. | M |
| 7 | **No safe validation stage** | CTEM's V; the 84% false-urgency reduction. | L |
| 8 | **No VEX / attestation export** | Turns evidence into a customer-facing artifact and a compliance deliverable. | S |
| 9 | **Third-party imports not provenance-separated** | Once Nuclei output is laundered into first-party facts, you can no longer explain your own findings. | S |

### Tier 2 — Scale and operations

| # | Gap | Why | Effort |
|---|---|---|---|
| 10 | **Rule version not stamped on findings** | Without it, "why did this appear/disappear?" is unanswerable across content updates. | S |
| 11 | **Single outbox worker; no partitioning** | Covered in the prior doc. Add `SKIP LOCKED` for horizontal scale. | S |
| 12 | **Observation retention/tiering unplanned** | Retention window = retroactive-answering window. Needs a cost model before it becomes a bill. | M |
| 13 | **No cross-asset correlation** | Attack paths need a graph over assertions, not per-host findings. | L |
| 14 | **No detection-content CI pipeline** | Prerequisite for AI-assisted authoring; without it, generated rules are unshippable. | M |

### Where I'd start on Monday

**Item 4, coverage attestation, then item 3, retroactive detection.** Both are query layers over data already on disk, both are demo-able in a sales call, and both are impossible for a plugin-architecture competitor to answer. Ship item 1 next, because it's the structural fix that stops the drift class recurring. Item 2 is the biggest, and everything past Tier 0 depends on it, so start the design now even if implementation lags.

---

## Part 7 — Positioning

The one-sentence version:

> **Every scanner tells you what it found. Vedha also tells you what it checked, what it couldn't, and why — and can answer tomorrow's CVE against yesterday's evidence without touching your network.**

Three claims, all defensible, all technically grounded:

1. **Measured coverage, not claimed coverage.** Publish your own benchmark against vulhub the way Pentest-Tools did. If your coverage is lower than Nessus's but you *report the gap*, that is a stronger position than a silent 3x overstatement — and it is verifiable.
2. **Time-to-answer, not time-to-scan.** New CVE to fleet-wide answer, measured in minutes, without a rescan.
3. **Evidence-grade findings.** Every finding traces to the exact bytes observed, at a timestamp, by a named collector version. Every non-finding has a reason. Exportable as VEX.

Metrics worth instrumenting from day one, because they are the product:

- Time from advisory publication → tested detection in production
- Coverage ratio: checks assessed ÷ checks applicable, per engagement
- Retroactive answer latency, p50 and p99
- Identity confidence distribution across the fleet
- Findings closed by verified evidence ÷ findings closed by ticket

---

## Appendix — Reference implementation

`vedha_ref/` runs on stdlib Python 3.12, no install, no network. **45 tests passing.**

| File | What it proves |
|---|---|
| `pipeline.py`, `test_pipeline.py` | Pipeline correctness: reconciled state machine, leased outbox, detection trace, SSVC tiers (34 tests) |
| `fuzz_invariants.py` | 11 invariants under randomised interleaving; independent oracle (75,000 states, 0 violations) |
| `mutation_test.py` | 6 injected real bugs, all killed; found a genuine hole in my own suite |
| `evidence_store.py`, `test_evidence_store.py` | **This document:** provenance separation, identity resolution, retroactive detection, time travel, coverage honesty (11 tests) |

```bash
cd vedha_ref
python3 -m unittest discover -q            # 45 tests
python3 test_evidence_store.py demo        # the four numbers in Part 3
python3 fuzz_invariants.py 1500 50         # 75,000 states
python3 mutation_test.py                   # 6/6 mutants killed
```

### Sources for the market claims

- NIST, *NVD Operations Update* (2026-04-17) — enrichment criteria and the "Not Scheduled" reclassification
- CSA Lab Space research notes on the NVD triage overhaul (2026-04/05) — CPE gap analysis, VulnCheck 41.35% vs 76.95% coverage
- CISA, *BOD 26-04: Prioritizing Security Updates Based on Risk* (2026-06-10) and its implementation guidance
- CISA Vulnrichment / SSVC decision points (`Exploitation`, `Automatable`, `Technical Impact`)
- FIRST, *EPSS Data* — v5 publishing from 2026-06-15; bulk CSV vs API guidance
- Pentest-Tools.com, *Network Vulnerability Scanner Benchmark* (2024) — 167 vulhub environments
- DARPA, *AIxCC Results* (2025-08) and *SoK: DARPA's AI Cyber Challenge*, USENIX Security '26
- *A Survey of LLM-Driven Penetration Testing* (arXiv, 2026-06) — 81 papers, declining success rates
- Princeton SAGE, *RFC on AI Agent Security* — inconsistency as a security property
- Forrester, *Project Glasswing Shows That AI Will Break The Vulnerability Management Playbook* (2026-04-08)
- Verizon DBIR 2026 via Tenable — 26% KEV remediation rate, 43-day median
- runZero platform and exposure-management documentation — fingerprint-and-query architecture
