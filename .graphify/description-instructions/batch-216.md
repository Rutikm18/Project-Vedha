# Node Description Batch 217 of 332

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

- "main_scripts_mcp_ai_scanner_rationale_162": "The strongest possible evidence for a real MCP server: a WWW-Authenticate     he" | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L162 | neighbors=[_mcp_oauth_signal()] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_174": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L174 | neighbors=[_auth_shaped_json_body()] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_175": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=probe/main_scripts/mcp_ai_scanner.py:L175 | neighbors=[_auth_shaped_json_body()] | lang=en
- "main_scripts_mcp_ai_scanner_request": "_request()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L128 | neighbors=[mcp_ai_scanner.py] | lang=en
- "main_scripts_mobile_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L340 | neighbors=[mobile_scanner.py] | lang=en
- "main_scripts_mobile_scanner_rationale_1": "mobile_scanner.py — mobile device exposure detection.  Covers playbook 13 (Mobil" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L1 | neighbors=[mobile_scanner.py] | lang=en
- "main_scripts_mobile_scanner_rationale_152": "Attempt TCP connect to lockdownd port 62078.     Port open = iOS device present" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L152 | neighbors=[_probe_lockdownd()] | lang=en
- "main_scripts_mobile_scanner_rationale_188": "Build a DNS PTR query in mDNS wire format with QU bit set." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L188 | neighbors=[_build_mdns_query()] | lang=en
- "main_scripts_mobile_scanner_rationale_199": "Extract PTR target names (service instance names) from mDNS reply." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L199 | neighbors=[_parse_mdns_ptr_names()] | lang=en
- "main_scripts_mobile_scanner_rationale_259": "Send one mDNS PTR query to target:5353 and return instance names." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L259 | neighbors=[_probe_mdns_mobile_sync()] | lang=en
- "main_scripts_mobile_scanner_rationale_279": "Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L279 | neighbors=[MobileScanner] | lang=en
- "main_scripts_mobile_scanner_rationale_60": "Build an ADB A_CNXN (CONNECT) message — the standard handshake initiator." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L60 | neighbors=[_build_adb_cnxn()] | lang=en
- "main_scripts_mobile_scanner_rationale_71": "Parse a 24-byte ADB message header.  Returns parsed fields or None." | kind=entity | source=probe/main_scripts/mobile_scanner.py:L71 | neighbors=[_parse_adb_header()] | lang=pt
- "main_scripts_mobile_scanner_rationale_96": "Send ADB CNXN and read the device's CNXN reply.     Returns a dict with connecti" | kind=entity | source=probe/main_scripts/mobile_scanner.py:L96 | neighbors=[_probe_adb()] | lang=en
- "main_scripts_msrpc_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L172 | neighbors=[msrpc_scanner.py] | lang=en
- "main_scripts_msrpc_scanner_msrpcscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L85 | neighbors=[MSRPCScanner] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-216.json

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
