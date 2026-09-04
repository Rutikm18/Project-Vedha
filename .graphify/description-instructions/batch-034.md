# Node Description Batch 35 of 330

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

- "agent_agent_classify_connection_error": "_classify_connection_error()" | kind=code-symbol | source=probe/agent/agent.py:L140 | neighbors=[agent.py, _enroll_device(), main(), _manager_reachable(), _obtain_identity(), Map a low-level connection exception to…] | lang=en
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L74 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…] | lang=en
- "agent_agent_load_or_create_signing_identity": "_load_or_create_signing_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1116 | neighbors=[agent.py, _obtain_identity(), Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…] | lang=en
- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=probe/agent/agent.py:L181 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()] | lang=en
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
- "agent_transport_transport_bootstrap": ".bootstrap()" | kind=code-symbol | source=probe/agent/transport.py:L361 | neighbors=[Register using a manager-side shared bo…, Transport, .save_state(), TransportError, Register using a manager-side shared bo…, Register using a manager-side shared bo…] | lang=en
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
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L369 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…, ssh_inventory's dpkg_packages/rpm_packa…] | lang=en
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L91 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()] | lang=en
- "detection_explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L1 | neighbors=[6bb51ab feat: add detection-explain end…, fail(), GET(), backend.ts, backend(), BackendError] | lang=en
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…, 2885afa Add comprehensive probe testing…] | lang=en

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
