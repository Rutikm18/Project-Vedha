# Node Description Batch 35 of 236

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

- "main_scripts_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…, test_main_scripts_device.py]
- "main_scripts_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/main_scripts/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "main_scripts_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1029 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "main_scripts_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1012 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "main_scripts_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/main_scripts/findings.py:L989 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "main_scripts_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1125 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…, Derive findings from collected facts. P…]
- "main_scripts_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L307 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…, Combine TCP + neighbor signals into a c…]
- "main_scripts_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L416 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), is_locally_administered(), vendor_for_mac()]
- "main_scripts_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "main_scripts_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "main_scripts_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, .__init__(), OSError, _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "main_scripts_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L178 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …, Combine available stack signals into a …]
- "main_scripts_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…, Build an ICMP message (header + rest) w…]
- "main_scripts_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), os_family_from_ttl(), Round the observed TTL up to the neares…, Round the observed TTL up to the neares…]
- "main_scripts_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L404 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…, Bounded worker-pool scan of every reque…, Bounded worker-pool scan of every reque…]
- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner]
- "main_scripts_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L98 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L142 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
- "main_scripts_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L596 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…]
- "main_scripts_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L365 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…]
- "main_scripts_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L200 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …]
- "main_scripts_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L91 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…, Soft-match collected bytes to {service,…]
- "main_scripts_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L123 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), ._rung(), .scan_target()]
- "main_scripts_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L449 | neighbors=[service_enum.py, BaseScanner, .__init__(), ._open(), ._probe_port(), .scan_target()]
- "main_scripts_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "main_scripts_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "main_scripts_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L151 | neighbors=[syn_scanner.py, _parse_mss(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking(), Parse a raw IPv4+TCP packet (as receive…, Parse a raw IPv4+TCP packet (as receive…]
- "main_scripts_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L190 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…, Keyed 32-bit ISN for (dst_ip, dst_port,…]
- "main_scripts_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L197 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…, A genuine reply to our SYN acknowledges…]
- "main_scripts_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "main_scripts_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L227 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "main_scripts_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L277 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "main_scripts_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …, test_main_scripts_vantage.py]
- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanJob, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "portal_portalshell_portalshell": "PortalShell()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L118 | neighbors=[page.tsx, page.tsx, PortalShell.tsx, page.tsx, page.tsx, page.tsx]
- "reveal_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/[id]/reveal/route.ts:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, backend.ts, backend(), BackendError, bearerFrom(), GET()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-034.json

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
