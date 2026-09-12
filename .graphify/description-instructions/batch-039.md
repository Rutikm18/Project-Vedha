# Node Description Batch 40 of 380

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

- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py] | lang=en
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…] | lang=en
- "agent_local_run_main": "_main()" | kind=code-symbol | source=probe/agent/local_run.py:L158 | neighbors=[local_run.py, _parse_args(), _ports_from_env(), _scope_file(), summarize(), _usage_error()] | lang=en
- "agent_result_queue": "result_queue.py" | kind=code-symbol | source=probe/agent/result_queue.py:L1 | neighbors=[host_sealed_cipher(), NullCipher, QueueStats, Record, ResultQueue, result_queue.py — durable, crash-safe, …] | lang=en
- "agent_result_queue_resultqueue_files": "._files()" | kind=code-symbol | source=probe/agent/result_queue.py:L92 | neighbors=[ResultQueue, ._enforce_size_bounds(), ._find(), ._max_seq(), .pending(), .should_backpressure()] | lang=en
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()] | lang=en
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry(), Atomically write a result payload to th…] | lang=en
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save(), Attempt to upload a result with retries…] | lang=en
- "agent_transport_transport_heartbeat_ex": ".heartbeat_ex()" | kind=code-symbol | source=probe/agent/transport.py:L674 | neighbors=[Send a heartbeat and report WHY it fail…, Transport, .heartbeat(), .ensure_device_access(), Send a heartbeat and report WHY it fail…, Send a heartbeat and report WHY it fail…] | lang=en
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L290 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()] | lang=en
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "campaign_progress_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/campaign-progress/route.ts:L1 | neighbors=[fail(), GET(), backend.ts, backend(), BackendError, bearerFrom()] | lang=en
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()] | lang=en
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()] | lang=en
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()] | lang=en
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@06ccae8a753288921646a52aba9827a6568a38b2": "06ccae8 Phase 6: optional connect + uplink security (+9 tests)" | kind=Commit | source=git | neighbors=[connect.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 1727f4f feat(findings): MTTR + open-by-…, test_connect.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6136a6e73cb9ba1e98eb1c7ef7d557df91036364": "6136a6e feat(detection): stable group_key for fleet finding deduplication" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 10fce13 feat(probe): observe web auth s…, posture_rules.py, test_finding_grouping.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7dc9b08365a5a162037b343deaabb7c15e05080e": "7dc9b08 feat(detection): surface NEW findings in the run delta" | kind=Commit | source=git | neighbors=[1727f4f feat(findings): MTTR + open-by-…, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 09c6c0a feat(probe): per-host wall-cloc…, detection_runs.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@82fa20e105feebe53ad7d311fe28b491ea865d5a": "82fa20e Phase 5: manager-less self-scan of the host own IP (+6 tests)" | kind=Commit | source=git | neighbors=[self_scan.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 9e5f980 feat(findings): add assigned_to…, test_self_scan.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@93d36f9ef2eb622a9d859ce032ad6103a8b24239": "93d36f9 feat(scheduling): due-schedule selection and advancement" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, eec1b35 feat(scheduling): scan-schedule…, scheduler.py, test_scheduler.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ba06a446406d2afc1d2639e9ce3adce7fe4126bd": "ba06a44 Phase 10: release integrity + SBOM + 3-OS CI + hardening docs (+4 tests)" | kind=Commit | source=git | neighbors=[release.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 5bf1aab Wire independent admission gate…, test_release.py] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@dbe9b7816457b45e88259fa7eff4848df59bcb4e": "dbe9b78 Phase 1: typed-scope model (scope_model.py) + 18 tests" | kind=Commit | source=git | neighbors=[c1c3bcc feat(detection): flag end-of-li…, scope_model.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 6136a6e feat(detection): stable group_k…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f8a6940c6b185bd7c7ad0930be39a32451facde4": "f8a6940 Phase 4: durable encrypted result queue (+9 tests)" | kind=Commit | source=git | neighbors=[42b9cf2 Phase 3: exit-state protocol + …, result_queue.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 82fa20e Phase 5: manager-less self-scan…] | lang=pt
- "components_refreshbutton": "RefreshButton.tsx" | kind=code-symbol | source=manager/frontend/components/RefreshButton.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, PageShell.tsx, RefreshButton(), RefreshButtonProps, page.tsx] | lang=en
- "cve_correlator_correlate": "correlate()" | kind=code-symbol | source=probe/cve/correlator.py:L122 | neighbors=[correlator.py, _as_dict(), _backport_marker(), CVEFinding, risk_band(), risk_score()] | lang=en
- "detection_edr_edrqueryengine": "EDRQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L62 | neighbors=[edr.py, CrowdStrikeFalcon, .__init__(), .query_detections(), ._request(), MicrosoftDefender] | lang=en
- "detection_engine_ai_normalizer_ainormalizercache_get": ".get()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L152 | neighbors=[AINormalizerCache, ._key(), .propose_cpe(), extract_raw_text(), .propose_cpe(), propose_candidates()] | lang=en
- "detection_engine_bridge_apply_regression_reopen": "_apply_regression_reopen()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L296 | neighbors=[engine_bridge.py, create_findings_from_facts(), _persist_posture_findings(), A previously-remediated finding whose i…, A previously-remediated finding whose i…, A previously-remediated finding whose i…] | lang=en
- "detection_engine_bridge_find_remediated_match": "_find_remediated_match()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L319 | neighbors=[engine_bridge.py, create_findings_from_facts(), _persist_posture_findings(), A remediated finding with the same (eng…, A previously-remediated finding whose i…, A remediated finding with the same (eng…] | lang=en
- "detection_engine_bridge_rationale_112": "A previously-remediated finding whose issue reappeared this run: reopen     the" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L112 | neighbors=[_apply_regression_reopen(), create_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus] | lang=en
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L369 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…, ssh_inventory's dpkg_packages/rpm_packa…] | lang=en
- "detection_engine_posture_rules_evaluate_rule": "evaluate_rule()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L985 | neighbors=[posture_rules.py, detect_posture_traced(), _fact_indicates_no_service(), get_path(), TraceRow, Evaluate ONE rule against ONE fact and …] | lang=en
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L91 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()] | lang=en
- "detection_explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L1 | neighbors=[6bb51ab feat: add detection-explain end…, fail(), GET(), backend.ts, backend(), BackendError] | lang=en
- "detection_resolution_decide_resolution": "decide_resolution()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L81 | neighbors=[resolution.py, resolution_threshold(), ResolutionOutcome, evaluate_resolutions(), Pure heart of auto-resolution. Given wh…, Pure heart of auto-resolution. Given wh…] | lang=en
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…, 2885afa Add comprehensive probe testing…] | lang=en
- "detection_vantage_fusion": "vantage_fusion.py" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _collect(), fuse_exposure_results(), fused_service_exposure(), _is_external(), _verdict()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-039.json

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
