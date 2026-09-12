# Node Description Batch 300 of 380

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

- "services_llm_rationale_23": "Is an API key actually usable — not just present?      A key must be non-empty a" | kind=entity | source=manager/backend/app/services/llm.py:L23 | neighbors=[_usable_key()] | lang=en
- "services_llm_rationale_259": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L259 | neighbors=[._dispatch()] | lang=en
- "services_llm_rationale_300": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L300 | neighbors=[._dispatch()] | lang=en
- "services_llm_rationale_301": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L301 | neighbors=[._fallback_candidates()] | lang=en
- "services_llm_rationale_325": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L325 | neighbors=[.generate_with_fallback()] | lang=en
- "services_llm_rationale_342": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L342 | neighbors=[._fallback_candidates()] | lang=en
- "services_llm_rationale_366": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L366 | neighbors=[.generate_with_fallback()] | lang=en
- "services_llm_rationale_394": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L394 | neighbors=[._dispatch()] | lang=en
- "services_llm_rationale_446": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L446 | neighbors=[._fallback_candidates()] | lang=en
- "services_llm_rationale_470": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L470 | neighbors=[.generate_with_fallback()] | lang=en
- "services_llm_rationale_53": "Shape the system prompt into Anthropic prompt-cache blocks.      The system prom" | kind=entity | source=manager/backend/app/services/llm.py:L53 | neighbors=[_anthropic_system_blocks()] | lang=en
- "services_llm_rationale_81": "Wrap a plain system prompt as a single Anthropic prompt-cache block.      For th" | kind=entity | source=manager/backend/app/services/llm.py:L81 | neighbors=[cached_system_prompt()] | lang=pt
- "services_llm_rationale_85": "First configured cloud provider, or None. Cloud-only: never Ollama." | kind=entity | source=manager/backend/app/services/llm.py:L85 | neighbors=[._auto_cloud_provider()] | lang=en
- "services_notifications_rationale_1": "notifications.py — deliver a message to a tenant's configured integrations (emai" | kind=entity | source=manager/backend/app/services/notifications.py:L1 | neighbors=[notifications.py] | lang=pt
- "services_notifications_rationale_102": "Producer API: enqueue a durable notify event (commits with the caller's txn)." | kind=entity | source=manager/backend/app/services/notifications.py:L102 | neighbors=[enqueue_notification()] | lang=en
- "services_notifications_rationale_103": "Send via one integration. True on success; False on any handled failure     (log" | kind=entity | source=manager/backend/app/services/notifications.py:L103 | neighbors=[deliver()] | lang=en
- "services_notifications_rationale_119": "Deliver to every ENABLED integration for the tenant. Returns the count sent." | kind=entity | source=manager/backend/app/services/notifications.py:L119 | neighbors=[notify_tenant()] | lang=en
- "services_notifications_rationale_133": "Producer API: enqueue a durable notify event (commits with the caller's txn)." | kind=entity | source=manager/backend/app/services/notifications.py:L133 | neighbors=[enqueue_notification()] | lang=en
- "services_notifications_rationale_68": "Create a ServiceNow incident via the Table API.      ServiceNow is the ticketing" | kind=entity | source=manager/backend/app/services/notifications.py:L68 | neighbors=[_send_servicenow()] | lang=en
- "services_notifications_rationale_72": "Send via one integration. True on success; False on any handled failure     (log" | kind=entity | source=manager/backend/app/services/notifications.py:L72 | neighbors=[deliver()] | lang=en
- "services_notifications_rationale_88": "Deliver to every ENABLED integration for the tenant. Returns the count sent." | kind=entity | source=manager/backend/app/services/notifications.py:L88 | neighbors=[notify_tenant()] | lang=en
- "services_notifications_send_email": "_send_email()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L28 | neighbors=[notifications.py] | lang=en
- "services_notifications_send_jira": "_send_jira()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L52 | neighbors=[notifications.py] | lang=en
- "services_notifications_send_slack": "_send_slack()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L45 | neighbors=[notifications.py] | lang=en
- "services_portal_metrics_metricfinding": "MetricFinding" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L21 | neighbors=[portal_metrics.py] | lang=en
- "services_portal_metrics_rationale_1": "portal_metrics.py — pure aggregations for the customer dashboard.  Kept pure (no" | kind=entity | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[portal_metrics.py] | lang=en
- "services_portal_metrics_rationale_33": "Count findings by severity (all five buckets always present, zero-filled).     o" | kind=entity | source=manager/backend/app/services/portal_metrics.py:L33 | neighbors=[severity_breakdown()] | lang=en
- "services_portal_metrics_rationale_45": "(open, closed) totals over the given findings." | kind=entity | source=manager/backend/app/services/portal_metrics.py:L45 | neighbors=[open_closed_counts()] | lang=en
- "services_portal_metrics_rationale_56": "Per-month {period, opened, closed} for the last `months` months.      opened = f" | kind=entity | source=manager/backend/app/services/portal_metrics.py:L56 | neighbors=[status_timeline()] | lang=en
- "services_posture_rationale_1": "Posture scoring & patch-comparison — the single source of truth behind the dashb" | kind=entity | source=manager/backend/app/services/posture.py:L1 | neighbors=[posture.py] | lang=en
- "services_posture_rationale_105": "True when the finding was live as of run_at (first_seen ≤ run_at ≤ last_seen)." | kind=entity | source=manager/backend/app/services/posture.py:L105 | neighbors=[_present_in_run()] | lang=en
- "services_posture_rationale_121": "Bucket findings across the previous→latest run transition." | kind=entity | source=manager/backend/app/services/posture.py:L121 | neighbors=[compare()] | lang=en
- "services_posture_rationale_164": "Full dashboard/report payload. Degrades gracefully with 0 or 1 run." | kind=entity | source=manager/backend/app/services/posture.py:L164 | neighbors=[build_posture()] | lang=en
- "services_posture_rationale_23": "Duck-typed projection of a Finding + its asset's criticality." | kind=entity | source=manager/backend/app/services/posture.py:L23 | neighbors=[FindingView] | lang=en
- "services_posture_rationale_48": "Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Empty → 0.0. Always in [0, 100]." | kind=entity | source=manager/backend/app/services/posture.py:L48 | neighbors=[aggregate()] | lang=en
- "services_project_time_rationale_1": "project_time — one place that decides what \"now\" looks like to a human.  The man" | kind=entity | source=manager/backend/app/services/project_time.py:L1 | neighbors=[project_time.py] | lang=en
- "services_project_time_rationale_42": "The project timezone, degrading safely when tzdata is unavailable." | kind=entity | source=manager/backend/app/services/project_time.py:L42 | neighbors=[_resolve_project_tz()] | lang=en
- "services_project_time_rationale_61": "Current time as an AWARE datetime in the project timezone." | kind=entity | source=manager/backend/app/services/project_time.py:L61 | neighbors=[project_now()] | lang=en
- "services_project_time_rationale_66": "ISO-8601 instant in the project timezone: 2026-09-03T23:15:05+05:30." | kind=entity | source=manager/backend/app/services/project_time.py:L66 | neighbors=[project_timestamp()] | lang=en
- "services_project_time_rationale_71": "Re-render an existing datetime in the project timezone.      The instant is pres" | kind=entity | source=manager/backend/app/services/project_time.py:L71 | neighbors=[to_project_tz()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-299.json

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
