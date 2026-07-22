# Node Description Batch 32 of 76

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

- "vuln_nessus_nessusscanner_export_nessus_file": ".export_nessus_file()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L257 | neighbors=[NessusScanner, ._get_client(), Request + poll + download .nessus XML f…] | lang=en
- "vuln_nessus_nessusscanner_launch_scan": ".launch_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L140 | neighbors=[NessusScanner, ._get_client(), Returns scan_uuid (token for tracking).] | lang=en
- "vuln_nessus_nessusscanner_poll_status": ".poll_status()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L151 | neighbors=[NessusScanner, ._get_client(), Returns {status, progress_percent, host…] | lang=en
- "vuln_nessus_rationale_1": "NessusScanner — wraps the Tenable Nessus REST API v6.  Endpoints used:   POST /s" | kind=entity | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[FindingSeverity, FindingStatus, nessus.py] | lang=en
- "vuln_nessus_rationale_102": "Returns nessus scan_id as string." | kind=entity | source=manager/backend/app/vuln/nessus.py:L102 | neighbors=[FindingSeverity, FindingStatus, .create_scan()] | lang=en
- "vuln_nessus_rationale_141": "Returns scan_uuid (token for tracking)." | kind=entity | source=manager/backend/app/vuln/nessus.py:L141 | neighbors=[FindingSeverity, FindingStatus, .launch_scan()] | lang=en
- "vuln_nessus_rationale_152": "Returns {status, progress_percent, host_count}." | kind=entity | source=manager/backend/app/vuln/nessus.py:L152 | neighbors=[FindingSeverity, FindingStatus, .poll_status()] | lang=en
- "vuln_nessus_rationale_168": "Returns list of raw finding dicts from all hosts." | kind=entity | source=manager/backend/app/vuln/nessus.py:L168 | neighbors=[FindingSeverity, FindingStatus, .get_results()] | lang=en
- "vuln_nessus_rationale_207": "Map a raw Nessus vulnerability dict → Finding-compatible dict.         Returns a" | kind=entity | source=manager/backend/app/vuln/nessus.py:L207 | neighbors=[FindingSeverity, FindingStatus, .map_finding()] | lang=pt
- "vuln_nessus_rationale_258": "Request + poll + download .nessus XML for evidence storage." | kind=entity | source=manager/backend/app/vuln/nessus.py:L258 | neighbors=[FindingSeverity, FindingStatus, .export_nessus_file()] | lang=en
- "vuln_nessus_rationale_39": "Async Nessus API client. One instance per engagement scan session." | kind=entity | source=manager/backend/app/vuln/nessus.py:L39 | neighbors=[FindingSeverity, FindingStatus, NessusScanner] | lang=it
- "vuln_nessus_rationale_74": "Prefer API key auth (stateless, no session expiry).         Falls back to userna" | kind=entity | source=manager/backend/app/vuln/nessus.py:L74 | neighbors=[FindingSeverity, FindingStatus, .authenticate()] | lang=en
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, NucleiScanner, NucleiScanner — async subprocess wrappe…] | lang=en
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L74 | neighbors=[NucleiScanner, .parse_output(), Runs nuclei as an async subprocess.    …] | lang=en
- "vuln_tasks_run_post_scan_enrichment": "run_post_scan_enrichment()" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L37 | neighbors=[tasks.py, Triggered by the vuln scan API after a …, _fire_critical_webhook()] | lang=en
- "websocket_manager_agentconnectionmanager_push_job": ".push_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L146 | neighbors=[AgentConnectionManager, .unregister(), Push a job to a specific agent over Web…] | lang=en
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L164 | neighbors=[AgentConnectionManager, .unregister(), Push a job to the first online connecte…] | lang=en
- "websocket_manager_connectionmanager_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L33 | neighbors=[ConnectionManager, .handle_client(), Accept connection and add to room.] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L279 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L298 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…] | lang=en
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L288 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update.] | lang=en
- "workflow_asset_asset_merge_host_discovery": "._merge_host_discovery()" | kind=code-symbol | source=probe/workflow/asset.py:L95 | neighbors=[Asset, _parse_ts(), PortFact] | lang=en
- "workflow_asset_asset_merge_port_scan": "._merge_port_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L105 | neighbors=[Asset, _parse_ts(), PortFact] | lang=en
- "workflow_asset_asset_merge_udp_scan": "._merge_udp_scan()" | kind=code-symbol | source=probe/workflow/asset.py:L143 | neighbors=[Asset, _parse_ts(), PortFact] | lang=en
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=probe/workflow/asset.py:L71 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…] | lang=en
- "workflow_cache_classify_certainty": "classify_certainty()" | kind=code-symbol | source=probe/workflow/cache.py:L46 | neighbors=[cache.py, .get(), .put()] | lang=en
- "workflow_cache_workflowcache_get": ".get()" | kind=code-symbol | source=probe/workflow/cache.py:L109 | neighbors=[classify_certainty(), WorkflowCache, .should_recheck()] | lang=en
- "workflow_cache_workflowcache_load": "._load()" | kind=code-symbol | source=probe/workflow/cache.py:L89 | neighbors=[WorkflowCache, .__init__(), .from_jsonl_dict()] | lang=en
- "workflow_cache_workflowcache_put": ".put()" | kind=code-symbol | source=probe/workflow/cache.py:L112 | neighbors=[WorkflowCache, CacheEntry, classify_certainty()] | lang=en
- "workflow_cache_workflowcache_should_recheck": ".should_recheck()" | kind=code-symbol | source=probe/workflow/cache.py:L120 | neighbors=[True if there's no cached entry, OR the…, WorkflowCache, .get()] | lang=en
- "workflow_modes_assessment": "assessment()" | kind=code-symbol | source=probe/workflow/modes.py:L30 | neighbors=[modes.py, EngagementMode, Full funnel, every branch the profile a…] | lang=en
- "workflow_modes_re_scan": "re_scan()" | kind=code-symbol | source=probe/workflow/modes.py:L43 | neighbors=[modes.py, Loads a prior engagement's cache; only …, EngagementMode] | lang=en
- "workflow_modes_triage": "triage()" | kind=code-symbol | source=probe/workflow/modes.py:L24 | neighbors=[modes.py, Discovery + ports + banner only — no de…, EngagementMode] | lang=en
- "workflow_router_looks_like_tls": "looks_like_tls()" | kind=code-symbol | source=probe/workflow/router.py:L42 | neighbors=[router.py, True when this port's banner result is …, route_branches()] | lang=en
- "workflow_workflow_engine_gather_per_host": "_gather_per_host()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L50 | neighbors=[workflow_engine.py, Runs scanner.scan_target(host) across h…, run_engagement()] | lang=en
- "workflow_workflow_engine_port_candidates": "_port_candidates()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L79 | neighbors=[workflow_engine.py, Return TCP ports worth scanning for thi…, run_engagement()] | lang=en
- "workflow_workflow_engine_run_passive": "_run_passive()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L119 | neighbors=[workflow_engine.py, run_engagement(), _Sink] | lang=en
- "workflow_workflow_engine_split_cached": "_split_cached()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L61 | neighbors=[workflow_engine.py, Splits candidate_ports into (ports that…, run_engagement()] | lang=en
- "ad_adcs_adcschecker_has_low_priv": "._has_low_priv()" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L127 | neighbors=[ADCSChecker, .check_esc1()] | lang=en
- "ad_asreproast_asreproastchecker_get_no_preauth_accounts": ".get_no_preauth_accounts()" | kind=code-symbol | source=manager/backend/app/ad/asreproast.py:L42 | neighbors=[ASREPRoastChecker, Usernames of enabled accounts with pre-…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-031.json

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
