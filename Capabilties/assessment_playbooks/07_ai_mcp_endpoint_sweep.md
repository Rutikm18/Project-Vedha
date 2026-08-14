# 07 — AI / MCP Endpoint Sweep (Core-Level Playbook)

> **Goal:** Discover and assess AI-related network endpoints — LLM inference servers, vector DBs,
> and **Model Context Protocol (MCP)** servers — which are exploding in enterprises and frequently
> deployed with **no authentication**, exposing model access, internal tools, and data. This is a
> newer surface with immature defaults, so exposure is common.

---

## 1. Core theory: what these endpoints are and why they're risky

AI infrastructure introduces new network services that behave unlike traditional apps:

### 1.1 Local/self-hosted inference servers
Developers run models locally and often bind them to `0.0.0.0` with no auth:

| Service | Default port | Core fact |
|---------|--------------|-----------|
| **Ollama** | 11434 | REST API (`/api/tags`, `/api/generate`); **no auth by default**; lists & runs models |
| **LM Studio** | 1234 | OpenAI-compatible `/v1/*` API |
| **vLLM / TGI** | 8000 / 3000 | OpenAI-compatible serving; no auth unless added |
| **llama.cpp server** | 8080 | `/completion`, `/v1/chat/completions` |
| **Text-Generation-WebUI** | 7860/5000 | Gradio UI + API |
| **Jupyter** | 8888 | Notebooks = RCE if token/password missing |
| **Ray** | 8265/6379/10001 | Dashboard/Client — historically RCE (CVE-2023-48022 "ShadowRay") |
| **Triton** | 8000/8001/8002 | NVIDIA inference server |

### 1.2 Vector / RAG databases
| Service | Port | Note |
|---------|------|------|
| Chroma | 8000 | Often no auth |
| Qdrant | 6333/6334 | REST+gRPC |
| Weaviate | 8080 | GraphQL/REST |
| Milvus | 19530 | gRPC |
| Pinecone | (SaaS) | API-key based |

RAG stores contain **embedded proprietary/PII data** — reading them can reconstruct source text.

### 1.3 MCP (Model Context Protocol) — the important new surface
MCP is an open protocol (introduced by Anthropic, 2024) that lets LLM agents call **tools,
resources, and prompts** exposed by "MCP servers." Transport variants:
- **stdio** (local subprocess — not network-exposed),
- **HTTP + Server-Sent Events (SSE)** and **Streamable HTTP** — *these are network-reachable.*

Wire format: **JSON-RPC 2.0**. Handshake begins with an `initialize` request; then
`tools/list`, `resources/list`, `prompts/list`, and `tools/call`.

**Why MCP is high-risk:**
- MCP servers frequently ship **without authentication** and bound to network interfaces.
- `tools/list` on an unauthenticated server **enumerates the internal capabilities the agent can
  invoke** — file access, shell, database queries, cloud APIs. `tools/call` may let you invoke them.
- MCP tool descriptions are fed to an LLM → **prompt-injection / tool-poisoning** surface (a
  malicious tool description can hijack an agent). Confused-deputy and token-passthrough issues are
  documented in the MCP security guidance.
- Exposed MCP = potential **RCE / data access / SSRF** via whatever tools it wraps.

---

## 2. Approach from a single system (methodology + commands)

**Step 1 — port sweep for AI services:**
```bash
nmap -sS -p 1234,3000,5000,6333,6379,7860,8000,8001,8080,8265,8888,11434,19530,4840 \
     -sV --script "http-headers,http-title" -iL live.txt -oX ai_ports.xml
```

**Step 2 — fingerprint inference endpoints (unauth checks):**
```bash
# Ollama — lists local models, no auth
curl -s http://<host>:11434/api/tags | jq .
# OpenAI-compatible servers (vLLM/LM Studio/llama.cpp)
curl -s http://<host>:8000/v1/models
# Jupyter — is a token required?
curl -s http://<host>:8888/api/  ; curl -s http://<host>:8888/  # login page vs open
# Ray dashboard
curl -s http://<host>:8265/api/version
```

