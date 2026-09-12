# Node Description Batch 76 of 380

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

- "agent_connect_run": "run()" | kind=code-symbol | source=probe/agent/connect.py:L87 | neighbors=[connect.py, Opt-in: enroll + run the daemon under t…, connect_env(), kill_switch_active()]
- "agent_connect_verify_job": "verify_job()" | kind=code-symbol | source=probe/agent/connect.py:L41 | neighbors=[connect.py, admit_job(), Verify contract version, Ed25519 signat…, canonical_job_bytes()]
- "agent_deps_ensure_venv": "ensure_venv()" | kind=code-symbol | source=probe/agent/deps.py:L40 | neighbors=[deps.py, venv_dir(), venv_python(), install_requirements()]
- "agent_deps_venv_dir": "venv_dir()" | kind=code-symbol | source=probe/agent/deps.py:L16 | neighbors=[deps.py, ensure_venv(), install_requirements(), venv_python()]
- "agent_engine_results_by_target": "_results_by_target()" | kind=code-symbol | source=probe/agent/engine.py:L486 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), _derive_post_stage()]
- "agent_exit_state_make": "make()" | kind=code-symbol | source=probe/agent/exit_state.py:L72 | neighbors=[exit_state.py, class_for_reason(), code_for_class(), ExitState]
- "agent_hw_bind_check_hw_bind": "check_hw_bind()" | kind=code-symbol | source=probe/agent/hw_bind.py:L34 | neighbors=[hw_bind.py, get_hw_id(), HWBindError, Verify the binary is running on the mac…]
- "agent_hw_bind_hwbinderror": "HWBindError" | kind=code-symbol | source=probe/agent/hw_bind.py:L19 | neighbors=[hw_bind.py, check_hw_bind(), RuntimeError, Raised when the binary is running on an…]
- "agent_instance_lock_instancelockerror": "InstanceLockError" | kind=code-symbol | source=probe/agent/instance_lock.py:L51 | neighbors=[instance_lock.py, acquire_instance_lock(), RuntimeError, Another live process already owns this …]
- "agent_license_gauntlet": "gauntlet()" | kind=code-symbol | source=probe/agent/license.py:L101 | neighbors=[license.py, check_license(), Combined startup gauntlet: HW bind → li…, Combined startup gauntlet: HW bind → li…]
- "agent_license_short_id": "short_id()" | kind=code-symbol | source=probe/agent/license.py:L41 | neighbors=[license.py, check_license(), host_fingerprint(), verify_license()]
- "agent_local_run_summarize": "summarize()" | kind=code-symbol | source=probe/agent/local_run.py:L90 | neighbors=[local_run.py, _main(), _clean(), _port_label()]
- "agent_obs_build_diagnostics": "build_diagnostics()" | kind=code-symbol | source=probe/agent/obs.py:L73 | neighbors=[obs.py, _mask_addr(), redact(), A support bundle with secrets stripped …]
- "agent_obs_redact": "redact()" | kind=code-symbol | source=probe/agent/obs.py:L24 | neighbors=[obs.py, build_diagnostics(), log_line(), _is_sensitive()]
- "agent_result_queue_resultqueue_enforce_size_bounds": "._enforce_size_bounds()" | kind=code-symbol | source=probe/agent/result_queue.py:L135 | neighbors=[ResultQueue, ._bytes(), ._files(), .enqueue()]
- "agent_result_queue_resultqueue_find": "._find()" | kind=code-symbol | source=probe/agent/result_queue.py:L104 | neighbors=[ResultQueue, .ack(), .enqueue(), ._files()]
- "agent_result_queue_resultqueue_read": "._read()" | kind=code-symbol | source=probe/agent/result_queue.py:L129 | neighbors=[ResultQueue, .pending(), .decrypt(), Record]
- "agent_scope_validator_networks_for_target": "_networks_for_target()" | kind=code-symbol | source=probe/agent/scope_validator.py:L27 | neighbors=[scope_validator.py, Parse one IP, CIDR, or inclusive IP ran…, targets_in_excludes(), validate_targets_in_scope()]
- "agent_scope_validator_targets_in_excludes": "targets_in_excludes()" | kind=code-symbol | source=probe/agent/scope_validator.py:L120 | neighbors=[scope_validator.py, Remove targets that fall inside any exc…, _networks_for_target(), Remove targets that fall inside any exc…]
- "agent_scope_validator_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L81 | neighbors=[scope_validator.py, Check targets against the authoritative…, _networks_for_target(), Fetch the engagement's authoritative sc…]
- "agent_self_scan_plan_self_scan": "plan_self_scan()" | kind=code-symbol | source=probe/agent/self_scan.py:L29 | neighbors=[self_scan.py, SelfScanPlan, Pure decision. Returns (plan, reason); …, run_from()]
- "agent_self_scan_run_from": "run_from()" | kind=code-symbol | source=probe/agent/self_scan.py:L59 | neighbors=[self_scan.py, run(), execute(), plan_self_scan()]
- "agent_setup_cmd_collect_diagnostics": "cmd_collect_diagnostics()" | kind=code-symbol | source=probe/agent/setup.py:L126 | neighbors=[setup.py, _is_privileged(), _resolved(), _state_dir()]
- "agent_setup_cmd_connect": "cmd_connect()" | kind=code-symbol | source=probe/agent/setup.py:L103 | neighbors=[setup.py, _os_name(), _resolved(), _state_dir()]
- "agent_setup_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/setup.py:L84 | neighbors=[setup.py, _is_privileged(), _resolved(), _state_dir()]
- "agent_task_runner_prepare_result_dir": "prepare_result_dir()" | kind=code-symbol | source=probe/agent/task_runner.py:L57 | neighbors=[task_runner.py, _result_dir(), Create the result archive directory at …, Create the result archive directory at …]
- "agent_transport_strip_nul": "_strip_nul()" | kind=code-symbol | source=probe/agent/transport.py:L31 | neighbors=[transport.py, Recursively remove NUL (U+0000) charact…, .submit_chunk(), .submit_result()]
- "agent_transport_sync_directory": "_sync_directory()" | kind=code-symbol | source=probe/agent/transport.py:L131 | neighbors=[transport.py, _atomic_write_private_state(), .close(), .update_state()]
- "agent_transport_transport_submit_chunk": ".submit_chunk()" | kind=code-symbol | source=probe/agent/transport.py:L789 | neighbors=[Commit ONE finished host while the job …, Transport, _strip_nul(), .ensure_device_access()]
- "ai_agent_agentdecisionengine_overview": "._overview()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L269 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), ._count(), _val()]
- "ai_agent_agentdecisionengine_persist": "._persist()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L352 | neighbors=[AgentDecisionEngine, _maybe_decimal(), _maybe_uuid(), .run()]
- "ai_hallucination": "hallucination.py" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[HallucinationGuard, HallucinationGuard — post-generation va…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_enum": "_enum()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L338 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding(), _remediation_plan_prompt()]
- "ai_llm_report_llmreportgenerator_complete": "._complete()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L113 | neighbors=[LLMReportGenerator, LLMUnavailableError, ._generate_and_store(), .generate_remediation_plan()]
- "ai_llm_report_llmreportgenerator_generate_remediation_steps": ".generate_remediation_steps()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L228 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]
- "ai_llm_report_llmreportgenerator_generate_technical_finding": ".generate_technical_finding()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L203 | neighbors=[LLMReportGenerator, _enum(), _finding_scores(), ._generate_and_store()]
- "ai_llm_report_rationale_1": "LLMReportGenerator — Claude-backed narrative generation for VAPT reports.  Uses" | kind=entity | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[llm_report.py, HallucinationGuard, ReviewStatus, LLMOutput]
- "ai_llm_report_rationale_47": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/llm_report.py:L47 | neighbors=[LLMUnavailableError, HallucinationGuard, ReviewStatus, LLMOutput]
- "ai_verification_graph": "verification_graph.py" | kind=code-symbol | source=manager/backend/app/ai/verification_graph.py:L1 | neighbors=[graph_available(), run_verification(), verification_graph.py — optional LangGr…, c02c465 feat(verification): optional La…]
- "app_main_gziprequestmiddleware": "GzipRequestMiddleware" | kind=code-symbol | source=manager/backend/app/main.py:L133 | neighbors=[main.py, .__call__(), .__init__(), TenantIsolationMiddleware]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-075.json

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
