# Node Description Batch 24 of 227

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

- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L709 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…]
- "agent_device_identity": "device_identity.py" | kind=code-symbol | source=probe/agent/device_identity.py:L1 | neighbors=[decode_key(), encode_key(), generate_signing_identity(), sign_b64(), signing_public_from_private(), verify_site_policy()]
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L371 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()]
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError]
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=probe/agent/result_spool.py:L184 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists(), ._path(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L110 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L652 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Generic authenticated GET, returns pars…, Establish an authenticated WebSocket co…]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L524 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L438 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L234 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …]
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …]
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings, AiRuntimeError]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L249 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…, Identify the Manager API without exposi…]
- "assistant_modelswitcher": "ModelSwitcher.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L1 | neighbors=[AssistantDrawer.tsx, AiStatus, ModelSelection, ModelSwitcher(), ProviderStatus, readStored()]
- "auth_exceptions_vedhaautherror": "VedhaAuthError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L15 | neighbors=[exceptions.py, AuthenticationError, DatabaseUnavailableError, PasswordRotationError, Base for all Vedha auth exceptions., SeedConfigurationError]
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…]
- "cli_auth_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L46 | neighbors=[auth.ts, serverUrl(), admin.ts, engagement.ts, interactive.ts, report.ts]
- "cli_llm_client": "client()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L10 | neighbors=[llm.ts, commentOnStage(), explainFindings(), planExploit(), recommendNextPhase(), streamAsk()]
- "commands_interactive_picktargets": "pickTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L226 | neighbors=[interactive.ts, ask(), choose(), confirm(), detectLocalSubnet(), inferHostsFromFindings()]
- "commands_interactive_wizardengagement": "wizardEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1769 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), divider(), fetchEngagements()]
- "commands_interactive_wizardreport": "wizardReport()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1847 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardvalidate": "wizardValidate()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1465 | neighbors=[interactive.ts, mainMenu(), runValidationFlow(), ask(), choose(), confirm()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@25344045b42fb3f74183072c0b432ee8c30db287": "2534404 scanner(service_enum): commit owner's in-progress changes as-is + re-sy…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, 4733f24 evasion(scanner): --source-port…, service_enum.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@35691030666303cbdc4b5214a09373d49b3d2bcf": "3569103 docs(agent): research + design for Vedha Autonomous Engagement Agent" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, testing/all-features]
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), Protocol, CPECandidate, Fact, pipeline.py — Phase 1 + Phase 2 end to …]
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()]
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()]
- "detection_verification": "verification.py" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, de2d1c9 feat(verification): optional fa…, compute_verdict(), _int_confidence(), _qualifies_for_llm(), VerificationVerdict]
- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L24 | neighbors=[xml_parser.py, ._parse_host(), .open_ports(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "enum": "Enum" | kind=code-symbol | neighbors=[models.py, FindingState, SourceConfidence, verifier.py, agent.py, enums.py]
- "frontend_proxy": "proxy.ts" | kind=code-symbol | source=manager/frontend/proxy.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES]
- "lib_adapters_touifinding": "toUiFinding()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L112 | neighbors=[route.ts, route.ts, adapters.ts, evidenceToUi(), severityToPriority(), security-context.ts]
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()]
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, proxy.ts, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost()]
- "main_scripts_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L286 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), ._icmp_timestamp(), .__init__(), .scan_target()]
- "main_scripts_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L864 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "main_scripts_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L564 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()]
- "main_scripts_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
