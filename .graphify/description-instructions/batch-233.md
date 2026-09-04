# Node Description Batch 234 of 330

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

- "routers_ai_report_generate_report": "generate_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L64 | neighbors=[ai_report.py] | lang=en
- "routers_ai_report_rationale_192": "Deterministic report section from the same posture payload the dashboard uses." | kind=entity | source=manager/backend/app/routers/ai_report.py:L192 | neighbors=[build_posture_report_section()] | lang=en
- "routers_ai_report_rationale_293": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L293 | neighbors=[_run_generation()] | lang=en
- "routers_ai_report_rationale_382": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L382 | neighbors=[_run_regeneration()] | lang=en
- "routers_ai_report_report_status": "report_status()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L92 | neighbors=[ai_report.py] | lang=en
- "routers_analytics_exposure": "exposure()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L46 | neighbors=[analytics.py] | lang=en
- "routers_analytics_rationale_87": "Map joined (Finding, Asset.criticality) rows to duck-typed views." | kind=entity | source=manager/backend/app/routers/analytics.py:L87 | neighbors=[_finding_views()] | lang=en
- "routers_customer_access_assign_agent": "assign_agent()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L270 | neighbors=[customer_access.py] | lang=en
- "routers_customer_access_list_scan_requests": "list_scan_requests()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L308 | neighbors=[customer_access.py] | lang=en
- "routers_customer_access_rationale_1": "customer_access.py — operator-facing management of the customer portal (Part 2," | kind=entity | source=manager/backend/app/routers/customer_access.py:L1 | neighbors=[customer_access.py] | lang=en
- "routers_customer_access_rationale_101": "A lowercase, hyphenated, DNS-label-safe base for a customer portal handle     (s" | kind=entity | source=manager/backend/app/routers/customer_access.py:L101 | neighbors=[_slugify()] | lang=pt
- "routers_customer_access_rationale_102": "A lowercase, hyphenated, DNS-label-safe base for a customer portal handle     (s" | kind=entity | source=manager/backend/app/routers/customer_access.py:L102 | neighbors=[_slugify()] | lang=pt
- "routers_customer_access_rationale_103": "A lowercase, hyphenated, DNS-label-safe base for a customer portal handle     (s" | kind=entity | source=manager/backend/app/routers/customer_access.py:L103 | neighbors=[_slugify()] | lang=pt
- "routers_customer_access_rationale_108": "Per-tenant-unique portal slug: <base>, else <base>-2, <base>-3, … Two     custom" | kind=entity | source=manager/backend/app/routers/customer_access.py:L108 | neighbors=[_unique_portal_slug()] | lang=en
- "routers_customer_access_rationale_109": "Per-tenant-unique portal slug: <base>, else <base>-2, <base>-3, … Two     custom" | kind=entity | source=manager/backend/app/routers/customer_access.py:L109 | neighbors=[_unique_portal_slug()] | lang=en
- "routers_customer_access_rationale_110": "Per-tenant-unique portal slug: <base>, else <base>-2, <base>-3, … Two     custom" | kind=entity | source=manager/backend/app/routers/customer_access.py:L110 | neighbors=[_unique_portal_slug()] | lang=en
- "routers_customer_access_rationale_122": "Pure: turn an approved request into a pending ScanJob on the engagement's     as" | kind=entity | source=manager/backend/app/routers/customer_access.py:L122 | neighbors=[build_scan_job()] | lang=en
- "routers_customer_access_rationale_123": "Pure: turn an approved request into a pending ScanJob on the engagement's     as" | kind=entity | source=manager/backend/app/routers/customer_access.py:L123 | neighbors=[build_scan_job()] | lang=en
- "routers_customer_access_rationale_124": "Pure: turn an approved request into a pending ScanJob on the engagement's     as" | kind=entity | source=manager/backend/app/routers/customer_access.py:L124 | neighbors=[build_scan_job()] | lang=en
- "routers_customer_access_rationale_385": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L385 | neighbors=[list_customers()] | lang=en
- "routers_customer_access_rationale_394": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L394 | neighbors=[list_customers()] | lang=en
- "routers_customer_access_rationale_398": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L398 | neighbors=[list_customers()] | lang=en
- "routers_customer_access_rationale_400": "Every provisioned customer login (role=client) in the tenant, with its     bound" | kind=entity | source=manager/backend/app/routers/customer_access.py:L400 | neighbors=[list_customers()] | lang=en
- "routers_customer_access_rationale_430": "Decrypt and return a customer login's stored password. Tenant-scoped and     wri" | kind=entity | source=manager/backend/app/routers/customer_access.py:L430 | neighbors=[reveal_customer_password()] | lang=en
- "routers_customer_access_rationale_432": "Decrypt and return a customer login's stored password. Tenant-scoped and     wri" | kind=entity | source=manager/backend/app/routers/customer_access.py:L432 | neighbors=[reveal_customer_password()] | lang=en
- "routers_customer_access_rationale_96": "A URL-safe temporary password the operator hands to the customer once." | kind=entity | source=manager/backend/app/routers/customer_access.py:L96 | neighbors=[generate_password()] | lang=en
- "routers_customer_access_rationale_97": "A URL-safe temporary password the operator hands to the customer once." | kind=entity | source=manager/backend/app/routers/customer_access.py:L97 | neighbors=[generate_password()] | lang=en
- "routers_customer_access_rationale_98": "A URL-safe temporary password the operator hands to the customer once." | kind=entity | source=manager/backend/app/routers/customer_access.py:L98 | neighbors=[generate_password()] | lang=en
- "routers_detection_configure_siem": "configure_siem()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L61 | neighbors=[detection.py] | lang=en
- "routers_detection_get_coverage": "get_coverage()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L148 | neighbors=[detection.py] | lang=en
- "routers_detection_get_gaps": "get_gaps()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L187 | neighbors=[detection.py] | lang=en
- "routers_detection_run_validation": "run_validation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L96 | neighbors=[detection.py] | lang=en
- "routers_engagements_engagementupdate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L523 | neighbors=[EngagementUpdate] | lang=en
- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L539 | neighbors=[EngagementUpdate] | lang=en
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L533 | neighbors=[EngagementUpdate] | lang=en
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L459 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1222 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L625 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[engagements.py] | lang=en
- "routers_engagements_rationale_1115": "The machine-readable answer to \"the scripts catch it but the manager doesn't\"." | kind=entity | source=manager/backend/app/routers/engagements.py:L1115 | neighbors=[detection_explain()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-233.json

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
