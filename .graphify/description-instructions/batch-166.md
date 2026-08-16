# Node Description Batch 167 of 209

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

- "services_posture_rationale_105": "True when the finding was live as of run_at (first_seen ≤ run_at ≤ last_seen)." | kind=entity | source=manager/backend/app/services/posture.py:L105 | neighbors=[_present_in_run()] | lang=en
- "services_posture_rationale_121": "Bucket findings across the previous→latest run transition." | kind=entity | source=manager/backend/app/services/posture.py:L121 | neighbors=[compare()] | lang=en
- "services_posture_rationale_164": "Full dashboard/report payload. Degrades gracefully with 0 or 1 run." | kind=entity | source=manager/backend/app/services/posture.py:L164 | neighbors=[build_posture()] | lang=en
- "services_posture_rationale_23": "Duck-typed projection of a Finding + its asset's criticality." | kind=entity | source=manager/backend/app/services/posture.py:L23 | neighbors=[FindingView] | lang=en
- "services_posture_rationale_48": "Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Empty → 0.0. Always in [0, 100]." | kind=entity | source=manager/backend/app/services/posture.py:L48 | neighbors=[aggregate()] | lang=en
- "services_risk_rank_compute_risk_rank": "compute_risk_rank()" | kind=code-symbol | source=manager/backend/app/services/risk_rank.py:L16 | neighbors=[risk_rank.py] | lang=en
- "services_risk_rank_rationale_1": "risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se" | kind=entity | source=manager/backend/app/services/risk_rank.py:L1 | neighbors=[risk_rank.py] | lang=en
- "services_scope_crypto_rationale_1": "scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 publi" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[scope_crypto.py] | lang=en
- "services_scope_crypto_rationale_35": "Encrypt scope JSON to a specific probe's X25519 public key.      Args:         s" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L35 | neighbors=[encrypt_scope()] | lang=en
- "services_scope_crypto_rationale_78": "Convenience: dict → JSON → encrypt → base64 string." | kind=entity | source=manager/backend/app/services/scope_crypto.py:L78 | neighbors=[encrypt_scope_b64()] | lang=en
- "services_scope_crypto_rationale_86": "Decode a base64-encoded X25519 public key to raw bytes.      Returns empty bytes" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L86 | neighbors=[public_key_from_b64()] | lang=en
- "services_scope_targets_rationale_1": "scope_targets.py — the single source of truth for \"is this scan target inside th" | kind=entity | source=manager/backend/app/services/scope_targets.py:L1 | neighbors=[scope_targets.py] | lang=en
- "services_scope_targets_rationale_38": "Expand raw target tokens (IP / CIDR / ``a-b`` range) into networks.      Returns" | kind=entity | source=manager/backend/app/services/scope_targets.py:L38 | neighbors=[_expand_requested()] | lang=en
- "services_scope_targets_rationale_71": "Return the normalized list of authorized target networks, or ``None``.      * ``" | kind=entity | source=manager/backend/app/services/scope_targets.py:L71 | neighbors=[validate_targets_in_scope()] | lang=en
- "services_sla_slaresult_is_tracked": ".is_tracked()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L56 | neighbors=[SlaResult] | lang=en
- "services_validation_ingest_rationale_1": "validation_ingest.py — turn a probe's safe active-validation result into a findi" | kind=entity | source=manager/backend/app/services/validation_ingest.py:L1 | neighbors=[validation_ingest.py] | lang=pt
- "services_validation_ingest_rationale_33": "Apply a validation verdict to a finding object (pure — no DB/session)." | kind=entity | source=manager/backend/app/services/validation_ingest.py:L33 | neighbors=[apply_validation_outcome()] | lang=pt
- "services_validation_ingest_rationale_45": "Cheap gate so normal scan submissions never trigger a lookup: a probe     valida" | kind=entity | source=manager/backend/app/services/validation_ingest.py:L45 | neighbors=[looks_like_validation_result()] | lang=pt
- "services_validation_ingest_rationale_52": "If ``job_id`` belongs to a ValidationRequest, store the result, set its     outc" | kind=entity | source=manager/backend/app/services/validation_ingest.py:L52 | neighbors=[ingest_validation_result()] | lang=en
- "settings_page_accesssection": "AccessSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L162 | neighbors=[page.tsx] | lang=en
- "settings_page_airuntimesection": "AiRuntimeSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L99 | neighbors=[page.tsx] | lang=en
- "settings_page_aistatus": "AiStatus" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L14 | neighbors=[page.tsx] | lang=en
- "settings_page_configfield": "ConfigField" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L30 | neighbors=[page.tsx] | lang=en
- "settings_page_default_rules": "DEFAULT_RULES" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L44 | neighbors=[page.tsx] | lang=en
- "settings_page_deploymentstatus": "DeploymentStatus" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L22 | neighbors=[page.tsx] | lang=en
- "settings_page_email_fields": "EMAIL_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L15 | neighbors=[page.tsx] | lang=en
- "settings_page_envsetting": "EnvSetting" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L12 | neighbors=[page.tsx] | lang=en
- "settings_page_integrationfields": "IntegrationFields()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L72 | neighbors=[page.tsx] | lang=en
- "settings_page_integrations": "INTEGRATIONS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L39 | neighbors=[page.tsx] | lang=en
- "settings_page_integrationsection": "IntegrationSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L193 | neighbors=[page.tsx] | lang=en
- "settings_page_jira_fields": "JIRA_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L28 | neighbors=[page.tsx] | lang=en
- "settings_page_notificationssection": "NotificationsSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L249 | neighbors=[page.tsx] | lang=en
- "settings_page_readonlynotice": "ReadOnlyNotice()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L90 | neighbors=[page.tsx] | lang=en
- "settings_page_sectionheader": "SectionHeader()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L54 | neighbors=[page.tsx] | lang=en
- "settings_page_sectiontitle": "SectionTitle()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L78 | neighbors=[page.tsx] | lang=en
- "settings_page_settingspage": "SettingsPage()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L273 | neighbors=[page.tsx] | lang=en
- "settings_page_sla_policy": "SLA_POLICY" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L71 | neighbors=[page.tsx] | lang=en
- "settings_page_slack_fields": "SLACK_FIELDS" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "settings_page_slasection": "SlaSection()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L232 | neighbors=[page.tsx] | lang=en
- "settings_page_testbutton": "TestButton()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L111 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-166.json

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
