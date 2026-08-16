# Node Description Batch 51 of 209

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

- "routers_customer_access_patch_client_user": "patch_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L239 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password()]
- "routers_customer_access_unique_portal_slug": "_unique_portal_slug()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L108 | neighbors=[customer_access.py, provision_client_user(), Per-tenant-unique portal slug: <base>, …, _slugify()]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…, Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L421 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_findings_reopen_finding": "reopen_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L243 | neighbors=[findings.py, Operator reverses a resolution (auto or…, _tenant_finding(), Operator reverses a resolution (auto or…]
- "routers_findings_sla_summary": "sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L44 | neighbors=[findings.py, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…]
- "routers_portal_metric_finding": "_metric_finding()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L158 | neighbors=[portal.py, _enum_val(), portal_summary(), portal_trends()]
- "routers_portal_posture_view": "_posture_view()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L165 | neighbors=[portal.py, portal_posture(), portal_summary(), _enum_val()]
- "routers_probe_enrollment_authenticated_request": "_authenticated_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L477 | neighbors=[probe_enrollment.py, activate_enrollment(), _secret_hash(), poll_enrollment()]
- "routers_probe_enrollment_decode_public_key": "_decode_public_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L78 | neighbors=[probe_enrollment.py, create_enrollment_request(), .validate_key(), _verify_signature()]
- "routers_probe_enrollment_get_or_create_auto_enroll_site": "_get_or_create_auto_enroll_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L321 | neighbors=[probe_enrollment.py, create_enrollment_request(), auto_enroll_cidrs(), The singleton per-tenant Site that trus…]
- "routers_probe_enrollment_refresh_device_token": "refresh_device_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L640 | neighbors=[probe_enrollment.py, _rate_limit(), _secret_hash(), _verify_signature()]
- "routers_probe_enrollment_sitepolicyinput": "SitePolicyInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L148 | neighbors=[probe_enrollment.py, BaseModel, .require_site_reference(), .validate_networks()]
- "routers_probe_enrollment_verify_signature": "_verify_signature()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L88 | neighbors=[probe_enrollment.py, activate_enrollment(), refresh_device_token(), _decode_public_key()]
- "routers_validation_request_out": "_request_out()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L128 | neighbors=[validation.py, create_validation_request(), list_validation_requests(), ValidationRequestOut]
- "routers_validation_roe_allows_active_validation": "_roe_allows_active_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L81 | neighbors=[validation.py, approve_validation(), create_validation_request(), RoE gate: active validation is allowed …]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L525 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "scanner_delta_scanner_delta": "Delta" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L69 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…]
- "scanner_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/scanner/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…]
- "scanner_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/scanner/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "scanner_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/scanner/findings.py:L552 | neighbors=[findings.py, _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay()]
- "scanner_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/scanner/findings.py:L599 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…]
- "scanner_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/scanner/findings.py:L582 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…]
- "scanner_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/scanner/findings.py:L559 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…]
- "scanner_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=probe/scanner/findings.py:L230 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=probe/scanner/findings.py:L253 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=probe/scanner/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=probe/scanner/findings.py:L284 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_web": "_rule_web()" | kind=code-symbol | source=probe/scanner/findings.py:L395 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_run_findings": "run_findings()" | kind=code-symbol | source=probe/scanner/findings.py:L622 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict()]
- "scanner_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "scanner_init": "__init__.py" | kind=code-symbol | source=probe/scanner/__init__.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, VA scanner module — pure collection/sca…, 298a9d4 trim frontend to 7 core pages; …]
- "scanner_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L443 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…]
- "scanner_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L450 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "scanner_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L269 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding.]
- "scanner_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L281 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…]
- "scanner_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L155 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-050.json

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
