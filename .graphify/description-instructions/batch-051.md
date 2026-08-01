# Node Description Batch 52 of 119

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

- "dashboard_protocolrow_riskcolor": "riskColor()" | kind=code-symbol | source=manager/frontend/components/dashboard/ProtocolRow.tsx:L6 | neighbors=[ProtocolRow.tsx, ProtocolRow()]
- "dashboard_slarow_getsla": "getSla()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L6 | neighbors=[SlaRow.tsx, SlaRow()]
- "dashboard_slastatus_pct": "pct()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L54 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "dashboard_slastatus_slastatus": "SlaStatus()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L115 | neighbors=[page.tsx, SlaStatus.tsx]
- "dashboard_slastatus_timelabel": "timeLabel()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L46 | neighbors=[SlaStatus.tsx, SlaRowView()]
- "dashboard_slasummarycell_slasummarycell": "SlaSummaryCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaSummaryCell.tsx:L11 | neighbors=[SlaSummaryCell.tsx, page.tsx]
- "data_mock_dashboard_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L11 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_attack_paths": "ATTACK_PATHS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L41 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_pathstatus": "PathStatus" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L10 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L31 | neighbors=[ProtocolRow.tsx, mock-dashboard.ts]
- "data_mock_dashboard_protocols": "PROTOCOLS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L57 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_sla_findings": "SLA_FINDINGS" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L49 | neighbors=[mock-dashboard.ts, page.tsx]
- "data_mock_dashboard_slafinding": "SlaFinding" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L22 | neighbors=[SlaRow.tsx, mock-dashboard.ts]
- "data_mock_dashboard_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L36 | neighbors=[ZoneRow.tsx, mock-dashboard.ts]
- "data_mock_dashboard_zones": "ZONES" | kind=code-symbol | source=manager/frontend/data/mock-dashboard.ts:L64 | neighbors=[mock-dashboard.ts, page.tsx]
- "detection_correlator_detectioncorrelator_generate_gap_report": ".generate_gap_report()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L192 | neighbors=[DetectionCorrelator, DetectionGap]
- "detection_correlator_host_matches": "_host_matches()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L68 | neighbors=[correlator.py, ._host_for()]
- "detection_edr_crowdstrikefalcon_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L98 | neighbors=[CrowdStrikeFalcon, ._request()]
- "detection_edr_microsoftdefender_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L147 | neighbors=[MicrosoftDefender, ._request()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-051.json

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
