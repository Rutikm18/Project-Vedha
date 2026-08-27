# Node Description Batch 89 of 92

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

- "tests_test_workflow_execution_test_execution_trace_reports_partial_component": "test_execution_trace_reports_partial_component()" | kind=code-symbol | source=tests/test_workflow_execution.py:L99 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_explicit_empty_port_catalog_never_falls_back_to_top_ports": "test_explicit_empty_port_catalog_never_falls_back_to_top_ports()" | kind=code-symbol | source=tests/test_workflow_execution.py:L143 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_filtered_jobs_use_only_requested_tcp_catalogs": "test_filtered_jobs_use_only_requested_tcp_catalogs()" | kind=code-symbol | source=tests/test_workflow_execution.py:L136 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_manifest_does_not_claim_external_engine_executed": "test_manifest_does_not_claim_external_engine_executed()" | kind=code-symbol | source=tests/test_workflow_execution.py:L119 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_planned_components_respect_stage_ceiling_and_udp_only_branches": "test_planned_components_respect_stage_ceiling_and_udp_only_branches()" | kind=code-symbol | source=tests/test_workflow_execution.py:L148 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_snmp_only_workflow_never_falls_back_to_tcp": "test_snmp_only_workflow_never_falls_back_to_tcp()" | kind=code-symbol | source=tests/test_workflow_execution.py:L341 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_udp_only_workflow_never_falls_back_to_tcp_or_banner": "test_udp_only_workflow_never_falls_back_to_tcp_or_banner()" | kind=code-symbol | source=tests/test_workflow_execution.py:L309 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_web_job_constrains_discovery_and_port_scan_to_web_catalog": "test_web_job_constrains_discovery_and_port_scan_to_web_catalog()" | kind=code-symbol | source=tests/test_workflow_execution.py:L373 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_workflow_advances_only_live_host_and_routes_observed_http": "test_workflow_advances_only_live_host_and_routes_observed_http()" | kind=code-symbol | source=tests/test_workflow_execution.py:L238 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_workflow_stops_at_port_stage_before_banner": "test_workflow_stops_at_port_stage_before_banner()" | kind=code-symbol | source=tests/test_workflow_execution.py:L177 | neighbors=[test_workflow_execution.py]
- "tests_test_ws_claim_protocol_test_busy_probe_declines_additional_offer": "test_busy_probe_declines_additional_offer()" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L76 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_http_spool_flush_removes_only_manager_acknowledged_result": "test_http_spool_flush_removes_only_manager_acknowledged_result()" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L120 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_offer_is_staged_and_only_sends_ack": "test_offer_is_staged_and_only_sends_ack()" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L17 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_positive_confirmation_releases_exactly_the_staged_job": "test_positive_confirmation_releases_exactly_the_staged_job()" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L45 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_staged_job_is_not_released_without_positive_confirmation": "test_staged_job_is_not_released_without_positive_confirmation()" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L34 | neighbors=[test_ws_claim_protocol.py]
- "tests_test_ws_claim_protocol_test_ws_job_does_not_duplicate_task_runner_result_submission": "test_ws_job_does_not_duplicate_task_runner_result_submission()" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L96 | neighbors=[test_ws_claim_protocol.py]
- "tools_issue_license_rationale_49": "Print the vendor PUBLIC key (hex) derived from the private key.      build/seal-" | kind=entity | source=tools/issue_license.py:L49 | neighbors=[pubkey()]
- "workflow_asset_asset_merge_db_scan": "._merge_db_scan()" | kind=code-symbol | source=workflow/asset.py:L151 | neighbors=[Asset]
- "workflow_asset_asset_merge_dns_scan": "._merge_dns_scan()" | kind=code-symbol | source=workflow/asset.py:L167 | neighbors=[Asset]
- "workflow_asset_asset_merge_ftp_scan": "._merge_ftp_scan()" | kind=code-symbol | source=workflow/asset.py:L179 | neighbors=[Asset]
- "workflow_asset_asset_merge_ipmi_scan": "._merge_ipmi_scan()" | kind=code-symbol | source=workflow/asset.py:L191 | neighbors=[Asset]
- "workflow_asset_asset_merge_ldap_scan": "._merge_ldap_scan()" | kind=code-symbol | source=workflow/asset.py:L163 | neighbors=[Asset]
- "workflow_asset_asset_merge_mcp_ai_scan": "._merge_mcp_ai_scan()" | kind=code-symbol | source=workflow/asset.py:L155 | neighbors=[Asset]
- "workflow_asset_asset_merge_msrpc_scan": "._merge_msrpc_scan()" | kind=code-symbol | source=workflow/asset.py:L199 | neighbors=[Asset]
- "workflow_asset_asset_merge_nfs_scan": "._merge_nfs_scan()" | kind=code-symbol | source=workflow/asset.py:L175 | neighbors=[Asset]
- "workflow_asset_asset_merge_passive_collect": "._merge_passive_collect()" | kind=code-symbol | source=workflow/asset.py:L215 | neighbors=[Asset]
- "workflow_asset_asset_merge_printer_scan": "._merge_printer_scan()" | kind=code-symbol | source=workflow/asset.py:L203 | neighbors=[Asset]
- "workflow_asset_asset_merge_rsync_scan": "._merge_rsync_scan()" | kind=code-symbol | source=workflow/asset.py:L183 | neighbors=[Asset]
- "workflow_asset_asset_merge_service_banner": "._merge_service_banner()" | kind=code-symbol | source=workflow/asset.py:L129 | neighbors=[Asset]
- "workflow_asset_asset_merge_smb_enum_scan": "._merge_smb_enum_scan()" | kind=code-symbol | source=workflow/asset.py:L171 | neighbors=[Asset]
- "workflow_asset_asset_merge_smb_scan": "._merge_smb_scan()" | kind=code-symbol | source=workflow/asset.py:L141 | neighbors=[Asset]
- "workflow_asset_asset_merge_smtp_scan": "._merge_smtp_scan()" | kind=code-symbol | source=workflow/asset.py:L195 | neighbors=[Asset]
- "workflow_asset_asset_merge_snmp_scan": "._merge_snmp_scan()" | kind=code-symbol | source=workflow/asset.py:L147 | neighbors=[Asset]
- "workflow_asset_asset_merge_ssh_inventory": "._merge_ssh_inventory()" | kind=code-symbol | source=workflow/asset.py:L221 | neighbors=[Asset]
- "workflow_asset_asset_merge_ssh_scan": "._merge_ssh_scan()" | kind=code-symbol | source=workflow/asset.py:L159 | neighbors=[Asset]
- "workflow_asset_asset_merge_tls_scan": "._merge_tls_scan()" | kind=code-symbol | source=workflow/asset.py:L133 | neighbors=[Asset]
- "workflow_asset_asset_merge_vnc_scan": "._merge_vnc_scan()" | kind=code-symbol | source=workflow/asset.py:L187 | neighbors=[Asset]
- "workflow_asset_asset_merge_web_scan": "._merge_web_scan()" | kind=code-symbol | source=workflow/asset.py:L137 | neighbors=[Asset]
- "workflow_asset_asset_merge_windows_inventory": "._merge_windows_inventory()" | kind=code-symbol | source=workflow/asset.py:L225 | neighbors=[Asset]
- "workflow_asset_asset_open_ports_for_deep_scan": ".open_ports_for_deep_scan()" | kind=code-symbol | source=workflow/asset.py:L92 | neighbors=[Asset]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-088.json

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
