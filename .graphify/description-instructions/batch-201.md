# Node Description Batch 202 of 380

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

- "agent_engine_rationale_501": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L501 | neighbors=[run_scan()]
- "agent_engine_rationale_506": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=probe/agent/engine.py:L506 | neighbors=[_derive_devices()]
- "agent_engine_rationale_51": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L51 | neighbors=[_env_number()]
- "agent_engine_rationale_511": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L511 | neighbors=[_derive_exposure()]
- "agent_engine_rationale_512": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L512 | neighbors=[run_scan()]
- "agent_engine_rationale_515": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L515 | neighbors=[LeaseLostError]
- "agent_engine_rationale_516": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=probe/agent/engine.py:L516 | neighbors=[_derive_devices()]
- "agent_engine_rationale_52": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L52 | neighbors=[_env_number()]
- "agent_engine_rationale_524": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=probe/agent/engine.py:L524 | neighbors=[_derive_devices()]
- "agent_engine_rationale_526": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L526 | neighbors=[_derive_exposure()]
- "agent_engine_rationale_53": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L53 | neighbors=[_env_number()]
- "agent_engine_rationale_54": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L54 | neighbors=[_env_number()]
- "agent_engine_rationale_541": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L541 | neighbors=[run_scan()]
- "agent_engine_rationale_544": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L544 | neighbors=[_derive_exposure()]
- "agent_engine_rationale_551": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L551 | neighbors=[LeaseLostError]
- "agent_engine_rationale_561": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L561 | neighbors=[LeaseLostError]
- "agent_engine_rationale_562": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L562 | neighbors=[run_scan()]
- "agent_engine_rationale_569": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L569 | neighbors=[LeaseLostError]
- "agent_engine_rationale_577": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L577 | neighbors=[run_scan()]
- "agent_engine_rationale_587": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L587 | neighbors=[run_scan()]
- "agent_engine_rationale_597": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L597 | neighbors=[run_scan()]
- "agent_engine_rationale_75": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L75 | neighbors=[_error_result()]
- "agent_engine_rationale_77": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L77 | neighbors=[_clamp()]
- "agent_engine_rationale_80": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L80 | neighbors=[_error_result()]
- "agent_engine_rationale_81": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L81 | neighbors=[_error_result()]
- "agent_engine_rationale_82": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L82 | neighbors=[_error_result()]
- "agent_engine_rationale_83": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L83 | neighbors=[_error_result()]
- "agent_engine_rationale_87": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L87 | neighbors=[_tuning_from_params()]
- "agent_engine_resolve_scan_type": "resolve_scan_type()" | kind=code-symbol | source=probe/agent/engine.py:L192 | neighbors=[engine.py]
- "agent_exit_state_class_for_code": "class_for_code()" | kind=code-symbol | source=probe/agent/exit_state.py:L58 | neighbors=[exit_state.py]
- "agent_exit_state_parse_stderr_line": "parse_stderr_line()" | kind=code-symbol | source=probe/agent/exit_state.py:L115 | neighbors=[exit_state.py]
- "agent_exit_state_rationale_1": "exit_state.py — the wide exit-state channel (0b contract).  Replaces overloaded" | kind=entity | source=probe/agent/exit_state.py:L1 | neighbors=[exit_state.py]
- "agent_exit_state_stderr_line": "stderr_line()" | kind=code-symbol | source=probe/agent/exit_state.py:L111 | neighbors=[exit_state.py]
- "agent_explain_plan_rationale_1": "explain_plan.py — \"which scanners will run against this host, and WHY?\"      pyt" | kind=entity | source=probe/agent/explain_plan.py:L1 | neighbors=[explain_plan.py]
- "agent_explain_plan_rationale_44": "Recreate this branch's decision and say, in one line, what drove it." | kind=entity | source=probe/agent/explain_plan.py:L44 | neighbors=[_why()]
- "agent_hw_bind_rationale_1": "hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina" | kind=entity | source=probe/agent/hw_bind.py:L1 | neighbors=[hw_bind.py]
- "agent_hw_bind_rationale_20": "Raised when the binary is running on an unauthorized machine." | kind=entity | source=probe/agent/hw_bind.py:L20 | neighbors=[HWBindError]
- "agent_hw_bind_rationale_24": "Deterministic per-machine fingerprint built from stable hardware IDs.      Combi" | kind=entity | source=probe/agent/hw_bind.py:L24 | neighbors=[get_hw_id()]
- "agent_hw_bind_rationale_35": "Verify the binary is running on the machine it was compiled for.      Reads HW_B" | kind=entity | source=probe/agent/hw_bind.py:L35 | neighbors=[check_hw_bind()]
- "agent_init_rationale_1": "agent — the probe transport layer (sealed, push-driven, hardware-bound).  Archit" | kind=entity | source=probe/agent/__init__.py:L1 | neighbors=[__init__.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-201.json

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
