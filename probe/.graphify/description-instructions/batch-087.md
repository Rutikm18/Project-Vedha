# Node Description Batch 88 of 92

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_validation_test_score_inventory_reports_precision_recall_and_unscored_dimensions": "test_score_inventory_reports_precision_recall_and_unscored_dimensions()" | kind=code-symbol | source=tests/test_validation.py:L62 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_target_address_count_is_conservative": "test_target_address_count_is_conservative()" | kind=code-symbol | source=tests/test_validation.py:L47 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts": "test_validate_ground_truth_rejects_invalid_ports_and_duplicate_hosts()" | kind=code-symbol | source=tests/test_validation.py:L51 | neighbors=[test_validation.py] | lang=en
- "tests_test_validation_test_validate_targets_enforces_scope_and_exclusions": "test_validate_targets_enforces_scope_and_exclusions()" | kind=code-symbol | source=tests/test_validation.py:L32 | neighbors=[test_validation.py] | lang=en
- "tests_test_web_methods_test_dangerous_methods_flagged": "test_dangerous_methods_flagged()" | kind=code-symbol | source=tests/test_web_methods.py:L4 | neighbors=[test_web_methods.py] | lang=en
- "tests_test_web_methods_test_no_allow_header": "test_no_allow_header()" | kind=code-symbol | source=tests/test_web_methods.py:L17 | neighbors=[test_web_methods.py] | lang=en
- "tests_test_web_methods_test_safe_methods_only": "test_safe_methods_only()" | kind=code-symbol | source=tests/test_web_methods.py:L12 | neighbors=[test_web_methods.py] | lang=en
- "tests_test_wire_identity_rationale_1": "test_wire_identity.py — the scanner must NOT sign its own packets.  A brand stri" | kind=entity | source=tests/test_wire_identity.py:L1 | neighbors=[test_wire_identity.py] | lang=en
- "tests_test_wire_identity_rationale_39": "Evasion: a fixed source port (e.g. 53/88) slips past naive stateless ACLs." | kind=entity | source=tests/test_wire_identity.py:L39 | neighbors=[TestChooseSourcePort] | lang=pt
- "tests_test_wire_identity_rationale_58": "Evasion: blur a fixed scan cadence with a bounded random per-probe delay." | kind=entity | source=tests/test_wire_identity.py:L58 | neighbors=[TestJitteredDelay] | lang=pt
- "tests_test_wire_identity_rationale_81": "Import-time probe constants built from user_agent() must be signature-free." | kind=entity | source=tests/test_wire_identity.py:L81 | neighbors=[TestModuleConstantsUnbranded] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_boundary_ports_are_valid": ".test_boundary_ports_are_valid()" | kind=code-symbol | source=tests/test_wire_identity.py:L52 | neighbors=[TestChooseSourcePort] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_none_gives_random_ephemeral": ".test_none_gives_random_ephemeral()" | kind=code-symbol | source=tests/test_wire_identity.py:L45 | neighbors=[TestChooseSourcePort] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_out_of_range_falls_back_to_random": ".test_out_of_range_falls_back_to_random()" | kind=code-symbol | source=tests/test_wire_identity.py:L48 | neighbors=[TestChooseSourcePort] | lang=en
- "tests_test_wire_identity_testchoosesourceport_test_uses_configured_valid_port": ".test_uses_configured_valid_port()" | kind=code-symbol | source=tests/test_wire_identity.py:L41 | neighbors=[TestChooseSourcePort] | lang=en
- "tests_test_wire_identity_testevasionflags_test_randomize_and_scan_delay_flags_present": ".test_randomize_and_scan_delay_flags_present()" | kind=code-symbol | source=tests/test_wire_identity.py:L74 | neighbors=[TestEvasionFlags] | lang=en
- "tests_test_wire_identity_testjittereddelay_test_never_negative_even_at_full_jitter": ".test_never_negative_even_at_full_jitter()" | kind=code-symbol | source=tests/test_wire_identity.py:L68 | neighbors=[TestJitteredDelay] | lang=en
- "tests_test_wire_identity_testjittereddelay_test_stays_within_jitter_band": ".test_stays_within_jitter_band()" | kind=code-symbol | source=tests/test_wire_identity.py:L64 | neighbors=[TestJitteredDelay] | lang=en
- "tests_test_wire_identity_testjittereddelay_test_zero_or_negative_base_is_zero": ".test_zero_or_negative_base_is_zero()" | kind=code-symbol | source=tests/test_wire_identity.py:L60 | neighbors=[TestJitteredDelay] | lang=en
- "tests_test_wire_identity_testmoduleconstantsunbranded_test_iot_rtsp_options": ".test_iot_rtsp_options()" | kind=code-symbol | source=tests/test_wire_identity.py:L87 | neighbors=[TestModuleConstantsUnbranded] | lang=en
- "tests_test_wire_identity_testmoduleconstantsunbranded_test_service_banner_http_probe": ".test_service_banner_http_probe()" | kind=code-symbol | source=tests/test_wire_identity.py:L83 | neighbors=[TestModuleConstantsUnbranded] | lang=en
- "tests_test_wire_identity_testprobepayload_test_default_carries_no_brand": ".test_default_carries_no_brand()" | kind=code-symbol | source=tests/test_wire_identity.py:L29 | neighbors=[TestProbePayload] | lang=en
- "tests_test_wire_identity_testprobepayload_test_env_override": ".test_env_override()" | kind=code-symbol | source=tests/test_wire_identity.py:L33 | neighbors=[TestProbePayload] | lang=en
- "tests_test_wire_identity_testuseragent_test_default_is_generic_browser_no_brand": ".test_default_is_generic_browser_no_brand()" | kind=code-symbol | source=tests/test_wire_identity.py:L18 | neighbors=[TestUserAgent] | lang=en
- "tests_test_wire_identity_testuseragent_test_env_override": ".test_env_override()" | kind=code-symbol | source=tests/test_wire_identity.py:L23 | neighbors=[TestUserAgent] | lang=en
- "tests_test_workflow_execution_concurrencyscanner_init": ".__init__()" | kind=code-symbol | source=tests/test_workflow_execution.py:L49 | neighbors=[_ConcurrencyScanner] | lang=en
- "tests_test_workflow_execution_concurrencyscanner_scan_target": ".scan_target()" | kind=code-symbol | source=tests/test_workflow_execution.py:L53 | neighbors=[_ConcurrencyScanner] | lang=en
- "tests_test_workflow_execution_explodingscanner_scan_target": ".scan_target()" | kind=code-symbol | source=tests/test_workflow_execution.py:L32 | neighbors=[_ExplodingScanner] | lang=en
- "tests_test_workflow_execution_test_agent_scan_types_have_distinct_stage_ceilings": "test_agent_scan_types_have_distinct_stage_ceilings()" | kind=code-symbol | source=tests/test_workflow_execution.py:L419 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_database_gate_uses_scanner_port_catalog": "test_database_gate_uses_scanner_port_catalog()" | kind=code-symbol | source=tests/test_workflow_execution.py:L132 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_empty_authoritative_scope_never_falls_back_to_job_targets": "test_empty_authoritative_scope_never_falls_back_to_job_targets()" | kind=code-symbol | source=tests/test_workflow_execution.py:L519 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_applies_configured_target_ceiling": "test_engine_applies_configured_target_ceiling()" | kind=code-symbol | source=tests/test_workflow_execution.py:L446 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_deadline_fails_when_no_evidence_exists": "test_engine_deadline_fails_when_no_evidence_exists()" | kind=code-symbol | source=tests/test_workflow_execution.py:L467 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_deadline_preserves_verified_partial_evidence": "test_engine_deadline_preserves_verified_partial_evidence()" | kind=code-symbol | source=tests/test_workflow_execution.py:L486 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_enforces_local_scope_after_engagement_scope": "test_engine_enforces_local_scope_after_engagement_scope()" | kind=code-symbol | source=tests/test_workflow_execution.py:L455 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_exposes_component_manifest_and_run_states": "test_engine_exposes_component_manifest_and_run_states()" | kind=code-symbol | source=tests/test_workflow_execution.py:L530 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_fails_when_every_observation_is_an_error": "test_engine_fails_when_every_observation_is_an_error()" | kind=code-symbol | source=tests/test_workflow_execution.py:L566 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_rejects_non_string_targets": "test_engine_rejects_non_string_targets()" | kind=code-symbol | source=tests/test_workflow_execution.py:L431 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_engine_rejects_oversized_cidr_instead_of_false_success": "test_engine_rejects_oversized_cidr_instead_of_false_success()" | kind=code-symbol | source=tests/test_workflow_execution.py:L438 | neighbors=[test_workflow_execution.py] | lang=en
- "tests_test_workflow_execution_test_error_result_does_not_mutate_asset_state": "test_error_result_does_not_mutate_asset_state()" | kind=code-symbol | source=tests/test_workflow_execution.py:L87 | neighbors=[test_workflow_execution.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-087.json

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
