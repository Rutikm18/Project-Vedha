# Node Description Batch 16 of 104

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

- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L103 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, run_engagement(), _run_passive(), .close(), .__init__()]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L214 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]
- "agent_agent_main": "main()" | kind=code-symbol | source=probe/agent/agent.py:L58 | neighbors=[agent.py, _load_env(), _obtain_identity(), _run_ws_push_loop(), say(), _startup_gauntlet()]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=probe/agent/agent.py:L667 | neighbors=[agent.py, main(), _load_or_create_identity(), say(), Return (agent_id, token, fresh, identit…, Return (agent_id, token, fresh, identit…]
- "agent_agent_run": ".Run()" | kind=code-symbol | source=probe-go/agent/agent.go:L50 | neighbors=[agent.py, .obtainIdentity(), .runPollLoop(), .runWSLoop(), say(), .runJob()]
- "agent_agent_runjob": ".runJob()" | kind=code-symbol | source=probe-go/agent/agent.go:L248 | neighbors=[agent.py, mapToJob(), .Run(), say(), .runPollLoop(), .wsSession()]
- "agent_agent_scanningagent_poll_and_execute": "._poll_and_execute()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L672 | neighbors=[ScanningAgent, JobType, ScanJob, ._api_call(), ._execute_job(), .run()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L515 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …]
- "agent_agent_ws_flush_spool": "_ws_flush_spool()" | kind=code-symbol | source=probe/agent/agent.py:L489 | neighbors=[agent.py, Re-submit previously spooled results ov…, _run_ws_push_loop(), say(), _ws_http_poll_fallback(), Re-submit previously spooled results ov…]
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L378 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), say(), Run one job while keeping WS status/res…]
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/cli.py:L309 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()]
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=probe/agent/cli.py:L442 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L101 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), .__init__(), .request()]
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=probe/agent/engine.py:L152 | neighbors=[engine.py, Execute a scan and return the enriched …, _count_open_port_facts(), _error_result(), _targets(), _tuning_from_params()]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 2885afa Add comprehensive probe testing…, test_hw_bind.py]
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L87 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L32 | neighbors=[transport.py, Raised when a transport operation fails…, .connect_ws(), .poll_jobs(), .register(), Exception]
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L249 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()]
- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L183 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()]
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend.ts, backend(), BackendError, bearerFrom(), 298a9d4 trim frontend to 7 core pages; …]
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_refresh_token(), decode_token(), _now(), 298a9d4 trim frontend to 7 core pages; …]
- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts]
- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()]
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()]
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()]
- "dashboard_zonerow": "ZoneRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ZoneRow.tsx:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Exposure.tsx, ZoneRow(), mock-dashboard.ts, ZoneHealth, page.tsx]
- "detection_correlator_detectionresultdto": "DetectionResultDTO" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L46 | neighbors=[correlator.py, .correlate(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_ai_normalizer_anthropicaiclient": "AnthropicAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L96 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), CPECandidate, Fact, Real implementation, gated behind the a…]
- "detection_engine_ai_normalizer_fakeaiclient": "FakeAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L123 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), CPECandidate, Fact, Test double — a fixed lookup table, no …]
- "detection_engine_ai_normalizer_propose_candidates": "propose_candidates()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L230 | neighbors=[ai_normalizer.py, AINormalizerCache, .get(), .put(), validate_cpe_exists(), The Phase 2 entry point. raw_text is wh…]
- "detection_engine_bridge_rationale_1": "engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[engine_bridge.py, DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_112": "New raw-facts path: detect CVE findings from result['facts'] and persist     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L112 | neighbors=[create_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_209": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L209 | neighbors=[run_detection_job(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_45": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L45 | neighbors=[_vuln_db_meta(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_83": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L83 | neighbors=[detect_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_correlate": "correlate.py" | kind=code-symbol | source=manager/detection_engine/correlate.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, correlate_smb_patch(), dedup_findings(), _product_from_cpe(), suppress_negated(), correlate.py — dedup, authoritative-sup…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-015.json

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
