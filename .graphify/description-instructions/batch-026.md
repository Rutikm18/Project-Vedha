# Node Description Batch 27 of 209

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

- "routers_agents_rationale_90": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L90 | neighbors=[Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob, Service]
- "routers_analytics_exposureanalytics": "ExposureAnalytics" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L40 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L30 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L35 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_engagements_import_facts": "import_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L294 | neighbors=[engagements.py, _parse_probe_file(), _promote_from_facts(), _read_capped(), _refresh_overview_cache(), Offline ingest path: upload a probe's s…]
- "routers_findings_rationale_25": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L25 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_26": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L26 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_48": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L48 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_49": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L49 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_probe_enrollment_activate_enrollment": "activate_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L600 | neighbors=[probe_enrollment.py, _authenticated_request(), _derive_refresh_secret(), _policy(), _rate_limit(), _secret_hash()]
- "scanner_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L160 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()]
- "scanner_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L413 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), is_locally_administered(), vendor_for_mac()]
- "scanner_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=probe/scanner/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()]
- "scanner_ja4x": "ja4x.py" | kind=code-symbol | source=probe/scanner/ja4x.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious()]
- "scanner_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L198 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()]
- "scanner_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L236 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()]
- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L220 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), .__init__(), .scan_target(), ICMP-echo liveness + TTL harvest -> OS-…]
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()]
- "scanner_run_all": "run_all.py" | kind=code-symbol | source=probe/scanner/run_all.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _log(), main(), _open_tcp_ports(), _ports_arg(), _read_jsonl()]
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L749 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L294 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L129 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]
- "scanner_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L200 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…]
- "scanner_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L261 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L276 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[auth.py, BaseModel, Parsed from JWT claims — attached to re…, Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…]
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L44 | neighbors=[engagement.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), EngagementStatus]
- "schemas_finding_findingpatch": "FindingPatch" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[finding.py, BaseModel, All fields optional — PATCH semantics., All fields optional — PATCH semantics., DetectionStatus, FindingSeverity]
- "scripts_seed_admin_seed_once": "_seed_once()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L192 | neighbors=[seed_admin.py, All DB work in a single transaction. Ro…, _detect_drift(), _hash(), log_info(), _verify_hash()]
- "scripts_startup_validator_validationreport": "ValidationReport" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L42 | neighbors=[startup_validator.py, run_all_validators(), .add(), .errors(), .print_summary(), .raise_if_errors()]
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L127 | neighbors=[job_result_service.py, _promote_assets(), result_checksum(), validate_result_scope(), Process a scan job result.  Called from…, Process a scan job result.  Called from…]
- "services_job_result_service_rationale_143": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L143 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_rationale_33": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L33 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_llm_managerllmservice_client": "._client()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L367 | neighbors=[ManagerLlmService, ._anthropic(), ._ensure_installed_ollama_model(), ._ollama(), ._openai(), ._openrouter()]
- "services_llm_managerllmservice_default_runtime": "._default_runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L94 | neighbors=[ManagerLlmService, AiRuntimeError, ._auto_cloud_provider(), Runtime, ._fallback_candidates(), .generate()]
- "services_llm_managerllmservice_generate_with_fallback": ".generate_with_fallback()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L322 | neighbors=[ManagerLlmService, AiRuntimeError, ._build_system(), ._dispatch(), ._ensure_installed_ollama_model(), ._fallback_candidates()]
- "services_posture_compute_scores": "compute_scores()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L79 | neighbors=[posture.py, build_posture(), aggregate(), _exploit_prob(), grade_for(), _risk_prob()]
- "siem_config_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, SIEMConfig, GET(), POST(), 298a9d4 trim frontend to 7 core pages; …]
- "summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), with-backend.ts, withBackend(), ApiSummary]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
