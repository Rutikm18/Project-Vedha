# Node Description Batch 184 of 236

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

- "scanner_snmp_scanner_rationale_105": "Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]." | kind=entity | source=probe/scanner/snmp_scanner.py:L105 | neighbors=[_ber_parse()] | lang=en
- "scanner_snmp_scanner_rationale_127": "Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response" | kind=entity | source=probe/scanner/snmp_scanner.py:L127 | neighbors=[_parse_varbinds()] | lang=en
- "scanner_snmp_scanner_rationale_246": "Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli" | kind=entity | source=probe/scanner/snmp_scanner.py:L246 | neighbors=[SNMPScanner] | lang=en
- "scanner_snmp_scanner_rationale_278": "Return (community, sysdescr) for the first responding community, or None." | kind=entity | source=probe/scanner/snmp_scanner.py:L278 | neighbors=[._discover_community()] | lang=en
- "scanner_snmp_scanner_rationale_292": "GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]." | kind=entity | source=probe/scanner/snmp_scanner.py:L292 | neighbors=[._walk_subtree()] | lang=en
- "scanner_snmp_scanner_rationale_315": "One GETBULK request — measure response/request size ratio." | kind=entity | source=probe/scanner/snmp_scanner.py:L315 | neighbors=[._amplification_factor()] | lang=en
- "scanner_snmp_scanner_rationale_325": "Send a SNMPv3 Discover. Any reply = v3 agent present." | kind=entity | source=probe/scanner/snmp_scanner.py:L325 | neighbors=[._snmpv3_present()] | lang=pt
- "scanner_snmp_scanner_rationale_46": "Dotted-notation OID string → BER-encoded bytes." | kind=entity | source=probe/scanner/snmp_scanner.py:L46 | neighbors=[_encode_oid()] | lang=en
- "scanner_snmp_scanner_rationale_64": "BER-encoded OID bytes → dotted-notation string." | kind=entity | source=probe/scanner/snmp_scanner.py:L64 | neighbors=[_decode_oid()] | lang=en
- "scanner_snmp_scanner_rationale_79": "Human-readable SNMP value for common ASN.1/SNMP types." | kind=entity | source=probe/scanner/snmp_scanner.py:L79 | neighbors=[_decode_value()] | lang=en
- "scanner_snmp_scanner_snmpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L252 | neighbors=[SNMPScanner] | lang=en
- "scanner_ssh_collector_collect_over_ssh": "_collect_over_ssh()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L52 | neighbors=[ssh_collector.py] | lang=en
- "scanner_ssh_collector_main": "main()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L125 | neighbors=[ssh_collector.py] | lang=en
- "scanner_ssh_collector_rationale_1": "ssh_collector.py — credentialed (authenticated) inventory collection for Linux." | kind=entity | source=probe/scanner/ssh_collector.py:L1 | neighbors=[ssh_collector.py] | lang=en
- "scanner_ssh_collector_sshcollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L83 | neighbors=[SSHCollector] | lang=en
- "scanner_syn_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L465 | neighbors=[syn_scanner.py] | lang=en
- "scanner_syn_scanner_rationale_1": "syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH" | kind=entity | source=probe/scanner/syn_scanner.py:L1 | neighbors=[syn_scanner.py] | lang=en
- "scanner_syn_scanner_rationale_104": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=probe/scanner/syn_scanner.py:L104 | neighbors=[build_tcp_syn()] | lang=pt
- "scanner_syn_scanner_rationale_105": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=probe/scanner/syn_scanner.py:L105 | neighbors=[build_tcp_syn()] | lang=pt
- "scanner_syn_scanner_rationale_107": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket)." | kind=entity | source=probe/scanner/syn_scanner.py:L107 | neighbors=[parse_packet()] | lang=pt
- "scanner_syn_scanner_rationale_123": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/scanner/syn_scanner.py:L123 | neighbors=[classify()] | lang=en
- "scanner_syn_scanner_rationale_125": "Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked" | kind=entity | source=probe/scanner/syn_scanner.py:L125 | neighbors=[_parse_mss()] | lang=en
- "scanner_syn_scanner_rationale_126": "Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked" | kind=entity | source=probe/scanner/syn_scanner.py:L126 | neighbors=[_parse_mss()] | lang=en
- "scanner_syn_scanner_rationale_134": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/scanner/syn_scanner.py:L134 | neighbors=[syn_cookie()] | lang=en
- "scanner_syn_scanner_rationale_141": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/scanner/syn_scanner.py:L141 | neighbors=[verify_reply_cookie()] | lang=en
- "scanner_syn_scanner_rationale_151": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also" | kind=entity | source=probe/scanner/syn_scanner.py:L151 | neighbors=[parse_packet()] | lang=pt
- "scanner_syn_scanner_rationale_152": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also" | kind=entity | source=probe/scanner/syn_scanner.py:L152 | neighbors=[parse_packet()] | lang=pt
- "scanner_syn_scanner_rationale_154": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/scanner/syn_scanner.py:L154 | neighbors=[syn_scan_supported()] | lang=pt
- "scanner_syn_scanner_rationale_175": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=probe/scanner/syn_scanner.py:L175 | neighbors=[_local_source_ip()] | lang=en
- "scanner_syn_scanner_rationale_179": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/scanner/syn_scanner.py:L179 | neighbors=[classify()] | lang=en
- "scanner_syn_scanner_rationale_180": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/scanner/syn_scanner.py:L180 | neighbors=[classify()] | lang=en
- "scanner_syn_scanner_rationale_189": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/scanner/syn_scanner.py:L189 | neighbors=[SynScanner] | lang=en
- "scanner_syn_scanner_rationale_190": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/scanner/syn_scanner.py:L190 | neighbors=[syn_cookie()] | lang=en
- "scanner_syn_scanner_rationale_191": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/scanner/syn_scanner.py:L191 | neighbors=[syn_cookie()] | lang=en
- "scanner_syn_scanner_rationale_197": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/scanner/syn_scanner.py:L197 | neighbors=[verify_reply_cookie()] | lang=en
- "scanner_syn_scanner_rationale_198": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/scanner/syn_scanner.py:L198 | neighbors=[verify_reply_cookie()] | lang=en
- "scanner_syn_scanner_rationale_210": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/scanner/syn_scanner.py:L210 | neighbors=[syn_scan_supported()] | lang=pt
- "scanner_syn_scanner_rationale_211": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/scanner/syn_scanner.py:L211 | neighbors=[syn_scan_supported()] | lang=pt
- "scanner_syn_scanner_rationale_231": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=probe/scanner/syn_scanner.py:L231 | neighbors=[_local_source_ip()] | lang=en
- "scanner_syn_scanner_rationale_232": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=probe/scanner/syn_scanner.py:L232 | neighbors=[_local_source_ip()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-183.json

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
