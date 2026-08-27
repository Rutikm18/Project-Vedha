# Node Description Batch 78 of 236

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

- "routers_probe_enrollment_enrollmentsecret": "EnrollmentSecret" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L140 | neighbors=[probe_enrollment.py, EnrollmentActivate, BaseModel]
- "routers_probe_enrollment_keyed_hash": "_keyed_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L41 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request()]
- "routers_probe_enrollment_next_probe_name": "_next_probe_name()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L546 | neighbors=[probe_enrollment.py, approve_request_simple(), Auto-assign the next sequential probe n…]
- "routers_probe_enrollment_poll_enrollment": "poll_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L491 | neighbors=[probe_enrollment.py, _authenticated_request(), _rate_limit()]
- "routers_remediation_build_upsert_stmt": "_build_upsert_stmt()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L62 | neighbors=[remediation.py, Build the atomic INSERT … ON CONFLICT D…, _upsert_plan()]
- "routers_remediation_cached_plan": "_cached_plan()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L52 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_remediation_serialize": "_serialize()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L103 | neighbors=[remediation.py, generate_remediation(), get_remediation()]
- "routers_sla_policy_get_sla_policy": "get_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L81 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_put_sla_policy": "put_sla_policy()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L86 | neighbors=[sla_policy.py, _out(), _row()]
- "routers_sla_policy_slapolicyout": "SlaPolicyOut" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L30 | neighbors=[sla_policy.py, _out(), BaseModel]
- "routers_validation_approve_validation": "approve_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L214 | neighbors=[validation.py, _get_request_or_404(), _roe_allows_active_validation()]
- "routers_validation_default_check_kind": "_default_check_kind()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L88 | neighbors=[validation.py, create_validation_request(), Pick a safe check for the finding. TLS …]
- "routers_validation_get_request_or_404": "_get_request_or_404()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L115 | neighbors=[validation.py, approve_validation(), reject_validation()]
- "routers_validation_validationrequestout": "ValidationRequestOut" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L63 | neighbors=[validation.py, _request_out(), BaseModel]
- "routers_vuln_scans_finish_cancelled_nuclei_job": "_finish_cancelled_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L516 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "routers_vuln_scans_set_nuclei_job_state": "_set_nuclei_job_state()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L493 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "scanner_accuracy_main": "_main()" | kind=code-symbol | source=probe/scanner/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()]
- "scanner_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()]
- "scanner_accuracy_ratio": "_ratio()" | kind=code-symbol | source=probe/scanner/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()]
- "scanner_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, AdaptiveTimeout, from_rtts()]
- "scanner_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "scanner_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…]
- "scanner_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.]
- "scanner_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…]
- "scanner_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…]
- "scanner_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…]
- "scanner_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…]
- "scanner_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L98 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…]
- "scanner_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L201 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…]
- "scanner_findings_is_open": "_is_open()" | kind=code-symbol | source=probe/scanner/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "scanner_findings_summarize": "summarize()" | kind=code-symbol | source=probe/scanner/findings.py:L1151 | neighbors=[findings.py, _main(), _tally()]
- "scanner_host_discovery_hostdiscoveryscanner_arp_table": "._arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L177 | neighbors=[HostDiscoveryScanner, read_arp_table(), .scan_target()]
- "scanner_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/scanner/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "scanner_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "scanner_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "scanner_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "scanner_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "scanner_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=probe/scanner/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-077.json

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
