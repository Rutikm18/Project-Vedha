# Node Description Batch 61 of 131

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

- "lib_tenant_rootdomain": "rootDomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L17 | neighbors=[tenant.ts, subdomainFromHost()]
- "lib_tenant_server_clientfromrequest": "clientFromRequest()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L16 | neighbors=[tenant-server.ts, readTenantSubdomain()]
- "lib_tenant_server_currentclient": "currentClient()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L26 | neighbors=[tenant-server.ts, tenantSubdomain()]
- "lib_tenant_server_readtenantsubdomain": "readTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L12 | neighbors=[tenant-server.ts, clientFromRequest()]
- "lib_tenant_server_tenantsubdomain": "tenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L21 | neighbors=[tenant-server.ts, currentClient()]
- "lib_testssl_parser_parsetestssloutput": "parseTestsslOutput()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L34 | neighbors=[testssl-parser.ts, parseTestsslJson()]
- "login_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L33 | neighbors=[route.ts, setSessionCookies()]
- "login_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L75 | neighbors=[route.ts, setSessionCookies()]
- "models_audit_log_rationale_12": "Immutable, append-only audit trail for all exploit actions.     No TimestampMixi" | kind=entity | source=manager/backend/app/models/audit_log.py:L12 | neighbors=[AuditLog, Base]
- "models_probe_site": "probe_site.py" | kind=code-symbol | source=manager/backend/app/models/probe_site.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, ProbeSite]
- "models_scan_job_attempt": "scan_job_attempt.py" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, ScanJobAttempt]
- "native_dir_bust_loadwordlist": "loadWordlist()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L97 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dir_bust_probe": "probe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L71 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dns_recon_attemptzonetransfer": "attemptZoneTransfer()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L96 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_dns_recon_nativeptrsweep": "nativePtrSweep()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L147 | neighbors=[dns-recon.ts, tool-runners.ts]
- "native_dns_recon_safe": "safe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L49 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_http_probe_nativehttpprobe": "nativeHttpProbe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L248 | neighbors=[tool-runners.ts, http-probe.ts]
- "native_port_scan_groupresults": "groupResults()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L261 | neighbors=[tool-runners.ts, port-scan.ts]
- "native_port_scan_resolveports": "resolvePorts()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L131 | neighbors=[port-scan.ts, nativePortScan()]
- "native_tls_info_nativetlsinfo": "nativeTlsInfo()" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L38 | neighbors=[tls-info.ts, tool-runners.ts]
- "probe_pipeline_collector_write": ".write()" | kind=code-symbol | source=probe/pipeline.py:L126 | neighbors=[_Collector, _run_active()]
- "probe_push_results_die": "die()" | kind=code-symbol | source=probe/push_results.py:L29 | neighbors=[push_results.py, main()]
- "probe_push_results_load_facts": "load_facts()" | kind=code-symbol | source=probe/push_results.py:L34 | neighbors=[push_results.py, main()]
- "probe_run_scan_main": "main()" | kind=code-symbol | source=probe/run_scan.py:L135 | neighbors=[run_scan.py, _orchestrate()]
- "probe_run_scan_orchestrate": "_orchestrate()" | kind=code-symbol | source=probe/run_scan.py:L62 | neighbors=[run_scan.py, main()]
- "probe_selftest_live_check": "check()" | kind=code-symbol | source=probe/selftest_live.py:L38 | neighbors=[selftest_live.py, main()]
- "probe_selftest_live_fact": "_fact()" | kind=code-symbol | source=probe/selftest_live.py:L81 | neighbors=[selftest_live.py, main()]
- "probe_selftest_live_free_port": "_free_port()" | kind=code-symbol | source=probe/selftest_live.py:L69 | neighbors=[selftest_live.py, main()]
- "probe_showcase_run_list_use_cases": "list_use_cases()" | kind=code-symbol | source=probe/showcase_run.py:L39 | neighbors=[showcase_run.py, main()]
- "probe_showcase_run_print_summary": "_print_summary()" | kind=code-symbol | source=probe/showcase_run.py:L49 | neighbors=[showcase_run.py, main()]
- "probe_showcase_run_split": "_split()" | kind=code-symbol | source=probe/showcase_run.py:L35 | neighbors=[showcase_run.py, main()]
- "prompts_exploit_builder": "exploit-builder.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/exploit-builder.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "reports_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L84 | neighbors=[page.tsx, ReportsPage()]
- "reports_page_reportspage": "ReportsPage()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L297 | neighbors=[page.tsx, formatDate()]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L681 | neighbors=[agents.py, _agent_ownership_check()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-060.json

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
