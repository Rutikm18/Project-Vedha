# Node Description Batch 38 of 332

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

- "routers_agents_rationale_425": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L425 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service]
- "routers_agents_rationale_444": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L444 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service]
- "routers_agents_rationale_706": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L706 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service]
- "routers_agents_rationale_90": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L90 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L93 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…, Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L103 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_analytics_exposureanalytics": "ExposureAnalytics" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L40 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L30 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L35 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_engagements_compute_overview": "_compute_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L67 | neighbors=[engagements.py, engagements_overview(), Shared aggregation — used by both the c…, _refresh_overview_cache(), Shared aggregation — used by both the c…, Shared aggregation — used by both the c…]
- "routers_engagements_engagements_overview": "engagements_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L425 | neighbors=[engagements.py, _compute_overview(), _overview_cache_key(), P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…]
- "routers_findings_rationale_25": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L25 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_26": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L26 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_48": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L48 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_49": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L49 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_probe_enrollment_activate_enrollment": "activate_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L684 | neighbors=[probe_enrollment.py, _authenticated_request(), _derive_refresh_secret(), _policy(), _rate_limit(), _secret_hash()]
- "scanner_cpe": "cpe.py" | kind=code-symbol | source=probe/scanner/cpe.py:L1 | neighbors=[6e2818f Add support for additional serv…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _extract_version(), to_cpe(), cpe.py — derive a CPE 2.3 identity from…]
- "scanner_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L159 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "scanner_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L206 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "scanner_dns_scanner": "dns_scanner.py" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, derive_zones(), DNSScanner, _is_ip(), main(), dns_scanner.py — DNS server hygiene: zo…]
- "scanner_dns_scanner_dnsscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L178 | neighbors=[DNSScanner, derive_zones(), ._axfr(), ._chaos_txt(), ._dnssec_present(), ._ptr_self()]
- "scanner_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/scanner/findings.py:L1082 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()]
- "scanner_ftp_scanner": "ftp_scanner.py" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, banner_software(), FTPScanner, main(), parse_pasv(), ftp_scanner.py — FTP anonymous-access c…]
- "scanner_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L406 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + UDP + neighbor signals in…, Combine TCP + neighbor signals into a c…]
- "scanner_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L301 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "scanner_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L362 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line(), Bulk {ip: normalized_mac} snapshot of t…, Bulk {ip: normalized_mac} snapshot of t…, ._arp_table()]
- "scanner_ipmi_scanner": "ipmi_scanner.py" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_open_session_request(), IPMIScanner, main(), parse_open_session_response(), ipmi_scanner.py — IPMI 2.0 cipher-zero …]
- "scanner_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=probe/scanner/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()]
- "scanner_ja4x": "ja4x.py" | kind=code-symbol | source=probe/scanner/ja4x.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious()]
- "scanner_ldap_scanner": "ldap_scanner.py" | kind=code-symbol | source=probe/scanner/ldap_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _first(), LDAPScanner, main(), ldap_scanner.py — LDAP anonymous-bind e…]
- "scanner_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L199 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()]
- "scanner_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L237 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()]
- "scanner_nfs_scanner_parse_mount_export": "parse_mount_export()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L96 | neighbors=[nfs_scanner.py, ._mount_export(), is_world_readable(), _XDR, .string(), .u32()]
- "scanner_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L48 | neighbors=[nmap_wrapper.py, OSError, .__init__(), _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "scanner_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), match_stack_signature(), os_family_from_ttl(), Round the observed TTL up to the neares…]
- "scanner_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L337 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…, p0f-style match on (initial TTL, option…]
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()]
- "scanner_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L175 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L519 | neighbors=[PortScanner, ._attempt(), One port's terminal result, gated by th…, .scan_target(), classify_os_error(), ._build()]
- "scanner_run_all_main": "main()" | kind=code-symbol | source=probe/scanner/run_all.py:L110 | neighbors=[run_all.py, _advertised_dynamic_ports(), _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-037.json

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
