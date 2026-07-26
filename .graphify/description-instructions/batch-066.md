# Node Description Batch 67 of 104

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

- "app_config_settings_is_production": ".is_production()" | kind=code-symbol | source=manager/backend/app/config.py:L81 | neighbors=[Settings] | lang=en
- "app_database_get_db": "get_db()" | kind=code-symbol | source=manager/backend/app/database.py:L44 | neighbors=[database.py] | lang=en
- "app_database_rationale_57": "Read-only session (no commit) routed to the replica when configured.     For SEL" | kind=entity | source=manager/backend/app/database.py:L57 | neighbors=[get_read_db()] | lang=en
- "app_dependencies_get_redis": "get_redis()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L19 | neighbors=[dependencies.py] | lang=en
- "app_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …] | lang=en
- "app_layout_metadata": "metadata" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L7 | neighbors=[layout.tsx] | lang=en
- "app_layout_rootlayout": "RootLayout()" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L12 | neighbors=[layout.tsx] | lang=en
- "app_main_gziprequestmiddleware_call": ".__call__()" | kind=code-symbol | source=manager/backend/app/main.py:L96 | neighbors=[GzipRequestMiddleware] | lang=en
- "app_main_gziprequestmiddleware_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/main.py:L93 | neighbors=[GzipRequestMiddleware] | lang=en
- "app_main_lifespan": "lifespan()" | kind=code-symbol | source=manager/backend/app/main.py:L63 | neighbors=[main.py] | lang=en
- "app_main_root_redirect": "_root_redirect()" | kind=code-symbol | source=manager/backend/app/main.py:L205 | neighbors=[main.py] | lang=en
- "app_main_unhandled_exception_handler": "unhandled_exception_handler()" | kind=code-symbol | source=manager/backend/app/main.py:L158 | neighbors=[main.py] | lang=en
- "app_page_agent": "Agent" | kind=code-symbol | source=manager/frontend/app/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "app_page_agent_status": "AGENT_STATUS" | kind=code-symbol | source=manager/frontend/app/page.tsx:L26 | neighbors=[page.tsx] | lang=en
- "app_page_agentrow": "AgentRow()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L102 | neighbors=[page.tsx] | lang=en
- "app_page_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/app/page.tsx:L21 | neighbors=[page.tsx] | lang=en
- "app_page_confidencebar": "ConfidenceBar()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L64 | neighbors=[page.tsx] | lang=en
- "app_page_dashboard": "Dashboard()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L139 | neighbors=[page.tsx] | lang=en
- "app_page_glowcard": "GlowCard()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L60 | neighbors=[page.tsx] | lang=en
- "app_page_path_status": "PATH_STATUS" | kind=code-symbol | source=manager/frontend/app/page.tsx:L26 | neighbors=[page.tsx] | lang=en
- "app_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L33 | neighbors=[page.tsx] | lang=en
- "app_page_sev_label": "SEV_LABEL" | kind=code-symbol | source=manager/frontend/app/page.tsx:L32 | neighbors=[page.tsx] | lang=en
- "app_page_widgetplaceholder": "WidgetPlaceholder()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "app_ratelimit_check": "_check()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L26 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_1": "ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi" | kind=entity | source=manager/backend/app/ratelimit.py:L1 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_17": "Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox" | kind=entity | source=manager/backend/app/ratelimit.py:L17 | neighbors=[client_ip()] | lang=pt
- "app_ratelimit_rationale_44": "FastAPI dependency factory. Keys the window by (scope, client-IP)." | kind=entity | source=manager/backend/app/ratelimit.py:L44 | neighbors=[rate_limit()] | lang=en
- "approve_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/approve/route.ts:L5 | neighbors=[route.ts] | lang=en
- "assetid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L5 | neighbors=[route.ts] | lang=en
- "assets_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L8 | neighbors=[route.ts] | lang=en
- "attack_graph_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L5 | neighbors=[route.ts] | lang=en
- "attack_paths_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L5 | neighbors=[route.ts] | lang=en
- "auth_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/auth/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_jwt_decode_token": "decode_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L53 | neighbors=[jwt.py] | lang=en
- "auth_jwt_rationale_39": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L39 | neighbors=[create_refresh_token()] | lang=en
- "auth_middleware_rationale_15": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L15 | neighbors=[TenantIsolationMiddleware] | lang=en
- "auth_middleware_rationale_21": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L21 | neighbors=[TenantIsolationMiddleware] | lang=en
- "auth_pat_pat_scope_allows": "pat_scope_allows()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L80 | neighbors=[pat.py] | lang=en
- "auth_router_list_personal_access_tokens": "list_personal_access_tokens()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L141 | neighbors=[router.py] | lang=en
- "auth_router_login": "login()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L48 | neighbors=[router.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-066.json

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
