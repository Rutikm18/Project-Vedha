# Node Description Batch 13 of 92

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

- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=main_scripts/windows_collector.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "scanner_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=scanner/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=scanner/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "scanner_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=scanner/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "scanner_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=scanner/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "scanner_delta_scanner_main": "main()" | kind=code-symbol | source=scanner/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "scanner_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=scanner/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "scanner_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=scanner/findings.py:L689 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner(), DNS server hygiene: a full AXFR zone tr…]
- "scanner_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=scanner/findings.py:L776 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner(), Confirmed FTP anonymous access (upgrade…]
- "scanner_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=scanner/findings.py:L874 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner(), IPMI/BMC exposure. Cipher-zero is a cri…]
- "scanner_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=scanner/findings.py:L651 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner(), Anonymous LDAP exposure. An anonymous R…]
- "scanner_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=scanner/findings.py:L940 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner(), Windows RPC endpoint-mapper disclosure …]
- "scanner_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=scanner/findings.py:L739 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner(), NFS anonymous export exposure. A world-…]
- "scanner_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=scanner/findings.py:L967 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner(), Exposed network printer — an informatio…]
- "scanner_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=scanner/findings.py:L535 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner(), Confirmed RDP (X.224 handshake) + NLA d…]
- "scanner_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=scanner/findings.py:L805 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner(), rsync daemon exposure. Anonymously-sele…]
- "scanner_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=scanner/findings.py:L600 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner(), Anonymous SMB (null-session) informatio…]
- "scanner_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=scanner/findings.py:L906 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner(), SMTP hygiene: VRFY/EXPN user enumeratio…]
- "scanner_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=scanner/findings.py:L467 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner(), JA4X-based threat-intel match. Fires on…]
- "scanner_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=scanner/findings.py:L515 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner(), JA4S-based threat-intel match on the TL…]
- "scanner_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=scanner/findings.py:L489 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner(), Proven UNAUTHENTICATED access to a data…]
- "scanner_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=scanner/findings.py:L843 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner(), VNC/RFB authentication exposure. 'None'…]
- "scanner_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/host_discovery.py:L416 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), is_locally_administered(), vendor_for_mac()]
- "scanner_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=scanner/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=scanner/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, OSError, .__init__(), _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=scanner/os_fingerprint.py:L298 | neighbors=[OSFingerprintScanner, accept_echo_reply(), build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…]
- "scanner_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=scanner/rdp_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner]
- "scanner_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=scanner/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_run_all_main": "main()" | kind=code-symbol | source=scanner/run_all.py:L98 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]
- "scanner_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=scanner/scan_funnel.py:L142 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
- "scanner_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=scanner/scanner_base.py:L725 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=scanner/scanner_base.py:L695 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=scanner/service_banner.py:L123 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=scanner/service_enum.py:L449 | neighbors=[service_enum.py, BaseScanner, .__init__(), ._open(), ._probe_port(), .scan_target()]
- "scanner_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=scanner/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=scanner/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "scanner_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=scanner/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=scanner/ssh_collector.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-012.json

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
