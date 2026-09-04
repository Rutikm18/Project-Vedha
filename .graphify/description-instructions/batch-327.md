# Node Description Batch 328 of 330

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
- "workflow_modes_rationale_94": "Liveness, TCP ports, and service banners without deep branches." | kind=entity | source=probe/workflow/modes.py:L94 | neighbors=[service_fingerprint()] | lang=en
- "workflow_report_asset_to_dict": "asset_to_dict()" | kind=code-symbol | source=probe/workflow/report.py:L11 | neighbors=[report.py] | lang=en
- "workflow_report_engagement_summary": "engagement_summary()" | kind=code-symbol | source=probe/workflow/report.py:L30 | neighbors=[report.py] | lang=en
- "workflow_report_rationale_1": "report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d" | kind=entity | source=probe/workflow/report.py:L1 | neighbors=[report.py] | lang=en
- "workflow_report_rationale_43": "re-scan mode's delta report: what changed between two engagements." | kind=entity | source=probe/workflow/report.py:L43 | neighbors=[diff_assets()] | lang=en
- "workflow_router_rationale_1": "router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content," | kind=entity | source=probe/workflow/router.py:L1 | neighbors=[router.py] | lang=en
- "workflow_router_rationale_102": "True when a service banner carries a database greeting signature, so a DB     on" | kind=entity | source=probe/workflow/router.py:L102 | neighbors=[looks_like_db()] | lang=pt
- "workflow_router_rationale_115": "True when a service banner is an SSH identification string, so an SSH     server" | kind=entity | source=probe/workflow/router.py:L115 | neighbors=[looks_like_ssh()] | lang=en
- "workflow_router_rationale_130": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L130 | neighbors=[route_branches()] | lang=en
- "workflow_router_rationale_43": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=probe/workflow/router.py:L43 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_51": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=probe/workflow/router.py:L51 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_56": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L56 | neighbors=[route_branches()] | lang=en
- "workflow_router_rationale_63": "True when a service banner carries a database greeting signature, so a DB     on" | kind=entity | source=probe/workflow/router.py:L63 | neighbors=[looks_like_db()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-327.json

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
