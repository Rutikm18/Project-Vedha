# Node Description Batch 138 of 186

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

- "routers_agents_rationale_858": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L858 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_864": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L864 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_92": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L92 | neighbors=[_required_scan_type()] | lang=en
- "routers_agents_rationale_921": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L921 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_979": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L979 | neighbors=[get_job_status()] | lang=en
- "routers_ai_ai_generate": "ai_generate()" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L19 | neighbors=[ai.py] | lang=en
- "routers_ai_ai_status": "ai_status()" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L13 | neighbors=[ai.py] | lang=en
- "routers_ai_report_generate_report": "generate_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L64 | neighbors=[ai_report.py] | lang=en
- "routers_ai_report_rationale_192": "Deterministic report section from the same posture payload the dashboard uses." | kind=entity | source=manager/backend/app/routers/ai_report.py:L192 | neighbors=[build_posture_report_section()] | lang=en
- "routers_ai_report_rationale_293": "Background task: build the summary, generate every section, persist as pending." | kind=entity | source=manager/backend/app/routers/ai_report.py:L293 | neighbors=[_run_generation()] | lang=en
- "routers_ai_report_rationale_382": "Background task: regenerate rejected sections after human feedback." | kind=entity | source=manager/backend/app/routers/ai_report.py:L382 | neighbors=[_run_regeneration()] | lang=en
- "routers_ai_report_report_status": "report_status()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L92 | neighbors=[ai_report.py] | lang=en
- "routers_analytics_exposure": "exposure()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L46 | neighbors=[analytics.py] | lang=en
- "routers_analytics_rationale_87": "Map joined (Finding, Asset.criticality) rows to duck-typed views." | kind=entity | source=manager/backend/app/routers/analytics.py:L87 | neighbors=[_finding_views()] | lang=en
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
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L160 | neighbors=[findings.py] | lang=en
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L69 | neighbors=[findings.py] | lang=en
- "routers_findings_rationale_242": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L242 | neighbors=[reopen_finding()] | lang=pt
- "routers_findings_rationale_248": "Operator reverses a resolution (auto or manual). Only a `remediated`     finding" | kind=entity | source=manager/backend/app/routers/findings.py:L248 | neighbors=[reopen_finding()] | lang=pt
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L40 | neighbors=[health.py] | lang=en
- "routers_health_rationale_1": "Health endpoints.  GET /health          — liveness: DB + Redis reachability (fas" | kind=entity | source=manager/backend/app/routers/health.py:L1 | neighbors=[health.py] | lang=en
- "routers_health_rationale_165": "Returns the cached report from the last startup diagnostics run.     If the repo" | kind=entity | source=manager/backend/app/routers/health.py:L165 | neighbors=[health_startup()] | lang=en
- "routers_health_rationale_82": "Validates the authentication subsystem without touching login state.     Returns" | kind=entity | source=manager/backend/app/routers/health.py:L82 | neighbors=[health_auth()] | lang=en
- "routers_probe_enrollment_list_enrollment_requests": "list_enrollment_requests()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L428 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_1": "Device-code enrollment for probes; no human credential is installed on a probe." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_246": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L246 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_62": "Return (raw_token, token_hash, token_prefix). Raw is shown once." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[generate_enroll_token()] | lang=en
- "routers_probe_enrollment_rationale_68": "A token can auto-approve only while live, unrevoked, and under max_uses." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[enroll_token_is_usable()] | lang=en
- "routers_probe_enrollment_revoke_enroll_token": "revoke_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L682 | neighbors=[probe_enrollment.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-137.json

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
