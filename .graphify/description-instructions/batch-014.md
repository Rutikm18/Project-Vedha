# Node Description Batch 15 of 119

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

- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()]
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L270 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()]
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/scanner/host_discovery.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, HostDiscoveryScanner, main()]
- "services_llm_managerllmservice_generate": ".generate()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L199 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._default_runtime(), ._ensure_installed_ollama_model(), ._ollama()]
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L1 | neighbors=[b4b12a9 Rename project and update files, agent.py, engine.py, transport.py, _cached_transport(), test_cached_identity_refreshes_current_…]
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L90 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_nuclei_scanner": "test_nuclei_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, FakeProcess, _finding_line(), test_missing_binary_is_a_reported_failu…, test_nonzero_exit_retains_and_marks_par…, test_nonzero_exit_without_findings_rais…]
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()]
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L911 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_ot_passive()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()]
- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L93 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_fully_excluded_cidr_is_dropped(), .test_hostname_passes_through()]
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds()]
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L1 | neighbors=[b4b12a9 Rename project and update files, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…, test_offer_is_staged_and_only_sends_ack…]
- "vuln_prioritizer_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetInput, FindingInput, vulnPrioritizer, DEMO_ASSETS, DEMO_FINDINGS]
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, AgentConnectionManager, ConnectionManager, GraphWebSocketManager]
- "websocket_manager_connectionmanager": "ConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L25 | neighbors=[manager.py, .broadcast(), .connect(), .disconnect(), .get_room_clients(), .__init__()]
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L290 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()]
- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=probe/workflow/cache.py:L78 | neighbors=[cache.py, In-memory (host, port, scanner) -> Cach…, .all_entries_for_host(), .get(), .__init__(), ._load()]
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L133 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L764 | neighbors=[agent.py, main(), _load_or_create_identity(), say(), Return (agent_id, token, fresh, identit…, Return (agent_id, token, fresh, identit…]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L620 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L505 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), say(), Run one job while keeping WS status/res…]
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, test_integration.py, test_result_spool.py]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L86 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_count()]
- "agent_transport_transport_update_state": ".update_state()" | kind=code-symbol | source=probe/agent/transport.py:L177 | neighbors=[Merge and atomically persist private st…, Transport, .clear_state(), .save_state(), _atomic_write_private_state(), _sync_directory()]
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …]
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings, AiRuntimeError]
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-014.json

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
