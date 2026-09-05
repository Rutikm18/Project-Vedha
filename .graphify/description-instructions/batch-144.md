# Node Description Batch 145 of 336

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

- "scanner_udp_scanner_tftp_probe": "_tftp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L132 | neighbors=[udp_scanner.py, TFTP RRQ for a non-existent file.  Erro…]
- "scanner_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L386 | neighbors=[UDPScanner, ._probe()]
- "scanner_unauth_access_as_text": "_as_text()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L40 | neighbors=[unauth_access.py, classify_unauth_access()]
- "scanner_va_campaign_atomic_write_json": "_atomic_write_json()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L282 | neighbors=[va_campaign.py, ._flush()]
- "scanner_va_campaign_bounded_gather": "_bounded_gather()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L374 | neighbors=[va_campaign.py, Run coro_factory(item) over items with …]
- "scanner_va_campaign_campaignoptions": "CampaignOptions" | kind=code-symbol | source=probe/scanner/va_campaign.py:L97 | neighbors=[va_campaign.py, Everything that changes WHAT the campai…]
- "scanner_va_campaign_cliprogressview_format": "._format()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L690 | neighbors=[CliProgressView, ._redraw()]
- "scanner_va_campaign_cliprogressview_transitions": "._transitions()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L678 | neighbors=[CliProgressView, .__call__()]
- "scanner_va_campaign_discover_ipv6": "_discover_ipv6()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L343 | neighbors=[va_campaign.py, Best-effort IPv6 neighbor discovery (ND…]
- "scanner_va_campaign_progressreporter_current": "._current()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L230 | neighbors=[ProgressReporter, .snapshot()]
- "scanner_va_campaign_progressreporter_percent": "._percent()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L222 | neighbors=[ProgressReporter, .snapshot()]
- "scanner_va_campaign_stage": "Stage" | kind=code-symbol | source=probe/scanner/va_campaign.py:L126 | neighbors=[va_campaign.py, default_stages()]
- "scanner_va_campaign_stageoutcome": "StageOutcome" | kind=code-symbol | source=probe/scanner/va_campaign.py:L113 | neighbors=[va_campaign.py, What a stage produced. `count` is stage…]
- "scanner_va_campaign_stagestate_to_dict": ".to_dict()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L161 | neighbors=[.snapshot(), StageState]
- "scanner_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "scanner_vnc_scanner_vncscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L127 | neighbors=[VNCScanner, .scan_target()]
- "scanner_vnc_scanner_vncscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L145 | neighbors=[VNCScanner, ._scan_port()]
- "scanner_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L78 | neighbors=[web_scanner.py, parse_allow_header()]
- "scanner_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/web_scanner.py:L55 | neighbors=[web_scanner.py, .redirect_request()]
- "scanner_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L176 | neighbors=[WebScanner, ._scan_port()]
- "scanner_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "scanner_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "scans_page_prettytype": "prettyType()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L75 | neighbors=[page.tsx, JobCard()]
- "scans_page_reltime": "relTime()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L74 | neighbors=[page.tsx, JobCard()]
- "schemas_ai_aigenerateresponse": "AiGenerateResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L59 | neighbors=[ai.py, BaseModel]
- "schemas_ai_aimessage": "AiMessage" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L13 | neighbors=[ai.py, BaseModel]
- "schemas_auth_loginrequest": "LoginRequest" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L9 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreate": "PersonalAccessTokenCreate" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L35 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreated": "PersonalAccessTokenCreated" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L41 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokenout": "PersonalAccessTokenOut" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L52 | neighbors=[auth.py, BaseModel]
- "schemas_auth_tokenresponse": "TokenResponse" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L14 | neighbors=[auth.py, BaseModel]
- "schemas_common_errordetail": "ErrorDetail" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L18 | neighbors=[common.py, BaseModel]
- "schemas_common_paginate": "paginate()" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L22 | neighbors=[common.py, PaginatedResponse]
- "schemas_engagement_engagementcreate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L66 | neighbors=[EngagementCreate, validate_engagement_dates()]
- "schemas_engagement_engagementcreate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L62 | neighbors=[EngagementCreate, validate_scope_entries()]
- "schemas_engagement_rationale_13": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L13 | neighbors=[validate_scope_entries(), EngagementStatus]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-144.json

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
