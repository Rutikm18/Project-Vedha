# Node Description Batch 203 of 380

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

- "agent_instance_lock_rationale_1": "instance_lock.py — one probe process per state file.  WHY THIS EXISTS (observed" | kind=entity | source=probe/agent/instance_lock.py:L1 | neighbors=[instance_lock.py] | lang=en
- "agent_instance_lock_rationale_135": "Release explicitly. Process exit would do this anyway — this is for tests     an" | kind=entity | source=probe/agent/instance_lock.py:L135 | neighbors=[release_instance_lock()] | lang=en
- "agent_instance_lock_rationale_52": "Another live process already owns this state file." | kind=entity | source=probe/agent/instance_lock.py:L52 | neighbors=[InstanceLockError] | lang=en
- "agent_instance_lock_rationale_56": "Sidecar lock path for a state file. Never the state file itself — locking     th" | kind=entity | source=probe/agent/instance_lock.py:L56 | neighbors=[lock_path_for()] | lang=en
- "agent_instance_lock_rationale_63": "Best-effort description of the current holder, for the error message only." | kind=entity | source=probe/agent/instance_lock.py:L63 | neighbors=[_holder_hint()] | lang=en
- "agent_instance_lock_rationale_86": "Take the single-instance lock for `state_file`.      Returns the open handle, wh" | kind=entity | source=probe/agent/instance_lock.py:L86 | neighbors=[acquire_instance_lock()] | lang=en
- "agent_job_admission_drop_denied": "drop_denied()" | kind=code-symbol | source=probe/agent/job_admission.py:L36 | neighbors=[job_admission.py] | lang=en
- "agent_job_admission_rationale_1": "job_admission.py — the agent's independent, defense-in-depth admission gate.  Wi" | kind=entity | source=probe/agent/job_admission.py:L1 | neighbors=[job_admission.py] | lang=en
- "agent_job_admission_rationale_22": "Resolve the Manager's IP from PLATFORM_URL so the fleet can never scan its     o" | kind=entity | source=probe/agent/job_admission.py:L22 | neighbors=[manager_ip_from_env()] | lang=en
- "agent_job_admission_verify_signed_job": "verify_signed_job()" | kind=code-symbol | source=probe/agent/job_admission.py:L44 | neighbors=[job_admission.py] | lang=en
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
- "agent_local_run_rationale_1": "local_run.py — run the probe's REAL pipeline (workflow.run_engagement) directly" | kind=entity | source=probe/agent/local_run.py:L1 | neighbors=[local_run.py] | lang=en
- "agent_local_run_rationale_110": "Actionable input error on stderr → exit code 2. No traceback: this is     operat" | kind=entity | source=probe/agent/local_run.py:L110 | neighbors=[_usage_error()] | lang=en
- "agent_local_run_rationale_121": "Validate positional args (args[0]=target, [1]=profile, [2]=stage, [3]=filter)" | kind=entity | source=probe/agent/local_run.py:L121 | neighbors=[_parse_args()] | lang=en
- "agent_local_run_rationale_200": "Synchronous entrypoint for the `local-run` CLI subcommand." | kind=entity | source=probe/agent/local_run.py:L200 | neighbors=[run()] | lang=en
- "agent_local_run_rationale_43": "Resolve the port set from PROBE_LOCAL_PORTS.        unset      → [22, 80, 443]" | kind=entity | source=probe/agent/local_run.py:L43 | neighbors=[_ports_from_env()] | lang=en
- "agent_local_run_rationale_69": "Drop internal bookkeeping keys (_collected_at, _via…) for readable output." | kind=entity | source=probe/agent/local_run.py:L69 | neighbors=[_clean()] | lang=en
- "agent_local_run_rationale_76": "Render a port fact unambiguously: '445/tcp open', '11211/udp open|filtered     (" | kind=entity | source=probe/agent/local_run.py:L76 | neighbors=[_port_label()] | lang=pt
- "agent_obs_rationale_1": "obs.py — observability (Phase 8): redacted structured logs, low-cardinality hear" | kind=entity | source=probe/agent/obs.py:L1 | neighbors=[obs.py] | lang=en
- "agent_obs_rationale_38": "Mask the host octet so an own-IP never lands verbatim in a shared bundle." | kind=entity | source=probe/agent/obs.py:L38 | neighbors=[mask_ip()] | lang=en
- "agent_obs_rationale_56": "Bounded-cardinality fleet-health signal. No IPs/hostnames/targets as keys." | kind=entity | source=probe/agent/obs.py:L56 | neighbors=[heartbeat_metrics()] | lang=en
- "agent_obs_rationale_75": "A support bundle with secrets stripped and own-IPs masked." | kind=entity | source=probe/agent/obs.py:L75 | neighbors=[build_diagnostics()] | lang=en
- "agent_release_rationale_1": "release.py — release integrity + SBOM (Phase 10).  The checksum manifest is the" | kind=entity | source=probe/agent/release.py:L1 | neighbors=[release.py] | lang=en
- "agent_result_queue_rationale_1": "result_queue.py — durable, crash-safe, encrypted result spool (Phase 4).  Sits b" | kind=entity | source=probe/agent/result_queue.py:L1 | neighbors=[result_queue.py] | lang=en
- "agent_result_queue_rationale_31": "Identity cipher — tests + explicitly-plaintext deployments only." | kind=entity | source=probe/agent/result_queue.py:L31 | neighbors=[NullCipher] | lang=en
- "agent_result_queue_rationale_37": "Fernet cipher keyed by a per-host key file (0600) that never leaves the     host" | kind=entity | source=probe/agent/result_queue.py:L37 | neighbors=[host_sealed_cipher()] | lang=en
- "agent_result_spool_rationale_1": "result_spool.py — local result persistence with upload retry.  When the probe co" | kind=entity | source=probe/agent/result_spool.py:L1 | neighbors=[result_spool.py] | lang=en
- "agent_result_spool_rationale_100": "Load a previously spooled result, returning None if missing/corrupt." | kind=entity | source=probe/agent/result_spool.py:L100 | neighbors=[.load()] | lang=pt
- "agent_result_spool_rationale_102": "Remove the spool file for a successfully uploaded result." | kind=entity | source=probe/agent/result_spool.py:L102 | neighbors=[.remove()] | lang=en
- "agent_result_spool_rationale_111": "Remove the spool file for a successfully uploaded result." | kind=entity | source=probe/agent/result_spool.py:L111 | neighbors=[.remove()] | lang=en
- "agent_result_spool_rationale_114": "Attempt to upload a result with retries and local spool as fallback.          Ar" | kind=entity | source=probe/agent/result_spool.py:L114 | neighbors=[.submit_with_retry()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-202.json

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
