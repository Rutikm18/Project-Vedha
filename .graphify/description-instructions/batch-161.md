# Node Description Batch 162 of 236

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "main_scripts_scanner_base_rationale_170": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/main_scripts/scanner_base.py:L170 | neighbors=[classify_os_error()] | lang=en
- "main_scripts_scanner_base_rationale_181": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/main_scripts/scanner_base.py:L181 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_rationale_186": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/main_scripts/scanner_base.py:L186 | neighbors=[describe_os_error()] | lang=en
- "main_scripts_scanner_base_rationale_201": "One observation about one target. Pure fact, no interpretation.      Network-sta" | kind=entity | source=probe/main_scripts/scanner_base.py:L201 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_rationale_252": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/main_scripts/scanner_base.py:L252 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_rationale_282": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/main_scripts/scanner_base.py:L282 | neighbors=[.networks()] | lang=en
- "main_scripts_scanner_base_rationale_287": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/main_scripts/scanner_base.py:L287 | neighbors=[.excludes()] | lang=en
- "main_scripts_scanner_base_rationale_295": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/main_scripts/scanner_base.py:L295 | neighbors=[RateLimiter] | lang=it
- "main_scripts_scanner_base_rationale_314": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=probe/main_scripts/scanner_base.py:L314 | neighbors=[inet_checksum()] | lang=en
- "main_scripts_scanner_base_rationale_331": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/main_scripts/scanner_base.py:L331 | neighbors=[AdaptiveRateController] | lang=pt
- "main_scripts_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/main_scripts/scanner_base.py:L353 | neighbors=[.networks()] | lang=en
- "main_scripts_scanner_base_rationale_358": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/main_scripts/scanner_base.py:L358 | neighbors=[.excludes()] | lang=en
- "main_scripts_scanner_base_rationale_363": "Current integer window (>= min_window)." | kind=entity | source=probe/main_scripts/scanner_base.py:L363 | neighbors=[.window()] | lang=en
- "main_scripts_scanner_base_rationale_366": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/main_scripts/scanner_base.py:L366 | neighbors=[RateLimiter] | lang=it
- "main_scripts_scanner_base_rationale_385": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=probe/main_scripts/scanner_base.py:L385 | neighbors=[inet_checksum()] | lang=en
- "main_scripts_scanner_base_rationale_400": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/main_scripts/scanner_base.py:L400 | neighbors=[expand_targets()] | lang=en
- "main_scripts_scanner_base_rationale_402": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/main_scripts/scanner_base.py:L402 | neighbors=[AdaptiveRateController] | lang=pt
- "main_scripts_scanner_base_rationale_434": "Current integer window (>= min_window)." | kind=entity | source=probe/main_scripts/scanner_base.py:L434 | neighbors=[.window()] | lang=en
- "main_scripts_scanner_base_rationale_461": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/main_scripts/scanner_base.py:L461 | neighbors=[resolve()] | lang=en
- "main_scripts_scanner_base_rationale_471": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/main_scripts/scanner_base.py:L471 | neighbors=[expand_targets()] | lang=en
- "main_scripts_scanner_base_rationale_485": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/main_scripts/scanner_base.py:L485 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_rationale_518": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/main_scripts/scanner_base.py:L518 | neighbors=[async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_532": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/main_scripts/scanner_base.py:L532 | neighbors=[resolve()] | lang=en
- "main_scripts_scanner_base_rationale_549": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/main_scripts/scanner_base.py:L549 | neighbors=[async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_rationale_56": "HTTP/RTSP User-Agent to send — a generic browser UA by default so it does     no" | kind=entity | source=probe/main_scripts/scanner_base.py:L56 | neighbors=[user_agent()] | lang=en
- "main_scripts_scanner_base_rationale_565": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/main_scripts/scanner_base.py:L565 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_rationale_568": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/main_scripts/scanner_base.py:L568 | neighbors=[bracket_host()] | lang=en
- "main_scripts_scanner_base_rationale_580": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/main_scripts/scanner_base.py:L580 | neighbors=[parse_ports()] | lang=pt
- "main_scripts_scanner_base_rationale_598": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/main_scripts/scanner_base.py:L598 | neighbors=[async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_616": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/main_scripts/scanner_base.py:L616 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_rationale_62": "Benign, non-attributing payload for ICMP/UDP probes — looks like ordinary     pi" | kind=entity | source=probe/main_scripts/scanner_base.py:L62 | neighbors=[probe_payload()] | lang=en
- "main_scripts_scanner_base_rationale_629": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/main_scripts/scanner_base.py:L629 | neighbors=[async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_rationale_646": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/main_scripts/scanner_base.py:L646 | neighbors=[BaseScanner] | lang=pt
- "main_scripts_scanner_base_rationale_648": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/main_scripts/scanner_base.py:L648 | neighbors=[bracket_host()] | lang=en
- "main_scripts_scanner_base_rationale_660": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/main_scripts/scanner_base.py:L660 | neighbors=[parse_ports()] | lang=pt
- "main_scripts_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=probe/main_scripts/scanner_base.py:L69 | neighbors=[choose_source_port()] | lang=en
- "main_scripts_scanner_base_rationale_696": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/main_scripts/scanner_base.py:L696 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_rationale_726": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/main_scripts/scanner_base.py:L726 | neighbors=[BaseScanner] | lang=pt
- "main_scripts_scanner_base_rationale_750": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/main_scripts/scanner_base.py:L750 | neighbors=[main_entrypoint()] | lang=en
- "main_scripts_scanner_base_rationale_778": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/main_scripts/scanner_base.py:L778 | neighbors=[run_cli()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-161.json

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
