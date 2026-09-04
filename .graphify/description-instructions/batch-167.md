# Node Description Batch 168 of 332

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

- "tests_test_vuln_enrichment_rationale_53": "Create a mock httpx.AsyncClient that returns different responses per URL." | kind=entity | source=manager/backend/tests/test_vuln_enrichment.py:L53 | neighbors=[_make_http_mock(), VulnEnrichmentService]
- "tests_test_vuln_enrichment_test_check_cisa_kev_absent": "test_check_cisa_kev_absent()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L134 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_check_cisa_kev_case_insensitive": "test_check_cisa_kev_case_insensitive()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L140 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_check_cisa_kev_present": "test_check_cisa_kev_present()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L128 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_enrich_full": "test_enrich_full()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L205 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_epss_success": "test_fetch_epss_success()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L106 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_mitre_from_nvd_references": "test_fetch_mitre_from_nvd_references()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L155 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_nvd_caches_result": "test_fetch_nvd_caches_result()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L94 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_vuln_enrichment_test_fetch_nvd_success": "test_fetch_nvd_success()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L72 | neighbors=[test_vuln_enrichment.py, _make_http_mock()]
- "tests_test_weakness_map_testclicorrelatemerges_test_correlate_includes_weakness_findings": ".test_correlate_includes_weakness_findings()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L189 | neighbors=[TestCliCorrelateMerges, _wrapped()]
- "tests_test_weakness_map_testclicorrelatemerges_test_no_weakness_map_flag_disables_it": ".test_no_weakness_map_flag_disables_it()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L200 | neighbors=[TestCliCorrelateMerges, _wrapped()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_cve_absent_from_mirror_still_emitted_with_note": ".test_cve_absent_from_mirror_still_emitted_with_note()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L113 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_exposure_boosts_risk": ".test_exposure_boosts_risk()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L82 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_no_db_degrades_gracefully": ".test_no_db_degrades_gracefully()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L120 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_obsolete_tls_both_when_both_offered": ".test_obsolete_tls_both_when_both_offered()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L104 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_obsolete_tls_sslv2_only_drown": ".test_obsolete_tls_sslv2_only_drown()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L98 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_obsolete_tls_sslv3_only_poodle": ".test_obsolete_tls_sslv3_only_poodle()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L92 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_smbv1_maps_to_eternalblue_with_live_enrichment": ".test_smbv1_maps_to_eternalblue_with_live_enrichment()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L70 | neighbors=[TestCorrelateWeaknesses, _wrapped()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_sorted_by_risk_desc": ".test_sorted_by_risk_desc()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L130 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_terrapin_high_confidence": ".test_terrapin_high_confidence()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L88 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_to_dict_shape_matches_cve_finding": ".test_to_dict_shape_matches_cve_finding()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L137 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testcorrelateweaknesses_test_unmapped_rule_yields_nothing": ".test_unmapped_rule_yields_nothing()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L110 | neighbors=[TestCorrelateWeaknesses, _raw()]
- "tests_test_weakness_map_testfindingview_test_raw_shape": ".test_raw_shape()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L61 | neighbors=[TestFindingView, _raw()]
- "tests_test_weakness_map_testfindingview_test_wrapped_shape": ".test_wrapped_shape()" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L57 | neighbors=[TestFindingView, _wrapped()]
- "tests_test_wire_identity_testevasionflags": "TestEvasionFlags" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L73 | neighbors=[test_wire_identity.py, .test_randomize_and_scan_delay_flags_pr…]
- "tests_test_workflow_execution_test_host_fanout_is_bounded": "test_host_fanout_is_bounded()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L76 | neighbors=[test_workflow_execution.py, _ConcurrencyScanner]
- "tests_test_workflow_execution_test_per_target_exception_preserves_other_results": "test_per_target_exception_preserves_other_results()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L61 | neighbors=[test_workflow_execution.py, _ExplodingScanner]
- "tests_test_xml_parser_rationale_1": "Unit tests for NmapXMLParser." | kind=entity | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[test_xml_parser.py, NmapXMLParser]
- "tools_gen_ssh_kexdb_build": "build()" | kind=code-symbol | source=probe/tools/gen_ssh_kexdb.py:L83 | neighbors=[gen_ssh_kexdb.py, main()]
- "tools_gen_ssh_kexdb_main": "main()" | kind=code-symbol | source=probe/tools/gen_ssh_kexdb.py:L102 | neighbors=[gen_ssh_kexdb.py, build()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-167.json

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
