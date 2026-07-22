# Node Description Batch 42 of 76

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

- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L36 | neighbors=[PortScanner, .scan_target()]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L65 | neighbors=[PortScanner, ._scan_port()]
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
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L42 | neighbors=[ServiceBannerScanner, .scan_target()]
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L97 | neighbors=[ServiceBannerScanner, ._grab()]
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()]
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L56 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L91 | neighbors=[SMBScanner, _netbios_session()]
- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L30 | neighbors=[snmp_scanner.py, ._query()]
- "scanner_snmp_scanner_extract_sysdescr": "_extract_sysdescr()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L44 | neighbors=[snmp_scanner.py, .scan_target()]
- "scanner_snmp_scanner_snmpscanner_query": "._query()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L84 | neighbors=[SNMPScanner, _build_get()]
- "scanner_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L100 | neighbors=[SNMPScanner, _extract_sysdescr()]
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]
- "scanner_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L95 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "scanner_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L162 | neighbors=[TLSScanner, .scan_target()]
- "scanner_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L180 | neighbors=[TLSScanner, ._scan_port()]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L87 | neighbors=[UDPScanner, .scan_target()]
- "scanner_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L130 | neighbors=[UDPScanner, ._probe()]
- "scanner_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/web_scanner.py:L41 | neighbors=[web_scanner.py, .redirect_request()]
- "scanner_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L119 | neighbors=[WebScanner, .scan_target()]
- "scanner_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L136 | neighbors=[WebScanner, ._scan_port()]
- "scanner_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "scanner_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "schemas_auth_loginrequest": "LoginRequest" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L9 | neighbors=[auth.py, BaseModel]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-041.json

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
