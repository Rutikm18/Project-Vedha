# Node Description Batch 110 of 380

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

- "main_scripts_accuracy_gate_main": "_main()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L204 | neighbors=[accuracy_gate.py, format_gate_report(), run_gate()]
- "main_scripts_accuracy_main": "_main()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "main_scripts_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "main_scripts_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "main_scripts_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "main_scripts_cpe_extract_version": "_extract_version()" | kind=code-symbol | source=probe/main_scripts/cpe.py:L103 | neighbors=[cpe.py, Prefer an explicit version field; else …, to_cpe()]
- "main_scripts_cpe_to_cpe": "to_cpe()" | kind=code-symbol | source=probe/main_scripts/cpe.py:L116 | neighbors=[cpe.py, Return {vendor, product, version, cpe23…, _extract_version()]
- "main_scripts_db_scanner_build_op_msg_command": "build_op_msg_command()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L258 | neighbors=[db_scanner.py, _probe_mongodb(), Frame a single-field admin command as O…]
- "main_scripts_db_scanner_extract_mongo_version": "extract_mongo_version()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L288 | neighbors=[db_scanner.py, _probe_mongodb(), Pull a MongoDB server version out of a …]
- "main_scripts_db_scanner_interpret_mongodb_auth": "interpret_mongodb_auth()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L300 | neighbors=[db_scanner.py, _probe_mongodb(), Classify a serverStatus reply into auth…]
- "main_scripts_db_scanner_parse_mysql_greeting": "parse_mysql_greeting()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L53 | neighbors=[db_scanner.py, _probe_mysql(), Parse a MySQL/MariaDB initial handshake…]
- "main_scripts_db_scanner_parse_tds_prelogin": "parse_tds_prelogin()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L164 | neighbors=[db_scanner.py, _probe_mssql(), Read server version and encryption post…]
- "main_scripts_db_scanner_stamp_db_fact": "stamp_db_fact()" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L434 | neighbors=[db_scanner.py, ._scan_port(), Stamp the `db: True` discriminator onto…]
- "main_scripts_dns_scanner_derive_zones": "derive_zones()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L55 | neighbors=[dns_scanner.py, ._probe(), Candidate zone names to try AXFR / DNSS…]
- "main_scripts_dns_scanner_dnsscanner_axfr": "._axfr()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L139 | neighbors=[DNSScanner, ._probe(), Attempt a zone transfer, reading increm…]
- "main_scripts_findings_finding_row": "_finding_row()" | kind=code-symbol | source=probe/main_scripts/findings.py:L1257 | neighbors=[findings.py, One finding as the finding-section show…, summarize()]
- "main_scripts_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/main_scripts/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "main_scripts_ftp_scanner_banner_software": "banner_software()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L55 | neighbors=[ftp_scanner.py, ._probe(), Best-effort software token from the 220…]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-109.json

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
