# OWASP API Security Top 10 (2023) + OWASP Top 10 for LLM Applications (2025)

Sources: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ and
https://genai.owasp.org/llm-top-10/ (verified 2026-10).

## API Security Top 10:2023

| ID | Risk | What to check in a FastAPI route / WebSocket |
|---|---|---|
| API1 | Broken Object Level Authorization (BOLA) | Every object fetch scoped to principal's tenant/ownership; test with another tenant's ID |
| API2 | Broken Authentication | Token validation (alg, exp, aud), refresh rotation, PAT scope, brute-force limits |
| API3 | Broken Object Property Level Authorization | Separate read/write schemas; no mass assignment; don't return internal/secret fields |
| API4 | Unrestricted Resource Consumption | Page size caps, body size, upload size, rate limits, timeouts, expensive-query guards |
| API5 | Broken Function Level Authorization | Admin/ops endpoints require admin role server-side; HTTP method swaps don't bypass |
| API6 | Unrestricted Access to Sensitive Business Flows | Scan launch, export, invite, report generation — quotas & abuse limits |
| API7 | Server Side Request Forgery | URL inputs validated (see A01 SSRF); integrations egress-restricted |
| API8 | Security Misconfiguration | CORS, headers, verbose errors, docs exposure, TLS |
| API9 | Improper Inventory Management | New routes registered/documented; old versions removed; no shadow/debug routes |
| API10 | Unsafe Consumption of APIs | Treat NVD/EPSS/KEV/LLM/third-party responses as untrusted: validate schema, size, timeouts, TLS verify |

## LLM Top 10:2025 (for `manager/backend/app/ai/*` and any AI gateway work — see ADR-0003/0004)

| ID | Risk | Control |
|---|---|---|
| LLM01 | Prompt Injection (direct & indirect — scan output, banners, CVE text, filenames are attacker-controlled) | Delimit/label untrusted content; never let model output choose privileged actions without allow-list + authz; human-in-loop for impactful actions |
| LLM02 | Sensitive Information Disclosure | Minimise/redact what's sent (creds, internal IPs per tenant policy); tenant isolation of context; no cross-tenant retrieval |
| LLM03 | Supply Chain | Pin model/provider versions and SDKs; vet model files; no unpickling downloaded models |
| LLM04 | Data and Model Poisoning | Provenance for training/fine-tune/RAG data; tenant-separated stores |
| LLM05 | Improper Output Handling | Model output is untrusted input: escape before rendering (XSS), never into SQL/shell/eval, validate JSON against schema |
| LLM06 | Excessive Agency | Least-privilege tools, read-only by default, per-tenant scoping inside tools, confirmation for writes |
| LLM07 | System Prompt Leakage | No secrets/keys/authz logic in prompts; enforce authz outside the model |
| LLM08 | Vector and Embedding Weaknesses | Per-tenant namespaces with access checks at query time; poisoning checks |
| LLM09 | Misinformation | Ground claims (CVE IDs, CVSS, remediation) in data; show sources; deterministic fallback (ADR-0004) |
| LLM10 | Unbounded Consumption | Token/request caps per tenant, timeouts, cost budgets, rate limiting |
