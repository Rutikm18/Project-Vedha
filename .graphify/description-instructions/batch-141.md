# Node Description Batch 142 of 336

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

- "scanner_dns_scanner_is_ip": "_is_ip()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L47 | neighbors=[dns_scanner.py, ._ptr_self()]
- "scanner_findings_finding_to_dict": ".to_dict()" | kind=code-symbol | source=probe/scanner/findings.py:L78 | neighbors=[Finding, _main()]
- "scanner_findings_tally": "_tally()" | kind=code-symbol | source=probe/scanner/findings.py:L1311 | neighbors=[findings.py, summarize()]
- "scanner_ftp_scanner_ftpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L152 | neighbors=[FTPScanner, .scan_target()]
- "scanner_ftp_scanner_ftpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L171 | neighbors=[FTPScanner, ._scan_port()]
- "scanner_host_discovery_now": "_now()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L392 | neighbors=[host_discovery.py, fuse_liveness()]
- "scanner_host_discovery_reverse_dns": "_reverse_dns()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L162 | neighbors=[host_discovery.py, PTR lookup; None on any failure. Runs i…]
- "scanner_host_discovery_state_for_confidence": "_state_for_confidence()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L396 | neighbors=[host_discovery.py, fuse_liveness()]
- "scanner_host_discovery_vendor_for_mac": "vendor_for_mac()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L233 | neighbors=[host_discovery.py, .scan_target()]
- "scanner_iot_scanner_parse_ssdp_headers": "_parse_ssdp_headers()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L49 | neighbors=[iot_scanner.py, _probe_ssdp_sync()]
- "scanner_iot_scanner_probe_mdns_sync": "_probe_mdns_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L190 | neighbors=[iot_scanner.py, _parse_mdns_response()]
- "scanner_iot_scanner_probe_rtsp": "_probe_rtsp()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L216 | neighbors=[iot_scanner.py, .scan_target()]
- "scanner_ipmi_scanner_ipmiscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L90 | neighbors=[IPMIScanner, .scan_target()]
- "scanner_ipmi_scanner_ipmiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L108 | neighbors=[IPMIScanner, ._scan_port()]
- "scanner_ipv6_discovery_main": "main()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L155 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts()]
- "scanner_ja4s_alpn_code": "_alpn_code()" | kind=code-symbol | source=probe/scanner/ja4s.py:L78 | neighbors=[ja4s.py, ja4s_from_fields()]
- "scanner_ja4s_version_str": "_version_str()" | kind=code-symbol | source=probe/scanner/ja4s.py:L52 | neighbors=[ja4s.py, ja4s_from_fields()]
- "scanner_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/scanner/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]
- "scanner_ldap_scanner_first": "_first()" | kind=code-symbol | source=probe/scanner/ldap_scanner.py:L40 | neighbors=[ldap_scanner.py, ._probe()]
- "scanner_ldap_scanner_ldapscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/ldap_scanner.py:L134 | neighbors=[LDAPScanner, .scan_target()]
- "scanner_ldap_scanner_ldapscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/ldap_scanner.py:L156 | neighbors=[LDAPScanner, ._scan_port()]
- "scanner_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]
- "scanner_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L229 | neighbors=[_ConnectSweep, ._probe()]
- "scanner_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L60 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=probe/scanner/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L206 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L316 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L183 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "scanner_msrpc_scanner_msrpcscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L144 | neighbors=[MSRPCScanner, .scan_target()]
- "scanner_msrpc_scanner_msrpcscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L167 | neighbors=[MSRPCScanner, ._scan_port()]
- "scanner_nfs_scanner_nfsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L259 | neighbors=[NFSScanner, .scan_target()]
- "scanner_nfs_scanner_nfsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L277 | neighbors=[NFSScanner, ._scan_port()]
- "scanner_nfs_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L156 | neighbors=[nfs_scanner.py, _recv_record()]
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L160 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L121 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()]
- "scanner_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-141.json

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
