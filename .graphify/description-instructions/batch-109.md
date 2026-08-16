# Node Description Batch 110 of 209

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

- "tests_test_syn_scanner_testverifyreplycookie_test_valid_cookie_verifies": ".test_valid_cookie_verifies()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L119 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_syn_scanner_testverifyreplycookie_test_wrong_ack_fails": ".test_wrong_ack_fails()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L124 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_task_runner_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L12 | neighbors=[test_task_runner.py, Return a minimal successful result with…]
- "tests_test_task_runner_runner": "runner()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L37 | neighbors=[test_task_runner.py, TaskRunner with no-op dependencies (no …]
- "tests_test_tls_fingerprint_testparseserverhello_test_extracts_version_and_cipher": ".test_extracts_version_and_cipher()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L59 | neighbors=[TestParseServerHello, _synthetic_server_hello()]
- "tests_test_tls_fingerprint_testparseserverhello_test_tls13_version_from_supported_versions_ext": ".test_tls13_version_from_supported_versions_ext()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L65 | neighbors=[TestParseServerHello, _synthetic_server_hello()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_a_modern": ".test_grade_a_modern()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L73 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_b_no_tls13": ".test_grade_b_no_tls13()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L78 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_c_tls11": ".test_grade_c_tls11()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L83 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_f_tls10": ".test_grade_f_tls10()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L94 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_validation_endpoints_exec": "_exec()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L28 | neighbors=[test_validation_endpoints.py, _mock_db()]
- "tests_test_validation_ingest_test_confirmed_never_overrides_human_closed_finding": "test_confirmed_never_overrides_human_closed_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L55 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_confirmed_raises_certainty": "test_confirmed_raises_certainty()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L32 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_contradicted_marks_false_positive_without_touching_status": "test_contradicted_marks_false_positive_without_touching_status()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L40 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_inconclusive_leaves_finding_unchanged": "test_inconclusive_leaves_finding_unchanged()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L48 | neighbors=[test_validation_ingest.py, _finding()]
- "tests_test_validation_ingest_test_ingest_unknown_job_is_noop": "test_ingest_unknown_job_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L107 | neighbors=[test_validation_ingest.py, _exec()]
- "tests_test_validation_request_schema": "test_validation_request_schema.py" | kind=code-symbol | source=manager/backend/tests/test_validation_request_schema.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, test_validation_request_columns_and_def…]
- "tests_test_vantage_fusion_test_ambiguous_when_only_open_filtered": "test_ambiguous_when_only_open_filtered()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L51 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_declared_external_vantage_without_hint_name": "test_declared_external_vantage_without_hint_name()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L64 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_external_vantage_open_makes_port_external": "test_external_vantage_open_makes_port_external()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L24 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_fused_service_exposure_is_keyed_for_service_rows": "test_fused_service_exposure_is_keyed_for_service_rows()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L79 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_internal_only_when_no_external_probe_sees_open": "test_internal_only_when_no_external_probe_sees_open()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L35 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_internal_open_does_not_imply_external": "test_internal_open_does_not_imply_external()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L43 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_not_exposed_when_closed_everywhere": "test_not_exposed_when_closed_everywhere()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L57 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vantage_fusion_test_single_probe_matches_its_own_verdict": "test_single_probe_matches_its_own_verdict()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L72 | neighbors=[test_vantage_fusion.py, _probe()]
- "tests_test_vuln_enrichment_rationale_1": "Unit tests for VulnEnrichmentService — all external HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_vuln_enrichment.py:L1 | neighbors=[test_vuln_enrichment.py, VulnEnrichmentService]
- "tests_test_vuln_enrichment_rationale_53": "Create a mock httpx.AsyncClient that returns different responses per URL." | kind=entity | source=manager/backend/tests/test_vuln_enrichment.py:L53 | neighbors=[_make_http_mock(), VulnEnrichmentService]
- "tests_test_vuln_enrichment_test_check_cisa_kev_absent": "test_check_cisa_kev_absent()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L134 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_check_cisa_kev_case_insensitive": "test_check_cisa_kev_case_insensitive()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L140 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_check_cisa_kev_present": "test_check_cisa_kev_present()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L128 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_enrich_full": "test_enrich_full()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L205 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_epss_success": "test_fetch_epss_success()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L106 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_mitre_from_nvd_references": "test_fetch_mitre_from_nvd_references()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L155 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_nvd_caches_result": "test_fetch_nvd_caches_result()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L94 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_nvd_success": "test_fetch_nvd_success()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L72 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_workflow_execution_test_host_fanout_is_bounded": "test_host_fanout_is_bounded()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L76 | neighbors=[test_workflow_execution.py, _ConcurrencyScanner]
- "tests_test_workflow_execution_test_per_target_exception_preserves_other_results": "test_per_target_exception_preserves_other_results()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L61 | neighbors=[test_workflow_execution.py, _ExplodingScanner]
- "tests_test_xml_parser_rationale_1": "Unit tests for NmapXMLParser." | kind=entity | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[test_xml_parser.py, NmapXMLParser]
- "tools_installer_downloadfile": "downloadFile()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L68 | neighbors=[installer.ts, installTool()]
- "tools_installer_extract": "extract()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L104 | neighbors=[installer.ts, installTool()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-109.json

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
