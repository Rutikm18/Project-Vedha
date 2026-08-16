# Autonomous Offensive-Security AI Agents — Research Report

**Date:** 2026-08-16
**Question:** How do leading companies and researchers build a *fully autonomous*
AI offensive-security / pentest agent as an **agentic control plane** (LLM tool-use
orchestrator) driving existing tooling — and what is the best, evidence-backed
approach for Vedha?

> Method note: the deep-research workflow's parallel search agents hit the account
> session limit and returned 0 sources. I re-ran the searches sequentially from the
> main loop; the findings below are from those primary sources (company engineering
> blogs + arXiv). Fresh, exhaustive multi-agent verification can be re-run after the
> limit resets — treat single-source claims as "reported," not independently verified.

---

## 0. The five findings that should drive Vedha's design

1. **The market leader deliberately does NOT let GenAI write or run exploits.**
   Horizon3.ai NodeZero: *"NodeZero never uses GenAI to create or execute exploits.
   Every action is deterministic, pre-validated, and tested internally."* AI is used
   for orchestration/analysis; the exploitation itself is deterministic. [H3]
2. **Naive "fully autonomous" agents fail catastrophically; structure is what works.**
   Fully-autonomous PentestAgent scores ~3% and VulnBot ~6%, while structured/guided
   systems reach 39–91%. The delta is *architecture* (planning, memory, verification),
   not model size. [PGP2][PTEVAL]
3. **Planning — not tools — determines multi-step success.** PentestGPT v2 ablation:
   a typed tool layer alone adds +14 pts on web tasks but **zero** improvement on a
   multi-host Active-Directory range; adding tree-search planning + memory doubles
   hosts owned. [PGP2]
4. **Grounding/RAG is decisive.** Fang et al.: GPT-4 exploits **87%** of one-day
   vulns *given the CVE description* vs **7%** without it — an 80-point swing from
   context alone. [FANG1]
5. **Safety must be structural, not prompt-based.** The consensus safety pattern is
   **verdict-vs-action separation** (the agent may decide; a deterministic checker or
   human authorizes any irreversible action) plus a layered kill-switch, and treating
   the agent runtime as **untrusted by construction** (assume prompt-injected). [GRD]

**Implication for Vedha:** build the LLM as the *reasoning/orchestration brain* over
a **deterministic, policy-gated execution layer** (reuse the existing exploit engine,
nuclei/nessus, ScopeGuard, exploit-approval), add **planning + memory + RAG + a
validator loop**, and enforce safety **outside** the model. This is precisely the
"agentic control plane driving tools" architecture — and it is the safest of the
options studied.

---

## 1. Commercial landscape — AI-native vs marketing

### XBOW (agentic, GenAI-in-the-loop)
Architecture is described as **attack-surface mapping → a coordinator that prioritizes
what to test → short-lived autonomous agents that execute attacks → validators that
confirm findings.** Agents are *"short-lived, focused attack workers, retired after
each mission to avoid bias,"* use *"the same tools used by human pentesters (e.g.
sqlmap, XSS tooling) and LLMs for reasoning and adaptation,"* *"generate custom
payloads,"* and *"quickly adapt… test hypotheses, then pivot."* The stated key
innovation is **exploit-execution validation over theoretical detection** — every
finding must be reproduced, *"eliminating false positives."* Coordinator prioritization
logic, memory, and verification internals are **undisclosed.** [XBOW1][XBOW2]

### Horizon3.ai NodeZero (deterministic execution, AI orchestration)
Autonomously **discovers, exploits, and chains** weaknesses (lateral movement,
credential attacks, data mining, control bypass), delivering *"proof of exploit rather
than a CVSS score."* Runs from an ephemeral, **one-time-use isolated VPC**; no persistent
agents. Crucially, exploitation is **deterministic and pre-validated — explicitly not
GenAI-generated.** This is the strongest signal in the whole landscape for how to keep
autonomous offense safe. [H3][H3WEB]

### Others (brief)
- **ProjectDiscovery** — nuclei + AI-assisted/NL→template generation; recon/scanning
  layer, not an autonomous exploiter. A tool the control plane *calls*.
- **Endor Labs** — reachability/exploitability triage (does a vuln lie on a reachable
  path?); the *triage/prioritization* pattern, applicable to Vedha's prioritizer.
- **Google Big Sleep / Project Zero (Naptime)** — LLM agent for *vulnerability research*
  (finding new bugs in code), a different problem than network pentest, but the source
  of the "give the model the same tools a human researcher uses" tool-design philosophy.

---

## 2. Academic research

| Work | Approach | Result | Limitation |
|------|----------|--------|------------|
| **Fang et al. 2024 — one-day** [FANG1] | GPT-4 + simple ReAct agent + CVE text | **87%** exploit success on 15 real one-day CVEs; 0% for GPT-3.5/OSS and for ZAP/Metasploit scanners; **7%** without the CVE text | Needs the CVE description; small N=15; web-app bias |
| **Fang et al. 2024 — zero-day (HPTSA)** [FANG2] | **Multi-agent**: a planner dispatches task-specific sub-agents | Team beats single agent on unseen (zero-day) vulns | Cost/coordination overhead |
| **PentestGPT / v2** [PGP2] | Tool+Skill layer (38 typed tools + RAG), Task-Difficulty Assessment, **Evidence-Guided Attack-Tree Search**, external memory | **85–91%** on XBOW web bench; 12/13 machines rooted; **4/5** on a 5-host AD range; live HTB S8 **10/13 (76.9%)**, top-100/8036 | Creativity barrier (out-of-distribution), honeypot poisoning, no multi-week continuity |
| **EnIGMA** | Interactive agent w/ specialized interfaces | SOTA on NYU CTF + Cybench | CTF-scoped |
| **HackingBuddyGPT** | Minimal agent for Linux **privilege-escalation** | Autonomous privesc in terminal envs | Narrow scope |
| **HackSynth / xOffense / VulnBot** | Autonomous multi-agent / domain-adapted LLMs | Framework baselines | Fully-autonomous variants score low (3–6%) |

