# Node Description Batch 10 of 330

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

- "commands_interactive_wizardscan": "wizardScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L329 | neighbors=[interactive.ts, mainMenu(), ask(), banner(), choose(), confirm()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@02b63412fd2723bf5ed084158210ecdfe3da8183": "02b6341 feat(active-validation): pure escalation decision core" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@045c9ae0769ca5697260d9485812cc159ef0734c": "045c9ae fix(posture): normalize run_at in _present_in_run; drop dead scores_pre…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0d6be8593e79e58693a30c36cf650836a1cbb684": "0d6be85 feat(risk-rank): explainable 0-1000 finding priority" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0e22dbf9a3d7b87c329cbfa701b15bcc9e540c8c": "0e22dbf feat(probe): bounded auto-troubleshoot for Manager connectivity" | kind=Commit | source=git | neighbors=[agent.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0f0097bd1d03cc4d36e8d8e0f8dbe4bf2d68ae0a": "0f0097b feat(posture): mirror posture scorecard into generated reports" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@237a8319dd25a9eada7aec7f140dc7dba66b7dcd": "237a831 feat(posture): add run comparison, matrix, and response builder" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2cddd526f80b7999775f6cfdc6726ad8e77325ac": "2cddd52 fix(posture): tenant-scope run helper; test null asset/score paths; tid…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c277ba6178b4f0198b100b89c77054277f136d7": "3c277ba feat(lifecycle): add POST /findings/{id}/reopen endpoint" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@3c7740e5aee15e561362096ff219155ee7220b17": "3c7740e feat(lifecycle): pure manual-reopen helper" | kind=Commit | source=git | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@52388652e83dde75d08604b07cfbeea2a3929271": "5238865 feat(posture): add pure scoring core (noisy-OR risk/exploit/posture)" | kind=Commit | source=git | neighbors=[10ceaca feat: implement AI model fallba…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6be8259eadeca140adc8b3b0d2d0566889bae772": "6be8259 feat(integrations): outbox delivery worker + Send test (email/Slack/Jir…" | kind=Commit | source=git | neighbors=[00c6648 feat(settings): editable email/…, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6c1f014f6e8fbacb7080f4aeed9329f17df208fe": "6c1f014 feat(correlation): implement composite findings for NTLM relay, legacy …" | kind=Commit | source=git | neighbors=[4d0377d Add unit tests for SMB scanner,…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@72f68af6099a8d2994b17533d41b44a3d1462134": "72f68af feat(verification): expose verification verdict + needs_review on findi…" | kind=Commit | source=git | neighbors=[2fcec73 feat(verification): stamp verdi…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7bd104a4484e9f6a90aad27a805339e333f13edf": "7bd104a feat(active-validation): pure result interpretation" | kind=Commit | source=git | neighbors=[02b6341 feat(active-validation): pure e…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@85e45373dae6a51a7abbd155431cc14324239f15": "85e4537 feat(risk-rank): expose risk_rank on findings API; add P2/P3/P4 plans" | kind=Commit | source=git | neighbors=[3c7740e feat(lifecycle): pure manual-re…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8cf23c236eb3cc74c9a7c7c156243658165f54e3": "8cf23c2 feat(resolution): wire coverage ledger + auto-resolution into detection…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@937737b010d12e40761c6d3593787c0bd0f87d6b": "937737b feat(resolution): reopen + flag regressions on the original finding row" | kind=Commit | source=git | neighbors=[8cf23c2 feat(resolution): wire coverage…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9a36729c7f6547ad20b1c35fee4ab54d4d603e9d": "9a36729 feat(resolution): coverage builder from completed-scanner facts" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9de087aedb96212596b5b8b4229dfe6215bbd2de": "9de087a feat(posture): add GET /analytics/posture endpoint" | kind=Commit | source=git | neighbors=[045c9ae fix(posture): normalize run_at …, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a4b970ca55febc554c4d6d9f90369fafaa5f8111": "a4b970c feat(fleet): add run command for already-downloaded install.sh" | kind=Commit | source=git | neighbors=[30261eb feat: enhance advisor flow with…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@b393dbe812e14abae4e65efa69a5640e3264827a": "b393dbe feat: Enhance Sidebar UI and introduce local run capabilities" | kind=Commit | source=git | neighbors=[3ad95f4 feat: Optimize asset service fe…, agent.py, local_run.py, use_cases.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd409f5724ece8d940d48f06f98b9f6188970117": "bd409f5 feat(resolution): async applier over engine-managed open findings" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c02c4652680a709056c4a8e342699c00e80454dc": "c02c465 feat(verification): optional LangGraph orchestration skin" | kind=Commit | source=git | neighbors=[verification_graph.py, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5e2d0ed7a2fe2e171616a98cebb2295cf557314": "c5e2d0e chore: retire probe-go to spike/probe-go branch" | kind=Commit | source=git | neighbors=[1fe16c8 stable but some dead code, need…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@caf1e5d0a9e53f79a5c9e541a083b332aa127fdd": "caf1e5d feat(verification): deterministic passive verdict core" | kind=Commit | source=git | neighbors=[0fbec7d feat(verification): add finding…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@cbf5d6cb96915e7c031de705eb116568a081940b": "cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db gu…" | kind=Commit | source=git | neighbors=[9a36729 feat(resolution): coverage buil…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de2d1c9825984fa315f761df4bb2da6139d7ff36": "de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage" | kind=Commit | source=git | neighbors=[caf1e5d feat(verification): determinist…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=nl
- "commit:repo:github.com/Rutikm18/Project-Vedha@fadb4f53f6fecb205c9da67b084b4f8ad43ea578": "fadb4f5 fix(posture): hoist report-section test import; flush before section co…" | kind=Commit | source=git | neighbors=[0f0097b feat(posture): mirror posture s…, addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=en
- "console_primitives": "Primitives.tsx" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 5d5c158 refactor: remove unused dashboa…, f473173 merge: network VA accuracy, KEV…, Delta(), Meter()] | lang=en
- "detection_engine_version_compare": "version_compare.py" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _char_order(), _clear_validation_cache(), _compare_non_digit(), _compare_part()] | lang=en
- "graph_builder_graphbuilder": "GraphBuilder" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L90 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph(), .build_from_db()] | lang=en
- "lib_cases_store": "cases-store.ts" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, addComment(), Case, CaseActivity, CaseComment, CaseSeverity] | lang=en
- "lib_testssl_parser": "testssl-parser.ts" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, types.ts, LiveFinding, Severity] | lang=en
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/login/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 10ceaca feat: implement AI model fallba…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 3c9062a refactor: Update dashboard comp…] | lang=en
- "models_enums_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L114 | neighbors=[enums.py, str, LLMReportGenerator, LLMUnavailableError, LLMReportGenerator — Claude-backed narr…, Raised when the Anthropic SDK or API ke…] | lang=en
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=probe/scanner/mass_scan.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _ConnectSweep, _have_masscan(), main()] | lang=en
- "services_job_result_service": "job_result_service.py" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 21ebc46 feat(detection): unified priori…, 22701ea Add tests for scanner parity an…, 3565ada fix(ingest): NUL-safe result su…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files] | lang=en
- "supporting_research_evidence_store": "evidence_store.py" | kind=code-symbol | source=Supporting_research/evidence_store.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, AssetVerdict, connect(), coverage_summary(), exposure_timeline(), get_path()] | lang=en
- "tests_findings_store_test": "findings-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, LiveFinding, resetCounters(), getAllFindings(), getFindingById()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-009.json

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
