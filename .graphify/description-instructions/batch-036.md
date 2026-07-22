# Node Description Batch 37 of 76

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

- "discovery_rate_limiter_ratelimiter_consume_token": "._consume_token()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L85 | neighbors=[RateLimiter, .acquire()]
- "discovery_rate_limiter_ratelimiter_resolve_cidr": "._resolve_cidr()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L75 | neighbors=[RateLimiter, .acquire()]
- "discovery_service_id_serviceidentifier_identify": ".identify()" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L74 | neighbors=[ServiceIdentifier, ServiceFingerprint]
- "discovery_worker_discoveryworker_grab_one": "._grab_one()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L161 | neighbors=[DiscoveryWorker, ._banner_grab_all()]
- "discovery_worker_discoveryworker_run_nmap": "._run_nmap()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L119 | neighbors=[DiscoveryWorker, .run()]
- "discovery_worker_discoveryworker_save_assets": "._save_assets()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L194 | neighbors=[DiscoveryWorker, .run()]
- "discovery_worker_discoveryworker_set_status": "._set_status()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L270 | neighbors=[DiscoveryWorker, .run()]
- "discovery_xml_parser_nmapxmlparser_parse": ".parse()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L44 | neighbors=[NmapXMLParser, ._parse_host()]
- "e2e_interop_verify": "interop_verify.py" | kind=code-symbol | source=manager/frontend/tests/e2e/interop_verify.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Verify the Python probe can open what t…]
- "e2e_mock_manager_make_handler": "_make_handler()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L118 | neighbors=[mock_manager.py, start()]
- "e2e_mock_manager_managerstate_mgr_box_pub_b64": ".mgr_box_pub_b64()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L67 | neighbors=[ManagerState, b64e()]
- "e2e_mock_manager_managerstate_mgr_sig_pub_b64": ".mgr_sig_pub_b64()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L63 | neighbors=[ManagerState, b64e()]
- "e2e_mock_manager_managerstate_mint_scope_token": "._mint_scope_token()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L76 | neighbors=[ManagerState, .next_job_for()]
- "e2e_mock_manager_self_signed": "_self_signed()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L195 | neighbors=[mock_manager.py, start()]
- "e2e_run_probe_env": "probe_env()" | kind=code-symbol | source=manager/frontend/tests/e2e/run.py:L75 | neighbors=[run.py, main()]
- "e2e_run_run_probe": "run_probe()" | kind=code-symbol | source=manager/frontend/tests/e2e/run.py:L95 | neighbors=[run.py, main()]
- "e2e_run_scan_plan": "scan_plan()" | kind=code-symbol | source=manager/frontend/tests/e2e/run.py:L50 | neighbors=[run.py, main()]
- "engine_scan_modules_modules": "MODULES" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L48 | neighbors=[interactive.ts, scan-modules.ts]
- "engine_scan_modules_modulesbycategory": "modulesByCategory()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L333 | neighbors=[interactive.ts, scan-modules.ts]
- "engine_scan_modules_modulesforports": "modulesForPorts()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L378 | neighbors=[scan-modules.ts, scanner.ts]
- "engine_scan_modules_profilemodules": "profileModules()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L349 | neighbors=[interactive.ts, scan-modules.ts]
- "engine_scanner_byseveritycount": "bySeverityCount()" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L11 | neighbors=[scanner.ts, runScan()]
- "engine_tool_runners_httpbannergrab": "httpBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L311 | neighbors=[tool-runners.ts, nativeBannerGrab()]
- "engine_tool_runners_tcpbannergrab": "tcpBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L357 | neighbors=[tool-runners.ts, nativeBannerGrab()]
- "engine_types_evidence": "Evidence" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L77 | neighbors=[types.ts, findings-store.ts]
- "exploit_msf_client_metasploitrpcclient_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L53 | neighbors=[MetasploitRPCClient, ._call()]
- "exploit_msf_client_metasploitrpcclient_module_info": ".module_info()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L126 | neighbors=[MetasploitRPCClient, ._call()]
- "exploit_nuclei_exploit_nucleiexploitrunner_extract_evidence": "._extract_evidence()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L184 | neighbors=[NucleiExploitRunner, ._parse_poc_output()]
- "exploit_nuclei_exploit_nucleiexploitrunner_safe_template_check": ".safe_template_check()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L60 | neighbors=[NucleiExploitRunner, Parse template YAML and validate it con…]
- "exploit_nuclei_exploit_rationale_1": "NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[nuclei_exploit.py, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_121": "Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L121 | neighbors=[.run_cve_poc(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_161": "Parse nuclei JSONL output for a single CVE PoC result." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L161 | neighbors=[._parse_poc_output(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_49": "Run Nuclei CVE PoC templates against a single target.     Every template is safe" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L49 | neighbors=[NucleiExploitRunner, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_61": "Parse template YAML and validate it contains no write/delete/DoS actions." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L61 | neighbors=[.safe_template_check(), SafetyViolationError]
- "exploit_orchestrator_exploitorchestrator_audit": "._audit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L322 | neighbors=[ExploitOrchestrator, .execute()]
- "exploit_orchestrator_exploitorchestrator_generate_dns_callback_token": ".generate_dns_callback_token()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L255 | neighbors=[ExploitOrchestrator, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_requires_approval": "requires_approval()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L239 | neighbors=[safety.py, True if this target requires human mana…]
- "findings_page_findingspage": "FindingsPage()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L714 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_getslacolor": "getSlaColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L93 | neighbors=[page.tsx, FindingDetail()]
- "findings_page_riskbadge": "RiskBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L137 | neighbors=[page.tsx, riskScoreColor()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-036.json

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
