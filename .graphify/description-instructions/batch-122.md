# Node Description Batch 123 of 227

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "agent_agent_rationale_586": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L586 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_593": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L593 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_601": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L601 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_607": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L607 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_609": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L609 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_612": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L612 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_614": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L614 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_621": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L621 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_63": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L63 | neighbors=[_load_env()] | lang=en
- "agent_agent_rationale_65": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L65 | neighbors=[_load_env()] | lang=en
- "agent_agent_rationale_662": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L662 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_667": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L667 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_668": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L668 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_669": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L669 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_670": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L670 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_672": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L672 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_692": "Acknowledge an offer without executing it before claim confirmation." | kind=entity | source=probe/agent/agent.py:L692 | neighbors=[_ws_stage_job_offer()] | lang=en
- "agent_agent_rationale_706": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L706 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_707": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L707 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_716": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L716 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_723": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L723 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_724": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L724 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_736": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L736 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_737": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L737 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_744": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L744 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_763": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L763 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_769": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L769 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_783": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L783 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_784": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L784 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_805": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L805 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_81": "Return no work for transient poll failures without hiding auth failures." | kind=entity | source=probe/agent/agent.py:L81 | neighbors=[_poll_jobs_or_empty()] | lang=en
- "agent_agent_rationale_831": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L831 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_832": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L832 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_842": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L842 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_859": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L859 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_872": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L872 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_880": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L880 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_881": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L881 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_913": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L913 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_914": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L914 | neighbors=[_enroll_device()] | lang=en

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
