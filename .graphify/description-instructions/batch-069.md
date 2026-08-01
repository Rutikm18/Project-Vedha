# Node Description Batch 70 of 119

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

- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_cli_configstore_init": ".__init__()" | kind=code-symbol | source=probe/agent/cli.py:L56 | neighbors=[ConfigStore] | lang=en
- "agent_cli_rationale_574": "Run a bounded capability suite and optionally score known ground truth." | kind=entity | source=probe/agent/cli.py:L574 | neighbors=[cmd_validate()] | lang=en
- "agent_engine_rationale_1": "engine.py — adapt a manager scan job to scanner_module's workflow engine and ret" | kind=entity | source=probe/agent/engine.py:L1 | neighbors=[engine.py] | lang=en
- "agent_engine_rationale_145": "Count concrete open services, not generic host-liveness observations." | kind=entity | source=probe/agent/engine.py:L145 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_157": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L157 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_158": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L158 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_168": "Return the effective whole-job deadline; callers can only reduce it." | kind=entity | source=probe/agent/engine.py:L168 | neighbors=[_job_runtime_seconds()] | lang=en
- "agent_engine_rationale_178": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L178 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_rationale_236": "Count unique open network endpoints, not every confirming scanner fact." | kind=entity | source=probe/agent/engine.py:L236 | neighbors=[_count_open_port_facts()] | lang=en
- "agent_engine_rationale_257": "Build promotion-ready hosts without duplicating scanner facts per port." | kind=entity | source=probe/agent/engine.py:L257 | neighbors=[_hosts_from_facts()] | lang=it
- "agent_engine_rationale_29": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L29 | neighbors=[_error_result()] | lang=en
- "agent_engine_rationale_305": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L305 | neighbors=[_applied_tuning()] | lang=en
- "agent_engine_rationale_336": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L336 | neighbors=[_build_run_stats()] | lang=en
- "agent_engine_rationale_372": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L372 | neighbors=[run_scan()] | lang=en
- "agent_engine_rationale_46": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L46 | neighbors=[_env_number()] | lang=en
- "agent_engine_rationale_75": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L75 | neighbors=[_error_result()] | lang=en
- "agent_engine_rationale_77": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L77 | neighbors=[_clamp()] | lang=en
- "agent_engine_rationale_87": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L87 | neighbors=[_tuning_from_params()] | lang=en
- "agent_engine_resolve_scan_type": "resolve_scan_type()" | kind=code-symbol | source=probe/agent/engine.py:L128 | neighbors=[engine.py] | lang=en
- "agent_hw_bind_rationale_1": "hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina" | kind=entity | source=probe/agent/hw_bind.py:L1 | neighbors=[hw_bind.py] | lang=en
- "agent_hw_bind_rationale_20": "Raised when the binary is running on an unauthorized machine." | kind=entity | source=probe/agent/hw_bind.py:L20 | neighbors=[HWBindError] | lang=en
- "agent_hw_bind_rationale_24": "Deterministic per-machine fingerprint built from stable hardware IDs.      Combi" | kind=entity | source=probe/agent/hw_bind.py:L24 | neighbors=[get_hw_id()] | lang=en
- "agent_hw_bind_rationale_35": "Verify the binary is running on the machine it was compiled for.      Reads HW_B" | kind=entity | source=probe/agent/hw_bind.py:L35 | neighbors=[check_hw_bind()] | lang=en
- "agent_init_rationale_1": "agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit" | kind=entity | source=probe/agent/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "agent_license_licenseerror_init": ".__init__()" | kind=code-symbol | source=probe/agent/license.py:L30 | neighbors=[LicenseError] | lang=en
- "agent_license_rationale_1": "license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p" | kind=entity | source=probe/agent/license.py:L1 | neighbors=[license.py] | lang=en
- "agent_license_rationale_102": "Combined startup gauntlet: HW bind → license check. Fails fast.      This is the" | kind=entity | source=probe/agent/license.py:L102 | neighbors=[gauntlet()] | lang=en
- "agent_license_rationale_105": "Combined startup gauntlet: HW bind → license check. Fails fast.      This is the" | kind=entity | source=probe/agent/license.py:L105 | neighbors=[gauntlet()] | lang=en
- "agent_license_rationale_36": "Stable per-machine ID, derived from hw_bind's hardware fingerprint." | kind=entity | source=probe/agent/license.py:L36 | neighbors=[host_fingerprint()] | lang=en
- "agent_license_rationale_39": "Stable per-machine ID, derived from hw_bind's hardware fingerprint." | kind=entity | source=probe/agent/license.py:L39 | neighbors=[host_fingerprint()] | lang=en
- "agent_license_rationale_51": "Returns the license payload dict if valid; raises LicenseError otherwise.     To" | kind=entity | source=probe/agent/license.py:L51 | neighbors=[verify_license()] | lang=en
- "agent_license_rationale_54": "Returns the license payload dict if valid; raises LicenseError otherwise.     To" | kind=entity | source=probe/agent/license.py:L54 | neighbors=[verify_license()] | lang=en
- "agent_license_rationale_85": "The gate the agent calls at startup. Honors LICENSE_ENFORCED and     reads the t" | kind=entity | source=probe/agent/license.py:L85 | neighbors=[check_license()] | lang=en
- "agent_license_rationale_88": "The gate the agent calls at startup. Honors LICENSE_ENFORCED and     reads the t" | kind=entity | source=probe/agent/license.py:L88 | neighbors=[check_license()] | lang=en
- "agent_result_spool_rationale_1": "result_spool.py — local result persistence with upload retry.  When the probe co" | kind=entity | source=probe/agent/result_spool.py:L1 | neighbors=[result_spool.py] | lang=en
- "agent_result_spool_rationale_102": "Remove the spool file for a successfully uploaded result." | kind=entity | source=probe/agent/result_spool.py:L102 | neighbors=[.remove()] | lang=en
- "agent_result_spool_rationale_114": "Attempt to upload a result with retries and local spool as fallback.          Ar" | kind=entity | source=probe/agent/result_spool.py:L114 | neighbors=[.submit_with_retry()] | lang=en
- "agent_result_spool_rationale_130": "Re-attempt upload of all previously spooled results.          Called once at pro" | kind=entity | source=probe/agent/result_spool.py:L130 | neighbors=[.flush_spool()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-069.json

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
