"""Product-boundary tests for the single-dashboard Manager API."""

from app.main import app


def test_manager_does_not_mount_a_static_dashboard():
    paths = {getattr(route, "path", None) for route in app.routes}

    assert "/dashboard" not in paths
    assert "/dashboard/{path:path}" not in paths


def test_manager_root_is_service_metadata():
    root = next(
        route
        for route in app.routes
        if getattr(route, "path", None) == "/"
    )

    assert root.name == "_service_root"
