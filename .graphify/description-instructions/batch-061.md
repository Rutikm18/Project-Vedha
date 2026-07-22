# Node Description Batch 62 of 76

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

- "lib_naabu_parser_naaburesult": "NaabuResult" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L3 | neighbors=[naabu-parser.ts]
- "lib_nmap_parser_nmaphost": "NmapHost" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L18 | neighbors=[nmap-parser.ts]
- "lib_nmap_parser_nmapscriptresult": "NmapScriptResult" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L13 | neighbors=[nmap-parser.ts]
- "lib_nmap_parser_nmapservice": "NmapService" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L3 | neighbors=[nmap-parser.ts]
- "lib_nmap_parser_parser": "parser" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L27 | neighbors=[nmap-parser.ts]
- "lib_nuclei_parser_nucleiraw": "NucleiRaw" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L17 | neighbors=[nuclei-parser.ts]
- "lib_openvas_client_cvsstoseverity": "cvssToSeverity()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L36 | neighbors=[openvas-client.ts]
- "lib_openvas_client_openvastaskstate": "OpenVASTaskState" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L18 | neighbors=[openvas-client.ts]
- "lib_openvas_client_taskstore": "taskStore" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L26 | neighbors=[openvas-client.ts]
- "lib_permissions_store_data_path": "DATA_PATH" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L4 | neighbors=[permissions-store.ts]
- "lib_permissions_store_permissionsfile": "PermissionsFile" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L16 | neighbors=[permissions-store.ts]
- "lib_permissions_store_userrole": "UserRole" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L6 | neighbors=[permissions-store.ts]
- "lib_scan_events_callback": "Callback" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L3 | neighbors=[scan-events.ts]
- "lib_scan_events_scanlisteners": "scanListeners" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L5 | neighbors=[scan-events.ts]
- "lib_scan_pipeline_eventqueues": "eventQueues" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L65 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_pipelinecontext": "PipelineContext" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L15 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_pipelinestore": "pipelineStore" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L64 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_stage_weights": "STAGE_WEIGHTS" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L47 | neighbors=[scan-pipeline.ts]
- "lib_target_parser_common_ranges": "COMMON_RANGES" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L132 | neighbors=[target-parser.ts]
- "lib_target_parser_isprivaterange": "isPrivateRange()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L35 | neighbors=[target-parser.ts]
- "lib_target_parser_parseresult": "ParseResult" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L59 | neighbors=[target-parser.ts]
- "lib_target_parser_rfc1918": "RFC1918" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L6 | neighbors=[target-parser.ts]
- "lib_target_parser_toapitargets": "toApiTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L127 | neighbors=[target-parser.ts]
- "lib_tenant_reserved": "RESERVED" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L15 | neighbors=[tenant.ts]
- "lib_testssl_parser_skip_severity": "SKIP_SEVERITY" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L12 | neighbors=[testssl-parser.ts]
- "lib_testssl_parser_testsslissue": "TestsslIssue" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L4 | neighbors=[testssl-parser.ts]
- "lib_with_backend_backendctx": "BackendCtx" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L12 | neighbors=[with-backend.ts]
- "lib_with_backend_handler": "Handler" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L16 | neighbors=[with-backend.ts]
- "list_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scans/list/route.ts:L7 | neighbors=[route.ts]
- "login_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L9 | neighbors=[route.ts]
- "login_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L41 | neighbors=[route.ts]
- "me_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L10 | neighbors=[route.ts]
- "models_base_uuidmixin": "UUIDMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L25 | neighbors=[base.py]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …]
- "naabu_route_parsenaabuoutput": "parseNaabuOutput()" | kind=code-symbol | source=manager/frontend/app/api/scan/naabu/route.ts:L13 | neighbors=[route.ts]
- "native_dir_bust_builtin_paths": "BUILTIN_PATHS" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L16 | neighbors=[dir-bust.ts]
- "native_dir_bust_dirbustresult": "DirBustResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L57 | neighbors=[dir-bust.ts]
- "native_dir_bust_nativediropts": "NativeDirOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L90 | neighbors=[dir-bust.ts]
- "native_dir_bust_proberesp": "ProbeResp" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L66 | neighbors=[dir-bust.ts]
- "native_dns_recon_common_subdomains": "COMMON_SUBDOMAINS" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L33 | neighbors=[dns-recon.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-061.json

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
