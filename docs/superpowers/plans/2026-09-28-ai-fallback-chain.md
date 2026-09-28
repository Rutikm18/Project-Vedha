# AI Fallback Chain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every AI call in the manager picks its model automatically — Claude first, OpenAI second, budget/free models after, a no-model grounded answer last — with shared cooldowns, spend caps, stored answers and free-tier masking, so no user ever chooses a provider and a provider limit never becomes a Vedha outage.

**Architecture:** Extend the existing single egress point `ManagerLlmService` (`manager/backend/app/services/llm.py`) instead of adopting LiteLLM/OpenRouter. New pure modules under `app/ai/` hold the policy (tiers, task floors, failure classes, header parsing, spend math); a small KV abstraction (`app/ai/kv.py`, Redis with fail-open memory fallback) holds shared state. The chain walker consults them per attempt. The two Anthropic-SDK callers (`llm_report.py`, `agent.py`) gain a fallback through the same chain.

**Tech Stack:** Python 3.13, FastAPI, httpx (MockTransport in tests), redis.asyncio, pytest/pytest-asyncio; Next.js/TypeScript frontend.

**Design reference:** artifact "Vedha AI Routing" — https://claude.ai/artifact/JKJ2rtmSr4dgXY11Tg3L4C

## Global Constraints

- Work only in worktree `.claude/worktrees/ai-fallback-chain` on branch `feat/ai-fallback-chain`; stage explicit paths, never `git add -A`.
- Never `pip install` into `manager/backend/.venv` (symlinked, shared by other sessions). No new Python or npm dependencies.
- Every model call keeps going through `ManagerLlmService._dispatch` (gateway + audit chain). New callers persist `svc.audit_records`.
- Sovereign profile: cloud candidates are never offered (existing behaviour must hold).
- Ollama / local_openai appear in a chain only when named explicitly (LLM_PROVIDER or LLM_CHAIN) — never as an implicit fallback.
- Free tiers (`gemini` unless `GEMINI_PAID=true`, `groq`, `openrouter`) are ALWAYS pseudonymized, even under the `cloud` profile.
- Redis is optional for the AI path: any Redis error degrades to per-process memory and logs once (`ai.kv.redis_unavailable`).
- Tests never touch the network: provider HTTP goes through `httpx.MockTransport`; shared state through `MemoryKv` (autouse fixture).
- Run backend tests from `manager/backend` with `.venv/bin/python -m pytest`.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Out of scope (recorded decisions)

- **Batch lane** (Anthropic Message Batches / OpenAI Batch for reports): turns report generation into an hours-long async job — a product decision, not a routing change. Deferred.
- **Node CLI** (`frontend/cli/*`, `frontend/lib/agent/*`, `frontend/lib/engine/scanner.ts`): an operator-local tool with its own key, not on the manager's customer-data path. Unchanged.
- **Learned router** (RouteLLM-style): needs preference data the telemetry in this plan will start collecting.

## File Structure

