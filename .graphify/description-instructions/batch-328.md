# Node Description Batch 329 of 332

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
- "workflow_host_health_hosthealthmonitor_offline_hosts": ".offline_hosts()" | kind=code-symbol | source=probe/workflow/host_health.py:L345 | neighbors=[HostHealthMonitor]
- "workflow_host_health_rationale_1": "host_health.py — detect a target that was proven alive and has since gone away," | kind=entity | source=probe/workflow/host_health.py:L1 | neighbors=[host_health.py]
- "workflow_host_health_rationale_114": "Tracks per-host reachability across the deep-scan stages.      `liveness_probe`" | kind=entity | source=probe/workflow/host_health.py:L114 | neighbors=[HostHealthMonitor]
- "workflow_host_health_rationale_134": "True when a component ran and got nothing back that proves life.          An emp" | kind=entity | source=probe/workflow/host_health.py:L134 | neighbors=[._is_silence()]
- "workflow_host_health_rationale_153": "Feed one component's results in.          Only pass components that had POSITIVE" | kind=entity | source=probe/workflow/host_health.py:L153 | neighbors=[.observe()]
- "workflow_host_health_rationale_195": "Re-probe a suspected host and record the verdict.          Returns VERDICT_OFFLI" | kind=entity | source=probe/workflow/host_health.py:L195 | neighbors=[.confirm()]
- "workflow_host_health_rationale_257": "Heartbeat a host for as long as it is being scanned.          This, not the stri" | kind=entity | source=probe/workflow/host_health.py:L257 | neighbors=[.watch()]
- "workflow_host_health_rationale_302": "Emit one fact per offline host, plus any flaky notes gathered." | kind=entity | source=probe/workflow/host_health.py:L302 | neighbors=[.finalize()]
- "workflow_host_health_rationale_83": "Consecutive silent components before we spend a re-check on this host." | kind=entity | source=probe/workflow/host_health.py:L83 | neighbors=[_strike_threshold()]
- "workflow_host_health_rationale_88": "Seconds between liveness heartbeats while a host is being scanned." | kind=entity | source=probe/workflow/host_health.py:L88 | neighbors=[_heartbeat_interval()]
- "workflow_host_health_rationale_96": "Consecutive missed heartbeats before a host is declared offline." | kind=entity | source=probe/workflow/host_health.py:L96 | neighbors=[_heartbeat_misses()]
- "workflow_init_rationale_1": "workflow — conditional, caching, dependency-aware orchestrator that replaces pip" | kind=entity | source=probe/workflow/__init__.py:L1 | neighbors=[__init__.py]
- "workflow_intensity_rationale_1": "intensity.py — the third, orthogonal scan knob.  Two knobs already compose in th" | kind=entity | source=probe/workflow/intensity.py:L1 | neighbors=[intensity.py]
- "workflow_intensity_rationale_65": "Return a COPY of the preset for `name` (falling back to the default).      Raise" | kind=entity | source=probe/workflow/intensity.py:L65 | neighbors=[resolve_intensity()]
- "workflow_intensity_rationale_84": "Concrete TCP port list for this intensity, or None to defer to the     profile c" | kind=entity | source=probe/workflow/intensity.py:L84 | neighbors=[intensity_port_override()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-328.json

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
