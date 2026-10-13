import itertools

import pytest

from app.graph.assessment_state import summarize_goal


def test_blocked_route_with_surviving_alternative_is_supported():
    result = summarize_goal(
        ("blocked", "supported"), compute="complete", coverage="complete"
    )
    assert result.state == "supported"
    assert result.supported_proofs == 1


@pytest.mark.parametrize("compute", ["truncated", "failed"])
def test_positive_proof_survives_incomplete_search_with_qualifier(compute):
    result = summarize_goal(
        ("supported", "blocked"), compute=compute, coverage="partial"
    )
    assert result.state == "supported"
    assert "compute_" + compute in result.reason_codes
    assert "coverage_partial" in result.reason_codes


@pytest.mark.parametrize(
    "compute,coverage",
    list(
        itertools.product(
            ["complete", "truncated", "failed"],
            ["complete", "partial", "restricted", "unsupported", "not_collected"],
        )
    ),
)
def test_absence_is_qualified_by_computation_and_collection(compute, coverage):
    result = summarize_goal(("blocked",), compute=compute, coverage=coverage)
    expected = (
        "not_derived_in_declared_model"
        if (compute, coverage) == ("complete", "complete")
        else "indeterminate"
    )
    assert result.state == expected


@pytest.mark.parametrize(
    "proof", ["missing_prerequisites", "conflicted", "stale", "not_evaluated"]
)
def test_uncertain_route_is_never_an_all_clear(proof):
    result = summarize_goal(("blocked", proof), compute="complete", coverage="complete")
    assert result.state == "indeterminate"


def test_no_compute_is_not_evaluated():
    result = summarize_goal((), compute="not_evaluated", coverage="not_collected")
    assert result.state == "not_evaluated"


def test_complete_empty_query_is_limited_to_declared_model():
    result = summarize_goal((), compute="complete", coverage="complete")
    assert result.state == "not_derived_in_declared_model"
    assert result.reason_codes == (
        "no_supported_derivation_in_complete_declared_model",
    )


def test_order_does_not_change_conclusion():
    a = summarize_goal(
        ("blocked", "supported", "stale"), compute="truncated", coverage="partial"
    )
    b = summarize_goal(
        ("stale", "supported", "blocked"), compute="truncated", coverage="partial"
    )
    assert a == b


@pytest.mark.parametrize(
    "proofs,compute,coverage",
    [
        (("secure",), "complete", "complete"),
        ((), "top_k", "complete"),
        ((), "complete", "unknown"),
        (("supported",), "not_evaluated", "complete"),
    ],
)
def test_invalid_or_contradictory_states_rejected(proofs, compute, coverage):
    with pytest.raises(ValueError):
        summarize_goal(proofs, compute=compute, coverage=coverage)
