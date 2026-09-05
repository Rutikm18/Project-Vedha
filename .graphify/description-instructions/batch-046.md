# Node Description Batch 47 of 336

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

- "main_scripts_ssh_scanner_parse_kexinit": "parse_kexinit()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L106 | neighbors=[ssh_scanner.py, _Cursor, .read(), .read_name_list(), Parse a SSH_MSG_KEXINIT body into its n…, ._scan_port()]
- "main_scripts_ssh_scanner_sshscanner": "SSHScanner" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L242 | neighbors=[ssh_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_ssh_scanner_sshscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L279 | neighbors=[SSHScanner, _dedup(), evaluate_algorithms(), parse_kexinit(), parse_ssh_banner(), .scan_target()]
- "main_scripts_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L91 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…]
- "main_scripts_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L115 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …]
- "main_scripts_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L213 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking(), SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…]
- "main_scripts_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L295 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking(), A genuine reply to our SYN acknowledges…, Outbound-interface IP for reaching dst_…, Outbound-interface IP for reaching dst_…]
- "main_scripts_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L176 | neighbors=[syn_scanner.py, parse_tcp_options(), Back-compat shim: MSS only. New code us…, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]
- "main_scripts_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L273 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__(), True only when a real SYN scan can work…, True only when a real SYN scan can work…, True only when a real SYN scan can work…]
- "main_scripts_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L274 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "main_scripts_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L282 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "main_scripts_va_campaign_vacampaign": "VACampaign" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L290 | neighbors=[va_campaign.py, build_campaign(), Runs the ordered stages sequentially, e…, .__init__(), ._refresh_totals(), .run()]
- "main_scripts_va_campaign_vacampaign_run": ".run()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L301 | neighbors=[run_campaign(), VACampaign, .finish(), .mark(), .snapshot(), ._refresh_totals()]
- "main_scripts_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …, test_main_scripts_vantage.py]
- "main_scripts_vnc_scanner_vncscanner": "VNCScanner" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L101 | neighbors=[vnc_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_vnc_scanner_vncscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L108 | neighbors=[Blocking: RFB version handshake + read …, VNCScanner, classify_security_types(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "main_scripts_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), ._schemes_for()]
- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "reveal_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/[id]/reveal/route.ts:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_ineligibility_reason": "_ineligibility_reason()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L178 | neighbors=[agents.py, enqueue_agent_job(), _job_reachability_scope(), _required_scan_type(), _scope_is_reachable(), Explain, in one line, WHY a probe can't…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L292 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), build_posture_report_section(), _set_job(), Background task: build the summary, gen…]
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[analytics.py, Asset, Engagement, FindingStatus, Finding, Service]
- "routers_customer_access_generate_password": "generate_password()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L95 | neighbors=[customer_access.py, patch_client_user(), provision_client_user(), A URL-safe temporary password the opera…, A URL-safe temporary password the opera…, A URL-safe temporary password the opera…]
- "routers_customer_access_list_customers": "list_customers()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L394 | neighbors=[customer_access.py, CustomerListItem, Every provisioned customer login (role=…, Every provisioned customer login (role=…, Every provisioned customer login (role=…, Every provisioned customer login (role=…]
- "routers_customer_access_unique_portal_slug": "_unique_portal_slug()" | kind=code-symbol | source=manager/backend/app/routers/customer_access.py:L107 | neighbors=[customer_access.py, provision_client_user(), Per-tenant-unique portal slug: <base>, …, _slugify(), Per-tenant-unique portal slug: <base>, …, Per-tenant-unique portal slug: <base>, …]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L206 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L253 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…, Upsert assets (and their services) from…, Upsert assets (and their services) from…, Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L188 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …]
- "routers_findings_reopen_finding": "reopen_finding()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L357 | neighbors=[findings.py, Operator reverses a resolution (auto or…, _tenant_finding(), Operator reverses a resolution (auto or…, Operator reverses a resolution (auto or…, Operator reverses a resolution (auto or…]
- "routers_findings_sla_summary": "sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L83 | neighbors=[findings.py, Compute SLA state across the tenant's t…, Build the detail contract with bounded …, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…]
- "routers_portal_enum_val": "_enum_val()" | kind=code-symbol | source=manager/backend/app/routers/portal.py:L82 | neighbors=[portal.py, _metric_finding(), portal_engagement(), portal_scans(), _posture_view(), portal_posture()]
- "routers_probe_enrollment_provision_agent_for_site": "_provision_agent_for_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L235 | neighbors=[probe_enrollment.py, approve_enrollment(), approve_request_simple(), create_enrollment_request(), Bind a request to a Site policy and cre…, Bind a request to a Site policy and cre…]
- "routers_probe_enrollment_secret_hash": "_secret_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L37 | neighbors=[probe_enrollment.py, activate_enrollment(), _authenticated_request(), create_enrollment_request(), generate_enroll_token(), refresh_device_token()]
- "scanner_accuracy_gate_run_gate": "run_gate()" | kind=code-symbol | source=probe/scanner/accuracy_gate.py:L141 | neighbors=[accuracy_gate.py, _main(), Score every corpus in `directory` and c…, check_thresholds(), is_independent(), load_corpora()]
- "scanner_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=probe/scanner/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/scanner/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-046.json

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
