from scanner.db_scanner import interpret_redis_info


def test_redis_unauthenticated():
    out = interpret_redis_info("$100\r\n# Server\r\nredis_version:7.2.4\r\n")
    assert out["auth_required"] is False
    assert out["unauthenticated_read"] is True
    assert out["server_version"] == "7.2.4"


def test_redis_authenticated():
    out = interpret_redis_info("-NOAUTH Authentication required.\r\n")
    assert out["auth_required"] is True
    assert out["unauthenticated_read"] is False
