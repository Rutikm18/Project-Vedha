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
    original = Settings.model_config.get("env_file")
    Settings.model_config["env_file"] = None
    try:
        yield
    finally:
        Settings.model_config["env_file"] = original