| File | Status | Responsibility |
|---|---|---|
| `manager/backend/app/ai/failures.py` | create | Classify a provider failure → kind, cooldown, blocked, escalates. Pure. |
| `manager/backend/app/ai/kv.py` | create | `KvStore` protocol, `MemoryKv`, fail-open `RedisKv`, `default_kv()` |
| `manager/backend/app/ai/health.py` | create | Per-provider circuit breaker (healthy/cooling/blocked/probing) on the KV |
| `manager/backend/app/ai/routing.py` | create | Tiers, `TaskPolicy` per task, chain order, floor rule. Pure. |
| `manager/backend/app/ai/headroom.py` | create | Parse `anthropic-ratelimit-*` / `x-ratelimit-*` headers → pre-emptive cooldown seconds. Pure. |
| `manager/backend/app/ai/spend.py` | create | Token usage extraction, price table, daily spend meter + caps |
| `manager/backend/app/ai/answer_store.py` | create | Exact-hash answer reuse with upgrade-on-read |
| `manager/backend/app/ai/openai_tools.py` | create | Anthropic-SDK-shaped client over OpenAI tool calling (agent failover) |
| `manager/backend/app/services/llm.py` | modify | Groq adapter, `Runtime.tier`, free-tier masking, failure attach, reply capture, chain walker, `complete_raw`, status chain |
| `manager/backend/app/config.py` | modify | `llm_chain`, `gemini_paid`, `groq_*`, `ai_daily_cap_usd`, `ai_model_prices`, `ai_answer_cache_ttl_seconds` |
| `manager/backend/app/schemas/ai.py` | modify | `ProviderId` incl. groq, `AiChainEntry`, `AiStatusResponse.chain`, `AiGenerateResponse.tier` |
| `manager/backend/app/schemas/portal.py` | modify | `ClientAssistantReply.fallback`, `.tier` |
| `manager/backend/app/routers/ai.py`, `routers/portal.py` | modify | pass `tier`/`fallback` through |
| `manager/backend/app/ai/llm_report.py` | modify | SDK path honours health, falls back via `complete_raw` |
| `manager/backend/app/ai/agent.py` | modify | ordered client list, failover to `OpenAiToolClient` |
| `manager/backend/tests/conftest.py` | modify | autouse fresh `MemoryKv` per test |
| `manager/backend/tests/test_ai_failures.py`, `test_ai_kv.py`, `test_ai_health.py`, `test_ai_routing.py`, `test_ai_headroom.py`, `test_ai_spend.py`, `test_ai_chain.py`, `test_ai_answer_store.py`, `test_llm_report_fallback.py`, `test_ai_openai_tools.py` | create | unit + walker tests |
| `manager/frontend/app/aibrain/page.tsx`, `app/api/brain/route.ts`, `app/globals.css` | modify | chain panel replaces picker; served-by + fallback badge |
| `docker-compose.yml`, `.env.docker.example` | modify | pass new env through; document chain config |
| `docs/adr/0004-ai-fallback-chain.md` | create | decision record |

---

### Task 1: Failure classification

**Files:** Create `app/ai/failures.py`, `tests/test_ai_failures.py`; Modify `app/services/llm.py` (`_provider_error_message`, signal tuples).

**Interfaces — Produces:**
- `Failure(kind: str, cooldown_s: float | None, blocked: bool = False, escalates: bool = False)` (frozen dataclass)
- `classify_http(status: int, reason: str, retry_after: float | None = None) -> Failure`
- `parse_retry_after(value: str | None, now: datetime | None = None) -> float | None`
- `seconds_until_next_month(now: datetime | None = None) -> float`
- constants `TIMEOUT`, `NETWORK`, `INVALID_OUTPUT`, `SPEND_CAP_SIGNALS`, `BILLING_SIGNALS`, `AUTH_SIGNALS`, `ESCALATION_CAP_S = 600.0`

Rules, first match wins: spend-cap signal (`"spend limit"`, `"spending limit"`, `"usage limit"`, `"regain access"`) → `spend_cap`, blocked, cooldown until the 1st of next month UTC · billing signal or 402 → `billing`, blocked, 3600 s · 401/403 or auth signal → `auth`, blocked, 3600 s · 429 or "rate limit" → `rate_limit`, `retry_after or 60` · ≥500 or "overloaded" → `overloaded`, 30 s, escalates · else → `request`, no cooldown. `TIMEOUT = Failure("timeout", 60, escalates=True)`, `NETWORK = Failure("network", 30, escalates=True)`, `INVALID_OUTPUT = Failure("invalid_output", None)`.

- [ ] **Step 1: Write failing tests** — spend-cap 429 is blocked with cooldown equal to `seconds_until_next_month`; OpenAI `429 insufficient_quota` → billing (not rate_limit); 429 with retry_after=12 → 12, without → 60; 503 escalates; 400 malformed → `cooldown_s is None`; 401 → auth blocked; `parse_retry_after("7")==7`, HTTP-date in the future → positive seconds, `"soon"` → None; `seconds_until_next_month(datetime(2026,9,28,12,tzinfo=utc)) == 216000`; `_provider_error_message("anthropic", 429, "You have reached your specified API usage limits")` returns status 402 and mentions "spend limit".
- [ ] **Step 2: Run** `pytest tests/test_ai_failures.py -q` → FAIL (module missing).
- [ ] **Step 3: Implement** `failures.py`; in `llm.py` import the three signal tuples (keep `_BILLING_SIGNALS`/`_AUTH_SIGNALS` as aliases) and add the spend-cap branch as the FIRST check of `_provider_error_message`, returning `(f"{provider} has reached its monthly API spend limit — raise it in the {provider} console; Vedha is using the next configured provider meanwhile.", 402)`.
- [ ] **Step 4: Run** new tests + `tests/test_manager_ai.py` → PASS.
- [ ] **Step 5: Commit** `feat(ai): classify provider failures incl. Anthropic monthly spend cap`.

