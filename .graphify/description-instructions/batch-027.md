# Node Description Batch 28 of 119

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

- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=probe/agent/agent.py:L285 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, say()]
- "agent_agent_runpolledjob": ".runPolledJob()" | kind=code-symbol | source=probe-go/agent/agent.go:L447 | neighbors=[agent.py, .heartbeatWithRetry(), .runJob(), .runPollLoop()]
- "agent_agent_runwsloop": ".runWSLoop()" | kind=code-symbol | source=probe-go/agent/agent.go:L90 | neighbors=[agent.py, .Run(), say(), .wsSession()]
- "agent_agent_str": "str()" | kind=code-symbol | source=probe-go/agent/agent.go:L907 | neighbors=[agent.py, mapToJob(), .rejectJob(), .wsSession()]
- "agent_agent_stringlist": "stringList()" | kind=code-symbol | source=probe-go/agent/agent.go:L863 | neighbors=[agent.py, firstTargetList(), mapToJob(), dedupStrings()]
- "agent_agent_submitwithspool": ".submitWithSpool()" | kind=code-symbol | source=probe-go/agent/agent.go:L590 | neighbors=[agent.py, .runPollLoop(), resultPayload(), say()]
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L480 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say()]
- "agent_cli_build_parser": "build_parser()" | kind=code-symbol | source=probe/agent/cli.py:L931 | neighbors=[cli.py, default_config_path(), _env(), main()]
- "agent_cli_cmd_agents_list": "cmd_agents_list()" | kind=code-symbol | source=probe/agent/cli.py:L407 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_list": "cmd_engagements_list()" | kind=code-symbol | source=probe/agent/cli.py:L424 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_engagements_scope": "cmd_engagements_scope()" | kind=code-symbol | source=probe/agent/cli.py:L472 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_scan_status": "cmd_scan_status()" | kind=code-symbol | source=probe/agent/cli.py:L528 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_cmd_use_cases": "cmd_use_cases()" | kind=code-symbol | source=probe/agent/cli.py:L391 | neighbors=[cli.py, client_from_args(), .request(), output()]
- "agent_cli_configstore_remove_profile": ".remove_profile()" | kind=code-symbol | source=probe/agent/cli.py:L94 | neighbors=[cmd_auth_logout(), ConfigStore, .load(), .save()]
- "agent_cli_configstore_set_profile": ".set_profile()" | kind=code-symbol | source=probe/agent/cli.py:L88 | neighbors=[cmd_auth_login(), ConfigStore, .load(), .save()]
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L167 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan()]
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…]
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…]
- "agent_license_host_fingerprint": "host_fingerprint()" | kind=code-symbol | source=probe/agent/license.py:L38 | neighbors=[license.py, Stable per-machine ID, derived from hw_…, short_id(), verify_license()]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L44 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_result_spool_resultspool_spool_count": ".spool_count()" | kind=code-symbol | source=probe/agent/result_spool.py:L179 | neighbors=[Number of pending (unsubmitted) results…, ResultSpool, .exists(), Number of pending (unsubmitted) results…]
- "agent_result_spool_resultspool_sync_directory": "._sync_directory()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .remove(), .save(), .exists()]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…]
- "agent_spool_delete": ".Delete()" | kind=code-symbol | source=probe-go/agent/spool.go:L71 | neighbors=[spool.go, .path(), syncDir(), .Flush()]
- "agent_spool_path": ".path()" | kind=code-symbol | source=probe-go/agent/spool.go:L132 | neighbors=[spool.go, .Delete(), .Flush(), .Save()]
- "agent_spool_test": "spool_test.go" | kind=code-symbol | source=probe-go/agent/spool_test.go:L1 | neighbors=[entryNames(), TestSpoolFlushDeletesOnlyAcknowledgedRe…, TestSpoolSaveIsAtomicAndRejectsTraversa…, b4b12a9 Rename project and update files]
- "agent_state_test_newidentityserver": "newIdentityServer()" | kind=code-symbol | source=probe-go/agent/state_test.go:L24 | neighbors=[state_test.go, writeJSON(), TestObtainIdentityPersistsAndReusesRegi…, TestObtainIdentityRecoversFromCorruptSt…]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L398 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), Submit the result, with spool-and-retry…]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L47 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state()]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L37 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L449 | neighbors=[Establish an authenticated WebSocket co…, Transport, TransportError, Establish an authenticated WebSocket co…]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L335 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, TransportError, Poll for pending jobs (HTTP fallback fo…]
- "ai_agent_agentdecisionengine_overview": "._overview()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L264 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), ._count(), _val()]
- "ai_agent_agentdecisionengine_persist": "._persist()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L336 | neighbors=[AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), .run()]
- "ai_hallucination": "hallucination.py" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[HallucinationGuard, HallucinationGuard — post-generation va…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_llmreportgenerator_generate_remediation_steps": ".generate_remediation_steps()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L222 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]
- "ai_llm_report_llmreportgenerator_generate_technical_finding": ".generate_technical_finding()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L197 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]
- "ai_llm_report_rationale_1": "LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses" | kind=entity | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[HallucinationGuard, llm_report.py, ReviewStatus, LLMOutput]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-027.json

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
