# Node Description Batch 63 of 186

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

- "routers_engagements_get_engagement_scope": "get_engagement_scope()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L663 | neighbors=[engagements.py, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…]
- "routers_engagements_overview_cache_key": "_overview_cache_key()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L35 | neighbors=[engagements.py, engagements_overview(), _refresh_overview_cache()]
- "routers_engagements_re_detect": "re_detect()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L123 | neighbors=[engagements.py, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …]
- "routers_exploits_approval_out": "_approval_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L433 | neighbors=[exploits.py, ApprovalOut, list_approvals()]
- "routers_exploits_get_approval_or_404": "_get_approval_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L408 | neighbors=[exploits.py, approve_exploit(), reject_exploit()]
- "routers_exploits_get_exploit_result": "get_exploit_result()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L205 | neighbors=[exploits.py, _get_result_or_404(), _result_out()]
- "routers_exploits_run_approved_exploit": "_run_approved_exploit()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L445 | neighbors=[exploits.py, Background task: run the exploit after …, Background task: run the exploit after …]
- "routers_probe_enrollment_approve_enrollment": "approve_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L455 | neighbors=[probe_enrollment.py, _keyed_hash(), _provision_agent_for_site()]
- "routers_probe_enrollment_enrollmentcreate": "EnrollmentCreate" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L112 | neighbors=[probe_enrollment.py, BaseModel, .validate_key()]
- "routers_probe_enrollment_enrollmentsecret": "EnrollmentSecret" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L139 | neighbors=[probe_enrollment.py, EnrollmentActivate, BaseModel]
- "routers_probe_enrollment_keyed_hash": "_keyed_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L40 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request()]
- "routers_probe_enrollment_poll_enrollment": "poll_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L415 | neighbors=[probe_enrollment.py, _authenticated_request(), _rate_limit()]
- "routers_validation_approve_validation": "approve_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L214 | neighbors=[validation.py, _get_request_or_404(), _roe_allows_active_validation()]
- "routers_validation_default_check_kind": "_default_check_kind()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L88 | neighbors=[validation.py, create_validation_request(), Pick a safe check for the finding. TLS …]
- "routers_validation_get_request_or_404": "_get_request_or_404()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L115 | neighbors=[validation.py, approve_validation(), reject_validation()]
- "routers_validation_validationrequestout": "ValidationRequestOut" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L63 | neighbors=[validation.py, _request_out(), BaseModel]
- "routers_vuln_scans_finish_cancelled_nuclei_job": "_finish_cancelled_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L516 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "routers_vuln_scans_set_nuclei_job_state": "_set_nuclei_job_state()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L493 | neighbors=[vuln_scans.py, _finish_failed_nuclei_job(), _run_nuclei_and_save()]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()]
- "scanner_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…]
- "scanner_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…]
- "scanner_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.]
- "scanner_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…]
- "scanner_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…]
- "scanner_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…]
- "scanner_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…]
- "scanner_host_discovery_hostdiscoveryscanner_arp_table": "._arp_table()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L177 | neighbors=[HostDiscoveryScanner, read_arp_table(), .scan_target()]
- "scanner_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/scanner/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "scanner_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "scanner_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L346 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…]
- "scanner_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L129 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…]
- "scanner_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L57 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…]
- "scanner_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L257 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "scanner_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L359 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content.]
- "scanner_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L381 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "scanner_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L403 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…]
- "scanner_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L89 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "scanner_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "scanner_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L173 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…]
- "scanner_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L151 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-062.json

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