### Task 2: Shared KV store

**Files:** Create `app/ai/kv.py`, `tests/test_ai_kv.py`; Modify `tests/conftest.py`.

**Interfaces — Produces:** `KvStore` protocol with async `get(key)->str|None`, `set(key, value, ttl_s)`, `set_nx(key, value, ttl_s)->bool`, `delete(*keys)`, `incr(key, ttl_s)->int` (TTL set only on creation), `incr_float(key, amount, ttl_s)->float`, `ttl(key)->float|None`. `MemoryKv(clock=time.monotonic)`, `RedisKv(fallback: MemoryKv | None = None)` (uses `app.dependencies.get_redis`, every op falls back to memory on any exception, warns once), `default_kv() -> KvStore`, `set_default_kv(store | None)`.

- [ ] **Step 1: Failing tests** — MemoryKv expiry with a fake clock; `set_nx` only once; `incr` keeps original TTL; `incr_float` accumulates; `ttl` None when absent; `RedisKv` with `app.dependencies.get_redis` monkeypatched to raise still round-trips set/get via fallback.
- [ ] **Step 2:** run → FAIL.
- [ ] **Step 3: Implement** `kv.py`; add to `tests/conftest.py` an autouse function-scoped fixture `_fresh_ai_kv` that calls `set_default_kv(MemoryKv())` and resets to `None` afterwards (prevents cooldowns leaking between tests and prevents real Redis use).
- [ ] **Step 4:** run → PASS.
- [ ] **Step 5: Commit** `feat(ai): fail-open shared KV for router state`.

### Task 3: Provider health (circuit breaker)

**Files:** Create `app/ai/health.py`, `tests/test_ai_health.py`.

**Interfaces — Consumes:** `Failure`, `ESCALATION_CAP_S` (Task 1); `KvStore`, `default_kv` (Task 2). **Produces:** `HealthState(state: str, reason: str | None = None, retry_in_s: float | None = None)`; `ProviderHealth(kv: KvStore | None = None)` with async `state(p) -> HealthState`, `acquire(p) -> HealthState` (probing: only the `SET NX ai:probe:{p}` winner gets `probing`, others get `cooling/probe_in_flight`), `record_failure(p, failure)`, `record_success(p)`, `cool_for_headroom(p, seconds)`; static `ProviderHealth.allows(state) -> bool` (healthy|probing). Keys: `ai:cool:{p}` = JSON `{"reason","blocked"}` with TTL; `ai:strikes:{p}` (1 h); `ai:probe:{p}` (30 s). Escalating failures: cooldown = `min(600, base * 2**(strikes-1))`.

- [ ] **Step 1: Failing tests** — healthy by default; rate_limit → cooling w/ reason + retry; expiry → probing; first acquire allowed, second sees `probe_in_flight`; success → healthy; overloaded 30→60→120; billing → blocked; `cooldown_s=None` → no state change; headroom cooling → healthy after expiry (no probe).
- [ ] **Step 2:** FAIL. **Step 3:** implement. **Step 4:** PASS.
- [ ] **Step 5: Commit** `feat(ai): shared per-provider circuit breaker`.

### Task 4: Routing policy

**Files:** Create `app/ai/routing.py`, `tests/test_ai_routing.py`; Modify `app/config.py` (`llm_chain: str = ""`, `gemini_paid: bool = False`).

**Interfaces — Produces:** constants `PREMIUM, BUDGET, FREE, LOCAL`, `TIER_RANK = {premium:0, budget:1, free:2}`, `CLOUD_PROVIDERS = ("anthropic","openai","gemini","groq","openrouter")`, `LOCAL_PROVIDERS = ("local_openai","ollama")`; `provider_tier(provider, *, gemini_paid=False) -> str`; `TaskPolicy(lowest_tier, deadline_s, json_output=False, cacheable=False)`; `task_policy(task) -> TaskPolicy`; `chain_order(chain_csv: str, pinned: str) -> list[str]`; `allowed_by_floor(tier, lowest_tier, best_configured_rank) -> bool`; `attempt_budget(remaining_s, is_last, cap_s) -> float`.

