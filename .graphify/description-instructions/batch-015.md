# Node Description Batch 16 of 380

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@2be040ca5c7a29aa1dd6caa2bfefb6f305d23693": "2be040c improve(probe/install): portability, supply-chain, ops hardening" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5b980e1cf0c571409a6d765442112df458b0456f": "5b980e1 docs(spec): installer warning + fleet job visibility + engagement host-…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b41065b13542a7c39f04677314b02d8698bce31": "6b41065 probe fixed" | kind=Commit | source=git | neighbors=[agent.py, transport.py, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9e188b89006db238b7f9a09dd1b17eb4eba7ad87": "9e188b8 fix(probe/install): LOCAL preflight + self-healing venv + daemon/lock g…" | kind=Commit | source=git | neighbors=[22e4f8d chore: update version, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "components_themeprovider": "ThemeProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L1 | neighbors=[layout.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, subscribeToHydration()]
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L35 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…]
- "lib_evidence_presentation": "evidence-presentation.ts" | kind=code-symbol | source=manager/frontend/lib/evidence-presentation.ts:L1 | neighbors=[315cf9c feat(frontend): refine reports …, 76240ac UI UX Update, ce7ab6e Merge origin/main: reconcile fi…, page.tsx, adapters.ts, EvidenceArtifact]
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[ask.ts, findings.ts, interactive.ts, findings-store.ts, deleteFinding(), ensureDir()]
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()]
- "lib_reports_workspace_api": "reports-workspace-api.ts" | kind=code-symbol | source=manager/frontend/lib/reports-workspace-api.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, adapters.ts, toUiEngagement(), toUiFinding(), fetcher.ts, fetchJson()]
- "lib_scanner_request_validation": "scanner-request-validation.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L1 | neighbors=[b4b12a9 Rename project and update files, isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest]
- "lib_scanner_workspace_api": "scanner-workspace-api.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-workspace-api.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, CampaignProgress.tsx, RawFacts.tsx, adapters.ts, toUiEngagement(), fetcher.ts]
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, TimestampMixin, Base, TimestampMixin, AgentRegisterRequest]
- "routers_ai_report_reviewrequest": "ReviewRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L52 | neighbors=[ai_report.py, RejectRequest, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset]
- "routers_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2cddd52 fix(posture): tenant-scope run …, 9de087a feat(posture): add GET /analyti…, a0b870c fix(posture): score over open f…, dependencies.py, exposure()]
- "routers_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, configure_siem(), get_coverage(), get_gaps()]
- "routers_validation": "validation.py" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, dependencies.py, approve_validation(), create_validation_request(), _default_check_kind(), _get_request_or_404()]
- "routers_vuln_scans_findingimport": "FindingImport" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L49 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nessusscanrequest": "NessusScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L35 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "routers_vuln_scans_nucleiscanrequest": "NucleiScanRequest" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L43 | neighbors=[vuln_scans.py, BaseModel, Asset, Engagement, FindingSeverity, FindingStatus]
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 37376de hardening(scanner): OPSEC de-si…, d1b4dd3 trim frontend to 7 core pages; …, _auth_shaped_json_body(), _known_false_positive(), main()]
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _coverage(), _device_hint(), _is_readable(), _listener_error_code()]
- "scanner_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, build_default_funnel(), _candidate_ports(), FunnelResult]
- "scripts_startup_validator": "startup_validator.py" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator]
- "str": "str" | kind=code-symbol | neighbors=[FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType, DetectionStatus]
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, .test_attack_narrative_carried_in_evide…, .test_invalid_severity_falls_back_to_in…, .test_required_fields_present(), ADCSChecker, CertTemplate]
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_detection_validation_action": "_action()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L37 | neighbors=[test_detection_validation.py, .test_compute_coverage(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking(), .test_gap_report_ignores_detected(), .test_generate_gap_report()]
- "tests_test_finding_ai": "test_finding_ai.py" | kind=code-symbol | source=manager/backend/tests/test_finding_ai.py:L1 | neighbors=[ef14810 Implement instance locking mech…, _f(), _llm_returning(), _run(), test_empty_or_whitespace_values_are_rej…, test_json_wrapped_in_code_fences_is_par…]
- "tests_test_finding_content": "test_finding_content.py" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L1 | neighbors=[ef14810 Implement instance locking mech…, _f(), test_active_exploitation_adds_urgency_t…, test_business_impact_scales_up_for_a_cr…, test_cves_are_woven_into_technical_deta…, test_epss_thresholds_map_to_maturity_ba…]
- "tests_test_online": "test_online.py" | kind=code-symbol | source=probe/tests/test_online.py:L1 | neighbors=[6e2818f Add support for additional serv…, cli.py, correlator.py, online.py, _finding(), _get_raising()]
- "tests_test_pipeline_openssh_vuln_db": "_openssh_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L49 | neighbors=[test_pipeline.py, _mock_vuln_db(), Returns a VulnDB with a record that mat…, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default()]
- "tests_test_portal_finding_actions": "test_portal_finding_actions.py" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 3ddc104 feat: unify customer and manage…, 3e6b187 feat: unify customer and manage…, _client(), _finding(), test_customer_cannot_mutate_a_finding_o…]
- "tests_test_posture_rules_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L22 | neighbors=[test_posture_rules.py, ._host(), .test_dedup_same_rule_same_port(), .test_detect_all_sorts_by_risk_desc(), .test_deterministic_id_across_runs(), .test_unvalidated_scanner_only_suspects…]
- "tests_test_posture_rules_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L15 | neighbors=[test_posture_rules.py, ._host(), .test_dedup_same_rule_same_port(), .test_detect_all_sorts_by_risk_desc(), .test_deterministic_id_across_runs(), .test_unvalidated_scanner_only_suspects…]
- "tests_test_scanner_congestion_scanner": "_scanner()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L139 | neighbors=[test_scanner_congestion.py, .test_floor_scales_with_concurrency(), .test_all_silent_host_shrinks_the_windo…, .test_congestion_can_be_disabled(), .test_responsive_host_is_not_throttled(), .test_scan_completes_every_port_under_t…]
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, currentPlatform(), Platform, TOOL_MANIFEST]
- "workflow_execution_executiontrace": "ExecutionTrace" | kind=code-symbol | source=probe/workflow/execution.py:L243 | neighbors=[execution.py, .as_list(), .degraded(), ._ensure(), .failed(), .finalize()]
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L55 | neighbors=[ldap_enum.py, .get_users(), ADConnectionError, DependencyMissingError, _FakeAttr, _FakeEntry]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-015.json

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
