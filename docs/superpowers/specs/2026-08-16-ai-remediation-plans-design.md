# Spec — AI Remediation Plans for findings

**Date:** 2026-08-16
**Status:** in implementation

Adapts the AttackLens remediation-AI design onto Vedha. **We reuse our existing
LLM/safety/caching layers and add only the three things AttackLens does better:**
structured JSON plans, OS-awareness, and a deterministic KB fallback.

## What we reuse (NOT rebuilt)
- **LLM transport** → `ai/llm_report.py::LLMReportGenerator._complete` (Anthropic
  SDK + retry/refusal/truncation handling). No aiohttp / ResilientHTTPClient port.
- **Command safety** → `ai/hallucination.py::HallucinationGuard.validate_remediation_commands`
  (AttackLens has no equivalent).
- **Prompt-injection defense** → already in `LLMReportGenerator.SYSTEM_PROMPT`.
- **Tenant scoping** → `routers/findings.py::_tenant_finding` (findings have no
  tenant_id; scope through the engagement join).

## Components

### 1. `services/remediation_kb.py` (pure — the always-available fallback)
- `classify_finding(finding) -> str`: no `category` column exists, so classify on
  title keywords + CVE + port hints. Keys: `weak_tls`, `smb_signing`, `exposed_rdp`,
  `default_credentials`, `missing_patch`, `open_mgmt_port`, `anon_ftp`,
  `outdated_ssh`, else `generic`.
- `RECIPES`: 8 seeded recipes. Each step carries per-OS commands
  `{linux, windows, macos, generic}` + verification + risk. Plus effort,
  remediation_risk, compensating_controls, long_term_recommendations.
- `recipe_for_finding(finding, os) -> dict`: classify → recipe → filter each step's
  commands to the requested OS. `source="deterministic_kb"`. Network/appliance and
  `generic` yield guidance strings, not shell commands.

### 2. `LLMReportGenerator.generate_remediation_plan(finding, os)` (new method)
- Emits the structured JSON schema (steps w/ command/verification/risk, effort,
  remediation_risk, compensating_controls, long_term_recommendations). OS named in
  the prompt; `severity`/`cvss`/`epss_score`/`exploitable`/`exploit_validated`
  injected for urgency calibration (all local finding fields — no network).
- `_parse_json_response`: strip ``` fences, then first-`{`/last-`}` fallback.
- **Every command runs through `validate_remediation_commands`**; unsafe commands
  are stripped and the step flagged. `source="ai"`.

### 3. `models/remediation_plan.py` + migration `0028`
`RemediationPlan(id, tenant_id, engagement_id, finding_id, os, plan JSONB, source,
model, reviewed bool=false, generated_at)`, `UNIQUE(finding_id, os)`.

### 4. Endpoints (`routers/remediation.py`, operator; + portal)
- `GET /findings/{id}/remediation?os=linux` → cached AI plan if present else the KB
  recipe. **Never empty**; carries `source` + `os`.
- `POST /findings/{id}/remediation/generate?os=linux&force=&publish=` → generate,
  guard-validate, cache. `publish=true` sets `reviewed=true`. Operator-only.
- `GET /portal/findings/{id}/remediation?os=` → KB always; the AI plan only when
  `reviewed=true` (mirrors the report-approval gate so unreviewed AI never leaks).

### 5. Frontend
- Operator finding: OS selector + "Generate AI plan" button + `source` badge +
  structured steps (command/verification/risk).
- User Portal finding: upgrade the plain `remediation` string to the structured plan.

## Testing
- Pure KB: classify each seeded category; `recipe_for_finding` OS filtering;
  unknown → generic; every recipe has all 4 OS keys per command step.
- Generator: `_parse_json_response` robustness (fences, preamble, junk → {});
  unsafe-command stripping; schema shape.
- Routes: GET returns KB on miss (`source=deterministic_kb`) / AI on hit; POST
  caches + `publish` sets reviewed; tenant scoping (cross-tenant → 404); portal
  returns KB unless reviewed.

## Out of scope (YAGNI)
No aiohttp/ResilientHTTPClient port, no OpenRouter cost-guard (we pin the
provider), no new notification path (Spec 3 integrations owns that; the generate
endpoint leaves the hook).
