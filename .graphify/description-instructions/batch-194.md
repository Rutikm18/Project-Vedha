# Node Description Batch 195 of 330

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
- "detection_prioritization_rationale_1": "Persist the canonical Manager risk score for all active findings.  WHY THIS EXIS" | kind=entity | source=manager/backend/app/detection/prioritization.py:L1 | neighbors=[prioritization.py] | lang=en
- "detection_prioritization_rationale_103": "Compatibility wrapper around the canonical 0-1000 risk function." | kind=entity | source=manager/backend/app/detection/prioritization.py:L103 | neighbors=[composite_risk_score()] | lang=en
- "detection_prioritization_rationale_116": "(Re)compute risk_score for every still-relevant finding in the engagement." | kind=entity | source=manager/backend/app/detection/prioritization.py:L116 | neighbors=[prioritize_engagement_findings()] | lang=en
- "detection_prioritization_rationale_125": "The most-exposed value among an asset's services (external beats internal)." | kind=entity | source=manager/backend/app/detection/prioritization.py:L125 | neighbors=[_strongest_exposure()] | lang=en
- "detection_prioritization_rationale_131": "(kev_db, epss_db) from the pinned snapshots, or (None, None) if the     detectio" | kind=entity | source=manager/backend/app/detection/prioritization.py:L131 | neighbors=[_load_offline_kev_epss()] | lang=en
- "detection_prioritization_rationale_148": "(Re)compute risk_score for every still-relevant finding in the engagement." | kind=entity | source=manager/backend/app/detection/prioritization.py:L148 | neighbors=[prioritize_engagement_findings()] | lang=en
- "detection_prioritization_rationale_58": "Score a posture finding with the Manager formula.      The historical name is re" | kind=entity | source=manager/backend/app/detection/prioritization.py:L58 | neighbors=[_posture_risk_on_manager_scale()] | lang=en
- "detection_prioritization_rationale_74": "The unified 0-1000 composite (see module docstring). Pure + deterministic." | kind=entity | source=manager/backend/app/detection/prioritization.py:L74 | neighbors=[composite_risk_score()] | lang=en
- "detection_prioritization_rationale_93": "The most-exposed value among an asset's services (external beats internal)." | kind=entity | source=manager/backend/app/detection/prioritization.py:L93 | neighbors=[_strongest_exposure()] | lang=en
- "detection_prioritization_rationale_99": "(kev_db, epss_db) from the pinned snapshots, or (None, None) if the     detectio" | kind=entity | source=manager/backend/app/detection/prioritization.py:L99 | neighbors=[_load_offline_kev_epss()] | lang=en
- "detection_resolution_rationale_1": "resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c" | kind=entity | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[resolution.py] | lang=en
- "detection_resolution_rationale_132": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L132 | neighbors=[apply_manual_reopen()] | lang=en
- "detection_resolution_rationale_141": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L141 | neighbors=[apply_manual_reopen()] | lang=en
- "detection_resolution_rationale_28": "IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin" | kind=entity | source=manager/backend/app/detection/resolution.py:L28 | neighbors=[host_of()] | lang=en
- "detection_resolution_rationale_29": "IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin" | kind=entity | source=manager/backend/app/detection/resolution.py:L29 | neighbors=[host_of()] | lang=en
- "detection_resolution_rationale_36": "What this run PROVABLY re-observed. An asset is covered only if a     completed" | kind=entity | source=manager/backend/app/detection/resolution.py:L36 | neighbors=[build_coverage()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-194.json

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
