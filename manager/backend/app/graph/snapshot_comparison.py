"""Compare sealed readiness records without awarding remediation credit."""


def compare_readiness(baseline, current) -> dict:
    """Rows must already be authorized within the same engagement.

    A missing record, lifecycle edit or newer model is not fresh verification.
    This readiness adapter does not produce supported capability proofs.
    """
    if (baseline.tenant_id, baseline.engagement_id) != (
        current.tenant_id, current.engagement_id
    ):
        raise ValueError("comparison_scope_mismatch")
    if baseline.status != "completed" or current.status != "completed":
        raise ValueError("comparison_requires_completed_snapshots")
    if baseline.request_sequence >= current.request_sequence:
        raise ValueError("comparison_requires_earlier_baseline")
    before, after = baseline.result_document, current.result_document
    reasons = ["readiness_only", "partial_observation_coverage"]
    model_fields = ("normalization_version", "rule_pack_version", "rule_artifact_sha256")
    if any(getattr(baseline, k) != getattr(current, k) for k in model_fields):
        reasons.append("model_changed")
    if before.get("compute") != "complete_for_readiness" or after.get("compute") != "complete_for_readiness":
        reasons.append("computation_incomplete")
    old = {r["finding_id"]: r for r in before.get("assessments", [])}
    new = {r["finding_id"]: r for r in after.get("assessments", [])}
    changes = []
    for finding_id in sorted(old.keys() | new.keys()):
        left, right = old.get(finding_id), new.get(finding_id)
        changed = sorted(
            key for key in left.keys() | right.keys() if left.get(key) != right.get(key)
        ) if left is not None and right is not None else []
        if left is None or right is None or changed:
            changes.append({
                "finding_id": finding_id,
                "change": "added" if left is None else "absent_from_current" if right is None else "changed",
                "changed_fields": changed,
                "verification_state": "not_verified",
            })
    return {
        "baseline_id": str(baseline.id),
        "current_id": str(current.id),
        "comparison_state": "inconclusive_for_remediation",
        "reasons": reasons,
        "changes": changes,
        "verification_required": "Collect fresh evidence for the same service instance, entry context and permissions; finding removal or lifecycle edits do not verify a fix.",
    }
