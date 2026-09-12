# Node Description Batch 78 of 380

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

- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()]
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()]
- "detection_engine_bridge_accepted": "_accepted()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L139 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), The subset of `facts` ingest accepted. …, The subset of `facts` ingest accepted. …]
- "detection_engine_bridge_detect_all_from_facts": "detect_all_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L267 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), Backward-compatible (cve, posture) view…, Backward-compatible (cve, posture) view…]
- "detection_engine_bridge_ensure_importable": "_ensure_importable()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L77 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), _vuln_db_meta(), detect_findings_from_facts()]
- "detection_engine_bridge_ingest_census": "_ingest_census()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L105 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), (census, rejected_line_numbers) from th…, (census, rejected_line_numbers) from th…]
- "detection_engine_bridge_log_ingest_health": "_log_ingest_health()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L149 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), Escalate by severity of loss. A TOTAL w…, Escalate by severity of loss. A TOTAL w…]
- "detection_engine_bridge_posture_title": "_posture_title()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L287 | neighbors=[engine_bridge.py, _persist_posture_findings(), Stable, human title for a posture findi…, Stable, human title for a posture findi…]
- "detection_engine_consistency_aggregate": "aggregate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L100 | neighbors=[consistency.py, ConsistencyReport, FindingConsistency, run_findings: one list of Findings per …]
- "detection_engine_correlate_suppressionrecord": "SuppressionRecord" | kind=code-symbol | source=manager/detection_engine/correlate.py:L37 | neighbors=[correlate.py, Why a candidate finding was omitted fro…, suppress_negated_with_audit(), .to_dict()]
- "detection_engine_cpe_normalizer_all_osv_source_packages": "all_osv_source_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L413 | neighbors=[cpe_normalizer.py, Every distinct OSV source-package name …, Every distinct OSV source-package name …, Every distinct OSV source-package name …]
- "detection_engine_cpe_normalizer_normalize": "normalize()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L404 | neighbors=[cpe_normalizer.py, Dispatch a single Fact to the right par…, Dispatch a single Fact to the right par…, Dispatch a single Fact to the right par…]
- "detection_engine_cvss_base_score": "base_score()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L43 | neighbors=[cvss.py, parse_vector(), _roundup(), Returns the CVSS v3.1 base score (0.0-1…]
- "detection_engine_enrichment_db_load_epss": "load_epss()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L69 | neighbors=[enrichment_db.py, _cache_key(), EpssDB, .get()]
- "detection_engine_enrichment_db_load_kev": "load_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L55 | neighbors=[enrichment_db.py, _cache_key(), .get(), KevDB]
- "detection_engine_exploitability_apply_to_findings": "apply_to_findings()" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L173 | neighbors=[exploitability.py, assess(), priority_for(), Enrich posture findings in place with e…]
- "detection_engine_ingest_extract_aliases": "_extract_aliases()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L101 | neighbors=[ingest.py, ingest_file(), Real, verified hostname-alias sources i…, Real, verified hostname-alias sources i…]
- "detection_engine_ingest_rationale_1": "ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host" | kind=entity | source=manager/detection_engine/ingest.py:L1 | neighbors=[ingest.py, Asset, Fact, SourceConfidence]
- "detection_engine_ingest_rationale_100": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L100 | neighbors=[ingest_file(), Asset, Fact, SourceConfidence]
- "detection_engine_ingest_rationale_60": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L60 | neighbors=[_validate(), Asset, Fact, SourceConfidence]
- "detection_engine_ingest_rationale_83": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L83 | neighbors=[_extract_aliases(), Asset, Fact, SourceConfidence]
- "detection_engine_ingest_validate": "_validate()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L70 | neighbors=[ingest.py, ingest_file(), Returns an error reason string if inval…, Returns an error reason string if inval…]
- "detection_engine_matcher_version_in_ranges": "_version_in_ranges()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L44 | neighbors=[matcher.py, match_candidate(), Returns (matched, matched_interval_desc…, _safe_compare()]
- "detection_engine_pipeline_ab_evaluate": "ab_evaluate()" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L179 | neighbors=[pipeline.py, run_pipeline(), Phase 2 exit criteria: recall gain from…, Phase 2 exit criteria: recall gain from…]
- "detection_engine_port_intel_contradicts_port_hypothesis": "contradicts_port_hypothesis()" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L201 | neighbors=[port_intel.py, classify_port(), _normalized(), True when an identified product proves …]
- "detection_engine_posture_confidence_assess_confidence": "assess_confidence()" | kind=code-symbol | source=manager/detection_engine/posture_confidence.py:L78 | neighbors=[posture_confidence.py, corroborating_chains(), calibrate_host_findings(), Return (confidence 0-100, precision_fac…]
- "detection_engine_posture_rules_calibrate_host_findings": "_calibrate_host_findings()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1020 | neighbors=[posture_rules.py, detect_posture_traced(), Best-effort confidence calibration (laz…, Best-effort confidence calibration (laz…]
- "detection_engine_posture_rules_cert": "_cert()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L332 | neighbors=[posture_rules.py, _d(), _tls_expired(), _tls_self_signed()]
- "detection_engine_posture_rules_detect_all": "detect_all()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1296 | neighbors=[posture_rules.py, detect_posture(), Run posture detection across every asse…, Run posture detection across every asse…]
- "detection_engine_posture_rules_detect_all_traced": "detect_all_traced()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1281 | neighbors=[posture_rules.py, detect_posture_traced(), Traced counterpart of `detect_all` — fi…, Traced counterpart of `detect_all` — fi…]
- "detection_engine_posture_rules_fact_indicates_no_service": "_fact_indicates_no_service()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L972 | neighbors=[posture_rules.py, evaluate_rule(), True when the scanner ran but the servi…, True when the scanner ran but the servi…]
- "detection_engine_posture_rules_get_path": "get_path()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L72 | neighbors=[posture_rules.py, evaluate_rule(), Resolve `a.b.c` inside a Fact.data dict…, Resolve `a.b.c` inside a Fact.data dict…]
- "detection_engine_posture_rules_rdp_no_nla": "_rdp_no_nla()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L259 | neighbors=[posture_rules.py, Fires on EITHER of the rdp_scanner's tw…, _d(), Fires on EITHER of the rdp_scanner's tw…]
- "detection_engine_posture_rules_rdp_no_tls": "_rdp_no_tls()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L300 | neighbors=[posture_rules.py, The server REFUSED a TLS-capable negoti…, _d(), The server REFUSED a TLS-capable negoti…]
- "detection_engine_posture_rules_state_for": "_state_for()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L961 | neighbors=[posture_rules.py, detect_exposed_services(), detect_posture_traced(), is_validated()]
- "detection_engine_posture_rules_vnc_weak_auth": "_vnc_weak_auth()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L555 | neighbors=[posture_rules.py, VNC type 2 is the legacy DES-based chal…, _d(), VNC type 2 is the legacy DES-based chal…]
- "detection_engine_update_snapshot_query_osv": "_query_osv()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L54 | neighbors=[update_snapshot.py, _ssl_context(), All known vulnerabilities OSV has for t…, sync_snapshot()]
- "detection_engine_update_snapshot_sync_epss_full": "sync_epss_full()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L177 | neighbors=[update_snapshot.py, main(), The ENTIRE EPSS catalog (every scored C…, _ssl_context()]
- "detection_engine_update_snapshot_sync_snapshot": "sync_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L76 | neighbors=[update_snapshot.py, main(), Fetch real OSV records for every produc…, _query_osv()]
- "detection_engine_verifier_rationale_1": "verifier.py — Phase 3: the generalized verifier, the anti-false-positive backbon" | kind=entity | source=manager/detection_engine/verifier.py:L1 | neighbors=[verifier.py, Finding, FindingState, SourceConfidence]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-077.json

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
