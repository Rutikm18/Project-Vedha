# Node Description Batch 68 of 227

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

- "detection_engine_enrichment_enrich_finding": "enrich_finding()" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L32 | neighbors=[enrichment.py, _compute_priority(), Mutates and returns `finding` with cvss…]
- "detection_engine_ingest_extract_aliases": "_extract_aliases()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L82 | neighbors=[ingest.py, ingest_file(), Real, verified hostname-alias sources i…]
- "detection_engine_ingest_ingest_files": "ingest_files()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L153 | neighbors=[ingest.py, ingest_file(), IngestResult]
- "detection_engine_ingest_ingestresult_get_or_create_asset": ".get_or_create_asset()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L48 | neighbors=[ingest_file(), IngestResult, _is_ip()]
- "detection_engine_ingest_validate": "_validate()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L59 | neighbors=[ingest.py, ingest_file(), Returns an error reason string if inval…]
- "detection_engine_matcher_match_candidate": "match_candidate()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L80 | neighbors=[matcher.py, _version_in_ranges(), All Findings this single CPE candidate …]
- "detection_engine_matcher_safe_compare": "_safe_compare()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L33 | neighbors=[matcher.py, dpkg_compare, but None instead of a mis…, _version_in_ranges()]
- "detection_engine_models_asset_as_of": ".as_of()" | kind=code-symbol | source=manager/detection_engine/models.py:L107 | neighbors=[Asset, .add_fact(), Reconstruct this asset using only facts…]
- "detection_engine_pipeline_ab_evaluate": "ab_evaluate()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L109 | neighbors=[pipeline.py, run_pipeline(), Phase 2 exit criteria: recall gain from…]
- "detection_engine_pipeline_run_pipeline": "run_pipeline()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L35 | neighbors=[pipeline.py, ab_evaluate(), exposure: optional {asset_ip: {"interne…]
- "detection_engine_verifier_classify_tier": "classify_tier()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L65 | neighbors=[verifier.py, _evidence_scanners(), verify()]
- "detection_engine_verifier_evidence_scanners": "_evidence_scanners()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L51 | neighbors=[verifier.py, classify_tier(), The scanner names behind this finding's…]
- "detection_engine_verifier_verify": "verify()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L94 | neighbors=[verifier.py, Calibrate and stamp a Finding. Mutates …, classify_tier()]
- "detection_engine_version_compare_compare_non_digit": "_compare_non_digit()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L74 | neighbors=[version_compare.py, _char_order(), _compare_part()]
- "detection_engine_version_compare_load_validation_markers": "_load_validation_markers()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L224 | neighbors=[version_compare.py, _save_validation_marker(), verify_pure_python_matches_dpkg()]
- "detection_engine_version_compare_save_validation_marker": "_save_validation_marker()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L232 | neighbors=[version_compare.py, _load_validation_markers(), verify_pure_python_matches_dpkg()]
- "detection_engine_vuln_db_boundary_versions": "_boundary_versions()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L139 | neighbors=[vuln_db.py, Every version string that appears as a …, _read_snapshot()]
- "detection_engine_vuln_db_default_products": "_default_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L46 | neighbors=[vuln_db.py, Derives the synced product list from cp…, Derives the synced product list from cp…]
- "detection_engine_vuln_db_vulndb_get_cvss_vector": ".get_cvss_vector()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L112 | neighbors=[The CVSS v3 vector string OSV embedded …, VulnDB, The CVSS v3 vector string OSV embedded …]
- "detection_engine_vuln_db_vulndb_lookup": ".lookup()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L101 | neighbors=[Raw OSV vulnerability records for this …, VulnDB, Raw OSV vulnerability records for this …]
- "detection_exposure_fusion_service_recompute_fused_exposure": "recompute_fused_exposure()" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L50 | neighbors=[exposure_fusion_service.py, Fuse all probes' exposure_matrix observ…, _results_from_scan_rows()]
- "detection_exposure_fusion_service_results_from_scan_rows": "_results_from_scan_rows()" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L30 | neighbors=[exposure_fusion_service.py, Reconstruct one {"exposure": [...]} dic…, recompute_fused_exposure()]
- "detection_logger_attacklogger_log_action": ".log_action()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L27 | neighbors=[AttackLogger, _as_uuid(), Persist a single attack action. Returns…]
- "detection_resolution_build_coverage": "build_coverage()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L35 | neighbors=[resolution.py, host_of(), What this run PROVABLY re-observed. An …]
- "detection_resolution_evaluate_resolutions": "evaluate_resolutions()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L90 | neighbors=[resolution.py, decide_resolution(), Apply decide_resolution to every engine…]
- "detection_resolution_host_of": "host_of()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L27 | neighbors=[resolution.py, build_coverage(), IP/host part of a probe target: '10.0.0…]
- "detection_resolution_resolution_threshold": "resolution_threshold()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L57 | neighbors=[resolution.py, decide_resolution(), Consecutive coverage-proven clean runs …]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-067.json

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
