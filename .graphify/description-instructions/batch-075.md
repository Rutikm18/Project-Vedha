# Node Description Batch 76 of 332

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

- "routers_portal_portal_use_cases": "_portal_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L75 | neighbors=[portal.py, create_scan_request(), The operator use-case catalog (single s…, The operator use-case catalog (single s…]
- "routers_portal_posture_view": "_posture_view()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L190 | neighbors=[portal.py, portal_posture(), portal_summary(), _enum_val()]
- "routers_probe_enrollment_authenticated_request": "_authenticated_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L477 | neighbors=[probe_enrollment.py, activate_enrollment(), _secret_hash(), poll_enrollment()]
- "routers_probe_enrollment_auto_enroll_cidrs": "auto_enroll_cidrs()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L313 | neighbors=[probe_enrollment.py, approve_request_simple(), _get_or_create_auto_enroll_site(), Parse settings.probe_auto_enroll_cidrs …]
- "routers_probe_enrollment_decode_public_key": "_decode_public_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L78 | neighbors=[probe_enrollment.py, create_enrollment_request(), .validate_key(), _verify_signature()]
- "routers_probe_enrollment_get_or_create_auto_enroll_site": "_get_or_create_auto_enroll_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L321 | neighbors=[probe_enrollment.py, create_enrollment_request(), auto_enroll_cidrs(), The singleton per-tenant Site that trus…]
- "routers_probe_enrollment_refresh_device_token": "refresh_device_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L724 | neighbors=[probe_enrollment.py, _rate_limit(), _secret_hash(), _verify_signature()]
- "routers_probe_enrollment_sitepolicyinput": "SitePolicyInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L148 | neighbors=[probe_enrollment.py, BaseModel, .require_site_reference(), .validate_networks()]
- "routers_probe_enrollment_verify_signature": "_verify_signature()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L88 | neighbors=[probe_enrollment.py, activate_enrollment(), refresh_device_token(), _decode_public_key()]
- "routers_remediation_build_upsert_stmt": "_build_upsert_stmt()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L64 | neighbors=[remediation.py, Build the atomic INSERT … ON CONFLICT D…, _upsert_plan(), Build the atomic INSERT … ON CONFLICT D…]
- "routers_remediation_get_remediation": "get_remediation()" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L122 | neighbors=[remediation.py, _cached_plan(), _serialize(), _tenant_finding()]
- "routers_sla_policy_resolve_windows": "resolve_windows()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L58 | neighbors=[sla_policy.py, The tenant's custom SLA windows if set,…, _row(), _windows_of()]
- "routers_sla_policy_row": "_row()" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L47 | neighbors=[sla_policy.py, get_sla_policy(), put_sla_policy(), resolve_windows()]
- "routers_users_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/users.py:L42 | neighbors=[users.py, get_user(), list_users(), UserOut]
- "routers_validation_request_out": "_request_out()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L128 | neighbors=[validation.py, create_validation_request(), list_validation_requests(), ValidationRequestOut]
- "routers_validation_roe_allows_active_validation": "_roe_allows_active_validation()" | kind=code-symbol | source=manager/backend/app/routers/validation.py:L81 | neighbors=[validation.py, approve_validation(), create_validation_request(), RoE gate: active validation is allowed …]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L525 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_accuracy_gate_load_corpus": "load_corpus()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L65 | neighbors=[accuracy_gate.py, load_corpora(), CorpusError, Load and structurally validate one corp…]
- "scanner_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "scanner_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L123 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…, Best-effort service name from data dict…]
- "scanner_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L140 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string., Best-effort version string.]
- "scanner_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L298 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…, Heuristic priority for a newly-detected…]
- "scanner_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L55 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…, Normalised representation of one ScanRe…]
- "scanner_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L310 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…, True if version changed in a security-r…]
- "scanner_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L93 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…, Derive a stable host identity from a ra…]
- "scanner_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L110 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…, Fuse OS family + open ports + service p…]
- "scanner_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L237 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…, Convenience adapter: extract classifier…]
- "scanner_dns_scanner_dnsscanner_ptr_self": "._ptr_self()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L119 | neighbors=[DNSScanner, ._probe(), _is_ip(), Ask the target (as a resolver) for the …]
- "scanner_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/scanner/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "scanner_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=probe/scanner/findings.py:L254 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=probe/scanner/findings.py:L277 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_ssh": "_rule_ssh()" | kind=code-symbol | source=probe/scanner/findings.py:L582 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=probe/scanner/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=probe/scanner/findings.py:L308 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_web": "_rule_web()" | kind=code-symbol | source=probe/scanner/findings.py:L419 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_ftp_scanner_ftpscanner_cmd": "._cmd()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L91 | neighbors=[FTPScanner, ._read_response(), ._list_bounded(), ._probe()]
- "scanner_host_discovery_hostdiscoveryscanner_udp_liveness": "._udp_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L560 | neighbors=[HostDiscoveryScanner, .scan_target(), ._udp_one(), Run the UDP tier concurrently; return e…]
- "scanner_host_discovery_hostdiscoveryscanner_udp_one": "._udp_one()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L534 | neighbors=[HostDiscoveryScanner, ._udp_liveness(), parse_nbstat(), One UDP liveness probe -> structured si…]
- "scanner_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/scanner/host_discovery.py:L294 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…, One OS neighbor-cache observation about…]
- "scanner_host_discovery_parse_nbstat": "parse_nbstat()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L103 | neighbors=[host_discovery.py, ._udp_one(), normalize_mac(), Parse a NetBIOS NBSTAT (node status) re…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-075.json

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
