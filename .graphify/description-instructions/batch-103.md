# Node Description Batch 104 of 336

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

- "routers_probe_enrollment_approve_enrollment": "approve_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L615 | neighbors=[probe_enrollment.py, _keyed_hash(), _provision_agent_for_site()]
- "routers_probe_enrollment_enrollmentcreate": "EnrollmentCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L113 | neighbors=[probe_enrollment.py, BaseModel, .validate_key()]
- "routers_probe_enrollment_enrollmentsecret": "EnrollmentSecret" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L140 | neighbors=[probe_enrollment.py, EnrollmentActivate, BaseModel]
- "routers_probe_enrollment_keyed_hash": "_keyed_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L41 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request()]
- "routers_probe_enrollment_next_probe_name": "_next_probe_name()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L546 | neighbors=[probe_enrollment.py, approve_request_simple(), Auto-assign the next sequential vedha-a…]
- "routers_probe_enrollment_poll_enrollment": "poll_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L491 | neighbors=[probe_enrollment.py, _authenticated_request(), _rate_limit()]
- "routers_remediation_cached_plan": "_cached_plan()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L54 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_remediation_serialize": "_serialize()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L105 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_sla_policy_get_sla_policy": "get_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L81 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_put_sla_policy": "put_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L86 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_slapolicyout": "SlaPolicyOut" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L30 | neighbors=[sla_policy.py, _out(), BaseModel]
- "routers_users_userout": "UserOut" | kind=code-symbol | source=manager/backend/app/routers/users.py:L30 | neighbors=[users.py, _out(), BaseModel]
- "routers_validation_approve_validation": "approve_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L214 | neighbors=[validation.py, _get_request_or_404(), _roe_allows_active_validation()]
- "routers_validation_default_check_kind": "_default_check_kind()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L88 | neighbors=[validation.py, create_validation_request(), Pick a safe check for the finding. TLS …]
- "routers_validation_get_request_or_404": "_get_request_or_404()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L115 | neighbors=[validation.py, approve_validation(), reject_validation()]
- "routers_validation_validationrequestout": "ValidationRequestOut" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L63 | neighbors=[validation.py, _request_out(), BaseModel]
- "routers_vuln_scans_finish_cancelled_nuclei_job": "_finish_cancelled_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L516 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "routers_vuln_scans_set_nuclei_job_state": "_set_nuclei_job_state()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L493 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "scanner_accuracy_gate_check_thresholds": "check_thresholds()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L105 | neighbors=[accuracy_gate.py, Threshold violations for one scored cor…, run_gate()]
- "scanner_accuracy_gate_is_independent": "is_independent()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L100 | neighbors=[accuracy_gate.py, True when this corpus's labels can supp…, run_gate()]
- "scanner_accuracy_gate_main": "_main()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L204 | neighbors=[accuracy_gate.py, format_gate_report(), run_gate()]
- "scanner_accuracy_main": "_main()" | kind=code-symbol | source=probe/scanner/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "scanner_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "scanner_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/scanner/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "scanner_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, AdaptiveTimeout, from_rtts()]
- "scanner_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "scanner_cpe_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/cpe.py:L103 | neighbors=[cpe.py, Prefer an explicit version field; else …, to_cpe()]
- "scanner_cpe_to_cpe": "to_cpe()" | kind=code-symbol | source=probe/scanner/cpe.py:L116 | neighbors=[cpe.py, Return {vendor, product, version, cpe23…, _extract_version()]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "scanner_dns_scanner_derive_zones": "derive_zones()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L55 | neighbors=[dns_scanner.py, ._probe(), Candidate zone names to try AXFR / DNSS…]
- "scanner_dns_scanner_dnsscanner_axfr": "._axfr()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L139 | neighbors=[DNSScanner, ._probe(), Attempt a zone transfer, reading increm…]
- "scanner_findings_finding_row": "_finding_row()" | kind=code-symbol | source=probe/scanner/findings.py:L1257 | neighbors=[findings.py, One finding as the finding-section show…, summarize()]
- "scanner_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/scanner/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "scanner_ftp_scanner_banner_software": "banner_software()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L55 | neighbors=[ftp_scanner.py, ._probe(), Best-effort software token from the 220…]
- "scanner_ftp_scanner_parse_pasv": "parse_pasv()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L44 | neighbors=[ftp_scanner.py, ._list_bounded(), Extract the passive data PORT from a 22…]
- "scanner_host_discovery_hostdiscoveryscanner_arp_table": "._arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L177 | neighbors=[HostDiscoveryScanner, read_arp_table(), .scan_target()]
- "scanner_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "scanner_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "scanner_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-103.json

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
