# Node Description Batch 192 of 330

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

- "detection_engine_consistency_consistencyreport_stable": ".stable()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L92 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_findingconsistency_classification": ".classification()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L67 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_consistency_findingconsistency_rate": ".rate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L59 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_correlate_rationale_105": "Apply authoritative-version suppression and preserve every decision.      The ac" | kind=entity | source=manager/detection_engine/correlate.py:L105 | neighbors=[suppress_negated_with_audit()] | lang=en
- "detection_engine_correlate_rationale_158": "The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp" | kind=entity | source=manager/detection_engine/correlate.py:L158 | neighbors=[_product_from_cpe()] | lang=en
- "detection_engine_correlate_rationale_178": "SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS" | kind=entity | source=manager/detection_engine/correlate.py:L178 | neighbors=[correlate_smb_patch()] | lang=en
- "detection_engine_correlate_rationale_38": "Why a candidate finding was omitted from the active result set." | kind=entity | source=manager/detection_engine/correlate.py:L38 | neighbors=[SuppressionRecord] | lang=en
- "detection_engine_correlate_rationale_55": "Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the" | kind=entity | source=manager/detection_engine/correlate.py:L55 | neighbors=[dedup_findings()] | lang=en
- "detection_engine_correlate_rationale_82": "Suppress a suspected/potential (inferred-source) finding when the     SAME host" | kind=entity | source=manager/detection_engine/correlate.py:L82 | neighbors=[suppress_negated()] | lang=en
- "detection_engine_correlate_suppressionrecord_to_dict": ".to_dict()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L50 | neighbors=[SuppressionRecord] | lang=en
- "detection_engine_cpe_normalizer_cpecandidate_cpe23": ".cpe23()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L72 | neighbors=[CPECandidate] | lang=en
- "detection_engine_cpe_normalizer_rationale_220": "service_banner.py's parsed product/version (or raw banner) -> CPE.      Prefers" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L220 | neighbors=[normalize_banner()] | lang=en
- "detection_engine_cpe_normalizer_rationale_251": "service_banner.py's parsed product/version (or raw banner) -> CPE.      Prefers" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L251 | neighbors=[normalize_banner()] | lang=en
- "detection_engine_cpe_normalizer_rationale_255": "web_scanner.py's Server header + tech_hints[] -> CPE candidates." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L255 | neighbors=[normalize_web()] | lang=en
- "detection_engine_cpe_normalizer_rationale_283": "db_scanner.py's real-protocol-handshake engine + server_version -> CPE.      \"my" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L283 | neighbors=[normalize_db()] | lang=en
- "detection_engine_cpe_normalizer_rationale_286": "web_scanner.py's Server header + tech_hints[] -> CPE candidates." | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L286 | neighbors=[normalize_web()] | lang=en
- "detection_engine_cpe_normalizer_rationale_314": "db_scanner.py's real-protocol-handshake engine + server_version -> CPE.      \"my" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L314 | neighbors=[normalize_db()] | lang=en
- "detection_engine_cpe_normalizer_rationale_325": "Yields (package_name, raw_version, upstream_version) for each     'name version'" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L325 | neighbors=[_parse_package_lines()] | lang=en
- "detection_engine_cpe_normalizer_rationale_339": "ssh_inventory's dpkg_packages/rpm_packages -> CPE candidates. ALL high     confi" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L339 | neighbors=[normalize_credentialed_packages()] | lang=en
- "detection_engine_cpe_normalizer_rationale_356": "Yields (package_name, raw_version, upstream_version) for each     'name version'" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L356 | neighbors=[_parse_package_lines()] | lang=en
- "detection_engine_cpe_normalizer_rationale_370": "ssh_inventory's dpkg_packages/rpm_packages -> CPE candidates. ALL high     confi" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L370 | neighbors=[normalize_credentialed_packages()] | lang=en
- "detection_engine_cpe_normalizer_rationale_374": "Dispatch a single Fact to the right parser based on which scanner     produced i" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L374 | neighbors=[normalize()] | lang=en
- "detection_engine_cpe_normalizer_rationale_383": "Every distinct OSV source-package name across ALL three tables     (credentialed" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L383 | neighbors=[all_osv_source_packages()] | lang=en
- "detection_engine_cpe_normalizer_rationale_405": "Dispatch a single Fact to the right parser based on which scanner     produced i" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L405 | neighbors=[normalize()] | lang=en
- "detection_engine_cpe_normalizer_rationale_414": "Every distinct OSV source-package name across ALL three tables     (credentialed" | kind=entity | source=manager/detection_engine/cpe_normalizer.py:L414 | neighbors=[all_osv_source_packages()] | lang=en
- "detection_engine_cvss_rationale_1": "cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network" | kind=entity | source=manager/detection_engine/cvss.py:L1 | neighbors=[cvss.py] | lang=en
- "detection_engine_cvss_rationale_23": "CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r" | kind=entity | source=manager/detection_engine/cvss.py:L23 | neighbors=[_roundup()] | lang=en
- "detection_engine_cvss_rationale_44": "Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin" | kind=entity | source=manager/detection_engine/cvss.py:L44 | neighbors=[base_score()] | lang=en
- "detection_engine_enrichment_db_epssdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L25 | neighbors=[EpssDB] | lang=en
- "detection_engine_enrichment_db_kevdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L16 | neighbors=[KevDB] | lang=en
- "detection_engine_enrichment_db_kevdb_is_kev": ".is_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L20 | neighbors=[KevDB] | lang=en
- "detection_engine_enrichment_db_rationale_1": "enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d" | kind=entity | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[enrichment_db.py] | lang=en
- "detection_engine_enrichment_db_rationale_29": "{'epss': float, 'percentile': float} or None if not covered." | kind=entity | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[.get()] | lang=en
- "detection_engine_enrichment_db_rationale_30": "{'epss': float, 'percentile': float} or None if not covered." | kind=entity | source=manager/detection_engine/enrichment_db.py:L30 | neighbors=[.get()] | lang=en
- "detection_engine_enrichment_db_rationale_44": "Test hook: drop the memoized KEV/EPSS caches so the next load re-reads." | kind=entity | source=manager/detection_engine/enrichment_db.py:L44 | neighbors=[_clear_caches()] | lang=en
- "detection_engine_exploitability_rationale_1": "exploitability.py — join real-world exploitation evidence (CISA KEV + FIRST EPSS" | kind=entity | source=manager/detection_engine/exploitability.py:L1 | neighbors=[exploitability.py] | lang=en
- "detection_engine_exploitability_rationale_131": "Exploitability evidence for one posture rule.      Returns {kev_refs, epss_max," | kind=entity | source=manager/detection_engine/exploitability.py:L131 | neighbors=[assess()] | lang=en
- "detection_engine_exploitability_rationale_174": "Enrich posture findings in place with exploitation evidence and re-rank.      Th" | kind=entity | source=manager/detection_engine/exploitability.py:L174 | neighbors=[apply_to_findings()] | lang=en
- "detection_engine_exploitability_rationale_209": "The band table posture_rules.compute_risk uses, shared so a re-rank here     can" | kind=entity | source=manager/detection_engine/exploitability.py:L209 | neighbors=[priority_for()] | lang=en
- "detection_engine_exploitability_rationale_58": "One documented relationship between a posture weakness and a CVE." | kind=entity | source=manager/detection_engine/exploitability.py:L58 | neighbors=[KevLink] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-191.json

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
