# Node Description Batch 17 of 332

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

- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, d1b4dd3 trim frontend to 7 core pages; …, f473173 merge: network VA accuracy, KEV…, AttackAction, _aware()]
- "detection_engine_posture_rules_detect_posture_traced": "detect_posture_traced()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L827 | neighbors=[posture_rules.py, detect_all_traced(), detect_posture(), _calibrate_host_findings(), compute_risk(), detect_exposed_services()]
- "detection_resolution": "resolution.py" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, 9a36729 feat(resolution): coverage buil…, bd409f5 feat(resolution): async applier…, cbf5d6c feat(resolution): pure decision…, d98f654 feat(manager): network-VA campa…, apply_manual_reopen()]
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload]
- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend()]
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()]
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…, APP_VERSION]
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 8f6bf49 Refactor code structure and rem…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend()]
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L353 | neighbors=[os_fingerprint.py, BaseScanner, ._apply_smb_build(), ._icmp_echo_ttl(), ._icmp_scan_target(), ._icmp_timestamp()]
- "main_scripts_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L239 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()]
- "main_scripts_ssh_scanner": "ssh_scanner.py" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, _Cursor, _dedup(), evaluate_algorithms(), main()]
- "main_scripts_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, classify_cipher(), _get_cert_der(), grade_tls_posture()]
- "main_scripts_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L317 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[attack_timeline.py, Base, TimestampMixin, Append-only ledger of every attack acti…, AttackLogger, AttackLogger — records every attack act…]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 58c2d10 feat(active-validation): Valida…, 6bb51ab feat: add detection-explain end…, 81c81cb feat: implement outbox reclaim …]
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L47 | neighbors=[outbox.py, Base, TimestampMixin, Base, TimestampMixin, Event]
- "portal_timestamp": "Timestamp.tsx" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L1 | neighbors=[page.tsx, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, page.tsx, page.tsx, formatCompact()]
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L180 | neighbors=[agents.py, BaseModel, .validate_network_segments(), Asset, Engagement, ScanJobStatus]
- "routers_agents_get_job_status": "get_job_status()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1071 | neighbors=[agents.py, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…]
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L206 | neighbors=[agents.py, BaseModel, .require_fence_for_running_job(), Asset, Engagement, ScanJobStatus]
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[_run_generation(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[_run_regeneration(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L61 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L47 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L65 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_integrations": "integrations.py" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 6be8259 feat(integrations): outbox deli…, dependencies.py, delete_integration(), integration_secret(), IntegrationIn]
- "routers_vuln_scans_rationale_278": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L278 | neighbors=[_run_nuclei_and_save(), Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "scanner_nfs_scanner": "nfs_scanner.py" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, is_world_readable(), main(), NFSScanner, parse_mount_export(), parse_portmap_dump()]
- "scanner_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/scanner/port_scanner.py:L239 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()]
- "scanner_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=probe/scanner/scanner_base.py:L465 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()]
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1133 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L317 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "services_finding_events": "finding_events.py" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, build_timeline(), _decorate(), _detected_actor(), _detected_detail(), _ev()]
- "services_llm_airuntimeerror": "AiRuntimeError" | kind=code-symbol | source=manager/backend/app/services/llm.py:L22 | neighbors=[llm.py, RuntimeError, .__init__(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model()]
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L38 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-016.json

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
