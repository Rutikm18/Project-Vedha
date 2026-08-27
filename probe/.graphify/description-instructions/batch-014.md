# Node Description Batch 15 of 92

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

- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=agent/cli.py:L153 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()] | lang=en
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=agent/engine.py:L351 | neighbors=[engine.py, _scan_method_for(), _build_run_stats(), Serialize effective limits without ever…, Serialize effective limits without ever…] | lang=en
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=agent/engine.py:L196 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…] | lang=en
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=agent/engine.py:L206 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan(), Return the effective whole-job deadline…] | lang=en
- "agent_engine_rationale_1": "engine.py — adapt a manager scan job to scanner_module's workflow engine and ret" | kind=entity | source=agent/engine.py:L1 | neighbors=[engine.py, ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_148": "syn' for wide sweeps (deep intensity / full-port audit), else 'connect'." | kind=entity | source=agent/engine.py:L148 | neighbors=[_scan_method_for(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_154": "syn' for wide sweeps (deep intensity / full-port audit), else 'connect'." | kind=entity | source=agent/engine.py:L154 | neighbors=[_scan_method_for(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_191": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=agent/engine.py:L191 | neighbors=[_clamp(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_197": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=agent/engine.py:L197 | neighbors=[_clamp(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_201": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=agent/engine.py:L201 | neighbors=[_job_runtime_seconds(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_207": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=agent/engine.py:L207 | neighbors=[_job_runtime_seconds(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_211": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=agent/engine.py:L211 | neighbors=[_tuning_from_params(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_217": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=agent/engine.py:L217 | neighbors=[_tuning_from_params(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_277": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=agent/engine.py:L277 | neighbors=[_count_open_port_facts(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_283": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=agent/engine.py:L283 | neighbors=[_count_open_port_facts(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_298": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=agent/engine.py:L298 | neighbors=[_hosts_from_facts(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=it
- "agent_engine_rationale_304": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=agent/engine.py:L304 | neighbors=[_hosts_from_facts(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=it
- "agent_engine_rationale_348": "Serialize effective limits without ever echoing credential values." | kind=entity | source=agent/engine.py:L348 | neighbors=[_applied_tuning(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_354": "Serialize effective limits without ever echoing credential values." | kind=entity | source=agent/engine.py:L354 | neighbors=[_applied_tuning(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_385": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=agent/engine.py:L385 | neighbors=[_build_run_stats(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_391": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=agent/engine.py:L391 | neighbors=[_build_run_stats(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_437": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=agent/engine.py:L437 | neighbors=[_derive_post_stage(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_443": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=agent/engine.py:L443 | neighbors=[_derive_post_stage(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_470": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=agent/engine.py:L470 | neighbors=[_derive_devices(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_486": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=agent/engine.py:L486 | neighbors=[LeaseLostError, ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_490": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=agent/engine.py:L490 | neighbors=[_derive_exposure(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_51": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=agent/engine.py:L51 | neighbors=[_env_number(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_512": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=agent/engine.py:L512 | neighbors=[run_scan(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_515": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=agent/engine.py:L515 | neighbors=[LeaseLostError, ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_541": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=agent/engine.py:L541 | neighbors=[run_scan(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_rationale_80": "Single factory for error result dicts — no copy-paste." | kind=entity | source=agent/engine.py:L80 | neighbors=[_error_result(), ScanResult, ScopeGuard, WorkflowCache, ExecutionTrace] | lang=en
- "agent_engine_scan_method_for": "_scan_method_for()" | kind=code-symbol | source=agent/engine.py:L153 | neighbors=[engine.py, _applied_tuning(), syn' for wide sweeps (deep intensity / …, run_scan(), syn' for wide sweeps (deep intensity / …] | lang=en
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=agent/engine.py:L216 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …] | lang=en
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry()] | lang=en
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save()] | lang=en
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=agent/result_spool.py:L59 | neighbors=[ResultSpool, .quarantine(), .remove(), .save(), .exists()] | lang=en
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=agent/transport.py:L456 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError] | lang=en
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=agent/use_cases.py:L254 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code(), Coerce an int-or-numeric-string to int,…] | lang=en
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=agent/use_cases.py:L276 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve(), Accept an intensity as a number (1/2/3)…] | lang=en
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=agent/use_cases.py:L293 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-014.json

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
