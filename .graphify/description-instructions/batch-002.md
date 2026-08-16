# Node Description Batch 3 of 209

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DiscoveredHost, LiveFinding, ScanSummary]
- "dashboard_slastatus": "SlaStatus.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, DashboardGrid.tsx, Primitives.tsx, Meter(), SeverityChip()]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, Evidence, LiveFinding, Severity]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ADJ, adjacency(), ATTACK_PATHS, AttackPath]
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[exploit_approval.py, Base, TimestampMixin, Created when a high-risk target require…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[exploit_result.py, Base, TimestampMixin, Immutable record of every exploit attem…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, fe868e6 feat(probe): real UDP amplifica…, _dns_probe()]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()]
- "agent_transport_transport": "Transport" | kind=code-symbol | source=probe/agent/transport.py:L77 | neighbors=[transport.py, HTTP (+ future WebSocket) transport to …, .activate_enrollment(), .agent_id(), .agent_token(), .auth_header()]
- "lib_backend_backend": "backend()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L33 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "lib_adapters": "adapters.ts" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …, route.ts, route.ts]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[audit_log.py, Base, Immutable, append-only audit trail for …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[base.py, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[exploit_approval.py, str, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…]
- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, Raised when an LDAP/Kerberos/SMB connec…, FindingSeverity, FindingStatus, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, Raised when an optional offensive depen…, FindingSeverity, FindingStatus, ACE]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …]
- "lib_severity": "severity.ts" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L1 | neighbors=[FactCard.tsx, 1fe16c8 stable but some dead code, need…, 5d5c158 refactor: remove unused dashboa…, b4b12a9 Rename project and update files, Primitives.tsx, LiveOverview.tsx]
- "main_scripts_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, AdaptiveRateController, async_udp_probe(), async_udp_probe_retry(), base_argparser(), BaseScanner]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L15 | neighbors=[enums.py, str, Engagement, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ATTACK_TIMELINE, AttackAction, computeCoverage(), correlate()]
- "main_scripts_findings": "findings.py" | kind=code-symbol | source=probe/main_scripts/findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, 6c1f014 feat(correlation): implement co…, _as_dict(), build_service_index(), _by_target()]
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L637 | neighbors=[test_detection_core.py, .test_ai_cap_at_60(), .test_ai_no_cap_if_already_below(), .test_auth_enforced_penalty(), .test_authoritative_tier_base_95(), .test_backport_penalty()]
- "tests_test_probe_next_features": "test_probe_next_features.py" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, engine.py, use_cases.py, scanner_base.py, _cache_with(), test_device_inventory_post_stage_classi…]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "dashboard_dashboardgrid": "DashboardGrid.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/DashboardGrid.tsx:L1 | neighbors=[page.tsx, 5d5c158 refactor: remove unused dashboa…, Primitives.tsx, Panel(), Agent, AGENT_STATUS]
- "dashboard_liveoverview": "LiveOverview.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5d5c158 refactor: remove unused dashboa…, d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, Primitives.tsx]
- "lib_agents_store": "agents-store.ts" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Agent, AgentCapability, AGENTS, agentsStore, AgentStatus]
- "routers_customer_access": "customer_access.py" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, dependencies.py, approve_scan_request()]
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _ber_len(), _ber_parse()]
- "schemas_common_paginatedresponse": "PaginatedResponse" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L8 | neighbors=[common.py, paginate(), BaseModel, EngagementUpdate, Re-runs the detection pipeline against …, Read an UploadFile in chunks, aborting …]
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, .setup_method(), .test_compute_coverage(), .test_coverage_empty(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking()]
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L61 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "assistant_assistantdrawer": "AssistantDrawer.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantDrawer.tsx:L1 | neighbors=[AdvisorFlow.tsx, AdvisorFlow(), AssistantDrawer(), ExplainResponse, Msg, Served]
- "components_dashboardcharts": "DashboardCharts.tsx" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L1 | neighbors=[page.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 5d5c158 refactor: remove unused dashboa…, d1b4dd3 trim frontend to 7 core pages; …, ActivityItem]
- "portal_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, c52feb4 feat(portal): reskin User Porta…, portal-client.ts, GRADE_VAR, portalApi(), PortalEngagement]
- "scanner_findings": "findings.py" | kind=code-symbol | source=probe/scanner/findings.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_dict(), build_service_index(), _by_target(), _corr_cleartext_cluster(), _corr_legacy_windows()]

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
