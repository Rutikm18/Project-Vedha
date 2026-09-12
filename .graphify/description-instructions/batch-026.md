# Node Description Batch 27 of 380

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

- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=probe/agent/agent.py:L251 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()] | lang=en
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L57 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()] | lang=en
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L198 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError] | lang=en
- "agent_engine_hosts_from_facts": "_hosts_from_facts()" | kind=code-symbol | source=probe/agent/engine.py:L344 | neighbors=[engine.py, _build_run_stats(), Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…] | lang=en
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L231 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan(), Return the effective whole-job deadline…, Return the effective whole-job deadline…] | lang=en
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()] | lang=en
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L141 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state(), Durably replace one private JSON state …, Durably replace one private JSON state …] | lang=en
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()] | lang=en
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py] | lang=en
- "assistant_advisorflow": "AdvisorFlow.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L1 | neighbors=[AdvisorFlow(), CommandRow(), CopyButton(), PATCH_PILL, RichText(), Section()] | lang=en
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_device_access_token(), create_refresh_token(), decode_token(), _now()] | lang=en
- "chat_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L1 | neighbors=[ManagerAiResponse, POST(), backend.ts, backend(), BackendError, bearerFrom()] | lang=en
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts] | lang=en
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR] | lang=en
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2c38782317674ba6a0323a1ea1539a68587a356d": "2c38782 docs: spec CVE-breadth phase — snapshot must answer for every recognize…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@32651d687af0eb0d407c35e3906b79ac8fcf891d": "32651d6 Windows setup: auto-install Python on fresh machines + install guide" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3630d4e5baf6b9734f7577022947ca505b5382ad": "3630d4e Add design spec for report-section integration (admin + portal + backen…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@79ea84ad4d636edee7ffd6a163818f488be003a0": "79ea84a Finish pending gaps: real clock-skew measurement + active manager denial" | kind=Commit | source=git | neighbors=[5bf1aab Wire independent admission gate…, doctor.py, job_admission.py, task_runner.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aeb6fcf36d3639ea14c002971e656a36ad051de2": "aeb6fcf Add Phase 1 implementation plan for report-section (admin reports)" | kind=Commit | source=git | neighbors=[3630d4e Add design spec for report-sect…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@e6887615b9b918bc1d73744b9df59e47adc70afe": "e688761 Add Windows native probe agent (git-based, source-mode setup)" | kind=Commit | source=git | neighbors=[5c59db1 Implement instance locking mech…, 1209_system_ui_backend_level_changes, codex/customer-portal-parity, cross-os-agent-installer, cross-os-vedha-agent-install, feat/va-maturity-gaps] | lang=en
- "customer_access_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, 7a637eb feat: network VA accuracy, KEV …, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…, RefreshButton.tsx, RefreshButton()] | lang=en
- "cve_weakness_map": "weakness_map.py" | kind=code-symbol | source=probe/cve/weakness_map.py:L1 | neighbors=[6e2818f Add support for additional serv…, _Assoc, correlate_weaknesses(), _finding_view(), _has_version(), _mirror_cve()] | lang=en
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender] | lang=en
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient] | lang=en
- "detection_engine_bridge_detect_all_from_facts_traced": "detect_all_from_facts_traced()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L184 | neighbors=[engine_bridge.py, detect_all_from_facts(), _accepted(), _ensure_importable(), _ingest_census(), _log_ingest_health()] | lang=en
- "detection_engine_enrichment_db": "enrichment_db.py" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _cache_key(), _clear_caches(), EpssDB, KevDB] | lang=en
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L125 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine] | lang=en
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()] | lang=en
- "detection_engine_posture_rules_detect_exposed_services": "detect_exposed_services()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1145 | neighbors=[posture_rules.py, compute_risk(), _evidence_ref(), _exposed_title(), make_posture_id(), PostureFinding] | lang=en
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert] | lang=en
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()] | lang=en
- "exploit_orchestrator_rationale_104": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L104 | neighbors=[.validate_safety(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_111": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L111 | neighbors=[.validate_scope(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_131": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L131 | neighbors=[.execute(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_253": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L253 | neighbors=[.generate_dns_callback_token(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_266": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L266 | neighbors=[._check_blast_radius(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en
- "exploit_orchestrator_rationale_297": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L297 | neighbors=[._check_approval_required(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement] | lang=en

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
