# Node Description Batch 48 of 336

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

- "scanner_delta_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L319 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "scanner_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/scanner/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "scanner_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/scanner/findings.py:L1129 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "scanner_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/scanner/findings.py:L1112 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "scanner_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/scanner/findings.py:L1089 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "scanner_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=probe/scanner/findings.py:L707 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner(), DNS server hygiene: a full AXFR zone tr…]
- "scanner_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=probe/scanner/findings.py:L794 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner(), Confirmed FTP anonymous access (upgrade…]
- "scanner_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=probe/scanner/findings.py:L892 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner(), IPMI/BMC exposure. Cipher-zero is a cri…]
- "scanner_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=probe/scanner/findings.py:L669 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner(), Anonymous LDAP exposure. An anonymous R…]
- "scanner_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=probe/scanner/findings.py:L958 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner(), Windows RPC endpoint-mapper disclosure …]
- "scanner_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=probe/scanner/findings.py:L757 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner(), NFS anonymous export exposure. A world-…]
- "scanner_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=probe/scanner/findings.py:L985 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner(), Exposed network printer — an informatio…]
- "scanner_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/scanner/findings.py:L535 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner(), Confirmed RDP (X.224 handshake) + NLA d…]
- "scanner_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=probe/scanner/findings.py:L823 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner(), rsync daemon exposure. Anonymously-sele…]
- "scanner_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=probe/scanner/findings.py:L618 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner(), Anonymous SMB (null-session) informatio…]
- "scanner_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=probe/scanner/findings.py:L924 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner(), SMTP hygiene: VRFY/EXPN user enumeratio…]
- "scanner_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/scanner/findings.py:L467 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner(), JA4X-based threat-intel match. Fires on…]
- "scanner_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/scanner/findings.py:L515 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner(), JA4S-based threat-intel match on the TL…]
- "scanner_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/scanner/findings.py:L489 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner(), Proven UNAUTHENTICATED access to a data…]
- "scanner_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=probe/scanner/findings.py:L861 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner(), VNC/RFB authentication exposure. 'None'…]
- "scanner_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/scanner/findings.py:L1225 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…, Derive findings from collected facts. P…]
- "scanner_ftp_scanner_ftpscanner_list_bounded": "._list_bounded()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L128 | neighbors=[FTPScanner, ._cmd(), ._read_response(), parse_pasv(), ._probe(), Confirm anonymous READ via PASV + LIST,…]
- "scanner_ftp_scanner_ftpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L95 | neighbors=[FTPScanner, banner_software(), ._cmd(), ._list_bounded(), ._read_response(), Blocking: greeting → anonymous login → …]
- "scanner_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L239 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …, Best-effort device classification from …, Best-effort device classification from …]
- "scanner_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L222 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…]
- "scanner_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L208 | neighbors=[host_discovery.py, parse_nbstat(), parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "scanner_ipmi_scanner_ipmiscanner": "IPMIScanner" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L65 | neighbors=[ipmi_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_ipv6_discovery_discover_ipv6_hosts": "discover_ipv6_hosts()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L118 | neighbors=[ipv6_discovery.py, _own_ipv6_addresses(), _ping_all_nodes(), _read_neighbor_cache(), main(), Discover live IPv6 neighbors on the seg…]
- "scanner_ldap_scanner_ldapscanner": "LDAPScanner" | kind=code-symbol | source=probe/scanner/ldap_scanner.py:L47 | neighbors=[ldap_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed(), Run masscan over the given target specs…, _parse_masscan_json()]
- "scanner_msrpc_scanner_msrpcscanner": "MSRPCScanner" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L82 | neighbors=[msrpc_scanner.py, BaseScanner, ._enumerate(), .__init__(), ._scan_port(), .scan_target()]
- "scanner_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…, Build an ICMP message (header + rest) w…]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L436 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…, Send an ICMP timestamp request (type 13…]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…, Listen-only discovery. No active probin…]
- "scanner_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L267 | neighbors=[.scan_target(), Tally exactly one terminal per-port obs…, ScanMetrics, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…]
- "scanner_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), probe_rdp_posture(), One synchronous RDP handshake offering …, One synchronous RDP handshake. Best-eff…]
- "scanner_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L135 | neighbors=[rdp_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), main()]
- "scanner_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/scanner/run_all.py:L59 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log(), Run one scanner module as a subprocess,…, Run one scanner module as a subprocess,…]
- "scanner_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L497 | neighbors=[AdaptiveRateController, Current integer window (>= min_window)., Current integer window (>= min_window)., Current integer window (>= min_window)., Full, debuggable classification for att…, Current integer window (>= min_window).]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
