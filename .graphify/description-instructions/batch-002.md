# Node Description Batch 3 of 380

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

- "tests_test_detection_core_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L62 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), .test_authoritative_tier4()]
- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "aibrain_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L1 | neighbors=[AIBrainPage(), AIBrainWorkspace(), AiStatus, Engagement, Message, providerLabel()]
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/fleet/page.tsx:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 1d5ae94 feat(fleet): live "Connected pr…, 25c014d feat: enhance campaign progress…, 2b4ff71 feat(fleet): one-click Approve …, 30261eb feat: enhance advisor flow with…, 7a637eb feat: network VA accuracy, KEV …]
- "commit:repo:github.com/Rutikm18/Project-Vedha@42f4e28317618b82de8e74935b9fa6cdecb6b488": "42f4e28 feat: enhance security operations UX and risk workflows" | kind=Commit | source=git | neighbors=[07ba102 feat: enhance UI UX and detecti…, layout.tsx, AssistantProvider.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity]
- "main_scripts_findings": "findings.py" | kind=code-symbol | source=probe/main_scripts/findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6c1f014 feat(correlation): implement co…, 6e2818f Add support for additional serv…, _as_dict()]
- "tests_test_detection_core": "test_detection_core.py" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 7d8d3f3 merge: resolve conflicts with o…, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, _candidate()]
- "detection_engine_ingest_ingestresult": "IngestResult" | kind=code-symbol | source=manager/detection_engine/ingest.py:L49 | neighbors=[ingest.py, ingest_file(), ingest_files(), .get_or_create_asset(), .__init__(), Asset]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L64 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@d98f65416aeabb92769aab5cba1fba3581321689": "d98f654 feat(manager): network-VA campaign, finding lifecycle timeline, AI life…" | kind=Commit | source=git | neighbors=[0236a60 fix(detection): full EPSS catal…, route.ts, FactCard.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity]
- "detection_engine_enrichment_db_epssdb": "EpssDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L24 | neighbors=[enrichment_db.py, .get(), .__init__(), load_epss(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "detection_engine_enrichment_db_kevdb": "KevDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L15 | neighbors=[enrichment_db.py, .__init__(), .is_kev(), load_kev(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "tests_test_probe_core_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L71 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "lib_portal_client": "portal-client.ts" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, 3ddc104 feat: unify customer and manage…, 3e6b187 feat: unify customer and manage…, 8f6bf49 Refactor code structure and rem…, b393dbe feat: Enhance Sidebar UI and in…, c140451 fix(portal): clean 409 on dupli…]
- "reportsection_finding_model": "finding-model.ts" | kind=code-symbol | source=reportsection/finding-model.ts:L1 | neighbors=[ef14810 Implement instance locking mech…, AGGRAVATING, assess(), AssessedFinding, attackerStatement(), Confidence]
- "scanner_findings": "findings.py" | kind=code-symbol | source=probe/scanner/findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _as_dict(), build_service_index(), _by_target()]
- "tests_test_main_scripts_findings": "test_main_scripts_findings.py" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, _ids(), _run(), test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…]
- "dashboard_dashboardgrid": "DashboardGrid.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 198bae4 snapshot: uncommitted system/ui…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…]
- "detection_engine_consistency_findingconsistency": "FindingConsistency" | kind=code-symbol | source=manager/detection_engine/consistency.py:L50 | neighbors=[consistency.py, aggregate(), .ci(), .classification(), .rate(), Finding]
- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, modulesForPorts(), bySeverityCount()]
- "scans_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…, 3c9062a refactor: Update dashboard comp…, 5c6aa54 feat(portal-ui): portal shell/p…, 7a637eb feat: network VA accuracy, KEV …]
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 315cf9c feat(frontend): refine reports …, 3c9062a refactor: Update dashboard comp…]
- "detection_engine_consistency_consistencyreport": "ConsistencyReport" | kind=code-symbol | source=manager/detection_engine/consistency.py:L86 | neighbors=[consistency.py, aggregate(), .intermittent(), .stable(), Finding, Detection engine test suite — unit test…]
- "detection_engine_verifier_evidencetier": "EvidenceTier" | kind=code-symbol | source=manager/detection_engine/verifier.py:L41 | neighbors=[verifier.py, IntEnum, Finding, FindingState, SourceConfidence, Detection engine test suite — unit test…]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[safety.py, Exception, .__init__(), Raised when a high-risk target requires…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "lib_console_source": "console-source.tsx" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L1 | neighbors=[page.tsx, 198bae4 snapshot: uncommitted system/ui…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, DashboardCharts.tsx]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L181 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .activate_enrollment(), .agent_id(), .agent_token(), .auth_header()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c59db12213dc68c991cb8a5e97cb749c0a06d33": "5c59db1 Implement instance locking mechanism to prevent multiple probe processe…" | kind=Commit | source=git | neighbors=[agent.py, engine.py, instance_lock.py, transport.py, middleware.py, router.py]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …]
- "detection_engine_vuln_db_snapshotmeta": "SnapshotMeta" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L77 | neighbors=[vuln_db.py, _merge_companion(), _read_snapshot(), load_snapshot(), Detection engine test suite — unit test…, TestAggregate]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[safety.py, Exception, Raised when a job would exceed the maxi…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[safety.py, Raised when a requested payload or modu…, Exception, validate_module(), validate_payload(), ApprovalOut]
- "portal_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, c52feb4 feat(portal): reskin User Porta…]
- "app_dependencies": "dependencies.py" | kind=code-symbol | source=manager/backend/app/dependencies.py:L1 | neighbors=[config.py, database.py, close_redis(), get_current_user(), get_redis(), main.py]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[AssistantDrawer.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, EngagementStatusControl.tsx, PageShell.tsx]
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 25c014d feat: enhance campaign progress…, 64e8290 feat(campaign): implement VA ca…, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …]
- "routers_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, c0f3b4c feat(probe-enroll): trust-on-fi…, d98f654 feat(manager): network-VA campa…, eff17d6 feat(probe): one-click approve …, config.py]
- "tests_test_main_scripts_findings_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L15 | neighbors=[test_main_scripts_findings.py, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_dou…, test_confirmed_ftp_cleartext_is_high_co…, test_confirmed_redis_is_high_confidence…]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-002.json

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
