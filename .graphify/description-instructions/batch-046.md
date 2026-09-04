# Node Description Batch 47 of 332

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

- "main_scripts_vnc_scanner_vncscanner": "VNCScanner" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L101 | neighbors=[vnc_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_vnc_scanner_vncscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L108 | neighbors=[Blocking: RFB version handshake + read …, VNCScanner, classify_security_types(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "main_scripts_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), ._schemes_for()]
- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "reveal_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/[id]/reveal/route.ts:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
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
- "scanner_delta_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L319 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "scanner_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/scanner/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "scanner_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=probe/scanner/findings.py:L1129 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "scanner_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=probe/scanner/findings.py:L1112 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "scanner_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=probe/scanner/findings.py:L1089 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "scanner_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=probe/scanner/findings.py:L707 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner(), DNS server hygiene: a full AXFR zone tr…]
- "scanner_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=probe/scanner/findings.py:L794 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner(), Confirmed FTP anonymous access (upgrade…]
- "scanner_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=probe/scanner/findings.py:L892 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner(), IPMI/BMC exposure. Cipher-zero is a cri…]
- "scanner_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=probe/scanner/findings.py:L669 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner(), Anonymous LDAP exposure. An anonymous R…]
- "scanner_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=probe/scanner/findings.py:L958 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner(), Windows RPC endpoint-mapper disclosure …]
- "scanner_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=probe/scanner/findings.py:L757 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner(), NFS anonymous export exposure. A world-…]
- "scanner_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=probe/scanner/findings.py:L985 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner(), Exposed network printer — an informatio…]
- "scanner_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/scanner/findings.py:L535 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner(), Confirmed RDP (X.224 handshake) + NLA d…]
- "scanner_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=probe/scanner/findings.py:L823 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner(), rsync daemon exposure. Anonymously-sele…]
- "scanner_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=probe/scanner/findings.py:L618 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner(), Anonymous SMB (null-session) informatio…]

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
