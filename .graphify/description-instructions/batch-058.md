# Node Description Batch 59 of 336

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

- "main_scripts_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L137 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "main_scripts_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L242 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "main_scripts_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L185 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L283 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L313 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L165 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni(), Attempt a handshake forcing one protoco…]
- "main_scripts_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L295 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe(), Acquire the concurrency gate (adaptive …, Acquire the concurrency gate (adaptive …]
- "main_scripts_unauth_access": "unauth_access.py" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_text(), classify_unauth_access(), is_rce_capable(), test_main_scripts_unauth.py]
- "main_scripts_va_campaign_progressreporter_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L174 | neighbors=[ProgressReporter, _monotonic(), _now(), ._flush(), StageState]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_base": "base.py" | kind=code-symbol | source=manager/backend/app/models/base.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Base, TimestampMixin, UUIDMixin, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 6bb51ab feat: add detection-explain end…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest, 298a9d4 trim frontend to 7 core pages; …]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 6be8259 feat(integrations): outbox deli…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, AgentCredential, ProbeEnrollmentRequest, ProbeEnrollmentToken]
- "models_scan_request": "scan_request.py" | kind=code-symbol | source=manager/backend/app/models/scan_request.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c7f226f chore: bundle pending working-t…, ScanRequest, scan_request.py — a customer-initiated,…]
- "path_route_proxy": "proxy()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L17 | neighbors=[route.ts, GET(), PATCH(), POST(), portalToken()]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, graphStore, GET(), 298a9d4 trim frontend to 7 core pages; …, graph-store.ts]
- "portscan_portscanner_attempt": "._attempt()" | kind=code-symbol | source=portscan.py:L145 | neighbors=[PortScanner, classify_os_error(), family_of(), ._record(), .scan_port()]
- "results_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, GET(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "routers_agent_advisor_rationale_1": "agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag" | kind=entity | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[agent_advisor.py, AgentDecisionEngine, AgentUnavailableError, AgentRecommendation, Engagement]
- "routers_agents_get_agent_job_history": "get_agent_job_history()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1258 | neighbors=[agents.py, Read-only per-probe job list — the prob…, Read-only per-probe job list — the prob…, Read-only per-probe job list — the prob…, Read-only per-probe job list — the prob…]
- "routers_agents_pending_job_count": "_pending_job_count()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1153 | neighbors=[agents.py, cancel_agent_job(), enqueue_agent_job(), How many jobs are queued (not yet claim…, How many jobs are queued (not yet claim…]
- "routers_attack_paths_build_analyzer": "_build_analyzer()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L175 | neighbors=[attack_paths.py, attack_graph(), blast_radius(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_list_chokepoints": "list_chokepoints()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L117 | neighbors=[attack_paths.py, _all_paths_to_critical(), _asset_labels(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_recompute_and_store": "_recompute_and_store()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L199 | neighbors=[attack_paths.py, list_attack_paths(), _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_customer_access_build_scan_job": "build_scan_job()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L121 | neighbors=[customer_access.py, approve_scan_request(), Pure: turn an approved request into a p…, Pure: turn an approved request into a p…, Pure: turn an approved request into a p…]
- "routers_customer_access_clientuserout": "ClientUserOut" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L62 | neighbors=[customer_access.py, BaseModel, get_client_user(), patch_client_user(), provision_client_user()]
- "routers_customer_access_provision_client_user": "provision_client_user()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L171 | neighbors=[customer_access.py, ClientUserOut, _existing_client_user(), generate_password(), _unique_portal_slug()]
- "routers_customer_access_slugify": "_slugify()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L100 | neighbors=[customer_access.py, A lowercase, hyphenated, DNS-label-safe…, _unique_portal_slug(), A lowercase, hyphenated, DNS-label-safe…, A lowercase, hyphenated, DNS-label-safe…]
- "routers_detection_runs_rationale_1": "detection_runs.py — temporal detection API (\"what changed since last time\").  GE" | kind=entity | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[detection_runs.py, DetectionRun, Engagement, FindingStatus, Finding]
- "routers_engagements_campaign_progress": "campaign_progress()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L766 | neighbors=[engagements.py, _job_phase(), _reconcile_status(), _result_summary(), One call powers the VA Campaigns page: …]
- "routers_engagements_get_engagement_scope": "get_engagement_scope()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L1259 | neighbors=[engagements.py, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…, Probe-facing: the probe calls this inde…]
- "routers_engagements_re_detect": "re_detect()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L150 | neighbors=[engagements.py, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …, Re-runs the detection pipeline against …]
- "routers_findings_rationale_29": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L29 | neighbors=[Engagement, FindingStatus, Finding, sla_summary(), PaginatedResponse]
- "routers_probe_enrollment_approve_request_simple": "approve_request_simple()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L567 | neighbors=[probe_enrollment.py, auto_enroll_cidrs(), _next_probe_name(), _provision_agent_for_site(), SimpleApproveInput]
- "routers_probe_enrollment_enroll_token_is_usable": "enroll_token_is_usable()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L68 | neighbors=[probe_enrollment.py, create_enrollment_request(), list_enroll_tokens(), A token can auto-approve only while liv…, A token can auto-approve only while liv…]
- "routers_probe_enrollment_generate_enroll_token": "generate_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L62 | neighbors=[probe_enrollment.py, create_enroll_token(), _secret_hash(), Return (raw_token, token_hash, token_pr…, Return (raw_token, token_hash, token_pr…]
- "routers_probe_enrollment_rate_limit": "_rate_limit()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L99 | neighbors=[probe_enrollment.py, activate_enrollment(), create_enrollment_request(), poll_enrollment(), refresh_device_token()]
- "routers_probe_enrollment_simpleapproveinput": "SimpleApproveInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L530 | neighbors=[probe_enrollment.py, approve_request_simple(), One-click "Approve Site": every field i…, BaseModel, ._validate_networks()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-058.json

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
