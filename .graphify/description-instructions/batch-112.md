# Node Description Batch 113 of 119

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

- "tests_test_workflow_execution_test_database_gate_uses_scanner_port_catalog": "test_database_gate_uses_scanner_port_catalog()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L132 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_empty_authoritative_scope_never_falls_back_to_job_targets": "test_empty_authoritative_scope_never_falls_back_to_job_targets()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L519 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_applies_configured_target_ceiling": "test_engine_applies_configured_target_ceiling()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L446 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_deadline_fails_when_no_evidence_exists": "test_engine_deadline_fails_when_no_evidence_exists()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L467 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_deadline_preserves_verified_partial_evidence": "test_engine_deadline_preserves_verified_partial_evidence()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L486 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_enforces_local_scope_after_engagement_scope": "test_engine_enforces_local_scope_after_engagement_scope()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L455 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_exposes_component_manifest_and_run_states": "test_engine_exposes_component_manifest_and_run_states()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L530 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_fails_when_every_observation_is_an_error": "test_engine_fails_when_every_observation_is_an_error()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L566 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_rejects_non_string_targets": "test_engine_rejects_non_string_targets()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L431 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_rejects_oversized_cidr_instead_of_false_success": "test_engine_rejects_oversized_cidr_instead_of_false_success()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L438 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_error_result_does_not_mutate_asset_state": "test_error_result_does_not_mutate_asset_state()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L87 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_execution_trace_reports_partial_component": "test_execution_trace_reports_partial_component()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L99 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_explicit_empty_port_catalog_never_falls_back_to_top_ports": "test_explicit_empty_port_catalog_never_falls_back_to_top_ports()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L143 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_filtered_jobs_use_only_requested_tcp_catalogs": "test_filtered_jobs_use_only_requested_tcp_catalogs()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L136 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_manifest_does_not_claim_external_engine_executed": "test_manifest_does_not_claim_external_engine_executed()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L119 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_planned_components_respect_stage_ceiling_and_udp_only_branches": "test_planned_components_respect_stage_ceiling_and_udp_only_branches()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L148 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_snmp_only_workflow_never_falls_back_to_tcp": "test_snmp_only_workflow_never_falls_back_to_tcp()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L341 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_udp_only_workflow_never_falls_back_to_tcp_or_banner": "test_udp_only_workflow_never_falls_back_to_tcp_or_banner()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L309 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_web_job_constrains_discovery_and_port_scan_to_web_catalog": "test_web_job_constrains_discovery_and_port_scan_to_web_catalog()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L373 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_workflow_advances_only_live_host_and_routes_observed_http": "test_workflow_advances_only_live_host_and_routes_observed_http()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L238 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_workflow_stops_at_port_stage_before_banner": "test_workflow_stops_at_port_stage_before_banner()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L177 | neighbors=[test_workflow_execution.py]
- "tests_test_ws_claim_protocol_test_busy_probe_declines_additional_offer": "test_busy_probe_declines_additional_offer()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L62 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_http_spool_flush_removes_only_manager_acknowledged_result": "test_http_spool_flush_removes_only_manager_acknowledged_result()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L106 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_offer_is_staged_and_only_sends_ack": "test_offer_is_staged_and_only_sends_ack()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L17 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_positive_confirmation_releases_exactly_the_staged_job": "test_positive_confirmation_releases_exactly_the_staged_job()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L45 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_staged_job_is_not_released_without_positive_confirmation": "test_staged_job_is_not_released_without_positive_confirmation()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L34 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_ws_job_does_not_duplicate_task_runner_result_submission": "test_ws_job_does_not_duplicate_task_runner_result_submission()" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L82 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_xml_parser_testnmapxmlparser_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L43 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_cpe_extraction": ".test_cpe_extraction()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L71 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_empty_scan": ".test_empty_scan()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L76 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_empty_string": ".test_empty_string()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L84 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_malformed_xml_returns_empty": ".test_malformed_xml_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L80 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_multiple_hosts": ".test_multiple_hosts()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L90 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_none_safe": ".test_none_safe()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L87 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_open_ports_only": ".test_open_ports_only()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L59 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_parse_full_host": ".test_parse_full_host()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L46 | neighbors=[TestNmapXMLParser]
- "tests_test_xml_parser_testnmapxmlparser_test_port_details": ".test_port_details()" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L65 | neighbors=[TestNmapXMLParser]
- "tools_installer_installedmanifest": "InstalledManifest" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L29 | neighbors=[installer.ts]
- "tools_installer_installedrecord": "InstalledRecord" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L20 | neighbors=[installer.ts]
- "tools_installer_installprogress": "InstallProgress" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L149 | neighbors=[installer.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-112.json

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