Policies: advisor / security_followup / client_assistant → FREE, 90 s · security_brief → BUDGET, 90 s, cacheable · advisor_flow → BUDGET, 90 s, json, cacheable · remediation_refine → BUDGET, 120 s, json, cacheable · compliance_brief → PREMIUM, 90 s, cacheable · engagement_report → PREMIUM, 180 s, json, cacheable · report → PREMIUM, 240 s · unknown → FREE, 90 s.
Floor rule: LOCAL always allowed; effective floor rank = `max(rank(lowest_tier), best_configured_rank)` (an operator who configured only free models chose free models).
`attempt_budget`: last candidate → `min(remaining, cap)`; otherwise `min(cap, remaining, max(15, remaining/2))`.

- [ ] **Step 1: Failing tests** — default chain premium-first; pinned `gemini` moves first; pinned `ollama` included only when pinned; LLM_CHAIN parse drops unknown/duplicates, keeps order; `provider_tier("gemini", gemini_paid=True) == BUDGET`; floor excludes free for compliance when premium configured, allows it when only free configured; local always allowed; attempt_budget cases.
- [ ] **Step 2–4:** FAIL → implement → PASS.
- [ ] **Step 5: Commit** `feat(ai): tier + task policy + chain order`.

### Task 5: Groq provider + single provider-id type

**Files:** Modify `app/config.py` (`groq_api_key=""`, `groq_model="openai/gpt-oss-120b"`, `groq_base_url="https://api.groq.com/openai/v1"`), `app/schemas/ai.py` (`ProviderId` Literal incl. `"groq"` used in all four places), `app/services/llm.py` (`_runtime` groq branch with model allowlist, `_openai_compatible(...)` shared by `_openai`/`_groq`, dispatch, `status()` entry); Test `tests/test_ai_chain.py` (new file, groq section).

- [ ] **Step 1: Failing tests** — groq generation posts to `/openai/v1/chat/completions` with `Bearer` key and configured model; unconfigured groq → 503 "not configured"; `status()` lists `groq`.
- [ ] **Step 2–4:** FAIL → implement → PASS (plus `tests/test_manager_ai.py`).
- [ ] **Step 5: Commit** `feat(ai): Groq provider (OpenAI-compatible free tier)`.

### Task 6: Runtime tier + free-tier masking

**Files:** Modify `app/services/llm.py`: `Runtime.tier: str | None = None`; `self._tier(provider)` via `provider_tier(..., gemini_paid=settings.gemini_paid)`; every `Runtime(...)` built in `_runtime`/`_default_runtime` carries its tier; `_dispatch` uses `force_pseudonymize = settings.ai_pseudonymize or tier == FREE`. Test: `tests/test_ai_chain.py`.

- [ ] **Step 1: Failing tests** — cloud profile, gemini free: request body contains `[IP-1]` and not `10.9.8.7`, answer rehydrated; `gemini_paid=True`: raw IP sent; anthropic: raw IP sent.
- [ ] **Step 2–4:** FAIL → implement → PASS (+ `tests/test_ai_gateway.py`).
- [ ] **Step 5: Commit** `feat(ai): always pseudonymize on free tiers`.

### Task 7: Failures on errors, reply capture, headroom

**Files:** Create `app/ai/headroom.py`, `tests/test_ai_headroom.py`; Modify `app/services/llm.py`.

**Interfaces — Produces:** `AiRuntimeError(message, status_code=502, failure: Failure | None = None)`; `_REPLY_META: ContextVar[dict | None]` + `_capture_reply(response)` called by every adapter after `raise_for_status()` (stores lower-cased `headers` and parsed `body`); `headroom.parse_duration(value) -> float | None` (`"1m30s"`, `"250ms"`, `"2.5s"`); `headroom.parse_reset(value, now=None) -> float | None` (duration or RFC 3339); `headroom.headroom_cooldown(headers, now=None) -> float | None` (any requests/tokens `*-remaining` == 0 → seconds until its reset, clamp 1..300).
`_dispatch` attaches: HTTPStatusError → `classify_http(status, reason, parse_retry_after(retry-after))`; timeout → `TIMEOUT`; UnicodeEncodeError → blocked `auth`; other transport/shape errors → `NETWORK`; empty content → `INVALID_OUTPUT`.

