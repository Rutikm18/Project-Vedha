# Remediation AI — Technical Deep-Dive (Vedha)

> LLM transport: **httpx** (`ManagerLlmService`) + the official **Anthropic SDK**
> (`LLMReportGenerator`) — Vedha's existing AI stacks. We deliberately do NOT port
> AttackLens's `aiohttp` / `ResilientHTTPClient`; we already have equivalents.
>
> Codebase roots: `manager/backend/app/services/remediation_kb.py`,
> `manager/backend/app/ai/llm_report.py`, `manager/backend/app/routers/remediation.py`,
> `manager/backend/app/models/remediation_plan.py`

---

## 0. Why this exists (and what we reused vs. built)

The AttackLens remediation subsystem was the design inspiration, but Vedha already
shipped most of its machinery. Rather than re-implement transport, retries, and
prompt-injection defense, we **reused** them and added only the three things
AttackLens genuinely does better.

| Capability | AttackLens | Vedha — reused / new |
|---|---|---|
| HTTP transport + retry + breaker | `aiohttp` + `ResilientHTTPClient` | **reused** `ManagerLlmService` (httpx) / `LLMReportGenerator` (Anthropic SDK) |
| Prompt-injection defense | `SYSTEM_PROMPT` untrusted-data rules | **reused** `LLMReportGenerator.SYSTEM_PROMPT` |
| Command safety | *(none)* | **reused** `HallucinationGuard.validate_remediation_commands` |
| Cache + review workflow | SQLite `ai_analysis` | **reused** pattern; new `remediation_plans` table |
| Structured JSON plan | ✓ | **new** `generate_remediation_plan` |
| OS-aware plans | ✓ (macOS) | **new**, but Linux/Windows/appliance-first (network focus) |
| Deterministic KB fallback | `recipe_for_finding` | **new** `services/remediation_kb.py` |

---

## 1. Architecture Overview

```
FastAPI Route Layer   (routers/remediation.py, portal.py)
        │
        ├───────────────► services/remediation_kb.py   (pure, always-available)
        │                   classify_finding → RECIPES → recipe_for_finding(os)
        ▼
LLMReportGenerator    (ai/llm_report.py)      ← generate_remediation_plan(finding, os)
        │                   _parse_json_response · _normalize_ai_plan · _safe_commands
        ▼
HallucinationGuard    (ai/hallucination.py)   ← validate_remediation_commands (safety)
        │
        ▼
Anthropic SDK (httpx) ← _complete: retry / refusal / truncation handling
        │
        ▼
remediation_plans     (models/remediation_plan.py)   UNIQUE(finding_id, os)
```

Two totally independent paths produce a plan:

1. **Deterministic KB** — a pure function. No network, no AI, no DB. Always returns
   a structured, OS-filtered plan. This is the floor: the endpoints can never be
   empty.
2. **AI** — `LLMReportGenerator.generate_remediation_plan`, reusing the report
   stack's transport/retry/safety. Its output is normalized into the *same* schema
   the KB emits, so the API and UI render both identically.

---

## 2. The Deterministic KB — `services/remediation_kb.py`

Pure and unit-tested. Three surfaces:

### 2.1 `classify_finding(finding) -> str`

Findings have **no `category` column**, so classification is keyword/CVE-driven over
`title + description + remediation`. Order matters (first match wins), so specific
signatures precede broad ones — notably `outdated_ssh` is checked **before**
`weak_tls` so "OpenSSH weak ciphers" routes to SSH hardening, not the TLS recipe
(both mention "cipher"). A CVE with no keyword hit falls to `missing_patch`;
anything else is `generic`.

Categories: `weak_tls`, `smb_signing`, `exposed_rdp`, `default_credentials`,
`missing_patch`, `open_mgmt_port`, `anon_ftp`, `outdated_ssh`, `generic`.

### 2.2 `RECIPES`

Eight seeded recipes plus `generic`. Each **step** carries a per-OS command map:

```python
"commands": {"linux": [...], "windows": [...], "macos": [...], "generic": [...]}
```

`generic` is required and holds vendor-neutral guidance (for appliances/switches
with no shell). Per-OS lists fall back to `generic` when absent. Every command is
hand-authored and non-destructive.

### 2.3 `recipe_for_finding(finding, os) -> dict`

Classify → pick recipe → resolve each step's `commands_for_os` for the requested OS
(`network`/unknown → `generic`). Returns the canonical plan schema with
`source="deterministic_kb"`. The full per-OS `commands` map is retained so the UI
can offer a client-side OS switch without a round-trip.

---

## 3. The AI path — `LLMReportGenerator.generate_remediation_plan(finding, os)`

Lives on the existing report generator so it inherits `_complete` (Anthropic SDK +
exponential backoff, refusal detection, truncation logging) and the `_guard`.

Flow:

