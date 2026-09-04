# Node Description Batch 73 of 330

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

- "main_scripts_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L174 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…, JSON-typed body that actually talks abo…]
- "main_scripts_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L152 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…, Server/body fingerprint match against k…]
- "main_scripts_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L161 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…, The strongest possible evidence for a r…]
- "main_scripts_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "main_scripts_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), Detects mobile device exposure on the n…]
- "main_scripts_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]
- "main_scripts_msrpc_scanner_summarize": "_summarize()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L69 | neighbors=[msrpc_scanner.py, ._enumerate(), Reduce the raw endpoint list to distinc…, _extract_tcp_ports()]
- "main_scripts_nfs_scanner_nfsscanner_mount_export": "._mount_export()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L221 | neighbors=[NFSScanner, ._rpc(), parse_mount_export(), ._probe()]
- "main_scripts_nfs_scanner_nfsscanner_portmap_dump": "._portmap_dump()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L203 | neighbors=[NFSScanner, ._rpc(), parse_portmap_dump(), ._probe()]
- "main_scripts_nfs_scanner_recv_record": "_recv_record()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L136 | neighbors=[nfs_scanner.py, Read RPC record-marking fragments (RFC …, _recv_exact(), _rpc_call()]
- "main_scripts_nfs_scanner_xdr_u32": ".u32()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L63 | neighbors=[parse_mount_export(), parse_portmap_dump(), _XDR, .opaque()]
- "main_scripts_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L320 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…]
- "main_scripts_os_fingerprint_match_stack_signature": "match_stack_signature()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L202 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl(), p0f-style match on (initial TTL, option…]
- "main_scripts_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L482 | neighbors=[OSFingerprintScanner, ._icmp_scan_target(), fingerprint_os(), remote_clock()]
- "main_scripts_os_fingerprint_osfingerprintscanner_tcp_ttl_result": "._tcp_ttl_result()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L468 | neighbors=[OSFingerprintScanner, ._icmp_scan_target(), fingerprint_os(), FIX 3b: aliveness/TTL came from a TCP S…]
- "main_scripts_os_fingerprint_parse_icmp_timestamps": "parse_icmp_timestamps()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L108 | neighbors=[os_fingerprint.py, ._icmp_timestamp(), _strip_ip_header(), Parse an ICMP timestamp reply (type 14)…]
- "main_scripts_os_fingerprint_remote_clock": "remote_clock()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L121 | neighbors=[os_fingerprint.py, ._icmp_scan_target(), Interpret a timestamp reply's transmit …, .scan_target()]
- "main_scripts_os_fingerprint_strip_ip_header": "_strip_ip_header()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L81 | neighbors=[os_fingerprint.py, parse_icmp_reply(), parse_icmp_timestamps(), Return (ttl, icmp_bytes). Raw-socket de…]
- "main_scripts_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…]
- "main_scripts_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-072.json

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
