# Vedha dashboard

This Next.js application is Vedha's **only dashboard**. It is an unprivileged
control and reporting surface: it authenticates operators, calls the Manager
API through server-side BFF routes, dispatches jobs, and renders results.

It does not scan networks. Production scan flow is:

```text
Dashboard → Manager API → Vedha Probe → raw facts → Manager detection → Dashboard
```

The supported scanner is [`../../probe/`](../../probe/). Scanner binaries,
raw-socket capabilities, probe credentials, and vulnerability collection do not
belong in the dashboard container.

## Run with the product

From the repository root:

```bash
cp .env.docker.example .env
make up       # Manager + dashboard
make full     # Manager + dashboard + one local test probe
```

- Dashboard: `http://localhost:3000`
- Manager API: `http://localhost:18080`
- API documentation: `http://localhost:18080/docs`

Port `18080` is an API listener, not another dashboard. Port `18018` is not
part of Vedha.

## Direct frontend development

Start the Manager first, then:

```bash
cp .env.example .env.local
npm ci
npm run dev
```

Set `BACKEND_INTERNAL_URL` to the Manager API. `AUTH_SECRET` must match the
Manager JWT secret. Browser access and refresh tokens are stored only in
`HttpOnly`, `SameSite=Strict` cookies. Set `AUTH_COOKIE_SECURE=true` whenever
the dashboard is served over HTTPS; local HTTP Compose defaults it to `false`.

AI execution is owned by Manager; the dashboard only forwards authenticated
requests and never receives provider credentials. Configure the Manager or root
Compose environment. Local Ollama is the free default:

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b
LLM_REQUEST_TIMEOUT_SECONDS=180
```

For OpenRouter, set `LLM_PROVIDER=openrouter`, `OPENROUTER_API_KEY`, and any
model enabled for the account in `OPENROUTER_MODEL`. The default is the zero-cost
`openrouter/free` router; free-tier limits and provider data terms still apply.
Provider keys are read only by Manager. Existing Anthropic deployments remain
supported with `LLM_PROVIDER=anthropic`.

The root deployment can install and persist the selected Ollama model:

```bash
OLLAMA_BASE_URL=http://ollama:11434 \
docker compose --profile ui --profile local-ai up -d --build
```

## Validation

```bash
npm run lint
npx tsc --noEmit
npm test
npm run build
```

The canonical Scan page uses only these BFF routes:

- `GET /api/scan/use-cases`
- `GET /api/scan/probes`
- `POST /api/scan/launch`
- `GET /api/scan/jobs/:id`

Manager-local scanner routes are intentionally absent. All scan execution must
cross the Manager's tenant, scope, capability, and job-dispatch controls.
The dashboard does not accept target credentials; the Manager rejects secret
material in persisted job parameters until an ephemeral credential broker is
available.
