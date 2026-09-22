"""
ScopeError is a ValueError, and nothing in the suite may reload a module.

`importlib.reload()` rebinds every class in a module to a NEW object. A handler
or `pytest.raises` holding a name bound before the reload then matches a class
nothing raises any more — the fresh class is not a subclass of the stale one,
so no choice of base class can fix it. The hazard is removed at its source:
the suite does not reload, and the guard below keeps it that way.

The ValueError base stays for what it says: a boundary that is not an IP or
CIDR is a bad value, as ipaddress itself reports. Every handler around a scope
call fails closed, so a wider catch changes which branch reports a refusal,
never whether a target gets scanned — TestTheGateStillRefuses pins that.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from scanner import scanner_base as sb

TESTS_DIR = Path(__file__).resolve().parent


class TestNoReload:
    def test_scope_error_is_a_value_error(self):
        assert issubclass(sb.ScopeError, ValueError)

    def test_no_test_reloads_a_module(self):
        offenders = []
        for path in sorted(TESTS_DIR.glob("test_*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                fn = node.func
                name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
                if name == "reload":
                    offenders.append(f"{path.name}:{node.lineno}")
        assert offenders == [], (
            "reload rebinds classes and breaks every name bound before it; "
            f"patch the module attribute instead: {offenders}")


class TestTheGateStillRefuses:
    """A widened catch must not widen the SCOPE. These assert the refusal
    itself, independent of which handler reports it."""

    def test_out_of_scope_target_is_still_refused(self):
        guard = sb.ScopeGuard.from_list(["10.0.0.0/24"])
        assert guard.in_scope("192.168.1.1") is False
        with pytest.raises(sb.ScopeError):
            guard.assert_in_scope("192.168.1.1")

    def test_strict_mode_still_rejects_a_malformed_boundary(self):
        with pytest.raises(sb.ScopeError, match="10.0.0.0/244"):
            sb.ScopeGuard.from_list(["10.0.0.0/244"], strict=True)

    def test_strict_mode_still_rejects_a_malformed_exclusion(self):
        """The dangerous direction: a dropped exclusion SCANS the host the
        operator carved out."""
        with pytest.raises(sb.ScopeError, match="10.0.0.5/33"):
            sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=["10.0.0.5/33"], strict=True)

    def test_an_excluded_host_is_still_out_of_scope(self):
        guard = sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=["10.0.0.5"])
        assert guard.in_scope("10.0.0.5") is False
        assert guard.in_scope("10.0.0.6") is True
