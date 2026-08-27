# Node Description Batch 14 of 236

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

- "tests_test_perf_optimization": "test_perf_optimization.py" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, clean_guard_cache(), test_clear_caches_forces_reload(), test_dpkg_compare_does_not_call_the_bin…, test_guard_is_noop_without_dpkg(), test_guard_passes_when_pure_python_agre…]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()]
- "tests_test_validation": "test_validation.py" | kind=code-symbol | source=probe/tests/test_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, validation.py, FakeClient, _preflight_responses(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…]
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[3ad95f4 feat: Optimize asset service fe…, b4b12a9 Rename project and update files, c7f226f chore: bundle pending working-t…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, 3ad95f4 feat: Optimize asset service fe…, c7f226f chore: bundle pending working-t…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=probe/agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L49 | neighbors=[transport.py, DeviceAlreadyEnrolledError, Raised when a transport operation fails…, .bootstrap(), .connect_ws(), .poll_jobs()]
- "ai_hallucination_hallucinationguard": "HallucinationGuard" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L41 | neighbors=[hallucination.py, .validate(), .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), LLMReportGenerator]
- "approve_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/[id]/approve/route.ts:L1 | neighbors=[POST(), backend.ts, backend(), BackendError, bearerFrom(), 10dfc80 Add comprehensive probe testing…]
- "auth_startup_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L49 | neighbors=[startup.py, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors(), _check_database()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1af3404cd899c56eec3439d379b9f621f044baf9": "1af3404 feat(deploy): probe-free manager stack + port-80 edge ingress" | kind=Commit | source=git | neighbors=[0e22dbf feat(probe): bounded auto-troub…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2c53ae99b6e203a1fefff8d7998d849e906ee0c1": "2c53ae9 evasion(scanner): randomized scan order + jittered scan-delay (task C1/…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 37fa611 harden(scanner): XML-entity gua…, port_scanner.py]
- "detection_attack_paths": "attack_paths.py" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, attack_path_findings(), _bump(), _cleartext_cluster(), _exposed_db_unauth(), _group()]
- "detection_engine_ingest": "ingest.py" | kind=code-symbol | source=manager/detection_engine/ingest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _classify_confidence(), _extract_aliases(), ingest_file(), ingest_files()]
- "discovery_finding_translator": "finding_translator.py" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_probe_result(), create_scan_health_finding(), _escalate_by_exposure()]
- "discovery_xml_parser_nmapxmlparser": "NmapXMLParser" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L40 | neighbors=[xml_parser.py, .parse(), ._parse_host(), ._parse_port(), Parse nmap -oX XML into a list of Parse…, DiscoveryJobPayload]
- "engine_tool_runners_spawnopts": "spawnOpts()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L83 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runHttpx(), runNaabu()]
- "engine_types_livefinding": "LiveFinding" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L83 | neighbors=[tools.ts, llm.ts, ask.ts, interactive.ts, scan.ts, scanner.ts]
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, f00ce5f fix(ui): session-timer persiste…, APP_VERSION]
- "hooks_usetoast": "useToast.ts" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, page.tsx, page.tsx, page.tsx, page.tsx, ToastContext]
- "lib_engagements_store": "engagements-store.ts" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ACTIVITY, Credential, Engagement, engagementsStore]
- "lib_errors": "errors.ts" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, diagnoseSpawnError(), ErrorCode, Errors]
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L312 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "models_attack_timeline_attacktimeline": "AttackTimeline" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L11 | neighbors=[attack_timeline.py, Base, TimestampMixin, Append-only ledger of every attack acti…, AttackLogger, AttackLogger — records every attack act…]
- "models_outbox_outboxevent": "OutboxEvent" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L47 | neighbors=[outbox.py, Base, TimestampMixin, Base, TimestampMixin, Event]
- "routers_agents_agentregisterrequest": "AgentRegisterRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L179 | neighbors=[agents.py, BaseModel, .validate_network_segments(), Asset, Engagement, ScanJobStatus]
- "routers_agents_encrypt_scope_for_agent": "_encrypt_scope_for_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L535 | neighbors=[agents.py, enqueue_agent_job(), get_agent_jobs(), Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…]
- "routers_agents_heartbeatrequest": "HeartbeatRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L205 | neighbors=[agents.py, BaseModel, .require_fence_for_running_job(), Asset, Engagement, ScanJobStatus]
- "routers_ai_report_rationale_1": "AI report API (AIReportAPI).  POST /engagements/{id}/ai-report/generate  — async" | kind=entity | source=manager/backend/app/routers/ai_report.py:L1 | neighbors=[ai_report.py, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_263": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L263 | neighbors=[_run_generation(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_ai_report_rationale_321": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L321 | neighbors=[_run_regeneration(), LLMReportGenerator, LLMUnavailableError, Asset, AttackPath, DetectionResult]
- "routers_exploits_approverequest": "ApproveRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L61 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_exploitrunrequest": "ExploitRunRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L47 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_exploits_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L65 | neighbors=[exploits.py, BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError]
- "routers_integrations": "integrations.py" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 6be8259 feat(integrations): outbox deli…, dependencies.py, delete_integration(), integration_secret(), IntegrationIn]
- "routers_vuln_scans_rationale_278": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L278 | neighbors=[_run_nuclei_and_save(), Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=probe/scanner/scanner_base.py:L251 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L312 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "services_llm_airuntimeerror": "AiRuntimeError" | kind=code-symbol | source=manager/backend/app/services/llm.py:L21 | neighbors=[llm.py, RuntimeError, .__init__(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-013.json

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
