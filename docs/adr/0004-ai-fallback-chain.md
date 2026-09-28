# ADR-0004 — Automatic AI fallback chain

Status: accepted and implemented (`feat/ai-fallback-chain`)
Date: 2026-09-28
Design with diagrams: artifact "Vedha AI Routing" — https://claude.ai/artifact/JKJ2rtmSr4dgXY11Tg3L4C
Plan: `docs/superpowers/plans/2026-09-28-ai-fallback-chain.md`

## 1. Context

- The manager could use exactly one provider per request (`LLM_PROVIDER`) plus an
  optional OpenRouter free-tier fallback, and deliberately never fell back to a second
  paid provider. In practice the only fallback had no key, so a rate limit or an empty
  balance on the one provider was a Vedha outage.
- The report generator and the advisor agent called Anthropic directly with no fallback.
- The operator chose the provider in the AI Brain UI. The requirement is the opposite:
  nobody chooses. Premium models answer while they can, and free models take over when
  premium models can't.
- Consumer subscriptions (Claude Pro/Max, ChatGPT Plus) do not include API access. The
  chain runs on API keys only.

## 2. Decision

Extend the single egress point (`ManagerLlmService`) instead of adopting a router
library. The gateway, pseudonymization and the hash-chained audit log already live
there, so every hop in the chain gets them for free. LiteLLM was rejected: its PyPI
releases 1.82.7/1.82.8 were compromised on 24 Mar 2026, and it would need the gateway
and audit rebuilt inside it. Routing all traffic through OpenRouter was rejected because
it adds a third party that sees every premium call, which conflicts with ADR-0003.

| Layer | Module | What it does |
|---|---|---|
| Order | `app/ai/routing.py` | Tiers: premium (Anthropic, OpenAI) → budget (paid Gemini) → free (Gemini free, Groq, OpenRouter) → local. `LLM_CHAIN` sets the order; the default is premium-first. Local models join only when named. |
| Quality floor | `app/ai/routing.py` | Each task sets the lowest tier allowed to answer it (reports and compliance: premium; briefs: budget; chat: free) and a total deadline. The floor relaxes to the best configured tier. |
| Failure meaning | `app/ai/failures.py` | Provider text and status map to a routing decision. The Anthropic monthly spend cap (a 429) blocks until the 1st; billing and auth problems block with an hourly re-check; rate limits honour `Retry-After`; overloads escalate. |
| Shared memory | `app/ai/kv.py`, `app/ai/health.py` | Per-provider circuit breaker (healthy / cooling / blocked / probing) in Redis, shared by every worker. If Redis is unavailable it falls back to process memory. |
| Early backoff | `app/ai/headroom.py` | When `anthropic-ratelimit-*` or `x-ratelimit-*` headers show zero remaining, the provider is cooled until its reset instead of first collecting a 429. |
| Spend | `app/ai/spend.py` | A daily USD meter from provider `usage` blocks. `AI_DAILY_CAP_USD` makes a capped provider step aside until midnight IST. |
| Reuse | `app/ai/answer_store.py` | Byte-identical one-shot requests reuse the stored answer (exact hash, never semantic). An answer written by a lower tier is regenerated once premium is healthy again. |
| Privacy | `app/services/llm.py` → `app/ai/gateway.py` | Free tiers are always pseudonymized, even under the `cloud` profile. Sovereign still offers no cloud candidate. |
| Callers | `app/ai/llm_report.py`, `app/ai/agent.py`, `app/ai/openai_tools.py` | The report generator falls back via `complete_raw`. The agent fails over to OpenAI tool calling behind an Anthropic-SDK-shaped client. |
| Visibility | `/ai/status` `chain`, `ai.attempt` logs, AI Brain | The chain order, health, spend and cap are visible. Every answer says which provider served it and whether it was a fallback. |

## 3. Consequences

- The "never a second paid provider" rule is gone. Paid-to-paid fallback is now
  visible (`fallback`, `served_by`) and bounded (daily caps) instead of forbidden.
- The auto-detect order changed from OpenAI-first to Anthropic-first. The compose
  default `LLM_PROVIDER` changed from `ollama` to empty (automatic).
- Stored answers live in Redis for `AI_ANSWER_CACHE_TTL_SECONDS` (7 days by default;
  0 disables). Redis is internal and already holds tenant-scoped cache data.
- An attempt cancelled by the deadline may already have reached the provider. No audit
  record is written for an answer that was never received.

## 4. Deferred

- Batch lane (Message Batches / OpenAI Batch, about 50% cheaper) for reports: this makes
  report generation an asynchronous, hours-long job, which is a product decision.
- The Node CLI (`frontend/cli`, `frontend/lib/agent`, `frontend/lib/engine/scanner.ts`)
  still calls Anthropic directly. It is an operator-local tool, not on the manager's
  customer-data path.
- A learned router (RouteLLM-style). The `ai.attempt` telemetry starts collecting the
  data it would need.
