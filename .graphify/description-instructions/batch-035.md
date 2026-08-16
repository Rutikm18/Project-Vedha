# Node Description Batch 36 of 209

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

- "app_version": "version.py" | kind=code-symbol | source=manager/backend/app/version.py:L1 | neighbors=[main.py, get_version(), Single source of truth for the deployed…, b5ffcb0 Refactor Vedha probe installer …, health.py] | lang=en
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "assistant_assistantfab": "AssistantFab.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantFab.tsx:L1 | neighbors=[AssistantFab(), AssistantProvider.tsx, useAssistant(), 1fe16c8 stable but some dead code, need…, 41b692a Update project files] | lang=en
- "assistant_assistanttext": "AssistantText.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AssistantText.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, AssistantText(), plain(), 1fe16c8 stable but some dead code, need…] | lang=en
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "attack_paths_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_jwt_create_refresh_token": "create_refresh_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L67 | neighbors=[jwt.py, _now(), Returns (token, jti) — jti is stored in…, Returns (token, jti) — jti is stored in…, Returns (token, jti) — jti is stored in…] | lang=en
- "auth_pat_build_personal_access_token": "build_personal_access_token()" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L54 | neighbors=[pat.py, hash_pat_token(), new_pat_token(), pat_display_prefix(), validate_pat_scopes()] | lang=en
- "auth_portal_scope_resolve_scope": "resolve_scope()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L47 | neighbors=[portal_scope.py, The safe engagement id to filter by.   …, assert_client(), scoped_engagement(), The safe engagement id to filter by.   …] | lang=en
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
- "commit:repo:github.com/Rutikm18/Project-Vedha@1af3404cd899c56eec3439d379b9f621f044baf9": "1af3404 feat(deploy): probe-free manager stack + port-80 edge ingress" | kind=Commit | source=git | neighbors=[0e22dbf feat(probe): bounded auto-troub…, feat/syn-scanner-osfp-adaptive, main, 65e5684 feat(probe): transparent job lo…, feat/user-portal-reskin-scan-request] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@54503ae3d26d1926e1232f1dc9803e8cfd20faec": "54503ae feat(scanner): SYN path harvests OS-fingerprint intel + RTT-adaptive ti…" | kind=Commit | source=git | neighbors=[feat/syn-scanner-osfp-adaptive, syn_scanner.py, syn_scanner.py, test_syn_scanner.py, c52feb4 feat(portal): reskin User Porta…] | lang=en
- "customer_access_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/customer-access/page.tsx:L1 | neighbors=[22701ea Add tests for scanner parity an…, ca(), ClientUser, CustomerAccessPage(), ScanReq] | lang=en
- "dashboard_slastatus_slarowview": "SlaRowView()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L122 | neighbors=[SlaStatus.tsx, deadlineTitle(), elapsedPct(), timeLabel(), pct()] | lang=en
- "detection_attack_paths_group": "_group()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L130 | neighbors=[attack_paths.py, attack_path_findings(), _HostSignals, .finalize(), .observe()] | lang=en
- "detection_correlator_detectioncorrelator_correlate": ".correlate()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L82 | neighbors=[DetectionCorrelator, ._host_for(), ._in_window(), ._min_latency(), DetectionResultDTO] | lang=en
- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
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
- "detection_engine_version_compare_dpkg_compare_pure_python": "_dpkg_compare_pure_python()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L161 | neighbors=[version_compare.py, dpkg_compare(), _compare_part(), _split_dpkg_version(), verify_pure_python_matches_dpkg()] | lang=en
- "detection_engine_version_compare_dpkg_compare_via_binary": "_dpkg_compare_via_binary()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L36 | neighbors=[version_compare.py, Real dpkg --compare-versions. None (not…, verify_pure_python_matches_dpkg(), dpkg_compare(), Real dpkg --compare-versions. None (not…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-035.json

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
