# Node Description Batch 256 of 336

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

- "scanner_scanner_base_rationale_463": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L463 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_466": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L466 | neighbors=[AdaptiveRateController] | lang=pt
- "scanner_scanner_base_rationale_469": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L469 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_471": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/scanner/scanner_base.py:L471 | neighbors=[expand_targets()] | lang=en
- "scanner_scanner_base_rationale_485": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L485 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_rationale_490": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L490 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_491": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L491 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_498": "Current integer window (>= min_window)." | kind=entity | source=probe/scanner/scanner_base.py:L498 | neighbors=[.window()] | lang=en
- "scanner_scanner_base_rationale_505": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L505 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_518": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L518 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_520": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L520 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_532": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L532 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_536": "Blocking packets-per-second pacer with AIMD rate adaptation, for raw-socket" | kind=entity | source=probe/scanner/scanner_base.py:L536 | neighbors=[SendPacer] | lang=en
- "scanner_scanner_base_rationale_549": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/scanner/scanner_base.py:L549 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_56": "HTTP/RTSP User-Agent to send — a generic browser UA by default so it does     no" | kind=entity | source=probe/scanner/scanner_base.py:L56 | neighbors=[user_agent()] | lang=en
- "scanner_scanner_base_rationale_563": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L563 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_565": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L565 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_rationale_568": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L568 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_578": "Block just long enough to hold `rate` packets/sec. No-op at rate <= 0." | kind=entity | source=probe/scanner/scanner_base.py:L578 | neighbors=[.pace()] | lang=en
- "scanner_scanner_base_rationale_580": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L580 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_591": "Fold one send/collect round's reply ratio into the rate (AIMD).          Returns" | kind=entity | source=probe/scanner/scanner_base.py:L591 | neighbors=[.observe_round()] | lang=en
- "scanner_scanner_base_rationale_598": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L598 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_607": "Pacing telemetry for the scan summary (so a throttled scan is visible)." | kind=entity | source=probe/scanner/scanner_base.py:L607 | neighbors=[.stats()] | lang=en
- "scanner_scanner_base_rationale_616": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L616 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_62": "Benign, non-attributing payload for ICMP/UDP probes — looks like ordinary     pi" | kind=entity | source=probe/scanner/scanner_base.py:L62 | neighbors=[probe_payload()] | lang=en
- "scanner_scanner_base_rationale_620": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=probe/scanner/scanner_base.py:L620 | neighbors=[expand_targets()] | lang=en
- "scanner_scanner_base_rationale_624": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L624 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_629": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/scanner/scanner_base.py:L629 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_639": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L639 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_646": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L646 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_648": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L648 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_652": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L652 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_660": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L660 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_667": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L667 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_67": "The project timezone, degrading safely when tzdata is unavailable." | kind=entity | source=probe/scanner/scanner_base.py:L67 | neighbors=[_resolve_project_tz()] | lang=en
- "scanner_scanner_base_rationale_681": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L681 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_696": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L696 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_70": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L70 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_rationale_706": "EVERY distinct (family, sockaddr) for `target`, in getaddrinfo/RFC-6724 order." | kind=entity | source=probe/scanner/scanner_base.py:L706 | neighbors=[resolve_candidates()] | lang=en
- "scanner_scanner_base_rationale_726": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L726 | neighbors=[BaseScanner] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-255.json

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
