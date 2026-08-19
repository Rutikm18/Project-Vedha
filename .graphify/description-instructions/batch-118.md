# Node Description Batch 119 of 227

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
- "tests_test_wire_identity_testevasionflags": "TestEvasionFlags" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L73 | neighbors=[test_wire_identity.py, .test_randomize_and_scan_delay_flags_pr…]
- "tests_test_workflow_execution_test_host_fanout_is_bounded": "test_host_fanout_is_bounded()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L76 | neighbors=[test_workflow_execution.py, _ConcurrencyScanner]
- "tests_test_workflow_execution_test_per_target_exception_preserves_other_results": "test_per_target_exception_preserves_other_results()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L61 | neighbors=[test_workflow_execution.py, _ExplodingScanner]
- "tests_test_xml_parser_rationale_1": "Unit tests for NmapXMLParser." | kind=entity | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[test_xml_parser.py, NmapXMLParser]
- "tools_installer_downloadfile": "downloadFile()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L68 | neighbors=[installer.ts, installTool()]
- "tools_installer_extract": "extract()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L104 | neighbors=[installer.ts, installTool()]
- "tools_installer_picksource": "pickSource()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L141 | neighbors=[installer.ts, installTool()]
- "tools_installer_sha256file": "sha256File()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L97 | neighbors=[installer.ts, installTool()]
- "tools_issue_license_b64": "_b64()" | kind=code-symbol | source=probe/tools/issue_license.py:L31 | neighbors=[issue_license.py, issue()]
- "tools_issue_license_keygen": "keygen()" | kind=code-symbol | source=probe/tools/issue_license.py:L35 | neighbors=[issue_license.py, main()]
- "tools_manifest_adversa_manifest_file": "ADVERSA_MANIFEST_FILE" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L22 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_adversa_tools_dir": "ADVERSA_TOOLS_DIR" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L21 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_currentplatform": "currentPlatform()" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L54 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_toolsource": "ToolSource" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L29 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_toolspec": "ToolSpec" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L40 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_vedha_manifest_file": "VEDHA_MANIFEST_FILE" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L22 | neighbors=[installer.ts, manifest.ts]
- "tools_manifest_vedha_tools_dir": "VEDHA_TOOLS_DIR" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L21 | neighbors=[installer.ts, manifest.ts]
- "tools_probe_local_run_main": "main()" | kind=code-symbol | source=probe/tools/probe_local_run.py:L57 | neighbors=[probe_local_run.py, summarize()]
- "tools_probe_local_run_summarize": "summarize()" | kind=code-symbol | source=probe/tools/probe_local_run.py:L40 | neighbors=[probe_local_run.py, main()]
- "ui_output_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L53 | neighbors=[output.ts, ln()]
- "ui_output_findingstable": "findingsTable()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L210 | neighbors=[output.ts, ln()]
- "ui_output_hostline": "hostLine()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L149 | neighbors=[output.ts, ln()]
- "ui_output_info": "info()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L273 | neighbors=[output.ts, ln()]
- "ui_output_sevbadge": "sevBadge()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L43 | neighbors=[output.ts, findingLine()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-118.json

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
