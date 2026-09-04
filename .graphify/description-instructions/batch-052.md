# Node Description Batch 53 of 332

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "ad_kerberoast": "kerberoast.py" | kind=code-symbol | source=manager/backend/app/ad/kerberoast.py:L1 | neighbors=[KerberoastChecker, KerberoastChecker — find SPN-bearing ac…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L204 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L266 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L193 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_job_intent": "_job_intent()" | kind=code-symbol | source=probe/agent/agent.py:L103 | neighbors=[agent.py, Human label for what a job will actuall…, _ws_run_job(), Human label for what a job will actuall…, Human label for what a job will actuall…]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L276 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L61 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L35 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L48 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L480 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()]
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L155 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()]
- "agent_engine_derive_devices": "_derive_devices()" | kind=code-symbol | source=probe/agent/engine.py:L490 | neighbors=[engine.py, _results_by_target(), _derive_post_stage(), Classify each target's device role from…, Classify each target's device role from…]
- "agent_engine_derive_exposure": "_derive_exposure()" | kind=code-symbol | source=probe/agent/engine.py:L510 | neighbors=[engine.py, _results_by_target(), _derive_post_stage(), Reconcile each target's per-vantage rea…, Reconcile each target's per-vantage rea…]
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L35 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license(), Stable per-machine ID, derived from hw_…]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L29 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L215 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists(), Number of pending (unsubmitted) results…, Number of pending (unsubmitted) results…]
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=probe/agent/result_spool.py:L59 | neighbors=[ResultSpool, .quarantine(), .remove(), .save(), .exists()]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L92 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job(), Structured result from running one scan…, Structured result from running one scan…]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L111 | neighbors=[Args:             http_get:       Callb…, TaskRunner, Args:             http_get:       Callb…, Create the result archive directory at …, Args:             http_get:       Callb…]
- "agent_transport_devicealreadyenrollederror": "DeviceAlreadyEnrolledError" | kind=code-symbol | source=probe/agent/transport.py:L53 | neighbors=[transport.py, TransportError, The probe's device signing key is alrea…, .create_enrollment_request(), The probe's device signing key is alrea…]
- "agent_transport_enrollmentrequestnotfound": "EnrollmentRequestNotFound" | kind=code-symbol | source=probe/agent/transport.py:L64 | neighbors=[transport.py, TransportError, A poll/activate targeted an enrollment …, .activate_enrollment(), .poll_enrollment()]
- "agent_transport_transport_activate_enrollment": ".activate_enrollment()" | kind=code-symbol | source=probe/agent/transport.py:L442 | neighbors=[Transport, EnrollmentRequestNotFound, manager_fingerprint(), .load_state(), .update_state()]
- "agent_transport_transport_heartbeat_ex": ".heartbeat_ex()" | kind=code-symbol | source=probe/agent/transport.py:L608 | neighbors=[Send a heartbeat and report WHY it fail…, Transport, .heartbeat(), .ensure_device_access(), Send a heartbeat and report WHY it fail…]
- "agent_validation_score_inventory": "score_inventory()" | kind=code-symbol | source=probe/agent/validation.py:L201 | neighbors=[validation.py, Score promoted inventory against explic…, _metric(), _not_scored(), validate_ground_truth()]
- "ai_hallucination_hallucinationguard_validate": ".validate()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L101 | neighbors=[HallucinationGuard, .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), Run all relevant checks and return a co…]
- "ai_llm_report_normalize_ai_plan": "_normalize_ai_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L426 | neighbors=[llm_report.py, .generate_remediation_plan(), _safe_commands(), Coerce a parsed AI response into the sa…, Coerce a parsed AI response into the sa…]
- "ai_llm_report_remediation_plan_prompt": "_remediation_plan_prompt()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L356 | neighbors=[llm_report.py, .generate_remediation_plan(), Build the structured-remediation prompt…, _enum(), Build the structured-remediation prompt…]
- "ai_prioritizer_extract_features": "extract_features()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L72 | neighbors=[prioritizer.py, _to_float(), Build the model's feature vector from a…, .explain_prediction(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_fallback_score": ".fallback_score()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L204 | neighbors=[Weighted composite 0–1000 (same shape a…, VulnPrioritizer, .explain_prediction(), ._formula_contributions(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_predict_priority": ".predict_priority()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L148 | neighbors=[Return a 0–1000 priority score. Uses th…, VulnPrioritizer, .explain_prediction(), extract_features(), .fallback_score()]
- "app_version": "version.py" | kind=code-symbol | source=manager/backend/app/version.py:L1 | neighbors=[main.py, get_version(), Single source of truth for the deployed…, b5ffcb0 Refactor Vedha probe installer …, health.py]
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "assistant_assistantfab": "AssistantFab.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L1 | neighbors=[AssistantFab(), AssistantProvider.tsx, useAssistant(), 1fe16c8 stable but some dead code, need…, 41b692a Update project files]
- "assistant_assistanttext": "AssistantText.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText(), plain(), 1fe16c8 stable but some dead code, need…]
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "attack_paths_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "auth_jwt_create_refresh_token": "create_refresh_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L67 | neighbors=[jwt.py, _now(), Returns (token, jti) — jti is stored in…, Returns (token, jti) — jti is stored in…, Returns (token, jti) — jti is stored in…]
- "auth_pat_build_personal_access_token": "build_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L54 | neighbors=[pat.py, hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()]
- "auth_portal_scope_resolve_scope": "resolve_scope()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L47 | neighbors=[portal_scope.py, The safe engagement id to filter by.   …, assert_client(), scoped_engagement(), The safe engagement id to filter by.   …]
- "auth_startup_check_admin_account": "_check_admin_account()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L157 | neighbors=[startup.py, CheckResult, Verify the seeded admin account exists …, run_startup_diagnostics(), Verify the seeded admin account exists …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-052.json

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
