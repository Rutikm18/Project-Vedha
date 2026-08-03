# Node Description Batch 81 of 131

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

- "alembic_env_run_migrations_offline": "run_migrations_offline()" | kind=code-symbol | source=manager/backend/alembic/env.py:L24 | neighbors=[env.py] | lang=en
- "alembic_env_run_migrations_online": "run_migrations_online()" | kind=code-symbol | source=manager/backend/alembic/env.py:L47 | neighbors=[env.py] | lang=en
- "app_config_settings_cors_origins": ".cors_origins()" | kind=code-symbol | source=manager/backend/app/config.py:L112 | neighbors=[Settings] | lang=en
- "app_config_settings_is_production": ".is_production()" | kind=code-symbol | source=manager/backend/app/config.py:L116 | neighbors=[Settings] | lang=en
- "app_database_get_db": "get_db()" | kind=code-symbol | source=manager/backend/app/database.py:L51 | neighbors=[database.py] | lang=en
- "app_database_rationale_57": "Read-only session (no commit) routed to the replica when configured.     For SEL" | kind=entity | source=manager/backend/app/database.py:L57 | neighbors=[get_read_db()] | lang=en
- "app_database_rationale_64": "Read-only session (no commit) routed to the replica when configured.     For SEL" | kind=entity | source=manager/backend/app/database.py:L64 | neighbors=[get_read_db()] | lang=en
- "app_dependencies_get_redis": "get_redis()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L19 | neighbors=[dependencies.py] | lang=en
- "app_layout_metadata": "metadata" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L8 | neighbors=[layout.tsx] | lang=en
- "app_layout_rootlayout": "RootLayout()" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L13 | neighbors=[layout.tsx] | lang=en
- "app_main_gziprequestmiddleware_call": ".__call__()" | kind=code-symbol | source=manager/backend/app/main.py:L115 | neighbors=[GzipRequestMiddleware] | lang=en
- "app_main_gziprequestmiddleware_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/main.py:L112 | neighbors=[GzipRequestMiddleware] | lang=en
- "app_main_lifespan": "lifespan()" | kind=code-symbol | source=manager/backend/app/main.py:L64 | neighbors=[main.py] | lang=en
- "app_main_rationale_234": "Identify the Manager API without exposing a second dashboard." | kind=entity | source=manager/backend/app/main.py:L234 | neighbors=[_service_root()] | lang=en
- "app_main_root_redirect": "_root_redirect()" | kind=code-symbol | source=manager/backend/app/main.py:L205 | neighbors=[main.py] | lang=en
- "app_main_unhandled_exception_handler": "unhandled_exception_handler()" | kind=code-symbol | source=manager/backend/app/main.py:L191 | neighbors=[main.py] | lang=en
- "app_page_agent": "Agent" | kind=code-symbol | source=manager/frontend/app/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "app_page_agent_status": "AGENT_STATUS" | kind=code-symbol | source=manager/frontend/app/page.tsx:L27 | neighbors=[page.tsx] | lang=en
- "app_page_agentrow": "AgentRow()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L115 | neighbors=[page.tsx] | lang=en
- "app_page_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/app/page.tsx:L22 | neighbors=[page.tsx] | lang=en
- "app_page_confidencebar": "ConfidenceBar()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L64 | neighbors=[page.tsx] | lang=en
- "app_page_dashboard": "Dashboard()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L152 | neighbors=[page.tsx] | lang=en
- "app_page_decisioncenter": "DecisionCenter()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L53 | neighbors=[page.tsx] | lang=en
- "app_page_glowcard": "GlowCard()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L73 | neighbors=[page.tsx] | lang=en
- "app_page_path_status": "PATH_STATUS" | kind=code-symbol | source=manager/frontend/app/page.tsx:L26 | neighbors=[page.tsx] | lang=en
- "app_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L34 | neighbors=[page.tsx] | lang=en
- "app_page_sev_label": "SEV_LABEL" | kind=code-symbol | source=manager/frontend/app/page.tsx:L32 | neighbors=[page.tsx] | lang=en
- "app_page_widgetplaceholder": "WidgetPlaceholder()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "app_ratelimit_check": "_check()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L26 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_1": "ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi" | kind=entity | source=manager/backend/app/ratelimit.py:L1 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_17": "Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox" | kind=entity | source=manager/backend/app/ratelimit.py:L17 | neighbors=[client_ip()] | lang=pt
- "app_ratelimit_rationale_44": "FastAPI dependency factory. Keys the window by (scope, client-IP)." | kind=entity | source=manager/backend/app/ratelimit.py:L44 | neighbors=[rate_limit()] | lang=en
- "app_version_get_version": "get_version()" | kind=code-symbol | source=manager/backend/app/version.py:L17 | neighbors=[version.py] | lang=en
- "app_version_rationale_1": "Single source of truth for the deployed application version.  The value is injec" | kind=entity | source=manager/backend/app/version.py:L1 | neighbors=[version.py] | lang=en
- "approve_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/approve/route.ts:L4 | neighbors=[route.ts] | lang=en
- "assetid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L5 | neighbors=[route.ts] | lang=en
- "assets_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L8 | neighbors=[route.ts] | lang=en
- "assistant_assistantdrawer_msg": "Msg" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L10 | neighbors=[AssistantDrawer.tsx] | lang=en
- "assistant_assistantprovider_assistantctx": "AssistantCtx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L14 | neighbors=[AssistantProvider.tsx] | lang=en
- "assistant_assistantprovider_ctx": "Ctx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L6 | neighbors=[AssistantProvider.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-080.json

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
