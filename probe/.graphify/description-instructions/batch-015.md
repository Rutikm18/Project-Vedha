# Node Description Batch 16 of 92

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=agent/use_cases.py:L265 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int(), Map a numeric use-case code → use_case_…] | lang=en
- "agent_validation_score_inventory": "score_inventory()" | kind=code-symbol | source=agent/validation.py:L201 | neighbors=[validation.py, Score promoted inventory against explic…, _metric(), _not_scored(), validate_ground_truth()] | lang=en
- "commit:repo:local/probe@20f2a9dc@de583d868b01429dcc83e0d6e8485b4931699bf8": "de583d8 feat(workflow): wire os_fingerprint + service_enum into the probe pipel…" | kind=Commit | source=git | neighbors=[a548359 feat(auto-enrollment): implemen…, feat/wire-osfp-service-enum, asset.py, cache.py, workflow_engine.py] | lang=en
- "exception": "Exception" | kind=code-symbol | neighbors=[CliError, LicenseError, TransportError, ScopeError, ScopeError] | lang=en
- "main_scripts_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=main_scripts/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …] | lang=en
- "main_scripts_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=main_scripts/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()] | lang=en
- "main_scripts_db_scanner_rationale_1": "db_scanner.py — fingerprint database services.  WHY: databases are everywhere on" | kind=entity | source=main_scripts/db_scanner.py:L1 | neighbors=[db_scanner.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_db_scanner_rationale_102": "Classify a Redis INFO reply. `unauthenticated_read` is True only when we     act" | kind=entity | source=main_scripts/db_scanner.py:L102 | neighbors=[interpret_redis_info(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_device_classifier": "device_classifier.py" | kind=code-symbol | source=main_scripts/device_classifier.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…, test_main_scripts_device.py] | lang=en
- "main_scripts_findings_corr_anon_data_exposure": "_corr_anon_data_exposure()" | kind=code-symbol | source=main_scripts/findings.py:L1080 | neighbors=[findings.py, _by_target(), Finding, Two or more INDEPENDENT anonymous data-…, Two or more INDEPENDENT anonymous data-…] | lang=en
- "main_scripts_findings_corr_mgmt_plane_exposed": "_corr_mgmt_plane_exposed()" | kind=code-symbol | source=main_scripts/findings.py:L1122 | neighbors=[findings.py, _by_target(), Finding, Out-of-band / console management surfac…, Out-of-band / console management surfac…] | lang=en
- "main_scripts_findings_corr_user_enum_plus_weak_auth": "_corr_user_enum_plus_weak_auth()" | kind=code-symbol | source=main_scripts/findings.py:L1099 | neighbors=[findings.py, _by_target(), Finding, A disclosed user list (SMB null session…, A disclosed user list (SMB null session…] | lang=en
- "main_scripts_findings_rule_cleartext_and_exposure": "_rule_cleartext_and_exposure()" | kind=code-symbol | source=main_scripts/findings.py:L340 | neighbors=[findings.py, build_service_index(), Finding, _is_open(), _scanner()] | lang=en
- "main_scripts_host_discovery_fuse_liveness": "fuse_liveness()" | kind=code-symbol | source=main_scripts/host_discovery.py:L307 | neighbors=[host_discovery.py, _now(), _state_for_confidence(), .scan_target(), Combine TCP + neighbor signals into a c…] | lang=en
- "main_scripts_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=main_scripts/host_discovery.py:L195 | neighbors=[host_discovery.py, BaseScanner, ScanResult, parse_neighbor_line(), One OS neighbor-cache observation about…] | lang=en
- "main_scripts_iot_scanner_rationale_1": "iot_scanner.py — IoT / embedded device fingerprint and exposure scanner.  Covers" | kind=entity | source=main_scripts/iot_scanner.py:L1 | neighbors=[iot_scanner.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_131": "Decode a DNS wire-format name, following pointers.  Returns (name, end_offset)." | kind=entity | source=main_scripts/iot_scanner.py:L131 | neighbors=[_decode_mdns_name(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_iot_scanner_rationale_157": "Extract PTR target names from mDNS response (services discovered)." | kind=entity | source=main_scripts/iot_scanner.py:L157 | neighbors=[_parse_mdns_response(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_272": "MQTT variable-length encoding." | kind=entity | source=main_scripts/iot_scanner.py:L272 | neighbors=[_mqtt_remaining_len(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_284": "MQTT SUBSCRIBE to '#' (all topics), QoS 0." | kind=entity | source=main_scripts/iot_scanner.py:L284 | neighbors=[_mqtt_subscribe_all(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_349": "CoAP Confirmable GET for /.well-known/core — resource discovery." | kind=entity | source=main_scripts/iot_scanner.py:L349 | neighbors=[_coap_get_wellknown_core(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_362": "Extract CoAP response code and content." | kind=entity | source=main_scripts/iot_scanner.py:L362 | neighbors=[_parse_coap_response(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_406": "HTTP GET to CWMP port — detect ACS or CPE management interface." | kind=entity | source=main_scripts/iot_scanner.py:L406 | neighbors=[_probe_cwmp(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_446": "Surveys a target for IoT/embedded device exposure across 6 protocol families." | kind=entity | source=main_scripts/iot_scanner.py:L446 | neighbors=[IoTScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_iot_scanner_rationale_59": "HTTP GET the UPnP rootDesc.xml and extract device info." | kind=entity | source=main_scripts/iot_scanner.py:L59 | neighbors=[_fetch_upnp_root_desc(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=main_scripts/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_1": "mcp_ai_scanner.py — discover exposed AI inference servers and MCP endpoints.  WH" | kind=entity | source=main_scripts/mcp_ai_scanner.py:L1 | neighbors=[mcp_ai_scanner.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_153": "Server/body fingerprint match against known non-AI squatters, or None." | kind=entity | source=main_scripts/mcp_ai_scanner.py:L153 | neighbors=[_known_false_positive(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_162": "The strongest possible evidence for a real MCP server: a WWW-Authenticate     he" | kind=entity | source=main_scripts/mcp_ai_scanner.py:L162 | neighbors=[_mcp_oauth_signal(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mcp_ai_scanner_rationale_175": "JSON-typed body that actually talks about auth, not just any error text." | kind=entity | source=main_scripts/mcp_ai_scanner.py:L175 | neighbors=[_auth_shaped_json_body(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…] | lang=en
- "main_scripts_mobile_scanner_rationale_1": "mobile_scanner.py — mobile device exposure detection.  Covers playbook 13 (Mobil" | kind=entity | source=main_scripts/mobile_scanner.py:L1 | neighbors=[mobile_scanner.py, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_152": "Attempt TCP connect to lockdownd port 62078.     Port open = iOS device present" | kind=entity | source=main_scripts/mobile_scanner.py:L152 | neighbors=[_probe_lockdownd(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_188": "Build a DNS PTR query in mDNS wire format with QU bit set." | kind=entity | source=main_scripts/mobile_scanner.py:L188 | neighbors=[_build_mdns_query(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_199": "Extract PTR target names (service instance names) from mDNS reply." | kind=entity | source=main_scripts/mobile_scanner.py:L199 | neighbors=[_parse_mdns_ptr_names(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_259": "Send one mDNS PTR query to target:5353 and return instance names." | kind=entity | source=main_scripts/mobile_scanner.py:L259 | neighbors=[_probe_mdns_mobile_sync(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_279": "Detects mobile device exposure on the network:     ADB (Android) | lockdownd (iO" | kind=entity | source=main_scripts/mobile_scanner.py:L279 | neighbors=[MobileScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_60": "Build an ADB A_CNXN (CONNECT) message — the standard handshake initiator." | kind=entity | source=main_scripts/mobile_scanner.py:L60 | neighbors=[_build_adb_cnxn(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_mobile_scanner_rationale_71": "Parse a 24-byte ADB message header.  Returns parsed fields or None." | kind=entity | source=main_scripts/mobile_scanner.py:L71 | neighbors=[_parse_adb_header(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_mobile_scanner_rationale_96": "Send ADB CNXN and read the device's CNXN reply.     Returns a dict with connecti" | kind=entity | source=main_scripts/mobile_scanner.py:L96 | neighbors=[_probe_adb(), BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-015.json

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
