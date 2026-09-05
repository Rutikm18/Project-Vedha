# Node Description Batch 75 of 336

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

- "main_scripts_smb_scanner_spnego_init": "_spnego_init()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L133 | neighbors=[smb_scanner.py, ntlm_os_build(), Wrap an NTLMSSP Type-1 in a minimal SPN…, _der()]
- "main_scripts_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "main_scripts_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "main_scripts_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "main_scripts_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "main_scripts_ssh_scanner_evaluate_algorithms": "evaluate_algorithms()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L133 | neighbors=[ssh_scanner.py, _dedup(), Grade a server's offered algorithms aga…, ._scan_port()]
- "main_scripts_ssh_scanner_read_packet": "_read_packet()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L225 | neighbors=[ssh_scanner.py, Read one unencrypted SSH binary packet …, _recv_exact(), ._probe()]
- "main_scripts_ssh_scanner_sshscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L249 | neighbors=[Blocking: connect, exchange identificat…, SSHScanner, _read_ident(), _read_packet()]
- "main_scripts_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L130 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "main_scripts_syn_scanner_parse_tcp_options": "parse_tcp_options()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L137 | neighbors=[syn_scanner.py, _parse_mss(), parse_packet(), Walk a TCP options field into a p0f-sty…]
- "main_scripts_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "main_scripts_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe(), Parse IKEv1 or IKEv2 response header.]
- "main_scripts_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe(), Parse RMCP Pong; extract supported enti…]
- "main_scripts_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe(), Return byte count and check QR bit (1 =…]
- "main_scripts_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe(), Extract SIP version + server header fro…]
- "main_scripts_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe(), Extract Location and Server from SSDP r…]
- "main_scripts_va_campaign_default_stages": "default_stages()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L390 | neighbors=[va_campaign.py, build_campaign(), Stage, Build the real capability stages from a…]
- "main_scripts_va_campaign_now": "_now()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L61 | neighbors=[va_campaign.py, .__init__(), .mark(), .snapshot()]
- "main_scripts_va_campaign_progressreporter_mark": ".mark()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L202 | neighbors=[ProgressReporter, _now(), ._flush(), .run()]
- "main_scripts_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "main_scripts_vnc_scanner_read_security_types": "_read_security_types()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L81 | neighbors=[vnc_scanner.py, Read the offered security types, handli…, _recv_exact(), ._probe()]
- "main_scripts_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…, Read the Allow header from an OPTIONS r…]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Engagement, 298a9d4 trim frontend to 7 core pages; …]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder — production-gr…]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[LLMOutput, Base, TimestampMixin, ReviewStatus]
- "models_probe_enrollment_probeenrollmenttoken": "ProbeEnrollmentToken" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L72 | neighbors=[probe_enrollment.py, Base, TimestampMixin, Pre-authorized, Site-bound enrollment t…]
- "models_scan_job_attempt_scanjobattempt": "ScanJobAttempt" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L11 | neighbors=[scan_job_attempt.py, One immutable, fenced execution claim f…, Base, TimestampMixin]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_service": "service.py" | kind=code-symbol | source=manager/backend/app/models/service.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Service, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant": "tenant.py" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, d1b4dd3 trim frontend to 7 core pages; …, Tenant, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder — production-gr…]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "portal_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/portal/layout.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, c52feb4 feat(portal): reskin User Porta…, PortalLayout(), NAV]
- "portscan_main": "main()" | kind=code-symbol | source=portscan.py:L216 | neighbors=[portscan.py, parse_ports(), PortScanner, .run()]
- "portscan_portscanner_scan_port": ".scan_port()" | kind=code-symbol | source=portscan.py:L180 | neighbors=[PortScanner, .run(), ._attempt(), .wait()]
- "portscan_ratelimiter": "RateLimiter" | kind=code-symbol | source=portscan.py:L95 | neighbors=[portscan.py, .__init__(), .__init__(), .wait()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-074.json

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
