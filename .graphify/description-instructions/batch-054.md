# Node Description Batch 55 of 76

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

- "engagements_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L56 | neighbors=[page.tsx] | lang=en
- "engagements_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L48 | neighbors=[page.tsx] | lang=en
- "engagements_page_steps": "STEPS" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "engagements_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L13 | neighbors=[route.ts] | lang=en
- "engagements_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L30 | neighbors=[route.ts] | lang=en
- "engine_scan_modules_defaultmodules": "defaultModules()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L345 | neighbors=[scan-modules.ts] | lang=en
- "engine_scan_modules_depthdefaults": "depthDefaults()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L385 | neighbors=[scan-modules.ts] | lang=en
- "engine_scan_modules_modulebyid": "moduleById()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L329 | neighbors=[scan-modules.ts] | lang=en
- "engine_scan_modules_modulecategory": "ModuleCategory" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L19 | neighbors=[scan-modules.ts] | lang=en
- "engine_scan_modules_moduleinput": "ModuleInput" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L27 | neighbors=[scan-modules.ts] | lang=en
- "engine_scan_modules_moduleoutput": "ModuleOutput" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L28 | neighbors=[scan-modules.ts] | lang=en
- "engine_scan_modules_scanmodule": "ScanModule" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L30 | neighbors=[scan-modules.ts] | lang=en
- "engine_tool_runners_httpxline": "HttpxLine" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L661 | neighbors=[tool-runners.ts] | lang=en
- "engine_tool_runners_naabu_rate": "NAABU_RATE" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L24 | neighbors=[tool-runners.ts] | lang=en
- "engine_tool_runners_nmap_timing": "NMAP_TIMING" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L25 | neighbors=[tool-runners.ts] | lang=en
- "engine_tool_runners_nserunspec": "NseRunSpec" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L983 | neighbors=[tool-runners.ts] | lang=en
- "engine_tool_runners_nsesection": "nseSection()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1019 | neighbors=[tool-runners.ts] | lang=en
- "engine_tool_runners_processresult": "ProcessResult" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L96 | neighbors=[tool-runners.ts] | lang=en
- "engine_tool_runners_rundnsrecon": "runDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L562 | neighbors=[tool-runners.ts] | lang=en
- "engine_types_agentjob": "AgentJob" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L132 | neighbors=[types.ts] | lang=en
- "engine_types_agentjobresult": "AgentJobResult" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L145 | neighbors=[types.ts] | lang=en
- "engine_types_discoverydepth": "DiscoveryDepth" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L34 | neighbors=[types.ts] | lang=en
- "engine_types_scanprofile": "ScanProfile" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L3 | neighbors=[types.ts] | lang=en
- "exploit_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/exploit/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …] | lang=en
- "exploit_msf_client_metasploitrpcclient_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L30 | neighbors=[MetasploitRPCClient] | lang=en
- "exploit_msf_client_rationale_1": "MetasploitRPCClient — async client for msfrpcd.  Protocol: MessagePack RPC over" | kind=entity | source=manager/backend/app/exploit/msf_client.py:L1 | neighbors=[msf_client.py] | lang=en
- "exploit_msf_client_rationale_103": "Returns {status, output, uuid}." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L103 | neighbors=[.get_job_status()] | lang=en
- "exploit_msf_client_rationale_119": "Returns True if job was successfully killed." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L119 | neighbors=[.kill_job()] | lang=en
- "exploit_msf_client_rationale_138": "Poll until job completes or max_wait exceeded." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L138 | neighbors=[.wait_for_job()] | lang=en
- "exploit_msf_client_rationale_152": "Authenticated RPC call — prepends token." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L152 | neighbors=[._call()] | lang=en
- "exploit_msf_client_rationale_28": "Async Metasploit RPC client using msgpack-over-HTTPS." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L28 | neighbors=[MetasploitRPCClient] | lang=en
- "exploit_msf_client_rationale_39": "Authenticate with msfrpcd and store the session token." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L39 | neighbors=[.connect()] | lang=en
- "exploit_msf_client_rationale_66": "module_type: exploit | auxiliary | payload | post | encoder         Returns list" | kind=entity | source=manager/backend/app/exploit/msf_client.py:L66 | neighbors=[.list_modules()] | lang=en
- "exploit_msf_client_rationale_89": "Execute a Metasploit module.         Returns job_id as string." | kind=entity | source=manager/backend/app/exploit/msf_client.py:L89 | neighbors=[.run_module()] | lang=pt
- "exploit_orchestrator_exploitorchestrator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L56 | neighbors=[ExploitOrchestrator] | lang=en
- "exploit_safety_approvalrequirederror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L30 | neighbors=[ApprovalRequiredError] | lang=en
- "exploit_safety_rationale_1": "Safety constants, exceptions, and validators for the exploitation engine.  All s" | kind=entity | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[safety.py] | lang=en
- "exploit_safety_rationale_17": "Raised when a requested payload or module is not on the allowlist." | kind=entity | source=manager/backend/app/exploit/safety.py:L17 | neighbors=[SafetyViolationError] | lang=en
- "exploit_safety_rationale_175": "Raises SafetyViolationError if payload is not on allowlist     or violates per-p" | kind=entity | source=manager/backend/app/exploit/safety.py:L175 | neighbors=[validate_payload()] | lang=en
- "exploit_safety_rationale_203": "Raises SafetyViolationError if module is on the block list." | kind=entity | source=manager/backend/app/exploit/safety.py:L203 | neighbors=[validate_module()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-054.json

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
