# Node Description Batch 1 of 76

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
- "models_enums_findingseverity": "FindingSeverity" | kind=code-symbol | source=manager/backend/app/models/enums.py:L35 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…, ESC1: enrollee supplies subject + clien…, ESC4: a low-privilege principal holds a…]
- "models_enums_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L43 | neighbors=[ADConnectionError, ADError, DependencyMissingError, Shared building blocks for the Active D…, Assemble a Finding-compatible dict.    …, Base class for Active Directory assessm…]
- "commands_interactive": "interactive.ts" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1 | neighbors=[index.ts, agent.py, auth.ts, apiFetch(), clearSession(), loadSession()]
- "engine_tool_runners": "tool-runners.ts" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1 | neighbors=[tools.ts, 298a9d4 trim frontend to 7 core pages; …, scanner.ts, bin(), binName(), collectProcess()]
- "models_finding_finding": "Finding" | kind=code-symbol | source=manager/backend/app/models/finding.py:L13 | neighbors=[engine_bridge.py — run the deterministi…, New raw-facts path: detect CVE findings…, Background entry point (P1: keep detect…, (content_hash, fetched_at) of the pinne…, facts (ScanResult dicts) -> detection_e…, Convert a probe's self-assessed `findin…]
- "models_engagement_engagement": "Engagement" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L12 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_asset_asset": "Asset" | kind=code-symbol | source=manager/backend/app/models/asset.py:L12 | neighbors=[Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…, A still-relevant Finding with the same …, Convert a probe's self-assessed `findin…, DiscoveryJobPayload, DiscoveryWorker]
- "ad_ldap_enum_ldapenumerator": "LDAPEnumerator" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L118 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…, ESC1: enrollee supplies subject + clien…, ESC4: a low-privilege principal holds a…]
- "agent_agent": "agent.py" | kind=code-symbol | source=probe/agent/agent.py:L1 | neighbors=[AgentDeps, AgentOpts, build_ssl_context(), _check_anti_debug(), check_tool_availability(), count_by_severity()]
- "models_scan_job_scanjob": "ScanJob" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L12 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, scan_job.py, Base]
- "models_enums_scanjobtype": "ScanJobType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L58 | neighbors=[enums.py, str, ScanJob, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST …]
- "findings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), ComplianceRef, CopyBtn(), COVERAGE_COLOR]
- "lib_ai_engine": "ai-engine.ts" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L1 | neighbors=[route.ts, route.ts, 298a9d4 trim frontend to 7 core pages; …, route.ts, route.ts, route.ts]
- "app_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/page.tsx:L1 | neighbors=[Agent, AGENT_STATUS, AgentRow(), AgentStatus, Dashboard(), GlowCard()]
- "exploit_msf_client_metasploitrpcclient": "MetasploitRPCClient" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L27 | neighbors=[msf_client.py, ._call(), .connect(), .disconnect(), .get_job_status(), .__init__()]
- "lib_findings_store": "findings-store.ts" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L1 | neighbors=[tools.ts, route.ts, route.ts, ask.ts, findings.ts, interactive.ts]
- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[ADAssessRequest, Neo4jConfig, AgentRegisterRequest, AgentRegisterResponse, EnqueueJobRequest, HeartbeatRequest]
- "engine_scanner": "scanner.ts" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L1 | neighbors=[tools.ts, interactive.ts, scan.ts, 298a9d4 trim frontend to 7 core pages; …, scan-modules.ts, modulesForPorts()]
- "exploit_safety_safetyviolationerror": "SafetyViolationError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L16 | neighbors=[NucleiExploitRunner, NucleiExploitRunner — CVE PoC validatio…, Run Nuclei CVE PoC template against tar…, Parse nuclei JSONL output for a single …, Run Nuclei CVE PoC templates against a …, Parse template YAML and validate it con…]
- "models_service_service": "Service" | kind=code-symbol | source=manager/backend/app/models/service.py:L10 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, GraphBuilder, GraphBuilder — turns engagement assets/…]
- "detection_engine_models_sourceconfidence": "SourceConfidence" | kind=code-symbol | source=manager/detection_engine/models.py:L24 | neighbors=[correlate.py — dedup, authoritative-sup…, The CPE 'product' field — used as the j…, SMBv1 enabled + (credentialed hotfix li…, Collapse by finding_id (deterministic: …, Suppress a suspected/potential (inferre…, CPECandidate]
- "models_enums_scanjobstatus": "ScanJobStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L69 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, enums.py, str]
- "models_enums_assettype": "AssetType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L19 | neighbors=[Convert a probe's self-assessed `findin…, Find the Asset for a probe-reported tar…, A still-relevant Finding with the same …, Convert a probe's self-assessed `findin…, DiscoveryJobPayload, DiscoveryWorker]
- "engine_types": "types.ts" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[agent.py, tools.ts, llm.ts, ask.ts, findings.ts, interactive.ts]
- "pipeline_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), nuclei-parser.ts, countBySeverity(), nucleiMatchToFinding()]
- "cli_index": "index.ts" | kind=code-symbol | source=manager/frontend/cli/index.ts:L1 | neighbors=[program, admin.ts, buildAdminCommand(), ask.ts, buildAskCommand(), doctor.ts]
- "detection_engine_models_fact": "Fact" | kind=code-symbol | source=manager/detection_engine/models.py:L44 | neighbors=[AIClient, AINormalizerCache, AnthropicAIClient, FakeAIClient, ai_normalizer.py — Phase 2: AI normaliz…, Test double — a fixed lookup table, no …]
- "exploit_safety_approvalrequirederror": "ApprovalRequiredError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L28 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_outofscopeerror": "OutOfScopeError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L20 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "detection_engine_cpe_normalizer_cpecandidate": "CPECandidate" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L42 | neighbors=[AIClient, AINormalizerCache, AnthropicAIClient, FakeAIClient, ai_normalizer.py — Phase 2: AI normaliz…, Test double — a fixed lookup table, no …]
- "exploit_safety_blastradiusexceedederror": "BlastRadiusExceededError" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L24 | neighbors=[ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…, Raises OutOfScopeError if target_ip not…, Full exploit execution pipeline with sa…, Returns a unique FQDN for out-of-band D…]
- "models_enums_detectionstatus": "DetectionStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L51 | neighbors=[AttackAction, DetectionCorrelator, DetectionGap, DetectionResultDTO, DetectionCorrelator — matches red-team …, Normalise naive datetimes to UTC so com…]
- "commands_interactive_ln": "ln()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L32 | neighbors=[interactive.ts, banner(), choose(), chooseNextPhase(), divider(), ensureAuthenticated()]
- "lib_graph_store": "graph-store.ts" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L1 | neighbors=[route.ts, route.ts, route.ts, route.ts, 298a9d4 trim frontend to 7 core pages; …, ADJ]
- "ui_output": "output.ts" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L1 | neighbors=[findings.ts, interactive.ts, scan.ts, 298a9d4 trim frontend to 7 core pages; …, types.ts, DiscoveredHost]
- "detection_engine_models_finding": "Finding" | kind=code-symbol | source=manager/detection_engine/models.py:L138 | neighbors=[ConsistencyReport, FindingConsistency, consistency.py — Phase 5: N-run consist…, run_findings: one list of Findings per …, The spec's reporting line, e.g.:     'H…, Wilson score interval for a binomial pr…]
- "tools_installer": "installer.ts" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L1 | neighbors=[tools.ts, 298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, downloadFile(), extract(), getInstalledRecord()]
- "models_base_base": "Base" | kind=code-symbol | source=manager/backend/app/models/base.py:L9 | neighbors=[Agent, AgentStatus, Asset, AttackPath, AttackTimeline, Append-only ledger of every attack acti…]
- "scan_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L1 | neighbors=[0557559 scanner: real use-case library,…, 298a9d4 trim frontend to 7 core pages; …, PageShell.tsx, PageShell(), useToast.ts, useToast()]

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
