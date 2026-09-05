# Node Description Batch 39 of 336

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
- "scanner_run_all_main": "main()" | kind=code-symbol | source=probe/scanner/run_all.py:L110 | neighbors=[run_all.py, _advertised_dynamic_ports(), _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl()]
- "scanner_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L162 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), reconcile_ports(), route_ports()]
- "scanner_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L848 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L680 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "scanner_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/scanner/service_banner.py:L235 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…, Soft-match collected bytes to {service,…]
- "scanner_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_enum.py:L558 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()]
- "scanner_smb_enum_scanner_smbenumscanner_enumerate": "._enumerate()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L227 | neighbors=[Blocking: attempt a null session and en…, SMBEnumScanner, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _merge_users()]
- "scanner_smtp_scanner": "smtp_scanner.py" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, main(), parse_ehlo_capabilities(), SMTPScanner, vrfy_leaks(), smtp_scanner.py — SMTP hygiene: user en…]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]
- "scanner_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L224 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…, Keyed 32-bit ISN for (dst_ip, dst_port,…]
- "scanner_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L231 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…, A genuine reply to our SYN acknowledges…]
- "scanner_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L275 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L165 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni(), Attempt a handshake forcing one protoco…, Attempt a handshake forcing one protoco…]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L282 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "scanner_va_campaign_build_campaign": "build_campaign()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L620 | neighbors=[va_campaign.py, CampaignContext, default_stages(), ProgressReporter, VACampaign, Wire a campaign with the real scanners …]
- "scanner_va_campaign_cliprogressview": "CliProgressView" | kind=code-symbol | source=probe/scanner/va_campaign.py:L649 | neighbors=[va_campaign.py, .__call__(), ._format(), .__init__(), ._redraw(), ._transitions()]
- "scanner_va_campaign_progressreporter_flush": "._flush()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L265 | neighbors=[ProgressReporter, .finish(), _atomic_write_json(), .snapshot(), .__init__(), .mark()]
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[auth.py, BaseModel, Parsed from JWT claims — attached to re…, Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…]
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L44 | neighbors=[engagement.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), EngagementStatus]
- "scripts_seed_admin_seed_once": "_seed_once()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L192 | neighbors=[seed_admin.py, All DB work in a single transaction. Ro…, _detect_drift(), _hash(), log_info(), _verify_hash()]
- "scripts_startup_validator_validationreport": "ValidationReport" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L42 | neighbors=[startup_validator.py, run_all_validators(), .add(), .errors(), .print_summary(), .raise_if_errors()]
- "services_finding_events_synthesize_events": "synthesize_events()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L108 | neighbors=[finding_events.py, build_timeline(), Derive the canonical lifecycle events t…, _detected_actor(), _detected_detail(), _ev()]
- "services_job_result_service_rationale_143": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L143 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_rationale_33": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L33 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_validate_result_scope": "validate_result_scope()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L131 | neighbors=[job_result_service.py, process_job_result(), Return result identities outside the jo…, _identity_ip(), _result_network_identities(), Return result identities outside the jo…]
- "services_llm_managerllmservice_client": "._client()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L408 | neighbors=[ManagerLlmService, ._anthropic(), ._ensure_installed_ollama_model(), ._ollama(), ._openai(), ._openrouter()]
- "services_llm_managerllmservice_default_runtime": "._default_runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L135 | neighbors=[ManagerLlmService, AiRuntimeError, ._auto_cloud_provider(), Runtime, ._fallback_candidates(), .generate()]
- "services_llm_managerllmservice_fallback_candidates": "._fallback_candidates()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L341 | neighbors=[ManagerLlmService, ._default_runtime(), ._runtime(), Runtime, .generate_with_fallback(), Ordered runtimes to try: requested/defa…]
- "services_posture_compute_scores": "compute_scores()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L79 | neighbors=[posture.py, build_posture(), aggregate(), _exploit_prob(), grade_for(), _risk_prob()]
- "services_project_time": "project_time.py" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, project_file_stamp(), project_now(), project_timestamp(), _resolve_project_tz(), to_project_tz()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
