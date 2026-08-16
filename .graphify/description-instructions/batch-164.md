# Node Description Batch 165 of 209

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

- "scanner_udp_scanner_rationale_78": "Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing     AES-256-" | kind=entity | source=probe/scanner/udp_scanner.py:L78 | neighbors=[_ike_probe()] | lang=fr
- "scanner_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L54 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L279 | neighbors=[UDPScanner] | lang=en
- "scanner_udp_scanner_udpscanner_send_recv": "._send_recv()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L157 | neighbors=[UDPScanner] | lang=en
- "scanner_unauth_access_is_rce_capable": "is_rce_capable()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L68 | neighbors=[unauth_access.py] | lang=en
- "scanner_unauth_access_rationale_49": "Decide whether `banner` proves unauthenticated access for `service`.      True =" | kind=entity | source=probe/scanner/unauth_access.py:L49 | neighbors=[classify_unauth_access()] | lang=en
- "scanner_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=probe/scanner/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "scanner_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=probe/scanner/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "scanner_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=probe/scanner/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "scanner_web_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L165 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L55 | neighbors=[_NoRedirect] | lang=en
- "scanner_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=probe/scanner/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_rationale_45": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=probe/scanner/web_scanner.py:L45 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L138 | neighbors=[WebScanner] | lang=en
- "scanner_windows_collector_main": "main()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=probe/scanner/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=probe/scanner/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "scanner_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "scanner_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "scans_page_intensities": "INTENSITIES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L22 | neighbors=[page.tsx] | lang=en
- "scans_page_looksliketarget": "looksLikeTarget()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L39 | neighbors=[page.tsx] | lang=en
- "scans_page_portalscans": "PortalScans()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L48 | neighbors=[page.tsx] | lang=en
- "scans_page_scan_types": "SCAN_TYPES" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L11 | neighbors=[page.tsx] | lang=en
- "scans_page_status_style": "STATUS_STYLE" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L8 | neighbors=[page.tsx] | lang=en
- "scans_page_status_var": "STATUS_VAR" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L28 | neighbors=[page.tsx] | lang=en
- "schemas_ai_aigeneraterequest_validate_bounded_input": ".validate_bounded_input()" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L27 | neighbors=[AiGenerateRequest] | lang=en
- "schemas_asset_assetin_validate_ip": ".validate_ip()" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L23 | neighbors=[AssetIn] | lang=en
- "schemas_auth_rationale_18": "Parsed from JWT claims — attached to request.state and injected as dependency." | kind=entity | source=manager/backend/app/schemas/auth.py:L18 | neighbors=[CurrentUser] | lang=en
- "schemas_auth_rationale_21": "Parsed from JWT claims — attached to request.state and injected as dependency." | kind=entity | source=manager/backend/app/schemas/auth.py:L21 | neighbors=[CurrentUser] | lang=en
- "schemas_engagement_engagementcreate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L54 | neighbors=[EngagementCreate] | lang=en
- "schemas_finding_rationale_105": "Compute the explainable 0-1000 unified rank at serialization time so         eve" | kind=entity | source=manager/backend/app/schemas/finding.py:L105 | neighbors=[._populate_risk_rank()] | lang=en
- "schemas_finding_rationale_22": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L22 | neighbors=[FindingPatch] | lang=en
- "schemas_portal_rationale_1": "schemas/portal.py — customer-safe response shapes.  CRITICAL: these are WHITELIS" | kind=entity | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[portal.py] | lang=en
- "schemas_portal_rationale_101": "A customer's rich scan request. The customer may ask for any active scan     typ" | kind=entity | source=manager/backend/app/schemas/portal.py:L101 | neighbors=[ScanRequestCreate] | lang=en
- "schemas_portal_rationale_23": "A finding as a CUSTOMER may see it. model_validate(from_attributes=True)     rea" | kind=entity | source=manager/backend/app/schemas/portal.py:L23 | neighbors=[ClientFindingOut] | lang=en
- "schemas_portal_rationale_60": "One call powering the dashboard header: posture + KPI counts + queue state." | kind=entity | source=manager/backend/app/schemas/portal.py:L60 | neighbors=[ClientSummaryOut] | lang=en
- "scripts_seed_admin_rationale_151": "Warn if the tenant has multiple admins or a stale admin email." | kind=entity | source=manager/backend/scripts/seed_admin.py:L151 | neighbors=[_detect_drift()] | lang=en
- "scripts_seed_admin_rationale_193": "All DB work in a single transaction. Rolls back on any failure.     Verifies the" | kind=entity | source=manager/backend/scripts/seed_admin.py:L193 | neighbors=[_seed_once()] | lang=en
- "scripts_seed_admin_rationale_295": "Exponential-backoff retry for transient DB connectivity issues." | kind=entity | source=manager/backend/scripts/seed_admin.py:L295 | neighbors=[_seed_with_retry()] | lang=en
- "scripts_seed_admin_rationale_96": "Returns (email, password, tenant_name, force_reset).     Raises SeedConfiguratio" | kind=entity | source=manager/backend/scripts/seed_admin.py:L96 | neighbors=[_validate_env()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-164.json

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
