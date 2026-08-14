# Node Description Batch 46 of 186

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

- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[LLMOutput, Base, TimestampMixin, ReviewStatus]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_probe_enrollment_probeenrollmenttoken": "ProbeEnrollmentToken" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L72 | neighbors=[probe_enrollment.py, Base, TimestampMixin, Pre-authorized, Site-bound enrollment t…]
- "models_scan_job_attempt_scanjobattempt": "ScanJobAttempt" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L11 | neighbors=[scan_job_attempt.py, One immutable, fenced execution claim f…, Base, TimestampMixin]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant": "tenant.py" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, d1b4dd3 trim frontend to 7 core pages; …, Tenant, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder — production-gr…]
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, d1b4dd3 trim frontend to 7 core pages; …, User, 298a9d4 trim frontend to 7 core pages; …]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "portscan_main": "main()" | kind=code-symbol | source=portscan.py:L216 | neighbors=[portscan.py, parse_ports(), PortScanner, .run()]
- "portscan_portscanner_scan_port": ".scan_port()" | kind=code-symbol | source=portscan.py:L180 | neighbors=[PortScanner, .run(), ._attempt(), .wait()]
- "portscan_ratelimiter": "RateLimiter" | kind=code-symbol | source=portscan.py:L95 | neighbors=[portscan.py, .__init__(), .__init__(), .wait()]
- "probe_pipeline_collector": "_Collector" | kind=code-symbol | source=probe/pipeline.py:L121 | neighbors=[pipeline.py, .__init__(), .write(), _run_active()]
- "probe_push_results": "push_results.py" | kind=code-symbol | source=probe/push_results.py:L1 | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, die(), load_facts(), main()]
- "probe_selftest_live_handler": "_Handler" | kind=code-symbol | source=probe/selftest_live.py:L46 | neighbors=[selftest_live.py, .do_GET(), .do_OPTIONS(), .log_message()]
- "probe_selftest_live_main": "main()" | kind=code-symbol | source=probe/selftest_live.py:L91 | neighbors=[selftest_live.py, check(), _fact(), _free_port()]
- "probe_showcase_run_main": "main()" | kind=code-symbol | source=probe/showcase_run.py:L100 | neighbors=[showcase_run.py, list_use_cases(), _print_summary(), _split()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[activity.py, Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_token_from_websocket": "_agent_token_from_websocket()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L40 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Read an agent bearer token exclusively …, Read an agent bearer token exclusively …]
- "routers_agent_ws_claim_pushed_job": "_claim_pushed_job()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L46 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Validate eligibility and atomically cla…, Validate eligibility and atomically cla…]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L893 | neighbors=[agents.py, _agent_can_execute_job(), _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_agents_normalize_intensity_name": "_normalize_intensity_name()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L318 | neighbors=[agents.py, enqueue_agent_job(), ._validate_intensity(), Accept an intensity as a number (1/2/3)…]
- "routers_ai_report_run_regeneration": "_run_regeneration()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L381 | neighbors=[ai_report.py, Background task: regenerate rejected se…, _build_engagement_summary(), Background task: regenerate rejected se…]
- "routers_analytics_finding_views": "_finding_views()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L86 | neighbors=[analytics.py, _sev_str(), posture(), Map joined (Finding, Asset.criticality)…]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L191 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L225 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L153 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L181 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…, Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L421 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_findings_reopen_finding": "reopen_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L243 | neighbors=[findings.py, Operator reverses a resolution (auto or…, _tenant_finding(), Operator reverses a resolution (auto or…]
- "routers_findings_sla_summary": "sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L44 | neighbors=[findings.py, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…]
- "routers_probe_enrollment_authenticated_request": "_authenticated_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L401 | neighbors=[probe_enrollment.py, activate_enrollment(), _secret_hash(), poll_enrollment()]
- "routers_probe_enrollment_decode_public_key": "_decode_public_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L77 | neighbors=[probe_enrollment.py, create_enrollment_request(), .validate_key(), _verify_signature()]
- "routers_probe_enrollment_enroll_token_is_usable": "enroll_token_is_usable()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L67 | neighbors=[probe_enrollment.py, create_enrollment_request(), list_enroll_tokens(), A token can auto-approve only while liv…]
- "routers_probe_enrollment_generate_enroll_token": "generate_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L61 | neighbors=[probe_enrollment.py, create_enroll_token(), _secret_hash(), Return (raw_token, token_hash, token_pr…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-045.json

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
