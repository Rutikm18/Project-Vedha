# Node Description Batch 27 of 92

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

- "agent_scope_crypt_decrypt_scope": "decrypt_scope()" | kind=code-symbol | source=agent/scope_crypt.py:L97 | neighbors=[scope_crypt.py, decrypt_scope_b64(), Decrypt a scope blob using the probe's …] | lang=en
- "agent_scope_crypt_decrypt_scope_b64": "decrypt_scope_b64()" | kind=code-symbol | source=agent/scope_crypt.py:L155 | neighbors=[scope_crypt.py, decrypt_scope(), decrypt_scope() accepting a base64 stri…] | lang=en
- "agent_scope_crypt_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=agent/scope_crypt.py:L55 | neighbors=[scope_crypt.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…] | lang=en
- "agent_scope_crypt_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=agent/scope_crypt.py:L150 | neighbors=[scope_crypt.py, encrypt_scope(), encrypt_scope() returning a base64 stri…] | lang=en
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target()] | lang=en
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target()] | lang=en
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=agent/task_runner.py:L27 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job()] | lang=en
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=agent/task_runner.py:L442 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job()] | lang=en
- "agent_transport_enrollment_conflict_detail": "_enrollment_conflict_detail()" | kind=code-symbol | source=agent/transport.py:L64 | neighbors=[transport.py, Best-effort extraction of the manager's…, .create_enrollment_request()] | lang=en
- "agent_transport_strip_nul": "_strip_nul()" | kind=code-symbol | source=agent/transport.py:L31 | neighbors=[transport.py, Recursively remove NUL (U+0000) charact…, .submit_result()] | lang=en
- "agent_transport_transport_activate_enrollment": ".activate_enrollment()" | kind=code-symbol | source=agent/transport.py:L369 | neighbors=[Transport, .load_state(), .update_state()] | lang=en
- "agent_transport_transport_create_enrollment_request": ".create_enrollment_request()" | kind=code-symbol | source=agent/transport.py:L350 | neighbors=[Transport, DeviceAlreadyEnrolledError, _enrollment_conflict_detail()] | lang=en
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=agent/transport.py:L507 | neighbors=[Send a heartbeat to the manager.       …, Transport, .ensure_device_access()] | lang=en
- "agent_validation_validate_ground_truth": "validate_ground_truth()" | kind=code-symbol | source=agent/validation.py:L106 | neighbors=[validation.py, Validate the small, explicit inventory …, score_inventory()] | lang=en
- "branch:repo:local/probe@20f2a9dc#feat/wire-osfp-service-enum": "feat/wire-osfp-service-enum" | kind=Branch | source=git | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, de583d8 feat(workflow): wire os_fingerp…] | lang=en
- "main_scripts_accuracy_main": "_main()" | kind=code-symbol | source=main_scripts/accuracy.py:L163 | neighbors=[accuracy.py, evaluate_corpus(), format_report()] | lang=en
- "main_scripts_accuracy_observed_states": "_observed_states()" | kind=code-symbol | source=main_scripts/accuracy.py:L79 | neighbors=[accuracy.py, (target, port) -> status, from port/syn…, score_port_states()] | lang=en
- "main_scripts_accuracy_ratio": "_ratio()" | kind=code-symbol | source=main_scripts/accuracy.py:L26 | neighbors=[accuracy.py, score_findings(), score_port_states()] | lang=en
- "main_scripts_adaptive_timeout_adaptivetimeout_observe": ".observe()" | kind=code-symbol | source=main_scripts/adaptive_timeout.py:L31 | neighbors=[AdaptiveTimeout, from_rtts(), Fold one round-trip sample (seconds) in…] | lang=en
- "main_scripts_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=main_scripts/db_scanner.py:L266 | neighbors=[DBScanner, ._probe_one(), .scan_target()] | lang=en
- "main_scripts_db_scanner_interpret_redis_info": "interpret_redis_info()" | kind=code-symbol | source=main_scripts/db_scanner.py:L101 | neighbors=[db_scanner.py, _probe_redis(), Classify a Redis INFO reply. `unauthent…] | lang=en
- "main_scripts_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L121 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…] | lang=en
- "main_scripts_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L138 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string.] | lang=en
- "main_scripts_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L296 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…] | lang=en
- "main_scripts_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=main_scripts/delta_scanner.py:L53 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…] | lang=en
- "main_scripts_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…] | lang=en
- "main_scripts_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…] | lang=en
- "main_scripts_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=main_scripts/device_classifier.py:L98 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…] | lang=en
- "main_scripts_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=main_scripts/device_classifier.py:L201 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…] | lang=en
- "main_scripts_findings_is_open": "_is_open()" | kind=code-symbol | source=main_scripts/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()] | lang=en
- "main_scripts_findings_summarize": "summarize()" | kind=code-symbol | source=main_scripts/findings.py:L1175 | neighbors=[findings.py, _main(), _tally()] | lang=en
- "main_scripts_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=main_scripts/host_discovery.py:L398 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…] | lang=en
- "main_scripts_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=main_scripts/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…] | lang=en
- "main_scripts_host_discovery_rationale_1": "host_discovery.py — determine which hosts are alive, with graded confidence.  ME" | kind=entity | source=main_scripts/host_discovery.py:L1 | neighbors=[host_discovery.py, BaseScanner, ScanResult] | lang=en
- "main_scripts_host_discovery_rationale_112": "Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower." | kind=entity | source=main_scripts/host_discovery.py:L112 | neighbors=[normalize_mac(), BaseScanner, ScanResult] | lang=en
- "main_scripts_host_discovery_rationale_126": "True if the 2nd-least-significant bit of the first octet is set —     i.e. a loc" | kind=entity | source=main_scripts/host_discovery.py:L126 | neighbors=[is_locally_administered(), BaseScanner, ScanResult] | lang=en
- "main_scripts_host_discovery_rationale_143": "Best-effort device classification from the L2/L3 evidence." | kind=entity | source=main_scripts/host_discovery.py:L143 | neighbors=[device_hint(), BaseScanner, ScanResult] | lang=en
- "main_scripts_host_discovery_rationale_196": "One OS neighbor-cache observation about a target, with graded freshness." | kind=entity | source=main_scripts/host_discovery.py:L196 | neighbors=[Neighbor, BaseScanner, ScanResult] | lang=pt
- "main_scripts_host_discovery_rationale_203": "Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.      Handles bo" | kind=entity | source=main_scripts/host_discovery.py:L203 | neighbors=[parse_neighbor_line(), BaseScanner, ScanResult] | lang=pt
- "main_scripts_host_discovery_rationale_233": "Targeted, POST-probe neighbor lookup for a single IP (unprivileged).      Reads" | kind=entity | source=main_scripts/host_discovery.py:L233 | neighbors=[read_neighbor(), BaseScanner, ScanResult] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-026.json

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
