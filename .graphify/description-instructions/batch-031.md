# Node Description Batch 32 of 119

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

- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …, Pull short printable ASCII runs from a …]
- "scanner_port": "port.go" | kind=code-symbol | source=probe-go/scanner/port.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, PortRange(), ScanPorts(), 2885afa Add comprehensive probe testing…]
- "scanner_safe_retry": "Retry()" | kind=code-symbol | source=probe-go/scanner/safe.go:L64 | neighbors=[safe.go, DialContext(), backoff(), IsTransient()]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L389 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L43 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .to_json()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L64 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L157 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_scopeguard_inscope": ".InScope()" | kind=code-symbol | source=probe-go/scanner/scope.go:L93 | neighbors=[ScopeGuard, .ExpandRequested(), .isAllowed(), .isExcluded()]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L127 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L133 | neighbors=[tls_scanner.py, _get_cert_der(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L56 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L65 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "schemas_asset_assetout": "AssetOut" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L34 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_asset_bulkassetimportresult": "BulkAssetImportResult" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L54 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_engagement_engagementdetail": "EngagementDetail" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L109 | neighbors=[engagement.py, EngagementStatus, FindingSeverity, EngagementOut]
- "schemas_engagement_engagementfilter": "EngagementFilter" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L72 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L82 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_rationale_21": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[DetectionStatus, FindingSeverity, FindingStatus, FindingPatch]
- "scripts_seed_admin_rationale_1": "Idempotent admin seeder.  Creates a tenant + admin user so you can log in (there" | kind=entity | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[UserRole, Tenant, User, seed_admin.py]
- "services_job_result_service_promote_assets": "_promote_assets()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[job_result_service.py, process_job_result(), Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L50 | neighbors=[Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, DataState.tsx]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L177 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L28 | neighbors=[test_agents.py, ScanJobType, .test_network_types_included(), .test_server_side_types_excluded()]
- "tests_test_agents_testagentregistrationrefresh": "TestAgentRegistrationRefresh" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L208 | neighbors=[test_agents.py, ScanJobType, .test_agent_can_refresh_only_its_own_ro…, .test_agent_cannot_refresh_another_iden…]
- "tests_test_agents_testlistagents": "TestListAgents" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L478 | neighbors=[test_agents.py, ScanJobType, .test_fresh_disconnected_agent_is_not_r…, .test_lists_with_online_flag()]
- "tests_test_agents_testregisteragent_test_agent_token_is_long_lived": ".test_agent_token_is_long_lived()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L564 | neighbors=[Agent token must outlive the 15-min acc…, TestRegisterAgent, _user(), Agent token must outlive the 15-min acc…]
- "tests_test_agents_testregisteragent_test_reuses_existing_probe_by_name": ".test_reuses_existing_probe_by_name()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L529 | neighbors=[Re-registering the same-named probe mus…, TestRegisterAgent, _user(), Re-registering the same-named probe mus…]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L1 | neighbors=[e8262a3 feat(probe): explicit unauthent…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_exploit_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L38 | neighbors=[test_exploit_engine.py, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_nessus_scanner_rationale_1": "Unit tests for NessusScanner — all HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[FindingSeverity, FindingStatus, test_nessus_scanner.py, NessusScanner]
- "tests_test_nuclei_scanner_finding_line": "_finding_line()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L12 | neighbors=[test_nuclei_scanner.py, test_nonzero_exit_retains_and_marks_par…, test_run_scan_streams_jsonl_and_separat…, test_timeout_retains_findings_emitted_b…]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L453 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L243 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-031.json

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
