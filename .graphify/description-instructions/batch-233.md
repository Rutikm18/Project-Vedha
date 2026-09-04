# Node Description Batch 234 of 332

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

- "routers_agents_rationale_1003": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1003 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_1012": "The tenant-wide job feed powering the Fleet page: every probe's jobs, newest" | kind=entity | source=manager/backend/app/routers/agents.py:L1012 | neighbors=[list_all_jobs()] | lang=en
- "routers_agents_rationale_1035": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1035 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_105": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L105 | neighbors=[_scope_is_reachable()] | lang=pt
- "routers_agents_rationale_1050": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1050 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_107": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L107 | neighbors=[_scope_is_reachable()] | lang=pt
- "routers_agents_rationale_1072": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1072 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_1120": "How many jobs are queued (not yet claimed) for this engagement." | kind=entity | source=manager/backend/app/routers/agents.py:L1120 | neighbors=[_pending_job_count()] | lang=en
- "routers_agents_rationale_1140": "Operator-initiated stop for a queued or running scan job.      Two cases, one en" | kind=entity | source=manager/backend/app/routers/agents.py:L1140 | neighbors=[cancel_agent_job()] | lang=en
- "routers_agents_rationale_1230": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1230 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_141": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L141 | neighbors=[_job_reachability_scope()] | lang=en
- "routers_agents_rationale_143": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L143 | neighbors=[_job_reachability_scope()] | lang=en
- "routers_agents_rationale_166": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L166 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_167": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L167 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_215": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L215 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_275": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L275 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_276": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L276 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_277": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L277 | neighbors=[_normalize_intensity_name()] | lang=pt
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
- "routers_agents_rationale_537": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L537 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_550": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L550 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_559": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L559 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_560": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L560 | neighbors=[list_intensities()] | lang=en
- "routers_agents_rationale_564": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L564 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_571": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L571 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_574": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L574 | neighbors=[_agent_ownership_check()] | lang=en

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
