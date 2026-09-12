# Node Description Batch 205 of 380

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

- "agent_scope_validator_rationale_121": "Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl" | kind=entity | source=probe/agent/scope_validator.py:L121 | neighbors=[merge_exclusions()] | lang=en
- "agent_scope_validator_rationale_124": "Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)." | kind=entity | source=probe/agent/scope_validator.py:L124 | neighbors=[targets_in_excludes()] | lang=en
- "agent_scope_validator_rationale_158": "Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl" | kind=entity | source=probe/agent/scope_validator.py:L158 | neighbors=[merge_exclusions()] | lang=en
- "agent_scope_validator_rationale_28": "Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None``" | kind=entity | source=probe/agent/scope_validator.py:L28 | neighbors=[_networks_for_target()] | lang=en
- "agent_scope_validator_rationale_31": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L31 | neighbors=[fetch_engagement_scope()] | lang=en
- "agent_scope_validator_rationale_85": "Check targets against the authoritative scope CIDRs.      Returns (allowed, reje" | kind=entity | source=probe/agent/scope_validator.py:L85 | neighbors=[validate_targets_in_scope()] | lang=en
- "agent_scope_validator_rationale_88": "Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)." | kind=entity | source=probe/agent/scope_validator.py:L88 | neighbors=[targets_in_excludes()] | lang=en
- "agent_self_scan_rationale_1": "self_scan.py — scan THIS host's own IP, no Manager (Phase 5).  Assembles the sco" | kind=entity | source=probe/agent/self_scan.py:L1 | neighbors=[self_scan.py] | lang=en
- "agent_self_scan_rationale_112": "Runnable entry: `python -m agent.self_scan [--profile it|iot] [--stage …]`." | kind=entity | source=probe/agent/self_scan.py:L112 | neighbors=[main()] | lang=en
- "agent_self_scan_rationale_32": "Pure decision. Returns (plan, reason); reason is non-empty on refusal." | kind=entity | source=probe/agent/self_scan.py:L32 | neighbors=[plan_self_scan()] | lang=en
- "agent_self_scan_rationale_47": "Write the own-IP scope file, run the engine, archive the summary." | kind=entity | source=probe/agent/self_scan.py:L47 | neighbors=[execute()] | lang=en
- "agent_service_default_runner": "_default_runner()" | kind=code-symbol | source=probe/agent/service.py:L106 | neighbors=[service.py] | lang=en
- "agent_service_rationale_1": "service.py — per-OS service install with restart limits (Phase 9).  The unit is" | kind=entity | source=probe/agent/service.py:L1 | neighbors=[service.py] | lang=en
- "agent_service_rationale_63": "Return (target_path, body). Windows returns ('SCHTASKS', command_string)." | kind=entity | source=probe/agent/service.py:L63 | neighbors=[render_unit()] | lang=en
- "agent_setup_rationale_1": "setup.py — the brain CLI that ties the hardened components together.  Subcommand" | kind=entity | source=probe/agent/setup.py:L1 | neighbors=[setup.py] | lang=en
- "agent_supervisor_rationale_1": "supervisor.py — restart supervisor with a per-class policy (0b contract).  - suc" | kind=entity | source=probe/agent/supervisor.py:L1 | neighbors=[supervisor.py] | lang=en
- "agent_supervisor_supervise": "supervise()" | kind=code-symbol | source=probe/agent/supervisor.py:L24 | neighbors=[supervisor.py] | lang=en
- "agent_task_runner_rationale_1": "task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a" | kind=entity | source=probe/agent/task_runner.py:L1 | neighbors=[task_runner.py] | lang=en
- "agent_task_runner_rationale_105": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L105 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_107": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L107 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_122": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L122 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_126": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L126 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_159": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L159 | neighbors=[.run_job()] | lang=pt
- "agent_task_runner_rationale_162": "A callback the scan engine invokes when ONE host is finished.          Commits t" | kind=entity | source=probe/agent/task_runner.py:L162 | neighbors=[._chunk_sink()] | lang=en
- "agent_task_runner_rationale_183": "Hosts the manager already holds for this job — a retry skips them.          Fail" | kind=entity | source=probe/agent/task_runner.py:L183 | neighbors=[._already_committed()] | lang=en
- "agent_task_runner_rationale_204": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L204 | neighbors=[.run_job()] | lang=pt
- "agent_task_runner_rationale_28": "Structured result from running one scan job." | kind=entity | source=probe/agent/task_runner.py:L28 | neighbors=[JobResult] | lang=en
- "agent_task_runner_rationale_283": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L283 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_30": "Structured result from running one scan job." | kind=entity | source=probe/agent/task_runner.py:L30 | neighbors=[JobResult] | lang=en
- "agent_task_runner_rationale_397": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L397 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_399": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L399 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_40": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L40 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_42": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L42 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_436": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L436 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_443": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L443 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_508": "Write the outbound payload to the local result archive.          Called on the s" | kind=entity | source=probe/agent/task_runner.py:L508 | neighbors=[._archive_result()] | lang=en
- "agent_task_runner_rationale_546": "Write the outbound payload to the local result archive.          Called on the s" | kind=entity | source=probe/agent/task_runner.py:L546 | neighbors=[._archive_result()] | lang=en
- "agent_task_runner_rationale_548": "Submit the result, with spool-and-retry if available.          Every outbound pa" | kind=entity | source=probe/agent/task_runner.py:L548 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_57": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L57 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_586": "Submit the result, with spool-and-retry if available.          Every outbound pa" | kind=entity | source=probe/agent/task_runner.py:L586 | neighbors=[._submit_or_spool()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-204.json

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
