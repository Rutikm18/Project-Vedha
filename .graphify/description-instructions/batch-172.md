# Node Description Batch 173 of 336

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

- "agent_agent_rationale_1045": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L1045 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_1047": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L1047 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_1049": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1049 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_1058": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1058 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_1064": "Retry durable result files using the acknowledged HTTP result path." | kind=entity | source=probe/agent/agent.py:L1064 | neighbors=[_flush_spool_over_http()] | lang=en
- "agent_agent_rationale_1068": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1068 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_107": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L107 | neighbors=[_result_summary()] | lang=en
- "agent_agent_rationale_1077": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L1077 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_1080": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1080 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_1092": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1092 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_1117": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1117 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_1124": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L1124 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_1129": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1129 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_1140": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1140 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_1150": "Request UI approval, poll, prove key possession, and activate." | kind=entity | source=probe/agent/agent.py:L1150 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_1163": "Request UI approval, poll, prove key possession, and activate.      `_recreate_b" | kind=entity | source=probe/agent/agent.py:L1163 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_117": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L117 | neighbors=[_result_summary()] | lang=en
- "agent_agent_rationale_1172": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L1172 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_118": "One-line, transparent summary of what a scan actually found so the operator" | kind=entity | source=probe/agent/agent.py:L118 | neighbors=[_result_summary()] | lang=en
- "agent_agent_rationale_1187": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1187 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_1189": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1189 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_1213": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1213 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_1221": "Load or atomically create the probe's Ed25519 enrollment identity." | kind=entity | source=probe/agent/agent.py:L1221 | neighbors=[_load_or_create_signing_identity()] | lang=en
- "agent_agent_rationale_1223": "Request UI approval, poll, prove key possession, and activate.      `_recreate_b" | kind=entity | source=probe/agent/agent.py:L1223 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_1231": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1231 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_1255": "Request UI approval, poll, prove key possession, and activate.      `_recreate_b" | kind=entity | source=probe/agent/agent.py:L1255 | neighbors=[_enroll_device()] | lang=en
- "agent_agent_rationale_131": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L131 | neighbors=[_classify_connection_error()] | lang=en
- "agent_agent_rationale_1323": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1323 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_1371": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1371 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_141": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L141 | neighbors=[_classify_connection_error()] | lang=en
- "agent_agent_rationale_142": "Map a low-level connection exception to (reason, how-to-fix)." | kind=entity | source=probe/agent/agent.py:L142 | neighbors=[_classify_connection_error()] | lang=en
- "agent_agent_rationale_1451": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1451 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_1483": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L1483 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_157": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L157 | neighbors=[_manager_reachable()] | lang=en
- "agent_agent_rationale_167": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L167 | neighbors=[_manager_reachable()] | lang=en
- "agent_agent_rationale_172": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L172 | neighbors=[_wait_for_manager()] | lang=en
- "agent_agent_rationale_179": "GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net." | kind=entity | source=probe/agent/agent.py:L179 | neighbors=[_manager_reachable()] | lang=en
- "agent_agent_rationale_182": "Bounded reachability preflight. Proceeds the moment the Manager answers     /hea" | kind=entity | source=probe/agent/agent.py:L182 | neighbors=[_wait_for_manager()] | lang=en
- "agent_agent_rationale_199": "Poll for work. Auth failures (TransportError) and transient network     failures" | kind=entity | source=probe/agent/agent.py:L199 | neighbors=[_poll_jobs_or_empty()] | lang=en
- "agent_agent_rationale_210": "Auto-troubleshoot the single silent killer of job execution: a scan     ceiling" | kind=entity | source=probe/agent/agent.py:L210 | neighbors=[_preflight_scope_check()] | lang=en

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
