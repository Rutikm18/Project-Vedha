# Node Description Batch 65 of 92

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

- "scanner_scan_funnel_rationale_209": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L209 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_211": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L211 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_212": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L212 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_215": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L215 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_216": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L216 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_218": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L218 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_219": "Wire the funnel with the package's real scanners. Imported lazily so the     fun" | kind=entity | source=scanner/scan_funnel.py:L219 | neighbors=[build_default_funnel()] | lang=en
- "scanner_scan_funnel_rationale_57": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L57 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_59": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L59 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_60": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L60 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_63": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L63 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_64": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L64 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_66": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L66 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_67": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=scanner/scan_funnel.py:L67 | neighbors=[route_ports()] | lang=en
- "scanner_scan_funnel_rationale_74": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L74 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_76": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L76 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_77": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L77 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_80": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L80 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_81": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L81 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_83": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L83 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_84": "The full outcome of funnelling one host." | kind=entity | source=scanner/scan_funnel.py:L84 | neighbors=[FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_88": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L88 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_rationale_90": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L90 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_rationale_91": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L91 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_rationale_94": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L94 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_rationale_95": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L95 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_rationale_97": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L97 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_rationale_98": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=scanner/scan_funnel.py:L98 | neighbors=[_candidate_ports()] | lang=en
- "scanner_scan_funnel_scanfunnel_init": ".__init__()" | kind=code-symbol | source=scanner/scan_funnel.py:L125 | neighbors=[ScanFunnel] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_init": ".__init__()" | kind=code-symbol | source=scanner/scanner_base.py:L421 | neighbors=[AdaptiveRateController] | lang=en
- "scanner_scanner_base_base_argparser": "base_argparser()" | kind=code-symbol | source=scanner/scanner_base.py:L804 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_ratelimiter_init": ".__init__()" | kind=code-symbol | source=scanner/scanner_base.py:L368 | neighbors=[RateLimiter] | lang=en
- "scanner_scanner_base_rationale_1": "scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD" | kind=entity | source=scanner/scanner_base.py:L1 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_rationale_170": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=scanner/scanner_base.py:L170 | neighbors=[classify_os_error()] | lang=en
- "scanner_scanner_base_rationale_186": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=scanner/scanner_base.py:L186 | neighbors=[describe_os_error()] | lang=en
- "scanner_scanner_base_rationale_201": "One observation about one target. Pure fact, no interpretation.      Network-sta" | kind=entity | source=scanner/scanner_base.py:L201 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_rationale_252": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=scanner/scanner_base.py:L252 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=scanner/scanner_base.py:L353 | neighbors=[.networks()] | lang=en
- "scanner_scanner_base_rationale_358": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=scanner/scanner_base.py:L358 | neighbors=[.excludes()] | lang=en
- "scanner_scanner_base_rationale_366": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=scanner/scanner_base.py:L366 | neighbors=[RateLimiter] | lang=it

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-064.json

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
