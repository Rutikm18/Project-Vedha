# Node Description Batch 38 of 119

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

- "detection_engine_correlate_product_from_cpe": "_product_from_cpe()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L114 | neighbors=[correlate.py, The CPE 'product' field — used as the j…, suppress_negated()]
- "detection_engine_correlate_suppress_negated": "suppress_negated()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L61 | neighbors=[correlate.py, Suppress a suspected/potential (inferre…, _product_from_cpe()]
- "detection_engine_cpe_normalizer_clean_debian_version": "clean_debian_version()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L77 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), dpkg version syntax: [epoch:]upstream_v…]
- "detection_engine_cpe_normalizer_normalize_banner": "normalize_banner()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L213 | neighbors=[cpe_normalizer.py, CPECandidate, service_banner.py's first_line/banner t…]
- "detection_engine_cpe_normalizer_normalize_db": "normalize_db()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L259 | neighbors=[cpe_normalizer.py, CPECandidate, db_scanner.py's real-protocol-handshake…]
- "detection_engine_cpe_normalizer_normalize_web": "normalize_web()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L231 | neighbors=[cpe_normalizer.py, CPECandidate, web_scanner.py's Server header + tech_h…]
- "detection_engine_cpe_normalizer_parse_package_lines": "_parse_package_lines()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L301 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), Yields (package_name, raw_version, upst…]
- "detection_engine_cpe_normalizer_rationale_1": "cpe_normalizer.py — observed strings -> CPE 2.3 candidates, deterministically." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[cpe_normalizer.py, Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_150": "Every distinct OSV source-package name _PACKAGE_TO_CPE covers." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L150 | neighbors=[osv_source_packages(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_214": "service_banner.py's first_line/banner text -> CPE. SSH only for now —     generi" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L214 | neighbors=[normalize_banner(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_232": "web_scanner.py's Server header + tech_hints[] -> CPE candidates." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L232 | neighbors=[normalize_web(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_260": "db_scanner.py's real-protocol-handshake engine + server_version -> CPE.      \"my" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L260 | neighbors=[normalize_db(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_302": "Yields (package_name, raw_version, upstream_version) for each     'name version'" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L302 | neighbors=[_parse_package_lines(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_316": "ssh_inventory's dpkg_packages/rpm_packages -> CPE candidates. ALL high     confi" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L316 | neighbors=[normalize_credentialed_packages(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_351": "Dispatch a single Fact to the right parser based on which scanner     produced i" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L351 | neighbors=[normalize(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_360": "Every distinct OSV source-package name across ALL three tables     (credentialed" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L360 | neighbors=[all_osv_source_packages(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_78": "dpkg version syntax: [epoch:]upstream_version[-debian_revision].     '1:8.4p1-5+" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L78 | neighbors=[clean_debian_version(), Fact, SourceConfidence]
- "detection_engine_cpe_normalizer_rationale_93": "rpm queried as '%{VERSION}-%{RELEASE}' (see ssh_collector.py's     rpm_packages" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L93 | neighbors=[clean_rpm_version(), Fact, SourceConfidence]
- "detection_engine_cvss_roundup": "_roundup()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L22 | neighbors=[cvss.py, base_score(), CVSS spec's exact rounding rule (avoids…]
- "detection_engine_enrichment_compute_priority": "_compute_priority()" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L52 | neighbors=[enrichment.py, enrich_finding(), Returns (tier, human-readable reason). …]
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
- "detection_engine_version_compare_char_order": "_char_order()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L52 | neighbors=[version_compare.py, _compare_non_digit(), dpkg's non-digit character ordering: '~…]
- "detection_engine_version_compare_compare_non_digit": "_compare_non_digit()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L68 | neighbors=[version_compare.py, _char_order(), _compare_part()]
- "detection_engine_version_compare_dpkg_compare_via_binary": "_dpkg_compare_via_binary()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L30 | neighbors=[version_compare.py, dpkg_compare(), Real dpkg --compare-versions. None (not…]
- "detection_engine_version_compare_has_ambiguous_epoch": "has_ambiguous_epoch()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L123 | neighbors=[version_compare.py, _split_dpkg_version(), True when exactly one of the two versio…]
- "detection_engine_version_compare_semver_compare": "semver_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L177 | neighbors=[version_compare.py, Plain dotted-numeric comparison for non…, _compare_part()]
- "detection_engine_vuln_db_content_hash": "_content_hash()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L59 | neighbors=[vuln_db.py, load_snapshot(), Stable hash of the snapshot's actual vu…]
- "detection_logger_attacklogger_log_action": ".log_action()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L27 | neighbors=[AttackLogger, _as_uuid(), Persist a single attack action. Returns…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-037.json

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
