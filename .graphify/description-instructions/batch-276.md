# Node Description Batch 277 of 336

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

- "tests_test_branch_registry_testregistryconsistency_test_components_are_unique": ".test_components_are_unique()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L77 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_every_branch_has_a_scanner_the_engine_can_resolve": ".test_every_branch_has_a_scanner_the_engine_can_resolve()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L49 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_every_component_is_in_the_plan_catalog": ".test_every_component_is_in_the_plan_catalog()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L53 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_kwargs_builders_have_the_expected_signature": ".test_kwargs_builders_have_the_expected_signature()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L81 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_campaign_progress_rationale_1": "VA Campaigns live view: per-probe jobs + pipeline phases + findings+remediation." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L1 | neighbors=[test_campaign_progress.py] | lang=en
- "tests_test_campaign_progress_rationale_118": "Build a campaign_progress scenario with a given job + detection-run state." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L118 | neighbors=[_run_scenario()] | lang=pt
- "tests_test_campaign_progress_rationale_168": "Regression: RUN_COMPLETED is 'completed', not 'done' — the endpoint must not" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L168 | neighbors=[test_completed_run_is_not_stuck_at_dete…] | lang=en
- "tests_test_campaign_progress_rationale_218": "The invariant. Checked across the states a real campaign passes through." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L218 | neighbors=[test_percent_reaches_100_exactly_when_t…] | lang=en
- "tests_test_campaign_progress_rationale_22": "A result whose .all() returns raw rows (used for the queue-state query)." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L22 | neighbors=[_rows()] | lang=en
- "tests_test_campaign_progress_rationale_239": "The exact regression: the newest submission was detected, an earlier one was" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L239 | neighbors=[test_uncovered_submission_holds_progres…] | lang=en
- "tests_test_campaign_progress_rationale_268": "The other way a campaign never finishes: a run that starts and never     complet" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L268 | neighbors=[test_a_wedged_detection_run_explains_it…] | lang=en
- "tests_test_campaign_progress_rationale_284": "A run that started seconds ago is busy, not wedged — no alarming reason." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L284 | neighbors=[test_a_briefly_running_run_is_not_calle…] | lang=en
- "tests_test_campaign_progress_rationale_295": "started_at can come back tz-naive depending on the driver; subtracting it     fr" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L295 | neighbors=[test_naive_started_at_does_not_crash_th…] | lang=en
- "tests_test_campaign_progress_rationale_327": "THE CRY-WOLF CASE. 90 minutes in, worker heartbeating — this is a large     scop" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L327 | neighbors=[test_a_long_run_with_a_live_worker_is_n…] | lang=en
- "tests_test_campaign_progress_rationale_337": "No patience needed when the thing that would finish the run has stopped     hear" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L337 | neighbors=[test_a_dead_worker_is_called_out_quickl…] | lang=en
- "tests_test_campaign_progress_rationale_346": "Under the floor: a heartbeat gap of a few seconds around a restart must not" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L346 | neighbors=[test_a_briefly_running_run_with_a_dead_…] | lang=pt
- "tests_test_campaign_progress_rationale_354": "No heartbeat table (migration not yet run) — duration is all we have, so the" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L354 | neighbors=[test_unknown_worker_liveness_falls_back…] | lang=en
- "tests_test_campaign_progress_rationale_367": "Whatever the verdict, a stalled run must not flip the campaign complete." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L367 | neighbors=[test_stall_never_claims_completion_eith…] | lang=en
- "tests_test_campaign_progress_terminal_rationale_1": "A campaign whose jobs all ended without producing results must reach a TERMINAL" | kind=entity | source=manager/backend/tests/test_campaign_progress_terminal.py:L1 | neighbors=[test_campaign_progress_terminal.py] | lang=pt
- "tests_test_campaign_progress_terminal_rationale_50": "The normal path must be untouched: a completed job with no run yet is         ge" | kind=entity | source=manager/backend/tests/test_campaign_progress_terminal.py:L50 | neighbors=[.test_does_not_hijack_a_campaign_that_p…] | lang=en
- "tests_test_campaign_progress_terminal_rationale_57": "Precedence: work in flight is reported before any terminal verdict." | kind=entity | source=manager/backend/tests/test_campaign_progress_terminal.py:L57 | neighbors=[.test_running_job_still_wins()] | lang=en
- "tests_test_campaign_progress_terminal_rationale_67": "One good job is enough to expect a detection run." | kind=entity | source=manager/backend/tests/test_campaign_progress_terminal.py:L67 | neighbors=[.test_partial_cancel_with_one_success_s…] | lang=en
- "tests_test_campaign_progress_terminal_rationale_73": "Regression guard: the happy path and its known edge cases still hold." | kind=entity | source=manager/backend/tests/test_campaign_progress_terminal.py:L73 | neighbors=[TestNormalPipelineUnaffected] | lang=en
- "tests_test_campaign_progress_terminal_rationale_94": "Callers that don't pass the new inputs must behave as before." | kind=entity | source=manager/backend/tests/test_campaign_progress_terminal.py:L94 | neighbors=[.test_defaults_keep_backwards_compatibi…] | lang=en
- "tests_test_cli_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_cli.py:L153 | neighbors=[FakeClient] | lang=en
- "tests_test_cli_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_cli.py:L157 | neighbors=[FakeClient] | lang=en
- "tests_test_cli_test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity": "test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity()" | kind=code-symbol | source=probe/tests/test_cli.py:L318 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_cmd_doctor_fails_when_no_agent_unless_allowed": "test_cmd_doctor_fails_when_no_agent_unless_allowed()" | kind=code-symbol | source=probe/tests/test_cli.py:L248 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_config_store_rejects_malformed_json": "test_config_store_rejects_malformed_json()" | kind=code-symbol | source=probe/tests/test_cli.py:L31 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_config_store_rejects_non_object_profiles": "test_config_store_rejects_non_object_profiles()" | kind=code-symbol | source=probe/tests/test_cli.py:L38 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_config_store_writes_private_file": "test_config_store_writes_private_file()" | kind=code-symbol | source=probe/tests/test_cli.py:L13 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_normalize_manager_url_trims_and_validates": "test_normalize_manager_url_trims_and_validates()" | kind=code-symbol | source=probe/tests/test_cli.py:L72 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_parse_param_pairs_rejects_missing_equals": "test_parse_param_pairs_rejects_missing_equals()" | kind=code-symbol | source=probe/tests/test_cli.py:L59 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_parse_param_pairs_supports_json_values": "test_parse_param_pairs_supports_json_values()" | kind=code-symbol | source=probe/tests/test_cli.py:L45 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_parser_accepts_json_after_concrete_commands": "test_parser_accepts_json_after_concrete_commands()" | kind=code-symbol | source=probe/tests/test_cli.py:L80 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_resolve_profile_env_overrides_config": "test_resolve_profile_env_overrides_config()" | kind=code-symbol | source=probe/tests/test_cli.py:L106 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_resolve_profile_reports_missing_manager_or_token": "test_resolve_profile_reports_missing_manager_or_token()" | kind=code-symbol | source=probe/tests/test_cli.py:L134 | neighbors=[test_cli.py] | lang=en
- "tests_test_cli_test_split_values_accepts_repeated_and_csv_values": "test_split_values_accepts_repeated_and_csv_values()" | kind=code-symbol | source=probe/tests/test_cli.py:L64 | neighbors=[test_cli.py] | lang=en
- "tests_test_customer_access_rationale_1": "test_customer_access.py — Phase 1: operator provisioning + scan-request inbox. H" | kind=entity | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[test_customer_access.py] | lang=en
- "tests_test_customer_access_rationale_125": "An email already used elsewhere in the tenant (the operator's own login," | kind=entity | source=manager/backend/tests/test_customer_access.py:L125 | neighbors=[.test_duplicate_email_in_tenant_is_conf…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-276.json

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
