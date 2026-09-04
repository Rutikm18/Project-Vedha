# Node Description Batch 167 of 330

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
- "tests_test_vnc_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L76 | neighbors=[test_vnc_scanner.py, .test_main_scripts()]
- "tests_test_vnc_scanner_testvncfindings_test_no_auth_is_critical": ".test_no_auth_is_critical()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L57 | neighbors=[TestVNCFindings, ._fact()]
- "tests_test_vnc_scanner_testvncfindings_test_strong_auth_silent": ".test_strong_auth_silent()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L69 | neighbors=[TestVNCFindings, ._fact()]
- "tests_test_vnc_scanner_testvncfindings_test_weak_only_is_medium": ".test_weak_only_is_medium()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L63 | neighbors=[TestVNCFindings, ._fact()]
- "tests_test_vnc_scanner_testvncscanner_test_no_auth_open": ".test_no_auth_open()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L38 | neighbors=[TestVNCScanner, ._sc()]
- "tests_test_vnc_scanner_testvncscanner_test_no_vnc_filtered": ".test_no_vnc_filtered()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L46 | neighbors=[TestVNCScanner, ._sc()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-166.json

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
