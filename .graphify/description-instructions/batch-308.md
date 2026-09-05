# Node Description Batch 309 of 336

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

- "tests_test_router_signals_teststructuredservice_test_http_by_service_field": ".test_http_by_service_field()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L43 | neighbors=[TestStructuredService]
- "tests_test_router_signals_teststructuredservice_test_ssh_by_service_field": ".test_ssh_by_service_field()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L48 | neighbors=[TestStructuredService]
- "tests_test_router_signals_testtlsprobednegative_test_absence_guess_kept_for_facts_without_the_flag": ".test_absence_guess_kept_for_facts_without_the_flag()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L125 | neighbors=[TestTlsProbedNegative]
- "tests_test_router_signals_testtlsprobednegative_test_probed_and_failed_is_not_tls": ".test_probed_and_failed_is_not_tls()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L117 | neighbors=[TestTlsProbedNegative]
- "tests_test_router_signals_testtlsprobednegative_test_probed_and_succeeded_still_routes": ".test_probed_and_succeeded_still_routes()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L122 | neighbors=[TestTlsProbedNegative]
- "tests_test_router_signals_testwebschemes_test_observed_tls_prefers_https": ".test_observed_tls_prefers_https()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L60 | neighbors=[TestWebSchemes]
- "tests_test_router_signals_testwebschemes_test_static_table_still_applies": ".test_static_table_still_applies()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L65 | neighbors=[TestWebSchemes]
- "tests_test_rsync_scanner_fakesock_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L38 | neighbors=[_FakeSock]
- "tests_test_rsync_scanner_fakesock_recv": ".recv()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L42 | neighbors=[_FakeSock]
- "tests_test_rsync_scanner_fakesock_sendall": ".sendall()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L46 | neighbors=[_FakeSock]
- "tests_test_rsync_scanner_rationale_1": "test_rsync_scanner.py — rsync daemon anonymous-module exposure.  Pure protocol p" | kind=entity | source=probe/tests/test_rsync_scanner.py:L1 | neighbors=[test_rsync_scanner.py]
- "tests_test_rsync_scanner_rationale_35": "Minimal socket stand-in: replays the daemon greeting, records what the     scann" | kind=entity | source=probe/tests/test_rsync_scanner.py:L35 | neighbors=[_FakeSock]
- "tests_test_rsync_scanner_rationale_51": "Protocol >= 32 daemons append their digest-name list to the greeting and     rej" | kind=entity | source=probe/tests/test_rsync_scanner.py:L51 | neighbors=[TestHandshake]
- "tests_test_rsync_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L121 | neighbors=[TestParity]
- "tests_test_rsync_scanner_testparsemodules_test_bounded": ".test_bounded()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L29 | neighbors=[TestParseModules]
- "tests_test_rsync_scanner_testparsemodules_test_protocol_lines_ignored": ".test_protocol_lines_ignored()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L25 | neighbors=[TestParseModules]
- "tests_test_rsync_scanner_testparsemodules_test_tab_and_space_separated": ".test_tab_and_space_separated()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L19 | neighbors=[TestParseModules]
- "tests_test_run_all_reconcile_rationale_1": "test_run_all_reconcile.py — cross-cutting: run_all and scan_funnel must derive t" | kind=entity | source=probe/tests/test_run_all_reconcile.py:L1 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_all_reconcile_test_advertised_dynamic_ports_extraction": "test_advertised_dynamic_ports_extraction()" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L34 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_all_reconcile_test_open_tcp_ports_ignores_non_open_and_udp": "test_open_tcp_ports_ignores_non_open_and_udp()" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L57 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_all_reconcile_test_reconcile_folds_in_only_reachable_dynamic_ports": "test_reconcile_folds_in_only_reachable_dynamic_ports()" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L51 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_all_reconcile_test_reconcile_matches_between_pipelines_when_epm_unreachable": "test_reconcile_matches_between_pipelines_when_epm_unreachable()" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L41 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_all_reconcile_test_run_all_imports_the_shared_reconciler_not_a_copy": "test_run_all_imports_the_shared_reconciler_not_a_copy()" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L26 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_all_reconcile_test_run_all_runs_rdp_scanner_stage": "test_run_all_runs_rdp_scanner_stage()" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L18 | neighbors=[test_run_all_reconcile.py]
- "tests_test_run_scoped_fact_scope_rationale_1": "Run-scoped facts must not be scope-checked as if they were hosts.  THE BUG THIS" | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L1 | neighbors=[test_run_scoped_fact_scope.py]
- "tests_test_run_scoped_fact_scope_rationale_103": "Authorization is IP/CIDR-only; a hostname must not pass." | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L103 | neighbors=[.test_hostname_target_is_still_refused()]
- "tests_test_run_scoped_fact_scope_rationale_112": "The pre-existing <nmap-run> exemption this fix is modelled on." | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L112 | neighbors=[.test_scanner_control_record_exemption_…]
- "tests_test_run_scoped_fact_scope_rationale_45": "The exact payload that caused the 422." | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L45 | neighbors=[.test_ipv6_discovery_auto_target_is_not…]
- "tests_test_run_scoped_fact_scope_rationale_50": "Same record, but an interface actually resolved — still not a host." | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L50 | neighbors=[.test_ipv6_discovery_interface_name_is_…]
- "tests_test_run_scoped_fact_scope_rationale_59": "The damage was collateral: one non-host descriptor discarded every         legit" | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L59 | neighbors=[.test_a_real_result_with_one_run_scoped…]
- "tests_test_run_scoped_fact_scope_rationale_73": "The exemption must be narrow. These are the security assertions." | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L73 | neighbors=[TestTheScopeGateStillWorks]
- "tests_test_run_scoped_fact_scope_rationale_89": "Only the documented run-scoped scanners are exempt — a scanner name         the" | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L89 | neighbors=[.test_an_unknown_scanner_gets_no_exempt…]
- "tests_test_run_scoped_fact_scope_rationale_95": "The exemption skips the record entirely rather than trusting its         target," | kind=entity | source=manager/backend/tests/test_run_scoped_fact_scope.py:L95 | neighbors=[.test_run_scoped_name_does_not_launder_…]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_out_of_scope_finding_is_still_rejected": ".test_out_of_scope_finding_is_still_rejected()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L84 | neighbors=[TestTheScopeGateStillWorks]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_out_of_scope_host_row_is_still_rejected": ".test_out_of_scope_host_row_is_still_rejected()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L80 | neighbors=[TestTheScopeGateStillWorks]
- "tests_test_runtime_requirements_coverage_rationale_1": "test_runtime_requirements_coverage.py — the probe IMAGE must be able to run ever" | kind=entity | source=probe/tests/test_runtime_requirements_coverage.py:L1 | neighbors=[test_runtime_requirements_coverage.py]
- "tests_test_runtime_requirements_coverage_rationale_43": "Package names declared in a requirements file, normalised and lowercased." | kind=entity | source=probe/tests/test_runtime_requirements_coverage.py:L43 | neighbors=[_declared()]
- "tests_test_runtime_requirements_coverage_rationale_67": "A package shipped in the image but absent from requirements.txt is a     depende" | kind=entity | source=probe/tests/test_runtime_requirements_coverage.py:L67 | neighbors=[test_runtime_is_a_subset_of_the_develop…]
- "tests_test_runtime_topology_rationale_1": "Product-boundary tests for the single-dashboard Manager API." | kind=entity | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[test_runtime_topology.py]
- "tests_test_runtime_topology_test_manager_does_not_mount_a_static_dashboard": "test_manager_does_not_mount_a_static_dashboard()" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L6 | neighbors=[test_runtime_topology.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-308.json

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
