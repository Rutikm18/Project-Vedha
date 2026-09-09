# Prompt & Output Log — Vedha Manager AI Architecture

_Saved from the last two prompt/output pairs._

---

## 1. Prompt

> i wanted to integrate ai , i have keys but when i added to its not properly config..can you do check with manager with architecture..first give me understanding of ai architectrue.. langgraph , ai how the architecture in your ming and that you think about.. guide me with that part

## 1. Output

### The mental model I use for any LLM system

Think of it as **5 layers + 1 spine**. Every production AI system is some arrangement of these:

| Layer | Question it answers | Your code |
|---|---|---|
| **L0 — Model access** | *Which model, how do I call it, what if it fails?* | `services/llm.py` (`ManagerLlmService`), `llm_http_client.py`, `config.py` |
| **L1 — Grounding / retrieval** | *What real data does the model see?* | Read-only Postgres tools + `<security_context>` injection (structured, **not** vector RAG) |
| **L2 — Guardrails** | *How do I stop hallucination / injection / unsafe output?* | `ai/hallucination.py`, system-prompt rules in `llm.py` |
| **L3 — Orchestration** | *One shot, a tool loop, or a multi-step graph?* | `generate_with_fallback()` · `ai/agent.py` (tool loop) · `ai/verification_graph.py` (**LangGraph**) |
| **L4 — Applications** | *What user problem?* | AI advisor (`routers/ai.py`), report (`ai/llm_report.py`), prioritizer (`ai/prioritizer.py`), enrichment (`services/finding_ai.py`) |
| **Spine (cross-cutting)** | *deterministic-first · fail-closed · human-in-the-loop · grounded · provider-agnostic* | the philosophy every module above follows |

The **spine** is the most important thing in your codebase and the thing most teams get wrong. Your platform gets it right.

### Your manager's AI architecture (grounded in the actual files)

```
┌─────────────────────────── L4  APPLICATIONS ───────────────────────────┐
│  AI Advisor/Brief      AI Report           ML Prioritizer     Finding    │
│  routers/ai.py         ai/llm_report.py    ai/prioritizer.py  enrichment │
│  (the "AI Brain")      routers/ai_report   (XGBoost + det.)   finding_ai │
└───────────────┬─────────────────────────────────────────────┬──────────┘
                │                                               │
┌───────────────▼─────────────── L3  ORCHESTRATION ────────────▼──────────┐
│  Single-shot + fallback     Tool-use loop            LangGraph graph     │
│  generate_with_fallback()   ai/agent.py              ai/verification_    │
│  (fail over across          (Claude reads Postgres    graph.py           │
│   providers)                 via READ-ONLY tools,     (StateGraph; 1 node │
│                              recommend-only)          today, staged for   │
│                                                       human-in-the-loop)  │
└───────────────┬───────────────────────────────────────────────┬─────────┘
                │                                                 │
┌───────────────▼──────────── L2  GUARDRAILS ─────────────────────▼────────┐
│  HallucinationGuard (no invented CVEs/scores, no destructive cmds)        │
│  System rules: treat <security_context> as UNTRUSTED data, no exploit     │
│  instructions, separate facts from hypotheses                             │
└───────────────┬──────────────────────────────────────────────────────────┘
                │
┌───────────────▼──────────── L1  GROUNDING ────────────────────────────────┐
│  Read-only Postgres tools + structured context injection.                 │
│  NOTE: not a vector DB — precise, permissioned, per-tenant. Right choice.  │
└───────────────┬───────────────────────────────────────────────────────────┘
                │
┌───────────────▼──────────── L0  MODEL ACCESS ─────────────────────────────┐
│  ManagerLlmService (services/llm.py)                                       │
│   ├─ providers: ollama | openrouter | anthropic | openai | gemini          │
│   ├─ _usable_key() guard  ├─ _dispatch per-provider  ├─ fallback chain      │
│  Config: config.py Settings ← .env  (LLM_PROVIDER + <PROVIDER>_API_KEY)     │
└────────────────────────────────────────────────────────────────────────────┘
```

**The two things that make this architecture unusually good:**

1. **Deterministic-first, AI-optional.** Every AI path has a deterministic floor and the LLM is never a hard dependency:
   - Prioritizer → XGBoost, *falls back to* a weighted formula.
   - Verification → deterministic core, *optionally* wrapped in LangGraph, *optionally* LLM rationale.
   - Enrichment → curated KB, *optionally* AI polish.
   - No key / provider down → clean **503 or deterministic result**, never a crash or a fabricated answer.

