from scanner.web_scanner import parse_allow_header


def test_dangerous_methods_flagged():
    out = parse_allow_header("GET, POST, PUT, DELETE, OPTIONS, TRACE")
    assert "PUT" in out["dangerous_methods"]
    assert "DELETE" in out["dangerous_methods"]
    assert "TRACE" in out["dangerous_methods"]
    assert "GET" in out["allowed_methods"]


def test_safe_methods_only():
    out = parse_allow_header("GET, HEAD, OPTIONS")
    assert out["dangerous_methods"] == []


def test_no_allow_header():
    assert parse_allow_header(None)["allowed_methods"] == []
