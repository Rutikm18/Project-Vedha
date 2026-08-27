# Node Description Batch 127 of 236

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

- "agent_engine_rationale_158": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L158 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_168": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L168 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_178": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L178 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_181": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L181 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_197": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L197 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_207": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L207 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_211": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L211 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_217": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L217 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_236": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L236 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_257": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L257 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_267": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L267 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_277": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L277 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_283": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L283 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_288": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L288 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_29": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L29 | neighbors=[_error_result()] | lang=en
- "agent_engine_rationale_298": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L298 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_304": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L304 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_305": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L305 | neighbors=[_applied_tuning()] | lang=en
- "agent_engine_rationale_336": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L336 | neighbors=[_build_run_stats()] | lang=en
- "agent_engine_rationale_338": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L338 | neighbors=[_applied_tuning()] | lang=en
- "agent_engine_rationale_348": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L348 | neighbors=[_applied_tuning()] | lang=en
- "agent_engine_rationale_354": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L354 | neighbors=[_applied_tuning()] | lang=en
- "agent_engine_rationale_367": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L367 | neighbors=[LeaseLostError] | lang=en
- "agent_engine_rationale_372": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L372 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_374": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L374 | neighbors=[_build_run_stats()] | lang=en
- "agent_engine_rationale_385": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L385 | neighbors=[_build_run_stats()] | lang=en
- "agent_engine_rationale_391": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L391 | neighbors=[_build_run_stats()] | lang=en
- "agent_engine_rationale_393": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L393 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_426": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L426 | neighbors=[_derive_post_stage()] | lang=en
- "agent_engine_rationale_437": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L437 | neighbors=[_derive_post_stage()] | lang=en
- "agent_engine_rationale_443": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L443 | neighbors=[_derive_post_stage()] | lang=en
- "agent_engine_rationale_46": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L46 | neighbors=[_env_number()] | lang=en
- "agent_engine_rationale_470": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=probe/agent/engine.py:L470 | neighbors=[_derive_devices()] | lang=en
- "agent_engine_rationale_475": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L475 | neighbors=[LeaseLostError] | lang=en
- "agent_engine_rationale_486": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L486 | neighbors=[LeaseLostError] | lang=en
- "agent_engine_rationale_490": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L490 | neighbors=[_derive_exposure()] | lang=en
- "agent_engine_rationale_501": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L501 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_51": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L51 | neighbors=[_env_number()] | lang=en
- "agent_engine_rationale_512": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L512 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_515": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L515 | neighbors=[LeaseLostError] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-126.json

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
