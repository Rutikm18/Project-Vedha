# Node Description Batch 61 of 330

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
- "services_validation_ingest": "validation_ingest.py" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's s…]
- "supporting_research_evidence_store_retroactive_detect": "retroactive_detect()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L296 | neighbors=[evidence_store.py, Answer a brand-new rule against evidenc…, AssetVerdict, _iso(), time_travel()]
- "supporting_research_evidence_store_unionfind": "_UnionFind" | kind=code-symbol | source=Supporting_research/evidence_store.py:L146 | neighbors=[evidence_store.py, resolve_identity(), .find(), .__init__(), .union()]
- "tests_conftest": "conftest.py" | kind=code-symbol | source=probe/tests/conftest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 8f6bf49 Refactor code structure and rem…, _isolate_result_archive(), pytest_configure(), 2885afa Add comprehensive probe testing…]
- "tests_test_active_validation_interpret": "test_active_validation_interpret.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L1 | neighbors=[7bd104a feat(active-validation): pure r…, test_confirmed_upgrades_and_sets_exploi…, test_contradicted_marks_false_positive(), test_inconclusive_keeps_state_unchanged…, test_missing_or_garbage_result_is_incon…]
- "tests_test_ad_assessment_enum_with_entries": "_enum_with_entries()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L45 | neighbors=[test_ad_assessment.py, .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_adaptive_rate_testudpretransmit": "TestUdpRetransmit" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L119 | neighbors=[test_adaptive_rate.py, .test_retries_exhaust_on_silence(), .test_retry_recovers_dropped_reply(), .test_returns_immediately_on_closed(), .test_returns_immediately_on_reply()]

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
