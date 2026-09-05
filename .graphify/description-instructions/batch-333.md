# Node Description Batch 334 of 336

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

- "workflow_execution_rationale_67": "Return the runtime engine inventory without claiming optional tools ran." | kind=entity | source=probe/workflow/execution.py:L67 | neighbors=[engine_manifest()] | lang=en
- "workflow_gates_gate_4_service_banner": "gate_4_service_banner()" | kind=code-symbol | source=probe/workflow/gates.py:L118 | neighbors=[gates.py] | lang=en
- "workflow_gates_gate_6_credentialed_collection": "gate_6_credentialed_collection()" | kind=code-symbol | source=probe/workflow/gates.py:L163 | neighbors=[gates.py] | lang=en
- "workflow_gates_rationale_1": "gates.py — precondition functions deciding whether each stage of the workflow ru" | kind=entity | source=probe/workflow/gates.py:L1 | neighbors=[gates.py] | lang=en
- "workflow_gates_rationale_123": "OS identity for a host already proven alive. Runs on the SAME evidence the     p" | kind=entity | source=probe/workflow/gates.py:L123 | neighbors=[gate_4b_os_fingerprint()] | lang=en
- "workflow_gates_rationale_136": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L136 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_46": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L46 | neighbors=[gate_0_is_passive_profile()] | lang=en
- "workflow_gates_rationale_48": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L48 | neighbors=[gate_0_is_passive_profile()] | lang=en
- "workflow_gates_rationale_64": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L64 | neighbors=[gate_0_is_passive_profile()] | lang=en
- "workflow_gates_rationale_72": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L72 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_74": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L74 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_90": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=probe/workflow/gates.py:L90 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_99": "True means OT/ICS passive-only mode — a hard stop, never reached by     any acti" | kind=entity | source=probe/workflow/gates.py:L99 | neighbors=[gate_0_is_passive_profile()] | lang=en
- "workflow_host_health_hosthealthmonitor_offline_hosts": ".offline_hosts()" | kind=code-symbol | source=probe/workflow/host_health.py:L345 | neighbors=[HostHealthMonitor] | lang=en
- "workflow_host_health_rationale_1": "host_health.py — detect a target that was proven alive and has since gone away," | kind=entity | source=probe/workflow/host_health.py:L1 | neighbors=[host_health.py] | lang=en
- "workflow_host_health_rationale_114": "Tracks per-host reachability across the deep-scan stages.      `liveness_probe`" | kind=entity | source=probe/workflow/host_health.py:L114 | neighbors=[HostHealthMonitor] | lang=en
- "workflow_host_health_rationale_134": "True when a component ran and got nothing back that proves life.          An emp" | kind=entity | source=probe/workflow/host_health.py:L134 | neighbors=[._is_silence()] | lang=en
- "workflow_host_health_rationale_153": "Feed one component's results in.          Only pass components that had POSITIVE" | kind=entity | source=probe/workflow/host_health.py:L153 | neighbors=[.observe()] | lang=en
- "workflow_host_health_rationale_195": "Re-probe a suspected host and record the verdict.          Returns VERDICT_OFFLI" | kind=entity | source=probe/workflow/host_health.py:L195 | neighbors=[.confirm()] | lang=en
- "workflow_host_health_rationale_257": "Heartbeat a host for as long as it is being scanned.          This, not the stri" | kind=entity | source=probe/workflow/host_health.py:L257 | neighbors=[.watch()] | lang=en
- "workflow_host_health_rationale_302": "Emit one fact per offline host, plus any flaky notes gathered." | kind=entity | source=probe/workflow/host_health.py:L302 | neighbors=[.finalize()] | lang=en
- "workflow_host_health_rationale_83": "Consecutive silent components before we spend a re-check on this host." | kind=entity | source=probe/workflow/host_health.py:L83 | neighbors=[_strike_threshold()] | lang=en
- "workflow_host_health_rationale_88": "Seconds between liveness heartbeats while a host is being scanned." | kind=entity | source=probe/workflow/host_health.py:L88 | neighbors=[_heartbeat_interval()] | lang=en
- "workflow_host_health_rationale_96": "Consecutive missed heartbeats before a host is declared offline." | kind=entity | source=probe/workflow/host_health.py:L96 | neighbors=[_heartbeat_misses()] | lang=en
- "workflow_init_rationale_1": "workflow — conditional, caching, dependency-aware orchestrator that replaces pip" | kind=entity | source=probe/workflow/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "workflow_intensity_rationale_1": "intensity.py — the third, orthogonal scan knob.  Two knobs already compose in th" | kind=entity | source=probe/workflow/intensity.py:L1 | neighbors=[intensity.py] | lang=en
- "workflow_intensity_rationale_65": "Return a COPY of the preset for `name` (falling back to the default).      Raise" | kind=entity | source=probe/workflow/intensity.py:L65 | neighbors=[resolve_intensity()] | lang=en
- "workflow_intensity_rationale_84": "Concrete TCP port list for this intensity, or None to defer to the     profile c" | kind=entity | source=probe/workflow/intensity.py:L84 | neighbors=[intensity_port_override()] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-333.json

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
