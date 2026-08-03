from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

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

    # JWT
    jwt_secret: str = "change-me-at-least-32-chars-long!!"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Manager-owned AI runtime. The dashboard never receives provider credentials
    # and never calls a model directly. Ollama is the free/local default;
    # OpenRouter and Anthropic are optional server-side providers.
    llm_provider: str = "ollama"
    llm_request_timeout_seconds: float = 180.0
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
