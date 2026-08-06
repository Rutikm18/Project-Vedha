# Node Description Batch 98 of 134

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

- "lib_graph_store_gedge": "GEdge" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L27 | neighbors=[graph-store.ts]
- "lib_graph_store_gnode": "GNode" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L11 | neighbors=[graph-store.ts]
- "lib_graph_store_internet_exposed_ids": "INTERNET_EXPOSED_IDS" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L257 | neighbors=[graph-store.ts]
- "lib_graph_store_nodes_nodes_edges_edges": "{ nodes: NODES, edges: EDGES }" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L237 | neighbors=[graph-store.ts]
- "lib_graph_store_nodetype": "NodeType" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L4 | neighbors=[graph-store.ts]
- "lib_graph_store_pathstatus": "PathStatus" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L9 | neighbors=[graph-store.ts]
- "lib_graph_store_relationtype": "RelationType" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L5 | neighbors=[graph-store.ts]
- "lib_graph_store_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L8 | neighbors=[graph-store.ts]
- "lib_graph_store_target_ids": "TARGET_IDS" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L258 | neighbors=[graph-store.ts]
- "lib_httpx_parser_httpxjsonldecoder_malformedlines": ".malformedLines()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L112 | neighbors=[HttpxJsonlDecoder]
- "lib_httpx_parser_httpxlineparseresult": "HttpxLineParseResult" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L12 | neighbors=[httpx-parser.ts]
- "lib_job_store_job": "Job" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L8 | neighbors=[job-store.ts]
- "lib_job_store_jobs_file": "JOBS_FILE" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L4 | neighbors=[job-store.ts]
- "lib_job_store_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L6 | neighbors=[job-store.ts]
- "lib_naabu_parser_naaburaw": "NaabuRaw" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L9 | neighbors=[naabu-parser.ts]
- "lib_naabu_parser_naaburesult": "NaabuResult" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L3 | neighbors=[naabu-parser.ts]
- "lib_netexec_parser_netexechost": "NetExecHost" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L3 | neighbors=[netexec-parser.ts]
- "lib_netexec_parser_netexecparseresult": "NetExecParseResult" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L13 | neighbors=[netexec-parser.ts]
- "lib_nmap_parser_nmaphost": "NmapHost" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L18 | neighbors=[nmap-parser.ts]
- "lib_nmap_parser_nmapscriptresult": "NmapScriptResult" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L13 | neighbors=[nmap-parser.ts]
- "lib_nmap_parser_nmapservice": "NmapService" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L3 | neighbors=[nmap-parser.ts]
- "lib_nmap_parser_parser": "parser" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L27 | neighbors=[nmap-parser.ts]
- "lib_nuclei_parser_countbyseverity": "countBySeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L98 | neighbors=[nuclei-parser.ts]
- "lib_nuclei_parser_nucleiraw": "NucleiRaw" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L17 | neighbors=[nuclei-parser.ts]
- "lib_nuclei_parser_nucleirawline": "NucleiRawLine" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L82 | neighbors=[nuclei-parser.ts]
- "lib_openvas_client_cvsstoseverity": "cvssToSeverity()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L39 | neighbors=[openvas-client.ts]
- "lib_openvas_client_gettask": "getTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L31 | neighbors=[openvas-client.ts]
- "lib_openvas_client_isopenvasfinding": "isOpenVASFinding()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L54 | neighbors=[openvas-client.ts]
- "lib_openvas_client_openvashelperoutput": "OpenVASHelperOutput" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L47 | neighbors=[openvas-client.ts]
- "lib_openvas_client_openvastaskstate": "OpenVASTaskState" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L19 | neighbors=[openvas-client.ts]
- "lib_openvas_client_taskstore": "taskStore" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L29 | neighbors=[openvas-client.ts]
- "lib_permissions_store_data_path": "DATA_PATH" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L4 | neighbors=[permissions-store.ts]
- "lib_permissions_store_permissionsfile": "PermissionsFile" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L16 | neighbors=[permissions-store.ts]
- "lib_permissions_store_userrole": "UserRole" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L6 | neighbors=[permissions-store.ts]
- "lib_scan_events_broadcasttoscan": "broadcastToScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L20 | neighbors=[scan-events.ts]
- "lib_scan_events_callback": "Callback" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L3 | neighbors=[scan-events.ts]
- "lib_scan_events_scanlisteners": "scanListeners" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L5 | neighbors=[scan-events.ts]
- "lib_scan_events_subscribescan": "subscribeScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L7 | neighbors=[scan-events.ts]
- "lib_scan_pipeline_computeoverallprogress": "computeOverallProgress()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L114 | neighbors=[scan-pipeline.ts]
- "lib_scan_pipeline_createinitialpipelinestate": "createInitialPipelineState()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L84 | neighbors=[scan-pipeline.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-097.json

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
