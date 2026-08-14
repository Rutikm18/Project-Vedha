# Node Description Batch 27 of 186

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

- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L463 | neighbors=[Send a heartbeat to the manager.       …, Transport, .ensure_device_access(), Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …] | lang=en
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L537 | neighbors=[Submit a scan result to the manager.   …, Transport, .ensure_device_access(), Submit a scan result to the manager.   …, Submit a scan result to the manager.   …, Submit a scan result to the manager.   …] | lang=en
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L249 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()] | lang=en
- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L183 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()] | lang=en
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service] | lang=en
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service] | lang=en
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()] | lang=en
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts] | lang=en
- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()] | lang=en
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()] | lang=en
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@02b63412fd2723bf5ed084158210ecdfe3da8183": "02b6341 feat(active-validation): pure escalation decision core" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, 7bd104a feat(active-validation): pure r…, active_validation.py, test_active_validation_escalation.py, 72f68af feat(verification): expose veri…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@08e0594c53bb049b1860e796d7c8315f1a5afd7e": "08e0594 deployement ready" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 41b692a Update project files, cac022c Everything is done and verified…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0d6be8593e79e58693a30c36cf650836a1cbb684": "0d6be85 feat(risk-rank): explainable 0-1000 finding priority" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, 3c7740e feat(lifecycle): pure manual-re…, risk_rank.py, test_risk_rank.py, 58c2d10 feat(active-validation): Valida…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2a36f8a328c12c4fd1f8d9d7a61f80bddc044304": "2a36f8a fix: update docker compose commands to use .env file for environment va…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, f1da96f fix: update environment variabl…, 6b6acb8 fix: update AWS compose command…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c277ba6178b4f0198b100b89c77054277f136d7": "3c277ba feat(lifecycle): add POST /findings/{id}/reopen endpoint" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, 50d6554 feat(active-validation): approv…, findings.py, test_finding_reopen_endpoint.py, 85e4537 feat(risk-rank): expose risk_ra…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c7740e5aee15e561362096ff219155ee7220b17": "3c7740e feat(lifecycle): pure manual-reopen helper" | kind=Commit | source=git | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, feat/coverage-gated-auto-resolution, integration/all-branches, 85e4537 feat(risk-rank): expose risk_ra…, resolution.py, test_manual_reopen.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 2a36f8a fix: update docker compose comm…, d7329cf feat: enhance AWS deployment wi…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@72f68af6099a8d2994b17533d41b44a3d1462134": "72f68af feat(verification): expose verification verdict + needs_review on findi…" | kind=Commit | source=git | neighbors=[2fcec73 feat(verification): stamp verdi…, feat/coverage-gated-auto-resolution, integration/all-branches, 02b6341 feat(active-validation): pure e…, finding.py, test_finding_verification_api.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7bd104a4484e9f6a90aad27a805339e333f13edf": "7bd104a feat(active-validation): pure result interpretation" | kind=Commit | source=git | neighbors=[02b6341 feat(active-validation): pure e…, feat/coverage-gated-auto-resolution, integration/all-branches, 58c2d10 feat(active-validation): Valida…, active_validation.py, test_active_validation_interpret.py] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@85e45373dae6a51a7abbd155431cc14324239f15": "85e4537 feat(risk-rank): expose risk_rank on findings API; add P2/P3/P4 plans" | kind=Commit | source=git | neighbors=[3c7740e feat(lifecycle): pure manual-re…, feat/coverage-gated-auto-resolution, integration/all-branches, 3c277ba feat(lifecycle): add POST /find…, finding.py, test_finding_risk_rank_api.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, f3c3591 docs: Phase 0 queue-control imp…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8cf23c236eb3cc74c9a7c7c156243658165f54e3": "8cf23c2 feat(resolution): wire coverage ledger + auto-resolution into detection…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, 937737b feat(resolution): reopen + flag…, engine_bridge.py, test_engine_bridge_resolution.py, bd409f5 feat(resolution): async applier…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9347a9a16f87a98cc882c39ad050f50544b65e0b": "9347a9a feat(posture): surface posture scorecard + patch matrix on dashboard" | kind=Commit | source=git | neighbors=[page.tsx, feat/coverage-gated-auto-resolution, integration/all-branches, main, a079178 fix(posture): full-width postur…, d2eb44c feat(posture): add dashboard Pa…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@937737b010d12e40761c6d3593787c0bd0f87d6b": "937737b feat(resolution): reopen + flag regressions on the original finding row" | kind=Commit | source=git | neighbors=[8cf23c2 feat(resolution): wire coverage…, feat/coverage-gated-auto-resolution, integration/all-branches, 0fbec7d feat(verification): add finding…, engine_bridge.py, test_engine_bridge_regression.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9a36729c7f6547ad20b1c35fee4ab54d4d603e9d": "9a36729 feat(resolution): coverage builder from completed-scanner facts" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, cbf5d6c feat(resolution): pure decision…, resolution.py, test_resolution_coverage.py, ddb51f2 feat(resolution): add finding r…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0791783d160c85c688ea511dc20396a7ac4e2e2": "a079178 fix(posture): full-width posture section; avoid blank grid column on de…" | kind=Commit | source=git | neighbors=[9347a9a feat(posture): surface posture …, page.tsx, feat/coverage-gated-auto-resolution, integration/all-branches, main, 0f0097b feat(posture): mirror posture s…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aa560a0292202728647e1f6cde4e0ca942782cd6": "aa560a0 feat(posture): add dashboard PostureScorecard component" | kind=Commit | source=git | neighbors=[2cddd52 fix(posture): tenant-scope run …, feat/coverage-gated-auto-resolution, integration/all-branches, main, d2eb44c feat(posture): add dashboard Pa…, PostureScorecard.tsx] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd409f5724ece8d940d48f06f98b9f6188970117": "bd409f5 feat(resolution): async applier over engine-managed open findings" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, 8cf23c2 feat(resolution): wire coverage…, resolution.py, test_resolution_apply.py, cbf5d6c feat(resolution): pure decision…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c02c4652680a709056c4a8e342699c00e80454dc": "c02c465 feat(verification): optional LangGraph orchestration skin" | kind=Commit | source=git | neighbors=[verification_graph.py, feat/coverage-gated-auto-resolution, integration/all-branches, 2fcec73 feat(verification): stamp verdi…, test_verification_graph.py, de2d1c9 feat(verification): optional fa…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ca41cbf25bddbb70f2808dcfbb236405c24bfc69": "ca41cbf docs: pre-auth probe enrollment token design spec" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 81c81cb feat: implement outbox reclaim …, f1da96f fix: update environment variabl…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@caf1e5d0a9e53f79a5c9e541a083b332aa127fdd": "caf1e5d feat(verification): deterministic passive verdict core" | kind=Commit | source=git | neighbors=[0fbec7d feat(verification): add finding…, feat/coverage-gated-auto-resolution, integration/all-branches, de2d1c9 feat(verification): optional fa…, verification.py, test_verification_core.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@cbf5d6cb96915e7c031de705eb116568a081940b": "cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db gu…" | kind=Commit | source=git | neighbors=[9a36729 feat(resolution): coverage buil…, feat/coverage-gated-auto-resolution, integration/all-branches, bd409f5 feat(resolution): async applier…, resolution.py, test_resolution_decision.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d2eb44c3d2c1f5ac6a3398dc1bf865c46447a9a8": "d2eb44c feat(posture): add dashboard PatchComparisonMatrix component" | kind=Commit | source=git | neighbors=[aa560a0 feat(posture): add dashboard Po…, feat/coverage-gated-auto-resolution, integration/all-branches, main, 9347a9a feat(posture): surface posture …, PatchComparisonMatrix.tsx] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7329cfe261cfa5fd29d0892344b94340cbe0b77": "d7329cf feat: enhance AWS deployment with new environment variables and scripts…" | kind=Commit | source=git | neighbors=[b5ffcb0 Refactor Vedha probe installer …, feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, 6b6acb8 fix: update AWS compose command…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de2d1c9825984fa315f761df4bb2da6139d7ff36": "de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage" | kind=Commit | source=git | neighbors=[caf1e5d feat(verification): determinist…, feat/coverage-gated-auto-resolution, integration/all-branches, c02c465 feat(verification): optional La…, verification.py, test_verification_llm.py] | lang=nl
- "commit:repo:github.com/Rutikm18/Project-Vedha@f1da96f64e70aef9d0275a6cdcdbf89b7334e948": "f1da96f fix: update environment variables and resource limits in docker-compose…" | kind=Commit | source=git | neighbors=[2a36f8a fix: update docker compose comm…, feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, ca41cbf docs: pre-auth probe enrollment…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3c359163f16baf103a46a5170e40a9e95edda9d": "f3c3591 docs: Phase 0 queue-control implementation plan (8 TDD tasks)" | kind=Commit | source=git | neighbors=[879cdfa docs: probe fleet automation de…, feat/coverage-gated-auto-resolution, integration/all-branches, main, worktree-fleet-already-downloaded-cmd, c76b428 backend and login page error ha…] | lang=en
- "detection_active_validation": "active_validation.py" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, 7bd104a feat(active-validation): pure r…, interpret_validation(), should_escalate(), ValidationOutcome, active_validation.py — manager-side dec…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
