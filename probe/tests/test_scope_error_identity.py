"""
ScopeError must stay catchable across a module reload.

`importlib.reload(scanner_base)` — which tests/test_project_timezone.py does —
rebinds every class in the module to a NEW object. Code holding a name bound at
import time then catches a class that nothing raises any more, and the exception
escapes. This already bit twice: once in a test, once in agent/engine.py's
run_scan, whose docstring promises it never raises.

The standing mitigation is a convention — "always reference it through the
module" — enforced only by comments, in a codebase where the natural spelling is
`from scanner.scanner_base import ScopeError`. Conventions that must be
remembered at every call site are not controls.

Making ScopeError a ValueError removes the hazard instead of documenting it: a
builtin is never reloaded, so `except ValueError` keeps working no matter how
many times the module is rebuilt. It is also true to the meaning — a scope entry
that is not an IP or CIDR is a bad value, and ipaddress raises ValueError for the
same input.

This does NOT soften the control. Every handler on every raise path is
fail-closed (error ScanResult / error result / exit 1), so a widened catch
changes which branch reports the refusal, never whether the target gets scanned.
TestTheGateStillRefuses pins that.
"""
from __future__ import annotations

import importlib

import pytest

from scanner import scanner_base as sb


class TestReloadSafety:
    def test_scope_error_is_a_value_error(self):
        """The whole point: a builtin base class survives any reload."""
        assert issubclass(sb.ScopeError, ValueError)

    def test_a_reload_really_does_rebind_the_class(self):
        """Guards the PREMISE. If reload ever stopped rebinding, this suite
        would be testing a hazard that no longer exists."""
        stale = sb.ScopeError
        try:
            importlib.reload(sb)
            assert sb.ScopeError is not stale
        finally:
            importlib.reload(sb)

    def test_a_handler_bound_before_a_reload_still_catches(self):
        """The actual failure mode, reproduced: bind the name, reload, raise
        the fresh class. `except ValueError` catches it; the stale name cannot."""
        stale = sb.ScopeError
        try:
            importlib.reload(sb)
            fresh = sb.ScopeError

            with pytest.raises(ValueError):
                raise fresh("target '10.0.0.1' is NOT in authorized scope")

            assert not issubclass(fresh, stale)
        finally:
            importlib.reload(sb)


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
