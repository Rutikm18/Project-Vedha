# Node Description Batch 22 of 236

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

- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L425 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_permanent_client_errors_are_marke…, .test_retryable_client_errors_return_fa…]
- "tests_test_validation_endpoints": "test_validation_endpoints.py" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _mock_db(), test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids()]
- "tests_test_vantage_fusion_probe": "_probe()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L15 | neighbors=[test_vantage_fusion.py, Build a one-target probe exposure resul…, test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_…, test_external_vantage_open_makes_port_e…, test_fused_service_exposure_is_keyed_fo…]
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()]
- "tests_test_wire_identity": "test_wire_identity.py" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L1 | neighbors=[2c53ae9 evasion(scanner): randomized sc…, 37376de hardening(scanner): OPSEC de-si…, 4733f24 evasion(scanner): --source-port…, TestChooseSourcePort, TestEvasionFlags, TestJitteredDelay]
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…]
- "tools_issue_license": "issue_license.py" | kind=code-symbol | source=probe/tools/issue_license.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, _b64(), issue(), keygen()]
- "verify_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, verifyOtp(), addUser(), getUser(), POST()]
- "vuln_enrichment_ttlcache": "TTLCache" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L27 | neighbors=[enrichment.py, LRU + TTL eviction. Expired keys are pu…, OrderedDict, .__contains__(), .get(), .__getitem__()]
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L293 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process(), _reclaim_stale()]
- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=probe/workflow/cache.py:L78 | neighbors=[cache.py, In-memory (host, port, scanner) -> Cach…, .all_entries_for_host(), .get(), .__init__(), ._load()]
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L500 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, _bounded_env_int(), say(), Run an HTTP-claimed job while renewing …]
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L237 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient]
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L377 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_integration.py]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L672 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Establish an authenticated WebSocket co…, Generic authenticated GET, returns pars…]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L542 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L456 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L252 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L581 | neighbors=[Submit a scan result to the manager.   …, Transport, _strip_nul(), .ensure_device_access(), Submit a scan result to the manager.   …, Submit a scan result to the manager.   …]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L293 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …, Return (scan_type, profile, intensity) …]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L260 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…]
- "assistant_factcard": "FactCard.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard(), Pip(), assistant.ts, FactCardVM]
- "auth_portal_scope": "portal_scope.py" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L1 | neighbors=[dependencies.py, assert_client(), client_scoped(), require_client(), resolve_scope(), scoped_engagement()]
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[clearSession(), loadSession(), buildLogoutCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildStatusCommand(), ScanRow, STATUS_COLOR, d1b4dd3 trim frontend to 7 core pages; …]
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildWhoamiCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2de251b6a34cad99831e042cf014ca1bcfa6aed2": "2de251b feat(scanner): ICMP timestamp fallback — echo-filter bypass + clock har…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 9c973dd feat(scanner): tarpit/honeypot …, os_fingerprint.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@daf3de2734a3efdd04df485c8544d56209bd5554": "daf3de2 feat(scanner): add service enumeration and enrichment layer" | kind=Commit | source=git | neighbors=[6be8259 feat(integrations): outbox deli…, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3bb8dba0a692bc5cd7881b8be1ce1529f8f659a": "f3bb8db feat(manager): cross-worker WS backplane + agent job-history + fleet qu…" | kind=Commit | source=git | neighbors=[3565ada fix(ingest): NUL-safe result su…, main.py, feat/nvd-vuln-detection-and-ingest-hard…, bd85323 feat(probe): self-heal re-enrol…, page.tsx, route.ts]
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO]
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L99 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine]
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[pipeline.py, AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB]
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[ab_evaluate(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB]
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[run_pipeline(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB]
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()]
- "detection_engine_vuln_db_read_snapshot": "_read_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L160 | neighbors=[vuln_db.py, load_snapshot(), _merge_companion(), The actual parse + integrity-verify + b…, _boundary_versions(), _content_hash()]
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L72 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
