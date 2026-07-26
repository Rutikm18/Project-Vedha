# Node Description Batch 50 of 104

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
- "logout_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/logout/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, POST()]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Asset]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AttackPath]
- "models_attack_timeline": "attack_timeline.py" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AttackTimeline]
- "models_audit_log": "audit_log.py" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AuditLog]
- "models_audit_log_rationale_12": "Immutable, append-only audit trail for all exploit actions.     No TimestampMixi" | kind=entity | source=manager/backend/app/models/audit_log.py:L12 | neighbors=[AuditLog, Base]
- "models_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/models/detection.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, DetectionResult]
- "models_detection_config": "detection_config.py" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, DetectionConfig]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Engagement]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ExploitResult]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output": "llm_output.py" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, LLMOutput]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ScanResult]
- "models_service": "service.py" | kind=code-symbol | source=manager/backend/app/models/service.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Service]
- "models_tenant": "tenant.py" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Tenant]
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, User]
- "naabu_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/naabu/route.ts:L38 | neighbors=[route.ts, validateTargets()]
- "naabu_route_validatetargets": "validateTargets()" | kind=code-symbol | source=manager/frontend/app/api/scan/naabu/route.ts:L9 | neighbors=[route.ts, POST()]
- "native_dir_bust_loadwordlist": "loadWordlist()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L97 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dir_bust_probe": "probe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L71 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dns_recon_attemptzonetransfer": "attemptZoneTransfer()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L96 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_dns_recon_nativeptrsweep": "nativePtrSweep()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L147 | neighbors=[tool-runners.ts, dns-recon.ts]
- "native_dns_recon_safe": "safe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L49 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_http_probe_nativehttpprobe": "nativeHttpProbe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L248 | neighbors=[tool-runners.ts, http-probe.ts]
- "native_port_scan_groupresults": "groupResults()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L261 | neighbors=[tool-runners.ts, port-scan.ts]
- "native_port_scan_resolveports": "resolvePorts()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L131 | neighbors=[port-scan.ts, nativePortScan()]
- "native_tls_info_nativetlsinfo": "nativeTlsInfo()" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L38 | neighbors=[tool-runners.ts, tls-info.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-049.json

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
