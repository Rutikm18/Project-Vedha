# Node Description Batch 139 of 380

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

- "agent_engine_facts_from_cache": "_facts_from_cache()" | kind=code-symbol | source=probe/agent/engine.py:L334 | neighbors=[engine.py, run_scan()]
- "agent_engine_rationale_178": "syn' for wide sweeps (deep intensity / full-port audit), else 'connect'." | kind=entity | source=probe/agent/engine.py:L178 | neighbors=[_scan_method_for(), _tuning_from_params()]
- "agent_engine_rationale_191": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L191 | neighbors=[_clamp(), _job_runtime_seconds()]
- "agent_engine_rationale_201": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L201 | neighbors=[_job_runtime_seconds(), _tuning_from_params()]
- "agent_engine_rationale_437": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L437 | neighbors=[_build_run_stats(), _derive_post_stage()]
- "agent_engine_rationale_536": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L536 | neighbors=[_derive_exposure(), LeaseLostError]
- "agent_exit_state_read": "read()" | kind=code-symbol | source=probe/agent/exit_state.py:L103 | neighbors=[exit_state.py, from_json()]
- "agent_exit_state_to_json": "to_json()" | kind=code-symbol | source=probe/agent/exit_state.py:L78 | neighbors=[exit_state.py, write()]
- "agent_exit_state_write": "write()" | kind=code-symbol | source=probe/agent/exit_state.py:L98 | neighbors=[exit_state.py, to_json()]
- "agent_explain_plan_main": "main()" | kind=code-symbol | source=probe/agent/explain_plan.py:L104 | neighbors=[explain_plan.py, _print_table()]
- "agent_instance_lock_release_instance_lock": "release_instance_lock()" | kind=code-symbol | source=probe/agent/instance_lock.py:L134 | neighbors=[instance_lock.py, Release explicitly. Process exit would …]
- "agent_job_admission_manager_ip_from_env": "manager_ip_from_env()" | kind=code-symbol | source=probe/agent/job_admission.py:L21 | neighbors=[job_admission.py, Resolve the Manager's IP from PLATFORM_…]
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=probe/agent/license.py:L45 | neighbors=[license.py, verify_license()]
- "agent_local_run_scope_file": "_scope_file()" | kind=code-symbol | source=probe/agent/local_run.py:L38 | neighbors=[local_run.py, _main()]
- "agent_obs_heartbeat_metrics": "heartbeat_metrics()" | kind=code-symbol | source=probe/agent/obs.py:L51 | neighbors=[obs.py, Bounded-cardinality fleet-health signal…]
- "agent_obs_is_sensitive": "_is_sensitive()" | kind=code-symbol | source=probe/agent/obs.py:L18 | neighbors=[obs.py, redact()]
- "agent_obs_log_line": "log_line()" | kind=code-symbol | source=probe/agent/obs.py:L28 | neighbors=[obs.py, redact()]
- "agent_release_main": "main()" | kind=code-symbol | source=probe/agent/release.py:L65 | neighbors=[release.py, sbom_from_requirements()]
- "agent_release_parse_requirements": "parse_requirements()" | kind=code-symbol | source=probe/agent/release.py:L38 | neighbors=[release.py, sbom_from_requirements()]
- "agent_release_sha256_manifest": "sha256_manifest()" | kind=code-symbol | source=probe/agent/release.py:L25 | neighbors=[release.py, sha256_file()]
- "agent_release_verify_manifest": "verify_manifest()" | kind=code-symbol | source=probe/agent/release.py:L29 | neighbors=[release.py, sha256_file()]
- "agent_result_queue_host_sealed_cipher": "host_sealed_cipher()" | kind=code-symbol | source=probe/agent/result_queue.py:L36 | neighbors=[result_queue.py, Fernet cipher keyed by a per-host key f…]
- "agent_result_queue_nullcipher_decrypt": ".decrypt()" | kind=code-symbol | source=probe/agent/result_queue.py:L33 | neighbors=[NullCipher, ._read()]
- "agent_result_queue_nullcipher_encrypt": ".encrypt()" | kind=code-symbol | source=probe/agent/result_queue.py:L32 | neighbors=[NullCipher, .enqueue()]
- "agent_result_queue_queuestats": "QueueStats" | kind=code-symbol | source=probe/agent/result_queue.py:L69 | neighbors=[result_queue.py, .stats()]
- "agent_result_queue_record": "Record" | kind=code-symbol | source=probe/agent/result_queue.py:L61 | neighbors=[result_queue.py, ._read()]
- "agent_result_queue_resultqueue_ack": ".ack()" | kind=code-symbol | source=probe/agent/result_queue.py:L160 | neighbors=[ResultQueue, ._find()]
- "agent_result_queue_resultqueue_atomic_write": "._atomic_write()" | kind=code-symbol | source=probe/agent/result_queue.py:L111 | neighbors=[ResultQueue, .enqueue()]
- "agent_result_queue_resultqueue_prune": ".prune()" | kind=code-symbol | source=probe/agent/result_queue.py:L165 | neighbors=[ResultQueue, .pending()]
- "agent_result_queue_resultqueue_should_backpressure": ".should_backpressure()" | kind=code-symbol | source=probe/agent/result_queue.py:L181 | neighbors=[ResultQueue, ._files()]
- "agent_result_spool_resultspool_at_capacity": ".at_capacity()" | kind=code-symbol | source=probe/agent/result_spool.py:L235 | neighbors=[Whether new jobs must pause until pendi…, ResultSpool]
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…]
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…]
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…]
- "agent_scope_model_classify_interface": "classify_interface()" | kind=code-symbol | source=probe/agent/scope_model.py:L47 | neighbors=[scope_model.py, parse_linux_ip_json()]
- "agent_scope_model_interface": "Interface" | kind=code-symbol | source=probe/agent/scope_model.py:L24 | neighbors=[scope_model.py, parse_linux_ip_json()]
- "agent_scope_model_refusal_reason": "refusal_reason()" | kind=code-symbol | source=probe/agent/scope_model.py:L146 | neighbors=[scope_model.py, Refuse LAN scanning from inside a conta…]
- "agent_scope_model_validate_scope": "validate_scope()" | kind=code-symbol | source=probe/agent/scope_model.py:L104 | neighbors=[scope_model.py, validate_segment()]
- "agent_scope_model_validate_segment": "validate_segment()" | kind=code-symbol | source=probe/agent/scope_model.py:L85 | neighbors=[scope_model.py, validate_scope()]
- "agent_scope_validator_rationale_58": "Fetch the engagement's authoritative scope from the manager.      Args:" | kind=entity | source=probe/agent/scope_validator.py:L58 | neighbors=[fetch_engagement_scope(), validate_targets_in_scope()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-138.json

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
