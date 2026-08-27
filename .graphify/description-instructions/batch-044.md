# Node Description Batch 45 of 236

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

- "routers_probe_enrollment_generate_enroll_token": "generate_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[probe_enrollment.py, create_enroll_token(), _secret_hash(), Return (raw_token, token_hash, token_pr…, Return (raw_token, token_hash, token_pr…]
- "routers_probe_enrollment_rate_limit": "_rate_limit()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L99 | neighbors=[probe_enrollment.py, activate_enrollment(), create_enrollment_request(), poll_enrollment(), refresh_device_token()]
- "routers_probe_enrollment_simpleapproveinput": "SimpleApproveInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L530 | neighbors=[probe_enrollment.py, approve_request_simple(), One-click "Approve Site": every field i…, BaseModel, ._validate_networks()]
- "routers_remediation_generate_remediation": "generate_remediation()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L135 | neighbors=[remediation.py, _cached_plan(), _serialize(), _tenant_finding(), _upsert_plan()]
- "routers_sla_policy_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L65 | neighbors=[sla_policy.py, get_sla_policy(), SlaPolicyOut, _windows_of_named(), put_sla_policy()]
- "routers_validation_create_validation_request": "create_validation_request()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L145 | neighbors=[validation.py, _default_check_kind(), _load_finding_and_eng(), _request_out(), _roe_allows_active_validation()]
- "run_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, POST(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "scanner_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=probe/scanner/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …]
- "scanner_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()]
- "scanner_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts()]
- "scanner_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/scanner/findings.py:L1029 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "scanner_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/scanner/findings.py:L1012 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "scanner_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/scanner/findings.py:L989 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "scanner_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=probe/scanner/findings.py:L316 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()]
- "scanner_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=probe/scanner/findings.py:L665 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner()]
- "scanner_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=probe/scanner/findings.py:L752 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner()]
- "scanner_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=probe/scanner/findings.py:L850 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner()]
- "scanner_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=probe/scanner/findings.py:L627 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner()]
- "scanner_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=probe/scanner/findings.py:L916 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner()]
- "scanner_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=probe/scanner/findings.py:L715 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner()]
- "scanner_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=probe/scanner/findings.py:L943 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner()]
- "scanner_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/scanner/findings.py:L511 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner()]
- "scanner_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=probe/scanner/findings.py:L781 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner()]
- "scanner_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=probe/scanner/findings.py:L576 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner()]
- "scanner_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=probe/scanner/findings.py:L882 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/scanner/findings.py:L443 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/scanner/findings.py:L491 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner()]
- "scanner_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/scanner/findings.py:L465 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner()]
- "scanner_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=probe/scanner/findings.py:L819 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner()]
- "scanner_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/scanner/findings.py:L1125 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…]
- "scanner_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L142 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …, Best-effort device classification from …]
- "scanner_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L125 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…]
- "scanner_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L445 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…, Surveys a target for IoT/embedded devic…]
- "scanner_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L271 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding., MQTT variable-length encoding.]
- "scanner_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L283 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…, MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "scanner_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…, Extract PTR target names from mDNS resp…]
- "scanner_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=probe/scanner/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…, Parse masscan -oJ output robustly: hand…, _run_masscan()]
- "scanner_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L329 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-044.json

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
