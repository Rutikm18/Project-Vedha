# Node Description Batch 285 of 336

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

- "tests_test_exposed_services_testobservedservicesignals_test_telnet_label_off_port_23_is_cleartext": ".test_telnet_label_off_port_23_is_cleartext()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L140 | neighbors=[TestObservedServiceSignals]
- "tests_test_exposed_services_testporthypothesiscontradiction_test_airplay_suppresses_the_cassandra_guess": ".test_airplay_suppresses_the_cassandra_guess()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L202 | neighbors=[TestPortHypothesisContradiction]
- "tests_test_exposed_services_testporthypothesiscontradiction_test_airplay_suppresses_the_docker_registry_guess": ".test_airplay_suppresses_the_docker_registry_guess()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L198 | neighbors=[TestPortHypothesisContradiction]
- "tests_test_exposed_services_testporthypothesiscontradiction_test_an_unrelated_product_does_not_suppress": ".test_an_unrelated_product_does_not_suppress()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L206 | neighbors=[TestPortHypothesisContradiction]
- "tests_test_exposed_services_testporthypothesiscontradiction_test_contradiction_helper_is_case_and_format_insensitive": ".test_contradiction_helper_is_case_and_format_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L217 | neighbors=[TestPortHypothesisContradiction]
- "tests_test_exposure_rationale_1": "test_exposure.py — the probe exposure_matrix → Service verdict + severity bump." | kind=entity | source=manager/backend/tests/test_exposure.py:L1 | neighbors=[test_exposure.py]
- "tests_test_exposure_test_critical_stays_critical": "test_critical_stays_critical()" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L43 | neighbors=[test_exposure.py]
- "tests_test_exposure_test_external_escalates_one_rung": "test_external_escalates_one_rung()" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L37 | neighbors=[test_exposure.py]
- "tests_test_exposure_test_non_external_never_escalates": "test_non_external_never_escalates()" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L47 | neighbors=[test_exposure.py]
- "tests_test_exposure_test_service_exposure_flattens_per_port_verdicts": "test_service_exposure_flattens_per_port_verdicts()" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L13 | neighbors=[test_exposure.py]
- "tests_test_exposure_test_service_exposure_ignores_malformed_and_non_exposure": "test_service_exposure_ignores_malformed_and_non_exposure()" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L30 | neighbors=[test_exposure.py]
- "tests_test_external_engine_wrappers_test_masscan_nonzero_with_valid_output_is_degraded": "test_masscan_nonzero_with_valid_output_is_degraded()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L103 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_range_must_be_fully_in_scope": "test_masscan_range_must_be_fully_in_scope()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L123 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_timeout_is_not_zero_findings": "test_masscan_timeout_is_not_zero_findings()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L91 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_tolerates_partial_json_and_counts_bad_records": "test_masscan_tolerates_partial_json_and_counts_bad_records()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L82 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_empty_failure_is_not_zero_findings": "test_nmap_empty_failure_is_not_zero_findings()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L42 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_extra_args_accept_bounded_tuning": "test_nmap_extra_args_accept_bounded_tuning()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L29 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_extra_args_cannot_replace_validated_targets": "test_nmap_extra_args_cannot_replace_validated_targets()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L21 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_malformed_xml_is_an_explicit_parse_error": "test_nmap_malformed_xml_is_an_explicit_parse_error()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L60 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_xml_error_state_is_preserved_as_result": "test_nmap_xml_error_state_is_preserved_as_result()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L67 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_fact_contract_rationale_1": "test_fact_contract.py — the machine-checkable contract between the probe's emitt" | kind=entity | source=manager/detection_engine/tests/test_fact_contract.py:L1 | neighbors=[test_fact_contract.py]
- "tests_test_fact_contract_rationale_103": "Reverse direction, informational: data the probe collects that NO rule reads." | kind=entity | source=manager/detection_engine/tests/test_fact_contract.py:L103 | neighbors=[test_report_unconsumed_evidence()]
- "tests_test_fact_contract_rationale_35": "Map scanner -> set of top-level data keys it has been observed to emit." | kind=entity | source=manager/detection_engine/tests/test_fact_contract.py:L35 | neighbors=[_emitted_paths_by_scanner()]
- "tests_test_fact_contract_rationale_47": "Run the corpus through the REAL ingester, exactly as engine_bridge does:     one" | kind=entity | source=manager/detection_engine/tests/test_fact_contract.py:L47 | neighbors=[_ingest_corpus()]
- "tests_test_fact_contract_rationale_66": "The gate the name-level check above cannot provide: a corpus whose field NAMES" | kind=entity | source=manager/detection_engine/tests/test_fact_contract.py:L66 | neighbors=[test_corpus_survives_ingestion()]
- "tests_test_fact_contract_rationale_83": "The gate: for every rule, every declared `requires` path must be emitted by at" | kind=entity | source=manager/detection_engine/tests/test_fact_contract.py:L83 | neighbors=[test_every_rule_input_is_emitted_by_its…]
- "tests_test_fd_limit_rationale_1": "test_fd_limit.py — FIX 1: ulimit-aware concurrency for full-range scans.  A full" | kind=entity | source=probe/tests/test_fd_limit.py:L1 | neighbors=[test_fd_limit.py]
- "tests_test_fd_limit_test_caps_below_soft_limit": "test_caps_below_soft_limit()" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L14 | neighbors=[test_fd_limit.py]
- "tests_test_fd_limit_test_floor_when_limit_tiny": "test_floor_when_limit_tiny()" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L27 | neighbors=[test_fd_limit.py]
- "tests_test_fd_limit_test_full_profile_covers_the_whole_tcp_space": "test_full_profile_covers_the_whole_tcp_space()" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L37 | neighbors=[test_fd_limit.py]
- "tests_test_fd_limit_test_get_fd_limit_returns_pair": "test_get_fd_limit_returns_pair()" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L32 | neighbors=[test_fd_limit.py]
- "tests_test_fd_limit_test_no_rlimit_caps_modestly": "test_no_rlimit_caps_modestly()" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L20 | neighbors=[test_fd_limit.py]
- "tests_test_fd_limit_test_top1000_misses_arbitrary_high_ports_full_does_not": "test_top1000_misses_arbitrary_high_ports_full_does_not()" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L45 | neighbors=[test_fd_limit.py]
- "tests_test_finding_events_rationale_1": "test_finding_events.py — the finding lifecycle audit trail.  The synthesis half" | kind=entity | source=manager/backend/tests/test_finding_events.py:L1 | neighbors=[test_finding_events.py]
- "tests_test_finding_events_testeventtypeforstatus_test_maps_status_to_specific_event": ".test_maps_status_to_specific_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L132 | neighbors=[TestEventTypeForStatus]
- "tests_test_finding_out_computed_rationale_1": "FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring" | kind=entity | source=manager/backend/tests/test_finding_out_computed.py:L1 | neighbors=[test_finding_out_computed.py]
- "tests_test_finding_resolution_schema_test_finding_has_resolution_lifecycle_columns": "test_finding_has_resolution_lifecycle_columns()" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L6 | neighbors=[test_finding_resolution_schema.py]
- "tests_test_finding_risk_rank_api_test_finding_schema_exposes_risk_rank": "test_finding_schema_exposes_risk_rank()" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L6 | neighbors=[test_finding_risk_rank_api.py]
- "tests_test_finding_schema_test_finding_patch_accepts_documented_maximum_risk_score": "test_finding_patch_accepts_documented_maximum_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L9 | neighbors=[test_finding_schema.py]
- "tests_test_finding_schema_test_finding_patch_rejects_risk_score_above_scale": "test_finding_patch_rejects_risk_score_above_scale()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L15 | neighbors=[test_finding_schema.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-284.json

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
