# Node Description Batch 89 of 119

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

- "lib_security_context_securitycontexterror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L11 | neighbors=[SecurityContextError]
- "lib_severity_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L17 | neighbors=[severity.ts]
- "lib_severity_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L16 | neighbors=[severity.ts]
- "lib_severity_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L14 | neighbors=[severity.ts]
- "lib_severity_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L13 | neighbors=[severity.ts]
- "lib_target_parser_common_ranges": "COMMON_RANGES" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L132 | neighbors=[target-parser.ts]
- "lib_target_parser_isprivaterange": "isPrivateRange()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L35 | neighbors=[target-parser.ts]
- "lib_target_parser_parseresult": "ParseResult" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L59 | neighbors=[target-parser.ts]
- "lib_target_parser_rfc1918": "RFC1918" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L6 | neighbors=[target-parser.ts]
- "lib_target_parser_toapitargets": "toApiTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L127 | neighbors=[target-parser.ts]
- "lib_tenant_reserved": "RESERVED" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L15 | neighbors=[tenant.ts]
- "lib_testssl_parser_skip_severity": "SKIP_SEVERITY" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L12 | neighbors=[testssl-parser.ts]
- "lib_testssl_parser_testsslissue": "TestsslIssue" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L4 | neighbors=[testssl-parser.ts]
- "lib_testssl_parser_testssloutput": "TestsslOutput" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L26 | neighbors=[testssl-parser.ts]
- "lib_testssl_parser_testsslparseresult": "TestsslParseResult" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L28 | neighbors=[testssl-parser.ts]
- "lib_whatweb_parser_whatwebparseresult": "WhatWebParseResult" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L6 | neighbors=[whatweb-parser.ts]
- "lib_whatweb_parser_whatwebresult": "WhatWebResult" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L1 | neighbors=[whatweb-parser.ts]
- "lib_with_backend_backendctx": "BackendCtx" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L12 | neighbors=[with-backend.ts]
- "lib_with_backend_handler": "Handler" | kind=code-symbol | source=manager/frontend/lib/with-backend.ts:L16 | neighbors=[with-backend.ts]
- "login_page_loginform": "LoginForm()" | kind=code-symbol | source=manager/frontend/app/login/page.tsx:L18 | neighbors=[page.tsx]
- "login_page_loginpage": "LoginPage()" | kind=code-symbol | source=manager/frontend/app/login/page.tsx:L10 | neighbors=[page.tsx]
- "logout_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/logout/route.ts:L4 | neighbors=[route.ts]
- "me_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L10 | neighbors=[route.ts]
- "models_base_uuidmixin": "UUIDMixin" | kind=code-symbol | source=manager/backend/app/models/base.py:L25 | neighbors=[base.py]
- "native_dir_bust_builtin_paths": "BUILTIN_PATHS" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L16 | neighbors=[dir-bust.ts]
- "native_dir_bust_dirbustresult": "DirBustResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L57 | neighbors=[dir-bust.ts]
- "native_dir_bust_nativediropts": "NativeDirOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L90 | neighbors=[dir-bust.ts]
- "native_dir_bust_proberesp": "ProbeResp" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L66 | neighbors=[dir-bust.ts]
- "native_dns_recon_common_subdomains": "COMMON_SUBDOMAINS" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L33 | neighbors=[dns-recon.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-088.json

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
