# Node Description Batch 74 of 336

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

- "main_scripts_os_fingerprint_parse_icmp_timestamps": "parse_icmp_timestamps()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L108 | neighbors=[os_fingerprint.py, ._icmp_timestamp(), _strip_ip_header(), Parse an ICMP timestamp reply (type 14)…]
- "main_scripts_os_fingerprint_remote_clock": "remote_clock()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L121 | neighbors=[os_fingerprint.py, ._icmp_scan_target(), Interpret a timestamp reply's transmit …, .scan_target()]
- "main_scripts_os_fingerprint_strip_ip_header": "_strip_ip_header()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L81 | neighbors=[os_fingerprint.py, parse_icmp_reply(), parse_icmp_timestamps(), Return (ttl, icmp_bytes). Raw-socket de…]
- "main_scripts_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…]
- "main_scripts_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…]
- "main_scripts_port_scanner_portscanner_is_ambiguous": "._is_ambiguous()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L614 | neighbors=[PortScanner, .scan_target(), True for the one state a retry can legi…, True for the one state a retry can legi…]
- "main_scripts_port_scanner_portscanner_reprobe_ambiguous": "._reprobe_ambiguous()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L619 | neighbors=[PortScanner, .scan_target(), Gentle second look at ports that stayed…, Gentle second look at ports that stayed…]
- "main_scripts_printer_scanner_build_ipp_get_printer_attributes": "build_ipp_get_printer_attributes()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L54 | neighbors=[printer_scanner.py, _ipp_attr(), ._probe_ipp(), A minimal IPP/1.1 Get-Printer-Attribute…]
- "main_scripts_printer_scanner_printerscanner_probe_pjl": "._probe_pjl()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L103 | neighbors=[PrinterScanner, ._probe(), parse_pjl_id(), _recv_bounded()]
- "main_scripts_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L42 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…, TPKT + X.224 Connection Request carryin…]
- "main_scripts_rsync_scanner_recv_until": "_recv_until()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L57 | neighbors=[rsync_scanner.py, _handshake(), ._list_modules(), ._test_anon()]
- "main_scripts_rsync_scanner_rsyncscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L130 | neighbors=[Blocking: list modules, then anon-test …, RsyncScanner, ._list_modules(), ._test_anon()]
- "main_scripts_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L244 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…]
- "main_scripts_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L497 | neighbors=[AdaptiveRateController, Current integer window (>= min_window)., Current integer window (>= min_window)., Current integer window (>= min_window).]
- "main_scripts_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L977 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "main_scripts_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L868 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…]
- "main_scripts_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L448 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "main_scripts_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L880 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…]
- "main_scripts_scanner_base_project_now": "project_now()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L85 | neighbors=[scanner_base.py, project_file_stamp(), project_timestamp(), Current time as an AWARE datetime in th…]
- "main_scripts_scanner_base_raise_fd_limit": "raise_fd_limit()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1044 | neighbors=[scanner_base.py, get_fd_limit(), Raise the soft fd limit toward the hard…, safe_connect_concurrency()]
- "main_scripts_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L680 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "main_scripts_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L311 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "main_scripts_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L404 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "main_scripts_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L421 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…]
- "main_scripts_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L416 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…]
- "main_scripts_service_enum_classify_roles": "classify_roles()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L389 | neighbors=[service_enum.py, Descriptive role tags from the open-por…, .scan_target(), Descriptive role tags from the open-por…]
- "main_scripts_service_enum_dns_read_name": "_dns_read_name()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L155 | neighbors=[service_enum.py, mdns_hostname(), Decode a DNS name (with 0xC0 compressio…, Decode a DNS name (with 0xC0 compressio…]
- "main_scripts_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L133 | neighbors=[service_enum.py, Everything learned about one target bey…, .scan_target(), Everything learned about one target bey…]
- "main_scripts_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L340 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target(), Best-effort OS guess from voluntary evi…]
- "main_scripts_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L424 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …, Directly-connected subnets and default …]
- "main_scripts_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L176 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …, Ask the host over multicast DNS (5353) …]
- "main_scripts_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L203 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…, NetBIOS first-level name encoding (16-b…]
- "main_scripts_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L213 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…, NBNS node-status (NBSTAT) query to UDP/…]
- "main_scripts_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L244 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target(), Run the three name sources concurrently…]
- "main_scripts_smb_enum_scanner_enum_shares": "_enum_shares()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L87 | neighbors=[smb_enum_scanner.py, _decode(), List SMB shares over the null session. …, ._enumerate()]
- "main_scripts_smb_enum_scanner_enum_users_ridcycle": "_enum_users_ridcycle()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L148 | neighbors=[smb_enum_scanner.py, _decode(), RID-cycling fallback via LSAT: resolve …, ._enumerate()]
- "main_scripts_smb_enum_scanner_enum_users_samr": "_enum_users_samr()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L102 | neighbors=[smb_enum_scanner.py, _decode(), Enumerate domain/local users via the SA…, ._enumerate()]
- "main_scripts_smb_scanner_parse_ntlm_challenge": "parse_ntlm_challenge()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L176 | neighbors=[smb_scanner.py, ntlm_os_build(), windows_release_from_build(), Parse an NTLMSSP CHALLENGE (Type-2) out…]
- "main_scripts_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L38 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target(), Read signing posture from a SUCCESSFUL …]
- "main_scripts_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L403 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-073.json

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
