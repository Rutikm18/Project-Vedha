"""The agent-release-sync service must stay small, opt-in and secret-free, in BOTH compose files.

Production (manager/docker-compose.yml, installed by deploy/aws/install.sh) is the file that matters; the
repo-root file is for local development. The service pulls signed releases from GitHub into the folder the api
serves, so what it is allowed to see is the whole security story: public keys and an optional read-only GitHub
token, never the database, Redis, JWT secret or a signing key.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
FILES = [ROOT / "manager" / "docker-compose.yml", ROOT / "docker-compose.yml"]
FORBIDDEN = ("DATABASE_URL", "REDIS_URL", "JWT_SECRET", "POSTGRES", "SIGNING_KEY", "PROBE_POLICY", "NEO4J", "LLM_", "SEED_")


@pytest.fixture(params=FILES, ids=lambda p: p.parent.name + "/" + p.name)
def compose(request):
    return yaml.safe_load(request.param.read_text(encoding="utf-8"))


def test_the_service_is_opt_in(compose):
    service = compose["services"]["agent-release-sync"]
    assert service["profiles"] == ["release-sync"]            # `docker compose up` alone never starts it


def test_it_runs_the_watch_command_from_the_backend_image(compose):
    service = compose["services"]["agent-release-sync"]
    assert service["command"][:3] == ["python", "scripts/agent_release.py", "watch"]
    assert "build" in service and service["image"]            # the same image the api uses: no extra thing to build


def test_it_sees_only_public_keys_and_its_own_settings(compose):
    env = compose["services"]["agent-release-sync"]["environment"]
    assert set(env) == {
        "AGENT_RELEASE_GITHUB_REPO", "AGENT_RELEASE_GITHUB_TOKEN", "AGENT_RELEASE_SYNC_INTERVAL_MINUTES",
        "AGENT_RELEASE_SYNC_AUTO_PROMOTE", "AGENT_RELEASE_PUBLIC_KEY", "AGENT_RELEASE_P256_PUBLIC_KEY", "TZ",
    }
    assert not [k for k in env for bad in FORBIDDEN if bad in k]


def test_it_is_locked_down_and_can_write_only_the_release_folder(compose):
    service = compose["services"]["agent-release-sync"]
    assert service["read_only"] is True and service["cap_drop"] == ["ALL"]
    assert "no-new-privileges:true" in service["security_opt"]
    assert "ports" not in service and "depends_on" not in service       # no listener, no database, no redis
    mounts = service["volumes"]
    assert len(mounts) == 1 and mounts[0].endswith(":/var/lib/vedha/agent-releases")
    assert not mounts[0].endswith(":ro")                                 # it must be able to write the store


def test_the_api_still_mounts_the_same_folder_read_only(compose):
    assert any(v.endswith(":/var/lib/vedha/agent-releases:ro") for v in compose["services"]["api"]["volumes"])


def test_tokenless_install_can_be_switched_on_from_the_env_file_in_both_files(compose):
    env = compose["x-backend-env"]
    assert env["AGENT_ALLOW_TOKENLESS_INSTALL"].endswith(":-false}")     # off unless the owner turns it on
