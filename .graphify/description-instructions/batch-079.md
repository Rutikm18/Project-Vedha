# Node Description Batch 80 of 236

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

- "scanner_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "scanner_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L284 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "scanner_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "scanner_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L139 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…, RMCP Ping (ASF Presence Ping) to detect…]
- "scanner_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…, mDNS PTR query for _services._dns-sd._u…]
- "scanner_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "scanner_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…, UPnP/SSDP M-SEARCH — unicast to target:…]
- "scanner_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "scanner_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "scans_page_jobcard": "JobCard()" | kind=code-symbol | source=manager/frontend/app/portal/scans/page.tsx:L136 | neighbors=[page.tsx, prettyType(), relTime()]
- "schemas_engagement_rationale_14": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L14 | neighbors=[EngagementStatus, FindingSeverity, validate_scope_entries()]
- "schemas_portal_clientfindingout": "ClientFindingOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L22 | neighbors=[portal.py, BaseModel, A finding as a CUSTOMER may see it. mod…]
- "schemas_portal_clientreportout": "ClientReportOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L80 | neighbors=[portal.py, ClientReportContent, BaseModel]
- "schemas_portal_clientsummaryout": "ClientSummaryOut" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L59 | neighbors=[portal.py, BaseModel, One call powering the dashboard header:…]
- "schemas_portal_scanrequestcreate": "ScanRequestCreate" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L100 | neighbors=[portal.py, A customer's rich scan request. The cus…, BaseModel]
- "scripts_startup_validator_appenvironmentvalidator": "AppEnvironmentValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L151 | neighbors=[startup_validator.py, .validate(), Validates APP_ENV and related productio…]
- "scripts_startup_validator_appenvironmentvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L154 | neighbors=[AppEnvironmentValidator, CheckResult, .add()]
- "scripts_startup_validator_configvalidator": "ConfigValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L72 | neighbors=[startup_validator.py, .validate(), Validates required env vars are present…]
- "scripts_startup_validator_configvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L93 | neighbors=[ConfigValidator, CheckResult, .add()]
- "scripts_startup_validator_cookievalidator": "CookieValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L214 | neighbors=[startup_validator.py, .validate(), Validates secure cookie configuration.]
- "scripts_startup_validator_cookievalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L217 | neighbors=[CookieValidator, CheckResult, .add()]
- "scripts_startup_validator_corsvalidator": "CorsValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L174 | neighbors=[startup_validator.py, .validate(), Validates CORS_ORIGINS is production-sa…]
- "scripts_startup_validator_corsvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L179 | neighbors=[CorsValidator, CheckResult, .add()]
- "scripts_startup_validator_databaseconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L313 | neighbors=[DatabaseConnectivityValidator, CheckResult, .add()]
- "scripts_startup_validator_databaseurlvalidator": "DatabaseURLValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L244 | neighbors=[startup_validator.py, .validate(), Validates DATABASE_URL format and safet…]
- "scripts_startup_validator_databaseurlvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L249 | neighbors=[DatabaseURLValidator, CheckResult, .add()]
- "scripts_startup_validator_detectionenginevalidator": "DetectionEngineValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L279 | neighbors=[startup_validator.py, .validate(), Validates the baked-in detection engine…]
- "scripts_startup_validator_detectionenginevalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L282 | neighbors=[DetectionEngineValidator, CheckResult, .add()]
- "scripts_startup_validator_redisconnectivityvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L357 | neighbors=[RedisConnectivityValidator, CheckResult, .add()]
- "scripts_startup_validator_secretsvalidator": "SecretsValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L120 | neighbors=[startup_validator.py, Validates secrets meet minimum strength…, .validate()]
- "scripts_startup_validator_secretsvalidator_validate": ".validate()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L125 | neighbors=[SecretsValidator, CheckResult, .add()]
- "scripts_startup_validator_validationreport_raise_if_errors": ".raise_if_errors()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L62 | neighbors=[run_all_validators(), ValidationReport, StartupValidationError]
- "services_agent_policy_classify_action": "classify_action()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L49 | neighbors=[agent_policy.py, evaluate_action(), Map an action name to its risk tier; un…]
- "services_agent_policy_decision": "Decision" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L74 | neighbors=[agent_policy.py, _deny(), evaluate_action()]
- "services_agent_policy_deny": "_deny()" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L82 | neighbors=[agent_policy.py, Decision, evaluate_action()]
- "services_audit": "audit.py" | kind=code-symbol | source=manager/backend/app/services/audit.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, record_audit(), audit.py — the append-only audit-log wr…]
- "services_job_attempt_service_claim_job_attempt": "claim_job_attempt()" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L24 | neighbors=[job_attempt_service.py, AttemptClaim, Atomically claim a pending job and crea…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-079.json

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
