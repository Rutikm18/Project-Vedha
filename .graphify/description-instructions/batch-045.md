# Node Description Batch 46 of 209

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

- "ai_verification_graph": "verification_graph.py" | kind=code-symbol | source=manager/backend/app/ai/verification_graph.py:L1 | neighbors=[graph_available(), run_verification(), verification_graph.py — optional LangGr…, c02c465 feat(verification): optional La…] | lang=en
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L118 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware] | lang=en
- "assistant_assistantprovider_useassistant": "useAssistant()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L16 | neighbors=[AssistantDrawer.tsx, AssistantFab.tsx, AssistantProvider.tsx, page.tsx] | lang=en
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L65 | neighbors=[TenantIsolationMiddleware, agent_jwt_path_allows(), _is_public_enrollment_request(), ._authenticate_pat()] | lang=en
- "auth_portal_scope_client_scoped": "client_scoped()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L61 | neighbors=[portal_scope.py, assert_client(), The single choke point every portal SEL…, The single choke point every portal SEL…] | lang=en
- "auth_portal_scope_require_client": "require_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L72 | neighbors=[portal_scope.py, Role gate for portal routes — 403 unles…, assert_client(), Role gate for portal routes — 403 unles…] | lang=en
- "auth_portal_scope_scoped_engagement": "scoped_engagement()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L80 | neighbors=[portal_scope.py, Route dependency yielding the client's …, resolve_scope(), Route dependency yielding the client's …] | lang=en
- "auth_rbac": "rbac.py" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L1 | neighbors=[dependencies.py, require_role(), d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_router_authenticate": "_authenticate()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L58 | neighbors=[router.py, login(), Validates credentials and returns the U…, Validates credentials and returns the U…] | lang=en
- "auth_startup_check_admin_account": "_check_admin_account()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L159 | neighbors=[startup.py, CheckResult, Verify the seeded admin account exists …, run_startup_diagnostics()] | lang=en
- "auth_startup_check_bcrypt": "_check_bcrypt()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L147 | neighbors=[startup.py, CheckResult, Verify the bcrypt library can round-tri…, run_startup_diagnostics()] | lang=en
- "auth_startup_check_tenant": "_check_tenant()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L197 | neighbors=[startup.py, CheckResult, Verify the default tenant is active., run_startup_diagnostics()] | lang=en
- "auth_startup_startupaborterror": "StartupAbortError" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L92 | neighbors=[startup.py, Raised when one or more fatal checks fa…, run_startup_diagnostics(), RuntimeError] | lang=en
- "commands_interactive_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L104 | neighbors=[interactive.ts, ln(), runInteractive(), wizardScan()] | lang=en
- "commands_interactive_choosenextphase": "chooseNextPhase()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L927 | neighbors=[interactive.ts, choose(), ln(), runIterativeEngagement()] | lang=en
- "commands_interactive_pickmodulesbycategory": "pickModulesByCategory()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L300 | neighbors=[interactive.ts, confirm(), ln(), wizardScan()] | lang=en
- "commands_interactive_runrulebasedvalidation": "runRuleBasedValidation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1355 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardstatus": "wizardStatus()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1938 | neighbors=[interactive.ts, mainMenu(), divider(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 298a9d4 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, a388bb3 script updated, architecture de…, f5ce592 first commit] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, agents/greeting-introduction, main, bd7383f scanner fine ..now integrations] | lang=fr
- "components_queryprovider": "QueryProvider.tsx" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, QueryProvider(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L53 | neighbors=[PageShell.tsx, Sidebar.tsx, page.tsx, page.tsx] | lang=en
- "console_primitives_meter": "Meter()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L86 | neighbors=[Primitives.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx] | lang=en
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L61 | neighbors=[DashboardGrid.tsx, LiveOverview.tsx, verdict(), page.tsx] | lang=en
- "dashboard_patchcomparisonmatrix_patchcomparisonmatrix": "PatchComparisonMatrix()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L70 | neighbors=[DashboardGrid.tsx, PatchComparisonMatrix.tsx, n(), page.tsx] | lang=en
- "dashboard_posturescorecard_posturescorecard": "PostureScorecard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L105 | neighbors=[DashboardGrid.tsx, PostureScorecard.tsx, usePosture(), page.tsx] | lang=en
- "detection_correlator_aware": "_aware()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L209 | neighbors=[correlator.py, ._in_window(), ._min_latency(), Normalise naive datetimes to UTC so com…] | lang=en
- "detection_edr_edrqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L78 | neighbors=[.query_detections(), EDRQueryEngine, .query_detections(), .query_detections()] | lang=en
- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()] | lang=en
- "detection_engine_bridge_apply_regression_reopen": "_apply_regression_reopen()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L113 | neighbors=[engine_bridge.py, create_findings_from_facts(), A previously-remediated finding whose i…, A previously-remediated finding whose i…] | lang=en
- "detection_engine_bridge_find_remediated_match": "_find_remediated_match()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L129 | neighbors=[engine_bridge.py, create_findings_from_facts(), A remediated finding with the same (eng…, A remediated finding with the same (eng…] | lang=en
- "detection_engine_bridge_persist_attack_paths": "_persist_attack_paths()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L171 | neighbors=[engine_bridge.py, create_findings_from_facts(), _engagement_device_roles(), Correlate composite attack paths from t…] | lang=en
- "detection_engine_bridge_stamp_verification": "_stamp_verification()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L141 | neighbors=[engine_bridge.py, create_findings_from_facts(), Best-effort: compute + stamp each findi…, Best-effort: compute + stamp each findi…] | lang=en
- "detection_engine_consistency_aggregate": "aggregate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L100 | neighbors=[consistency.py, ConsistencyReport, FindingConsistency, run_findings: one list of Findings per …] | lang=en
- "detection_engine_cvss_base_score": "base_score()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L43 | neighbors=[cvss.py, parse_vector(), _roundup(), Returns the CVSS v3.1 base score (0.0-1…] | lang=en
- "detection_engine_enrichment_db_load_epss": "load_epss()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L69 | neighbors=[enrichment_db.py, _cache_key(), EpssDB, .get()] | lang=en
- "detection_engine_enrichment_db_load_kev": "load_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L55 | neighbors=[enrichment_db.py, _cache_key(), .get(), KevDB] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-045.json

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
