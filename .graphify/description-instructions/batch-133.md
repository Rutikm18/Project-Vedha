# Node Description Batch 134 of 336

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
- "main_scripts_accuracy_expected_keys": "_expected_keys()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L37 | neighbors=[accuracy.py, score_findings()]
- "main_scripts_accuracy_finding_key": "_finding_key()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L31 | neighbors=[accuracy.py, score_findings()]
- "main_scripts_accuracy_format_report": "format_report()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L145 | neighbors=[accuracy.py, _main()]
- "main_scripts_accuracy_gate_format_gate_report": "format_gate_report()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L175 | neighbors=[accuracy_gate.py, _main()]
- "main_scripts_adaptive_timeout_adaptivetimeout_timeout": ".timeout()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L44 | neighbors=[AdaptiveTimeout, Current timeout: base until we have a s…]
- "main_scripts_db_scanner_dbscanner_probe_one": "._probe_one()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L247 | neighbors=[DBScanner, ._scan_port()]
- "main_scripts_db_scanner_dbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L281 | neighbors=[DBScanner, ._scan_port()]
- "main_scripts_db_scanner_probe_redis": "_probe_redis()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L114 | neighbors=[db_scanner.py, interpret_redis_info()]
- "main_scripts_delta_scanner_delta_to_dict": ".to_dict()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L87 | neighbors=[Delta, main()]
- "main_scripts_delta_scanner_deltaengine_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L290 | neighbors=[DeltaEngine, main()]
- "main_scripts_dns_scanner_dnsscanner_chaos_txt": "._chaos_txt()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L98 | neighbors=[DNSScanner, ._probe()]
- "main_scripts_dns_scanner_dnsscanner_dnssec_present": "._dnssec_present()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L161 | neighbors=[DNSScanner, ._probe()]
- "main_scripts_dns_scanner_dnsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L215 | neighbors=[DNSScanner, .scan_target()]
- "main_scripts_dns_scanner_dnsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L237 | neighbors=[DNSScanner, ._scan_port()]
- "main_scripts_dns_scanner_is_ip": "_is_ip()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L47 | neighbors=[dns_scanner.py, ._ptr_self()]
- "main_scripts_findings_finding_to_dict": ".to_dict()" | kind=code-symbol | source=probe/main_scripts/findings.py:L78 | neighbors=[Finding, _main()]
- "main_scripts_findings_rationale_619": "Anonymous SMB (null-session) information disclosure. The null session is a     m" | kind=entity | source=probe/main_scripts/findings.py:L619 | neighbors=[_rule_smb_enum(), load_facts_jsonl()]
- "main_scripts_findings_tally": "_tally()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1311 | neighbors=[findings.py, summarize()]
- "main_scripts_ftp_scanner_ftpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L152 | neighbors=[FTPScanner, .scan_target()]
- "main_scripts_ftp_scanner_ftpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L171 | neighbors=[FTPScanner, ._scan_port()]
- "main_scripts_host_discovery_now": "_now()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L392 | neighbors=[host_discovery.py, fuse_liveness()]
- "main_scripts_host_discovery_reverse_dns": "_reverse_dns()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L162 | neighbors=[host_discovery.py, PTR lookup; None on any failure. Runs i…]
- "main_scripts_host_discovery_state_for_confidence": "_state_for_confidence()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L396 | neighbors=[host_discovery.py, fuse_liveness()]
- "main_scripts_host_discovery_vendor_for_mac": "vendor_for_mac()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L233 | neighbors=[host_discovery.py, .scan_target()]
- "main_scripts_init": "__init__.py" | kind=code-symbol | source=probe/main_scripts/__init__.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, VA scanner module — pure collection/sca…]
- "main_scripts_iot_scanner_parse_ssdp_headers": "_parse_ssdp_headers()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L49 | neighbors=[iot_scanner.py, _probe_ssdp_sync()]
- "main_scripts_iot_scanner_probe_mdns_sync": "_probe_mdns_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L190 | neighbors=[iot_scanner.py, _parse_mdns_response()]
- "main_scripts_iot_scanner_probe_rtsp": "_probe_rtsp()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L216 | neighbors=[iot_scanner.py, .scan_target()]
- "main_scripts_ipmi_scanner_ipmiscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L90 | neighbors=[IPMIScanner, .scan_target()]
- "main_scripts_ipmi_scanner_ipmiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L108 | neighbors=[IPMIScanner, ._scan_port()]
- "main_scripts_ipv6_discovery_main": "main()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L155 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts()]
- "main_scripts_ja4s_alpn_code": "_alpn_code()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L78 | neighbors=[ja4s.py, ja4s_from_fields()]
- "main_scripts_ja4s_version_str": "_version_str()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L52 | neighbors=[ja4s.py, ja4s_from_fields()]
- "main_scripts_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-133.json

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
