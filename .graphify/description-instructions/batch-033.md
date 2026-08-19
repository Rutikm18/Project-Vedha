# Node Description Batch 34 of 227

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

- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner]
- "main_scripts_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L88 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L98 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L131 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
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
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L138 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]
- "routers_agents_normalize_intensity_name": "_normalize_intensity_name()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L274 | neighbors=[agents.py, enqueue_agent_job(), ._validate_intensity(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L92 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…, Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L102 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L292 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), build_posture_report_section(), _set_job(), Background task: build the summary, gen…]
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[analytics.py, Asset, Engagement, FindingStatus, Finding, Service]
- "routers_customer_access_generate_password": "generate_password()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L95 | neighbors=[customer_access.py, patch_client_user(), provision_client_user(), A URL-safe temporary password the opera…, A URL-safe temporary password the opera…, A URL-safe temporary password the opera…]
- "routers_customer_access_list_customers": "list_customers()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L394 | neighbors=[customer_access.py, CustomerListItem, Every provisioned customer login (role=…, Every provisioned customer login (role=…, Every provisioned customer login (role=…, Every provisioned customer login (role=…]
- "routers_customer_access_unique_portal_slug": "_unique_portal_slug()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L107 | neighbors=[customer_access.py, provision_client_user(), Per-tenant-unique portal slug: <base>, …, _slugify(), Per-tenant-unique portal slug: <base>, …, Per-tenant-unique portal slug: <base>, …]
- "routers_portal_enum_val": "_enum_val()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L77 | neighbors=[portal.py, _metric_finding(), portal_engagement(), portal_scans(), _posture_view(), portal_posture()]
- "routers_probe_enrollment_provision_agent_for_site": "_provision_agent_for_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L235 | neighbors=[probe_enrollment.py, approve_enrollment(), approve_request_simple(), create_enrollment_request(), Bind a request to a Site policy and cre…, Bind a request to a Site policy and cre…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-033.json

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
