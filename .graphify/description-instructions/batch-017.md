# Node Description Batch 18 of 92

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

- "main_scripts_snmp_scanner_rationale_292": "GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]." | kind=entity | source=main_scripts/snmp_scanner.py:L292 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, ._walk_subtree()] | lang=en
- "main_scripts_snmp_scanner_rationale_315": "One GETBULK request — measure response/request size ratio." | kind=entity | source=main_scripts/snmp_scanner.py:L315 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, ._amplification_factor()] | lang=en
- "main_scripts_snmp_scanner_rationale_325": "Send a SNMPv3 Discover. Any reply = v3 agent present." | kind=entity | source=main_scripts/snmp_scanner.py:L325 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, ._snmpv3_present()] | lang=pt
- "main_scripts_snmp_scanner_rationale_46": "Dotted-notation OID string → BER-encoded bytes." | kind=entity | source=main_scripts/snmp_scanner.py:L46 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _encode_oid()] | lang=en
- "main_scripts_snmp_scanner_rationale_64": "BER-encoded OID bytes → dotted-notation string." | kind=entity | source=main_scripts/snmp_scanner.py:L64 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _decode_oid()] | lang=en
- "main_scripts_snmp_scanner_rationale_79": "Human-readable SNMP value for common ASN.1/SNMP types." | kind=entity | source=main_scripts/snmp_scanner.py:L79 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _decode_value()] | lang=en
- "main_scripts_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()] | lang=en
- "main_scripts_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=main_scripts/ssh_collector.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…] | lang=en
- "main_scripts_ssh_collector_rationale_1": "ssh_collector.py — credentialed (authenticated) inventory collection for Linux." | kind=entity | source=main_scripts/ssh_collector.py:L1 | neighbors=[RateLimiter, ResultWriter, ScanResult, ScopeGuard, ssh_collector.py] | lang=en
- "main_scripts_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L62 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()] | lang=en
- "main_scripts_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…] | lang=en
- "main_scripts_tls_fingerprint_rationale_1": "tls_fingerprint.py — active TLS server fingerprint (Tier 2.3, JARM methodology)." | kind=entity | source=main_scripts/tls_fingerprint.py:L1 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, tls_fingerprint.py] | lang=en
- "main_scripts_tls_fingerprint_rationale_137": "Parse the negotiated version + cipher + extensions from a ServerHello." | kind=entity | source=main_scripts/tls_fingerprint.py:L137 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, parse_server_hello()] | lang=en
- "main_scripts_tls_fingerprint_rationale_178": "2-char code from the cipher's position in CIPHER_LIST ('00' if unknown)." | kind=entity | source=main_scripts/tls_fingerprint.py:L178 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, cipher_code()] | lang=en
- "main_scripts_tls_fingerprint_rationale_185": "Concatenate the ServerHello extension TYPE codes (2 bytes each). We hash types," | kind=entity | source=main_scripts/tls_fingerprint.py:L185 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _server_ext_types()] | lang=en
- "main_scripts_tls_fingerprint_rationale_201": "JARM-shaped 62-char fuzzy hash: 3 chars per probe (cipher[2] + version[1])," | kind=entity | source=main_scripts/tls_fingerprint.py:L201 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, jarm_style_digest()] | lang=it
- "main_scripts_tls_fingerprint_rationale_242": "Read exactly the first TLS record (the ServerHello or an alert) and stop —     n" | kind=entity | source=main_scripts/tls_fingerprint.py:L242 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _recv_first_record()] | lang=en
- "main_scripts_tls_fingerprint_rationale_262": "Send one crafted ClientHello, read + parse the ServerHello. Sync." | kind=entity | source=main_scripts/tls_fingerprint.py:L262 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _one_probe()] | lang=en
- "main_scripts_tls_fingerprint_rationale_275": "Run all probes and return (62-char digest, per-probe results)." | kind=entity | source=main_scripts/tls_fingerprint.py:L275 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, fingerprint_host()] | lang=en
- "main_scripts_tls_fingerprint_rationale_91": "Build a complete TLS ClientHello record (record layer + handshake)." | kind=entity | source=main_scripts/tls_fingerprint.py:L91 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, build_client_hello()] | lang=pt
- "main_scripts_tls_scanner_rationale_1": "tls_scanner.py — collect TLS/SSL configuration facts.  METHOD (collection only):" | kind=entity | source=main_scripts/tls_scanner.py:L1 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, tls_scanner.py] | lang=en
- "main_scripts_tls_scanner_rationale_105": "Grade overall TLS posture A/B/C/F from accepted protocol versions and the     cl" | kind=entity | source=main_scripts/tls_scanner.py:L105 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, grade_tls_posture()] | lang=en
- "main_scripts_tls_scanner_rationale_147": "Never send an IP literal as SNI — non-conformant; some servers reject it." | kind=entity | source=main_scripts/tls_scanner.py:L147 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _sni()] | lang=en
- "main_scripts_tls_scanner_rationale_156": "Attempt a handshake forcing one protocol version. Returns cipher dict or None." | kind=entity | source=main_scripts/tls_scanner.py:L156 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, _try_version()] | lang=pt
- "main_scripts_tls_scanner_rationale_61": "Flag the security-relevant properties of an OpenSSL cipher-suite name:     forwa" | kind=entity | source=main_scripts/tls_scanner.py:L61 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, classify_cipher()] | lang=en
- "main_scripts_unauth_access": "unauth_access.py" | kind=code-symbol | source=main_scripts/unauth_access.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _as_text(), classify_unauth_access(), is_rce_capable(), test_main_scripts_unauth.py] | lang=en
- "main_scripts_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=main_scripts/web_scanner.py:L1 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, web_scanner.py] | lang=en
- "main_scripts_web_scanner_rationale_46": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=main_scripts/web_scanner.py:L46 | neighbors=[BaseScanner, ResultWriter, ScanResult, ScopeGuard, parse_allow_header()] | lang=en
- "main_scripts_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=main_scripts/windows_collector.py:L1 | neighbors=[RateLimiter, ResultWriter, ScanResult, ScopeGuard, windows_collector.py] | lang=en
- "main_scripts_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=main_scripts/windows_collector.py:L160 | neighbors=[RateLimiter, ResultWriter, ScanResult, ScopeGuard, _smb_registry_collect()] | lang=en
- "scanner_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=scanner/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …] | lang=en
- "scanner_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=scanner/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()] | lang=en
- "scanner_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=scanner/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts()] | lang=en
- "scanner_findings_corr_anon_data_exposure": "_corr_anon_data_exposure()" | kind=code-symbol | source=scanner/findings.py:L1080 | neighbors=[findings.py, _by_target(), Finding, Two or more INDEPENDENT anonymous data-…, Two or more INDEPENDENT anonymous data-…] | lang=en
- "scanner_findings_corr_mgmt_plane_exposed": "_corr_mgmt_plane_exposed()" | kind=code-symbol | source=scanner/findings.py:L1122 | neighbors=[findings.py, _by_target(), Finding, Out-of-band / console management surfac…, Out-of-band / console management surfac…] | lang=en
- "scanner_findings_corr_user_enum_plus_weak_auth": "_corr_user_enum_plus_weak_auth()" | kind=code-symbol | source=scanner/findings.py:L1099 | neighbors=[findings.py, _by_target(), Finding, A disclosed user list (SMB null session…, A disclosed user list (SMB null session…] | lang=en
- "scanner_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=scanner/findings.py:L340 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()] | lang=en
- "scanner_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=scanner/host_discovery.py:L307 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-017.json

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
