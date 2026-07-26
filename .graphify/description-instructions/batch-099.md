# Node Description Batch 100 of 104

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

- "tests_test_transport_testsubmitresult_test_network_error_returns_false": ".test_network_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L201 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_server_error_returns_false": ".test_server_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L192 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_small_payload_not_gzipped": ".test_small_payload_not_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L237 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_successful_submit": ".test_successful_submit()" | kind=code-symbol | source=probe/tests/test_transport.py:L183 | neighbors=[TestSubmitResult]
- "tests_test_transport_testwebsocket_test_is_ws_connected_false_by_default": ".test_is_ws_connected_false_by_default()" | kind=code-symbol | source=probe/tests/test_transport.py:L276 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_requires_token": ".test_ws_requires_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L294 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_url_http": ".test_ws_url_http()" | kind=code-symbol | source=probe/tests/test_transport.py:L280 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_url_https": ".test_ws_url_https()" | kind=code-symbol | source=probe/tests/test_transport.py:L287 | neighbors=[TestWebSocket]
- "tests_test_version_compare_rationale_1": "Cross-validates the pure-Python Debian version comparator against the real `dpkg" | kind=entity | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[test_version_compare.py]
- "tests_test_version_compare_test_dpkg_compare_public_api": "test_dpkg_compare_public_api()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L65 | neighbors=[test_version_compare.py]
- "tests_test_version_compare_test_pure_python_matches_known_pairs": "test_pure_python_matches_known_pairs()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L45 | neighbors=[test_version_compare.py]
- "tests_test_version_compare_test_pure_python_matches_real_dpkg_binary": "test_pure_python_matches_real_dpkg_binary()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L52 | neighbors=[test_version_compare.py]
- "tests_test_vuln_enrichment_test_dedup_hash_case_insensitive_cve": "test_dedup_hash_case_insensitive_cve()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L242 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_dedup_hash_different_inputs": "test_dedup_hash_different_inputs()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L248 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_dedup_hash_stable": "test_dedup_hash_stable()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L236 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_fetch_epss_empty": "test_fetch_epss_empty()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L114 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_fetch_mitre_known_cve": "test_fetch_mitre_known_cve()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L148 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_fetch_nvd_not_found": "test_fetch_nvd_not_found()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L82 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_kev_bonus_increases_score": "test_kev_bonus_increases_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L186 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_max_risk_score": "test_max_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L164 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_risk_score_bounds": "test_risk_score_bounds()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L193 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_zero_risk_score": "test_zero_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L175 | neighbors=[test_vuln_enrichment.py]
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
- "testssl_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/testssl/route.ts:L11 | neighbors=[route.ts]
- "threadinghttpserver": "ThreadingHTTPServer" | kind=code-symbol | neighbors=[_QuietServer]
- "tools_installer_installedmanifest": "InstalledManifest" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L29 | neighbors=[installer.ts]
- "tools_installer_installedrecord": "InstalledRecord" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L20 | neighbors=[installer.ts]
- "tools_installer_installprogress": "InstallProgress" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L149 | neighbors=[installer.ts]
- "tools_installer_toolstatus": "ToolStatus" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L254 | neighbors=[installer.ts]
- "tools_manifest_platform": "Platform" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L24 | neighbors=[manifest.ts]
- "ui_output_a": "A" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L5 | neighbors=[output.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-099.json

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
