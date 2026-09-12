# Node Description Batch 199 of 380

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

- "agent_agent_rationale_919": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L919 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_921": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L921 | neighbors=[_ws_stage_job_offer()] | lang=en
- "agent_agent_rationale_927": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L927 | neighbors=[_ws_stage_job_offer()] | lang=en
- "agent_agent_rationale_928": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L928 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_93": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L93 | neighbors=[_job_intent()] | lang=en
- "agent_agent_rationale_939": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L939 | neighbors=[_ws_take_confirmed_job()] | lang=en
- "agent_agent_rationale_940": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L940 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_943": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L943 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_945": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L945 | neighbors=[_ws_take_confirmed_job()] | lang=en
- "agent_agent_rationale_955": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L955 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_960": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L960 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_967": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L967 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_972": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L972 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_976": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L976 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_978": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L978 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_979": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L979 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_985": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L985 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_986": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L986 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_996": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L996 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_997": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L997 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rung": "Rung" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L18 | neighbors=[agent.py] | lang=en
- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_bootstrap_rationale_1": "bootstrap.py — Layer-1 (Python runtime) install + optional installer verificatio" | kind=entity | source=probe/agent/bootstrap.py:L1 | neighbors=[bootstrap.py] | lang=en
- "agent_bootstrap_rationale_14": "The per-OS command that installs Python 3 + the venv module. Empty list     mean" | kind=entity | source=probe/agent/bootstrap.py:L14 | neighbors=[python_install_cmd()] | lang=en
- "agent_bootstrap_rationale_32": "strict wins a conflict (safer). Otherwise permissive — the initial-phase     def" | kind=entity | source=probe/agent/bootstrap.py:L32 | neighbors=[security_mode()] | lang=en
- "agent_bootstrap_rationale_40": "Verify a fetched installer. strict = fail-closed; permissive = warn+continue." | kind=entity | source=probe/agent/bootstrap.py:L40 | neighbors=[verify_download()] | lang=pt
- "agent_cli_configstore_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L58 | neighbors=[ConfigStore] | lang=en
- "agent_cli_rationale_574": "Run a bounded capability suite and optionally score known ground truth." | kind=entity | source=probe/agent/cli.py:L574 | neighbors=[cmd_validate()] | lang=en
- "agent_cli_rationale_576": "Run a bounded capability suite and optionally score known ground truth." | kind=entity | source=probe/agent/cli.py:L576 | neighbors=[cmd_validate()] | lang=en
- "agent_config_model_rationale_1": "config_model.py — single config precedence chain + effective source map.  Implem" | kind=entity | source=probe/agent/config_model.py:L1 | neighbors=[config_model.py] | lang=en
- "agent_config_model_rationale_32": "Parse KEY=VALUE lines; ignore blanks and #comments." | kind=entity | source=probe/agent/config_model.py:L32 | neighbors=[parse_env_file()] | lang=en
- "agent_config_model_rationale_45": "Return (values, sources). Precedence: cli > env > probe.env > manager > default." | kind=entity | source=probe/agent/config_model.py:L45 | neighbors=[resolve()] | lang=en
- "agent_config_model_rationale_72": "Rows of (field, value, winning-source) for `config show --effective`." | kind=entity | source=probe/agent/config_model.py:L72 | neighbors=[render_effective()] | lang=en
- "agent_config_model_to_bool": "_to_bool()" | kind=code-symbol | source=probe/agent/config_model.py:L12 | neighbors=[config_model.py] | lang=en
- "agent_connect_rationale_1": "connect.py — OPTIONAL Manager mode + uplink security (Phase 6).  The agent is fu" | kind=entity | source=probe/agent/connect.py:L1 | neighbors=[connect.py] | lang=en
- "agent_connect_rationale_36": "Deterministic bytes the Manager signs and the agent verifies (sig excluded)." | kind=entity | source=probe/agent/connect.py:L36 | neighbors=[canonical_job_bytes()] | lang=en
- "agent_connect_rationale_42": "Verify contract version, Ed25519 signature (pinned key), and validity window." | kind=entity | source=probe/agent/connect.py:L42 | neighbors=[verify_job()] | lang=en
- "agent_connect_rationale_67": "The independent ceiling: a job is admitted only if it is validly signed AND" | kind=entity | source=probe/agent/connect.py:L67 | neighbors=[admit_job()] | lang=en
- "agent_connect_rationale_89": "Opt-in: enroll + run the daemon under the supervisor, honoring the kill     swit" | kind=entity | source=probe/agent/connect.py:L89 | neighbors=[run()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-198.json

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
