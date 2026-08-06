from workflow.router import looks_like_db


def test_mysql_greeting_on_odd_port():
    # MySQL greeting carries a version string like "5.7.42-log" early in the banner.
    assert looks_like_db({"banner": "J\x00\x00\x00\x0a5.7.42-log\x00"}) is True


def test_redis_noauth_signature():
    assert looks_like_db({"banner": "-NOAUTH Authentication required."}) is True


def test_plain_http_is_not_db():
    assert looks_like_db({"first_line": "HTTP/1.1 200 OK", "banner": "<html>"}) is False
