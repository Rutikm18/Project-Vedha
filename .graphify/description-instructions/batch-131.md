# Node Description Batch 132 of 186

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

- "main_scripts_scanner_base_adaptiveratecontroller_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L350 | neighbors=[AdaptiveRateController] | lang=en
- "main_scripts_scanner_base_base_argparser": "base_argparser()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L724 | neighbors=[scanner_base.py] | lang=en
- "main_scripts_scanner_base_ratelimiter_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L297 | neighbors=[RateLimiter] | lang=en
- "main_scripts_scanner_base_rationale_1": "scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD" | kind=entity | source=probe/main_scripts/scanner_base.py:L1 | neighbors=[scanner_base.py] | lang=en
- "main_scripts_scanner_base_rationale_115": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/main_scripts/scanner_base.py:L115 | neighbors=[describe_os_error()] | lang=en
- "main_scripts_scanner_base_rationale_130": "One observation about one target. Pure fact, no interpretation.      Network-sta" | kind=entity | source=probe/main_scripts/scanner_base.py:L130 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_rationale_181": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/main_scripts/scanner_base.py:L181 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_rationale_282": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/main_scripts/scanner_base.py:L282 | neighbors=[.networks()] | lang=en
- "main_scripts_scanner_base_rationale_287": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/main_scripts/scanner_base.py:L287 | neighbors=[.excludes()] | lang=en
- "main_scripts_scanner_base_rationale_295": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/main_scripts/scanner_base.py:L295 | neighbors=[RateLimiter] | lang=it
- "main_scripts_scanner_base_rationale_314": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=probe/main_scripts/scanner_base.py:L314 | neighbors=[inet_checksum()] | lang=en
- "main_scripts_scanner_base_rationale_331": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/main_scripts/scanner_base.py:L331 | neighbors=[AdaptiveRateController] | lang=pt
- "main_scripts_scanner_base_rationale_363": "Current integer window (>= min_window)." | kind=entity | source=probe/main_scripts/scanner_base.py:L363 | neighbors=[.window()] | lang=en
- "main_scripts_scanner_base_rationale_400": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/main_scripts/scanner_base.py:L400 | neighbors=[expand_targets()] | lang=en
- "main_scripts_scanner_base_rationale_461": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/main_scripts/scanner_base.py:L461 | neighbors=[resolve()] | lang=en
- "main_scripts_scanner_base_rationale_485": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/main_scripts/scanner_base.py:L485 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_rationale_518": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/main_scripts/scanner_base.py:L518 | neighbors=[async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_549": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/main_scripts/scanner_base.py:L549 | neighbors=[async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_rationale_568": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/main_scripts/scanner_base.py:L568 | neighbors=[bracket_host()] | lang=en
- "main_scripts_scanner_base_rationale_580": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/main_scripts/scanner_base.py:L580 | neighbors=[parse_ports()] | lang=pt
- "main_scripts_scanner_base_rationale_616": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/main_scripts/scanner_base.py:L616 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_rationale_646": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/main_scripts/scanner_base.py:L646 | neighbors=[BaseScanner] | lang=pt
- "main_scripts_scanner_base_rationale_750": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/main_scripts/scanner_base.py:L750 | neighbors=[main_entrypoint()] | lang=en
- "main_scripts_scanner_base_rationale_778": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/main_scripts/scanner_base.py:L778 | neighbors=[run_cli()] | lang=en
- "main_scripts_scanner_base_rationale_99": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/main_scripts/scanner_base.py:L99 | neighbors=[classify_os_error()] | lang=en
- "main_scripts_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L618 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L160 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L228 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L192 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L741 | neighbors=[scanner_base.py] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L511 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L497 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L501 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L494 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_service_banner_main": "main()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L219 | neighbors=[service_banner.py] | lang=en
- "main_scripts_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=probe/main_scripts/service_banner.py:L1 | neighbors=[service_banner.py] | lang=en
- "main_scripts_service_banner_rationale_116": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L116 | neighbors=[._rung()] | lang=en
- "main_scripts_service_banner_rationale_130": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L130 | neighbors=[._rung()] | lang=en
- "main_scripts_service_banner_rationale_82": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L82 | neighbors=[match_service()] | lang=en
- "main_scripts_service_banner_rationale_89": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L89 | neighbors=[match_service()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-131.json

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
