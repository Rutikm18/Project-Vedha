# Node Description Batch 241 of 336

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

- "routers_engagements_rationale_426": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L426 | neighbors=[engagements_overview()] | lang=en
- "routers_engagements_rationale_68": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L68 | neighbors=[_compute_overview()] | lang=en
- "routers_engagements_rationale_682": "Map a ScanJob status to the operator-facing scan phase shown on the card." | kind=entity | source=manager/backend/app/routers/engagements.py:L682 | neighbors=[_job_phase()] | lang=en
- "routers_engagements_rationale_685": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L685 | neighbors=[get_engagement_scope()] | lang=en
- "routers_engagements_rationale_699": "Derive ONE authoritative campaign phase from reconciled evidence, not from a" | kind=entity | source=manager/backend/app/routers/engagements.py:L699 | neighbors=[_reconcile_status()] | lang=en
- "routers_engagements_rationale_745": "A SAFE, bounded view of a job's raw result — the counts an operator needs to" | kind=entity | source=manager/backend/app/routers/engagements.py:L745 | neighbors=[_result_summary()] | lang=en
- "routers_engagements_rationale_767": "One call powers the VA Campaigns page: every probe's job (status + a safe raw" | kind=entity | source=manager/backend/app/routers/engagements.py:L767 | neighbors=[campaign_progress()] | lang=en
- "routers_engagements_rationale_99": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L99 | neighbors=[_refresh_overview_cache()] | lang=en
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L337 | neighbors=[exploits.py] | lang=en
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L203 | neighbors=[findings.py] | lang=en
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L109 | neighbors=[findings.py] | lang=en
- "routers_findings_rationale_242": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L242 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_248": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L248 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_250": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L250 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_269": "The finding's full lifecycle, oldest-first: stored audit events (who did     wha" | kind=entity | source=manager/backend/app/routers/findings.py:L269 | neighbors=[finding_timeline()] | lang=en
- "routers_findings_rationale_27": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L27 | neighbors=[_tenant_finding()] | lang=en
- "routers_findings_rationale_32": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L32 | neighbors=[_tenant_finding()] | lang=en
- "routers_findings_rationale_363": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L363 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_88": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L88 | neighbors=[sla_summary()] | lang=en
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L40 | neighbors=[health.py] | lang=en
- "routers_health_rationale_1": "Health endpoints.  GET /health          — liveness: DB + Redis reachability (fas" | kind=entity | source=manager/backend/app/routers/health.py:L1 | neighbors=[health.py] | lang=en
- "routers_health_rationale_163": "Returns the cached report from the last startup diagnostics run.     If the repo" | kind=entity | source=manager/backend/app/routers/health.py:L163 | neighbors=[health_startup()] | lang=en
- "routers_health_rationale_165": "Returns the cached report from the last startup diagnostics run.     If the repo" | kind=entity | source=manager/backend/app/routers/health.py:L165 | neighbors=[health_startup()] | lang=en
- "routers_health_rationale_82": "Validates the authentication subsystem without touching login state.     Returns" | kind=entity | source=manager/backend/app/routers/health.py:L82 | neighbors=[health_auth()] | lang=en
- "routers_integrations_rationale_1": "integrations.py — operator management of notification integrations (email/Slack/" | kind=entity | source=manager/backend/app/routers/integrations.py:L1 | neighbors=[integrations.py] | lang=en
- "routers_integrations_rationale_107": "Enqueue a durable test notification; the outbox worker fans it out to every" | kind=entity | source=manager/backend/app/routers/integrations.py:L107 | neighbors=[test_integrations()] | lang=en
- "routers_integrations_rationale_118": "Decrypt an integration's secret for the delivery worker (never the API)." | kind=entity | source=manager/backend/app/routers/integrations.py:L118 | neighbors=[integration_secret()] | lang=en
- "routers_portal_portal_activity": "portal_activity()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L541 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_exposure": "portal_exposure()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L520 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_finding": "portal_finding()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L123 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_findings": "portal_findings()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L105 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_posture_analytics": "portal_posture_analytics()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L527 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_report": "portal_report()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L259 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_reports": "portal_reports()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L248 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_sla_summary": "portal_sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L534 | neighbors=[portal.py] | lang=en
- "routers_portal_rationale_1": "portal.py — the CUSTOMER-facing read API (Part 2, Phase 2). Every route is scope" | kind=entity | source=manager/backend/app/routers/portal.py:L1 | neighbors=[portal.py] | lang=en
- "routers_portal_rationale_116": "Customer-facing structured remediation, replacing the plain `remediation`     st" | kind=entity | source=manager/backend/app/routers/portal.py:L116 | neighbors=[portal_finding_remediation()] | lang=en
- "routers_portal_rationale_134": "Customer-facing structured remediation, replacing the plain `remediation`     st" | kind=entity | source=manager/backend/app/routers/portal.py:L134 | neighbors=[portal_finding_remediation()] | lang=en
- "routers_portal_rationale_139": "Customer-facing structured remediation, replacing the plain `remediation`     st" | kind=entity | source=manager/backend/app/routers/portal.py:L139 | neighbors=[portal_finding_remediation()] | lang=en
- "routers_portal_rationale_417": "The whitelist that reaches the model — deliberately the same shape the     custo" | kind=entity | source=manager/backend/app/routers/portal.py:L417 | neighbors=[_assistant_finding_view()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-240.json

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
