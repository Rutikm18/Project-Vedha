# Node Description Batch 88 of 134

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

- "dashboard_slastatus_sev_style": "SEV_STYLE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L37 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slaitem": "SlaItem" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L32 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slastate": "SlaState" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L30 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_slasummary": "SlaSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L37 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_state": "STATE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L42 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_state_color": "STATE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L30 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_statecell": "StateCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L76 | neighbors=[SlaStatus.tsx]
- "dashboard_slastatus_summarycell": "SummaryCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L61 | neighbors=[SlaStatus.tsx]
- "declarativebase": "DeclarativeBase" | kind=code-symbol | neighbors=[Base]
- "detection_correlator_detectioncorrelator_compute_coverage": ".compute_coverage()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L159 | neighbors=[DetectionCorrelator]
- "detection_correlator_detectioncorrelator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L76 | neighbors=[DetectionCorrelator]
- "detection_edr_build_edr_engine": "build_edr_engine()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L235 | neighbors=[edr.py]
- "detection_edr_edrdetection_is_prevented": ".is_prevented()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L43 | neighbors=[EDRDetection]
- "detection_edr_edrqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L65 | neighbors=[EDRQueryEngine]
- "detection_edr_edrqueryengine_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L70 | neighbors=[EDRQueryEngine]
- "detection_edr_rationale_1": "EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender" | kind=entity | source=manager/backend/app/detection/edr.py:L1 | neighbors=[edr.py]
- "detection_edr_rationale_141": "Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi" | kind=entity | source=manager/backend/app/detection/edr.py:L141 | neighbors=[MicrosoftDefender]
- "detection_edr_rationale_187": "SentinelOne via the REST ``/web/api/v2.1/threats`` endpoint.     config: {base_u" | kind=entity | source=manager/backend/app/detection/edr.py:L187 | neighbors=[SentinelOne]
- "detection_edr_rationale_92": "Falcon: query detection IDs then fetch their summaries.     config: {base_url, t" | kind=entity | source=manager/backend/app/detection/edr.py:L92 | neighbors=[CrowdStrikeFalcon]
- "detection_engine_ai_normalizer_ainormalizercache_post_init": ".__post_init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L142 | neighbors=[AINormalizerCache]
- "detection_engine_ai_normalizer_anthropicaiclient_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L103 | neighbors=[AnthropicAIClient]
- "detection_engine_ai_normalizer_fakeaiclient_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L131 | neighbors=[FakeAIClient]
- "detection_engine_consistency_consistencyreport_intermittent": ".intermittent()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L96 | neighbors=[ConsistencyReport]
- "detection_engine_consistency_consistencyreport_stable": ".stable()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L92 | neighbors=[ConsistencyReport]
- "detection_engine_consistency_findingconsistency_classification": ".classification()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L67 | neighbors=[FindingConsistency]
- "detection_engine_consistency_findingconsistency_rate": ".rate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L59 | neighbors=[FindingConsistency]
- "detection_engine_cpe_normalizer_cpecandidate_cpe23": ".cpe23()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L72 | neighbors=[CPECandidate]
- "detection_engine_cvss_rationale_1": "cvss.py — CVSS v3.1 base score from a vector string. Pure arithmetic, no network" | kind=entity | source=manager/detection_engine/cvss.py:L1 | neighbors=[cvss.py]
- "detection_engine_cvss_rationale_23": "CVSS spec's exact rounding rule (avoids float-precision drift from a     naive r" | kind=entity | source=manager/detection_engine/cvss.py:L23 | neighbors=[_roundup()]
- "detection_engine_cvss_rationale_44": "Returns the CVSS v3.1 base score (0.0-10.0), or None if the vector     is missin" | kind=entity | source=manager/detection_engine/cvss.py:L44 | neighbors=[base_score()]
- "detection_engine_enrichment_db_epssdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L24 | neighbors=[EpssDB]
- "detection_engine_enrichment_db_kevdb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L15 | neighbors=[KevDB]
- "detection_engine_enrichment_db_kevdb_is_kev": ".is_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L19 | neighbors=[KevDB]
- "detection_engine_enrichment_db_rationale_1": "enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as vuln_d" | kind=entity | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[enrichment_db.py]
- "detection_engine_enrichment_db_rationale_29": "{'epss': float, 'percentile': float} or None if not covered." | kind=entity | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[.get()]
- "detection_engine_ingest_ingestresult_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L43 | neighbors=[IngestResult]
- "detection_engine_models_asset_add_alias": ".add_alias()" | kind=code-symbol | source=manager/detection_engine/models.py:L97 | neighbors=[Asset]
- "detection_engine_models_asset_facts_by_scanner": ".facts_by_scanner()" | kind=code-symbol | source=manager/detection_engine/models.py:L101 | neighbors=[Asset]
- "detection_engine_models_asset_open_ports": ".open_ports()" | kind=code-symbol | source=manager/detection_engine/models.py:L104 | neighbors=[Asset]
- "detection_engine_models_finding_post_init": ".__post_init__()" | kind=code-symbol | source=manager/detection_engine/models.py:L179 | neighbors=[Finding]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-087.json

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
