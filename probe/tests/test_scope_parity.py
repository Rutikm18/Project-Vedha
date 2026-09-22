"""
B2 — the probe and the manager must agree on what a valid scope is.

THE DIVERGENCE
--------------
The manager already refuses anything that is not an IP/CIDR: every write path
for `Engagement.scope_cidrs` runs schemas/engagement.validate_scope_entries,
which requires ipaddress.ip_network(value, strict=False) to parse.

ScopeGuard.from_list is the opposite — it is fail-OPEN by construction. Any
entry that does not parse as a network is silently reclassified as a hostname:

    from_list(["10.0.0.0/244"])    -> hostname "10.0.0.0/244", matches nothing
    from_list(["10.0.0."])         -> hostname "10.0.0.", matches nothing

So a typo in an authorization boundary becomes an inert allowlist entry instead
of an error, and nothing anywhere says so.

The excludes path is worse, because it fails open in the DANGEROUS direction:

    from_list(["10.0.0.0/24"], excludes=["10.0.0.5/33"])

`10.0.0.5/33` does not parse, the exclusion is silently DROPPED, and the host
the operator explicitly carved out gets scanned. That is a safety failure, not
just a data-loss one.

THE FIX
-------
`strict=True` — opt-in, used by the agent path — makes the probe's acceptance
rule byte-identical to the manager's: parse as a network or raise.

`from_list` keeps its lenient default and `from_file` keeps hostname support,
because that is documented, tested, CLI-facing behaviour (a standalone operator
really can authorize `scanme.example.com` in a scope file). Only the
manager-driven path is tightened, and that is exactly the path where the two
models have to agree.
"""
from __future__ import annotations

import ipaddress

import pytest

# Referenced through the MODULE, never bound at import time.
# tests/test_project_timezone.py calls importlib.reload(scanner_base), which
# rebinds ScopeGuard and ScopeError to NEW class objects. A name bound here at
# collection time would then be a different class from the one the reloaded
# from_list() raises, and pytest.raises() would stop matching — a failure that
# only appears when the suite runs in alphabetical order. Module-qualified
# lookups always resolve to the live classes.
from scanner import scanner_base as sb

# The manager's rule, stated once (schemas/engagement.validate_scope_entries).
def _manager_accepts(entry: str) -> bool:
    try:
        ipaddress.ip_network(entry.strip(), strict=False)
        return True
    except ValueError:
        return False


# Entries that must be judged identically by both sides.
CORPUS = [
    "10.0.0.0/24",          # ordinary CIDR
    "192.168.1.50",         # bare host
    "192.168.1.50/32",      # explicit /32
    "2001:db8::/32",        # IPv6 network
    "fe80::1",              # IPv6 host
    "0.0.0.0/0",            # everything (valid, if alarming)
    "10.0.0.0/244",         # malformed prefix — a typo, not a hostname
    "10.0.0.",              # truncated — a typo, not a hostname
    "scanme.example.com",   # a genuine hostname
    "not an address",       # junk
    "10.0.0.1-10.0.0.9",    # range syntax ScopeGuard does not parse
]


class TestParityWithTheManager:
    @pytest.mark.parametrize("entry", CORPUS)
    def test_strict_mode_accepts_exactly_what_the_manager_accepts(self, entry):
        """The whole point of B2: one rule, two processes."""
        if _manager_accepts(entry):
            sb.ScopeGuard.from_list([entry], strict=True)      # must not raise
        else:
            with pytest.raises(sb.ScopeError):
                sb.ScopeGuard.from_list([entry], strict=True)

    @pytest.mark.parametrize("entry", CORPUS)
    def test_strict_mode_holds_for_excludes_too(self, entry):
        """An exclusion is an authorization boundary like any other."""
        if _manager_accepts(entry):
            sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=[entry], strict=True)
        else:
            with pytest.raises(sb.ScopeError):
                sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=[entry],
                                     strict=True)


class TestStrictModeCatchesWhatSilenceHid:
    def test_a_malformed_cidr_is_an_error_not_a_hostname(self):
        with pytest.raises(sb.ScopeError, match="10.0.0.0/244"):
            sb.ScopeGuard.from_list(["10.0.0.0/244"], strict=True)

    def test_a_hostname_is_refused_on_the_manager_driven_path(self):
        with pytest.raises(sb.ScopeError, match="scanme.example.com"):
            sb.ScopeGuard.from_list(["scanme.example.com"], strict=True)

    def test_a_dropped_exclusion_is_an_error_not_a_silent_scan(self):
        """The dangerous one: fail-open in the direction that scans more.

        Without strict mode this returns a guard that scans 10.0.0.5 — the host
        the operator explicitly carved out.
        """
        with pytest.raises(sb.ScopeError, match="10.0.0.5/33"):
            sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=["10.0.0.5/33"],
                                 strict=True)

    def test_the_error_names_the_offending_entry(self):
        with pytest.raises(sb.ScopeError) as exc:
            sb.ScopeGuard.from_list(["10.0.0.0/24", "oops"], strict=True)
        assert "oops" in str(exc.value)

    def test_blank_entries_are_still_skipped_not_rejected(self):
        guard = sb.ScopeGuard.from_list(["10.0.0.0/24", "", "  "], strict=True)
        assert guard.in_scope("10.0.0.1") is True


class TestTheCliPathIsUnchanged:
    """Standalone use really can authorize a hostname; do not break it."""

    def test_default_from_list_still_accepts_a_hostname(self):
        guard = sb.ScopeGuard.from_list(["scanme.example.com"])
        assert guard.in_scope("scanme.example.com") is True

    def test_default_from_list_still_tolerates_a_malformed_exclude(self):
        guard = sb.ScopeGuard.from_list(["10.0.0.0/24"], excludes=["nonsense"])
        assert guard.in_scope("10.0.0.1") is True

    def test_from_file_still_supports_the_documented_format(self, tmp_path):
        path = tmp_path / "scope.txt"
        path.write_text("10.0.0.0/24\nscanme.example.com\n# comment\n")
        guard = sb.ScopeGuard.from_file(path)
        assert guard.in_scope("10.0.0.1") is True
        assert guard.in_scope("scanme.example.com") is True


class TestTheAgentPathUsesStrictMode:
    def test_engine_builds_its_scope_strictly(self):
        """Source-level: the parity is worthless if the agent path opts out."""
        import inspect

        from agent import engine

        src = inspect.getsource(engine.run_scan)
        assert "strict=True" in src, \
            "the agent path must build its ScopeGuard with strict=True"

    def test_an_invalid_engagement_scope_returns_a_clean_error_result(self):
        """A bad scope must FAIL THE JOB, not crash the runner — run_scan's
        docstring promises it never raises."""
        from agent import engine

        result = engine.run_scan(
            "discovery",
            {"targets": ["10.0.0.1"], "scope_cidrs": ["10.0.0.0/244"]},
        )
        assert result["ok"] is False
        assert result["error_code"] == "invalid_scope"
        assert "10.0.0.0/244" in result["error"]

    def test_a_valid_engagement_scope_still_runs(self):
        from agent import engine

        result = engine.run_scan(
            "discovery",
            {"targets": ["10.0.0.1"], "scope_cidrs": ["10.0.0.0/24"]},
        )
        assert result["ok"] is True
