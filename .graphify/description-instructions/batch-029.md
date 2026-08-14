# Node Description Batch 30 of 186

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

- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L91 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…, Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L101 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L292 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), build_posture_report_section(), _set_job(), Background task: build the summary, gen…]
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[analytics.py, Asset, Engagement, FindingStatus, Finding, Service]
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L25 | neighbors=[findings.py, get_finding(), patch_finding(), Fetch a finding scoped to the caller's …, reopen_finding(), Fetch a finding scoped to the caller's …]
- "routers_probe_enrollment_secret_hash": "_secret_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L36 | neighbors=[probe_enrollment.py, activate_enrollment(), _authenticated_request(), create_enrollment_request(), generate_enroll_token(), refresh_device_token()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/scanner/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "scanner_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "scanner_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "scanner_delta_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/scanner/host_discovery.py:L388 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._arp_table()]
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L395 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…]
- "scanner_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed(), Run masscan over the given target specs…, _parse_masscan_json()]
- "scanner_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, OSError, .__init__(), _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L232 | neighbors=[OSFingerprintScanner, build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…, Send one ICMP echo; return observed TTL…]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…, Listen-only discovery. No active probin…]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L346 | neighbors=[PortScanner, ._attempt(), .scan_target(), classify_os_error(), ._build(), ._maybe()]
- "scanner_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L98 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "scanner_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L131 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
- "scanner_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L567 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…]
- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L399 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli(), Accepts CIDRs ('10.0.0.0/24'), single I…, Accepts CIDRs ('10.0.0.0/24'), single I…, A self-tuning concurrency window, model…]
- "scanner_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L579 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…]
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L120 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), ._rung(), .scan_target()]
- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community(), ._query()]
- "scanner_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "scanner_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "scanner_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L227 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version(), Never send an IP literal as SNI — non-c…, Never send an IP literal as SNI — non-c…]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L155 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni(), Attempt a handshake forcing one protoco…, Attempt a handshake forcing one protoco…]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "schemas_ai_aigeneraterequest": "AiGenerateRequest" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L18 | neighbors=[ai.py, BaseModel, .validate_bounded_input(), AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_finding_findingout": "FindingOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L68 | neighbors=[finding.py, BaseModel, ._populate_risk_rank(), DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_seed_with_retry": "_seed_with_retry()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L294 | neighbors=[seed_admin.py, main(), Exponential-backoff retry for transient…, log_error(), log_warn(), _seed_once()]
- "services_llm_managerllmservice_fallback_candidates": "._fallback_candidates()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L300 | neighbors=[ManagerLlmService, ._default_runtime(), ._runtime(), Runtime, .generate_with_fallback(), Ordered runtimes to try: requested/defa…]
- "services_llm_managerllmservice_runtime": "._runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L114 | neighbors=[ManagerLlmService, ._fallback_candidates(), .generate(), AiRuntimeError, _is_local_ollama_model(), Runtime]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-029.json

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
