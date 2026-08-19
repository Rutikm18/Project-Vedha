# Node Description Batch 176 of 227

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

- "scanner_scanner_base_rationale_580": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L580 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_598": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L598 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_616": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L616 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_62": "Benign, non-attributing payload for ICMP/UDP probes — looks like ordinary     pi" | kind=entity | source=probe/scanner/scanner_base.py:L62 | neighbors=[probe_payload()] | lang=en
- "scanner_scanner_base_rationale_624": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L624 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_629": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/scanner/scanner_base.py:L629 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_639": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L639 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_646": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L646 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_648": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L648 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_652": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L652 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_660": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L660 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_667": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L667 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_696": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L696 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_70": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L70 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_rationale_726": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L726 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_750": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L750 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_778": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L778 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_79": "A per-probe delay of `base` seconds ± up to `jitter` fraction of random     vari" | kind=entity | source=probe/scanner/scanner_base.py:L79 | neighbors=[jittered_delay()] | lang=en
- "scanner_scanner_base_rationale_837": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L837 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_865": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L865 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_90": "Heuristic: is this host a tarpit / honeypot / ACK-everything middlebox?      Suc" | kind=entity | source=probe/scanner/scanner_base.py:L90 | neighbors=[assess_tarpit()] | lang=en
- "scanner_scanner_base_rationale_99": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/scanner/scanner_base.py:L99 | neighbors=[classify_os_error()] | lang=en
- "scanner_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L698 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L231 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L299 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L263 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L828 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L591 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L577 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L581 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L574 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_service_banner_main": "main()" | kind=code-symbol | source=probe/scanner/service_banner.py:L222 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=probe/scanner/service_banner.py:L1 | neighbors=[service_banner.py] | lang=en
- "scanner_service_banner_rationale_116": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/scanner/service_banner.py:L116 | neighbors=[._rung()] | lang=en
- "scanner_service_banner_rationale_130": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/scanner/service_banner.py:L130 | neighbors=[._rung()] | lang=en
- "scanner_service_banner_rationale_133": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/scanner/service_banner.py:L133 | neighbors=[._rung()] | lang=en
- "scanner_service_banner_rationale_82": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L82 | neighbors=[match_service()] | lang=en
- "scanner_service_banner_rationale_89": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L89 | neighbors=[match_service()] | lang=en
- "scanner_service_banner_rationale_92": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/scanner/service_banner.py:L92 | neighbors=[match_service()] | lang=en
- "scanner_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/service_banner.py:L126 | neighbors=[ServiceBannerScanner] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-175.json

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
