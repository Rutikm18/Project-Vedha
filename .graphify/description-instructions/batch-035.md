# Node Description Batch 36 of 380

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

- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L24 | neighbors=[xml_parser.py, ._parse_host(), .open_ports(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "enum": "Enum" | kind=code-symbol | neighbors=[models.py, FindingState, SourceConfidence, verifier.py, agent.py, enums.py]
- "jobs_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/route.ts:L1 | neighbors=[25c014d feat: enhance campaign progress…, b393dbe feat: Enhance Sidebar UI and in…, f3bb8db feat(manager): cross-worker WS …, GET, backend.ts, backend()]
- "lib_ai_engine_generatereport": "generateReport()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L809 | neighbors=[route.ts, ai-engine.ts, generateReportSectioned(), generateReportSingleCall(), getClient(), stripFences()]
- "lib_assistant_access": "assistant-access.ts" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L1 | neighbors=[AssistantProvider.tsx, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, AssistantAuthState, canMountAssistant()]
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()]
- "lib_settings_workspace_api": "settings-workspace-api.ts" | kind=code-symbol | source=manager/frontend/lib/settings-workspace-api.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, fetcher.ts, fetchJson(), portal-client.ts, portalApi(), createSettingsWorkspaceApi()]
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, proxy.ts, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost()]
- "main_scripts_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L162 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()]
- "main_scripts_nfs_scanner_xdr": "_XDR" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L56 | neighbors=[nfs_scanner.py, parse_mount_export(), parse_portmap_dump(), Minimal, BOUNDED big-endian XDR reader …, .__init__(), .opaque()]
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L405 | neighbors=[OSFingerprintScanner, accept_echo_reply(), build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…]
- "main_scripts_printer_scanner_printerscanner": "PrinterScanner" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L96 | neighbors=[printer_scanner.py, BaseScanner, .__init__(), ._probe(), ._probe_ipp(), ._probe_pjl()]
- "main_scripts_rsync_scanner": "rsync_scanner.py" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _handshake(), main(), parse_modules(), _recv_until()]
- "main_scripts_rsync_scanner_rsyncscanner": "RsyncScanner" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L93 | neighbors=[rsync_scanner.py, BaseScanner, .__init__(), ._list_modules(), ._probe(), ._scan_port()]
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L129 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "main_scripts_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L839 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…]
- "main_scripts_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L366 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), ._connect(), ._read_some(), One probe-ladder rung on its own connec…]
- "main_scripts_smtp_scanner_smtpscanner": "SMTPScanner" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L60 | neighbors=[smtp_scanner.py, BaseScanner, ._cmd(), .__init__(), ._probe(), ._read_response()]
- "main_scripts_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]
- "main_scripts_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L181 | neighbors=[syn_scanner.py, parse_tcp_options(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking(), _parse_mss(), Parse a raw IPv4+TCP packet (as receive…]
- "main_scripts_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L201 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…]
- "main_scripts_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L262 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…]
- "main_scripts_va_campaign_progressreporter_snapshot": ".snapshot()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L246 | neighbors=[ProgressReporter, ._flush(), _now(), ._current(), ._eta_seconds(), ._percent()]
- "main_scripts_vnc_scanner": "vnc_scanner.py" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, classify_security_types(), main(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "main_scripts_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 8f6bf49 Refactor code structure and rem…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanJob, _stamp_reference()]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L139 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), _ineligibility_reason(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L93 | neighbors=[agents.py, _agent_can_execute_job(), _ineligibility_reason(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L103 | neighbors=[agents.py, _agent_can_execute_job(), _ineligibility_reason(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…]
- "routers_attack_paths_rationale_1": "Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path" | kind=entity | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[attack_paths.py, PathAnalyzer, GraphBuilder, GraphVisualizer, Asset, AttackPath]
- "routers_probe_enrollment_create_enrollment_request": "create_enrollment_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L361 | neighbors=[probe_enrollment.py, _decode_public_key(), enroll_token_is_usable(), _get_or_create_auto_enroll_site(), _keyed_hash(), _provision_agent_for_site()]
- "scanner_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L162 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()]
- "scanner_findings_main": "_main()" | kind=code-symbol | source=probe/scanner/findings.py:L1335 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…]
- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/scanner/host_discovery.py:L498 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._udp_liveness()]
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L516 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…]
- "scanner_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L569 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), ._udp_liveness(), is_locally_administered()]
- "scanner_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()]
- "scanner_msrpc_scanner": "msrpc_scanner.py" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _extract_tcp_ports(), main(), MSRPCScanner, _summarize()]
- "scanner_nfs_scanner_xdr": "_XDR" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L56 | neighbors=[nfs_scanner.py, parse_mount_export(), parse_portmap_dump(), Minimal, BOUNDED big-endian XDR reader …, .__init__(), .opaque()]
- "scanner_printer_scanner_printerscanner": "PrinterScanner" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L96 | neighbors=[printer_scanner.py, BaseScanner, .__init__(), ._probe(), ._probe_ipp(), ._probe_pjl()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-035.json

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
