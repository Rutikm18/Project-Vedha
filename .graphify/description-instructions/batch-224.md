# Node Description Batch 225 of 330

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

- "main_scripts_ssh_scanner_rationale_47": "Parse an SSH identification string 'SSH-<proto>-<software>[ comments]'.      Ret" | kind=entity | source=probe/main_scripts/ssh_scanner.py:L47 | neighbors=[parse_ssh_banner()] | lang=en
- "main_scripts_ssh_scanner_sshscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L245 | neighbors=[SSHScanner] | lang=en
- "main_scripts_syn_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L595 | neighbors=[syn_scanner.py] | lang=en
- "main_scripts_syn_scanner_rationale_1": "syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).  WH" | kind=entity | source=probe/main_scripts/syn_scanner.py:L1 | neighbors=[syn_scanner.py] | lang=en
- "main_scripts_syn_scanner_rationale_104": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L104 | neighbors=[build_tcp_syn()] | lang=pt
- "main_scripts_syn_scanner_rationale_105": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L105 | neighbors=[build_tcp_syn()] | lang=pt
- "main_scripts_syn_scanner_rationale_107": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L107 | neighbors=[parse_packet()] | lang=pt
- "main_scripts_syn_scanner_rationale_117": "Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L117 | neighbors=[build_tcp_syn()] | lang=pt
- "main_scripts_syn_scanner_rationale_123": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L123 | neighbors=[classify()] | lang=en
- "main_scripts_syn_scanner_rationale_125": "Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked" | kind=entity | source=probe/main_scripts/syn_scanner.py:L125 | neighbors=[_parse_mss()] | lang=en
- "main_scripts_syn_scanner_rationale_126": "Walk a TCP options field for the MSS value (kind 2, len 4).      Bounds-checked" | kind=entity | source=probe/main_scripts/syn_scanner.py:L126 | neighbors=[_parse_mss()] | lang=en
- "main_scripts_syn_scanner_rationale_134": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/main_scripts/syn_scanner.py:L134 | neighbors=[syn_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_138": "Walk a TCP options field into a p0f-style profile.      Returns {mss, wscale, sa" | kind=entity | source=probe/main_scripts/syn_scanner.py:L138 | neighbors=[parse_tcp_options()] | lang=pt
- "main_scripts_syn_scanner_rationale_141": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/main_scripts/syn_scanner.py:L141 | neighbors=[verify_reply_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_151": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also" | kind=entity | source=probe/main_scripts/syn_scanner.py:L151 | neighbors=[parse_packet()] | lang=pt
- "main_scripts_syn_scanner_rationale_152": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also" | kind=entity | source=probe/main_scripts/syn_scanner.py:L152 | neighbors=[parse_packet()] | lang=pt
- "main_scripts_syn_scanner_rationale_154": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/main_scripts/syn_scanner.py:L154 | neighbors=[syn_scan_supported()] | lang=pt
- "main_scripts_syn_scanner_rationale_175": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L175 | neighbors=[_local_source_ip()] | lang=en
- "main_scripts_syn_scanner_rationale_177": "Back-compat shim: MSS only. New code uses parse_tcp_options()." | kind=entity | source=probe/main_scripts/syn_scanner.py:L177 | neighbors=[_parse_mss()] | lang=en
- "main_scripts_syn_scanner_rationale_179": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L179 | neighbors=[classify()] | lang=en
- "main_scripts_syn_scanner_rationale_180": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L180 | neighbors=[classify()] | lang=en
- "main_scripts_syn_scanner_rationale_182": "Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).      Also" | kind=entity | source=probe/main_scripts/syn_scanner.py:L182 | neighbors=[parse_packet()] | lang=pt
- "main_scripts_syn_scanner_rationale_189": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/main_scripts/syn_scanner.py:L189 | neighbors=[SynScanner] | lang=en
- "main_scripts_syn_scanner_rationale_190": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/main_scripts/syn_scanner.py:L190 | neighbors=[syn_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_191": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/main_scripts/syn_scanner.py:L191 | neighbors=[syn_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_197": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/main_scripts/syn_scanner.py:L197 | neighbors=[verify_reply_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_198": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/main_scripts/syn_scanner.py:L198 | neighbors=[verify_reply_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_210": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/main_scripts/syn_scanner.py:L210 | neighbors=[syn_scan_supported()] | lang=pt
- "main_scripts_syn_scanner_rationale_211": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/main_scripts/syn_scanner.py:L211 | neighbors=[syn_scan_supported()] | lang=pt
- "main_scripts_syn_scanner_rationale_214": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L214 | neighbors=[classify()] | lang=en
- "main_scripts_syn_scanner_rationale_225": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=probe/main_scripts/syn_scanner.py:L225 | neighbors=[syn_cookie()] | lang=en
- "main_scripts_syn_scanner_rationale_231": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L231 | neighbors=[_local_source_ip()] | lang=en
- "main_scripts_syn_scanner_rationale_244": "Block until `sock` has a packet waiting, or `timeout` seconds elapse.     Return" | kind=entity | source=probe/main_scripts/syn_scanner.py:L244 | neighbors=[_wait_readable()] | lang=pt
- "main_scripts_syn_scanner_rationale_245": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/main_scripts/syn_scanner.py:L245 | neighbors=[SynScanner] | lang=en
- "main_scripts_syn_scanner_rationale_246": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/main_scripts/syn_scanner.py:L246 | neighbors=[SynScanner] | lang=en
- "main_scripts_syn_scanner_rationale_275": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=probe/main_scripts/syn_scanner.py:L275 | neighbors=[syn_scan_supported()] | lang=pt
- "main_scripts_syn_scanner_rationale_296": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=probe/main_scripts/syn_scanner.py:L296 | neighbors=[_local_source_ip()] | lang=en
- "main_scripts_syn_scanner_rationale_310": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=probe/main_scripts/syn_scanner.py:L310 | neighbors=[SynScanner] | lang=en
- "main_scripts_syn_scanner_rationale_414": "Turn resolved port states + harvested intel into ScanResults. Pure —         no" | kind=entity | source=probe/main_scripts/syn_scanner.py:L414 | neighbors=[._build_results()] | lang=en
- "main_scripts_syn_scanner_rationale_418": "Turn resolved port states + harvested intel into ScanResults. Pure —         no" | kind=entity | source=probe/main_scripts/syn_scanner.py:L418 | neighbors=[._build_results()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-224.json

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
