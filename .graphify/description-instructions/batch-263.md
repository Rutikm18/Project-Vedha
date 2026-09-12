# Node Description Batch 264 of 380

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

- "report_findingreport_copybutton": "CopyButton()" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L70 | neighbors=[FindingReport.tsx]
- "report_findingreport_evidenceartifact": "EvidenceArtifact()" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L133 | neighbors=[FindingReport.tsx]
- "report_findingreport_findingreportprops": "FindingReportProps" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L217 | neighbors=[FindingReport.tsx]
- "report_findingreport_gap": "Gap()" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L107 | neighbors=[FindingReport.tsx]
- "report_findingreport_prose": "Prose()" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L118 | neighbors=[FindingReport.tsx]
- "report_findingreport_reportmode": "ReportMode" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L40 | neighbors=[FindingReport.tsx]
- "report_findingreport_reportmodecontext": "ReportModeContext" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L41 | neighbors=[FindingReport.tsx]
- "report_findingreport_section": "Section()" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L85 | neighbors=[FindingReport.tsx]
- "report_findingreport_sevfilter": "SevFilter" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L570 | neighbors=[FindingReport.tsx]
- "report_findingreport_sevtag": "SevTag()" | kind=code-symbol | source=manager/frontend/components/report/FindingReport.tsx:L57 | neighbors=[FindingReport.tsx]
- "reports_layout_metadata": "metadata" | kind=code-symbol | source=manager/frontend/app/reports/layout.tsx:L8 | neighbors=[layout.tsx]
- "reports_layout_reportslayout": "ReportsLayout()" | kind=code-symbol | source=manager/frontend/app/reports/layout.tsx:L13 | neighbors=[layout.tsx]
- "reports_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L49 | neighbors=[page.tsx]
- "reports_page_aidraft": "AiDraft" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L46 | neighbors=[page.tsx]
- "reports_page_aijobstatus": "AiJobStatus" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L45 | neighbors=[page.tsx]
- "reports_page_aipanel": "AiPanel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L415 | neighbors=[page.tsx]
- "reports_page_aireportpanel": "AiReportPanel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L403 | neighbors=[page.tsx]
- "reports_page_compliancecontrol": "ComplianceControl" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L12 | neighbors=[page.tsx]
- "reports_page_complianceframework": "ComplianceFramework" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L10 | neighbors=[page.tsx]
- "reports_page_complianceframeworkdata": "ComplianceFrameworkData" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L22 | neighbors=[page.tsx]
- "reports_page_compliancereport": "ComplianceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L267 | neighbors=[page.tsx]
- "reports_page_conf_style": "CONF_STYLE" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L149 | neighbors=[page.tsx]
- "reports_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L126 | neighbors=[page.tsx]
- "reports_page_coveragetab": "CoverageTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L744 | neighbors=[page.tsx]
- "reports_page_cvetab": "CveTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L683 | neighbors=[page.tsx]
- "reports_page_decisionbox": "DecisionBox()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L382 | neighbors=[page.tsx]
- "reports_page_documentstab": "DocumentsTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L586 | neighbors=[page.tsx]
- "reports_page_domain_label": "DOMAIN_LABEL" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L133 | neighbors=[page.tsx]
- "reports_page_effortdot": "EffortDot()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L161 | neighbors=[page.tsx]
- "reports_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L32 | neighbors=[page.tsx]
- "reports_page_evidblock": "EvidBlock()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L201 | neighbors=[page.tsx]
- "reports_page_evidenceitem": "EvidenceItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L39 | neighbors=[page.tsx]
- "reports_page_evidencereport": "EvidenceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L230 | neighbors=[page.tsx]
- "reports_page_evidencestats": "evidenceStats" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L35 | neighbors=[page.tsx]
- "reports_page_evidencesummary": "EvidenceSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L717 | neighbors=[page.tsx]
- "reports_page_evidtab": "EvidTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L998 | neighbors=[page.tsx]
- "reports_page_exectab": "ExecTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L588 | neighbors=[page.tsx]
- "reports_page_executivedoc": "ExecutiveDoc()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L86 | neighbors=[page.tsx]
- "reports_page_executivereport": "ExecutiveReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L155 | neighbors=[page.tsx]
- "reports_page_executivesummary": "ExecutiveSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L546 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-263.json

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
