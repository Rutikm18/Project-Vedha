from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

from app.ai.failures import (
    INVALID_OUTPUT,
    NETWORK,
    TIMEOUT,
    classify_http,
    parse_retry_after,
    seconds_until_next_month,
)
from app.services.llm import _provider_error_message

_SPEND_CAP_MSG = "You have reached your specified API usage limits. You will regain access on 2026-10-01."


def test_anthropic_spend_cap_429_is_blocked_until_next_month():
    failure = classify_http(429, _SPEND_CAP_MSG)
    assert failure.kind == "spend_cap"
    assert failure.blocked is True
    assert 0 < failure.cooldown_s <= 31 * 86400


def test_openai_insufficient_quota_is_billing_not_rate_limit():
    failure = classify_http(429, "You exceeded your current quota (insufficient_quota)")
    assert failure.kind == "billing"
    assert failure.blocked is True


def test_anthropic_credit_balance_400_is_billing():
    assert classify_http(400, "Your credit balance is too low").kind == "billing"


def test_rate_limit_honours_retry_after_else_defaults_to_60():
    assert classify_http(429, "rate_limit_error", retry_after=12).cooldown_s == 12
    default = classify_http(429, "rate_limit_error")
    assert (default.kind, default.cooldown_s, default.blocked) == ("rate_limit", 60, False)


def test_overload_escalates_and_malformed_request_does_not_cool_down():
    overloaded = classify_http(529, "overloaded_error")
    assert (overloaded.kind, overloaded.escalates) == ("overloaded", True)
    malformed = classify_http(400, "messages: field required")
    assert (malformed.kind, malformed.cooldown_s) == ("request", None)


def test_auth_failure_is_blocked():
    failure = classify_http(401, "invalid x-api-key")
    assert (failure.kind, failure.blocked) == ("auth", True)


def test_exception_failures():
    assert TIMEOUT.kind == "timeout" and TIMEOUT.escalates
    assert NETWORK.kind == "network" and NETWORK.escalates
    assert INVALID_OUTPUT.cooldown_s is None


def test_parse_retry_after_seconds_date_and_garbage():
    assert parse_retry_after("7") == 7
    now = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
    later = format_datetime(now + timedelta(seconds=90), usegmt=True)
    assert parse_retry_after(later, now=now) == 90
    assert parse_retry_after("soon") is None
    assert parse_retry_after(None) is None


def test_seconds_until_next_month():
    now = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)
    assert seconds_until_next_month(now) == 2.5 * 86400
    december = datetime(2026, 12, 31, 0, 0, tzinfo=timezone.utc)
    assert seconds_until_next_month(december) == 86400


def test_spend_cap_message_is_actionable():
    message, status = _provider_error_message("anthropic", 429, _SPEND_CAP_MSG)
    assert status == 402
    assert "spend limit" in message


def test_openai_empty_prepaid_balance_is_billing_without_relying_on_the_url():
    # Observed live 2026-09-28 (HTTP 429). The URL is stripped here so the match
    # cannot come from the word "billing" in the settings link.
    failure = classify_http(429, "You have no credits remaining. Add credits to continue using the API.")
    assert (failure.kind, failure.blocked) == ("billing", True)


def test_provider_reason_never_carries_key_fragments():
    # Observed on AWS: OpenAI echoes a masked copy of the rejected key, and the
    # manager logged it verbatim (first 8 + last 4 characters).
    import httpx
    from app.services.llm import _provider_error_reason
    body = {"error": {"message": "Incorrect API key provided: proj-I0K****************cPUA. "
                                 "You can find your API key at https://platform.openai.com/account/api-keys."}}
    reason = _provider_error_reason(httpx.Response(401, json=body))
    assert "I0K" not in reason and "cPUA" not in reason
    assert "Incorrect API key provided" in reason          # still diagnosable
    for leaked in ("sk-proj-AbCdEf123456789", "sk-ant-api03-AbCdEf123456", "AIzaSyAbCdEf1234567890",
                   "gsk_AbCdEf1234567890abcd"):
        reason = _provider_error_reason(httpx.Response(400, json={"error": {"message": f"bad key {leaked} here"}}))
        assert leaked not in reason and "[redacted]" in reason
