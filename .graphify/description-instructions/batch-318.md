# Node Description Batch 319 of 336

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
- "tests_test_tls_port_coverage_rationale_70": "3389 reaches TLS only after the X.224 rdpNegReq. rdp_scanner already         obs" | kind=entity | source=probe/tests/test_tls_port_coverage.py:L70 | neighbors=[.test_rdp_is_excluded()]
- "tests_test_tls_port_coverage_rationale_77": "5986 is WinRM's TLS listener and IS included; these two are plaintext." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L77 | neighbors=[.test_winrm_plaintext_listeners_exclude…]
- "tests_test_tls_port_coverage_rationale_83": "STARTTLS negotiates in-band; implicit TLS would fail." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L83 | neighbors=[.test_starttls_upgrade_ports_excluded()]
- "tests_test_tls_port_coverage_rationale_88": "Why widening is safe.      A port that does not speak TLS yields `status=\"error\"" | kind=entity | source=probe/tests/test_tls_port_coverage.py:L88 | neighbors=[test_refused_handshake_is_an_error_not_…]
- "tests_test_tls_port_coverage_testsinglesourceoftruth_test_branch_port_table_reuses_it_too": ".test_branch_port_table_reuses_it_too()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L35 | neighbors=[TestSingleSourceOfTruth]
- "tests_test_tls_port_coverage_testsinglesourceoftruth_test_gates_reuses_the_same_object": ".test_gates_reuses_the_same_object()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L32 | neighbors=[TestSingleSourceOfTruth]
- "tests_test_tls_port_coverage_testwidenedcoverage_test_classic_implicit_tls_still_covered": ".test_classic_implicit_tls_still_covered()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L46 | neighbors=[TestWidenedCoverage]
- "tests_test_tls_port_coverage_testwidenedcoverage_test_management_and_api_surfaces_now_covered": ".test_management_and_api_surfaces_now_covered()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L59 | neighbors=[TestWidenedCoverage]
- "tests_test_tls_port_coverage_testwidenedcoverage_test_the_set_actually_grew": ".test_the_set_actually_grew()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L62 | neighbors=[TestWidenedCoverage]
- "tests_test_tls_posture_rationale_1": "test_tls_posture.py — Tier 2.4: cipher-suite classification + TLS posture gradin" | kind=entity | source=probe/tests/test_tls_posture.py:L1 | neighbors=[test_tls_posture.py]
- "tests_test_tls_posture_testclassifycipher_test_3des_is_weak": ".test_3des_is_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L43 | neighbors=[TestClassifyCipher]
- "tests_test_tls_posture_testclassifycipher_test_anonymous_is_weak": ".test_anonymous_is_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L55 | neighbors=[TestClassifyCipher]
- "tests_test_tls_posture_testclassifycipher_test_chacha20_is_aead": ".test_chacha20_is_aead()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L60 | neighbors=[TestClassifyCipher]
- "tests_test_tls_posture_testclassifycipher_test_export_and_md5_are_weak": ".test_export_and_md5_are_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L48 | neighbors=[TestClassifyCipher]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-318.json

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
