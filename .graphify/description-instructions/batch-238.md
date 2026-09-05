# Node Description Batch 239 of 336

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

- "routers_agents_rationale_592": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L592 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_595": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L595 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_597": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L597 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_604": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L604 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_606": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L606 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_607": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L607 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_608": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L608 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_615": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L615 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_619": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L619 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_630": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L630 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_631": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L631 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_642": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L642 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_654": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L654 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_665": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L665 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_858": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L858 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_864": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L864 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_92": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L92 | neighbors=[_required_scan_type()] | lang=en
- "routers_agents_rationale_921": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L921 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_94": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L94 | neighbors=[_required_scan_type()] | lang=en
- "routers_agents_rationale_944": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L944 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_979": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L979 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_988": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L988 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_993": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L993 | neighbors=[get_job_status()] | lang=en
- "routers_ai_ai_generate": "ai_generate()" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L19 | neighbors=[ai.py] | lang=en
- "routers_ai_ai_status": "ai_status()" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L13 | neighbors=[ai.py] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-238.json

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
