# Node Description Batch 35 of 380

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

- "agent_engine_scan_method_for": "_scan_method_for()" | kind=code-symbol | source=probe/agent/engine.py:L178 | neighbors=[engine.py, _applied_tuning(), syn' for wide sweeps (deep intensity / …, run_scan(), syn' for wide sweeps (deep intensity / …, syn' for wide sweeps (deep intensity / …] | lang=en
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError] | lang=en
- "agent_release": "release.py" | kind=code-symbol | source=probe/agent/release.py:L1 | neighbors=[main(), parse_requirements(), sbom_from_requirements(), sha256_file(), sha256_manifest(), verify_manifest()] | lang=en
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=probe/agent/result_spool.py:L184 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists(), ._path(), .quarantine(), .remove()] | lang=en
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L110 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()] | lang=en
- "agent_service": "service.py" | kind=code-symbol | source=probe/agent/service.py:L1 | neighbors=[commands_for(), _default_runner(), install(), render_unit(), uninstall(), uninstall_commands()] | lang=en
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=probe/agent/transport.py:L274 | neighbors=[Transport, .activate_enrollment(), .ensure_device_access(), .__init__(), .refresh_device_access_ex(), .refresh_registration()] | lang=en
- "agent_transport_transport_refresh_device_access": ".refresh_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L518 | neighbors=[Backwards-compatible bool wrapper over …, Transport, .ensure_device_access(), .refresh_device_access_ex(), Backwards-compatible bool wrapper over …, Backwards-compatible bool wrapper over …] | lang=en
- "agent_transport_transport_refresh_device_access_ex": ".refresh_device_access_ex()" | kind=code-symbol | source=probe/agent/transport.py:L522 | neighbors=[Refresh the short-lived device access t…, Transport, .refresh_device_access(), manager_fingerprint(), .load_state(), .update_state()] | lang=en
- "ai_llm_report_llmreportgenerator_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L249 | neighbors=[LLMReportGenerator, ._complete(), _normalize_ai_plan(), _parse_json_response(), _remediation_plan_prompt(), Generate a STRUCTURED, OS-specific reme…] | lang=en
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings, AiRuntimeError] | lang=en
- "assistant_modelswitcher": "ModelSwitcher.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L1 | neighbors=[AssistantDrawer.tsx, AiStatus, ModelSelection, ModelSwitcher(), ProviderStatus, readStored()] | lang=en
- "auth_exceptions_vedhaautherror": "VedhaAuthError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L15 | neighbors=[exceptions.py, AuthenticationError, DatabaseUnavailableError, PasswordRotationError, Base for all Vedha auth exceptions., SeedConfigurationError] | lang=en
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()] | lang=en
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…] | lang=en
- "cli_auth_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L46 | neighbors=[auth.ts, serverUrl(), admin.ts, engagement.ts, interactive.ts, report.ts] | lang=en
- "cli_llm_client": "client()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L10 | neighbors=[llm.ts, commentOnStage(), explainFindings(), planExploit(), recommendNextPhase(), streamAsk()] | lang=en
- "commands_interactive_picktargets": "pickTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L226 | neighbors=[interactive.ts, ask(), choose(), confirm(), detectLocalSubnet(), inferHostsFromFindings()] | lang=en
- "commands_interactive_wizardengagement": "wizardEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1769 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), divider(), fetchEngagements()] | lang=en
- "commands_interactive_wizardreport": "wizardReport()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1847 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()] | lang=en
- "commands_interactive_wizardvalidate": "wizardValidate()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1465 | neighbors=[interactive.ts, mainMenu(), runValidationFlow(), ask(), choose(), confirm()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@06587d101bf5762f6eb93fff96b937d92b8369ad": "06587d1 Phase 8: observability + collect-diagnostics (+5 tests)" | kind=Commit | source=git | neighbors=[obs.py, setup.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 30d45bb Document the 8-phase hardened-a…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@09c6c0a257795d7d2df71e493da4c948c04148cf": "09c6c0a feat(probe): per-host wall-clock budget with honest partial results" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 42b7429 feat(probe): deep intensity get…, port_scanner.py, port_scanner.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@10fce13fa981f60e6b9ba3c16dc2133fbeca2879": "10fce13 feat(probe): observe web auth surface (facts-only, no credential attemp…" | kind=Commit | source=git | neighbors=[1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 831bdef feat(detection): default-creden…, web_scanner.py, web_scanner.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@1727f4faa9c0ff677bb3caf0a2f45f713e375a7b": "1727f4f feat(findings): MTTR + open-by-owner metrics endpoint" | kind=Commit | source=git | neighbors=[06ccae8 Phase 6: optional connect + upl…, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 7dc9b08 feat(detection): surface NEW fi…, findings.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@5bf1aab894efaff6b199a420e9a77ae89bd60b4c": "5bf1aab Wire independent admission gate into the live daemon (+5 tests)" | kind=Commit | source=git | neighbors=[job_admission.py, task_runner.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 79ea84a Finish pending gaps: real clock…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@831bdef00ce8072f80dd26f15a3a0026b5de4b8d": "831bdef feat(detection): default-credential candidates for IoT, cameras and pri…" | kind=Commit | source=git | neighbors=[10fce13 feat(probe): observe web auth s…, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 08d8fe1 Phase 2: config precedence load…, default_creds_catalog.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9e5f98047549f35db0bbefc8cb20b15c4d89c6c0": "9e5f980 feat(findings): add assigned_to for remediation ownership" | kind=Commit | source=git | neighbors=[82fa20e Phase 5: manager-less self-scan…, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, 06ccae8 Phase 6: optional connect + upl…, finding.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c1c3bcc8d43dfc15e06ec356e30ba59901bb8371": "c1c3bcc feat(detection): flag end-of-life operating systems" | kind=Commit | source=git | neighbors=[8402f01 Phase 0: STRIDE threat model + …, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, dbe9b78 Phase 1: typed-scope model (sco…, eol_catalog.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de0005eeb092b959e491cb0a627112c1f82589fc": "de0005e Phase 9: per-OS service install/uninstall with restart limits (+6 tests)" | kind=Commit | source=git | neighbors=[30d45bb Document the 8-phase hardened-a…, service.py, setup.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@eec1b35742643281f4ce937087ef8f62548b22f5": "eec1b35 feat(scheduling): scan-schedule CRUD endpoints" | kind=Commit | source=git | neighbors=[93d36f9 feat(scheduling): due-schedule …, main.py, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, ac8d1ee Phase 7: dependency bootstrap +…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f300b2ae7d2898cc302897ad4e08c0f4bd353ab6": "f300b2a feat(integrations): ServiceNow incident creation" | kind=Commit | source=git | neighbors=[42b7429 feat(probe): deep intensity get…, 1209_system_ui_backend_level_changes, feat/va-maturity-gaps, testing/all-features, e80b25f feat(scheduling): ScanSchedule …, integrations.py] | lang=pt
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), Protocol, CPECandidate, Fact, pipeline.py — Phase 1 + Phase 2 end to …] | lang=en
- "detection_engine_bridge_persist_posture_findings": "_persist_posture_findings()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L352 | neighbors=[engine_bridge.py, create_findings_from_facts(), _apply_regression_reopen(), _find_remediated_match(), _posture_description(), _posture_title()] | lang=en
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L749 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts(), Background entry point (P1: keep detect…, Background entry point (P1: keep detect…, Background entry point (P1: keep detect…] | lang=en
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L56 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable(), (content_hash, fetched_at) of the pinne…, (content_hash, fetched_at) of the pinne…] | lang=en
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()] | lang=en
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()] | lang=en
- "detection_verification": "verification.py" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, de2d1c9 feat(verification): optional fa…, compute_verdict(), _int_confidence(), _qualifies_for_llm(), VerificationVerdict] | lang=en

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
