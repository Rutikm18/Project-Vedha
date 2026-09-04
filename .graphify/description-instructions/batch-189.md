# Node Description Batch 190 of 330

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

- "dashboard_posturescorecard_delta": "Delta()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L45 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_dial": "Dial()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L57 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_grade": "GRADE" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L44 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_grade_color": "GRADE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L39 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_metrictile": "MetricTile()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L95 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_posture": "Posture" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L29 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_readout": "Readout()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L82 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_scores": "Scores" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L23 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_posturescorecard_statcard": "StatCard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L55 | neighbors=[PostureScorecard.tsx] | lang=en
- "dashboard_slastatus_sev": "Sev" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L17 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_sev_style": "SEV_STYLE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L37 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_slaitem": "SlaItem" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L33 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_slastate": "SlaState" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L31 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_slasummary": "SlaSummary" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L38 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_state": "STATE" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L43 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_state_color": "STATE_COLOR" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L30 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_statecell": "StateCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L83 | neighbors=[SlaStatus.tsx] | lang=en
- "dashboard_slastatus_summarycell": "SummaryCell()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L61 | neighbors=[SlaStatus.tsx] | lang=en
- "declarativebase": "DeclarativeBase" | kind=code-symbol | neighbors=[Base] | lang=en
- "detection_active_validation_rationale_1": "active_validation.py — manager-side decision core for safe active validation.  P" | kind=entity | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[active_validation.py] | lang=en
- "detection_active_validation_rationale_18": "True iff this finding warrants an approval-gated active re-check.     Escalate o" | kind=entity | source=manager/backend/app/detection/active_validation.py:L18 | neighbors=[should_escalate()] | lang=en
- "detection_active_validation_rationale_41": "Map a probe safe-check result to a verdict transition. Anything that isn't     a" | kind=entity | source=manager/backend/app/detection/active_validation.py:L41 | neighbors=[interpret_validation()] | lang=pt
- "detection_attack_paths_bump": "_bump()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L45 | neighbors=[attack_paths.py] | lang=en
- "detection_attack_paths_cleartext_cluster": "_cleartext_cluster()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L202 | neighbors=[attack_paths.py] | lang=en
- "detection_attack_paths_hostsignals_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L65 | neighbors=[_HostSignals] | lang=en
- "detection_attack_paths_rationale_1": "attack_paths.py — manager-native composite correlation over raw probe facts.  Th" | kind=entity | source=manager/backend/app/detection/attack_paths.py:L1 | neighbors=[attack_paths.py] | lang=en
- "detection_attack_paths_rationale_125": "Fold in a persisted device role (from a prior device_inventory scan)." | kind=entity | source=manager/backend/app/detection/attack_paths.py:L125 | neighbors=[.finalize()] | lang=en
- "detection_attack_paths_rationale_222": "B3: an exposed datastore with unauthenticated access = direct data breach." | kind=entity | source=manager/backend/app/detection/attack_paths.py:L222 | neighbors=[_exposed_db_unauth()] | lang=en
- "detection_attack_paths_rationale_243": "B3: a default SNMP community on network gear = topology/creds for lateral moveme" | kind=entity | source=manager/backend/app/detection/attack_paths.py:L243 | neighbors=[_snmp_public_lateral()] | lang=en
- "detection_attack_paths_rationale_276": "Correlate composite attack paths from raw probe facts.      `device_roles` maps" | kind=entity | source=manager/backend/app/detection/attack_paths.py:L276 | neighbors=[attack_path_findings()] | lang=en
- "detection_attack_paths_rationale_63": "The weaknesses observed on ONE host, distilled from its facts." | kind=entity | source=manager/backend/app/detection/attack_paths.py:L63 | neighbors=[_HostSignals] | lang=en
- "detection_correlator_detectioncorrelator_compute_coverage": ".compute_coverage()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L181 | neighbors=[DetectionCorrelator] | lang=en
- "detection_correlator_detectioncorrelator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L96 | neighbors=[DetectionCorrelator] | lang=en
- "detection_correlator_rationale_238": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L238 | neighbors=[_aware()] | lang=en
- "detection_edr_build_edr_engine": "build_edr_engine()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L235 | neighbors=[edr.py] | lang=en
- "detection_edr_edrdetection_is_prevented": ".is_prevented()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L43 | neighbors=[EDRDetection] | lang=en
- "detection_edr_edrqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L65 | neighbors=[EDRQueryEngine] | lang=en
- "detection_edr_edrqueryengine_query_detections": ".query_detections()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L70 | neighbors=[EDRQueryEngine] | lang=en
- "detection_edr_rationale_1": "EDR query engines — abstract interface + CrowdStrike Falcon / Microsoft Defender" | kind=entity | source=manager/backend/app/detection/edr.py:L1 | neighbors=[edr.py] | lang=en
- "detection_edr_rationale_141": "Microsoft Defender via the Graph Security API ``/security/alerts_v2``.     confi" | kind=entity | source=manager/backend/app/detection/edr.py:L141 | neighbors=[MicrosoftDefender] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-189.json

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
