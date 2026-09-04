# Node Description Batch 176 of 332

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

- "agent_engine_rationale_354": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L354 | neighbors=[_applied_tuning()]
- "agent_engine_rationale_367": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L367 | neighbors=[LeaseLostError]
- "agent_engine_rationale_372": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L372 | neighbors=[run_scan()]
- "agent_engine_rationale_374": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L374 | neighbors=[_build_run_stats()]
- "agent_engine_rationale_375": "Serialize effective limits without ever echoing credential values." | kind=entity | source=probe/agent/engine.py:L375 | neighbors=[_applied_tuning()]
- "agent_engine_rationale_385": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L385 | neighbors=[_build_run_stats()]
- "agent_engine_rationale_391": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L391 | neighbors=[_build_run_stats()]
- "agent_engine_rationale_393": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L393 | neighbors=[run_scan()]
- "agent_engine_rationale_412": "Build one consistent result summary for complete and interrupted runs." | kind=entity | source=probe/agent/engine.py:L412 | neighbors=[_build_run_stats()]
- "agent_engine_rationale_426": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L426 | neighbors=[_derive_post_stage()]
- "agent_engine_rationale_437": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L437 | neighbors=[_derive_post_stage()]
- "agent_engine_rationale_443": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L443 | neighbors=[_derive_post_stage()]
- "agent_engine_rationale_46": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L46 | neighbors=[_env_number()]
- "agent_engine_rationale_464": "Return (extra ScanResults to append as facts, a top-level rollup dict).      Pur" | kind=entity | source=probe/agent/engine.py:L464 | neighbors=[_derive_post_stage()]
- "agent_engine_rationale_470": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=probe/agent/engine.py:L470 | neighbors=[_derive_devices()]
- "agent_engine_rationale_475": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L475 | neighbors=[LeaseLostError]
- "agent_engine_rationale_486": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L486 | neighbors=[LeaseLostError]
- "agent_engine_rationale_490": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L490 | neighbors=[_derive_exposure()]
- "agent_engine_rationale_491": "Classify each target's device role from its collected facts (no I/O).     Return" | kind=entity | source=probe/agent/engine.py:L491 | neighbors=[_derive_devices()]
- "agent_engine_rationale_501": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L501 | neighbors=[run_scan()]
- "agent_engine_rationale_51": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L51 | neighbors=[_env_number()]
- "agent_engine_rationale_511": "Reconcile each target's per-vantage reachability into an exposure matrix     (no" | kind=entity | source=probe/agent/engine.py:L511 | neighbors=[_derive_exposure()]
- "agent_engine_rationale_512": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L512 | neighbors=[run_scan()]
- "agent_engine_rationale_515": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L515 | neighbors=[LeaseLostError]
- "agent_engine_rationale_52": "Read a bounded numeric safety setting without trusting the environment." | kind=entity | source=probe/agent/engine.py:L52 | neighbors=[_env_number()]
- "agent_engine_rationale_536": "Raised when Manager fencing revokes the running attempt." | kind=entity | source=probe/agent/engine.py:L536 | neighbors=[LeaseLostError]
- "agent_engine_rationale_541": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L541 | neighbors=[run_scan()]
- "agent_engine_rationale_562": "Execute a scan and return the enriched result bundle.      Args:         scan_ty" | kind=entity | source=probe/agent/engine.py:L562 | neighbors=[run_scan()]
- "agent_engine_rationale_75": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L75 | neighbors=[_error_result()]
- "agent_engine_rationale_77": "Coerce val to float and clamp to [lo, hi]; fall back to default on junk.     Def" | kind=entity | source=probe/agent/engine.py:L77 | neighbors=[_clamp()]
- "agent_engine_rationale_80": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L80 | neighbors=[_error_result()]
- "agent_engine_rationale_81": "Single factory for error result dicts — no copy-paste." | kind=entity | source=probe/agent/engine.py:L81 | neighbors=[_error_result()]
- "agent_engine_rationale_87": "Translate operator-supplied job params into run_engagement() kwargs.      This i" | kind=entity | source=probe/agent/engine.py:L87 | neighbors=[_tuning_from_params()]
- "agent_engine_resolve_scan_type": "resolve_scan_type()" | kind=code-symbol | source=probe/agent/engine.py:L176 | neighbors=[engine.py]
- "agent_explain_plan_rationale_1": "explain_plan.py — \"which scanners will run against this host, and WHY?\"      pyt" | kind=entity | source=probe/agent/explain_plan.py:L1 | neighbors=[explain_plan.py]
- "agent_explain_plan_rationale_44": "Recreate this branch's decision and say, in one line, what drove it." | kind=entity | source=probe/agent/explain_plan.py:L44 | neighbors=[_why()]
- "agent_hw_bind_rationale_1": "hw_bind.py — hardware fingerprinting for binary host-locking.  The compiled bina" | kind=entity | source=probe/agent/hw_bind.py:L1 | neighbors=[hw_bind.py]
- "agent_hw_bind_rationale_20": "Raised when the binary is running on an unauthorized machine." | kind=entity | source=probe/agent/hw_bind.py:L20 | neighbors=[HWBindError]
- "agent_hw_bind_rationale_24": "Deterministic per-machine fingerprint built from stable hardware IDs.      Combi" | kind=entity | source=probe/agent/hw_bind.py:L24 | neighbors=[get_hw_id()]
- "agent_hw_bind_rationale_35": "Verify the binary is running on the machine it was compiled for.      Reads HW_B" | kind=entity | source=probe/agent/hw_bind.py:L35 | neighbors=[check_hw_bind()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-175.json

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
