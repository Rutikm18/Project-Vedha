# Node Description Batch 31 of 380

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

- "agent_connect": "connect.py" | kind=code-symbol | source=probe/agent/connect.py:L1 | neighbors=[admit_job(), canonical_job_bytes(), connect_env(), kill_switch_active(), run(), verify_job()] | lang=en
- "agent_doctor_run": "run()" | kind=code-symbol | source=probe/agent/doctor.py:L140 | neighbors=[doctor.py, Check, check_clock(), check_disk(), check_privilege(), check_python()] | lang=en
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L75 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…, Single factory for error result dicts —…] | lang=en
- "agent_instance_lock": "instance_lock.py" | kind=code-symbol | source=probe/agent/instance_lock.py:L1 | neighbors=[agent.py, acquire_instance_lock(), _holder_hint(), InstanceLockError, lock_path_for(), release_instance_lock()] | lang=en
- "agent_obs": "obs.py" | kind=code-symbol | source=probe/agent/obs.py:L1 | neighbors=[build_diagnostics(), heartbeat_metrics(), _is_sensitive(), log_line(), _mask_addr(), mask_ip()] | lang=en
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_integration.py] | lang=en
- "agent_transport_transport_bootstrap": ".bootstrap()" | kind=code-symbol | source=probe/agent/transport.py:L409 | neighbors=[Register using a manager-side shared bo…, Transport, .save_state(), TransportError, Register using a manager-side shared bo…, Register using a manager-side shared bo…] | lang=en
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L268 | neighbors=[True if we have both an agent_id and a …, Transport, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …] | lang=en
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L293 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …, Return (scan_type, profile, intensity) …] | lang=en
- "auth_portal_scope": "portal_scope.py" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L1 | neighbors=[dependencies.py, assert_client(), client_scoped(), require_client(), resolve_scope(), scoped_engagement()] | lang=en
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[clearSession(), loadSession(), buildLogoutCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildStatusCommand(), ScanRow, STATUS_COLOR, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildWhoamiCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@08d8fe1e02b99061c0873bb109a2963fa84cfca4": "08d8fe1 Phase 2: config precedence loader + real doctor (+12 tests)" | kind=Commit | source=git | neighbors=[config_model.py, doctor.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 42b9cf2 Phase 3: exit-state protocol + …] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@42b7429ac9bc252cc2b53493ade589593107521c": "42b7429 feat(probe): deep intensity gets a 30-minute per-host ceiling" | kind=Commit | source=git | neighbors=[09c6c0a feat(probe): per-host wall-cloc…, engine.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, f300b2a feat(integrations): ServiceNow …] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@42b9cf2bee9690fe1d53cbf097072c0583bf3631": "42b9cf2 Phase 3: exit-state protocol + supervisor (+12 tests)" | kind=Commit | source=git | neighbors=[08d8fe1 Phase 2: config precedence load…, exit_state.py, supervisor.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7a87d1964cd2b45dc3d3d4d34617425eec4f30cf": "7a87d19 docs: add Ubuntu Docker probe deployment runbook" | kind=Commit | source=git | neighbors=[3e6b187 feat: unify customer and manage…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@e80b25f2f953a1726814cdf02829b80437d4ad51": "e80b25f feat(scheduling): ScanSchedule model + migration 0040" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 93d36f9 feat(scheduling): due-schedule …, __init__.py, scan_schedule.py] | lang=en
- "cve_online": "online.py" | kind=code-symbol | source=probe/cve/online.py:L1 | neighbors=[6e2818f Add support for additional serv…, _apply(), enrich_findings(), lookup_nvd(), lookup_vulners(), OnlineResult] | lang=en
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L273 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), CVE finding dicts only — backward-compa…, CVE finding dicts only — backward-compa…, create_findings_from_facts(), _ensure_importable()] | lang=en
- "detection_engine_exploitability": "exploitability.py" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, apply_to_findings(), assess(), kev_links_for(), KevLink] | lang=en
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[pipeline.py, AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[ab_evaluate(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[run_pipeline(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()] | lang=en
- "detection_engine_vuln_db_read_snapshot": "_read_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L160 | neighbors=[vuln_db.py, load_snapshot(), _merge_companion(), The actual parse + integrity-verify + b…, _boundary_versions(), _content_hash()] | lang=en
- "discovery_finding_translator_create_findings_from_probe_result": "create_findings_from_probe_result()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L191 | neighbors=[finding_translator.py, _escalate_by_exposure(), _find_open_duplicate(), _map_severity(), _resolve_asset(), Convert a probe's self-assessed `findin…] | lang=en
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L72 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…] | lang=en
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()] | lang=en
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()] | lang=en
- "events_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/events/route.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, fail(), GET(), backend.ts] | lang=en
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L120 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()] | lang=en
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, Exposure, GET, backend.ts, backend()] | lang=en
- "frontend_proxy": "proxy.ts" | kind=code-symbol | source=manager/frontend/proxy.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, 1fe16c8 stable but some dead code, need…, config, isPublic(), proxy(), PUBLIC_PATHS] | lang=en
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder] | lang=en
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()] | lang=en
- "lib_console_source_useconsolequery": "useConsoleQuery()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L266 | neighbors=[DashboardCharts.tsx, DashboardGrid.tsx, DashboardWorkspace.tsx, ExposureCards.tsx, LiveOverview.tsx, PostureScorecard.tsx] | lang=en
- "lib_fleet_workspace_api": "fleet-workspace-api.ts" | kind=code-symbol | source=manager/frontend/lib/fleet-workspace-api.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, FleetJobs.tsx, page.tsx, fetcher.ts, fetchJson(), createFleetWorkspaceApi()] | lang=en
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()] | lang=en
- "lib_scan_launch": "scan-launch.ts" | kind=code-symbol | source=manager/frontend/lib/scan-launch.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, route.ts, buildScanLaunchRequest(), INTENSITY_PRESETS, JOB_TYPE_MAP, ScanLaunchBody] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-030.json

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