- [ ] **Step 1: Failing tests** — headroom parsing (Anthropic RFC 3339 reset, OpenAI `"1m30s"`, remaining > 0 → None, clamp 300); `_dispatch` on 429 with `retry-after: 17` raises `AiRuntimeError` whose `failure.kind == "rate_limit"` and `cooldown_s == 17`.
- [ ] **Step 2–4:** FAIL → implement → PASS.
- [ ] **Step 5: Commit** `feat(ai): attach failure class + capture rate-limit headroom`.

### Task 8: The chain walker

**Files:** Modify `app/services/llm.py`; Modify `tests/test_manager_ai.py` (auto-detect is now Anthropic-first); Extend `tests/test_ai_chain.py`.

**Interfaces — Produces:** `ManagerLlmService(settings=None, *, transport=None, http_client=None, kv: KvStore | None = None)`; `self.health: ProviderHealth`; `_configured_chain() -> list[Runtime]`; `_candidates(task, provider=None, model=None) -> list[Runtime]` (sovereign → local only, as before; requested provider first; then configured chain; floor-filtered); `_fallback_candidates(request)` delegates; `_walk(task, system, messages, max_tokens, json_mode, candidates) -> tuple[str, Runtime, bool]`; `_default_runtime()` = first configured chain entry (sovereign logic unchanged; "No cloud AI provider is configured" message kept, now naming GROQ too).
Walker per candidate: `health.acquire` → skip unless allowed · deadline via `attempt_budget` + `asyncio.wait_for` · `_REPLY_META` set around the attempt · JSON tasks validated with `finding_ai._extract_json` (None → `INVALID_OUTPUT`, next tier) · on failure `health.record_failure` · on success `record_success`, headroom cooldown from captured headers · structured log `ai.attempt` (task, provider, model, tier, outcome, ms, failure, index) · `fallback_used = index > 0`. All skipped/failed → raise last error (or 504 "AI deadline exceeded").

- [ ] **Step 1: Failing tests** (`MockTransport` routing by host; one shared `MemoryKv`):
  1. anthropic+openai+gemini configured, anthropic 200 → served by anthropic, `fallback False`.
  2. anthropic 429 (`retry-after: 30`) → openai serves, `fallback True`; `health.state("anthropic")` cooling/rate_limit.
  3. a SECOND service instance on the same kv skips anthropic — transport sees zero anthropic calls.
  4. anthropic 429 spend-cap message → blocked.
  5. compliance_brief: anthropic+openai fail, gemini free never called, raises.
  6. compliance_brief with ONLY gemini configured → gemini serves (floor relaxes).
  7. advisor_flow: anthropic returns prose → openai serves; anthropic NOT cooling.
  8. deadline: `task_policy` patched to 0.5 s, anthropic handler sleeps 2 s → openai serves within deadline, anthropic cooling/timeout.
  9. success response with `anthropic-ratelimit-requests-remaining: 0` → anthropic cooling/headroom.
  10. default runtime with anthropic+openai keys is anthropic.
- [ ] **Step 2–4:** FAIL → implement → PASS; update `test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter` to the new Anthropic-first order; full AI test set green.
- [ ] **Step 5: Commit** `feat(ai): premium-first chain walker with shared cooldowns and deadline`.

### Task 9: Spend meter

**Files:** Create `app/ai/spend.py`, `tests/test_ai_spend.py`; Modify `app/config.py` (`ai_daily_cap_usd: str = ""` e.g. `anthropic=20,openai=10`; `ai_model_prices: str = ""` e.g. `gpt-4.1=2:8`), `app/services/llm.py` (walker skips `over_cap`, records after success; `self.spend`).

