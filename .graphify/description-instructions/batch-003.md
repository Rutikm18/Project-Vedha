# Node Description Batch 4 of 332

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

- "routers_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 7a637eb feat: network VA accuracy, KEV …, b393dbe feat: Enhance Sidebar UI and in…, c52feb4 feat(portal): reskin User Porta…, c7f226f chore: bundle pending working-t…]
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[interactive.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, DiscoveredHost, LiveFinding, ScanSummary]
- "base": "Base" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, AuditLog]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, interactive.ts, d1b4dd3 trim frontend to 7 core pages; …, Evidence, LiveFinding, Severity]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, ADJ, adjacency(), ATTACK_PATHS, AttackPath]
- "main_scripts_findings_finding": "Finding" | kind=code-symbol | source=probe/main_scripts/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "models_exploit_approval_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L19 | neighbors=[exploit_approval.py, Base, TimestampMixin, Created when a high-risk target require…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "models_exploit_result_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L11 | neighbors=[exploit_result.py, Base, TimestampMixin, Immutable record of every exploit attem…, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "routers_customer_access": "customer_access.py" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, 3ad95f4 feat: Optimize asset service fe…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, c7f226f chore: bundle pending working-t…]
- "scanner_findings_finding": "Finding" | kind=code-symbol | source=probe/scanner/findings.py:L63 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract()]
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=probe/workflow/asset.py:L51 | neighbors=[asset.py, ._merge_db_scan(), ._merge_dns_scan(), ._merge_ftp_scan(), ._merge_host_discovery(), ._merge_ipmi_scan()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65f22a7e7696fead81236a6770771f450c0d15a6": "65f22a7 Add comprehensive tests for authentication and admin seeding- Implement…" | kind=Commit | source=git | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, main.py, AssistantDrawer.tsx, exceptions.py, router.py, startup.py]
- "lib_console_source": "console-source.tsx" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L1 | neighbors=[page.tsx, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…, DashboardCharts.tsx, DashboardGrid.tsx]
- "lib_fetcher": "fetcher.ts" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L1 | neighbors=[page.tsx, page.tsx, AssistantDrawer.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …]
- "tests_test_detection_validation_testdetectioncorrelator": "TestDetectionCorrelator" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L49 | neighbors=[test_detection_validation.py, .setup_method(), .test_compute_coverage(), .test_coverage_empty(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking()]
- "workflow_gates": "gates.py" | kind=code-symbol | source=probe/workflow/gates.py:L1 | neighbors=[explain_plan.py, local_run.py, 10dfc80 Add comprehensive probe testing…, 64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …]
- "app_config": "config.py" | kind=code-symbol | source=manager/backend/app/config.py:L1 | neighbors=[agent.py, llm_report.py, env.py, get_settings(), Settings, database.py]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "models_audit_log_auditlog": "AuditLog" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L11 | neighbors=[audit_log.py, Base, Immutable, append-only audit trail for …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "models_base_timestampmixin": "TimestampMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L13 | neighbors=[base.py, Agent, AgentStatus, AgentRecommendation, agent_recommendation.py — decisions/act…, Asset]
- "models_enums_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L15 | neighbors=[enums.py, str, Operator-set lifecycle. `ongoing` (asse…, Engagement, EngagementUpdate, Re-runs the detection pipeline against …]
- "models_exploit_approval_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L12 | neighbors=[exploit_approval.py, str, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…]
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, 95904f1 feat(probe): detect SMB signing…]
- "states_datastate": "DataState.tsx" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L1 | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx]
- "tests_test_campaign_progress": "test_campaign_progress.py" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L1 | neighbors=[25c014d feat: enhance campaign progress…, 64e8290 feat(campaign): implement VA ca…, 6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _beat()]
- "ad_findings_adconnectionerror": "ADConnectionError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L26 | neighbors=[findings.py, ADError, Raised when an LDAP/Kerberos/SMB connec…, FindingSeverity, FindingStatus, ACE]
- "ad_findings_dependencymissingerror": "DependencyMissingError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L30 | neighbors=[findings.py, ADError, Raised when an optional offensive depen…, FindingSeverity, FindingStatus, ACE]
- "agent_transport": "transport.py" | kind=code-symbol | source=probe/agent/transport.py:L1 | neighbors=[agent.py, _atomic_write_private_state(), DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), EnrollmentRequestNotFound, manager_fingerprint()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6bb51ab467a0f73fc92a18af6b6c55e2513d1c81": "6bb51ab feat: add detection-explain endpoint and enhance campaign progress UI- …" | kind=Commit | source=git | neighbors=[25c014d feat: enhance campaign progress…, addcapabilities-fable, main, ui-ux-backend-updates0109, 07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@81c81cbb1d1a039f73bc699431d61b9dd84648fe": "81c81cb feat: implement outbox reclaim tests and add enrollment token functiona…" | kind=Commit | source=git | neighbors=[agent.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "tests_test_va_campaign": "test_va_campaign.py" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, scanner_base.py, va_campaign.py, _Buf, _detect_stage()]
- "timestampmixin": "TimestampMixin" | kind=code-symbol | neighbors=[Agent, AgentRecommendation, Asset, AttackPath, AttackTimeline, DetectionConfig]
- "agent_tools": "tools.ts" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L1 | neighbors=[agent.py, AgentState, mergeHosts(), persistAgentFindings(), Risk, runOnePhase()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5d5c158ce109aafccb3ad1e6407c6d6bf231a1f3": "5d5c158 refactor: remove unused dashboard components and mock data- Deleted Sla…" | kind=Commit | source=git | neighbors=[layout.tsx, page.tsx, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "engagements_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…]
- "lib_detection_store": "detection-store.ts" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ATTACK_TIMELINE, AttackAction, computeCoverage(), correlate()]
- "tests_test_detection_core_testverify": "TestVerify" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L706 | neighbors=[test_detection_core.py, .test_ai_cap_at_60(), .test_ai_no_cap_if_already_below(), .test_auth_enforced_penalty(), .test_authoritative_tier_base_95(), .test_backport_penalty()]
- "tests_test_probe_next_features": "test_probe_next_features.py" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, engine.py, use_cases.py, scanner_base.py, _cache_with(), test_device_inventory_post_stage_classi…]
- "workers_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 6bb51ab feat: add detection-explain end…, 6be8259 feat(integrations): outbox deli…, 81c81cb feat: implement outbox reclaim …, 8f6bf49 Refactor code structure and rem…]

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
