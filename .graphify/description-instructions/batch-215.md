# Node Description Batch 216 of 330

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

- "main_scripts_msrpc_scanner_rationale_1": "msrpc_scanner.py — MSRPC endpoint-mapper (EPM) enumeration over port 135 (VA che" | kind=entity | source=probe/main_scripts/msrpc_scanner.py:L1 | neighbors=[msrpc_scanner.py] | lang=it
- "main_scripts_msrpc_scanner_rationale_52": "Parse ncacn_ip_tcp bindings → (all_tcp_ports, dynamic_tcp_ports).      Pure and" | kind=entity | source=probe/main_scripts/msrpc_scanner.py:L52 | neighbors=[_extract_tcp_ports()] | lang=en
- "main_scripts_msrpc_scanner_rationale_70": "Reduce the raw endpoint list to distinct interfaces and dynamic ports." | kind=entity | source=probe/main_scripts/msrpc_scanner.py:L70 | neighbors=[_summarize()] | lang=en
- "main_scripts_msrpc_scanner_rationale_90": "Blocking: EPM ept_lookup via impacket. Monkeypatchable for tests." | kind=entity | source=probe/main_scripts/msrpc_scanner.py:L90 | neighbors=[._enumerate()] | lang=en
- "main_scripts_nfs_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L282 | neighbors=[nfs_scanner.py] | lang=en
- "main_scripts_nfs_scanner_nfsscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L190 | neighbors=[NFSScanner] | lang=en
- "main_scripts_nfs_scanner_rationale_1": "nfs_scanner.py — NFS export exposure over ONC RPC (VA checklist: anonymous netwo" | kind=entity | source=probe/main_scripts/nfs_scanner.py:L1 | neighbors=[nfs_scanner.py] | lang=en
- "main_scripts_nfs_scanner_rationale_117": "An export with no client restriction, or one shared to a wildcard group,     is" | kind=entity | source=probe/main_scripts/nfs_scanner.py:L117 | neighbors=[is_world_readable()] | lang=en
- "main_scripts_nfs_scanner_rationale_126": "Send one ONC-RPC CALL (AUTH_NULL) over a TCP record-marked stream and     return" | kind=entity | source=probe/main_scripts/nfs_scanner.py:L126 | neighbors=[_rpc_call()] | lang=en
- "main_scripts_nfs_scanner_rationale_137": "Read RPC record-marking fragments (RFC 1057 §10) until the last fragment." | kind=entity | source=probe/main_scripts/nfs_scanner.py:L137 | neighbors=[_recv_record()] | lang=en
- "main_scripts_nfs_scanner_rationale_167": "Strip the ONC-RPC reply header; return the accepted-SUCCESS result bytes." | kind=entity | source=probe/main_scripts/nfs_scanner.py:L167 | neighbors=[_parse_rpc_reply()] | lang=en
- "main_scripts_nfs_scanner_rationale_233": "Blocking: portmap DUMP + mountd EXPORT. Monkeypatchable for tests." | kind=entity | source=probe/main_scripts/nfs_scanner.py:L233 | neighbors=[._probe()] | lang=en
- "main_scripts_nfs_scanner_rationale_57": "Minimal, BOUNDED big-endian XDR reader (RFC 4506)." | kind=entity | source=probe/main_scripts/nfs_scanner.py:L57 | neighbors=[_XDR] | lang=en
- "main_scripts_nfs_scanner_rationale_83": "Parse a PMAPPROC_DUMP reply — the list of registered RPC programs." | kind=entity | source=probe/main_scripts/nfs_scanner.py:L83 | neighbors=[parse_portmap_dump()] | lang=en
- "main_scripts_nfs_scanner_rationale_97": "Parse a MOUNTPROC_EXPORT reply — exports + their allowed client groups." | kind=entity | source=probe/main_scripts/nfs_scanner.py:L97 | neighbors=[parse_mount_export()] | lang=pt
- "main_scripts_nfs_scanner_xdr_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L59 | neighbors=[_XDR] | lang=en
- "main_scripts_nmap_wrapper_have_nmap": "_have_nmap()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L117 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_main": "main()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L253 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_nmapexecutionerror_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L51 | neighbors=[NmapExecutionError] | lang=en
- "main_scripts_nmap_wrapper_rationale_1": "nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.  WHY:" | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_rationale_183": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L183 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_rationale_191": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L191 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_rationale_197": "# NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree" | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L197 | neighbors=[nmap_wrapper.py] | lang=en
- "main_scripts_nmap_wrapper_rationale_43": "Actionable subprocess failure; never reinterpret it as zero findings." | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L43 | neighbors=[NmapExecutionError] | lang=en
- "main_scripts_nmap_wrapper_rationale_49": "Actionable subprocess failure; never reinterpret it as zero findings." | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L49 | neighbors=[NmapExecutionError] | lang=en
- "main_scripts_nmap_wrapper_rationale_70": "Allow tuning only; target, script, and output controls stay owned here." | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L70 | neighbors=[_validated_extra_args()] | lang=en
- "main_scripts_nmap_wrapper_rationale_76": "Allow tuning only; target, script, and output controls stay owned here." | kind=entity | source=probe/main_scripts/nmap_wrapper.py:L76 | neighbors=[_validated_extra_args()] | lang=en
- "main_scripts_os_fingerprint_main": "main()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L571 | neighbors=[os_fingerprint.py] | lang=en
- "main_scripts_os_fingerprint_osfingerprintscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L360 | neighbors=[OSFingerprintScanner] | lang=en
- "main_scripts_os_fingerprint_rationale_1": "os_fingerprint.py — OS/stack fingerprinting via ICMP + TTL (Tier 2.1 + 2.2).  TW" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L1 | neighbors=[os_fingerprint.py] | lang=pt
- "main_scripts_os_fingerprint_rationale_102": "Round the observed TTL up to the nearest standard initial TTL." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L102 | neighbors=[infer_initial_ttl()] | lang=en
- "main_scripts_os_fingerprint_rationale_109": "Parse an ICMP timestamp reply (type 14): id/seq/ttl plus the three 32-bit     ti" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L109 | neighbors=[parse_icmp_timestamps()] | lang=en
- "main_scripts_os_fingerprint_rationale_122": "Interpret a timestamp reply's transmit value. Per RFC 792 a *standard* value" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L122 | neighbors=[remote_clock()] | lang=pt
- "main_scripts_os_fingerprint_rationale_129": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L129 | neighbors=[fingerprint_os()] | lang=pt
- "main_scripts_os_fingerprint_rationale_138": "True only for an ICMP ECHO reply that actually came FROM the probed host.      A" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L138 | neighbors=[accept_echo_reply()] | lang=en
- "main_scripts_os_fingerprint_rationale_153": "Round the observed TTL up to the nearest standard initial TTL." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L153 | neighbors=[infer_initial_ttl()] | lang=en
- "main_scripts_os_fingerprint_rationale_180": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L180 | neighbors=[fingerprint_os()] | lang=pt
- "main_scripts_os_fingerprint_rationale_188": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=probe/main_scripts/os_fingerprint.py:L188 | neighbors=[icmp_supported()] | lang=en
- "main_scripts_os_fingerprint_rationale_221": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L221 | neighbors=[OSFingerprintScanner] | lang=en
- "main_scripts_os_fingerprint_rationale_227": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L227 | neighbors=[fingerprint_os()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-215.json

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
