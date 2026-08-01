# Node Description Batch 26 of 119

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

- "schemas_finding_slasummary": "SlaSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L44 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin": "seed_admin.py" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, database.py, seed(), Idempotent admin seeder.  Creates a ten…, 298a9d4 trim frontend to 7 core pages; …]
- "services_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, compute_exposure(), _sev(), Exposure analytics — protocol risk + zo…, 2885afa Add comprehensive probe testing…]
- "services_sla_compute": "compute()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L60 | neighbors=[sla.py, SlaResult, _windows(), Compute the SLA state for one finding. …, summarize()]
- "services_sla_slaresult": "SlaResult" | kind=code-symbol | source=manager/backend/app/services/sla.py:L46 | neighbors=[sla.py, compute(), FindingStatus, Finding, .is_tracked()]
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L106 | neighbors=[page.tsx, page.tsx, page.tsx, page.tsx, DataState.tsx]
- "tests_test_ad_assessment_enum_with_entries": "_enum_with_entries()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L45 | neighbors=[test_ad_assessment.py, .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_agent_dispatch_testusecasecatalogparity": "TestUseCaseCatalogParity" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L35 | neighbors=[test_agent_dispatch.py, ScanJobStatus, ScanJobType, .test_manager_and_probe_route_use_cases…, AgentConnectionManager]
- "tests_test_agents_testregisteragent": "TestRegisterAgent" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L526 | neighbors=[test_agents.py, ScanJobType, .test_agent_token_is_long_lived(), .test_creates_when_none_exists(), .test_reuses_existing_probe_by_name()]
- "tests_test_ai_engine_resp": "_resp()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L165 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard()]
- "tests_test_ai_engine_testllmreportgenerator_test_technical_finding_runs_guard": ".test_technical_finding_runs_guard()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L205 | neighbors=[TestLLMReportGenerator, _asset(), _finding(), _mock_db(), _resp()]
- "tests_test_detection_core_testenrichfinding_test_enriches_cvss_from_vuln_db": ".test_enriches_cvss_from_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L787 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_epss": ".test_enriches_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L809 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_kev": ".test_enriches_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L801 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_idempotent": ".test_idempotent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L825 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_no_data_still_sets_priority": ".test_no_data_still_sets_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L817 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_passive_collector_socket": "_Socket" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L23 | neighbors=[test_passive_collector.py, .close(), .fileno(), .__init__(), test_subset_listener_failure_reports_de…]
- "tests_test_probe_core_testenginesummary": "TestEngineSummary" | kind=code-symbol | source=probe/tests/test_probe_core.py:L582 | neighbors=[test_probe_core.py, .test_affirmative_fact_creates_one_dedu…, .test_negative_or_ambiguous_facts_do_no…, .test_open_port_count_deduplicates_conf…, .test_open_port_count_excludes_host_liv…]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=probe/tests/test_probe_core.py:L254 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=probe/tests/test_probe_core.py:L346 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L368 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=probe/tests/test_probe_core.py:L383 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=probe/tests/test_probe_core.py:L794 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L825 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_router_db": "test_router_db.py" | kind=code-symbol | source=probe/tests/test_router_db.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, test_mysql_greeting_on_odd_port(), test_plain_http_is_not_db(), test_redis_noauth_signature(), router.py]
- "tests_test_transport_testwebsocket": "TestWebSocket" | kind=code-symbol | source=probe/tests/test_transport.py:L393 | neighbors=[test_transport.py, .test_is_ws_connected_false_by_default(), .test_ws_requires_token(), .test_ws_url_http(), .test_ws_url_https()]
- "tests_test_web_methods": "test_web_methods.py" | kind=code-symbol | source=probe/tests/test_web_methods.py:L1 | neighbors=[bce780a feat(probe): enumerate HTTP met…, web_scanner.py, test_dangerous_methods_flagged(), test_no_allow_header(), test_safe_methods_only()]
- "tools_installer_getinstalledrecord": "getInstalledRecord()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L63 | neighbors=[installer.ts, readInstalled(), installAll(), installTool(), tools.ts]
- "tools_installer_ismanaged": "isManaged()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L56 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), managedPath()]
- "tools_installer_readinstalled": "readInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L33 | neighbors=[installer.ts, getInstalledRecord(), installTool(), listStatus(), removeTool()]
- "tools_installer_removetool": "removeTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L243 | neighbors=[tools.ts, installer.ts, managedPath(), readInstalled(), writeInstalled()]
- "ui_output_rule": "rule()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L50 | neighbors=[output.ts, findingDetail(), ln(), scanHeader(), summary()]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0002_services_agents": "0002_services_agents.py" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add services and agents tables  Revisio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0003_vuln_scan_fields": "0003_vuln_scan_fields.py" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add enrichment fields index + webhook c…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0004_exploit_tables": "0004_exploit_tables.py" | kind=code-symbol | source=manager/backend/alembic/versions/0004_exploit_tables.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Exploit results, approvals, and audit l…, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-025.json

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
