# Node Description Batch 1 of 104

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

- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@298a9d489c8ecbabc70d474cce518d1295aa66cd": "298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validatio…" | kind=Commit | source=git | neighbors=[0510df3 going to build prompt and conne…, adcs.py, asreproast.py, bloodhound.py, findings.py, __init__.py]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@2885afab48ed2cf48cc14de457e9730f9d14b08b": "2885afa Add comprehensive probe testing guide with step-by-step instructions- D…" | kind=Commit | source=git | neighbors=[0557559 scanner: real use-case library,…, route.ts, agent.py, cli.py, engine.py, hw_bind.py]
- "models_enums_findingseverity": "FindingSeverity" | kind=code-symbol | source=manager/backend/app/models/enums.py:L35 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…, ESC1: enrollee supplies subject + clien…, ESC4: a low-privilege principal holds a…]
- "models_enums_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L43 | neighbors=[ADConnectionError, ADError, DependencyMissingError, Shared building blocks for the Active D…, Assemble a Finding-compatible dict.    …, Base class for Active Directory assessm…]
- "models_finding_finding": "Finding" | kind=code-symbol | source=manager/backend/app/models/finding.py:L13 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, engine_bridge.py — run the deterministi…, New raw-facts path: detect CVE findings…]
- "commands_interactive": "interactive.ts" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1 | neighbors=[index.ts, agent.py, auth.ts, apiFetch(), clearSession(), loadSession()]
- "models_engagement_engagement": "Engagement" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L12 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "engine_tool_runners": "tool-runners.ts" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1 | neighbors=[tools.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, scanner.ts, bin(), binName()]
- "detection_engine_models_sourceconfidence": "SourceConfidence" | kind=code-symbol | source=manager/detection_engine/models.py:L24 | neighbors=[correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…, Collapse by finding_id (deterministic: …, Suppress a suspected/potential (inferre…, CPECandidate]
- "models_asset_asset": "Asset" | kind=code-symbol | source=manager/backend/app/models/asset.py:L12 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…]
- "agent_agent": "agent.py" | kind=code-symbol | source=probe/agent/agent.py:L1 | neighbors=[agent.py, AgentDeps, AgentOpts, build_ssl_context(), _check_anti_debug(), check_tool_availability()]
- "detection_engine_models_fact": "Fact" | kind=code-symbol | source=manager/detection_engine/models.py:L44 | neighbors=[AIClient, AINormalizerCache, AnthropicAIClient, FakeAIClient, ai_normalizer.py — Phase 2: AI normaliz…, Test double — a fixed lookup table, no …]
- "detection_engine_cpe_normalizer_cpecandidate": "CPECandidate" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L42 | neighbors=[AIClient, AINormalizerCache, AnthropicAIClient, FakeAIClient, ai_normalizer.py — Phase 2: AI normaliz…, Test double — a fixed lookup table, no …]
- "detection_engine_models_finding": "Finding" | kind=code-symbol | source=manager/detection_engine/models.py:L138 | neighbors=[ConsistencyReport, FindingConsistency, consistency.py — Phase 5: N-run consist…, run_findings: one list of Findings per …, The spec's reporting line, e.g.:     'H…, Wilson score interval for a binomial pr…]
- "models_scan_job_scanjob": "ScanJob" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L12 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, scan_job.py, Base]
- "detection_engine_vuln_db_vulndb": "VulnDB" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L78 | neighbors=[enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…, Returns (tier, human-readable reason). …, matcher.py — does this CPE candidate's …, dpkg_compare, but None instead of a mis…, Returns (matched, matched_interval_desc…]
- "detection_engine_models_asset": "Asset" | kind=code-symbol | source=manager/detection_engine/models.py:L70 | neighbors=[correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…, Collapse by finding_id (deterministic: …, Suppress a suspected/potential (inferre…, IngestResult]
- "detection_engine_models_findingstate": "FindingState" | kind=code-symbol | source=manager/detection_engine/models.py:L119 | neighbors=[correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…, Collapse by finding_id (deterministic: …, Suppress a suspected/potential (inferre…, matcher.py — does this CPE candidate's …]
- "ad_ldap_enum_ldapenumerator": "LDAPEnumerator" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L118 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…, ESC1: enrollee supplies subject + clien…, ESC4: a low-privilege principal holds a…]
- "models_service_service": "Service" | kind=code-symbol | source=manager/backend/app/models/service.py:L10 | neighbors=[AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…, Raised when the Anthropic SDK or API ke…, DiscoveryJobPayload, DiscoveryWorker]
- "tests_test_detection_core_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L56 | neighbors=[test_detection_core.py, .test_dedup_within_run(), .test_multi_run_intermittent(), .test_multi_run_stable(), .test_single_run(), .test_authoritative_tier4()]
- "app_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/page.tsx:L1 | neighbors=[Agent, AGENT_STATUS, AgentRow(), AgentStatus, Dashboard(), GlowCard()]
- "tests_test_probe_core": "test_probe_core.py" | kind=code-symbol | source=probe/tests/test_probe_core.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, engine.py, use_cases.py, scanner_base.py, _asset(), _scan_result()]
- "detection_engine_ingest_ingestresult": "IngestResult" | kind=code-symbol | source=manager/detection_engine/ingest.py:L42 | neighbors=[ingest.py, ingest_file(), ingest_files(), .get_or_create_asset(), .__init__(), Asset]
- "detection_engine_enrichment_db_epssdb": "EpssDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L23 | neighbors=[enrichment_db.py, .get(), .__init__(), load_epss(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "detection_engine_enrichment_db_kevdb": "KevDB" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L14 | neighbors=[enrichment_db.py, .__init__(), .is_kev(), load_kev(), enrichment.py — join CVSS + KEV + EPSS …, Mutates and returns `finding` with cvss…]
- "models_enums_scanjobtype": "ScanJobType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L58 | neighbors=[enums.py, str, ScanJob, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST …]
- "tests_test_probe_core_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L49 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[ActivityItem, ADAssessRequest, Neo4jConfig, AgentRegisterRequest, AgentRegisterResponse, EnqueueJobRequest]
- "lib_ai_engine": "ai-engine.ts" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L1 | neighbors=[route.ts, route.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, route.ts, route.ts]
- "findings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), ComplianceRef, CopyBtn(), COVERAGE_COLOR]
- "tests_test_detection_core": "test_detection_core.py" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, _candidate(), _fact(), _finding(), _mock_epss_db(), _mock_kev_db()]
- "detection_engine_consistency_findingconsistency": "FindingConsistency" | kind=code-symbol | source=manager/detection_engine/consistency.py:L50 | neighbors=[consistency.py, aggregate(), .ci(), .classification(), .rate(), Finding]
- "models_enums_scanjobstatus": "ScanJobStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L69 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, enums.py, str]
- "detection_engine_consistency_consistencyreport": "ConsistencyReport" | kind=code-symbol | source=manager/detection_engine/consistency.py:L86 | neighbors=[consistency.py, aggregate(), .intermittent(), .stable(), Finding, Detection engine test suite — unit test…]
- "detection_engine_verifier_evidencetier": "EvidenceTier" | kind=code-symbol | source=manager/detection_engine/verifier.py:L41 | neighbors=[verifier.py, Finding, FindingState, SourceConfidence, IntEnum, Detection engine test suite — unit test…]
- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, route.ts, route.ts, ask.ts, findings.ts, interactive.ts]
- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, scan.ts, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, scan-modules.ts]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[NucleiExploitRunner, NucleiExploitRunner — CVE PoC validatio…, Run Nuclei CVE PoC template against tar…, Parse nuclei JSONL output for a single …, Run Nuclei CVE PoC templates against a …, Parse template YAML and validate it con…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-000.json

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
