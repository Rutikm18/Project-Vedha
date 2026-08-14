# Node Description Batch 142 of 186

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

- "scanner_nmap_wrapper_rationale_183": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/scanner/nmap_wrapper.py:L183 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_rationale_43": "Actionable subprocess failure; never reinterpret it as zero findings." | kind=entity | source=probe/scanner/nmap_wrapper.py:L43 | neighbors=[NmapExecutionError] | lang=en
- "scanner_nmap_wrapper_rationale_70": "Allow tuning only; target, script, and output controls stay owned here." | kind=entity | source=probe/scanner/nmap_wrapper.py:L70 | neighbors=[_validated_extra_args()] | lang=en
- "scanner_nmap_wrapper_rationale_72": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/scanner/nmap_wrapper.py:L72 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_os_fingerprint_main": "main()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L288 | neighbors=[os_fingerprint.py] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L227 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_1": "os_fingerprint.py — OS/stack fingerprinting via ICMP + TTL (Tier 2.1 + 2.2).  TW" | kind=entity | source=probe/scanner/os_fingerprint.py:L1 | neighbors=[os_fingerprint.py] | lang=pt
- "scanner_os_fingerprint_rationale_102": "Round the observed TTL up to the nearest standard initial TTL." | kind=entity | source=probe/scanner/os_fingerprint.py:L102 | neighbors=[infer_initial_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_129": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=probe/scanner/os_fingerprint.py:L129 | neighbors=[fingerprint_os()] | lang=pt
- "scanner_os_fingerprint_rationale_172": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L172 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_188": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L188 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_189": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L189 | neighbors=[_open_icmp_socket()] | lang=en
- "scanner_os_fingerprint_rationale_217": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L217 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_221": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/scanner/os_fingerprint.py:L221 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_233": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L233 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_58": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=probe/scanner/os_fingerprint.py:L58 | neighbors=[_icmp()] | lang=en
- "scanner_os_fingerprint_rationale_80": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=probe/scanner/os_fingerprint.py:L80 | neighbors=[parse_icmp_reply()] | lang=en
- "scanner_passive_collector_main": "main()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L357 | neighbors=[passive_collector.py] | lang=en
- "scanner_passive_collector_passivecollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L218 | neighbors=[PassiveCollector] | lang=en
- "scanner_passive_collector_passivelistenererror_init": ".__init__()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L109 | neighbors=[PassiveListenerError] | lang=en
- "scanner_passive_collector_rationale_1": "passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS)." | kind=entity | source=probe/scanner/passive_collector.py:L1 | neighbors=[passive_collector.py] | lang=en
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
- "scanner_port_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L418 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L253 | neighbors=[PortScanner] | lang=en
- "scanner_port_scanner_rationale_1": "port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD" | kind=entity | source=probe/scanner/port_scanner.py:L1 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_rationale_104": "Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier" | kind=entity | source=probe/scanner/port_scanner.py:L104 | neighbors=[classify_os_error()] | lang=en
- "scanner_port_scanner_rationale_117": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L117 | neighbors=[_family_of()] | lang=en
- "scanner_port_scanner_rationale_127": "Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier" | kind=entity | source=probe/scanner/port_scanner.py:L127 | neighbors=[classify_os_error()] | lang=en
- "scanner_port_scanner_rationale_128": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=probe/scanner/port_scanner.py:L128 | neighbors=[resolve_profile()] | lang=pt
- "scanner_port_scanner_rationale_154": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=probe/scanner/port_scanner.py:L154 | neighbors=[ScanMetrics] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-141.json

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
