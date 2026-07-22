# Node Description Batch 47 of 76

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

- "agent_agent_agentdeps": "AgentDeps" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L39 | neighbors=[agent.py] | lang=en
- "agent_agent_agentopts": "AgentOpts" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L26 | neighbors=[agent.py] | lang=en
- "agent_agent_rationale_138": "Fast port discovery with naabu. Feeds port list to Nmap." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L138 | neighbors=[execute_naabu()] | lang=en
- "agent_agent_rationale_202": "Nmap service enumeration. Accepts port list from Naabu." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L202 | neighbors=[execute_discovery()] | lang=en
- "agent_agent_rationale_239": "Nuclei vulnerability scan — production-ready." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L239 | neighbors=[execute_vuln_scan()] | lang=en
- "agent_agent_rationale_258": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L258 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_263": "Persistent WebSocket push loop.      Returns False if WebSocket is unavailable (" | kind=entity | source=probe/agent/agent.py:L263 | neighbors=[_run_ws_push_loop()] | lang=en
- "agent_agent_rationale_304": "Impacket-based AD enumeration: Kerberoast, AS-REP roast, LDAP anonymous bind." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L304 | neighbors=[execute_ad_enum()] | lang=en
- "agent_agent_rationale_374": "NetExec SMB validation: signing, null sessions, SMBv1." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L374 | neighbors=[execute_smb_validation()] | lang=en
- "agent_agent_rationale_382": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L382 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_387": "Run one job while keeping WS status/result frames best-effort." | kind=entity | source=probe/agent/agent.py:L387 | neighbors=[_ws_run_job()] | lang=en
- "agent_agent_rationale_43": "Load key=value lines from probe.env for dev convenience." | kind=entity | source=probe/agent/agent.py:L43 | neighbors=[_load_env()] | lang=en
- "agent_agent_rationale_437": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L437 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_442": "Poll pending jobs even while WS is connected.      This makes result delivery re" | kind=entity | source=probe/agent/agent.py:L442 | neighbors=[_ws_http_poll_fallback()] | lang=en
- "agent_agent_rationale_454": "testssl.sh TLS/SSL analysis." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L454 | neighbors=[execute_tls_scan()] | lang=en
- "agent_agent_rationale_470": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L470 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_475": "Send periodic heartbeats over WebSocket." | kind=entity | source=probe/agent/agent.py:L475 | neighbors=[_ws_heartbeat_sender()] | lang=en
- "agent_agent_rationale_485": "Re-submit previously spooled results over WebSocket." | kind=entity | source=probe/agent/agent.py:L485 | neighbors=[_ws_flush_spool()] | lang=en
- "agent_agent_rationale_490": "Re-submit previously spooled results over WebSocket." | kind=entity | source=probe/agent/agent.py:L490 | neighbors=[_ws_flush_spool()] | lang=en
- "agent_agent_rationale_500": "Extract HTTP/HTTPS URLs from nmap XML output." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L500 | neighbors=[extract_web_urls_from_nmap()] | lang=en
- "agent_agent_rationale_511": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L511 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_516": "Run all startup security checks before any network I/O.      Order matters: HW b" | kind=entity | source=probe/agent/agent.py:L516 | neighbors=[_startup_gauntlet()] | lang=pt
- "agent_agent_rationale_528": "EyeWitness screenshot evidence collection." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L528 | neighbors=[execute_eyewitness()] | lang=en
- "agent_agent_rationale_559": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L559 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_564": "Detect common debugging/tracing tools.  Informational only — does     NOT block" | kind=entity | source=probe/agent/agent.py:L564 | neighbors=[_check_anti_debug()] | lang=en
- "agent_agent_rationale_597": "Safe lateral movement checks — no actual exploitation." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L597 | neighbors=[execute_lateral_movement()] | lang=en
- "agent_agent_rationale_606": "Cloud infrastructure scan (AWS/Azure/GCP)." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L606 | neighbors=[execute_cloud_scan()] | lang=en
- "agent_agent_rationale_607": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L607 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_612": "Load the probe's X25519 identity from persistent state, or create one.      Retu" | kind=entity | source=probe/agent/agent.py:L612 | neighbors=[_load_or_create_identity()] | lang=en
- "agent_agent_rationale_667": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L667 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_672": "Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64)." | kind=entity | source=probe/agent/agent.py:L672 | neighbors=[_obtain_identity()] | lang=en
- "agent_agent_rationale_76": "Fetches credentials from HashiCorp Vault at runtime. Never caches to disk." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L76 | neighbors=[VaultCredentialFetcher] | lang=en
- "agent_agent_rationale_82": "Read a KV-v2 secret from Vault." | kind=entity | source=manager/frontend/infrastructure/agent/agent.py:L82 | neighbors=[.get_credentials()] | lang=en
- "agent_agent_rung": "Rung" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L18 | neighbors=[agent.py] | lang=en
- "agent_agent_rung_labels": "RUNG_LABELS" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L20 | neighbors=[agent.py] | lang=en
- "agent_agent_scanningagent_handle_shutdown": "._handle_shutdown()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L728 | neighbors=[ScanningAgent] | lang=en
- "agent_agent_toanthropictool": "toAnthropicTool()" | kind=code-symbol | source=manager/frontend/lib/agent/agent.ts:L67 | neighbors=[agent.py] | lang=en
- "agent_agent_vaultcredentialfetcher_init": ".__init__()" | kind=code-symbol | source=manager/frontend/infrastructure/agent/agent.py:L78 | neighbors=[VaultCredentialFetcher] | lang=en
- "agent_engine_rationale_1": "engine.py — adapt a manager scan job to scanner_module's workflow engine and ret" | kind=entity | source=probe/agent/engine.py:L1 | neighbors=[engine.py] | lang=en
- "agent_engine_rationale_145": "Count concrete open services, not generic host-liveness observations." | kind=entity | source=probe/agent/engine.py:L145 | neighbors=[_count_open_port_facts()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-046.json

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
