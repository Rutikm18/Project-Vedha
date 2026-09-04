# Node Description Batch 162 of 332

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_reference_testtellingthemapart_test_a_reference_is_distinguishable_from_a_uuid": ".test_a_reference_is_distinguishable_from_a_uuid()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L75 | neighbors=[TestTellingThemApart, _at()]
- "tests_test_remediation_generator_testnormalizeaiplan_test_drops_unsafe_command_and_flags_step": ".test_drops_unsafe_command_and_flags_step()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L93 | neighbors=[TestNormalizeAiPlan, ._raw()]
- "tests_test_remediation_generator_testnormalizeaiplan_test_emits_kb_schema_with_source_ai": ".test_emits_kb_schema_with_source_ai()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L83 | neighbors=[TestNormalizeAiPlan, ._raw()]
- "tests_test_remediation_generator_testnormalizeaiplan_test_keeps_safe_command_without_flag": ".test_keeps_safe_command_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L99 | neighbors=[TestNormalizeAiPlan, ._raw()]
- "tests_test_remediation_kb_testclassify_test_cve_without_keyword_is_patch": ".test_cve_without_keyword_is_patch()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L31 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testclassify_test_keyword_categories": ".test_keyword_categories()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L28 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testclassify_test_order_specificity_anon_ftp_beats_generic": ".test_order_specificity_anon_ftp_beats_generic()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L38 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testclassify_test_unmatched_is_generic": ".test_unmatched_is_generic()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L35 | neighbors=[TestClassify, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_missing_os_defaults_to_generic": ".test_missing_os_defaults_to_generic()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L84 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_network_os_falls_back_to_generic_guidance": ".test_network_os_falls_back_to_generic_guidance()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L72 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_returns_kb_source_and_category": ".test_returns_kb_source_and_category()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L60 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_steps_are_numbered_and_os_filtered": ".test_steps_are_numbered_and_os_filtered()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L66 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_kb_testrecipeforfinding_test_unknown_finding_yields_generic_plan": ".test_unknown_finding_yields_generic_plan()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L79 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_routes_fakedb_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L72 | neighbors=[_FakeDB, _scalar_result()]
- "tests_test_remediation_routes_genunavailable": "_GenUnavailable" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L80 | neighbors=[test_remediation_routes.py, .__init__()]
- "tests_test_remediation_routes_testupsertstatement_test_refreshes_generated_at_on_conflict": ".test_refreshes_generated_at_on_conflict()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L210 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_regeneration_resets_review_gate_not_inherits_prior_approval": ".test_regeneration_resets_review_gate_not_inherits_prior_approval()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L201 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_targets_the_unique_constraint": ".test_targets_the_unique_constraint()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L198 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_upsert_integration_stmt": "_stmt()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L49 | neighbors=[test_remediation_upsert_integration.py, _run()]
- "tests_test_remediation_upsert_integration_test_upsert_resets_gate_and_is_race_safe": "test_upsert_resets_gate_and_is_race_safe()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L103 | neighbors=[test_remediation_upsert_integration.py, _run()]
- "tests_test_resolve_testresolvefamily_test_default_no_family_is_backward_compatible": ".test_default_no_family_is_backward_compatible()" | kind=code-symbol | source=probe/tests/test_resolve.py:L34 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_family_absent_falls_back_to_first": ".test_requested_family_absent_falls_back_to_first()" | kind=code-symbol | source=probe/tests/test_resolve.py:L28 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_ipv4_selected_over_v6_first": ".test_requested_ipv4_selected_over_v6_first()" | kind=code-symbol | source=probe/tests/test_resolve.py:L21 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_result_archive_reset_archive_latch": "_reset_archive_latch()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L26 | neighbors=[test_result_archive.py, The disable latch is module state; keep…]
- "tests_test_result_archive_testarchiveisbesteffort_test_default_location_is_the_probe_root": ".test_default_location_is_the_probe_root()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L151 | neighbors=[Unset env => alongside agent/ scanner/ …, TestArchiveIsBestEffort]
- "tests_test_result_archive_testprepareatstartup_test_existing_but_unwritable_directory_is_caught_at_startup": ".test_existing_but_unwritable_directory_is_caught_at_startup()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L184 | neighbors=[The Linux bind-mount case: Docker creat…, TestPrepareAtStartup]
- "tests_test_risk_port_coverage_test_named_high_value_ports_are_scanned": "test_named_high_value_ports_are_scanned()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L151 | neighbors=[test_risk_port_coverage.py, _swept_by_network_va()]
- "tests_test_risk_rank_test_bounds": "test_bounds()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L15 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_confirmed_exploitable_outranks_contradicted": "test_confirmed_exploitable_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L23 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_contradicted_sinks_below_inferred": "test_contradicted_sinks_below_inferred()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L29 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_internet_facing_raises_and_auth_lowers": "test_internet_facing_raises_and_auth_lowers()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L37 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_kev_raises_rank": "test_kev_raises_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L33 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_low_confidence_lowers_rank": "test_low_confidence_lowers_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L42 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_severity_remains_an_impact_signal_without_cvss": "test_severity_remains_an_impact_signal_without_cvss()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L72 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_router_signals_test_https_on_odd_port_routes_tls_and_web": "test_https_on_odd_port_routes_tls_and_web()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L52 | neighbors=[test_router_signals.py, _open()]
- "tests_test_router_signals_test_no_tls_flag_omits_the_marker": "test_no_tls_flag_omits_the_marker()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L161 | neighbors=[test_router_signals.py, --no-tls means no handshake was tried, …]
- "tests_test_router_signals_test_service_banner_records_tls_probed": "test_service_banner_records_tls_probed()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L137 | neighbors=[test_router_signals.py, The flag must actually be emitted, or t…]
- "tests_test_router_signals_test_workflow_hands_observed_tls_ports_to_web_scanner": "test_workflow_hands_observed_tls_ports_to_web_scanner()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L70 | neighbors=[test_router_signals.py, 9000 is in the static WEB table but NOT…]
- "tests_test_router_signals_testtlsprobednegative_test_binary_protocol_ports_route_nowhere": ".test_binary_protocol_ports_route_nowhere()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L129 | neighbors=[TestTlsProbedNegative, _open()]
- "tests_test_rsync_scanner_testhandshake_test_echo_stops_at_the_first_line": ".test_echo_stops_at_the_first_line()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L68 | neighbors=[TestHandshake, _FakeSock]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-161.json

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
