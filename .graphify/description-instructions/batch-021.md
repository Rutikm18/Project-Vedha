# Node Description Batch 22 of 227

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@37fa611652538968dbf827eaf98cdcab59c052b2": "37fa611 harden(scanner): XML-entity guard + list-form argv (CWE-611/78/88)" | kind=Commit | source=git | neighbors=[2c53ae9 evasion(scanner): randomized sc…, feat/complete-pending-work, main, 2de251b feat(scanner): ICMP timestamp f…, host_discovery.py, nmap_wrapper.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@9c973dd02e4777bcd7cebae84b6c80fd96fa001f": "9c973dd feat(scanner): tarpit/honeypot detection in port-scan summary (C5)" | kind=Commit | source=git | neighbors=[2de251b feat(scanner): ICMP timestamp f…, feat/complete-pending-work, main, 5b980e1 docs(spec): installer warning +…, port_scanner.py, scanner_base.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@aedddfae1bea375d5864f92e26f2ceb7f0bf8065": "aedddfa feat(settings): editable SLA policy windows wired to backend (item 4 UI)" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, testing/all-features, 027f4e4 feat(integrations): per-tenant …] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@dec1e7cfa829a295630af88da9f11a5f2e8175d4": "dec1e7c fix(scanner): resolve() family fallback for dual-stack hosts (task A9)" | kind=Commit | source=git | neighbors=[78d51c5 opsec(scanner): de-sign service…, feat/complete-pending-work, main, 2c53ae9 evasion(scanner): randomized sc…, os_fingerprint.py, scanner_base.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@eff17d69ed457a0f00a6cec466932ff1357fb74f": "eff17d6 feat(probe): one-click approve endpoint — no code, auto name/caps/scope…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, testing/all-features, e3958e7 feat(customers): reveal + copy …] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@f8ff2296e5ec2c593a6bed4ab40633d8a857d40f": "f8ff229 feat(ui): remove decorative session clock from both dashboards (item 6)" | kind=Commit | source=git | neighbors=[ecbb4ad feat(agent): rules-of-engagemen…, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main, testing/all-features] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@fc7afc36732bf000de12e42189e63124bd643652": "fc7afc3 chore(graphify): refresh knowledge graph for remediation subsystem" | kind=Commit | source=git | neighbors=[5c6aa54 feat(portal-ui): portal shell/p…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/remediation-ai-plans, integration/all-branches] | lang=en
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
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, _dec(), main(), match_service()] | lang=en
- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Enum, Agent] | lang=en
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, toUiAgent(), backend(), withBackend(), GET, 2885afa Add comprehensive probe testing…] | lang=en
- "reopen_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L1 | neighbors=[8ebc053 feat(risk-rank-ui): surface ver…, adapters.ts, toUiFinding(), backend.ts, backend(), BackendError] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), isEmailAllowed(), POST(), 2885afa Add comprehensive probe testing…] | lang=en
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ad.py, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[_run_ad_assessment_and_save(), ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L547 | neighbors=[agents.py, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…] | lang=en
- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[_scope_is_reachable(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[_job_reachability_scope(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[_required_scan_type(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()] | lang=en
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L270 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
