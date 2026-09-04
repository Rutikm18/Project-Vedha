# Node Description Batch 302 of 330

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

- "tests_test_result_spool_testresultspool_test_remove_missing": ".test_remove_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L76 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_and_load": ".test_save_and_load()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L19 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_is_atomic_no_temp_leftover": ".test_save_is_atomic_no_temp_leftover()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L26 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_spool_count": ".test_spool_count()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L80 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_spool_directory_and_result_are_private": ".test_spool_directory_and_result_are_private()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L46 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_exception": ".test_submit_with_retry_exception()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L113 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_failure": ".test_submit_with_retry_failure()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L100 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_success": ".test_submit_with_retry_success()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L87 | neighbors=[TestResultSpool]
- "tests_test_risk_port_coverage_rationale_1": "test_risk_port_coverage.py — the collection half of the exposed-service rules." | kind=entity | source=probe/tests/test_risk_port_coverage.py:L1 | neighbors=[test_risk_port_coverage.py]
- "tests_test_risk_port_coverage_rationale_101": "A connect scan is one socket per port per host, so this list is a cost as     we" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L101 | neighbors=[test_sweep_stays_within_a_sane_budget()]
- "tests_test_risk_port_coverage_rationale_110": "The sweep is profile catalog UNION the TCP branch tables; a regression that" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L110 | neighbors=[test_branch_tables_still_contribute()]
- "tests_test_risk_port_coverage_rationale_128": "The complement of the rule above, pinned so a future edit cannot quietly     add" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L128 | neighbors=[test_datagram_branch_ports_are_not_in_t…]
- "tests_test_risk_port_coverage_rationale_54": "Exactly what a default network_va puts on the wire: the profile catalog     plus" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L54 | neighbors=[_swept_by_network_va()]
- "tests_test_risk_port_coverage_rationale_72": "Called out separately: these carry the highest severity and were 100%     unscan" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L72 | neighbors=[test_every_backdoor_port_is_swept()]
- "tests_test_risk_port_coverage_rationale_81": "Reverse direction: VA_RISK_PORTS must not accumulate ports the manager has     n" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L81 | neighbors=[test_va_risk_ports_are_all_actually_in_…]
- "tests_test_risk_port_coverage_test_it_ports_is_the_union_and_stays_sorted_unique": "test_it_ports_is_the_union_and_stays_sorted_unique()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L95 | neighbors=[test_risk_port_coverage.py]
- "tests_test_risk_port_coverage_test_va_risk_ports_has_no_duplicates_and_is_valid": "test_va_risk_ports_has_no_duplicates_and_is_valid()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L90 | neighbors=[test_risk_port_coverage.py]
- "tests_test_risk_rank_test_distinct_high_risks_do_not_collapse_at_the_ceiling": "test_distinct_high_risks_do_not_collapse_at_the_ceiling()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L54 | neighbors=[test_risk_rank.py]
- "tests_test_risk_rank_test_missing_optionals_do_not_crash": "test_missing_optionals_do_not_crash()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L46 | neighbors=[test_risk_rank.py]
- "tests_test_risk_score_contract_rationale_1": "Regression tests for posture findings entering the Manager risk contract." | kind=entity | source=manager/backend/tests/test_risk_score_contract.py:L1 | neighbors=[test_risk_score_contract.py]
- "tests_test_risk_score_contract_test_only_detection_engine_posture_evidence_uses_the_boundary_conversion": "test_only_detection_engine_posture_evidence_uses_the_boundary_conversion()" | kind=code-symbol | source=manager/backend/tests/test_risk_score_contract.py:L30 | neighbors=[test_risk_score_contract.py]
- "tests_test_risk_score_contract_test_posture_severity_and_evidence_drive_manager_risk": "test_posture_severity_and_evidence_drive_manager_risk()" | kind=code-symbol | source=manager/backend/tests/test_risk_score_contract.py:L18 | neighbors=[test_risk_score_contract.py]
- "tests_test_risk_score_contract_test_upstream_posture_score_cannot_force_the_manager_ceiling": "test_upstream_posture_score_cannot_force_the_manager_ceiling()" | kind=code-symbol | source=manager/backend/tests/test_risk_score_contract.py:L6 | neighbors=[test_risk_score_contract.py]
- "tests_test_router_db_test_mysql_greeting_on_odd_port": "test_mysql_greeting_on_odd_port()" | kind=code-symbol | source=probe/tests/test_router_db.py:L4 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_plain_http_is_not_db": "test_plain_http_is_not_db()" | kind=code-symbol | source=probe/tests/test_router_db.py:L13 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_redis_noauth_signature": "test_redis_noauth_signature()" | kind=code-symbol | source=probe/tests/test_router_db.py:L9 | neighbors=[test_router_db.py]
- "tests_test_router_signals_rationale_1": "test_router_signals.py — router.py consumes service_banner's POSITIVE signals (t" | kind=entity | source=probe/tests/test_router_signals.py:L1 | neighbors=[test_router_signals.py]
- "tests_test_router_signals_rationale_108": "service_banner now ATTEMPTS a TLS handshake on every unidentified port and     r" | kind=entity | source=probe/tests/test_router_signals.py:L108 | neighbors=[TestTlsProbedNegative]
- "tests_test_router_signals_rationale_138": "The flag must actually be emitted, or the router change is inert." | kind=entity | source=probe/tests/test_router_signals.py:L138 | neighbors=[test_service_banner_records_tls_probed()]
- "tests_test_router_signals_rationale_162": "--no-tls means no handshake was tried, so the absence guess must remain     avai" | kind=entity | source=probe/tests/test_router_signals.py:L162 | neighbors=[test_no_tls_flag_omits_the_marker()]
- "tests_test_router_signals_rationale_71": "9000 is in the static WEB table but NOT the TLS table: only the banner's     obs" | kind=entity | source=probe/tests/test_router_signals.py:L71 | neighbors=[test_workflow_hands_observed_tls_ports_…]
- "tests_test_router_signals_testpositivetls_test_absence_heuristic_still_works": ".test_absence_heuristic_still_works()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L31 | neighbors=[TestPositiveTls]
- "tests_test_router_signals_testpositivetls_test_alert_record_service_routes": ".test_alert_record_service_routes()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L28 | neighbors=[TestPositiveTls]
- "tests_test_router_signals_testpositivetls_test_handshake_fact_routes_even_on_client_first_port": ".test_handshake_fact_routes_even_on_client_first_port()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L25 | neighbors=[TestPositiveTls]
- "tests_test_router_signals_teststructuredservice_test_db_by_service_field": ".test_db_by_service_field()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L38 | neighbors=[TestStructuredService]
- "tests_test_router_signals_teststructuredservice_test_http_by_service_field": ".test_http_by_service_field()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L43 | neighbors=[TestStructuredService]
- "tests_test_router_signals_teststructuredservice_test_ssh_by_service_field": ".test_ssh_by_service_field()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L48 | neighbors=[TestStructuredService]
- "tests_test_router_signals_testtlsprobednegative_test_absence_guess_kept_for_facts_without_the_flag": ".test_absence_guess_kept_for_facts_without_the_flag()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L125 | neighbors=[TestTlsProbedNegative]
- "tests_test_router_signals_testtlsprobednegative_test_probed_and_failed_is_not_tls": ".test_probed_and_failed_is_not_tls()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L117 | neighbors=[TestTlsProbedNegative]
- "tests_test_router_signals_testtlsprobednegative_test_probed_and_succeeded_still_routes": ".test_probed_and_succeeded_still_routes()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L122 | neighbors=[TestTlsProbedNegative]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-301.json

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
