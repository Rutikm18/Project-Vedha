# Node Description Batch 166 of 227

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
- "routers_engagements_engagementupdate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L496 | neighbors=[EngagementUpdate] | lang=en
- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L512 | neighbors=[EngagementUpdate] | lang=en
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L506 | neighbors=[EngagementUpdate] | lang=en
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L432 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L626 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L598 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L371 | neighbors=[engagements.py] | lang=en
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L337 | neighbors=[exploits.py] | lang=en
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L162 | neighbors=[findings.py] | lang=en
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L71 | neighbors=[findings.py] | lang=en
- "routers_findings_rationale_242": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L242 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_248": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L248 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_250": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L250 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_27": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L27 | neighbors=[_tenant_finding()] | lang=en
- "routers_findings_rationale_50": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L50 | neighbors=[sla_summary()] | lang=en
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L40 | neighbors=[health.py] | lang=en
- "routers_health_rationale_1": "Health endpoints.  GET /health          — liveness: DB + Redis reachability (fas" | kind=entity | source=manager/backend/app/routers/health.py:L1 | neighbors=[health.py] | lang=en
- "routers_health_rationale_163": "Returns the cached report from the last startup diagnostics run.     If the repo" | kind=entity | source=manager/backend/app/routers/health.py:L163 | neighbors=[health_startup()] | lang=en
- "routers_health_rationale_165": "Returns the cached report from the last startup diagnostics run.     If the repo" | kind=entity | source=manager/backend/app/routers/health.py:L165 | neighbors=[health_startup()] | lang=en
- "routers_health_rationale_82": "Validates the authentication subsystem without touching login state.     Returns" | kind=entity | source=manager/backend/app/routers/health.py:L82 | neighbors=[health_auth()] | lang=en
- "routers_integrations_rationale_1": "integrations.py — operator management of notification integrations (email/Slack/" | kind=entity | source=manager/backend/app/routers/integrations.py:L1 | neighbors=[integrations.py] | lang=en
- "routers_integrations_rationale_107": "Enqueue a durable test notification; the outbox worker fans it out to every" | kind=entity | source=manager/backend/app/routers/integrations.py:L107 | neighbors=[test_integrations()] | lang=en
- "routers_integrations_rationale_118": "Decrypt an integration's secret for the delivery worker (never the API)." | kind=entity | source=manager/backend/app/routers/integrations.py:L118 | neighbors=[integration_secret()] | lang=en
- "routers_portal_portal_finding": "portal_finding()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L118 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_findings": "portal_findings()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L100 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_report": "portal_report()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L254 | neighbors=[portal.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-165.json

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
