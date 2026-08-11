from __future__ import annotations

from app.models.validation_request import (
    CHECK_TLS, VR_PENDING, ValidationRequest,
)


def test_validation_request_columns_and_defaults():
    cols = ValidationRequest.__table__.columns
    for name in ("engagement_id", "finding_id", "target_ip", "target_port",
                 "check_kind", "status", "outcome", "job_id", "result",
                 "requested_by", "requested_at"):
        assert name in cols, f"missing column {name}"
    assert VR_PENDING == "pending"
    assert CHECK_TLS == "tls_handshake"
