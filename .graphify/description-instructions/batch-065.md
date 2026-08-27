# Node Description Batch 66 of 92

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

- "scanner_scanner_base_rationale_385": "Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP," | kind=entity | source=scanner/scanner_base.py:L385 | neighbors=[inet_checksum()] | lang=en
- "scanner_scanner_base_rationale_402": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=scanner/scanner_base.py:L402 | neighbors=[AdaptiveRateController] | lang=pt
- "scanner_scanner_base_rationale_434": "Current integer window (>= min_window)." | kind=entity | source=scanner/scanner_base.py:L434 | neighbors=[.window()] | lang=en
- "scanner_scanner_base_rationale_471": "Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges     ('10" | kind=entity | source=scanner/scanner_base.py:L471 | neighbors=[expand_targets()] | lang=en
- "scanner_scanner_base_rationale_532": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=scanner/scanner_base.py:L532 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_56": "HTTP/RTSP User-Agent to send — a generic browser UA by default so it does     no" | kind=entity | source=scanner/scanner_base.py:L56 | neighbors=[user_agent()] | lang=en
- "scanner_scanner_base_rationale_565": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=scanner/scanner_base.py:L565 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_rationale_598": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=scanner/scanner_base.py:L598 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_62": "Benign, non-attributing payload for ICMP/UDP probes — looks like ordinary     pi" | kind=entity | source=scanner/scanner_base.py:L62 | neighbors=[probe_payload()] | lang=en
- "scanner_scanner_base_rationale_629": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=scanner/scanner_base.py:L629 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_648": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=scanner/scanner_base.py:L648 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_660": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=scanner/scanner_base.py:L660 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=scanner/scanner_base.py:L69 | neighbors=[choose_source_port()] | lang=en
- "scanner_scanner_base_rationale_696": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=scanner/scanner_base.py:L696 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_726": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=scanner/scanner_base.py:L726 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_79": "A per-probe delay of `base` seconds ± up to `jitter` fraction of random     vari" | kind=entity | source=scanner/scanner_base.py:L79 | neighbors=[jittered_delay()] | lang=en
- "scanner_scanner_base_rationale_837": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=scanner/scanner_base.py:L837 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_865": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=scanner/scanner_base.py:L865 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_90": "Heuristic: is this host a tarpit / honeypot / ACK-everything middlebox?      Suc" | kind=entity | source=scanner/scanner_base.py:L90 | neighbors=[assess_tarpit()] | lang=en
- "scanner_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=scanner/scanner_base.py:L698 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=scanner/scanner_base.py:L231 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=scanner/scanner_base.py:L299 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=scanner/scanner_base.py:L263 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=scanner/scanner_base.py:L828 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=scanner/scanner_base.py:L591 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=scanner/scanner_base.py:L577 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=scanner/scanner_base.py:L581 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=scanner/scanner_base.py:L574 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_service_banner_main": "main()" | kind=code-symbol | source=scanner/service_banner.py:L240 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=scanner/service_banner.py:L1 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_rationale_133": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=scanner/service_banner.py:L133 | neighbors=[._rung()] | lang=en
- "scanner_service_banner_rationale_92": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=scanner/service_banner.py:L92 | neighbors=[match_service()] | lang=en
- "scanner_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=scanner/service_banner.py:L126 | neighbors=[ServiceBannerScanner] | lang=en
- "scanner_service_enum_rationale_1": "service_enum.py — enrichment / enumeration layer that runs AFTER host_discovery." | kind=entity | source=scanner/service_enum.py:L1 | neighbors=[service_enum.py] | lang=en
- "scanner_service_enum_rationale_105": "Everything learned about one target beyond 'it is alive'." | kind=entity | source=scanner/service_enum.py:L105 | neighbors=[Enrichment] | lang=en
- "scanner_service_enum_rationale_127": "Decode a DNS name (with 0xC0 compression) -> (name, next_offset)." | kind=entity | source=scanner/service_enum.py:L127 | neighbors=[_dns_read_name()] | lang=en
- "scanner_service_enum_rationale_148": "Ask the host over multicast DNS (5353) for the PTR of its own address." | kind=entity | source=scanner/service_enum.py:L148 | neighbors=[mdns_hostname()] | lang=en
- "scanner_service_enum_rationale_175": "NetBIOS first-level name encoding (16-byte name -> 32 nibble bytes)." | kind=entity | source=scanner/service_enum.py:L175 | neighbors=[_nb_encode()] | lang=en
- "scanner_service_enum_rationale_185": "NBNS node-status (NBSTAT) query to UDP/137; return the workstation name." | kind=entity | source=scanner/service_enum.py:L185 | neighbors=[netbios_name()] | lang=en
- "scanner_service_enum_rationale_216": "Run the three name sources concurrently off the event loop." | kind=entity | source=scanner/service_enum.py:L216 | neighbors=[resolve_hostnames()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-065.json

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
