# Node Description Batch 27 of 104

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

- "probe_go_main_renderreport": "renderReport()" | kind=code-symbol | source=probe-go/main.go:L129 | neighbors=[main.go, localScan(), findServiceLabel(), protoOr()]
- "probe_pipeline_collector": "_Collector" | kind=code-symbol | source=probe/pipeline.py:L121 | neighbors=[pipeline.py, .__init__(), .write(), _run_active()]
- "results_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, detection-store.ts, detectionStore, GET()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[Engagement, Finding, ScanJob, activity.py]
- "routers_agents_encrypt_scope_for_agent": "_encrypt_scope_for_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L207 | neighbors=[agents.py, enqueue_agent_job(), get_agent_jobs(), Encrypt the engagement scope for a spec…]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L262 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), _set_job()]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L192 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L226 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L154 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L182 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_engagements_compute_overview": "_compute_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L39 | neighbors=[engagements.py, engagements_overview(), Shared aggregation — used by both the c…, _refresh_overview_cache()]
- "routers_engagements_engagements_overview": "engagements_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L397 | neighbors=[engagements.py, _compute_overview(), _overview_cache_key(), P1: kills the BFF N+1 (was list + one d…]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L422 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_health": "health.py" | kind=code-symbol | source=manager/backend/app/routers/health.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, database.py, dependencies.py, health()]
- "run_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, detection-store.ts, detectionStore, POST()]
- "scanner_banner": "banner.go" | kind=code-symbol | source=probe-go/scanner/banner.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, GrabBanner(), guessService(), ParseHTTPResponse()]
- "scanner_discover_probealive": "probeAlive()" | kind=code-symbol | source=probe-go/scanner/discover.go:L50 | neighbors=[discover.go, DiscoverHosts(), intStr(), isRefused()]
- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/scanner/host_discovery.py:L29 | neighbors=[host_discovery.py, BaseScanner, ._probe(), .scan_target()]
- "scanner_nmap_runnmapversion": "RunNmapVersion()" | kind=code-symbol | source=probe-go/scanner/nmap.go:L34 | neighbors=[nmap.go, joinInts(), NmapAvailable(), parseNmapXML()]
- "scanner_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L81 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…]
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L134 | neighbors=[PassiveCollector, _device_hint(), _open_listener(), ._select()]
- "scanner_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L204 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…]
- "scanner_safe_retry": "Retry()" | kind=code-symbol | source=probe-go/scanner/safe.go:L64 | neighbors=[safe.go, DialContext(), backoff(), IsTransient()]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L389 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L43 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .to_json()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L64 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L157 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_scope": "scope.go" | kind=code-symbol | source=probe-go/scanner/scope.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, NewScopeGuard(), ScopeFromFile(), ScopeGuard]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_tls": "tls.go" | kind=code-symbol | source=probe-go/scanner/tls.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, enumerateWeakCiphers(), parseCert(), ProbeTLS()]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L133 | neighbors=[tls_scanner.py, _get_cert_der(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L56 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L65 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "schemas_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AssetIn, AssetOut, BulkAssetImportResult]
- "schemas_asset_assetout": "AssetOut" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L34 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_asset_bulkassetimportresult": "BulkAssetImportResult" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L54 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_common": "common.py" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ErrorDetail, paginate(), PaginatedResponse]
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L12 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_engagementdetail": "EngagementDetail" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L58 | neighbors=[engagement.py, EngagementStatus, FindingSeverity, EngagementOut]
- "schemas_engagement_engagementfilter": "EngagementFilter" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L21 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-026.json

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
