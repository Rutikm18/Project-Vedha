# Node Description Batch 91 of 330

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
- "auth_exceptions_usernotfounderror": "UserNotFoundError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L33 | neighbors=[exceptions.py, No user record for the supplied email., AuthenticationError]
- "auth_jwt_create_access_token": "create_access_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L27 | neighbors=[jwt.py, _now(), create_device_access_token()]
- "auth_jwt_now": "_now()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L23 | neighbors=[jwt.py, create_access_token(), create_refresh_token()]
- "auth_middleware_agent_jwt_path_allows": "agent_jwt_path_allows()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L37 | neighbors=[middleware.py, Least-privilege route allowlist for leg…, .dispatch()]
- "auth_startup_check_cookie_config": "_check_cookie_config()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L228 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_cors": "_check_cors()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L243 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_database": "_check_database()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L96 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_jwt_secret": "_check_jwt_secret()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L128 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_redis": "_check_redis()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L115 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "auth_startup_check_required_env_vars": "_check_required_env_vars()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L257 | neighbors=[startup.py, CheckResult, run_startup_diagnostics()]
- "brain_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L48 | neighbors=[route.ts, validMessages(), assistant.test.ts]
- "cli_auth_clearsession": "clearSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L29 | neighbors=[auth.ts, interactive.ts, logout.ts]
- "cli_auth_savesession": "saveSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L24 | neighbors=[auth.ts, interactive.ts, login.ts]
- "cli_llm_streamask": "streamAsk()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L340 | neighbors=[llm.ts, client(), ask.ts]
- "commands_doctor_render": "render()" | kind=code-symbol | source=manager/frontend/cli/commands/doctor.ts:L41 | neighbors=[doctor.ts, ln(), symbol()]
- "commands_interactive_fetchengagements": "fetchEngagements()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1746 | neighbors=[interactive.ts, pickEngagementId(), wizardEngagement()]
- "commands_interactive_inferhostsfromfindings": "inferHostsFromFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1418 | neighbors=[interactive.ts, pickTargets(), wizardScan()]
- "commands_interactive_mergehosts": "mergeHosts()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1165 | neighbors=[interactive.ts, runPhasePortScan(), runPhaseServiceDetect()]
- "commands_interactive_printhostdiscoverydiagnostic": "printHostDiscoveryDiagnostic()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L917 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_printhostsummary": "printHostSummary()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L905 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_printstatesummary": "printStateSummary()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L895 | neighbors=[interactive.ts, ln(), runIterativeEngagement()]
- "commands_interactive_runphaseenumeration": "runPhaseEnumeration()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1044 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()]
- "commands_interactive_runphasehostdiscovery": "runPhaseHostDiscovery()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1023 | neighbors=[interactive.ts, runIterativeEngagement(), runPhaseWithTools()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, f5ce592 first commit]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2c38782317674ba6a0323a1ea1539a68587a356d": "2c38782 docs: spec CVE-breadth phase — snapshot must answer for every recognize…" | kind=Commit | source=git | neighbors=[main, 8f6bf49 Refactor code structure and rem…, f473173 merge: network VA accuracy, KEV…]
- "components_dashboardcharts_dashboardcharts": "DashboardCharts()" | kind=code-symbol | source=manager/frontend/components/DashboardCharts.tsx:L180 | neighbors=[page.tsx, DashboardCharts.tsx, page.tsx]
- "cve_cli_cmd_correlate": "cmd_correlate()" | kind=code-symbol | source=probe/cve/cli.py:L81 | neighbors=[cli.py, _merge_findings(), _read_facts()]
- "cve_cli_merge_findings": "_merge_findings()" | kind=code-symbol | source=probe/cve/cli.py:L65 | neighbors=[cli.py, cmd_correlate(), Merge CVE-finding lists, dedup by (cve_…]

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
