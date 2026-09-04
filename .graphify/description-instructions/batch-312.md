# Node Description Batch 313 of 330

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

- "tests_test_tls_integration_tlsserver_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L51 | neighbors=[_TLSServer] | lang=en
- "tests_test_tls_integration_tlsserver_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L63 | neighbors=[_TLSServer] | lang=en
- "tests_test_tls_legacy_versions_legacytlsserver_enter": ".__enter__()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L87 | neighbors=[_LegacyTLSServer] | lang=en
- "tests_test_tls_legacy_versions_legacytlsserver_exit": ".__exit__()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L91 | neighbors=[_LegacyTLSServer] | lang=en
- "tests_test_tls_legacy_versions_legacytlsserver_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L58 | neighbors=[_LegacyTLSServer] | lang=en
- "tests_test_tls_legacy_versions_legacytlsserver_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L73 | neighbors=[_LegacyTLSServer] | lang=en
- "tests_test_tls_legacy_versions_rationale_1": "test_tls_legacy_versions.py — the deprecated-TLS detection must measure the SERV" | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L1 | neighbors=[test_tls_legacy_versions.py] | lang=en
- "tests_test_tls_legacy_versions_rationale_126": "A version the probe cannot OFFER is 'not tested', not 'server refused'." | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L126 | neighbors=[test_try_version_reports_client_side_re…] | lang=en
- "tests_test_tls_legacy_versions_rationale_145": "When the probe genuinely cannot test a version, the result must say so     inste" | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L145 | neighbors=[test_untested_versions_are_surfaced_in_…] | lang=en
- "tests_test_tls_legacy_versions_rationale_56": "A loopback server pinned to exactly one (legacy) TLS version." | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L56 | neighbors=[_LegacyTLSServer] | lang=en
- "tests_test_tls_legacy_versions_rationale_98": "Skip rather than fail on a build with the legacy protocol compiled out." | kind=entity | source=probe/tests/test_tls_legacy_versions.py:L98 | neighbors=[_server_supports()] | lang=en
- "tests_test_tls_legacy_versions_test_try_version_reports_server_rejection_as_none": "test_try_version_reports_server_rejection_as_none()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L136 | neighbors=[test_tls_legacy_versions.py] | lang=en
- "tests_test_tls_port_coverage_rationale_1": "TLS branch coverage — the gap behind `tls_scan: invocations: 0`.  A real scan of" | kind=entity | source=probe/tests/test_tls_port_coverage.py:L1 | neighbors=[test_tls_port_coverage.py] | lang=en
- "tests_test_tls_port_coverage_rationale_39": "The drift that used to exist: spec allows a port the gate refuses." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L39 | neighbors=[.test_branch_spec_matches_the_gate()] | lang=en
- "tests_test_tls_port_coverage_rationale_67": "Excluded on purpose — a bare ClientHello is the WRONG packet here." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L67 | neighbors=[TestDeliberateExclusions] | lang=en
- "tests_test_tls_port_coverage_rationale_70": "3389 reaches TLS only after the X.224 rdpNegReq. rdp_scanner already         obs" | kind=entity | source=probe/tests/test_tls_port_coverage.py:L70 | neighbors=[.test_rdp_is_excluded()] | lang=en
- "tests_test_tls_port_coverage_rationale_77": "5986 is WinRM's TLS listener and IS included; these two are plaintext." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L77 | neighbors=[.test_winrm_plaintext_listeners_exclude…] | lang=en
- "tests_test_tls_port_coverage_rationale_83": "STARTTLS negotiates in-band; implicit TLS would fail." | kind=entity | source=probe/tests/test_tls_port_coverage.py:L83 | neighbors=[.test_starttls_upgrade_ports_excluded()] | lang=en
- "tests_test_tls_port_coverage_rationale_88": "Why widening is safe.      A port that does not speak TLS yields `status=\"error\"" | kind=entity | source=probe/tests/test_tls_port_coverage.py:L88 | neighbors=[test_refused_handshake_is_an_error_not_…] | lang=en
- "tests_test_tls_port_coverage_testsinglesourceoftruth_test_branch_port_table_reuses_it_too": ".test_branch_port_table_reuses_it_too()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L35 | neighbors=[TestSingleSourceOfTruth] | lang=en
- "tests_test_tls_port_coverage_testsinglesourceoftruth_test_gates_reuses_the_same_object": ".test_gates_reuses_the_same_object()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L32 | neighbors=[TestSingleSourceOfTruth] | lang=en
- "tests_test_tls_port_coverage_testwidenedcoverage_test_classic_implicit_tls_still_covered": ".test_classic_implicit_tls_still_covered()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L46 | neighbors=[TestWidenedCoverage] | lang=en
- "tests_test_tls_port_coverage_testwidenedcoverage_test_management_and_api_surfaces_now_covered": ".test_management_and_api_surfaces_now_covered()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L59 | neighbors=[TestWidenedCoverage] | lang=en
- "tests_test_tls_port_coverage_testwidenedcoverage_test_the_set_actually_grew": ".test_the_set_actually_grew()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L62 | neighbors=[TestWidenedCoverage] | lang=en
- "tests_test_tls_posture_rationale_1": "test_tls_posture.py — Tier 2.4: cipher-suite classification + TLS posture gradin" | kind=entity | source=probe/tests/test_tls_posture.py:L1 | neighbors=[test_tls_posture.py] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_3des_is_weak": ".test_3des_is_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L43 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_anonymous_is_weak": ".test_anonymous_is_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L55 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_chacha20_is_aead": ".test_chacha20_is_aead()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L60 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_export_and_md5_are_weak": ".test_export_and_md5_are_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L48 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_modern_aead_pfs": ".test_modern_aead_pfs()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L19 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_null_cipher_is_weak": ".test_null_cipher_is_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L38 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_rc4_is_weak": ".test_rc4_is_weak()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L33 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testclassifycipher_test_rsa_cbc_no_pfs": ".test_rsa_cbc_no_pfs()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L26 | neighbors=[TestClassifyCipher] | lang=en
- "tests_test_tls_posture_testgradetlsposture_test_empty_cipher_details_still_grades_protocols": ".test_empty_cipher_details_still_grades_protocols()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L104 | neighbors=[TestGradeTlsPosture] | lang=en
- "tests_test_tls_posture_testgradetlsposture_test_grade_c_no_forward_secrecy": ".test_grade_c_no_forward_secrecy()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L88 | neighbors=[TestGradeTlsPosture] | lang=en
- "tests_test_tls_posture_testgradetlsposture_test_grade_f_weak_cipher": ".test_grade_f_weak_cipher()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L99 | neighbors=[TestGradeTlsPosture] | lang=en
- "tests_test_transport_rationale_1": "Tests for agent/transport.py" | kind=entity | source=probe/tests/test_transport.py:L1 | neighbors=[test_transport.py] | lang=en
- "tests_test_transport_rationale_16": "Create a Transport with a real state file path but no actual HTTP calls." | kind=entity | source=probe/tests/test_transport.py:L16 | neighbors=[transport()] | lang=pt
- "tests_test_transport_rationale_18": "Create a Transport with a real state file path but no actual HTTP calls." | kind=entity | source=probe/tests/test_transport.py:L18 | neighbors=[transport()] | lang=pt
- "tests_test_transport_testdeviceenrollment_test_activation_persists_recoverable_device_credential": ".test_activation_persists_recoverable_device_credential()" | kind=code-symbol | source=probe/tests/test_transport.py:L172 | neighbors=[TestDeviceEnrollment] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-312.json

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
