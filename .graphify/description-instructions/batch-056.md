# Node Description Batch 57 of 131

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

- "detection_edr_sentinelone_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L193 | neighbors=[SentinelOne, ._request()]
- "detection_engine_ai_normalizer_aiclient_propose_cpe": ".propose_cpe()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L89 | neighbors=[AIClient, Returns a list of {"vendor", "product",…]
- "detection_engine_ai_normalizer_anthropicaiclient_propose_cpe": ".propose_cpe()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L108 | neighbors=[AnthropicAIClient, .get()]
- "detection_engine_ai_normalizer_fakeaiclient_propose_cpe": ".propose_cpe()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L134 | neighbors=[FakeAIClient, .get()]
- "detection_engine_consistency_findingconsistency_ci": ".ci()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L63 | neighbors=[FindingConsistency, wilson_ci()]
- "detection_engine_consistency_format_line": "format_line()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L130 | neighbors=[consistency.py, The spec's reporting line, e.g.:     'H…]
- "detection_engine_consistency_rationale_1": "consistency.py — Phase 5: N-run consistency & reporting.  \"A single scan is an a" | kind=entity | source=manager/detection_engine/consistency.py:L1 | neighbors=[consistency.py, Finding]
- "detection_engine_consistency_rationale_102": "run_findings: one list of Findings per run (N runs). Aggregated by     the deter" | kind=entity | source=manager/detection_engine/consistency.py:L102 | neighbors=[aggregate(), Finding]
- "detection_engine_consistency_rationale_131": "The spec's reporting line, e.g.:     'Host 10.0.0.5 — CVE-2021-41773 in 27/30 ru" | kind=entity | source=manager/detection_engine/consistency.py:L131 | neighbors=[format_line(), Finding]
- "detection_engine_consistency_rationale_33": "Wilson score interval for a binomial proportion k/n, as percentages.     Chosen" | kind=entity | source=manager/detection_engine/consistency.py:L33 | neighbors=[wilson_ci(), Finding]
- "detection_engine_correlate_correlate_smb_patch": "correlate_smb_patch()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L134 | neighbors=[correlate.py, SMBv1 enabled + (credentialed hotfix li…]
- "detection_engine_correlate_dedup_findings": "dedup_findings()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L35 | neighbors=[correlate.py, Collapse by finding_id (deterministic: …]
- "detection_engine_cpe_normalizer_all_osv_source_packages": "all_osv_source_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L359 | neighbors=[cpe_normalizer.py, Every distinct OSV source-package name …]
- "detection_engine_cpe_normalizer_clean_rpm_version": "clean_rpm_version()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L92 | neighbors=[cpe_normalizer.py, rpm queried as '%{VERSION}-%{RELEASE}' …]
- "detection_engine_cpe_normalizer_normalize": "normalize()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L350 | neighbors=[cpe_normalizer.py, Dispatch a single Fact to the right par…]
- "detection_engine_cpe_normalizer_osv_source_packages": "osv_source_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L149 | neighbors=[cpe_normalizer.py, Every distinct OSV source-package name …]
- "detection_engine_cvss_parse_vector": "parse_vector()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L33 | neighbors=[cvss.py, base_score()]
- "detection_engine_enrichment_db_epssdb_get": ".get()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L28 | neighbors=[EpssDB, {'epss': float, 'percentile': float} or…]
- "detection_engine_enrichment_db_load_epss": "load_epss()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L39 | neighbors=[enrichment_db.py, EpssDB]
- "detection_engine_enrichment_db_load_kev": "load_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L33 | neighbors=[enrichment_db.py, KevDB]
- "detection_engine_ingest_classify_confidence": "_classify_confidence()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L54 | neighbors=[ingest.py, ingest_file()]
- "detection_engine_ingest_is_ip": "_is_ip()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L74 | neighbors=[ingest.py, .get_or_create_asset()]
- "detection_engine_init": "__init__.py" | kind=code-symbol | source=manager/detection_engine/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]
- "detection_engine_models_asset_add_fact": ".add_fact()" | kind=code-symbol | source=manager/detection_engine/models.py:L90 | neighbors=[Asset, .as_of()]
- "detection_engine_models_fact_ref": ".ref()" | kind=code-symbol | source=manager/detection_engine/models.py:L60 | neighbors=[Fact, A stable, human-readable pointer back t…]
- "detection_engine_models_make_finding_id": "make_finding_id()" | kind=code-symbol | source=manager/detection_engine/models.py:L125 | neighbors=[models.py, Deterministic finding ID: the SAME (ass…]
- "detection_engine_update_snapshot_all_known_cve_ids": "_all_known_cve_ids()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L174 | neighbors=[update_snapshot.py, main()]
- "detection_engine_verifier_deception_score": "deception_score()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L75 | neighbors=[verifier.py, A starter honeypot/deception heuristic …]
- "detection_engine_version_compare_split_segments": "_split_segments()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L78 | neighbors=[version_compare.py, _compare_part()]
- "detection_engine_vuln_db_default_products": "_default_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L43 | neighbors=[vuln_db.py, Derives the synced product list from cp…]
- "detection_engine_vuln_db_vulndb_build_cve_index": "._build_cve_index()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L89 | neighbors=[VulnDB, .__init__()]
- "detection_engine_vuln_db_vulndb_get_cvss_vector": ".get_cvss_vector()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L109 | neighbors=[The CVSS v3 vector string OSV embedded …, VulnDB]
- "detection_engine_vuln_db_vulndb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L83 | neighbors=[VulnDB, ._build_cve_index()]
- "detection_engine_vuln_db_vulndb_lookup": ".lookup()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L98 | neighbors=[Raw OSV vulnerability records for this …, VulnDB]
- "detection_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/detection/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "detection_logger_as_uuid": "_as_uuid()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L69 | neighbors=[logger.py, .log_action()]
- "detection_logger_rationale_1": "AttackLogger — records every attack action to the ``attack_timeline`` table.  Al" | kind=entity | source=manager/backend/app/detection/logger.py:L1 | neighbors=[logger.py, AttackTimeline]
- "detection_logger_rationale_40": "Persist a single attack action. Returns the AttackTimeline row.          ``times" | kind=entity | source=manager/backend/app/detection/logger.py:L40 | neighbors=[.log_action(), AttackTimeline]
- "detection_siem_elasticsiem_build_query": ".build_query()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L191 | neighbors=[ElasticSIEM, .query_alerts()]
- "detection_siem_sentinelsiem_build_kql": ".build_kql()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L141 | neighbors=[SentinelSIEM, .query_alerts()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-056.json

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
