# Node Description Batch 251 of 332

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

- "scanner_scanner_base_rationale_293": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L293 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_295": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/scanner/scanner_base.py:L295 | neighbors=[RateLimiter] | lang=it
- "scanner_scanner_base_rationale_314": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=probe/scanner/scanner_base.py:L314 | neighbors=[inet_checksum()] | lang=en
- "scanner_scanner_base_rationale_316": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L316 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_rationale_323": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L323 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_329": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L329 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_331": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L331 | neighbors=[AdaptiveRateController] | lang=pt
- "scanner_scanner_base_rationale_335": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L335 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_350": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L350 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_358": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/scanner/scanner_base.py:L358 | neighbors=[.excludes()] | lang=en
- "scanner_scanner_base_rationale_363": "Current integer window (>= min_window)." | kind=entity | source=probe/scanner/scanner_base.py:L363 | neighbors=[.window()] | lang=en
- "scanner_scanner_base_rationale_365": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L365 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_366": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/scanner/scanner_base.py:L366 | neighbors=[RateLimiter] | lang=it
- "scanner_scanner_base_rationale_374": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L374 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_rationale_385": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=probe/scanner/scanner_base.py:L385 | neighbors=[inet_checksum()] | lang=en
- "scanner_scanner_base_rationale_392": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L392 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_400": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/scanner/scanner_base.py:L400 | neighbors=[expand_targets()] | lang=en
- "scanner_scanner_base_rationale_401": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L401 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_402": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L402 | neighbors=[AdaptiveRateController] | lang=pt
- "scanner_scanner_base_rationale_407": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L407 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_417": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L417 | neighbors=[.networks()] | lang=en
- "scanner_scanner_base_rationale_422": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=probe/scanner/scanner_base.py:L422 | neighbors=[.excludes()] | lang=en
- "scanner_scanner_base_rationale_423": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/scanner/scanner_base.py:L423 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_430": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=probe/scanner/scanner_base.py:L430 | neighbors=[RateLimiter] | lang=it
- "scanner_scanner_base_rationale_431": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L431 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_434": "Current integer window (>= min_window)." | kind=entity | source=probe/scanner/scanner_base.py:L434 | neighbors=[.window()] | lang=en
- "scanner_scanner_base_rationale_438": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/scanner/scanner_base.py:L438 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_44": "One observation about one target. Pure fact, no interpretation." | kind=entity | source=probe/scanner/scanner_base.py:L44 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_rationale_442": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L442 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_449": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=probe/scanner/scanner_base.py:L449 | neighbors=[inet_checksum()] | lang=en
- "scanner_scanner_base_rationale_45": "One observation about one target. Pure fact, no interpretation." | kind=entity | source=probe/scanner/scanner_base.py:L45 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_rationale_454": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L454 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_457": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L457 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_461": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L461 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_463": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L463 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_466": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L466 | neighbors=[AdaptiveRateController] | lang=pt
- "scanner_scanner_base_rationale_469": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L469 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_471": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/scanner/scanner_base.py:L471 | neighbors=[expand_targets()] | lang=en
- "scanner_scanner_base_rationale_485": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L485 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_rationale_490": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L490 | neighbors=[ResultWriter] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-250.json

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
