# Node Description Batch 135 of 186

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

- "main_scripts_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "main_scripts_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/main_scripts/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "main_scripts_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/main_scripts/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "main_scripts_web_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L165 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L55 | neighbors=[_NoRedirect] | lang=en
- "main_scripts_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/main_scripts/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "main_scripts_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "main_scripts_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L138 | neighbors=[WebScanner] | lang=en
- "main_scripts_windows_collector_main": "main()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/main_scripts/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "main_scripts_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "main_scripts_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "me_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L10 | neighbors=[route.ts] | lang=en
- "models_base_uuidmixin": "UUIDMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L25 | neighbors=[base.py] | lang=en
- "models_probe_enrollment_rationale_73": "Pre-authorized, Site-bound enrollment token.      Lets a probe auto-enroll (no o" | kind=entity | source=manager/backend/app/models/probe_enrollment.py:L73 | neighbors=[ProbeEnrollmentToken] | lang=pt
- "models_scan_job_attempt_rationale_12": "One immutable, fenced execution claim for a logical scan job." | kind=entity | source=manager/backend/app/models/scan_job_attempt.py:L12 | neighbors=[ScanJobAttempt] | lang=en
- "models_validation_request_rationale_1": "validation_request.py — an approval-gated request to safely re-check a finding l" | kind=entity | source=manager/backend/app/models/validation_request.py:L1 | neighbors=[validation_request.py] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-134.json

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
