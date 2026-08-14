# Node Description Batch 111 of 186

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

- "auth_exceptions_rationale_64": "Could not reach the database during authentication — infrastructure failure." | kind=entity | source=manager/backend/app/auth/exceptions.py:L64 | neighbors=[DatabaseFailureError]
- "auth_exceptions_rationale_69": "JWT token could not be created — JWT_SECRET missing or library failure." | kind=entity | source=manager/backend/app/auth/exceptions.py:L69 | neighbors=[JWTFailureError]
- "auth_exceptions_rationale_74": "Caller exceeded the login rate limit — already handled by the rate-limit middlew" | kind=entity | source=manager/backend/app/auth/exceptions.py:L74 | neighbors=[RateLimitError]
- "auth_exceptions_rationale_82": "Required env var missing, value invalid, or weak password in production." | kind=entity | source=manager/backend/app/auth/exceptions.py:L82 | neighbors=[SeedConfigurationError]
- "auth_exceptions_rationale_87": "Password rotation was requested but could not complete (hash verify failed, etc." | kind=entity | source=manager/backend/app/auth/exceptions.py:L87 | neighbors=[PasswordRotationError]
- "auth_exceptions_rationale_92": "Database is not reachable at all — raised by startup diagnostics and seeder." | kind=entity | source=manager/backend/app/auth/exceptions.py:L92 | neighbors=[DatabaseUnavailableError]
- "auth_exceptions_vedhaautherror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L20 | neighbors=[VedhaAuthError]
- "auth_jwt_decode_token": "decode_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L82 | neighbors=[jwt.py]
- "auth_jwt_rationale_39": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L39 | neighbors=[create_refresh_token()]
- "auth_jwt_rationale_61": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L61 | neighbors=[create_refresh_token()]
- "auth_jwt_rationale_68": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L68 | neighbors=[create_refresh_token()]
- "auth_middleware_rationale_15": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L15 | neighbors=[TenantIsolationMiddleware]
- "auth_middleware_rationale_20": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L20 | neighbors=[TenantIsolationMiddleware]
- "auth_middleware_rationale_21": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L21 | neighbors=[TenantIsolationMiddleware]
- "auth_middleware_rationale_38": "Least-privilege route allowlist for legacy probe access JWTs.      This is the i" | kind=entity | source=manager/backend/app/auth/middleware.py:L38 | neighbors=[agent_jwt_path_allows()]
- "auth_middleware_rationale_59": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L59 | neighbors=[TenantIsolationMiddleware]
- "auth_pat_pat_scope_allows": "pat_scope_allows()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L80 | neighbors=[pat.py]
- "auth_router_list_personal_access_tokens": "list_personal_access_tokens()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L302 | neighbors=[router.py]
- "auth_router_me": "me()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L217 | neighbors=[router.py]
- "auth_router_rationale_52": "Validates credentials and returns the User on success.     Raises a typed Authen" | kind=entity | source=manager/backend/app/auth/router.py:L52 | neighbors=[_authenticate()]
- "auth_router_rationale_59": "Validates credentials and returns the User on success.     Raises a typed Authen" | kind=entity | source=manager/backend/app/auth/router.py:L59 | neighbors=[_authenticate()]
- "auth_router_revoke_personal_access_token": "revoke_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L336 | neighbors=[router.py]
- "auth_startup_checkresult_fatal": ".fatal()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L62 | neighbors=[CheckResult]
- "auth_startup_checkresult_ok": ".ok()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L58 | neighbors=[CheckResult]
- "auth_startup_diagnosticsreport_all_ok": ".all_ok()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L77 | neighbors=[DiagnosticsReport]
- "auth_startup_diagnosticsreport_as_dict": ".as_dict()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L80 | neighbors=[DiagnosticsReport]
- "auth_startup_diagnosticsreport_has_fatal": ".has_fatal()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L73 | neighbors=[DiagnosticsReport]
- "auth_startup_get_last_report": "get_last_report()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L348 | neighbors=[startup.py]
- "auth_startup_rationale_1": "Startup diagnostics for Vedha Manager API.  Runs during FastAPI lifespan (before" | kind=entity | source=manager/backend/app/auth/startup.py:L1 | neighbors=[startup.py]
- "auth_startup_rationale_148": "Verify the bcrypt library can round-trip a hash — catches misconfigured passlib." | kind=entity | source=manager/backend/app/auth/startup.py:L148 | neighbors=[_check_bcrypt()]
- "auth_startup_rationale_160": "Verify the seeded admin account exists and is active." | kind=entity | source=manager/backend/app/auth/startup.py:L160 | neighbors=[_check_admin_account()]
- "auth_startup_rationale_198": "Verify the default tenant is active." | kind=entity | source=manager/backend/app/auth/startup.py:L198 | neighbors=[_check_tenant()]
- "auth_startup_rationale_283": "Run all startup checks concurrently.     Called from FastAPI lifespan before the" | kind=entity | source=manager/backend/app/auth/startup.py:L283 | neighbors=[run_startup_diagnostics()]
- "auth_startup_rationale_93": "Raised when one or more fatal checks fail — aborts app startup." | kind=entity | source=manager/backend/app/auth/startup.py:L93 | neighbors=[StartupAbortError]
- "basehttpmiddleware": "BaseHTTPMiddleware" | kind=code-symbol | neighbors=[TenantIsolationMiddleware]
- "basesettings": "BaseSettings" | kind=code-symbol | neighbors=[Settings]
- "brain_route_aimessage": "AiMessage" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L6 | neighbors=[route.ts]
- "brain_route_evidencetext": "evidenceText()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L40 | neighbors=[route.ts]
- "brain_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L11 | neighbors=[route.ts]
- "chat_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L11 | neighbors=[route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-110.json

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
