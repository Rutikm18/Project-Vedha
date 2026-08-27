# Node Description Batch 178 of 236

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

- "scanner_mobile_scanner_rationale_279": "Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO" | kind=entity | source=probe/scanner/mobile_scanner.py:L279 | neighbors=[MobileScanner] | lang=en
- "scanner_mobile_scanner_rationale_60": "Build an ADB A_CNXN (CONNECT) message — the standard handshake initiator." | kind=entity | source=probe/scanner/mobile_scanner.py:L60 | neighbors=[_build_adb_cnxn()] | lang=en
- "scanner_mobile_scanner_rationale_71": "Parse a 24-byte ADB message header.  Returns parsed fields or None." | kind=entity | source=probe/scanner/mobile_scanner.py:L71 | neighbors=[_parse_adb_header()] | lang=pt
- "scanner_mobile_scanner_rationale_96": "Send ADB CNXN and read the device's CNXN reply.     Returns a dict with connecti" | kind=entity | source=probe/scanner/mobile_scanner.py:L96 | neighbors=[_probe_adb()] | lang=en
- "scanner_nmap_wrapper_have_nmap": "_have_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L111 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_main": "main()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L247 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_nmapexecutionerror_init": ".__init__()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L45 | neighbors=[NmapExecutionError] | lang=en
- "scanner_nmap_wrapper_rationale_1": "nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:" | kind=entity | source=probe/scanner/nmap_wrapper.py:L1 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_rationale_183": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/scanner/nmap_wrapper.py:L183 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_rationale_191": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/scanner/nmap_wrapper.py:L191 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_nmap_wrapper_rationale_43": "Actionable subprocess failure; never reinterpret it as zero findings." | kind=entity | source=probe/scanner/nmap_wrapper.py:L43 | neighbors=[NmapExecutionError] | lang=en
- "scanner_nmap_wrapper_rationale_70": "Allow tuning only; target, script, and output controls stay owned here." | kind=entity | source=probe/scanner/nmap_wrapper.py:L70 | neighbors=[_validated_extra_args()] | lang=en
- "scanner_nmap_wrapper_rationale_72": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/scanner/nmap_wrapper.py:L72 | neighbors=[nmap_wrapper.py] | lang=en
- "scanner_os_fingerprint_main": "main()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L414 | neighbors=[os_fingerprint.py] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L293 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_1": "os_fingerprint.py — OS/stack fingerprinting via ICMP + TTL (Tier 2.1 + 2.2).  TW" | kind=entity | source=probe/scanner/os_fingerprint.py:L1 | neighbors=[os_fingerprint.py] | lang=pt
- "scanner_os_fingerprint_rationale_102": "Round the observed TTL up to the nearest standard initial TTL." | kind=entity | source=probe/scanner/os_fingerprint.py:L102 | neighbors=[infer_initial_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_109": "Parse an ICMP timestamp reply (type 14): id/seq/ttl plus the three 32-bit     ti" | kind=entity | source=probe/scanner/os_fingerprint.py:L109 | neighbors=[parse_icmp_timestamps()] | lang=en
- "scanner_os_fingerprint_rationale_122": "Interpret a timestamp reply's transmit value. Per RFC 792 a *standard* value" | kind=entity | source=probe/scanner/os_fingerprint.py:L122 | neighbors=[remote_clock()] | lang=pt
- "scanner_os_fingerprint_rationale_129": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=probe/scanner/os_fingerprint.py:L129 | neighbors=[fingerprint_os()] | lang=pt
- "scanner_os_fingerprint_rationale_138": "True only for an ICMP ECHO reply that actually came FROM the probed host.      A" | kind=entity | source=probe/scanner/os_fingerprint.py:L138 | neighbors=[accept_echo_reply()] | lang=en
- "scanner_os_fingerprint_rationale_153": "Round the observed TTL up to the nearest standard initial TTL." | kind=entity | source=probe/scanner/os_fingerprint.py:L153 | neighbors=[infer_initial_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_172": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L172 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_180": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=probe/scanner/os_fingerprint.py:L180 | neighbors=[fingerprint_os()] | lang=pt
- "scanner_os_fingerprint_rationale_188": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L188 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_189": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L189 | neighbors=[_open_icmp_socket()] | lang=en
- "scanner_os_fingerprint_rationale_217": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L217 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_221": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/scanner/os_fingerprint.py:L221 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_233": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L233 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_254": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/scanner/os_fingerprint.py:L254 | neighbors=[icmp_supported()] | lang=en
- "scanner_os_fingerprint_rationale_271": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L271 | neighbors=[_open_icmp_socket()] | lang=en
- "scanner_os_fingerprint_rationale_287": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/scanner/os_fingerprint.py:L287 | neighbors=[OSFingerprintScanner] | lang=en
- "scanner_os_fingerprint_rationale_299": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=probe/scanner/os_fingerprint.py:L299 | neighbors=[._icmp_echo_ttl()] | lang=en
- "scanner_os_fingerprint_rationale_330": "Send an ICMP timestamp request (type 13); return {ttl, transmit} from a" | kind=entity | source=probe/scanner/os_fingerprint.py:L330 | neighbors=[._icmp_timestamp()] | lang=en
- "scanner_os_fingerprint_rationale_58": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=probe/scanner/os_fingerprint.py:L58 | neighbors=[_icmp()] | lang=en
- "scanner_os_fingerprint_rationale_60": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=probe/scanner/os_fingerprint.py:L60 | neighbors=[_icmp()] | lang=en
- "scanner_os_fingerprint_rationale_80": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=probe/scanner/os_fingerprint.py:L80 | neighbors=[parse_icmp_reply()] | lang=en
- "scanner_os_fingerprint_rationale_82": "Return (ttl, icmp_bytes). Raw-socket delivery prepends the full IPv4 header" | kind=entity | source=probe/scanner/os_fingerprint.py:L82 | neighbors=[_strip_ip_header()] | lang=en
- "scanner_os_fingerprint_rationale_95": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=probe/scanner/os_fingerprint.py:L95 | neighbors=[parse_icmp_reply()] | lang=en
- "scanner_passive_collector_main": "main()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L357 | neighbors=[passive_collector.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-177.json

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
