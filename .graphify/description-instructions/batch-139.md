# Node Description Batch 140 of 380

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

- "agent_self_scan_primary_ipv4": "primary_ipv4()" | kind=code-symbol | source=probe/agent/self_scan.py:L70 | neighbors=[self_scan.py, run()] | lang=en
- "agent_self_scan_read": "_read()" | kind=code-symbol | source=probe/agent/self_scan.py:L82 | neighbors=[self_scan.py, detect_host_container()] | lang=en
- "agent_self_scan_selfscanplan": "SelfScanPlan" | kind=code-symbol | source=probe/agent/self_scan.py:L21 | neighbors=[self_scan.py, plan_self_scan()] | lang=en
- "agent_service_commands_for": "commands_for()" | kind=code-symbol | source=probe/agent/service.py:L85 | neighbors=[service.py, install()] | lang=en
- "agent_service_uninstall": "uninstall()" | kind=code-symbol | source=probe/agent/service.py:L123 | neighbors=[service.py, uninstall_commands()] | lang=en
- "agent_service_uninstall_commands": "uninstall_commands()" | kind=code-symbol | source=probe/agent/service.py:L96 | neighbors=[service.py, uninstall()] | lang=en
- "agent_setup_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/setup.py:L59 | neighbors=[setup.py, main()] | lang=en
- "agent_setup_cmd_config": "cmd_config()" | kind=code-symbol | source=probe/agent/setup.py:L91 | neighbors=[setup.py, _resolved()] | lang=en
- "agent_setup_cmd_self_scan": "cmd_self_scan()" | kind=code-symbol | source=probe/agent/setup.py:L98 | neighbors=[setup.py, _state_dir()] | lang=en
- "agent_setup_main": "main()" | kind=code-symbol | source=probe/agent/setup.py:L144 | neighbors=[setup.py, build_parser()] | lang=en
- "agent_setup_probe_env": "_probe_env()" | kind=code-symbol | source=probe/agent/setup.py:L46 | neighbors=[setup.py, _resolved()] | lang=en
- "agent_task_runner_rationale_56": "Create the result archive directory at agent startup.      _archive_result() wou" | kind=entity | source=probe/agent/task_runner.py:L56 | neighbors=[prepare_result_dir(), .__init__()] | lang=en
- "agent_task_runner_rationale_58": "Create the result archive directory at agent startup.      _archive_result() wou" | kind=entity | source=probe/agent/task_runner.py:L58 | neighbors=[prepare_result_dir(), .__init__()] | lang=en
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L15 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L313 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L24 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L98 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L26 | neighbors=[agent.py, tools.ts] | lang=en
- "agent_transport_rationale_111": "Best-effort extraction of the manager's 409 ``detail`` message." | kind=entity | source=probe/agent/transport.py:L111 | neighbors=[_enrollment_conflict_detail(), .is_authenticated()] | lang=en
- "agent_transport_rationale_142": "Durably replace one private JSON state file without exposing secrets." | kind=entity | source=probe/agent/transport.py:L142 | neighbors=[_atomic_write_private_state(), .register()] | lang=en
- "agent_transport_rationale_185": "True if we have both an agent_id and a token for API calls." | kind=entity | source=probe/agent/transport.py:L185 | neighbors=[.is_authenticated(), .update_state()] | lang=en
- "agent_transport_rationale_277": "Merge and atomically persist private state while preserving fields." | kind=entity | source=probe/agent/transport.py:L277 | neighbors=[.update_state(), .refresh_registration()] | lang=en
- "agent_transport_rationale_32": "Recursively remove NUL (U+0000) characters from every string in a payload." | kind=entity | source=probe/agent/transport.py:L32 | neighbors=[_strip_nul(), TransportError] | lang=en
- "agent_transport_rationale_330": "Forget everything a SPECIFIC manager issued, keeping the probe's own         key" | kind=entity | source=probe/agent/transport.py:L330 | neighbors=[.clear_manager_binding(), .connect_ws()] | lang=en
- "agent_transport_rationale_354": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L354 | neighbors=[.fetch_scope(), .is_ws_connected()] | lang=en
- "agent_transport_rationale_419": "Register using a manager-side shared bootstrap key (no user login needed)." | kind=entity | source=probe/agent/transport.py:L419 | neighbors=[.bootstrap(), .refresh_registration()] | lang=pt
- "agent_transport_rationale_421": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=probe/agent/transport.py:L421 | neighbors=[.ensure_device_access(), .http_get()] | lang=en
- "agent_transport_rationale_514": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=probe/agent/transport.py:L514 | neighbors=[.ensure_device_access(), .heartbeat()] | lang=en
- "agent_transport_rationale_519": "Backwards-compatible bool wrapper over `refresh_device_access_ex`." | kind=entity | source=probe/agent/transport.py:L519 | neighbors=[.refresh_device_access(), .fetch_scope()] | lang=en
- "agent_transport_rationale_538": "Refresh routing metadata using the cached agent identity.          Returns True" | kind=entity | source=probe/agent/transport.py:L538 | neighbors=[.refresh_registration(), .submit_result()] | lang=en
- "agent_transport_rationale_564": "Refresh routing metadata using the cached agent identity.          Returns True" | kind=entity | source=probe/agent/transport.py:L564 | neighbors=[.refresh_registration(), .submit_result()] | lang=en
- "agent_transport_rationale_627": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L627 | neighbors=[.http_get(), .connect_ws()] | lang=en
- "agent_transport_rationale_647": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L647 | neighbors=[.poll_jobs(), .http_get()] | lang=en
- "agent_transport_rationale_65": "A poll/activate targeted an enrollment request the manager does not have     (HT" | kind=entity | source=probe/agent/transport.py:L65 | neighbors=[EnrollmentRequestNotFound, _enrollment_conflict_detail()] | lang=en
- "agent_transport_rationale_673": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L673 | neighbors=[.poll_jobs(), .connect_ws()] | lang=en
- "agent_transport_rationale_777": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L777 | neighbors=[.http_get(), .connect_ws()] | lang=en
- "agent_transport_transport_clear_state": ".clear_state()" | kind=code-symbol | source=probe/agent/transport.py:L322 | neighbors=[Transport, .update_state()] | lang=en
- "agent_transport_transport_close": ".close()" | kind=code-symbol | source=probe/agent/transport.py:L984 | neighbors=[_sync_directory(), Transport] | lang=en
- "agent_transport_transport_init": ".__init__()" | kind=code-symbol | source=probe/agent/transport.py:L189 | neighbors=[Transport, .load_state()] | lang=en
- "agent_transport_transport_poll_enrollment": ".poll_enrollment()" | kind=code-symbol | source=probe/agent/transport.py:L463 | neighbors=[Transport, EnrollmentRequestNotFound] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-139.json

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
