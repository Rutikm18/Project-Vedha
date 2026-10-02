# VEDHA — convenience wrapper around docker compose.
.DEFAULT_GOAL := help

# Two compose entrypoints, two intents:
#   COMPOSE (root docker-compose.yml)        — LOCAL dev all-in-one. Includes a
#       probe under `--profile probe` for convenient end-to-end testing on a laptop.
#   MANAGER_COMPOSE (manager/docker-compose.yml) — the DEPLOY stack (server / AWS).
#       PROBE-FREE by design: probes run on client machines via probe/install.sh,
#       never on the manager server. `make full` and the aws-* targets use this.
COMPOSE := docker compose
MANAGER_COMPOSE := docker compose --env-file .env -f manager/docker-compose.yml

# Admin-credential ops act on the RUNNING server deploy. `--project-directory .`
# makes the Compose project name the repo-dir basename (e.g. /opt/vedha -> `vedha`),
# matching what deploy/aws/install.sh created, so `run` joins the live stack.
ADMIN_COMPOSE := docker compose --project-directory . --env-file .env -f manager/docker-compose.yml

# Edge-overlay priority (highest wins):
#  1. deploy/tls/   — created by `make tls` (Let's Encrypt via Caddy, external DNS flow)
#  2. deploy/aws/   — created by install.sh (Caddy with ACME, AWS EC2 flow)
#  3. (none)        — plain HTTP edge ingress for local dev
TLS_OVERLAY := $(wildcard deploy/tls/docker-compose.tls.yml)
AWS_PROD_OVERLAY := $(wildcard deploy/aws/docker-compose.prod.yml)

ifneq ($(TLS_OVERLAY),)
DEPLOY_COMPOSE := $(MANAGER_COMPOSE) -f $(TLS_OVERLAY)
INGRESS_PROFILE :=
else ifneq ($(AWS_PROD_OVERLAY),)
DEPLOY_COMPOSE := $(MANAGER_COMPOSE) -f $(AWS_PROD_OVERLAY)
INGRESS_PROFILE :=
else
DEPLOY_COMPOSE := $(MANAGER_COMPOSE)
INGRESS_PROFILE := --profile edge
endif

# Deployed version, sourced from the repo-root VERSION file (auto-bumped by the
# .githooks/pre-commit hook). Exported so every `docker compose build` below bakes
# it into the backend image via the VEDHA_VERSION build arg.
export VEDHA_VERSION := $(shell cat VERSION 2>/dev/null || echo dev)

.PHONY: help doctor run dev full ui up up-graph up-ai api-only down logs ps migrate seed admin-show admin-reset shell venv test probe-build probe-run probe-pat seal seal-parity agent-keygen agent-release agent-publish agent-verify onprem-bundle clean version setup-hooks aws-up aws-up-ui aws-down aws-logs aws-ps gen-env tls tls-check tls-status tls-rollback prod-diagnose

version: ## Print the current deployed version
	@echo $(VEDHA_VERSION)

setup-hooks: ## Enable the auto version-bump git hook (run once per clone)
	git config core.hooksPath .githooks
	@echo "Version auto-bump enabled: every commit ticks VERSION (currently $(VEDHA_VERSION))."

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	  awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

doctor: ## Preflight: Docker, ports, .env, and insecure production defaults
	@sh scripts/doctor.sh

# NOTE: migrate, api, and worker all share `image: vedha-backend:local`. Building
# with `up --build` makes buildx bake export that one tag from three targets in
# parallel → "image already exists" failure. So every target below builds the
# shared backend image ONCE (via the `api` service — migrate/worker then reuse the
# tag), builds any other distinct-image services, and finally `up -d` WITHOUT
# `--build`. Keep this shape when adding new up-style targets.

run: ## Build + start platform + local probe (API + probe, no frontend) — fast
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) build api
	$(COMPOSE) --profile probe build probe
	$(COMPOSE) --profile probe up -d
	@port=$$(grep -E '^API_PORT=' .env | cut -d= -f2); port=$${port:-18080}; \
	  echo "API → http://localhost:$$port  (docs: /docs)  |  probe: docker compose logs -f probe"

