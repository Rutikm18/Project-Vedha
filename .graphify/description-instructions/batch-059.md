# Node Description Batch 60 of 380

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

- "agent_deps_install_requirements": "install_requirements()" | kind=code-symbol | source=probe/agent/deps.py:L48 | neighbors=[deps.py, ensure_venv(), pip_install_argsets(), reqs_hash(), venv_dir()]
- "agent_instance_lock_acquire_instance_lock": "acquire_instance_lock()" | kind=code-symbol | source=probe/agent/instance_lock.py:L85 | neighbors=[instance_lock.py, _holder_hint(), InstanceLockError, lock_path_for(), Take the single-instance lock for `stat…]
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L35 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license(), Stable per-machine ID, derived from hw_…]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L29 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()]
- "agent_result_queue_nullcipher": "NullCipher" | kind=code-symbol | source=probe/agent/result_queue.py:L30 | neighbors=[result_queue.py, .decrypt(), .encrypt(), Identity cipher — tests + explicitly-pl…, .__init__()]
- "agent_result_queue_resultqueue_enqueue": ".enqueue()" | kind=code-symbol | source=probe/agent/result_queue.py:L144 | neighbors=[ResultQueue, .encrypt(), ._atomic_write(), ._enforce_size_bounds(), ._find()]
- "agent_result_queue_resultqueue_pending": ".pending()" | kind=code-symbol | source=probe/agent/result_queue.py:L157 | neighbors=[ResultQueue, ._files(), ._read(), .prune(), .stats()]
- "agent_result_queue_resultqueue_stats": ".stats()" | kind=code-symbol | source=probe/agent/result_queue.py:L174 | neighbors=[ResultQueue, QueueStats, ._bytes(), ._files(), .pending()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L215 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists(), Number of pending (unsubmitted) results…, Number of pending (unsubmitted) results…]
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=probe/agent/result_spool.py:L59 | neighbors=[ResultSpool, .quarantine(), .remove(), .save(), .exists()]
- "agent_self_scan_run": "run()" | kind=code-symbol | source=probe/agent/self_scan.py:L98 | neighbors=[self_scan.py, main(), detect_host_container(), primary_ipv4(), run_from()]
- "agent_transport_devicealreadyenrollederror": "DeviceAlreadyEnrolledError" | kind=code-symbol | source=probe/agent/transport.py:L53 | neighbors=[transport.py, TransportError, The probe's device signing key is alrea…, .create_enrollment_request(), The probe's device signing key is alrea…]
- "agent_transport_enrollmentrequestnotfound": "EnrollmentRequestNotFound" | kind=code-symbol | source=probe/agent/transport.py:L64 | neighbors=[transport.py, TransportError, A poll/activate targeted an enrollment …, .activate_enrollment(), .poll_enrollment()]
- "agent_transport_transport_activate_enrollment": ".activate_enrollment()" | kind=code-symbol | source=probe/agent/transport.py:L478 | neighbors=[Transport, EnrollmentRequestNotFound, manager_fingerprint(), .load_state(), .update_state()]
- "agent_validation_score_inventory": "score_inventory()" | kind=code-symbol | source=probe/agent/validation.py:L201 | neighbors=[validation.py, Score promoted inventory against explic…, _metric(), _not_scored(), validate_ground_truth()]
- "ai_hallucination_hallucinationguard_validate": ".validate()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L101 | neighbors=[HallucinationGuard, .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), Run all relevant checks and return a co…]
- "ai_llm_report_parse_json_response": "_parse_json_response()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L385 | neighbors=[llm_report.py, .generate_remediation_plan(), Fault-tolerant JSON extraction from an …, Fault-tolerant JSON extraction from an …, Fault-tolerant JSON extraction from an …]
- "ai_llm_report_safe_commands": "_safe_commands()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L412 | neighbors=[llm_report.py, _normalize_ai_plan(), Extract a step's command(s) and drop an…, Extract a step's command(s) and drop an…, Extract a step's command(s) and drop an…]
- "ai_prioritizer_extract_features": "extract_features()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L72 | neighbors=[prioritizer.py, _to_float(), Build the model's feature vector from a…, .explain_prediction(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_fallback_score": ".fallback_score()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L204 | neighbors=[Weighted composite 0–1000 (same shape a…, VulnPrioritizer, .explain_prediction(), ._formula_contributions(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_predict_priority": ".predict_priority()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L148 | neighbors=[Return a 0–1000 priority score. Uses th…, VulnPrioritizer, .explain_prediction(), extract_features(), .fallback_score()]
- "app_version": "version.py" | kind=code-symbol | source=manager/backend/app/version.py:L1 | neighbors=[main.py, get_version(), Single source of truth for the deployed…, b5ffcb0 Refactor Vedha probe installer …, health.py]
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "assistant_assistantfab": "AssistantFab.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L1 | neighbors=[AssistantFab(), AssistantProvider.tsx, useAssistant(), 1fe16c8 stable but some dead code, need…, 41b692a Update project files]
- "assistant_assistanttext": "AssistantText.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText(), plain(), 1fe16c8 stable but some dead code, need…]
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "attack_paths_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "auth_jwt_create_refresh_token": "create_refresh_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L67 | neighbors=[jwt.py, _now(), Returns (token, jti) — jti is stored in…, Returns (token, jti) — jti is stored in…, Returns (token, jti) — jti is stored in…]
- "auth_middleware_tenantisolationmiddleware_dispatch": ".dispatch()" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L84 | neighbors=[TenantIsolationMiddleware, agent_jwt_path_allows(), _is_public_enrollment_request(), portal_jwt_path_allows(), ._authenticate_pat()]
- "auth_pat_build_personal_access_token": "build_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L54 | neighbors=[pat.py, hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()]
- "auth_portal_scope_resolve_scope": "resolve_scope()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L47 | neighbors=[portal_scope.py, The safe engagement id to filter by.   …, assert_client(), scoped_engagement(), The safe engagement id to filter by.   …]
- "auth_router_authenticate": "_authenticate()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L84 | neighbors=[router.py, login(), Validates credentials and returns the U…, Validates credentials and returns the U…, Validates credentials and returns the U…]
- "auth_startup_check_admin_account": "_check_admin_account()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L157 | neighbors=[startup.py, CheckResult, Verify the seeded admin account exists …, run_startup_diagnostics(), Verify the seeded admin account exists …]
- "auth_startup_check_bcrypt": "_check_bcrypt()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L145 | neighbors=[startup.py, CheckResult, Verify the bcrypt library can round-tri…, run_startup_diagnostics(), Verify the bcrypt library can round-tri…]
- "auth_startup_check_tenant": "_check_tenant()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L195 | neighbors=[startup.py, CheckResult, Verify the default tenant is active., run_startup_diagnostics(), Verify the default tenant is active.]
- "auth_startup_diagnosticsreport": "DiagnosticsReport" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L65 | neighbors=[startup.py, .all_ok(), .as_dict(), .has_fatal(), run_startup_diagnostics()]
- "auth_startup_startupaborterror": "StartupAbortError" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L90 | neighbors=[startup.py, Raised when one or more fatal checks fa…, run_startup_diagnostics(), RuntimeError, Raised when one or more fatal checks fa…]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#agents/greeting-introduction": "agents/greeting-introduction" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 8d65c92 first commit, a388bb3 script updated, architecture de…, bd7383f scanner fine ..now integrations, f5ce592 first commit]
- "chokepoints_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/chokepoints/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "cli_auth_serverurl": "serverUrl()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L42 | neighbors=[auth.ts, apiFetch(), doctor.ts, interactive.ts, login.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-059.json

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
