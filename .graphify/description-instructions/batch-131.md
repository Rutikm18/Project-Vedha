# Node Description Batch 132 of 332

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

- "lib_findings_store_getfindingsbyengagement": "getFindingsByEngagement()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L90 | neighbors=[findings-store.ts, getAllFindings()]
- "lib_findings_store_setdatapath": "setDataPath()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L13 | neighbors=[findings-store.ts, findings-store.test.ts]
- "lib_findings_store_sladeadline": "slaDeadline()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L27 | neighbors=[findings-store.ts, saveFindings()]
- "lib_graph_store_edgesforpath": "edgesForPath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L225 | neighbors=[graph-store.ts, buildAttackPaths()]
- "lib_graph_store_scorepath": "scorePath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L209 | neighbors=[graph-store.ts, buildAttackPaths()]
- "lib_httpx_parser_httpxjsonldecoder_finish": ".finish()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L106 | neighbors=[HttpxJsonlDecoder, .decode()]
- "lib_httpx_parser_httpxjsonldecoder_push": ".push()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L99 | neighbors=[HttpxJsonlDecoder, .decode()]
- "lib_httpx_parser_httpxjsonrecord": "HttpxJsonRecord" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[tool-runners.ts, httpx-parser.ts]
- "lib_httpx_parser_isoptionalnumber": "isOptionalNumber()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L37 | neighbors=[httpx-parser.ts, parseHttpxJsonLine()]
- "lib_httpx_parser_isoptionalstring": "isOptionalString()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L16 | neighbors=[httpx-parser.ts, parseHttpxJsonLine()]
- "lib_httpx_parser_normalizeport": "normalizePort()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L20 | neighbors=[httpx-parser.ts, parseHttpxJsonLine()]
- "lib_job_store_genjobid": "genJobId()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L37 | neighbors=[job-store.ts, createJob()]
- "lib_job_store_getalljobs": "getAllJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L94 | neighbors=[job-store.ts, readJobs()]
- "lib_job_store_getjobbyscanid": "getJobByScanId()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L98 | neighbors=[job-store.ts, readJobs()]
- "lib_job_store_getnextjobforagent": "getNextJobForAgent()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L62 | neighbors=[job-store.ts, readJobs()]
- "lib_netexec_parser_parseboolean": "parseBoolean()" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L24 | neighbors=[netexec-parser.ts, parseNetExecLog()]
- "lib_nuclei_parser_nucleimatch": "NucleiMatch" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L3 | neighbors=[nuclei-parser.ts, scan-pipeline.ts]
- "lib_nuclei_parser_nucleimatchtofinding": "nucleiMatchToFinding()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L84 | neighbors=[nuclei-parser.ts, nucleiSeverityToSeverity()]
- "lib_openvas_client_boundedenvms": "boundedEnvMs()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L100 | neighbors=[openvas-client.ts, runOpenVASScanBackground()]
- "lib_openvas_client_openvasfinding": "OpenVASFinding" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L4 | neighbors=[openvas-client.ts, scan-pipeline.ts]
- "lib_permissions_store_getallusers": "getAllUsers()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L40 | neighbors=[permissions-store.ts, read()]
- "lib_permissions_store_iptoint": "ipToInt()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L120 | neighbors=[permissions-store.ts, targetMatchesScope()]
- "lib_permissions_store_isadmin": "isAdmin()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L55 | neighbors=[permissions-store.ts, getUser()]
- "lib_permissions_store_permitteduser": "PermittedUser" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L8 | neighbors=[admin.ts, permissions-store.ts]
- "lib_permissions_store_targetmatchesscope": "targetMatchesScope()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L124 | neighbors=[permissions-store.ts, ipToInt()]
- "lib_portal_client_grade_style": "GRADE_STYLE" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L89 | neighbors=[portal-client.ts, page.tsx]
- "lib_portal_client_portalposture": "PortalPosture" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L51 | neighbors=[portal-client.ts, page.tsx]
- "lib_portal_client_portalreport": "PortalReport" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L70 | neighbors=[portal-client.ts, page.tsx]
- "lib_portal_client_portalusecase": "PortalUseCase" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L92 | neighbors=[portal-client.ts, page.tsx]
- "lib_portal_client_severity_style": "SEVERITY_STYLE" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L81 | neighbors=[page.tsx, portal-client.ts]
- "lib_scanner_request_validation_isvalidscannertarget": "isValidScannerTarget()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L46 | neighbors=[scanner-request-validation.ts, isValidHostname()]
- "lib_severity_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L44 | neighbors=[page.tsx, severity.ts]
- "lib_severity_epsscolor": "epssColor()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L72 | neighbors=[page.tsx, severity.ts]
- "lib_severity_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L56 | neighbors=[page.tsx, severity.ts]
- "lib_severity_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L40 | neighbors=[page.tsx, severity.ts]
- "lib_severity_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L48 | neighbors=[page.tsx, severity.ts]
- "lib_severity_priority_label": "PRIORITY_LABEL" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L52 | neighbors=[page.tsx, severity.ts]
- "lib_severity_sev": "sev()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L123 | neighbors=[severity.ts, toSeverity()]
- "lib_severity_sevvars": "sevVars()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L128 | neighbors=[Primitives.tsx, severity.ts]
- "lib_severity_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L28 | neighbors=[page.tsx, severity.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-131.json

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
