# Node Description Batch 95 of 131

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

- "lib_finding_id_counters": "counters" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L11 | neighbors=[finding-id.ts]
- "lib_finding_id_sev_prefix": "SEV_PREFIX" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L3 | neighbors=[finding-id.ts]
- "lib_findings_store_default_data_path": "DEFAULT_DATA_PATH" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L9 | neighbors=[findings-store.ts]
- "lib_findings_store_isduplicate": "isDuplicate()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L43 | neighbors=[findings-store.ts]
- "lib_findings_store_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L15 | neighbors=[findings-store.ts]
- "lib_graph_store_adj": "ADJ" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L238 | neighbors=[graph-store.ts]
- "lib_graph_store_adjacency": "adjacency()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L182 | neighbors=[graph-store.ts]
- "lib_graph_store_attack_paths": "ATTACK_PATHS" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L301 | neighbors=[graph-store.ts]
- "lib_graph_store_attackpath": "AttackPath" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L39 | neighbors=[graph-store.ts]
- "lib_graph_store_bfspath": "bfsPath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L194 | neighbors=[graph-store.ts]
- "lib_graph_store_bfsreach": "bfsReach()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L194 | neighbors=[graph-store.ts]
- "lib_graph_store_blastradiusresult": "BlastRadiusResult" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L64 | neighbors=[graph-store.ts]
- "lib_graph_store_buildchokepoints": "buildChokepoints()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L304 | neighbors=[graph-store.ts]
- "lib_graph_store_builddemograph": "buildDemoGraph()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L73 | neighbors=[graph-store.ts]
- "lib_graph_store_chokepoint": "Chokepoint" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L53 | neighbors=[graph-store.ts]
- "lib_graph_store_chokepoints": "CHOKEPOINTS" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L327 | neighbors=[graph-store.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-094.json

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
