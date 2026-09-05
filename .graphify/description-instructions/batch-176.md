# Node Description Batch 177 of 336

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

- "agent_agent_rationale_997": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L997 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rung": "Rung" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L18 | neighbors=[agent.py] | lang=en
- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_cli_configstore_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L58 | neighbors=[ConfigStore] | lang=en
- "agent_cli_rationale_574": "Run a bounded capability suite and optionally score known ground truth." | kind=entity | source=probe/agent/cli.py:L574 | neighbors=[cmd_validate()] | lang=en
- "agent_cli_rationale_576": "Run a bounded capability suite and optionally score known ground truth." | kind=entity | source=probe/agent/cli.py:L576 | neighbors=[cmd_validate()] | lang=en
- "agent_device_identity_encode_key": "encode_key()" | kind=code-symbol | source=probe/agent/device_identity.py:L26 | neighbors=[device_identity.py] | lang=en
- "agent_device_identity_generate_signing_identity": "generate_signing_identity()" | kind=code-symbol | source=probe/agent/device_identity.py:L12 | neighbors=[device_identity.py] | lang=en
- "agent_device_identity_rationale_38": "Verify a Manager-signed policy and return its public key for TOFU pinning." | kind=entity | source=probe/agent/device_identity.py:L38 | neighbors=[verify_site_policy()] | lang=en
- "agent_device_identity_sign_b64": "sign_b64()" | kind=code-symbol | source=probe/agent/device_identity.py:L21 | neighbors=[device_identity.py] | lang=en
- "agent_device_identity_signing_public_from_private": "signing_public_from_private()" | kind=code-symbol | source=probe/agent/device_identity.py:L17 | neighbors=[device_identity.py] | lang=en
- "agent_engine_rationale_1": "engine.py — adapt a manager scan job to scanner_module's workflow engine and ret" | kind=entity | source=probe/agent/engine.py:L1 | neighbors=[engine.py] | lang=en
- "agent_engine_rationale_145": "Count concrete open services, not generic host-liveness observations." | kind=entity | source=probe/agent/engine.py:L145 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_148": "syn' for wide sweeps (deep intensity / full-port audit), else 'connect'." | kind=entity | source=probe/agent/engine.py:L148 | neighbors=[_scan_method_for()] | lang=en
- "agent_engine_rationale_154": "syn' for wide sweeps (deep intensity / full-port audit), else 'connect'." | kind=entity | source=probe/agent/engine.py:L154 | neighbors=[_scan_method_for()] | lang=en
- "agent_engine_rationale_157": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L157 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_158": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L158 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_163": "syn' for wide sweeps (deep intensity / full-port audit), else 'connect'." | kind=entity | source=probe/agent/engine.py:L163 | neighbors=[_scan_method_for()] | lang=en
- "agent_engine_rationale_168": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L168 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_181": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L181 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_197": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L197 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_206": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L206 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_207": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L207 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_211": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L211 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_216": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L216 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_217": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L217 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_221": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L221 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_226": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L226 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_231": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L231 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_236": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L236 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_241": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L241 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_257": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L257 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_267": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L267 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_277": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L277 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_283": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L283 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_288": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L288 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_29": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L29 | neighbors=[_error_result()] | lang=en
- "agent_engine_rationale_292": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L292 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_298": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L298 | neighbors=[_hosts_from_facts()] | lang=it

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-176.json

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
