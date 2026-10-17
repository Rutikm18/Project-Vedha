"""
test_gen_env_public_url.py — scripts/gen-env.sh must never downgrade an https://
MANAGER_PUBLIC_URL to http://<public-ip>.

Field bug (Oct 2026): deploy/aws/install.sh writes MANAGER_PUBLIC_URL=https://get.<domain>
but no TLS_DOMAIN, so the next `make full` ran gen-env.sh, which replaced it with
http://<ip>. The Windows installer only talks to https://, so Fleet → Add agent lost
every Windows install command ("This manager address cannot be embedded safely").
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
GEN_ENV = REPO / "scripts" / "gen-env.sh"

pytestmark = pytest.mark.skipif(not (shutil.which("bash") and shutil.which("openssl")),
                                reason="needs bash and openssl")


def _run(tmp_path: Path, env_text: str) -> str:
    env_file = tmp_path / ".env"
    env_file.write_text(env_text)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    # Fake curl: no IMDS token, and checkip answers with a fixed public IP.
    (fake_bin / "curl").write_text(
        '#!/bin/sh\ncase "$*" in *checkip*) printf "16.4.75.44\\n" ;; *) exit 7 ;; esac\n')
    (fake_bin / "curl").chmod(0o755)
    (fake_bin / "docker").write_text("#!/bin/sh\nexit 1\n")
    (fake_bin / "docker").chmod(0o755)
    env = {**os.environ, "ENV_FILE": str(env_file), "PATH": f"{fake_bin}:{os.environ['PATH']}"}
    subprocess.run(["bash", str(GEN_ENV)], env=env, check=True, capture_output=True, text=True)
    return env_file.read_text()


def _get(text: str, key: str) -> str:
    for line in text.splitlines():
        if line.startswith(key + "="):
            return line.split("=", 1)[1]
    return ""


def test_https_facade_written_by_install_sh_is_kept(tmp_path):
    out = _run(tmp_path, "APP_ENV=production\nAUTH_COOKIE_SECURE=true\n"
                         "MANAGER_PUBLIC_URL=https://get.vedhasec.com\nCORS_ORIGINS=https://vedhasec.com\n")
    assert _get(out, "MANAGER_PUBLIC_URL") == "https://get.vedhasec.com"
    assert _get(out, "CORS_ORIGINS") == "https://vedhasec.com"


def test_plain_http_testing_path_still_follows_the_public_ip(tmp_path):
    out = _run(tmp_path, "MANAGER_PUBLIC_URL=http://10.0.0.9\n")
    assert _get(out, "MANAGER_PUBLIC_URL") == "http://16.4.75.44"


def test_unset_url_gets_the_public_ip(tmp_path):
    out = _run(tmp_path, "")
    assert _get(out, "MANAGER_PUBLIC_URL") == "http://16.4.75.44"
