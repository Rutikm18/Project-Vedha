"""Phase 7 — Layer-2 dependency install logic (wheel-first, strict = wheel-only).
Pure."""
from __future__ import annotations

import os

from agent import deps as d


def test_venv_python_is_os_correct():
    p = d.venv_python("/opt/probe")
    if os.name == "nt":
        assert p.endswith("Scripts\\python.exe") or p.endswith("Scripts/python.exe")
    else:
        assert p.endswith(".venv/bin/python")


def test_reqs_hash_stable_and_sensitive(tmp_path):
    f = tmp_path / "r.txt"
    f.write_text("httpx>=0.27\n")
    h1 = d.reqs_hash(str(f))
    assert h1 == d.reqs_hash(str(f))
    f.write_text("httpx>=0.27\nwebsockets>=12\n")
    assert d.reqs_hash(str(f)) != h1


def test_permissive_is_wheel_first_then_source_fallback():
    sets = d.pip_install_argsets("/v/bin/python", "/p/req.txt", strict=False)
    assert len(sets) == 2
    assert "--only-binary=:all:" in sets[0]
    assert "--only-binary=:all:" not in sets[1]     # source fallback allowed


def test_strict_is_wheel_only_no_source_build():
    sets = d.pip_install_argsets("/v/bin/python", "/p/req.txt", strict=True)
    assert len(sets) == 1
    assert "--only-binary=:all:" in sets[0]         # never compiles untrusted source
    for s in sets:
        assert s[:3] == ["/v/bin/python", "-m", "pip"] and "-r" in s
