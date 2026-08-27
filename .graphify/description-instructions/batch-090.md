# Node Description Batch 91 of 92

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

- "workflow_gates_rationale_76": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L76 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_78": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L78 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_80": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L80 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_84": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L84 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_86": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L86 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_89": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L89 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_gates_rationale_90": "Does `branch` apply to this host?       - Must be in this profile's allowed deep" | kind=entity | source=workflow/gates.py:L90 | neighbors=[gate_5_branch_eligible()] | lang=en
- "workflow_init_rationale_1": "workflow — conditional, caching, dependency-aware orchestrator that replaces pip" | kind=entity | source=workflow/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "workflow_intensity_rationale_1": "intensity.py — the third, orthogonal scan knob.  Two knobs already compose in th" | kind=entity | source=workflow/intensity.py:L1 | neighbors=[intensity.py] | lang=en
- "workflow_intensity_rationale_65": "Return a COPY of the preset for `name` (falling back to the default).      Raise" | kind=entity | source=workflow/intensity.py:L65 | neighbors=[resolve_intensity()] | lang=en
- "workflow_intensity_rationale_84": "Concrete TCP port list for this intensity, or None to defer to the     profile c" | kind=entity | source=workflow/intensity.py:L84 | neighbors=[intensity_port_override()] | lang=en
- "workflow_modes_rationale_1": "modes.py — engagement mode configurations. Each mode is a thin config that tunes" | kind=entity | source=workflow/modes.py:L1 | neighbors=[modes.py] | lang=en
- "workflow_modes_rationale_105": "Discovery + ports + banner only — no deep dives, no credentials." | kind=entity | source=workflow/modes.py:L105 | neighbors=[triage()] | lang=en
- "workflow_modes_rationale_112": "Full funnel, every branch the profile allows." | kind=entity | source=workflow/modes.py:L112 | neighbors=[assessment()] | lang=en
- "workflow_modes_rationale_127": "Loads a prior engagement's cache; only facts older than     recheck_older_than g" | kind=entity | source=workflow/modes.py:L127 | neighbors=[re_scan()] | lang=pt
- "workflow_modes_rationale_30": "Resolve the explicit ceiling while preserving the legacy triage knob." | kind=entity | source=workflow/modes.py:L30 | neighbors=[resolve_stage_ceiling()] | lang=en
- "workflow_modes_rationale_46": "Return whether a bounded plan includes `stage`." | kind=entity | source=workflow/modes.py:L46 | neighbors=[includes_stage()] | lang=pt
- "workflow_modes_rationale_61": "Host discovery plus the profile's TCP port catalog." | kind=entity | source=workflow/modes.py:L61 | neighbors=[discovery()] | lang=en
- "workflow_modes_rationale_72": "Liveness checks only." | kind=entity | source=workflow/modes.py:L72 | neighbors=[host_discovery()] | lang=en
- "workflow_modes_rationale_83": "Liveness checks plus the profile's TCP port catalog." | kind=entity | source=workflow/modes.py:L83 | neighbors=[port_scan()] | lang=en
- "workflow_modes_rationale_94": "Liveness, TCP ports, and service banners without deep branches." | kind=entity | source=workflow/modes.py:L94 | neighbors=[service_fingerprint()] | lang=en
- "workflow_report_asset_to_dict": "asset_to_dict()" | kind=code-symbol | source=workflow/report.py:L11 | neighbors=[report.py] | lang=en
- "workflow_report_engagement_summary": "engagement_summary()" | kind=code-symbol | source=workflow/report.py:L30 | neighbors=[report.py] | lang=en
- "workflow_report_rationale_1": "report.py — JSON-safe Asset serialization, engagement summary, and the re-scan d" | kind=entity | source=workflow/report.py:L1 | neighbors=[report.py] | lang=en
- "workflow_report_rationale_43": "re-scan mode's delta report: what changed between two engagements." | kind=entity | source=workflow/report.py:L43 | neighbors=[diff_assets()] | lang=en
- "workflow_router_rationale_1": "router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content," | kind=entity | source=workflow/router.py:L1 | neighbors=[router.py] | lang=en
- "workflow_router_rationale_51": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=workflow/router.py:L51 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_63": "True when a service banner carries a database greeting signature, so a DB     on" | kind=entity | source=workflow/router.py:L63 | neighbors=[looks_like_db()] | lang=pt
- "workflow_router_rationale_72": "True when a service banner is an SSH identification string, so an SSH     server" | kind=entity | source=workflow/router.py:L72 | neighbors=[looks_like_ssh()] | lang=en
- "workflow_router_rationale_85": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=workflow/router.py:L85 | neighbors=[route_branches()] | lang=en
- "workflow_workflow_engine_rationale_1": "workflow_engine.py — the async DAG executor. Loops through gates, checks precond" | kind=entity | source=workflow/workflow_engine.py:L1 | neighbors=[workflow_engine.py] | lang=en
- "workflow_workflow_engine_rationale_102": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L102 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_rationale_104": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L104 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_rationale_106": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L106 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_rationale_107": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=workflow/workflow_engine.py:L107 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_rationale_113": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L113 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_115": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L115 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_116": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L116 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_119": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L119 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_121": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=workflow/workflow_engine.py:L121 | neighbors=[_port_candidates()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-090.json

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
