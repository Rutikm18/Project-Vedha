# Node Description Batch 106 of 380

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

- "detection_engine_matcher_safe_compare": "_safe_compare()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L33 | neighbors=[matcher.py, dpkg_compare, but None instead of a mis…, _version_in_ranges()]
- "detection_engine_models_asset_as_of": ".as_of()" | kind=code-symbol | source=manager/detection_engine/models.py:L107 | neighbors=[Asset, .add_fact(), Reconstruct this asset using only facts…]
- "detection_engine_pipeline_run_full_detection": "run_full_detection()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L123 | neighbors=[pipeline.py, Unified detection over one set of inges…, run_pipeline()]
- "detection_engine_posture_confidence_calibrate_host_findings": "calibrate_host_findings()" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L119 | neighbors=[posture_confidence.py, assess_confidence(), Second pass over ONE host's posture fin…]
- "detection_engine_posture_confidence_corroborating_chains": "corroborating_chains()" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L68 | neighbors=[posture_confidence.py, assess_confidence(), Chains this rule belongs to where ≥1 OT…]
- "detection_engine_posture_rules_db_auth": "_db_auth()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L650 | neighbors=[posture_rules.py, _d(), Auth posture for risk shaping — only wh…]
- "detection_engine_posture_rules_db_cleartext_transport": "_db_cleartext_transport()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L633 | neighbors=[posture_rules.py, _d(), A database listener that cannot negotia…]
- "detection_engine_posture_rules_db_unauthenticated": "_db_unauthenticated()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L615 | neighbors=[posture_rules.py, _d(), A database that served data to an UNAUT…]
- "detection_engine_posture_rules_default_cred_candidate": "_default_cred_candidate()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L418 | neighbors=[posture_rules.py, _d(), A device from a known-defaults vendor t…]
- "detection_engine_posture_rules_evidence_ref": "_evidence_ref()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L966 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced()]
- "detection_engine_posture_rules_os_eol": "_os_eol()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L459 | neighbors=[posture_rules.py, _d(), An OS past its vendor end-of-SECURITY-s…]
- "detection_engine_posture_rules_summarize_traces": "summarize_traces()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1251 | neighbors=[posture_rules.py, Engagement-level coverage roll-up over …, Engagement-level coverage roll-up over …]
- "detection_engine_posture_rules_verdict_for_rule": "verdict_for_rule()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1233 | neighbors=[posture_rules.py, Collapse every trace for one rule into …, Collapse every trace for one rule into …]
- "detection_engine_verifier_classify_tier": "classify_tier()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L65 | neighbors=[verifier.py, _evidence_scanners(), verify()]
- "detection_engine_verifier_evidence_scanners": "_evidence_scanners()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L51 | neighbors=[verifier.py, classify_tier(), The scanner names behind this finding's…]
- "detection_engine_verifier_verify": "verify()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L94 | neighbors=[verifier.py, Calibrate and stamp a Finding. Mutates …, classify_tier()]
- "detection_engine_version_compare_compare_non_digit": "_compare_non_digit()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L74 | neighbors=[version_compare.py, _char_order(), _compare_part()]
- "detection_engine_version_compare_load_validation_markers": "_load_validation_markers()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L224 | neighbors=[version_compare.py, _save_validation_marker(), verify_pure_python_matches_dpkg()]
- "detection_engine_version_compare_save_validation_marker": "_save_validation_marker()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L232 | neighbors=[version_compare.py, _load_validation_markers(), verify_pure_python_matches_dpkg()]
- "detection_engine_vuln_db_clear_caches": "_clear_caches()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L137 | neighbors=[vuln_db.py, Test hook: drop the memoized snapshot c…, Test hook: drop the memoized snapshot c…]
- "detection_exposure_fusion_service_recompute_fused_exposure": "recompute_fused_exposure()" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L50 | neighbors=[exposure_fusion_service.py, Fuse all probes' exposure_matrix observ…, _results_from_scan_rows()]
- "detection_exposure_fusion_service_results_from_scan_rows": "_results_from_scan_rows()" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L30 | neighbors=[exposure_fusion_service.py, Reconstruct one {"exposure": [...]} dic…, recompute_fused_exposure()]
- "detection_logger_attacklogger_log_action": ".log_action()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L27 | neighbors=[AttackLogger, _as_uuid(), Persist a single attack action. Returns…]
- "detection_siem_elasticsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L219 | neighbors=[ElasticSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_elasticsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L204 | neighbors=[ElasticSIEM, .build_query(), ._request()]
- "detection_siem_sentinelsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L163 | neighbors=[SentinelSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_sentinelsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L152 | neighbors=[SentinelSIEM, .build_kql(), ._request()]
- "detection_siem_splunksiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L107 | neighbors=[SplunkSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_splunksiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L96 | neighbors=[SplunkSIEM, ._request(), .build_spl()]
- "detection_vantage_fusion_collect": "_collect()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L37 | neighbors=[vantage_fusion.py, fuse_exposure_results(), (ip → {(proto,port): {vantage: status}}…]
- "detection_vantage_fusion_fused_service_exposure": "fused_service_exposure()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L118 | neighbors=[vantage_fusion.py, fuse_exposure_results(), (ip, proto, port) → fused exposure verd…]
- "detection_vantage_fusion_is_external": "_is_external()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L30 | neighbors=[vantage_fusion.py, fuse_exposure_results(), _verdict()]
- "detection_vantage_fusion_verdict": "_verdict()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L67 | neighbors=[vantage_fusion.py, fuse_exposure_results(), _is_external()]
- "detection_verification_qualifies_for_llm": "_qualifies_for_llm()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L75 | neighbors=[verification.py, Only spend an LLM call where a rational…, verify_finding()]
- "detection_verification_verificationverdict": "VerificationVerdict" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L29 | neighbors=[verification.py, compute_verdict(), verify_finding()]
- "discovery_device_profile_asset_type_for": "asset_type_for()" | kind=code-symbol | source=manager/backend/app/discovery/device_profile.py:L29 | neighbors=[device_profile.py, device_profiles(), The AssetType for a classifier device_t…]
- "discovery_device_profile_device_profiles": "device_profiles()" | kind=code-symbol | source=manager/backend/app/discovery/device_profile.py:L36 | neighbors=[device_profile.py, asset_type_for(), ip → {asset_type, device_role, role_det…]
- "discovery_finding_translator_load_finding_index": "load_finding_index()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L132 | neighbors=[finding_translator.py, load_open_finding_index(), {(asset_id, title): Finding} for one en…]
- "discovery_finding_translator_load_open_finding_index": "load_open_finding_index()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L156 | neighbors=[finding_translator.py, load_finding_index(), The dedup-suppressing set: what `_find_…]
- "discovery_rate_limiter_ratelimiter_is_within_window": ".is_within_window()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L43 | neighbors=[RateLimiter, .acquire(), True if current time is inside the allo…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-105.json

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
