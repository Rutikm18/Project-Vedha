# Node Description Batch 3 of 236

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

- "branch:repo:github.com/Rutikm18/Project-Vedha#worktree-fleet-already-downloaded-cmd": "worktree-fleet-already-downloaded-cmd" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L33 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "basescanner": "BaseScanner" | kind=code-symbol | neighbors=[DBScanner, HostDiscoveryScanner, IoTScanner, _ConnectSweep, MCPAIScanner, MobileScanner]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L56 | neighbors=[enums.py, str, AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO]
- "agent_cli": "cli.py" | kind=code-symbol | source=probe/agent/cli.py:L1 | neighbors=[build_parser(), client_from_args(), CliError, cmd_agents_list(), cmd_auth_login(), cmd_auth_logout()]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, buildAdminCommand(), buildAskCommand(), buildDoctorCommand(), buildEngagementCommand(), buildFindingsCommand()]
- "tests_test_workflow_execution": "test_workflow_execution.py" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, port_scanner.py, scanner_base.py, _ConcurrencyScanner, _ExplodingScanner]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[base.py, DeclarativeBase, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…]
- "tests_test_main_scripts_findings_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L15 | neighbors=[test_main_scripts_findings.py, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_confirmed_and_port_hint_do_not_dou…, test_confirmed_ftp_cleartext_is_high_co…, test_confirmed_redis_is_high_confidence…]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L115 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .activate_enrollment(), .agent_id(), .agent_token(), .auth_header()]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, AgentJob]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[safety.py, Exception, Raised when a target IP is outside the …, validate_scope(), ApprovalOut, ApproveRequest]
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, fe868e6 feat(probe): real UDP amplifica…]
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DiscoveredHost, LiveFinding, ScanSummary]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, DashboardGrid.tsx, Primitives.tsx, Meter(), SeverityChip()]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, Evidence, LiveFinding, Severity]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ADJ, adjacency(), ATTACK_PATHS, AttackPath]
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[exploit_approval.py, Base, TimestampMixin, Created when a high-risk target require…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[exploit_result.py, Base, TimestampMixin, Immutable record of every exploit attem…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "routers_customer_access": "customer_access.py" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 3ad95f4 feat: Optimize asset service fe…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, c7f226f chore: bundle pending working-t…]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()]
- "main_scripts_findings_finding": "Finding" | kind=code-symbol | source=probe/main_scripts/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "scanner_findings_finding": "Finding" | kind=code-symbol | source=probe/scanner/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "scans_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, b393dbe feat: Enhance Sidebar UI and in…, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…, portal-client.ts]
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=probe/workflow/asset.py:L51 | neighbors=[asset.py, ._merge_db_scan(), ._merge_dns_scan(), ._merge_ftp_scan(), ._merge_host_discovery(), ._merge_ipmi_scan()]
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[audit_log.py, Base, Immutable, append-only audit trail for …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[base.py, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[exploit_approval.py, str, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…]
- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, Raised when an LDAP/Kerberos/SMB connec…, FindingSeverity, FindingStatus, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, Raised when an optional offensive depen…, FindingSeverity, FindingStatus, ACE]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65f22a7e7696fead81236a6770771f450c0d15a6": "65f22a7 Add comprehensive tests for authentication and admin seeding- Implement…" | kind=Commit | source=git | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, main.py, AssistantDrawer.tsx, exceptions.py, router.py, startup.py]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …]
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[FactCard.tsx, 1fe16c8 stable but some dead code, need…, 5d5c158 refactor: remove unused dashboa…, b4b12a9 Rename project and update files, Primitives.tsx, LiveOverview.tsx]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L15 | neighbors=[enums.py, str, Engagement, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ATTACK_TIMELINE, AttackAction, computeCoverage(), correlate()]

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
