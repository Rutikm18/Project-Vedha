# Node Description Batch 170 of 236

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "routers_agents_rationale_319": "Accept an intensity as a number (1/2/3) or a name; return the name (or     None)" | kind=entity | source=manager/backend/app/routers/agents.py:L319 | neighbors=[_normalize_intensity_name()] | lang=en
- "routers_agents_rationale_324": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L324 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_407": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L407 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_445": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L445 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_464": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L464 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_477": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L477 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_478": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L478 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_491": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L491 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_502": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L502 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_512": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L512 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_515": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L515 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_521": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L521 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_526": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L526 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_535": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L535 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_536": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L536 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_550": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L550 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_559": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L559 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_560": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L560 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_564": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L564 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_571": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L571 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_574": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L574 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_583": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L583 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_592": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L592 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_595": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L595 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_597": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L597 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_604": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L604 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_606": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L606 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_607": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L607 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_609": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L609 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_615": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L615 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_619": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L619 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_620": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L620 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_630": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L630 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_858": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L858 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_864": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L864 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_92": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L92 | neighbors=[_required_scan_type()] | lang=en
- "routers_agents_rationale_921": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L921 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_944": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L944 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_979": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L979 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_988": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L988 | neighbors=[get_job_status()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-169.json

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
