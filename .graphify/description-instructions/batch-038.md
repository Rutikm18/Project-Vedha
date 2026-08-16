# Node Description Batch 39 of 209

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

- "main_scripts_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…]
- "main_scripts_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), .__init__(), RuntimeError, All passive sources failed before the l…]
- "main_scripts_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L390 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…, Bounded worker-pool scan of every reque…]
- "main_scripts_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L516 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…]
- "main_scripts_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L688 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "main_scripts_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L294 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…]
- "main_scripts_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L129 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json()]
- "main_scripts_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L88 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…]
- "main_scripts_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L142 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "main_scripts_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "main_scripts_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community()]
- "main_scripts_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "main_scripts_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "main_scripts_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "main_scripts_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]
- "main_scripts_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "main_scripts_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…]
- "main_scripts_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L150 | neighbors=[syn_scanner.py, _parse_mss(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking(), Parse a raw IPv4+TCP packet (as receive…]
- "main_scripts_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L189 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…]
- "main_scripts_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L196 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…]
- "main_scripts_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L62 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L282 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L255 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_unauth_access": "unauth_access.py" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_text(), classify_unauth_access(), is_rce_capable(), test_main_scripts_unauth.py]
- "main_scripts_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L135 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_base": "base.py" | kind=code-symbol | source=manager/backend/app/models/base.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Base, TimestampMixin, UUIDMixin, 298a9d4 trim frontend to 7 core pages; …]
- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest, 298a9d4 trim frontend to 7 core pages; …]
- "models_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, AgentCredential, ProbeEnrollmentRequest, ProbeEnrollmentToken]
- "path_route_proxy": "proxy()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L17 | neighbors=[route.ts, GET(), PATCH(), POST(), portalToken()]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, graphStore, GET(), 298a9d4 trim frontend to 7 core pages; …, graph-store.ts]
- "portal_portalshell_portalshell": "PortalShell()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L117 | neighbors=[page.tsx, page.tsx, PortalShell.tsx, page.tsx, page.tsx]
- "portscan_portscanner_attempt": "._attempt()" | kind=code-symbol | source=portscan.py:L145 | neighbors=[PortScanner, classify_os_error(), family_of(), ._record(), .scan_port()]
- "results_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, GET(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "routers_agent_advisor_rationale_1": "agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag" | kind=entity | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[agent_advisor.py, AgentDecisionEngine, AgentUnavailableError, AgentRecommendation, Engagement]
- "routers_attack_paths_build_analyzer": "_build_analyzer()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L175 | neighbors=[attack_paths.py, attack_graph(), blast_radius(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_list_chokepoints": "list_chokepoints()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L117 | neighbors=[attack_paths.py, _all_paths_to_critical(), _asset_labels(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_recompute_and_store": "_recompute_and_store()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L199 | neighbors=[attack_paths.py, list_attack_paths(), _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_customer_access_clientuserout": "ClientUserOut" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L63 | neighbors=[customer_access.py, BaseModel, get_client_user(), patch_client_user(), provision_client_user()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
