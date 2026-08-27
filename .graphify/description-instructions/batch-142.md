# Node Description Batch 143 of 236

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

- "detection_engine_version_compare_rationale_178": "Plain dotted-numeric comparison for non-distro upstream versions     (banner-der" | kind=entity | source=manager/detection_engine/version_compare.py:L178 | neighbors=[semver_compare()] | lang=en
- "detection_engine_version_compare_rationale_190": "Plain dotted-numeric comparison for non-distro upstream versions     (banner-der" | kind=entity | source=manager/detection_engine/version_compare.py:L190 | neighbors=[semver_compare()] | lang=en
- "detection_engine_version_compare_rationale_220": "Test hook: drop the in-memory record of which snapshots were validated." | kind=entity | source=manager/detection_engine/version_compare.py:L220 | neighbors=[_clear_validation_cache()] | lang=en
- "detection_engine_version_compare_rationale_244": "Confirm pure-Python agrees with the real dpkg binary on the ordering of     `ver" | kind=entity | source=manager/detection_engine/version_compare.py:L244 | neighbors=[verify_pure_python_matches_dpkg()] | lang=en
- "detection_engine_version_compare_rationale_31": "Real dpkg --compare-versions. None (not an error) if dpkg isn't     installed or" | kind=entity | source=manager/detection_engine/version_compare.py:L31 | neighbors=[_dpkg_compare_via_binary()] | lang=en
- "detection_engine_version_compare_rationale_37": "Real dpkg --compare-versions. None (not an error) if dpkg isn't     installed or" | kind=entity | source=manager/detection_engine/version_compare.py:L37 | neighbors=[_dpkg_compare_via_binary()] | lang=en
- "detection_engine_version_compare_rationale_53": "dpkg's non-digit character ordering: '~' sorts before EVERYTHING,     including" | kind=entity | source=manager/detection_engine/version_compare.py:L53 | neighbors=[_char_order()] | lang=en
- "detection_engine_version_compare_rationale_59": "dpkg's non-digit character ordering: '~' sorts before EVERYTHING,     including" | kind=entity | source=manager/detection_engine/version_compare.py:L59 | neighbors=[_char_order()] | lang=en
- "detection_engine_version_compare_rationale_86": "upstream_version or debian_revision comparison (no epoch, no '-')." | kind=entity | source=manager/detection_engine/version_compare.py:L86 | neighbors=[_compare_part()] | lang=en
- "detection_engine_version_compare_rationale_92": "upstream_version or debian_revision comparison (no epoch, no '-')." | kind=entity | source=manager/detection_engine/version_compare.py:L92 | neighbors=[_compare_part()] | lang=en
- "detection_engine_vuln_db_rationale_1": "vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN" | kind=entity | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[vuln_db.py] | lang=en
- "detection_engine_vuln_db_rationale_102": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L102 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_rationale_106": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L106 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_rationale_110": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L110 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_113": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L113 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_117": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L117 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_134": "Test hook: drop the memoized snapshot cache so the next load re-reads." | kind=entity | source=manager/detection_engine/vuln_db.py:L134 | neighbors=[_clear_caches()] | lang=en
- "detection_engine_vuln_db_rationale_138": "Test hook: drop the memoized snapshot cache so the next load re-reads." | kind=entity | source=manager/detection_engine/vuln_db.py:L138 | neighbors=[_clear_caches()] | lang=en
- "detection_engine_vuln_db_rationale_140": "Every version string that appears as a range boundary in the snapshot —     the" | kind=entity | source=manager/detection_engine/vuln_db.py:L140 | neighbors=[_boundary_versions()] | lang=en
- "detection_engine_vuln_db_rationale_144": "Every version string that appears as a range boundary in the snapshot —     the" | kind=entity | source=manager/detection_engine/vuln_db.py:L144 | neighbors=[_boundary_versions()] | lang=en
- "detection_engine_vuln_db_rationale_157": "The actual parse + integrity-verify + build. Kept separate from     load_snapsho" | kind=entity | source=manager/detection_engine/vuln_db.py:L157 | neighbors=[_read_snapshot()] | lang=en
- "detection_engine_vuln_db_rationale_161": "The actual parse + integrity-verify + build. Kept separate from     load_snapsho" | kind=entity | source=manager/detection_engine/vuln_db.py:L161 | neighbors=[_read_snapshot()] | lang=en
- "detection_engine_vuln_db_rationale_185": "Merge an NVD/CPE companion snapshot into the primary VulnDB.      Records are co" | kind=entity | source=manager/detection_engine/vuln_db.py:L185 | neighbors=[_merge_companion()] | lang=en
- "detection_engine_vuln_db_rationale_44": "Derives the synced product list from cpe_normalizer.py's tables —     the single" | kind=entity | source=manager/detection_engine/vuln_db.py:L44 | neighbors=[_default_products()] | lang=en
- "detection_engine_vuln_db_rationale_47": "Derives the synced product list from cpe_normalizer.py's tables —     the single" | kind=entity | source=manager/detection_engine/vuln_db.py:L47 | neighbors=[_default_products()] | lang=en
- "detection_engine_vuln_db_rationale_51": "Derives the synced product list from cpe_normalizer.py's tables —     the single" | kind=entity | source=manager/detection_engine/vuln_db.py:L51 | neighbors=[_default_products()] | lang=en
- "detection_engine_vuln_db_rationale_60": "Stable hash of the snapshot's actual vulnerability content — recorded     in eve" | kind=entity | source=manager/detection_engine/vuln_db.py:L60 | neighbors=[_content_hash()] | lang=en
- "detection_engine_vuln_db_rationale_63": "Stable hash of the snapshot's actual vulnerability content — recorded     in eve" | kind=entity | source=manager/detection_engine/vuln_db.py:L63 | neighbors=[_content_hash()] | lang=en
- "detection_engine_vuln_db_rationale_67": "Stable hash of the snapshot's actual vulnerability content — recorded     in eve" | kind=entity | source=manager/detection_engine/vuln_db.py:L67 | neighbors=[_content_hash()] | lang=en
- "detection_engine_vuln_db_rationale_79": "In-memory index over a loaded snapshot: product -> OSV vuln records.     Constru" | kind=entity | source=manager/detection_engine/vuln_db.py:L79 | neighbors=[VulnDB] | lang=pt
- "detection_engine_vuln_db_rationale_82": "In-memory index over a loaded snapshot: product -> OSV vuln records.     Constru" | kind=entity | source=manager/detection_engine/vuln_db.py:L82 | neighbors=[VulnDB] | lang=pt
- "detection_engine_vuln_db_rationale_86": "In-memory index over a loaded snapshot: product -> OSV vuln records.     Constru" | kind=entity | source=manager/detection_engine/vuln_db.py:L86 | neighbors=[VulnDB] | lang=pt
- "detection_engine_vuln_db_rationale_99": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L99 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_vulndb_covers": ".covers()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L113 | neighbors=[VulnDB] | lang=en
- "detection_engine_vuln_db_vulndb_known_products": ".known_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L122 | neighbors=[VulnDB] | lang=en
- "detection_exposure_fusion_service_rationale_1": "exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows." | kind=entity | source=manager/backend/app/detection/exposure_fusion_service.py:L1 | neighbors=[exposure_fusion_service.py] | lang=en
- "detection_exposure_fusion_service_rationale_31": "Reconstruct one {\"exposure\": [...]} dict per probe from persisted facts.      Ea" | kind=entity | source=manager/backend/app/detection/exposure_fusion_service.py:L31 | neighbors=[_results_from_scan_rows()] | lang=en
- "detection_exposure_fusion_service_rationale_53": "Fuse all probes' exposure_matrix observations for an engagement and stamp     th" | kind=entity | source=manager/backend/app/detection/exposure_fusion_service.py:L53 | neighbors=[recompute_fused_exposure()] | lang=en
- "detection_logger_attacklogger_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L24 | neighbors=[AttackLogger] | lang=en
- "detection_prioritization_rationale_1": "prioritization.py — the single risk-scoring engine for ALL findings.  WHY THIS E" | kind=entity | source=manager/backend/app/detection/prioritization.py:L1 | neighbors=[prioritization.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-142.json

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
