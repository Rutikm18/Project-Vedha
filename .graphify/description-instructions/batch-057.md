# Node Description Batch 58 of 332

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

- "main_scripts_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L251 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…, Full, debuggable classification for att…, Full, debuggable classification for att…]
- "main_scripts_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L619 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli(), Accepts CIDRs ('10.0.0.0/24'), single I…, Accepts CIDRs ('10.0.0.0/24'), single I…]
- "main_scripts_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1105 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…]
- "main_scripts_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L494 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target(), Connect to one port and read whatever i…]
- "main_scripts_smb_enum_scanner_decode": "_decode()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L212 | neighbors=[smb_enum_scanner.py, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _safe()]
- "main_scripts_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "main_scripts_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community()]
- "main_scripts_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "main_scripts_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "main_scripts_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "main_scripts_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]
- "main_scripts_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "main_scripts_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…]
- "main_scripts_ssh_scanner_cursor": "_Cursor" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L72 | neighbors=[ssh_scanner.py, .__init__(), .read(), .read_name_list(), parse_kexinit()]
- "main_scripts_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L528 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking(), Turn resolved port states + harvested i…, Turn resolved port states + harvested i…]
- "main_scripts_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L178 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "main_scripts_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L63 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "main_scripts_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L137 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "main_scripts_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L242 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "main_scripts_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L185 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L283 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L313 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L165 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni(), Attempt a handshake forcing one protoco…]
- "main_scripts_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L295 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe(), Acquire the concurrency gate (adaptive …, Acquire the concurrency gate (adaptive …]
- "main_scripts_unauth_access": "unauth_access.py" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_text(), classify_unauth_access(), is_rce_capable(), test_main_scripts_unauth.py]
- "main_scripts_va_campaign_progressreporter_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L174 | neighbors=[ProgressReporter, _monotonic(), _now(), ._flush(), StageState]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_base": "base.py" | kind=code-symbol | source=manager/backend/app/models/base.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Base, TimestampMixin, UUIDMixin, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 6bb51ab feat: add detection-explain end…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest, 298a9d4 trim frontend to 7 core pages; …]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 6be8259 feat(integrations): outbox deli…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, AgentCredential, ProbeEnrollmentRequest, ProbeEnrollmentToken]
- "models_scan_request": "scan_request.py" | kind=code-symbol | source=manager/backend/app/models/scan_request.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c7f226f chore: bundle pending working-t…, ScanRequest, scan_request.py — a customer-initiated,…]
- "path_route_proxy": "proxy()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L17 | neighbors=[route.ts, GET(), PATCH(), POST(), portalToken()]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, graphStore, GET(), 298a9d4 trim frontend to 7 core pages; …, graph-store.ts]
- "portscan_portscanner_attempt": "._attempt()" | kind=code-symbol | source=portscan.py:L145 | neighbors=[PortScanner, classify_os_error(), family_of(), ._record(), .scan_port()]
- "results_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, GET(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "routers_agent_advisor_rationale_1": "agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag" | kind=entity | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[agent_advisor.py, AgentDecisionEngine, AgentUnavailableError, AgentRecommendation, Engagement]
- "routers_attack_paths_build_analyzer": "_build_analyzer()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L175 | neighbors=[attack_paths.py, attack_graph(), blast_radius(), list_chokepoints(), _recompute_and_store()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-057.json

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