**Interfaces — Produces:** `usage_tokens(provider, body) -> tuple[float, float] | None` (anthropic incl. cache write ×1.25 / read ×0.1; openai-shaped `usage.prompt_tokens/completion_tokens`; gemini `usageMetadata`; ollama `prompt_eval_count/eval_count`); `parse_prices(csv)`, `parse_caps(csv)`; `DEFAULT_PRICES = {"claude-sonnet-4-6": (3.0, 15.0)}` (USD per 1M tokens in/out); `SpendMeter(kv, settings)` with async `record(provider, model, body) -> float`, `today(provider) -> float`, `over_cap(provider) -> bool`, and `cap(provider) -> float | None`. Key `ai:spend:{provider}:{IST date}` (48 h TTL).

- [ ] **Step 1: Failing tests** — usage parsing per provider; cost math for Sonnet (1M in + 1M out = $18); unknown model price → 0 recorded; `over_cap` flips at the cap; walker skips a capped anthropic and serves openai.
- [ ] **Step 2–4:** FAIL → implement → PASS.
- [ ] **Step 5: Commit** `feat(ai): daily spend meter with per-provider caps`.

### Task 10: Answer store

**Files:** Create `app/ai/answer_store.py`, `tests/test_ai_answer_store.py`; Modify `app/config.py` (`ai_answer_cache_ttl_seconds: int = 604800`, 0 disables), `app/services/llm.py`.

**Interfaces — Produces:** `StoredAnswer(text, provider, model, privacy, tier)`; `AnswerStore(kv, ttl_s)` with static `key(task, system, messages, lowest_tier) -> str` (`ai:ans:` + sha256 of canonical JSON), async `get(key)`, `put(key, answer)`. Walker: only when `policy.cacheable`, ttl > 0 and exactly one user message; a stored non-premium answer is ignored while any premium candidate is healthy (upgrade on read); hit → no egress, `ai.answer_store.hit` log.

- [ ] **Step 1: Failing tests** — second identical security_brief makes zero HTTP calls; different context → miss; advisor (not cacheable) never stored; a stored gemini answer is ignored when anthropic is healthy and reused when anthropic is cooling; ttl 0 disables.
- [ ] **Step 2–4:** FAIL → implement → PASS.
- [ ] **Step 5: Commit** `feat(ai): exact-hash answer reuse with upgrade-on-read`.

### Task 11: Status exposes the chain

**Files:** Modify `app/schemas/ai.py` (`AiChainEntry{provider, model, tier, state, reason, retry_in_s, spend_today_usd, daily_cap_usd}`; `AiStatusResponse.chain: list[AiChainEntry] = []`; `AiGenerateResponse.tier: str | None = None`), `app/services/llm.py` (`status()` builds chain entries from `health.state` — never `acquire`), `app/routers/ai.py` (`tier=getattr(runtime, "tier", None)`), `app/schemas/portal.py` + `app/routers/portal.py` (`fallback`, `tier` on `ClientAssistantReply`).

- [ ] **Step 1: Failing tests** — status lists anthropic/openai in order with `state == "healthy"`; after a recorded rate_limit anthropic shows `cooling`, `reason == "rate_limit"`, `retry_in_s > 0`; cap + spend reported.
- [ ] **Step 2–4:** FAIL → implement → PASS (+ portal assistant tests).
- [ ] **Step 5: Commit** `feat(ai): status reports chain health, spend and tier`.

### Task 12: Report generator falls back through the chain

**Files:** Modify `app/services/llm.py` (`complete_raw(*, task, system, messages, max_tokens, exclude=frozenset())`), `app/ai/llm_report.py`; Create `tests/test_llm_report_fallback.py`.

Behaviour: `_complete` → if an Anthropic client exists and `ProviderHealth().acquire("anthropic")` allows → `_complete_sdk` (the old body; pseudonymization moves inside it; 429 no longer retried locally; every SDK failure is recorded via `classify_http` and raised as `LLMUnavailableError`; success records health) → on `LLMUnavailableError` or when not allowed → `_complete_via_chain` (`complete_raw(task="report", ..., exclude={"anthropic"})`, audit records persisted best-effort, `ai.report.fallback` warning). `available` is true when either the SDK client exists or `complete_raw` has candidates.

