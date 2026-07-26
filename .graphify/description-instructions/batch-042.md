# Node Description Batch 43 of 104

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

- "agent_agent_isblocked": "isBlocked()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L62 | neighbors=[agent.py, runAutonomousEngagement()]
- "agent_agent_parse_spn_output": "parse_spn_output()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L294 | neighbors=[agent.py, execute_ad_enum()]
- "agent_agent_requiresapproval": "requiresApproval()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L54 | neighbors=[agent.py, runAutonomousEngagement()]
- "agent_agent_scanjob": "ScanJob" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L62 | neighbors=[agent.py, ._poll_and_execute()]
- "agent_agent_scanningagent_report_progress": "._report_progress()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L665 | neighbors=[ScanningAgent, ._api_call()]
- "agent_agent_str": "str()" | kind=code-symbol | source=probe-go/agent/agent.go:L367 | neighbors=[agent.py, mapToJob()]
- "agent_cli_cmd_whoami": "cmd_whoami()" | kind=code-symbol | source=probe/agent/cli.py:L294 | neighbors=[cli.py, cmd_auth_status()]
- "agent_cli_doctor_check": "_doctor_check()" | kind=code-symbol | source=probe/agent/cli.py:L298 | neighbors=[cli.py, cmd_doctor()]
- "agent_cli_main": "main()" | kind=code-symbol | source=probe/agent/cli.py:L660 | neighbors=[cli.py, build_parser()]
- "agent_cli_managerclient_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L102 | neighbors=[ManagerClient, normalize_manager_url()]
- "agent_engine_targets": "_targets()" | kind=code-symbol | source=probe/agent/engine.py:L71 | neighbors=[engine.py, run_scan()]
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L48 | neighbors=[license.py, verify_license()]
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L76 | neighbors=[Remove the spool file for a successfull…, ResultSpool]
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…]
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…]
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…]
- "agent_scope_validator_fetch_engagement_scope": "fetch_engagement_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Fetch the engagement's authoritative sc…]
- "agent_scope_validator_merge_exclusions": "merge_exclusions()" | kind=code-symbol | source=probe/agent/scope_validator.py:L117 | neighbors=[scope_validator.py, Merge engagement-level exclusions with …]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L84 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L54 | neighbors=[scope_validator.py, Check targets against the authoritative…]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L48 | neighbors=[Args:             http_get:       Callb…, TaskRunner]
- "agent_tools_agentstate": "AgentState" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L16 | neighbors=[agent.py, tools.ts]
- "agent_tools_persistagentfindings": "persistAgentFindings()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L314 | neighbors=[agent.py, tools.ts]
- "agent_tools_risk": "Risk" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L25 | neighbors=[agent.py, tools.ts]
- "agent_tools_tool_registry": "TOOL_REGISTRY" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L99 | neighbors=[agent.py, tools.ts]
- "agent_tools_tooldef": "ToolDef" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L27 | neighbors=[agent.py, tools.ts]
- "agent_transport_get": ".get()" | kind=code-symbol | source=probe-go/agent/transport.go:L113 | neighbors=[transport.py, .PollJobs()]
- "agent_transport_heartbeat": ".Heartbeat()" | kind=code-symbol | source=probe-go/agent/transport.go:L66 | neighbors=[transport.py, .patch()]
- "agent_transport_login": ".Login()" | kind=code-symbol | source=probe-go/agent/transport.go:L35 | neighbors=[transport.py, .post()]
- "agent_transport_patch": ".patch()" | kind=code-symbol | source=probe-go/agent/transport.go:L161 | neighbors=[transport.py, .Heartbeat()]
- "agent_transport_polljobs": ".PollJobs()" | kind=code-symbol | source=probe-go/agent/transport.go:L75 | neighbors=[transport.py, .get()]
- "agent_transport_register": ".Register()" | kind=code-symbol | source=probe-go/agent/transport.go:L46 | neighbors=[transport.py, .post()]
- "agent_transport_submitresult": ".SubmitResult()" | kind=code-symbol | source=probe-go/agent/transport.go:L83 | neighbors=[transport.py, .post()]
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L232 | neighbors=[Fetch the engagement's authoritative sc…, Transport]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L189 | neighbors=[Send a heartbeat to the manager.       …, Transport]
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L302 | neighbors=[Generic authenticated GET, returns pars…, Transport]
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L110 | neighbors=[True if we have both an agent_id and a …, Transport]
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L353 | neighbors=[True if the WebSocket connection is act…, Transport]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L116 | neighbors=[Transport, .register()]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L251 | neighbors=[Submit a scan result to the manager.   …, Transport]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-042.json

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
