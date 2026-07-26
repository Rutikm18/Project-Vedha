# Node Description Batch 22 of 104

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

- "scanner_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L75 | neighbors=[snmp_scanner.py, BaseScanner, .__init__(), ._query(), .scan_target()]
- "scanner_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L155 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/scanner/web_scanner.py:L112 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "schemas_asset_assetin": "AssetIn" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L9 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType, .validate_ip()]
- "schemas_engagement_engagementout": "EngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L42 | neighbors=[engagement.py, EngagementDetail, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_findingfilter": "FindingFilter" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L10 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_findingout": "FindingOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L54 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slaitem": "SlaItem" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L34 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slasummary": "SlaSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L44 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "services_scope_crypto": "scope_crypto.py" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt…]
- "services_sla_compute": "compute()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L60 | neighbors=[sla.py, SlaResult, _windows(), Compute the SLA state for one finding. …, summarize()]
- "services_sla_slaresult": "SlaResult" | kind=code-symbol | source=manager/backend/app/services/sla.py:L46 | neighbors=[sla.py, compute(), FindingStatus, Finding, .is_tracked()]
- "tests_test_ad_assessment_enum_with_entries": "_enum_with_entries()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L45 | neighbors=[test_ad_assessment.py, .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_agents_testenqueueagentjob": "TestEnqueueAgentJob" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L43 | neighbors=[test_agents.py, ScanJobType, .test_404_when_engagement_missing(), .test_rejects_server_side_type(), .test_success_creates_pending_job()]
- "tests_test_agents_testregisteragent": "TestRegisterAgent" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L203 | neighbors=[test_agents.py, ScanJobType, .test_agent_token_is_long_lived(), .test_creates_when_none_exists(), .test_reuses_existing_probe_by_name()]
- "tests_test_ai_engine_resp": "_resp()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L165 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard()]
- "tests_test_ai_engine_testllmreportgenerator_test_technical_finding_runs_guard": ".test_technical_finding_runs_guard()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L205 | neighbors=[TestLLMReportGenerator, _asset(), _finding(), _mock_db(), _resp()]
- "tests_test_detection_core_testenrichfinding_test_enriches_cvss_from_vuln_db": ".test_enriches_cvss_from_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L787 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_epss": ".test_enriches_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L809 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_kev": ".test_enriches_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L801 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_idempotent": ".test_idempotent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L825 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_no_data_still_sets_priority": ".test_no_data_still_sets_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L817 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_hw_bind": "test_hw_bind.py" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, hw_bind.py, TestCheckHwBind, TestGetHwId, Tests for agent/hw_bind.py]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=probe/tests/test_probe_core.py:L254 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=probe/tests/test_probe_core.py:L342 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L364 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=probe/tests/test_probe_core.py:L379 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=probe/tests/test_probe_core.py:L702 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L733 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=probe/tests/test_result_spool.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, result_spool.py, spool(), TestResultSpool, Tests for agent/result_spool.py]
- "tests_test_scope_crypt": "test_scope_crypt.py" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, scope_crypt.py, TestEncryptDecryptRoundtrip, TestKeyGeneration, Tests for agent/scope_crypt.py]
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L27 | neighbors=[test_transport.py, .test_auth_header(), .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds(), .test_save_and_clear_state()]
- "tests_test_transport_testwebsocket": "TestWebSocket" | kind=code-symbol | source=probe/tests/test_transport.py:L275 | neighbors=[test_transport.py, .test_is_ws_connected_false_by_default(), .test_ws_requires_token(), .test_ws_url_http(), .test_ws_url_https()]
- "tests_test_version_compare": "test_version_compare.py" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, test_dpkg_compare_public_api(), test_pure_python_matches_known_pairs(), test_pure_python_matches_real_dpkg_bina…, Cross-validates the pure-Python Debian …]
- "tools_installer_getinstalledrecord": "getInstalledRecord()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L63 | neighbors=[tools.ts, installer.ts, readInstalled(), installAll(), installTool()]
- "tools_installer_ismanaged": "isManaged()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L56 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), managedPath()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-021.json

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
