# Node Description Batch 202 of 236

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

- "tests_test_host_discovery_mobile_testdevicehint_test_iphone_lockdownd_port": ".test_iphone_lockdownd_port()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L53 | neighbors=[TestDeviceHint]
- "tests_test_host_discovery_mobile_testdevicehint_test_mobile_vendor": ".test_mobile_vendor()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L59 | neighbors=[TestDeviceHint]
- "tests_test_host_discovery_mobile_testdevicehint_test_no_signal": ".test_no_signal()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L65 | neighbors=[TestDeviceHint]
- "tests_test_host_discovery_mobile_testdevicehint_test_plain_vendor_passthrough": ".test_plain_vendor_passthrough()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L62 | neighbors=[TestDeviceHint]
- "tests_test_host_discovery_mobile_testdevicehint_test_randomized_mac_is_mobile": ".test_randomized_mac_is_mobile()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L56 | neighbors=[TestDeviceHint]
- "tests_test_host_discovery_mobile_testlocallyadministered_test_globally_unique_macs": ".test_globally_unique_macs()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L39 | neighbors=[TestLocallyAdministered]
- "tests_test_host_discovery_mobile_testlocallyadministered_test_randomized_phone_macs": ".test_randomized_phone_macs()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L33 | neighbors=[TestLocallyAdministered]
- "tests_test_host_discovery_mobile_testnormalizemac_test_extracts_from_arp_line": ".test_extracts_from_arp_line()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L17 | neighbors=[TestNormalizeMac]
- "tests_test_host_discovery_mobile_testnormalizemac_test_lowercases": ".test_lowercases()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L14 | neighbors=[TestNormalizeMac]
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_broadcast": ".test_rejects_broadcast()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L21 | neighbors=[TestNormalizeMac]
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_garbage": ".test_rejects_garbage()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L27 | neighbors=[TestNormalizeMac]
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_multicast": ".test_rejects_multicast()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L24 | neighbors=[TestNormalizeMac]
- "tests_test_host_discovery_mobile_testnormalizemac_test_zero_pads_octets": ".test_zero_pads_octets()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L10 | neighbors=[TestNormalizeMac]
- "tests_test_host_discovery_mobile_testvendorlookup_test_known_oui": ".test_known_oui()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L45 | neighbors=[TestVendorLookup]
- "tests_test_host_discovery_mobile_testvendorlookup_test_unknown_oui": ".test_unknown_oui()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L48 | neighbors=[TestVendorLookup]
- "tests_test_http_lease_test_engine_cancellation_stops_async_scan_work": "test_engine_cancellation_stops_async_scan_work()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L94 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_poll_auth_failure_is_not_hidden": "test_poll_auth_failure_is_not_hidden()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L28 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_polled_job_renews_lease_until_runner_finishes": "test_polled_job_renews_lease_until_runner_finishes()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L37 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_repeated_lease_rejection_cancels_running_attempt": "test_repeated_lease_rejection_cancels_running_attempt()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L69 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_transient_poll_failure_propagates_to_loop_handler": "test_transient_poll_failure_propagates_to_loop_handler()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L15 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_transient_poll_failure_returns_no_jobs": "test_transient_poll_failure_returns_no_jobs()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L15 | neighbors=[test_http_lease.py]
- "tests_test_hw_bind_rationale_1": "Tests for agent/hw_bind.py" | kind=entity | source=probe/tests/test_hw_bind.py:L1 | neighbors=[test_hw_bind.py]
- "tests_test_hw_bind_testcheckhwbind_test_passes_when_match": ".test_passes_when_match()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L22 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_raises_on_mismatch": ".test_raises_on_mismatch()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L28 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_raises_when_unset_and_enforced": ".test_raises_when_unset_and_enforced()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L39 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_skips_when_unset_and_dev_mode": ".test_skips_when_unset_and_dev_mode()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L34 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testgethwid_test_deterministic_within_session": ".test_deterministic_within_session()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L17 | neighbors=[TestGetHwId]
- "tests_test_hw_bind_testgethwid_test_returns_32_hex_chars": ".test_returns_32_hex_chars()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L12 | neighbors=[TestGetHwId]
- "tests_test_installer_contract_test_installer_rejects_missing_or_unknown_arguments": "test_installer_rejects_missing_or_unknown_arguments()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L31 | neighbors=[test_installer_contract.py]
- "tests_test_installer_contract_test_installer_requires_only_manager_endpoint_in_dry_run": "test_installer_requires_only_manager_endpoint_in_dry_run()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L11 | neighbors=[test_installer_contract.py]
- "tests_test_installer_contract_test_installer_source_has_no_human_or_job_credentials": "test_installer_source_has_no_human_or_job_credentials()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L49 | neighbors=[test_installer_contract.py]
- "tests_test_integration_rationale_1": "Integration tests — full probe lifecycles exercised through the public APIs of a" | kind=entity | source=probe/tests/test_integration.py:L1 | neighbors=[test_integration.py]
- "tests_test_integration_rationale_101": "Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it." | kind=entity | source=probe/tests/test_integration.py:L101 | neighbors=[TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_rationale_104": "Job carries encrypted_scope → TaskRunner decrypts → uses it." | kind=entity | source=probe/tests/test_integration.py:L104 | neighbors=[.test_decrypts_encrypted_scope_from_job…]
- "tests_test_integration_rationale_136": "Wrong key → decryption fails → graceful fallback to params scope." | kind=entity | source=probe/tests/test_integration.py:L136 | neighbors=[.test_falls_back_when_decryption_fails()]
- "tests_test_integration_rationale_166": "Phase 1: combined scope validation (validate + excludes)." | kind=entity | source=probe/tests/test_integration.py:L166 | neighbors=[TestScopeValidationPipeline]
- "tests_test_integration_rationale_198": "Phase 1: result spool with upload retry." | kind=entity | source=probe/tests/test_integration.py:L198 | neighbors=[TestResultSpoolWithRetry]
- "tests_test_integration_rationale_239": "Phase 4 + Phase 1: Transport sends public_key during registration." | kind=entity | source=probe/tests/test_integration.py:L239 | neighbors=[TestTransportWithIdentity]
- "tests_test_integration_rationale_260": "Backward compat: registration without public_key is fine." | kind=entity | source=probe/tests/test_integration.py:L260 | neighbors=[.test_register_without_public_key()]
- "tests_test_integration_rationale_274": "Phase 2: WebSocket message parsing." | kind=entity | source=probe/tests/test_integration.py:L274 | neighbors=[TestWebSocketMessageProtocol]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-201.json

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
