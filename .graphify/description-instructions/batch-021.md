# Node Description Batch 22 of 209

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

- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes] | lang=en
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L93 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_fully_excluded_cidr_is_dropped(), .test_hostname_passes_through()] | lang=en
- "tests_test_service_match": "test_service_match.py" | kind=code-symbol | source=probe/tests/test_service_match.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, service_banner.py, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder] | lang=en
- "tests_test_tls_posture_testclassifycipher": "TestClassifyCipher" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L18 | neighbors=[test_tls_posture.py, .test_3des_is_weak(), .test_anonymous_is_weak(), .test_chacha20_is_aead(), .test_export_and_md5_are_weak(), .test_modern_aead_pfs()] | lang=en
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds()] | lang=en
- "vuln_prioritizer_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetInput, FindingInput, vulnPrioritizer, DEMO_ASSETS, DEMO_FINDINGS] | lang=en
- "websocket_manager_connectionmanager": "ConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L25 | neighbors=[manager.py, .broadcast(), .connect(), .disconnect(), .get_room_clients(), .__init__()] | lang=en
- "workers_reaper": "reaper.py" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, config.py, database.py, expire_attempt(), reap_once()] | lang=en
- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=probe/workflow/cache.py:L78 | neighbors=[cache.py, In-memory (host, port, scanner) -> Cach…, .all_entries_for_host(), .get(), .__init__(), ._load()] | lang=en
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()] | lang=en
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…] | lang=en
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L47 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()] | lang=en
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L709 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…] | lang=en
- "agent_device_identity": "device_identity.py" | kind=code-symbol | source=probe/agent/device_identity.py:L1 | neighbors=[decode_key(), encode_key(), generate_signing_identity(), sign_b64(), signing_public_from_private(), verify_site_policy()] | lang=en
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L371 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()] | lang=en
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError] | lang=en
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=probe/agent/result_spool.py:L184 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists(), ._path(), .quarantine(), .remove()] | lang=en
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L110 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()] | lang=en
- "agent_transport_transport_ensure_device_access": ".ensure_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L394 | neighbors=[Refresh a device token before expiry; l…, Transport, .connect_ws(), .load_state(), .refresh_device_access(), .heartbeat()] | lang=en
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
- "commit:repo:github.com/Rutikm18/Project-Vedha@08e0594c53bb049b1860e796d7c8315f1a5afd7e": "08e0594 deployement ready" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 41b692a Update project files] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0e22dbf9a3d7b87c329cbfa701b15bcc9e540c8c": "0e22dbf feat(probe): bounded auto-troubleshoot for Manager connectivity" | kind=Commit | source=git | neighbors=[agent.py, feat/syn-scanner-osfp-adaptive, main, 1af3404 feat(deploy): probe-free manage…, agents.py, test_http_lease.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2a36f8a328c12c4fd1f8d9d7a61f80bddc044304": "2a36f8a fix: update docker compose commands to use .env file for environment va…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, f1da96f fix: update environment variabl…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 2a36f8a fix: update docker compose comm…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9347a9a16f87a98cc882c39ad050f50544b65e0b": "9347a9a feat(posture): surface posture scorecard + patch matrix on dashboard" | kind=Commit | source=git | neighbors=[page.tsx, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, a079178 fix(posture): full-width postur…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0791783d160c85c688ea511dc20396a7ac4e2e2": "a079178 fix(posture): full-width posture section; avoid blank grid column on de…" | kind=Commit | source=git | neighbors=[9347a9a feat(posture): surface posture …, page.tsx, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aa560a0292202728647e1f6cde4e0ca942782cd6": "aa560a0 feat(posture): add dashboard PostureScorecard component" | kind=Commit | source=git | neighbors=[2cddd52 fix(posture): tenant-scope run …, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, d2eb44c feat(posture): add dashboard Pa…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@ca41cbf25bddbb70f2808dcfbb236405c24bfc69": "ca41cbf docs: pre-auth probe enrollment token design spec" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 81c81cb feat: implement outbox reclaim …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
