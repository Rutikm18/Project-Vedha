# Node Description Batch 173 of 330

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

- "agent_agent_rationale_723": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L723 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_724": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L724 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_736": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L736 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_737": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L737 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_744": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L744 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_75": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L75 | neighbors=[_load_env()] | lang=en
- "agent_agent_rationale_763": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L763 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_769": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L769 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_783": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L783 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_802": "Release a staged job only after the manager confirms its claim." | kind=entity | source=probe/agent/agent.py:L802 | neighbors=[_ws_take_confirmed_job()] | lang=en
- "agent_agent_rationale_805": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L805 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_81": "Return no work for transient poll failures without hiding auth failures." | kind=entity | source=probe/agent/agent.py:L81 | neighbors=[_poll_jobs_or_empty()] | lang=en
- "agent_agent_rationale_814": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L814 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_831": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L831 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_832": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L832 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_836": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L836 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_842": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L842 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_851": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L851 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_859": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L859 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_868": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L868 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_872": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L872 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_880": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L880 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_906": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L906 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_913": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L913 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_914": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L914 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_919": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L919 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_928": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L928 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_93": "Human label for what a job will actually run — the use-case (real intent),     n" | kind=entity | source=probe/agent/agent.py:L93 | neighbors=[_job_intent()] | lang=en
- "agent_agent_rationale_943": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L943 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_960": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L960 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_967": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L967 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_973": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L973 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_976": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L976 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_986": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L986 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_996": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L996 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_997": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L997 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rung": "Rung" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L18 | neighbors=[agent.py] | lang=en
- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_cli_configstore_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L58 | neighbors=[ConfigStore] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-172.json

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
