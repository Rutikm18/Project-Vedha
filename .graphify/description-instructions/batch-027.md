# Node Description Batch 28 of 144

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@3c7740e5aee15e561362096ff219155ee7220b17": "3c7740e feat(lifecycle): pure manual-reopen helper" | kind=Commit | source=git | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, feat/coverage-gated-auto-resolution, 85e4537 feat(risk-rank): expose risk_ra…, resolution.py, test_manual_reopen.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@6b6acb87b50e17f444fd6433cdaaf57cca5c2918": "6b6acb8 fix: update AWS compose command and set default MANAGER_PUBLIC_URL in d…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, main, worktree-fleet-already-downloaded-cmd, 2a36f8a fix: update docker compose comm…, d7329cf feat: enhance AWS deployment wi…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@72f68af6099a8d2994b17533d41b44a3d1462134": "72f68af feat(verification): expose verification verdict + needs_review on findi…" | kind=Commit | source=git | neighbors=[2fcec73 feat(verification): stamp verdi…, feat/coverage-gated-auto-resolution, 02b6341 feat(active-validation): pure e…, finding.py, test_finding_verification_api.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@7bd104a4484e9f6a90aad27a805339e333f13edf": "7bd104a feat(active-validation): pure result interpretation" | kind=Commit | source=git | neighbors=[02b6341 feat(active-validation): pure e…, feat/coverage-gated-auto-resolution, 58c2d10 feat(active-validation): Valida…, active_validation.py, test_active_validation_interpret.py] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@85e45373dae6a51a7abbd155431cc14324239f15": "85e4537 feat(risk-rank): expose risk_rank on findings API; add P2/P3/P4 plans" | kind=Commit | source=git | neighbors=[3c7740e feat(lifecycle): pure manual-re…, feat/coverage-gated-auto-resolution, 3c277ba feat(lifecycle): add POST /find…, finding.py, test_finding_risk_rank_api.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@879cdfa25f56102c23df1efdc671934f88d1b793": "879cdfa docs: probe fleet automation design spec (Phase 0 detailed)" | kind=Commit | source=git | neighbors=[41b692a Update project files, feat/coverage-gated-auto-resolution, main, worktree-fleet-already-downloaded-cmd, f3c3591 docs: Phase 0 queue-control imp…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8cf23c236eb3cc74c9a7c7c156243658165f54e3": "8cf23c2 feat(resolution): wire coverage ledger + auto-resolution into detection…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, 937737b feat(resolution): reopen + flag…, engine_bridge.py, test_engine_bridge_resolution.py, bd409f5 feat(resolution): async applier…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9347a9a16f87a98cc882c39ad050f50544b65e0b": "9347a9a feat(posture): surface posture scorecard + patch matrix on dashboard" | kind=Commit | source=git | neighbors=[page.tsx, feat/coverage-gated-auto-resolution, main, a079178 fix(posture): full-width postur…, d2eb44c feat(posture): add dashboard Pa…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@937737b010d12e40761c6d3593787c0bd0f87d6b": "937737b feat(resolution): reopen + flag regressions on the original finding row" | kind=Commit | source=git | neighbors=[8cf23c2 feat(resolution): wire coverage…, feat/coverage-gated-auto-resolution, 0fbec7d feat(verification): add finding…, engine_bridge.py, test_engine_bridge_regression.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9a36729c7f6547ad20b1c35fee4ab54d4d603e9d": "9a36729 feat(resolution): coverage builder from completed-scanner facts" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, cbf5d6c feat(resolution): pure decision…, resolution.py, test_resolution_coverage.py, ddb51f2 feat(resolution): add finding r…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0791783d160c85c688ea511dc20396a7ac4e2e2": "a079178 fix(posture): full-width posture section; avoid blank grid column on de…" | kind=Commit | source=git | neighbors=[9347a9a feat(posture): surface posture …, page.tsx, feat/coverage-gated-auto-resolution, main, 0f0097b feat(posture): mirror posture s…] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@aa560a0292202728647e1f6cde4e0ca942782cd6": "aa560a0 feat(posture): add dashboard PostureScorecard component" | kind=Commit | source=git | neighbors=[2cddd52 fix(posture): tenant-scope run …, feat/coverage-gated-auto-resolution, main, d2eb44c feat(posture): add dashboard Pa…, PostureScorecard.tsx] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd409f5724ece8d940d48f06f98b9f6188970117": "bd409f5 feat(resolution): async applier over engine-managed open findings" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, 8cf23c2 feat(resolution): wire coverage…, resolution.py, test_resolution_apply.py, cbf5d6c feat(resolution): pure decision…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c02c4652680a709056c4a8e342699c00e80454dc": "c02c465 feat(verification): optional LangGraph orchestration skin" | kind=Commit | source=git | neighbors=[verification_graph.py, feat/coverage-gated-auto-resolution, 2fcec73 feat(verification): stamp verdi…, test_verification_graph.py, de2d1c9 feat(verification): optional fa…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ca41cbf25bddbb70f2808dcfbb236405c24bfc69": "ca41cbf docs: pre-auth probe enrollment token design spec" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, main, worktree-fleet-already-downloaded-cmd, 81c81cb feat: implement outbox reclaim …, f1da96f fix: update environment variabl…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@caf1e5d0a9e53f79a5c9e541a083b332aa127fdd": "caf1e5d feat(verification): deterministic passive verdict core" | kind=Commit | source=git | neighbors=[0fbec7d feat(verification): add finding…, feat/coverage-gated-auto-resolution, de2d1c9 feat(verification): optional fa…, verification.py, test_verification_core.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@cbf5d6cb96915e7c031de705eb116568a081940b": "cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db gu…" | kind=Commit | source=git | neighbors=[9a36729 feat(resolution): coverage buil…, feat/coverage-gated-auto-resolution, bd409f5 feat(resolution): async applier…, resolution.py, test_resolution_decision.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d2eb44c3d2c1f5ac6a3398dc1bf865c46447a9a8": "d2eb44c feat(posture): add dashboard PatchComparisonMatrix component" | kind=Commit | source=git | neighbors=[aa560a0 feat(posture): add dashboard Po…, feat/coverage-gated-auto-resolution, main, 9347a9a feat(posture): surface posture …, PatchComparisonMatrix.tsx] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@d7329cfe261cfa5fd29d0892344b94340cbe0b77": "d7329cf feat: enhance AWS deployment with new environment variables and scripts…" | kind=Commit | source=git | neighbors=[b5ffcb0 Refactor Vedha probe installer …, feat/coverage-gated-auto-resolution, main, worktree-fleet-already-downloaded-cmd, 6b6acb8 fix: update AWS compose command…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de2d1c9825984fa315f761df4bb2da6139d7ff36": "de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage" | kind=Commit | source=git | neighbors=[caf1e5d feat(verification): determinist…, feat/coverage-gated-auto-resolution, c02c465 feat(verification): optional La…, verification.py, test_verification_llm.py] | lang=nl
- "commit:repo:github.com/Rutikm18/Project-Vedha@f1da96f64e70aef9d0275a6cdcdbf89b7334e948": "f1da96f fix: update environment variables and resource limits in docker-compose…" | kind=Commit | source=git | neighbors=[2a36f8a fix: update docker compose comm…, feat/coverage-gated-auto-resolution, main, worktree-fleet-already-downloaded-cmd, ca41cbf docs: pre-auth probe enrollment…] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f3c359163f16baf103a46a5170e40a9e95edda9d": "f3c3591 docs: Phase 0 queue-control implementation plan (8 TDD tasks)" | kind=Commit | source=git | neighbors=[879cdfa docs: probe fleet automation de…, feat/coverage-gated-auto-resolution, main, worktree-fleet-already-downloaded-cmd, c76b428 backend and login page error ha…] | lang=en
- "dashboard_slastatus_slarowview": "SlaRowView()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L122 | neighbors=[SlaStatus.tsx, deadlineTitle(), elapsedPct(), timeLabel(), pct()] | lang=en
- "detection_correlator_detectioncorrelator_correlate": ".correlate()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L82 | neighbors=[DetectionCorrelator, ._host_for(), ._in_window(), ._min_latency(), DetectionResultDTO] | lang=en
- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L85 | neighbors=[engine_bridge.py, create_findings_from_facts(), _ensure_importable(), facts (ScanResult dicts) -> detection_e…, facts (ScanResult dicts) -> detection_e…] | lang=en
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L291 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts(), Background entry point (P1: keep detect…, Background entry point (P1: keep detect…] | lang=en
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L47 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable(), (content_hash, fetched_at) of the pinne…] | lang=en
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L315 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…] | lang=en
- "detection_engine_enrichment": "enrichment.py" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_enrichment_db_epssdb_get": ".get()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[EpssDB, load_epss(), load_kev(), {'epss': float, 'percentile': float} or…, {'epss': float, 'percentile': float} or…] | lang=en
- "detection_engine_enrichment_rationale_1": "enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier." | kind=entity | source=manager/detection_engine/enrichment.py:L1 | neighbors=[enrichment.py, EpssDB, KevDB, Finding, VulnDB] | lang=pt
- "detection_engine_enrichment_rationale_33": "Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr" | kind=entity | source=manager/detection_engine/enrichment.py:L33 | neighbors=[enrich_finding(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_enrichment_rationale_53": "Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li" | kind=entity | source=manager/detection_engine/enrichment.py:L53 | neighbors=[_compute_priority(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_ingest_quarantinedline": "QuarantinedLine" | kind=code-symbol | source=manager/detection_engine/ingest.py:L35 | neighbors=[ingest.py, ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_pipeline": "pipeline.py" | kind=code-symbol | source=manager/detection_engine/pipeline.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ab_evaluate(), run_pipeline(), pipeline.py — Phase 1 + Phase 2 end to …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_update_snapshot_main": "main()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L184 | neighbors=[update_snapshot.py, _all_known_cve_ids(), sync_epss_snapshot(), sync_kev_snapshot(), sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_ssl_context": "_ssl_context()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L37 | neighbors=[update_snapshot.py, _query_osv(), Some macOS python.org installs ship exp…, sync_epss_snapshot(), sync_kev_snapshot()] | lang=en
- "detection_engine_version_compare_dpkg_compare": "dpkg_compare()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L172 | neighbors=[version_compare.py, _dpkg_compare_pure_python(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…, _dpkg_compare_via_binary(), -1 if a<b, 0 if a==b, 1 if a>b, per Deb…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-027.json

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
