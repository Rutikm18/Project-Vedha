# Node Description Batch 107 of 332

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

- "scanner_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…, UPnP/SSDP M-SEARCH — unicast to target:…]
- "scanner_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "scanner_va_campaign_campaigncontext": "CampaignContext" | kind=code-symbol | source=probe/scanner/va_campaign.py:L138 | neighbors=[va_campaign.py, build_campaign(), Mutable state threaded through the stag…]
- "scanner_va_campaign_cliprogressview_call": ".__call__()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L663 | neighbors=[CliProgressView, ._redraw(), ._transitions()]
- "scanner_va_campaign_cliprogressview_redraw": "._redraw()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L669 | neighbors=[CliProgressView, .__call__(), ._format()]
- "scanner_va_campaign_monotonic": "_monotonic()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L276 | neighbors=[va_campaign.py, ._eta_seconds(), .__init__()]
- "scanner_va_campaign_progressreporter_eta_seconds": "._eta_seconds()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L236 | neighbors=[ProgressReporter, _monotonic(), .snapshot()]
- "scanner_va_campaign_progressreporter_finish": ".finish()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L217 | neighbors=[ProgressReporter, ._flush(), .run()]
- "scanner_va_campaign_progressreporter_set_totals": ".set_totals()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L213 | neighbors=[ProgressReporter, ._flush(), ._refresh_totals()]
- "scanner_va_campaign_run_campaign": "run_campaign()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L639 | neighbors=[va_campaign.py, build_campaign(), .run()]
- "scanner_va_campaign_stagestate": "StageState" | kind=code-symbol | source=probe/scanner/va_campaign.py:L151 | neighbors=[va_campaign.py, .__init__(), .to_dict()]
- "scanner_va_campaign_vacampaign_refresh_totals": "._refresh_totals()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L322 | neighbors=[VACampaign, .set_totals(), .run()]
- "scanner_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "scanner_vnc_scanner_classify_security_types": "classify_security_types()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L60 | neighbors=[vnc_scanner.py, Turn a list of offered security-type id…, ._probe()]
- "scanner_vnc_scanner_parse_rfb_version": "parse_rfb_version()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L46 | neighbors=[vnc_scanner.py, Parse a 'RFB 003.008' banner into (majo…, ._probe()]
- "scanner_vnc_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L71 | neighbors=[vnc_scanner.py, _read_security_types(), ._probe()]
- "scanner_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L155 | neighbors=[WebScanner, ._schemes_for(), .scan_target()]
- "scanner_web_scanner_webscanner_schemes_for": "._schemes_for()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L148 | neighbors=[Preferred scheme first, the other as a …, WebScanner, ._scan_port()]
- "scans_page_jobcard": "JobCard()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L125 | neighbors=[page.tsx, prettyType(), relTime()]
- "schemas_engagement_rationale_14": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L14 | neighbors=[EngagementStatus, FindingSeverity, validate_scope_entries()]
- "schemas_finding_findingeventout": "FindingEventOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L68 | neighbors=[finding.py, BaseModel, One entry in a finding's lifecycle time…]
- "schemas_finding_findingout_populate_risk_rank": "._populate_risk_rank()" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L160 | neighbors=[FindingOut, Compute the explainable 0-1000 unified …, Compute the explainable 0-1000 unified …]
- "schemas_finding_findingreopen": "FindingReopen" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L44 | neighbors=[finding.py, BaseModel, .normalize_reason()]
- "schemas_portal_clientassistantask": "ClientAssistantAsk" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L135 | neighbors=[portal.py, BaseModel, ._bounded()]
- "schemas_portal_clientassistantmessage": "ClientAssistantMessage" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L128 | neighbors=[portal.py, BaseModel, One turn of the customer's conversation…]
- "schemas_portal_clientfindingout": "ClientFindingOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L22 | neighbors=[portal.py, BaseModel, A finding as a CUSTOMER may see it. mod…]
- "schemas_portal_clientreportout": "ClientReportOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L80 | neighbors=[portal.py, ClientReportContent, BaseModel]
- "schemas_portal_clientsummaryout": "ClientSummaryOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L59 | neighbors=[portal.py, BaseModel, One call powering the dashboard header:…]
- "schemas_portal_scanrequestcreate": "ScanRequestCreate" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L100 | neighbors=[portal.py, A customer's rich scan request. The cus…, BaseModel]
- "schemas_remediation_remediationplandetailout": "RemediationPlanDetailOut" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L28 | neighbors=[remediation.py, BaseModel, .normalize_risk_levels()]
- "schemas_remediation_remediationstepout": "RemediationStepOut" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L11 | neighbors=[remediation.py, BaseModel, .normalize_risk()]
- "scripts_startup_validator_appenvironmentvalidator": "AppEnvironmentValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L151 | neighbors=[startup_validator.py, .validate(), Validates APP_ENV and related productio…]
- "scripts_startup_validator_appenvironmentvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L154 | neighbors=[AppEnvironmentValidator, CheckResult, .add()]
- "scripts_startup_validator_configvalidator": "ConfigValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L72 | neighbors=[startup_validator.py, .validate(), Validates required env vars are present…]
- "scripts_startup_validator_configvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L93 | neighbors=[ConfigValidator, CheckResult, .add()]
- "scripts_startup_validator_cookievalidator": "CookieValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L214 | neighbors=[startup_validator.py, .validate(), Validates secure cookie configuration.]
- "scripts_startup_validator_cookievalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L217 | neighbors=[CookieValidator, CheckResult, .add()]
- "scripts_startup_validator_corsvalidator": "CorsValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L174 | neighbors=[startup_validator.py, .validate(), Validates CORS_ORIGINS is production-sa…]
- "scripts_startup_validator_corsvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L179 | neighbors=[CorsValidator, CheckResult, .add()]
- "scripts_startup_validator_databaseconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L313 | neighbors=[DatabaseConnectivityValidator, CheckResult, .add()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-106.json

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
