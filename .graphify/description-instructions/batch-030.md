# Node Description Batch 31 of 119

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

- "lib_permissions_store_adduser": "addUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L60 | neighbors=[permissions-store.ts, read(), write(), route.ts]
- "lib_permissions_store_isemailallowed": "isEmailAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L48 | neighbors=[auth-middleware.ts, permissions-store.ts, read(), route.ts]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget()]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder.  Creates a ten…]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[Base, TimestampMixin, ReviewStatus, LLMOutput]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder.  Creates a ten…]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "pipeline_pipeline_assembleerror": "assembleError()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L478 | neighbors=[pipeline.go, assemble(), Reject(), Run()]
- "probe_go_main_localscan": "localScan()" | kind=code-symbol | source=probe-go/main.go:L86 | neighbors=[main.go, renderReport(), run(), main()]
- "probe_go_main_renderreport": "renderReport()" | kind=code-symbol | source=probe-go/main.go:L129 | neighbors=[main.go, localScan(), findServiceLabel(), protoOr()]
- "probe_pipeline_collector": "_Collector" | kind=code-symbol | source=probe/pipeline.py:L121 | neighbors=[pipeline.py, .__init__(), .write(), _run_active()]
- "probe_selftest_live_handler": "_Handler" | kind=code-symbol | source=probe/selftest_live.py:L46 | neighbors=[selftest_live.py, .do_GET(), .do_OPTIONS(), .log_message()]
- "probe_selftest_live_main": "main()" | kind=code-symbol | source=probe/selftest_live.py:L91 | neighbors=[selftest_live.py, check(), _fact(), _free_port()]
- "probe_showcase_run_main": "main()" | kind=code-symbol | source=probe/showcase_run.py:L100 | neighbors=[showcase_run.py, list_use_cases(), _print_summary(), _split()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[Engagement, Finding, ScanJob, activity.py]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L617 | neighbors=[agents.py, _agent_can_execute_job(), _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L138 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L92 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type()]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L262 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), _set_job()]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L192 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L226 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L154 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L182 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…, Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L422 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_findings_tenant_finding": "_tenant_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L25 | neighbors=[findings.py, get_finding(), patch_finding(), Fetch a finding scoped to the caller's …]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L526 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_discover_probealive": "probeAlive()" | kind=code-symbol | source=probe-go/scanner/discover.go:L50 | neighbors=[discover.go, DiscoverHosts(), intStr(), isRefused()]
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L36 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…]
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan(), Excluded networks -> masscan --exclude …]
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan(), A CIDR spec is in scope only if it is f…]
- "scanner_nmap_runnmapversion": "RunNmapVersion()" | kind=code-symbol | source=probe-go/scanner/nmap.go:L34 | neighbors=[nmap.go, joinInts(), NmapAvailable(), parseNmapXML()]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…, Open ONE recv-only UDP listener. Return…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-030.json

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
