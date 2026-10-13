from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from app.graph.environment_engine import (
    ReadTransition,
    SystemRef,
    TransferEvidence,
    derive_environment_paths,
)

NOW = datetime(2026, 10, 13, tzinfo=timezone.utc)
TENANT, ENV, ACTOR, E1, E2 = (UUID(int=i) for i in range(1, 6))
A = SystemRef(
    engagement_id=E1,
    asset_id=UUID(int=10),
    service_id=UUID(int=11),
    instance_ref="observed:listener-A",
    protocol="tcp",
    port=6379,
)
B = SystemRef(
    engagement_id=E2,
    asset_id=UUID(int=20),
    service_id=UUID(int=21),
    instance_ref="observed:listener-B",
    protocol="tcp",
    port=5432,
)


def transition(number, target, source=None):
    kinds = [
        "directed_reachability",
        "authenticated_application_read"
        if source
        else "unauthenticated_application_read",
    ] + (["credential_access", "credential_authentication"] if source else [])
    identity = "identity:exact-target-reader" if source else None
    evidence = tuple(
        TransferEvidence(
            id=UUID(int=number * 100 + i),
            tenant_id=TENANT,
            environment_id=ENV,
            actor_id=ACTOR,
            context_ref="authorized:scenario",
            source=source,
            target=target,
            identity_ref=identity,
            kind=kind,
            state="supported",
            raw_ref=f"synthetic:raw/{number}/{i}",
            collector_version="fixture@1",
            sha256="a" * 64,
            operation_ref=f"synthetic:operation/{number}/{i}",
            observed_at=NOW - timedelta(hours=1),
            valid_until=NOW + timedelta(hours=1),
            known_at=NOW,
        )
        for i, kind in enumerate(kinds)
    )
    return ReadTransition(
        id=UUID(int=number),
        rule_id="credential_backed_data_read"
        if source
        else "unauthenticated_data_read",
        tenant_id=TENANT,
        environment_id=ENV,
        actor_id=ACTOR,
        context_ref="authorized:scenario",
        source=source,
        target=target,
        identity_ref=identity,
        finding_id=UUID(int=number + 1000),
        finding_asset_id=target.asset_id,
        finding_service_id=target.service_id,
        finding_lifecycle="open",
        finding_evidence_ids=(evidence[1].id,),
        evidence=evidence,
    )


def derive(values, **kw):
    return derive_environment_paths(
        tuple(values),
        tenant_id=TENANT,
        environment_id=ENV,
        engagement_ids=frozenset({E1, E2}),
        as_of=NOW,
        known_at=NOW,
        **kw,
    )


def test_explicit_current_credential_bridge_composes_two_engagements():
    root, transfer = transition(100, A), transition(200, B, A)
    result = derive([transfer, root])
    assert len(result["supported_proofs"]) == 2
    target = next(
        p for p in result["supported_proofs"] if p["target"]["engagement_id"] == str(E2)
    )
    assert target["source_proof_id"] == str(root.id)
    assert target["capability"] == "service_data_read_only"
    assert target["realization"] == "not_observed_chain"
    assert result == derive([root, transfer])


@pytest.mark.parametrize("index", range(4))
def test_every_transfer_and_premise_is_required(index):
    transfer = transition(200, B, A)
    transfer = transfer.model_copy(
        update={"evidence": transfer.evidence[:index] + transfer.evidence[index + 1 :]}
    )
    result = derive([transition(100, A), transfer])
    assert len(result["supported_proofs"]) == 1
    assert result["unresolved"][0]["reason"] == "required_evidence_bundle_missing"


@pytest.mark.parametrize(
    "field,value,reason",
    [
        ("state", "unknown", "evidence_unknown"),
        ("state", "conflicted", "evidence_conflicted"),
        ("valid_until", NOW, "evidence_not_current_at_cut"),
        ("known_at", NOW + timedelta(seconds=1), "evidence_not_current_at_cut"),
        ("operation_ref", None, "operation_reference_missing"),
    ],
)
def test_uncertain_stale_late_and_unattributed_operations_do_not_support(
    field, value, reason
):
    root = transition(100, A)
    root = root.model_copy(
        update={
            "evidence": (
                root.evidence[0],
                root.evidence[1].model_copy(update={field: value}),
            )
        }
    )
    result = derive([root])
    assert not result["supported_proofs"]
    assert result["unresolved"][0]["reason"] == reason


def test_no_source_capability_means_no_transfer_even_with_evidence():
    result = derive([transition(200, B, A)])
    assert result["unresolved"][0]["reason"] == "source_capability_missing"


def test_unknown_or_other_scope_cannot_be_joined():
    root = transition(100, A)
    with pytest.raises(ValueError, match="scope_mismatch"):
        derive([root.model_copy(update={"tenant_id": UUID(int=999)})])
    with pytest.raises(ValueError, match="incompatible_actor_context"):
        derive(
            [root, transition(200, B, A).model_copy(update={"actor_id": UUID(int=999)})]
        )


def test_wrong_instance_and_withdrawn_finding_do_not_support():
    root = transition(100, A)
    bad = root.evidence[0].model_copy(
        update={
            "target": A.model_copy(
                update={"instance_ref": "reused-address:other-instance"}
            )
        }
    )
    assert not derive([root.model_copy(update={"evidence": (bad, root.evidence[1])})])[
        "supported_proofs"
    ]
    assert not derive([root.model_copy(update={"finding_lifecycle": "remediated"})])[
        "supported_proofs"
    ]


def test_cycles_cannot_bootstrap_and_budgets_remain_qualified():
    assert not derive([transition(100, A, B), transition(200, B, A)])[
        "supported_proofs"
    ]
    result = derive([transition(100, A), transition(200, B, A)], max_applications=1)
    assert len(result["supported_proofs"]) == 1
    assert result["compute"] == "truncated"
    assert result["coverage"] == "partial"
    limited = derive([transition(100, A), transition(200, B, A)], max_depth=1)
    assert limited["compute"] == "truncated"
    assert limited["unresolved"][0]["reason"] == "depth_limit"
