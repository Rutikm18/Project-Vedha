# Node Description Batch 134 of 134

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

- "workflow_report_rationale_43": "re-scan mode's delta report: what changed between two engagements." | kind=entity | source=probe/workflow/report.py:L43 | neighbors=[diff_assets()] | lang=en
- "workflow_router_rationale_1": "router.py — dynamic Gate-5 branch routing from OBSERVED service_banner content," | kind=entity | source=probe/workflow/router.py:L1 | neighbors=[router.py] | lang=en
- "workflow_router_rationale_43": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=probe/workflow/router.py:L43 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_51": "True when this port's banner result is exactly the silent-on-garbage     signatu" | kind=entity | source=probe/workflow/router.py:L51 | neighbors=[looks_like_tls()] | lang=en
- "workflow_router_rationale_56": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L56 | neighbors=[route_branches()] | lang=en
- "workflow_router_rationale_63": "True when a service banner carries a database greeting signature, so a DB     on" | kind=entity | source=probe/workflow/router.py:L63 | neighbors=[looks_like_db()] | lang=pt
- "workflow_router_rationale_73": "For every open port with a banner fact, returns {port: {branches}}     that obse" | kind=entity | source=probe/workflow/router.py:L73 | neighbors=[route_branches()] | lang=en
- "workflow_workflow_engine_rationale_1": "workflow_engine.py — the async DAG executor. Loops through gates, checks precond" | kind=entity | source=probe/workflow/workflow_engine.py:L1 | neighbors=[workflow_engine.py] | lang=en
- "workflow_workflow_engine_rationale_104": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L104 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_rationale_110": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L110 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_134": "In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/     WindowsColl" | kind=entity | source=probe/workflow/workflow_engine.py:L134 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_rationale_136": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L136 | neighbors=[run_engagement()] | lang=en
- "workflow_workflow_engine_rationale_236": "Runs gates 0/2-6 (in order) across `targets`, mutating and returning     the Ass" | kind=entity | source=probe/workflow/workflow_engine.py:L236 | neighbors=[run_engagement()] | lang=en
- "workflow_workflow_engine_rationale_51": "Runs scanner.scan_target(host) across hosts concurrently; the     scanner's own" | kind=entity | source=probe/workflow/workflow_engine.py:L51 | neighbors=[_gather_per_host()] | lang=en
- "workflow_workflow_engine_rationale_59": "Run one component without allowing a target-specific bug to abort peers." | kind=entity | source=probe/workflow/workflow_engine.py:L59 | neighbors=[_scan_one()] | lang=en
- "workflow_workflow_engine_rationale_64": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L64 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_rationale_77": "Run per-host probes with bounded fan-out and failure isolation." | kind=entity | source=probe/workflow/workflow_engine.py:L77 | neighbors=[_gather_per_host()] | lang=en
- "workflow_workflow_engine_rationale_80": "Return TCP ports worth scanning for this profile and requested branch set." | kind=entity | source=probe/workflow/workflow_engine.py:L80 | neighbors=[_port_candidates()] | lang=en
- "workflow_workflow_engine_rationale_94": "Splits candidate_ports into (ports that actually need a fresh probe,     ScanRes" | kind=entity | source=probe/workflow/workflow_engine.py:L94 | neighbors=[_split_cached()] | lang=en
- "workflow_workflow_engine_sink_close": ".close()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L145 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_sink_init": ".__init__()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L141 | neighbors=[_Sink] | lang=en
- "workflow_workflow_engine_sink_write": ".write()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L143 | neighbors=[_Sink] | lang=en
- "agent_agent_rationale_138": "Fast port discovery with naabu. Feeds port list to Nmap." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L138 | lang=en
- "agent_agent_rationale_202": "Nmap service enumeration. Accepts port list from Naabu." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L202 | lang=en
- "agent_agent_rationale_239": "Nuclei vulnerability scan — production-ready." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L239 | lang=en
- "agent_agent_rationale_304": "Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L304 | lang=en
- "agent_agent_rationale_374": "NetExec SMB validation: signing, null sessions, SMBv1." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L374 | lang=en
- "agent_agent_rationale_454": "testssl.sh TLS/SSL analysis." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L454 | lang=en
- "agent_agent_rationale_500": "Extract HTTP/HTTPS URLs from nmap XML output." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L500 | lang=en
- "agent_agent_rationale_528": "EyeWitness screenshot evidence collection." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L528 | lang=en
- "agent_agent_rationale_597": "Safe lateral movement checks — no actual exploitation." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L597 | lang=en
- "agent_agent_rationale_606": "Cloud infrastructure scan (AWS/Azure/GCP)." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L606 | lang=en
- "agent_agent_rationale_76": "Fetches credentials from HashiCorp Vault at runtime. Never caches to disk." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L76 | lang=en
- "agent_agent_rationale_82": "Read a KV-v2 secret from Vault." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L82 | lang=en
- "e2e_interop_verify_rationale_1": "Verify the Python probe can open what the TypeScript manager sealed (T14 interop" | kind=entity | source=manager/frontend/tests/e2e/interop_verify.py:L1 | lang=en
- "e2e_mock_manager_rationale_1": "Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO" | kind=entity | source=manager/frontend/tests/e2e/mock_manager.py:L1 | lang=en
- "e2e_mock_manager_rationale_235": "Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64)." | kind=entity | source=manager/frontend/tests/e2e/mock_manager.py:L235 | lang=en
- "e2e_run_rationale_1": "End-to-end probe test: real probe process ↔ reference mock manager over HTTPS." | kind=entity | source=manager/frontend/tests/e2e/run.py:L1 | lang=en
- "e2e_run_rationale_30": "Deterministic stand-ins emitting realistic output for 127.0.0.1." | kind=entity | source=manager/frontend/tests/e2e/run.py:L30 | lang=en
- "threadinghttpserver": "ThreadingHTTPServer" | kind=code-symbol | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-133.json

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
