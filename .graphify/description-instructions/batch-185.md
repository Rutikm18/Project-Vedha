# Node Description Batch 186 of 380

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

- "tests_test_scan_schedule_model_testcolumns_test_next_run_at_is_not_nullable": ".test_next_run_at_is_not_nullable()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_model.py:L35 | neighbors=[A schedule with no due time would never…, TestColumns]
- "tests_test_scan_schedule_model_testrelationshipsafety_test_created_by_survives_user_deletion": ".test_created_by_survives_user_deletion()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_model.py:L52 | neighbors=[SET NULL, not CASCADE — losing the auth…, TestRelationshipSafety]
- "tests_test_scan_schedule_model_testrelationshipsafety_test_engagement_deletion_removes_the_schedule": ".test_engagement_deletion_removes_the_schedule()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_model.py:L57 | neighbors=[CASCADE here IS right: a schedule for a…, TestRelationshipSafety]
- "tests_test_scan_schedule_model_testrelationshipsafety_test_is_registered_in_the_model_aggregator": ".test_is_registered_in_the_model_aggregator()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_model.py:L63 | neighbors=[An unregistered model is invisible to A…, TestRelationshipSafety]
- "tests_test_scanner_congestion_testcollapserecovery_test_slow_start_is_used_below_ssthresh": ".test_slow_start_is_used_below_ssthresh()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L579 | neighbors=[TestCollapseRecovery, ._collapsed()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_responsive_host_is_not_throttled": ".test_responsive_host_is_not_throttled()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L163 | neighbors=[TestConnectCongestionWindow, _scanner()]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_floor_is_clamped": ".test_floor_is_clamped()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L492 | neighbors=[TestDeliveryAwareBackoff, ._sc()]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_floor_is_configurable": ".test_floor_is_configurable()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L489 | neighbors=[TestDeliveryAwareBackoff, ._sc()]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_window_is_bounded": ".test_window_is_bounded()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L470 | neighbors=[TestDeliveryAwareBackoff, ._sc()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_short_tcp_info_buffer_is_ignored": ".test_short_tcp_info_buffer_is_ignored()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L259 | neighbors=[TestHarvestTcpStack, _FakeSock]
- "tests_test_scanner_congestion_testreprobecleanuppass_silent_attempt": "._silent_attempt()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L379 | neighbors=[TestReprobeCleanupPass, .test_genuinely_filtered_ports_stay_fil…]
- "tests_test_scanner_congestion_testresolvecandidates_test_deduplicates_repeated_addresses": ".test_deduplicates_repeated_addresses()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L302 | neighbors=[TestResolveCandidates, _fake_gai()]
- "tests_test_scanner_congestion_testresolvecandidates_test_family_filter_restricts_results": ".test_family_filter_restricts_results()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L313 | neighbors=[TestResolveCandidates, _fake_gai()]
- "tests_test_scanner_congestion_testresolvecandidates_test_returns_every_family_in_order": ".test_returns_every_family_in_order()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L297 | neighbors=[TestResolveCandidates, _fake_gai()]
- "tests_test_scanner_parity_test_scanner_module_matches_main_scripts": "test_scanner_module_matches_main_scripts()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L48 | neighbors=[test_scanner_parity.py, Each scanner/<mod>.py is byte-identical…]
- "tests_test_scheduler_testadvance_test_is_never_left_in_the_past": ".test_is_never_left_in_the_past()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L79 | neighbors=[TestAdvance, _sched()]
- "tests_test_scheduler_testadvance_test_sets_last_run_and_next_by_interval": ".test_sets_last_run_and_next_by_interval()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L65 | neighbors=[TestAdvance, _sched()]
- "tests_test_scheduler_testdueselection_test_disabled_is_never_selected_even_when_overdue": ".test_disabled_is_never_selected_even_when_overdue()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L52 | neighbors=[TestDueSelection, _sched()]
- "tests_test_scheduler_testdueselection_test_future_is_not_selected": ".test_future_is_not_selected()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L49 | neighbors=[TestDueSelection, _sched()]
- "tests_test_scheduler_testdueselection_test_mixed_set": ".test_mixed_set()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L55 | neighbors=[TestDueSelection, _sched()]
- "tests_test_scheduler_testdueselection_test_past_due_and_enabled_is_selected": ".test_past_due_and_enabled_is_selected()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L40 | neighbors=[TestDueSelection, _sched()]
- "tests_test_scheduler_testrundue_test_enqueues_and_advances_due_only": ".test_enqueues_and_advances_due_only()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L87 | neighbors=[TestRunDue, _sched()]
- "tests_test_scheduler_testrundue_test_nothing_due_is_a_no_op": ".test_nothing_due_is_a_no_op()" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L124 | neighbors=[TestRunDue, _sched()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_multiple_encrypts_different": ".test_multiple_encrypts_different()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L78 | neighbors=[Each encryption uses a fresh ephemeral …, TestEncryptDecryptRoundtrip]
- "tests_test_scope_targets_test_property_every_accepted_target_is_subnet_of_scope": "test_property_every_accepted_target_is_subnet_of_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L98 | neighbors=[test_scope_targets.py, Whatever the validator accepts must be …]
- "tests_test_scope_targets_testnoscopeauthorizesnothing": "TestNoScopeAuthorizesNothing" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L15 | neighbors=[test_scope_targets.py, .test_empty_scope_denies_all()]
- "tests_test_seed_admin_testdatabaseunavailable": "TestDatabaseUnavailable" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L288 | neighbors=[test_seed_admin.py, .test_retries_then_raises_database_unav…]
- "tests_test_seed_admin_testexistingadminnoreset": "TestExistingAdminNoReset" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L139 | neighbors=[test_seed_admin.py, .test_noop_when_user_exists_and_no_forc…]
- "tests_test_seed_admin_testfirstdeployment": "TestFirstDeployment" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L96 | neighbors=[test_seed_admin.py, .test_creates_tenant_and_admin_on_first…]
- "tests_test_self_scan_test_execute_writes_scope_runs_engine_and_archives": "test_execute_writes_scope_runs_engine_and_archives()" | kind=code-symbol | source=probe/tests/test_self_scan.py:L40 | neighbors=[test_self_scan.py, FakeQueue]
- "tests_test_service_banner_ident_self_signed": "_self_signed()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L247 | neighbors=[test_service_banner_ident.py, test_https_on_arbitrary_port_identifies…]
- "tests_test_service_banner_ident_test_prefers_decrypted_tls_reply_over_plaintext_noise": "test_prefers_decrypted_tls_reply_over_plaintext_noise()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L196 | neighbors=[test_service_banner_ident.py, _scanner()]
- "tests_test_service_banner_ident_test_slow_greeting_still_identifies": "test_slow_greeting_still_identifies()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L170 | neighbors=[test_service_banner_ident.py, A speak-first daemon that delays its 22…]
- "tests_test_service_banner_ident_testladder_test_client_first_ports_skip_null_rung": ".test_client_first_ports_skip_null_rung()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L147 | neighbors=[TestLadder, _scanner()]
- "tests_test_service_banner_ident_testladder_test_greet_timeout_tracks_operator_timeout": ".test_greet_timeout_tracks_operator_timeout()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L156 | neighbors=[TestLadder, _scanner()]
- "tests_test_service_banner_ident_testladder_test_no_tls_flag_drops_rung": ".test_no_tls_flag_drops_rung()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L153 | neighbors=[TestLadder, _scanner()]
- "tests_test_service_identifier_rationale_1": "Unit tests for ServiceIdentifier." | kind=entity | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[test_service_identifier.py, ServiceIdentifier]
- "tests_test_service_identifier_testserviceidentifier_test_confidence_floor_port_hint": ".test_confidence_floor_port_hint()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L70 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ftp_banner": ".test_ftp_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L28 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_high_confidence_combined": ".test_high_confidence_combined()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L75 | neighbors=[TestServiceIdentifier, ._id()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-185.json

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
