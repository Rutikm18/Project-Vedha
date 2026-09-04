# Node Description Batch 247 of 332

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

- "scanner_os_fingerprint_rationale_254": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L254 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_271": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L271 | neighbors=[_open_icmp_socket()] | lang=en
- "scanner_os_fingerprint_rationale_287": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/scanner/os_fingerprint.py:L287 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_299": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L299 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_321": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L321 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_330": "Send an ICMP timestamp request (type 13); return {ttl, transmit} from a" | kind=entity | source=probe/scanner/os_fingerprint.py:L330 | neighbors=[._icmp_timestamp()] | lang=en
- "scanner_os_fingerprint_rationale_338": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L338 | neighbors=[_open_icmp_socket()] | lang=en
- "scanner_os_fingerprint_rationale_354": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/scanner/os_fingerprint.py:L354 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_371": "Best-effort exact Windows build via SMB2 NTLM (shared impl). {} on any         f" | kind=entity | source=probe/scanner/os_fingerprint.py:L371 | neighbors=[._smb_build()] | lang=en
- "scanner_os_fingerprint_rationale_383": "Fuse an SMB2 NTLM build into an OS result: authoritative release + build," | kind=entity | source=probe/scanner/os_fingerprint.py:L383 | neighbors=[._apply_smb_build()] | lang=en
- "scanner_os_fingerprint_rationale_406": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L406 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_437": "Send an ICMP timestamp request (type 13); return {ttl, transmit} from a" | kind=entity | source=probe/scanner/os_fingerprint.py:L437 | neighbors=[._icmp_timestamp()] | lang=en
- "scanner_os_fingerprint_rationale_469": "FIX 3b: aliveness/TTL came from a TCP SYN-ACK, not ICMP. Label the TTL         s" | kind=entity | source=probe/scanner/os_fingerprint.py:L469 | neighbors=[._tcp_ttl_result()] | lang=en
- "scanner_os_fingerprint_rationale_58": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=probe/scanner/os_fingerprint.py:L58 | neighbors=[_icmp()] | lang=en
- "scanner_os_fingerprint_rationale_60": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=probe/scanner/os_fingerprint.py:L60 | neighbors=[_icmp()] | lang=en
- "scanner_os_fingerprint_rationale_80": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=probe/scanner/os_fingerprint.py:L80 | neighbors=[parse_icmp_reply()] | lang=en
- "scanner_os_fingerprint_rationale_82": "Return (ttl, icmp_bytes). Raw-socket delivery prepends the full IPv4 header" | kind=entity | source=probe/scanner/os_fingerprint.py:L82 | neighbors=[_strip_ip_header()] | lang=en
- "scanner_os_fingerprint_rationale_95": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=probe/scanner/os_fingerprint.py:L95 | neighbors=[parse_icmp_reply()] | lang=en
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
- "scanner_port_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L722 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_portscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L342 | neighbors=[PortScanner] | lang=en
- "scanner_port_scanner_rationale_1": "port_scanner.py — TCP connect scan with an evidence-based state engine.  METHOD" | kind=entity | source=probe/scanner/port_scanner.py:L1 | neighbors=[port_scanner.py] | lang=en
- "scanner_port_scanner_rationale_104": "Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier" | kind=entity | source=probe/scanner/port_scanner.py:L104 | neighbors=[classify_os_error()] | lang=en
- "scanner_port_scanner_rationale_117": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L117 | neighbors=[_family_of()] | lang=en
- "scanner_port_scanner_rationale_127": "Map a connect()-time OSError to (state, reason).      DNS failures (socket.gaier" | kind=entity | source=probe/scanner/port_scanner.py:L127 | neighbors=[classify_os_error()] | lang=en
- "scanner_port_scanner_rationale_128": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=probe/scanner/port_scanner.py:L128 | neighbors=[resolve_profile()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-246.json

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
