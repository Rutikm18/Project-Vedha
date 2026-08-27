# Node Description Batch 43 of 236

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

- "main_scripts_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1171 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…]
- "main_scripts_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=probe/main_scripts/findings.py:L316 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()]
- "main_scripts_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=probe/main_scripts/findings.py:L665 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L752 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=probe/main_scripts/findings.py:L850 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=probe/main_scripts/findings.py:L627 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=probe/main_scripts/findings.py:L916 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=probe/main_scripts/findings.py:L715 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=probe/main_scripts/findings.py:L943 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L511 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=probe/main_scripts/findings.py:L781 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=probe/main_scripts/findings.py:L576 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L882 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L443 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L491 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/main_scripts/findings.py:L465 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=probe/main_scripts/findings.py:L819 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner()]
- "main_scripts_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L391 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target()]
- "main_scripts_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L445 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…, Surveys a target for IoT/embedded devic…]
- "main_scripts_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L271 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding., MQTT variable-length encoding.]
- "main_scripts_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L283 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…, MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "main_scripts_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…, Extract PTR target names from mDNS resp…]
- "main_scripts_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "main_scripts_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "main_scripts_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L270 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…]
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L329 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…]
- "main_scripts_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L94 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), _strip_ip_header(), Parse an ICMP reply. Handles both raw-s…, Parse an ICMP reply. Handles both raw-s…]
- "main_scripts_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…]
- "main_scripts_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), .__init__(), RuntimeError, All passive sources failed before the l…]
- "main_scripts_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L92 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "main_scripts_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L55 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log(), Run one scanner module as a subprocess,…]
- "main_scripts_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L768 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "main_scripts_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L131 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), One probe-ladder rung on its own connec…, One probe-ladder rung on its own connec…]
- "main_scripts_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L142 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "main_scripts_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "main_scripts_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community()]
- "main_scripts_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "main_scripts_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "main_scripts_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-042.json

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
