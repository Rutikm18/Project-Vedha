# Node Description Batch 36 of 119

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "agent_scope_crypt_encrypt_scope": "encrypt_scope()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L55 | neighbors=[scope_crypt.py, encrypt_scope_b64(), Encrypt scope JSON to a specific probe'…]
- "agent_scope_crypt_encrypt_scope_b64": "encrypt_scope_b64()" | kind=code-symbol | source=probe/agent/scope_crypt.py:L150 | neighbors=[scope_crypt.py, encrypt_scope(), encrypt_scope() returning a base64 stri…]
- "agent_scope_validator_fetch_engagement_scope": "fetch_engagement_scope()" | kind=code-symbol | source=probe/agent/scope_validator.py:L54 | neighbors=[scope_validator.py, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_scope_validator_merge_exclusions": "merge_exclusions()" | kind=code-symbol | source=probe/agent/scope_validator.py:L154 | neighbors=[scope_validator.py, Merge engagement-level exclusions with …, Merge engagement-level exclusions with …]
- "agent_spool_flush": ".Flush()" | kind=code-symbol | source=probe-go/agent/spool.go:L83 | neighbors=[spool.go, .Delete(), .path()]
- "agent_spool_save": ".Save()" | kind=code-symbol | source=probe-go/agent/spool.go:L26 | neighbors=[spool.go, .path(), syncDir()]
- "agent_spool_syncdir": "syncDir()" | kind=code-symbol | source=probe-go/agent/spool.go:L139 | neighbors=[spool.go, .Delete(), .Save()]
- "agent_state_saveidentitystate": "saveIdentityState()" | kind=code-symbol | source=probe-go/agent/state.go:L65 | neighbors=[state.go, secureStateDirectory(), syncStateDirectory()]
- "agent_state_securestatedirectory": "secureStateDirectory()" | kind=code-symbol | source=probe-go/agent/state.go:L146 | neighbors=[state.go, saveIdentityState(), secureStatePath()]
- "agent_state_securestatepath": "secureStatePath()" | kind=code-symbol | source=probe-go/agent/state.go:L136 | neighbors=[state.go, loadIdentityState(), secureStateDirectory()]
- "agent_state_test_testobtainidentitypersistsandreusesregistration": "TestObtainIdentityPersistsAndReusesRegistration()" | kind=code-symbol | source=probe-go/agent/state_test.go:L78 | neighbors=[state_test.go, identityTestConfig(), newIdentityServer()]
- "agent_state_test_testobtainidentityrecoversfromcorruptstate": "TestObtainIdentityRecoversFromCorruptState()" | kind=code-symbol | source=probe-go/agent/state_test.go:L127 | neighbors=[state_test.go, identityTestConfig(), newIdentityServer()]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L29 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job()]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L48 | neighbors=[Args:             http_get:       Callb…, TaskRunner, Args:             http_get:       Callb…]
- "agent_transport_heartbeat": ".Heartbeat()" | kind=code-symbol | source=probe-go/agent/transport.go:L82 | neighbors=[transport.py, .postContext(), .patch()]
- "agent_transport_managertlsconfig": "managerTLSConfig()" | kind=code-symbol | source=probe-go/agent/transport.go:L38 | neighbors=[transport.py, .ConnectWS(), NewTransport()]
- "agent_transport_postcontext": ".postContext()" | kind=code-symbol | source=probe-go/agent/transport.go:L175 | neighbors=[transport.py, .Heartbeat(), .post()]
- "agent_transport_test": "transport_test.go" | kind=code-symbol | source=probe-go/agent/transport_test.go:L1 | neighbors=[TestConnectWSHonorsTLSVerificationAndMa…, TestHeartbeatUsesManagerContractAndRetr…, b4b12a9 Rename project and update files]
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L353 | neighbors=[Fetch the engagement's authoritative sc…, Transport, Fetch the engagement's authoritative sc…]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L310 | neighbors=[Send a heartbeat to the manager.       …, Transport, Send a heartbeat to the manager.       …]
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L423 | neighbors=[Generic authenticated GET, returns pars…, Transport, Generic authenticated GET, returns pars…]
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L165 | neighbors=[True if we have both an agent_id and a …, Transport, True if we have both an agent_id and a …]
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L479 | neighbors=[True if the WebSocket connection is act…, Transport, Fetch the engagement's authoritative sc…]
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=probe/agent/transport.py:L171 | neighbors=[Transport, .__init__(), .update_state()]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L270 | neighbors=[Refresh routing metadata using the cach…, Transport, TransportError]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L202 | neighbors=[Transport, .register(), .update_state()]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L372 | neighbors=[Submit a scan result to the manager.   …, Transport, Submit a scan result to the manager.   …]
- "agent_transport_transport_ws_url": ".ws_url()" | kind=code-symbol | source=probe/agent/transport.py:L439 | neighbors=[Return the WebSocket endpoint without e…, Transport, Return the WebSocket connection URL wit…]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L118 | neighbors=[use_cases.py, Return (scan_type, profile) for a job. …, Return (scan_type, profile) for a job. …]
- "ai_agent_agentdecisionengine_list_findings": "._list_findings()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L283 | neighbors=[AgentDecisionEngine, ._exec_read_tool(), _val()]
- "ai_agent_val": "_val()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L382 | neighbors=[agent.py, ._list_findings(), ._overview()]
- "ai_hallucination_hallucinationguard_validate_cve_claims": ".validate_cve_claims()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L45 | neighbors=[HallucinationGuard, .validate(), Flag any CVE ID mentioned in ``text`` t…]
- "ai_hallucination_hallucinationguard_validate_cvss_scores": ".validate_cvss_scores()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L60 | neighbors=[HallucinationGuard, .validate(), Flag CVSS scores in the text that don't…]
- "ai_hallucination_hallucinationguard_validate_remediation_commands": ".validate_remediation_commands()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L89 | neighbors=[HallucinationGuard, .validate(), Flag destructive-looking commands that …]
- "ai_llm_report_enum": "_enum()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L310 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_finding_scores": "_finding_scores()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L321 | neighbors=[llm_report.py, .generate_remediation_steps(), .generate_technical_finding()]
- "ai_llm_report_llmreportgenerator_complete": "._complete()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L110 | neighbors=[LLMReportGenerator, LLMUnavailableError, ._generate_and_store()]
- "ai_llm_report_llmreportgenerator_generate_executive_summary": ".generate_executive_summary()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L171 | neighbors=[LLMReportGenerator, _collect_cves_scores(), ._generate_and_store()]
- "ai_prioritizer_vulnprioritizer_formula_contributions": "._formula_contributions()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L191 | neighbors=[VulnPrioritizer, .explain_prediction(), .fallback_score()]
- "auth_jwt_create_refresh_token": "create_refresh_token()" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L38 | neighbors=[jwt.py, _now(), Returns (token, jti) — jti is stored in…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-035.json

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
