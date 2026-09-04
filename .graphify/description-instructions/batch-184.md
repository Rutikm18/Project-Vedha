# Node Description Batch 185 of 330

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

- "auth_portal_scope_rationale_75": "Role gate for portal routes — 403 unless a properly-bound client." | kind=entity | source=manager/backend/app/auth/portal_scope.py:L75 | neighbors=[require_client()]
- "auth_portal_scope_rationale_82": "Route dependency yielding the client's engagement id, rejecting any     mismatch" | kind=entity | source=manager/backend/app/auth/portal_scope.py:L82 | neighbors=[scoped_engagement()]
- "auth_portal_scope_rationale_84": "Route dependency yielding the client's engagement id, rejecting any     mismatch" | kind=entity | source=manager/backend/app/auth/portal_scope.py:L84 | neighbors=[scoped_engagement()]
- "auth_router_list_personal_access_tokens": "list_personal_access_tokens()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L302 | neighbors=[router.py]
- "auth_router_me": "me()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L217 | neighbors=[router.py]
- "auth_router_rationale_52": "Validates credentials and returns the User on success.     Raises a typed Authen" | kind=entity | source=manager/backend/app/auth/router.py:L52 | neighbors=[_authenticate()]
- "auth_router_rationale_59": "Validates credentials and returns the User on success.     Raises a typed Authen" | kind=entity | source=manager/backend/app/auth/router.py:L59 | neighbors=[_authenticate()]
- "auth_router_revoke_personal_access_token": "revoke_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L336 | neighbors=[router.py]
- "auth_startup_checkresult_fatal": ".fatal()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L60 | neighbors=[CheckResult]
- "auth_startup_checkresult_ok": ".ok()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L56 | neighbors=[CheckResult]
- "auth_startup_diagnosticsreport_all_ok": ".all_ok()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L75 | neighbors=[DiagnosticsReport]
- "auth_startup_diagnosticsreport_as_dict": ".as_dict()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L78 | neighbors=[DiagnosticsReport]
- "auth_startup_diagnosticsreport_has_fatal": ".has_fatal()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L71 | neighbors=[DiagnosticsReport]
- "auth_startup_get_last_report": "get_last_report()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L346 | neighbors=[startup.py]
- "auth_startup_rationale_1": "Startup diagnostics for Vedha Manager API.  Runs during FastAPI lifespan (before" | kind=entity | source=manager/backend/app/auth/startup.py:L1 | neighbors=[startup.py]
- "auth_startup_rationale_146": "Verify the bcrypt library can round-trip a hash — catches misconfigured passlib." | kind=entity | source=manager/backend/app/auth/startup.py:L146 | neighbors=[_check_bcrypt()]
- "auth_startup_rationale_148": "Verify the bcrypt library can round-trip a hash — catches misconfigured passlib." | kind=entity | source=manager/backend/app/auth/startup.py:L148 | neighbors=[_check_bcrypt()]
- "auth_startup_rationale_158": "Verify the seeded admin account exists and is active." | kind=entity | source=manager/backend/app/auth/startup.py:L158 | neighbors=[_check_admin_account()]
- "auth_startup_rationale_160": "Verify the seeded admin account exists and is active." | kind=entity | source=manager/backend/app/auth/startup.py:L160 | neighbors=[_check_admin_account()]
- "auth_startup_rationale_196": "Verify the default tenant is active." | kind=entity | source=manager/backend/app/auth/startup.py:L196 | neighbors=[_check_tenant()]
- "auth_startup_rationale_198": "Verify the default tenant is active." | kind=entity | source=manager/backend/app/auth/startup.py:L198 | neighbors=[_check_tenant()]
- "auth_startup_rationale_281": "Run all startup checks concurrently.     Called from FastAPI lifespan before the" | kind=entity | source=manager/backend/app/auth/startup.py:L281 | neighbors=[run_startup_diagnostics()]
- "auth_startup_rationale_283": "Run all startup checks concurrently.     Called from FastAPI lifespan before the" | kind=entity | source=manager/backend/app/auth/startup.py:L283 | neighbors=[run_startup_diagnostics()]
- "auth_startup_rationale_91": "Raised when one or more fatal checks fail — aborts app startup." | kind=entity | source=manager/backend/app/auth/startup.py:L91 | neighbors=[StartupAbortError]
- "auth_startup_rationale_93": "Raised when one or more fatal checks fail — aborts app startup." | kind=entity | source=manager/backend/app/auth/startup.py:L93 | neighbors=[StartupAbortError]
- "basehttpmiddleware": "BaseHTTPMiddleware" | kind=code-symbol | neighbors=[TenantIsolationMiddleware]
- "basesettings": "BaseSettings" | kind=code-symbol | neighbors=[Settings]
- "brain_route_aimessage": "AiMessage" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L6 | neighbors=[route.ts]
- "brain_route_evidencetext": "evidenceText()" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L40 | neighbors=[route.ts]
- "brain_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/brain/route.ts:L11 | neighbors=[route.ts]
- "campaign_page_ago": "ago()" | kind=code-symbol | source=manager/frontend/app/campaign/page.tsx:L32 | neighbors=[page.tsx]
- "campaign_page_campaignlistpage": "CampaignListPage()" | kind=code-symbol | source=manager/frontend/app/campaign/page.tsx:L41 | neighbors=[page.tsx]
- "campaign_page_campaignsummary": "CampaignSummary" | kind=code-symbol | source=manager/frontend/app/campaign/page.tsx:L10 | neighbors=[page.tsx]
- "campaign_page_engagementsummary": "EngagementSummary" | kind=code-symbol | source=manager/frontend/app/campaign/page.tsx:L16 | neighbors=[page.tsx]
- "campaign_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/campaign/page.tsx:L25 | neighbors=[page.tsx]
- "campaigns_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/scan/campaigns/route.ts:L17 | neighbors=[route.ts]
- "campaigns_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/campaigns/route.ts:L21 | neighbors=[route.ts]
- "cancel_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/fleet/jobs/[jobId]/cancel/route.ts:L17 | neighbors=[route.ts]
- "chat_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L11 | neighbors=[route.ts]
- "chat_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L20 | neighbors=[route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-184.json

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
