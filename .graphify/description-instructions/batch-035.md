# Node Description Batch 36 of 236

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

- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L138 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]
- "routers_agents_list_intensities": "list_intensities()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L618 | neighbors=[agents.py, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…, The numeric scan-hardness scale: 1 ligh…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L92 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…, Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L102 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L292 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), build_posture_report_section(), _set_job(), Background task: build the summary, gen…]
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[analytics.py, Asset, Engagement, FindingStatus, Finding, Service]
- "routers_customer_access_generate_password": "generate_password()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L95 | neighbors=[customer_access.py, patch_client_user(), provision_client_user(), A URL-safe temporary password the opera…, A URL-safe temporary password the opera…, A URL-safe temporary password the opera…]
- "routers_customer_access_list_customers": "list_customers()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L394 | neighbors=[customer_access.py, CustomerListItem, Every provisioned customer login (role=…, Every provisioned customer login (role=…, Every provisioned customer login (role=…, Every provisioned customer login (role=…]
- "routers_customer_access_unique_portal_slug": "_unique_portal_slug()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L107 | neighbors=[customer_access.py, provision_client_user(), Per-tenant-unique portal slug: <base>, …, _slugify(), Per-tenant-unique portal slug: <base>, …, Per-tenant-unique portal slug: <base>, …]
- "routers_engagements_compute_overview": "_compute_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L41 | neighbors=[engagements.py, engagements_overview(), Shared aggregation — used by both the c…, _refresh_overview_cache(), Shared aggregation — used by both the c…, Shared aggregation — used by both the c…]
- "routers_engagements_engagements_overview": "engagements_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L399 | neighbors=[engagements.py, _compute_overview(), _overview_cache_key(), P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…]
- "routers_portal_enum_val": "_enum_val()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L77 | neighbors=[portal.py, _metric_finding(), portal_engagement(), portal_scans(), _posture_view(), portal_posture()]
- "routers_probe_enrollment_provision_agent_for_site": "_provision_agent_for_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L235 | neighbors=[probe_enrollment.py, approve_enrollment(), approve_request_simple(), create_enrollment_request(), Bind a request to a Site policy and cre…, Bind a request to a Site policy and cre…]
- "routers_probe_enrollment_secret_hash": "_secret_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L37 | neighbors=[probe_enrollment.py, activate_enrollment(), _authenticated_request(), create_enrollment_request(), generate_enroll_token(), refresh_device_token()]
- "scanner_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=probe/scanner/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/scanner/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "scanner_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "scanner_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "scanner_delta_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "scanner_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/scanner/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "scanner_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L307 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…, Combine TCP + neighbor signals into a c…]
- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/scanner/host_discovery.py:L391 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._arp_table()]
- "scanner_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "scanner_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L263 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line(), Bulk {ip: normalized_mac} snapshot of t…, ._arp_table(), Return {ip: normalized_mac} from the OS…]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed(), Run masscan over the given target specs…, _parse_masscan_json()]
- "scanner_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, OSError, .__init__(), _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "scanner_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L178 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …, Combine available stack signals into a …]
- "scanner_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…, Build an ICMP message (header + rest) w…]
- "scanner_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), os_family_from_ttl(), Round the observed TTL up to the neares…, Round the observed TTL up to the neares…]
- "scanner_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L270 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…, Listen-only discovery. No active probin…]
- "scanner_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L92 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L382 | neighbors=[PortScanner, ._attempt(), .scan_target(), classify_os_error(), ._build(), ._maybe()]
- "scanner_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner]
- "scanner_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_run_all_main": "main()" | kind=code-symbol | source=probe/scanner/run_all.py:L98 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]

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
