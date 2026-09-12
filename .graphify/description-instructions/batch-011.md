# Node Description Batch 12 of 380

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

- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L38 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…]
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L81 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1122 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), ConsistencyReport]
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L664 | neighbors=[test_detection_core.py, .test_authoritative_tier4(), .test_multi_signal_tier2(), .test_protocol_scanner_tier3(), .test_single_banner_tier1(), ConsistencyReport]
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L629 | neighbors=[test_detection_core.py, .test_no_smb_facts_returns_none(), .test_smbv1_with_missing_hotfixes_retur…, .test_smbv1_with_patched_host_returns_n…, .test_smbv1_without_hotfix_data_returns…, ConsistencyReport]
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L525 | neighbors=[test_detection_core.py, .test_authoritative_upgrades_state(), .test_different_ids_preserved(), .test_evidence_refs_dedup_preserving_or…, .test_merges_same_id(), ConsistencyReport]
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1096 | neighbors=[test_detection_core.py, .test_classification_intermittent(), .test_classification_mostly_stable(), .test_classification_stable(), .test_rate(), ConsistencyReport]
- "tests_test_detection_core_testwilsonci": "TestWilsonCi" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1077 | neighbors=[test_detection_core.py, .test_all_appearances(), .test_perfect_appearance(), .test_zero_appearances(), .test_zero_n(), ConsistencyReport]
- "tests_test_detection_validation_testsiemparsing": "TestSIEMParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L213 | neighbors=[test_detection_validation.py, .test_elastic_parse(), .test_factory(), .test_sentinel_parse(), .test_splunk_parse(), .test_splunk_spl_includes_host_and_time…]
- "tests_test_os_fingerprint": "test_os_fingerprint.py" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 2de251b feat(scanner): ICMP timestamp f…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, TestAcceptEchoReply]
- "tests_test_pipeline": "test_pipeline.py" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 4d0377d Add unit tests for SMB scanner,…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, _banner_jsonl(), _empty_epss()]
- "tests_test_remediation_routes": "test_remediation_routes.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, _db_scalar()]
- "tests_test_service_banner_ident": "test_service_banner_ident.py" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, scanner_base.py, service_banner.py, _scanner(), _self_signed()]
- "tests_test_service_identifier_testserviceidentifier": "TestServiceIdentifier" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L6 | neighbors=[test_service_identifier.py, ._id(), .setup_method(), .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined()]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, explain_plan.py, 10dfc80 Add comprehensive probe testing…, 3ad95f4 feat: Optimize asset service fe…, 7a637eb feat: network VA accuracy, KEV …, c7f226f chore: bundle pending working-t…]
- "workflow_execution": "execution.py" | kind=code-symbol | source=probe/workflow/execution.py:L1 | neighbors=[engine.py, explain_plan.py, 7a637eb feat: network VA accuracy, KEV …, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, f473173 merge: network VA accuracy, KEV…]
- "ad_orchestrator_adassessmentrunner": "ADAssessmentRunner" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L39 | neighbors=[orchestrator.py, ._anonymous_bind_finding(), .__init__(), .run(), Coordinates all AD checkers for a singl…, ADCSChecker]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L1115 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_transport_transport_update_state": ".update_state()" | kind=code-symbol | source=probe/agent/transport.py:L283 | neighbors=[Merge and atomically persist private st…, Transport, .activate_enrollment(), .clear_manager_binding(), .clear_state(), .refresh_device_access_ex()]
- "ai_agent_agentdecisionengine": "AgentDecisionEngine" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L162 | neighbors=[agent.py, .available(), ._count(), ._create(), ._exec_read_tool(), .__init__()]
- "assistant_assistantprovider": "AssistantProvider.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantProvider.tsx:L1 | neighbors=[layout.tsx, AssistantDrawer.tsx, AssistantFab.tsx, AssistantDrawer(), AssistantFab(), AssistantCtx]
- "commands_interactive_choose": "choose()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L85 | neighbors=[interactive.ts, ask(), ln(), chooseNextPhase(), mainMenu(), pickEngagementId()]
- "commands_interactive_wizardscan": "wizardScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L329 | neighbors=[interactive.ts, mainMenu(), ask(), banner(), choose(), confirm()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2de251b6a34cad99831e042cf014ca1bcfa6aed2": "2de251b feat(scanner): ICMP timestamp fallback — echo-filter bypass + clock har…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/complete-pending-work]
- "commit:repo:github.com/Rutikm18/Project-Vedha@35691030666303cbdc4b5214a09373d49b3d2bcf": "3569103 docs(agent): research + design for Vedha Autonomous Engagement Agent" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/autonomous-offensive-agent]
- "commit:repo:github.com/Rutikm18/Project-Vedha@3e6b1872a118f010dd4de4465d55e44779434dc5": "3e6b187 feat: unify customer and manager findings workflows" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-vedha-agent-install, feat/va-maturity-gaps, main, testing/all-features]
- "commit:repo:github.com/Rutikm18/Project-Vedha@daf3de2734a3efdd04df485c8544d56209bd5554": "daf3de2 feat(scanner): add service enumeration and enrichment layer" | kind=Commit | source=git | neighbors=[6be8259 feat(integrations): outbox deli…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install]
- "console_primitives": "Primitives.tsx" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, f473173 merge: network VA accuracy, KEV…, Delta(), Meter()]
- "detection_engine_bridge_create_findings_from_facts": "create_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L541 | neighbors=[engine_bridge.py, _apply_regression_reopen(), _find_remediated_match(), _load_remediated_index(), _lock_engagement_for_detection(), _persist_attack_paths()]
- "detection_engine_version_compare": "version_compare.py" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part()]
- "graph_builder_graphbuilder": "GraphBuilder" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L90 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph(), .build_from_db()]
- "lib_cases_store": "cases-store.ts" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addComment(), Case, CaseActivity, CaseComment, CaseSeverity]
- "lib_portal_client_portalapi": "portalApi()" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L15 | neighbors=[aibrain-workspace-api.ts, campaign-workspace-api.ts, console-source.tsx, engagement-workspace-api.ts, findings-workspace-api.ts, fleet-workspace-api.ts]
- "lib_testssl_parser": "testssl-parser.ts" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, LiveFinding, Severity]
- "models_enums_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L114 | neighbors=[enums.py, str, LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _ConnectSweep, _have_masscan(), main()]
- "services_job_result_service": "job_result_service.py" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 22701ea Add tests for scanner parity an…, 3565ada fix(ingest): NUL-safe result su…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files]
- "supporting_research_evidence_store": "evidence_store.py" | kind=code-symbol | source=Supporting_research/evidence_store.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, AssetVerdict, connect(), coverage_summary(), exposure_timeline(), get_path()]
- "tests_findings_store_test": "findings-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, LiveFinding, resetCounters(), getAllFindings(), getFindingById()]
- "tests_test_ad_assessment_fakeentry": "_FakeEntry" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L36 | neighbors=[test_ad_assessment.py, .__getitem__(), .__init__(), .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-011.json

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
