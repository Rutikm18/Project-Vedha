# Node Description Batch 333 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "workflow_asset_rationale_73": "Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep" | kind=entity | source=probe/workflow/asset.py:L73 | neighbors=[.needs_recheck_live()]
- "workflow_asset_rationale_83": "Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep" | kind=entity | source=probe/workflow/asset.py:L83 | neighbors=[.needs_recheck_live()]
- "workflow_asset_rationale_84": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L84 | neighbors=[.merge_result()]
- "workflow_asset_rationale_85": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L85 | neighbors=[.merge_result()]
- "workflow_asset_rationale_86": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L86 | neighbors=[.merge_result()]
- "workflow_asset_rationale_90": "Is liveness unknown, or stale past `threshold`? Threshold is         profile-dep" | kind=entity | source=probe/workflow/asset.py:L90 | neighbors=[.needs_recheck_live()]
- "workflow_asset_rationale_96": "Dispatch a real ScanResult into the right sub-structure, keyed         on result" | kind=entity | source=probe/workflow/asset.py:L96 | neighbors=[.merge_result()]
- "workflow_branches_rationale_1": "branches.py — the deep-scan branch registry: ONE declarative description of ever" | kind=entity | source=probe/workflow/branches.py:L1 | neighbors=[branches.py]
- "workflow_branches_rationale_102": "True when the fact describes the host rather than one port — it is         cache" | kind=entity | source=probe/workflow/branches.py:L102 | neighbors=[.host_level()]
- "workflow_branches_rationale_50": "The default: hand the scanner the ports that still need probing." | kind=entity | source=probe/workflow/branches.py:L50 | neighbors=[_ports_kwargs()]
- "workflow_branches_rationale_55": "For scanners that take no `ports` argument — a host-level branch, or a     datag" | kind=entity | source=probe/workflow/branches.py:L55 | neighbors=[_no_kwargs()]
- "workflow_branches_rationale_61": "Tell the web scanner which of these ports service_banner OBSERVED     speaking T" | kind=entity | source=probe/workflow/branches.py:L61 | neighbors=[_web_kwargs()]
- "workflow_branches_rationale_69": "Ports with a known database engine get that engine's probe; ports the     router" | kind=entity | source=probe/workflow/branches.py:L69 | neighbors=[_db_kwargs()]
- "workflow_branches_rationale_86": "One deep-scan branch. `branch` is the gate key (gates.PROFILE_DEEP_BRANCHES" | kind=entity | source=probe/workflow/branches.py:L86 | neighbors=[BranchSpec]
- "workflow_cache_rationale_1": "cache.py — (host, port, scanner) -> CacheEntry, so deterministic facts are colle" | kind=entity | source=probe/workflow/cache.py:L1 | neighbors=[cache.py]
- "workflow_cache_rationale_100": "In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c" | kind=entity | source=probe/workflow/cache.py:L100 | neighbors=[WorkflowCache]
- "workflow_cache_rationale_122": "True if there's no cached entry, OR the entry is uncertain         (always worth" | kind=entity | source=probe/workflow/cache.py:L122 | neighbors=[.should_recheck()]
- "workflow_cache_rationale_124": "True if there's no cached entry, OR the entry is uncertain         (always worth" | kind=entity | source=probe/workflow/cache.py:L124 | neighbors=[.should_recheck()]
- "workflow_cache_rationale_143": "True if there's no cached entry, OR the entry is uncertain         (always worth" | kind=entity | source=probe/workflow/cache.py:L143 | neighbors=[.should_recheck()]
- "workflow_cache_rationale_79": "In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c" | kind=entity | source=probe/workflow/cache.py:L79 | neighbors=[WorkflowCache]
- "workflow_cache_rationale_81": "In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c" | kind=entity | source=probe/workflow/cache.py:L81 | neighbors=[WorkflowCache]
- "workflow_cache_workflowcache_all_entries_for_host": ".all_entries_for_host()" | kind=code-symbol | source=probe/workflow/cache.py:L160 | neighbors=[WorkflowCache]
- "workflow_cli_rationale_1": "cli.py — entrypoint for the conditional workflow engine. Flag conventions follow" | kind=entity | source=probe/workflow/cli.py:L1 | neighbors=[cli.py]
- "workflow_cli_rationale_29": "7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar" | kind=entity | source=probe/workflow/cli.py:L29 | neighbors=[_parse_duration()]
- "workflow_cli_rationale_30": "7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar" | kind=entity | source=probe/workflow/cli.py:L30 | neighbors=[_parse_duration()]
- "workflow_execution_executiontrace_degraded": ".degraded()" | kind=code-symbol | source=probe/workflow/execution.py:L376 | neighbors=[ExecutionTrace]
- "workflow_execution_executiontrace_issues": ".issues()" | kind=code-symbol | source=probe/workflow/execution.py:L368 | neighbors=[ExecutionTrace]
- "workflow_execution_rationale_1": "Execution telemetry and failure normalization for the probe workflow." | kind=entity | source=probe/workflow/execution.py:L1 | neighbors=[execution.py]
- "workflow_execution_rationale_105": "Resolve the exact collector plan for one workflow invocation." | kind=entity | source=probe/workflow/execution.py:L105 | neighbors=[planned_components()]
- "workflow_execution_rationale_114": "Resolve the exact collector plan for one workflow invocation." | kind=entity | source=probe/workflow/execution.py:L114 | neighbors=[planned_components()]
- "workflow_execution_rationale_154": "Map low-level failures into stable, operator-actionable categories." | kind=entity | source=probe/workflow/execution.py:L154 | neighbors=[classify_scanner_error()]
- "workflow_execution_rationale_166": "Map low-level failures into stable, operator-actionable categories." | kind=entity | source=probe/workflow/execution.py:L166 | neighbors=[classify_scanner_error()]
- "workflow_execution_rationale_210": "Represent an unexpected component exception without aborting other hosts." | kind=entity | source=probe/workflow/execution.py:L210 | neighbors=[scanner_failure_result()]
- "workflow_execution_rationale_222": "Represent an unexpected component exception without aborting other hosts." | kind=entity | source=probe/workflow/execution.py:L222 | neighbors=[scanner_failure_result()]
- "workflow_execution_rationale_232": "Mutable per-run component accounting, serialized only after completion." | kind=entity | source=probe/workflow/execution.py:L232 | neighbors=[ExecutionTrace]
- "workflow_execution_rationale_244": "Mutable per-run component accounting, serialized only after completion." | kind=entity | source=probe/workflow/execution.py:L244 | neighbors=[ExecutionTrace]
- "workflow_execution_rationale_274": "Accumulate wall time for one component.          Without this, `scanner_runs` sa" | kind=entity | source=probe/workflow/execution.py:L274 | neighbors=[.timing()]
- "workflow_execution_rationale_351": "True when execution produced errors and no usable or cached facts." | kind=entity | source=probe/workflow/execution.py:L351 | neighbors=[.failed()]
- "workflow_execution_rationale_381": "True when execution produced errors and no usable or cached facts." | kind=entity | source=probe/workflow/execution.py:L381 | neighbors=[.failed()]
- "workflow_execution_rationale_59": "Return the runtime engine inventory without claiming optional tools ran." | kind=entity | source=probe/workflow/execution.py:L59 | neighbors=[engine_manifest()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-332.json

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
