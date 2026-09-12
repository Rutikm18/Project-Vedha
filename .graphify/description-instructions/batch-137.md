# Node Description Batch 138 of 380

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

- "ad_ntlm_relay_rationale_39": "For each IP, returns {signing_enabled, signing_required}.          A host is rel" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L39 | neighbors=[.check_smb_signing(), FindingSeverity] | lang=en
- "ad_ntlm_relay_rationale_81": "Returns True if the DC *enforces* LDAP signing / channel binding.          We at" | kind=entity | source=manager/backend/app/ad/ntlm_relay.py:L81 | neighbors=[.check_ldap_signing(), FindingSeverity] | lang=en
- "ad_orchestrator_adassessmentrunner_anonymous_bind_finding": "._anonymous_bind_finding()" | kind=code-symbol | source=manager/backend/app/ad/orchestrator.py:L186 | neighbors=[ADAssessmentRunner, .run()] | lang=en
- "agent_agent_isblocked": "isBlocked()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L62 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_agent_rationale_1032": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L1032 | neighbors=[_flush_spool_over_http(), _check_anti_debug()] | lang=en
- "agent_agent_rationale_1049": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L1049 | neighbors=[_ws_http_poll_fallback(), _enroll_device()] | lang=en
- "agent_agent_rationale_1080": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L1080 | neighbors=[_ws_heartbeat_sender(), _load_or_create_identity()] | lang=en
- "agent_agent_rationale_1163": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1163 | neighbors=[_check_anti_debug(), _enroll_device()] | lang=en
- "agent_agent_rationale_194": "Best-effort primary IPv4 of this host — the address a scan sources from.     Use" | kind=entity | source=probe/agent/agent.py:L194 | neighbors=[_detect_primary_ipv4(), _wait_for_manager()] | lang=en
- "agent_agent_rationale_470": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L470 | neighbors=[_ws_stage_job_offer(), _ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_608": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L608 | neighbors=[_ws_run_job(), _flush_spool_over_http()] | lang=en
- "agent_agent_rationale_63": "Return an integer environment setting constrained to a safe range." | kind=entity | source=probe/agent/agent.py:L63 | neighbors=[_bounded_env_int(), _load_env()] | lang=en
- "agent_agent_rationale_692": "Run an HTTP-claimed job while renewing its manager lease." | kind=entity | source=probe/agent/agent.py:L692 | neighbors=[_run_polled_job_with_heartbeats(), _ws_stage_job_offer()] | lang=en
- "agent_agent_rationale_710": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L710 | neighbors=[_ws_take_confirmed_job(), _load_or_create_identity()] | lang=en
- "agent_agent_rationale_724": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L724 | neighbors=[_run_ws_push_loop(), _flush_spool_over_http()] | lang=en
- "agent_agent_rationale_763": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L763 | neighbors=[_run_ws_push_loop(), _obtain_identity()] | lang=en
- "agent_agent_rationale_784": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L784 | neighbors=[_ws_stage_job_offer(), _check_anti_debug()] | lang=en
- "agent_agent_rationale_814": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L814 | neighbors=[_ws_take_confirmed_job(), _ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_881": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L881 | neighbors=[_startup_gauntlet(), _load_or_create_signing_identity()] | lang=pt
- "agent_agent_rationale_906": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L906 | neighbors=[_ws_take_confirmed_job(), _ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_973": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L973 | neighbors=[_ws_run_job(), _startup_gauntlet()] | lang=en
- "agent_agent_requiresapproval": "requiresApproval()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L54 | neighbors=[agent.py, runAutonomousEngagement()] | lang=en
- "agent_bootstrap_python_install_cmd": "python_install_cmd()" | kind=code-symbol | source=probe/agent/bootstrap.py:L13 | neighbors=[bootstrap.py, The per-OS command that installs Python…] | lang=en
- "agent_bootstrap_security_mode": "security_mode()" | kind=code-symbol | source=probe/agent/bootstrap.py:L31 | neighbors=[bootstrap.py, strict wins a conflict (safer). Otherwi…] | lang=en
- "agent_bootstrap_verify_download": "verify_download()" | kind=code-symbol | source=probe/agent/bootstrap.py:L39 | neighbors=[bootstrap.py, Verify a fetched installer. strict = fa…] | lang=en
- "agent_cli_cmd_whoami": "cmd_whoami()" | kind=code-symbol | source=probe/agent/cli.py:L298 | neighbors=[cli.py, cmd_auth_status()] | lang=en
- "agent_cli_doctor_check": "_doctor_check()" | kind=code-symbol | source=probe/agent/cli.py:L302 | neighbors=[cli.py, cmd_doctor()] | lang=en
- "agent_cli_main": "main()" | kind=code-symbol | source=probe/agent/cli.py:L1131 | neighbors=[cli.py, build_parser()] | lang=en
- "agent_cli_manager_is_local": "_manager_is_local()" | kind=code-symbol | source=probe/agent/cli.py:L570 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_cli_managerclient_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L106 | neighbors=[ManagerClient, normalize_manager_url()] | lang=en
- "agent_cli_write_private_json": "_write_private_json()" | kind=code-symbol | source=probe/agent/cli.py:L536 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_config_model_parse_env_file": "parse_env_file()" | kind=code-symbol | source=probe/agent/config_model.py:L31 | neighbors=[config_model.py, Parse KEY=VALUE lines; ignore blanks an…] | lang=en
- "agent_config_model_render_effective": "render_effective()" | kind=code-symbol | source=probe/agent/config_model.py:L71 | neighbors=[config_model.py, Rows of (field, value, winning-source) …] | lang=en
- "agent_config_model_resolve": "resolve()" | kind=code-symbol | source=probe/agent/config_model.py:L43 | neighbors=[config_model.py, Return (values, sources). Precedence: c…] | lang=en
- "agent_connect_connect_env": "connect_env()" | kind=code-symbol | source=probe/agent/connect.py:L25 | neighbors=[connect.py, run()] | lang=en
- "agent_connect_kill_switch_active": "kill_switch_active()" | kind=code-symbol | source=probe/agent/connect.py:L82 | neighbors=[connect.py, run()] | lang=en
- "agent_deps_pip_install_argsets": "pip_install_argsets()" | kind=code-symbol | source=probe/agent/deps.py:L32 | neighbors=[deps.py, install_requirements()] | lang=en
- "agent_deps_reqs_hash": "reqs_hash()" | kind=code-symbol | source=probe/agent/deps.py:L27 | neighbors=[deps.py, install_requirements()] | lang=en
- "agent_device_identity_decode_key": "decode_key()" | kind=code-symbol | source=probe/agent/device_identity.py:L30 | neighbors=[device_identity.py, verify_site_policy()] | lang=en
- "agent_doctor_measure_manager": "_measure_manager()" | kind=code-symbol | source=probe/agent/doctor.py:L95 | neighbors=[doctor.py, run()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-137.json

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
