# Node Description Batch 264 of 336

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

- "scanner_web_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L182 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "scanner_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/scanner/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_rationale_149": "Preferred scheme first, the other as a fallback: a scheme guess must         nev" | kind=entity | source=probe/scanner/web_scanner.py:L149 | neighbors=[._schemes_for()] | lang=pt
- "scanner_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/scanner/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_rationale_46": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/scanner/web_scanner.py:L46 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L139 | neighbors=[WebScanner] | lang=en
- "scanner_windows_collector_main": "main()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/scanner/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/scanner/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "scanner_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "scanner_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "scans_page_field": "Field()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L114 | neighbors=[page.tsx] | lang=en
- "scans_page_group": "Group()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L172 | neighbors=[page.tsx] | lang=en
- "scans_page_intensities": "INTENSITIES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L18 | neighbors=[page.tsx] | lang=en
- "scans_page_jobmeta": "JobMeta" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L38 | neighbors=[page.tsx] | lang=en
- "scans_page_looksliketarget": "looksLikeTarget()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L26 | neighbors=[page.tsx] | lang=en
- "scans_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L36 | neighbors=[page.tsx] | lang=en
- "scans_page_phaseticker": "PhaseTicker()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L85 | neighbors=[page.tsx] | lang=en
- "scans_page_portalscans": "PortalScans()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L184 | neighbors=[page.tsx] | lang=en
- "scans_page_scan_types": "SCAN_TYPES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L11 | neighbors=[page.tsx] | lang=en
- "scans_page_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L8 | neighbors=[page.tsx] | lang=en
- "scans_page_status_var": "STATUS_VAR" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L28 | neighbors=[page.tsx] | lang=en
- "scans_page_statusicon": "StatusIcon()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "schemas_ai_aigeneraterequest_validate_bounded_input": ".validate_bounded_input()" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L28 | neighbors=[AiGenerateRequest] | lang=en
- "schemas_asset_assetin_validate_ip": ".validate_ip()" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L23 | neighbors=[AssetIn] | lang=en
- "schemas_auth_rationale_18": "Parsed from JWT claims — attached to request.state and injected as dependency." | kind=entity | source=manager/backend/app/schemas/auth.py:L18 | neighbors=[CurrentUser] | lang=en
- "schemas_auth_rationale_21": "Parsed from JWT claims — attached to request.state and injected as dependency." | kind=entity | source=manager/backend/app/schemas/auth.py:L21 | neighbors=[CurrentUser] | lang=en
- "schemas_engagement_engagementcreate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L54 | neighbors=[EngagementCreate] | lang=en
- "schemas_finding_findingpatch_normalize_action_reason": ".normalize_action_reason()" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L38 | neighbors=[FindingPatch] | lang=en
- "schemas_finding_findingreopen_normalize_reason": ".normalize_reason()" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L49 | neighbors=[FindingReopen] | lang=en
- "schemas_finding_rationale_105": "Compute the explainable 0-1000 unified rank at serialization time so         eve" | kind=entity | source=manager/backend/app/schemas/finding.py:L105 | neighbors=[._populate_risk_rank()] | lang=en
- "schemas_finding_rationale_161": "Compute the explainable 0-1000 unified rank at serialization time so         eve" | kind=entity | source=manager/backend/app/schemas/finding.py:L161 | neighbors=[._populate_risk_rank()] | lang=en
- "schemas_finding_rationale_22": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L22 | neighbors=[FindingPatch] | lang=en
- "schemas_finding_rationale_69": "One entry in a finding's lifecycle timeline. `id` is null for synthesized     ev" | kind=entity | source=manager/backend/app/schemas/finding.py:L69 | neighbors=[FindingEventOut] | lang=en
- "schemas_portal_clientassistantask_bounded": "._bounded()" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L142 | neighbors=[ClientAssistantAsk] | lang=en
- "schemas_portal_rationale_1": "schemas/portal.py — customer-safe response shapes.  CRITICAL: these are WHITELIS" | kind=entity | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[portal.py] | lang=en
- "schemas_portal_rationale_101": "A customer's rich scan request. The customer may ask for any active scan     typ" | kind=entity | source=manager/backend/app/schemas/portal.py:L101 | neighbors=[ScanRequestCreate] | lang=en
- "schemas_portal_rationale_129": "One turn of the customer's conversation. Bounded so a crafted client can't     p" | kind=entity | source=manager/backend/app/schemas/portal.py:L129 | neighbors=[ClientAssistantMessage] | lang=en
- "schemas_portal_rationale_23": "A finding as a CUSTOMER may see it. model_validate(from_attributes=True)     rea" | kind=entity | source=manager/backend/app/schemas/portal.py:L23 | neighbors=[ClientFindingOut] | lang=en

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
