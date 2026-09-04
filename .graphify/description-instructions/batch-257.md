# Node Description Batch 258 of 330

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

- "scanner_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/scanner/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "scanner_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/scanner/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "scanner_vnc_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L150 | neighbors=[vnc_scanner.py] | lang=en
- "scanner_vnc_scanner_rationale_1": "vnc_scanner.py — VNC/RFB authentication exposure (VA checklist: unauthenticated" | kind=entity | source=probe/scanner/vnc_scanner.py:L1 | neighbors=[vnc_scanner.py] | lang=en
- "scanner_vnc_scanner_rationale_109": "Blocking: RFB version handshake + read offered security types.         Monkeypat" | kind=entity | source=probe/scanner/vnc_scanner.py:L109 | neighbors=[._probe()] | lang=en
- "scanner_vnc_scanner_rationale_47": "Parse a 'RFB 003.008' banner into (major, minor), or None if not RFB." | kind=entity | source=probe/scanner/vnc_scanner.py:L47 | neighbors=[parse_rfb_version()] | lang=pt
- "scanner_vnc_scanner_rationale_61": "Turn a list of offered security-type ids into a verdict." | kind=entity | source=probe/scanner/vnc_scanner.py:L61 | neighbors=[classify_security_types()] | lang=pt
- "scanner_vnc_scanner_rationale_82": "Read the offered security types, handling the RFB 3.3 (single 4-byte type)     v" | kind=entity | source=probe/scanner/vnc_scanner.py:L82 | neighbors=[_read_security_types()] | lang=en
- "scanner_vnc_scanner_vncscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L104 | neighbors=[VNCScanner] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-257.json

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
