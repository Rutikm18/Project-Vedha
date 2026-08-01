# Node Description Batch 42 of 119

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

- "lib_nmap_parser_toarray": "toArray()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L34 | neighbors=[nmap-parser.ts, extractScripts(), parseNmapXml()]
- "lib_nuclei_parser_parsenucleiline": "parseNucleiLine()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L35 | neighbors=[tool-runners.ts, nuclei-parser.ts, parsers.test.ts]
- "lib_openvas_client_parseopenvashelperoutput": "parseOpenVASHelperOutput()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L69 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), scanner-adapters.test.ts]
- "lib_openvas_client_settask": "setTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L35 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), startOpenVASScan()]
- "lib_openvas_client_startopenvasscan": "startOpenVASScan()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L111 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), setTask()]
- "lib_permissions_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L20 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_isscopeallowed": "isScopeAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L109 | neighbors=[permissions-store.ts, getUser(), read()]
- "lib_permissions_store_removeuser": "removeUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L91 | neighbors=[permissions-store.ts, read(), write()]
- "lib_permissions_store_updatescopes": "updateScopes()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L100 | neighbors=[permissions-store.ts, read(), write()]
- "lib_scanner_request_validation_isrecord": "isRecord()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L34 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_isvalidhostname": "isValidHostname()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L38 | neighbors=[scanner-request-validation.ts, isValidScannerTarget(), validateHost()]
- "lib_scanner_request_validation_validatehost": "validateHost()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L90 | neighbors=[scanner-request-validation.ts, isValidHostname(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_validatesafestring": "validateSafeString()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L96 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_scanner_request_validation_validatescannertargets": "validateScannerTargets()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L66 | neighbors=[scanner-request-validation.ts, validateNetExecScanRequest(), validateOpenVASScanRequest()]
- "lib_security_context_publiccverecord": "publicCveRecord()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L18 | neighbors=[security-context.ts, SecurityContextError, resolveSecurityReference()]
- "lib_severity_sev_palette": "SEV_PALETTE" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L78 | neighbors=[page.tsx, severity.ts, page.tsx]
- "lib_target_parser_isvalidtarget": "isValidTarget()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L19 | neighbors=[target-parser.ts, validOctets(), parseTargets()]
- "lib_tenant_resolvetenantsubdomain": "resolveTenantSubdomain()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L45 | neighbors=[proxy.ts, tenant.ts, subdomainFromHost()]
- "lib_tenant_subdomainfromhost": "subdomainFromHost()" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L22 | neighbors=[tenant.ts, resolveTenantSubdomain(), rootDomain()]
- "lib_testssl_parser_mapseverity": "mapSeverity()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L14 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslJson()]
- "lib_whatweb_parser_parsewhatweboutput": "parseWhatWebOutput()" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L12 | neighbors=[tool-runners.ts, whatweb-parser.ts, scanner-adapters.test.ts]
- "login_route_setsessioncookies": "setSessionCookies()" | kind=code-symbol | source=manager/frontend/app/api/auth/login/route.ts:L12 | neighbors=[route.ts, POST(), PUT()]
- "models_agent_recommendation_rationale_1": "agent_recommendation.py — decisions/actions proposed by the agentic AI advisor." | kind=entity | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[agent_recommendation.py, Base, TimestampMixin]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackPath, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline": "attack_timeline.py" | kind=code-symbol | source=manager/backend/app/models/attack_timeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackTimeline, 298a9d4 trim frontend to 7 core pages; …]
- "models_attack_timeline_rationale_12": "Append-only ledger of every attack action performed during an engagement.      W" | kind=entity | source=manager/backend/app/models/attack_timeline.py:L12 | neighbors=[AttackTimeline, Base, TimestampMixin]
- "models_audit_log": "audit_log.py" | kind=code-symbol | source=manager/backend/app/models/audit_log.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AuditLog, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection": "detection.py" | kind=code-symbol | source=manager/backend/app/models/detection.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config": "detection_config.py" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DetectionConfig, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_config_rationale_11": "Per-engagement SIEM + EDR connection settings used by the detection     validati" | kind=entity | source=manager/backend/app/models/detection_config.py:L11 | neighbors=[Base, TimestampMixin, DetectionConfig]
- "models_detection_run_rationale_1": "detection_run.py — one execution of the deterministic detection engine over a fa" | kind=entity | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[Base, TimestampMixin, detection_run.py]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Engagement, 298a9d4 trim frontend to 7 core pages; …]
- "models_exploit_approval_rationale_20": "Created when a high-risk target requires manager sign-off.     Auto-queues the e" | kind=entity | source=manager/backend/app/models/exploit_approval.py:L20 | neighbors=[Base, TimestampMixin, ExploitApprovalRequest]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_exploit_result_rationale_12": "Immutable record of every exploit attempt.     Never updated after creation — ap" | kind=entity | source=manager/backend/app/models/exploit_result.py:L12 | neighbors=[Base, TimestampMixin, ExploitResult]
- "models_llm_output": "llm_output.py" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, LLMOutput, 298a9d4 trim frontend to 7 core pages; …]
- "models_outbox_rationale_1": "outbox.py — transactional outbox for durable, exactly-once background work.  THE" | kind=entity | source=manager/backend/app/models/outbox.py:L1 | neighbors=[Base, TimestampMixin, outbox.py]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ScanResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_scan_result_rationale_11": "Append-only raw probe facts (P3-#10).      Decoupled from scan_jobs so:       (a" | kind=entity | source=manager/backend/app/models/scan_result.py:L11 | neighbors=[Base, TimestampMixin, ScanResult]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
