# Node Description Batch 35 of 131

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

- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L153 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L181 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L179 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…, Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L226 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…, Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L161 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …, Read an UploadFile in chunks, aborting …]
- "routers_exploits_result_out": "_result_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L421 | neighbors=[exploits.py, get_exploit_result(), list_exploit_results(), ExploitResultOut]
- "routers_findings_sla_summary": "sla_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L43 | neighbors=[findings.py, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…, Compute SLA state across the tenant's t…]
- "routers_probe_enrollment_authenticated_request": "_authenticated_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L401 | neighbors=[probe_enrollment.py, activate_enrollment(), _secret_hash(), poll_enrollment()]
- "routers_probe_enrollment_decode_public_key": "_decode_public_key()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L77 | neighbors=[probe_enrollment.py, create_enrollment_request(), .validate_key(), _verify_signature()]
- "routers_probe_enrollment_enroll_token_is_usable": "enroll_token_is_usable()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L67 | neighbors=[probe_enrollment.py, create_enrollment_request(), list_enroll_tokens(), A token can auto-approve only while liv…]
- "routers_probe_enrollment_generate_enroll_token": "generate_enroll_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L61 | neighbors=[probe_enrollment.py, create_enroll_token(), _secret_hash(), Return (raw_token, token_hash, token_pr…]
- "routers_probe_enrollment_provision_agent_for_site": "_provision_agent_for_site()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L234 | neighbors=[probe_enrollment.py, approve_enrollment(), create_enrollment_request(), Bind a request to a Site policy and cre…]
- "routers_probe_enrollment_refresh_device_token": "refresh_device_token()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L564 | neighbors=[probe_enrollment.py, _rate_limit(), _secret_hash(), _verify_signature()]
- "routers_probe_enrollment_sitepolicyinput": "SitePolicyInput" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L147 | neighbors=[probe_enrollment.py, BaseModel, .require_site_reference(), .validate_networks()]
- "routers_probe_enrollment_verify_signature": "_verify_signature()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L87 | neighbors=[probe_enrollment.py, activate_enrollment(), refresh_device_token(), _decode_public_key()]
- "routers_vuln_scans_finish_failed_nuclei_job": "_finish_failed_nuclei_job()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L525 | neighbors=[vuln_scans.py, _finish_cancelled_nuclei_job(), _set_nuclei_job_state(), _run_nuclei_and_save()]
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L36 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…, Return 'open', 'refused', or None (no r…]
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan(), Excluded networks -> masscan --exclude …]
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan(), A CIDR spec is in scope only if it is f…]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…, Open ONE recv-only UDP listener. Return…]
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …, Pull short printable ASCII runs from a …]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L389 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L43 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .to_json()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L64 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L157 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L127 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L133 | neighbors=[tls_scanner.py, _get_cert_der(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L56 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L65 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "schemas_asset_assetout": "AssetOut" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L34 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_asset_bulkassetimportresult": "BulkAssetImportResult" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L54 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_engagement_engagementdetail": "EngagementDetail" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L108 | neighbors=[engagement.py, EngagementOut, EngagementStatus, FindingSeverity]
- "schemas_engagement_engagementfilter": "EngagementFilter" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L71 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L81 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_validate_scope_entries": "validate_scope_entries()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L12 | neighbors=[engagement.py, .validate_scopes(), Validate and de-duplicate exact IP/CIDR…, Validate and de-duplicate exact IP/CIDR…]
- "schemas_finding_rationale_21": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[FindingPatch, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_detect_drift": "_detect_drift()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L150 | neighbors=[seed_admin.py, log_warn(), Warn if the tenant has multiple admins …, _seed_once()]
- "scripts_seed_admin_log": "_log()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L71 | neighbors=[seed_admin.py, log_error(), log_info(), log_warn()]
- "scripts_seed_admin_log_error": "log_error()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L89 | neighbors=[seed_admin.py, _log(), main(), _seed_with_retry()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-034.json

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