**Takeaway:** the winning recipe is consistent — **typed tools + RAG grounding +
explicit planning (tree search) + external memory + a validation loop**, ideally with
a **multi-agent planner/executor/critic** split.

---

## 3. Best-practice agent architecture (what measurably works)

- **Tool & skill layer** — typed, structured-I/O interfaces to real tools (not free-form
  shell). Eliminates "capability" (Type-A) failures. [PGP2]
- **Planning > reactive prompting** — Evidence-Guided **Attack-Tree Search** with a
  difficulty estimate to prune low-value branches and avoid context exhaustion. This is
  what unlocks multi-step chains. [PGP2]
- **External memory** — branch summaries + selective context injection so long
  engagements don't overflow the context window. [PGP2]
- **Multi-agent (planner / executor / critic-validator)** — beats single-agent on unseen
  targets; the validator enforces "reproduce the exploit or it didn't happen." [FANG2][XBOW1]
- **RAG over security knowledge** — MITRE ATT&CK, CVE/EPSS/KEV, exploit DBs. Given
  Fang's 87%-vs-7%, retrieval of the *right* CVE/exploit context is the single highest-ROI
  component. [FANG1]

---

## 4. Safety & guardrails for autonomous offense

- **Verdict-vs-action separation** — the agent reaches a verdict; a deterministic checker
  or human authorizes any **irreversible** action. Reversible/recon actions may run in
  scope; destructive/irreversible ones are gated. [GRD]
- **Deterministic execution-control layer** — guardrails must be code, not prompts:
  *"probabilistic guessing systems… fail against prompt injection."* [GRD]
- **Treat the agent runtime as untrusted by construction** — assume it may be
  prompt-injected by target output, compromised, or misaligned; place controls it cannot
  disable. [GRD]
- **Kill switch = layered containment** — terminate session, revoke credentials + tool
  access, freeze orchestration, roll back to known-safe state. Not a single button. [GRD][KILL]
- **Prompt-injection isolation** — target output (banners, HTTP responses) is untrusted
  data; never let it act as instructions (Vedha already applies this pattern in the
  remediation prompt).
- **Scope / rules-of-engagement + blast-radius limits + immutable audit + legal
  authorization** framing around every engagement.

---

## 5. Evaluation & benchmarks (public scores)

| Benchmark | What it tests | Notable score |
|-----------|---------------|---------------|
| **Cybench** | 40 pro CTF tasks | multi-agent frameworks ~22.5%; frontier agents higher |
| **NYU CTF Bench** | CSAW CTF challenges | ~22% (multi-agent); EnIGMA SOTA |
| **HackTheBox (live)** | Real machines | PentestGPT v2 76.9% (10/13), top-100/8036 |
| **GOAD** | 5-host Active Directory | PentestGPT v2 4/5 |
| **XBOW web bench** | 104 web tasks | PentestGPT v2 91% |
| **AutoPenBench / HackSynth / CAIBench** | Autonomous-pentest / meta-benchmark | framework baselines |

**Reality check:** even SOTA tops out on **Easy/Medium** targets; Hard/Insane and novel
protocols still need humans. *"Fully autonomous penetration testing remains distant."*
[PGP2] Vedha should therefore ship **bounded autonomy with human escalation**, not a
promise of hands-off mastery.

---

## Sources

- [XBOW1] XBOW — *Core Components of an AI Pentesting Framework* — https://xbow.com/blog/core-components-ai-pentesting-framework
- [XBOW2] XBOW — platform / autonomous offensive security — https://xbow.com/
- [H3] Horizon3.ai — *AI at Horizon3* — https://horizon3.ai/ai-in-horizon3-ai/
- [H3WEB] Horizon3.ai — Autonomous Web App Pentesting — https://horizon3.ai/web-application-pentesting/
- [FANG1] Fang et al. — *LLM Agents can Autonomously Exploit One-day Vulnerabilities* — https://arxiv.org/abs/2404.08144
- [FANG2] Fang et al. — *Teams of LLM Agents can Exploit Zero-Day Vulnerabilities* — https://arxiv.org/pdf/2406.01637
- [PGP2] *What Makes a Good LLM Agent for Real-world Penetration Testing?* (PentestGPT v2) — https://arxiv.org/html/2602.17622v1
- [PTEVAL] *PentestEval: Benchmarking LLM-based Penetration Testing* — https://arxiv.org/html/2512.14233v1
- [GRD] UnderDefense — *AI SOC Guardrails: Scope Limits, Override Policies, Control Over Autonomous Agents* — https://underdefense.com/blog/ai-soc-guardrails/
- [KILL] Sakura Sky — *Trustworthy AI Agents: Kill Switches and Circuit Breakers* — https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-6/
- Multi-Agent Penetration Testing AI for the Web — https://arxiv.org/pdf/2508.20816
- xOffense (domain-adapted multi-agent) — https://arxiv.org/pdf/2509.13021
- HackSynth — https://arxiv.org/pdf/2412.01778
- CAIBench (meta-benchmark) — https://arxiv.org/pdf/2510.24317
