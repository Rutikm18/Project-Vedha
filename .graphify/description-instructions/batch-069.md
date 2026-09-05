# Node Description Batch 70 of 336

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

- "detection_engine_consistency_aggregate": "aggregate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L100 | neighbors=[consistency.py, ConsistencyReport, FindingConsistency, run_findings: one list of Findings per …] | lang=en
- "detection_engine_correlate_suppressionrecord": "SuppressionRecord" | kind=code-symbol | source=manager/detection_engine/correlate.py:L37 | neighbors=[correlate.py, Why a candidate finding was omitted fro…, suppress_negated_with_audit(), .to_dict()] | lang=en
- "detection_engine_cpe_normalizer_all_osv_source_packages": "all_osv_source_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L413 | neighbors=[cpe_normalizer.py, Every distinct OSV source-package name …, Every distinct OSV source-package name …, Every distinct OSV source-package name …] | lang=en
- "detection_engine_cpe_normalizer_normalize": "normalize()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L404 | neighbors=[cpe_normalizer.py, Dispatch a single Fact to the right par…, Dispatch a single Fact to the right par…, Dispatch a single Fact to the right par…] | lang=en
- "detection_engine_cvss_base_score": "base_score()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L43 | neighbors=[cvss.py, parse_vector(), _roundup(), Returns the CVSS v3.1 base score (0.0-1…] | lang=en
- "detection_engine_enrichment_db_load_epss": "load_epss()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L69 | neighbors=[enrichment_db.py, _cache_key(), EpssDB, .get()] | lang=en
- "detection_engine_enrichment_db_load_kev": "load_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L55 | neighbors=[enrichment_db.py, _cache_key(), .get(), KevDB] | lang=en
- "detection_engine_exploitability_apply_to_findings": "apply_to_findings()" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L173 | neighbors=[exploitability.py, assess(), priority_for(), Enrich posture findings in place with e…] | lang=en
- "detection_engine_ingest_extract_aliases": "_extract_aliases()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L101 | neighbors=[ingest.py, ingest_file(), Real, verified hostname-alias sources i…, Real, verified hostname-alias sources i…] | lang=en
- "detection_engine_ingest_rationale_1": "ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host" | kind=entity | source=manager/detection_engine/ingest.py:L1 | neighbors=[ingest.py, Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_100": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L100 | neighbors=[ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_60": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L60 | neighbors=[_validate(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_83": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L83 | neighbors=[_extract_aliases(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_validate": "_validate()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L70 | neighbors=[ingest.py, ingest_file(), Returns an error reason string if inval…, Returns an error reason string if inval…] | lang=en
- "detection_engine_matcher_version_in_ranges": "_version_in_ranges()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L44 | neighbors=[matcher.py, match_candidate(), Returns (matched, matched_interval_desc…, _safe_compare()] | lang=en
- "detection_engine_pipeline_ab_evaluate": "ab_evaluate()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L179 | neighbors=[pipeline.py, run_pipeline(), Phase 2 exit criteria: recall gain from…, Phase 2 exit criteria: recall gain from…] | lang=en
- "detection_engine_port_intel_contradicts_port_hypothesis": "contradicts_port_hypothesis()" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L201 | neighbors=[port_intel.py, classify_port(), _normalized(), True when an identified product proves …] | lang=en
- "detection_engine_posture_confidence_assess_confidence": "assess_confidence()" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L78 | neighbors=[posture_confidence.py, corroborating_chains(), calibrate_host_findings(), Return (confidence 0-100, precision_fac…] | lang=en
- "detection_engine_posture_rules_cert": "_cert()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L330 | neighbors=[posture_rules.py, _d(), _tls_expired(), _tls_self_signed()] | lang=en
- "detection_engine_posture_rules_compute_risk": "compute_risk()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L133 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced(), severity × exposure × state → (risk_sco…] | lang=en
- "detection_engine_posture_rules_detect_posture": "detect_posture()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L908 | neighbors=[posture_rules.py, detect_all(), detect_posture_traced(), Apply every posture rule to one asset's…] | lang=en
- "detection_engine_posture_rules_make_posture_id": "make_posture_id()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L161 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced(), Deterministic id — same (asset, rule, p…] | lang=en
- "detection_engine_posture_rules_state_for": "_state_for()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L756 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced(), is_validated()] | lang=en
- "detection_engine_update_snapshot_query_osv": "_query_osv()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L54 | neighbors=[update_snapshot.py, _ssl_context(), All known vulnerabilities OSV has for t…, sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_sync_epss_full": "sync_epss_full()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L177 | neighbors=[update_snapshot.py, main(), The ENTIRE EPSS catalog (every scored C…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_snapshot": "sync_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L76 | neighbors=[update_snapshot.py, main(), Fetch real OSV records for every produc…, _query_osv()] | lang=en
- "detection_engine_verifier_rationale_1": "verifier.py — Phase 3: the generalized verifier, the anti-false-positive backbon" | kind=entity | source=manager/detection_engine/verifier.py:L1 | neighbors=[verifier.py, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_verifier_rationale_52": "The scanner names behind this finding's evidence refs. A ref looks     like 'fil" | kind=entity | source=manager/detection_engine/verifier.py:L52 | neighbors=[_evidence_scanners(), Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_verifier_rationale_76": "A starter honeypot/deception heuristic (0.0-1.0). Real hosts run a     handful o" | kind=entity | source=manager/detection_engine/verifier.py:L76 | neighbors=[deception_score(), Finding, FindingState, SourceConfidence] | lang=pt
- "detection_engine_verifier_rationale_96": "Calibrate and stamp a Finding. Mutates and returns it.      reachability: \"open\"" | kind=entity | source=manager/detection_engine/verifier.py:L96 | neighbors=[verify(), Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_version_compare_char_order": "_char_order()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L58 | neighbors=[version_compare.py, _compare_non_digit(), dpkg's non-digit character ordering: '~…, dpkg's non-digit character ordering: '~…] | lang=en
- "detection_engine_version_compare_has_ambiguous_epoch": "has_ambiguous_epoch()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L129 | neighbors=[version_compare.py, _split_dpkg_version(), True when exactly one of the two versio…, True when exactly one of the two versio…] | lang=en
- "detection_engine_version_compare_semver_compare": "semver_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L189 | neighbors=[version_compare.py, Plain dotted-numeric comparison for non…, _compare_part(), Plain dotted-numeric comparison for non…] | lang=en
- "detection_engine_vuln_db_boundary_versions": "_boundary_versions()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L143 | neighbors=[vuln_db.py, Every version string that appears as a …, _read_snapshot(), Every version string that appears as a …] | lang=en
- "detection_engine_vuln_db_default_products": "_default_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L50 | neighbors=[vuln_db.py, Derives the synced product list from cp…, Derives the synced product list from cp…, Derives the synced product list from cp…] | lang=en
- "detection_engine_vuln_db_vulndb_get_cvss_vector": ".get_cvss_vector()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L116 | neighbors=[The CVSS v3 vector string OSV embedded …, VulnDB, The CVSS v3 vector string OSV embedded …, The CVSS v3 vector string OSV embedded …] | lang=en
- "detection_engine_vuln_db_vulndb_lookup": ".lookup()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L105 | neighbors=[Raw OSV vulnerability records for this …, VulnDB, Raw OSV vulnerability records for this …, Raw OSV vulnerability records for this …] | lang=en
- "detection_exposure_fusion_service": "exposure_fusion_service.py" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, recompute_fused_exposure(), _results_from_scan_rows(), exposure_fusion_service.py — apply mult…] | lang=en
- "detection_logger_attacklogger": "AttackLogger" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L23 | neighbors=[logger.py, .__init__(), .log_action(), AttackTimeline] | lang=en
- "detection_prioritization_composite_risk_score": "composite_risk_score()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L90 | neighbors=[prioritization.py, prioritize_engagement_findings(), Compatibility wrapper around the canoni…, The unified 0-1000 composite (see modul…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-069.json

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
