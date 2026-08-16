# Node Description Batch 154 of 209

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
- "routers_portal_create_scan_request": "create_scan_request()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L280 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_finding": "portal_finding()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L100 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_findings": "portal_findings()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L82 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_report": "portal_report()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L234 | neighbors=[portal.py] | lang=en
- "routers_portal_portal_reports": "portal_reports()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L223 | neighbors=[portal.py] | lang=en
- "routers_portal_rationale_1": "portal.py — the CUSTOMER-facing read API (Part 2, Phase 2). Every route is scope" | kind=entity | source=manager/backend/app/routers/portal.py:L1 | neighbors=[portal.py] | lang=en
- "routers_portal_rationale_116": "Customer-facing structured remediation, replacing the plain `remediation`     st" | kind=entity | source=manager/backend/app/routers/portal.py:L116 | neighbors=[portal_finding_remediation()] | lang=en
- "routers_probe_enrollment_list_enrollment_requests": "list_enrollment_requests()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L504 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_1": "Device-code enrollment for probes; no human credential is installed on a probe." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_246": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L246 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_247": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L247 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_314": "Parse settings.probe_auto_enroll_cidrs → a non-empty CIDR list (RFC1918     defa" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L314 | neighbors=[auto_enroll_cidrs()] | lang=pt
- "routers_probe_enrollment_rationale_322": "The singleton per-tenant Site that trust-on-first-use enrollment binds to." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L322 | neighbors=[_get_or_create_auto_enroll_site()] | lang=en
- "routers_probe_enrollment_rationale_62": "Return (raw_token, token_hash, token_prefix). Raw is shown once." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[generate_enroll_token()] | lang=en
- "routers_probe_enrollment_rationale_63": "Return (raw_token, token_hash, token_prefix). Raw is shown once." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L63 | neighbors=[generate_enroll_token()] | lang=en
- "routers_probe_enrollment_rationale_68": "A token can auto-approve only while live, unrevoked, and under max_uses." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[enroll_token_is_usable()] | lang=en
- "routers_probe_enrollment_rationale_69": "A token can auto-approve only while live, unrevoked, and under max_uses." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L69 | neighbors=[enroll_token_is_usable()] | lang=en
- "routers_probe_enrollment_revoke_enroll_token": "revoke_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L758 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_sitepolicyinput_require_site_reference": ".require_site_reference()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L168 | neighbors=[SitePolicyInput] | lang=en
- "routers_probe_enrollment_sitepolicyinput_validate_networks": ".validate_networks()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L164 | neighbors=[SitePolicyInput] | lang=en
- "routers_validation_rationale_1": "Approval-gated safe active-validation API (P3).  POST /engagements/{id}/findings" | kind=entity | source=manager/backend/app/routers/validation.py:L1 | neighbors=[validation.py] | lang=en
- "routers_validation_rationale_82": "RoE gate: active validation is allowed unless the engagement's RoE     explicitl" | kind=entity | source=manager/backend/app/routers/validation.py:L82 | neighbors=[_roe_allows_active_validation()] | lang=en
- "routers_validation_rationale_89": "Pick a safe check for the finding. TLS findings → tls_handshake, else a     bann" | kind=entity | source=manager/backend/app/routers/validation.py:L89 | neighbors=[_default_check_kind()] | lang=en
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L215 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L66 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L119 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L165 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L194 | neighbors=[vuln_scans.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-153.json

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