1. `_remediation_plan_prompt(finding, os, os_label)` — asks for **VALID JSON ONLY**
   in a fixed schema, names the target OS, and injects exploitation signals
   (`severity`, `cvss_score`, `epss_score`, `exploitable`, `exploit_validated`,
   CVE) so the model calibrates `effort` / `remediation_risk`. All local finding
   fields — **no network enrichment call**.
2. `await self._complete(prompt, max_tokens=2000)`.
3. `_parse_json_response(text)` — fault-tolerant: strips ```` ```json ```` fences,
   then falls back to the first `{` … last `}` substring, else `{}`.
4. `_normalize_ai_plan(raw, os, guard)` — coerces the parse into the **same schema
   the KB emits** and runs **every command through the safety guard**. Flagged
   (destructive) commands are dropped and the step marked
   `unsafe_commands_removed: true`. Missing/oddly-typed fields degrade gracefully.
5. Raises `ValueError` if no usable steps survive → the caller falls back to the KB.

`source="ai"`, and `model` records which model produced it.

---

## 4. Storage — `models/remediation_plan.py` + migration `0028`

```
remediation_plans
  id, tenant_id, engagement_id, finding_id,
  os          "linux" | "windows" | "macos" | "generic"
  plan        JSONB   (the structured schema)
  source      "ai" | "deterministic_kb"
  model        text | null
  reviewed     bool  default false
  generated_at, created_at, updated_at
  UNIQUE(finding_id, os)
```

Cached **per (finding, os)** so the AI is billed once per finding/OS. `reviewed`
gates portal visibility (Section 6). Tenancy is stored explicitly (findings have no
`tenant_id`; it's derived from the engagement at generation time).

---

## 5. Operator endpoints — `routers/remediation.py`

Operator-only (`require_role(["admin","manager"])`), tenant-scoped through the
engagement join.

- **`GET /findings/{id}/remediation?os=linux`** — the cached AI plan if present,
  else `recipe_for_finding` (KB). **Never empty.** Response carries `source`,
  `reviewed`, `cached`, `generated_at`, and the `plan`.
- **`POST /findings/{id}/remediation/generate?os=linux&force=&publish=`** — generate
  an AI plan; on any AI unavailability (`LLMUnavailableError` / unparseable output)
  fall back to the KB so a usable plan is always cached. Upserts by `(finding, os)`.
  `publish=true` sets `reviewed=true`.

---

## 6. Portal exposure — `routers/portal.py`

- **`GET /portal/findings/{id}/remediation?os=`** — customer-facing. Returns the KB
  recipe **always**, and the AI plan **only when `reviewed=true`**. This mirrors the
  report-approval gate: an unreviewed AI plan never leaks to the customer. Scoped by
  the existing `client_scoped` choke point.

The portal finding view upgrades its current plain `remediation` string to this
structured, step-by-step plan.

---

## 7. Data-flow summary

```
POST /findings/{id}/remediation/generate?os=linux&publish=true
│
├─ _tenant_finding(db, id, tenant)                      ── 404 if cross-tenant
├─ os_key = _os_key("linux") = "linux"
├─ cache hit? → return (optionally flip reviewed)
├─ LLMReportGenerator(db).available?
│    ├─ yes → generate_remediation_plan(finding, "linux")
│    │         ├─ _complete → Anthropic SDK (httpx)
│    │         ├─ _parse_json_response
│    │         └─ _normalize_ai_plan + guard (drop unsafe cmds)   source="ai"
│    └─ no / ValueError → recipe_for_finding(finding, "linux")    source="kb"
├─ upsert remediation_plans (reviewed = publish)
└─ return {finding_id, os, source, reviewed, plan}
```

---

## 8. Testing

- **KB (pure):** every category classifies; `recipe_for_finding` OS filtering;
  `network`→generic guidance; unknown→generic; every recipe step exposes all four
  OS keys with a non-empty `generic`.
- **Generator (pure helpers):** `_parse_json_response` (fences / preamble / junk→{});
  `_normalize_ai_plan` drops guard-flagged commands and flags the step; empty steps
  → `ValueError`.
- **Routes:** GET returns KB on miss (`source=deterministic_kb`) / AI on hit; POST
  caches and `publish` sets `reviewed`; cross-tenant → 404; portal returns KB unless
  `reviewed`.

---

## 9. Deliberately out of scope (YAGNI)

- **No `aiohttp` / `ResilientHTTPClient` port** — `ManagerLlmService` /
  `LLMReportGenerator` already provide transport, retry, and refusal handling.
- **No OpenRouter cost-guard** — the provider is pinned (`LLM_PROVIDER=anthropic`,
  `claude-sonnet-4-6`); see the AI-pipeline notes.
- **No new notification path** — the Slack/Jira/email work is a separate spec; the
  generate endpoint simply leaves the hook for it.
