"""The agent we ship is its own import closure — never the judgement rules, the
campaign runner, main_scripts, cve or tests.

tools/agent_closure.py feeds every agent build (Linux image, compiled agent).
These tests pin what it includes, what it refuses, and that a dynamic import
(invisible to a compiler) fails the build instead of crashing in the field.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

PROBE = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("agent_closure", PROBE / "tools" / "agent_closure.py")
closure_tool = importlib.util.module_from_spec(_spec)
sys.modules["agent_closure"] = closure_tool  # dataclasses resolve their module by name
_spec.loader.exec_module(closure_tool)


def test_real_agent_closure_passes_and_holds_the_runtime():
    closure = closure_tool.compute()
    assert closure_tool.check(closure) == []
    for needed in ("agent.agent", "agent.transport", "agent.engine", "scanner.port_scanner",
                   "scanner.service_banner", "workflow"):
        assert needed in closure.modules, needed
    assert {"httpx", "websockets", "cryptography"} <= set(closure.third_party)


def test_sensitive_and_dev_modules_never_ship():
    modules = set(closure_tool.compute().modules)
    for forbidden in ("scanner.findings", "scanner.run_all", "scanner.va_campaign",
                      "scanner.accuracy", "scanner.accuracy_gate", "agent.setup",
                      "agent.deps", "agent.bootstrap", "agent.cli"):
        assert forbidden not in modules, forbidden
    assert not any(m.split(".")[0] in ("main_scripts", "cve", "tests") for m in modules)


def _fake_repo(tmp_path, agent_source: str, extra: dict[str, str] | None = None) -> Path:
    files = {
        "agent/__init__.py": "",
        "agent/agent.py": agent_source,
        "agent/helper.py": "from . import util\n",
        "agent/util.py": "X = 1\n",
        "scanner/__init__.py": "",
        "scanner/port_scanner.py": "import socket\n",
        "scanner/findings.py": "RULES = []\n",
        "scanner/unused.py": "",
        **(extra or {}),
    }
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return tmp_path


def test_follows_relative_and_function_level_imports(tmp_path):
    root = _fake_repo(tmp_path, "def run():\n    from agent import helper\n    import scanner.port_scanner\n")
    closure = closure_tool.compute(root)
    assert closure.modules == ["agent", "agent.agent", "agent.helper", "agent.util",
                               "scanner", "scanner.port_scanner"]
    assert "scanner.unused" not in closure.modules


def test_a_new_import_of_a_blocked_module_fails_the_check(tmp_path):
    root = _fake_repo(tmp_path, "from scanner import findings\n")
    problems = closure_tool.check(closure_tool.compute(root))
    assert problems == ["blocked module in the agent closure: scanner.findings"]


def test_a_dynamic_import_fails_the_check(tmp_path):
    root = _fake_repo(tmp_path, "import importlib\nmod = importlib.import_module('scanner.' + 'x')\n")
    problems = closure_tool.check(closure_tool.compute(root))
    assert len(problems) == 1 and "dynamic import" in problems[0] and "agent.agent:2" in problems[0]


def test_export_copies_only_the_closure(tmp_path):
    root = _fake_repo(tmp_path / "repo", "from agent import helper\n")
    dest = tmp_path / "out"
    count = closure_tool.export(closure_tool.compute(root), dest, root)
    shipped = sorted(p.relative_to(dest).as_posix() for p in dest.rglob("*.py"))
    assert shipped == ["agent/__init__.py", "agent/agent.py", "agent/helper.py", "agent/util.py"]
    assert count == 4


def test_cli_check_exit_codes(tmp_path, capsys):
    assert closure_tool.main(["--check"]) == 0
    root = _fake_repo(tmp_path, "import scanner.findings\n")
    assert closure_tool.main(["--check", "--root", str(root)]) == 1
    assert "scanner.findings" in capsys.readouterr().err


def test_generated_module_list_matches_the_closure():
    """agent/_closure.py drives `runtime-check`; regenerate it with
    `python tools/agent_closure.py --write-module` when imports change."""
    from agent._closure import MODULES
    assert list(MODULES) == closure_tool.compute().modules


def test_verified_names_pragma_allows_only_the_marked_line(tmp_path):
    root = _fake_repo(tmp_path, (
        "import importlib\n"
        "importlib.import_module('agent.util')  # agent-closure: verified-names\n"
        "importlib.import_module('agent.' + 'x')\n"
    ))
    problems = closure_tool.check(closure_tool.compute(root))
    assert len(problems) == 1 and "agent.agent:3" in problems[0]


def test_runtime_check_imports_every_agent_module():
    import subprocess
    import sys as _sys
    result = subprocess.run([_sys.executable, "-m", "agent.agent", "runtime-check"],
                            cwd=PROBE, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "runtime-check OK" in result.stdout


def test_both_dockerfiles_ship_only_the_closure_and_the_sealed_one_has_the_deep_libs():
    plain = (PROBE / "Dockerfile").read_text()
    sealed = (PROBE / "Dockerfile.sealed").read_text()
    for name, text in (("Dockerfile", plain), ("Dockerfile.sealed", sealed)):
        assert "tools/agent_closure.py --check" in text, name
        assert "COPY --from=select /closure/" in text, name
        assert "COPY scanner/" not in text, name          # never the whole folder
    assert "runtime-check" in plain
    # The sealed build once shipped without impacket/ldap3/dnspython, silently
    # degrading the SMB / LDAP / DNS deep branches on every sealed agent.
    assert "requirements-runtime.txt" in sealed
    for pkg in ("impacket", "ldap3", "dns"):
        assert f"--include-package={pkg}" in sealed
