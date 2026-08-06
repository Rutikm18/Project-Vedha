# Node Description Batch 133 of 134

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

- "workflow_cache_rationale_1": "cache.py — (host, port, scanner) -> CacheEntry, so deterministic facts are colle" | kind=entity | source=probe/workflow/cache.py:L1 | neighbors=[cache.py] | lang=en
- "workflow_cache_rationale_122": "True if there's no cached entry, OR the entry is uncertain         (always worth" | kind=entity | source=probe/workflow/cache.py:L122 | neighbors=[.should_recheck()] | lang=en
- "workflow_cache_rationale_79": "In-memory (host, port, scanner) -> CacheEntry, optionally JSONL-backed     for c" | kind=entity | source=probe/workflow/cache.py:L79 | neighbors=[WorkflowCache] | lang=en
- "workflow_cache_workflowcache_all_entries_for_host": ".all_entries_for_host()" | kind=code-symbol | source=probe/workflow/cache.py:L139 | neighbors=[WorkflowCache] | lang=en
- "workflow_cli_rationale_1": "cli.py — entrypoint for the conditional workflow engine. Flag conventions follow" | kind=entity | source=probe/workflow/cli.py:L1 | neighbors=[cli.py] | lang=en
- "workflow_cli_rationale_29": "7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar" | kind=entity | source=probe/workflow/cli.py:L29 | neighbors=[_parse_duration()] | lang=en
- "workflow_cli_rationale_30": "7d' / '12h' / '30m' -> timedelta. Simple single-unit parser —     engagements ar" | kind=entity | source=probe/workflow/cli.py:L30 | neighbors=[_parse_duration()] | lang=en
- "workflow_execution_executiontrace_degraded": ".degraded()" | kind=code-symbol | source=probe/workflow/execution.py:L346 | neighbors=[ExecutionTrace] | lang=en
- "workflow_execution_executiontrace_issues": ".issues()" | kind=code-symbol | source=probe/workflow/execution.py:L338 | neighbors=[ExecutionTrace] | lang=en
- "workflow_execution_rationale_1": "Execution telemetry and failure normalization for the probe workflow." | kind=entity | source=probe/workflow/execution.py:L1 | neighbors=[execution.py] | lang=en
- "workflow_execution_rationale_105": "Resolve the exact collector plan for one workflow invocation." | kind=entity | source=probe/workflow/execution.py:L105 | neighbors=[planned_components()] | lang=en
- "workflow_execution_rationale_154": "Map low-level failures into stable, operator-actionable categories." | kind=entity | source=probe/workflow/execution.py:L154 | neighbors=[classify_scanner_error()] | lang=en
- "workflow_execution_rationale_210": "Represent an unexpected component exception without aborting other hosts." | kind=entity | source=probe/workflow/execution.py:L210 | neighbors=[scanner_failure_result()] | lang=en
- "workflow_execution_rationale_232": "Mutable per-run component accounting, serialized only after completion." | kind=entity | source=probe/workflow/execution.py:L232 | neighbors=[ExecutionTrace] | lang=en
- "workflow_execution_rationale_351": "True when execution produced errors and no usable or cached facts." | kind=entity | source=probe/workflow/execution.py:L351 | neighbors=[.failed()] | lang=en
- "workflow_execution_rationale_59": "Return the runtime engine inventory without claiming optional tools ran." | kind=entity | source=probe/workflow/execution.py:L59 | neighbors=[engine_manifest()] | lang=en
- "workflow_gates_gate_4_service_banner": "gate_4_service_banner()" | kind=code-symbol | source=probe/workflow/gates.py:L67 | neighbors=[gates.py] | lang=en
- "workflow_gates_gate_6_credentialed_collection": "gate_6_credentialed_collection()" | kind=code-symbol | source=probe/workflow/gates.py:L101 | neighbors=[gates.py] | lang=en
- "workflow_gates_rationale_1": "gates.py — precondition functions deciding whether each stage of the workflow ru" | kind=entity | source=probe/workflow/gates.py:L1 | neighbors=[gates.py] | lang=en
- "workflow_gates_rationale_46": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L46 | neighbors=[gate_0_is_passive_profile()] | lang=en
- "workflow_gates_rationale_48": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L48 | neighbors=[gate_0_is_passive_profile()] | lang=en
- "workflow_gates_rationale_72": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L72 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_74": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L74 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_init_rationale_1": "workflow — conditional, caching, dependency-aware orchestrator that replaces pip" | kind=entity | source=probe/workflow/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "workflow_modes_rationale_1": "modes.py — engagement mode configurations. Each mode is a thin config that tunes" | kind=entity | source=probe/workflow/modes.py:L1 | neighbors=[modes.py] | lang=en
- "workflow_modes_rationale_105": "Discovery + ports + banner only — no deep dives, no credentials." | kind=entity | source=probe/workflow/modes.py:L105 | neighbors=[triage()] | lang=en
- "workflow_modes_rationale_112": "Full funnel, every branch the profile allows." | kind=entity | source=probe/workflow/modes.py:L112 | neighbors=[assessment()] | lang=en
- "workflow_modes_rationale_127": "Loads a prior engagement's cache; only facts older than     recheck_older_than g" | kind=entity | source=probe/workflow/modes.py:L127 | neighbors=[re_scan()] | lang=pt
- "workflow_modes_rationale_25": "Discovery + ports + banner only — no deep dives, no credentials." | kind=entity | source=probe/workflow/modes.py:L25 | neighbors=[triage()] | lang=en
- "workflow_modes_rationale_30": "Resolve the explicit ceiling while preserving the legacy triage knob." | kind=entity | source=probe/workflow/modes.py:L30 | neighbors=[resolve_stage_ceiling()] | lang=en
- "workflow_modes_rationale_31": "Full funnel, every branch the profile allows." | kind=entity | source=probe/workflow/modes.py:L31 | neighbors=[assessment()] | lang=en
- "workflow_modes_rationale_44": "Loads a prior engagement's cache; only facts older than     recheck_older_than g" | kind=entity | source=probe/workflow/modes.py:L44 | neighbors=[re_scan()] | lang=pt
- "workflow_modes_rationale_46": "Return whether a bounded plan includes `stage`." | kind=entity | source=probe/workflow/modes.py:L46 | neighbors=[includes_stage()] | lang=pt
- "workflow_modes_rationale_61": "Host discovery plus the profile's TCP port catalog." | kind=entity | source=probe/workflow/modes.py:L61 | neighbors=[discovery()] | lang=en
- "workflow_modes_rationale_72": "Liveness checks only." | kind=entity | source=probe/workflow/modes.py:L72 | neighbors=[host_discovery()] | lang=en
- "workflow_modes_rationale_83": "Liveness checks plus the profile's TCP port catalog." | kind=entity | source=probe/workflow/modes.py:L83 | neighbors=[port_scan()] | lang=en
- "workflow_modes_rationale_94": "Liveness, TCP ports, and service banners without deep branches." | kind=entity | source=probe/workflow/modes.py:L94 | neighbors=[service_fingerprint()] | lang=en
- "workflow_report_asset_to_dict": "asset_to_dict()" | kind=code-symbol | source=probe/workflow/report.py:L11 | neighbors=[report.py] | lang=en
- "workflow_report_engagement_summary": "engagement_summary()" | kind=code-symbol | source=probe/workflow/report.py:L30 | neighbors=[report.py] | lang=en
- "workflow_report_rationale_1": "report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d" | kind=entity | source=probe/workflow/report.py:L1 | neighbors=[report.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-132.json

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
