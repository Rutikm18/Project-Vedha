# Node Description Batch 97 of 134

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

- "lib_errors_adversaerror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L65 | neighbors=[AdversaError]
- "lib_errors_adversaerror_render": ".render()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L94 | neighbors=[AdversaError]
- "lib_errors_adversaerror_tojson": ".toJSON()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L76 | neighbors=[AdversaError]
- "lib_errors_adversaerroropts": "AdversaErrorOpts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L48 | neighbors=[errors.ts]
- "lib_errors_errorcode": "ErrorCode" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L14 | neighbors=[errors.ts]
- "lib_errors_vedhaerror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L65 | neighbors=[VedhaError]
- "lib_errors_vedhaerror_render": ".render()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L94 | neighbors=[VedhaError]
- "lib_errors_vedhaerror_tojson": ".toJSON()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L76 | neighbors=[VedhaError]
- "lib_errors_vedhaerroropts": "VedhaErrorOpts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L48 | neighbors=[errors.ts]
- "lib_exploit_store_approvals": "approvals" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L78 | neighbors=[exploit-store.ts]
- "lib_exploit_store_approvalstatus": "ApprovalStatus" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L3 | neighbors=[exploit-store.ts]
- "lib_exploit_store_auditentry": "AuditEntry" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L54 | neighbors=[exploit-store.ts]
- "lib_exploit_store_auditlog": "auditLog" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L79 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitapprovalrequest": "ExploitApprovalRequest" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L36 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitevidence": "ExploitEvidence" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L5 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitjob": "ExploitJob" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L20 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitresult": "ExploitResult" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L13 | neighbors=[exploit-store.ts]
- "lib_exploit_store_exploitstore": "exploitStore" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L81 | neighbors=[exploit-store.ts]
- "lib_exploit_store_genid": "genId()" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L68 | neighbors=[exploit-store.ts]
- "lib_exploit_store_jobs": "jobs" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L77 | neighbors=[exploit-store.ts]
- "lib_exploit_store_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L2 | neighbors=[exploit-store.ts]
- "lib_exploit_store_nowiso": "nowIso()" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L72 | neighbors=[exploit-store.ts]
- "lib_exploit_store_payloadtype": "PayloadType" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[exploit-store.ts]
- "lib_fetcher_apierror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L10 | neighbors=[ApiError]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-096.json

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
