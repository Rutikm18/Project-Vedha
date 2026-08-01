# Node Description Batch 118 of 119

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
- "workflow_router_rationale_43": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=probe/workflow/router.py:L43 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_51": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=probe/workflow/router.py:L51 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_56": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L56 | neighbors=[route_branches()] | lang=en
- "workflow_router_rationale_63": "True when a service banner carries a database greeting signature, so a DB     on" | kind=entity | source=probe/workflow/router.py:L63 | neighbors=[looks_like_db()] | lang=pt
- "workflow_router_rationale_73": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L73 | neighbors=[route_branches()] | lang=en
- "workflow_workflow_engine_rationale_1": "workflow_engine.py — the async DAG executor. Loops through gates, checks precond" | kind=entity | source=probe/workflow/workflow_engine.py:L1 | neighbors=[workflow_engine.py] | lang=en
- "workflow_workflow_engine_rationale_104": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L104 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_rationale_110": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L110 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_134": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L134 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_rationale_136": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L136 | neighbors=[run_engagement()] | lang=en
- "workflow_workflow_engine_rationale_236": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L236 | neighbors=[run_engagement()] | lang=en
- "workflow_workflow_engine_rationale_51": "Runs scanner.scan_target(host) across hosts concurrently; the     scanner's own" | kind=entity | source=probe/workflow/workflow_engine.py:L51 | neighbors=[_gather_per_host()] | lang=en
- "workflow_workflow_engine_rationale_59": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L59 | neighbors=[_scan_one()] | lang=en
- "workflow_workflow_engine_rationale_64": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L64 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_rationale_77": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L77 | neighbors=[_gather_per_host()] | lang=en
- "workflow_workflow_engine_rationale_80": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L80 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_94": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L94 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_sink_close": ".close()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L145 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_sink_init": ".__init__()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L141 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_sink_write": ".write()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L143 | neighbors=[_Sink] | lang=en
- "agent_agent_rationale_138": "Fast port discovery with naabu. Feeds port list to Nmap." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L138 | lang=en
- "agent_agent_rationale_202": "Nmap service enumeration. Accepts port list from Naabu." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L202 | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-117.json

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
