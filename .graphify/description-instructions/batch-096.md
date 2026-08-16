# Node Description Batch 97 of 209

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

- "scanner_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "scanner_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L77 | neighbors=[web_scanner.py, parse_allow_header()]
- "scanner_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/web_scanner.py:L54 | neighbors=[web_scanner.py, .redirect_request()]
- "scanner_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L142 | neighbors=[WebScanner, .scan_target()]
- "scanner_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L159 | neighbors=[WebScanner, ._scan_port()]
- "scanner_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "scanner_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "schemas_ai_aigenerateresponse": "AiGenerateResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L58 | neighbors=[ai.py, BaseModel]
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
- "schemas_engagement_validate_engagement_dates": "validate_engagement_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L30 | neighbors=[engagement.py, .validate_dates()]
- "schemas_finding_findingout_populate_risk_rank": "._populate_risk_rank()" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L104 | neighbors=[FindingOut, Compute the explainable 0-1000 unified …]
- "schemas_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/schemas/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "schemas_portal_clientengagementout": "ClientEngagementOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L40 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientpostureout": "ClientPostureOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L51 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientreportcontent": "ClientReportContent" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L88 | neighbors=[portal.py, ClientReportOut]
- "schemas_portal_clientscanout": "ClientScanOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L92 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clientscanrequestout": "ClientScanRequestOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L114 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clienttrendpoint": "ClientTrendPoint" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L69 | neighbors=[portal.py, BaseModel]
- "schemas_portal_clienttrendsout": "ClientTrendsOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L75 | neighbors=[portal.py, BaseModel]
- "scripts_seed_admin_hash": "_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L135 | neighbors=[seed_admin.py, _seed_once()]
- "scripts_seed_admin_verify_hash": "_verify_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L139 | neighbors=[seed_admin.py, _seed_once()]
- "scripts_startup_validator_validationreport_print_summary": ".print_summary()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L56 | neighbors=[run_all_validators(), ValidationReport]
- "services_analytics_compute_exposure": "compute_exposure()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L35 | neighbors=[analytics.py, _sev()]
- "services_analytics_sev": "_sev()" | kind=code-symbol | source=manager/backend/app/services/analytics.py:L31 | neighbors=[analytics.py, compute_exposure()]
- "services_audit_record_audit": "record_audit()" | kind=code-symbol | source=manager/backend/app/services/audit.py:L13 | neighbors=[audit.py, Append one immutable audit row (caller …]
- "services_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/services/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2885afa Add comprehensive probe testing…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-096.json

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
