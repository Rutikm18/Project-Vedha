# Node Description Batch 86 of 131

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

- "detection_engine_consistency_consistencyreport_intermittent": ".intermittent()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L96 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_consistencyreport_stable": ".stable()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L92 | neighbors=[ConsistencyReport] | lang=en
- "detection_engine_consistency_findingconsistency_classification": ".classification()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L67 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_consistency_findingconsistency_rate": ".rate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L59 | neighbors=[FindingConsistency] | lang=en
- "detection_engine_cpe_normalizer_cpecandidate_cpe23": ".cpe23()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L72 | neighbors=[CPECandidate] | lang=en
- "detection_engine_cvss_rationale_1": "cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network" | kind=entity | source=manager/detection_engine/cvss.py:L1 | neighbors=[cvss.py] | lang=en
- "detection_engine_cvss_rationale_23": "CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r" | kind=entity | source=manager/detection_engine/cvss.py:L23 | neighbors=[_roundup()] | lang=en
- "detection_engine_cvss_rationale_44": "Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin" | kind=entity | source=manager/detection_engine/cvss.py:L44 | neighbors=[base_score()] | lang=en
- "detection_engine_enrichment_db_epssdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L24 | neighbors=[EpssDB] | lang=en
- "detection_engine_enrichment_db_kevdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L15 | neighbors=[KevDB] | lang=en
- "detection_engine_enrichment_db_kevdb_is_kev": ".is_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L19 | neighbors=[KevDB] | lang=en
- "detection_engine_enrichment_db_rationale_1": "enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d" | kind=entity | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[enrichment_db.py] | lang=en
- "detection_engine_enrichment_db_rationale_29": "{'epss': float, 'percentile': float} or None if not covered." | kind=entity | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[.get()] | lang=en
- "detection_engine_ingest_ingestresult_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L43 | neighbors=[IngestResult] | lang=en
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
- "detection_engine_update_snapshot_rationale_1": "update_snapshot.py — the ONLY module in this package that talks to the network." | kind=entity | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[update_snapshot.py] | lang=en
- "detection_engine_update_snapshot_rationale_118": "The full CISA Known Exploited Vulnerabilities catalog — a single flat     list," | kind=entity | source=manager/detection_engine/update_snapshot.py:L118 | neighbors=[sync_kev_snapshot()] | lang=en
- "detection_engine_update_snapshot_rationale_140": "EPSS scores for exactly the CVE IDs this detection run actually cares     about" | kind=entity | source=manager/detection_engine/update_snapshot.py:L140 | neighbors=[sync_epss_snapshot()] | lang=en
- "detection_engine_update_snapshot_rationale_38": "Some macOS python.org installs ship expecting `Install Certificates.     command" | kind=entity | source=manager/detection_engine/update_snapshot.py:L38 | neighbors=[_ssl_context()] | lang=en
- "detection_engine_update_snapshot_rationale_55": "All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n" | kind=entity | source=manager/detection_engine/update_snapshot.py:L55 | neighbors=[_query_osv()] | lang=en
- "detection_engine_update_snapshot_rationale_79": "Fetch real OSV records for every product, write a pinned snapshot.      rate_lim" | kind=entity | source=manager/detection_engine/update_snapshot.py:L79 | neighbors=[sync_snapshot()] | lang=en
- "detection_engine_version_compare_rationale_1": "version_compare.py — per-scheme version comparators.  Spec calls this \"the highe" | kind=entity | source=manager/detection_engine/version_compare.py:L1 | neighbors=[version_compare.py] | lang=en
- "detection_engine_version_compare_rationale_105": "1:8.4p1-5+deb11u1' -> (epoch='1', upstream='8.4p1', revision='5+deb11u1').     N" | kind=entity | source=manager/detection_engine/version_compare.py:L105 | neighbors=[_split_dpkg_version()] | lang=en
- "detection_engine_version_compare_rationale_124": "True when exactly one of the two version strings carries an explicit,     non-ze" | kind=entity | source=manager/detection_engine/version_compare.py:L124 | neighbors=[has_ambiguous_epoch()] | lang=en
- "detection_engine_version_compare_rationale_167": "-1 if a<b, 0 if a==b, 1 if a>b, per Debian version ordering. Prefers     the rea" | kind=entity | source=manager/detection_engine/version_compare.py:L167 | neighbors=[dpkg_compare()] | lang=pt
- "detection_engine_version_compare_rationale_178": "Plain dotted-numeric comparison for non-distro upstream versions     (banner-der" | kind=entity | source=manager/detection_engine/version_compare.py:L178 | neighbors=[semver_compare()] | lang=en
- "detection_engine_version_compare_rationale_31": "Real dpkg --compare-versions. None (not an error) if dpkg isn't     installed or" | kind=entity | source=manager/detection_engine/version_compare.py:L31 | neighbors=[_dpkg_compare_via_binary()] | lang=en
- "detection_engine_version_compare_rationale_53": "dpkg's non-digit character ordering: '~' sorts before EVERYTHING,     including" | kind=entity | source=manager/detection_engine/version_compare.py:L53 | neighbors=[_char_order()] | lang=en
- "detection_engine_version_compare_rationale_86": "upstream_version or debian_revision comparison (no epoch, no '-')." | kind=entity | source=manager/detection_engine/version_compare.py:L86 | neighbors=[_compare_part()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-085.json

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
