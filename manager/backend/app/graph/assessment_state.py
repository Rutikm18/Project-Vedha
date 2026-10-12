"""Result quantifiers for a trusted evaluator's selected proofs and goal query."""

from typing import Literal

from pydantic import Field

from app.graph.local_rule import ContractModel

ProofState = Literal[
    "supported",
    "blocked",
    "missing_prerequisites",
    "conflicted",
    "stale",
    "not_evaluated",
]
ComputeState = Literal["complete", "truncated", "failed", "not_evaluated"]
CoverageState = Literal[
    "complete", "partial", "restricted", "unsupported", "not_collected"
]
GoalState = Literal[
    "supported", "not_derived_in_declared_model", "indeterminate", "not_evaluated"
]


class GoalAssessment(ContractModel):
    state: GoalState
    compute: ComputeState
    coverage: CoverageState
    supported_proofs: int = Field(ge=0)
    evaluated_proofs: int = Field(ge=0)
    reason_codes: tuple[str, ...]


def summarize_goal(
    proofs: tuple[ProofState, ...], *, compute: ComputeState, coverage: CoverageState
) -> GoalAssessment:
    """Summarize one fixed scope/scenario/goal/input/rule query.

    This internal function must receive validated evaluator outcomes, not caller
    verdicts. Complete means exhaustive derivation within the declared model;
    display pagination or top-K explanations cannot establish that completeness.
    """
    if compute not in ("complete", "truncated", "failed", "not_evaluated"):
        raise ValueError("unknown compute state")
    if coverage not in (
        "complete",
        "partial",
        "restricted",
        "unsupported",
        "not_collected",
    ):
        raise ValueError("unknown coverage state")
    allowed = {
        "supported",
        "blocked",
        "missing_prerequisites",
        "conflicted",
        "stale",
        "not_evaluated",
    }
    if any(state not in allowed for state in proofs):
        raise ValueError("unknown proof state")
    if compute == "not_evaluated" and any(p != "not_evaluated" for p in proofs):
        raise ValueError("unevaluated query cannot contain evaluated proofs")
    supported = proofs.count("supported")
    evaluated = sum(p != "not_evaluated" for p in proofs)
    reasons = []
    if compute != "complete":
        reasons.append("compute_" + compute)
    if coverage != "complete":
        reasons.append("coverage_" + coverage)
    uncertain = {"missing_prerequisites", "conflicted", "stale", "not_evaluated"}
    if supported:
        state = "supported"
        reasons.insert(0, "supported_derivation_exists")
    elif compute == "not_evaluated":
        state = "not_evaluated"
    elif (
        compute != "complete"
        or coverage != "complete"
        or any(p in uncertain for p in proofs)
    ):
        state = "indeterminate"
        reasons.extend(sorted({"proof_" + p for p in proofs if p in uncertain}))
    else:
        state = "not_derived_in_declared_model"
        reasons.append("no_supported_derivation_in_complete_declared_model")
    return GoalAssessment(
        state=state,
        compute=compute,
        coverage=coverage,
        supported_proofs=supported,
        evaluated_proofs=evaluated,
        reason_codes=tuple(reasons),
    )
