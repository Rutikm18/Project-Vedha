# Node Description Batch 3 of 332

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

- "tests_test_main_scripts_findings": "test_main_scripts_findings.py" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, _ids(), _run(), test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…]
- "detection_engine_consistency_findingconsistency": "FindingConsistency" | kind=code-symbol | source=manager/detection_engine/consistency.py:L50 | neighbors=[consistency.py, aggregate(), .ci(), .classification(), .rate(), Finding]
- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, modulesForPorts(), bySeverityCount()]
- "fleet_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/fleet/page.tsx:L1 | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, 25c014d feat: enhance campaign progress…, 2b4ff71 feat(fleet): one-click Approve …, 30261eb feat: enhance advisor flow with…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…]
- "dashboard_dashboardgrid": "DashboardGrid.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L1 | neighbors=[page.tsx, 07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…]
- "detection_engine_consistency_consistencyreport": "ConsistencyReport" | kind=code-symbol | source=manager/detection_engine/consistency.py:L86 | neighbors=[consistency.py, aggregate(), .intermittent(), .stable(), Finding, Detection engine test suite — unit test…]
- "detection_engine_verifier_evidencetier": "EvidenceTier" | kind=code-symbol | source=manager/detection_engine/verifier.py:L41 | neighbors=[verifier.py, IntEnum, Finding, FindingState, SourceConfidence, Detection engine test suite — unit test…]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[safety.py, Exception, .__init__(), Raised when a high-risk target requires…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "aibrain_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/aibrain/page.tsx:L1 | neighbors=[AIBrainPage(), AiStatus, Engagement, Message, providerLabel(), STARTER_PROMPTS]
- "commit:repo:github.com/Rutikm18/Project-Vedha@42f4e28317618b82de8e74935b9fa6cdecb6b488": "42f4e28 feat: enhance security operations UX and risk workflows" | kind=Commit | source=git | neighbors=[07ba102 feat: enhance UI UX and detecti…, layout.tsx, AssistantProvider.tsx, addcapabilities-fable, main, ui-ux-backend-updates0109]
- "detection_engine_vuln_db_snapshotmeta": "SnapshotMeta" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L77 | neighbors=[vuln_db.py, _merge_companion(), _read_snapshot(), load_snapshot(), Detection engine test suite — unit test…, TestAggregate]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[safety.py, Exception, Raised when a job would exceed the maxi…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[safety.py, Raised when a requested payload or modu…, Exception, validate_module(), validate_payload(), ApprovalOut]
- "commit:repo:github.com/Rutikm18/Project-Vedha@d98f65416aeabb92769aab5cba1fba3581321689": "d98f654 feat(manager): network-VA campaign, finding lifecycle timeline, AI life…" | kind=Commit | source=git | neighbors=[0236a60 fix(detection): full EPSS catal…, route.ts, FactCard.tsx, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main]
- "routers_engagements": "engagements.py" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 25c014d feat: enhance campaign progress…, 64e8290 feat(campaign): implement VA ca…, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …]
- "routers_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, c0f3b4c feat(probe-enroll): trust-on-fi…, d98f654 feat(manager): network-VA campa…, eff17d6 feat(probe): one-click approve …, config.py]
- "scans_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 22701ea Add tests for scanner parity an…, 3c9062a refactor: Update dashboard comp…, 5c6aa54 feat(portal-ui): portal shell/p…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…]
- "tests_test_main_scripts_findings_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L15 | neighbors=[test_main_scripts_findings.py, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_dou…, test_confirmed_ftp_cleartext_is_high_co…, test_confirmed_redis_is_high_confidence…]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "app_dependencies": "dependencies.py" | kind=code-symbol | source=manager/backend/app/dependencies.py:L1 | neighbors=[config.py, database.py, close_redis(), get_current_user(), get_redis(), main.py]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L181 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .activate_enrollment(), .agent_id(), .agent_token(), .auth_header()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#worktree-fleet-already-downloaded-cmd": "worktree-fleet-already-downloaded-cmd" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "portal_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, c52feb4 feat(portal): reskin User Porta…, f473173 merge: network VA accuracy, KEV…]
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 7a637eb feat: network VA accuracy, KEV …, b4b12a9 Rename project and update files, f473173 merge: network VA accuracy, KEV…, port_scanner.py, scanner_base.py]
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L63 | neighbors=[enums.py, str, AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, buildAdminCommand(), buildAskCommand(), buildDoctorCommand(), buildEngagementCommand(), buildFindingsCommand()]
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[page.tsx, 07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c9062a refactor: Update dashboard comp…, 42f4e28 feat: enhance security operatio…]
- "components_pageshell": "PageShell.tsx" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L1 | neighbors=[page.tsx, page.tsx, page.tsx, 07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2fcec73 feat(verification): stamp verdi…, 6bb51ab feat: add detection-explain end…]
- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…]
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …]
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[FactCard.tsx, 07ba102 feat: enhance UI UX and detecti…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 5d5c158 refactor: remove unused dashboa…, 7d8d3f3 merge: resolve conflicts with o…]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[base.py, DeclarativeBase, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…]
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …]
- "dashboard_posturescorecard": "PostureScorecard.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 6b41065 probe fixed, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, AgentJob]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[safety.py, Exception, Raised when a target IP is outside the …, validate_scope(), ApprovalOut, ApproveRequest]
- "lib_portal_client": "portal-client.ts" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L1 | neighbors=[page.tsx, 22701ea Add tests for scanner parity an…, 8f6bf49 Refactor code structure and rem…, b393dbe feat: Enhance Sidebar UI and in…, c140451 fix(portal): clean 409 on dupli…, c52feb4 feat(portal): reskin User Porta…]

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
