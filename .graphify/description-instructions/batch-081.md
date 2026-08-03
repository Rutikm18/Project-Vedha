# Node Description Batch 82 of 131

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

- "assistant_assistanttext_plain": "plain()" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L5 | neighbors=[AssistantText.tsx]
- "assistant_factcard_pip": "Pip()" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L10 | neighbors=[FactCard.tsx]
- "attack_graph_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L5 | neighbors=[route.ts]
- "attack_paths_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L5 | neighbors=[route.ts]
- "auth_exceptions_rationale_1": "Typed exception hierarchy for Vedha authentication.  Design principle:   - Every" | kind=entity | source=manager/backend/app/auth/exceptions.py:L1 | neighbors=[exceptions.py]
- "auth_exceptions_rationale_16": "Base for all Vedha auth exceptions." | kind=entity | source=manager/backend/app/auth/exceptions.py:L16 | neighbors=[VedhaAuthError]
- "auth_exceptions_rationale_29": "A login attempt failed for any reason." | kind=entity | source=manager/backend/app/auth/exceptions.py:L29 | neighbors=[AuthenticationError]
- "auth_exceptions_rationale_34": "No user record for the supplied email." | kind=entity | source=manager/backend/app/auth/exceptions.py:L34 | neighbors=[UserNotFoundError]
- "auth_exceptions_rationale_39": "User exists but supplied password does not match the stored hash." | kind=entity | source=manager/backend/app/auth/exceptions.py:L39 | neighbors=[PasswordMismatchError]
- "auth_exceptions_rationale_44": "User account exists but is_active=False." | kind=entity | source=manager/backend/app/auth/exceptions.py:L44 | neighbors=[DisabledUserError]
- "auth_exceptions_rationale_49": "Tenant account is disabled — all users in it are locked out." | kind=entity | source=manager/backend/app/auth/exceptions.py:L49 | neighbors=[DisabledTenantError]
- "auth_exceptions_rationale_54": "User's password_expires_at is in the past — must rotate before logging in." | kind=entity | source=manager/backend/app/auth/exceptions.py:L54 | neighbors=[ExpiredPasswordError]
- "auth_exceptions_rationale_59": "bcrypt raised an exception during verification — indicates a corrupt hash or lib" | kind=entity | source=manager/backend/app/auth/exceptions.py:L59 | neighbors=[BcryptFailureError]
- "auth_exceptions_rationale_64": "Could not reach the database during authentication — infrastructure failure." | kind=entity | source=manager/backend/app/auth/exceptions.py:L64 | neighbors=[DatabaseFailureError]
- "auth_exceptions_rationale_69": "JWT token could not be created — JWT_SECRET missing or library failure." | kind=entity | source=manager/backend/app/auth/exceptions.py:L69 | neighbors=[JWTFailureError]
- "auth_exceptions_rationale_74": "Caller exceeded the login rate limit — already handled by the rate-limit middlew" | kind=entity | source=manager/backend/app/auth/exceptions.py:L74 | neighbors=[RateLimitError]
- "auth_exceptions_rationale_82": "Required env var missing, value invalid, or weak password in production." | kind=entity | source=manager/backend/app/auth/exceptions.py:L82 | neighbors=[SeedConfigurationError]
- "auth_exceptions_rationale_87": "Password rotation was requested but could not complete (hash verify failed, etc." | kind=entity | source=manager/backend/app/auth/exceptions.py:L87 | neighbors=[PasswordRotationError]
- "auth_exceptions_rationale_92": "Database is not reachable at all — raised by startup diagnostics and seeder." | kind=entity | source=manager/backend/app/auth/exceptions.py:L92 | neighbors=[DatabaseUnavailableError]
- "auth_exceptions_vedhaautherror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L20 | neighbors=[VedhaAuthError]
- "auth_jwt_decode_token": "decode_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L75 | neighbors=[jwt.py]
- "auth_jwt_rationale_39": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L39 | neighbors=[create_refresh_token()]
- "auth_jwt_rationale_61": "Returns (token, jti) — jti is stored in Redis for revocation." | kind=entity | source=manager/backend/app/auth/jwt.py:L61 | neighbors=[create_refresh_token()]
- "auth_middleware_rationale_15": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L15 | neighbors=[TenantIsolationMiddleware]
- "auth_middleware_rationale_20": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L20 | neighbors=[TenantIsolationMiddleware]
- "auth_middleware_rationale_21": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L21 | neighbors=[TenantIsolationMiddleware]
- "auth_middleware_rationale_38": "Least-privilege route allowlist for legacy probe access JWTs.      This is the i" | kind=entity | source=manager/backend/app/auth/middleware.py:L38 | neighbors=[agent_jwt_path_allows()]
- "auth_middleware_rationale_59": "Extracts JWT from Authorization header and injects tenant_id + user     claims i" | kind=entity | source=manager/backend/app/auth/middleware.py:L59 | neighbors=[TenantIsolationMiddleware]
- "auth_pat_pat_scope_allows": "pat_scope_allows()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L80 | neighbors=[pat.py]
- "auth_router_list_personal_access_tokens": "list_personal_access_tokens()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L280 | neighbors=[router.py]
- "auth_router_me": "me()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L195 | neighbors=[router.py]
- "auth_router_rationale_52": "Validates credentials and returns the User on success.     Raises a typed Authen" | kind=entity | source=manager/backend/app/auth/router.py:L52 | neighbors=[_authenticate()]
- "auth_router_revoke_personal_access_token": "revoke_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L314 | neighbors=[router.py]
- "auth_startup_checkresult_fatal": ".fatal()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L62 | neighbors=[CheckResult]
- "auth_startup_checkresult_ok": ".ok()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L58 | neighbors=[CheckResult]
- "auth_startup_diagnosticsreport_all_ok": ".all_ok()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L77 | neighbors=[DiagnosticsReport]
- "auth_startup_diagnosticsreport_as_dict": ".as_dict()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L80 | neighbors=[DiagnosticsReport]
- "auth_startup_diagnosticsreport_has_fatal": ".has_fatal()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L73 | neighbors=[DiagnosticsReport]
- "auth_startup_get_last_report": "get_last_report()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L348 | neighbors=[startup.py]
- "auth_startup_rationale_1": "Startup diagnostics for Vedha Manager API.  Runs during FastAPI lifespan (before" | kind=entity | source=manager/backend/app/auth/startup.py:L1 | neighbors=[startup.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-081.json

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
