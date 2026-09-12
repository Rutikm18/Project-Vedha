# Node Description Batch 268 of 380

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

- "routers_agents_rationale_1012": "The tenant-wide job feed powering the Fleet page: every probe's jobs, newest" | kind=entity | source=manager/backend/app/routers/agents.py:L1012 | neighbors=[list_all_jobs()] | lang=en
- "routers_agents_rationale_1035": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1035 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_1046": "The tenant-wide job feed powering the Fleet page: every probe's jobs, newest" | kind=entity | source=manager/backend/app/routers/agents.py:L1046 | neighbors=[list_all_jobs()] | lang=en
- "routers_agents_rationale_105": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L105 | neighbors=[_scope_is_reachable()] | lang=pt
- "routers_agents_rationale_1050": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1050 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_1065": "The tenant-wide job feed powering the Fleet page: every probe's jobs, newest" | kind=entity | source=manager/backend/app/routers/agents.py:L1065 | neighbors=[list_all_jobs()] | lang=en
- "routers_agents_rationale_107": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L107 | neighbors=[_scope_is_reachable()] | lang=pt
- "routers_agents_rationale_1072": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1072 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_1078": "The tenant-wide job feed powering the Fleet page: every probe's jobs, newest" | kind=entity | source=manager/backend/app/routers/agents.py:L1078 | neighbors=[list_all_jobs()] | lang=en
- "routers_agents_rationale_1106": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1106 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_1120": "How many jobs are queued (not yet claimed) for this engagement." | kind=entity | source=manager/backend/app/routers/agents.py:L1120 | neighbors=[_pending_job_count()] | lang=en
- "routers_agents_rationale_1125": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1125 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_1138": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1138 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_1140": "Operator-initiated stop for a queued or running scan job.      Two cases, one en" | kind=entity | source=manager/backend/app/routers/agents.py:L1140 | neighbors=[cancel_agent_job()] | lang=en
- "routers_agents_rationale_1154": "How many jobs are queued (not yet claimed) for this engagement." | kind=entity | source=manager/backend/app/routers/agents.py:L1154 | neighbors=[_pending_job_count()] | lang=en
- "routers_agents_rationale_1174": "Operator-initiated stop for a queued or running scan job.      Two cases, one en" | kind=entity | source=manager/backend/app/routers/agents.py:L1174 | neighbors=[cancel_agent_job()] | lang=en
- "routers_agents_rationale_1181": "Can the probe a job is pinned to still plausibly run it?      Row existence is N" | kind=entity | source=manager/backend/app/routers/agents.py:L1181 | neighbors=[_pinned_agent_is_live()] | lang=en
- "routers_agents_rationale_1194": "Can the probe a job is pinned to still plausibly run it?      Row existence is N" | kind=entity | source=manager/backend/app/routers/agents.py:L1194 | neighbors=[_pinned_agent_is_live()] | lang=en
- "routers_agents_rationale_1206": "How many jobs are queued (not yet claimed) for this engagement." | kind=entity | source=manager/backend/app/routers/agents.py:L1206 | neighbors=[_pending_job_count()] | lang=en
- "routers_agents_rationale_1219": "How many jobs are queued (not yet claimed) for this engagement." | kind=entity | source=manager/backend/app/routers/agents.py:L1219 | neighbors=[_pending_job_count()] | lang=en
- "routers_agents_rationale_1226": "Operator-initiated stop for a queued or running scan job.      Two cases, one en" | kind=entity | source=manager/backend/app/routers/agents.py:L1226 | neighbors=[cancel_agent_job()] | lang=en
- "routers_agents_rationale_1230": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1230 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_1239": "Operator-initiated stop for a queued or running scan job.      Two cases, one en" | kind=entity | source=manager/backend/app/routers/agents.py:L1239 | neighbors=[cancel_agent_job()] | lang=en
- "routers_agents_rationale_1264": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1264 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_1317": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1317 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_1330": "Read-only per-probe job list — the probe's running job (its serial queue head)" | kind=entity | source=manager/backend/app/routers/agents.py:L1330 | neighbors=[get_agent_job_history()] | lang=en
- "routers_agents_rationale_141": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L141 | neighbors=[_job_reachability_scope()] | lang=en
- "routers_agents_rationale_143": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L143 | neighbors=[_job_reachability_scope()] | lang=en
- "routers_agents_rationale_1605": "Buffer one host's evidence so a probe that dies mid-scan does not lose it." | kind=entity | source=manager/backend/app/routers/agents.py:L1605 | neighbors=[submit_result_chunk()] | lang=en
- "routers_agents_rationale_1636": "What a retrying probe reads so it does not rescan finished hosts." | kind=entity | source=manager/backend/app/routers/agents.py:L1636 | neighbors=[list_result_chunks()] | lang=en
- "routers_agents_rationale_166": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L166 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_167": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L167 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_184": "Explain, in one line, WHY a probe can't execute a job.      Mirrors :func:`_agen" | kind=entity | source=manager/backend/app/routers/agents.py:L184 | neighbors=[_ineligibility_reason()] | lang=pt
- "routers_agents_rationale_215": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L215 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_276": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L276 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_277": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L277 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_311": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L311 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_319": "Accept an intensity as a number (1/2/3) or a name; return the name (or     None)" | kind=entity | source=manager/backend/app/routers/agents.py:L319 | neighbors=[_normalize_intensity_name()] | lang=en
- "routers_agents_rationale_324": "Accept an intensity as a number (1/2/3), a name (light/standard/deep), or a" | kind=entity | source=manager/backend/app/routers/agents.py:L324 | neighbors=[_normalize_intensity_name()] | lang=pt
- "routers_agents_rationale_407": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L407 | neighbors=[_encrypt_scope_for_agent()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-267.json

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
