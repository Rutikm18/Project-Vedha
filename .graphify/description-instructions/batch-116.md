# Node Description Batch 117 of 186

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

- "detection_engine_vuln_db_rationale_110": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L110 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_113": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L113 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_134": "Test hook: drop the memoized snapshot cache so the next load re-reads." | kind=entity | source=manager/detection_engine/vuln_db.py:L134 | neighbors=[_clear_caches()] | lang=en
- "detection_engine_vuln_db_rationale_140": "Every version string that appears as a range boundary in the snapshot —     the" | kind=entity | source=manager/detection_engine/vuln_db.py:L140 | neighbors=[_boundary_versions()] | lang=en
- "detection_engine_vuln_db_rationale_157": "The actual parse + integrity-verify + build. Kept separate from     load_snapsho" | kind=entity | source=manager/detection_engine/vuln_db.py:L157 | neighbors=[_read_snapshot()] | lang=en
- "detection_engine_vuln_db_rationale_44": "Derives the synced product list from cpe_normalizer.py's tables —     the single" | kind=entity | source=manager/detection_engine/vuln_db.py:L44 | neighbors=[_default_products()] | lang=en
- "detection_engine_vuln_db_rationale_47": "Derives the synced product list from cpe_normalizer.py's tables —     the single" | kind=entity | source=manager/detection_engine/vuln_db.py:L47 | neighbors=[_default_products()] | lang=en
- "detection_engine_vuln_db_rationale_60": "Stable hash of the snapshot's actual vulnerability content — recorded     in eve" | kind=entity | source=manager/detection_engine/vuln_db.py:L60 | neighbors=[_content_hash()] | lang=en
- "detection_engine_vuln_db_rationale_63": "Stable hash of the snapshot's actual vulnerability content — recorded     in eve" | kind=entity | source=manager/detection_engine/vuln_db.py:L63 | neighbors=[_content_hash()] | lang=en
- "detection_engine_vuln_db_rationale_79": "In-memory index over a loaded snapshot: product -> OSV vuln records.     Constru" | kind=entity | source=manager/detection_engine/vuln_db.py:L79 | neighbors=[VulnDB] | lang=pt
- "detection_engine_vuln_db_rationale_82": "In-memory index over a loaded snapshot: product -> OSV vuln records.     Constru" | kind=entity | source=manager/detection_engine/vuln_db.py:L82 | neighbors=[VulnDB] | lang=pt
- "detection_engine_vuln_db_rationale_99": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L99 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_vulndb_covers": ".covers()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L109 | neighbors=[VulnDB] | lang=en
- "detection_engine_vuln_db_vulndb_known_products": ".known_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L118 | neighbors=[VulnDB] | lang=en
- "detection_logger_attacklogger_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L24 | neighbors=[AttackLogger] | lang=en
- "detection_resolution_rationale_1": "resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c" | kind=entity | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[resolution.py] | lang=en
- "detection_resolution_rationale_132": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L132 | neighbors=[apply_manual_reopen()] | lang=en
- "detection_resolution_rationale_28": "IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin" | kind=entity | source=manager/backend/app/detection/resolution.py:L28 | neighbors=[host_of()] | lang=en
- "detection_resolution_rationale_36": "What this run PROVABLY re-observed. An asset is covered only if a     completed" | kind=entity | source=manager/backend/app/detection/resolution.py:L36 | neighbors=[build_coverage()] | lang=en
- "detection_resolution_rationale_58": "Consecutive coverage-proven clean runs required before auto-close.     critical/" | kind=entity | source=manager/backend/app/detection/resolution.py:L58 | neighbors=[resolution_threshold()] | lang=en
- "detection_resolution_rationale_73": "Pure heart of auto-resolution. Given whether the finding's asset was     re-obse" | kind=entity | source=manager/backend/app/detection/resolution.py:L73 | neighbors=[decide_resolution()] | lang=en
- "detection_resolution_rationale_93": "Apply decide_resolution to every engine-managed open/confirmed finding     NOT t" | kind=entity | source=manager/backend/app/detection/resolution.py:L93 | neighbors=[evaluate_resolutions()] | lang=en
- "detection_siem_build_siem_engine": "build_siem_engine()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L249 | neighbors=[siem.py] | lang=en
- "detection_siem_rationale_1": "SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic" | kind=entity | source=manager/backend/app/detection/siem.py:L1 | neighbors=[siem.py] | lang=en
- "detection_siem_rationale_135": "Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi" | kind=entity | source=manager/backend/app/detection/siem.py:L135 | neighbors=[SentinelSIEM] | lang=en
- "detection_siem_rationale_185": "Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_" | kind=entity | source=manager/backend/app/detection/siem.py:L185 | neighbors=[ElasticSIEM] | lang=en
- "detection_siem_rationale_51": "Abstract SIEM connector." | kind=entity | source=manager/backend/app/detection/siem.py:L51 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_siem_rationale_82": "Splunk via the REST search endpoint (``/services/search/jobs/export``) with an" | kind=entity | source=manager/backend/app/detection/siem.py:L82 | neighbors=[SplunkSIEM] | lang=en
- "detection_siem_siemqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L55 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_siem_siemqueryengine_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L60 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_sigma_rationale_1": "SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu" | kind=entity | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[sigma.py] | lang=pt
- "detection_sigma_rationale_114": "Return a Sigma rule (YAML string) for the technique, customised with the" | kind=entity | source=manager/backend/app/detection/sigma.py:L114 | neighbors=[.generate_sigma_for_technique()] | lang=en
- "detection_verification_rationale_1": "verification.py — normalized, dashboard-facing verification verdict.  The determ" | kind=entity | source=manager/backend/app/detection/verification.py:L1 | neighbors=[verification.py] | lang=en
- "detection_verification_rationale_46": "Deterministic passive verdict from a detection finding's evidence dict." | kind=entity | source=manager/backend/app/detection/verification.py:L46 | neighbors=[compute_verdict()] | lang=en
- "detection_verification_rationale_76": "Only spend an LLM call where a rationale / FP-triage is worth it:     uncertain" | kind=entity | source=manager/backend/app/detection/verification.py:L76 | neighbors=[_qualifies_for_llm()] | lang=en
- "detection_verification_rationale_83": "Deterministic verdict, optionally enriched by an LLM rationale. The LLM     (duc" | kind=entity | source=manager/backend/app/detection/verification.py:L83 | neighbors=[verify_finding()] | lang=en
- "dev_hint_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/auth/dev-hint/route.ts:L17 | neighbors=[route.ts] | lang=en
- "discovery_finding_translator_rationale_124": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L124 | neighbors=[_find_open_duplicate()] | lang=en
- "discovery_finding_translator_rationale_144": "Convert a probe's self-assessed `findings` list into persisted Finding rows." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L144 | neighbors=[create_findings_from_probe_result()] | lang=pt
- "discovery_finding_translator_rationale_210": "Raise ONE engagement-level finding when the probe's own metrics say the     scan" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L210 | neighbors=[create_scan_health_finding()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-116.json

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
