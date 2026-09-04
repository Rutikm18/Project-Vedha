# Node Description Batch 35 of 332

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L367 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…] | lang=en
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L98 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), gate_4b_os_fingerprint(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…] | lang=en
- "workflow_host_health_hosthealthmonitor_state": "._state()" | kind=code-symbol | source=probe/workflow/host_health.py:L129 | neighbors=[HostHealthMonitor, .confirm(), .is_offline(), ._mark_offline(), .note_skipped(), .observe()] | lang=en
- "workflow_workflow_engine_run_branch": "_run_branch()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L292 | neighbors=[workflow_engine.py, Run ONE deep-scan branch for one host: …, _record(), _record_reused(), _scan_one(), _split_cached()] | lang=en
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity] | lang=en
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…] | lang=en
- "agent_agent_poll_jobs_or_empty": "_poll_jobs_or_empty()" | kind=code-symbol | source=probe/agent/agent.py:L278 | neighbors=[agent.py, main(), Poll for work. Auth failures (Transport…, Poll for work. Auth failures (Transport…, Poll for work. Auth failures (Transport…, say()] | lang=en
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L497 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()] | lang=en
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L105 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()] | lang=en
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L73 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…, Single factory for error result dicts —…] | lang=en
- "agent_engine_hosts_from_facts": "_hosts_from_facts()" | kind=code-symbol | source=probe/agent/engine.py:L318 | neighbors=[engine.py, _build_run_stats(), Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…] | lang=en
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py] | lang=en
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…] | lang=en
- "agent_local_run_main": "_main()" | kind=code-symbol | source=probe/agent/local_run.py:L158 | neighbors=[local_run.py, _parse_args(), _ports_from_env(), _scope_file(), summarize(), _usage_error()] | lang=en
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()] | lang=en
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry(), Atomically write a result payload to th…] | lang=en
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save(), Attempt to upload a result with retries…] | lang=en
- "agent_transport_transport_refresh_device_access": ".refresh_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L482 | neighbors=[Backwards-compatible bool wrapper over …, Transport, .ensure_device_access(), .refresh_device_access_ex(), Backwards-compatible bool wrapper over …, .load_state()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L286 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L245 | neighbors=[LLMReportGenerator, ._complete(), _normalize_ai_plan(), _parse_json_response(), _remediation_plan_prompt(), Generate a STRUCTURED, OS-specific reme…] | lang=en
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "campaign_progress_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/campaign-progress/route.ts:L1 | neighbors=[fail(), GET(), backend.ts, backend(), BackendError, bearerFrom()] | lang=en
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()] | lang=en
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()] | lang=en
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()] | lang=en
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0236a6011fa2a49e65e7f5cad6b04f643f83c6f7": "0236a60 fix(detection): full EPSS catalog so exploit-probability isn't blind" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, d98f654 feat(manager): network-VA campa…, update_snapshot.py] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b41065b13542a7c39f04677314b02d8698bce31": "6b41065 probe fixed" | kind=Commit | source=git | neighbors=[agent.py, transport.py, main, PostureScorecard.tsx, page.tsx, page.tsx] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd853230be2d89a28a641677bd8900d3071b1186": "bd85323 feat(probe): self-heal re-enroll, local-run driver, WS send resilience" | kind=Commit | source=git | neighbors=[agent.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, bf61dbc docs: probe run/test guide; git…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@dbcff7fc782d1da19c2bf749b8ac45146179b864": "dbcff7f feat: Update UseCaseCard component for improved description handling an…" | kind=Commit | source=git | neighbors=[b393dbe feat: Enhance Sidebar UI and in…, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, d0d1931 feat(detection): NVD/CPE vuln f…] | lang=en
- "components_refreshbutton": "RefreshButton.tsx" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, PageShell.tsx, RefreshButton(), RefreshButtonProps, page.tsx] | lang=en
- "cve_correlator_correlate": "correlate()" | kind=code-symbol | source=probe/cve/correlator.py:L122 | neighbors=[correlator.py, _as_dict(), _backport_marker(), CVEFinding, risk_band(), risk_score()] | lang=en
- "detection_edr_edrqueryengine": "EDRQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L62 | neighbors=[edr.py, CrowdStrikeFalcon, .__init__(), .query_detections(), ._request(), MicrosoftDefender] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_get": ".get()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L152 | neighbors=[AINormalizerCache, ._key(), .propose_cpe(), extract_raw_text(), .propose_cpe(), propose_candidates()] | lang=en
- "detection_engine_bridge_persist_posture_findings": "_persist_posture_findings()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L321 | neighbors=[engine_bridge.py, create_findings_from_facts(), _apply_regression_reopen(), _find_remediated_match(), _posture_description(), _posture_title()] | lang=en
- "detection_engine_bridge_rationale_112": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L112 | neighbors=[_apply_regression_reopen(), create_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus] | lang=en
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L677 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts(), Background entry point (P1: keep detect…, Background entry point (P1: keep detect…, Background entry point (P1: keep detect…] | lang=en
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L55 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable(), (content_hash, fetched_at) of the pinne…, (content_hash, fetched_at) of the pinne…] | lang=en

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
