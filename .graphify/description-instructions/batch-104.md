# Node Description Batch 105 of 380

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

- "detection_edr_crowdstrikefalcon_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L118 | neighbors=[CrowdStrikeFalcon, EDRDetection, _parse_dt()]
- "detection_edr_microsoftdefender_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L158 | neighbors=[MicrosoftDefender, EDRDetection, _parse_dt()]
- "detection_edr_sentinelone_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L209 | neighbors=[SentinelOne, EDRDetection, _parse_dt()]
- "detection_engine_ai_normalizer_ainormalizercache_key": "._key()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L149 | neighbors=[AINormalizerCache, .get(), .put()]
- "detection_engine_ai_normalizer_ainormalizercache_put": ".put()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L155 | neighbors=[AINormalizerCache, ._key(), propose_candidates()]
- "detection_engine_ai_normalizer_extract_raw_text": "extract_raw_text()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L206 | neighbors=[ai_normalizer.py, .get(), The raw observable text worth sending t…]
- "detection_engine_ai_normalizer_rationale_1": "ai_normalizer.py — Phase 2: AI normalization assist, gated by deterministic look" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[ai_normalizer.py, CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_124": "Test double — a fixed lookup table, no network. Used to validate the     surroun" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L124 | neighbors=[FakeAIClient, CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_170": "True iff the real NVD CPE dictionary has at least one entry for this     vendor:" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L170 | neighbors=[validate_cpe_exists(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_207": "The raw observable text worth sending to the AI normalizer for this     Fact's s" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L207 | neighbors=[extract_raw_text(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_233": "The Phase 2 entry point. raw_text is whatever observed string the     rule-based" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L233 | neighbors=[propose_candidates(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_90": "Returns a list of {\"vendor\", \"product\", \"version\"} dicts —         exactly the v" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L90 | neighbors=[.propose_cpe(), CPECandidate, Fact]
- "detection_engine_ai_normalizer_rationale_97": "Real implementation, gated behind the anthropic SDK + an API key.     Forces the" | kind=entity | source=manager/detection_engine/ai_normalizer.py:L97 | neighbors=[AnthropicAIClient, CPECandidate, Fact]
- "detection_engine_bridge_load_remediated_index": "_load_remediated_index()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L312 | neighbors=[engine_bridge.py, create_findings_from_facts(), The regression candidates, in ONE query…]
- "detection_engine_bridge_run_detection_engine": "_run_detection_engine()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L169 | neighbors=[engine_bridge.py, create_findings_from_facts(), `detect_all_from_facts_traced` on a wor…]
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
- "detection_engine_default_creds_catalog": "default_creds_catalog.py" | kind=code-symbol | source=manager/detection_engine/default_creds_catalog.py:L1 | neighbors=[831bdef feat(detection): default-creden…, has_known_defaults(), default_creds_catalog.py — vendors that…]
- "detection_engine_enrichment_compute_priority": "_compute_priority()" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L52 | neighbors=[enrichment.py, enrich_finding(), Returns (tier, human-readable reason). …]
- "detection_engine_enrichment_db_cache_key": "_cache_key()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L50 | neighbors=[enrichment_db.py, load_epss(), load_kev()]
- "detection_engine_enrichment_enrich_finding": "enrich_finding()" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L32 | neighbors=[enrichment.py, _compute_priority(), Mutates and returns `finding` with cvss…]
- "detection_engine_eol_catalog": "eol_catalog.py" | kind=code-symbol | source=manager/detection_engine/eol_catalog.py:L1 | neighbors=[c1c3bcc feat(detection): flag end-of-li…, lookup_eol(), eol_catalog.py — curated end-of-life / …]
- "detection_engine_exploitability_priority_for": "priority_for()" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L208 | neighbors=[exploitability.py, apply_to_findings(), The band table posture_rules.compute_ri…]
- "detection_engine_ingest_ingest_files": "ingest_files()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L186 | neighbors=[ingest.py, ingest_file(), IngestResult]
- "detection_engine_ingest_ingestresult_get_or_create_asset": ".get_or_create_asset()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L59 | neighbors=[ingest_file(), IngestResult, _is_ip()]
- "detection_engine_matcher_match_candidate": "match_candidate()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L80 | neighbors=[matcher.py, _version_in_ranges(), All Findings this single CPE candidate …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-104.json

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
