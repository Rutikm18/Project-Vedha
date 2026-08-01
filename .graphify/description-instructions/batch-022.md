# Node Description Batch 23 of 119

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

- "websocket_manager_graphwebsocketmanager_handle_message": "._handle_message()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L317 | neighbors=[GraphWebSocketManager, .handle_client(), .broadcast(), .send_personal(), Handle incoming WebSocket messages., Handle incoming WebSocket messages.]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L42 | neighbors=[outbox.py, _claim_batch(), OutboxEvent, ScanResult, main(), run_worker()]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L71 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_tls(), For every open port with a banner fact,…]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L62 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…]
- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L294 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, say(), Run an HTTP-claimed job while renewing …]
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L487 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L274 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L59 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L33 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L46 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L478 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()]
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L153 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L157 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L235 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count concrete open services, not gener…, run_scan()]
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L67 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…]
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L177 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L35 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license(), Stable per-machine ID, derived from hw_…]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L29 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L90 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L108 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .remove(), .save(), Attempt to upload a result with retries…]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L396 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L44 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state(), Durably replace one private JSON state …]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L446 | neighbors=[Establish an authenticated WebSocket co…, Transport, TransportError, Establish an authenticated WebSocket co…, Establish an authenticated WebSocket co…]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L332 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_validation_score_inventory": "score_inventory()" | kind=code-symbol | source=probe/agent/validation.py:L201 | neighbors=[validation.py, Score promoted inventory against explic…, _metric(), _not_scored(), validate_ground_truth()]
- "ai_hallucination_hallucinationguard_validate": ".validate()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L101 | neighbors=[HallucinationGuard, .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), Run all relevant checks and return a co…]
- "ai_prioritizer_extract_features": "extract_features()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L72 | neighbors=[prioritizer.py, _to_float(), Build the model's feature vector from a…, .explain_prediction(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_fallback_score": ".fallback_score()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L204 | neighbors=[Weighted composite 0–1000 (same shape a…, VulnPrioritizer, .explain_prediction(), ._formula_contributions(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_predict_priority": ".predict_priority()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L148 | neighbors=[Return a 0–1000 priority score. Uses th…, VulnPrioritizer, .explain_prediction(), extract_features(), .fallback_score()]
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "assistant_assistantfab": "AssistantFab.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L1 | neighbors=[AssistantFab(), AssistantProvider.tsx, useAssistant(), 1fe16c8 stable but some dead code, need…, 41b692a Update project files]
- "assistant_assistanttext": "AssistantText.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText(), plain(), 1fe16c8 stable but some dead code, need…]
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-022.json

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
