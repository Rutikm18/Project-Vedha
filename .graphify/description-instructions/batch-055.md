# Node Description Batch 56 of 92

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_ja4s_rationale_100": "JA4S from `parse_server_hello`'s output ({version, cipher, extensions})." | kind=entity | source=main_scripts/ja4s.py:L100 | neighbors=[ja4s_from_parsed()]
- "main_scripts_ja4s_rationale_110": "JA4S from raw ServerHello record bytes (reuses the JARM parser)." | kind=entity | source=main_scripts/ja4s.py:L110 | neighbors=[ja4s_from_serverhello()]
- "main_scripts_ja4s_rationale_117": "Do one standard TLS handshake and compute the server's JA4S. Reuses the     JARM" | kind=entity | source=main_scripts/ja4s.py:L117 | neighbors=[compute_ja4s()]
- "main_scripts_ja4s_rationale_57": "Yield (type, value) for each extension in a ServerHello extensions blob." | kind=entity | source=main_scripts/ja4s.py:L57 | neighbors=[_walk_extensions()]
- "main_scripts_ja4s_rationale_70": "The single ALPN protocol the server chose (b'' if none)." | kind=entity | source=main_scripts/ja4s.py:L70 | neighbors=[_selected_alpn()]
- "main_scripts_ja4s_rationale_87": "Pure JA4S from already-extracted ServerHello fields." | kind=entity | source=main_scripts/ja4s.py:L87 | neighbors=[ja4s_from_fields()]
- "main_scripts_ja4x_rationale_118": "Return a threat-intel label if this JA4X is a known-suspicious fingerprint," | kind=entity | source=main_scripts/ja4x.py:L118 | neighbors=[match_suspicious()]
- "main_scripts_ja4x_rationale_40": "DER-encode an OID's content octets and hex-encode them.      '2.5.4.6' -> '55040" | kind=entity | source=main_scripts/ja4x.py:L40 | neighbors=[oid_to_hex()]
- "main_scripts_ja4x_rationale_77": "Pure JA4X from the three ordered OID lists (dotted-decimal strings)." | kind=entity | source=main_scripts/ja4x.py:L77 | neighbors=[ja4x_from_oid_lists()]
- "main_scripts_ja4x_rationale_83": "JA4X from a `cryptography` x509 Certificate object. None if unusable." | kind=entity | source=main_scripts/ja4x.py:L83 | neighbors=[ja4x_from_cert()]
- "main_scripts_ja4x_rationale_94": "JA4X from raw DER bytes. `cryptography` is imported lazily so this module     st" | kind=entity | source=main_scripts/ja4x.py:L94 | neighbors=[ja4x_from_der()]
- "main_scripts_mass_scan_connectsweep_init": ".__init__()" | kind=code-symbol | source=main_scripts/mass_scan.py:L209 | neighbors=[_ConnectSweep]
- "main_scripts_mass_scan_main": "main()" | kind=code-symbol | source=main_scripts/mass_scan.py:L341 | neighbors=[mass_scan.py]
- "main_scripts_mcp_ai_scanner_main": "main()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L323 | neighbors=[mcp_ai_scanner.py]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L202 | neighbors=[MCPAIScanner]
- "main_scripts_mcp_ai_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L111 | neighbors=[_NoRedirect]
- "main_scripts_mcp_ai_scanner_request": "_request()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L128 | neighbors=[mcp_ai_scanner.py]
- "main_scripts_mobile_scanner_main": "main()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L340 | neighbors=[mobile_scanner.py]
- "main_scripts_nmap_wrapper_have_nmap": "_have_nmap()" | kind=code-symbol | source=main_scripts/nmap_wrapper.py:L111 | neighbors=[nmap_wrapper.py]
- "main_scripts_nmap_wrapper_main": "main()" | kind=code-symbol | source=main_scripts/nmap_wrapper.py:L247 | neighbors=[nmap_wrapper.py]
- "main_scripts_nmap_wrapper_nmapexecutionerror_init": ".__init__()" | kind=code-symbol | source=main_scripts/nmap_wrapper.py:L45 | neighbors=[NmapExecutionError]
- "main_scripts_os_fingerprint_main": "main()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L414 | neighbors=[os_fingerprint.py]
- "main_scripts_os_fingerprint_osfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L293 | neighbors=[OSFingerprintScanner]
- "main_scripts_passive_collector_main": "main()" | kind=code-symbol | source=main_scripts/passive_collector.py:L357 | neighbors=[passive_collector.py]
- "main_scripts_passive_collector_passivecollector_init": ".__init__()" | kind=code-symbol | source=main_scripts/passive_collector.py:L218 | neighbors=[PassiveCollector]
- "main_scripts_passive_collector_passivelistenererror_init": ".__init__()" | kind=code-symbol | source=main_scripts/passive_collector.py:L109 | neighbors=[PassiveListenerError]
- "main_scripts_port_scanner_main": "main()" | kind=code-symbol | source=main_scripts/port_scanner.py:L472 | neighbors=[port_scanner.py]
- "main_scripts_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/port_scanner.py:L259 | neighbors=[PortScanner]
- "main_scripts_port_scanner_scanmetrics_classified": ".classified()" | kind=code-symbol | source=main_scripts/port_scanner.py:L199 | neighbors=[ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_complete": ".complete()" | kind=code-symbol | source=main_scripts/port_scanner.py:L215 | neighbors=[ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_degraded": ".degraded()" | kind=code-symbol | source=main_scripts/port_scanner.py:L227 | neighbors=[ScanMetrics]
- "main_scripts_rdp_scanner_rdpscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L98 | neighbors=[RDPScanner]
- "main_scripts_scan_funnel_main": "main()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L327 | neighbors=[scan_funnel.py]
- "main_scripts_scan_funnel_scanfunnel_init": ".__init__()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L125 | neighbors=[ScanFunnel]
- "main_scripts_scanner_base_adaptiveratecontroller_init": ".__init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L421 | neighbors=[AdaptiveRateController]
- "main_scripts_scanner_base_base_argparser": "base_argparser()" | kind=code-symbol | source=main_scripts/scanner_base.py:L804 | neighbors=[scanner_base.py]
- "main_scripts_scanner_base_ratelimiter_init": ".__init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L368 | neighbors=[RateLimiter]
- "main_scripts_scanner_base_rationale_1": "scanner_base.py — shared foundation for every scanner module.  SCOPE OF THIS MOD" | kind=entity | source=main_scripts/scanner_base.py:L1 | neighbors=[scanner_base.py]
- "main_scripts_scanner_base_rationale_170": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=main_scripts/scanner_base.py:L170 | neighbors=[classify_os_error()]
- "main_scripts_scanner_base_rationale_186": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=main_scripts/scanner_base.py:L186 | neighbors=[describe_os_error()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-055.json

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
