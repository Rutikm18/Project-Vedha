# Node Description Batch 263 of 330

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "settings_page_probefleetsection": "ProbeFleetSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L411 | neighbors=[page.tsx] | lang=en
- "settings_page_readonlynotice": "ReadOnlyNotice()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L171 | neighbors=[page.tsx] | lang=en
- "settings_page_role_colors": "ROLE_COLORS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L133 | neighbors=[page.tsx] | lang=en
- "settings_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L54 | neighbors=[page.tsx] | lang=en
- "settings_page_sectiontitle": "SectionTitle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L159 | neighbors=[page.tsx] | lang=en
- "settings_page_settingspage": "SettingsPage()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L839 | neighbors=[page.tsx] | lang=en
- "settings_page_sla_policy": "SLA_POLICY" | kind=code-symbol | source=manager/frontend/app/portal/settings/page.tsx:L13 | neighbors=[page.tsx] | lang=en
- "settings_page_sla_rows": "SLA_ROWS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L660 | neighbors=[page.tsx] | lang=en
- "settings_page_slack_fields": "SLACK_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "settings_page_slaform": "SlaForm" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L50 | neighbors=[page.tsx] | lang=en
- "settings_page_slapolicyresp": "SlaPolicyResp" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L42 | neighbors=[page.tsx] | lang=en
- "settings_page_slasection": "SlaSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L668 | neighbors=[page.tsx] | lang=en
- "settings_page_teamsection": "TeamSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L223 | neighbors=[page.tsx] | lang=en
- "settings_page_teamuser": "TeamUser" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L59 | neighbors=[page.tsx] | lang=en
- "settings_page_testbutton": "TestButton()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L111 | neighbors=[page.tsx] | lang=en
- "settings_page_toggle": "Toggle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L141 | neighbors=[page.tsx] | lang=en
- "siem_config_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L5 | neighbors=[route.ts] | lang=en
- "siem_config_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L14 | neighbors=[route.ts] | lang=en
- "sla_policy_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/sla-policy/route.ts:L10 | neighbors=[route.ts] | lang=en
- "sla_policy_route_put": "PUT" | kind=code-symbol | source=manager/frontend/app/api/sla-policy/route.ts:L14 | neighbors=[route.ts] | lang=en
- "sla_summary_route_apislaitem": "ApiSlaItem" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L17 | neighbors=[route.ts] | lang=en
- "sla_summary_route_apislasummary": "ApiSlaSummary" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L22 | neighbors=[route.ts] | lang=en
- "sla_summary_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L27 | neighbors=[route.ts] | lang=en
- "sla_summary_route_sev_to_ui": "SEV_TO_UI" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L13 | neighbors=[route.ts] | lang=en
- "states_datastate_btn": "btn" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L135 | neighbors=[DataState.tsx] | lang=en
- "states_datastate_center": "center" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L130 | neighbors=[DataState.tsx] | lang=en
- "states_datastate_datastateprops": "DataStateProps" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L96 | neighbors=[DataState.tsx] | lang=en
- "states_datastate_offlinebanner": "OfflineBanner()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L83 | neighbors=[DataState.tsx] | lang=en
- "states_datastate_unauthorized": "Unauthorized()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L70 | neighbors=[DataState.tsx] | lang=en
- "status_route_required": "required" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L4 | neighbors=[route.ts] | lang=en
- "summary_route_apisummary": "ApiSummary" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L5 | neighbors=[route.ts] | lang=en
- "summary_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L18 | neighbors=[route.ts] | lang=en
- "supporting_research_evidence_store_connect": "connect()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L89 | neighbors=[evidence_store.py] | lang=en
- "supporting_research_evidence_store_identityresult_asset_count": ".asset_count()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L139 | neighbors=[IdentityResult] | lang=en
- "supporting_research_evidence_store_identityresult_observations_for": ".observations_for()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L142 | neighbors=[IdentityResult] | lang=en
- "supporting_research_evidence_store_rationale_1": "vedha_ref.evidence_store -- the layer the whole strategy rests on.  Thesis under" | kind=entity | source=Supporting_research/evidence_store.py:L1 | neighbors=[evidence_store.py] | lang=en
- "supporting_research_evidence_store_rationale_175": "Cluster observations into assets using fingerprint keys.      Strong keys merge" | kind=entity | source=Supporting_research/evidence_store.py:L175 | neighbors=[resolve_identity()] | lang=en
- "supporting_research_evidence_store_rationale_258": "The industry default, for comparison. Included so the cost is measurable." | kind=entity | source=Supporting_research/evidence_store.py:L258 | neighbors=[naive_ip_identity()] | lang=en
- "supporting_research_evidence_store_rationale_300": "Answer a brand-new rule against evidence already on disk.      No network traffi" | kind=entity | source=Supporting_research/evidence_store.py:L300 | neighbors=[retroactive_detect()] | lang=pt
- "supporting_research_evidence_store_rationale_363": "What a customer should actually be shown: three numbers, not one." | kind=entity | source=Supporting_research/evidence_store.py:L363 | neighbors=[coverage_summary()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-262.json

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
