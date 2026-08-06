# Node Description Batch 91 of 134

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

- "engine_types_agentjobresult": "AgentJobResult" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L145 | neighbors=[types.ts] | lang=en
- "engine_types_discoverydepth": "DiscoveryDepth" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L34 | neighbors=[types.ts] | lang=en
- "engine_types_scanprofile": "ScanProfile" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L3 | neighbors=[types.ts] | lang=en
- "enrollment_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/route.ts:L5 | neighbors=[route.ts] | lang=en
- "enrollment_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/fleet/enrollment/route.ts:L13 | neighbors=[route.ts] | lang=en
- "explain_route_managerairesponse": "ManagerAiResponse" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L14 | neighbors=[route.ts] | lang=en
- "explain_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L21 | neighbors=[route.ts] | lang=en
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
- "exploit_nuclei_exploit_rationale_120": "Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L120 | neighbors=[.run_cve_poc()] | lang=en
- "exploit_nuclei_exploit_rationale_160": "Parse nuclei JSONL output for a single CVE PoC result." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L160 | neighbors=[._parse_poc_output()] | lang=en
- "exploit_nuclei_exploit_rationale_48": "Run Nuclei CVE PoC templates against a single target.     Every template is safe" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L48 | neighbors=[NucleiExploitRunner] | lang=en
- "exploit_nuclei_exploit_rationale_60": "Parse template YAML and validate it contains no write/delete/DoS actions." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L60 | neighbors=[.safe_template_check()] | lang=en
- "exploit_orchestrator_exploitorchestrator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L53 | neighbors=[ExploitOrchestrator] | lang=en
- "exploit_safety_approvalrequirederror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L30 | neighbors=[ApprovalRequiredError] | lang=en
- "exploit_safety_rationale_1": "Safety constants, exceptions, and validators for the exploitation engine.  All s" | kind=entity | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[safety.py] | lang=en
- "exploit_safety_rationale_17": "Raised when a requested payload or module is not on the allowlist." | kind=entity | source=manager/backend/app/exploit/safety.py:L17 | neighbors=[SafetyViolationError] | lang=en
- "exploit_safety_rationale_175": "Raises SafetyViolationError if payload is not on allowlist     or violates per-p" | kind=entity | source=manager/backend/app/exploit/safety.py:L175 | neighbors=[validate_payload()] | lang=en
- "exploit_safety_rationale_203": "Raises SafetyViolationError if module is on the block list." | kind=entity | source=manager/backend/app/exploit/safety.py:L203 | neighbors=[validate_module()] | lang=en
- "exploit_safety_rationale_21": "Raised when a target IP is outside the engagement scope CIDRs." | kind=entity | source=manager/backend/app/exploit/safety.py:L21 | neighbors=[OutOfScopeError] | lang=en
- "exploit_safety_rationale_217": "Raises OutOfScopeError if target_ip is not in scope or is excluded." | kind=entity | source=manager/backend/app/exploit/safety.py:L217 | neighbors=[validate_scope()] | lang=en
- "exploit_safety_rationale_240": "True if this target requires human manager approval before exploit runs." | kind=entity | source=manager/backend/app/exploit/safety.py:L240 | neighbors=[requires_approval()] | lang=en
- "exploit_safety_rationale_25": "Raised when a job would exceed the maximum hosts per run." | kind=entity | source=manager/backend/app/exploit/safety.py:L25 | neighbors=[BlastRadiusExceededError] | lang=en
- "exploit_safety_rationale_29": "Raised when a high-risk target requires manager approval before running." | kind=entity | source=manager/backend/app/exploit/safety.py:L29 | neighbors=[ApprovalRequiredError] | lang=pt
- "exposure_route_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L10 | neighbors=[route.ts] | lang=en
- "exposure_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L15 | neighbors=[route.ts] | lang=en
- "findings_page_complianceref": "ComplianceRef" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L45 | neighbors=[page.tsx] | lang=en
- "findings_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L127 | neighbors=[page.tsx] | lang=en
- "findings_page_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "findings_page_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "findings_page_detectionpill": "DetectionPill()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L190 | neighbors=[page.tsx] | lang=en
- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L204 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-090.json

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
