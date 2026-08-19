# Node Description Batch 7 of 227

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

- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, classify_cipher(), _get_cert_der()]
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, c76b428 backend and login page error ha…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _detect_drift(), _hash()]
- "tests_test_ad_assessment_testkerberoastchecker": "TestKerberoastChecker" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L168 | neighbors=[test_ad_assessment.py, ._ldap_with_users(), .setup_method(), .test_finding_critical_when_privileged(), .test_finding_high_when_not_privileged(), .test_get_spn_accounts_filters_krbtgt_a…]
- "tests_test_async_udp": "test_async_udp.py" | kind=code-symbol | source=probe/tests/test_async_udp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, _SinkProtocol, _start_server()]
- "tests_test_detection_core_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L32 | neighbors=[test_detection_core.py, .test_add_fact_updates_first_last_seen(), .test_as_of_cutoff(), .test_facts_by_scanner(), .test_open_ports(), .test_smbv1_with_missing_hotfixes_retur…]
- "tests_test_detection_core_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L75 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_detection_core_testaggregate": "TestAggregate" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1053 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), ConsistencyReport]
- "tests_test_detection_core_testclassifytier": "TestClassifyTier" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L595 | neighbors=[test_detection_core.py, .test_authoritative_tier4(), .test_multi_signal_tier2(), .test_protocol_scanner_tier3(), .test_single_banner_tier1(), ConsistencyReport]
- "tests_test_detection_core_testcorrelatesmbpatch": "TestCorrelateSmbPatch" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L560 | neighbors=[test_detection_core.py, .test_no_smb_facts_returns_none(), .test_smbv1_with_missing_hotfixes_retur…, .test_smbv1_with_patched_host_returns_n…, .test_smbv1_without_hotfix_data_returns…, ConsistencyReport]
- "tests_test_detection_core_testdedupfindings": "TestDedupFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L483 | neighbors=[test_detection_core.py, .test_authoritative_upgrades_state(), .test_different_ids_preserved(), .test_evidence_refs_dedup_preserving_or…, .test_merges_same_id(), ConsistencyReport]
- "tests_test_detection_core_testfindingconsistency": "TestFindingConsistency" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1027 | neighbors=[test_detection_core.py, .test_classification_intermittent(), .test_classification_mostly_stable(), .test_classification_stable(), .test_rate(), ConsistencyReport]
- "tests_test_detection_core_testsuppressnegated": "TestSuppressNegated" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L516 | neighbors=[test_detection_core.py, .test_keeps_authoritative_finding(), .test_keeps_inferred_when_auth_version_…, .test_keeps_inferred_when_no_authoritat…, .test_suppresses_inferred_when_authorit…, ConsistencyReport]
- "tests_test_detection_core_testwilsonci": "TestWilsonCi" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1008 | neighbors=[test_detection_core.py, .test_all_appearances(), .test_perfect_appearance(), .test_zero_appearances(), .test_zero_n(), ConsistencyReport]
- "tests_test_detection_validation_testsiemparsing": "TestSIEMParsing" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L186 | neighbors=[test_detection_validation.py, .test_elastic_parse(), .test_factory(), .test_sentinel_parse(), .test_splunk_parse(), .test_splunk_spl_includes_host_and_time…]
- "tests_test_manager_ai": "test_manager_ai.py" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 75650c1 feat: add Posture & Patch-Compa…, config.py, _cloud(), test_ai_request_rejects_unsafe_model_an…, test_default_auto_detect_prefers_openai…]
- "tests_test_service_identifier_testserviceidentifier": "TestServiceIdentifier" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L6 | neighbors=[test_service_identifier.py, ._id(), .setup_method(), .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined()]
- "tests_test_syn_scanner": "test_syn_scanner.py" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 54503ae feat(scanner): SYN path harvest…, ae08d19 feat(scanner): adaptive timeout…, scanner_base.py, _synack_with_options(), TestAdaptiveTimeoutToggle]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=probe/tests/test_transport.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 81c81cb feat: implement outbox reclaim …, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, transport.py]
- "workflow_asset_asset": "Asset" | kind=code-symbol | source=probe/workflow/asset.py:L51 | neighbors=[asset.py, ._merge_db_scan(), ._merge_host_discovery(), ._merge_mcp_ai_scan(), ._merge_passive_collect(), ._merge_port_scan()]
- "ad_orchestrator_adassessmentrunner": "ADAssessmentRunner" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L39 | neighbors=[orchestrator.py, ._anonymous_bind_finding(), .__init__(), .run(), Coordinates all AD checkers for a singl…, ADCSChecker]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1208 | neighbors=[agent.py, main(), _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device()]
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L505 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _derive_post_stage(), _error_result(), _facts_from_cache()]
- "ai_agent_agentdecisionengine": "AgentDecisionEngine" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L161 | neighbors=[agent.py, .available(), ._count(), ._create(), ._exec_read_tool(), .__init__()]
- "ai_llm_report": "llm_report.py" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[_collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, LLMUnavailableError, _normalize_ai_plan()]
- "ai_llm_report_llmunavailableerror": "LLMUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L47 | neighbors=[llm_report.py, ._complete(), RuntimeError, Raised when the Anthropic SDK or API ke…, Raised when the Anthropic SDK or API ke…, HallucinationGuard]
- "commands_interactive_choose": "choose()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L85 | neighbors=[interactive.ts, ask(), ln(), chooseNextPhase(), mainMenu(), pickEngagementId()]
- "commands_interactive_wizardscan": "wizardScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L329 | neighbors=[interactive.ts, mainMenu(), ask(), banner(), choose(), confirm()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@01f43989ed63ef32dcf3abe8b305659ff281c464": "01f4398 feat(probe): IoT survey reaches the banner stage (service_fingerprint)" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@50d65540db573b6b680c257d3d693b216940069f": "50d6554 feat(active-validation): approve→enqueue endpoint + result ingestion (P…" | kind=Commit | source=git | neighbors=[3c277ba feat(lifecycle): add POST /find…, main.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5c8e696210c1e7beaf5f6911e452bd38c701b1e8": "5c8e696 docs(probe): correct overclaiming use-case descriptions to match curren…" | kind=Commit | source=git | neighbors=[10dfc80 Add comprehensive probe testing…, use_cases.py, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@75650c143e0e92e93ca7fed76c46893953456bf8": "75650c1 feat: add Posture & Patch-Comparison Scorecard design spec" | kind=Commit | source=git | neighbors=[agent.py, config.py, ModelSwitcher.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution]
- "commit:repo:github.com/Rutikm18/Project-Vedha@cdee859546b57100944ef98e4f180fc049700dbe": "cdee859 feat(probe): add container/cloud/infra ports to IT catalog" | kind=Commit | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "commit:repo:github.com/Rutikm18/Project-Vedha@e8262a30bd57c27b86d69584e3fee5ac6cd0af2b": "e8262a3 feat(probe): explicit unauthenticated_read fact for Redis exposure" | kind=Commit | source=git | neighbors=[95904f1 feat(probe): detect SMB signing…, backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux]
- "dashboard_exposurecards": "ExposureCards.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ExposureCards.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, DashboardGrid.tsx, Primitives.tsx, Meter(), Exposure, healthBand()]
- "detection_engine_version_compare": "version_compare.py" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part()]
- "generate_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, POST(), backend.ts, backend(), BackendError]
- "graph_builder_graphbuilder": "GraphBuilder" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L90 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph(), .build_from_db()]
- "lib_cases_store": "cases-store.ts" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addComment(), Case, CaseActivity, CaseComment, CaseSeverity]
- "lib_testssl_parser": "testssl-parser.ts" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, LiveFinding, Severity]
- "lib_with_backend_withbackend": "withBackend()" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L22 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-006.json

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
