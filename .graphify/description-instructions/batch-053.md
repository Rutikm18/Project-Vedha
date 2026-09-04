# Node Description Batch 54 of 332

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

- "auth_startup_check_bcrypt": "_check_bcrypt()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L145 | neighbors=[startup.py, CheckResult, Verify the bcrypt library can round-tri…, run_startup_diagnostics(), Verify the bcrypt library can round-tri…] | lang=en
- "auth_startup_check_tenant": "_check_tenant()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L195 | neighbors=[startup.py, CheckResult, Verify the default tenant is active., run_startup_diagnostics(), Verify the default tenant is active.] | lang=en
- "auth_startup_diagnosticsreport": "DiagnosticsReport" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L65 | neighbors=[startup.py, .all_ok(), .as_dict(), .has_fatal(), run_startup_diagnostics()] | lang=en
- "auth_startup_startupaborterror": "StartupAbortError" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L90 | neighbors=[startup.py, Raised when one or more fatal checks fa…, run_startup_diagnostics(), RuntimeError, Raised when one or more fatal checks fa…] | lang=en
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#agents/greeting-introduction": "agents/greeting-introduction" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 8d65c92 first commit, a388bb3 script updated, architecture de…, bd7383f scanner fine ..now integrations, f5ce592 first commit] | lang=en
- "chokepoints_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/chokepoints/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "cli_auth_serverurl": "serverUrl()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L42 | neighbors=[auth.ts, apiFetch(), doctor.ts, interactive.ts, login.ts] | lang=en
- "commands_interactive_runinteractive": "runInteractive()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2102 | neighbors=[index.ts, interactive.ts, banner(), ensureAuthenticated(), mainMenu()] | lang=en
- "commands_interactive_runphaseexploitation": "runPhaseExploitation()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1070 | neighbors=[interactive.ts, runIterativeEngagement(), choose(), confirm(), ln()] | lang=en
- "commands_interactive_runphaseportscan": "runPhasePortScan()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1028 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphaseservicedetect": "runPhaseServiceDetect()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1037 | neighbors=[interactive.ts, runIterativeEngagement(), mergeHosts(), pickHostSubset(), runPhaseWithTools()] | lang=en
- "commands_interactive_runphasevulnassess": "runPhaseVulnAssess()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1051 | neighbors=[interactive.ts, runIterativeEngagement(), confirm(), ln(), runPhaseWithTools()] | lang=en
- "commands_interactive_runvulnassessmentflow": "runVulnAssessmentFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1184 | neighbors=[interactive.ts, confirm(), ln(), runValidationFlow(), wizardScan()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@83d2039c69cb442be6b6efdfdea7459270fb4598": "83d2039 docs: add prompt output documentation and bump version to 1.0.121" | kind=Commit | source=git | neighbors=[3c9062a refactor: Update dashboard comp…, addcapabilities-fable, main, ui-ux-backend-updates0109, 7d8d3f3 merge: resolve conflicts with o…] | lang=en
- "cve_ingest_ingest_all": "ingest_all()" | kind=code-symbol | source=probe/cve/ingest.py:L234 | neighbors=[ingest.py, ingest_epss(), ingest_kev(), ingest_nvd(), Refresh every enabled feed. KEV/EPSS fi…] | lang=en
- "cve_online_enrich_findings": "enrich_findings()" | kind=code-symbol | source=probe/cve/online.py:L128 | neighbors=[online.py, _apply(), lookup_nvd(), lookup_vulners(), Enrich CVE findings in place from live …] | lang=en
- "cve_version": "version.py" | kind=code-symbol | source=probe/cve/version.py:L1 | neighbors=[6e2818f Add support for additional serv…, compare(), in_range(), parse_version(), version.py — loose version comparison f…] | lang=en
- "dashboard_slastatus_slarowview": "SlaRowView()" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaStatus.tsx:L131 | neighbors=[SlaStatus.tsx, deadlineTitle(), elapsedPct(), timeLabel(), pct()] | lang=en
- "detection_attack_paths_group": "_group()" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L130 | neighbors=[attack_paths.py, attack_path_findings(), _HostSignals, .finalize(), .observe()] | lang=en
- "detection_correlator_aware": "_aware()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L237 | neighbors=[correlator.py, ._in_window(), ._min_latency(), Normalise naive datetimes to UTC so com…, Normalise naive datetimes to UTC so com…] | lang=en
- "detection_correlator_detectioncorrelator_correlate": ".correlate()" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L102 | neighbors=[DetectionCorrelator, ._host_for(), ._in_window(), ._min_latency(), DetectionResultDTO] | lang=en
- "detection_correlator_rationale_1": "DetectionCorrelator — matches red-team attack actions against blue-team SIEM ale" | kind=entity | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_correlator_rationale_210": "Normalise naive datetimes to UTC so comparisons never raise." | kind=entity | source=manager/backend/app/detection/correlator.py:L210 | neighbors=[_aware(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus] | lang=en
- "detection_engine_bridge_persist_attack_paths": "_persist_attack_paths()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L417 | neighbors=[engine_bridge.py, create_findings_from_facts(), _engagement_device_roles(), Correlate composite attack paths from t…, Correlate composite attack paths from t…] | lang=en
- "detection_engine_bridge_stamp_verification": "_stamp_verification()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L387 | neighbors=[engine_bridge.py, create_findings_from_facts(), Best-effort: compute + stamp each findi…, Best-effort: compute + stamp each findi…, Best-effort: compute + stamp each findi…] | lang=en
- "detection_engine_build_nvd_cpe_snapshot": "build_nvd_cpe_snapshot.py" | kind=code-symbol | source=manager/detection_engine/build_nvd_cpe_snapshot.py:L1 | neighbors=[d0d1931 feat(detection): NVD/CPE vuln f…, _content_hash(), main(), _rec(), build_nvd_cpe_snapshot.py — generate th…] | lang=en
- "detection_engine_correlate_product_from_cpe": "_product_from_cpe()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L157 | neighbors=[correlate.py, The CPE 'product' field — used as the j…, suppress_negated_with_audit(), The CPE 'product' field — used as the j…, suppress_negated()] | lang=en
- "detection_engine_correlate_suppress_negated": "suppress_negated()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L80 | neighbors=[correlate.py, Suppress a suspected/potential (inferre…, suppress_negated_with_audit(), Suppress a suspected/potential (inferre…, _product_from_cpe()] | lang=en
- "detection_engine_correlate_suppress_negated_with_audit": "suppress_negated_with_audit()" | kind=code-symbol | source=manager/detection_engine/correlate.py:L101 | neighbors=[correlate.py, Apply authoritative-version suppression…, suppress_negated(), _product_from_cpe(), SuppressionRecord] | lang=en
- "detection_engine_cpe_normalizer_normalize_banner": "normalize_banner()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L250 | neighbors=[cpe_normalizer.py, CPECandidate, service_banner.py's parsed product/vers…, service_banner.py's parsed product/vers…, service_banner.py's first_line/banner t…] | lang=en
- "detection_engine_cpe_normalizer_normalize_db": "normalize_db()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L313 | neighbors=[cpe_normalizer.py, CPECandidate, db_scanner.py's real-protocol-handshake…, db_scanner.py's real-protocol-handshake…, db_scanner.py's real-protocol-handshake…] | lang=en
- "detection_engine_cpe_normalizer_normalize_web": "normalize_web()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L285 | neighbors=[cpe_normalizer.py, CPECandidate, web_scanner.py's Server header + tech_h…, web_scanner.py's Server header + tech_h…, web_scanner.py's Server header + tech_h…] | lang=en
- "detection_engine_cpe_normalizer_parse_package_lines": "_parse_package_lines()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L355 | neighbors=[cpe_normalizer.py, normalize_credentialed_packages(), Yields (package_name, raw_version, upst…, Yields (package_name, raw_version, upst…, Yields (package_name, raw_version, upst…] | lang=en
- "detection_engine_enrichment": "enrichment.py" | kind=code-symbol | source=manager/detection_engine/enrichment.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _compute_priority(), enrich_finding(), enrichment.py — join CVSS + KEV + EPSS …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_enrichment_db_epssdb_get": ".get()" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L29 | neighbors=[EpssDB, load_epss(), load_kev(), {'epss': float, 'percentile': float} or…, {'epss': float, 'percentile': float} or…] | lang=en
- "detection_engine_enrichment_rationale_1": "enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier." | kind=entity | source=manager/detection_engine/enrichment.py:L1 | neighbors=[enrichment.py, EpssDB, KevDB, Finding, VulnDB] | lang=pt
- "detection_engine_enrichment_rationale_33": "Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr" | kind=entity | source=manager/detection_engine/enrichment.py:L33 | neighbors=[enrich_finding(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_enrichment_rationale_53": "Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li" | kind=entity | source=manager/detection_engine/enrichment.py:L53 | neighbors=[_compute_priority(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_exploitability_assess": "assess()" | kind=code-symbol | source=manager/detection_engine/exploitability.py:L130 | neighbors=[exploitability.py, apply_to_findings(), kev_links_for(), _tier(), Exploitability evidence for one posture…] | lang=en
- "detection_engine_ingest_quarantinedline": "QuarantinedLine" | kind=code-symbol | source=manager/detection_engine/ingest.py:L42 | neighbors=[ingest.py, ingest_file(), Asset, Fact, SourceConfidence] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-053.json

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
