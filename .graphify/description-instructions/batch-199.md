# Node Description Batch 200 of 332

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

- "exploit_orchestrator_exploitorchestrator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L53 | neighbors=[ExploitOrchestrator] | lang=en
- "exploit_safety_approvalrequirederror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L30 | neighbors=[ApprovalRequiredError] | lang=en
- "exploit_safety_rationale_1": "Safety constants, exceptions, and validators for the exploitation engine.  All s" | kind=entity | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[safety.py] | lang=en
- "exploit_safety_rationale_17": "Raised when a requested payload or module is not on the allowlist." | kind=entity | source=manager/backend/app/exploit/safety.py:L17 | neighbors=[SafetyViolationError] | lang=en
- "exploit_safety_rationale_175": "Raises SafetyViolationError if payload is not on allowlist     or violates per-p" | kind=entity | source=manager/backend/app/exploit/safety.py:L175 | neighbors=[validate_payload()] | lang=en
- "exploit_safety_rationale_203": "Raises SafetyViolationError if module is on the block list." | kind=entity | source=manager/backend/app/exploit/safety.py:L203 | neighbors=[validate_module()] | lang=en
- "exploit_safety_rationale_21": "Raised when a target IP is outside the engagement scope CIDRs." | kind=entity | source=manager/backend/app/exploit/safety.py:L21 | neighbors=[OutOfScopeError] | lang=en
- "exploit_safety_rationale_217": "Raises OutOfScopeError if target_ip is not in scope or is excluded." | kind=entity | source=manager/backend/app/exploit/safety.py:L217 | neighbors=[validate_scope()] | lang=en
- "exploit_safety_rationale_240": "True if this target requires human manager approval before exploit runs." | kind=entity | source=manager/backend/app/exploit/safety.py:L240 | neighbors=[requires_approval()] | lang=en
- "exploit_safety_rationale_25": "Raised when a job would exceed the maximum hosts per run." | kind=entity | source=manager/backend/app/exploit/safety.py:L25 | neighbors=[BlastRadiusExceededError] | lang=en
- "exploit_safety_rationale_29": "Raised when a high-risk target requires manager approval before running." | kind=entity | source=manager/backend/app/exploit/safety.py:L29 | neighbors=[ApprovalRequiredError] | lang=pt
- "exposure_route_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L10 | neighbors=[route.ts] | lang=en
- "exposure_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L15 | neighbors=[route.ts] | lang=en
- "findings_page_autoresolvedbadge": "AutoResolvedBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L401 | neighbors=[page.tsx] | lang=en
- "findings_page_chiprow": "ChipRow()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L451 | neighbors=[page.tsx] | lang=en
- "findings_page_compliancepanel": "CompliancePanel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1314 | neighbors=[page.tsx] | lang=en
- "findings_page_complianceref": "ComplianceRef" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L96 | neighbors=[page.tsx] | lang=en
- "findings_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L286 | neighbors=[page.tsx] | lang=en
- "findings_page_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "findings_page_cvechip": "CveChip()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L42 | neighbors=[page.tsx] | lang=en
- "findings_page_cvss_aggravating": "CVSS_AGGRAVATING" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L846 | neighbors=[page.tsx] | lang=en
- "findings_page_cvss_metric": "CVSS_METRIC" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L834 | neighbors=[page.tsx] | lang=en
- "findings_page_cvssmetric": "CvssMetric" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L848 | neighbors=[page.tsx] | lang=en
- "findings_page_detailtab": "DetailTab" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1487 | neighbors=[page.tsx] | lang=en
- "findings_page_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L59 | neighbors=[page.tsx] | lang=en
- "findings_page_detectionpill": "DetectionPill()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L419 | neighbors=[page.tsx] | lang=en
- "findings_page_engagementoption": "EngagementOption" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L214 | neighbors=[page.tsx] | lang=en
- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L268 | neighbors=[page.tsx] | lang=en
- "findings_page_event_color": "EVENT_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1343 | neighbors=[page.tsx] | lang=en
- "findings_page_eventactor": "eventActor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1358 | neighbors=[page.tsx] | lang=en
- "findings_page_eventdetaillabel": "eventDetailLabel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1383 | neighbors=[page.tsx] | lang=en
- "findings_page_eventnarrative": "eventNarrative()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1364 | neighbors=[page.tsx] | lang=en
- "findings_page_evidencegallery": "EvidenceGallery()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L635 | neighbors=[page.tsx] | lang=en
- "findings_page_evidencepresentation": "evidencePresentation()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L618 | neighbors=[page.tsx] | lang=en
- "findings_page_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L58 | neighbors=[page.tsx] | lang=en
- "findings_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L136 | neighbors=[page.tsx] | lang=en
- "findings_page_findingoverview": "FindingOverview()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L962 | neighbors=[page.tsx] | lang=en
- "findings_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L193 | neighbors=[page.tsx] | lang=en
- "findings_page_findingrow": "FindingRow" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L2041 | neighbors=[page.tsx] | lang=en
- "findings_page_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L57 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-199.json

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
