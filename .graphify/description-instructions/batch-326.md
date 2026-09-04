# Node Description Batch 327 of 330

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
- "workflow_execution_rationale_67": "Return the runtime engine inventory without claiming optional tools ran." | kind=entity | source=probe/workflow/execution.py:L67 | neighbors=[engine_manifest()]
- "workflow_gates_gate_4_service_banner": "gate_4_service_banner()" | kind=code-symbol | source=probe/workflow/gates.py:L118 | neighbors=[gates.py]
- "workflow_gates_gate_6_credentialed_collection": "gate_6_credentialed_collection()" | kind=code-symbol | source=probe/workflow/gates.py:L163 | neighbors=[gates.py]
- "workflow_gates_rationale_1": "gates.py — precondition functions deciding whether each stage of the workflow ru" | kind=entity | source=probe/workflow/gates.py:L1 | neighbors=[gates.py]
- "workflow_gates_rationale_123": "OS identity for a host already proven alive. Runs on the SAME evidence the     p" | kind=entity | source=probe/workflow/gates.py:L123 | neighbors=[gate_4b_os_fingerprint()]
- "workflow_gates_rationale_136": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L136 | neighbors=[gate_5_branch_eligible()]
- "workflow_gates_rationale_46": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L46 | neighbors=[gate_0_is_passive_profile()]
- "workflow_gates_rationale_48": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L48 | neighbors=[gate_0_is_passive_profile()]
- "workflow_gates_rationale_64": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L64 | neighbors=[gate_0_is_passive_profile()]
- "workflow_gates_rationale_72": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L72 | neighbors=[gate_5_branch_eligible()]
- "workflow_gates_rationale_74": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L74 | neighbors=[gate_5_branch_eligible()]
- "workflow_gates_rationale_90": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L90 | neighbors=[gate_5_branch_eligible()]
- "workflow_gates_rationale_99": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L99 | neighbors=[gate_0_is_passive_profile()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-326.json

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
