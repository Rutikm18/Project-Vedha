# Node Description Batch 123 of 330

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

- "agent_agent_requiresapproval": "requiresApproval()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L54 | neighbors=[agent.py, runAutonomousEngagement()]
- "agent_cli_cmd_whoami": "cmd_whoami()" | kind=code-symbol | source=probe/agent/cli.py:L298 | neighbors=[cli.py, cmd_auth_status()]
- "agent_cli_doctor_check": "_doctor_check()" | kind=code-symbol | source=probe/agent/cli.py:L302 | neighbors=[cli.py, cmd_doctor()]
- "agent_cli_main": "main()" | kind=code-symbol | source=probe/agent/cli.py:L1131 | neighbors=[cli.py, build_parser()]
- "agent_cli_manager_is_local": "_manager_is_local()" | kind=code-symbol | source=probe/agent/cli.py:L570 | neighbors=[cli.py, cmd_validate()]
- "agent_cli_managerclient_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L106 | neighbors=[ManagerClient, normalize_manager_url()]
- "agent_cli_write_private_json": "_write_private_json()" | kind=code-symbol | source=probe/agent/cli.py:L536 | neighbors=[cli.py, cmd_validate()]
- "agent_device_identity_decode_key": "decode_key()" | kind=code-symbol | source=probe/agent/device_identity.py:L30 | neighbors=[device_identity.py, verify_site_policy()]
- "agent_engine_facts_from_cache": "_facts_from_cache()" | kind=code-symbol | source=probe/agent/engine.py:L308 | neighbors=[engine.py, run_scan()]
- "agent_engine_rationale_191": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L191 | neighbors=[_clamp(), _job_runtime_seconds()]
- "agent_engine_rationale_201": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L201 | neighbors=[_job_runtime_seconds(), _tuning_from_params()]
- "agent_explain_plan_main": "main()" | kind=code-symbol | source=probe/agent/explain_plan.py:L104 | neighbors=[explain_plan.py, _print_table()]
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L45 | neighbors=[license.py, verify_license()]
- "agent_local_run_scope_file": "_scope_file()" | kind=code-symbol | source=probe/agent/local_run.py:L38 | neighbors=[local_run.py, _main()]
- "agent_result_spool_resultspool_at_capacity": ".at_capacity()" | kind=code-symbol | source=probe/agent/result_spool.py:L235 | neighbors=[Whether new jobs must pause until pendi…, ResultSpool]
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…]
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…]
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…]
- "agent_scope_validator_rationale_58": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L58 | neighbors=[fetch_engagement_scope(), validate_targets_in_scope()]
- "agent_task_runner_rationale_56": "Create the result archive directory at agent startup.      _archive_result() wou" | kind=entity | source=probe/agent/task_runner.py:L56 | neighbors=[prepare_result_dir(), .__init__()]
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L15 | neighbors=[agent.py, tools.ts]
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L313 | neighbors=[agent.py, tools.ts]
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L24 | neighbors=[agent.py, tools.ts]
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L98 | neighbors=[agent.py, tools.ts]
- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L26 | neighbors=[agent.py, tools.ts]
- "agent_transport_rationale_111": "Best-effort extraction of the manager's 409 ``detail`` message." | kind=entity | source=probe/agent/transport.py:L111 | neighbors=[_enrollment_conflict_detail(), .is_authenticated()]
- "agent_transport_rationale_185": "True if we have both an agent_id and a token for API calls." | kind=entity | source=probe/agent/transport.py:L185 | neighbors=[.is_authenticated(), .update_state()]
- "agent_transport_rationale_277": "Merge and atomically persist private state while preserving fields." | kind=entity | source=probe/agent/transport.py:L277 | neighbors=[.update_state(), .refresh_registration()]
- "agent_transport_rationale_32": "Recursively remove NUL (U+0000) characters from every string in a payload." | kind=entity | source=probe/agent/transport.py:L32 | neighbors=[_strip_nul(), TransportError]
- "agent_transport_rationale_354": "Fetch the engagement's authoritative scope.          Returns the response dict i" | kind=entity | source=probe/agent/transport.py:L354 | neighbors=[.fetch_scope(), .is_ws_connected()]
- "agent_transport_rationale_421": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=probe/agent/transport.py:L421 | neighbors=[.ensure_device_access(), .http_get()]
- "agent_transport_rationale_514": "Refresh a device token before expiry; legacy identities are unchanged." | kind=entity | source=probe/agent/transport.py:L514 | neighbors=[.ensure_device_access(), .heartbeat()]
- "agent_transport_rationale_538": "Refresh routing metadata using the cached agent identity.          Returns True" | kind=entity | source=probe/agent/transport.py:L538 | neighbors=[.refresh_registration(), .submit_result()]
- "agent_transport_rationale_627": "Generic authenticated GET, returns parsed JSON or None on failure.          Used" | kind=entity | source=probe/agent/transport.py:L627 | neighbors=[.http_get(), .connect_ws()]
- "agent_transport_rationale_647": "Poll for pending jobs (HTTP fallback for WebSocket).          Returns a list of" | kind=entity | source=probe/agent/transport.py:L647 | neighbors=[.poll_jobs(), .http_get()]
- "agent_transport_transport_clear_state": ".clear_state()" | kind=code-symbol | source=probe/agent/transport.py:L299 | neighbors=[Transport, .update_state()]
- "agent_transport_transport_close": ".close()" | kind=code-symbol | source=probe/agent/transport.py:L817 | neighbors=[_sync_directory(), Transport]
- "agent_transport_transport_init": ".__init__()" | kind=code-symbol | source=probe/agent/transport.py:L177 | neighbors=[Transport, .load_state()]
- "agent_validation_metric": "_metric()" | kind=code-symbol | source=probe/agent/validation.py:L173 | neighbors=[validation.py, score_inventory()]
- "agent_validation_not_scored": "_not_scored()" | kind=code-symbol | source=probe/agent/validation.py:L197 | neighbors=[validation.py, score_inventory()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-122.json

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
