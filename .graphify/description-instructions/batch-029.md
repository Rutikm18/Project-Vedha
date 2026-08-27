# Node Description Batch 30 of 92

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

- "main_scripts_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "main_scripts_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L79 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…]
- "main_scripts_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L103 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …]
- "main_scripts_syn_scanner_classify": "classify()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L179 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L231 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L125 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…]
- "main_scripts_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L209 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__()]
- "main_scripts_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L415 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/syn_scanner.py:L284 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "main_scripts_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …]
- "main_scripts_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…]
- "main_scripts_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …]
- "main_scripts_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…]
- "main_scripts_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync()]
- "main_scripts_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "main_scripts_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=main_scripts/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync()]
- "main_scripts_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe()]
- "main_scripts_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe()]
- "main_scripts_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe()]
- "main_scripts_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe()]
- "main_scripts_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe()]
- "main_scripts_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "main_scripts_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L290 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe()]
- "main_scripts_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=main_scripts/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "main_scripts_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=main_scripts/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "main_scripts_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=main_scripts/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…]
- "scanner_accuracy_main": "_main()" | kind=code-symbol | source=scanner/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "scanner_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=scanner/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "scanner_accuracy_ratio": "_ratio()" | kind=code-symbol | source=scanner/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "scanner_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=scanner/adaptive_timeout.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, AdaptiveTimeout, from_rtts()]
- "scanner_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=scanner/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=scanner/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "scanner_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=scanner/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…]
- "scanner_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=scanner/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.]
- "scanner_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=scanner/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…]
- "scanner_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=scanner/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-029.json

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
