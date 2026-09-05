# Node Description Batch 155 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_integration_testfulljoblifecycle_test_job_ot_passive_profile": ".test_job_ot_passive_profile()" | kind=code-symbol | source=probe/tests/test_integration.py:L408 | neighbors=[OT passive profile resolves correctly., TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_rejected_all_targets_out_of_scope": ".test_job_rejected_all_targets_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L382 | neighbors=[All targets outside scope → job is reje…, TestFullJobLifecycle]
- "tests_test_integration_testidentityandencryption_test_different_key_cannot_decrypt": ".test_different_key_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_integration.py:L91 | neighbors=[A different probe cannot decrypt scope …, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_full_identity_lifecycle": ".test_full_identity_lifecycle()" | kind=code-symbol | source=probe/tests/test_integration.py:L67 | neighbors=[Generate identity → encrypt scope → dec…, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_scope_encryption_roundtrip": ".test_scope_encryption_roundtrip()" | kind=code-symbol | source=probe/tests/test_integration.py:L78 | neighbors=[Manager encrypts → probe decrypts., TestIdentityAndEncryption]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_hw_bind_blocks": ".test_gauntlet_hw_bind_blocks()" | kind=code-symbol | source=probe/tests/test_integration.py:L442 | neighbors=[Wrong HW fingerprint blocks startup., TestStartupGauntlet]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_skips_in_dev_mode": ".test_gauntlet_skips_in_dev_mode()" | kind=code-symbol | source=probe/tests/test_integration.py:L434 | neighbors=[With LICENSE_ENFORCED=false, gauntlet r…, TestStartupGauntlet]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_decrypts_encrypted_scope_from_job": ".test_decrypts_encrypted_scope_from_job()" | kind=code-symbol | source=probe/tests/test_integration.py:L103 | neighbors=[Job carries encrypted_scope → TaskRunne…, TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_falls_back_when_decryption_fails": ".test_falls_back_when_decryption_fails()" | kind=code-symbol | source=probe/tests/test_integration.py:L135 | neighbors=[Wrong key → decryption fails → graceful…, TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_testtransportwithidentity_test_register_without_public_key": ".test_register_without_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L259 | neighbors=[Backward compat: registration without p…, TestTransportWithIdentity]
- "tests_test_integrations_testlistintegrations": "TestListIntegrations" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L63 | neighbors=[test_integrations.py, .test_list_masks_secret()]
- "tests_test_integrations_testlistintegrations_test_list_masks_secret": ".test_list_masks_secret()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L64 | neighbors=[TestListIntegrations, _operator()]
- "tests_test_ipmi_scanner_testipmifindings_test_cipher_zero_is_critical": ".test_cipher_zero_is_critical()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L67 | neighbors=[TestIPMIFindings, ._fact()]
- "tests_test_ipmi_scanner_testipmifindings_test_reachable_bmc_is_low": ".test_reachable_bmc_is_low()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L71 | neighbors=[TestIPMIFindings, ._fact()]
- "tests_test_ipmi_scanner_testipmiscanner_test_cipher_zero_open": ".test_cipher_zero_open()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L49 | neighbors=[TestIPMIScanner, ._sc()]
- "tests_test_ipmi_scanner_testipmiscanner_test_no_ipmi_filtered": ".test_no_ipmi_filtered()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L56 | neighbors=[TestIPMIScanner, ._sc()]
- "tests_test_ipmi_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L76 | neighbors=[test_ipmi_scanner.py, .test_main_scripts()]
- "tests_test_ipmi_scanner_testwireformat_test_parse_nonzero_status_is_safe": ".test_parse_nonzero_status_is_safe()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L35 | neighbors=[TestWireFormat, _resp()]
- "tests_test_ipmi_scanner_testwireformat_test_parse_status_zero_is_cipher_zero": ".test_parse_status_zero_is_cipher_zero()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L31 | neighbors=[TestWireFormat, _resp()]
- "tests_test_ipv6_discovery_testdiscoverfiltering_test_dedups": ".test_dedups()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L64 | neighbors=[TestDiscoverFiltering, ._patch()]
- "tests_test_ipv6_discovery_testdiscoverfiltering_test_excludes_own_addresses": ".test_excludes_own_addresses()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L56 | neighbors=[TestDiscoverFiltering, ._patch()]
- "tests_test_ipv6_discovery_testdiscoverfiltering_test_keeps_usable_drops_dead_states": ".test_keeps_usable_drops_dead_states()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L44 | neighbors=[TestDiscoverFiltering, ._patch()]
- "tests_test_ipv6_discovery_testdiscoverfiltering_test_link_local_can_be_excluded": ".test_link_local_can_be_excluded()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L69 | neighbors=[TestDiscoverFiltering, ._patch()]
- "tests_test_ipv6_discovery_testdiscoverfiltering_test_never_raises_on_empty": ".test_never_raises_on_empty()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L75 | neighbors=[TestDiscoverFiltering, ._patch()]
- "tests_test_job_cancel_probe_testheartbeatoutcomes_test_other_rejections_are_plain_failures": ".test_other_rejections_are_plain_failures()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L53 | neighbors=[These may be transient/refreshable, so …, TestHeartbeatOutcomes]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_test_probe_debug_restores_full_tracing": ".test_probe_debug_restores_full_tracing()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L103 | neighbors=[TestPollingNoiseIsSuppressed, ._configure()]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_test_probe_own_narration_is_unaffected_at_info": ".test_probe_own_narration_is_unaffected_at_info()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L107 | neighbors=[TestPollingNoiseIsSuppressed, ._configure()]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_test_transport_loggers_are_quiet_by_default": ".test_transport_loggers_are_quiet_by_default()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L87 | neighbors=[TestPollingNoiseIsSuppressed, ._configure()]
- "tests_test_job_cancel_test_cancelled_is_distinct_from_failed": "test_cancelled_is_distinct_from_failed()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L175 | neighbors=[test_job_cancel.py, An operator stop must never be mistaken…]
- "tests_test_job_cancel_test_current_user_has_no_email_field": "test_current_user_has_no_email_field()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L224 | neighbors=[test_job_cancel.py, Pins the reason this endpoint may not r…]
- "tests_test_loaders_testloadepsserrors_test_epss_get_returns_none_for_unknown_cve": ".test_epss_get_returns_none_for_unknown_cve()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L172 | neighbors=[TestLoadEpssErrors, _valid_epss()]
- "tests_test_loaders_testloadepsserrors_test_valid_epss_loads": ".test_valid_epss_loads()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L164 | neighbors=[TestLoadEpssErrors, _valid_epss()]
- "tests_test_loaders_testloadkeverrors_test_valid_kev_loads": ".test_valid_kev_loads()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L138 | neighbors=[TestLoadKevErrors, _valid_kev()]
- "tests_test_loaders_testloadsnapshoterrors_test_error_message_mentions_re_sync": ".test_error_message_mentions_re_sync()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L101 | neighbors=[The FileNotFoundError message should me…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_malformed_json_raises": ".test_malformed_json_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L77 | neighbors=[Completely broken JSON must propagate a…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_missing_file_raises_file_not_found": ".test_missing_file_raises_file_not_found()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L59 | neighbors=[A path that doesn't exist must raise Fi…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_missing_required_key_raises": ".test_missing_required_key_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L85 | neighbors=[A JSON file that is valid JSON but miss…, TestLoadSnapshotErrors]
- "tests_test_loaders_valid_kev": "_valid_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L42 | neighbors=[test_loaders.py, .test_valid_kev_loads()]
- "tests_test_main_scripts_completeness_test_fallback_count_based_when_no_requested_set": "test_fallback_count_based_when_no_requested_set()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L64 | neighbors=[test_main_scripts_completeness.py, _rec()]
- "tests_test_main_scripts_correlation_test_correlations_are_evidence_backed": "test_correlations_are_evidence_backed()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L91 | neighbors=[test_main_scripts_correlation.py, _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-154.json

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