- [ ] **Step 1: Failing tests** — `complete_raw` excludes anthropic and serves openai via MockTransport; generator with a client raising `anthropic.RateLimitError` → returns chain text, anthropic cooling; anthropic already cooling → SDK client never called; chain failure → `LLMUnavailableError` mentioning both causes; no Anthropic key but OpenAI key → `available is True`.
- [ ] **Step 2–4:** FAIL → implement → PASS (+ `tests/test_remediation_generator.py`).
- [ ] **Step 5: Commit** `feat(ai): report generator falls back through the chain`.

### Task 13: Advisor agent fails over to OpenAI tool calling

**Files:** Create `app/ai/openai_tools.py`, `tests/test_ai_openai_tools.py`; Modify `app/ai/agent.py`.

**Interfaces — Produces:** `to_openai_tool(tool) -> dict`, `to_openai_messages(system, messages) -> list[dict]` (Anthropic blocks → system/user/assistant+`tool_calls`/`tool` messages), `from_openai_response(data) -> SimpleNamespace(content=[blocks], stop_reason, stop_details=None)` (finish_reason tool_calls→tool_use, stop→end_turn, length→max_tokens, content_filter→refusal), `OpenAiToolClient(settings, *, http=None)` exposing `.messages.create(**kwargs)`. `AgentDecisionEngine(db, *, client=None, clients=None)` — `clients: list[tuple[name, client, model]]`; default = anthropic (if key) then openai (if usable key); `_create` walks them honouring `ProviderHealth`, records failures/success, sets `self._model` to the serving model, raises `AgentUnavailableError` when none can serve.

- [ ] **Step 1: Failing tests** — message conversion round trip (assistant tool_use → `tool_calls` with JSON args; tool_result → `role: tool`); response conversion; `OpenAiToolClient` posts the converted body via MockTransport; engine `_create` with failing anthropic + working openai returns openai's response, anthropic cooling; both failing → `AgentUnavailableError`.
- [ ] **Step 2–4:** FAIL → implement → PASS (+ `tests/test_agent_read_tools.py`).
- [ ] **Step 5: Commit** `feat(ai): advisor agent fails over to OpenAI tool calling`.

### Task 14: Frontend — automatic runtime, no picker

**Files:** Modify `manager/frontend/app/aibrain/page.tsx`, `app/api/brain/route.ts`, `app/globals.css`.

- Remove provider/model state and both `<select>`s; the send payload no longer carries `provider`/`model`.
- `AiStatus` gains `chain: ChainEntry[]`; the runtime card lists the chain in order (label, tier, state dot + reason, spend/cap when set). `ready = status?.configured || chain.some(healthy-ish)`.
- RUNTIME status item shows `AUTO · <first healthy label>`.
- Message header shows `served by <label> · <model>` and a `fallback` badge when `fallback` is true; BFF returns `fallback` and `tier`; portal replies carry the same fields.
- `providerLabel` knows `groq`.

- [ ] **Step 1:** implement. **Step 2:** `npx tsc --noEmit -p .` from `manager/frontend` → no new errors. **Step 3: Commit** `feat(ui): AI Brain shows the automatic chain instead of a provider picker`.

### Task 15: Config, compose, docs

**Files:** Modify `docker-compose.yml` (pass `LLM_CHAIN`, `GEMINI_*`, `GEMINI_PAID`, `GROQ_*`, `AI_DAILY_CAP_USD`, `AI_MODEL_PRICES`, `AI_ANSWER_CACHE_TTL_SECONDS`; `LLM_PROVIDER` default becomes empty so auto premium-first applies), `.env.docker.example` (documented block), `app/config.py` comments; Create `docs/adr/0004-ai-fallback-chain.md`.

- [ ] **Step 1:** edit. **Step 2:** `docker compose config -q` → exit 0. **Step 3: Commit** `docs(ai): fallback chain config + ADR-0004`.

### Task 16: Verification

- [ ] Full backend suite: `.venv/bin/python -m pytest tests -q` → all pass (baseline 1651 + new).
- [ ] Frontend: `npx tsc --noEmit -p .` clean for touched files.
- [ ] Live smoke (real keys from the main checkout `.env`, one tiny prompt): chain serves from Anthropic; with the Anthropic key forced invalid in-process, the answer comes from the next tier and `status()` shows anthropic `blocked/auth`.
- [ ] `graphify update .`
- [ ] Report; ask before merging to `main` / pushing; give the `.env` lines for Phase 0.

