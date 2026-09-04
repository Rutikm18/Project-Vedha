# Node Description Batch 59 of 332

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

- "routers_attack_paths_list_chokepoints": "list_chokepoints()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L117 | neighbors=[attack_paths.py, _all_paths_to_critical(), _asset_labels(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_recompute_and_store": "_recompute_and_store()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L199 | neighbors=[attack_paths.py, list_attack_paths(), _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_customer_access_build_scan_job": "build_scan_job()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L121 | neighbors=[customer_access.py, approve_scan_request(), Pure: turn an approved request into a p…, Pure: turn an approved request into a p…, Pure: turn an approved request into a p…]
- "routers_customer_access_clientuserout": "ClientUserOut" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L62 | neighbors=[customer_access.py, BaseModel, get_client_user(), patch_client_user(), provision_client_user()]
- "routers_customer_access_provision_client_user": "provision_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L171 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password(), _unique_portal_slug()]
- "routers_customer_access_slugify": "_slugify()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L100 | neighbors=[customer_access.py, A lowercase, hyphenated, DNS-label-safe…, _unique_portal_slug(), A lowercase, hyphenated, DNS-label-safe…, A lowercase, hyphenated, DNS-label-safe…]
- "routers_detection_runs_rationale_1": "detection_runs.py — temporal detection API (\"what changed since last time\").  GE" | kind=entity | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[detection_runs.py, DetectionRun, Engagement, FindingStatus, Finding]
- "routers_engagements_campaign_progress": "campaign_progress()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L766 | neighbors=[engagements.py, _job_phase(), _reconcile_status(), _result_summary(), One call powers the VA Campaigns page: …]
- "routers_engagements_get_engagement_scope": "get_engagement_scope()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1259 | neighbors=[engagements.py, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…]
- "routers_engagements_re_detect": "re_detect()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L150 | neighbors=[engagements.py, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …]
- "routers_findings_rationale_29": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L29 | neighbors=[Engagement, FindingStatus, Finding, sla_summary(), PaginatedResponse]
- "routers_probe_enrollment_approve_request_simple": "approve_request_simple()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L567 | neighbors=[probe_enrollment.py, auto_enroll_cidrs(), _next_probe_name(), _provision_agent_for_site(), SimpleApproveInput]
- "routers_probe_enrollment_enroll_token_is_usable": "enroll_token_is_usable()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[probe_enrollment.py, create_enrollment_request(), list_enroll_tokens(), A token can auto-approve only while liv…, A token can auto-approve only while liv…]
- "routers_probe_enrollment_generate_enroll_token": "generate_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[probe_enrollment.py, create_enroll_token(), _secret_hash(), Return (raw_token, token_hash, token_pr…, Return (raw_token, token_hash, token_pr…]
- "routers_probe_enrollment_rate_limit": "_rate_limit()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L99 | neighbors=[probe_enrollment.py, activate_enrollment(), create_enrollment_request(), poll_enrollment(), refresh_device_token()]
- "routers_probe_enrollment_simpleapproveinput": "SimpleApproveInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L530 | neighbors=[probe_enrollment.py, approve_request_simple(), One-click "Approve Site": every field i…, BaseModel, ._validate_networks()]
- "routers_remediation_generate_remediation": "generate_remediation()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L139 | neighbors=[remediation.py, _cached_plan(), _serialize(), _tenant_finding(), _upsert_plan()]
- "routers_remediation_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L41 | neighbors=[remediation.py, generate_remediation(), get_remediation(), Fetch a finding scoped to the caller's …, Fetch a finding scoped to the caller's …]
- "routers_remediation_upsert_plan": "_upsert_plan()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L94 | neighbors=[remediation.py, generate_remediation(), Execute the atomic upsert and return th…, _build_upsert_stmt(), Execute the atomic upsert and return th…]
- "routers_sla_policy_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L65 | neighbors=[sla_policy.py, get_sla_policy(), SlaPolicyOut, _windows_of_named(), put_sla_policy()]
- "routers_validation_create_validation_request": "create_validation_request()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L145 | neighbors=[validation.py, _default_check_kind(), _load_finding_and_eng(), _request_out(), _roe_allows_active_validation()]
- "run_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, POST(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "scanner_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=probe/scanner/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …]
- "scanner_accuracy_gate_corpuserror": "CorpusError" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L61 | neighbors=[accuracy_gate.py, ValueError, load_corpora(), load_corpus(), A corpus is malformed or unlabeled — a …]
- "scanner_accuracy_gate_load_corpora": "load_corpora()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L92 | neighbors=[accuracy_gate.py, CorpusError, load_corpus(), Every *.json corpus in `directory`, sor…, run_gate()]
- "scanner_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=probe/scanner/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()]
- "scanner_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts()]
- "scanner_delta_scanner_delta": "Delta" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L71 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…, One security-relevant change between tw…]
- "scanner_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/scanner/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, classify_device(), classify_from_results(), device_classifier.py — infer a device's…]
- "scanner_findings_corr_anon_data_exposure": "_corr_anon_data_exposure()" | kind=code-symbol | source=probe/scanner/findings.py:L1156 | neighbors=[findings.py, _by_target(), Finding, Two or more INDEPENDENT anonymous data-…, Two or more INDEPENDENT anonymous data-…]
- "scanner_findings_corr_mgmt_plane_exposed": "_corr_mgmt_plane_exposed()" | kind=code-symbol | source=probe/scanner/findings.py:L1198 | neighbors=[findings.py, _by_target(), Finding, Out-of-band / console management surfac…, Out-of-band / console management surfac…]
- "scanner_findings_corr_user_enum_plus_weak_auth": "_corr_user_enum_plus_weak_auth()" | kind=code-symbol | source=probe/scanner/findings.py:L1175 | neighbors=[findings.py, _by_target(), Finding, A disclosed user list (SMB null session…, A disclosed user list (SMB null session…]
- "scanner_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=probe/scanner/findings.py:L1319 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…]
- "scanner_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=probe/scanner/findings.py:L340 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()]
- "scanner_findings_rule_os_identification": "_rule_os_identification()" | kind=code-symbol | source=probe/scanner/findings.py:L1010 | neighbors=[findings.py, Fuse OS signals across scanners into ON…, _data(), Finding, _scanner()]
- "scanner_findings_summarize": "summarize()" | kind=code-symbol | source=probe/scanner/findings.py:L1279 | neighbors=[findings.py, _main(), Roll up findings for the finding sectio…, _finding_row(), _tally()]
- "scanner_ftp_scanner_ftpscanner_read_response": "._read_response()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L69 | neighbors=[FTPScanner, ._cmd(), ._list_bounded(), ._probe(), Read one (possibly multi-line) FTP repl…]
- "scanner_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L445 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…, Surveys a target for IoT/embedded devic…]
- "scanner_iot_scanner_mqtt_remaining_len": "_mqtt_remaining_len()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L271 | neighbors=[iot_scanner.py, _mqtt_connect(), _mqtt_subscribe_all(), MQTT variable-length encoding., MQTT variable-length encoding.]
- "scanner_iot_scanner_mqtt_subscribe_all": "_mqtt_subscribe_all()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L283 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt(), MQTT SUBSCRIBE to '#' (all topics), QoS…, MQTT SUBSCRIBE to '#' (all topics), QoS…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-058.json

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
