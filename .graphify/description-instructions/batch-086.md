# Node Description Batch 87 of 144

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "ai_prioritizer_rationale_159": "Per-feature contribution to this prediction. Uses SHAP when available;         o" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L159 | neighbors=[.explain_prediction()]
- "ai_prioritizer_rationale_205": "Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)." | kind=entity | source=manager/backend/app/ai/prioritizer.py:L205 | neighbors=[.fallback_score()]
- "ai_prioritizer_rationale_73": "Build the model's feature vector from a Finding (+ optional Asset + extra     co" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L73 | neighbors=[extract_features()]
- "ai_prioritizer_vulnprioritizer_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L100 | neighbors=[VulnPrioritizer]
- "ai_prioritizer_vulnprioritizer_is_trained": ".is_trained()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L105 | neighbors=[VulnPrioritizer]
- "ai_verification_graph_graph_available": "graph_available()" | kind=code-symbol | source=manager/backend/app/ai/verification_graph.py:L24 | neighbors=[verification_graph.py]
- "ai_verification_graph_rationale_1": "verification_graph.py — optional LangGraph orchestration for passive verificatio" | kind=entity | source=manager/backend/app/ai/verification_graph.py:L1 | neighbors=[verification_graph.py]
- "ai_verification_graph_rationale_29": "Run passive verification. Uses the LangGraph StateGraph when available;     othe" | kind=entity | source=manager/backend/app/ai/verification_graph.py:L29 | neighbors=[run_verification()]
- "aibrain_page_agent": "Agent" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L15 | neighbors=[page.tsx]
- "aibrain_page_aistatus": "AiStatus" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L24 | neighbors=[page.tsx]
- "aibrain_page_animatedmessage": "AnimatedMessage()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L126 | neighbors=[page.tsx]
- "aibrain_page_barcolor": "barColor()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L100 | neighbors=[page.tsx]
- "aibrain_page_criticalchain": "criticalChain" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L74 | neighbors=[page.tsx]
- "aibrain_page_defaultagents": "defaultAgents" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L49 | neighbors=[page.tsx]
- "aibrain_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L41 | neighbors=[page.tsx]
- "aibrain_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L21 | neighbors=[page.tsx]
- "aibrain_page_findings": "findings" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L57 | neighbors=[page.tsx]
- "aibrain_page_formattime": "formatTime()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L82 | neighbors=[page.tsx]
- "aibrain_page_graphstats": "graphStats" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L65 | neighbors=[page.tsx]
- "aibrain_page_initialmessage": "initialMessage" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L38 | neighbors=[page.tsx]
- "aibrain_page_message": "Message" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L15 | neighbors=[page.tsx]
- "aibrain_page_quickprompts": "quickPrompts" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L30 | neighbors=[page.tsx]
- "aibrain_page_severitycolor": "severityColor()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L87 | neighbors=[page.tsx]
- "aibrain_page_starter_prompts": "STARTER_PROMPTS" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L48 | neighbors=[page.tsx]
- "aibrain_page_statusdot": "StatusDot()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L109 | neighbors=[page.tsx]
- "aibrain_page_welcome": "WELCOME" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L67 | neighbors=[page.tsx]
- "alembic_env_do_run_migrations": "do_run_migrations()" | kind=code-symbol | source=manager/backend/alembic/env.py:L37 | neighbors=[env.py]
- "alembic_env_run_migrations_offline": "run_migrations_offline()" | kind=code-symbol | source=manager/backend/alembic/env.py:L24 | neighbors=[env.py]
- "alembic_env_run_migrations_online": "run_migrations_online()" | kind=code-symbol | source=manager/backend/alembic/env.py:L47 | neighbors=[env.py]
- "app_config_settings_cors_origins": ".cors_origins()" | kind=code-symbol | source=manager/backend/app/config.py:L117 | neighbors=[Settings]
- "app_config_settings_is_production": ".is_production()" | kind=code-symbol | source=manager/backend/app/config.py:L121 | neighbors=[Settings]
- "app_database_get_db": "get_db()" | kind=code-symbol | source=manager/backend/app/database.py:L51 | neighbors=[database.py]
- "app_database_rationale_57": "Read-only session (no commit) routed to the replica when configured.     For SEL" | kind=entity | source=manager/backend/app/database.py:L57 | neighbors=[get_read_db()]
- "app_database_rationale_64": "Read-only session (no commit) routed to the replica when configured.     For SEL" | kind=entity | source=manager/backend/app/database.py:L64 | neighbors=[get_read_db()]
- "app_dependencies_get_redis": "get_redis()" | kind=code-symbol | source=manager/backend/app/dependencies.py:L19 | neighbors=[dependencies.py]
- "app_layout_metadata": "metadata" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L9 | neighbors=[layout.tsx]
- "app_layout_rootlayout": "RootLayout()" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L14 | neighbors=[layout.tsx]
- "app_main_gziprequestmiddleware_call": ".__call__()" | kind=code-symbol | source=manager/backend/app/main.py:L115 | neighbors=[GzipRequestMiddleware]
- "app_main_gziprequestmiddleware_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/main.py:L112 | neighbors=[GzipRequestMiddleware]
- "app_main_lifespan": "lifespan()" | kind=code-symbol | source=manager/backend/app/main.py:L64 | neighbors=[main.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-086.json

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
