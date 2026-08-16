# Node Description Batch 120 of 209

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

- "agent_transport_rationale_78": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L78 | neighbors=[Transport] | lang=en
- "agent_transport_rationale_80": "HTTP (+ future WebSocket) transport to the manager.      Thread-safe for sequent" | kind=entity | source=probe/agent/transport.py:L80 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_id": ".agent_id()" | kind=code-symbol | source=probe/agent/transport.py:L145 | neighbors=[Transport] | lang=en
- "agent_transport_transport_agent_token": ".agent_token()" | kind=code-symbol | source=probe/agent/transport.py:L153 | neighbors=[Transport] | lang=en
- "agent_transport_transport_auth_header": ".auth_header()" | kind=code-symbol | source=probe/agent/transport.py:L161 | neighbors=[Transport] | lang=en
- "agent_transport_transport_create_enrollment_request": ".create_enrollment_request()" | kind=code-symbol | source=probe/agent/transport.py:L312 | neighbors=[Transport] | lang=en
- "agent_transport_transport_poll_enrollment": ".poll_enrollment()" | kind=code-symbol | source=probe/agent/transport.py:L317 | neighbors=[Transport] | lang=en
- "agent_use_cases_rationale_1": "use_cases.py — the finite, pre-defined library of scan scenarios the manager can" | kind=entity | source=probe/agent/use_cases.py:L1 | neighbors=[use_cases.py] | lang=en
- "agent_use_cases_rationale_119": "Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id" | kind=entity | source=probe/agent/use_cases.py:L119 | neighbors=[resolve()] | lang=en
- "agent_use_cases_rationale_120": "Return (scan_type, profile) for a job.      Resolution order:     1. use_case_id" | kind=entity | source=probe/agent/use_cases.py:L120 | neighbors=[resolve()] | lang=en
- "agent_use_cases_rationale_167": "Return (scan_type, profile, intensity) for a job.      Resolution order:     1." | kind=entity | source=probe/agent/use_cases.py:L167 | neighbors=[resolve()] | lang=en
- "agent_use_cases_rationale_196": "Coerce an int-or-numeric-string to int, else None (non-numeric)." | kind=entity | source=probe/agent/use_cases.py:L196 | neighbors=[_as_int()] | lang=en
- "agent_use_cases_rationale_207": "Map a numeric use-case code → use_case_id (raises on an unknown code)." | kind=entity | source=probe/agent/use_cases.py:L207 | neighbors=[use_case_for_code()] | lang=en
- "agent_use_cases_rationale_218": "Accept an intensity as a number (1/2/3) OR a name; return the name.      None st" | kind=entity | source=probe/agent/use_cases.py:L218 | neighbors=[normalize_intensity()] | lang=en
- "agent_use_cases_rationale_237": "Return (scan_type, profile, intensity) for a job.      Resolution order:     1." | kind=entity | source=probe/agent/use_cases.py:L237 | neighbors=[resolve()] | lang=en
- "agent_validation_rationale_1": "Pure helpers for controlled Probe capability and accuracy validation." | kind=entity | source=probe/agent/validation.py:L1 | neighbors=[validation.py] | lang=en
- "agent_validation_rationale_107": "Validate the small, explicit inventory used for accuracy scoring." | kind=entity | source=probe/agent/validation.py:L107 | neighbors=[validate_ground_truth()] | lang=en
- "agent_validation_rationale_206": "Score promoted inventory against explicit host/port/service/CVE truth." | kind=entity | source=probe/agent/validation.py:L206 | neighbors=[score_inventory()] | lang=en
- "agent_validation_rationale_42": "Resolve suites plus explicit use-cases, preserving first-seen order." | kind=entity | source=probe/agent/validation.py:L42 | neighbors=[resolve_use_cases()] | lang=fr
- "agent_validation_rationale_60": "Require every IP/CIDR target to be fully allowed and not excluded." | kind=entity | source=probe/agent/validation.py:L60 | neighbors=[validate_targets()] | lang=en
- "agent_validation_rationale_94": "Return the conservative number of addresses represented by targets." | kind=entity | source=probe/agent/validation.py:L94 | neighbors=[target_address_count()] | lang=en
- "ai_agent_agentdecisionengine_available": ".available()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L178 | neighbors=[AgentDecisionEngine] | lang=en
- "ai_agent_agentdecisionengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L162 | neighbors=[AgentDecisionEngine] | lang=en
- "ai_hallucination_rationale_1": "HallucinationGuard — post-generation validation of LLM report text against the g" | kind=entity | source=manager/backend/app/ai/hallucination.py:L1 | neighbors=[hallucination.py] | lang=en
- "ai_hallucination_rationale_109": "Run all relevant checks and return a combined verdict:         ``{valid, issues," | kind=entity | source=manager/backend/app/ai/hallucination.py:L109 | neighbors=[.validate()] | lang=en
- "ai_hallucination_rationale_46": "Flag any CVE ID mentioned in ``text`` that isn't in the real finding set." | kind=entity | source=manager/backend/app/ai/hallucination.py:L46 | neighbors=[.validate_cve_claims()] | lang=en
- "ai_hallucination_rationale_61": "Flag CVSS scores in the text that don't match any real score.          ``actual_" | kind=entity | source=manager/backend/app/ai/hallucination.py:L61 | neighbors=[.validate_cvss_scores()] | lang=en
- "ai_hallucination_rationale_90": "Flag destructive-looking commands that shouldn't appear in a fix guide." | kind=entity | source=manager/backend/app/ai/hallucination.py:L90 | neighbors=[.validate_remediation_commands()] | lang=en
- "ai_llm_report_llmreportgenerator_available": ".available()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L106 | neighbors=[LLMReportGenerator] | lang=en
- "ai_llm_report_llmreportgenerator_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L82 | neighbors=[LLMReportGenerator] | lang=en
- "ai_llm_report_rationale_245": "Generate a STRUCTURED, OS-specific remediation plan (dict, not prose)." | kind=entity | source=manager/backend/app/ai/llm_report.py:L245 | neighbors=[.generate_remediation_plan()] | lang=pt
- "ai_llm_report_rationale_356": "Build the structured-remediation prompt. Exploitation signals (EPSS,     exploit" | kind=entity | source=manager/backend/app/ai/llm_report.py:L356 | neighbors=[_remediation_plan_prompt()] | lang=en
- "ai_llm_report_rationale_379": "Fault-tolerant JSON extraction from an LLM reply. Handles markdown fences     an" | kind=entity | source=manager/backend/app/ai/llm_report.py:L379 | neighbors=[_parse_json_response()] | lang=en
- "ai_llm_report_rationale_406": "Extract a step's command(s) and drop any the guard flags as destructive.     Ret" | kind=entity | source=manager/backend/app/ai/llm_report.py:L406 | neighbors=[_safe_commands()] | lang=en
- "ai_llm_report_rationale_424": "Coerce a parsed AI response into the same schema the KB emits, running every" | kind=entity | source=manager/backend/app/ai/llm_report.py:L424 | neighbors=[_normalize_ai_plan()] | lang=en
- "ai_llm_report_rationale_48": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/llm_report.py:L48 | neighbors=[LLMUnavailableError] | lang=en
- "ai_prioritizer_rationale_1": "VulnPrioritizer — ML-based vulnerability prioritisation with a deterministic fal" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[prioritizer.py] | lang=en
- "ai_prioritizer_rationale_111": "Fit an XGBoost regressor on historical findings. ``historical_findings_df``" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L111 | neighbors=[.train()] | lang=en
- "ai_prioritizer_rationale_149": "Return a 0–1000 priority score. Uses the model if trained, else the formula." | kind=entity | source=manager/backend/app/ai/prioritizer.py:L149 | neighbors=[.predict_priority()] | lang=en
- "ai_prioritizer_rationale_159": "Per-feature contribution to this prediction. Uses SHAP when available;         o" | kind=entity | source=manager/backend/app/ai/prioritizer.py:L159 | neighbors=[.explain_prediction()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-119.json

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
