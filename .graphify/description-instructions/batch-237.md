# Node Description Batch 238 of 332

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

- "routers_portal_rationale_550": "The customer's own probe fleet — normally one. Deliberately a NARROW     project" | kind=entity | source=manager/backend/app/routers/portal.py:L550 | neighbors=[portal_agents()] | lang=en
- "routers_portal_rationale_71": "The operator use-case catalog (single source of truth), curated to what a     cu" | kind=entity | source=manager/backend/app/routers/portal.py:L71 | neighbors=[_portal_use_cases()] | lang=en
- "routers_portal_rationale_76": "The operator use-case catalog (single source of truth), curated to what a     cu" | kind=entity | source=manager/backend/app/routers/portal.py:L76 | neighbors=[_portal_use_cases()] | lang=en
- "routers_probe_enrollment_list_enrollment_requests": "list_enrollment_requests()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L504 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_1": "Device-code enrollment for probes; no human credential is installed on a probe." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L1 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_rationale_246": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L246 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_247": "Bind a request to a Site policy and create the provisioning Agent.      Shared b" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L247 | neighbors=[_provision_agent_for_site()] | lang=en
- "routers_probe_enrollment_rationale_314": "Parse settings.probe_auto_enroll_cidrs → a non-empty CIDR list (RFC1918     defa" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L314 | neighbors=[auto_enroll_cidrs()] | lang=pt
- "routers_probe_enrollment_rationale_322": "The singleton per-tenant Site that trust-on-first-use enrollment binds to." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L322 | neighbors=[_get_or_create_auto_enroll_site()] | lang=en
- "routers_probe_enrollment_rationale_531": "One-click \"Approve Site\": every field is an OPTIONAL override — left blank," | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L531 | neighbors=[SimpleApproveInput] | lang=en
- "routers_probe_enrollment_rationale_547": "Auto-assign the next sequential vedha-agent name (vedha_agent_01, _02, …) so" | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L547 | neighbors=[_next_probe_name()] | lang=en
- "routers_probe_enrollment_rationale_62": "Return (raw_token, token_hash, token_prefix). Raw is shown once." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[generate_enroll_token()] | lang=en
- "routers_probe_enrollment_rationale_63": "Return (raw_token, token_hash, token_prefix). Raw is shown once." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L63 | neighbors=[generate_enroll_token()] | lang=en
- "routers_probe_enrollment_rationale_68": "A token can auto-approve only while live, unrevoked, and under max_uses." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[enroll_token_is_usable()] | lang=en
- "routers_probe_enrollment_rationale_69": "A token can auto-approve only while live, unrevoked, and under max_uses." | kind=entity | source=manager/backend/app/routers/probe_enrollment.py:L69 | neighbors=[enroll_token_is_usable()] | lang=en
- "routers_probe_enrollment_revoke_enroll_token": "revoke_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L842 | neighbors=[probe_enrollment.py] | lang=en
- "routers_probe_enrollment_simpleapproveinput_validate_networks": "._validate_networks()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L542 | neighbors=[SimpleApproveInput] | lang=en
- "routers_probe_enrollment_sitepolicyinput_require_site_reference": ".require_site_reference()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L168 | neighbors=[SitePolicyInput] | lang=en
- "routers_probe_enrollment_sitepolicyinput_validate_networks": ".validate_networks()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L164 | neighbors=[SitePolicyInput] | lang=en
- "routers_remediation_rationale_1": "remediation.py — per-finding remediation plans (operator-facing).  Two routes on" | kind=entity | source=manager/backend/app/routers/remediation.py:L1 | neighbors=[remediation.py] | lang=en
- "routers_remediation_rationale_41": "Fetch a finding scoped to the caller's tenant via its engagement." | kind=entity | source=manager/backend/app/routers/remediation.py:L41 | neighbors=[_tenant_finding()] | lang=en
- "routers_remediation_rationale_43": "Fetch a finding scoped to the caller's tenant via its engagement." | kind=entity | source=manager/backend/app/routers/remediation.py:L43 | neighbors=[_tenant_finding()] | lang=en
- "routers_remediation_rationale_64": "Build the atomic INSERT … ON CONFLICT DO UPDATE for a cached plan.      Pure (no" | kind=entity | source=manager/backend/app/routers/remediation.py:L64 | neighbors=[_build_upsert_stmt()] | lang=en
- "routers_remediation_rationale_66": "Build the atomic INSERT … ON CONFLICT DO UPDATE for a cached plan.      Pure (no" | kind=entity | source=manager/backend/app/routers/remediation.py:L66 | neighbors=[_build_upsert_stmt()] | lang=en
- "routers_remediation_rationale_95": "Execute the atomic upsert and return the RETURNING row for serialization." | kind=entity | source=manager/backend/app/routers/remediation.py:L95 | neighbors=[_upsert_plan()] | lang=en
- "routers_remediation_rationale_97": "Execute the atomic upsert and return the RETURNING row for serialization." | kind=entity | source=manager/backend/app/routers/remediation.py:L97 | neighbors=[_upsert_plan()] | lang=en
- "routers_sla_policy_rationale_1": "sla_policy.py — operator management of the tenant's custom SLA remediation windo" | kind=entity | source=manager/backend/app/routers/sla_policy.py:L1 | neighbors=[sla_policy.py] | lang=en
- "routers_sla_policy_rationale_59": "The tenant's custom SLA windows if set, else the env defaults. Shared by any" | kind=entity | source=manager/backend/app/routers/sla_policy.py:L59 | neighbors=[resolve_windows()] | lang=en
- "routers_users_activate_user": "activate_user()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L118 | neighbors=[users.py] | lang=en
- "routers_users_deactivate_user": "deactivate_user()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L92 | neighbors=[users.py] | lang=en
- "routers_users_rationale_1": "Tenant user management — list and deactivate operator accounts.  Exposed endpoin" | kind=entity | source=manager/backend/app/routers/users.py:L1 | neighbors=[users.py] | lang=en
- "routers_validation_rationale_1": "Approval-gated safe active-validation API (P3).  POST /engagements/{id}/findings" | kind=entity | source=manager/backend/app/routers/validation.py:L1 | neighbors=[validation.py] | lang=en
- "routers_validation_rationale_82": "RoE gate: active validation is allowed unless the engagement's RoE     explicitl" | kind=entity | source=manager/backend/app/routers/validation.py:L82 | neighbors=[_roe_allows_active_validation()] | lang=en
- "routers_validation_rationale_89": "Pick a safe check for the finding. TLS findings → tls_handshake, else a     bann" | kind=entity | source=manager/backend/app/routers/validation.py:L89 | neighbors=[_default_check_kind()] | lang=en
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L215 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L66 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L119 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L165 | neighbors=[vuln_scans.py] | lang=en
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L194 | neighbors=[vuln_scans.py] | lang=en
- "run_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L5 | neighbors=[route.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-237.json

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