2. **Grounded + human-in-the-loop by construction.** `ai/agent.py` is a Claude tool-use loop whose tools are **read-only Postgres queries + one terminal `submit_recommendations`**. The model *literally cannot* launch a scan or mutate a finding — its only "write" is recommendations that land `pending` for a human to approve.

### Where LangGraph fits — and where it already is in yours

**What LangGraph is:** a library for **stateful, multi-step LLM workflows modeled as a graph** — nodes (steps) + edges (transitions, including *conditional* ones) over a shared typed `State`. Its real value-adds over a plain loop:
- **Checkpointing** (persist state between steps → resume/replay)
- **Human-in-the-loop interrupts** (pause at a node, wait for approval, continue)
- **Conditional branching / cycles** (retry, escalate, loop-until-done)
- **Durable, auditable execution traces**

**Where it is in your code today** (`ai/verification_graph.py`): a deliberately *minimal* `StateGraph` — one node (`corroborate`) wrapping the deterministic verification core. It's **scaffolding**: *"the SAME wiring carries forward to P3, where active validation adds a checkpointed, human-in-the-loop node."* Absent LangGraph, it calls the core directly with identical results.

**When to expand it:**

| Use LangGraph when… | Use a plain tool-loop / single-shot when… |
|---|---|
| Multi-step with **conditional** paths (retry, escalate, branch) | Linear "reason once, answer" |
| You need **human approval mid-flow** (pause → approve → resume) | Fully autonomous read-only advice |
| **Checkpoint/replay/audit** of each step matters | Statelessness is fine |
| Long-running (a campaign that spans minutes/hours) | Sub-second interactive Q&A |

Concrete candidates in *your* platform where a graph earns its keep:
- **P3 active validation** (the intended one) — scan → corroborate → *interrupt for human approval* → validate → record.
- **`AgentDecisionEngine`** (`ai/agent.py`) → `gather-context → reason → propose → human-approve → act(gated)` with checkpoints and a loop-guard on step/token/cost budget.
- **Attack-path / next-action orchestration** — genuinely dynamic branching.

But **don't LangGraph-ify the AI Brain advisor or the report generator** — those are single-shot generations; a graph adds latency and complexity for zero benefit.

### Why your keys "aren't configuring"

This is a **layer-0 config problem**, with 3 traps:

1. **Keys go in the root `.env` (gitignored), read by `config.py` at startup** — not the frontend, not code:
   ```
   LLM_PROVIDER=anthropic          # which provider is the default
   ANTHROPIC_API_KEY=sk-ant-...    # <PROVIDER>_API_KEY
   LLM_MODEL=claude-sonnet-4-6     # Anthropic's model var (others: OPENAI_MODEL, GEMINI_MODEL...)
   ```
2. **Config is loaded once at process start.** Editing `.env` does nothing until you **restart the backend** — almost certainly why "I added the key but it's not configured."
3. **The `_usable_key()` guard rejects malformed keys.** Empty, whitespace, or **non-ASCII** (your old `OPENROUTER_API_KEY=₹`) → treated as *unconfigured*. Provider gotchas:
   - **OpenAI**: a key alone → `429 insufficient_quota` unless the account has **active billing**.
   - **OpenRouter**: `OPENROUTER_MODEL` must be a **live `:free` id** (e.g. `google/gemma-2-9b-it:free`).
   - **Gemini**: a real AI Studio key is `AIza...`. `AQ.Ab8...` looks like a **short-lived ephemeral token** and will expire.

**Configure + verify:**
```bash
# 1. Put keys in the ROOT .env (gitignored)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...        # a real, ASCII, active key
# 2. RESTART the backend (uvicorn / make run) — Settings reload only at startup
# 3. Verify: Settings page in the UI, or GET /ai/status → per-provider configured + reason
```

---

## 2. Prompt

> can you find the area of failure or improvement?

## 2. Output

Principal-level review of the AI subsystem, evidence-based with file:line, failure scenario, and fix. Ordered by severity.

### 🔴 Blocker / High — security & cost

**1. No rate-limit or cost ceiling on the AI endpoints** — `routers/ai.py:18`, `agent_advisor.py`, `ai_report.py` (grep: zero rate-limit deps).
*Scenario:* any authenticated user can spam `/ai/generate` (an expensive LLM call) with no per-user/tenant/day cap → runaway provider bill + quota exhaustion that takes the AI Brain down for everyone. Auth has `login_rate_limit`; AI has nothing.
*Fix:* per-user + per-tenant rate limit and a daily token/cost budget (fail closed to the deterministic layer when exceeded).

