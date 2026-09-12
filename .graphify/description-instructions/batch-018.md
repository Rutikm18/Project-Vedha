# Node Description Batch 19 of 380

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L926 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop(), Acknowledge an offer without executing …, Acknowledge an offer without executing …, Acknowledge an offer without executing …] | lang=en
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=probe/agent/cli.py:L575 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()] | lang=en
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L429 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()] | lang=en
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()] | lang=en
- "agent_scope_model": "scope_model.py" | kind=code-symbol | source=probe/agent/scope_model.py:L1 | neighbors=[classify_interface(), detect_container(), Interface, ipv6_scope_note(), is_denied(), parse_linux_ip_json()] | lang=en
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L720 | neighbors=[Backwards-compatible bool form of `hear…, Transport, .heartbeat_ex(), Backwards-compatible bool form of `hear…, Backwards-compatible bool form of `hear…, Backwards-compatible bool form of `hear…] | lang=en
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L738 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…] | lang=en
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L623 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…] | lang=en
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator] | lang=en
- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, agent_jwt_path_allows(), _is_public_enrollment_request(), portal_jwt_path_allows(), TenantIsolationMiddleware, 10dfc80 Add comprehensive probe testing…] | lang=en
- "auth_startup_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L49 | neighbors=[startup.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@86b4fb05a9c008593e4588492c64b3550a91796d": "86b4fb0 Add UI-Finding to RawFinding adapter with derivations + tests" | kind=Commit | source=git | neighbors=[00140b3 Vendor FindingReport component …, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@be2f89177cb100141a5755c182dac41dbc927453": "be2f891 Frontend consumes backend report enrichment (prefer over derivation)" | kind=Commit | source=git | neighbors=[6cf7e16 Expose report enrichment on Fin…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bf61dbc3d12b9690e3e603f4adbf0e341f656c0c": "bf61dbc docs: probe run/test guide; gitignore nohup.out" | kind=Commit | source=git | neighbors=[bd85323 feat(probe): self-heal re-enrol…, 1209_system_ui_backend_level_changes, addcapabilities-fable, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c6420a65579b0a798b8a8b4feb23c9af4a977eec": "c6420a6 Add deterministic verification (retest) KB + detection_method derivation" | kind=Commit | source=git | neighbors=[ac7c957 Render portal All-Findings via …, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=pt
- "cve_ingest": "ingest.py" | kind=code-symbol | source=probe/cve/ingest.py:L1 | neighbors=[6e2818f Add support for additional serv…, _cvss(), _get(), ingest_all(), ingest_epss(), ingest_kev()] | lang=en
- "detection_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, attack_path_findings(), _bump(), _cleartext_cluster(), _exposed_db_unauth(), _group()] | lang=en
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, AttackAction, _aware()] | lang=en
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload] | lang=en
- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend()] | lang=en
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()] | lang=en
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…, APP_VERSION] | lang=en
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend()] | lang=en
- "lib_adapters_touifinding": "toUiFinding()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L166 | neighbors=[route.ts, route.ts, adapters.ts, evidenceToUi(), severityToPriority(), console-source.tsx] | lang=en
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore] | lang=en
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors] | lang=en
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()] | lang=en
- "main_scripts_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L353 | neighbors=[os_fingerprint.py, BaseScanner, ._apply_smb_build(), ._icmp_echo_ttl(), ._icmp_scan_target(), ._icmp_timestamp()] | lang=en
- "main_scripts_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L697 | neighbors=[PortScanner, ._is_ambiguous(), ._reprobe_ambiguous(), ._silence_result(), ScanMetrics, .record()] | lang=en
- "main_scripts_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L239 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()] | lang=en
- "main_scripts_ssh_scanner": "ssh_scanner.py" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _Cursor, _dedup(), evaluate_algorithms(), main()] | lang=en
- "main_scripts_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L309 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()] | lang=en
- "main_scripts_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, classify_cipher(), _get_cert_der(), grade_tls_posture()] | lang=en
- "main_scripts_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L317 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()] | lang=en
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[attack_timeline.py, Base, TimestampMixin, Append-only ledger of every attack acti…, AttackLogger, AttackLogger — records every attack act…] | lang=en
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L47 | neighbors=[outbox.py, Base, TimestampMixin, Base, TimestampMixin, Event] | lang=en
- "portal_timestamp": "Timestamp.tsx" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, formatCompact(), formatExact(), formatRelative(), isoUtc()] | lang=en
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L214 | neighbors=[agents.py, BaseModel, .validate_network_segments(), Asset, Engagement, ScanJobStatus] | lang=en
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L240 | neighbors=[agents.py, BaseModel, .require_fence_for_running_job(), Asset, Engagement, ScanJobStatus] | lang=en
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-018.json

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
