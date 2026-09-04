# Node Description Batch 27 of 330

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

- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L362 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…]
- "workers_outbox_reclaim_stale": "_reclaim_stale()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L338 | neighbors=[outbox.py, Requeue events a dead worker left in PR…, _dead_letter_stale_stmt(), _requeue_stale_stmt(), _stale_cutoff(), run_worker()]
- "workflow_host_health": "host_health.py" | kind=code-symbol | source=probe/workflow/host_health.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, test_host_health.py, scanner_base.py, _env_int(), _heartbeat_interval(), _heartbeat_misses()]
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L57 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()]
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L801 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…]
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L239 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L205 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…, Coerce val to float and clamp to [lo, h…]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L291 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…]
- "agent_engine_derive_post_stage": "_derive_post_stage()" | kind=code-symbol | source=probe/agent/engine.py:L463 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), Return (extra ScanResults to append as …, run_scan(), Return (extra ScanResults to append as …]
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L225 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …, Translate operator-supplied job params …]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_integration.py]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L547 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), ._archive_result(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L129 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state(), Durably replace one private JSON state …, Durably replace one private JSON state …]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L293 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …, Return (scan_type, profile, intensity) …]
- "auth_portal_scope": "portal_scope.py" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L1 | neighbors=[dependencies.py, assert_client(), client_scoped(), require_client(), resolve_scope(), scoped_engagement()]
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[clearSession(), loadSession(), buildLogoutCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildStatusCommand(), ScanRow, STATUS_COLOR, d1b4dd3 trim frontend to 7 core pages; …]
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildWhoamiCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@21ebc4647fbc8013300844481aacf06393192c11": "21ebc46 feat(detection): unified prioritization engine (risk_score for every fi…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, 0236a60 fix(detection): full EPSS catal…, prioritization.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@22e4f8d2c085fe3c93a07a9eec8b728ac9e197f3": "22e4f8d chore: update version" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@3565ada02b223c451ee7c0a953852dcddf688973": "3565ada fix(ingest): NUL-safe result submission + network-service hygiene findi…" | kind=Commit | source=git | neighbors=[transport.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, f3bb8db feat(manager): cross-worker WS …]
- "commit:repo:github.com/Rutikm18/Project-Vedha@656e9098c880124f47c33abd669ec74a055d2761": "656e909 feat(ui): polish login page, top ribbon, and engagement toolbar" | kind=Commit | source=git | neighbors=[5b980e1 docs(spec): installer warning +…, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@d0d193118467023761f5f97d55f72b41d37ce287": "d0d1931 feat(detection): NVD/CPE vuln feed for network-service banners" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, 3565ada fix(ingest): NUL-safe result su…, build_nvd_cpe_snapshot.py]
- "cve_online": "online.py" | kind=code-symbol | source=probe/cve/online.py:L1 | neighbors=[6e2818f Add support for additional serv…, _apply(), enrich_findings(), lookup_nvd(), lookup_vulners(), OnlineResult]
- "detection_engine_bridge_detect_all_from_facts_traced": "detect_all_from_facts_traced()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L168 | neighbors=[engine_bridge.py, create_findings_from_facts(), detect_all_from_facts(), _accepted(), _ensure_importable(), _ingest_census()]
- "detection_engine_exploitability": "exploitability.py" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, apply_to_findings(), assess(), kev_links_for(), KevLink]
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[pipeline.py, AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB]
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[ab_evaluate(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB]
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[run_pipeline(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB]
- "detection_engine_posture_rules_detect_exposed_services": "detect_exposed_services()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L940 | neighbors=[posture_rules.py, compute_risk(), _evidence_ref(), _exposed_title(), make_posture_id(), PostureFinding]
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()]
- "detection_engine_vuln_db_read_snapshot": "_read_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L160 | neighbors=[vuln_db.py, load_snapshot(), _merge_companion(), The actual parse + integrity-verify + b…, _boundary_versions(), _content_hash()]
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L72 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()]
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()]
- "events_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/events/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fail(), GET(), backend.ts]
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L120 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()]
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, Exposure, GET, backend.ts, backend()]
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
