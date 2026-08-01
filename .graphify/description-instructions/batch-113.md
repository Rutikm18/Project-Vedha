# Node Description Batch 114 of 119

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
- "tools_installer_toolstatus": "ToolStatus" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L254 | neighbors=[installer.ts]
- "tools_manifest_platform": "Platform" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L24 | neighbors=[manifest.ts]
- "ui_output_a": "A" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L5 | neighbors=[output.ts]
- "ui_output_error": "error()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L269 | neighbors=[output.ts]
- "ui_output_line": "LINE" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L49 | neighbors=[output.ts]
- "ui_output_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L33 | neighbors=[output.ts]
- "ui_output_stage_col": "STAGE_COL" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L103 | neighbors=[output.ts]
- "ui_output_stage_label": "STAGE_LABEL" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L78 | neighbors=[output.ts]
- "use_cases_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L6 | neighbors=[route.ts]
- "utils_db_rationale_1": "Shared database helpers — single source of truth for patterns duplicated across" | kind=entity | source=manager/backend/app/utils/db.py:L1 | neighbors=[db.py]
- "utils_db_rationale_24": "Fetch a row by primary key, optionally scoped to a tenant.     Raises 404 if mis" | kind=entity | source=manager/backend/app/utils/db.py:L24 | neighbors=[get_or_404()]
- "utils_hash_rationale_1": "Shared hashing utilities — deduplication keys, fingerprinting." | kind=entity | source=manager/backend/app/utils/hash.py:L1 | neighbors=[hash.py]
- "utils_hash_rationale_11": "SHA-256 of (asset_id, cve_id, plugin_id) for finding deduplication.      Used by" | kind=entity | source=manager/backend/app/utils/hash.py:L11 | neighbors=[dedup_hash()]
- "utils_pagination_rationale_12": "Returns (items, total). Applies OFFSET/LIMIT to `query`." | kind=entity | source=manager/backend/app/utils/pagination.py:L12 | neighbors=[paginate_query()]
- "verify_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L6 | neighbors=[route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-113.json

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
