# Node Description Batch 25 of 131

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

- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L478 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()] | lang=en
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L153 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()] | lang=en
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L157 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…] | lang=en
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L235 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count concrete open services, not gener…, run_scan()] | lang=en
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L67 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…] | lang=en
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L177 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …] | lang=en
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L35 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license(), Stable per-machine ID, derived from hw_…] | lang=en
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L29 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()] | lang=en
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L215 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists(), Number of pending (unsubmitted) results…, Number of pending (unsubmitted) results…] | lang=en
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=probe/agent/result_spool.py:L59 | neighbors=[ResultSpool, .quarantine(), .remove(), .save(), .exists()] | lang=en
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L518 | neighbors=[Fetch the engagement's authoritative sc…, Transport, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…] | lang=en
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L600 | neighbors=[Generic authenticated GET, returns pars…, Transport, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…] | lang=en
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L164 | neighbors=[True if we have both an agent_id and a …, Transport, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …] | lang=en
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L658 | neighbors=[True if the WebSocket connection is act…, Transport, True if the WebSocket connection is act…, True if the WebSocket connection is act…, Fetch the engagement's authoritative sc…] | lang=en
- "agent_transport_transport_ws_url": ".ws_url()" | kind=code-symbol | source=probe/agent/transport.py:L616 | neighbors=[Return the WebSocket endpoint without e…, Transport, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket connection URL wit…] | lang=en
- "agent_validation_score_inventory": "score_inventory()" | kind=code-symbol | source=probe/agent/validation.py:L201 | neighbors=[validation.py, Score promoted inventory against explic…, _metric(), _not_scored(), validate_ground_truth()] | lang=en
- "ai_hallucination_hallucinationguard_validate": ".validate()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L101 | neighbors=[HallucinationGuard, .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), Run all relevant checks and return a co…] | lang=en
- "ai_prioritizer_extract_features": "extract_features()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L72 | neighbors=[prioritizer.py, _to_float(), Build the model's feature vector from a…, .explain_prediction(), .predict_priority()] | lang=en
- "ai_prioritizer_vulnprioritizer_fallback_score": ".fallback_score()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L204 | neighbors=[Weighted composite 0–1000 (same shape a…, VulnPrioritizer, .explain_prediction(), ._formula_contributions(), .predict_priority()] | lang=en
- "ai_prioritizer_vulnprioritizer_predict_priority": ".predict_priority()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L148 | neighbors=[Return a 0–1000 priority score. Uses th…, VulnPrioritizer, .explain_prediction(), extract_features(), .fallback_score()] | lang=en
- "app_version": "version.py" | kind=code-symbol | source=manager/backend/app/version.py:L1 | neighbors=[main.py, get_version(), Single source of truth for the deployed…, b5ffcb0 Refactor Vedha probe installer …, health.py] | lang=en
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "assistant_assistantfab": "AssistantFab.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L1 | neighbors=[AssistantFab(), AssistantProvider.tsx, useAssistant(), 1fe16c8 stable but some dead code, need…, 41b692a Update project files] | lang=en
- "assistant_assistanttext": "AssistantText.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText(), plain(), 1fe16c8 stable but some dead code, need…] | lang=en
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "attack_paths_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_pat_build_personal_access_token": "build_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L54 | neighbors=[pat.py, hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()] | lang=en
- "auth_startup_diagnosticsreport": "DiagnosticsReport" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L67 | neighbors=[startup.py, .all_ok(), .as_dict(), .has_fatal(), run_startup_diagnostics()] | lang=en
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#agents/greeting-introduction": "agents/greeting-introduction" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 8d65c92 first commit, a388bb3 script updated, architecture de…, bd7383f scanner fine ..now integrations, f5ce592 first commit] | lang=en
- "chokepoints_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/chokepoints/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "cli_auth_serverurl": "serverUrl()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L42 | neighbors=[auth.ts, apiFetch(), doctor.ts, interactive.ts, login.ts] | lang=en
- "commands_interactive_runinteractive": "runInteractive()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2102 | neighbors=[index.ts, interactive.ts, banner(), ensureAuthenticated(), mainMenu()] | lang=en
- "commands_interactive_runphaseexploitation": "runPhaseExploitation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1070 | neighbors=[interactive.ts, runIterativeEngagement(), choose(), confirm(), ln()] | lang=en
- "commands_interactive_runphaseportscan": "runPhasePortScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1028 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphaseservicedetect": "runPhaseServiceDetect()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1037 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphasevulnassess": "runPhaseVulnAssess()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1051 | neighbors=[interactive.ts, runIterativeEngagement(), confirm(), ln(), runPhaseWithTools()] | lang=en
- "commands_interactive_runvulnassessmentflow": "runVulnAssessmentFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1184 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow(), wizardScan()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@41b692a77a1dd6d2e5666f2fa2f8aa4b1e084e64": "41b692a Update project files" | kind=Commit | source=git | neighbors=[08e0594 deployement ready, AssistantFab.tsx, main, 879cdfa docs: probe fleet automation de…, page.tsx] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@80b6dbcc5515152a76b93176716127f4f997f356": "80b6dbc Remove environment secrets from repository" | kind=Commit | source=git | neighbors=[main, spike/probe-go, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, feat/probe-usecase-alignment] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-024.json

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
