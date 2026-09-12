# Node Description Batch 266 of 380

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "reports_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L524 | neighbors=[page.tsx]
- "reports_page_statuslabel": "statusLabel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L531 | neighbors=[page.tsx]
- "reports_page_statuspill": "StatusPill()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L85 | neighbors=[page.tsx]
- "reports_page_tab": "Tab" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L19 | neighbors=[page.tsx]
- "reports_page_tabs": "TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L53 | neighbors=[page.tsx]
- "reports_page_technicalreport": "TechnicalReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L198 | neighbors=[page.tsx]
- "reports_page_techtab": "TechTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L970 | neighbors=[page.tsx]
- "reports_page_topfindings": "TopFindings()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L65 | neighbors=[page.tsx]
- "reports_page_vm_label": "VM_LABEL" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L90 | neighbors=[page.tsx]
- "reports_page_vm_name": "VM_NAME" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L97 | neighbors=[page.tsx]
- "reports_page_window_style": "WINDOW_STYLE" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L155 | neighbors=[page.tsx]
- "reportsection_finding_model_aggravating": "AGGRAVATING" | kind=code-symbol | source=reportsection/finding-model.ts:L264 | neighbors=[finding-model.ts]
- "reportsection_finding_model_assessedfinding": "AssessedFinding" | kind=code-symbol | source=reportsection/finding-model.ts:L671 | neighbors=[finding-model.ts]
- "reportsection_finding_model_confidence": "Confidence" | kind=code-symbol | source=reportsection/finding-model.ts:L142 | neighbors=[finding-model.ts]
- "reportsection_finding_model_confidencelevel": "ConfidenceLevel" | kind=code-symbol | source=reportsection/finding-model.ts:L140 | neighbors=[finding-model.ts]
- "reportsection_finding_model_detection": "DETECTION" | kind=code-symbol | source=reportsection/finding-model.ts:L151 | neighbors=[finding-model.ts]
- "reportsection_finding_model_detectionmethod": "DetectionMethod" | kind=code-symbol | source=reportsection/finding-model.ts:L131 | neighbors=[finding-model.ts]
- "reportsection_finding_model_gap": "Gap" | kind=code-symbol | source=reportsection/finding-model.ts:L645 | neighbors=[finding-model.ts]
- "reportsection_finding_model_metric_name": "METRIC_NAME" | kind=code-symbol | source=reportsection/finding-model.ts:L240 | neighbors=[finding-model.ts]
- "reportsection_finding_model_metric_value": "METRIC_VALUE" | kind=code-symbol | source=reportsection/finding-model.ts:L248 | neighbors=[finding-model.ts]
- "reportsection_finding_model_outcome": "OUTCOME" | kind=code-symbol | source=reportsection/finding-model.ts:L281 | neighbors=[finding-model.ts]
- "reportsection_finding_model_prereq": "PREREQ" | kind=code-symbol | source=reportsection/finding-model.ts:L266 | neighbors=[finding-model.ts]
- "reportsection_finding_model_priority": "Priority" | kind=code-symbol | source=reportsection/finding-model.ts:L373 | neighbors=[finding-model.ts]
- "reportsection_finding_model_priority_label": "PRIORITY_LABEL" | kind=code-symbol | source=reportsection/finding-model.ts:L382 | neighbors=[finding-model.ts]
- "reportsection_finding_model_prioritycode": "PriorityCode" | kind=code-symbol | source=reportsection/finding-model.ts:L371 | neighbors=[finding-model.ts]
- "reportsection_finding_model_provenance": "Provenance" | kind=code-symbol | source=reportsection/finding-model.ts:L493 | neighbors=[finding-model.ts]
- "reportsection_finding_model_provenanceof": "provenanceOf()" | kind=code-symbol | source=reportsection/finding-model.ts:L500 | neighbors=[finding-model.ts]
- "reportsection_finding_model_rawasset": "RawAsset" | kind=code-symbol | source=reportsection/finding-model.ts:L47 | neighbors=[finding-model.ts]
- "reportsection_finding_model_rawevidence": "RawEvidence" | kind=code-symbol | source=reportsection/finding-model.ts:L34 | neighbors=[finding-model.ts]
- "reportsection_finding_model_rawfinding": "RawFinding" | kind=code-symbol | source=reportsection/finding-model.ts:L79 | neighbors=[finding-model.ts]
- "reportsection_finding_model_rawremediation": "RawRemediation" | kind=code-symbol | source=reportsection/finding-model.ts:L60 | neighbors=[finding-model.ts]
- "reportsection_finding_model_rawverification": "RawVerification" | kind=code-symbol | source=reportsection/finding-model.ts:L72 | neighbors=[finding-model.ts]
- "reportsection_finding_model_redact": "redact()" | kind=code-symbol | source=reportsection/finding-model.ts:L575 | neighbors=[finding-model.ts]
- "reportsection_finding_model_redaction": "Redaction" | kind=code-symbol | source=reportsection/finding-model.ts:L573 | neighbors=[finding-model.ts]
- "reportsection_finding_model_redactionrule": "RedactionRule" | kind=code-symbol | source=reportsection/finding-model.ts:L518 | neighbors=[finding-model.ts]
- "reportsection_finding_model_remediationstep": "RemediationStep" | kind=code-symbol | source=reportsection/finding-model.ts:L602 | neighbors=[finding-model.ts]
- "reportsection_finding_model_remediationtier": "RemediationTier" | kind=code-symbol | source=reportsection/finding-model.ts:L58 | neighbors=[finding-model.ts]
- "reportsection_finding_model_rules": "RULES" | kind=code-symbol | source=reportsection/finding-model.ts:L539 | neighbors=[finding-model.ts]
- "reportsection_finding_model_sla": "Sla" | kind=code-symbol | source=reportsection/finding-model.ts:L443 | neighbors=[finding-model.ts]
- "reportsection_finding_model_sla_days": "SLA_DAYS" | kind=code-symbol | source=reportsection/finding-model.ts:L437 | neighbors=[finding-model.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-265.json

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
