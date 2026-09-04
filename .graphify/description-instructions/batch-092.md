# Node Description Batch 93 of 330

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

- "detection_engine_ai_normalizer_rationale_233": "The Phase 2 entry point. raw_text is whatever observed string the     rule-based" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L233 | neighbors=[propose_candidates(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_90": "Returns a list of {\"vendor\", \"product\", \"version\"} dicts —         exactly the v" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L90 | neighbors=[.propose_cpe(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_97": "Real implementation, gated behind the anthropic SDK + an API key.     Forces the" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L97 | neighbors=[AnthropicAIClient, CPECandidate, Fact]
- "detection_engine_bridge_accepted": "_accepted()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L138 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), The subset of `facts` ingest accepted. …]
- "detection_engine_bridge_detect_all_from_facts": "detect_all_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L251 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), Backward-compatible (cve, posture) view…]
- "detection_engine_bridge_ingest_census": "_ingest_census()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L104 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), (census, rejected_line_numbers) from th…]
- "detection_engine_bridge_log_ingest_health": "_log_ingest_health()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L148 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), Escalate by severity of loss. A TOTAL w…]
- "detection_engine_bridge_posture_title": "_posture_title()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L271 | neighbors=[engine_bridge.py, _persist_posture_findings(), Stable, human title for a posture findi…]
- "detection_engine_consistency_wilson_ci": "wilson_ci()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L32 | neighbors=[consistency.py, .ci(), Wilson score interval for a binomial pr…]
- "detection_engine_correlate_correlate_smb_patch": "correlate_smb_patch()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L177 | neighbors=[correlate.py, SMBv1 enabled + (credentialed hotfix li…, SMBv1 enabled + (credentialed hotfix li…]
- "detection_engine_correlate_dedup_findings": "dedup_findings()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L54 | neighbors=[correlate.py, Collapse by finding_id (deterministic: …, Collapse by finding_id (deterministic: …]
- "detection_engine_cpe_normalizer_clean_debian_version": "clean_debian_version()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L77 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), dpkg version syntax: [epoch:]upstream_v…]
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
- "detection_engine_enrichment_db_cache_key": "_cache_key()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L50 | neighbors=[enrichment_db.py, load_epss(), load_kev()]
- "detection_engine_enrichment_enrich_finding": "enrich_finding()" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L32 | neighbors=[enrichment.py, _compute_priority(), Mutates and returns `finding` with cvss…]
- "detection_engine_exploitability_priority_for": "priority_for()" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L208 | neighbors=[exploitability.py, apply_to_findings(), The band table posture_rules.compute_ri…]
- "detection_engine_ingest_ingest_files": "ingest_files()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L186 | neighbors=[ingest.py, ingest_file(), IngestResult]
- "detection_engine_ingest_ingestresult_get_or_create_asset": ".get_or_create_asset()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L59 | neighbors=[ingest_file(), IngestResult, _is_ip()]
- "detection_engine_matcher_match_candidate": "match_candidate()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L80 | neighbors=[matcher.py, _version_in_ranges(), All Findings this single CPE candidate …]
- "detection_engine_matcher_safe_compare": "_safe_compare()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L33 | neighbors=[matcher.py, dpkg_compare, but None instead of a mis…, _version_in_ranges()]
- "detection_engine_models_asset_as_of": ".as_of()" | kind=code-symbol | source=manager/detection_engine/models.py:L107 | neighbors=[Asset, .add_fact(), Reconstruct this asset using only facts…]
- "detection_engine_pipeline_run_full_detection": "run_full_detection()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L123 | neighbors=[pipeline.py, Unified detection over one set of inges…, run_pipeline()]
- "detection_engine_posture_confidence_calibrate_host_findings": "calibrate_host_findings()" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L119 | neighbors=[posture_confidence.py, assess_confidence(), Second pass over ONE host's posture fin…]
- "detection_engine_posture_confidence_corroborating_chains": "corroborating_chains()" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L68 | neighbors=[posture_confidence.py, assess_confidence(), Chains this rule belongs to where ≥1 OT…]
- "detection_engine_posture_rules_calibrate_host_findings": "_calibrate_host_findings()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L815 | neighbors=[posture_rules.py, detect_posture_traced(), Best-effort confidence calibration (laz…]
- "detection_engine_posture_rules_detect_all": "detect_all()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1091 | neighbors=[posture_rules.py, detect_posture(), Run posture detection across every asse…]
- "detection_engine_posture_rules_detect_all_traced": "detect_all_traced()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1076 | neighbors=[posture_rules.py, detect_posture_traced(), Traced counterpart of `detect_all` — fi…]
- "detection_engine_posture_rules_evidence_ref": "_evidence_ref()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L761 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-092.json

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
