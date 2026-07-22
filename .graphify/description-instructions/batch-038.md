# Node Description Batch 39 of 76

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

- "lib_findings_store_sladeadline": "slaDeadline()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L27 | neighbors=[findings-store.ts, saveFindings()]
- "lib_graph_store_edgesforpath": "edgesForPath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L241 | neighbors=[graph-store.ts, buildAttackPaths()]
- "lib_graph_store_scorepath": "scorePath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L225 | neighbors=[graph-store.ts, buildAttackPaths()]
- "lib_job_store_genjobid": "genJobId()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L37 | neighbors=[job-store.ts, createJob()]
- "lib_job_store_getnextjobforagent": "getNextJobForAgent()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L62 | neighbors=[job-store.ts, readJobs()]
- "lib_nuclei_parser_nucleimatch": "NucleiMatch" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L3 | neighbors=[nuclei-parser.ts, scan-pipeline.ts]
- "lib_openvas_client_gettask": "getTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L28 | neighbors=[openvas-client.ts, route.ts]
- "lib_openvas_client_openvasfinding": "OpenVASFinding" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L3 | neighbors=[openvas-client.ts, scan-pipeline.ts]
- "lib_permissions_store_getallusers": "getAllUsers()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L40 | neighbors=[permissions-store.ts, read()]
- "lib_permissions_store_iptoint": "ipToInt()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L120 | neighbors=[permissions-store.ts, targetMatchesScope()]
- "lib_permissions_store_permitteduser": "PermittedUser" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L8 | neighbors=[admin.ts, permissions-store.ts]
- "lib_permissions_store_targetmatchesscope": "targetMatchesScope()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L124 | neighbors=[permissions-store.ts, ipToInt()]
- "lib_scan_events_broadcasttoscan": "broadcastToScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L20 | neighbors=[route.ts, scan-events.ts]
- "lib_scan_events_subscribescan": "subscribeScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L7 | neighbors=[scan-events.ts, route.ts]
- "lib_scan_pipeline_computeoverallprogress": "computeOverallProgress()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L117 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_createinitialpipelinestate": "createInitialPipelineState()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L89 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_drainscanevents": "drainScanEvents()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L83 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_pipelinestate": "PipelineState" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L33 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_profile_tools": "PROFILE_TOOLS" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L58 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_pushscanevent": "pushScanEvent()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L76 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_scanprofile": "ScanProfile" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L5 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_scantool": "ScanTool" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L4 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_setpipeline": "setPipeline()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L71 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_stagestate": "StageState" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L7 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_target_parser_estimatehostcount": "estimateHostCount()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L40 | neighbors=[target-parser.ts, parseTargets()]
- "lib_target_parser_validoctets": "validOctets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L12 | neighbors=[target-parser.ts, isValidTarget()]
- "lib_tenant_rootdomain": "rootDomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L17 | neighbors=[tenant.ts, subdomainFromHost()]
- "lib_tenant_server_clientfromrequest": "clientFromRequest()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L16 | neighbors=[tenant-server.ts, readTenantSubdomain()]
- "lib_tenant_server_currentclient": "currentClient()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L26 | neighbors=[tenant-server.ts, tenantSubdomain()]
- "lib_tenant_server_readtenantsubdomain": "readTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L12 | neighbors=[tenant-server.ts, clientFromRequest()]
- "lib_tenant_server_tenantsubdomain": "tenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L21 | neighbors=[tenant-server.ts, currentClient()]
- "lib_testssl_parser_mapseverity": "mapSeverity()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L14 | neighbors=[testssl-parser.ts, parseTestsslJson()]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Asset]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AttackPath]
- "models_attack_timeline": "attack_timeline.py" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AttackTimeline]
- "models_audit_log": "audit_log.py" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AuditLog]
- "models_audit_log_rationale_12": "Immutable, append-only audit trail for all exploit actions.     No TimestampMixi" | kind=entity | source=manager/backend/app/models/audit_log.py:L12 | neighbors=[AuditLog, Base]
- "models_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/models/detection.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, DetectionResult]
- "models_detection_config": "detection_config.py" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, DetectionConfig]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Engagement]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-038.json

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
