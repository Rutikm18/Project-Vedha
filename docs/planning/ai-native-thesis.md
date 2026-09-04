# Vedha — The AI-Native VAPT Plan

> A founder-grade strategy memo. Written to be argued with, not admired.
> Frame: think like a Silicon Valley founder deciding where to point the next 18 months, backed by top-1%-researcher rigor about what is actually *true* right now in AI-for-offensive-security.
>
> Author's stance: Vedha's current architecture is a genuine asset that most AI-pentest startups **do not have** — a real, sealed, distributed probe that runs inside customer networks and speaks a numeric use-case protocol to a manager. The mistake would be to throw that away and chase XBOW's web-app demo. The opportunity is to weld an AI-native brain onto the distributed-sensor body we already own. That combination is the whitespace.

Date: 2026-08-20 · Status: living document · Owner: Rutik

---

## 0. TL;DR — the one paragraph that matters

The market is bifurcating into two AI-offensive archetypes: **(A) autonomous web-app exploiters** (XBOW — #1 on HackerOne, $75M, machine-speed bug bounty) and **(B) continuous internal exposure validators** (Horizon3 NodeZero, Pentera — the "AEV/CTEM" category Gartner is formalizing). Vedha is architecturally a **B** (distributed probe inside the network, AD/Neo4j attack-pathing, numeric use-cases) but is being *tempted* to demo like an **A**. The academic reality is brutal and clarifying: the best published autonomous pentest agents solve only **~31% end-to-end** (PentestEval), and fully-autonomous agents "fail almost entirely." That means **the winning product is not "an AI that hacks"** — it is **an AI that turns raw distributed sensor data into validated, proof-carrying, prioritized attack paths, with a human-in-the-loop who trusts it because every finding ships with a reproducible PoC.** Vedha's moat is the probe (real ground truth, hard to replicate) + a validation loop that refuses to emit a finding it can't prove. The Anthropic-specific edge: build the whole thing so that *defensive refusal bias* and the *cyber safety classifier* become **our differentiator, not our tax** — a properly-scoped, authorization-gated, proof-carrying agent is exactly the shape of request the models are being trained to *allow*, while everyone hacking around guardrails is building on sand.

---

## 1. Where Vedha actually is today (honest current-state)

Grounding this in the real codebase, not aspiration:

| Layer | What exists | Strength | Latent gap |
|---|---|---|---|
| **Probe** (`probe/agent`, Nuitka-sealed, Ed25519 host-locked license) | Distributed executor inside customer LAN; dials out only; zero inbound surface | **This is the crown jewel.** Real ground truth; IP-protected; hard to clone | Enrollment/lifecycle brittleness (just hit the 409/refresh bug); no fleet-level orchestration brain |
| **Scanner** (`main_scripts` ≡ `scanner/`) | Strong host discovery, port/service, TLS/web/SMB/SNMP/UDP, OS fingerprint, IoT/OT/AI-MCP branches | Broad, accurate primitives; drift-guarded | Built-but-not-wired accuracy features (adaptive timeout, AIMD, SYN retransmit, accuracy corpus) |
| **Manager backend** (`manager/backend`, fully async) | Engagement/Asset/Finding/ScanJob model; numeric use-case dispatch (uc 1–81 × intensity 1–3) over WebSocket; scope-gated | Clean domain model; god nodes are the right ones (`Finding`, `Engagement`, `Asset`) | The "manager" is a dispatcher, not yet a *reasoner* |
| **AD / graph** | BloodHound.py collector + Neo4j ingest; MemberOf/attack edges | Attack-path substrate already present | Not yet fused with LLM planning or exposure scoring |
| **AI layer** (`app` LLM manager service) | Multi-provider httpx client, **pinned to Claude Sonnet 4.6** | Provider-abstracted, key-safe | Under-used: summarization, not agency. No agent loop, no validation loop, no memory/RAG over scan corpus |

**The one-sentence diagnosis:** Vedha has an excellent *body* (sensors, protocol, domain model) and a *vestigial brain*. Every competitor is racing to build a brain; almost none of them have a body like ours. **Build the brain onto the body.**

---

## 2. The landscape — who's doing what, and with which tech

### 2.1 United States

- **XBOW** — the headline. Autonomous AI pentester, **#1 on HackerOne's global leaderboard** (HackerOne then split human vs machine rankings — a category-defining moment), **$75M Series B (Northzone)**, "Pentest On-Demand" from **$4,000**, results in ~5 business days, no scoping calls. Tech shape: specialized agents that **chain vulnerabilities into real attack paths**, self-service, web-app-centric. *Weakness we can exploit:* it lives at the web-app/bug-bounty layer and is outside-in; it does not live *inside* the network with a trusted sensor doing AD/lateral-movement/OT.
  - [XBOW: how it ranked #1](https://xbow.com/blog/top-1-how-xbow-did-it) · [Pentest On-Demand](https://www.businesswire.com/news/home/20251112470912/en/Announcing-XBOW-Pentest-On-Demand-for-Security-at-Machine-Speed) · [Series B / $75M](https://it.slashdot.org/story/25/07/05/1847237/xbows-ai-powered-pentester-grabs-top-rank-on-hackerone-raises-75m-to-grow-platform)
- **Horizon3.ai / NodeZero** — **autonomous, agentless** internal+external pentest; no persistent implant or stored creds; chains misconfig+credential+exposure into attack paths. This is the closest philosophical competitor to where Vedha *should* go — except **Vedha has a sealed persistent probe**, which is a different (and for continuous/OT/air-gapped-ish environments, superior) deployment model.
  - [Horizon3 vs Pentera (Gartner Peer Insights)](https://www.gartner.com/reviews/market/adversarial-exposure-validation/compare/horizon3-ai-vs-pentera) · [Automated pentest platform comparison](https://generalanalysis.com/guides/best-automated-penetration-testing-tools)
- **Pentera** — automated internal pentest (password cracking, credential reuse, **Kerberoasting**, lateral movement) + EASM; **AI web attack testing w/ AI payload generation launched Aug 2025**. Mature, 300+ reviews.
- **MindFort, Cobalt, Picus, Hadrian** — the widening middle: PtaaS, breach-and-attack-simulation, EASM, all bolting on AI. [MindFort on Pentera alternatives](https://www.mindfort.ai/blog/best-pentera-alternatives) · [Hadrian on the 2026 Gartner AEV guide](https://hadrian.io/blog/what-the-2026-gartner-r-market-guide-for-adversarial-exposure-validation-means-for-offensive-security)

### 2.2 Israel

- **Terra Security** — the one to study. Founded 2024, **$30M Series A (Felicis, Dell Tech Capital), $38M total**, **agentic-AI continuous pentest with an explicit human-in-the-loop**, "tailored, context-aware," already Fortune 100 clients, won the AWS/CrowdStrike/NVIDIA accelerator. On the **Rising in Cyber 2026** list. Their thesis — *agentic + continuous + human-in-the-loop + context-aware* — is almost exactly the right thesis. Vedha's counter-position: **we own the in-network sensor; they're mostly outside-in web.**
  - [Terra $30M / SecurityWeek](https://www.securityweek.com/terra-security-raises-30-million-for-ai-penetration-testing-platform/) · [Agentic AI framing / TechTime](https://techtime.news/2025/09/16/terra-security/) · [Ctech](https://www.calcalistech.com/ctechnews/article/awdq1yv5k)
- **Cymulate** — BAS/CTEM incumbent; the CTEM vocabulary owner. [What is CTEM](https://cymulate.com/blog/what-is-continuous-threat-exposure-management/)
- The broader Israeli cluster (Cyera, Orca, Oligo, Noma, Token, Grip…) shows where capital and talent concentrate — data security and AI security. Offensive-AI is the adjacent, less-crowded lane. [Rising in Cyber 2026 — Israel](https://www.israeldefense.co.il/en/node/69001)

### 2.3 Academia (the reality check that should shape our whole design)

This is the most important section for a *researcher-grade* plan, because it tells us what is genuinely hard and therefore where the defensible engineering is.

- **PentestEval (arXiv 2512.14233)** — the sobering benchmark. Decomposes pentest into stages (Info Collection → Weakness Gathering → Attack Decision → Exploit Gen/Revision), 346 tasks, 12 scenarios. **End-to-end pipelines reach only ~31%. PentestGPT, PentestAgent, VulnBot show similar limits; fully-autonomous agents "fail almost entirely."** → *The product truth: don't sell autonomy, sell validated leverage.* [abs](https://arxiv.org/abs/2512.14233)
- **VulnBot (arXiv 2501.13411)** — multi-agent (recon/scan/exploit), **task-graph planner**, inter-agent comms; ~**30% completion** even at Llama-3.1-405B. Multi-agent helps but isn't magic. [html](https://arxiv.org/html/2501.13411)
- **PentestAgent / Autosecagent** — **RAG + recursive memory** across stages; the recurring winning primitive is *retrieval over a knowledge base + memory across a multi-step chain*. [Autosecagent (Springer)](https://link.springer.com/article/10.1007/s11227-026-08439-z) · [PentestAgent review](https://www.themoonlight.io/en/review/pentestagent-incorporating-llm-agents-to-automated-penetration-testing)
- **Multi-Agent Pentest for the Web (arXiv 2508.20816)** — Coordinator + per-job Docker **Sandbox** agents + a **Validation agent that converts candidate findings into verified end-to-end PoCs**. *This is the architectural pattern Vedha should adopt wholesale.* [pdf](https://arxiv.org/pdf/2508.20816)
- **Benchmarks to measure ourselves against:** Cybench (40 pro CTFs; Claude 3.7 Sonnet solved ~⅓ within 5 attempts, up from ~5% a year earlier — *capability is climbing fast*), AutoPenBench, PACEbench, AgentCyberRange, and "AI Agents vs Cybersecurity Professionals in real-world pentesting" (arXiv 2512.09882). [Cybench](https://openreview.net/forum?id=tc90LV0yRL) · [PACEbench](https://arxiv.org/pdf/2510.11688) · [AutoPenBench](https://arxiv.org/pdf/2410.03225) · [AI vs pros](https://arxiv.org/pdf/2512.09882)

**Synthesis of the literature into three design laws:**
1. **Autonomy is ~30% today and rising ~6× year-over-year.** Design for a *rising tide*: a human-in-the-loop product now that silently converts to more autonomy as models improve — without a rewrite.
2. **The reliable primitives are: multi-agent decomposition, RAG over a domain corpus, cross-step memory, and a sandbox-backed validation agent.** These aren't optional flourishes; they're the difference between 5% and 31%.
3. **The hard, valuable part is *validation* (proof-carrying findings), not *ideation*.** LLMs hallucinate exploits; a validation loop is what makes output trustworthy — and trust is the entire sale.

---

## 3. The market wind at our back — CTEM / AEV

Gartner formalized **CTEM** (Continuous Threat Exposure Management) in 2022 and predicted orgs running it would be **~3× less likely to breach**; the 2026 framing is a **hard shift from point-in-time pentests to continuous, automated, evidence-based validation.** Gartner now maintains a **Market Guide for Adversarial Exposure Validation (AEV)** and, as of **Nov 2025**, a first **Magic Quadrant for Exposure Assessment Platforms.** AEV = *"consistent, continuous, automated evidence of the feasibility of an attack."*

That definition is a gift: **"continuous automated evidence of attack feasibility"** is *exactly* what a persistent in-network probe + a validation-first AI brain produces. Vedha should stop describing itself as "AI pentest" (crowded, XBOW owns the mindshare) and position as **"AI-native Adversarial Exposure Validation — continuous, in-network, proof-carrying."**

Sources: [Gartner AEV 2026 (Hadrian)](https://hadrian.io/blog/what-the-2026-gartner-r-market-guide-for-adversarial-exposure-validation-means-for-offensive-security) · [CTEM guide 2026](https://www.armorcode.com/learning-center/the-ultimate-guide-to-continuous-threat-exposure-management-ctem) · [Terra: top CTEM vendors](https://www.terra.security/blog/top-ctem-vendors)

---

## 4. The Anthropic angle — turning model limitations into moats

The user asked specifically about **Anthropic/Mythos model limitations we can leverage.** Here is the rigorous version, grounded in the current Claude API facts (not folklore), with each limitation converted into a **product decision.**

### 4.1 The limitations that actually matter for a VAPT product

| # | Limitation (accurate, current) | Why it bites a security product | The move |
|---|---|---|---|
| **L1** | **Cyber safety classifier + `stop_reason:"refusal"`.** On **Claude Fable 5 / Mythos 5** the safety classifiers *specifically target most cybersecurity content* — Fable 5 is explicitly "not intended for" cyber, and benign security tooling triggers **false-positive refusals**. Refusals return HTTP 200 with `stop_details.category:"cyber"`. | An offensive-security agent on Fable 5 will randomly refuse mid-engagement. Research corroborates it: frontier models refuse **2–3 of 5** legit security runs ("Defensive Refusal Bias"). | **Pin the agent to `claude-opus-4-8`, not Fable/Mythos**, for the offensive loop (Opus 4.8 is the durable, capable, security-tolerant tier). Reserve Fable/Mythos for *non-cyber* tasks (report prose, exec summaries). Build a **refusal-handling layer**: detect `stop_reason=="refusal"`, and use the **server-side `fallbacks` parameter** (`betas:["server-side-fallback-2026-06-01"]`, `fallbacks:[{"model":"claude-opus-4-8"}]`) so a stray refusal is transparently re-served instead of failing an engagement. |
| **L2** | **Defensive Refusal Bias** — safety-tuned models refuse *authorized defensive* tasks when the text merely *contains offensive-sounding keywords*. Bypass tricks that work (scope/RoE, localhost-proxying) are exactly the ones attackers use — so they'll be *closed*. | If we prompt like a hacker, we get refused; if we jailbreak, we're on sand that Anthropic will sand-blast. | **Make authorization structural, not textual.** Every agent action carries a signed **engagement authorization + scope + RoE** object. Emerging governance says agents *should refuse based on environmental context, not just the user's words* — so we **feed the model the context that makes compliance correct**: signed scope, customer consent record, target-in-scope proof. This is a **moat**: we are the vendor whose requests are *designed to be allowable*, so we ride model upgrades instead of fighting them. [Defensive Refusal Bias](https://arxiv.org/html/2603.01246v1) · [Content-based refusal framework](https://arxiv.org/pdf/2602.15689) |
| **L3** | **ZDR / 30-day retention constraint on Fable 5** (400s under zero-data-retention). Security customers *demand* ZDR. | Our most privacy-sensitive customers can't use the most-capable model. | Standardize on **Opus 4.8** (no ZDR block) for the engagement brain; offer a **customer-hosted / BYO-key + ZDR** tier. Make "your scan data never trains a model, ZDR-compatible" a **sales line**, not a footnote. |
| **L4** | **Non-determinism** (`temperature`/`top_p` removed on 4.7/4.8; adaptive thinking only). | Pentests must be *reproducible* for compliance/audit. | Determinism can't come from the model — it must come from **us**: proof-carrying findings, recorded tool traces, replayable PoCs, and a **result cache keyed on (scope, use-case, target-state hash).** The *evidence* is deterministic even when the *reasoning* isn't. |
| **L5** | **Context + cost at fleet scale.** 1M context is large but a 100-probe continuous fleet generates far more. Long agentic turns can run *minutes*. | Naively shoving all scan output into the model is bankrupting and slow. | Use **RAG over our own scan corpus** (retrieve only relevant assets/findings), **compaction** (beta `compact-2026-01-12`) and **context editing** for long runs, **prompt caching** on the stable scope/RoE prefix (huge cost win on a fleet), and **effort tiering** (`low` for triage/summarization, `high`/`xhigh` for exploit reasoning). Batch non-urgent analysis via the **Batches API (50% cheaper).** |
| **L6** | **Thinking is never fully exposed / raw CoT withheld.** | We can't audit the model's private reasoning for a compliance trail. | Don't rely on CoT for the audit trail. The audit trail is the **tool-call transcript + PoC + evidence artifacts**, which we control and can sign. (Nice side effect: this is also more trustworthy to an auditor than "the AI thought….") |

### 4.2 The meta-move

Everyone else treats the safety layer as friction to jailbreak around. **We treat it as a spec.** Anthropic is actively building toward *context-aware* refusals for agents (refuse based on environment, not keywords) and even **disrupted an AI-orchestrated espionage campaign in late 2025** — meaning they will keep tightening keyword-based misuse while *opening* well-scoped authorized use. A product architected around **signed authorization + in-scope proof + proof-carrying output** is on the right side of that curve. That's not compliance theater; it's **durability**: our stack gets *more* capable with each model release instead of breaking. [Anthropic: building AI for cyber defenders](https://www.anthropic.com/research/building-ai-cyber-defenders) · [A framework for cybersecurity refusals in AI agents](https://arxiv.org/pdf/2606.02644)

---

## 5. The AI-native architecture we should build

This is the concrete engineering thesis. It fuses the reliable academic primitives (§2.3) onto Vedha's existing body (§1).

```
                         ┌───────────────────────────────────────────────┐
                         │  VEDHA MANAGER  (cloud, async, Opus 4.8 brain) │
                         │                                                │
  Engagement + signed    │   ┌────────────┐   retrieves   ┌────────────┐  │
  Authorization/Scope ──▶│   │ORCHESTRATOR│◀────RAG───────│ Scan Corpus │  │
  /RoE object            │   │  (planner) │   (assets,    │ (pgvector + │  │
                         │   └─────┬──────┘   findings,   │  Neo4j AD)  │  │
                         │         │ delegates KB/CVE)    └────────────┘  │
                         │   ┌─────▼─────┬──────────┬─────────────┐        │
                         │   │ Recon     │ Exploit  │ AD/Path     │  ...   │
                         │   │ Agent     │ Agent    │ Agent       │        │
                         │   └─────┬─────┴────┬─────┴──────┬──────┘        │
                         │         │ numeric use-cases (uc×intensity)       │
                         │   ┌─────▼──────────▼────────────▼──────┐        │
                         │   │  VALIDATION AGENT  (the moat)       │        │
                         │   │  candidate finding → sandbox PoC →  │        │
                         │   │  proof-carrying finding OR discard  │        │
                         │   └─────────────────┬───────────────────┘        │
                         │       Episodic MEMORY across the engagement       │
                         └─────────────────────┼───────────────────────────┘
                                               │ WebSocket (dial-out)
                    ┌──────────────────────────┼──────────────────────────┐
                    │        SEALED PROBE FLEET (inside customer LANs)      │
                    │   scanner primitives · AD collector · TLS/web/SMB…    │
                    │   per-job sandbox execution · zero inbound surface    │
                    └──────────────────────────────────────────────────────┘
```

**The seven components, each mapped to a proven primitive:**

1. **Orchestrator / Planner** — decomposes an engagement into a **task graph** (VulnBot's win), decides which `uc×intensity` to dispatch to which probe, and re-plans on new evidence. Runs on Opus 4.8 at `high`/`xhigh` effort with a **Task Budget** so a run paces itself.
2. **Specialist agents** (Recon, Service/Web, Exploit, **AD/Attack-Path**, Cloud, OT/IoT) — thin planners that map intent → Vedha's *existing* numeric use-cases. **We already have the tools; the agents just choose and sequence them.** This is our unfair advantage: competitors are building tools *and* brains; we're mostly adding the brain.
3. **RAG over our own corpus** — pgvector index of assets/services/findings + a curated CVE/technique KB + the **Neo4j AD graph** as a first-class retrieval source. The model retrieves *only* the relevant slice → controls cost (L5) and grounds reasoning (cuts hallucination).
4. **Episodic memory** — per-engagement memory file (Autosecagent's recursive memory) so a multi-day continuous engagement accrues context instead of re-deriving it. Also the substrate for "learned tradecraft" (see §7).
5. **The Validation Agent — the entire moat.** No finding is emitted unless it is reproduced end-to-end in a **per-job sandbox** and packaged as a **proof-carrying finding**: the exact steps, the observed evidence, a replay script, and a scope check. This is what pushes us from "31% of AI ideas are right" to "100% of shipped findings are true." **A finding without a PoC is a hypothesis, and we don't sell hypotheses.**
6. **Authorization plane (§4.2)** — signed engagement + scope + RoE injected into every model call and enforced at the probe (we already scope-gate). This is what makes the AI *allowable* and *auditable*.
7. **Human-in-the-loop review** — Terra's proven shape. The human reviews *proof-carrying* findings and approves the risky escalations. As models climb the Cybench curve, we **dial autonomy up per-customer** without re-architecting.

**Why this specific design wins:** it is the *only* configuration that is simultaneously (a) grounded by real in-network sensor data we already collect, (b) built from the exact primitives the literature shows actually work, (c) trustworthy because every output is proven, and (d) on the right side of the model-safety curve.

---

## 6. How AI makes Vedha *categorically* different from traditional VAPT

The differentiation matrix — the slide a founder shows an investor:

| Dimension | Traditional pentest / scanner | Vedha AI-native AEV |
|---|---|---|
| **Cadence** | Point-in-time, 1–4×/year | **Continuous** (persistent probe + always-on brain) |
| **Output** | 80-page PDF of *possible* issues, ~40% false positives | **Proof-carrying findings** — each with a reproducible PoC or it isn't shipped |
| **Prioritization** | CVSS list (context-free) | **Attack-path reachability** — "this exposure + these creds → domain admin," ranked by real feasibility (AEV) |
| **Scaling** | Linear in human hours (~$4k–$30k/engagement) | Marginal cost ≈ tokens + probe compute; **fleet-parallel** |
| **Coverage** | What the human had time for | Whole fleet, every use-case, every night |
| **Trust model** | "Trust the consultant's brand" | **"Trust the proof"** — replayable evidence, signed authorization, ZDR-safe |
| **Learning** | Resets each engagement | **Memory + corpus** compound across time and customers (privacy-partitioned) |
| **Guardrail posture** | N/A | **Allowable-by-design** — rides model upgrades instead of jailbreaking against them |

The narrative: *Traditional pentest tells you what might be wrong, once a year, and asks you to trust a brand. Vedha proves what is exploitable, continuously, and asks you to trust the evidence.*

---

## 7. The roadmap (PM-style: what / why / how we'll know)

Phased so each phase ships value and de-risks the next. Sequenced against Vedha's existing roadmap (posture scorecard → integrations → portal).

### Phase 0 — Foundation hardening (next 2–4 weeks) · *make the body reliable*
- **What:** Fix probe lifecycle robustness (the 409/refresh/enroll path we just touched), wire the built-but-dormant scanner accuracy features (adaptive timeout, AIMD, SYN retransmit), stand up the accuracy corpus as ground-truth eval data.
- **Why:** An AI brain on unreliable sensors amplifies noise. Accuracy corpus doubles as our **eval harness** (see Phase 4).
- **Metric:** probe enrollment success >99%; scanner precision/recall measured vs corpus.

### Phase 1 — The Validation Agent + proof-carrying findings (weeks 4–10) · *the moat, first*
- **What:** Per-job sandbox execution; a Validation Agent (Opus 4.8) that turns any candidate finding into a reproduced PoC + evidence bundle or **discards it.** Finding schema gains `proof`, `replay_script`, `evidence[]`, `scope_check`.
- **Why:** This is the single highest-trust, highest-differentiation feature and it works *today* even at 31% ideation accuracy — because we only ship the provable subset. Do the moat before the autonomy.
- **Metric:** % of shipped findings with a passing replay; false-positive rate → near-zero.

### Phase 2 — RAG corpus + AD attack-path fusion (weeks 8–16) · *grounding + the killer output*
- **What:** pgvector over assets/services/findings + CVE/technique KB; make the **Neo4j AD graph a retrieval + reasoning source**; Attack-Path Agent that composes exposure + credential + reachability into a ranked **"path to crown jewels."**
- **Why:** This is the AEV output Gartner is naming and that NodeZero/Pentera win on — and we have the AD substrate already.
- **Metric:** time-to-first-attack-path; analyst agreement with ranked paths.

### Phase 3 — Orchestrator + multi-agent continuous engagements (weeks 14–24) · *continuous, at fleet scale*
- **What:** Task-graph Orchestrator; specialist agents mapping to numeric use-cases; episodic memory; prompt-cache the scope/RoE prefix; Batches API for non-urgent nightly analysis; effort-tiering.
- **Why:** Turns Vedha from "scan-on-request" into "always-on validator" — the CTEM promise. Cost engineered from day one.
- **Metric:** cost per engagement; % autonomous vs human-approved actions; cache-read hit rate.

### Phase 4 — Eval-driven autonomy dial + the authorization plane (weeks 20–32) · *durable & safe*
- **What:** Internal benchmark (our corpus + Cybench/AutoPenBench-style tasks); signed engagement/scope/RoE injected into every call; server-side refusal `fallbacks`; per-customer autonomy slider gated on measured pass-rate.
- **Why:** As models climb (Cybench ~6× YoY), we *safely* let go of the wheel — evidence-gated, not vibe-gated. And we're allowable-by-design (§4.2).
- **Metric:** internal-benchmark pass-rate trend; zero unauthorized-scope actions; refusal-recovery rate.

---

## 8. Crazy / moonshot bets (the "think dynamically" section)

These are the 10× swings. Not all survive contact, but a founder should be holding options on them.

1. **Digital-twin continuous validation.** The probe fleet + corpus + Neo4j already approximate a live model of the customer's network. Turn it into a **queryable digital twin**: "if this new CVE dropped tonight, which of my hosts become a path to DA?" — answered from the twin, no rescan. This is *predictive* AEV; nobody ships it because nobody has both the sensor and the graph. **We do.**
2. **Purple-team loop.** Every proven attack path auto-generates the **matching detection/hardening artifact** (Sigma rule, config diff, mitigation PR). We're the only offensive tool that closes its own loop into defense — doubles the buyer (offense *and* SecOps).
3. **Federated tradecraft, privacy-partitioned.** Learn *generalizable* attack patterns across customers (never data), so the fleet gets smarter collectively while each tenant stays isolated — a compounding moat traditional consultancies structurally cannot have.
4. **"Allowable-by-design" as a category.** Publish the signed-authorization + proof-carrying spec as an open standard for AI offensive tooling. Whoever defines how AI hacking is *safely authorized* owns the trust layer — and it aligns perfectly with where Anthropic is pushing (context-aware agent refusals).
5. **Self-writing use-cases.** Today use-cases are numeric and hand-built. Let the agent *propose* new use-case pipelines from novel findings, validate them in the sandbox, and (human-approved) promote them into the numeric catalog. The product's capability surface grows itself. (Fable 5 is explicitly good at updating its own skills mid-task — but keep that on the *non-cyber* planning side to dodge L1.)
6. **The "prove it" button for auditors/insurers.** A cyber-insurer or SOC 2 auditor clicks once and gets a replayable, signed demonstration of exactly which exposures are real. Turns a security tool into a **financial/compliance instrument** — a very different, stickier buyer.

---

## 9. Risks, honestly

- **Model refuses mid-engagement (L1/L2).** Mitigation: Opus 4.8 pinning + server-side fallbacks + structural authorization. *Residual risk: medium, decreasing.*
- **XBOW/Terra move in-network.** They can raise capital to build a probe; we cannot out-fund them. Mitigation: **speed on the fused twin+AD+validation combo**, and the sealed-probe deployment moat for OT/regulated/air-gapped environments they'll reach last.
- **Autonomy over-promised.** The whole plan is built to *not* need autonomy to be valuable (proof-first, human-in-loop). This risk is designed out.
- **Cost blowup at fleet scale.** Engineered against from Phase 3 (RAG, caching, batching, effort-tiering). Watch cache-read ratio like a hawk.
- **Trust incident (an agent acts out of scope).** Existential for a security vendor. The authorization plane + probe-side scope gate + human approval on escalations are non-negotiable, not phase-4 nice-to-haves — pull scope enforcement forward if needed.

---

## 10. North-star metric & the bet

**North star:** *Validated Attack Paths per Customer per Week* (VAP/c/w) — a single number that captures continuous cadence × real coverage × proof (not raw findings, which reward false positives).

**The bet in one line:** The winner of AI-native offensive security will not be the flashiest autonomous hacker — it will be **the most trusted continuous validator.** Trust is manufactured from **proof + authorization + privacy**, and Vedha is the rare team that owns the **sensor** to generate the proof, the **graph** to rank it, and now the **discipline** to only ship what it can prove. Build the brain onto the body, make every finding carry its proof, and be the vendor whose AI is *allowable by design*.

---

### Appendix A — primary sources

**Industry / competitors:** [XBOW #1 HackerOne](https://xbow.com/blog/top-1-how-xbow-did-it) · [XBOW Pentest On-Demand](https://www.businesswire.com/news/home/20251112470912/en/Announcing-XBOW-Pentest-On-Demand-for-Security-at-Machine-Speed) · [XBOW $75M](https://it.slashdot.org/story/25/07/05/1847237/xbows-ai-powered-pentester-grabs-top-rank-on-hackerone-raises-75m-to-grow-platform) · [Horizon3 vs Pentera](https://www.gartner.com/reviews/market/adversarial-exposure-validation/compare/horizon3-ai-vs-pentera) · [Automated pentest platforms 2026](https://generalanalysis.com/guides/best-automated-penetration-testing-tools) · [Terra $30M](https://www.securityweek.com/terra-security-raises-30-million-for-ai-penetration-testing-platform/) · [Terra agentic AI](https://techtime.news/2025/09/16/terra-security/) · [Rising in Cyber 2026 (Israel)](https://www.israeldefense.co.il/en/node/69001)

**Market framing:** [Gartner AEV 2026 (Hadrian)](https://hadrian.io/blog/what-the-2026-gartner-r-market-guide-for-adversarial-exposure-validation-means-for-offensive-security) · [CTEM 2026 guide](https://www.armorcode.com/learning-center/the-ultimate-guide-to-continuous-threat-exposure-management-ctem) · [Cymulate: CTEM](https://cymulate.com/blog/what-is-continuous-threat-exposure-management/) · [Terra: top CTEM vendors](https://www.terra.security/blog/top-ctem-vendors)

**Academia:** [PentestEval 2512.14233](https://arxiv.org/abs/2512.14233) · [VulnBot 2501.13411](https://arxiv.org/html/2501.13411) · [Multi-Agent Pentest for Web 2508.20816](https://arxiv.org/pdf/2508.20816) · [Autosecagent (Springer)](https://link.springer.com/article/10.1007/s11227-026-08439-z) · [PentestAgent review](https://www.themoonlight.io/en/review/pentestagent-incorporating-llm-agents-to-automated-penetration-testing) · [Cybench](https://openreview.net/forum?id=tc90LV0yRL) · [PACEbench 2510.11688](https://arxiv.org/pdf/2510.11688) · [AutoPenBench 2410.03225](https://arxiv.org/pdf/2410.03225) · [AI Agents vs Professionals 2512.09882](https://arxiv.org/pdf/2512.09882)

**Refusal / dual-use / safety:** [Defensive Refusal Bias 2603.01246](https://arxiv.org/html/2603.01246v1) · [Content-based refusal framework 2602.15689](https://arxiv.org/pdf/2602.15689) · [Cybersecurity refusals in AI agents 2606.02644](https://arxiv.org/pdf/2606.02644) · [Anthropic: building AI for cyber defenders](https://www.anthropic.com/research/building-ai-cyber-defenders) · [Anthropic Frontier Red Team](https://www.anthropic.com/news/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team)

### Appendix B — Anthropic model decisions (locked)

- **Engagement brain:** `claude-opus-4-8`, adaptive thinking, effort `high`/`xhigh`, Task Budgets, server-side refusal `fallbacks` → `claude-opus-4-8`. *Not* Fable/Mythos for the cyber loop (cyber classifier / ZDR block).
- **Report prose / exec summaries (non-cyber):** Fable 5 / Mythos 5 acceptable; watch for reasoning-extraction refusals.
- **Triage / summarization / classification:** Sonnet 4.6 or Haiku 4.5 at low effort; Batches API for nightly bulk.
- **Cost controls:** prompt-cache the scope/RoE/system prefix; RAG-retrieve not dump; compaction + context-editing on long runs; verify `cache_read_input_tokens > 0`.
