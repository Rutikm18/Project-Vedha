# Vedha Autonomous Engagement Agent (VAEA) — Design & Plan

**Date:** 2026-08-16 · **Status:** DRAFT for validation
**Companion research:** `docs/superpowers/research/2026-08-16-autonomous-offensive-ai-agent-research.md`

> Goal chosen with the user: a **fully autonomous offensive agent**, running whole
> engagements **within scope/policy bounds**, built as an **agentic control plane**
> (LLM tool-use orchestrator) that drives Vedha's existing tooling.

---

## 1. Recommendation in one paragraph

Evolve Vedha's **existing** recommend-only agent (`ai/agent.py::AgentDecisionEngine`,
already a Claude tool-use loop) into a **planner → executor → validator** control plane.
The LLM is the **reasoning brain** — it plans attack trees, selects tools, chains
findings, and forms hypotheses — but **every intrusive action executes through Vedha's
deterministic, already-gated tools** (exploit engine, nuclei/nessus, ScopeGuard,
exploit-approval), **never as LLM-generated exploit code run blind** (the NodeZero
principle). Autonomy is granted by a **policy engine** that auto-authorizes low-risk,
reversible actions inside the rules-of-engagement and escalates the rest, with
**verdict-vs-action separation**, a **layered kill-switch**, **RAG grounding** over
ATT&CK/CVE/EPSS/KEV, and **immutable audit**. This is the safest architecture in the
research and the highest-scoring recipe (typed tools + tree-search planning + memory +
validator + RAG → 85–91% on public benches).

---

## 2. What Vedha already has (reuse as control-plane tools)

This is why VAEA is an **evolution, not a rebuild** — the primitives exist:

| Vedha component | Role in VAEA |
|---|---|
| `ai/agent.py::AgentDecisionEngine` (Claude tool-use loop, `max_iters`, read tools + terminal submit) | The **control-plane skeleton** to extend from read-only → action tools |
| `ALLOWED_ACTIONS` (`run_discovery_scan`, `run_targeted_scan`, `request_exploit_validation`, `recheck_finding`, …) | The **typed action vocabulary** (PentestGPT-v2 "tool layer") |
| `AgentRecommendation` (pending/approved) | The **verdict record**; becomes the audit + policy-decision log |
| `ExploitApprovalRequest` ("auto-queues the exploit job when status → approved") + exploit orchestrator | The **deterministic, gated execution layer** — policy engine flips `approved` within RoE |
| `services/scope_targets.py` / ScopeGuard | **Scope / rules-of-engagement enforcement** (deterministic, pre-LLM) |
| `ai/hallucination.py` (command-safety + CVE/score grounding) | **Deterministic guardrail** on every tool arg + output |
| attack-path correlation (`attack_paths`, `AttackPath`) | The **graph the planner reasons over** for chaining |
| nuclei / nessus / discovery / exploit engine | **Executor tools** |
| `models/outbox.py` (durable, retried, dead-letter) | **Durable step execution** for long engagements |
| `audit_log`, `exploit_result`, `attack_timeline` | **Immutable audit + timeline** |
| `ai/prioritizer.py`, EPSS/KEV signals | **RAG/triage inputs** (reachability/exploitability) |

**Net-new** we must build: the **planner (attack-tree search)**, **long-term memory**,
the **policy/autonomy engine**, the **security RAG index**, the **validator loop**, and
the **kill-switch/containment** primitives.

---

## 3. THE AI FLOW (validate this first)

An engagement runs as a bounded **Plan → Act → Observe → Verify → Re-plan** loop. Each
cycle is one durable, audited step; the LLM never touches the network directly.

