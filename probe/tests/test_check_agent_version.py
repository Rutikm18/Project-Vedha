"""The agent-version gate: shipped agent code may not change without a version bump."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

PROBE = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_agent_version", PROBE / "tools" / "check_agent_version.py")
gate = importlib.util.module_from_spec(_spec)
sys.modules["check_agent_version"] = gate
_spec.loader.exec_module(gate)

SHIPPED = {"probe/agent/agent.py", "probe/agent/transport.py", "probe/scanner/port_scanner.py",
           "probe/agent/version.py"}


def evaluate(changed, base, head):
    return gate.evaluate(changed, SHIPPED, base, head)


class TestEvaluate:
    def test_nothing_shipped_changed_needs_no_bump(self):
        assert evaluate(["docs/readme.md", "probe/tests/test_x.py", "manager/backend/app/x.py"],
                        "2.1.0", "2.1.0") == []

    def test_shipped_change_with_a_bump_is_fine(self):
        assert evaluate(["probe/agent/agent.py"], "2.1.0", "2.1.1") == []
        assert evaluate(["probe/scanner/port_scanner.py"], "2.1.0", "3.0.0") == []

    def test_shipped_change_without_a_bump_fails(self):
        problems = evaluate(["probe/agent/agent.py"], "2.1.0", "2.1.0")
        assert len(problems) == 1 and "probe/agent/agent.py" in problems[0] and "Bump" in problems[0]

    def test_a_lower_version_is_not_a_bump(self):
        assert evaluate(["probe/agent/transport.py"], "2.1.0", "2.0.9")

    def test_numeric_not_lexical(self):
        assert evaluate(["probe/agent/agent.py"], "2.9.0", "2.10.0") == []
        assert evaluate(["probe/agent/agent.py"], "2.10.0", "2.9.0")

    def test_only_the_version_file_changing_needs_nothing(self):
        assert evaluate(["probe/agent/version.py"], "2.1.0", "2.1.0") == []

    def test_introducing_the_version_file_is_allowed(self):
        assert evaluate(["probe/agent/agent.py", "probe/agent/version.py"], None, "2.1.0") == []

    def test_unreadable_head_version_fails(self):
        assert evaluate(["probe/agent/agent.py"], "2.1.0", None)
        assert evaluate(["probe/agent/agent.py"], "2.1.0", "garbage")

    def test_long_file_lists_are_summarised(self):
        shipped = {f"probe/scanner/s{i}.py" for i in range(20)} | {"probe/agent/version.py"}
        problems = gate.evaluate(sorted(shipped - {"probe/agent/version.py"}), shipped, "2.1.0", "2.1.0")
        assert "(+12 more)" in problems[0]


class TestRealRepo:
    def test_version_file_parses(self):
        text = (PROBE / "agent" / "version.py").read_text(encoding="utf-8")
        assert gate.read_agent_version(text) is not None

    def test_shipped_files_are_the_agent_not_the_rest(self):
        shipped = gate.shipped_files()
        assert "probe/agent/agent.py" in shipped
        assert "probe/agent/version.py" in shipped
        assert "probe/agent/update_check.py" in shipped
        assert "probe/requirements-runtime.txt" in shipped      # dependencies change the agent too
        assert not any("/tests/" in f or "/main_scripts/" in f or "/cve/" in f for f in shipped)
        assert "probe/scanner/findings.py" not in shipped

    def test_read_agent_version(self):
        assert gate.read_agent_version('AGENT_VERSION = "2.4.6"\n') == "2.4.6"
        assert gate.read_agent_version("AGENT_VERSION = '1.0'") == "1.0"
        assert gate.read_agent_version("# nothing here") is None

    def test_release_tool_and_gate_read_the_same_value(self):
        spec = importlib.util.spec_from_file_location("agent_release_tool", PROBE.parent / "scripts" / "agent_release.py")
        tool = importlib.util.module_from_spec(spec)
        sys.modules["agent_release_tool"] = tool
        spec.loader.exec_module(tool)
        text = (PROBE / "agent" / "version.py").read_text(encoding="utf-8")
        assert tool.read_agent_version() == gate.read_agent_version(text)
