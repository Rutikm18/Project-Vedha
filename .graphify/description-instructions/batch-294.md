# Node Description Batch 295 of 330

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

- "tests_test_posture_confidence_testassessor_test_deception_penalty": ".test_deception_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L60 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_final_is_clamped_and_recorded": ".test_final_is_clamped_and_recorded()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L66 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_lone_chain_member_gets_no_floor": ".test_lone_chain_member_gets_no_floor()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L52 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_unreachable_downgrades_and_is_recorded": ".test_unreachable_downgrades_and_is_recorded()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L46 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testassessor_test_validated_base_higher_than_unvalidated": ".test_validated_base_higher_than_unvalidated()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L39 | neighbors=[TestAssessor]
- "tests_test_posture_confidence_testchains_test_chain_floor_never_lowers_confidence": ".test_chain_floor_never_lowers_confidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L82 | neighbors=[TestChains]
- "tests_test_posture_confidence_testchains_test_ntlm_relay_chain_floors_both": ".test_ntlm_relay_chain_floors_both()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L74 | neighbors=[TestChains]
- "tests_test_posture_row_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L110 | neighbors=[_Row]
- "tests_test_posture_rules_rationale_1": "test_posture_rules.py — the manager posture/config detection engine.  Covers: th" | kind=entity | source=manager/detection_engine/tests/test_posture_rules.py:L1 | neighbors=[test_posture_rules.py]
- "tests_test_posture_rules_rationale_96": "The live tls_scanner labels its probe list \"TLSv1_0\"/\"TLSv1_1\" (from         ssl" | kind=entity | source=manager/detection_engine/tests/test_posture_rules.py:L96 | neighbors=[.test_deprecated_tls_version_underscore…]
- "tests_test_posture_rules_testriskmodel_test_auth_enforced_deescalates": ".test_auth_enforced_deescalates()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L133 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testriskmodel_test_internet_facing_unauth_escalates": ".test_internet_facing_unauth_escalates()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L138 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testriskmodel_test_priority_buckets": ".test_priority_buckets()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L148 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testriskmodel_test_suspected_scores_below_confirmed": ".test_suspected_scores_below_confirmed()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L143 | neighbors=[TestRiskModel]
- "tests_test_posture_rules_testtrusttier_test_registry_contains_user_validated_set": ".test_registry_contains_user_validated_set()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L43 | neighbors=[TestTrustTier]
- "tests_test_posture_test_aggregate_is_bounded_and_empty_is_zero": "test_aggregate_is_bounded_and_empty_is_zero()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L22 | neighbors=[test_posture.py]
- "tests_test_posture_test_aggregate_is_monotonic": "test_aggregate_is_monotonic()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L31 | neighbors=[test_posture.py]
- "tests_test_posture_test_build_posture_no_runs": "test_build_posture_no_runs()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L72 | neighbors=[test_posture.py]
- "tests_test_posture_test_compute_scores_empty_is_perfect": "test_compute_scores_empty_is_perfect()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L48 | neighbors=[test_posture.py]
- "tests_test_posture_test_grade_bands": "test_grade_bands()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L37 | neighbors=[test_posture.py]
- "tests_test_posture_test_posture_report_section_omitted_without_runs": "test_posture_report_section_omitted_without_runs()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L167 | neighbors=[test_posture.py]
- "tests_test_posture_test_posture_report_section_renders_scores_and_matrix": "test_posture_report_section_renders_scores_and_matrix()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L149 | neighbors=[test_posture.py]
- "tests_test_posture_test_sev_str_passes_through_plain_string": "test_sev_str_passes_through_plain_string()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L143 | neighbors=[test_posture.py]
- "tests_test_posture_trace_rationale_1": "test_posture_trace.py — the detection trace: every rule evaluation records an OU" | kind=entity | source=manager/detection_engine/tests/test_posture_trace.py:L1 | neighbors=[test_posture_trace.py]
- "tests_test_posture_trace_rationale_63": "I10 structurally: for EVERY rule with a declared contract, feeding a fact" | kind=entity | source=manager/detection_engine/tests/test_posture_trace.py:L63 | neighbors=[.test_missing_input_invariant_across_al…]
- "tests_test_printer_scanner_rationale_1": "test_printer_scanner.py — network printer exposure (9100 PJL / 631 IPP).  Pure P" | kind=entity | source=probe/tests/test_printer_scanner.py:L1 | neighbors=[test_printer_scanner.py]
- "tests_test_printer_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L62 | neighbors=[TestParity]
- "tests_test_printer_scanner_testprinterfindings_test_exposed_low": ".test_exposed_low()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L53 | neighbors=[TestPrinterFindings]
- "tests_test_printer_scanner_testpurelogic_test_build_ipp": ".test_build_ipp()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L23 | neighbors=[TestPureLogic]
- "tests_test_printer_scanner_testpurelogic_test_parse_ipp_make_model": ".test_parse_ipp_make_model()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L27 | neighbors=[TestPureLogic]
- "tests_test_printer_scanner_testpurelogic_test_parse_pjl_id": ".test_parse_pjl_id()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L19 | neighbors=[TestPureLogic]
- "tests_test_probe_auto_enroll_rationale_1": "test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.  T" | kind=entity | source=manager/backend/tests/test_probe_auto_enroll.py:L1 | neighbors=[test_probe_auto_enroll.py]
- "tests_test_probe_auto_enroll_test_auto_enroll_cidrs_defaults_to_rfc1918": "test_auto_enroll_cidrs_defaults_to_rfc1918()" | kind=code-symbol | source=manager/backend/tests/test_probe_auto_enroll.py:L23 | neighbors=[test_probe_auto_enroll.py]
- "tests_test_probe_auto_enroll_test_auto_enroll_cidrs_parses_and_trims_custom": "test_auto_enroll_cidrs_parses_and_trims_custom()" | kind=code-symbol | source=manager/backend/tests/test_probe_auto_enroll.py:L29 | neighbors=[test_probe_auto_enroll.py]
- "tests_test_probe_auto_enroll_test_auto_enroll_is_off_by_default": "test_auto_enroll_is_off_by_default()" | kind=code-symbol | source=manager/backend/tests/test_probe_auto_enroll.py:L17 | neighbors=[test_probe_auto_enroll.py]
- "tests_test_probe_auto_enroll_test_auto_enroll_site_name_is_stable": "test_auto_enroll_site_name_is_stable()" | kind=code-symbol | source=manager/backend/tests/test_probe_auto_enroll.py:L36 | neighbors=[test_probe_auto_enroll.py]
- "tests_test_probe_core_rationale_1": "Probe test suite — unit tests for the probe's pure-logic modules. Covers: ScopeG" | kind=entity | source=probe/tests/test_probe_core.py:L1 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_rationale_673": "ipv6_discovery reports on the RUN (its target is an interface name, or         t" | kind=entity | source=probe/tests/test_probe_core.py:L673 | neighbors=[.test_run_scoped_summary_does_not_becom…]
- "tests_test_probe_core_test_explicit_local_manager_urls": "test_explicit_local_manager_urls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L47 | neighbors=[test_probe_core.py]
- "tests_test_probe_core_test_nonlocal_manager_urls": "test_nonlocal_manager_urls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L57 | neighbors=[test_probe_core.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-294.json

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
