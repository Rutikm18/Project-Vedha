# Node Description Batch 37 of 92

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

- "workflow_router_looks_like_http": "looks_like_http()" | kind=code-symbol | source=workflow/router.py:L45 | neighbors=[router.py, looks_like_db(), route_branches()] | lang=en
- "workflow_router_looks_like_ssh": "looks_like_ssh()" | kind=code-symbol | source=workflow/router.py:L71 | neighbors=[router.py, True when a service banner is an SSH id…, route_branches()] | lang=en
- "workflow_router_looks_like_tls": "looks_like_tls()" | kind=code-symbol | source=workflow/router.py:L50 | neighbors=[router.py, True when this port's banner result is …, route_branches()] | lang=en
- "workflow_workflow_engine_run_inventory": "_run_inventory()" | kind=code-symbol | source=workflow/workflow_engine.py:L211 | neighbors=[workflow_engine.py, run_engagement(), _Sink] | lang=en
- "workflow_workflow_engine_run_passive": "_run_passive()" | kind=code-symbol | source=workflow/workflow_engine.py:L194 | neighbors=[workflow_engine.py, run_engagement(), _Sink] | lang=en
- "agent_cli_cmd_whoami": "cmd_whoami()" | kind=code-symbol | source=agent/cli.py:L296 | neighbors=[cli.py, cmd_auth_status()] | lang=en
- "agent_cli_doctor_check": "_doctor_check()" | kind=code-symbol | source=agent/cli.py:L300 | neighbors=[cli.py, cmd_doctor()] | lang=en
- "agent_cli_main": "main()" | kind=code-symbol | source=agent/cli.py:L1129 | neighbors=[cli.py, build_parser()] | lang=en
- "agent_cli_manager_is_local": "_manager_is_local()" | kind=code-symbol | source=agent/cli.py:L568 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_cli_managerclient_init": ".__init__()" | kind=code-symbol | source=agent/cli.py:L104 | neighbors=[ManagerClient, normalize_manager_url()] | lang=en
- "agent_cli_write_private_json": "_write_private_json()" | kind=code-symbol | source=agent/cli.py:L534 | neighbors=[cli.py, cmd_validate()] | lang=en
- "agent_device_identity_decode_key": "decode_key()" | kind=code-symbol | source=agent/device_identity.py:L30 | neighbors=[device_identity.py, verify_site_policy()] | lang=en
- "agent_engine_env_number": "_env_number()" | kind=code-symbol | source=agent/engine.py:L50 | neighbors=[engine.py, Read a bounded numeric safety setting w…] | lang=en
- "agent_engine_facts_from_cache": "_facts_from_cache()" | kind=code-symbol | source=agent/engine.py:L299 | neighbors=[engine.py, run_scan()] | lang=en
- "agent_license_b64d": "_b64d()" | kind=code-symbol | source=agent/license.py:L45 | neighbors=[license.py, verify_license()] | lang=en
- "agent_license_rationale_1": "license.py — host-locked, vendor-signed anti-copy gate for the probe.  DESIGN (p" | kind=entity | source=agent/license.py:L1 | neighbors=[HWBindError, license.py] | lang=en
- "agent_license_rationale_102": "Combined startup gauntlet: HW bind → license check. Fails fast.      This is the" | kind=entity | source=agent/license.py:L102 | neighbors=[HWBindError, gauntlet()] | lang=en
- "agent_license_rationale_36": "Stable per-machine ID, derived from hw_bind's hardware fingerprint." | kind=entity | source=agent/license.py:L36 | neighbors=[HWBindError, host_fingerprint()] | lang=en
- "agent_license_rationale_51": "Returns the license payload dict if valid; raises LicenseError otherwise.     To" | kind=entity | source=agent/license.py:L51 | neighbors=[HWBindError, verify_license()] | lang=en
- "agent_license_rationale_85": "The gate the agent calls at startup. Honors LICENSE_ENFORCED and     reads the t" | kind=entity | source=agent/license.py:L85 | neighbors=[HWBindError, check_license()] | lang=en
- "agent_local_run_rationale_1": "local_run.py — run the probe's REAL pipeline (workflow.run_engagement) directly" | kind=entity | source=agent/local_run.py:L1 | neighbors=[local_run.py, ScopeGuard] | lang=en
- "agent_local_run_rationale_110": "Actionable input error on stderr → exit code 2. No traceback: this is     operat" | kind=entity | source=agent/local_run.py:L110 | neighbors=[_usage_error(), ScopeGuard] | lang=en
- "agent_local_run_rationale_200": "Synchronous entrypoint for the `local-run` CLI subcommand." | kind=entity | source=agent/local_run.py:L200 | neighbors=[run(), ScopeGuard] | lang=en
- "agent_local_run_rationale_43": "Resolve the port set from PROBE_LOCAL_PORTS.        unset      → [22, 80, 443]" | kind=entity | source=agent/local_run.py:L43 | neighbors=[_ports_from_env(), ScopeGuard] | lang=en
- "agent_local_run_rationale_69": "Drop internal bookkeeping keys (_collected_at, _via…) for readable output." | kind=entity | source=agent/local_run.py:L69 | neighbors=[_clean(), ScopeGuard] | lang=en
- "agent_local_run_rationale_76": "Render a port fact unambiguously: '445/tcp open', '11211/udp open|filtered     (" | kind=entity | source=agent/local_run.py:L76 | neighbors=[_port_label(), ScopeGuard] | lang=pt
- "agent_local_run_scope_file": "_scope_file()" | kind=code-symbol | source=agent/local_run.py:L38 | neighbors=[local_run.py, _main()] | lang=en
- "agent_result_spool_resultspool_at_capacity": ".at_capacity()" | kind=code-symbol | source=agent/result_spool.py:L235 | neighbors=[Whether new jobs must pause until pendi…, ResultSpool] | lang=en
- "agent_scope_crypt_bytes_to_pubkey_b64": "bytes_to_pubkey_b64()" | kind=code-symbol | source=agent/scope_crypt.py:L165 | neighbors=[scope_crypt.py, Encode raw X25519 public key bytes to a…] | lang=en
- "agent_scope_crypt_generate_identity": "generate_identity()" | kind=code-symbol | source=agent/scope_crypt.py:L43 | neighbors=[scope_crypt.py, Generate a fresh X25519 keypair.      R…] | lang=en
- "agent_scope_crypt_pubkey_to_bytes": "pubkey_to_bytes()" | kind=code-symbol | source=agent/scope_crypt.py:L160 | neighbors=[scope_crypt.py, Decode a base64-encoded X25519 public k…] | lang=en
- "agent_scope_validator_fetch_engagement_scope": "fetch_engagement_scope()" | kind=code-symbol | source=agent/scope_validator.py:L54 | neighbors=[scope_validator.py, Fetch the engagement's authoritative sc…] | lang=en
- "agent_scope_validator_merge_exclusions": "merge_exclusions()" | kind=code-symbol | source=agent/scope_validator.py:L154 | neighbors=[scope_validator.py, Merge engagement-level exclusions with …] | lang=en
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=agent/task_runner.py:L46 | neighbors=[Args:             http_get:       Callb…, TaskRunner] | lang=en
- "agent_transport_transport_clear_state": ".clear_state()" | kind=code-symbol | source=agent/transport.py:L245 | neighbors=[Transport, .update_state()] | lang=en
- "agent_transport_transport_close": ".close()" | kind=code-symbol | source=agent/transport.py:L713 | neighbors=[_sync_directory(), Transport] | lang=en
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=agent/transport.py:L562 | neighbors=[Fetch the engagement's authoritative sc…, Transport] | lang=en
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=agent/transport.py:L646 | neighbors=[Generic authenticated GET, returns pars…, Transport] | lang=en
- "agent_transport_transport_init": ".__init__()" | kind=code-symbol | source=agent/transport.py:L123 | neighbors=[Transport, .load_state()] | lang=en
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=agent/transport.py:L202 | neighbors=[True if we have both an agent_id and a …, Transport] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-036.json

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
