# Node Description Batch 98 of 330

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

- "main_scripts_ftp_scanner_parse_pasv": "parse_pasv()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L44 | neighbors=[ftp_scanner.py, ._list_bounded(), Extract the passive data PORT from a 22…]
- "main_scripts_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "main_scripts_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "main_scripts_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "main_scripts_ipmi_scanner_build_open_session_request": "build_open_session_request()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L36 | neighbors=[ipmi_scanner.py, ._probe(), A fixed RMCP+ Open Session Request offe…]
- "main_scripts_ipmi_scanner_parse_open_session_response": "parse_open_session_response()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L52 | neighbors=[ipmi_scanner.py, ._probe(), Parse an RMCP+ Open Session Response; N…]
- "main_scripts_ipv6_discovery_is_ipv6": "_is_ipv6()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L34 | neighbors=[ipv6_discovery.py, parse_ip_neigh6(), parse_ndp()]
- "main_scripts_ipv6_discovery_own_ipv6_addresses": "_own_ipv6_addresses()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L80 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts(), Best-effort set of this host's own IPv6…]
- "main_scripts_ipv6_discovery_run": "_run()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L94 | neighbors=[ipv6_discovery.py, _ping_all_nodes(), _read_neighbor_cache()]
- "main_scripts_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…]
- "main_scripts_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()]
- "main_scripts_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-097.json

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
