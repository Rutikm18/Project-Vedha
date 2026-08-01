# Node Description Batch 96 of 119

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

- "schemas_asset_assetin_validate_ip": ".validate_ip()" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L23 | neighbors=[AssetIn]
- "schemas_auth_rationale_18": "Parsed from JWT claims — attached to request.state and injected as dependency." | kind=entity | source=manager/backend/app/schemas/auth.py:L18 | neighbors=[CurrentUser]
- "schemas_auth_rationale_21": "Parsed from JWT claims — attached to request.state and injected as dependency." | kind=entity | source=manager/backend/app/schemas/auth.py:L21 | neighbors=[CurrentUser]
- "schemas_engagement_engagementcreate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L54 | neighbors=[EngagementCreate]
- "scripts_seed_admin_seed": "seed()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L40 | neighbors=[seed_admin.py]
- "services_analytics_rationale_1": "Exposure analytics — protocol risk + zone health.  Derives two dashboard aggrega" | kind=entity | source=manager/backend/app/services/analytics.py:L1 | neighbors=[analytics.py]
- "services_llm_airuntimeerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L22 | neighbors=[AiRuntimeError]
- "services_llm_managerllmservice_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L65 | neighbors=[ManagerLlmService]
- "services_scope_crypto_rationale_1": "scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 publi" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[scope_crypto.py]
- "services_scope_crypto_rationale_35": "Encrypt scope JSON to a specific probe's X25519 public key.      Args:         s" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L35 | neighbors=[encrypt_scope()]
- "services_scope_crypto_rationale_78": "Convenience: dict → JSON → encrypt → base64 string." | kind=entity | source=manager/backend/app/services/scope_crypto.py:L78 | neighbors=[encrypt_scope_b64()]
- "services_scope_crypto_rationale_86": "Decode a base64-encoded X25519 public key to raw bytes.      Returns empty bytes" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L86 | neighbors=[public_key_from_b64()]
- "services_sla_slaresult_is_tracked": ".is_tracked()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L56 | neighbors=[SlaResult]
- "settings_page_accesssection": "AccessSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L162 | neighbors=[page.tsx]
- "settings_page_airuntimesection": "AiRuntimeSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L99 | neighbors=[page.tsx]
- "settings_page_aistatus": "AiStatus" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L14 | neighbors=[page.tsx]
- "settings_page_configfield": "ConfigField" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L30 | neighbors=[page.tsx]
- "settings_page_default_rules": "DEFAULT_RULES" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L44 | neighbors=[page.tsx]
- "settings_page_deploymentstatus": "DeploymentStatus" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L22 | neighbors=[page.tsx]
- "settings_page_email_fields": "EMAIL_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L15 | neighbors=[page.tsx]
- "settings_page_envsetting": "EnvSetting" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L12 | neighbors=[page.tsx]
- "settings_page_integrationfields": "IntegrationFields()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L72 | neighbors=[page.tsx]
- "settings_page_integrations": "INTEGRATIONS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L39 | neighbors=[page.tsx]
- "settings_page_integrationsection": "IntegrationSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L193 | neighbors=[page.tsx]
- "settings_page_jira_fields": "JIRA_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L28 | neighbors=[page.tsx]
- "settings_page_notificationssection": "NotificationsSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L249 | neighbors=[page.tsx]
- "settings_page_readonlynotice": "ReadOnlyNotice()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L90 | neighbors=[page.tsx]
- "settings_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L54 | neighbors=[page.tsx]
- "settings_page_sectiontitle": "SectionTitle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L78 | neighbors=[page.tsx]
- "settings_page_settingspage": "SettingsPage()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L273 | neighbors=[page.tsx]
- "settings_page_sla_policy": "SLA_POLICY" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L71 | neighbors=[page.tsx]
- "settings_page_slack_fields": "SLACK_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L24 | neighbors=[page.tsx]
- "settings_page_slasection": "SlaSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L232 | neighbors=[page.tsx]
- "settings_page_testbutton": "TestButton()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L111 | neighbors=[page.tsx]
- "settings_page_toggle": "Toggle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L141 | neighbors=[page.tsx]
- "siem_config_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L5 | neighbors=[route.ts]
- "siem_config_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L14 | neighbors=[route.ts]
- "sla_summary_route_apislaitem": "ApiSlaItem" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L17 | neighbors=[route.ts]
- "sla_summary_route_apislasummary": "ApiSlaSummary" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L22 | neighbors=[route.ts]
- "sla_summary_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L27 | neighbors=[route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-095.json

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
