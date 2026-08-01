# Node Description Batch 71 of 119

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

- "agent_result_spool_rationale_62": "Check if a spooled result exists for this job." | kind=entity | source=probe/agent/result_spool.py:L62 | neighbors=[.exists()] | lang=en
- "agent_result_spool_rationale_66": "Load a previously spooled result, returning None if missing/corrupt." | kind=entity | source=probe/agent/result_spool.py:L66 | neighbors=[.load()] | lang=pt
- "agent_result_spool_rationale_77": "Remove the spool file for a successfully uploaded result." | kind=entity | source=probe/agent/result_spool.py:L77 | neighbors=[.remove()] | lang=en
- "agent_result_spool_rationale_87": "Check if a spooled result exists for this job." | kind=entity | source=probe/agent/result_spool.py:L87 | neighbors=[.exists()] | lang=en
- "agent_result_spool_rationale_88": "Attempt to upload a result with retries and local spool as fallback.          Ar" | kind=entity | source=probe/agent/result_spool.py:L88 | neighbors=[.submit_with_retry()] | lang=en
- "agent_result_spool_rationale_91": "Load a previously spooled result, returning None if missing/corrupt." | kind=entity | source=probe/agent/result_spool.py:L91 | neighbors=[.load()] | lang=pt
- "agent_result_spool_resultspool_init": ".__init__()" | kind=code-symbol | source=probe/agent/result_spool.py:L29 | neighbors=[ResultSpool] | lang=en
- "agent_scope_crypt_rationale_1": "scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T" | kind=entity | source=probe/agent/scope_crypt.py:L1 | neighbors=[scope_crypt.py] | lang=en
- "agent_scope_crypt_rationale_151": "encrypt_scope() returning a base64 string suitable for JSON transport." | kind=entity | source=probe/agent/scope_crypt.py:L151 | neighbors=[encrypt_scope_b64()] | lang=en
- "agent_scope_crypt_rationale_156": "decrypt_scope() accepting a base64 string from JSON transport." | kind=entity | source=probe/agent/scope_crypt.py:L156 | neighbors=[decrypt_scope_b64()] | lang=en
- "agent_scope_crypt_rationale_161": "Decode a base64-encoded X25519 public key to raw bytes." | kind=entity | source=probe/agent/scope_crypt.py:L161 | neighbors=[pubkey_to_bytes()] | lang=en
- "agent_scope_crypt_rationale_166": "Encode raw X25519 public key bytes to a base64 string." | kind=entity | source=probe/agent/scope_crypt.py:L166 | neighbors=[bytes_to_pubkey_b64()] | lang=en
- "agent_scope_crypt_rationale_44": "Generate a fresh X25519 keypair.      Returns (private_key_bytes, public_key_byt" | kind=entity | source=probe/agent/scope_crypt.py:L44 | neighbors=[generate_identity()] | lang=pt
- "agent_scope_crypt_rationale_56": "Encrypt scope JSON to a specific probe's public key.      Args:         scope_js" | kind=entity | source=probe/agent/scope_crypt.py:L56 | neighbors=[encrypt_scope()] | lang=en
- "agent_scope_crypt_rationale_98": "Decrypt a scope blob using the probe's private key.      Args:         blob: Wir" | kind=entity | source=probe/agent/scope_crypt.py:L98 | neighbors=[decrypt_scope()] | lang=en
- "agent_scope_validator_rationale_1": "scope_validator.py — defense-in-depth scope re-validation for the probe.  The pr" | kind=entity | source=probe/agent/scope_validator.py:L1 | neighbors=[scope_validator.py] | lang=en
- "agent_scope_validator_rationale_121": "Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl" | kind=entity | source=probe/agent/scope_validator.py:L121 | neighbors=[merge_exclusions()] | lang=en
- "agent_scope_validator_rationale_124": "Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)." | kind=entity | source=probe/agent/scope_validator.py:L124 | neighbors=[targets_in_excludes()] | lang=en
- "agent_scope_validator_rationale_158": "Merge engagement-level exclusions with per-job exclusions.      Returns a dedupl" | kind=entity | source=probe/agent/scope_validator.py:L158 | neighbors=[merge_exclusions()] | lang=en
- "agent_scope_validator_rationale_28": "Parse one IP, CIDR, or inclusive IP range into covering networks.      ``None``" | kind=entity | source=probe/agent/scope_validator.py:L28 | neighbors=[_networks_for_target()] | lang=en
- "agent_scope_validator_rationale_31": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L31 | neighbors=[fetch_engagement_scope()] | lang=en
- "agent_scope_validator_rationale_85": "Check targets against the authoritative scope CIDRs.      Returns (allowed, reje" | kind=entity | source=probe/agent/scope_validator.py:L85 | neighbors=[validate_targets_in_scope()] | lang=en
- "agent_scope_validator_rationale_88": "Remove targets that fall inside any excluded CIDR.      Returns (kept, dropped)." | kind=entity | source=probe/agent/scope_validator.py:L88 | neighbors=[targets_in_excludes()] | lang=en
- "agent_task_runner_rationale_1": "task_runner.py — orchestrates the full lifecycle of a single scan job.  Given a" | kind=entity | source=probe/agent/task_runner.py:L1 | neighbors=[task_runner.py] | lang=en
- "agent_task_runner_rationale_28": "Structured result from running one scan job." | kind=entity | source=probe/agent/task_runner.py:L28 | neighbors=[JobResult] | lang=en
- "agent_task_runner_rationale_283": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L283 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_30": "Structured result from running one scan job." | kind=entity | source=probe/agent/task_runner.py:L30 | neighbors=[JobResult] | lang=en
- "agent_task_runner_rationale_397": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L397 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_399": "Submit the result, with spool-and-retry if available." | kind=entity | source=probe/agent/task_runner.py:L399 | neighbors=[._submit_or_spool()] | lang=en
- "agent_task_runner_rationale_40": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L40 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_42": "Orchestrates one scan job's lifecycle.      The runner holds injected dependenci" | kind=entity | source=probe/agent/task_runner.py:L42 | neighbors=[TaskRunner] | lang=en
- "agent_task_runner_rationale_56": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L56 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_57": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L57 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_58": "Args:             http_get:       Callback for authenticated GET (from Transport" | kind=entity | source=probe/agent/task_runner.py:L58 | neighbors=[.__init__()] | lang=en
- "agent_task_runner_rationale_80": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L80 | neighbors=[.run_job()] | lang=pt
- "agent_task_runner_rationale_87": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L87 | neighbors=[.run_job()] | lang=pt
- "agent_task_runner_rationale_89": "Execute a complete scan job lifecycle.          Args:             job: Job dict" | kind=entity | source=probe/agent/task_runner.py:L89 | neighbors=[.run_job()] | lang=pt
- "agent_tools_mergehosts": "mergeHosts()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L81 | neighbors=[tools.ts] | lang=en
- "agent_tools_runonephase": "runOnePhase()" | kind=code-symbol | source=manager/frontend/lib/agent/tools.ts:L40 | neighbors=[tools.ts] | lang=en
- "agent_transport_rationale_1": "transport.py — all manager communication (HTTP + WebSocket) in one place.  Encap" | kind=entity | source=probe/agent/transport.py:L1 | neighbors=[transport.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-070.json

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
