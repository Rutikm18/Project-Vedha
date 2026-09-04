# Node Description Batch 69 of 332

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

- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, agents/greeting-introduction, main, bd7383f scanner fine ..now integrations] | lang=fr
- "components_queryprovider": "QueryProvider.tsx" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, QueryProvider(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "components_refreshbutton_refreshbutton": "RefreshButton()" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L30 | neighbors=[PageShell.tsx, RefreshButton.tsx, page.tsx, PortalShell.tsx] | lang=en
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L54 | neighbors=[PageShell.tsx, Sidebar.tsx, page.tsx, page.tsx] | lang=en
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L26 | neighbors=[PageShell.tsx, ThemeProvider.tsx, PortalShell.tsx, page.tsx] | lang=en
- "console_primitives_meter": "Meter()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L90 | neighbors=[Primitives.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx] | lang=en
- "cve_ingest_ssl_context": "_ssl_context()" | kind=code-symbol | source=probe/cve/ingest.py:L45 | neighbors=[ingest.py, _get(), ingest_nvd(), certifi CA bundle if present, else the …] | lang=en
- "cve_online_apply": "_apply()" | kind=code-symbol | source=probe/cve/online.py:L174 | neighbors=[online.py, _was_exposed(), enrich_findings(), Fold one CVE's live result into a findi…] | lang=en
- "cve_online_lookup_nvd": "lookup_nvd()" | kind=code-symbol | source=probe/cve/online.py:L65 | neighbors=[online.py, enrich_findings(), OnlineResult, Query live NVD 2.0 for one CVE. Returns…] | lang=en
- "cve_version_compare": "compare()" | kind=code-symbol | source=probe/cve/version.py:L47 | neighbors=[version.py, parse_version(), in_range(), Return -1/0/1 for version a vs b (zero-…] | lang=en
- "cve_vulndb_norm": "_norm()" | kind=code-symbol | source=probe/cve/vulndb.py:L58 | neighbors=[vulndb.py, .add_cpe_match(), .cves_for_cpe(), .upsert_kev()] | lang=en
- "cve_vulndb_vulndb_cves_for_cpe": ".cves_for_cpe()" | kind=code-symbol | source=probe/cve/vulndb.py:L119 | neighbors=[All vulnerable CVEs whose CPE applicabi…, VulnDB, _norm(), ._enrich()] | lang=en
- "cve_weakness_map_correlate_weaknesses": "correlate_weaknesses()" | kind=code-symbol | source=probe/cve/weakness_map.py:L163 | neighbors=[weakness_map.py, _finding_view(), _mirror_cve(), Map observed weakness findings to their…] | lang=en
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L60 | neighbors=[DashboardGrid.tsx, LiveOverview.tsx, verdict(), page.tsx] | lang=en
- "dashboard_patchcomparisonmatrix_patchcomparisonmatrix": "PatchComparisonMatrix()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L70 | neighbors=[DashboardGrid.tsx, PatchComparisonMatrix.tsx, n(), page.tsx] | lang=en
- "dashboard_posturescorecard_posturescorecard": "PostureScorecard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L118 | neighbors=[DashboardGrid.tsx, PostureScorecard.tsx, usePosture(), page.tsx] | lang=en
- "detection_edr_edrqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L78 | neighbors=[.query_detections(), EDRQueryEngine, .query_detections(), .query_detections()] | lang=en
- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()] | lang=en
- "detection_engine_bridge_engagement_device_roles": "_engagement_device_roles()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L402 | neighbors=[engine_bridge.py, _persist_attack_paths(), ip → {device_role, role_detail} from al…, ip → {device_role, role_detail} from al…] | lang=en
- "detection_engine_bridge_ensure_importable": "_ensure_importable()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L76 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), _vuln_db_meta(), detect_findings_from_facts()] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-068.json

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
