# Node Description Batch 226 of 380

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

- "detection_engine_vuln_db_vulndb_known_products": ".known_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L122 | neighbors=[VulnDB]
- "detection_exposure_fusion_service_rationale_1": "exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows." | kind=entity | source=manager/backend/app/detection/exposure_fusion_service.py:L1 | neighbors=[exposure_fusion_service.py]
- "detection_exposure_fusion_service_rationale_31": "Reconstruct one {\"exposure\": [...]} dict per probe from persisted facts.      Ea" | kind=entity | source=manager/backend/app/detection/exposure_fusion_service.py:L31 | neighbors=[_results_from_scan_rows()]
- "detection_exposure_fusion_service_rationale_53": "Fuse all probes' exposure_matrix observations for an engagement and stamp     th" | kind=entity | source=manager/backend/app/detection/exposure_fusion_service.py:L53 | neighbors=[recompute_fused_exposure()]
- "detection_logger_attacklogger_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L24 | neighbors=[AttackLogger]
- "detection_prioritization_rationale_1": "Persist the canonical Manager risk score for all active findings.  WHY THIS EXIS" | kind=entity | source=manager/backend/app/detection/prioritization.py:L1 | neighbors=[prioritization.py]
- "detection_prioritization_rationale_103": "Compatibility wrapper around the canonical 0-1000 risk function." | kind=entity | source=manager/backend/app/detection/prioritization.py:L103 | neighbors=[composite_risk_score()]
- "detection_prioritization_rationale_116": "(Re)compute risk_score for every still-relevant finding in the engagement." | kind=entity | source=manager/backend/app/detection/prioritization.py:L116 | neighbors=[prioritize_engagement_findings()]
- "detection_prioritization_rationale_125": "The most-exposed value among an asset's services (external beats internal)." | kind=entity | source=manager/backend/app/detection/prioritization.py:L125 | neighbors=[_strongest_exposure()]
- "detection_prioritization_rationale_131": "(kev_db, epss_db) from the pinned snapshots, or (None, None) if the     detectio" | kind=entity | source=manager/backend/app/detection/prioritization.py:L131 | neighbors=[_load_offline_kev_epss()]
- "detection_prioritization_rationale_148": "(Re)compute risk_score for every still-relevant finding in the engagement." | kind=entity | source=manager/backend/app/detection/prioritization.py:L148 | neighbors=[prioritize_engagement_findings()]
- "detection_prioritization_rationale_58": "Score a posture finding with the Manager formula.      The historical name is re" | kind=entity | source=manager/backend/app/detection/prioritization.py:L58 | neighbors=[_posture_risk_on_manager_scale()]
- "detection_prioritization_rationale_74": "The unified 0-1000 composite (see module docstring). Pure + deterministic." | kind=entity | source=manager/backend/app/detection/prioritization.py:L74 | neighbors=[composite_risk_score()]
- "detection_prioritization_rationale_93": "The most-exposed value among an asset's services (external beats internal)." | kind=entity | source=manager/backend/app/detection/prioritization.py:L93 | neighbors=[_strongest_exposure()]
- "detection_prioritization_rationale_99": "(kev_db, epss_db) from the pinned snapshots, or (None, None) if the     detectio" | kind=entity | source=manager/backend/app/detection/prioritization.py:L99 | neighbors=[_load_offline_kev_epss()]
- "detection_resolution_rationale_1": "resolution.py — coverage-gated auto-resolution of findings.  Split into a PURE c" | kind=entity | source=manager/backend/app/detection/resolution.py:L1 | neighbors=[resolution.py]
- "detection_resolution_rationale_103": "Apply decide_resolution to every engine-managed open/confirmed finding     NOT t" | kind=entity | source=manager/backend/app/detection/resolution.py:L103 | neighbors=[evaluate_resolutions()]
- "detection_resolution_rationale_132": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L132 | neighbors=[apply_manual_reopen()]
- "detection_resolution_rationale_141": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L141 | neighbors=[apply_manual_reopen()]
- "detection_resolution_rationale_150": "Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's     r" | kind=entity | source=manager/backend/app/detection/resolution.py:L150 | neighbors=[apply_manual_reopen()]
- "detection_resolution_rationale_28": "IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin" | kind=entity | source=manager/backend/app/detection/resolution.py:L28 | neighbors=[host_of()]
- "detection_resolution_rationale_29": "IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.     Mirrors findin" | kind=entity | source=manager/backend/app/detection/resolution.py:L29 | neighbors=[host_of()]
- "detection_resolution_rationale_36": "What this run PROVABLY re-observed. An asset is covered only if a     completed" | kind=entity | source=manager/backend/app/detection/resolution.py:L36 | neighbors=[build_coverage()]
- "detection_resolution_rationale_37": "What this run PROVABLY re-observed. An asset is covered only if a     completed" | kind=entity | source=manager/backend/app/detection/resolution.py:L37 | neighbors=[build_coverage()]
- "detection_resolution_rationale_58": "Consecutive coverage-proven clean runs required before auto-close.     critical/" | kind=entity | source=manager/backend/app/detection/resolution.py:L58 | neighbors=[resolution_threshold()]
- "detection_resolution_rationale_59": "Consecutive coverage-proven clean runs required before auto-close.     critical/" | kind=entity | source=manager/backend/app/detection/resolution.py:L59 | neighbors=[resolution_threshold()]
- "detection_resolution_rationale_68": "Consecutive coverage-proven clean runs required before auto-close.     critical/" | kind=entity | source=manager/backend/app/detection/resolution.py:L68 | neighbors=[resolution_threshold()]
- "detection_resolution_rationale_73": "Pure heart of auto-resolution. Given whether the finding's asset was     re-obse" | kind=entity | source=manager/backend/app/detection/resolution.py:L73 | neighbors=[decide_resolution()]
- "detection_resolution_rationale_74": "Pure heart of auto-resolution. Given whether the finding's asset was     re-obse" | kind=entity | source=manager/backend/app/detection/resolution.py:L74 | neighbors=[decide_resolution()]
- "detection_resolution_rationale_83": "Pure heart of auto-resolution. Given whether the finding's asset was     re-obse" | kind=entity | source=manager/backend/app/detection/resolution.py:L83 | neighbors=[decide_resolution()]
- "detection_resolution_rationale_93": "Apply decide_resolution to every engine-managed open/confirmed finding     NOT t" | kind=entity | source=manager/backend/app/detection/resolution.py:L93 | neighbors=[evaluate_resolutions()]
- "detection_resolution_rationale_94": "Apply decide_resolution to every engine-managed open/confirmed finding     NOT t" | kind=entity | source=manager/backend/app/detection/resolution.py:L94 | neighbors=[evaluate_resolutions()]
- "detection_siem_build_siem_engine": "build_siem_engine()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L249 | neighbors=[siem.py]
- "detection_siem_rationale_1": "SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic" | kind=entity | source=manager/backend/app/detection/siem.py:L1 | neighbors=[siem.py]
- "detection_siem_rationale_135": "Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi" | kind=entity | source=manager/backend/app/detection/siem.py:L135 | neighbors=[SentinelSIEM]
- "detection_siem_rationale_185": "Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_" | kind=entity | source=manager/backend/app/detection/siem.py:L185 | neighbors=[ElasticSIEM]
- "detection_siem_rationale_51": "Abstract SIEM connector." | kind=entity | source=manager/backend/app/detection/siem.py:L51 | neighbors=[SIEMQueryEngine]
- "detection_siem_rationale_82": "Splunk via the REST search endpoint (``/services/search/jobs/export``) with an" | kind=entity | source=manager/backend/app/detection/siem.py:L82 | neighbors=[SplunkSIEM]
- "detection_siem_siemqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L55 | neighbors=[SIEMQueryEngine]
- "detection_siem_siemqueryengine_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L60 | neighbors=[SIEMQueryEngine]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-225.json

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
