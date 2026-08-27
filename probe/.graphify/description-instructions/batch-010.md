# Node Description Batch 11 of 92

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

- "tools_issue_license": "issue_license.py" | kind=code-symbol | source=tools/issue_license.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, _b64(), issue(), keygen(), main()]
- "workflow_intensity": "intensity.py" | kind=code-symbol | source=workflow/intensity.py:L1 | neighbors=[engine.py, a548359 feat(auto-enrollment): implemen…, test_probe_next_features.py, port_scanner.py, intensity_port_override(), resolve_intensity()]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=agent/agent.py:L47 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()]
- "agent_agent_classify_connection_error": "_classify_connection_error()" | kind=code-symbol | source=agent/agent.py:L130 | neighbors=[agent.py, _enroll_device(), main(), _manager_reachable(), _obtain_identity(), Map a low-level connection exception to…]
- "agent_agent_dbg": "_dbg()" | kind=code-symbol | source=agent/agent.py:L87 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), _wait_for_manager(), _ws_run_job()]
- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=agent/agent.py:L171 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()]
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=agent/agent.py:L804 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), _flush_spool_over_http(), say(), _ws_run_job()]
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=agent/cli.py:L311 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()]
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=agent/cli.py:L444 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, ae7a30b feat: add Posture & Patch-Compa…, test_hw_bind.py]
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, ae7a30b feat: add Posture & Patch-Compa…, test_integration.py, test_result_spool.py, test_ws_claim_protocol.py]
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=agent/result_spool.py:L184 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists(), ._path(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_quarantine": ".quarantine()" | kind=code-symbol | source=agent/result_spool.py:L115 | neighbors=[Move a terminally rejected result out o…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=agent/result_spool.py:L110 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "commit:repo:local/probe@20f2a9dc@a1430fbbc09e90e0e23577cc94b5aca8b2dcfcd8": "a1430fb Add local_run.py for direct probe execution and verify_windows_ground_t…" | kind=Commit | source=git | neighbors=[56508b2 Add unit tests for XML parsing,…, agent.py, local_run.py, use_cases.py, main, probe_local_run.py]
- "main_scripts_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=main_scripts/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "main_scripts_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=main_scripts/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "main_scripts_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "main_scripts_delta_scanner_main": "main()" | kind=code-symbol | source=main_scripts/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "main_scripts_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=main_scripts/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "main_scripts_findings_rule_dns": "_rule_dns()" | kind=code-symbol | source=main_scripts/findings.py:L689 | neighbors=[findings.py, DNS server hygiene: a full AXFR zone tr…, _data(), Finding, _scanner(), DNS server hygiene: a full AXFR zone tr…]
- "main_scripts_findings_rule_ftp": "_rule_ftp()" | kind=code-symbol | source=main_scripts/findings.py:L776 | neighbors=[findings.py, Confirmed FTP anonymous access (upgrade…, _data(), Finding, _scanner(), Confirmed FTP anonymous access (upgrade…]
- "main_scripts_findings_rule_ipmi": "_rule_ipmi()" | kind=code-symbol | source=main_scripts/findings.py:L874 | neighbors=[findings.py, IPMI/BMC exposure. Cipher-zero is a cri…, _data(), Finding, _scanner(), IPMI/BMC exposure. Cipher-zero is a cri…]
- "main_scripts_findings_rule_ldap": "_rule_ldap()" | kind=code-symbol | source=main_scripts/findings.py:L651 | neighbors=[findings.py, Anonymous LDAP exposure. An anonymous R…, _data(), Finding, _scanner(), Anonymous LDAP exposure. An anonymous R…]
- "main_scripts_findings_rule_msrpc": "_rule_msrpc()" | kind=code-symbol | source=main_scripts/findings.py:L940 | neighbors=[findings.py, Windows RPC endpoint-mapper disclosure …, _data(), Finding, _scanner(), Windows RPC endpoint-mapper disclosure …]
- "main_scripts_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=main_scripts/findings.py:L739 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner(), NFS anonymous export exposure. A world-…]
- "main_scripts_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=main_scripts/findings.py:L967 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner(), Exposed network printer — an informatio…]
- "main_scripts_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=main_scripts/findings.py:L535 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner(), Confirmed RDP (X.224 handshake) + NLA d…]
- "main_scripts_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=main_scripts/findings.py:L805 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner(), rsync daemon exposure. Anonymously-sele…]
- "main_scripts_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=main_scripts/findings.py:L600 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner(), Anonymous SMB (null-session) informatio…]
- "main_scripts_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=main_scripts/findings.py:L906 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner(), SMTP hygiene: VRFY/EXPN user enumeratio…]
- "main_scripts_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=main_scripts/findings.py:L467 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner(), JA4X-based threat-intel match. Fires on…]
- "main_scripts_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=main_scripts/findings.py:L515 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner(), JA4S-based threat-intel match on the TL…]
- "main_scripts_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=main_scripts/findings.py:L489 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner(), Proven UNAUTHENTICATED access to a data…]
- "main_scripts_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=main_scripts/findings.py:L843 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner(), VNC/RFB authentication exposure. 'None'…]
- "main_scripts_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/host_discovery.py:L416 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), is_locally_administered(), vendor_for_mac()]
- "main_scripts_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=main_scripts/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "main_scripts_init_rationale_1": "VA scanner module — pure collection/scanning layer.  Each submodule is an indepe" | kind=entity | source=main_scripts/__init__.py:L1 | neighbors=[__init__.py, BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard]
- "main_scripts_mass_scan_rationale_1": "mass_scan.py — fast large-scale TCP port discovery.  WHY THIS EXISTS (modern con" | kind=entity | source=main_scripts/mass_scan.py:L1 | neighbors=[mass_scan.py, BaseScanner, RateLimiter, ResultWriter, ScanResult, ScopeGuard]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-010.json

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
