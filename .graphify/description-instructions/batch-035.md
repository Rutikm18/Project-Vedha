# Node Description Batch 36 of 104

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

- "lib_fetcher_clearauth": "clearAuth()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L42 | neighbors=[PageShell.tsx, fetcher.ts, fetchJson()]
- "lib_fetcher_errormessage": "errorMessage()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L111 | neighbors=[page.tsx, fetcher.ts, DataState.tsx]
- "lib_fetcher_getstoredtoken": "getStoredToken()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L20 | neighbors=[page.tsx, fetcher.ts, fetchJson()]
- "lib_fetcher_storetoken": "storeToken()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L30 | neighbors=[fetcher.ts, fetchJson(), page.tsx]
- "lib_finding_id_resetcounters": "resetCounters()" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L20 | neighbors=[finding-id.ts, findings-store.test.ts, parsers.test.ts]
- "lib_findings_store_deletefinding": "deleteFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L142 | neighbors=[findings-store.ts, ensureDir(), getAllFindings()]
- "lib_findings_store_getfindingsbyengagement": "getFindingsByEngagement()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L90 | neighbors=[route.ts, findings-store.ts, getAllFindings()]
- "lib_findings_store_getfindingstats": "getFindingStats()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L94 | neighbors=[findings-store.ts, getAllFindings(), findings-store.test.ts]
- "lib_graph_store_buildattackpaths": "buildAttackPaths()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L260 | neighbors=[graph-store.ts, edgesForPath(), scorePath()]
- "lib_job_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L20 | neighbors=[job-store.ts, readJobs(), writeJobs()]
- "lib_job_store_getalljobs": "getAllJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L94 | neighbors=[job-store.ts, readJobs(), route.ts]
- "lib_job_store_getjobbyscanid": "getJobByScanId()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L98 | neighbors=[job-store.ts, readJobs(), route.ts]
- "lib_job_store_markdispatched": "markDispatched()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L73 | neighbors=[job-store.ts, readJobs(), writeJobs()]
- "lib_job_store_updatejobstatus": "updateJobStatus()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L83 | neighbors=[job-store.ts, readJobs(), writeJobs()]
- "lib_naabu_parser_groupnaaburesults": "groupNaabuResults()" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L30 | neighbors=[tool-runners.ts, naabu-parser.ts, parsers.test.ts]
- "lib_naabu_parser_parsenaabuline": "parseNaabuLine()" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L16 | neighbors=[tool-runners.ts, naabu-parser.ts, parsers.test.ts]
- "lib_nmap_parser_extractscripts": "extractScripts()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L39 | neighbors=[nmap-parser.ts, toArray(), parseNmapXml()]
- "lib_nmap_parser_toarray": "toArray()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L34 | neighbors=[nmap-parser.ts, extractScripts(), parseNmapXml()]
- "lib_nuclei_parser_countbyseverity": "countBySeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L98 | neighbors=[nuclei-parser.ts, route.ts, route.ts]
- "lib_nuclei_parser_nucleirawline": "NucleiRawLine" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L82 | neighbors=[nuclei-parser.ts, route.ts, route.ts]
- "lib_openvas_client_runopenvasscanbackground": "runOpenVASScanBackground()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L61 | neighbors=[openvas-client.ts, setTask(), startOpenVASScan()]
- "lib_openvas_client_settask": "setTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L32 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), startOpenVASScan()]
- "lib_permissions_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L20 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_isadmin": "isAdmin()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L55 | neighbors=[permissions-store.ts, getUser(), route.ts]
- "lib_permissions_store_removeuser": "removeUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L91 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_updatescopes": "updateScopes()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L100 | neighbors=[permissions-store.ts, read(), write()]
- "lib_scan_pipeline_getpipeline": "getPipeline()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L67 | neighbors=[scan-pipeline.ts, route.ts, route.ts]
- "lib_target_parser_isvalidtarget": "isValidTarget()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L19 | neighbors=[target-parser.ts, validOctets(), parseTargets()]
- "lib_tenant_resolvetenantsubdomain": "resolveTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L45 | neighbors=[middleware.ts, tenant.ts, subdomainFromHost()]
- "lib_tenant_subdomainfromhost": "subdomainFromHost()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L22 | neighbors=[tenant.ts, resolveTenantSubdomain(), rootDomain()]
- "lib_testssl_parser_testssloutput": "TestsslOutput" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L26 | neighbors=[testssl-parser.ts, route.ts, route.ts]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…]
- "models_agent_recommendation_rationale_1": "agent_recommendation.py — decisions/actions proposed by the agentic AI advisor." | kind=entity | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[agent_recommendation.py, Base, TimestampMixin]
- "models_attack_timeline_rationale_12": "Append-only ledger of every attack action performed during an engagement.      W" | kind=entity | source=manager/backend/app/models/attack_timeline.py:L12 | neighbors=[AttackTimeline, Base, TimestampMixin]
- "models_detection_config_rationale_11": "Per-engagement SIEM + EDR connection settings used by the detection     validati" | kind=entity | source=manager/backend/app/models/detection_config.py:L11 | neighbors=[Base, TimestampMixin, DetectionConfig]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, DetectionRun, detection_run.py — one execution of the…]
- "models_detection_run_rationale_1": "detection_run.py — one execution of the deterministic detection engine over a fa" | kind=entity | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[Base, TimestampMixin, detection_run.py]
- "models_exploit_approval_rationale_20": "Created when a high-risk target requires manager sign-off.     Auto-queues the e" | kind=entity | source=manager/backend/app/models/exploit_approval.py:L20 | neighbors=[Base, TimestampMixin, ExploitApprovalRequest]
- "models_exploit_result_rationale_12": "Immutable record of every exploit attempt.     Never updated after creation — ap" | kind=entity | source=manager/backend/app/models/exploit_result.py:L12 | neighbors=[Base, TimestampMixin, ExploitResult]
- "models_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/models/finding.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, Finding]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-035.json

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
