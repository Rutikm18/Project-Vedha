# Node Description Batch 182 of 227

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

- "services_job_result_service_rationale_137": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L137 | neighbors=[process_job_result()] | lang=en
- "services_job_result_service_rationale_30": "Stable idempotency checksum for one attempt completion payload." | kind=entity | source=manager/backend/app/services/job_result_service.py:L30 | neighbors=[result_checksum()] | lang=en
- "services_job_result_service_rationale_327": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L327 | neighbors=[_promote_assets()] | lang=en
- "services_job_result_service_rationale_356": "Stamp the probe's evidence-based device role onto an Asset (create/update)." | kind=entity | source=manager/backend/app/services/job_result_service.py:L356 | neighbors=[_apply_device_profile()] | lang=en
- "services_job_result_service_rationale_379": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L379 | neighbors=[_promote_assets()] | lang=en
- "services_job_result_service_rationale_42": "Return network identities that could create assets or findings.      Scanner-lev" | kind=entity | source=manager/backend/app/services/job_result_service.py:L42 | neighbors=[_result_network_identities()] | lang=en
- "services_job_result_service_rationale_72": "Parse a probe identity as an IP, tolerating common host:port notation." | kind=entity | source=manager/backend/app/services/job_result_service.py:L72 | neighbors=[_identity_ip()] | lang=en
- "services_job_result_service_rationale_91": "Return result identities outside the job's authoritative IP scope.      Fail clo" | kind=entity | source=manager/backend/app/services/job_result_service.py:L91 | neighbors=[validate_result_scope()] | lang=en
- "services_llm_airuntimeerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L22 | neighbors=[AiRuntimeError] | lang=en
- "services_llm_managerllmservice_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L75 | neighbors=[ManagerLlmService] | lang=en
- "services_llm_rationale_259": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L259 | neighbors=[._dispatch()] | lang=en
- "services_llm_rationale_301": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L301 | neighbors=[._fallback_candidates()] | lang=en
- "services_llm_rationale_325": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L325 | neighbors=[.generate_with_fallback()] | lang=en
- "services_llm_rationale_85": "First configured cloud provider, or None. Cloud-only: never Ollama." | kind=entity | source=manager/backend/app/services/llm.py:L85 | neighbors=[._auto_cloud_provider()] | lang=en
- "services_notifications_rationale_1": "notifications.py — deliver a message to a tenant's configured integrations (emai" | kind=entity | source=manager/backend/app/services/notifications.py:L1 | neighbors=[notifications.py] | lang=pt
- "services_notifications_rationale_102": "Producer API: enqueue a durable notify event (commits with the caller's txn)." | kind=entity | source=manager/backend/app/services/notifications.py:L102 | neighbors=[enqueue_notification()] | lang=en
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
- "services_remediation_kb_rationale_1": "remediation_kb.py — the deterministic remediation knowledge base.  Pure (no DB," | kind=entity | source=manager/backend/app/services/remediation_kb.py:L1 | neighbors=[remediation_kb.py] | lang=en
- "services_remediation_kb_rationale_27": "Normalize an arbitrary OS/target string to a supported KB key.      Public becau" | kind=entity | source=manager/backend/app/services/remediation_kb.py:L27 | neighbors=[os_key()] | lang=en
- "services_remediation_kb_rationale_347": "Return a structured, OS-filtered remediation plan for `finding`.      Always ret" | kind=entity | source=manager/backend/app/services/remediation_kb.py:L347 | neighbors=[recipe_for_finding()] | lang=en
- "services_remediation_kb_rationale_80": "Map a finding to a KB category key using title/description/CVE hints.      Deter" | kind=entity | source=manager/backend/app/services/remediation_kb.py:L80 | neighbors=[classify_finding()] | lang=pt
- "services_remediation_kb_rationale_97": "One remediation step. `generic` is REQUIRED (the vendor-neutral fallback);     p" | kind=entity | source=manager/backend/app/services/remediation_kb.py:L97 | neighbors=[_step()] | lang=en
- "services_risk_rank_compute_risk_rank": "compute_risk_rank()" | kind=code-symbol | source=manager/backend/app/services/risk_rank.py:L16 | neighbors=[risk_rank.py] | lang=en
- "services_risk_rank_rationale_1": "risk_rank.py — one explainable 0-1000 priority for a finding.  Blends impact (se" | kind=entity | source=manager/backend/app/services/risk_rank.py:L1 | neighbors=[risk_rank.py] | lang=en
- "services_scope_crypto_rationale_1": "scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 publi" | kind=entity | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[scope_crypto.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-181.json

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
