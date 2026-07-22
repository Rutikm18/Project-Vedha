# Node Description Batch 40 of 76

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ExploitResult]
- "models_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/models/finding.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Finding]
- "models_llm_output": "llm_output.py" | kind=code-symbol | source=manager/backend/app/models/llm_output.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, LLMOutput]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ScanJob]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ScanResult]
- "models_service": "service.py" | kind=code-symbol | source=manager/backend/app/models/service.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Service]
- "models_tenant": "tenant.py" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Tenant]
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, User]
- "naabu_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/naabu/route.ts:L38 | neighbors=[route.ts, validateTargets()]
- "naabu_route_validatetargets": "validateTargets()" | kind=code-symbol | source=manager/frontend/app/api/scan/naabu/route.ts:L9 | neighbors=[route.ts, POST()]
- "native_dir_bust_loadwordlist": "loadWordlist()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L97 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dir_bust_probe": "probe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L71 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dns_recon_attemptzonetransfer": "attemptZoneTransfer()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L96 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_dns_recon_nativeptrsweep": "nativePtrSweep()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L147 | neighbors=[tool-runners.ts, dns-recon.ts]
- "native_dns_recon_safe": "safe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L49 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_http_probe_nativehttpprobe": "nativeHttpProbe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L248 | neighbors=[tool-runners.ts, http-probe.ts]
- "native_port_scan_groupresults": "groupResults()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L261 | neighbors=[tool-runners.ts, port-scan.ts]
- "native_port_scan_resolveports": "resolvePorts()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L131 | neighbors=[port-scan.ts, nativePortScan()]
- "native_tls_info_nativetlsinfo": "nativeTlsInfo()" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L38 | neighbors=[tool-runners.ts, tls-info.ts]
- "netexec_route_parsenxcoutput": "parseNxcOutput()" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L22 | neighbors=[route.ts, POST()]
- "netexec_route_runnxc": "runNxc()" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L33 | neighbors=[route.ts, POST()]
- "nmap_route_parsenmapxml": "parseNmapXml()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L89 | neighbors=[route.ts, route.ts]
- "nmap_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L215 | neighbors=[route.ts, validateTarget()]
- "nmap_route_validatetarget": "validateTarget()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L62 | neighbors=[route.ts, POST()]
- "pipeline_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L549 | neighbors=[route.ts, runPipelineBackground()]
- "pipeline_route_runeyewitnessstage": "runEyewitnessStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L426 | neighbors=[route.ts, runPipelineBackground()]
- "pipeline_route_runnucleistage": "runNucleiStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L247 | neighbors=[route.ts, runPipelineBackground()]
- "pipeline_route_runtestsslstage": "runTestsslStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L349 | neighbors=[route.ts, runPipelineBackground()]
- "probe_pipeline_collector_write": ".write()" | kind=code-symbol | source=probe/pipeline.py:L126 | neighbors=[_Collector, _run_active()]
- "probe_run_scan_main": "main()" | kind=code-symbol | source=probe/run_scan.py:L135 | neighbors=[run_scan.py, _orchestrate()]
- "probe_run_scan_orchestrate": "_orchestrate()" | kind=code-symbol | source=probe/run_scan.py:L62 | neighbors=[run_scan.py, main()]
- "prompts_report": "report.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ai-engine.ts]
- "prompts_triage": "triage.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/triage.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ai-engine.ts]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agents_get_job_status": "get_job_status()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L458 | neighbors=[agents.py, Lets the frontend poll a specific job's…]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L356 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L264 | neighbors=[agents.py, Returns the finite library of scan use-…]
- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L277 | neighbors=[agents.py, AgentRegisterResponse]
- "routers_agents_resolve_scan_type": "_resolve_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L57 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_submit_job_result": "submit_job_result()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L619 | neighbors=[agents.py, _agent_ownership_check()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-039.json

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
