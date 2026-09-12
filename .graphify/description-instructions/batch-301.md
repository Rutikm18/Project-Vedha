# Node Description Batch 302 of 380

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

- "settings_page_configfield": "ConfigField" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L38 | neighbors=[page.tsx]
- "settings_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L199 | neighbors=[page.tsx]
- "settings_page_default_rules": "DEFAULT_RULES" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L745 | neighbors=[page.tsx]
- "settings_page_deploymentstatus": "DeploymentStatus" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L30 | neighbors=[page.tsx]
- "settings_page_email_fields": "EMAIL_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L15 | neighbors=[page.tsx]
- "settings_page_engagementsection": "EngagementSection()" | kind=code-symbol | source=manager/frontend/app/portal/settings/page.tsx:L32 | neighbors=[page.tsx]
- "settings_page_envsetting": "EnvSetting" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L12 | neighbors=[page.tsx]
- "settings_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L223 | neighbors=[page.tsx]
- "settings_page_formatrelative": "formatRelative()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L211 | neighbors=[page.tsx]
- "settings_page_integrationfields": "IntegrationFields()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L72 | neighbors=[page.tsx]
- "settings_page_integrationrow": "IntegrationRow" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L57 | neighbors=[page.tsx]
- "settings_page_integrations": "INTEGRATIONS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L106 | neighbors=[page.tsx]
- "settings_page_jira_fields": "JIRA_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L28 | neighbors=[page.tsx]
- "settings_page_nav_sections": "NAV_SECTIONS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L147 | neighbors=[page.tsx]
- "settings_page_notificationssection": "NotificationsSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L755 | neighbors=[page.tsx]
- "settings_page_pat": "Pat" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L74 | neighbors=[page.tsx]
- "settings_page_portal_nav_sections": "PORTAL_NAV_SECTIONS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L162 | neighbors=[page.tsx]
- "settings_page_portalsettings": "PortalSettings()" | kind=code-symbol | source=manager/frontend/app/portal/settings/page.tsx:L136 | neighbors=[page.tsx]
- "settings_page_portalsettingspage": "PortalSettingsPage()" | kind=code-symbol | source=manager/frontend/app/portal/settings/page.tsx:L5 | neighbors=[page.tsx]
- "settings_page_probefleetsection": "ProbeFleetSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L419 | neighbors=[page.tsx]
- "settings_page_readonlynotice": "ReadOnlyNotice()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L179 | neighbors=[page.tsx]
- "settings_page_role_colors": "ROLE_COLORS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L138 | neighbors=[page.tsx]
- "settings_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L54 | neighbors=[page.tsx]
- "settings_page_sectiontitle": "SectionTitle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L167 | neighbors=[page.tsx]
- "settings_page_settingspage": "SettingsPage()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L924 | neighbors=[page.tsx]
- "settings_page_settingsworkspace": "SettingsWorkspace()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L861 | neighbors=[page.tsx]
- "settings_page_sla_policy": "SLA_POLICY" | kind=code-symbol | source=manager/frontend/app/portal/settings/page.tsx:L13 | neighbors=[page.tsx]
- "settings_page_sla_rows": "SLA_ROWS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L681 | neighbors=[page.tsx]
- "settings_page_slack_fields": "SLACK_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L24 | neighbors=[page.tsx]
- "settings_page_slaform": "SlaForm" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L55 | neighbors=[page.tsx]
- "settings_page_slapolicyresp": "SlaPolicyResp" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L47 | neighbors=[page.tsx]
- "settings_page_slasection": "SlaSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L689 | neighbors=[page.tsx]
- "settings_page_teamsection": "TeamSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L231 | neighbors=[page.tsx]
- "settings_page_teamuser": "TeamUser" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L64 | neighbors=[page.tsx]
- "settings_page_testbutton": "TestButton()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L111 | neighbors=[page.tsx]
- "settings_page_toggle": "Toggle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L141 | neighbors=[page.tsx]
- "siem_config_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L5 | neighbors=[route.ts]
- "siem_config_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L14 | neighbors=[route.ts]
- "sla_policy_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/sla-policy/route.ts:L10 | neighbors=[route.ts]
- "sla_policy_route_put": "PUT" | kind=code-symbol | source=manager/frontend/app/api/sla-policy/route.ts:L14 | neighbors=[route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-301.json

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
