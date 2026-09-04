# Node Description Batch 137 of 330

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

- "native_dns_recon_attemptzonetransfer": "attemptZoneTransfer()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L96 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_dns_recon_nativeptrsweep": "nativePtrSweep()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L147 | neighbors=[dns-recon.ts, tool-runners.ts]
- "native_dns_recon_safe": "safe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L49 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_http_probe_nativehttpprobe": "nativeHttpProbe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L248 | neighbors=[tool-runners.ts, http-probe.ts]
- "native_port_scan_groupresults": "groupResults()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L261 | neighbors=[tool-runners.ts, port-scan.ts]
- "native_port_scan_resolveports": "resolvePorts()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L131 | neighbors=[port-scan.ts, nativePortScan()]
- "native_tls_info_nativetlsinfo": "nativeTlsInfo()" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L38 | neighbors=[tls-info.ts, tool-runners.ts]
- "oserror": "OSError" | kind=code-symbol | neighbors=[NmapExecutionError, NmapExecutionError]
- "path_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L45 | neighbors=[route.ts, proxy()]
- "path_route_patch": "PATCH()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/customer-access/[...path]/route.ts:L40 | neighbors=[route.ts, proxy()]
- "path_route_portaltoken": "portalToken()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L11 | neighbors=[route.ts, proxy()]
- "path_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L50 | neighbors=[route.ts, proxy()]
- "portal_timestamp_formatcompact": "formatCompact()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L35 | neighbors=[Timestamp.tsx, Timestamp()]
- "portal_timestamp_formatexact": "formatExact()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L23 | neighbors=[Timestamp.tsx, Timestamp()]
- "portal_timestamp_formatrelative": "formatRelative()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L47 | neighbors=[Timestamp.tsx, Timestamp()]
- "portal_timestamp_isoutc": "isoUtc()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L62 | neighbors=[Timestamp.tsx, Timestamp()]
- "portscan_family_of": "family_of()" | kind=code-symbol | source=portscan.py:L83 | neighbors=[portscan.py, ._attempt()]
- "portscan_parse_ports": "parse_ports()" | kind=code-symbol | source=portscan.py:L199 | neighbors=[portscan.py, main()]
- "portscan_portscanner_init": ".__init__()" | kind=code-symbol | source=portscan.py:L113 | neighbors=[PortScanner, RateLimiter]
- "portscan_portscanner_record": "._record()" | kind=code-symbol | source=portscan.py:L124 | neighbors=[PortScanner, ._attempt()]
- "portscan_ratelimiter_wait": ".wait()" | kind=code-symbol | source=portscan.py:L101 | neighbors=[.scan_port(), RateLimiter]
- "posture_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/posture/route.ts:L10 | neighbors=[route.ts, operator-routes.test.ts]
- "prompts_exploit_builder": "exploit-builder.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/exploit-builder.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "raw_facts_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L12 | neighbors=[route.ts, GET()]
- "raw_facts_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L17 | neighbors=[route.ts, fail()]
- "remediation_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L7 | neighbors=[route.ts, GET()]
- "remediation_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L15 | neighbors=[route.ts, fail()]
- "reopen_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L11 | neighbors=[route.ts, POST()]
- "reopen_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L16 | neighbors=[route.ts, fail()]
- "reports_page_cvsscolor": "cvssColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L76 | neighbors=[page.tsx, FindingCard()]
- "reports_page_cvssvector": "CvssVector()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L177 | neighbors=[page.tsx, parseCvssVector()]
- "reports_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L84 | neighbors=[page.tsx, ReportsPage()]
- "reports_page_parsecvss": "parseCvss()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L73 | neighbors=[page.tsx, FindingCard()]
- "reports_page_parsecvssvector": "parseCvssVector()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L83 | neighbors=[page.tsx, CvssVector()]
- "reports_page_portalreports": "PortalReports()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L705 | neighbors=[page.tsx, fmtDate()]
- "reports_page_reportcontent": "ReportContent" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L17 | neighbors=[page.tsx, PortalReport]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-136.json

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
