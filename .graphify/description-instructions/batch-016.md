# Node Description Batch 17 of 92

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

- "main_scripts_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L178 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …] | lang=en
- "main_scripts_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…] | lang=en
- "main_scripts_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), os_family_from_ttl(), Round the observed TTL up to the neares…] | lang=en
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L329 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…] | lang=en
- "main_scripts_os_fingerprint_rationale_1": "os_fingerprint.py — OS/stack fingerprinting via ICMP + TTL (Tier 2.1 + 2.2).  TW" | kind=entity | source=main_scripts/os_fingerprint.py:L1 | neighbors=[os_fingerprint.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_os_fingerprint_rationale_109": "Parse an ICMP timestamp reply (type 14): id/seq/ttl plus the three 32-bit     ti" | kind=entity | source=main_scripts/os_fingerprint.py:L109 | neighbors=[parse_icmp_timestamps(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_122": "Interpret a timestamp reply's transmit value. Per RFC 792 a *standard* value" | kind=entity | source=main_scripts/os_fingerprint.py:L122 | neighbors=[remote_clock(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_os_fingerprint_rationale_138": "True only for an ICMP ECHO reply that actually came FROM the probed host.      A" | kind=entity | source=main_scripts/os_fingerprint.py:L138 | neighbors=[accept_echo_reply(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_153": "Round the observed TTL up to the nearest standard initial TTL." | kind=entity | source=main_scripts/os_fingerprint.py:L153 | neighbors=[infer_initial_ttl(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_180": "Combine available stack signals into a best-guess OS family with a calibrated" | kind=entity | source=main_scripts/os_fingerprint.py:L180 | neighbors=[fingerprint_os(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_os_fingerprint_rationale_254": "True if we can open an ICMP socket (datagram-ICMP or raw)." | kind=entity | source=main_scripts/os_fingerprint.py:L254 | neighbors=[icmp_supported(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_271": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=main_scripts/os_fingerprint.py:L271 | neighbors=[_open_icmp_socket(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_287": "ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP" | kind=entity | source=main_scripts/os_fingerprint.py:L287 | neighbors=[OSFingerprintScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_299": "Send one ICMP echo; return observed TTL, None (no TTL), or \"down\"." | kind=entity | source=main_scripts/os_fingerprint.py:L299 | neighbors=[._icmp_echo_ttl(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_330": "Send an ICMP timestamp request (type 13); return {ttl, transmit} from a" | kind=entity | source=main_scripts/os_fingerprint.py:L330 | neighbors=[._icmp_timestamp(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_60": "Build an ICMP message (header + rest) with a valid checksum." | kind=entity | source=main_scripts/os_fingerprint.py:L60 | neighbors=[_icmp(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_82": "Return (ttl, icmp_bytes). Raw-socket delivery prepends the full IPv4 header" | kind=entity | source=main_scripts/os_fingerprint.py:L82 | neighbors=[_strip_ip_header(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_os_fingerprint_rationale_95": "Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header     pres" | kind=entity | source=main_scripts/os_fingerprint.py:L95 | neighbors=[parse_icmp_reply(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=main_scripts/port_scanner.py:L324 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…] | lang=en
- "main_scripts_rdp_scanner_rationale_44": "TPKT + X.224 Connection Request carrying an RDP Negotiation Request." | kind=entity | source=main_scripts/rdp_scanner.py:L44 | neighbors=[build_connection_request(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_rdp_scanner_rationale_56": "Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.     the" | kind=entity | source=main_scripts/rdp_scanner.py:L56 | neighbors=[parse_connection_confirm(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_rdp_scanner_rationale_84": "One synchronous RDP handshake. Best-effort; None on any failure." | kind=entity | source=main_scripts/rdp_scanner.py:L84 | neighbors=[probe_rdp(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=main_scripts/scanner_base.py:L596 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…] | lang=en
- "main_scripts_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=main_scripts/scanner_base.py:L768 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()] | lang=en
- "main_scripts_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=main_scripts/service_banner.py:L1 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, service_banner.py] | lang=en
- "main_scripts_service_banner_rationale_133": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=main_scripts/service_banner.py:L133 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, ._rung()] | lang=en
- "main_scripts_service_banner_rationale_92": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=main_scripts/service_banner.py:L92 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, match_service()] | lang=en
- "main_scripts_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=main_scripts/service_enum.py:L104 | neighbors=[service_enum.py, BaseScanner, ScanResult, Everything learned about one target bey…, .scan_target()] | lang=en
- "main_scripts_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=main_scripts/smb_scanner.py:L1 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, smb_scanner.py] | lang=en
- "main_scripts_smb_scanner_rationale_37": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=main_scripts/smb_scanner.py:L37 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, parse_smb2_security_mode()] | lang=en
- "main_scripts_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()] | lang=en
- "main_scripts_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community()] | lang=en
- "main_scripts_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()] | lang=en
- "main_scripts_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()] | lang=en
- "main_scripts_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()] | lang=en
- "main_scripts_snmp_scanner_rationale_1": "snmp_scanner.py — full SNMP enumeration: community discovery, targeted MIB walk," | kind=entity | source=main_scripts/snmp_scanner.py:L1 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, snmp_scanner.py] | lang=en
- "main_scripts_snmp_scanner_rationale_105": "Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]." | kind=entity | source=main_scripts/snmp_scanner.py:L105 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _ber_parse()] | lang=en
- "main_scripts_snmp_scanner_rationale_127": "Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response" | kind=entity | source=main_scripts/snmp_scanner.py:L127 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _parse_varbinds()] | lang=en
- "main_scripts_snmp_scanner_rationale_246": "Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli" | kind=entity | source=main_scripts/snmp_scanner.py:L246 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, SNMPScanner] | lang=en
- "main_scripts_snmp_scanner_rationale_278": "Return (community, sysdescr) for the first responding community, or None." | kind=entity | source=main_scripts/snmp_scanner.py:L278 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, ._discover_community()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-016.json

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
