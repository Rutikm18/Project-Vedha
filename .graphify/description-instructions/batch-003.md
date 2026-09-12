# Node Description Batch 4 of 380

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

- "branch:repo:github.com/Rutikm18/Project-Vedha#worktree-fleet-already-downloaded-cmd": "worktree-fleet-already-downloaded-cmd" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@65f22a7e7696fead81236a6770771f450c0d15a6": "65f22a7 Add comprehensive tests for authentication and admin seeding- Implement…" | kind=Commit | source=git | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, main.py, AssistantDrawer.tsx, exceptions.py, router.py, startup.py] | lang=en
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 2fcec73 feat(verification): stamp verdi…, 6bb51ab feat: add detection-explain end…] | lang=en
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[FactCard.tsx, 07ba102 feat: enhance UI UX and detecti…, 1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 5d5c158 refactor: remove unused dashboa…, 7d8d3f3 merge: resolve conflicts with o…] | lang=en
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 7a637eb feat: network VA accuracy, KEV …, b4b12a9 Rename project and update files, f473173 merge: network VA accuracy, KEV…, port_scanner.py, scanner_base.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6bb51ab467a0f73fc92a18af6b6c55e2513d1c81": "6bb51ab feat: add detection-explain endpoint and enhance campaign progress UI- …" | kind=Commit | source=git | neighbors=[25c014d feat: enhance campaign progress…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "lib_with_backend": "with-backend.ts" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L1 | neighbors=[route.ts, route.ts, route.ts, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L63 | neighbors=[enums.py, str, AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO] | lang=en
- "tests_test_manager_ai": "test_manager_ai.py" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 1fe16c8 stable but some dead code, need…, 75650c1 feat: add Posture & Patch-Compa…, 7d8d3f3 merge: resolve conflicts with o…, d98f654 feat(manager): network-VA campa…, ef14810 Implement instance locking mech…] | lang=en
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, buildAdminCommand(), buildAskCommand(), buildDoctorCommand(), buildEngagementCommand(), buildFindingsCommand()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@81c81cbb1d1a039f73bc699431d61b9dd84648fe": "81c81cb feat: implement outbox reclaim tests and add enrollment token functiona…" | kind=Commit | source=git | neighbors=[agent.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ef148108da60612ce9e5bf77fc47e5d635aee273": "ef14810 Implement instance locking mechanism to prevent multiple probe processe…" | kind=Commit | source=git | neighbors=[7a12ab2 Restructure /reports into one c…, page.tsx, config.py, route.ts, 1209_system_ui_backend_level_changes, codex/customer-portal-parity] | lang=en
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, interactive.ts, 5c59db1 Implement instance locking mech…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts] | lang=en
- "generate_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/reports/generate/route.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, 5c59db1 Implement instance locking mech…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, types.ts] | lang=en
- "portal_portalshell": "PortalShell.tsx" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L1 | neighbors=[page.tsx, page.tsx, 198bae4 snapshot: uncommitted system/ui…, 5c59db1 Implement instance locking mech…, 5c6aa54 feat(portal-ui): portal shell/p…, 7a637eb feat: network VA accuracy, KEV …] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@5d5c158ce109aafccb3ad1e6407c6d6bf231a1f3": "5d5c158 refactor: remove unused dashboard components and mock data- Deleted Sla…" | kind=Commit | source=git | neighbors=[layout.tsx, page.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer] | lang=en
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 7a637eb feat: network VA accuracy, KEV …] | lang=en
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[base.py, DeclarativeBase, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…] | lang=en
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@30261ebec685fe061217d7e71faa08b5a4b6d5ea": "30261eb feat: enhance advisor flow with structured brief and probe selection- A…" | kind=Commit | source=git | neighbors=[AdvisorFlow.tsx, AssistantDrawer.tsx, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@35f02a999c05b5ec503c4c44f7f158f5d0018937": "35f02a9 feat(portal): rich scan request (type/targets/intensity) + dashboard en…" | kind=Commit | source=git | neighbors=[portal_scope.py, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@37376de4dd5dbfb3ed764fc548cb277c51ad2077": "37376de hardening(scanner): OPSEC de-sign packets + os_fingerprint correctness/…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work] | lang=en
- "dashboard_posturescorecard": "PostureScorecard.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, 6b41065 probe fixed, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…] | lang=en
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[safety.py, Exception, Raised when a target IP is outside the …, validate_scope(), ApprovalOut, ApproveRequest] | lang=en
- "report_findingreport": "FindingReport.tsx" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L1 | neighbors=[00140b3 Vendor FindingReport component …, 198bae4 snapshot: uncommitted system/ui…, 315cf9c feat(frontend): refine reports …, 76240ac UI UX Update, aee1d86 Add assessor|client mode to Fin…, severity.ts] | lang=en
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DiscoveredHost, LiveFinding, ScanSummary] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a789cca150b7688941e2f9229631f493d3fab094": "a789cca scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent] | lang=pt
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, Evidence, LiveFinding, Severity] | lang=en
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ADJ, adjacency(), ATTACK_PATHS, AttackPath] | lang=en
- "main_scripts_findings_finding": "Finding" | kind=code-symbol | source=probe/main_scripts/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()] | lang=en
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[exploit_approval.py, Base, TimestampMixin, Created when a high-risk target require…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…] | lang=en
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[exploit_result.py, Base, TimestampMixin, Immutable record of every exploit attem…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…] | lang=en
- "routers_customer_access": "customer_access.py" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 3ad95f4 feat: Optimize asset service fe…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, c7f226f chore: bundle pending working-t…] | lang=en
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=probe/scanner/db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 198bae4 snapshot: uncommitted system/ui…, d1b4dd3 trim frontend to 7 core pages; …, e8262a3 feat(probe): explicit unauthent…, build_op_msg_command(), _build_tds_prelogin()] | lang=en
- "scanner_findings_finding": "Finding" | kind=code-symbol | source=probe/scanner/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()] | lang=en
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()] | lang=en
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=probe/workflow/asset.py:L51 | neighbors=[asset.py, ._merge_db_scan(), ._merge_dns_scan(), ._merge_ftp_scan(), ._merge_host_discovery(), ._merge_ipmi_scan()] | lang=en
- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, _atomic_write_private_state(), DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), EnrollmentRequestNotFound, manager_fingerprint()] | lang=en
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-003.json

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
