# Node Description Batch 167 of 332

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

- "tests_test_two_tree_parity_test_no_unmirrored_scanner_files": "test_no_unmirrored_scanner_files()" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L56 | neighbors=[test_two_tree_parity.py, A scanner that exists in only one tree …]
- "tests_test_va_campaign_test_catalog_ids_are_unique_and_match_default_stages": "test_catalog_ids_are_unique_and_match_default_stages()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L222 | neighbors=[test_va_campaign.py, _scope()]
- "tests_test_va_campaign_test_cli_view_deduplicates_unchanged_status": "test_cli_view_deduplicates_unchanged_status()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L311 | neighbors=[test_va_campaign.py, _Buf]
- "tests_test_va_campaign_test_cli_view_emits_one_line_per_transition": "test_cli_view_emits_one_line_per_transition()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L298 | neighbors=[test_va_campaign.py, _Buf]
- "tests_test_va_campaign_test_disabled_opt_in_stage_is_skipped_and_excluded_from_percent": "test_disabled_opt_in_stage_is_skipped_and_excluded_from_percent()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L80 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_enabled_opt_in_stage_runs": "test_enabled_opt_in_stage_runs()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L99 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_facts_accumulate_into_totals": "test_facts_accumulate_into_totals()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L137 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_gate_not_met_skips_stage": "test_gate_not_met_skips_stage()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L64 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_percent_and_current_stage_transitions": "test_percent_and_current_stage_transitions()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L175 | neighbors=[test_va_campaign.py, _reporter()]
- "tests_test_va_campaign_test_progress_snapshot_shape": "test_progress_snapshot_shape()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L159 | neighbors=[test_va_campaign.py, _reporter()]
- "tests_test_va_campaign_test_stage_error_is_isolated_not_fatal": "test_stage_error_is_isolated_not_fatal()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L119 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_stages_run_in_order_and_thread_context": "test_stages_run_in_order_and_thread_context()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L40 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_validation_endpoints_exec": "_exec()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L28 | neighbors=[test_validation_endpoints.py, _mock_db()]
- "tests_test_validation_gate_testnofabricatedicmpliveness": "TestNoFabricatedIcmpLiveness" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L71 | neighbors=[test_validation_gate.py, .test_icmp_unavailable_os_observation_r…]
- "tests_test_validation_gate_testnofabricatedicmpliveness_test_icmp_unavailable_os_observation_raises_no_exposure": ".test_icmp_unavailable_os_observation_raises_no_exposure()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L72 | neighbors=[TestNoFabricatedIcmpLiveness, _ids()]
- "tests_test_validation_gate_testrdpnlagate_test_nla_enforced_suppresses_no_nla_finding": ".test_nla_enforced_suppresses_no_nla_finding()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L56 | neighbors=[TestRdpNlaGate, _ids()]
- "tests_test_validation_gate_testrdpnlagate_test_positive_control_nla_off_is_flagged": ".test_positive_control_nla_off_is_flagged()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L62 | neighbors=[TestRdpNlaGate, _ids()]
- "tests_test_validation_gate_testudpnoreplyrejected_test_open_filtered_amplifier_not_flagged": ".test_open_filtered_amplifier_not_flagged()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L36 | neighbors=[TestUdpNoReplyRejected, _ids()]
- "tests_test_validation_gate_testudpnoreplyrejected_test_positive_control_answered_amplifier_is_flagged": ".test_positive_control_answered_amplifier_is_flagged()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L43 | neighbors=[TestUdpNoReplyRejected, _ids()]
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
