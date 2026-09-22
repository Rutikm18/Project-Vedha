"""
T2.4 — the kernel ceilings stop being advice nobody acts on.

A1 measures them and logs them. Nothing read the result, so a probe whose
conntrack table cannot hold the job's probe rate ran the job anyway, and the
kernel dropped the overflow with NO error to userspace. The scanner saw
silence, waited out its timeout, and recorded `filtered` — a claim about the
TARGET manufactured entirely by a limit on the SCANNER. The scan then looks
complete. That is the same deception `_refuse_if_infeasible` exists to prevent,
and it is invisible from inside the result.

WHY ONLY SOME CHECKS BLOCK
--------------------------
The line is not severity, it is whether the failure can SPEAK:

  conntrack  overflow is dropped silently and reported as `filtered`.  BLOCKS.
  ephemeral  surfaces as EADDRNOTAVAIL -> local_resource_error -> degraded.
             The scan reports its own injury, so refusing adds nothing.
  fd         surfaces as EMFILE, same path, same reason.
  neighbour  silent, AND the arithmetic only holds on a flat L2 segment. The
             probe cannot see its targets' topology, so a 1000-host sweep
             across ROUTED subnets never touches gc_thresh3 and refusing it
             would be a false refusal. Stays a warning — the one place where
             not knowing is a reason to speak rather than to act.
  raw_socket the connect() fallback is slow, not wrong, and the feasibility
             floor already refuses what cannot finish in time.

Refusal is overridable (`allow_degraded_kernel`), exactly as `allow_infeasible`
is: someone who wants the partial can have it, they just have to ask.
"""
from __future__ import annotations

import pytest

from agent import kernel_limits as kl
from agent.doctor import Check
from agent.engine import _refuse_if_kernel_unsafe

WARN_CONNTRACK = Check("conntrack", "warn", "table 65,536; 4000 pps needs ~480,000",
                       "raise nf_conntrack_max")
PASS_CONNTRACK = Check("conntrack", "pass", "table 65,536; 150 pps needs ~18,000")
WARN_NEIGHBOUR = Check("neighbour", "warn", "gc_thresh3 1024, sweeping 1000 host(s)",
                       "raise gc_thresh3")
WARN_EPHEMERAL = Check("ephemeral", "warn", "range sustains ~470 connect/sec",
                       "lower the rate")
WARN_FD = Check("fd", "warn", "soft limit 256, concurrency 300", "raise ulimit -n")
WARN_RAW = Check("raw_socket", "warn", "no CAP_NET_RAW", "grant NET_RAW")


class TestWhichChecksBlock:
    def test_conntrack_blocks(self):
        assert [c.name for c in kl.blocking_checks([WARN_CONNTRACK])] == ["conntrack"]

    @pytest.mark.parametrize("check", [WARN_EPHEMERAL, WARN_FD, WARN_RAW],
                             ids=lambda c: c.name)
    def test_a_self_reporting_failure_does_not_block(self, check):
        """These reach the result as local_resource_error / degraded. The scan
        already tells the truth about itself."""
        assert kl.blocking_checks([check]) == []

    def test_the_neighbour_table_warns_but_does_not_block(self):
        """Silent, but conditional on a flat L2 segment the probe cannot see."""
        assert kl.blocking_checks([WARN_NEIGHBOUR]) == []

    def test_a_passing_check_never_blocks(self):
        assert kl.blocking_checks([PASS_CONNTRACK]) == []

    def test_blocking_is_a_subset_of_warnings(self):
        mixed = [WARN_CONNTRACK, WARN_NEIGHBOUR, PASS_CONNTRACK, WARN_FD]
        assert all(c.status == "warn" for c in kl.blocking_checks(mixed))


class TestAdmission:
    def test_a_silent_ceiling_refuses_the_job(self):
        refusal = _refuse_if_kernel_unsafe([WARN_CONNTRACK], {})
        assert refusal is not None
        assert "conntrack" in refusal["error"]

    def test_the_refusal_carries_the_measurement_and_the_remedy(self):
        """An operator cannot act on a number nobody showed them."""
        refusal = _refuse_if_kernel_unsafe([WARN_CONNTRACK], {})
        assert "480,000" in refusal["error"]
        assert "nf_conntrack_max" in refusal["remediation"]
        assert "allow_degraded_kernel" in refusal["remediation"]

    def test_it_says_why_silence_is_the_problem(self):
        """The refusal has to explain that `filtered` becomes untrustworthy —
        otherwise it reads as a performance complaint."""
        refusal = _refuse_if_kernel_unsafe([WARN_CONNTRACK], {})
        assert "filtered" in refusal["error"] + refusal["remediation"]

    def test_a_healthy_host_is_not_refused(self):
        assert _refuse_if_kernel_unsafe([PASS_CONNTRACK], {}) is None

    def test_no_checks_at_all_is_not_a_refusal(self):
        """A host where nothing could be measured (macOS, no /proc) must still
        be able to scan — absence of evidence is not evidence of a ceiling."""
        assert _refuse_if_kernel_unsafe([], {}) is None

    @pytest.mark.parametrize("value", [True, "true", "1", "yes", "on"])
    def test_the_override_is_honoured(self, value):
        assert _refuse_if_kernel_unsafe(
            [WARN_CONNTRACK], {"allow_degraded_kernel": value}) is None

    @pytest.mark.parametrize("value", [False, "false", "0", "", None])
    def test_a_falsey_override_still_refuses(self, value):
        assert _refuse_if_kernel_unsafe(
            [WARN_CONNTRACK], {"allow_degraded_kernel": value}) is not None

    def test_advisory_warnings_alone_never_refuse(self):
        """The whole estate of warnings A1 emits must not become a wall."""
        assert _refuse_if_kernel_unsafe(
            [WARN_NEIGHBOUR, WARN_EPHEMERAL, WARN_FD, WARN_RAW], {}) is None


class TestTheCeilingsReachTheResult:
    """Measuring a limit and then discarding it is how this became advice
    nobody acts on. A scan that ran under a violated ceiling has to SAY so."""

    def test_checks_serialize_for_run_stats(self):
        stats = kl.as_run_stats([WARN_CONNTRACK, PASS_CONNTRACK])
        assert stats["warnings"] == 1
        assert stats["blocking"] == ["conntrack"]
        assert {"name": "conntrack", "status": "warn",
                "detail": WARN_CONNTRACK.detail} in stats["checks"]

    def test_a_clean_host_records_no_warnings(self):
        stats = kl.as_run_stats([PASS_CONNTRACK])
        assert stats["warnings"] == 0
        assert stats["blocking"] == []

    def test_unmeasurable_is_not_reported_as_clean(self):
        """None of the limits could be read. That is a different statement from
        'the ceilings are fine', and the result must not conflate them."""
        assert kl.as_run_stats([])["measured"] is False
        assert kl.as_run_stats([PASS_CONNTRACK])["measured"] is True
