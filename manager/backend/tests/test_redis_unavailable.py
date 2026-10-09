"""A Redis outage is reported as "dependency unavailable", not as our bug.

Login throttling, refresh tokens and the agent backplane live in Redis. When it
is down those routes stay failed closed, but they used to fall through to the
catch-all handler and answer 500 "Internal server error", which reads as a code
defect to the caller, the load balancer and whoever is on call.
"""
from __future__ import annotations

from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import ResponseError

from app.dependencies import get_redis
from app.main import app


class _Redis:
    """Every command raises `exc`, as a client does when the server is gone."""

    def __init__(self, exc: Exception):
        self._exc = exc

    def __getattr__(self, _name):
        async def _fail(*_a, **_k):
            raise self._exc
        return _fail


def _login_with(redis) -> object:
    async def _override():
        return redis
    app.dependency_overrides[get_redis] = _override
    try:
        client = TestClient(app, raise_server_exceptions=False)
        return client.post("/auth/login", json={"email": "a@example.com", "password": "x"})
    finally:
        app.dependency_overrides.pop(get_redis, None)


def test_a_redis_outage_on_login_is_a_503_with_retry_after():
    resp = _login_with(_Redis(RedisConnectionError("Connection refused")))
    assert resp.status_code == 503
    assert resp.headers["retry-after"] == "5"


def test_a_redis_command_error_is_still_a_500():
    # A rejected command is a defect in our code, not an outage.
    resp = _login_with(_Redis(ResponseError("WRONGTYPE")))
    assert resp.status_code == 500
