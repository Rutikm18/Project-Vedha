# Node Description Batch 94 of 104

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

- "tests_test_exploit_engine_testvalidatescope_test_ip_in_scope_passes": ".test_ip_in_scope_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L130 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_ip_out_of_scope_fails": ".test_ip_out_of_scope_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L133 | neighbors=[TestValidateScope] | lang=en
- "tests_test_exploit_engine_testvalidatescope_test_multiple_scope_cidrs": ".test_multiple_scope_cidrs()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L141 | neighbors=[TestValidateScope] | lang=en
- "tests_test_hw_bind_rationale_1": "Tests for agent/hw_bind.py" | kind=entity | source=probe/tests/test_hw_bind.py:L1 | neighbors=[test_hw_bind.py] | lang=en
- "tests_test_hw_bind_testcheckhwbind_test_passes_when_match": ".test_passes_when_match()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L22 | neighbors=[TestCheckHwBind] | lang=en
- "tests_test_hw_bind_testcheckhwbind_test_raises_on_mismatch": ".test_raises_on_mismatch()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L28 | neighbors=[TestCheckHwBind] | lang=en
- "tests_test_hw_bind_testcheckhwbind_test_raises_when_unset_and_enforced": ".test_raises_when_unset_and_enforced()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L39 | neighbors=[TestCheckHwBind] | lang=en
- "tests_test_hw_bind_testcheckhwbind_test_skips_when_unset_and_dev_mode": ".test_skips_when_unset_and_dev_mode()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L34 | neighbors=[TestCheckHwBind] | lang=en
- "tests_test_hw_bind_testgethwid_test_deterministic_within_session": ".test_deterministic_within_session()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L17 | neighbors=[TestGetHwId] | lang=en
- "tests_test_hw_bind_testgethwid_test_returns_32_hex_chars": ".test_returns_32_hex_chars()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L12 | neighbors=[TestGetHwId] | lang=en
- "tests_test_integration_rationale_1": "Integration tests — full probe lifecycles exercised through the public APIs of a" | kind=entity | source=probe/tests/test_integration.py:L1 | neighbors=[test_integration.py] | lang=en
- "tests_test_integration_rationale_101": "Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it." | kind=entity | source=probe/tests/test_integration.py:L101 | neighbors=[TestTaskRunnerWithEncryptedScope] | lang=en
- "tests_test_integration_rationale_104": "Job carries encrypted_scope → TaskRunner decrypts → uses it." | kind=entity | source=probe/tests/test_integration.py:L104 | neighbors=[.test_decrypts_encrypted_scope_from_job…] | lang=en
- "tests_test_integration_rationale_136": "Wrong key → decryption fails → graceful fallback to params scope." | kind=entity | source=probe/tests/test_integration.py:L136 | neighbors=[.test_falls_back_when_decryption_fails()] | lang=en
- "tests_test_integration_rationale_166": "Phase 1: combined scope validation (validate + excludes)." | kind=entity | source=probe/tests/test_integration.py:L166 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_rationale_198": "Phase 1: result spool with upload retry." | kind=entity | source=probe/tests/test_integration.py:L198 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_rationale_239": "Phase 4 + Phase 1: Transport sends public_key during registration." | kind=entity | source=probe/tests/test_integration.py:L239 | neighbors=[TestTransportWithIdentity] | lang=en
- "tests_test_integration_rationale_260": "Backward compat: registration without public_key is fine." | kind=entity | source=probe/tests/test_integration.py:L260 | neighbors=[.test_register_without_public_key()] | lang=en
- "tests_test_integration_rationale_274": "Phase 2: WebSocket message parsing." | kind=entity | source=probe/tests/test_integration.py:L274 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_rationale_312": "End-to-end: identity → register → job → decrypt → validate → scan → submit." | kind=entity | source=probe/tests/test_integration.py:L312 | neighbors=[TestFullJobLifecycle] | lang=en
- "tests_test_integration_rationale_315": "Simulate the full probe lifecycle from identity to result submission." | kind=entity | source=probe/tests/test_integration.py:L315 | neighbors=[.test_complete_flow_with_encrypted_scop…] | lang=en
- "tests_test_integration_rationale_383": "All targets outside scope → job is rejected cleanly." | kind=entity | source=probe/tests/test_integration.py:L383 | neighbors=[.test_job_rejected_all_targets_out_of_s…] | lang=en
- "tests_test_integration_rationale_409": "OT passive profile resolves correctly." | kind=entity | source=probe/tests/test_integration.py:L409 | neighbors=[.test_job_ot_passive_profile()] | lang=en
- "tests_test_integration_rationale_42": "Return a minimal valid scan result (no real network I/O)." | kind=entity | source=probe/tests/test_integration.py:L42 | neighbors=[_fake_run_scan()] | lang=pt
- "tests_test_integration_rationale_432": "Phase 5: startup gauntlet checks." | kind=entity | source=probe/tests/test_integration.py:L432 | neighbors=[TestStartupGauntlet] | lang=en
- "tests_test_integration_rationale_435": "With LICENSE_ENFORCED=false, gauntlet returns None." | kind=entity | source=probe/tests/test_integration.py:L435 | neighbors=[.test_gauntlet_skips_in_dev_mode()] | lang=en
- "tests_test_integration_rationale_443": "Wrong HW fingerprint blocks startup." | kind=entity | source=probe/tests/test_integration.py:L443 | neighbors=[.test_gauntlet_hw_bind_blocks()] | lang=en
- "tests_test_integration_rationale_65": "Phase 4: identity generation + scope encryption roundtrip." | kind=entity | source=probe/tests/test_integration.py:L65 | neighbors=[TestIdentityAndEncryption] | lang=en
- "tests_test_integration_rationale_68": "Generate identity → encrypt scope → decrypt scope." | kind=entity | source=probe/tests/test_integration.py:L68 | neighbors=[.test_full_identity_lifecycle()] | lang=en
- "tests_test_integration_rationale_79": "Manager encrypts → probe decrypts." | kind=entity | source=probe/tests/test_integration.py:L79 | neighbors=[.test_scope_encryption_roundtrip()] | lang=en
- "tests_test_integration_rationale_92": "A different probe cannot decrypt scope meant for another probe." | kind=entity | source=probe/tests/test_integration.py:L92 | neighbors=[.test_different_key_cannot_decrypt()] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_spool_persists_and_flushes": ".test_spool_persists_and_flushes()" | kind=code-symbol | source=probe/tests/test_integration.py:L200 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_submit_exhausts_retries": ".test_submit_exhausts_retries()" | kind=code-symbol | source=probe/tests/test_integration.py:L227 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_submit_retries_on_failure": ".test_submit_retries_on_failure()" | kind=code-symbol | source=probe/tests/test_integration.py:L216 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_accepts_in_scope_rejects_out_of_scope": ".test_accepts_in_scope_rejects_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L168 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_all_excluded_returns_empty": ".test_all_excluded_returns_empty()" | kind=code-symbol | source=probe/tests/test_integration.py:L190 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_excludes_override_scope": ".test_excludes_override_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L174 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_merge_exclusions_deduplicates": ".test_merge_exclusions_deduplicates()" | kind=code-symbol | source=probe/tests/test_integration.py:L184 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testtransportwithidentity_test_register_sends_public_key": ".test_register_sends_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L241 | neighbors=[TestTransportWithIdentity] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_heartbeat_message": ".test_heartbeat_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L306 | neighbors=[TestWebSocketMessageProtocol] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-093.json

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
