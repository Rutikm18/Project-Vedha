# Vedha stack — existing controls to reuse & checks to run

Verify against current code before relying on any line here (paths drift).

## Components
- **manager/backend** — FastAPI, async SQLAlchemy 2 + asyncpg (Postgres), Alembic,
  Pydantic v2, PyJWT, passlib/bcrypt, Redis, structlog, httpx. Optional extras
  (AI/anthropic, AD/ldap3/impacket, neo4j, minio) imported defensively.
- **manager/frontend** — Next.js 16 / React 19, TypeScript, Playwright e2e.
  Read `manager/frontend/CLAUDE.md` and `AGENTS.md` before frontend work.
- **probe** — Python agent (`probe/agent`), scanners (`probe/scanner`), sealed
  builds (`probe/SEALING.md`), runs **inside customer networks** — any RCE or
  command injection here is a customer-network compromise.
- **CI** — `.github/workflows/` (backend-ci, frontend-ci, agent-ci, secret-scan
  with gitleaks, images, scanner-accuracy, version gates).

## Existing security controls (reuse; don't reinvent)
| Concern | Where |
|---|---|
| JWT issue/verify (algorithm pinned) | `manager/backend/app/auth/jwt.py` |
| MFA / TOTP | `app/auth/mfa.py`, `app/auth/totp.py` |
| Personal access tokens | `app/auth/pat.py` |
| Refresh token store/rotation | `app/auth/refresh_store.py` |
| RBAC | `app/auth/rbac.py` |
| Portal scope | `app/auth/portal_scope.py` |
| Auth middleware / current user + tenant | `app/auth/middleware.py`, `app/dependencies.py` (`get_current_user` → `tenant_id`) |
| Password hashing | `app/auth/password.py` |
| Rate limiting | `app/ratelimit.py` |
| Agent access / release gating | `app/agent_access.py`, `app/agent_release.py` |
| AI audit chain | `app/ai/audit_chain.py` |
| Frontend CSP | `manager/frontend/lib/csp.ts`, `next.config.mjs`, `proxy.ts` |
| Secret scanning | `.pre-commit-config.yaml` (gitleaks, detect-private-key), `.github/workflows/secret-scan.yml`, `.gitleaks.toml` |

## Stack-specific rules
**FastAPI / Pydantic**
- Route deps: `Depends(get_current_user)` + RBAC check; tenant from `CurrentUser.tenant_id` only.
- Separate `Create`/`Update`/`Read` schemas; `model_config = ConfigDict(extra="forbid")` on inputs;
  constrained types (`conint`, `constr`/`Field(max_length=…)`, `IPvAnyAddress`, enums).
- `response_model` on every route so ORM objects never leak extra columns.
- Return 404 for objects outside the caller's tenant.

**SQLAlchemy / Alembic**
- `select(Model).where(Model.id == id, Model.tenant_id == user.tenant_id)`.
- `text()` only with bound params; dynamic ORDER BY via allow-list mapping.
- New tenant-scoped tables: `tenant_id` NOT NULL, FK, indexed (leading column in composites).
- Migrations have working `downgrade()`; avoid table-rewriting locks on big tables.

**Probe / scanners**
- `subprocess.run([...], shell=False, timeout=…)`; validate targets with `ipaddress`
  / strict hostname regex; insert `--` before positional targets.
- Parse tool XML with `defusedxml`; cap output sizes; treat all target responses as hostile.
- Never execute manager-supplied strings as commands; manager instructions are
  structured, allow-listed, and authenticated.
- Files written with restrictive perms; no secrets in probe logs.

**Next.js**
- No secrets in `NEXT_PUBLIC_*`. Auth checks in server code (route handlers / server actions), not only `proxy.ts`.
- No `dangerouslySetInnerHTML` without sanitisation; validate redirect targets (same-origin relative paths only).
- Keep CSP strict; don't add `unsafe-inline`/`unsafe-eval` to fix a bug.

## Checks to run (only claim what actually ran)
Backend (from `manager/backend`):
```
pytest -q                                   # or the targeted test file
python -m ruff check app || true            # if ruff is installed
pip-audit -r requirements-core.txt          # if installed / for new deps
bandit -q -r app -ll                        # if installed
```
Frontend (from `manager/frontend`):
```
npm run lint && npx tsc --noEmit
npm test --if-present
npm audit --omit=dev                        # for new deps
```
Probe (from `probe`):
```
pytest -q tests
bandit -q -r agent scanner -ll              # if installed
```
Repo-wide:
```
gitleaks detect --no-banner                 # if installed (pre-commit runs it too)
semgrep --config p/owasp-top-ten --config p/python --config p/typescript <changed paths>   # if installed
graphify update .                           # after code changes (project rule)
```
If a tool isn't installed, say "not run (not installed)" in the report. Don't install
global tools without asking.
