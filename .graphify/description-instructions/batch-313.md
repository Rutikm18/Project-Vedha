# Node Description Batch 314 of 332

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

- "tests_test_task_runner_testrunnerscopevalidation_test_manager_job_without_scope_fails_closed": ".test_manager_job_without_scope_fails_closed()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L354 | neighbors=[TestRunnerScopeValidation]
- "tests_test_task_runner_testrunnerscopevalidation_test_merge_engagement_and_job_excludes": ".test_merge_engagement_and_job_excludes()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L366 | neighbors=[TestRunnerScopeValidation]
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_excluded_target": ".test_rejects_excluded_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L303 | neighbors=[TestRunnerScopeValidation]
- "tests_test_task_runner_testrunnerscopevalidation_test_scope_fallback_preserves_manager_and_job_exclusions": ".test_scope_fallback_preserves_manager_and_job_exclusions()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L331 | neighbors=[TestRunnerScopeValidation]
- "tests_test_tier1_correlations_rationale_1": "test_tier1_correlations.py — enterprise attack-path correlations built from the" | kind=entity | source=probe/tests/test_tier1_correlations.py:L1 | neighbors=[test_tier1_correlations.py]
- "tests_test_tier1_wiring_gate_rationale_1": "test_tier1_wiring_gate.py — integration/accuracy gate for deep-scan capabilities" | kind=entity | source=probe/tests/test_tier1_wiring_gate.py:L1 | neighbors=[test_tier1_wiring_gate.py]
- "tests_test_tier1_wiring_gate_test_every_it_branch_has_port_table_entry": "test_every_it_branch_has_port_table_entry()" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L39 | neighbors=[test_tier1_wiring_gate.py]
- "tests_test_tier1_wiring_gate_test_new_tier1_branches_present": "test_new_tier1_branches_present()" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L60 | neighbors=[test_tier1_wiring_gate.py]
- "tests_test_tier1_wiring_gate_test_udp_hostwide_branches_have_merge_handlers": "test_udp_hostwide_branches_have_merge_handlers()" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L55 | neighbors=[test_tier1_wiring_gate.py]
- "tests_test_tls_fingerprint_rationale_1": "test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology)." | kind=entity | source=probe/tests/test_tls_fingerprint.py:L1 | neighbors=[test_tls_fingerprint.py]
- "tests_test_tls_fingerprint_testclienthello_test_contains_client_hello_handshake_type": ".test_contains_client_hello_handshake_type()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L28 | neighbors=[TestClientHello]
- "tests_test_tls_fingerprint_testclienthello_test_contains_sni_hostname": ".test_contains_sni_hostname()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L33 | neighbors=[TestClientHello]
- "tests_test_tls_fingerprint_testclienthello_test_declared_lengths_are_consistent": ".test_declared_lengths_are_consistent()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L37 | neighbors=[TestClientHello]
- "tests_test_tls_fingerprint_testclienthello_test_is_tls_handshake_record": ".test_is_tls_handshake_record()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L23 | neighbors=[TestClientHello]
- "tests_test_tls_fingerprint_testdigest_test_cipher_code_known_and_unknown": ".test_cipher_code_known_and_unknown()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L90 | neighbors=[TestDigest]
- "tests_test_tls_fingerprint_testdigest_test_digest_differs_with_cipher": ".test_digest_differs_with_cipher()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L109 | neighbors=[TestDigest]
- "tests_test_tls_fingerprint_testdigest_test_digest_is_62_chars": ".test_digest_is_62_chars()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L99 | neighbors=[TestDigest]
- "tests_test_tls_fingerprint_testdigest_test_digest_is_deterministic": ".test_digest_is_deterministic()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L104 | neighbors=[TestDigest]
- "tests_test_tls_fingerprint_testdigest_test_version_code": ".test_version_code()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L84 | neighbors=[TestDigest]
- "tests_test_tls_fingerprint_testdigest_test_zero_hash_when_no_responses": ".test_zero_hash_when_no_responses()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L95 | neighbors=[TestDigest]
- "tests_test_tls_fingerprint_testparseserverhello_test_returns_none_on_alert": ".test_returns_none_on_alert()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L72 | neighbors=[TestParseServerHello]
- "tests_test_tls_fingerprint_testparseserverhello_test_returns_none_on_short": ".test_returns_none_on_short()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L77 | neighbors=[TestParseServerHello]
- "tests_test_tls_integration_rationale_1": "test_tls_integration.py — Tier 2.4 live check: run the real TLSScanner against a" | kind=entity | source=probe/tests/test_tls_integration.py:L1 | neighbors=[test_tls_integration.py]
- "tests_test_tls_integration_tlsserver_enter": ".__enter__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L77 | neighbors=[_TLSServer]
- "tests_test_tls_integration_tlsserver_exit": ".__exit__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L81 | neighbors=[_TLSServer]
- "tests_test_tls_integration_tlsserver_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L51 | neighbors=[_TLSServer]
- "tests_test_tls_integration_tlsserver_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L63 | neighbors=[_TLSServer]
- "tests_test_tls_legacy_versions_legacytlsserver_enter": ".__enter__()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L87 | neighbors=[_LegacyTLSServer]
- "tests_test_tls_legacy_versions_legacytlsserver_exit": ".__exit__()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L91 | neighbors=[_LegacyTLSServer]
- "tests_test_tls_legacy_versions_legacytlsserver_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L58 | neighbors=[_LegacyTLSServer]
- "tests_test_tls_legacy_versions_legacytlsserver_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L73 | neighbors=[_LegacyTLSServer]
- "tests_test_tls_legacy_versions_rationale_1": "test_tls_legacy_versions.py — the deprecated-TLS detection must measure the SERV" | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L1 | neighbors=[test_tls_legacy_versions.py]
- "tests_test_tls_legacy_versions_rationale_126": "A version the probe cannot OFFER is 'not tested', not 'server refused'." | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L126 | neighbors=[test_try_version_reports_client_side_re…]
- "tests_test_tls_legacy_versions_rationale_145": "When the probe genuinely cannot test a version, the result must say so     inste" | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L145 | neighbors=[test_untested_versions_are_surfaced_in_…]
- "tests_test_tls_legacy_versions_rationale_56": "A loopback server pinned to exactly one (legacy) TLS version." | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L56 | neighbors=[_LegacyTLSServer]
- "tests_test_tls_legacy_versions_rationale_98": "Skip rather than fail on a build with the legacy protocol compiled out." | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L98 | neighbors=[_server_supports()]
- "tests_test_tls_legacy_versions_test_try_version_reports_server_rejection_as_none": "test_try_version_reports_server_rejection_as_none()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L136 | neighbors=[test_tls_legacy_versions.py]
- "tests_test_tls_port_coverage_rationale_1": "TLS branch coverage — the gap behind `tls_scan: invocations: 0`.  A real scan of" | kind=entity | source=probe/tests/test_tls_port_coverage.py:L1 | neighbors=[test_tls_port_coverage.py]
- "tests_test_tls_port_coverage_rationale_39": "The drift that used to exist: spec allows a port the gate refuses." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L39 | neighbors=[.test_branch_spec_matches_the_gate()]
- "tests_test_tls_port_coverage_rationale_67": "Excluded on purpose — a bare ClientHello is the WRONG packet here." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L67 | neighbors=[TestDeliberateExclusions]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-313.json

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