full: gen-env ## Deploy the COMPLETE manager stack (db, redis, api, worker, dashboard, edge). Probe-free + AWS-aware. ← use this on the server
	$(MANAGER_COMPOSE) build api
	$(MANAGER_COMPOSE) --profile ui build frontend
	$(DEPLOY_COMPOSE) $(INGRESS_PROFILE) --profile ui up -d --remove-orphans
	@if [ -n "$(TLS_OVERLAY)" ]; then \
	   d=$$(grep -m1 '^TLS_DOMAIN=' .env | cut -d= -f2); a=$$(grep -m1 '^TLS_API_HOST=' .env | cut -d= -f2); \
	   echo ""; echo "  Manager stack up over HTTPS."; \
	   echo "  Dashboard  → https://$$d"; echo "  API / probe→ https://$$a/health"; exit 0; \
	 fi; \
	 eport=$$(grep -m1 '^EDGE_HTTP_PORT=' .env 2>/dev/null | cut -d= -f2); eport=$${eport:-80}; \
	 fport=$$(grep -m1 '^FRONTEND_PORT=' .env 2>/dev/null | cut -d= -f2); fport=$${fport:-3000}; \
	 host=$$(grep -m1 '^MANAGER_PUBLIC_URL=' .env 2>/dev/null | cut -d= -f2); host=$${host:-http://localhost}; \
	 echo ""; \
	 echo "  Manager stack up (probe-free)."; \
	 echo "  Dashboard  → http://<HOST>:$$fport      (login with SEED_ADMIN_EMAIL / SEED_ADMIN_PASSWORD)"; \
	 echo "  API / probe→ $$host/health          ← probes: ./install.sh <HOST>"; \
	 echo "  On AWS: open inbound TCP $$eport (edge) and $$fport (dashboard) in the EC2 security group."

dev: ## LOCAL all-in-one for laptop e2e testing: API + Next.js dashboard + a probe (root compose)
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) build api
	$(COMPOSE) --profile ui build frontend
	$(COMPOSE) --profile probe build probe
	$(COMPOSE) --profile probe --profile ui up -d
	@fport=$$(grep -E '^FRONTEND_PORT=' .env | cut -d= -f2); fport=$${fport:-3000}; \
	  echo "Dashboard → http://localhost:$$fport   (login with SEED_ADMIN_EMAIL / SEED_ADMIN_PASSWORD)  |  probe: docker compose logs -f probe"

ui: ## Build + start just the Next.js dashboard (API must be up)
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) --profile ui build frontend
	$(COMPOSE) --profile ui up -d frontend

up: ## Build + start EVERYTHING incl. the dashboard (postgres, redis, migrate, api, frontend)
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) build api
	$(COMPOSE) --profile ui build frontend
	$(COMPOSE) --profile ui up -d
	@aport=$$(grep -E '^API_PORT=' .env | cut -d= -f2); aport=$${aport:-18080}; \
	 fport=$$(grep -E '^FRONTEND_PORT=' .env | cut -d= -f2); fport=$${fport:-3000}; \
	 echo ""; \
	 echo "  Dashboard  → http://localhost:$$fport         (login with SEED_ADMIN_EMAIL / SEED_ADMIN_PASSWORD)"; \
	 echo "  Manager API → http://localhost:$$aport        (docs: /docs)"; \
	 echo "  Probe      → cd probe && ./probe run"

api-only: ## Build + start the platform only (postgres, redis, migrate, api) — no dashboard
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) build api
	$(COMPOSE) up -d

up-graph: ## Start the platform + Neo4j (attack-path graph)
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) build api
	NEO4J_ENABLED=true $(COMPOSE) --profile graph up -d

up-ai: ## Start Manager with deployment-managed Ollama and pull OLLAMA_MODEL
	@test -f .env || cp .env.docker.example .env
	INSTALL_EXTRAS=1 $(COMPOSE) build api
	OLLAMA_BASE_URL=http://ollama:11434 INSTALL_EXTRAS=1 $(COMPOSE) --profile local-ai up -d

down: ## Stop ALL services incl. a stray probe/edge (keeps volumes)
	$(COMPOSE) --profile graph --profile probe --profile ui --profile local-ai down --remove-orphans

clean: ## Stop and DELETE volumes (wipes database and local AI models)
	$(COMPOSE) --profile graph --profile probe --profile ui --profile local-ai down -v --remove-orphans

logs: ## Tail API logs
	$(COMPOSE) logs -f api

ps: ## Show service status
	$(COMPOSE) ps

migrate: ## Re-run database migrations
	$(COMPOSE) run --rm migrate alembic upgrade head

seed: ## Re-run the admin seeder
	$(COMPOSE) run --rm migrate python scripts/seed_admin.py

admin-show: ## Print the deployed admin login (email + password) from .env
	@test -f .env || { echo "ERROR: .env not found — run from the repo root (e.g. cd /opt/vedha)"; exit 1; }
	@email=$$(grep -m1 '^SEED_ADMIN_EMAIL=' .env | cut -d= -f2-); \
	 pw=$$(grep -m1 '^SEED_ADMIN_PASSWORD=' .env | cut -d= -f2-); \
	 echo "Admin email    : $${email:-admin@vedha.io}"; \
	 echo "Admin password : $${pw:-<not in .env — check SSM, or run: make admin-reset>}"

