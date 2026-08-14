# Node Description Batch 48 of 186

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

- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L99 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "scanner_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L133 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie()]
- "scanner_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L140 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie()]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "scanner_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "scanner_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync(), Flag the security-relevant properties o…]
- "scanner_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync(), Grade overall TLS posture A/B/C/F from …]
- "schemas_asset_assetout": "AssetOut" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L34 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_asset_bulkassetimportresult": "BulkAssetImportResult" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L54 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_engagement_engagementdetail": "EngagementDetail" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L108 | neighbors=[engagement.py, EngagementOut, EngagementStatus, FindingSeverity]
- "schemas_engagement_engagementfilter": "EngagementFilter" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L71 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L81 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_validate_scope_entries": "validate_scope_entries()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L12 | neighbors=[engagement.py, .validate_scopes(), Validate and de-duplicate exact IP/CIDR…, Validate and de-duplicate exact IP/CIDR…]
- "schemas_finding_rationale_21": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[FindingPatch, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_detect_drift": "_detect_drift()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L150 | neighbors=[seed_admin.py, log_warn(), Warn if the tenant has multiple admins …, _seed_once()]
- "scripts_seed_admin_log": "_log()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L71 | neighbors=[seed_admin.py, log_error(), log_info(), log_warn()]
- "scripts_seed_admin_log_error": "log_error()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L89 | neighbors=[seed_admin.py, _log(), main(), _seed_with_retry()]
- "scripts_seed_admin_log_info": "log_info()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L81 | neighbors=[seed_admin.py, _log(), main(), _seed_once()]
- "scripts_seed_admin_rationale_1": "Idempotent admin seeder — production-grade rewrite.  Behavior:   First run : cre" | kind=entity | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[seed_admin.py, UserRole, Tenant, User]
- "scripts_seed_admin_validate_env": "_validate_env()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L95 | neighbors=[seed_admin.py, main(), Returns (email, password, tenant_name, …, log_warn()]
- "scripts_startup_validator_databaseconnectivityvalidator": "DatabaseConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L310 | neighbors=[startup_validator.py, .validate(), Verifies actual database connectivity a…, run_all_validators()]
- "scripts_startup_validator_redisconnectivityvalidator": "RedisConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L354 | neighbors=[startup_validator.py, Verifies Redis connectivity at startup., .validate(), run_all_validators()]
- "scripts_startup_validator_startupvalidationerror": "StartupValidationError" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L27 | neighbors=[startup_validator.py, Raised when a required configuration in…, RuntimeError, .raise_if_errors()]
- "services_llm_managerllmservice_anthropic": "._anthropic()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L456 | neighbors=[ManagerLlmService, ._client(), ._dispatch(), .generate()]
- "services_llm_managerllmservice_ollama": "._ollama()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L391 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openai": "._openai()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L435 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openrouter": "._openrouter()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L410 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_status": ".status()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L154 | neighbors=[ManagerLlmService, _is_local_ollama_model(), ._client(), ._default_runtime()]
- "services_posture_aggregate": "aggregate()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L47 | neighbors=[posture.py, _clamp01(), compute_scores(), Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Em…]
- "services_posture_present_in_run": "_present_in_run()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L104 | neighbors=[posture.py, compare(), _to_utc(), True when the finding was live as of ru…]
- "services_validation_ingest_ingest_validation_result": "ingest_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L51 | neighbors=[validation_ingest.py, apply_validation_outcome(), looks_like_validation_result(), If ``job_id`` belongs to a ValidationRe…]
- "tests_backend_auth_test": "backend-auth.test.ts" | kind=code-symbol | source=manager/frontend/tests/backend-auth.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, bearerFrom(), cookieFrom()]
- "tests_test_adaptive_rate_testudpscanneradaptive": "TestUdpScannerAdaptive" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L185 | neighbors=[test_adaptive_rate.py, .test_adaptive_scanner_creates_controll…, .test_adaptive_scanner_detects_open_on_…, .test_non_adaptive_scanner_has_no_contr…]
- "tests_test_adaptive_rate_testwindowgating": "TestWindowGating" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L79 | neighbors=[test_adaptive_rate.py, .test_acquire_blocks_when_window_full(), .test_release_unblocks_waiter(), .test_report_loss_shrinks_and_releases()]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L195 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L28 | neighbors=[test_agents.py, .test_network_types_included(), .test_server_side_types_excluded(), ScanJobType]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
