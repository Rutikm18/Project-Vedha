# Node Description Batch 160 of 227

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

- "main_scripts_syn_scanner_rationale_245": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/main_scripts/syn_scanner.py:L245 | neighbors=[SynScanner] | lang=en
- "main_scripts_syn_scanner_rationale_246": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/main_scripts/syn_scanner.py:L246 | neighbors=[SynScanner] | lang=en
- "main_scripts_syn_scanner_rationale_414": "Turn resolved port states + harvested intel into ScanResults. Pure —         no" | kind=entity | source=probe/main_scripts/syn_scanner.py:L414 | neighbors=[._build_results()] | lang=en
- "main_scripts_syn_scanner_rationale_418": "Turn resolved port states + harvested intel into ScanResults. Pure —         no" | kind=entity | source=probe/main_scripts/syn_scanner.py:L418 | neighbors=[._build_results()] | lang=en
- "main_scripts_syn_scanner_rationale_63": "Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma" | kind=entity | source=probe/main_scripts/syn_scanner.py:L63 | neighbors=[build_ip_header()] | lang=pt
- "main_scripts_syn_scanner_rationale_81": "Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma" | kind=entity | source=probe/main_scripts/syn_scanner.py:L81 | neighbors=[build_ip_header()] | lang=pt
- "main_scripts_syn_scanner_rationale_82": "Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma" | kind=entity | source=probe/main_scripts/syn_scanner.py:L82 | neighbors=[build_ip_header()] | lang=pt
- "main_scripts_syn_scanner_rationale_86": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L86 | neighbors=[build_tcp_syn()] | lang=pt
- "main_scripts_tls_fingerprint_main": "main()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L320 | neighbors=[tls_fingerprint.py] | lang=en
- "main_scripts_tls_fingerprint_rationale_1": "tls_fingerprint.py — active TLS server fingerprint (Tier 2.3, JARM methodology)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L1 | neighbors=[tls_fingerprint.py] | lang=en
- "main_scripts_tls_fingerprint_rationale_136": "Parse the negotiated version + cipher + extensions from a ServerHello." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L136 | neighbors=[parse_server_hello()] | lang=en
- "main_scripts_tls_fingerprint_rationale_137": "Parse the negotiated version + cipher + extensions from a ServerHello." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L137 | neighbors=[parse_server_hello()] | lang=en
- "main_scripts_tls_fingerprint_rationale_177": "2-char code from the cipher's position in CIPHER_LIST ('00' if unknown)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L177 | neighbors=[cipher_code()] | lang=en
- "main_scripts_tls_fingerprint_rationale_178": "2-char code from the cipher's position in CIPHER_LIST ('00' if unknown)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L178 | neighbors=[cipher_code()] | lang=en
- "main_scripts_tls_fingerprint_rationale_184": "Concatenate the ServerHello extension TYPE codes (2 bytes each). We hash types," | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L184 | neighbors=[_server_ext_types()] | lang=en
- "main_scripts_tls_fingerprint_rationale_185": "Concatenate the ServerHello extension TYPE codes (2 bytes each). We hash types," | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L185 | neighbors=[_server_ext_types()] | lang=en
- "main_scripts_tls_fingerprint_rationale_200": "JARM-shaped 62-char fuzzy hash: 3 chars per probe (cipher[2] + version[1])," | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L200 | neighbors=[jarm_style_digest()] | lang=it
- "main_scripts_tls_fingerprint_rationale_201": "JARM-shaped 62-char fuzzy hash: 3 chars per probe (cipher[2] + version[1])," | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L201 | neighbors=[jarm_style_digest()] | lang=it
- "main_scripts_tls_fingerprint_rationale_241": "Read exactly the first TLS record (the ServerHello or an alert) and stop —     n" | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L241 | neighbors=[_recv_first_record()] | lang=en
- "main_scripts_tls_fingerprint_rationale_242": "Read exactly the first TLS record (the ServerHello or an alert) and stop —     n" | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L242 | neighbors=[_recv_first_record()] | lang=en
- "main_scripts_tls_fingerprint_rationale_261": "Send one crafted ClientHello, read + parse the ServerHello. Sync." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L261 | neighbors=[_one_probe()] | lang=en
- "main_scripts_tls_fingerprint_rationale_262": "Send one crafted ClientHello, read + parse the ServerHello. Sync." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L262 | neighbors=[_one_probe()] | lang=en
- "main_scripts_tls_fingerprint_rationale_274": "Run all probes and return (62-char digest, per-probe results)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L274 | neighbors=[fingerprint_host()] | lang=en
- "main_scripts_tls_fingerprint_rationale_275": "Run all probes and return (62-char digest, per-probe results)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L275 | neighbors=[fingerprint_host()] | lang=en
- "main_scripts_tls_fingerprint_rationale_90": "Build a complete TLS ClientHello record (record layer + handshake)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L90 | neighbors=[build_client_hello()] | lang=pt
- "main_scripts_tls_fingerprint_rationale_91": "Build a complete TLS ClientHello record (record layer + handshake)." | kind=entity | source=probe/main_scripts/tls_fingerprint.py:L91 | neighbors=[build_client_hello()] | lang=pt
- "main_scripts_tls_fingerprint_tlsfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L285 | neighbors=[TLSFingerprintScanner] | lang=en
- "main_scripts_tls_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L287 | neighbors=[tls_scanner.py] | lang=en
- "main_scripts_tls_scanner_rationale_1": "tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):" | kind=entity | source=probe/main_scripts/tls_scanner.py:L1 | neighbors=[tls_scanner.py] | lang=en
- "main_scripts_tls_scanner_rationale_105": "Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl" | kind=entity | source=probe/main_scripts/tls_scanner.py:L105 | neighbors=[grade_tls_posture()] | lang=en
- "main_scripts_tls_scanner_rationale_147": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=probe/main_scripts/tls_scanner.py:L147 | neighbors=[_sni()] | lang=en
- "main_scripts_tls_scanner_rationale_156": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=probe/main_scripts/tls_scanner.py:L156 | neighbors=[_try_version()] | lang=pt
- "main_scripts_tls_scanner_rationale_61": "Flag the security-relevant properties of an OpenSSL cipher-suite name:     forwa" | kind=entity | source=probe/main_scripts/tls_scanner.py:L61 | neighbors=[classify_cipher()] | lang=en
- "main_scripts_tls_scanner_tlsscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L258 | neighbors=[TLSScanner] | lang=en
- "main_scripts_udp_scanner_dns_probe": "_dns_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L39 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L382 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_memcached_stats_probe": "_memcached_stats_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L73 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_netbios_probe": "_netbios_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L65 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_ntp_probe": "_ntp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L46 | neighbors=[udp_scanner.py] | lang=en
- "main_scripts_udp_scanner_rationale_1": "udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO" | kind=entity | source=probe/main_scripts/udp_scanner.py:L1 | neighbors=[udp_scanner.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-159.json

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
