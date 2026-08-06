# Node Description Batch 33 of 134

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

- "commands_interactive_pickmodulesbycategory": "pickModulesByCategory()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L300 | neighbors=[interactive.ts, confirm(), ln(), wizardScan()] | lang=en
- "commands_interactive_runrulebasedvalidation": "runRuleBasedValidation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1355 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardstatus": "wizardStatus()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1938 | neighbors=[interactive.ts, mainMenu(), divider(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 298a9d4 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, a388bb3 script updated, architecture de…, f5ce592 first commit] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, agents/greeting-introduction, main, bd7383f scanner fine ..now integrations] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@08e0594c53bb049b1860e796d7c8315f1a5afd7e": "08e0594 deployement ready" | kind=Commit | source=git | neighbors=[main, worktree-fleet-already-downloaded-cmd, 41b692a Update project files, cac022c Everything is done and verified…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2a36f8a328c12c4fd1f8d9d7a61f80bddc044304": "2a36f8a fix: update docker compose commands to use .env file for environment va…" | kind=Commit | source=git | neighbors=[main, worktree-fleet-already-downloaded-cmd, f1da96f fix: update environment variabl…, 6b6acb8 fix: update AWS compose command…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[main, worktree-fleet-already-downloaded-cmd, 2a36f8a fix: update docker compose comm…, d7329cf feat: enhance AWS deployment wi…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, main, worktree-fleet-already-downloaded-cmd, f3c3591 docs: Phase 0 queue-control imp…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9347a9a16f87a98cc882c39ad050f50544b65e0b": "9347a9a feat(posture): surface posture scorecard + patch matrix on dashboard" | kind=Commit | source=git | neighbors=[page.tsx, main, a079178 fix(posture): full-width postur…, d2eb44c feat(posture): add dashboard Pa…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0791783d160c85c688ea511dc20396a7ac4e2e2": "a079178 fix(posture): full-width posture section; avoid blank grid column on de…" | kind=Commit | source=git | neighbors=[9347a9a feat(posture): surface posture …, page.tsx, main, 0f0097b feat(posture): mirror posture s…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aa560a0292202728647e1f6cde4e0ca942782cd6": "aa560a0 feat(posture): add dashboard PostureScorecard component" | kind=Commit | source=git | neighbors=[2cddd52 fix(posture): tenant-scope run …, main, d2eb44c feat(posture): add dashboard Pa…, PostureScorecard.tsx] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@ca41cbf25bddbb70f2808dcfbb236405c24bfc69": "ca41cbf docs: pre-auth probe enrollment token design spec" | kind=Commit | source=git | neighbors=[main, worktree-fleet-already-downloaded-cmd, 81c81cb feat: implement outbox reclaim …, f1da96f fix: update environment variabl…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d2eb44c3d2c1f5ac6a3398dc1bf865c46447a9a8": "d2eb44c feat(posture): add dashboard PatchComparisonMatrix component" | kind=Commit | source=git | neighbors=[aa560a0 feat(posture): add dashboard Po…, main, 9347a9a feat(posture): surface posture …, PatchComparisonMatrix.tsx] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7329cfe261cfa5fd29d0892344b94340cbe0b77": "d7329cf feat: enhance AWS deployment with new environment variables and scripts…" | kind=Commit | source=git | neighbors=[b5ffcb0 Refactor Vedha probe installer …, main, worktree-fleet-already-downloaded-cmd, 6b6acb8 fix: update AWS compose command…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f1da96f64e70aef9d0275a6cdcdbf89b7334e948": "f1da96f fix: update environment variables and resource limits in docker-compose…" | kind=Commit | source=git | neighbors=[2a36f8a fix: update docker compose comm…, main, worktree-fleet-already-downloaded-cmd, ca41cbf docs: pre-auth probe enrollment…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3c359163f16baf103a46a5170e40a9e95edda9d": "f3c3591 docs: Phase 0 queue-control implementation plan (8 TDD tasks)" | kind=Commit | source=git | neighbors=[879cdfa docs: probe fleet automation de…, main, worktree-fleet-already-downloaded-cmd, c76b428 backend and login page error ha…] | lang=en
- "components_queryprovider": "QueryProvider.tsx" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, QueryProvider(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L49 | neighbors=[PageShell.tsx, Sidebar.tsx, page.tsx, page.tsx] | lang=en
- "detection_correlator_aware": "_aware()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L209 | neighbors=[correlator.py, ._in_window(), ._min_latency(), Normalise naive datetimes to UTC so com…] | lang=en
- "detection_edr_edrqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L78 | neighbors=[.query_detections(), EDRQueryEngine, .query_detections(), .query_detections()] | lang=en
- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()] | lang=en
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L82 | neighbors=[engine_bridge.py, create_findings_from_facts(), _ensure_importable(), facts (ScanResult dicts) -> detection_e…] | lang=en
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L44 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable()] | lang=en
- "detection_engine_consistency_aggregate": "aggregate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L100 | neighbors=[consistency.py, ConsistencyReport, FindingConsistency, run_findings: one list of Findings per …] | lang=en
- "detection_engine_cvss_base_score": "base_score()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L43 | neighbors=[cvss.py, parse_vector(), _roundup(), Returns the CVSS v3.1 base score (0.0-1…] | lang=en
- "detection_engine_ingest_rationale_1": "ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host" | kind=entity | source=manager/detection_engine/ingest.py:L1 | neighbors=[ingest.py, Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_100": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L100 | neighbors=[ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_60": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L60 | neighbors=[_validate(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_83": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L83 | neighbors=[_extract_aliases(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_matcher_version_in_ranges": "_version_in_ranges()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L44 | neighbors=[matcher.py, match_candidate(), Returns (matched, matched_interval_desc…, _safe_compare()] | lang=en
- "detection_engine_update_snapshot_query_osv": "_query_osv()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L54 | neighbors=[update_snapshot.py, _ssl_context(), All known vulnerabilities OSV has for t…, sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_sync_epss_snapshot": "sync_epss_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L138 | neighbors=[update_snapshot.py, main(), EPSS scores for exactly the CVE IDs thi…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_kev_snapshot": "sync_kev_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L117 | neighbors=[update_snapshot.py, main(), The full CISA Known Exploited Vulnerabi…, _ssl_context()] | lang=en
- "detection_engine_update_snapshot_sync_snapshot": "sync_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L76 | neighbors=[update_snapshot.py, main(), Fetch real OSV records for every produc…, _query_osv()] | lang=en
- "detection_engine_verifier_rationale_1": "verifier.py — Phase 3: the generalized verifier, the anti-false-positive backbon" | kind=entity | source=manager/detection_engine/verifier.py:L1 | neighbors=[verifier.py, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_verifier_rationale_52": "The scanner names behind this finding's evidence refs. A ref looks     like 'fil" | kind=entity | source=manager/detection_engine/verifier.py:L52 | neighbors=[_evidence_scanners(), Finding, FindingState, SourceConfidence] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-032.json

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
