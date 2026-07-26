# Node Description Batch 64 of 104

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

- "agent_agent_rung": "Rung" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L18 | neighbors=[agent.py] | lang=en
- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_scanningagent_handle_shutdown": "._handle_shutdown()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L728 | neighbors=[ScanningAgent] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_agent_vaultcredentialfetcher_init": ".__init__()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L78 | neighbors=[VaultCredentialFetcher] | lang=en
- "agent_cli_configstore_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L54 | neighbors=[ConfigStore] | lang=en
- "agent_engine_rationale_1": "engine.py — adapt a manager scan job to scanner_module's workflow engine and ret" | kind=entity | source=probe/agent/engine.py:L1 | neighbors=[engine.py] | lang=en
- "agent_engine_rationale_145": "Count concrete open services, not generic host-liveness observations." | kind=entity | source=probe/agent/engine.py:L145 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_157": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L157 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_29": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L29 | neighbors=[_error_result()] | lang=en
- "agent_engine_rationale_77": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L77 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_87": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L87 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_resolve_scan_type": "resolve_scan_type()" | kind=code-symbol | source=probe/agent/engine.py:L67 | neighbors=[engine.py] | lang=en
- "agent_hw_bind_rationale_1": "hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina" | kind=entity | source=probe/agent/hw_bind.py:L1 | neighbors=[hw_bind.py] | lang=en
- "agent_hw_bind_rationale_20": "Raised when the binary is running on an unauthorized machine." | kind=entity | source=probe/agent/hw_bind.py:L20 | neighbors=[HWBindError] | lang=en
- "agent_hw_bind_rationale_24": "Deterministic per-machine fingerprint built from stable hardware IDs.      Combi" | kind=entity | source=probe/agent/hw_bind.py:L24 | neighbors=[get_hw_id()] | lang=en
- "agent_hw_bind_rationale_35": "Verify the binary is running on the machine it was compiled for.      Reads HW_B" | kind=entity | source=probe/agent/hw_bind.py:L35 | neighbors=[check_hw_bind()] | lang=en
- "agent_init_rationale_1": "agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit" | kind=entity | source=probe/agent/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "agent_license_licenseerror_init": ".__init__()" | kind=code-symbol | source=probe/agent/license.py:L33 | neighbors=[LicenseError] | lang=en
- "agent_license_rationale_1": "license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p" | kind=entity | source=probe/agent/license.py:L1 | neighbors=[license.py] | lang=en
- "agent_license_rationale_105": "Combined startup gauntlet: HW bind → license check. Fails fast.      This is the" | kind=entity | source=probe/agent/license.py:L105 | neighbors=[gauntlet()] | lang=en
- "agent_license_rationale_39": "Stable per-machine ID, derived from hw_bind's hardware fingerprint." | kind=entity | source=probe/agent/license.py:L39 | neighbors=[host_fingerprint()] | lang=en
- "agent_license_rationale_54": "Returns the license payload dict if valid; raises LicenseError otherwise.     To" | kind=entity | source=probe/agent/license.py:L54 | neighbors=[verify_license()] | lang=en
- "agent_license_rationale_88": "The gate the agent calls at startup. Honors LICENSE_ENFORCED and     reads the t" | kind=entity | source=probe/agent/license.py:L88 | neighbors=[check_license()] | lang=en
- "agent_result_spool_rationale_1": "result_spool.py — local result persistence with upload retry.  When the probe co" | kind=entity | source=probe/agent/result_spool.py:L1 | neighbors=[result_spool.py] | lang=en
- "agent_result_spool_rationale_130": "Re-attempt upload of all previously spooled results.          Called once at pro" | kind=entity | source=probe/agent/result_spool.py:L130 | neighbors=[.flush_spool()] | lang=en
- "agent_result_spool_rationale_153": "Number of pending (unsubmitted) results in the spool." | kind=entity | source=probe/agent/result_spool.py:L153 | neighbors=[.spool_count()] | lang=en
- "agent_result_spool_rationale_25": "Persists scan results locally and retries failed uploads." | kind=entity | source=probe/agent/result_spool.py:L25 | neighbors=[ResultSpool] | lang=en
- "agent_result_spool_rationale_40": "Atomically write a result payload to the spool directory.          Returns the s" | kind=entity | source=probe/agent/result_spool.py:L40 | neighbors=[.save()] | lang=en
- "agent_result_spool_rationale_62": "Check if a spooled result exists for this job." | kind=entity | source=probe/agent/result_spool.py:L62 | neighbors=[.exists()] | lang=en
- "agent_result_spool_rationale_66": "Load a previously spooled result, returning None if missing/corrupt." | kind=entity | source=probe/agent/result_spool.py:L66 | neighbors=[.load()] | lang=pt
- "agent_result_spool_rationale_77": "Remove the spool file for a successfully uploaded result." | kind=entity | source=probe/agent/result_spool.py:L77 | neighbors=[.remove()] | lang=en
- "agent_result_spool_rationale_88": "Attempt to upload a result with retries and local spool as fallback.          Ar" | kind=entity | source=probe/agent/result_spool.py:L88 | neighbors=[.submit_with_retry()] | lang=en
- "agent_result_spool_resultspool_init": ".__init__()" | kind=code-symbol | source=probe/agent/result_spool.py:L27 | neighbors=[ResultSpool] | lang=en
- "agent_scope_crypt_rationale_1": "scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.  T" | kind=entity | source=probe/agent/scope_crypt.py:L1 | neighbors=[scope_crypt.py] | lang=en
- "agent_scope_crypt_rationale_151": "encrypt_scope() returning a base64 string suitable for JSON transport." | kind=entity | source=probe/agent/scope_crypt.py:L151 | neighbors=[encrypt_scope_b64()] | lang=en
- "agent_scope_crypt_rationale_156": "decrypt_scope() accepting a base64 string from JSON transport." | kind=entity | source=probe/agent/scope_crypt.py:L156 | neighbors=[decrypt_scope_b64()] | lang=en
- "agent_scope_crypt_rationale_161": "Decode a base64-encoded X25519 public key to raw bytes." | kind=entity | source=probe/agent/scope_crypt.py:L161 | neighbors=[pubkey_to_bytes()] | lang=en
- "agent_scope_crypt_rationale_166": "Encode raw X25519 public key bytes to a base64 string." | kind=entity | source=probe/agent/scope_crypt.py:L166 | neighbors=[bytes_to_pubkey_b64()] | lang=en
- "agent_scope_crypt_rationale_44": "Generate a fresh X25519 keypair.      Returns (private_key_bytes, public_key_byt" | kind=entity | source=probe/agent/scope_crypt.py:L44 | neighbors=[generate_identity()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-063.json

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
