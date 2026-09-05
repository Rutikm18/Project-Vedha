# Node Description Batch 72 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "lib_adapters_toapifindingpatch": "toApiFindingPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L235 | neighbors=[route.ts, adapters.ts, engagement-adapters.test.ts, findings-adapters.test.ts]
- "lib_adapters_touiengagement": "toUiEngagement()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L35 | neighbors=[route.ts, route.ts, adapters.ts, engStatusToUi()]
- "lib_agents_store_registeragent": "registerAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L362 | neighbors=[agents-store.ts, genFieldAgentId(), readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_writefieldagents": "writeFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L350 | neighbors=[agents-store.ts, registerAgent(), updateAgentLastSeen(), ensureDataDir()]
- "lib_ai_engine_tomodelfindings": "toModelFindings()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L552 | neighbors=[ai-engine.ts, generateReportSectioned(), generateReportSingleCall(), generateReport()]
- "lib_ai_engine_toscorecardinput": "toScorecardInput()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L532 | neighbors=[ai-engine.ts, generateReportSectioned(), generateReportSingleCall(), generateReport()]
- "lib_assistant_access_canmountassistant": "canMountAssistant()" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L12 | neighbors=[AssistantProvider.tsx, assistant-access.ts, isAssistantRoute(), operator-routes.test.ts]
- "lib_assistant_access_isassistantroute": "isAssistantRoute()" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L2 | neighbors=[AssistantProvider.tsx, assistant-access.ts, canMountAssistant(), operator-routes.test.ts]
- "lib_campaign_store_issafecampaignid": "isSafeCampaignId()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L87 | neighbors=[campaign-store.ts, getCampaign(), validateSnapshot(), campaign-store.test.ts]
- "lib_clients_store_createclient": "createClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L87 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_clients_store_updateclient": "updateClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L105 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_console_source_consolequerykey": "consoleQueryKey()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L139 | neighbors=[page.tsx, page.tsx, console-source.tsx, useConsoleQueryKey()]
- "lib_console_source_useconsolequerykey": "useConsoleQueryKey()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L144 | neighbors=[DashboardGrid.tsx, console-source.tsx, consoleQueryKey(), useConsoleSource()]
- "lib_console_source_useconsolesource": "useConsoleSource()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L131 | neighbors=[console-source.tsx, useConsoleCapability(), useConsoleQuery(), useConsoleQueryKey()]
- "lib_errors_diagnosespawnerror": "diagnoseSpawnError()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L244 | neighbors=[tool-runners.ts, errors.ts, VedhaError, AdversaError]
- "lib_httpx_parser_httpxjsonldecoder_decode": ".decode()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L116 | neighbors=[HttpxJsonlDecoder, .push(), parseHttpxJsonLine(), .finish()]
- "lib_job_store_createjob": "createJob()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L41 | neighbors=[job-store.ts, genJobId(), readJobs(), writeJobs()]
- "lib_nuclei_parser_nucleiseveritytoseverity": "nucleiSeverityToSeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L71 | neighbors=[tool-runners.ts, nuclei-parser.ts, nucleiMatchToFinding(), parsers.test.ts]
- "lib_permissions_store_adduser": "addUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L60 | neighbors=[permissions-store.ts, read(), write(), route.ts]
- "lib_permissions_store_isemailallowed": "isEmailAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L48 | neighbors=[auth-middleware.ts, permissions-store.ts, read(), route.ts]
- "lib_portal_client_severity_var": "SEVERITY_VAR" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L117 | neighbors=[page.tsx, portal-client.ts, page.tsx, page.tsx]
- "lib_severity_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L24 | neighbors=[FactCard.tsx, page.tsx, severity.ts, page.tsx]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget()]
- "login_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L54 | neighbors=[route.ts, isClientToken(), setPortalCookies(), setSessionCookies()]
- "login_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L104 | neighbors=[route.ts, isClientToken(), setPortalCookies(), setSessionCookies()]
- "main_scripts_accuracy_gate_load_corpus": "load_corpus()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L65 | neighbors=[accuracy_gate.py, load_corpora(), CorpusError, Load and structurally validate one corp…]
- "main_scripts_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, AdaptiveTimeout, from_rtts(), test_main_scripts_adaptive_timeout.py]
- "main_scripts_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "main_scripts_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L123 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…, Best-effort service name from data dict…]
- "main_scripts_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L140 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string., Best-effort version string.]
- "main_scripts_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L298 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…, Heuristic priority for a newly-detected…]
- "main_scripts_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L55 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…, Normalised representation of one ScanRe…]
- "main_scripts_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L310 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…, True if version changed in a security-r…]
- "main_scripts_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L93 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…, Derive a stable host identity from a ra…]
- "main_scripts_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L110 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…, Fuse OS family + open ports + service p…]
- "main_scripts_dns_scanner_dnsscanner_ptr_self": "._ptr_self()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L119 | neighbors=[DNSScanner, ._probe(), _is_ip(), Ask the target (as a resolver) for the …]
- "main_scripts_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/main_scripts/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "main_scripts_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=probe/main_scripts/findings.py:L254 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L277 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_ssh": "_rule_ssh()" | kind=code-symbol | source=probe/main_scripts/findings.py:L582 | neighbors=[findings.py, _data(), Finding, _scanner()]

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
