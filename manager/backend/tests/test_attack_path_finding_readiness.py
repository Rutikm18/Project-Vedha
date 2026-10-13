import pytest

from app.graph.finding_readiness import finding_readiness
from app.services.attack_assessments import compute_readiness, NORMALIZATION_VERSION


@pytest.fixture
def finding():
    return {
        "id": "finding-1",
        "asset_id": "asset-1",
        "title": "sample finding",
        "severity": "high",
        "status": "accepted",
        "evidence": {"service": "redis", "unauthenticated": True},
    }


def test_banner_noauth_and_accepted_risk_do_not_establish_application_read(finding):
    result = finding_readiness(
        finding, {"asset-1": {"id": "asset-1", "hostname": "test"}}, {}
    )
    assert result["goal_state"] == "indeterminate"
    assert result["supported_proofs"] == 0
    assert result["lifecycle"] == "accepted"
    assert result["rule_applicability"] == "candidate"
    assert (
        next(
            p
            for p in result["prerequisites"]
            if p["key"] == "unauthenticated_datastore_data_read_supported"
        )["state"]
        == "missing"
    )


def test_titles_do_not_map_rules_and_unmapped_findings_remain_visible(finding):
    finding["title"] = "Redis unauthenticated DOMAIN ADMIN takeover"
    finding["evidence"] = {}
    result = finding_readiness(finding, {}, {})
    assert result["goal_state"] == "not_evaluated"
    assert result["rule_applicability"] == "unmapped"
    assert result["finding_id"] == "finding-1"


def test_foreign_asset_or_service_ids_are_not_exposed_as_bound_entities(finding):
    finding["asset_id"] = "foreign-asset"
    finding["evidence"]["service_id"] = "00000000-0000-4000-8000-000000000009"
    result = finding_readiness(
        finding,
        {},
        {
            finding["evidence"]["service_id"]: {
                "id": finding["evidence"]["service_id"],
                "asset_id": "foreign-asset",
            }
        },
    )
    assert result["asset_id"] is None
    assert result["service_id"] is None


def test_malformed_raw_evidence_is_not_a_crash_or_supported_path(finding):
    finding["evidence"] = ["untrusted"]
    result = finding_readiness(finding, {}, {})
    assert result["supported_proofs"] == 0
    assert result["rule_applicability"] == "unmapped"


def test_truncation_and_denominator_are_preserved(finding):
    result = compute_readiness(
        {
            "normalization_version": NORMALIZATION_VERSION,
            "assets": [],
            "services": [],
            "findings": [finding],
            "input_truncated": True,
            "total_findings": 1001,
        }
    )
    assert result["compute"] == "truncated"
    assert result["total_findings"] == 1001
    assert result["assessed_findings"] == 1
    assert len(result["assessments"]) == 1


def test_unknown_normalization_cannot_silently_compute():
    with pytest.raises(ValueError, match="unsupported_normalization_version"):
        compute_readiness({"normalization_version": "unreviewed@9"})
