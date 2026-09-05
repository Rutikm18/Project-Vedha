# Node Description Batch 69 of 336

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

- "ai_llm_report_safe_commands": "_safe_commands()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L408 | neighbors=[llm_report.py, _normalize_ai_plan(), Extract a step's command(s) and drop an…, Extract a step's command(s) and drop an…] | lang=en
- "ai_verification_graph": "verification_graph.py" | kind=code-symbol | source=manager/backend/app/ai/verification_graph.py:L1 | neighbors=[graph_available(), run_verification(), verification_graph.py — optional LangGr…, c02c465 feat(verification): optional La…] | lang=en
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L132 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware] | lang=en
- "assistant_assistantprovider_useassistant": "useAssistant()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L22 | neighbors=[AssistantDrawer.tsx, AssistantFab.tsx, AssistantProvider.tsx, page.tsx] | lang=en
- "assistant_factcard_factcard": "FactCard()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L26 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, lifecycleSummary()] | lang=en
- "auth_middleware_agent_jwt_path_allows": "agent_jwt_path_allows()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L56 | neighbors=[middleware.py, Least-privilege route allowlist for leg…, .dispatch(), Routes a customer-portal token (aud=ved…] | lang=en
- "auth_portal_scope_client_scoped": "client_scoped()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L61 | neighbors=[portal_scope.py, assert_client(), The single choke point every portal SEL…, The single choke point every portal SEL…] | lang=en
- "auth_portal_scope_require_client": "require_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L72 | neighbors=[portal_scope.py, Role gate for portal routes — 403 unles…, assert_client(), Role gate for portal routes — 403 unles…] | lang=en
- "auth_portal_scope_scoped_engagement": "scoped_engagement()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L80 | neighbors=[portal_scope.py, Route dependency yielding the client's …, resolve_scope(), Route dependency yielding the client's …] | lang=en
- "auth_rbac": "rbac.py" | kind=code-symbol | source=manager/backend/app/auth/rbac.py:L1 | neighbors=[dependencies.py, require_role(), d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_router_access_claims_for": "access_claims_for()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L56 | neighbors=[router.py, login(), The audience + scoping claims an access…, refresh()] | lang=en
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
- "components_refreshbutton_refreshbutton": "RefreshButton()" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L30 | neighbors=[PageShell.tsx, RefreshButton.tsx, page.tsx, PortalShell.tsx] | lang=en
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L54 | neighbors=[PageShell.tsx, Sidebar.tsx, page.tsx, page.tsx] | lang=en
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L26 | neighbors=[PageShell.tsx, ThemeProvider.tsx, PortalShell.tsx, page.tsx] | lang=en
- "console_primitives_meter": "Meter()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L90 | neighbors=[Primitives.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx] | lang=en
- "cve_ingest_ssl_context": "_ssl_context()" | kind=code-symbol | source=probe/cve/ingest.py:L45 | neighbors=[ingest.py, _get(), ingest_nvd(), certifi CA bundle if present, else the …] | lang=en
- "cve_online_apply": "_apply()" | kind=code-symbol | source=probe/cve/online.py:L174 | neighbors=[online.py, _was_exposed(), enrich_findings(), Fold one CVE's live result into a findi…] | lang=en
- "cve_online_lookup_nvd": "lookup_nvd()" | kind=code-symbol | source=probe/cve/online.py:L65 | neighbors=[online.py, enrich_findings(), OnlineResult, Query live NVD 2.0 for one CVE. Returns…] | lang=en
- "cve_version_compare": "compare()" | kind=code-symbol | source=probe/cve/version.py:L47 | neighbors=[version.py, parse_version(), in_range(), Return -1/0/1 for version a vs b (zero-…] | lang=en
- "cve_vulndb_norm": "_norm()" | kind=code-symbol | source=probe/cve/vulndb.py:L58 | neighbors=[vulndb.py, .add_cpe_match(), .cves_for_cpe(), .upsert_kev()] | lang=en
- "cve_vulndb_vulndb_cves_for_cpe": ".cves_for_cpe()" | kind=code-symbol | source=probe/cve/vulndb.py:L119 | neighbors=[All vulnerable CVEs whose CPE applicabi…, VulnDB, _norm(), ._enrich()] | lang=en
- "cve_weakness_map_correlate_weaknesses": "correlate_weaknesses()" | kind=code-symbol | source=probe/cve/weakness_map.py:L163 | neighbors=[weakness_map.py, _finding_view(), _mirror_cve(), Map observed weakness findings to their…] | lang=en
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L60 | neighbors=[DashboardGrid.tsx, LiveOverview.tsx, verdict(), page.tsx] | lang=en
- "dashboard_patchcomparisonmatrix_patchcomparisonmatrix": "PatchComparisonMatrix()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L70 | neighbors=[DashboardGrid.tsx, PatchComparisonMatrix.tsx, n(), page.tsx] | lang=en
- "dashboard_posturescorecard_posturescorecard": "PostureScorecard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L118 | neighbors=[DashboardGrid.tsx, PostureScorecard.tsx, usePosture(), page.tsx] | lang=en
- "detection_edr_edrqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L78 | neighbors=[.query_detections(), EDRQueryEngine, .query_detections(), .query_detections()] | lang=en
- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()] | lang=en
- "detection_engine_bridge_engagement_device_roles": "_engagement_device_roles()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L402 | neighbors=[engine_bridge.py, _persist_attack_paths(), ip → {device_role, role_detail} from al…, ip → {device_role, role_detail} from al…] | lang=en
- "detection_engine_bridge_ensure_importable": "_ensure_importable()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L76 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), _vuln_db_meta(), detect_findings_from_facts()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-068.json

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
