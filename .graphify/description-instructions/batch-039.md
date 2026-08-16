# Node Description Batch 40 of 209

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

- "routers_customer_access_provision_client_user": "provision_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L169 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password(), _unique_portal_slug()]
- "routers_detection_runs_rationale_1": "detection_runs.py — temporal detection API (\"what changed since last time\").  GE" | kind=entity | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[detection_runs.py, DetectionRun, Engagement, FindingStatus, Finding]
- "routers_engagements_compute_overview": "_compute_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L40 | neighbors=[engagements.py, engagements_overview(), Shared aggregation — used by both the c…, _refresh_overview_cache(), Shared aggregation — used by both the c…]
- "routers_engagements_engagements_overview": "engagements_overview()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L398 | neighbors=[engagements.py, _compute_overview(), _overview_cache_key(), P1: kills the BFF N+1 (was list + one d…, P1: kills the BFF N+1 (was list + one d…]
- "routers_findings_rationale_29": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L29 | neighbors=[Engagement, FindingStatus, Finding, sla_summary(), PaginatedResponse]
- "routers_probe_enrollment_enroll_token_is_usable": "enroll_token_is_usable()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[probe_enrollment.py, create_enrollment_request(), list_enroll_tokens(), A token can auto-approve only while liv…, A token can auto-approve only while liv…]
- "routers_probe_enrollment_generate_enroll_token": "generate_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[probe_enrollment.py, create_enroll_token(), _secret_hash(), Return (raw_token, token_hash, token_pr…, Return (raw_token, token_hash, token_pr…]
- "routers_probe_enrollment_provision_agent_for_site": "_provision_agent_for_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L235 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request(), Bind a request to a Site policy and cre…, Bind a request to a Site policy and cre…]
- "routers_probe_enrollment_rate_limit": "_rate_limit()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L99 | neighbors=[probe_enrollment.py, activate_enrollment(), create_enrollment_request(), poll_enrollment(), refresh_device_token()]
- "routers_validation_create_validation_request": "create_validation_request()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L145 | neighbors=[validation.py, _default_check_kind(), _load_finding_and_eng(), _request_out(), _roe_allows_active_validation()]
- "run_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, POST(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "scanner_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=probe/scanner/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …]
- "scanner_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()]
- "scanner_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts()]
- "scanner_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=probe/scanner/findings.py:L316 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()]
- "scanner_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/scanner/findings.py:L511 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/scanner/findings.py:L443 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/scanner/findings.py:L491 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner()]
- "scanner_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/scanner/findings.py:L465 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner()]
- "scanner_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L142 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …, Best-effort device classification from …]
- "scanner_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L304 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…]
- "scanner_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L125 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…]
- "scanner_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L260 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line(), ._arp_table(), Return {ip: normalized_mac} from the OS…]
- "scanner_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=probe/scanner/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…, Parse masscan -oJ output robustly: hand…, _run_masscan()]
- "scanner_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "scanner_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L127 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …]
- "scanner_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L57 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…]
- "scanner_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L101 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), os_family_from_ttl(), Round the observed TTL up to the neares…]
- "scanner_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…, Best-effort device label from an announ…]
- "scanner_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…, Await readability on any listener witho…]
- "scanner_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/scanner/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), RuntimeError, .__init__(), All passive sources failed before the l…]
- "scanner_port_scanner_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L126 | neighbors=[port_scanner.py, ._attempt(), Map a connect()-time OSError to (state,…, ._scan_port(), Map a connect()-time OSError to (state,…]
- "scanner_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L90 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "scanner_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L547 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…, `async_udp_probe` with bounded per-port…]
- "scanner_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L688 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L460 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "scanner_service_banner_match_service": "match_service()" | kind=code-symbol | source=probe/scanner/service_banner.py:L88 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab(), Soft-match collected bytes to {service,…]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L142 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "scanner_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-039.json

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
