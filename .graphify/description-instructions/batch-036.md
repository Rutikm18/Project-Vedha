# Node Description Batch 37 of 336

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

- "lib_httpx_parser_httpxjsonldecoder": "HttpxJsonlDecoder" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L93 | neighbors=[tool-runners.ts, httpx-parser.ts, .decode(), .finish(), .malformedLines(), .push()]
- "lib_security_context_securitycontexterror": "SecurityContextError" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L9 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), resolveSecurityReference()]
- "main_scripts_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L159 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "main_scripts_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L206 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "main_scripts_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…]
- "main_scripts_dns_scanner_dnsscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L178 | neighbors=[DNSScanner, derive_zones(), ._axfr(), ._chaos_txt(), ._dnssec_present(), ._ptr_self()]
- "main_scripts_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1082 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "main_scripts_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1129 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "main_scripts_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1112 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "main_scripts_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1089 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "main_scripts_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1225 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…, Derive findings from collected facts. P…]
- "main_scripts_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L406 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + UDP + neighbor signals in…, Combine TCP + neighbor signals into a c…]
- "main_scripts_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L498 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._udp_liveness()]
- "main_scripts_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L569 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), ._udp_liveness(), is_locally_administered()]
- "main_scripts_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L301 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "main_scripts_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()]
- "main_scripts_ja4x": "ja4x.py" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious()]
- "main_scripts_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L199 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L237 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()]
- "main_scripts_msrpc_scanner": "msrpc_scanner.py" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _extract_tcp_ports(), main(), MSRPCScanner, _summarize()]
- "main_scripts_nfs_scanner_parse_mount_export": "parse_mount_export()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L96 | neighbors=[nfs_scanner.py, ._mount_export(), is_world_readable(), _XDR, .string(), .u32()]
- "main_scripts_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L48 | neighbors=[nmap_wrapper.py, .__init__(), OSError, _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "main_scripts_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), match_stack_signature(), os_family_from_ttl(), Round the observed TTL up to the neares…]
- "main_scripts_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()]
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L110 | neighbors=[run_all.py, _advertised_dynamic_ports(), _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl()]
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L162 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), reconcile_ports(), route_ports()]
- "main_scripts_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L817 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…]
- "main_scripts_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L429 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…]
- "main_scripts_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L266 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …]
- "main_scripts_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L235 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…, Soft-match collected bytes to {service,…]
- "main_scripts_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L558 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()]
- "main_scripts_smb_enum_scanner_smbenumscanner_enumerate": "._enumerate()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L227 | neighbors=[Blocking: attempt a null session and en…, SMBEnumScanner, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _merge_users()]
- "main_scripts_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L224 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…, Keyed 32-bit ISN for (dst_ip, dst_port,…]
- "main_scripts_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L231 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…, A genuine reply to our SYN acknowledges…]
- "main_scripts_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L275 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "main_scripts_va_campaign_build_campaign": "build_campaign()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L620 | neighbors=[va_campaign.py, CampaignContext, default_stages(), ProgressReporter, VACampaign, Wire a campaign with the real scanners …]
- "main_scripts_va_campaign_cliprogressview": "CliProgressView" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L649 | neighbors=[va_campaign.py, .__call__(), ._format(), .__init__(), ._redraw(), ._transitions()]
- "main_scripts_va_campaign_progressreporter_flush": "._flush()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L265 | neighbors=[ProgressReporter, .finish(), _atomic_write_json(), .snapshot(), .__init__(), .mark()]
- "me_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, backend(), withBackend(), GET, 298a9d4 trim frontend to 7 core pages; …, backend.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-036.json

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
