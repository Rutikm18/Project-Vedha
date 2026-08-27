# Node Description Batch 57 of 92

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

- "main_scripts_scanner_base_rationale_201": "One observation about one target. Pure fact, no interpretation.      Network-sta" | kind=entity | source=main_scripts/scanner_base.py:L201 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_rationale_252": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=main_scripts/scanner_base.py:L252 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=main_scripts/scanner_base.py:L353 | neighbors=[.networks()] | lang=en
- "main_scripts_scanner_base_rationale_358": "Read-only view of excluded networks (to build masscan --exclude)." | kind=entity | source=main_scripts/scanner_base.py:L358 | neighbors=[.excludes()] | lang=en
- "main_scripts_scanner_base_rationale_366": "Simple async rate limiter: at most `rate` operations per second." | kind=entity | source=main_scripts/scanner_base.py:L366 | neighbors=[RateLimiter] | lang=it
- "main_scripts_scanner_base_rationale_385": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=main_scripts/scanner_base.py:L385 | neighbors=[inet_checksum()] | lang=en
- "main_scripts_scanner_base_rationale_402": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=main_scripts/scanner_base.py:L402 | neighbors=[AdaptiveRateController] | lang=pt
- "main_scripts_scanner_base_rationale_434": "Current integer window (>= min_window)." | kind=entity | source=main_scripts/scanner_base.py:L434 | neighbors=[.window()] | lang=en
- "main_scripts_scanner_base_rationale_471": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=main_scripts/scanner_base.py:L471 | neighbors=[expand_targets()] | lang=en
- "main_scripts_scanner_base_rationale_532": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=main_scripts/scanner_base.py:L532 | neighbors=[resolve()] | lang=en
- "main_scripts_scanner_base_rationale_56": "HTTP/RTSP User-Agent to send — a generic browser UA by default so it does     no" | kind=entity | source=main_scripts/scanner_base.py:L56 | neighbors=[user_agent()] | lang=en
- "main_scripts_scanner_base_rationale_565": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=main_scripts/scanner_base.py:L565 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_rationale_598": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=main_scripts/scanner_base.py:L598 | neighbors=[async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_62": "Benign, non-attributing payload for ICMP/UDP probes — looks like ordinary     pi" | kind=entity | source=main_scripts/scanner_base.py:L62 | neighbors=[probe_payload()] | lang=en
- "main_scripts_scanner_base_rationale_629": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=main_scripts/scanner_base.py:L629 | neighbors=[async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_rationale_648": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=main_scripts/scanner_base.py:L648 | neighbors=[bracket_host()] | lang=en
- "main_scripts_scanner_base_rationale_660": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=main_scripts/scanner_base.py:L660 | neighbors=[parse_ports()] | lang=pt
- "main_scripts_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=main_scripts/scanner_base.py:L69 | neighbors=[choose_source_port()] | lang=en
- "main_scripts_scanner_base_rationale_696": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=main_scripts/scanner_base.py:L696 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_rationale_726": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=main_scripts/scanner_base.py:L726 | neighbors=[BaseScanner] | lang=pt
- "main_scripts_scanner_base_rationale_79": "A per-probe delay of `base` seconds ± up to `jitter` fraction of random     vari" | kind=entity | source=main_scripts/scanner_base.py:L79 | neighbors=[jittered_delay()] | lang=en
- "main_scripts_scanner_base_rationale_837": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=main_scripts/scanner_base.py:L837 | neighbors=[main_entrypoint()] | lang=en
- "main_scripts_scanner_base_rationale_865": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=main_scripts/scanner_base.py:L865 | neighbors=[run_cli()] | lang=en
- "main_scripts_scanner_base_rationale_90": "Heuristic: is this host a tarpit / honeypot / ACK-everything middlebox?      Suc" | kind=entity | source=main_scripts/scanner_base.py:L90 | neighbors=[assess_tarpit()] | lang=en
- "main_scripts_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L698 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L231 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=main_scripts/scanner_base.py:L299 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L263 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=main_scripts/scanner_base.py:L828 | neighbors=[scanner_base.py] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=main_scripts/scanner_base.py:L591 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=main_scripts/scanner_base.py:L577 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=main_scripts/scanner_base.py:L581 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L574 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_service_banner_main": "main()" | kind=code-symbol | source=main_scripts/service_banner.py:L240 | neighbors=[service_banner.py] | lang=en
- "main_scripts_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/service_banner.py:L126 | neighbors=[ServiceBannerScanner] | lang=en
- "main_scripts_service_enum_reverse_dns": "reverse_dns()" | kind=code-symbol | source=main_scripts/service_enum.py:L119 | neighbors=[service_enum.py] | lang=en
- "main_scripts_service_enum_serviceenumscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/service_enum.py:L452 | neighbors=[ServiceEnumScanner] | lang=en
- "main_scripts_smb_scanner_main": "main()" | kind=code-symbol | source=main_scripts/smb_scanner.py:L197 | neighbors=[smb_scanner.py] | lang=en
- "main_scripts_smb_scanner_smbscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/smb_scanner.py:L145 | neighbors=[SMBScanner] | lang=en
- "main_scripts_snmp_scanner_main": "main()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L401 | neighbors=[snmp_scanner.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-056.json

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
