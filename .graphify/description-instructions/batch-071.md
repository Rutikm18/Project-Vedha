# Node Description Batch 72 of 209

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

- "scanner_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L124 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…]
- "scanner_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L411 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking()]
- "scanner_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L280 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "scanner_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "scanner_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L187 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe()]
- "scanner_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L218 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe()]
- "scanner_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L246 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe()]
- "scanner_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L203 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe()]
- "scanner_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L231 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe()]
- "scanner_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "scanner_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L289 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe()]
- "scanner_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "scanner_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L44 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…]
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
- "services_audit": "audit.py" | kind=code-symbol | source=manager/backend/app/services/audit.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, record_audit(), audit.py — the append-only audit-log wr…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-071.json

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
