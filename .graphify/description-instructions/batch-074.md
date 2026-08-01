# Node Description Batch 75 of 119

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "app_page_widgetplaceholder": "WidgetPlaceholder()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "app_ratelimit_check": "_check()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L26 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_1": "ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi" | kind=entity | source=manager/backend/app/ratelimit.py:L1 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_17": "Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox" | kind=entity | source=manager/backend/app/ratelimit.py:L17 | neighbors=[client_ip()] | lang=pt
- "app_ratelimit_rationale_44": "FastAPI dependency factory. Keys the window by (scope, client-IP)." | kind=entity | source=manager/backend/app/ratelimit.py:L44 | neighbors=[rate_limit()] | lang=en
- "approve_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/approve/route.ts:L4 | neighbors=[route.ts] | lang=en
- "assetid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L5 | neighbors=[route.ts] | lang=en
- "assets_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L8 | neighbors=[route.ts] | lang=en
- "assistant_assistantdrawer_msg": "Msg" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L10 | neighbors=[AssistantDrawer.tsx] | lang=en
- "assistant_assistantprovider_assistantctx": "AssistantCtx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L14 | neighbors=[AssistantProvider.tsx] | lang=en
- "assistant_assistantprovider_ctx": "Ctx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L6 | neighbors=[AssistantProvider.tsx] | lang=en
- "assistant_assistanttext_plain": "plain()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L5 | neighbors=[AssistantText.tsx] | lang=en
- "assistant_factcard_pip": "Pip()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L10 | neighbors=[FactCard.tsx] | lang=en
- "attack_graph_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L5 | neighbors=[route.ts] | lang=en
- "attack_paths_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L5 | neighbors=[route.ts] | lang=en
- "auth_jwt_decode_token": "decode_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L53 | neighbors=[jwt.py] | lang=en
- "auth_jwt_rationale_39": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L39 | neighbors=[create_refresh_token()] | lang=en
- "auth_middleware_rationale_15": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L15 | neighbors=[TenantIsolationMiddleware] | lang=en
- "auth_middleware_rationale_20": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L20 | neighbors=[TenantIsolationMiddleware] | lang=en
- "auth_middleware_rationale_21": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L21 | neighbors=[TenantIsolationMiddleware] | lang=en
- "auth_pat_pat_scope_allows": "pat_scope_allows()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L80 | neighbors=[pat.py] | lang=en
- "auth_router_list_personal_access_tokens": "list_personal_access_tokens()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L141 | neighbors=[router.py] | lang=en
- "auth_router_login": "login()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L48 | neighbors=[router.py] | lang=en
- "auth_router_me": "me()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L33 | neighbors=[router.py] | lang=en
- "auth_router_revoke_personal_access_token": "revoke_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L175 | neighbors=[router.py] | lang=en
- "basehttpmiddleware": "BaseHTTPMiddleware" | kind=code-symbol | neighbors=[TenantIsolationMiddleware] | lang=en
- "basesettings": "BaseSettings" | kind=code-symbol | neighbors=[Settings] | lang=en
- "brain_route_aimessage": "AiMessage" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L6 | neighbors=[route.ts] | lang=en
- "brain_route_evidencetext": "evidenceText()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L40 | neighbors=[route.ts] | lang=en
- "brain_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L11 | neighbors=[route.ts] | lang=en
- "chat_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L11 | neighbors=[route.ts] | lang=en
- "chat_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L20 | neighbors=[route.ts] | lang=en
- "chokepoints_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/chokepoints/route.ts:L5 | neighbors=[route.ts] | lang=en
- "cli_auth_session": "Session" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L8 | neighbors=[auth.ts] | lang=en
- "cli_auth_session_dir": "SESSION_DIR" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L5 | neighbors=[auth.ts] | lang=en
- "cli_auth_session_file": "SESSION_FILE" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L6 | neighbors=[auth.ts] | lang=en
- "cli_index_program": "program" | kind=code-symbol | source=manager/frontend/cli/index.ts:L32 | neighbors=[index.ts] | lang=en
- "cli_llm_exploitplan": "ExploitPlan" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L265 | neighbors=[llm.ts] | lang=en
- "cli_llm_phase_labels": "PHASE_LABELS" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L211 | neighbors=[llm.ts] | lang=en
- "cli_llm_phaseid": "PhaseId" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L203 | neighbors=[llm.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-074.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
