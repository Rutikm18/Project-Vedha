# Node Description Batch 119 of 236

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

- "tests_test_remediation_kb_testrecipeforfinding_test_unknown_finding_yields_generic_plan": ".test_unknown_finding_yields_generic_plan()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L79 | neighbors=[TestRecipeForFinding, _f()]
- "tests_test_remediation_routes_fakedb_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L71 | neighbors=[_FakeDB, _scalar_result()]
- "tests_test_remediation_routes_genunavailable": "_GenUnavailable" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L79 | neighbors=[test_remediation_routes.py, .__init__()]
- "tests_test_remediation_routes_testupsertstatement_test_refreshes_generated_at_on_conflict": ".test_refreshes_generated_at_on_conflict()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L203 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_regeneration_resets_review_gate_not_inherits_prior_approval": ".test_regeneration_resets_review_gate_not_inherits_prior_approval()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L194 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_routes_testupsertstatement_test_targets_the_unique_constraint": ".test_targets_the_unique_constraint()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L191 | neighbors=[TestUpsertStatement, ._sql()]
- "tests_test_remediation_upsert_integration_stmt": "_stmt()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L49 | neighbors=[test_remediation_upsert_integration.py, _run()]
- "tests_test_remediation_upsert_integration_test_upsert_resets_gate_and_is_race_safe": "test_upsert_resets_gate_and_is_race_safe()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L103 | neighbors=[test_remediation_upsert_integration.py, _run()]
- "tests_test_resolve_testresolvefamily_test_default_no_family_is_backward_compatible": ".test_default_no_family_is_backward_compatible()" | kind=code-symbol | source=probe/tests/test_resolve.py:L34 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_family_absent_falls_back_to_first": ".test_requested_family_absent_falls_back_to_first()" | kind=code-symbol | source=probe/tests/test_resolve.py:L28 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_resolve_testresolvefamily_test_requested_ipv4_selected_over_v6_first": ".test_requested_ipv4_selected_over_v6_first()" | kind=code-symbol | source=probe/tests/test_resolve.py:L21 | neighbors=[TestResolveFamily, _infos()]
- "tests_test_risk_rank_test_bounds": "test_bounds()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L15 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_confirmed_exploitable_outranks_contradicted": "test_confirmed_exploitable_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L23 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_contradicted_sinks_below_inferred": "test_contradicted_sinks_below_inferred()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L29 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_internet_facing_raises_and_auth_lowers": "test_internet_facing_raises_and_auth_lowers()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L37 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_kev_raises_rank": "test_kev_raises_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L33 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_low_confidence_lowers_rank": "test_low_confidence_lowers_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L42 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_constructs_and_wires_real_scanners": ".test_constructs_and_wires_real_scanners()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L191 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_port_scanner_is_syn_scanner": ".test_port_scanner_is_syn_scanner()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L201 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_invoked_with_db_port": ".test_db_scanner_invoked_with_db_port()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L154 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_not_invoked_without_db_port": ".test_db_scanner_not_invoked_without_db_port()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L149 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_dead_host_forced_runs_full": ".test_dead_host_forced_runs_full()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L130 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_dead_host_skips_port_scan": ".test_dead_host_skips_port_scan()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L120 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_deep_scanner_receives_only_open_ports": ".test_deep_scanner_receives_only_open_ports()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L142 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_no_open_ports_runs_no_deep_scanners": ".test_no_open_ports_runs_no_deep_scanners()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L160 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_open_ports_extracted": ".test_open_ports_extracted()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L137 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_out_of_scope_target": ".test_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L175 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_results_aggregate_all_stages": ".test_results_aggregate_all_stages()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L167 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_stages_run_order": ".test_stages_run_order()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L181 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnelrun": "TestScanFunnelRun" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L217 | neighbors=[test_scan_funnel.py, .test_run_writes_all_results()]
- "tests_test_scan_funnel_testscanfunnelrun_test_run_writes_all_results": ".test_run_writes_all_results()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L218 | neighbors=[TestScanFunnelRun, _make_funnel()]
- "tests_test_scan_health_test_clean_scan_is_healthy_and_does_not_warn": "test_clean_scan_is_healthy_and_does_not_warn()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L17 | neighbors=[test_scan_health.py, _summary()]
- "tests_test_scan_health_test_local_resource_errors_flag_degraded": "test_local_resource_errors_flag_degraded()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L24 | neighbors=[test_scan_health.py, _summary()]
- "tests_test_scan_health_test_missing_ports_flag_incomplete": "test_missing_ports_flag_incomplete()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L32 | neighbors=[test_scan_health.py, _summary()]
- "tests_test_scanner_parity_test_scanner_module_matches_main_scripts": "test_scanner_module_matches_main_scripts()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L48 | neighbors=[test_scanner_parity.py, Each scanner/<mod>.py is byte-identical…]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_multiple_encrypts_different": ".test_multiple_encrypts_different()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L78 | neighbors=[Each encryption uses a fresh ephemeral …, TestEncryptDecryptRoundtrip]
- "tests_test_scope_targets_test_property_every_accepted_target_is_subnet_of_scope": "test_property_every_accepted_target_is_subnet_of_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L98 | neighbors=[test_scope_targets.py, Whatever the validator accepts must be …]
- "tests_test_scope_targets_testnoscopeauthorizesnothing": "TestNoScopeAuthorizesNothing" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L15 | neighbors=[test_scope_targets.py, .test_empty_scope_denies_all()]
- "tests_test_seed_admin_testdatabaseunavailable": "TestDatabaseUnavailable" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L288 | neighbors=[test_seed_admin.py, .test_retries_then_raises_database_unav…]
- "tests_test_seed_admin_testexistingadminnoreset": "TestExistingAdminNoReset" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L139 | neighbors=[test_seed_admin.py, .test_noop_when_user_exists_and_no_forc…]

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
