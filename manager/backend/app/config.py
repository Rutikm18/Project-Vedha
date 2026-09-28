from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env to ABSOLUTE paths so the backend loads the same secrets no matter
# which working directory it is started from. A relative ".env" only resolved when
# the process happened to start at the repo root, so a plain `uvicorn app.main:app`
# run from manager/backend/ silently loaded ZERO keys — leaving /ai/status with no
# provider and disabling the AI Brain composer.
# app/config.py → app → backend → manager → repo root.
_BACKEND_DIR = Path(__file__).resolve().parent.parent          # manager/backend
_REPO_ROOT = _BACKEND_DIR.parent.parent                        # repo root
# Later files override earlier ones; a local manager/backend/.env wins over the
# repo-root .env. In containers neither may exist and injected environment
# variables take precedence regardless, so this is a safe no-op there.
_ENV_FILES = (_REPO_ROOT / ".env", _BACKEND_DIR / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILES, env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://vapt:secret@localhost:5432/vapt_db"
    # P3: optional read-replica DSN. When set, read-heavy endpoints route here,
    # offloading the dashboard's aggregate reads from the primary. Unset →
    # reads fall back to the primary, so this is a no-op until a replica exists.
    database_read_url: str | None = None

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Database connection pool — these are per-process (each uvicorn worker has its
    # own pool). Keep pool_size small on shared EC2 to avoid exhausting Postgres
    # max_connections (default 100) with API_WORKERS=2 + background worker.
    db_pool_size: int = 5
    db_max_overflow: int = 5
    db_pool_recycle: int = 280   # recycle before AWS TCP idle kills at 350s
    db_pool_timeout: int = 10    # fail fast; don't hold up the request path

    # Job leasing: a claimed (running) job carries a lease renewed on every probe
    # heartbeat. If the probe dies mid-scan the lease expires and the reaper requeues
    # the job (pending) so it isn't stuck 'running' forever. Lease must comfortably
    # exceed the probe heartbeat interval (~30s); reaper runs on its own cadence.
    job_lease_seconds: int = 300
    reaper_interval_seconds: int = 60

    # Neo4j (attack-path graph store — optional; engine falls back to in-memory NetworkX)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "neo4j"
    neo4j_enabled: bool = False

    # P2 — passive verification (deterministic verdict always; LLM/LangGraph optional)
    verification_enabled: bool = True

    # JWT
    jwt_secret: str = "change-me-at-least-32-chars-long!!"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Manager-owned AI runtime. The dashboard never receives provider credentials
    # and never calls a model directly. Cloud-only by default: every configured cloud
    # key joins an automatic premium-first chain (anthropic → openai → gemini →
    # groq → openrouter) and the manager fails closed if none is set. A pinned
    # LLM_PROVIDER is tried first. "ollama" is an explicit local-dev opt-in and is
    # never selected automatically or used as an implicit fallback.
    llm_provider: str = ""
    # Ordered, automatic fallback chain (app/ai/routing.py), e.g.
    # "anthropic,openai,gemini,groq,openrouter". Empty = that premium-first default
    # with LLM_PROVIDER (if set) moved to the front. Unconfigured entries are skipped.
    llm_chain: str = ""
    # AI egress policy (app/ai/gateway.py). cloud = raw to cloud providers;
    # hybrid = cloud only with network identifiers pseudonymized (BFSI default);
    # sovereign = local models only, cloud refused. AI_PSEUDONYMIZE=true opts a
    # cloud deployment into pseudonymization too.
    deployment_profile: str = "cloud"
    ai_pseudonymize: bool = False
    # Offline intel bundles (app/intel/bundle.py) for air-gapped managers:
    # comma-separated base64 Ed25519 public keys trusted to sign bundles, and the
    # writable directory the detection engine prefers over its packaged snapshots.
    intel_bundle_public_keys: str = ""
    vedha_intel_dir: str = ""
    llm_request_timeout_seconds: float = 180.0
    # In-bank OpenAI-compatible model server (vLLM / TGI / LM Studio / Ollama /v1)
    # for sovereign deployments: LLM_PROVIDER=local_openai. The base URL must be a
    # private/internal address — a public URL labelled "local" is refused.
    local_llm_base_url: str = ""
    local_llm_model: str = ""
    local_llm_api_key: str = ""
    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "llama3.2:3b"
    openrouter_api_key: str = ""
    openrouter_model: str = "openrouter/free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_site_url: str = "https://vedha.local"
    openrouter_app_name: str = "Vedha"
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-6"
    # OpenAI — server-side cloud provider. Uses the same /chat/completions shape
    # as OpenRouter. Only openai_model is enabled by the deployment.
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    # Google Gemini — server-side cloud provider. Uses the Generative Language
    # `generateContent` API (NOT OpenAI-compatible), so it has its own adapter.
    # Get a key at aistudio.google.com/apikey (standard keys look like `AIza...`).
    # Set LLM_PROVIDER=gemini to make it the default; otherwise it is selectable.
    gemini_api_key: str = ""
    gemini_model: str = "gemini-flash-latest"  # 'gemini-2.0-flash' was retired (404); the -latest alias self-heals
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    # True when the Gemini key's project has billing enabled. Google's free tier may
    # use prompts to improve its products, so a free Gemini key is always sent
    # pseudonymized data; a paid one is treated as the "budget" tier.
    gemini_paid: bool = False
    # Groq — OpenAI-compatible free tier (console.groq.com). Free tier: always
    # pseudonymized by the AI gateway.
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    # Daily spend caps per provider in USD, e.g. "anthropic=20,openai=10". A
    # provider past its cap is skipped until midnight (IST) and the chain moves on.
    ai_daily_cap_usd: str = ""
    # Extra model prices (USD per 1M tokens, input:output), e.g. "gpt-4.1=2:8".
    # claude-sonnet-4-6 is built in; unpriced models are not metered.
    ai_model_prices: str = ""
    # Reuse window for answers to byte-identical one-shot requests (briefs,
    # refinement, compliance, report sections). 0 disables reuse.
    ai_answer_cache_ttl_seconds: int = 604800
    llm_max_tokens: int = 4096
    # Reasoning depth = token spend. Report writing is straightforward generation, so
    # "low" minimizes thinking-token cost on thinking-capable models (Sonnet 4.6,
    # Opus 4.6+, and Fable 5 — where thinking is always on and billed). Blank it to
    # omit output_config entirely for models that reject the effort parameter
    # (Sonnet 4.5 / Haiku 4.5). This replaces the old `temperature` knob, which
    # returns a 400 on Opus 4.7/4.8 and Fable 5.
    llm_effort: str = "low"
    llm_max_retries: int = 5

    # SLA remediation windows (hours from when a finding is first seen). A finding
    # still in an open/confirmed state past its window is "breached". 0 disables the
    # SLA clock for that severity (info findings carry no remediation deadline by
    # default). Tunable per deployment via SLA_HOURS_* env vars.
    sla_hours_critical: int = 24
    sla_hours_high: int = 72
    sla_hours_medium: int = 168   # 7 days
    sla_hours_low: int = 720      # 30 days
    sla_hours_info: int = 0       # no SLA

    # Legacy shared-secret bootstrap is unsafe for multi-tenant production. It is
    # disabled even when an old key remains in the environment unless a developer
    # deliberately enables the compatibility flag. Device-key enrollment replaces
    # this path.
    allow_unsafe_legacy_probe_bootstrap: bool = False
    probe_bootstrap_key: str = ""
    # Base64-encoded 32-byte Ed25519 private seed used only to sign immutable
    # Site policy envelopes. Production must provide a key distinct from JWT.
    # Development derives an ephemeral-compatible seed from JWT_SECRET.
    probe_policy_signing_key: str = ""

    # Trust-on-first-use probe enrollment. When TRUE, a probe that POSTs a device
    # enrollment request is auto-approved and issued an agent token with NO
    # operator action and NO pre-shared token — the probe's own keypair is its id.
    # Intended for single-owner / trusted-network fleets ("all ours"). OFF by
    # default: leaving it off means every probe needs a pre-authorized token or a
    # dashboard approval. Every auto-enrollment is written to the audit log.
    probe_auto_enroll: bool = False
    # Coarse authorized scope stamped on the auto-enroll Site policy (the probe
    # still enforces its own local ceiling, and jobs carry per-engagement scope).
    probe_auto_enroll_cidrs: str = "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

    # Peers whose X-Forwarded-For is believed (Caddy + the Next BFF on the private
    # docker network). A request from any other peer is keyed on its socket IP,
    # so a direct caller cannot spoof its way past the rate limiter.
    trusted_proxy_cidrs: str = "127.0.0.0/8,::1/128,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

    # App
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # CORS — accept a comma-separated string from CORS_ORIGINS and expose it as a
    # list. Declared as `str` on purpose: pydantic-settings JSON-decodes any env
    # value bound to a complex type (list/dict), and a bare "a,b" CSV isn't valid
    # JSON — that raised `SettingsError: error parsing value for field cors_origins`.
    cors_origins_csv: str = Field(
        default="http://localhost:3000,http://localhost:3001",
        validation_alias="CORS_ORIGINS",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_csv.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
