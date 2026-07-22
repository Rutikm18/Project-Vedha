# Node Description Batch 63 of 76

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

- "native_dns_recon_dnsreconresult": "DnsReconResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L15 | neighbors=[dns-recon.ts]
- "native_dns_recon_ptrsweepresult": "PtrSweepResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L28 | neighbors=[dns-recon.ts]
- "native_http_probe_extracttitle": "extractTitle()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L103 | neighbors=[http-probe.ts]
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
- "netexec_route_nxchost": "NxcHost" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L10 | neighbors=[route.ts]
- "nmap_route_createvulnfindings": "createVulnFindings()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L166 | neighbors=[route.ts]
- "nmap_route_nse_vuln_map": "NSE_VULN_MAP" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L77 | neighbors=[route.ts]
- "nmap_route_nsescript": "NseScript" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L8 | neighbors=[route.ts]
- "nmap_route_scan_profiles": "SCAN_PROFILES" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L66 | neighbors=[route.ts]
- "nmap_route_scanhost": "ScanHost" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L34 | neighbors=[route.ts]
- "nmap_route_scanport": "ScanPort" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L20 | neighbors=[route.ts]
- "nmap_route_scanresult": "ScanResult" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L46 | neighbors=[route.ts]
- "nmap_route_vulnref": "VulnRef" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L13 | neighbors=[route.ts]
- "nuclei_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/nuclei/route.ts:L11 | neighbors=[route.ts]
- "openvas_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/openvas/route.ts:L7 | neighbors=[route.ts]
- "ordereddict": "OrderedDict" | kind=code-symbol | neighbors=[TTLCache]
- "pathid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L5 | neighbors=[route.ts]
- "probe_pipeline_collector_init": ".__init__()" | kind=code-symbol | source=probe/pipeline.py:L122 | neighbors=[_Collector]
- "probe_pipeline_ip_key": "_ip_key()" | kind=code-symbol | source=probe/pipeline.py:L243 | neighbors=[pipeline.py]
- "probe_pipeline_main": "main()" | kind=code-symbol | source=probe/pipeline.py:L356 | neighbors=[pipeline.py]
- "probe_pipeline_rationale_133": "Make a per-host scanner instance share ONE rate limiter + semaphore with all" | kind=entity | source=probe/pipeline.py:L133 | neighbors=[_shared()]
- "probe_pipeline_rationale_252": "Make a raw banner safe and readable for the summary line.      Many services ans" | kind=entity | source=probe/pipeline.py:L252 | neighbors=[_clean()]
- "probe_pipeline_render_summary": "_render_summary()" | kind=code-symbol | source=probe/pipeline.py:L316 | neighbors=[pipeline.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-062.json

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