```
             ┌────────────────────── RULES OF ENGAGEMENT (deterministic gate) ─────────────────────┐
             │  scope CIDRs · excluded ranges · autonomy tier · blast-radius caps · time/kill window │
             └───────────────────────────────────────────────────────────────────────────────────┘
                                                   │  (every action is checked here, pre-LLM & pre-exec)
   ┌────────────┐   plan step    ┌──────────────┐  proposed action  ┌──────────────┐  authorize?  ┌───────────────┐
   │  PLANNER   │ ─────────────▶ │  POLICY      │ ────────────────▶ │  EXECUTOR    │ ───────────▶ │ DETERMINISTIC │
   │ (LLM +     │                │  ENGINE      │  tier 0/1: auto   │ (tool-use)   │              │ TOOLS         │
   │ attack-tree│ ◀───────────── │ verdict→     │  tier 2/3: queue  │ typed tools, │              │ scan/exploit/ │
   │ search +   │   observation  │ action sep.  │  → human/approval │ scope-checked│              │ recon/graph   │
   │ memory)    │                └──────────────┘                   └──────────────┘              └───────┬───────┘
        ▲                                                                                                  │ result
        │                                          ┌──────────────┐   reproduce & confirm   ┌──────────────▼──────┐
        └────────────── verified evidence ──────── │  VALIDATOR   │ ◀────────────────────── │  OBSERVATION        │
                        (or "unproven → drop")      │ (LLM critic) │   "exploit or it        │  (untrusted data,   │
                                                    └──────────────┘    didn't happen"        │  injection-isolated)│
                                                                                              └─────────────────────┘
                     Kill-switch spans the whole loop: halt · revoke tool creds · freeze · rollback.
```

**Step semantics**
1. **PLANNER** proposes the next node in an **attack tree** (ReAct is insufficient for
   multi-step; tree-search + a difficulty estimate is what unlocks chains — PentestGPT v2).
   Inputs: engagement state, attack-path graph, memory, RAG (relevant CVE/ATT&CK/exploit).
2. **POLICY ENGINE** classifies the proposed action's **risk tier** and applies
   **verdict-vs-action separation**: the plan is the verdict; authorization to *act* is a
   separate deterministic decision (auto within tier, else queue for approval).
3. **EXECUTOR** invokes a **typed tool** (not free-form shell). ScopeGuard + hallucination
   guard validate args **before** execution.
4. **OBSERVATION** returns tool output as **untrusted data** — prompt-injection-isolated
   (delimited, never interpreted as instructions).
5. **VALIDATOR** (critic agent) must **reproduce/confirm** exploitation before a finding
   is accepted — XBOW's zero-false-positive principle; unproven claims are dropped.
6. **Re-plan** with verified evidence in memory; loop until objectives met, budget spent,
   or kill-switch.

---

## 4. Policy / autonomy engine — how "fully autonomous within bounds" is safe

Autonomy is **tiered by action reversibility & blast radius**, not global:

| Tier | Examples | Default policy |
|---|---|---|
| **0 — passive** | recon, service/version ID, read Vedha data, RAG lookup | **auto** |
| **1 — reversible active** | port/vuln scan (nuclei/nessus), non-destructive validation, safe PoC checks | **auto within scope + rate caps** |
| **2 — intrusive** | exploit execution, credential use, lateral movement, post-exploit enumeration | **auto only if RoE grants "full autonomous"; else exploit-approval gate** |
| **3 — irreversible / high-impact** | data exfil beyond proof, DoS-capable modules, account/state mutation, egress | **always human approval** (never auto) |

- "Fully autonomous engagements" = operator opts an engagement into **auto-authorize up
  to Tier 2** within an explicit RoE (scope CIDRs, excluded ranges, time window,
  blast-radius caps, module denylist). Tier 3 stays human-gated **by construction**.
- The policy engine is **deterministic code** (not the LLM) and reuses `ScopeGuard` +
  `ExploitApprovalRequest`: for an in-policy Tier-2 action it simply sets the existing
  approval `status → approved` (which already auto-queues the job) and records *why*.

---

## 5. Safety architecture (structural, not prompt-based)

- **Untrusted-agent posture** — the planner LLM may be prompt-injected by target output;
  all enforcement (scope, tier, caps, kill) lives **outside** the model.
- **Layered kill-switch** — one operator action: pause loop → revoke the executor's tool
  credentials/tokens → freeze the outbox queue → mark engagement `halted` → rollback
  hook. Independent of the agent's cooperation.
