# Node Description Batch 68 of 92

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

- "scanner_syn_scanner_rationale_232": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=scanner/syn_scanner.py:L232 | neighbors=[_local_source_ip()] | lang=en
- "scanner_syn_scanner_rationale_246": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=scanner/syn_scanner.py:L246 | neighbors=[SynScanner] | lang=en
- "scanner_syn_scanner_rationale_418": "Turn resolved port states + harvested intel into ScanResults. Pure —         no" | kind=entity | source=scanner/syn_scanner.py:L418 | neighbors=[._build_results()] | lang=en
- "scanner_syn_scanner_rationale_82": "Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma" | kind=entity | source=scanner/syn_scanner.py:L82 | neighbors=[build_ip_header()] | lang=pt
- "scanner_tls_fingerprint_main": "main()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L320 | neighbors=[tls_fingerprint.py] | lang=en
- "scanner_tls_fingerprint_rationale_1": "tls_fingerprint.py — active TLS server fingerprint (Tier 2.3, JARM methodology)." | kind=entity | source=scanner/tls_fingerprint.py:L1 | neighbors=[tls_fingerprint.py] | lang=en
- "scanner_tls_fingerprint_rationale_137": "Parse the negotiated version + cipher + extensions from a ServerHello." | kind=entity | source=scanner/tls_fingerprint.py:L137 | neighbors=[parse_server_hello()] | lang=en
- "scanner_tls_fingerprint_rationale_178": "2-char code from the cipher's position in CIPHER_LIST ('00' if unknown)." | kind=entity | source=scanner/tls_fingerprint.py:L178 | neighbors=[cipher_code()] | lang=en
- "scanner_tls_fingerprint_rationale_185": "Concatenate the ServerHello extension TYPE codes (2 bytes each). We hash types," | kind=entity | source=scanner/tls_fingerprint.py:L185 | neighbors=[_server_ext_types()] | lang=en
- "scanner_tls_fingerprint_rationale_201": "JARM-shaped 62-char fuzzy hash: 3 chars per probe (cipher[2] + version[1])," | kind=entity | source=scanner/tls_fingerprint.py:L201 | neighbors=[jarm_style_digest()] | lang=it
- "scanner_tls_fingerprint_rationale_242": "Read exactly the first TLS record (the ServerHello or an alert) and stop —     n" | kind=entity | source=scanner/tls_fingerprint.py:L242 | neighbors=[_recv_first_record()] | lang=en
- "scanner_tls_fingerprint_rationale_262": "Send one crafted ClientHello, read + parse the ServerHello. Sync." | kind=entity | source=scanner/tls_fingerprint.py:L262 | neighbors=[_one_probe()] | lang=en
- "scanner_tls_fingerprint_rationale_275": "Run all probes and return (62-char digest, per-probe results)." | kind=entity | source=scanner/tls_fingerprint.py:L275 | neighbors=[fingerprint_host()] | lang=en
- "scanner_tls_fingerprint_rationale_91": "Build a complete TLS ClientHello record (record layer + handshake)." | kind=entity | source=scanner/tls_fingerprint.py:L91 | neighbors=[build_client_hello()] | lang=pt
- "scanner_tls_fingerprint_tlsfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L285 | neighbors=[TLSFingerprintScanner] | lang=en
- "scanner_tls_scanner_main": "main()" | kind=code-symbol | source=scanner/tls_scanner.py:L304 | neighbors=[tls_scanner.py] | lang=en
- "scanner_tls_scanner_rationale_1": "tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):" | kind=entity | source=scanner/tls_scanner.py:L1 | neighbors=[tls_scanner.py] | lang=en
- "scanner_tls_scanner_rationale_105": "Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl" | kind=entity | source=scanner/tls_scanner.py:L105 | neighbors=[grade_tls_posture()] | lang=en
- "scanner_tls_scanner_rationale_147": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=scanner/tls_scanner.py:L147 | neighbors=[_sni()] | lang=en
- "scanner_tls_scanner_rationale_156": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=scanner/tls_scanner.py:L156 | neighbors=[_try_version()] | lang=pt
- "scanner_tls_scanner_rationale_61": "Flag the security-relevant properties of an OpenSSL cipher-suite name:     forwa" | kind=entity | source=scanner/tls_scanner.py:L61 | neighbors=[classify_cipher()] | lang=en
- "scanner_tls_scanner_tlsscanner_init": ".__init__()" | kind=code-symbol | source=scanner/tls_scanner.py:L275 | neighbors=[TLSScanner] | lang=en
- "scanner_udp_scanner_dns_probe": "_dns_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L39 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_main": "main()" | kind=code-symbol | source=scanner/udp_scanner.py:L382 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_memcached_stats_probe": "_memcached_stats_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L73 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_netbios_probe": "_netbios_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L65 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_ntp_probe": "_ntp_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L46 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_rationale_1": "udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO" | kind=entity | source=scanner/udp_scanner.py:L1 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_rationale_114": "SIP OPTIONS request — safe fingerprint method." | kind=entity | source=scanner/udp_scanner.py:L114 | neighbors=[_sip_probe()] | lang=en
- "scanner_udp_scanner_rationale_133": "TFTP RRQ for a non-existent file.  Error reply confirms TFTP service." | kind=entity | source=scanner/udp_scanner.py:L133 | neighbors=[_tftp_probe()] | lang=en
- "scanner_udp_scanner_rationale_140": "RMCP Ping (ASF Presence Ping) to detect IPMI/BMC." | kind=entity | source=scanner/udp_scanner.py:L140 | neighbors=[_ipmi_probe()] | lang=en
- "scanner_udp_scanner_rationale_147": "UPnP/SSDP M-SEARCH — unicast to target:1900." | kind=entity | source=scanner/udp_scanner.py:L147 | neighbors=[_ssdp_probe()] | lang=en
- "scanner_udp_scanner_rationale_159": "mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)." | kind=entity | source=scanner/udp_scanner.py:L159 | neighbors=[_mdns_probe()] | lang=en
- "scanner_udp_scanner_rationale_189": "Parse IKEv1 or IKEv2 response header." | kind=entity | source=scanner/udp_scanner.py:L189 | neighbors=[interpret_ike()] | lang=en
- "scanner_udp_scanner_rationale_205": "Extract SIP version + server header from a SIP response." | kind=entity | source=scanner/udp_scanner.py:L205 | neighbors=[interpret_sip()] | lang=en
- "scanner_udp_scanner_rationale_220": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=scanner/udp_scanner.py:L220 | neighbors=[interpret_ipmi()] | lang=en
- "scanner_udp_scanner_rationale_233": "Extract Location and Server from SSDP response." | kind=entity | source=scanner/udp_scanner.py:L233 | neighbors=[interpret_ssdp()] | lang=en
- "scanner_udp_scanner_rationale_248": "Return byte count and check QR bit (1 = response)." | kind=entity | source=scanner/udp_scanner.py:L248 | neighbors=[interpret_mdns()] | lang=en
- "scanner_udp_scanner_rationale_291": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=scanner/udp_scanner.py:L291 | neighbors=[._gated_probe()] | lang=en
- "scanner_udp_scanner_rationale_78": "Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-" | kind=entity | source=scanner/udp_scanner.py:L78 | neighbors=[_ike_probe()] | lang=fr

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-067.json

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
