# Node Description Batch 20 of 186

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

- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L364 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, _bounded_env_int(), say(), Run an HTTP-claimed job while renewing …] | lang=en
- "agent_agent_ws_heartbeat_sender": "_ws_heartbeat_sender()" | kind=code-symbol | source=probe/agent/agent.py:L700 | neighbors=[agent.py, Send periodic heartbeats over WebSocket., _run_ws_push_loop(), Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket.] | lang=en
- "agent_device_identity": "device_identity.py" | kind=code-symbol | source=probe/agent/device_identity.py:L1 | neighbors=[decode_key(), encode_key(), generate_signing_identity(), sign_b64(), signing_public_from_private(), verify_site_policy()] | lang=en
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L371 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()] | lang=en
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError] | lang=en
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=probe/agent/result_spool.py:L184 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists(), ._path(), .quarantine(), .remove()] | lang=en
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L110 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()] | lang=en
- "agent_transport_transport_ensure_device_access": ".ensure_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L394 | neighbors=[Refresh a device token before expiry; l…, Transport, .connect_ws(), .load_state(), .refresh_device_access(), .heartbeat()] | lang=en
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings, AiRuntimeError] | lang=en
- "assistant_modelswitcher": "ModelSwitcher.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L1 | neighbors=[AssistantDrawer.tsx, AiStatus, ModelSelection, ModelSwitcher(), ProviderStatus, readStored()] | lang=en
- "auth_exceptions_vedhaautherror": "VedhaAuthError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L15 | neighbors=[exceptions.py, AuthenticationError, DatabaseUnavailableError, PasswordRotationError, Base for all Vedha auth exceptions., SeedConfigurationError] | lang=en
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()] | lang=en
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…] | lang=en
- "cli_auth_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L46 | neighbors=[auth.ts, serverUrl(), admin.ts, engagement.ts, interactive.ts, report.ts] | lang=en
- "cli_llm_client": "client()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L10 | neighbors=[llm.ts, commentOnStage(), explainFindings(), planExploit(), recommendNextPhase(), streamAsk()] | lang=en
- "commands_interactive_picktargets": "pickTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L226 | neighbors=[interactive.ts, ask(), choose(), confirm(), detectLocalSubnet(), inferHostsFromFindings()] | lang=en
- "commands_interactive_wizardengagement": "wizardEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1769 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), divider(), fetchEngagements()] | lang=en
- "commands_interactive_wizardreport": "wizardReport()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1847 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commands_interactive_wizardvalidate": "wizardValidate()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1465 | neighbors=[interactive.ts, mainMenu(), runValidationFlow(), ask(), choose(), confirm()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@41b692a77a1dd6d2e5666f2fa2f8aa4b1e084e64": "41b692a Update project files" | kind=Commit | source=git | neighbors=[08e0594 deployement ready, AssistantFab.tsx, feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@58c2d10f572ed4b7fce3da53bb9f95b696c4b94f": "58c2d10 feat(active-validation): ValidationRequest model + migration" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, 0d6be85 feat(risk-rank): explainable 0-…, __init__.py, validation_request.py, test_validation_request_schema.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@80b6dbcc5515152a76b93176716127f4f997f356": "80b6dbc Remove environment secrets from repository" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, spike/probe-go, worktree-fleet-already-downloaded-cmd, 1fe16c8 stable but some dead code, need…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/coverage-gated-auto-resolution, integration/all-branches, main, spike/probe-go, worktree-fleet-already-downloaded-cmd] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0b870c8a083dca715a6f06baf63cd015adb389d": "a0b870c fix(posture): score over open findings only; lock grade-band boundary t…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, 75650c1 feat: add Posture & Patch-Compa…, ai_report.py, analytics.py] | lang=pt
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), Protocol, CPECandidate, Fact, pipeline.py — Phase 1 + Phase 2 end to …] | lang=en
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()] | lang=en
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()] | lang=en
- "detection_verification": "verification.py" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, de2d1c9 feat(verification): optional fa…, compute_verdict(), _int_confidence(), _qualifies_for_llm(), VerificationVerdict] | lang=en
- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L24 | neighbors=[xml_parser.py, ._parse_host(), .open_ports(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …] | lang=en
- "enum": "Enum" | kind=code-symbol | neighbors=[models.py, FindingState, SourceConfidence, verifier.py, agent.py, enums.py] | lang=en
- "frontend_proxy": "proxy.ts" | kind=code-symbol | source=manager/frontend/proxy.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES] | lang=en
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[page.tsx, page.tsx, page.tsx, useToast.ts, page.tsx, page.tsx] | lang=en
- "lib_adapters_touifinding": "toUiFinding()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L112 | neighbors=[route.ts, route.ts, adapters.ts, evidenceToUi(), severityToPriority(), security-context.ts] | lang=en
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()] | lang=en
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, proxy.ts, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost()] | lang=en
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _family_of(), main(), PortScanner, resolve_profile(), ScanMetrics] | lang=en
- "main_scripts_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()] | lang=en
- "main_scripts_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L188 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._fallback_scan(), .__init__(), .scan_target()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
