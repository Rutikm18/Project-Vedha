# Node Description Batch 258 of 332

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

- "scanner_tls_fingerprint_tlsfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L286 | neighbors=[TLSFingerprintScanner] | lang=en
- "scanner_tls_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L345 | neighbors=[tls_scanner.py] | lang=en
- "scanner_tls_scanner_rationale_1": "tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):" | kind=entity | source=probe/scanner/tls_scanner.py:L1 | neighbors=[tls_scanner.py] | lang=en
- "scanner_tls_scanner_rationale_104": "Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl" | kind=entity | source=probe/scanner/tls_scanner.py:L104 | neighbors=[grade_tls_posture()] | lang=en
- "scanner_tls_scanner_rationale_105": "Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl" | kind=entity | source=probe/scanner/tls_scanner.py:L105 | neighbors=[grade_tls_posture()] | lang=en
- "scanner_tls_scanner_rationale_146": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=probe/scanner/tls_scanner.py:L146 | neighbors=[_sni()] | lang=en
- "scanner_tls_scanner_rationale_147": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=probe/scanner/tls_scanner.py:L147 | neighbors=[_sni()] | lang=en
- "scanner_tls_scanner_rationale_155": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=probe/scanner/tls_scanner.py:L155 | neighbors=[_try_version()] | lang=pt
- "scanner_tls_scanner_rationale_156": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=probe/scanner/tls_scanner.py:L156 | neighbors=[_try_version()] | lang=pt
- "scanner_tls_scanner_rationale_166": "Attempt a handshake forcing one protocol version.      Returns a cipher dict whe" | kind=entity | source=probe/scanner/tls_scanner.py:L166 | neighbors=[_try_version()] | lang=pt
- "scanner_tls_scanner_rationale_57": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=probe/scanner/tls_scanner.py:L57 | neighbors=[_sni()] | lang=en
- "scanner_tls_scanner_rationale_60": "Flag the security-relevant properties of an OpenSSL cipher-suite name:     forwa" | kind=entity | source=probe/scanner/tls_scanner.py:L60 | neighbors=[classify_cipher()] | lang=en
- "scanner_tls_scanner_rationale_61": "Flag the security-relevant properties of an OpenSSL cipher-suite name:     forwa" | kind=entity | source=probe/scanner/tls_scanner.py:L61 | neighbors=[classify_cipher()] | lang=en
- "scanner_tls_scanner_rationale_66": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=probe/scanner/tls_scanner.py:L66 | neighbors=[_try_version()] | lang=pt
- "scanner_tls_scanner_tlsscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L316 | neighbors=[TLSScanner] | lang=en
- "scanner_udp_scanner_dns_probe": "_dns_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L39 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L392 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_memcached_stats_probe": "_memcached_stats_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L73 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_netbios_probe": "_netbios_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L65 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_ntp_probe": "_ntp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L46 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_rationale_1": "udp_scanner.py — detect common UDP services via protocol-specific probes.  METHO" | kind=entity | source=probe/scanner/udp_scanner.py:L1 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_rationale_114": "SIP OPTIONS request — safe fingerprint method." | kind=entity | source=probe/scanner/udp_scanner.py:L114 | neighbors=[_sip_probe()] | lang=en
- "scanner_udp_scanner_rationale_133": "TFTP RRQ for a non-existent file.  Error reply confirms TFTP service." | kind=entity | source=probe/scanner/udp_scanner.py:L133 | neighbors=[_tftp_probe()] | lang=en
- "scanner_udp_scanner_rationale_139": "RMCP Ping (ASF Presence Ping) to detect IPMI/BMC." | kind=entity | source=probe/scanner/udp_scanner.py:L139 | neighbors=[_ipmi_probe()] | lang=en
- "scanner_udp_scanner_rationale_140": "RMCP Ping (ASF Presence Ping) to detect IPMI/BMC." | kind=entity | source=probe/scanner/udp_scanner.py:L140 | neighbors=[_ipmi_probe()] | lang=en
- "scanner_udp_scanner_rationale_146": "UPnP/SSDP M-SEARCH — unicast to target:1900." | kind=entity | source=probe/scanner/udp_scanner.py:L146 | neighbors=[_ssdp_probe()] | lang=en
- "scanner_udp_scanner_rationale_147": "UPnP/SSDP M-SEARCH — unicast to target:1900." | kind=entity | source=probe/scanner/udp_scanner.py:L147 | neighbors=[_ssdp_probe()] | lang=en
- "scanner_udp_scanner_rationale_158": "mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)." | kind=entity | source=probe/scanner/udp_scanner.py:L158 | neighbors=[_mdns_probe()] | lang=en
- "scanner_udp_scanner_rationale_159": "mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)." | kind=entity | source=probe/scanner/udp_scanner.py:L159 | neighbors=[_mdns_probe()] | lang=en
- "scanner_udp_scanner_rationale_188": "Parse IKEv1 or IKEv2 response header." | kind=entity | source=probe/scanner/udp_scanner.py:L188 | neighbors=[interpret_ike()] | lang=en
- "scanner_udp_scanner_rationale_189": "Parse IKEv1 or IKEv2 response header." | kind=entity | source=probe/scanner/udp_scanner.py:L189 | neighbors=[interpret_ike()] | lang=en
- "scanner_udp_scanner_rationale_204": "Extract SIP version + server header from a SIP response." | kind=entity | source=probe/scanner/udp_scanner.py:L204 | neighbors=[interpret_sip()] | lang=en
- "scanner_udp_scanner_rationale_205": "Extract SIP version + server header from a SIP response." | kind=entity | source=probe/scanner/udp_scanner.py:L205 | neighbors=[interpret_sip()] | lang=en
- "scanner_udp_scanner_rationale_219": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=probe/scanner/udp_scanner.py:L219 | neighbors=[interpret_ipmi()] | lang=en
- "scanner_udp_scanner_rationale_220": "Parse RMCP Pong; extract supported entities and IPMI capabilities." | kind=entity | source=probe/scanner/udp_scanner.py:L220 | neighbors=[interpret_ipmi()] | lang=en
- "scanner_udp_scanner_rationale_232": "Extract Location and Server from SSDP response." | kind=entity | source=probe/scanner/udp_scanner.py:L232 | neighbors=[interpret_ssdp()] | lang=en
- "scanner_udp_scanner_rationale_233": "Extract Location and Server from SSDP response." | kind=entity | source=probe/scanner/udp_scanner.py:L233 | neighbors=[interpret_ssdp()] | lang=en
- "scanner_udp_scanner_rationale_247": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/scanner/udp_scanner.py:L247 | neighbors=[interpret_mdns()] | lang=en
- "scanner_udp_scanner_rationale_248": "Return byte count and check QR bit (1 = response)." | kind=entity | source=probe/scanner/udp_scanner.py:L248 | neighbors=[interpret_mdns()] | lang=en
- "scanner_udp_scanner_rationale_290": "Acquire the concurrency gate (adaptive window or fixed semaphore),         run t" | kind=entity | source=probe/scanner/udp_scanner.py:L290 | neighbors=[._gated_probe()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-257.json

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
