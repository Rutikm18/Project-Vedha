# Node Description Batch 266 of 336

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

- "services_finding_events_rationale_55": "Accept a FindingEventType/FindingStatus enum or a bare string." | kind=entity | source=manager/backend/app/services/finding_events.py:L55 | neighbors=[_val()] | lang=pt
- "services_finding_events_rationale_82": "Best label for who first produced this finding, from its provenance.     A netwo" | kind=entity | source=manager/backend/app/services/finding_events.py:L82 | neighbors=[_detected_actor()] | lang=en
- "services_job_attempt_service_rationale_31": "Atomically claim a pending job and create its fenced attempt ledger row." | kind=entity | source=manager/backend/app/services/job_attempt_service.py:L31 | neighbors=[claim_job_attempt()] | lang=en
- "services_job_attempt_service_rationale_94": "Renew only the currently installed running attempt/fence." | kind=entity | source=manager/backend/app/services/job_attempt_service.py:L94 | neighbors=[renew_job_attempt()] | lang=en
- "services_job_result_service_rationale_111": "Return result identities outside the job's authoritative IP scope.      Fail clo" | kind=entity | source=manager/backend/app/services/job_result_service.py:L111 | neighbors=[validate_result_scope()] | lang=en
- "services_job_result_service_rationale_117": "Parse a probe identity as an IP, tolerating common host:port notation." | kind=entity | source=manager/backend/app/services/job_result_service.py:L117 | neighbors=[_identity_ip()] | lang=en
- "services_job_result_service_rationale_136": "Return result identities outside the job's authoritative IP scope.      Fail clo" | kind=entity | source=manager/backend/app/services/job_result_service.py:L136 | neighbors=[validate_result_scope()] | lang=en
- "services_job_result_service_rationale_137": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L137 | neighbors=[process_job_result()] | lang=en
- "services_job_result_service_rationale_157": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L157 | neighbors=[process_job_result()] | lang=en
- "services_job_result_service_rationale_182": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L182 | neighbors=[process_job_result()] | lang=en
- "services_job_result_service_rationale_327": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L327 | neighbors=[_promote_assets()] | lang=en
- "services_job_result_service_rationale_356": "Stamp the probe's evidence-based device role onto an Asset (create/update)." | kind=entity | source=manager/backend/app/services/job_result_service.py:L356 | neighbors=[_apply_device_profile()] | lang=en
- "services_job_result_service_rationale_379": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L379 | neighbors=[_promote_assets()] | lang=en
- "services_job_result_service_rationale_404": "Stamp the probe's evidence-based device role onto an Asset (create/update)." | kind=entity | source=manager/backend/app/services/job_result_service.py:L404 | neighbors=[_apply_device_profile()] | lang=en
- "services_job_result_service_rationale_42": "Return network identities that could create assets or findings.      Scanner-lev" | kind=entity | source=manager/backend/app/services/job_result_service.py:L42 | neighbors=[_result_network_identities()] | lang=en
- "services_job_result_service_rationale_427": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L427 | neighbors=[_promote_assets()] | lang=en
- "services_job_result_service_rationale_438": "Stamp the probe's evidence-based device role onto an Asset (create/update)." | kind=entity | source=manager/backend/app/services/job_result_service.py:L438 | neighbors=[_apply_device_profile()] | lang=en
- "services_job_result_service_rationale_461": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L461 | neighbors=[_promote_assets()] | lang=en
- "services_job_result_service_rationale_50": "Stable idempotency checksum for one attempt completion payload." | kind=entity | source=manager/backend/app/services/job_result_service.py:L50 | neighbors=[result_checksum()] | lang=en
- "services_job_result_service_rationale_62": "Return network identities that could create assets or findings.      Scanner-lev" | kind=entity | source=manager/backend/app/services/job_result_service.py:L62 | neighbors=[_result_network_identities()] | lang=en
- "services_job_result_service_rationale_72": "Parse a probe identity as an IP, tolerating common host:port notation." | kind=entity | source=manager/backend/app/services/job_result_service.py:L72 | neighbors=[_identity_ip()] | lang=en
- "services_job_result_service_rationale_79": "Return network identities that could create assets or findings.      Scanner-lev" | kind=entity | source=manager/backend/app/services/job_result_service.py:L79 | neighbors=[_result_network_identities()] | lang=en
- "services_job_result_service_rationale_91": "Return result identities outside the job's authoritative IP scope.      Fail clo" | kind=entity | source=manager/backend/app/services/job_result_service.py:L91 | neighbors=[validate_result_scope()] | lang=en
- "services_job_result_service_rationale_92": "Parse a probe identity as an IP, tolerating common host:port notation." | kind=entity | source=manager/backend/app/services/job_result_service.py:L92 | neighbors=[_identity_ip()] | lang=en
- "services_llm_airuntimeerror_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L23 | neighbors=[AiRuntimeError] | lang=en
- "services_llm_http_client_asyncllmhttpclient_open": ".open()" | kind=code-symbol | source=manager/backend/app/services/llm_http_client.py:L30 | neighbors=[AsyncLlmHttpClient] | lang=en
- "services_llm_http_client_rationale_1": "Shared asynchronous HTTP transport for every Manager LLM provider.  Provider ada" | kind=entity | source=manager/backend/app/services/llm_http_client.py:L1 | neighbors=[llm_http_client.py] | lang=en
- "services_llm_http_client_rationale_18": "Create bounded ``httpx.AsyncClient`` instances for LLM requests.      A fresh co" | kind=entity | source=manager/backend/app/services/llm_http_client.py:L18 | neighbors=[AsyncLlmHttpClient] | lang=en
- "services_llm_managerllmservice_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L112 | neighbors=[ManagerLlmService] | lang=en
- "services_llm_rationale_126": "First configured cloud provider, or None. Cloud-only: never Ollama." | kind=entity | source=manager/backend/app/services/llm.py:L126 | neighbors=[._auto_cloud_provider()] | lang=en
- "services_llm_rationale_259": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L259 | neighbors=[._dispatch()] | lang=en
- "services_llm_rationale_300": "Call one provider and normalize failures to AiRuntimeError.         Preserves th" | kind=entity | source=manager/backend/app/services/llm.py:L300 | neighbors=[._dispatch()] | lang=en
- "services_llm_rationale_301": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L301 | neighbors=[._fallback_candidates()] | lang=en
- "services_llm_rationale_325": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L325 | neighbors=[.generate_with_fallback()] | lang=en
- "services_llm_rationale_342": "Ordered runtimes to try: requested/default first, then the OpenRouter         fr" | kind=entity | source=manager/backend/app/services/llm.py:L342 | neighbors=[._fallback_candidates()] | lang=en
- "services_llm_rationale_366": "Try each candidate until one succeeds. On ANY provider failure (credit         e" | kind=entity | source=manager/backend/app/services/llm.py:L366 | neighbors=[.generate_with_fallback()] | lang=en
- "services_llm_rationale_85": "First configured cloud provider, or None. Cloud-only: never Ollama." | kind=entity | source=manager/backend/app/services/llm.py:L85 | neighbors=[._auto_cloud_provider()] | lang=en
- "services_notifications_rationale_1": "notifications.py — deliver a message to a tenant's configured integrations (emai" | kind=entity | source=manager/backend/app/services/notifications.py:L1 | neighbors=[notifications.py] | lang=pt
- "services_notifications_rationale_102": "Producer API: enqueue a durable notify event (commits with the caller's txn)." | kind=entity | source=manager/backend/app/services/notifications.py:L102 | neighbors=[enqueue_notification()] | lang=en
- "services_notifications_rationale_72": "Send via one integration. True on success; False on any handled failure     (log" | kind=entity | source=manager/backend/app/services/notifications.py:L72 | neighbors=[deliver()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-265.json

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
