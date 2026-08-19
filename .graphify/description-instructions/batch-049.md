# Node Description Batch 50 of 227

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

- "auth_router_authenticate": "_authenticate()" | kind=code-symbol | source=manager/backend/app/auth/router.py:L58 | neighbors=[router.py, login(), Validates credentials and returns the U…, Validates credentials and returns the U…] | lang=en
- "commands_interactive_banner": "banner()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L104 | neighbors=[interactive.ts, ln(), runInteractive(), wizardScan()] | lang=en
- "commands_interactive_choosenextphase": "chooseNextPhase()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L927 | neighbors=[interactive.ts, choose(), ln(), runIterativeEngagement()] | lang=en
- "commands_interactive_pickmodulesbycategory": "pickModulesByCategory()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L300 | neighbors=[interactive.ts, confirm(), ln(), wizardScan()] | lang=en
- "commands_interactive_runrulebasedvalidation": "runRuleBasedValidation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1355 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow()] | lang=en
- "commands_interactive_wizardstatus": "wizardStatus()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1938 | neighbors=[interactive.ts, mainMenu(), divider(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0510df3efb9374892a4822e5be4b3cdb4d0cdd4f": "0510df3 going to build prompt and connection, architecture almost done" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 298a9d4 trim frontend to 7 core pages; …, a388bb3 script updated, architecture de…] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@a388bb3e7f6e1db096cdb6b54966cdce98a43eed": "a388bb3 script updated, architecture design and integration with adversa repo" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, 0510df3 going to build prompt and conne…, bd7383f scanner fine ..now integrations] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@bd7383fc2cc71d9cb245832d165562e1d2db0a25": "bd7383f scanner fine ..now integrations" | kind=Commit | source=git | neighbors=[agents/greeting-introduction, main, a388bb3 script updated, architecture de…, f5ce592 first commit] | lang=en
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@f5ce59287539c2bdfa5634ab9086c7c75c11bebb": "f5ce592 first commit" | kind=Commit | source=git | neighbors=[8d65c92 first commit, agents/greeting-introduction, main, bd7383f scanner fine ..now integrations] | lang=fr
- "commit:repo:github.com/Rutikm18/Project-Vedha@185e6487d540cf5b1805c4d2a41a6ca0e9bd42c0": "185e648 docs: pending-work inventory (buckets A-G)" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, main, 78d51c5 opsec(scanner): de-sign service…, 2be040c improve(probe/install): portabi…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2be040ca5c7a29aa1dd6caa2bfefb6f305d23693": "2be040c improve(probe/install): portability, supply-chain, ops hardening" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, main, 185e648 docs: pending-work inventory (b…, 9e188b8 fix(probe/install): LOCAL prefl…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@5b980e1cf0c571409a6d765442112df458b0456f": "5b980e1 docs(spec): installer warning + fleet job visibility + engagement host-…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, main, 656e909 feat(ui): polish login page, to…, 9c973dd feat(scanner): tarpit/honeypot …] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9e188b89006db238b7f9a09dd1b17eb4eba7ad87": "9e188b8 fix(probe/install): LOCAL preflight + self-healing venv + daemon/lock g…" | kind=Commit | source=git | neighbors=[22e4f8d chore: update version, feat/complete-pending-work, main, 2be040c improve(probe/install): portabi…] | lang=en
- "components_queryprovider": "QueryProvider.tsx" | kind=code-symbol | source=manager/frontend/components/QueryProvider.tsx:L1 | neighbors=[layout.tsx, d1b4dd3 trim frontend to 7 core pages; …, QueryProvider(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "components_sidebar_sidebar": "Sidebar()" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L53 | neighbors=[PageShell.tsx, Sidebar.tsx, page.tsx, page.tsx] | lang=en
- "components_themeprovider_usetheme": "useTheme()" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L26 | neighbors=[PageShell.tsx, ThemeProvider.tsx, PortalShell.tsx, page.tsx] | lang=en
- "console_primitives_meter": "Meter()" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L86 | neighbors=[Primitives.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx] | lang=en
- "dashboard_liveoverview_liveoverview": "LiveOverview()" | kind=code-symbol | source=manager/frontend/components/dashboard/LiveOverview.tsx:L61 | neighbors=[DashboardGrid.tsx, LiveOverview.tsx, verdict(), page.tsx] | lang=en
- "dashboard_patchcomparisonmatrix_patchcomparisonmatrix": "PatchComparisonMatrix()" | kind=code-symbol | source=manager/frontend/components/dashboard/PatchComparisonMatrix.tsx:L70 | neighbors=[DashboardGrid.tsx, PatchComparisonMatrix.tsx, n(), page.tsx] | lang=en
- "dashboard_posturescorecard_posturescorecard": "PostureScorecard()" | kind=code-symbol | source=manager/frontend/components/dashboard/PostureScorecard.tsx:L105 | neighbors=[DashboardGrid.tsx, PostureScorecard.tsx, usePosture(), page.tsx] | lang=en
- "detection_correlator_aware": "_aware()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L209 | neighbors=[correlator.py, ._in_window(), ._min_latency(), Normalise naive datetimes to UTC so com…] | lang=en
- "detection_edr_edrqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L78 | neighbors=[.query_detections(), EDRQueryEngine, .query_detections(), .query_detections()] | lang=en
- "detection_edr_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L47 | neighbors=[edr.py, .parse_response(), .parse_response(), .parse_response()] | lang=en
- "detection_engine_ai_normalizer_validate_cpe_exists": "validate_cpe_exists()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L169 | neighbors=[ai_normalizer.py, propose_candidates(), True iff the real NVD CPE dictionary ha…, .get()] | lang=en
- "detection_engine_bridge_apply_regression_reopen": "_apply_regression_reopen()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L113 | neighbors=[engine_bridge.py, create_findings_from_facts(), A previously-remediated finding whose i…, A previously-remediated finding whose i…] | lang=en
- "detection_engine_bridge_find_remediated_match": "_find_remediated_match()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L129 | neighbors=[engine_bridge.py, create_findings_from_facts(), A remediated finding with the same (eng…, A remediated finding with the same (eng…] | lang=en
- "detection_engine_bridge_persist_attack_paths": "_persist_attack_paths()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L171 | neighbors=[engine_bridge.py, create_findings_from_facts(), _engagement_device_roles(), Correlate composite attack paths from t…] | lang=en
- "detection_engine_bridge_stamp_verification": "_stamp_verification()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L141 | neighbors=[engine_bridge.py, create_findings_from_facts(), Best-effort: compute + stamp each findi…, Best-effort: compute + stamp each findi…] | lang=en
- "detection_engine_consistency_aggregate": "aggregate()" | kind=code-symbol | source=manager/detection_engine/consistency.py:L100 | neighbors=[consistency.py, ConsistencyReport, FindingConsistency, run_findings: one list of Findings per …] | lang=en
- "detection_engine_cvss_base_score": "base_score()" | kind=code-symbol | source=manager/detection_engine/cvss.py:L43 | neighbors=[cvss.py, parse_vector(), _roundup(), Returns the CVSS v3.1 base score (0.0-1…] | lang=en
- "detection_engine_enrichment_db_load_epss": "load_epss()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L69 | neighbors=[enrichment_db.py, _cache_key(), EpssDB, .get()] | lang=en
- "detection_engine_enrichment_db_load_kev": "load_kev()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L55 | neighbors=[enrichment_db.py, _cache_key(), .get(), KevDB] | lang=en
- "detection_engine_ingest_rationale_1": "ingest.py — stream-read scanner_module JSONL output, validate, assemble per-host" | kind=entity | source=manager/detection_engine/ingest.py:L1 | neighbors=[ingest.py, Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_100": "Stream-read one JSONL file, validating and assembling Assets as it goes.      Pa" | kind=entity | source=manager/detection_engine/ingest.py:L100 | neighbors=[ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_60": "Returns an error reason string if invalid, else None." | kind=entity | source=manager/detection_engine/ingest.py:L60 | neighbors=[_validate(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_ingest_rationale_83": "Real, verified hostname-alias sources in scanner_module's output —     deliberat" | kind=entity | source=manager/detection_engine/ingest.py:L83 | neighbors=[_extract_aliases(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_matcher_version_in_ranges": "_version_in_ranges()" | kind=code-symbol | source=manager/detection_engine/matcher.py:L44 | neighbors=[matcher.py, match_candidate(), Returns (matched, matched_interval_desc…, _safe_compare()] | lang=en
- "detection_engine_update_snapshot_query_osv": "_query_osv()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L54 | neighbors=[update_snapshot.py, _ssl_context(), All known vulnerabilities OSV has for t…, sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_sync_epss_snapshot": "sync_epss_snapshot()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L138 | neighbors=[update_snapshot.py, main(), EPSS scores for exactly the CVE IDs thi…, _ssl_context()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-049.json

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
