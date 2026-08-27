# Node Description Batch 33 of 236

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

- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()]
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()]
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@185e6487d540cf5b1805c4d2a41a6ca0e9bd42c0": "185e648 docs: pending-work inventory (buckets A-G)" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 78d51c5 opsec(scanner): de-sign service…, 2be040c improve(probe/install): portabi…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@21ebc4647fbc8013300844481aacf06393192c11": "21ebc46 feat(detection): unified prioritization engine (risk_score for every fi…" | kind=Commit | source=git | neighbors=[feat/nvd-vuln-detection-and-ingest-hard…, 0236a60 fix(detection): full EPSS catal…, prioritization.py, job_result_service.py, outbox.py, bf61dbc docs: probe run/test guide; git…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2be040ca5c7a29aa1dd6caa2bfefb6f305d23693": "2be040c improve(probe/install): portability, supply-chain, ops hardening" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 185e648 docs: pending-work inventory (b…, 9e188b8 fix(probe/install): LOCAL prefl…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@3565ada02b223c451ee7c0a953852dcddf688973": "3565ada fix(ingest): NUL-safe result submission + network-service hygiene findi…" | kind=Commit | source=git | neighbors=[transport.py, feat/nvd-vuln-detection-and-ingest-hard…, f3bb8db feat(manager): cross-worker WS …, service_vuln.py, job_result_service.py, d0d1931 feat(detection): NVD/CPE vuln f…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5b980e1cf0c571409a6d765442112df458b0456f": "5b980e1 docs(spec): installer warning + fleet job visibility + engagement host-…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 656e909 feat(ui): polish login page, to…, 9c973dd feat(scanner): tarpit/honeypot …]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9e188b89006db238b7f9a09dd1b17eb4eba7ad87": "9e188b8 fix(probe/install): LOCAL preflight + self-healing venv + daemon/lock g…" | kind=Commit | source=git | neighbors=[22e4f8d chore: update version, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, 2be040c improve(probe/install): portabi…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@d0d193118467023761f5f97d55f72b41d37ce287": "d0d1931 feat(detection): NVD/CPE vuln feed for network-service banners" | kind=Commit | source=git | neighbors=[feat/nvd-vuln-detection-and-ingest-hard…, 3565ada fix(ingest): NUL-safe result su…, build_nvd_cpe_snapshot.py, cpe_normalizer.py, vuln_db.py, dbcff7f feat: Update UseCaseCard compon…]
- "customers_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/route.ts:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "detection_active_validation": "active_validation.py" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, 7bd104a feat(active-validation): pure r…, interpret_validation(), should_escalate(), ValidationOutcome, active_validation.py — manager-side dec…]
- "detection_attack_paths_hostsignals": "_HostSignals" | kind=code-symbol | source=manager/backend/app/detection/attack_paths.py:L62 | neighbors=[attack_paths.py, _group(), .finalize(), .__init__(), .observe(), The weaknesses observed on ONE host, di…]
- "detection_correlator_detectionresultdto": "DetectionResultDTO" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L46 | neighbors=[correlator.py, .correlate(), EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus]
- "detection_engine_ai_normalizer_anthropicaiclient": "AnthropicAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L96 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Real implementation, gated behind the a…, CPECandidate, Fact]
- "detection_engine_ai_normalizer_fakeaiclient": "FakeAIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L123 | neighbors=[ai_normalizer.py, .__init__(), .propose_cpe(), Test double — a fixed lookup table, no …, CPECandidate, Fact]
- "detection_engine_ai_normalizer_propose_candidates": "propose_candidates()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L230 | neighbors=[ai_normalizer.py, AINormalizerCache, .get(), .put(), validate_cpe_exists(), The Phase 2 entry point. raw_text is wh…]
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L87 | neighbors=[engine_bridge.py, create_findings_from_facts(), _ensure_importable(), facts (ScanResult dicts) -> detection_e…, facts (ScanResult dicts) -> detection_e…, facts (ScanResult dicts) -> detection_e…]
- "detection_engine_bridge_rationale_1": "engine_bridge.py — run the deterministic detection_engine on a probe's RAW FACTS" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[engine_bridge.py, DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_209": "Background entry point (P1: keep detection OFF the probe-result request     path" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L209 | neighbors=[run_detection_job(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_45": "(content_hash, fetched_at) of the pinned snapshot the engine will use, so     ev" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L45 | neighbors=[_vuln_db_meta(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_rationale_83": "facts (ScanResult dicts) -> detection_engine finding dicts. [] on any     failur" | kind=entity | source=manager/backend/app/detection/engine_bridge.py:L83 | neighbors=[detect_findings_from_facts(), DetectionRun, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "detection_engine_bridge_run_detection_job": "run_detection_job()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L367 | neighbors=[engine_bridge.py, Background entry point (P1: keep detect…, create_findings_from_facts(), Background entry point (P1: keep detect…, Background entry point (P1: keep detect…, Background entry point (P1: keep detect…]
- "detection_engine_bridge_vuln_db_meta": "_vuln_db_meta()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L49 | neighbors=[engine_bridge.py, create_findings_from_facts(), (content_hash, fetched_at) of the pinne…, _ensure_importable(), (content_hash, fetched_at) of the pinne…, (content_hash, fetched_at) of the pinne…]
- "detection_engine_correlate_rationale_1": "correlate.py — dedup, authoritative-suppression, and cross-fact composite correl" | kind=entity | source=manager/detection_engine/correlate.py:L1 | neighbors=[correlate.py, CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_115": "The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp" | kind=entity | source=manager/detection_engine/correlate.py:L115 | neighbors=[_product_from_cpe(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_135": "SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS" | kind=entity | source=manager/detection_engine/correlate.py:L135 | neighbors=[correlate_smb_patch(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_36": "Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the" | kind=entity | source=manager/detection_engine/correlate.py:L36 | neighbors=[dedup_findings(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_correlate_rationale_63": "Suppress a suspected/potential (inferred-source) finding when the     SAME host" | kind=entity | source=manager/detection_engine/correlate.py:L63 | neighbors=[suppress_negated(), CPECandidate, Asset, Finding, FindingState, SourceConfidence]
- "detection_engine_cpe_normalizer_normalize_credentialed_packages": "normalize_credentialed_packages()" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L338 | neighbors=[cpe_normalizer.py, clean_debian_version(), CPECandidate, _parse_package_lines(), ssh_inventory's dpkg_packages/rpm_packa…, ssh_inventory's dpkg_packages/rpm_packa…]
- "detection_engine_cvss": "cvss.py" | kind=code-symbol | source=manager/detection_engine/cvss.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, base_score(), parse_vector(), _roundup(), cvss.py — CVSS v3.1 base score from a v…, 298a9d4 trim frontend to 7 core pages; …]
- "detection_engine_matcher": "matcher.py" | kind=code-symbol | source=manager/detection_engine/matcher.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, match_candidate(), _safe_compare(), _version_in_ranges(), matcher.py — does this CPE candidate's …, 298a9d4 trim frontend to 7 core pages; …]
- "detection_engine_matcher_rationale_1": "matcher.py — does this CPE candidate's version fall inside a vulnerable range, p" | kind=entity | source=manager/detection_engine/matcher.py:L1 | neighbors=[matcher.py, CPECandidate, Finding, FindingState, SourceConfidence, VulnDB]
- "detection_engine_matcher_rationale_34": "dpkg_compare, but None instead of a misleading answer when one side     has an e" | kind=entity | source=manager/detection_engine/matcher.py:L34 | neighbors=[_safe_compare(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB]
- "detection_engine_matcher_rationale_45": "Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A" | kind=entity | source=manager/detection_engine/matcher.py:L45 | neighbors=[_version_in_ranges(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB]
- "detection_engine_matcher_rationale_81": "All Findings this single CPE candidate produces against the snapshot.     Empty" | kind=entity | source=manager/detection_engine/matcher.py:L81 | neighbors=[match_candidate(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB]
- "detection_engine_update_snapshot_main": "main()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L233 | neighbors=[update_snapshot.py, sync_epss_full(), sync_kev_snapshot(), sync_snapshot(), _all_known_cve_ids(), sync_epss_snapshot()]
- "detection_engine_update_snapshot_ssl_context": "_ssl_context()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L37 | neighbors=[update_snapshot.py, _query_osv(), Some macOS python.org installs ship exp…, sync_epss_full(), sync_epss_snapshot(), sync_kev_snapshot()]
- "detection_engine_version_compare_verify_pure_python_matches_dpkg": "verify_pure_python_matches_dpkg()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L243 | neighbors=[version_compare.py, Confirm pure-Python agrees with the rea…, _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), _load_validation_markers(), _save_validation_marker()]
- "detection_engine_vuln_db_content_hash": "_content_hash()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L66 | neighbors=[vuln_db.py, Stable hash of the snapshot's actual vu…, _read_snapshot(), Stable hash of the snapshot's actual vu…, load_snapshot(), Stable hash of the snapshot's actual vu…]

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
