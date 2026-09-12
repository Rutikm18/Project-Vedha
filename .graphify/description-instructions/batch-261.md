# Node Description Batch 262 of 380

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

- "native_http_probe_fingerprint": "fingerprint()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L108 | neighbors=[http-probe.ts]
- "native_http_probe_httpproberesult": "HttpProbeResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L79 | neighbors=[http-probe.ts]
- "native_http_probe_nativehttpopts": "NativeHttpOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L239 | neighbors=[http-probe.ts]
- "native_http_probe_probeone": "probeOne()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L143 | neighbors=[http-probe.ts]
- "native_http_probe_tech_rules": "TECH_RULES" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L38 | neighbors=[http-probe.ts]
- "native_http_probe_techrule": "TechRule" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L30 | neighbors=[http-probe.ts]
- "native_http_probe_web_port_proto": "WEB_PORT_PROTO" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L21 | neighbors=[http-probe.ts]
- "native_port_scan_checkopts": "CheckOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L159 | neighbors=[port-scan.ts]
- "native_port_scan_checkport": "checkPort()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L165 | neighbors=[port-scan.ts]
- "native_port_scan_expandtarget": "expandTarget()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L140 | neighbors=[port-scan.ts]
- "native_port_scan_nativeportresult": "NativePortResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L122 | neighbors=[port-scan.ts]
- "native_port_scan_nativescanopts": "NativeScanOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L209 | neighbors=[port-scan.ts]
- "native_port_scan_port_names": "PORT_NAMES" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L111 | neighbors=[port-scan.ts]
- "native_port_scan_portrange": "PortRange" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L129 | neighbors=[port-scan.ts]
- "native_port_scan_top_1000_tcp": "TOP_1000_TCP" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L23 | neighbors=[port-scan.ts]
- "native_tls_info_tlsinforesult": "TlsInfoResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L14 | neighbors=[tls-info.ts]
- "native_tls_info_weak_protocols": "WEAK_PROTOCOLS" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L36 | neighbors=[tls-info.ts]
- "native_tls_info_weak_signatures": "WEAK_SIGNATURES" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L35 | neighbors=[tls-info.ts]
- "ordereddict": "OrderedDict" | kind=code-symbol | neighbors=[TTLCache]
- "path_route_request_headers": "REQUEST_HEADERS" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L9 | neighbors=[route.ts]
- "path_route_response_headers": "RESPONSE_HEADERS" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L10 | neighbors=[route.ts]
- "path_route_routecontext": "RouteContext" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L7 | neighbors=[route.ts]
- "pathid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L5 | neighbors=[route.ts]
- "pats_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/pats/route.ts:L5 | neighbors=[route.ts]
- "pats_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/auth/pats/route.ts:L10 | neighbors=[route.ts]
- "portal_layout_nav": "NAV" | kind=code-symbol | source=manager/frontend/app/portal/layout.tsx:L7 | neighbors=[layout.tsx]
- "portal_layout_portallayout": "PortalLayout()" | kind=code-symbol | source=manager/frontend/app/portal/layout.tsx:L7 | neighbors=[layout.tsx]
- "portal_page_dashboardskeleton": "DashboardSkeleton()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L189 | neighbors=[page.tsx]
- "portal_page_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L16 | neighbors=[page.tsx]
- "portal_page_legend": "Legend()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L209 | neighbors=[page.tsx]
- "portal_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_page_panel": "Panel()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L27 | neighbors=[page.tsx]
- "portal_page_portaloverview": "PortalOverview()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L8 | neighbors=[page.tsx]
- "portal_page_queuestat": "QueueStat()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L218 | neighbors=[page.tsx]
- "portal_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L14 | neighbors=[page.tsx]
- "portal_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_portalshell_footerclock": "FooterClock()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L299 | neighbors=[PortalShell.tsx]
- "portal_portalshell_nav": "NAV" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L23 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalshellprops": "PortalShellProps" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L36 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalsidebar": "PortalSidebar()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L46 | neighbors=[PortalShell.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-261.json

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
