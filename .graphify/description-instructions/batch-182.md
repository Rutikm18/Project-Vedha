# Node Description Batch 183 of 330

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

- "app_main_rationale_261": "Identify the Manager API without exposing a second dashboard." | kind=entity | source=manager/backend/app/main.py:L261 | neighbors=[_service_root()] | lang=en
- "app_main_rationale_263": "Identify the Manager API without exposing a second dashboard." | kind=entity | source=manager/backend/app/main.py:L263 | neighbors=[_service_root()] | lang=en
- "app_main_root_redirect": "_root_redirect()" | kind=code-symbol | source=manager/backend/app/main.py:L205 | neighbors=[main.py] | lang=en
- "app_main_unhandled_exception_handler": "unhandled_exception_handler()" | kind=code-symbol | source=manager/backend/app/main.py:L212 | neighbors=[main.py] | lang=en
- "app_page_agent": "Agent" | kind=code-symbol | source=manager/frontend/app/page.tsx:L27 | neighbors=[page.tsx] | lang=en
- "app_page_agent_status": "AGENT_STATUS" | kind=code-symbol | source=manager/frontend/app/page.tsx:L29 | neighbors=[page.tsx] | lang=en
- "app_page_agentrow": "AgentRow()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L117 | neighbors=[page.tsx] | lang=en
- "app_page_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/app/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "app_page_confidencebar": "ConfidenceBar()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L64 | neighbors=[page.tsx] | lang=en
- "app_page_dashboard": "Dashboard()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L19 | neighbors=[page.tsx] | lang=en
- "app_page_decisioncenter": "DecisionCenter()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "app_page_glowcard": "GlowCard()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L75 | neighbors=[page.tsx] | lang=en
- "app_page_path_status": "PATH_STATUS" | kind=code-symbol | source=manager/frontend/app/page.tsx:L26 | neighbors=[page.tsx] | lang=en
- "app_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L36 | neighbors=[page.tsx] | lang=en
- "app_page_sev_label": "SEV_LABEL" | kind=code-symbol | source=manager/frontend/app/page.tsx:L32 | neighbors=[page.tsx] | lang=en
- "app_page_widgetplaceholder": "WidgetPlaceholder()" | kind=code-symbol | source=manager/frontend/app/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "app_ratelimit_check": "_check()" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L26 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_1": "ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the exi" | kind=entity | source=manager/backend/app/ratelimit.py:L1 | neighbors=[ratelimit.py] | lang=en
- "app_ratelimit_rationale_17": "Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a     prox" | kind=entity | source=manager/backend/app/ratelimit.py:L17 | neighbors=[client_ip()] | lang=pt
- "app_ratelimit_rationale_44": "FastAPI dependency factory. Keys the window by (scope, client-IP)." | kind=entity | source=manager/backend/app/ratelimit.py:L44 | neighbors=[rate_limit()] | lang=en
- "app_version_get_version": "get_version()" | kind=code-symbol | source=manager/backend/app/version.py:L17 | neighbors=[version.py] | lang=en
- "app_version_rationale_1": "Single source of truth for the deployed application version.  The value is injec" | kind=entity | source=manager/backend/app/version.py:L1 | neighbors=[version.py] | lang=en
- "approve_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/[id]/approve/route.ts:L10 | neighbors=[route.ts] | lang=en
- "assetid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L5 | neighbors=[route.ts] | lang=en
- "assets_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L8 | neighbors=[route.ts] | lang=en
- "assistant_advisorflow_commandrow": "CommandRow()" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L46 | neighbors=[AdvisorFlow.tsx] | lang=en
- "assistant_advisorflow_copybutton": "CopyButton()" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L27 | neighbors=[AdvisorFlow.tsx] | lang=en
- "assistant_advisorflow_patch_pill": "PATCH_PILL" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L67 | neighbors=[AdvisorFlow.tsx] | lang=en
- "assistant_advisorflow_richtext": "RichText()" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L10 | neighbors=[AdvisorFlow.tsx] | lang=en
- "assistant_advisorflow_section": "Section()" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L55 | neighbors=[AdvisorFlow.tsx] | lang=en
- "assistant_assistantdrawer_explainresponse": "ExplainResponse" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L14 | neighbors=[AssistantDrawer.tsx] | lang=en
- "assistant_assistantdrawer_msg": "Msg" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L12 | neighbors=[AssistantDrawer.tsx] | lang=en
- "assistant_assistantdrawer_served": "Served" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L13 | neighbors=[AssistantDrawer.tsx] | lang=en
- "assistant_assistantprovider_assistantctx": "AssistantCtx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L20 | neighbors=[AssistantProvider.tsx] | lang=en
- "assistant_assistantprovider_ctx": "Ctx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L12 | neighbors=[AssistantProvider.tsx] | lang=en
- "assistant_assistanttext_plain": "plain()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L5 | neighbors=[AssistantText.tsx] | lang=en
- "assistant_factcard_pip": "Pip()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L10 | neighbors=[FactCard.tsx] | lang=en
- "assistant_modelswitcher_aistatus": "AiStatus" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L16 | neighbors=[ModelSwitcher.tsx] | lang=en
- "assistant_modelswitcher_providerstatus": "ProviderStatus" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L7 | neighbors=[ModelSwitcher.tsx] | lang=en
- "assistant_modelswitcher_readstored": "readStored()" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L24 | neighbors=[ModelSwitcher.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-182.json

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