**2. The authenticated actor is thrown away** — `routers/ai.py:14` and `:20` both do `del current_user`.
*Scenario:* users ask the AI to reason over engagement data and there's **no audit** of who asked what, and no server-side check that the caller owns the `context` they submitted.
*Fix:* structured audit log (actor, tenant, task, model, tokens, correlation-id); consider validating context ownership.

**3. HallucinationGuard is not wired into the interactive path** — only `ai/llm_report.py` calls it; `routers/ai.py` `generate_with_fallback` and `ai/agent.py` do not.
*Scenario:* the AI Brain answer and the agent's recommendations can contain an **invented CVE, a wrong CVSS, or a destructive command** and it reaches the user unchecked.
*Fix:* run `HallucinationGuard.validate()` on advisor/agent output too (surface low-confidence / block destructive).

### 🟠 High — reliability & architecture

**4. Agent loop has no wall-clock deadline and no cumulative token/cost budget** — `ai/agent.py:199` (`for iteration in range(self._max_iters=8)`).
*Scenario:* the httpx provider timeout is **180s**; a stalled provider means one advisor run can hang up to ~**8 × 180s ≈ 24 minutes**, and cost is unbounded across 8 growing-context iterations.
*Fix:* an overall deadline (~60–90s), a cumulative token budget, and a shorter per-call timeout.

**5. The agent bypasses your provider abstraction entirely** — `ai/agent.py:245` calls the raw `anthropic` SDK (`self._client.messages.create`), not `ManagerLlmService`.
*Scenario:* the agentic advisor is **Anthropic-locked** — the Gemini/OpenAI keys you're wiring can't drive it — and it skips the `_usable_key` guard, the fallback chain, and unified error mapping. Two divergent "call an LLM" paths.
*Fix:* route the agent's calls through `ManagerLlmService` (add a tool-use-capable method), or at minimum share the key-validation + error mapping.

### 🟡 Medium — AI quality & operability

**6. No AI evals** — only `test_engine_bridge_regression.py` (detection, not AI); no golden dataset for advisor/report/enrichment.
*Scenario:* a prompt tweak or model swap silently regresses answer quality / structured-output compliance.
*Fix:* a small eval suite — happy path, prompt-injection, unsupported-question refusal, JSON-schema compliance, "guard catches invented CVE".

**7. HallucinationGuard false positives** — `ai/hallucination.py:35`: `\bshutdown\b|\breboot\b|\bhalt\b`.
*Scenario:* legitimate remediation ("reboot after patching", `Install-WindowsUpdate -AutoReboot`) gets flagged destructive → valid guidance blocked/degraded.
*Fix:* scope to genuinely destructive forms (`shutdown -h now`) or downgrade to informational.

**8. Health status isn't a real health check** — `services/llm.py status()`: `configured = _usable_key(key)`.
*Scenario:* exactly your "keys added but not configured" pain — a billing-dead OpenAI key or an **expired Gemini ephemeral token** shows **green/"configured"** while every call 429/401s. Presence ≠ health.
*Fix:* active probe (cheap auth ping per provider) → true health + a concrete reason string.

**9. No config-doctor / startup validation.**
*Scenario:* a malformed key (`₹`), a fake OpenRouter model id, or the ephemeral Gemini token only reveal themselves when a user hits an error.
*Fix:* startup validation + an operator-only `/ai/doctor` that pings each provider and reports format + reachability + model validity.

### ✅ What's already strong (don't change)
- **Deterministic-first everywhere** — every AI path has a fallback; the LLM is never a hard dependency.
- **Read-only + recommend-only agent** (`ai/agent.py:8–14`) — the model can't scan/exploit/mutate; recommendations land `pending` for human approval.
- Loop is **bounded** (8 iters), tool errors caught, read tools use row limits.
- `_usable_key` guard + the LangGraph human-in-the-loop seam are good foundations.

### Recommended fix order (highest leverage first)
1. **Health probes + config doctor (#8, #9)** — directly fixes the "keys not configuring" problem and makes it self-diagnosing.
2. **Rate-limit + audit on AI endpoints (#1, #2)** — closes the cost-DoS and governance gaps.
3. **Wire the guard into the interactive path + fix its false positives (#3, #7)**.
4. **Agent deadline + budget + route through ManagerLlmService (#4, #5)**.
5. **A starter eval suite (#6)**.
