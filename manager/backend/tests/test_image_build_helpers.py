"""test_image_build_helpers.py — deploy/aws/images.sh, run with a fake `docker`.

The helper builds the two release images concurrently, skips a build whose
immutable tag already exists, and tidies old releases' images after a deploy.
These run it under the installer's own `set -Eeuo pipefail` so a tidy-up failure
that would abort a good deploy shows up here.
"""
from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
HELPER = REPO / "deploy" / "aws" / "images.sh"

FAKE_DOCKER = textwrap.dedent("""\
    #!/usr/bin/env bash
    echo "docker $*" >> "$CALLS"
    # `docker compose -f x.yml build <svc>`: the subcommand is not the second word.
    if [ "$1" = "compose" ] && [[ " $* " == *" build "* ]]; then
      last="${@: -1}"
      [ "${FAIL_SERVICE:-}" = "$last" ] && { echo "boom building $last"; exit 1; }
      echo "built $last"; exit 0
    fi
    case "$1 $2" in
      "image inspect") grep -qxF "$3" "$EXISTING" ;;
      "images --format") grep "^$4:" "$EXISTING" | grep -v ":$" || true ;;
      "image rm") if grep -qxF "$3" "$UNREMOVABLE"; then exit 1; fi; exit 0 ;;
      *) exit 0 ;;
    esac
""")


@pytest.fixture
def sandbox(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    docker = bindir / "docker"
    docker.write_text(FAKE_DOCKER)
    docker.chmod(0o755)
    (tmp_path / "existing").write_text("")
    (tmp_path / "unremovable").write_text("")
    (tmp_path / "calls").write_text("")
    return tmp_path


def _run(sandbox, body, **env):
    script = textwrap.dedent(f"""\
        set -Eeuo pipefail
        log()  {{ echo "LOG: $*"; }}
        warn() {{ echo "WARN: $*" >&2; }}
        COMPOSE_CMD=(docker compose -f x.yml)
        VEDHA_BACKEND_IMAGE=vedha-backend:aaaaaaaaaaaa
        VEDHA_FRONTEND_IMAGE=vedha-frontend:aaaaaaaaaaaa
        . "{HELPER}"
        {body}
        echo DONE
    """)
    full = {**os.environ, "PATH": f"{sandbox / 'bin'}:{os.environ['PATH']}", "CALLS": str(sandbox / "calls"),
            "EXISTING": str(sandbox / "existing"), "UNREMOVABLE": str(sandbox / "unremovable"),
            "DEPLOY_LOG": str(sandbox / "deploy.log"), **env}
    return subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=full)


def _calls(sandbox) -> list[str]:
    return (sandbox / "calls").read_text().splitlines()


def test_builds_both_images_when_neither_exists(sandbox):
    result = _run(sandbox, "build_images")
    assert result.returncode == 0 and "DONE" in result.stdout, result.stderr
    builds = [c for c in _calls(sandbox) if "compose" in c and c.endswith(("api", "frontend"))]
    assert sorted(b.split()[-1] for b in builds) == ["api", "frontend"]


def test_skips_a_service_whose_release_image_already_exists(sandbox):
    (sandbox / "existing").write_text("vedha-backend:aaaaaaaaaaaa\n")
    result = _run(sandbox, "build_images")
    assert result.returncode == 0
    built = [c.split()[-1] for c in _calls(sandbox) if "compose" in c]
    assert built == ["frontend"]                      # the backend was reused
    assert "reusing vedha-backend:aaaaaaaaaaaa" in (sandbox / "deploy.log").read_text()


def test_force_rebuild_ignores_existing_images(sandbox):
    (sandbox / "existing").write_text("vedha-backend:aaaaaaaaaaaa\nvedha-frontend:aaaaaaaaaaaa\n")
    result = _run(sandbox, "build_images", FORCE_REBUILD="1")
    assert result.returncode == 0
    assert sorted(c.split()[-1] for c in _calls(sandbox) if "compose" in c) == ["api", "frontend"]


def test_serial_mode_builds_one_after_the_other(sandbox):
    result = _run(sandbox, "build_images", SERIAL_BUILD="1")
    assert result.returncode == 0
    assert [c.split()[-1] for c in _calls(sandbox) if "compose" in c] == ["api", "frontend"]


def test_a_failed_build_fails_the_step_and_shows_why_but_the_other_still_finishes(sandbox):
    result = _run(sandbox, "build_images || echo STEP-FAILED", FAIL_SERVICE="frontend")
    assert "STEP-FAILED" in result.stdout
    assert "frontend image build failed" in result.stderr and "boom building frontend" in result.stderr
    assert "backend image build failed" not in result.stderr
    assert any(c.endswith("api") for c in _calls(sandbox))        # the backend build ran to completion
    log = (sandbox / "deploy.log").read_text()
    assert "built api" in log and "boom building frontend" in log


def test_old_release_images_are_removed_but_current_and_previous_are_kept(sandbox):
    (sandbox / "existing").write_text("\n".join([
        "vedha-backend:aaaaaaaaaaaa", "vedha-backend:bbbbbbbbbbbb", "vedha-backend:cccccccccccc",
        "vedha-frontend:aaaaaaaaaaaa", "vedha-frontend:bbbbbbbbbbbb", "vedha-frontend:cccccccccccc",
        "vedha-backend:local", "vedha-frontend:latest",
    ]) + "\n")
    result = _run(sandbox, "PREVIOUS_BACKEND_IMAGE=vedha-backend:bbbbbbbbbbbb; "
                           "PREVIOUS_FRONTEND_IMAGE=vedha-frontend:bbbbbbbbbbbb; prune_old_images")
    assert result.returncode == 0, result.stderr
    removed = sorted(c.split()[-1] for c in _calls(sandbox) if c.startswith("docker image rm"))
    assert removed == ["vedha-backend:cccccccccccc", "vedha-frontend:cccccccccccc"]   # not :local / :latest


def test_an_image_still_in_use_does_not_fail_a_good_deploy(sandbox):
    (sandbox / "existing").write_text("vedha-backend:cccccccccccc\nvedha-frontend:cccccccccccc\n")
    (sandbox / "unremovable").write_text("vedha-backend:cccccccccccc\nvedha-frontend:cccccccccccc\n")
    result = _run(sandbox, "prune_old_images")
    assert result.returncode == 0 and "DONE" in result.stdout, result.stderr


def test_build_cache_is_capped(sandbox):
    result = _run(sandbox, "prune_old_images", BUILD_CACHE_KEEP="2GB")
    assert result.returncode == 0
    assert any(c == "docker builder prune -f --keep-storage 2GB" for c in _calls(sandbox))


def test_installer_uses_the_helper_and_prunes_only_after_promotion():
    source = (REPO / "deploy" / "aws" / "install.sh").read_text()
    assert '. "$APP_DIR/deploy/aws/images.sh"' in source and "build_images ||" in source
    assert source.index("promoted immutable release") < source.index("prune_old_images")
