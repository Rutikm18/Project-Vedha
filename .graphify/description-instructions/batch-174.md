# Node Description Batch 175 of 380

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

- "tests_test_instance_lock_testmutualexclusion_test_second_holder_in_another_process_is_refused": ".test_second_holder_in_another_process_is_refused()" | kind=code-symbol | source=probe/tests/test_instance_lock.py:L45 | neighbors=[Must be a REAL second process: flock is…, TestMutualExclusion]
- "tests_test_integration_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_integration.py:L41 | neighbors=[test_integration.py, Return a minimal valid scan result (no …]
- "tests_test_integration_testfulljoblifecycle_test_complete_flow_with_encrypted_scope": ".test_complete_flow_with_encrypted_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L314 | neighbors=[Simulate the full probe lifecycle from …, TestFullJobLifecycle]
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
- "tests_test_intensity_budget_testbudgets_test_deep_budget_exceeds_a_healthy_full_sweep": ".test_deep_budget_exceeds_a_healthy_full_sweep()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L36 | neighbors=[A full 65,535-port sweep runs ~21 min a…, TestBudgets]
- "tests_test_intensity_budget_testbudgets_test_every_preset_declares_the_key": ".test_every_preset_declares_the_key()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L31 | neighbors=[Absent-vs-None must not be ambiguous at…, TestBudgets]
- "tests_test_intensity_budget_testbudgets_test_light_is_unbounded": ".test_light_is_unbounded()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L23 | neighbors=[Already bounded by breadth — ~15 ports., TestBudgets]
- "tests_test_intensity_budget_testbudgets_test_standard_is_unbounded": ".test_standard_is_unbounded()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L27 | neighbors=[Already bounded by the profile's own po…, TestBudgets]
- "tests_test_intensity_budget_testtuningtranslation_test_override_can_bound_an_otherwise_unbounded_preset": ".test_override_can_bound_an_otherwise_unbounded_preset()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L72 | neighbors=[An operator running standard against a …, TestTuningTranslation]
- "tests_test_intensity_budget_testtuningtranslation_test_override_is_clamped_to_a_safe_envelope": ".test_override_is_clamped_to_a_safe_envelope()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L64 | neighbors=[Same clamping discipline as every other…, TestTuningTranslation]
- "tests_test_intensity_budget_testtuningtranslation_test_run_engagement_accepts_the_kwarg": ".test_run_engagement_accepts_the_kwarg()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L78 | neighbors=[Guards the seam: a tuning key run_engag…, TestTuningTranslation]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-174.json

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
