# Node Description Batch 78 of 209

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

- "tests_test_smb_scanner_test_signing_supported_field_present": "test_signing_supported_field_present()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L71 | neighbors=[test_smb_scanner.py, Step 13: expose signing_supported (prot…, _smb2_negotiate_response()]
- "tests_test_syn_scanner_synack_with_options": "_synack_with_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L325 | neighbors=[test_syn_scanner.py, A SYN/ACK carrying an MSS option (data …, .test_window_ttl_mss_surfaced()]
- "tests_test_syn_scanner_testadaptivetimeouttoggle": "TestAdaptiveTimeoutToggle" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L381 | neighbors=[test_syn_scanner.py, .test_adaptive_on_by_default(), .test_can_disable()]
- "tests_test_syn_scanner_testparsepacketsignals": "TestParsePacketSignals" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L335 | neighbors=[test_syn_scanner.py, .test_no_options_gives_none_mss(), .test_window_ttl_mss_surfaced()]
- "tests_test_syn_scanner_testsyndefaults": "TestSynDefaults" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L287 | neighbors=[test_syn_scanner.py, .test_default_ports_are_nmap_top100(), .test_default_retries_is_two()]
- "tests_test_task_runner_testrunnerscantypes": "TestRunnerScanTypes" | kind=code-symbol | source=probe/tests/test_task_runner.py:L447 | neighbors=[test_task_runner.py, .test_ot_passive_profile(), .test_web_triage_scan_type()]
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_out_of_scope_target": ".test_rejects_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L205 | neighbors=[When scope is fetched and targets are o…, TestRunnerScopeValidation, When scope is fetched and targets are o…]
- "tests_test_task_runner_testrunnerscopevalidation_test_scope_fallback_when_fetch_fails": ".test_scope_fallback_when_fetch_fails()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L318 | neighbors=[When scope fetch fails, manager-embedde…, TestRunnerScopeValidation, When scope fetch fails, manager-embedde…]
- "tests_test_task_runner_testrunnersubmission": "TestRunnerSubmission" | kind=code-symbol | source=probe/tests/test_task_runner.py:L389 | neighbors=[test_task_runner.py, .test_calls_submit_with_result(), .test_uses_spool_when_available()]
- "tests_test_task_runner_testrunnersubmission_test_calls_submit_with_result": ".test_calls_submit_with_result()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L390 | neighbors=[Verify the submit callback is called wi…, TestRunnerSubmission, Verify the submit callback is called wi…]
- "tests_test_task_runner_testrunnersubmission_test_uses_spool_when_available": ".test_uses_spool_when_available()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L415 | neighbors=[When spool_submit is provided, it's use…, TestRunnerSubmission, When spool_submit is provided, it's use…]
- "tests_test_tls_fingerprint_synthetic_server_hello": "_synthetic_server_hello()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L45 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_integration_self_signed": "_self_signed()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L29 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_integration_test_tls_fingerprint_is_nonzero_and_stable": "test_tls_fingerprint_is_nonzero_and_stable()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L111 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_tls_integration_test_tls_scanner_reports_posture_grade": "test_tls_scanner_reports_posture_grade()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L87 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=probe/tests/test_transport.py:L382 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()]
- "tests_test_transport_transport": "transport()" | kind=code-symbol | source=probe/tests/test_transport.py:L17 | neighbors=[test_transport.py, Create a Transport with a real state fi…, Create a Transport with a real state fi…]
- "tests_test_validation_endpoints_test_approve_conflict_when_not_pending": "test_approve_conflict_when_not_pending()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L116 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_approve_enqueues_safe_validate_job": "test_approve_enqueues_safe_validate_job()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L89 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_create_rejected_when_roe_forbids": "test_create_rejected_when_roe_forbids()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L74 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_create_request_is_pending_and_derives_tls_check": "test_create_request_is_pending_and_derives_tls_check()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L55 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_endpoints_test_reject_marks_rejected": "test_reject_marks_rejected()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L126 | neighbors=[test_validation_endpoints.py, _mock_db(), _user()]
- "tests_test_validation_ingest_exec": "_exec()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L72 | neighbors=[test_validation_ingest.py, test_ingest_confirmed_updates_request_a…, test_ingest_unknown_job_is_noop()]
- "tests_test_validation_ingest_test_ingest_confirmed_updates_request_and_finding": "test_ingest_confirmed_updates_request_and_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L88 | neighbors=[test_validation_ingest.py, _exec(), _finding()]
- "tests_test_verification_graph": "test_verification_graph.py" | kind=code-symbol | source=manager/backend/tests/test_verification_graph.py:L1 | neighbors=[c02c465 feat(verification): optional La…, test_graph_available_is_boolean(), test_run_verification_matches_core_with…]
- "tests_test_workflow_execution_explodingscanner": "_ExplodingScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L29 | neighbors=[test_workflow_execution.py, .scan_target(), test_per_target_exception_preserves_oth…]
- "tools_installer_liststatus": "listStatus()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L264 | neighbors=[tools.ts, installer.ts, readInstalled()]
- "tools_installer_writeinstalled": "writeInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L42 | neighbors=[installer.ts, installTool(), removeTool()]
- "tools_issue_license_issue": "issue()" | kind=code-symbol | source=probe/tools/issue_license.py:L62 | neighbors=[issue_license.py, _b64(), main()]
- "tools_issue_license_pubkey": "pubkey()" | kind=code-symbol | source=probe/tools/issue_license.py:L48 | neighbors=[issue_license.py, main(), Print the vendor PUBLIC key (hex) deriv…]
- "tools_manifest_tool_manifest": "TOOL_MANIFEST" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L74 | neighbors=[tools.ts, installer.ts, manifest.ts]
- "ui_output_findingdetail": "findingDetail()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L238 | neighbors=[output.ts, ln(), rule()]
- "ui_output_findingline": "findingLine()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L184 | neighbors=[output.ts, ln(), sevBadge()]
- "ui_output_scanheader": "scanHeader()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L63 | neighbors=[output.ts, ln(), rule()]
- "ui_output_stageerror": "stageError()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L133 | neighbors=[output.ts, ln(), w()]
- "ui_output_summary": "summary()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L194 | neighbors=[output.ts, ln(), rule()]
- "ui_output_w": "w()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L29 | neighbors=[output.ts, stageError(), stageProgress()]
- "utils_csv_parser": "csv_parser.py" | kind=code-symbol | source=manager/backend/app/utils/csv_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, parse_csv_assets(), 298a9d4 trim frontend to 7 core pages; …]
- "utils_csv_parser_rationale_26": "Parse CSV text into a list of AssetIn models and error strings." | kind=entity | source=manager/backend/app/utils/csv_parser.py:L26 | neighbors=[parse_csv_assets(), AssetCriticality, AssetType]
- "utils_pagination": "pagination.py" | kind=code-symbol | source=manager/backend/app/utils/pagination.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, paginate_query(), 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-077.json

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
