# Node Description Batch 94 of 119

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

- "scanner_passive_collector_rationale_107": "All passive sources failed before the listen window could start." | kind=entity | source=probe/scanner/passive_collector.py:L107 | neighbors=[PassiveListenerError] | lang=en
- "scanner_passive_collector_rationale_120": "Open one recv-only UDP listener or raise the socket error.      Multicast groups" | kind=entity | source=probe/scanner/passive_collector.py:L120 | neighbors=[_open_listener()] | lang=en
- "scanner_passive_collector_rationale_123": "Listen-only discovery. No active probing. Reports in-scope hosts that     announ" | kind=entity | source=probe/scanner/passive_collector.py:L123 | neighbors=[PassiveCollector] | lang=en
- "scanner_passive_collector_rationale_205": "Await readability on any listener without blocking the event loop." | kind=entity | source=probe/scanner/passive_collector.py:L205 | neighbors=[._select()] | lang=en
- "scanner_passive_collector_rationale_211": "Listen-only discovery. No active probing. Reports in-scope hosts that     announ" | kind=entity | source=probe/scanner/passive_collector.py:L211 | neighbors=[PassiveCollector] | lang=en
- "scanner_passive_collector_rationale_332": "Await readability on any listener without blocking the event loop." | kind=entity | source=probe/scanner/passive_collector.py:L332 | neighbors=[._select()] | lang=en
- "scanner_passive_collector_rationale_65": "Pull short printable ASCII runs from a payload, for human-readable evidence." | kind=entity | source=probe/scanner/passive_collector.py:L65 | neighbors=[_printable_strings()] | lang=en
- "scanner_passive_collector_rationale_74": "Pull short printable ASCII runs from a payload, for human-readable evidence." | kind=entity | source=probe/scanner/passive_collector.py:L74 | neighbors=[_printable_strings()] | lang=en
- "scanner_passive_collector_rationale_82": "Best-effort device label from an announcement payload (recv-only parsing)." | kind=entity | source=probe/scanner/passive_collector.py:L82 | neighbors=[_device_hint()] | lang=en
- "scanner_passive_collector_rationale_91": "Best-effort device label from an announcement payload (recv-only parsing)." | kind=entity | source=probe/scanner/passive_collector.py:L91 | neighbors=[_device_hint()] | lang=en
- "scanner_passive_collector_rationale_98": "Open ONE recv-only UDP listener. Returns None (with a warning) on failure." | kind=entity | source=probe/scanner/passive_collector.py:L98 | neighbors=[_open_listener()] | lang=en
- "scanner_port_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L71 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L30 | neighbors=[PortScanner] | lang=en
- "scanner_port_scanner_rationale_1": "port_scanner.py — TCP connect scan.  METHOD (collection only): a full TCP connec" | kind=entity | source=probe/scanner/port_scanner.py:L1 | neighbors=[port_scanner.py] | lang=pt
- "scanner_scanner_base_base_argparser": "base_argparser()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L437 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_ratelimiter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L185 | neighbors=[RateLimiter] | lang=en
- "scanner_scanner_base_rationale_1": "scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD" | kind=entity | source=probe/scanner/scanner_base.py:L1 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_rationale_170": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L170 | neighbors=[.networks()] | lang=en
- "scanner_scanner_base_rationale_175": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/scanner/scanner_base.py:L175 | neighbors=[.excludes()] | lang=en
- "scanner_scanner_base_rationale_183": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/scanner/scanner_base.py:L183 | neighbors=[RateLimiter] | lang=it
- "scanner_scanner_base_rationale_205": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/scanner/scanner_base.py:L205 | neighbors=[expand_targets()] | lang=en
- "scanner_scanner_base_rationale_266": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L266 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_281": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L281 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_293": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L293 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_329": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L329 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_359": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L359 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_44": "One observation about one target. Pure fact, no interpretation." | kind=entity | source=probe/scanner/scanner_base.py:L44 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_rationale_463": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L463 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_491": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L491 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_69": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L69 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L331 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L116 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L80 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L454 | neighbors=[scanner_base.py] | lang=en
- "scanner_service_banner_main": "main()" | kind=code-symbol | source=probe/scanner/service_banner.py:L103 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=probe/scanner/service_banner.py:L1 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/service_banner.py:L37 | neighbors=[ServiceBannerScanner] | lang=en
- "scanner_smb_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L159 | neighbors=[smb_scanner.py] | lang=en
- "scanner_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=probe/scanner/smb_scanner.py:L1 | neighbors=[smb_scanner.py] | lang=en
- "scanner_smb_scanner_rationale_37": "Read signing posture from an SMB2 NEGOTIATE response.      The response carries" | kind=entity | source=probe/scanner/smb_scanner.py:L37 | neighbors=[parse_smb2_security_mode()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-093.json

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