admin-reset: ## Rotate the deployed admin password. Optional PASSWORD=... EMAIL=... (auto-generates a strong one if PASSWORD unset)
	@test -f .env || { echo "ERROR: .env not found — run from the repo root (e.g. cd /opt/vedha)"; exit 1; }
	@email="$(EMAIL)"; [ -n "$$email" ] || email=$$(grep -m1 '^SEED_ADMIN_EMAIL=' .env | cut -d= -f2-); email=$${email:-admin@vedha.io}; \
	 pw="$(PASSWORD)"; [ -n "$$pw" ] || pw="$$(openssl rand -base64 18 | tr -d '\n/+=')Aa1!"; \
	 echo "→ Rotating admin password for $$email on the running deploy stack..."; \
	 $(ADMIN_COMPOSE) run --rm -e SEED_ADMIN_FORCE_RESET=true -e SEED_ADMIN_EMAIL="$$email" -e SEED_ADMIN_PASSWORD="$$pw" migrate python scripts/seed_admin.py || { echo "ERROR: seeder failed — is the stack up?  ($(ADMIN_COMPOSE) ps)"; exit 1; }; \
	 awk -v e="$$email" -v p="$$pw" 'BEGIN{de=0;dp=0} /^SEED_ADMIN_EMAIL=/{print "SEED_ADMIN_EMAIL=" e; de=1; next} /^SEED_ADMIN_PASSWORD=/{print "SEED_ADMIN_PASSWORD=" p; dp=1; next} {print} END{if(!de)print "SEED_ADMIN_EMAIL=" e; if(!dp)print "SEED_ADMIN_PASSWORD=" p}' .env > .env.admin.tmp && mv .env.admin.tmp .env && chmod 600 .env; \
	 echo ""; \
	 echo "✓ Admin password rotated and saved to .env"; \
	 echo "   Email    : $$email"; \
	 echo "   Password : $$pw"; \
	 echo "   Log in at your dashboard URL (you can also change it later in Settings)."

sync-vuln-snapshots: ## Refresh pinned vuln intel (OSV + full EPSS + CISA KEV + NVD/CPE). Rebuild after.
	cd manager/detection_engine && python3 update_snapshot.py all && python3 build_nvd_cpe_snapshot.py
	@echo "Snapshots refreshed → commit them and rebuild the image (make api-only / make up)."

shell: ## Open a shell in the API container
	$(COMPOSE) exec api sh

venv: ## Create manager/backend/.venv and install deps (needed by `make test`)
	cd manager/backend && python3 -m venv .venv && ./.venv/bin/pip install -q -U pip && ./.venv/bin/pip install -q -r requirements.txt
	@echo "venv ready → run: make test"

test: ## Run the backend test suite locally (auto-creates .venv if missing)
	@test -x manager/backend/.venv/bin/python || $(MAKE) venv
	cd manager/backend && ./.venv/bin/python -m pytest -q

probe-build: ## Build the probe image
	$(COMPOSE) build probe

probe-run: ## Start a local probe (joins the stack, self-registers)
	$(COMPOSE) --profile probe up -d probe

probe-pat: ## Mint a probe-scoped PAT (vpat_...) to deploy a real probe. ARGS="--days 90"
	@sh scripts/issue_pat.sh $(ARGS)

seal: ## Build the SEALED native-binary probe (no source/bytecode). ARGS="--hostid <id>"
	@cd probe && ./seal-probe.sh $(ARGS)

seal-parity: ## Local sealed-vs-plaintext manifest parity check (needs Docker; ~build time)
	@bash scripts/seal_parity.sh

# ── Agent release (served by the manager; never a public registry) ───────────
# Build machine only: the private key never goes on the manager server.
#   make agent-keygen                       once; prints AGENT_RELEASE_PUBLIC_KEY for .env
#   make agent-release                      build + sign amd64 and arm64 from VERSION
#   make agent-publish TO=user@host:/opt/Project-Vedha/manager/agent-releases
AGENT_RELEASE_KEY ?= $(HOME)/.vedha/agent-release-key.pem
AGENT_ARCH ?= amd64,arm64
RELEASE_PY := $(shell test -x manager/backend/.venv/bin/python && echo manager/backend/.venv/bin/python || echo python3)

agent-keygen: ## Create the agent release signing key (build machine only; prints the public key for .env)
	@$(RELEASE_PY) scripts/agent_release.py keygen --out "$(AGENT_RELEASE_KEY)"

agent-release: ## Build + sign the agent release from VERSION [AGENT_ARCH=amd64,arm64] [AGENT_RELEASE_KEY=...]
	@$(RELEASE_PY) scripts/agent_release.py build --key "$(AGENT_RELEASE_KEY)" --arch "$(AGENT_ARCH)"

