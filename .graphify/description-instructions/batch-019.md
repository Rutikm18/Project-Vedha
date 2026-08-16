# Node Description Batch 20 of 209

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@0f0097bd1d03cc4d36e8d8e0f8dbe4bf2d68ae0a": "0f0097b feat(posture): mirror posture scorecard into generated reports" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, fadb4f5 fix(posture): hoist report-sect…, ai_report.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@237a8319dd25a9eada7aec7f140dc7dba66b7dcd": "237a831 feat(posture): add run comparison, matrix, and response builder" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 045c9ae fix(posture): normalize run_at …, posture.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2cddd526f80b7999775f6cfdc6726ad8e77325ac": "2cddd52 fix(posture): tenant-scope run helper; test null asset/score paths; tid…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, aa560a0 feat(posture): add dashboard Po…, analytics.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c277ba6178b4f0198b100b89c77054277f136d7": "3c277ba feat(lifecycle): add POST /findings/{id}/reopen endpoint" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 50d6554 feat(active-validation): approv…, findings.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c7740e5aee15e561362096ff219155ee7220b17": "3c7740e feat(lifecycle): pure manual-reopen helper" | kind=Commit | source=git | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 85e4537 feat(risk-rank): expose risk_ra…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@52388652e83dde75d08604b07cfbeea2a3929271": "5238865 feat(posture): add pure scoring core (noisy-OR risk/exploit/posture)" | kind=Commit | source=git | neighbors=[10ceaca feat: implement AI model fallba…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 237a831 feat(posture): add run comparis…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6c1f014f6e8fbacb7080f4aeed9329f17df208fe": "6c1f014 feat(correlation): implement composite findings for NTLM relay, legacy …" | kind=Commit | source=git | neighbors=[4d0377d Add unit tests for SMB scanner,…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 22701ea Add tests for scanner parity an…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@72f68af6099a8d2994b17533d41b44a3d1462134": "72f68af feat(verification): expose verification verdict + needs_review on findi…" | kind=Commit | source=git | neighbors=[2fcec73 feat(verification): stamp verdi…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 02b6341 feat(active-validation): pure e…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7bd104a4484e9f6a90aad27a805339e333f13edf": "7bd104a feat(active-validation): pure result interpretation" | kind=Commit | source=git | neighbors=[02b6341 feat(active-validation): pure e…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 58c2d10 feat(active-validation): Valida…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@85e45373dae6a51a7abbd155431cc14324239f15": "85e4537 feat(risk-rank): expose risk_rank on findings API; add P2/P3/P4 plans" | kind=Commit | source=git | neighbors=[3c7740e feat(lifecycle): pure manual-re…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 3c277ba feat(lifecycle): add POST /find…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8cf23c236eb3cc74c9a7c7c156243658165f54e3": "8cf23c2 feat(resolution): wire coverage ledger + auto-resolution into detection…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 937737b feat(resolution): reopen + flag…, engine_bridge.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@937737b010d12e40761c6d3593787c0bd0f87d6b": "937737b feat(resolution): reopen + flag regressions on the original finding row" | kind=Commit | source=git | neighbors=[8cf23c2 feat(resolution): wire coverage…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 0fbec7d feat(verification): add finding…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9a36729c7f6547ad20b1c35fee4ab54d4d603e9d": "9a36729 feat(resolution): coverage builder from completed-scanner facts" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, cbf5d6c feat(resolution): pure decision…, resolution.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9de087aedb96212596b5b8b4229dfe6215bbd2de": "9de087a feat(posture): add GET /analytics/posture endpoint" | kind=Commit | source=git | neighbors=[045c9ae fix(posture): normalize run_at …, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 2cddd52 fix(posture): tenant-scope run …] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a4b970ca55febc554c4d6d9f90369fafaa5f8111": "a4b970c feat(fleet): add run command for already-downloaded install.sh" | kind=Commit | source=git | neighbors=[30261eb feat: enhance advisor flow with…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd409f5724ece8d940d48f06f98b9f6188970117": "bd409f5 feat(resolution): async applier over engine-managed open findings" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 8cf23c2 feat(resolution): wire coverage…, resolution.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c02c4652680a709056c4a8e342699c00e80454dc": "c02c465 feat(verification): optional LangGraph orchestration skin" | kind=Commit | source=git | neighbors=[verification_graph.py, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 2fcec73 feat(verification): stamp verdi…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c0f3b4c86830cc30f1c8a4da8694f7aa5c0807dc": "c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy…" | kind=Commit | source=git | neighbors=[22701ea Add tests for scanner parity an…, agent.py, config.py, feat/syn-scanner-osfp-adaptive, main, 0e22dbf feat(probe): bounded auto-troub…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5e2d0ed7a2fe2e171616a98cebb2295cf557314": "c5e2d0e chore: retire probe-go to spike/probe-go branch" | kind=Commit | source=git | neighbors=[1fe16c8 stable but some dead code, need…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, worktree-fleet-already-downloaded-cmd] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@caf1e5d0a9e53f79a5c9e541a083b332aa127fdd": "caf1e5d feat(verification): deterministic passive verdict core" | kind=Commit | source=git | neighbors=[0fbec7d feat(verification): add finding…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, de2d1c9 feat(verification): optional fa…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@cbf5d6cb96915e7c031de705eb116568a081940b": "cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db gu…" | kind=Commit | source=git | neighbors=[9a36729 feat(resolution): coverage buil…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, bd409f5 feat(resolution): async applier…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de2d1c9825984fa315f761df4bb2da6139d7ff36": "de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage" | kind=Commit | source=git | neighbors=[caf1e5d feat(verification): determinist…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, c02c465 feat(verification): optional La…] | lang=nl
- "commit:repo:github.com/Rutikm18/Project-Vedha@fadb4f53f6fecb205c9da67b084b4f8ad43ea578": "fadb4f5 fix(posture): hoist report-section test import; flush before section co…" | kind=Commit | source=git | neighbors=[0f0097b feat(posture): mirror posture s…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, a0b870c fix(posture): score over open f…] | lang=en
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO] | lang=en
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L99 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine] | lang=en
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[pipeline.py, AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[ab_evaluate(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[run_pipeline(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()] | lang=en
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L72 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…] | lang=en
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()] | lang=en
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()] | lang=en
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L120 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()] | lang=en
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 5d5c158 refactor: remove unused dashboa…, Exposure, GET, backend.ts, backend()] | lang=en
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder] | lang=en
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[page.tsx, page.tsx, page.tsx, page.tsx, useToast.ts, page.tsx] | lang=en
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()] | lang=en
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()] | lang=en
- "main_scripts_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml(), _run_nmap()] | lang=en
- "main_scripts_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L330 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
