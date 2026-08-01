from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.routers.engagements import EngagementUpdate
from app.schemas.engagement import EngagementCreate


def test_create_normalizes_name_scopes_and_duplicates():
    body = EngagementCreate(
        name="  Quarterly assessment  ",
        scope_cidrs=["10.0.0.0/24", "10.0.0.0/24", "2001:db8::/64"],
        excluded_cidrs=["10.0.0.5"],
    )

    assert body.name == "Quarterly assessment"
    assert body.scope_cidrs == ["10.0.0.0/24", "2001:db8::/64"]
    assert body.excluded_cidrs == ["10.0.0.5"]


@pytest.mark.parametrize(
    "scope",
    [
        [""],
        ["not a network"],
        ["https://10.0.0.1"],
        ["10.0.0.0/99"],
    ],
)
def test_create_rejects_invalid_scope_entries(scope):
    with pytest.raises(ValidationError, match="invalid IP address or CIDR|cannot be blank"):
        EngagementCreate(name="test", scope_cidrs=scope)


def test_create_rejects_reversed_date_range():
    with pytest.raises(ValidationError, match="end_time must be on or after start_time"):
        EngagementCreate(
            name="test",
            scope_cidrs=["10.0.0.0/24"],
            start_time=datetime(2026, 8, 2, tzinfo=timezone.utc),
            end_time=datetime(2026, 8, 1, tzinfo=timezone.utc),
        )


def test_update_rejects_blank_name_invalid_scope_and_reversed_dates():
    with pytest.raises(ValidationError, match="name"):
        EngagementUpdate(name="   ")
    with pytest.raises(ValidationError, match="invalid IP address or CIDR"):
        EngagementUpdate(scope_cidrs=["10.0.0.999"])
    with pytest.raises(ValidationError, match="end_time must be on or after start_time"):
        EngagementUpdate(
            start_time=datetime(2026, 8, 2),
            end_time=datetime(2026, 8, 1),
        )