agent-verify: ## Verify the built release: make agent-verify PUB=<AGENT_RELEASE_PUBLIC_KEY>
	@$(RELEASE_PY) scripts/agent_release.py verify dist/agent-release --public-key "$(PUB)"

agent-publish: ## Copy the built release to the manager: make agent-publish TO=user@host:/path (or a local dir)
	@test -n "$(TO)" || { echo "TO is required, e.g. TO=ubuntu@1.2.3.4:/opt/Project-Vedha/manager/agent-releases (local dev: TO=manager/agent-releases)"; exit 2; }
	@$(RELEASE_PY) scripts/agent_release.py publish dist/agent-release --to "$(TO)"

# On request only: an encrypted, signed platform bundle for ONE on-prem customer.
#   make onprem-bundle CUSTOMER="ACME Bank" RECIPIENT=age1...   (their `age-keygen` public key)
onprem-bundle: ## On-prem customer bundle (encrypted to them, signed): make onprem-bundle CUSTOMER=... RECIPIENT=age1...
	@test -n "$(CUSTOMER)" -a -n "$(RECIPIENT)" || { echo "CUSTOMER and RECIPIENT (the customer's age public key) are required"; exit 2; }
	@$(RELEASE_PY) scripts/onprem_bundle.py build --customer "$(CUSTOMER)" --recipient "$(RECIPIENT)" --key "$(AGENT_RELEASE_KEY)" $(if $(wildcard dist/agent-release/CURRENT),--agent-release dist/agent-release,)

# ── AWS / EC2 deploy targets ──────────────────────────────────────────────────
# All use the PROBE-FREE manager stack. `make full` is the full-stack deploy;
# aws-up is the lighter API/probe-plane-only variant (no dashboard).
AWS_COMPOSE := $(MANAGER_COMPOSE)

gen-env: ## Auto-generate .env with real random secrets (safe to re-run — skips existing values)
	@bash scripts/gen-env.sh

aws-up: gen-env ## AWS: build + start the API/probe plane behind the port-80 edge ingress (no dashboard)
	$(AWS_COMPOSE) build api
	$(DEPLOY_COMPOSE) $(INGRESS_PROFILE) up -d --remove-orphans
	@eport=$$(grep -m1 '^EDGE_HTTP_PORT=' .env 2>/dev/null | cut -d= -f2); eport=$${eport:-80}; \
	 aport=$$(grep -m1 '^API_PORT=' .env 2>/dev/null | cut -d= -f2); aport=$${aport:-18080}; \
	 echo ""; \
	 echo "  API (edge)  → http://<EC2-IP>$$( [ "$$eport" = 80 ] && echo '' || echo ":$$eport" )/health   ← probes dial this"; \
	 echo "  API (direct)→ http://<EC2-IP>:$$aport/health  (needs SG rule for $$aport)"; \
	 echo "  Docs        → http://<EC2-IP>/docs"; \
	 echo "  Logs        → make aws-logs   |   Status → make aws-ps"; \
	 echo "  NOTE: open inbound TCP $$eport in the EC2 security group for external access."

aws-up-ui: full ## AWS: alias for `make full` (complete manager stack incl. dashboard)

aws-logs: ## Tail API + worker logs on AWS
	$(AWS_COMPOSE) logs -f api worker

aws-ps: ## Show AWS stack container status
	$(AWS_COMPOSE) ps

aws-down: ## Stop the AWS stack incl. edge + any stray probe (keeps volumes / data)
	$(DEPLOY_COMPOSE) --profile edge --profile ui down --remove-orphans

prod-diagnose: ## Diagnose + auto-heal common prod issues (missing Caddy, stale health check, migration mismatch)
	@chmod +x scripts/prod-diagnose.sh && bash scripts/prod-diagnose.sh

# ── HTTPS (Let's Encrypt via Caddy) ───────────────────────────────────────────
# One command on the server:  make tls DOMAIN=vedha.example.com EMAIL=you@example.com
# Extra flags via TLS_ARGS, e.g. TLS_ARGS="--route53 --open-ports" or "--staging".
tls: ## HTTPS in one command: make tls DOMAIN=vedha.example.com EMAIL=you@x.com [TLS_ARGS="--route53 --open-ports"]
	@bash scripts/enable-tls.sh --domain "$(DOMAIN)" --email "$(EMAIL)" $(TLS_ARGS)

tls-check: ## Diagnose DNS / ports / CAA for HTTPS without changing anything: make tls-check DOMAIN=...
	@bash scripts/enable-tls.sh --check --domain "$(DOMAIN)" $(TLS_ARGS)

tls-status: ## Show certificate issuer + expiry for the HTTPS hosts
	@bash scripts/enable-tls.sh --status

tls-rollback: ## Undo `make tls`: restore the previous .env and the plain-HTTP port-80 edge
	@bash scripts/enable-tls.sh --rollback
