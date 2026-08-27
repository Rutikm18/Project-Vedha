# Node Description Batch 56 of 236

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

- "main_scripts_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L627 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…]
- "main_scripts_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L756 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "main_scripts_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L169 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …]
- "main_scripts_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L185 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…, Full, debuggable classification for att…]
- "main_scripts_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L470 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli(), Accepts CIDRs ('10.0.0.0/24'), single I…]
- "main_scripts_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L836 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…]
- "main_scripts_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L247 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "main_scripts_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L340 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "main_scripts_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L173 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "main_scripts_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L465 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target()]
- "main_scripts_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "main_scripts_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "main_scripts_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "main_scripts_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "main_scripts_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "main_scripts_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L118 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "main_scripts_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L125 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]
- "main_scripts_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L415 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking(), Turn resolved port states + harvested i…]
- "main_scripts_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "main_scripts_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "main_scripts_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "main_scripts_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "main_scripts_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "main_scripts_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L155 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "main_scripts_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe(), Parse IKEv1 or IKEv2 response header.]
- "main_scripts_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe(), Parse RMCP Pong; extract supported enti…]
- "main_scripts_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe(), Return byte count and check QR bit (1 =…]
- "main_scripts_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe(), Extract SIP version + server header fro…]
- "main_scripts_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe(), Extract Location and Server from SSDP r…]
- "main_scripts_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L290 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe(), Acquire the concurrency gate (adaptive …]
- "main_scripts_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "main_scripts_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…, Read the Allow header from an OPTIONS r…]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Engagement, 298a9d4 trim frontend to 7 core pages; …]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder — production-gr…]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[LLMOutput, Base, TimestampMixin, ReviewStatus]
- "models_probe_enrollment_probeenrollmenttoken": "ProbeEnrollmentToken" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L72 | neighbors=[probe_enrollment.py, Base, TimestampMixin, Pre-authorized, Site-bound enrollment t…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-055.json

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
