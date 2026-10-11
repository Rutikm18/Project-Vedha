"""Shared pytest fixtures for the Manager backend.

config.py now loads the repo-root .env by ABSOLUTE path so the app boots with the
same secrets no matter which working directory the process starts from (a plain
`uvicorn app.main:app` run from manager/backend/ used to silently load zero keys).

The side effect: without this fixture, tests would inherit the developer's real
.env (API keys, LLM_PROVIDER, etc.) and stop being deterministic — e.g. a
"no cloud key configured → fail closed" test would see a real GEMINI/ANTHROPIC key.
Previously the suite was isolated only by accident (pytest runs from manager/backend,
which has no .env of its own). Make that isolation explicit and permanent:
neutralize dotenv loading for the whole test session. Tests that need settings pass
them explicitly via Settings(**kwargs), which take precedence over env files anyway.
"""
import pytest

from app.config import Settings


@pytest.fixture(autouse=True, scope="session")
def _isolate_settings_from_dotenv():
    from app.config import get_settings

    original = Settings.model_config.get("env_file")
    Settings.model_config["env_file"] = None
    # get_settings() is lru_cached and is usually first called at IMPORT time —
    # before this fixture runs — so the cached instance would still carry the
    # developer's real .env keys. Drop it so every test sees key-free settings.
    get_settings.cache_clear()
    try:
        yield
    finally:
        Settings.model_config["env_file"] = original
        get_settings.cache_clear()


@pytest.fixture(autouse=True)
def _fresh_ai_kv():
    """The AI router keeps cooldowns, spend and stored answers in a shared KV
    (Redis in production). Give every test its own in-memory store so state never
    leaks between tests and no test touches a real Redis."""
    from app.ai.kv import MemoryKv, set_default_kv

    set_default_kv(MemoryKv())
    try:
        yield
    finally:
        set_default_kv(None)


@pytest.fixture(autouse=True)
def _offline_dns(monkeypatch):
    """Tenant-supplied outbound hosts (Jira, Slack webhook, SMTP...) are resolved by
    the SSRF guard before any request. Tests use made-up names like acme.service-now.com
    and must not depend on real DNS (or fail offline), so a name that does not resolve
    is treated as a public address. IP literals and real answers are untouched; tests
    of the guard itself (test_outbound_guard.py) restore the real resolver."""
    import ipaddress

    from app.services import outbound_guard as og

    real = og._resolve

    def resolve(host, port):
        try:
            return real(host, port)
        except og.OutboundBlocked:
            return [ipaddress.ip_address("93.184.216.34")]

    monkeypatch.setattr(og, "_resolve", resolve)
