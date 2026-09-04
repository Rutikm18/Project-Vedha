# Node Description Batch 194 of 332

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
- "detection_engine_ingest_ingestresult_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L50 | neighbors=[IngestResult] | lang=en
- "detection_engine_ingest_rationale_102": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L102 | neighbors=[_extract_aliases()] | lang=en
- "detection_engine_ingest_rationale_126": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L126 | neighbors=[ingest_file()] | lang=en
- "detection_engine_ingest_rationale_71": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L71 | neighbors=[_validate()] | lang=en
- "detection_engine_models_asset_add_alias": ".add_alias()" | kind=code-symbol | source=manager/detection_engine/models.py:L97 | neighbors=[Asset] | lang=en
- "detection_engine_models_asset_facts_by_scanner": ".facts_by_scanner()" | kind=code-symbol | source=manager/detection_engine/models.py:L101 | neighbors=[Asset] | lang=en
- "detection_engine_models_asset_open_ports": ".open_ports()" | kind=code-symbol | source=manager/detection_engine/models.py:L104 | neighbors=[Asset] | lang=en
- "detection_engine_models_finding_post_init": ".__post_init__()" | kind=code-symbol | source=manager/detection_engine/models.py:L179 | neighbors=[Finding] | lang=en
- "detection_engine_models_finding_to_dict": ".to_dict()" | kind=code-symbol | source=manager/detection_engine/models.py:L187 | neighbors=[Finding] | lang=en
- "detection_engine_models_rationale_1": "models.py — shared schema for the detection/correlation layer.  Two core objects" | kind=entity | source=manager/detection_engine/models.py:L1 | neighbors=[models.py] | lang=en
- "detection_engine_models_rationale_108": "Reconstruct this asset using only facts observed at or before         cutoff_ts" | kind=entity | source=manager/detection_engine/models.py:L108 | neighbors=[.as_of()] | lang=en
- "detection_engine_models_rationale_126": "Deterministic finding ID: the SAME (asset, CVE, CPE) triple always     hashes to" | kind=entity | source=manager/detection_engine/models.py:L126 | neighbors=[make_finding_id()] | lang=en
- "detection_engine_models_rationale_25": "How was this fact obtained? Drives every downstream confidence decision     (CPE" | kind=entity | source=manager/detection_engine/models.py:L25 | neighbors=[SourceConfidence] | lang=en
- "detection_engine_models_rationale_45": "One ScanResult line, carried forward with its ingestion-time     confidence tag" | kind=entity | source=manager/detection_engine/models.py:L45 | neighbors=[Fact] | lang=en
- "detection_engine_models_rationale_61": "A stable, human-readable pointer back to this exact observation —         what a" | kind=entity | source=manager/detection_engine/models.py:L61 | neighbors=[.ref()] | lang=en
- "detection_engine_models_rationale_71": "Every fact known about one host, merged across all scanners/runs.      IP is the" | kind=entity | source=manager/detection_engine/models.py:L71 | neighbors=[Asset] | lang=en
- "detection_engine_pipeline_rationale_127": "Unified detection over one set of ingested facts: the CVE track     (version→CVE" | kind=entity | source=manager/detection_engine/pipeline.py:L127 | neighbors=[run_full_detection()] | lang=en
- "detection_engine_pipeline_rationale_180": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L180 | neighbors=[ab_evaluate()] | lang=en
- "detection_engine_pipeline_rationale_52": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L52 | neighbors=[run_pipeline()] | lang=en
- "detection_engine_port_intel_escalate": "escalate()" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L25 | neighbors=[port_intel.py] | lang=en
- "detection_engine_port_intel_rationale_1": "port_intel.py — port-intelligence catalog for the exposed-service detector.  The" | kind=entity | source=manager/detection_engine/port_intel.py:L1 | neighbors=[port_intel.py] | lang=en
- "detection_engine_port_intel_rationale_203": "True when an identified product proves the catalog's port guess wrong." | kind=entity | source=manager/detection_engine/port_intel.py:L203 | neighbors=[contradicts_port_hypothesis()] | lang=en
- "detection_engine_port_intel_rationale_215": "Map an open TCP port (+ optional banner, the probe's soft-matched service     la" | kind=entity | source=manager/detection_engine/port_intel.py:L215 | neighbors=[classify_port()] | lang=en
- "detection_engine_posture_confidence_rationale_1": "posture_confidence.py — calibrated, auditable confidence for posture findings." | kind=entity | source=manager/detection_engine/posture_confidence.py:L1 | neighbors=[posture_confidence.py] | lang=en
- "detection_engine_posture_confidence_rationale_121": "Second pass over ONE host's posture findings: now that every rule that fired on" | kind=entity | source=manager/detection_engine/posture_confidence.py:L121 | neighbors=[calibrate_host_findings()] | lang=en
- "detection_engine_posture_confidence_rationale_69": "Chains this rule belongs to where ≥1 OTHER member also fired on the host.     A" | kind=entity | source=manager/detection_engine/posture_confidence.py:L69 | neighbors=[corroborating_chains()] | lang=en
- "detection_engine_posture_confidence_rationale_81": "Return (confidence 0-100, precision_factors). Pure and deterministic:     same i" | kind=entity | source=manager/detection_engine/posture_confidence.py:L81 | neighbors=[assess_confidence()] | lang=en
- "detection_engine_posture_rules_posturefinding_post_init": ".__post_init__()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L204 | neighbors=[PostureFinding] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-193.json

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
