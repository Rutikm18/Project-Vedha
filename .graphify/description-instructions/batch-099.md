# Node Description Batch 100 of 134

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "logout_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/logout/route.ts:L4 | neighbors=[route.ts] | lang=en
- "me_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L10 | neighbors=[route.ts] | lang=en
- "models_base_uuidmixin": "UUIDMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L25 | neighbors=[base.py] | lang=en
- "models_probe_enrollment_rationale_73": "Pre-authorized, Site-bound enrollment token.      Lets a probe auto-enroll (no o" | kind=entity | source=manager/backend/app/models/probe_enrollment.py:L73 | neighbors=[ProbeEnrollmentToken] | lang=pt
- "models_scan_job_attempt_rationale_12": "One immutable, fenced execution claim for a logical scan job." | kind=entity | source=manager/backend/app/models/scan_job_attempt.py:L12 | neighbors=[ScanJobAttempt] | lang=en
- "native_dir_bust_builtin_paths": "BUILTIN_PATHS" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L16 | neighbors=[dir-bust.ts] | lang=en
- "native_dir_bust_dirbustresult": "DirBustResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L57 | neighbors=[dir-bust.ts] | lang=en
- "native_dir_bust_nativediropts": "NativeDirOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L90 | neighbors=[dir-bust.ts] | lang=en
- "native_dir_bust_proberesp": "ProbeResp" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L66 | neighbors=[dir-bust.ts] | lang=en
- "native_dns_recon_common_subdomains": "COMMON_SUBDOMAINS" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L33 | neighbors=[dns-recon.ts] | lang=en
- "native_dns_recon_dnsreconresult": "DnsReconResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L15 | neighbors=[dns-recon.ts] | lang=en
- "native_dns_recon_ptrsweepresult": "PtrSweepResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L28 | neighbors=[dns-recon.ts] | lang=en
- "native_http_probe_extracttitle": "extractTitle()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L103 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_fingerprint": "fingerprint()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L108 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_httpproberesult": "HttpProbeResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L79 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_nativehttpopts": "NativeHttpOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L239 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_probeone": "probeOne()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L143 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_tech_rules": "TECH_RULES" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L38 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_techrule": "TechRule" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L30 | neighbors=[http-probe.ts] | lang=en
- "native_http_probe_web_port_proto": "WEB_PORT_PROTO" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L21 | neighbors=[http-probe.ts] | lang=en
- "native_port_scan_checkopts": "CheckOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L159 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_checkport": "checkPort()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L165 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_expandtarget": "expandTarget()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L140 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_nativeportresult": "NativePortResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L122 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_nativescanopts": "NativeScanOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L209 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_port_names": "PORT_NAMES" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L111 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_portrange": "PortRange" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L129 | neighbors=[port-scan.ts] | lang=en
- "native_port_scan_top_1000_tcp": "TOP_1000_TCP" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L23 | neighbors=[port-scan.ts] | lang=en
- "native_tls_info_tlsinforesult": "TlsInfoResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L14 | neighbors=[tls-info.ts] | lang=en
- "native_tls_info_weak_protocols": "WEAK_PROTOCOLS" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L36 | neighbors=[tls-info.ts] | lang=en
- "native_tls_info_weak_signatures": "WEAK_SIGNATURES" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L35 | neighbors=[tls-info.ts] | lang=en
- "ordereddict": "OrderedDict" | kind=code-symbol | neighbors=[TTLCache] | lang=en
- "oserror": "OSError" | kind=code-symbol | neighbors=[NmapExecutionError] | lang=en
- "pathid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L5 | neighbors=[route.ts] | lang=en
- "probe_pipeline_collector_init": ".__init__()" | kind=code-symbol | source=probe/pipeline.py:L122 | neighbors=[_Collector] | lang=en
- "probe_pipeline_ip_key": "_ip_key()" | kind=code-symbol | source=probe/pipeline.py:L243 | neighbors=[pipeline.py] | lang=en
- "probe_pipeline_main": "main()" | kind=code-symbol | source=probe/pipeline.py:L356 | neighbors=[pipeline.py] | lang=en
- "probe_pipeline_rationale_133": "Make a per-host scanner instance share ONE rate limiter + semaphore with all" | kind=entity | source=probe/pipeline.py:L133 | neighbors=[_shared()] | lang=en
- "probe_pipeline_rationale_252": "Make a raw banner safe and readable for the summary line.      Many services ans" | kind=entity | source=probe/pipeline.py:L252 | neighbors=[_clean()] | lang=en
- "probe_pipeline_render_summary": "_render_summary()" | kind=code-symbol | source=probe/pipeline.py:L316 | neighbors=[pipeline.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-099.json

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