**Step 3 — detect and probe MCP servers (SSE/HTTP transport):**
```bash
# SSE transport often at /sse or /mcp; Streamable HTTP at /mcp
curl -s -N http://<host>:PORT/sse            # SSE stream announces endpoint
# JSON-RPC initialize handshake
curl -s http://<host>:PORT/mcp -H 'Content-Type: application/json' -d '{
  "jsonrpc":"2.0","id":1,"method":"initialize",
  "params":{"protocolVersion":"2024-11-05","capabilities":{},
            "clientInfo":{"name":"assessment","version":"1.0"}}}'
# Then enumerate exposed capabilities (READ-ONLY)
# method: "tools/list", "resources/list", "prompts/list"
```
The presence of a working `initialize` → `tools/list` without any auth token **is the finding.**
Record the tool names/descriptions (they reveal what an attacker could invoke); **do not call
dangerous tools.**

**Step 4 — vector DB exposure:**
```bash
curl -s http://<host>:6333/collections           # Qdrant
curl -s http://<host>:8000/api/v1/collections     # Chroma
```

---

## 3. Vulnerability logic

- **Unauthenticated inference API** → free model use (cost abuse), prompt exfiltration of system
  prompts, potential jailbreak of downstream apps, model theft (weights via some servers).
- **Unauthenticated MCP server** → enumerate + invoke internal tools = RCE/data access/SSRF; the
  agent's privileges become the attacker's.
- **Jupyter/Ray without token** → direct RCE (execute code / submit jobs).
- **Exposed vector DB** → read embedded proprietary/PII data.
- **Prompt-injection / tool-poisoning** surface where LLM output drives actions.
- **Secrets in configs** — API keys (OpenAI/Anthropic/cloud) in exposed `.env`, notebooks, MCP
  server configs → cost abuse + pivot.

---

## 4. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Fast-moving, non-standard ports | New ecosystem, no conventions | Broad `-sV` + HTTP fingerprinting; look for `/v1/models`, `/api/tags`, JSON-RPC `initialize` responses |
| MCP transport ambiguity (stdio vs SSE vs HTTP) | Multiple transports, evolving spec | Test both `/sse` and `/mcp` (Streamable HTTP); confirm with a JSON-RPC `initialize` |
| Auth sometimes present (bearer/OAuth) | Newer MCP guidance adds OAuth | Distinguish "auth required" (good) from "auth absent" (finding); don't brute tokens |
| Invoking tools may cause real actions | `tools/call` can delete/exfiltrate/spend | Enumerate only (`*/list`); never call state-changing tools without explicit authorization |
| Cost/impact of hitting inference | Requests cost money / GPU time | Minimal probes; a single `/models` or `initialize` suffices |
| Honeypots for AI services | Deceptive Ollama/MCP decoys | Corroborate model list plausibility, latency, version consistency |
| Rapidly changing CVEs | Immature software | Track vendor advisories continuously (Ray, Triton, gradio, langchain, MCP servers) |
| Prompt-injection is behavioral, not a port | Logic-layer risk | Assess how LLM output is used downstream; test injection only in authorized app scope |

---

## 5. Considerations & guardrails

- **Enumerate, don't detonate.** Listing tools/models/collections proves exposure. Calling tools
  or generating large completions can cause real-world side effects and cost — avoid.
- **Treat discovered API keys as live secrets** — report, don't use out of scope.
- **This surface changes monthly.** Keep a living list of AI service ports and MCP spec versions.
- **Prompt injection is a genuine, in-scope class** for AI-integrated apps but is tested at the
  application layer with authorization, not by hammering endpoints.

---

## 6. References

- Model Context Protocol specification and **MCP security best practices** (modelcontextprotocol.io).
- JSON-RPC 2.0 spec; W3C Server-Sent Events.
- OWASP **Top 10 for LLM Applications** (LLM01 Prompt Injection … LLM10) and OWASP ML Security Top 10.
- NIST AI Risk Management Framework (AI RMF 1.0); MITRE **ATLAS** (adversarial ML threat matrix).
- Notable CVEs: Ray CVE-2023-48022 (ShadowRay), gradio path-traversal CVEs, langchain RCE issues.
- Vendor docs: Ollama, vLLM, LM Studio, Qdrant, Chroma, Weaviate, Ray, NVIDIA Triton.