- **Blast-radius limits** — per-engagement caps: max hosts touched, max exploit attempts,
  request-rate, wall-clock; breach → auto-halt.
- **Immutable audit + timeline** — every plan step, policy verdict, tool call, and result
  to `audit_log` / `attack_timeline` (append-only), reproducible.
- **Prompt-injection isolation** — target output delimited as data; the command-safety
  guard scans every proposed tool arg (extend it beyond the current command field).
- **Dry-run / simulation mode** — the whole loop runs with executor in "plan-only" to
  preview the attack tree before any packet leaves.
- **Legal/authorization** — engagement carries signed RoE + authorization; agent refuses
  to plan outside declared scope.

---

## 6. Security RAG (the highest-ROI single component — 87% vs 7%)

Index, retrieved per plan step and injected into the planner:
- **MITRE ATT&CK** (techniques ↔ tools/steps), **CVE + EPSS + KEV** (which vuln to chase),
  **exploit metadata** (Metasploit/nuclei module ↔ CVE), and Vedha's own prior
  engagements (what worked on similar targets — closes the "no continuity" gap).
- Grounding rule (already Vedha's posture): the planner may only cite retrieved facts —
  no invented CVEs/scores/hosts; the hallucination guard enforces it.

---

## 7. Phased roadmap (crawl → walk → run)

- **Phase 0 — Foundations & safety rails (no new autonomy).** Kill-switch, RoE model +
  blast-radius caps, policy-engine scaffold (all actions still human-approved), audit/timeline
  wiring, security-RAG index. *Ships safety before capability.*
- **Phase 1 — Planner + memory (Tier 0/1 auto).** Attack-tree planner + external memory;
  auto-authorize passive + reversible actions; validator loop for scan findings. Evaluate on
  a lab range.
- **Phase 2 — Gated exploitation (Tier 2, human-approved).** Executor drives the exploit
  engine via the existing approval gate; validator reproduces every exploit. Multi-agent
  planner/executor/critic split.
- **Phase 3 — Bounded full autonomy (Tier 2 auto within RoE).** Opt-in per engagement;
  Tier 3 stays human. Continuous/scheduled engagements via outbox.
- **Phase 4 — Learning loop.** Feed verified outcomes back into RAG/memory for
  cross-engagement continuity.

Each phase is independently shippable and independently useful.

---

## 8. Evaluation harness

Gate promotion between phases on measured scores, not vibes:
- Stand up **GOAD** (AD range) + a **HackTheBox/lab** set + a subset mirroring **Cybench /
  NYU CTF** in an isolated VPC (NodeZero's ephemeral-range pattern).
- Track: objective-completion %, exploits *validated* (not just claimed), false-positive
  rate (target ~0 via validator), mean steps/finding, human-escalations, and **safety
  violations = 0** (any scope/tier breach fails the phase).

---

## 9. Trade-offs & open decisions to validate

1. **Exploit generation policy** — *recommended:* deterministic/pre-validated modules only
   (NodeZero), LLM never emits exploit code that runs. Alternative: XBOW-style LLM payload
   generation inside a sandboxed validator (higher capability, higher risk). **Decide.**
2. **Single- vs multi-agent** — start single-agent planner+validator; split into
   planner/executor/critic in Phase 2 (evidence says multi-agent wins on unseen targets, at
   token cost).
3. **Model** — planner on the strongest reasoning model (Opus-class); cheap model for
   parsing/summarizing tool output. (Vedha currently pins Sonnet — revisit for the planner.)
4. **Autonomy ceiling** — confirm Tier-2 auto is acceptable for "fully autonomous," with
   Tier-3 always human. This is the core risk decision.
5. **Continuity** — how much cross-engagement memory before it becomes a data-governance
   concern.

---

## 10. Why this is the right "AI-native" answer

It makes the **LLM the orchestration brain** (native agentic control plane) while keeping
**execution deterministic and policy-bounded** — matching the only autonomous-pentest
approaches shown to be both effective (85–91% on Easy/Medium) and safe (NodeZero's
deterministic execution + verdict-vs-action separation). It reuses ~80% of Vedha's existing
machinery and adds capability **behind safety**, phase by phase.
