# Node Description Batch 42 of 134

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

- "ai_hallucination_hallucinationguard_validate_cvss_scores": ".validate_cvss_scores()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L60 | neighbors=[HallucinationGuard, .validate(), Flag CVSS scores in the text that don't…]
- "ai_hallucination_hallucinationguard_validate_remediation_commands": ".validate_remediation_commands()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L89 | neighbors=[HallucinationGuard, .validate(), Flag destructive-looking commands that …]
- "ai_llm_report_enum": "_enum()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L310 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_finding_scores": "_finding_scores()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L321 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_llmreportgenerator_complete": "._complete()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L110 | neighbors=[LLMReportGenerator, LLMUnavailableError, ._generate_and_store()]
- "ai_llm_report_llmreportgenerator_generate_executive_summary": ".generate_executive_summary()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L171 | neighbors=[LLMReportGenerator, _collect_cves_scores(), ._generate_and_store()]
- "ai_prioritizer_vulnprioritizer_formula_contributions": "._formula_contributions()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L191 | neighbors=[VulnPrioritizer, .explain_prediction(), .fallback_score()]
- "app_database_get_read_db": "get_read_db()" | kind=code-symbol | source=manager/backend/app/database.py:L63 | neighbors=[database.py, Read-only session (no commit) routed to…, Read-only session (no commit) routed to…]
- "app_main_service_root": "_service_root()" | kind=code-symbol | source=manager/backend/app/main.py:L233 | neighbors=[main.py, Identify the Manager API without exposi…, Identify the Manager API without exposi…]
- "assistant_assistanttext_assistanttext": "AssistantText()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L10 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText.tsx]
- "assistant_factcard_factcard": "FactCard()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L15 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx]
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
- "auth_exceptions_usernotfounderror": "UserNotFoundError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L33 | neighbors=[exceptions.py, No user record for the supplied email., AuthenticationError]
- "auth_jwt_create_access_token": "create_access_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L20 | neighbors=[jwt.py, _now(), create_device_access_token()]
- "auth_jwt_now": "_now()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L16 | neighbors=[jwt.py, create_access_token(), create_refresh_token()]
- "auth_middleware_agent_jwt_path_allows": "agent_jwt_path_allows()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L37 | neighbors=[middleware.py, Least-privilege route allowlist for leg…, .dispatch()]
- "auth_router_authenticate": "_authenticate()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L51 | neighbors=[router.py, login(), Validates credentials and returns the U…]
- "auth_startup_check_cookie_config": "_check_cookie_config()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L230 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_cors": "_check_cors()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L245 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_database": "_check_database()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L98 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_jwt_secret": "_check_jwt_secret()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L130 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_redis": "_check_redis()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L117 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_required_env_vars": "_check_required_env_vars()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L259 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "brain_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L48 | neighbors=[route.ts, validMessages(), assistant.test.ts]
- "cli_auth_clearsession": "clearSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L29 | neighbors=[auth.ts, interactive.ts, logout.ts]
- "cli_auth_savesession": "saveSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L24 | neighbors=[auth.ts, interactive.ts, login.ts]
- "cli_llm_streamask": "streamAsk()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L340 | neighbors=[llm.ts, client(), ask.ts]
- "commands_doctor_render": "render()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L41 | neighbors=[doctor.ts, ln(), symbol()]
- "commands_interactive_fetchengagements": "fetchEngagements()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1746 | neighbors=[interactive.ts, pickEngagementId(), wizardEngagement()]
- "commands_interactive_inferhostsfromfindings": "inferHostsFromFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1418 | neighbors=[interactive.ts, pickTargets(), wizardScan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
