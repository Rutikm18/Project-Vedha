# Node Description Batch 19 of 104

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

- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L205 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L311 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L267 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L194 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=probe/agent/agent.py:L563 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet(), Detect common debugging/tracing tools. …]
- "agent_agent_load_or_create_identity": "_load_or_create_identity()" | kind=code-symbol | source=probe/agent/agent.py:L611 | neighbors=[agent.py, say(), _obtain_identity(), Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…]
- "agent_agent_maptojob": "mapToJob()" | kind=code-symbol | source=probe-go/agent/agent.go:L319 | neighbors=[agent.py, firstStr(), floatOr(), str(), .runJob()]
- "agent_agent_runpollloop": ".runPollLoop()" | kind=code-symbol | source=probe-go/agent/agent.go:L207 | neighbors=[agent.py, .Run(), .runJob(), say(), .submitWithSpool()]
- "agent_agent_scanningagent_api_call": "._api_call()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L649 | neighbors=[ScanningAgent, ._execute_job(), ._heartbeat_loop(), ._poll_and_execute(), ._report_progress()]
- "agent_agent_vaultcredentialfetcher": "VaultCredentialFetcher" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L75 | neighbors=[agent.py, Fetches credentials from HashiCorp Vaul…, .__init__(), .get_credentials(), .__init__()]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L272 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L57 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L31 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L44 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L32 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 2885afa Add comprehensive probe testing…, test_integration.py, test_result_spool.py]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L61 | neighbors=[Check if a spooled result exists for th…, ResultSpool, .flush_spool(), .load(), .spool_count()]
- "agent_task_runner_taskrunner": "TaskRunner" | kind=code-symbol | source=probe/agent/task_runner.py:L41 | neighbors=[task_runner.py, Orchestrates one scan job's lifecycle. …, .__init__(), .run_job(), ._submit_or_spool()]
- "ai_hallucination_hallucinationguard_validate": ".validate()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L101 | neighbors=[HallucinationGuard, .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), Run all relevant checks and return a co…]
- "ai_prioritizer_extract_features": "extract_features()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L72 | neighbors=[prioritizer.py, _to_float(), Build the model's feature vector from a…, .explain_prediction(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_fallback_score": ".fallback_score()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L204 | neighbors=[Weighted composite 0–1000 (same shape a…, VulnPrioritizer, .explain_prediction(), ._formula_contributions(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_predict_priority": ".predict_priority()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L148 | neighbors=[Return a 0–1000 priority score. Uses th…, VulnPrioritizer, .explain_prediction(), extract_features(), .fallback_score()]
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, 298a9d4 trim frontend to 7 core pages; …]
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings]
- "approve_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/approve/route.ts:L1 | neighbors=[POST(), ai-engine.ts, aiReportStore, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "auth_pat_build_personal_access_token": "build_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L54 | neighbors=[pat.py, hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()]
- "brain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L1 | neighbors=[POST(), findings-store.ts, getAllFindings(), 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#agents/greeting-introduction": "agents/greeting-introduction" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 8d65c92 first commit, a388bb3 script updated, architecture de…, bd7383f scanner fine ..now integrations, f5ce592 first commit]
- "cli_auth_serverurl": "serverUrl()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L42 | neighbors=[auth.ts, apiFetch(), doctor.ts, interactive.ts, login.ts]
- "commands_interactive_runinteractive": "runInteractive()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2105 | neighbors=[index.ts, interactive.ts, banner(), ensureAuthenticated(), mainMenu()]
- "commands_interactive_runphaseexploitation": "runPhaseExploitation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1070 | neighbors=[interactive.ts, runIterativeEngagement(), choose(), confirm(), ln()]
- "commands_interactive_runphaseportscan": "runPhasePortScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1028 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()]
- "commands_interactive_runphaseservicedetect": "runPhaseServiceDetect()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1037 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()]
- "commands_interactive_runphasevulnassess": "runPhaseVulnAssess()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1051 | neighbors=[interactive.ts, runIterativeEngagement(), confirm(), ln(), runPhaseWithTools()]
- "commands_interactive_runvulnassessmentflow": "runVulnAssessmentFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1184 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow(), wizardScan()]
- "detection_correlator_detectioncorrelator_correlate": ".correlate()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L82 | neighbors=[DetectionCorrelator, ._host_for(), ._in_window(), ._min_latency(), DetectionResultDTO]
- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_bridge_create_findings_from_facts": "create_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L108 | neighbors=[engine_bridge.py, detect_findings_from_facts(), _vuln_db_meta(), New raw-facts path: detect CVE findings…, run_detection_job()]
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L315 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-018.json

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
