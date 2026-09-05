# Node Description Batch 91 of 336

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

- "agent_local_run_clean": "_clean()" | kind=code-symbol | source=probe/agent/local_run.py:L68 | neighbors=[local_run.py, Drop internal bookkeeping keys (_collec…, summarize()]
- "agent_local_run_parse_args": "_parse_args()" | kind=code-symbol | source=probe/agent/local_run.py:L120 | neighbors=[local_run.py, _main(), Validate positional args (args[0]=targe…]
- "agent_local_run_port_label": "_port_label()" | kind=code-symbol | source=probe/agent/local_run.py:L75 | neighbors=[local_run.py, Render a port fact unambiguously: '445/…, summarize()]
- "agent_local_run_ports_from_env": "_ports_from_env()" | kind=code-symbol | source=probe/agent/local_run.py:L42 | neighbors=[local_run.py, _main(), Resolve the port set from PROBE_LOCAL_P…]
- "agent_local_run_run": "run()" | kind=code-symbol | source=probe/agent/local_run.py:L199 | neighbors=[local_run.py, Synchronous entrypoint for the `local-r…, _main()]
- "agent_local_run_usage_error": "_usage_error()" | kind=code-symbol | source=probe/agent/local_run.py:L109 | neighbors=[local_run.py, _main(), Actionable input error on stderr → exit…]
- "agent_result_spool_resultspool_spool_bytes": ".spool_bytes()" | kind=code-symbol | source=probe/agent/result_spool.py:L222 | neighbors=[Total bytes held by pending result file…, ResultSpool, .exists()]
- "agent_scope_crypt_decrypt_scope": "decrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L97 | neighbors=[scope_crypt.py, decrypt_scope_b64(), Decrypt a scope blob using the probe's …]
- "agent_scope_crypt_decrypt_scope_b64": "decrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L155 | neighbors=[scope_crypt.py, decrypt_scope(), decrypt_scope() accepting a base64 stri…]
- "agent_scope_crypt_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L55 | neighbors=[scope_crypt.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…]
- "agent_scope_crypt_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L150 | neighbors=[scope_crypt.py, encrypt_scope(), encrypt_scope() returning a base64 stri…]
- "agent_scope_validator_fetch_engagement_scope": "fetch_engagement_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L54 | neighbors=[scope_validator.py, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_scope_validator_merge_exclusions": "merge_exclusions()" | kind=code-symbol | source=probe/agent/scope_validator.py:L154 | neighbors=[scope_validator.py, Merge engagement-level exclusions with …, Merge engagement-level exclusions with …]
- "agent_task_runner_prepare_result_dir": "prepare_result_dir()" | kind=code-symbol | source=probe/agent/task_runner.py:L55 | neighbors=[task_runner.py, _result_dir(), Create the result archive directory at …]
- "agent_task_runner_result_dir": "_result_dir()" | kind=code-symbol | source=probe/agent/task_runner.py:L47 | neighbors=[task_runner.py, prepare_result_dir(), ._archive_result()]
- "agent_transport_strip_nul": "_strip_nul()" | kind=code-symbol | source=probe/agent/transport.py:L31 | neighbors=[transport.py, Recursively remove NUL (U+0000) charact…, .submit_result()]
- "agent_transport_transport_clear_manager_binding": ".clear_manager_binding()" | kind=code-symbol | source=probe/agent/transport.py:L329 | neighbors=[Forget everything a SPECIFIC manager is…, Transport, .update_state()]
- "agent_transport_transport_create_enrollment_request": ".create_enrollment_request()" | kind=code-symbol | source=probe/agent/transport.py:L452 | neighbors=[Transport, DeviceAlreadyEnrolledError, _enrollment_conflict_detail()]
- "agent_validation_validate_ground_truth": "validate_ground_truth()" | kind=code-symbol | source=probe/agent/validation.py:L106 | neighbors=[validation.py, Validate the small, explicit inventory …, score_inventory()]
- "ai_agent_agentdecisionengine_list_findings": "._list_findings()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L283 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), _val()]
- "ai_agent_val": "_val()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L393 | neighbors=[agent.py, ._list_findings(), ._overview()]
- "ai_hallucination_hallucinationguard_validate_cve_claims": ".validate_cve_claims()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L45 | neighbors=[HallucinationGuard, .validate(), Flag any CVE ID mentioned in ``text`` t…]
- "ai_hallucination_hallucinationguard_validate_cvss_scores": ".validate_cvss_scores()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L60 | neighbors=[HallucinationGuard, .validate(), Flag CVSS scores in the text that don't…]
- "ai_hallucination_hallucinationguard_validate_remediation_commands": ".validate_remediation_commands()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L89 | neighbors=[HallucinationGuard, .validate(), Flag destructive-looking commands that …]
- "ai_llm_report_finding_scores": "_finding_scores()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L473 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_llmreportgenerator_generate_executive_summary": ".generate_executive_summary()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L173 | neighbors=[LLMReportGenerator, _collect_cves_scores(), ._generate_and_store()]
- "ai_prioritizer_vulnprioritizer_formula_contributions": "._formula_contributions()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L191 | neighbors=[VulnPrioritizer, .explain_prediction(), .fallback_score()]
- "app_database_get_read_db": "get_read_db()" | kind=code-symbol | source=manager/backend/app/database.py:L63 | neighbors=[database.py, Read-only session (no commit) routed to…, Read-only session (no commit) routed to…]
- "assistant_assistanttext_assistanttext": "AssistantText()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L10 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText.tsx]
- "auth_exceptions_bcryptfailureerror": "BcryptFailureError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L58 | neighbors=[exceptions.py, AuthenticationError, bcrypt raised an exception during verif…]
- "auth_exceptions_databasefailureerror": "DatabaseFailureError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L63 | neighbors=[exceptions.py, AuthenticationError, Could not reach the database during aut…]
- "auth_exceptions_databaseunavailableerror": "DatabaseUnavailableError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L91 | neighbors=[exceptions.py, VedhaAuthError, Database is not reachable at all — rais…]
- "auth_exceptions_disabledtenanterror": "DisabledTenantError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L48 | neighbors=[exceptions.py, AuthenticationError, Tenant account is disabled — all users …]
- "auth_exceptions_disabledusererror": "DisabledUserError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L43 | neighbors=[exceptions.py, AuthenticationError, User account exists but is_active=False.]
- "auth_exceptions_expiredpassworderror": "ExpiredPasswordError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L53 | neighbors=[exceptions.py, AuthenticationError, User's password_expires_at is in the pa…]
- "auth_exceptions_jwtfailureerror": "JWTFailureError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L68 | neighbors=[exceptions.py, AuthenticationError, JWT token could not be created — JWT_SE…]
- "auth_exceptions_passwordmismatcherror": "PasswordMismatchError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L38 | neighbors=[exceptions.py, AuthenticationError, User exists but supplied password does …]
- "auth_exceptions_passwordrotationerror": "PasswordRotationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L86 | neighbors=[exceptions.py, VedhaAuthError, Password rotation was requested but cou…]
- "auth_exceptions_ratelimiterror": "RateLimitError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L73 | neighbors=[exceptions.py, AuthenticationError, Caller exceeded the login rate limit — …]
- "auth_exceptions_seedconfigurationerror": "SeedConfigurationError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L81 | neighbors=[exceptions.py, Required env var missing, value invalid…, VedhaAuthError]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-090.json

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
