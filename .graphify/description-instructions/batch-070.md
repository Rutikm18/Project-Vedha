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

- "agent_agent_rationale_662": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L662 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_667": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L667 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_672": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L672 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_710": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L710 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_763": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L763 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rung": "Rung" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L18 | neighbors=[agent.py] | lang=en
- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_agent_ws_test_testresultpayloadwrapsmanagercontract": "TestResultPayloadWrapsManagerContract()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L478 | neighbors=[agent_ws_test.go] | lang=en
- "agent_agent_ws_test_testwsjsonwriterserializesconcurrentwrites": "TestWSJSONWriterSerializesConcurrentWrites()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L18 | neighbors=[agent_ws_test.go] | lang=en
- "agent_agent_ws_test_testwssessionrequiresatomicclaimfeature": "TestWSSessionRequiresAtomicClaimFeature()" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L77 | neighbors=[agent_ws_test.go] | lang=en
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
- "agent_identityserverstate": "identityServerState" | kind=code-symbol | source=probe-go/agent/state_test.go:L17 | neighbors=[state_test.go] | lang=en
- "agent_identitystate": "identityState" | kind=code-symbol | source=probe-go/agent/state.go:L13 | neighbors=[state.go] | lang=en
- "agent_init_rationale_1": "agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit" | kind=entity | source=probe/agent/__init__.py:L1 | neighbors=[__init__.py] | lang=en
- "agent_job_mapping_test_testadvertisedcapabilitieshaveexecutableplans": "TestAdvertisedCapabilitiesHaveExecutablePlans()" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L11 | neighbors=[job_mapping_test.go] | lang=en
- "agent_license_licenseerror_init": ".__init__()" | kind=code-symbol | source=probe/agent/license.py:L33 | neighbors=[LicenseError] | lang=en
- "agent_license_rationale_1": "license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p" | kind=entity | source=probe/agent/license.py:L1 | neighbors=[license.py] | lang=en

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
