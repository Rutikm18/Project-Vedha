# Node Description Batch 172 of 236

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

- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L599 | neighbors=[engagements.py] | lang=en
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L372 | neighbors=[engagements.py] | lang=en
- "routers_engagements_rationale_130": "Re-runs the detection pipeline against the CURRENT pinned vuln DB using     the" | kind=entity | source=manager/backend/app/routers/engagements.py:L130 | neighbors=[re_detect()] | lang=en
- "routers_engagements_rationale_163": "Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded     — s" | kind=entity | source=manager/backend/app/routers/engagements.py:L163 | neighbors=[_read_capped()] | lang=en
- "routers_engagements_rationale_181": "Parse a probe export into (facts, scan_type).      Accepts two shapes the probe" | kind=entity | source=manager/backend/app/routers/engagements.py:L181 | neighbors=[_parse_probe_file()] | lang=en
- "routers_engagements_rationale_228": "Upsert assets (and their services) from raw ScanResult facts.      Mirrors `agen" | kind=entity | source=manager/backend/app/routers/engagements.py:L228 | neighbors=[_promote_from_facts()] | lang=en
- "routers_engagements_rationale_302": "Offline ingest path: upload a probe's scan export and run it through the     SAM" | kind=entity | source=manager/backend/app/routers/engagements.py:L302 | neighbors=[import_facts()] | lang=en
- "routers_engagements_rationale_400": "P1: kills the BFF N+1 (was list + one detail call per engagement).     Computes" | kind=entity | source=manager/backend/app/routers/engagements.py:L400 | neighbors=[engagements_overview()] | lang=en
- "routers_engagements_rationale_42": "Shared aggregation — used by both the cached read path (ReadDB) and the     writ" | kind=entity | source=manager/backend/app/routers/engagements.py:L42 | neighbors=[_compute_overview()] | lang=en
- "routers_engagements_rationale_685": "Probe-facing: the probe calls this independently before scanning a job to     re" | kind=entity | source=manager/backend/app/routers/engagements.py:L685 | neighbors=[get_engagement_scope()] | lang=en
- "routers_engagements_rationale_99": "Write-through cache refresh on the WRITE session, right after flush.      Replac" | kind=entity | source=manager/backend/app/routers/engagements.py:L99 | neighbors=[_refresh_overview_cache()] | lang=en
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
- "routers_portal_portal_reports": "portal_reports()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L243 | neighbors=[portal.py] | lang=en
- "routers_portal_rationale_1": "portal.py — the CUSTOMER-facing read API (Part 2, Phase 2). Every route is scope" | kind=entity | source=manager/backend/app/routers/portal.py:L1 | neighbors=[portal.py] | lang=en
- "routers_portal_rationale_116": "Customer-facing structured remediation, replacing the plain `remediation`     st" | kind=entity | source=manager/backend/app/routers/portal.py:L116 | neighbors=[portal_finding_remediation()] | lang=en
- "routers_portal_rationale_134": "Customer-facing structured remediation, replacing the plain `remediation`     st" | kind=entity | source=manager/backend/app/routers/portal.py:L134 | neighbors=[portal_finding_remediation()] | lang=en
- "routers_portal_rationale_71": "The operator use-case catalog (single source of truth), curated to what a     cu" | kind=entity | source=manager/backend/app/routers/portal.py:L71 | neighbors=[_portal_use_cases()] | lang=en
- "routers_probe_enrollment_list_enrollment_requests": "list_enrollment_requests()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L504 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_1": "Device-code enrollment for probes; no human credential is installed on a probe." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_246": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L246 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_247": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L247 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_314": "Parse settings.probe_auto_enroll_cidrs → a non-empty CIDR list (RFC1918     defa" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L314 | neighbors=[auto_enroll_cidrs()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-171.json

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
