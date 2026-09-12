# Node Description Batch 155 of 380

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

- "path_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L56 | neighbors=[route.ts, proxyPortal()]
- "portal_timestamp_formatcompact": "formatCompact()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L35 | neighbors=[Timestamp.tsx, Timestamp()]
- "portal_timestamp_formatexact": "formatExact()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L23 | neighbors=[Timestamp.tsx, Timestamp()]
- "portal_timestamp_formatrelative": "formatRelative()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L47 | neighbors=[Timestamp.tsx, Timestamp()]
- "portal_timestamp_isoutc": "isoUtc()" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L62 | neighbors=[Timestamp.tsx, Timestamp()]
- "portscan_family_of": "family_of()" | kind=code-symbol | source=portscan.py:L83 | neighbors=[portscan.py, ._attempt()]
- "portscan_parse_ports": "parse_ports()" | kind=code-symbol | source=portscan.py:L199 | neighbors=[portscan.py, main()]
- "portscan_portscanner_init": ".__init__()" | kind=code-symbol | source=portscan.py:L113 | neighbors=[PortScanner, RateLimiter]
- "portscan_portscanner_record": "._record()" | kind=code-symbol | source=portscan.py:L124 | neighbors=[PortScanner, ._attempt()]
- "portscan_ratelimiter_wait": ".wait()" | kind=code-symbol | source=portscan.py:L101 | neighbors=[.scan_port(), RateLimiter]
- "posture_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/posture/route.ts:L10 | neighbors=[route.ts, operator-routes.test.ts]
- "prompts_exploit_builder": "exploit-builder.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/exploit-builder.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "prompts_report_attacknarrativeout": "AttackNarrativeOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L172 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_buildreportusermessage": "buildReportUserMessage()" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L346 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_buildscorecard": "buildScorecard()" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L209 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_controlsobservedout": "ControlsObservedOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L184 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_findingwriteupout": "FindingWriteupOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L179 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_limitationsout": "LimitationsOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L185 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_normaliseseverity": "normaliseSeverity()" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L36 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_remediationgroup": "RemediationGroup" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L110 | neighbors=[report.ts, page.tsx]
- "prompts_report_remediationgroupingout": "RemediationGroupingOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L176 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_reportdecision": "ReportDecision" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L126 | neighbors=[report.ts, page.tsx]
- "prompts_report_reportresult": "ReportResult" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L141 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_scorecard": "Scorecard" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L63 | neighbors=[report.ts, page.tsx]
- "prompts_report_scorecardinput": "ScorecardInput" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L43 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_sections_buildsectioninput": "buildSectionInput()" | kind=code-symbol | source=manager/frontend/lib/prompts/report-sections.ts:L452 | neighbors=[ai-engine.ts, report-sections.ts]
- "prompts_report_sections_section_prompts": "SECTION_PROMPTS" | kind=code-symbol | source=manager/frontend/lib/prompts/report-sections.ts:L424 | neighbors=[ai-engine.ts, report-sections.ts]
- "prompts_report_sections_sectionkey": "SectionKey" | kind=code-symbol | source=manager/frontend/lib/prompts/report-sections.ts:L433 | neighbors=[ai-engine.ts, report-sections.ts]
- "prompts_report_validatereport": "validateReport()" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L398 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_verdictsummaryout": "VerdictSummaryOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L171 | neighbors=[ai-engine.ts, report.ts]
- "raw_facts_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L12 | neighbors=[route.ts, GET()]
- "raw_facts_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L17 | neighbors=[route.ts, fail()]
- "remediation_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L7 | neighbors=[route.ts, GET()]
- "remediation_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L15 | neighbors=[route.ts, fail()]
- "reopen_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L11 | neighbors=[route.ts, POST()]
- "reopen_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L16 | neighbors=[route.ts, fail()]
- "report_adapt_portaltorawfinding": "portalToRawFinding()" | kind=code-symbol | source=manager/frontend/lib/report/adapt.ts:L79 | neighbors=[adapt.ts, report-portal-adapt.test.ts]
- "report_finding_model_detectionmethod": "DetectionMethod" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L131 | neighbors=[adapt.ts, finding-model.ts]
- "report_finding_model_joinlist": "joinList()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L360 | neighbors=[finding-model.ts, attackerStatement()]
- "report_finding_model_parsecvss": "parseCvss()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L690 | neighbors=[finding-model.ts, assess()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-154.json

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
