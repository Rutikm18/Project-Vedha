# Node Description Batch 66 of 104

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

- "agent_use_cases_rationale_1": "use_cases.py — the finite, pre-defined library of scan scenarios the manager can" | kind=entity | source=probe/agent/use_cases.py:L1 | neighbors=[use_cases.py]
- "agent_use_cases_rationale_120": "Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id" | kind=entity | source=probe/agent/use_cases.py:L120 | neighbors=[resolve()]
- "ai_agent_agentdecisionengine_available": ".available()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L178 | neighbors=[AgentDecisionEngine]
- "ai_agent_agentdecisionengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L162 | neighbors=[AgentDecisionEngine]
- "ai_hallucination_rationale_1": "HallucinationGuard — post-generation validation of LLM report text against the g" | kind=entity | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[hallucination.py]
- "ai_hallucination_rationale_109": "Run all relevant checks and return a combined verdict:         ``{valid, issues," | kind=entity | source=manager/backend/app/ai/hallucination.py:L109 | neighbors=[.validate()]
- "ai_hallucination_rationale_46": "Flag any CVE ID mentioned in ``text`` that isn't in the real finding set." | kind=entity | source=manager/backend/app/ai/hallucination.py:L46 | neighbors=[.validate_cve_claims()]
- "ai_hallucination_rationale_61": "Flag CVSS scores in the text that don't match any real score.          ``actual_" | kind=entity | source=manager/backend/app/ai/hallucination.py:L61 | neighbors=[.validate_cvss_scores()]
- "ai_hallucination_rationale_90": "Flag destructive-looking commands that shouldn't appear in a fix guide." | kind=entity | source=manager/backend/app/ai/hallucination.py:L90 | neighbors=[.validate_remediation_commands()]
- "ai_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/ai/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_llmreportgenerator_available": ".available()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L105 | neighbors=[LLMReportGenerator]
- "ai_llm_report_llmreportgenerator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L81 | neighbors=[LLMReportGenerator]
- "ai_prioritizer_rationale_1": "VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[prioritizer.py]
- "ai_prioritizer_rationale_111": "Fit an XGBoost regressor on historical findings. ``historical_findings_df``" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L111 | neighbors=[.train()]
- "ai_prioritizer_rationale_149": "Return a 0–1000 priority score. Uses the model if trained, else the formula." | kind=entity | source=manager/backend/app/ai/prioritizer.py:L149 | neighbors=[.predict_priority()]
- "ai_prioritizer_rationale_159": "Per-feature contribution to this prediction. Uses SHAP when available;         o" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L159 | neighbors=[.explain_prediction()]
- "ai_prioritizer_rationale_205": "Weighted composite 0–1000 (same shape as the Prompt-3 enrichment formula)." | kind=entity | source=manager/backend/app/ai/prioritizer.py:L205 | neighbors=[.fallback_score()]
- "ai_prioritizer_rationale_73": "Build the model's feature vector from a Finding (+ optional Asset + extra     co" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L73 | neighbors=[extract_features()]
- "ai_prioritizer_vulnprioritizer_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L100 | neighbors=[VulnPrioritizer]
- "ai_prioritizer_vulnprioritizer_is_trained": ".is_trained()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L105 | neighbors=[VulnPrioritizer]
- "ai_report_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/route.ts:L8 | neighbors=[route.ts]
- "aibrain_page_agent": "Agent" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L15 | neighbors=[page.tsx]
- "aibrain_page_aibrainpage": "AIBrainPage()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L184 | neighbors=[page.tsx]
- "aibrain_page_animatedmessage": "AnimatedMessage()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L126 | neighbors=[page.tsx]
- "aibrain_page_barcolor": "barColor()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L100 | neighbors=[page.tsx]
- "aibrain_page_criticalchain": "criticalChain" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L74 | neighbors=[page.tsx]
- "aibrain_page_defaultagents": "defaultAgents" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L49 | neighbors=[page.tsx]
- "aibrain_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L21 | neighbors=[page.tsx]
- "aibrain_page_findings": "findings" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L57 | neighbors=[page.tsx]
- "aibrain_page_formattime": "formatTime()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L82 | neighbors=[page.tsx]
- "aibrain_page_graphstats": "graphStats" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L65 | neighbors=[page.tsx]
- "aibrain_page_initialmessage": "initialMessage" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L38 | neighbors=[page.tsx]
- "aibrain_page_message": "Message" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L8 | neighbors=[page.tsx]
- "aibrain_page_quickprompts": "quickPrompts" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L30 | neighbors=[page.tsx]
- "aibrain_page_severitycolor": "severityColor()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L87 | neighbors=[page.tsx]
- "aibrain_page_statusdot": "StatusDot()" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L109 | neighbors=[page.tsx]
- "alembic_env_do_run_migrations": "do_run_migrations()" | kind=code-symbol | source=manager/backend/alembic/env.py:L37 | neighbors=[env.py]
- "alembic_env_run_migrations_offline": "run_migrations_offline()" | kind=code-symbol | source=manager/backend/alembic/env.py:L24 | neighbors=[env.py]
- "alembic_env_run_migrations_online": "run_migrations_online()" | kind=code-symbol | source=manager/backend/alembic/env.py:L47 | neighbors=[env.py]
- "app_config_settings_cors_origins": ".cors_origins()" | kind=code-symbol | source=manager/backend/app/config.py:L77 | neighbors=[Settings]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-065.json

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
