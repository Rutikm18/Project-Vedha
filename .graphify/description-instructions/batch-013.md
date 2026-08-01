# Node Description Batch 14 of 119

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

- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError, bearerFrom()] | lang=en
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()] | lang=en
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()] | lang=en
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder] | lang=en
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError, bearerFrom()] | lang=en
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()] | lang=en
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()] | lang=en
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, toUiAgent(), backend(), withBackend(), GET, 2885afa Add comprehensive probe testing…] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), isEmailAllowed(), POST(), 2885afa Add comprehensive probe testing…] | lang=en
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType] | lang=en
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType] | lang=en
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, config.py, database.py, _agent_token_from_websocket(), agent_websocket_endpoint()] | lang=en
- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()] | lang=en
- "scanner_db": "db.go" | kind=code-symbol | source=probe-go/scanner/db.go:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dial(), ProbeDB(), probeMongo(), probeMSSQL(), probeMysql()] | lang=en
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=probe/scanner/host_discovery.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, HostDiscoveryScanner, main()] | lang=en
- "scanner_vulncheck_correlate": "Correlate()" | kind=code-symbol | source=probe-go/scanner/vulncheck.go:L140 | neighbors=[vulncheck.go, checkDB(), checkService(), checkTLS(), checkUDP(), checkWeb()] | lang=en
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter, EngagementOut, FindingSummary] | lang=en
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L1 | neighbors=[b4b12a9 Rename project and update files, agent.py, engine.py, transport.py, _cached_transport(), test_cached_identity_refreshes_current_…] | lang=en
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()] | lang=en
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L90 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()] | lang=en
- "tests_test_nuclei_scanner": "test_nuclei_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, FakeProcess, _finding_line(), test_missing_binary_is_a_reported_failu…, test_nonzero_exit_retains_and_marks_par…, test_nonzero_exit_without_findings_rais…] | lang=en
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()] | lang=en
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L889 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_ot_passive()] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()] | lang=en
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L93 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_fully_excluded_cidr_is_dropped(), .test_hostname_passes_through()] | lang=en
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds()] | lang=en
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L1 | neighbors=[b4b12a9 Rename project and update files, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…, test_offer_is_staged_and_only_sends_ack…] | lang=en
- "vuln_prioritizer_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetInput, FindingInput, vulnPrioritizer, DEMO_ASSETS, DEMO_FINDINGS] | lang=en
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, AgentConnectionManager, ConnectionManager, GraphWebSocketManager] | lang=en
- "websocket_manager_connectionmanager": "ConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L25 | neighbors=[manager.py, .broadcast(), .connect(), .disconnect(), .get_room_clients(), .__init__()] | lang=en
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L290 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-013.json

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
