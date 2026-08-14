# Node Description Batch 61 of 186

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L749 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…]
- "main_scripts_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L302 | neighbors=[.acquire(), .run(), RateLimiter]
- "main_scripts_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L637 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "main_scripts_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L628 | neighbors=[.run(), ResultWriter, .to_json()]
- "main_scripts_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L205 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "main_scripts_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L253 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "main_scripts_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "main_scripts_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "main_scripts_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "main_scripts_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "main_scripts_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L60 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…]
- "main_scripts_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L84 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …]
- "main_scripts_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L122 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L174 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L106 | neighbors=[syn_scanner.py, Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking()]
- "main_scripts_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L152 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__()]
- "main_scripts_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L210 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "main_scripts_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync()]
- "main_scripts_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "main_scripts_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync()]
- "main_scripts_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L187 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe()]
- "main_scripts_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L218 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe()]
- "main_scripts_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L246 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe()]
- "main_scripts_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L203 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe()]
- "main_scripts_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L231 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe()]
- "main_scripts_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "main_scripts_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L289 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe()]
- "main_scripts_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "main_scripts_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L44 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…]
- "models_agent_recommendation_rationale_1": "agent_recommendation.py — decisions/actions proposed by the agentic AI advisor." | kind=entity | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[agent_recommendation.py, Base, TimestampMixin]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackPath, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline": "attack_timeline.py" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackTimeline, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline_rationale_12": "Append-only ledger of every attack action performed during an engagement.      W" | kind=entity | source=manager/backend/app/models/attack_timeline.py:L12 | neighbors=[AttackTimeline, Base, TimestampMixin]
- "models_audit_log": "audit_log.py" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AuditLog, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/models/detection.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config": "detection_config.py" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionConfig, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config_rationale_11": "Per-engagement SIEM + EDR connection settings used by the detection     validati" | kind=entity | source=manager/backend/app/models/detection_config.py:L11 | neighbors=[DetectionConfig, Base, TimestampMixin]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-060.json

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
