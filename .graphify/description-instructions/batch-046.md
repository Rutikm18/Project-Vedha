# Node Description Batch 47 of 104

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

- "detection_engine_update_snapshot_all_known_cve_ids": "_all_known_cve_ids()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L174 | neighbors=[update_snapshot.py, main()]
- "detection_engine_verifier_deception_score": "deception_score()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L75 | neighbors=[verifier.py, A starter honeypot/deception heuristic …]
- "detection_engine_version_compare_split_segments": "_split_segments()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L78 | neighbors=[version_compare.py, _compare_part()]
- "detection_engine_vuln_db_default_products": "_default_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L43 | neighbors=[vuln_db.py, Derives the synced product list from cp…]
- "detection_engine_vuln_db_vulndb_build_cve_index": "._build_cve_index()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L89 | neighbors=[VulnDB, .__init__()]
- "detection_engine_vuln_db_vulndb_get_cvss_vector": ".get_cvss_vector()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L109 | neighbors=[The CVSS v3 vector string OSV embedded …, VulnDB]
- "detection_engine_vuln_db_vulndb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L83 | neighbors=[VulnDB, ._build_cve_index()]
- "detection_engine_vuln_db_vulndb_lookup": ".lookup()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L98 | neighbors=[Raw OSV vulnerability records for this …, VulnDB]
- "detection_logger_as_uuid": "_as_uuid()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L69 | neighbors=[logger.py, .log_action()]
- "detection_logger_rationale_1": "AttackLogger — records every attack action to the ``attack_timeline`` table.  Al" | kind=entity | source=manager/backend/app/detection/logger.py:L1 | neighbors=[logger.py, AttackTimeline]
- "detection_logger_rationale_40": "Persist a single attack action. Returns the AttackTimeline row.          ``times" | kind=entity | source=manager/backend/app/detection/logger.py:L40 | neighbors=[.log_action(), AttackTimeline]
- "detection_siem_elasticsiem_build_query": ".build_query()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L191 | neighbors=[ElasticSIEM, .query_alerts()]
- "detection_siem_sentinelsiem_build_kql": ".build_kql()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L141 | neighbors=[SentinelSIEM, .query_alerts()]
- "detection_siem_splunksiem_build_spl": ".build_spl()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L88 | neighbors=[SplunkSIEM, .query_alerts()]
- "detection_sigma_sigmarulegenerator_customise_detection": "._customise_detection()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L153 | neighbors=[SigmaRuleGenerator, .generate_sigma_for_technique()]
- "detection_sigma_sigmarulegenerator_lookup_template": "._lookup_template()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L144 | neighbors=[SigmaRuleGenerator, .generate_sigma_for_technique()]
- "detection_sigma_stable_rule_id": "_stable_rule_id()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L166 | neighbors=[sigma.py, .generate_sigma_for_technique()]
- "discovery_finding_translator_map_severity": "_map_severity()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L46 | neighbors=[finding_translator.py, create_findings_from_probe_result()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-046.json

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
