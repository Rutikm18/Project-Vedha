# Node Description Batch 298 of 380

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

- "scripts_startup_validator_rationale_311": "Verifies actual database connectivity at startup." | kind=entity | source=manager/backend/scripts/startup_validator.py:L311 | neighbors=[DatabaseConnectivityValidator] | lang=en
- "scripts_startup_validator_rationale_355": "Verifies Redis connectivity at startup." | kind=entity | source=manager/backend/scripts/startup_validator.py:L355 | neighbors=[RedisConnectivityValidator] | lang=en
- "scripts_startup_validator_rationale_397": "Run all validators. Use in FastAPI lifespan:          from scripts.startup_valid" | kind=entity | source=manager/backend/scripts/startup_validator.py:L397 | neighbors=[run_all_validators()] | lang=en
- "scripts_startup_validator_rationale_73": "Validates required env vars are present and non-default." | kind=entity | source=manager/backend/scripts/startup_validator.py:L73 | neighbors=[ConfigValidator] | lang=en
- "scripts_startup_validator_validationreport_errors": ".errors()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L49 | neighbors=[ValidationReport] | lang=en
- "scripts_startup_validator_validationreport_warnings": ".warnings()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L53 | neighbors=[ValidationReport] | lang=en
- "services_agent_policy_rationale_1": "agent_policy.py — the deterministic policy engine for the Autonomous Engagement" | kind=entity | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[agent_policy.py] | lang=en
- "services_agent_policy_rationale_50": "Map an action name to its risk tier; unknown actions fail closed." | kind=entity | source=manager/backend/app/services/agent_policy.py:L50 | neighbors=[classify_action()] | lang=en
- "services_agent_policy_rationale_56": "The deterministic authorization envelope for one engagement's agent." | kind=entity | source=manager/backend/app/services/agent_policy.py:L56 | neighbors=[RulesOfEngagement] | lang=en
- "services_agent_policy_rationale_68": "Running engagement usage, checked against the blast-radius caps." | kind=entity | source=manager/backend/app/services/agent_policy.py:L68 | neighbors=[UsageCounters] | lang=en
- "services_agent_policy_rationale_89": "Decide whether `action` may proceed under `roe`. Order is deliberate:     hard d" | kind=entity | source=manager/backend/app/services/agent_policy.py:L89 | neighbors=[evaluate_action()] | lang=en
- "services_analytics_rationale_1": "Exposure analytics — protocol risk + zone health.  Derives two dashboard aggrega" | kind=entity | source=manager/backend/app/services/analytics.py:L1 | neighbors=[analytics.py] | lang=en
- "services_audit_rationale_1": "audit.py — the append-only audit-log writer, shared by the operator and portal r" | kind=entity | source=manager/backend/app/services/audit.py:L1 | neighbors=[audit.py] | lang=en
- "services_audit_rationale_16": "Append one immutable audit row (caller flushes within its own txn)." | kind=entity | source=manager/backend/app/services/audit.py:L16 | neighbors=[record_audit()] | lang=en
- "services_evidence_summary_rationale_1": "evidence_summary.py — flatten the arbitrary evidence JSONB into plain facts.  Fi" | kind=entity | source=manager/backend/app/services/evidence_summary.py:L1 | neighbors=[evidence_summary.py] | lang=en
- "services_evidence_summary_rationale_119": "Return a short, ordered, human-readable ``[{label, value}]`` fact list.      Non" | kind=entity | source=manager/backend/app/services/evidence_summary.py:L119 | neighbors=[summarize_evidence()] | lang=en
- "services_evidence_summary_rationale_72": "Render one evidence value as a short plain string, or None to skip it." | kind=entity | source=manager/backend/app/services/evidence_summary.py:L72 | neighbors=[_format_value()] | lang=en
- "services_finding_ai_rationale_1": "finding_ai.py — the OPTIONAL, fail-closed AI enrichment seam for findings.  The" | kind=entity | source=manager/backend/app/services/finding_ai.py:L1 | neighbors=[finding_ai.py] | lang=en
- "services_finding_ai_rationale_113": "Return an AI-authored ``content_overrides`` dict for a finding, or None.      ``" | kind=entity | source=manager/backend/app/services/finding_ai.py:L113 | neighbors=[generate_content_overrides()] | lang=en
- "services_finding_ai_rationale_72": "Pull the first JSON object out of a completion, tolerating code fences and     s" | kind=entity | source=manager/backend/app/services/finding_ai.py:L72 | neighbors=[_extract_json()] | lang=en
- "services_finding_ai_rationale_97": "Keep only well-formed override fields; None if nothing usable survives." | kind=entity | source=manager/backend/app/services/finding_ai.py:L97 | neighbors=[_validate()] | lang=en
- "services_finding_compliance_rationale_1": "finding_compliance.py — deterministic finding → compliance-control mapping.  Pur" | kind=entity | source=manager/backend/app/services/finding_compliance.py:L1 | neighbors=[finding_compliance.py] | lang=en
- "services_finding_compliance_rationale_237": "Return ``[{framework, controls, rationale}]`` for a finding, one entry per     f" | kind=entity | source=manager/backend/app/services/finding_compliance.py:L237 | neighbors=[compliance_for()] | lang=en
- "services_finding_content_findingcontent_to_dict": ".to_dict()" | kind=code-symbol | source=manager/backend/app/services/finding_content.py:L232 | neighbors=[FindingContent] | lang=en
- "services_finding_content_rationale_1": "finding_content.py — the deterministic per-finding explanation knowledge base." | kind=entity | source=manager/backend/app/services/finding_content.py:L1 | neighbors=[finding_content.py] | lang=en
- "services_finding_content_rationale_207": "The honest exploitation posture of a finding.      ``status`` is 'validated' onl" | kind=entity | source=manager/backend/app/services/finding_content.py:L207 | neighbors=[ExploitationView] | lang=en
- "services_finding_content_rationale_259": "Extract the raw exploitation signals from a finding + its evidence.      Never g" | kind=entity | source=manager/backend/app/services/finding_content.py:L259 | neighbors=[exploitation_signals()] | lang=en
- "services_finding_content_rationale_278": "Map exploitation signals to the frontend maturity enum.      WEAPONIZED — proven" | kind=entity | source=manager/backend/app/services/finding_content.py:L278 | neighbors=[exploit_maturity()] | lang=en
- "services_finding_content_rationale_293": "How the finding was ESTABLISHED, as the frontend confidence enum     (exploit |" | kind=entity | source=manager/backend/app/services/finding_content.py:L293 | neighbors=[detection_method()] | lang=en
- "services_finding_content_rationale_379": "Build the deterministic explanation + exploitation content for a finding.      `" | kind=entity | source=manager/backend/app/services/finding_content.py:L379 | neighbors=[finding_content()] | lang=en
- "services_finding_enrichment_rationale_1": "finding_enrichment.py — assemble the per-finding detail content for the API.  Th" | kind=entity | source=manager/backend/app/services/finding_enrichment.py:L1 | neighbors=[finding_enrichment.py] | lang=en
- "services_finding_enrichment_rationale_20": "Return the heavy detail-only enrichment fields for one finding.      Honours ``f" | kind=entity | source=manager/backend/app/services/finding_enrichment.py:L20 | neighbors=[detail_enrichment()] | lang=en
- "services_finding_events_rationale_1": "finding_events.py — the finding lifecycle audit trail.  Two sources feed one tim" | kind=entity | source=manager/backend/app/services/finding_events.py:L1 | neighbors=[finding_events.py] | lang=en
- "services_finding_events_rationale_109": "Derive the canonical lifecycle events that the finding's timestamp columns     a" | kind=entity | source=manager/backend/app/services/finding_events.py:L109 | neighbors=[synthesize_events()] | lang=en
- "services_finding_events_rationale_163": "Append one immutable audit row. The caller owns the transaction/flush." | kind=entity | source=manager/backend/app/services/finding_events.py:L163 | neighbors=[record_event()] | lang=en
- "services_finding_events_rationale_174": "Map a target FindingStatus to its specific event kind (so 'confirmed' reads" | kind=entity | source=manager/backend/app/services/finding_events.py:L174 | neighbors=[event_type_for_status()] | lang=en
- "services_finding_events_rationale_207": "Merge stored + synthesized events, oldest-first. A stored event of a given     k" | kind=entity | source=manager/backend/app/services/finding_events.py:L207 | neighbors=[merge_timeline()] | lang=pt
- "services_finding_events_rationale_217": "The finding's full lifecycle timeline: stored audit rows merged with the     eve" | kind=entity | source=manager/backend/app/services/finding_events.py:L217 | neighbors=[build_timeline()] | lang=en
- "services_finding_events_rationale_55": "Accept a FindingEventType/FindingStatus enum or a bare string." | kind=entity | source=manager/backend/app/services/finding_events.py:L55 | neighbors=[_val()] | lang=pt
- "services_finding_events_rationale_82": "Best label for who first produced this finding, from its provenance.     A netwo" | kind=entity | source=manager/backend/app/services/finding_events.py:L82 | neighbors=[_detected_actor()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-297.json

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
