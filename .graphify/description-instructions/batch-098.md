# Node Description Batch 99 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()]
- "main_scripts_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…]
- "main_scripts_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …]
- "main_scripts_ldap_scanner_ldapscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/ldap_scanner.py:L54 | neighbors=[LDAPScanner, _first(), Blocking: anonymous bind + RootDSE read…]
- "main_scripts_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan()]
- "main_scripts_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…]
- "main_scripts_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "main_scripts_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L212 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "main_scripts_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "main_scripts_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "main_scripts_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "main_scripts_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "main_scripts_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "main_scripts_msrpc_scanner_extract_tcp_ports": "_extract_tcp_ports()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L51 | neighbors=[msrpc_scanner.py, Parse ncacn_ip_tcp bindings → (all_tcp_…, _summarize()]
- "main_scripts_msrpc_scanner_msrpcscanner_enumerate": "._enumerate()" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L89 | neighbors=[MSRPCScanner, _summarize(), Blocking: EPM ept_lookup via impacket. …]
- "main_scripts_nfs_scanner_is_world_readable": "is_world_readable()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L116 | neighbors=[nfs_scanner.py, parse_mount_export(), An export with no client restriction, o…]
- "main_scripts_nfs_scanner_nfsscanner_portmap_getport": "._portmap_getport()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L212 | neighbors=[NFSScanner, ._rpc(), ._probe()]
- "main_scripts_nfs_scanner_parse_rpc_reply": "_parse_rpc_reply()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L166 | neighbors=[nfs_scanner.py, Strip the ONC-RPC reply header; return …, _rpc_call()]
- "main_scripts_nfs_scanner_xdr_opaque": ".opaque()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L70 | neighbors=[_XDR, .u32(), .string()]
- "main_scripts_nfs_scanner_xdr_string": ".string()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L78 | neighbors=[parse_mount_export(), _XDR, .opaque()]
- "main_scripts_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L75 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …, Allow tuning only; target, script, and …]
- "main_scripts_os_fingerprint_accept_echo_reply": "accept_echo_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L137 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), True only for an ICMP ECHO reply that a…]
- "main_scripts_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L66 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]
- "main_scripts_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L70 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_timestamp()]
- "main_scripts_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L162 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()]
- "main_scripts_os_fingerprint_osfingerprintscanner_apply_smb_build": "._apply_smb_build()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L382 | neighbors=[OSFingerprintScanner, ._smb_build(), Fuse an SMB2 NTLM build into an OS resu…]
- "main_scripts_os_fingerprint_osfingerprintscanner_smb_build": "._smb_build()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L370 | neighbors=[OSFingerprintScanner, ._apply_smb_build(), Best-effort exact Windows build via SMB…]
- "main_scripts_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…]
- "main_scripts_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …]
- "main_scripts_port_scanner_harvest_tcp_stack": "_harvest_tcp_stack()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L94 | neighbors=[port_scanner.py, ._attempt(), Peer TCP-stack signals readable from a …]
- "main_scripts_port_scanner_portscanner_note_probe_outcome": "._note_probe_outcome()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L583 | neighbors=[PortScanner, ._scan_port(), Record one probe and answer: is the PAT…]
- "main_scripts_printer_scanner_parse_ipp_make_model": "parse_ipp_make_model()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L65 | neighbors=[printer_scanner.py, ._probe_ipp(), Best-effort extraction of printer-make-…]
- "main_scripts_printer_scanner_parse_pjl_id": "parse_pjl_id()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L38 | neighbors=[printer_scanner.py, ._probe_pjl(), Extract the model string from a PJL INF…]
- "main_scripts_printer_scanner_printerscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L135 | neighbors=[PrinterScanner, ._probe_ipp(), ._probe_pjl()]
- "main_scripts_printer_scanner_recv_bounded": "_recv_bounded()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L83 | neighbors=[printer_scanner.py, ._probe_ipp(), ._probe_pjl()]
- "main_scripts_rdp_scanner_posture_from_selected": "_posture_from_selected()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L76 | neighbors=[rdp_scanner.py, parse_connection_confirm(), Map an RDP selectedProtocol bitmask to …]
- "main_scripts_rdp_scanner_probe_rdp_posture": "probe_rdp_posture()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L110 | neighbors=[rdp_scanner.py, probe_rdp(), Two-probe RDP posture (MS-RDPBCGR 2.2.1…]
- "main_scripts_rsync_scanner_parse_modules": "parse_modules()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L37 | neighbors=[rsync_scanner.py, Parse the daemon's module listing into …, ._list_modules()]
- "main_scripts_run_all_advertised_dynamic_ports": "_advertised_dynamic_ports()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L98 | neighbors=[run_all.py, main(), EPM-advertised dynamic RPC ports from t…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-098.json

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
