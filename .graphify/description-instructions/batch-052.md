# Node Description Batch 53 of 104

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

- "scanner_fingerprint_firstline": "firstLine()" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L245 | neighbors=[fingerprint.go, Fingerprint()]
- "scanner_fingerprint_matchsignature": "matchSignature()" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L222 | neighbors=[fingerprint.go, Fingerprint()]
- "scanner_fingerprint_sanitize": "sanitize()" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L256 | neighbors=[fingerprint.go, Fingerprint()]
- "scanner_fingerprint_sendprobe": "sendProbe()" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L202 | neighbors=[fingerprint.go, Fingerprint()]
- "scanner_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L50 | neighbors=[HostDiscoveryScanner, ._probe()]
- "scanner_init": "__init__.py" | kind=code-symbol | source=probe/scanner/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, VA scanner module — pure collection/sca…]
- "scanner_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L146 | neighbors=[_ConnectSweep, .scan_target()]
- "scanner_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L162 | neighbors=[_ConnectSweep, ._probe()]
- "scanner_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L49 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L117 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L205 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L315 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L182 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L109 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_nmap_joinints": "joinInts()" | kind=code-symbol | source=probe-go/scanner/nmap.go:L125 | neighbors=[nmap.go, RunNmapVersion()]
- "scanner_nmap_nmapavailable": "NmapAvailable()" | kind=code-symbol | source=probe-go/scanner/nmap.go:L16 | neighbors=[nmap.go, RunNmapVersion()]
- "scanner_nmap_parsenmapxml": "parseNmapXML()" | kind=code-symbol | source=probe-go/scanner/nmap.go:L94 | neighbors=[nmap.go, RunNmapVersion()]
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L224 | neighbors=[passive_collector.py, ._select()]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L36 | neighbors=[PortScanner, .scan_target()]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L65 | neighbors=[PortScanner, ._scan_port()]
- "scanner_safe_backoff": "backoff()" | kind=code-symbol | source=probe-go/scanner/safe.go:L93 | neighbors=[safe.go, Retry()]
- "scanner_safe_dialcontext": "DialContext()" | kind=code-symbol | source=probe-go/scanner/safe.go:L198 | neighbors=[safe.go, Retry()]
- "scanner_safe_istransient": "IsTransient()" | kind=code-symbol | source=probe-go/scanner/safe.go:L104 | neighbors=[safe.go, Retry()]
- "scanner_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L378 | neighbors=[BaseScanner, RateLimiter]
- "scanner_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L386 | neighbors=[BaseScanner, ._guarded()]
- "scanner_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L280 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…]
- "scanner_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L292 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…]
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L190 | neighbors=[.run(), RateLimiter]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L265 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…]
- "scanner_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L350 | neighbors=[ResultWriter, run_cli()]
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L57 | neighbors=[.write(), ScanResult]
- "scanner_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L174 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard]
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L161 | neighbors=[ScopeGuard, .in_scope()]
- "scanner_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L169 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard]
- "scanner_scope_newscopeguard": "NewScopeGuard()" | kind=code-symbol | source=probe-go/scanner/scope.go:L18 | neighbors=[scope.go, ScopeFromFile()]
- "scanner_scope_scopefromfile": "ScopeFromFile()" | kind=code-symbol | source=probe-go/scanner/scope.go:L65 | neighbors=[scope.go, NewScopeGuard()]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L42 | neighbors=[ServiceBannerScanner, .scan_target()]
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L97 | neighbors=[ServiceBannerScanner, ._grab()]
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()]
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-052.json

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
