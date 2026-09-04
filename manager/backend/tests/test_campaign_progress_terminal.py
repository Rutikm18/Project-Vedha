"""
A campaign whose jobs all ended without producing results must reach a TERMINAL
state, not wait forever on a detection run that can never be created.

THE BUG:
  `_reconcile_status` decided "aggregating" from `not run_exists` — "facts are in,
  the run hasn't been created yet". That inference is only valid when some job
  actually SUBMITTED facts. If every job was cancelled or failed, there is no
  submission, so no `facts.ready` event, so no DetectionRun, ever. The campaign
  sat at `aggregating` / `is_complete=False` permanently, which renders as a
  progress bar frozen at ~17% (1 of 6 phases) with a spinner that never stops and
  a frontend that keeps polling every 4s forever.

  `any_complete` was already being computed in the handler and then never used —
  the missing input for exactly this case.

Cancelling is now a first-class operator action, so this state is reachable on
purpose, not just after a failure.
"""
from __future__ import annotations

import pytest

from app.routers.engagements import _reconcile_status

BASE = dict(
    jobs_exist=True, any_running=False, scanning_done=True, run_exists=False,
    latest_failed=False, detection_done=False, evidence_covered=False,
    has_gaps=False, queue_pending=False, queue_overdue=False, queue_dead=False,
    worker_alive=True,
)


def _status(**over):
    return _reconcile_status(**{**BASE, **over})


class TestTerminalWithoutResults:
    def test_all_cancelled_campaign_is_terminal(self):
        status, complete = _status(any_complete=False, all_cancelled=True)
        assert status == "cancelled"
        assert complete is True, "must stop polling; nothing can advance it"

    def test_all_failed_campaign_is_terminal(self):
        status, complete = _status(any_complete=False, all_cancelled=False)
        assert status == "error"
        assert complete is True

    def test_does_not_hijack_a_campaign_that_produced_results(self):
        """The normal path must be untouched: a completed job with no run yet is
        genuinely still aggregating."""
        status, complete = _status(any_complete=True)
        assert status == "aggregating"
        assert complete is False

    def test_running_job_still_wins(self):
        """Precedence: work in flight is reported before any terminal verdict."""
        status, complete = _status(any_running=True, any_complete=False,
                                   all_cancelled=True)
        assert status == "scanning" and complete is False

    def test_a_dead_queue_is_still_reported_as_error_first(self):
        status, _ = _status(queue_dead=True, any_complete=False, all_cancelled=True)
        assert status == "error"

    def test_partial_cancel_with_one_success_still_aggregates(self):
        """One good job is enough to expect a detection run."""
        status, complete = _status(any_complete=True, all_cancelled=False)
        assert status == "aggregating" and complete is False


class TestNormalPipelineUnaffected:
    """Regression guard: the happy path and its known edge cases still hold."""

    def test_complete_campaign(self):
        assert _status(any_complete=True, run_exists=True, detection_done=True,
                       evidence_covered=True) == ("complete", True)

    def test_complete_with_gaps(self):
        assert _status(any_complete=True, run_exists=True, detection_done=True,
                       evidence_covered=True, has_gaps=True) == (
            "complete_with_gaps", True)

    def test_uncovered_submission_keeps_it_detecting(self):
        status, complete = _status(any_complete=True, run_exists=True,
                                   detection_done=True, evidence_covered=False)
        assert status == "detecting" and complete is False

    def test_no_jobs_is_pending(self):
        status, complete = _status(jobs_exist=False, any_complete=False)
        assert status == "pending" and complete is False

    def test_defaults_keep_backwards_compatibility(self):
        """Callers that don't pass the new inputs must behave as before."""
        assert _reconcile_status(**BASE) == ("aggregating", False)
