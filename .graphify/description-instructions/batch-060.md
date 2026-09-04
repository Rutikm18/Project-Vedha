# Node Description Batch 61 of 332

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

- "scanner_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "scanner_ssh_scanner_cursor": "_Cursor" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L72 | neighbors=[ssh_scanner.py, .__init__(), .read(), .read_name_list(), parse_kexinit()]
- "scanner_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L528 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking(), Turn resolved port states + harvested i…, Turn resolved port states + harvested i…]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L178 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L63 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L137 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L242 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "scanner_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L185 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "scanner_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L283 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L313 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L295 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe(), Acquire the concurrency gate (adaptive …, Acquire the concurrency gate (adaptive …]
- "scanner_va_campaign_progressreporter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L174 | neighbors=[ProgressReporter, _monotonic(), _now(), ._flush(), StageState]
- "scanner_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …]
- "schemas_ai_aiproviderstatus": "AiProviderStatus" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L38 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_ai_aistatusresponse": "AiStatusResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L48 | neighbors=[ai.py, BaseModel, AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetIn, AssetOut, BulkAssetImportResult, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_asset_assetin": "AssetIn" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L9 | neighbors=[asset.py, BaseModel, .validate_ip(), AssetCriticality, AssetType]
- "schemas_common": "common.py" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ErrorDetail, paginate(), PaginatedResponse, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_engagement_engagementout": "EngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L92 | neighbors=[engagement.py, EngagementDetail, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_finding_findingfilter": "FindingFilter" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L11 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L108 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slaitem": "SlaItem" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L88 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_finding_slasummary": "SlaSummary" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L98 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_log_warn": "log_warn()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L85 | neighbors=[seed_admin.py, _detect_drift(), _log(), _seed_with_retry(), _validate_env()]
- "scripts_seed_admin_main": "main()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L331 | neighbors=[seed_admin.py, log_error(), log_info(), _seed_with_retry(), _validate_env()]
- "services_agent_policy_evaluate_action": "evaluate_action()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L86 | neighbors=[agent_policy.py, classify_action(), Decision, _deny(), Decide whether `action` may proceed und…]
- "services_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, compute_exposure(), _sev(), Exposure analytics — protocol risk + zo…, 2885afa Add comprehensive probe testing…]
- "services_finding_events_build_timeline": "build_timeline()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L216 | neighbors=[finding_events.py, merge_timeline(), _row_to_dict(), synthesize_events(), The finding's full lifecycle timeline: …]
- "services_finding_events_val": "_val()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L54 | neighbors=[finding_events.py, event_type_for_status(), Accept a FindingEventType/FindingStatus…, record_event(), synthesize_events()]
- "services_job_attempt_service": "job_attempt_service.py" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, config.py, AttemptClaim, claim_job_attempt(), renew_job_attempt()]
- "services_job_result_service_apply_device_profile": "_apply_device_profile()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L437 | neighbors=[job_result_service.py, _promote_assets(), Stamp the probe's evidence-based device…, Stamp the probe's evidence-based device…, Stamp the probe's evidence-based device…]
- "services_job_result_service_identity_ip": "_identity_ip()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L116 | neighbors=[job_result_service.py, Parse a probe identity as an IP, tolera…, validate_result_scope(), Parse a probe identity as an IP, tolera…, Parse a probe identity as an IP, tolera…]
- "services_job_result_service_result_network_identities": "_result_network_identities()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L78 | neighbors=[job_result_service.py, Return network identities that could cr…, validate_result_scope(), Return network identities that could cr…, Return network identities that could cr…]
- "services_llm_http_client": "llm_http_client.py" | kind=code-symbol | source=manager/backend/app/services/llm_http_client.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, AsyncLlmHttpClient, Shared asynchronous HTTP transport for …]
- "services_llm_managerllmservice_ensure_installed_ollama_model": "._ensure_installed_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L411 | neighbors=[ManagerLlmService, AiRuntimeError, ._client(), .generate(), .generate_with_fallback()]
- "services_posture_build_posture": "build_posture()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L159 | neighbors=[posture.py, compare(), compute_scores(), _to_utc(), Full dashboard/report payload. Degrades…]
- "services_posture_compare": "compare()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L120 | neighbors=[posture.py, build_posture(), _present_in_run(), _severity(), Bucket findings across the previous→lat…]
- "services_remediation_kb_classify_finding": "classify_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L79 | neighbors=[remediation_kb.py, _cves(), _text(), Map a finding to a KB category key usin…, recipe_for_finding()]
- "services_scope_targets": "scope_targets.py" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _expand_requested(), _parse_networks(), validate_targets_in_scope(), scope_targets.py — the single source of…]
- "services_sla_slaresult": "SlaResult" | kind=code-symbol | source=manager/backend/app/services/sla.py:L46 | neighbors=[sla.py, compute(), .is_tracked(), FindingStatus, Finding]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-060.json

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
