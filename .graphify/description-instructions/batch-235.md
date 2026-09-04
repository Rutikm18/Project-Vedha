# Node Description Batch 236 of 330

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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-235.json

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
