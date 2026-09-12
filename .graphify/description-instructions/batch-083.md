# Node Description Batch 84 of 380

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

- "main_scripts_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…, Read the Allow header from an OPTIONS r…]
- "main_scripts_web_scanner_webscanner_schemes_for": "._schemes_for()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L212 | neighbors=[Preferred scheme first, the other as a …, WebScanner, ._scan_port(), Preferred scheme first, the other as a …]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Engagement, 298a9d4 trim frontend to 7 core pages; …]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder — production-gr…]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[LLMOutput, Base, TimestampMixin, ReviewStatus]
- "models_probe_enrollment_probeenrollmenttoken": "ProbeEnrollmentToken" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L72 | neighbors=[probe_enrollment.py, Base, TimestampMixin, Pre-authorized, Site-bound enrollment t…]
- "models_scan_job_attempt_scanjobattempt": "ScanJobAttempt" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L11 | neighbors=[scan_job_attempt.py, One immutable, fenced execution claim f…, Base, TimestampMixin]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_scan_schedule_scanschedule": "ScanSchedule" | kind=code-symbol | source=manager/backend/app/models/scan_schedule.py:L11 | neighbors=[scan_schedule.py, A recurring scan.      Vedha could only…, Base, TimestampMixin]
- "models_service": "service.py" | kind=code-symbol | source=manager/backend/app/models/service.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Service, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant": "tenant.py" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, d1b4dd3 trim frontend to 7 core pages; …, Tenant, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder — production-gr…]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "portscan_main": "main()" | kind=code-symbol | source=portscan.py:L216 | neighbors=[portscan.py, parse_ports(), PortScanner, .run()]
- "portscan_portscanner_scan_port": ".scan_port()" | kind=code-symbol | source=portscan.py:L180 | neighbors=[PortScanner, .run(), ._attempt(), .wait()]
- "portscan_ratelimiter": "RateLimiter" | kind=code-symbol | source=portscan.py:L95 | neighbors=[portscan.py, .__init__(), .__init__(), .wait()]
- "report_adapt_toreportassets": "toReportAssets()" | kind=code-symbol | source=manager/frontend/lib/report/adapt.ts:L39 | neighbors=[adapt.ts, toRawFinding(), deriveInternetReachable(), report-adapt.test.ts]
- "report_finding_model_confidenceof": "confidenceOf()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L198 | neighbors=[finding-model.ts, assess(), spec.ts, report-finding-model.test.ts]
- "report_finding_model_slaof": "slaOf()" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L455 | neighbors=[finding-model.ts, assess(), spec.ts, report-finding-model.test.ts]
- "reports_page_findingcard": "FindingCard()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L242 | neighbors=[page.tsx, cvssColor(), fmtDate(), parseCvss()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[activity.py, Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_token_from_websocket": "_agent_token_from_websocket()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L40 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Read an agent bearer token exclusively …, Read an agent bearer token exclusively …]
- "routers_agent_ws_claim_pushed_job": "_claim_pushed_job()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L46 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Validate eligibility and atomically cla…, Validate eligibility and atomically cla…]
- "routers_agents_pinned_agent_is_live": "_pinned_agent_is_live()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1193 | neighbors=[agents.py, get_agent_jobs(), Can the probe a job is pinned to still …, Can the probe a job is pinned to still …]
- "routers_ai_report_run_regeneration": "_run_regeneration()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L381 | neighbors=[ai_report.py, Background task: regenerate rejected se…, _build_engagement_summary(), Background task: regenerate rejected se…]
- "routers_analytics_finding_views": "_finding_views()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L86 | neighbors=[analytics.py, _sev_str(), posture(), Map joined (Finding, Asset.criticality)…]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L191 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L225 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L153 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L181 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_customer_access_existing_client_user": "_existing_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L157 | neighbors=[customer_access.py, get_client_user(), patch_client_user(), provision_client_user()]
- "routers_customer_access_patch_client_user": "patch_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L242 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password()]
- "routers_customer_access_reveal_customer_password": "reveal_customer_password()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L425 | neighbors=[customer_access.py, Decrypt and return a customer login's s…, RevealOut, Decrypt and return a customer login's s…]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L421 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_findings_finding_detail_out": "_finding_detail_out()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L53 | neighbors=[findings.py, get_finding(), Build the detail contract with bounded …, Build the detail contract with bounded …]
- "routers_findings_finding_timeline": "finding_timeline()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L345 | neighbors=[findings.py, _tenant_finding(), The finding's full lifecycle, oldest-fi…, The finding's full lifecycle, oldest-fi…]
- "routers_integrations_out": "_out()" | kind=code-symbol | source=manager/backend/app/routers/integrations.py:L43 | neighbors=[integrations.py, list_integrations(), IntegrationOut, put_integration()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-083.json

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
