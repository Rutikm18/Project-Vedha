"""ORM metadata must stay aligned with reporting-related migrations."""

from sqlalchemy import CheckConstraint

from app.models.detection_run import DetectionRun
from app.models.remediation_plan import RemediationPlan
from app.models.scan_job import ScanJob


def test_scan_identity_columns_match_migration_0046():
    job_columns = ScanJob.__table__.c
    assert job_columns.use_case_id.type.length == 64
    assert job_columns.use_case_id.nullable is True
    assert job_columns.intensity.type.length == 16
    assert job_columns.intensity.nullable is True

    run_job_id = DetectionRun.__table__.c.job_id
    assert run_job_id.type.as_uuid is True
    assert run_job_id.nullable is True
    assert run_job_id.index is True


def test_remediation_plan_columns_and_constraints_match_migration_0048():
    columns = RemediationPlan.__table__.c
    assert columns.finding_id.nullable is True
    assert columns.subject_type.type.length == 8
    assert columns.subject_type.nullable is False
    assert str(columns.subject_type.server_default.arg) == "finding"
    assert columns.fix_key.type.length == 12
    assert columns.fix_key.nullable is True
    assert columns.facts_fingerprint.type.length == 64
    assert columns.facts_fingerprint.nullable is True

    subject_constraint = next(
        constraint
        for constraint in RemediationPlan.__table__.constraints
        if isinstance(constraint, CheckConstraint)
        and constraint.name == "ck_remediation_subject"
    )
    constraint_sql = " ".join(str(subject_constraint.sqltext).split())
    assert constraint_sql == (
        "(subject_type = 'finding' AND finding_id IS NOT NULL) OR "
        "(subject_type = 'bundle' AND fix_key IS NOT NULL)"
    )

    bundle_index = next(
        index
        for index in RemediationPlan.__table__.indexes
        if index.name == "uq_remediation_bundle_os"
    )
    assert bundle_index.unique is True
    assert [column.name for column in bundle_index.columns] == [
        "engagement_id",
        "fix_key",
        "os",
    ]
    assert str(bundle_index.dialect_options["postgresql"]["where"]) == (
        "subject_type = 'bundle'"
    )
