# Node Description Batch 222 of 236

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

- "tests_test_tls_fingerprint_testdigest_test_version_code": ".test_version_code()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L84 | neighbors=[TestDigest] | lang=en
- "tests_test_tls_fingerprint_testdigest_test_zero_hash_when_no_responses": ".test_zero_hash_when_no_responses()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L95 | neighbors=[TestDigest] | lang=en
- "tests_test_tls_fingerprint_testparseserverhello_test_returns_none_on_alert": ".test_returns_none_on_alert()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L72 | neighbors=[TestParseServerHello] | lang=en
- "tests_test_tls_fingerprint_testparseserverhello_test_returns_none_on_short": ".test_returns_none_on_short()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L77 | neighbors=[TestParseServerHello] | lang=en
- "tests_test_tls_integration_rationale_1": "test_tls_integration.py — Tier 2.4 live check: run the real TLSScanner against a" | kind=entity | source=probe/tests/test_tls_integration.py:L1 | neighbors=[test_tls_integration.py] | lang=en
- "tests_test_tls_integration_tlsserver_enter": ".__enter__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L77 | neighbors=[_TLSServer] | lang=en
- "tests_test_tls_integration_tlsserver_exit": ".__exit__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L81 | neighbors=[_TLSServer] | lang=en
- "tests_test_tls_integration_tlsserver_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L51 | neighbors=[_TLSServer] | lang=en
- "tests_test_tls_integration_tlsserver_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L63 | neighbors=[_TLSServer] | lang=en
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
- "tests_test_transport_testdeviceenrollment_test_create_enrollment_request_409_raises_already_enrolled": ".test_create_enrollment_request_409_raises_already_enrolled()" | kind=code-symbol | source=probe/tests/test_transport.py:L230 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_create_enrollment_request_409_without_detail_has_default_message": ".test_create_enrollment_request_409_without_detail_has_default_message()" | kind=code-symbol | source=probe/tests/test_transport.py:L244 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_create_enrollment_request_forwards_enroll_token": ".test_create_enrollment_request_forwards_enroll_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L210 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_device_refresh_signs_unique_nonce_and_rotates_access_token": ".test_device_refresh_signs_unique_nonce_and_rotates_access_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L263 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_legacy_token_is_not_forced_through_device_refresh": ".test_legacy_token_is_not_forced_through_device_refresh()" | kind=code-symbol | source=probe/tests/test_transport.py:L253 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testfetchscope_test_http_error_returns_none": ".test_http_error_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L416 | neighbors=[TestFetchScope] | lang=en
- "tests_test_transport_testfetchscope_test_returns_scope": ".test_returns_scope()" | kind=code-symbol | source=probe/tests/test_transport.py:L406 | neighbors=[TestFetchScope] | lang=en
- "tests_test_transport_testheartbeat_test_heartbeat_401_returns_false": ".test_heartbeat_401_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L349 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testheartbeat_test_heartbeat_sends_current_job": ".test_heartbeat_sends_current_job()" | kind=code-symbol | source=probe/tests/test_transport.py:L358 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testheartbeat_test_successful_heartbeat": ".test_successful_heartbeat()" | kind=code-symbol | source=probe/tests/test_transport.py:L340 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testhttpget_test_exception_returns_none": ".test_exception_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L521 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testhttpget_test_non_200_returns_none": ".test_non_200_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L512 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testhttpget_test_successful_get": ".test_successful_get()" | kind=code-symbol | source=probe/tests/test_transport.py:L502 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testidentity_test_agent_state_updates_preserve_scope_identity": ".test_agent_state_updates_preserve_scope_identity()" | kind=code-symbol | source=probe/tests/test_transport.py:L70 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_auth_header": ".test_auth_header()" | kind=code-symbol | source=probe/tests/test_transport.py:L38 | neighbors=[TestIdentity] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-221.json

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
