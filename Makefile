# VEDHA — convenience wrapper around docker compose.
.DEFAULT_GOAL := help
COMPOSE := docker compose

# Deployed version, sourced from the repo-root VERSION file (auto-bumped by the
# .githooks/pre-commit hook). Exported so every `docker compose build` below bakes
# it into the backend image via the VEDHA_VERSION build arg.
export VEDHA_VERSION := $(shell cat VERSION 2>/dev/null || echo dev)

.PHONY: help doctor run full ui up up-graph up-ai api-only down logs ps migrate seed shell venv test probe-build probe-run probe-pat clean version setup-hooks aws-up aws-up-ui aws-down aws-logs aws-ps gen-env

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

full: ## Build + start THE WHOLE PROJECT (API + probe + Next.js dashboard). First build is slow.
	@test -f .env || cp .env.docker.example .env
	$(COMPOSE) build api
	$(COMPOSE) --profile ui build frontend
	$(COMPOSE) --profile probe build probe
	$(COMPOSE) --profile probe --profile ui up -d
	@fport=$$(grep -E '^FRONTEND_PORT=' .env | cut -d= -f2); fport=$${fport:-3000}; \
	  echo "Dashboard → http://localhost:$$fport   (login with SEED_ADMIN_EMAIL / SEED_ADMIN_PASSWORD)"

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

down: ## Stop all services (keeps volumes)
	$(COMPOSE) --profile graph --profile probe --profile ui --profile local-ai down

clean: ## Stop and DELETE volumes (wipes database and local AI models)
	$(COMPOSE) --profile graph --profile probe --profile ui --profile local-ai down -v

logs: ## Tail API logs
	$(COMPOSE) logs -f api

ps: ## Show service status
	$(COMPOSE) ps

migrate: ## Re-run database migrations
	$(COMPOSE) run --rm migrate alembic upgrade head

seed: ## Re-run the admin seeder
	$(COMPOSE) run --rm migrate python scripts/seed_admin.py

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

# ── AWS / EC2 testing targets ─────────────────────────────────────────────────
AWS_COMPOSE := docker compose --project-directory . -f manager/docker-compose.yml

gen-env: ## Auto-generate .env with real random secrets (safe to re-run — skips existing values)
	@bash scripts/gen-env.sh

aws-up: gen-env ## AWS: auto-generate .env + build + start API stack (no TLS/Caddy)
	$(AWS_COMPOSE) build api
	$(AWS_COMPOSE) up -d
	@aport=$$(grep -m1 '^API_PORT=' .env 2>/dev/null | cut -d= -f2); aport=$${aport:-18080}; \
	 echo ""; \
	 echo "  API     → http://<EC2-IP>:$$aport/health"; \
	 echo "  Docs    → http://<EC2-IP>:$$aport/docs"; \
	 echo "  Logs    → make aws-logs"; \
	 echo "  Status  → make aws-ps"

aws-up-ui: gen-env ## AWS: auto-generate .env + build + start API + frontend
	$(AWS_COMPOSE) build api
	$(AWS_COMPOSE) --profile ui build frontend
	$(AWS_COMPOSE) --profile ui up -d
	@aport=$$(grep -m1 '^API_PORT=' .env 2>/dev/null | cut -d= -f2); aport=$${aport:-18080}; \
	 fport=$$(grep -m1 '^FRONTEND_PORT=' .env 2>/dev/null | cut -d= -f2); fport=$${fport:-3000}; \
	 echo ""; \
	 echo "  Dashboard → http://<EC2-IP>:$$fport"; \
	 echo "  API       → http://<EC2-IP>:$$aport/health"

aws-logs: ## Tail API + worker logs on AWS
	$(AWS_COMPOSE) logs -f api worker

aws-ps: ## Show AWS stack container status
	$(AWS_COMPOSE) ps

aws-down: ## Stop the AWS stack (keeps volumes / data)
	$(AWS_COMPOSE) --profile ui down
