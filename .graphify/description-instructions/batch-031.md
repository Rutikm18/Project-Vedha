# Node Description Batch 32 of 209

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

- "main_scripts_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "main_scripts_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L227 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "main_scripts_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L276 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "main_scripts_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …, test_main_scripts_vantage.py]
- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanJob, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 65f22a7 Add comprehensive tests for aut…, c4386e4 feat(customers): operator Custo…, d1b4dd3 trim frontend to 7 core pages; …, User, 298a9d4 trim frontend to 7 core pages; …]
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L138 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]
- "routers_agents_normalize_intensity_name": "_normalize_intensity_name()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L274 | neighbors=[agents.py, enqueue_agent_job(), ._validate_intensity(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L92 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…, Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L102 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L292 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), build_posture_report_section(), _set_job(), Background task: build the summary, gen…]
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[analytics.py, Asset, Engagement, FindingStatus, Finding, Service]
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L25 | neighbors=[findings.py, get_finding(), patch_finding(), Fetch a finding scoped to the caller's …, reopen_finding(), Fetch a finding scoped to the caller's …]
- "routers_portal_enum_val": "_enum_val()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L59 | neighbors=[portal.py, _metric_finding(), portal_engagement(), portal_scans(), _posture_view(), portal_posture()]
- "routers_probe_enrollment_secret_hash": "_secret_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L37 | neighbors=[probe_enrollment.py, activate_enrollment(), _authenticated_request(), create_enrollment_request(), generate_enroll_token(), refresh_device_token()]
- "scanner_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=probe/scanner/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/scanner/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "scanner_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "scanner_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "scanner_delta_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "scanner_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/scanner/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "scanner_findings_main": "_main()" | kind=code-symbol | source=probe/scanner/findings.py:L684 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…]
- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/scanner/host_discovery.py:L388 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._arp_table()]
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L395 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…]
- "scanner_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed(), Run masscan over the given target specs…, _parse_masscan_json()]
- "scanner_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, OSError, .__init__(), _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L232 | neighbors=[OSFingerprintScanner, build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…, Send one ICMP echo; return observed TTL…]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…, Listen-only discovery. No active probin…]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L368 | neighbors=[PortScanner, ._attempt(), .scan_target(), classify_os_error(), ._build(), ._maybe()]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L390 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…, Bounded worker-pool scan of every reque…, ._scan_port()]
- "scanner_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner]
- "scanner_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_run_all_main": "main()" | kind=code-symbol | source=probe/scanner/run_all.py:L88 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-031.json

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
