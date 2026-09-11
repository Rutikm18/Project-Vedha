"""
ServiceNow incident creation.

"No ticketing integration (Jira, ServiceNow)" was half-wrong — Jira and Slack
already existed — but ServiceNow genuinely did not, and it is the ticketing
system most enterprise security teams actually run on. A finding that cannot
reach the queue where work is tracked is a finding nobody will action.

Follows the established shape exactly: a `_send_*` callable registered in
`_SENDERS`, validating required config and raising ValueError when it is missing.
`deliver()` already catches and logs, so a misconfigured integration degrades to
a logged failure rather than a 500 — but it must FAIL, not silently no-op, or an
operator would believe tickets were being filed when none were.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.routers.integrations import _KINDS
from app.services import notifications as n


class TestRegistration:
    def test_servicenow_is_an_accepted_kind(self):
        assert "servicenow" in _KINDS

    def test_existing_kinds_are_untouched(self):
        """Adding one must not disturb the integrations already in use."""
        assert {"email", "slack", "jira"} <= _KINDS

    def test_sender_is_registered_for_dispatch(self):
        """A kind the API accepts but deliver() cannot route would accept
        configuration and then silently drop every notification."""
        assert "servicenow" in n._SENDERS


class TestConfigValidation:
    @pytest.mark.parametrize("config,secret", [
        ({}, "tok"),                                             # nothing at all
        ({"SERVICENOW_URL": "https://x.service-now.com"}, "tok"),  # no user
        ({"SERVICENOW_USERNAME": "svc"}, "tok"),                 # no url
        ({"SERVICENOW_URL": "https://x.service-now.com",
          "SERVICENOW_USERNAME": "svc"}, None),                  # no token
    ])
    def test_missing_config_raises_rather_than_silently_passing(self, config, secret):
        with pytest.raises(ValueError, match="servicenow"):
            n._send_servicenow(config, secret, "subject", "body")


class TestIncidentCreation:
    def _config(self):
        return {
            "SERVICENOW_URL": "https://acme.service-now.com/",
            "SERVICENOW_USERNAME": "svc_vedha",
        }

    def test_posts_an_incident_to_the_table_api(self):
        with patch.object(n.httpx, "post", return_value=MagicMock()) as post:
            n._send_servicenow(self._config(), "tok", "SMBv1 on 10.0.0.5", "details")
        url = post.call_args[0][0]
        assert url == "https://acme.service-now.com/api/now/table/incident"

    def test_subject_and_body_map_to_servicenow_fields(self):
        with patch.object(n.httpx, "post", return_value=MagicMock()) as post:
            n._send_servicenow(self._config(), "tok", "SMBv1 on 10.0.0.5", "details")
        payload = post.call_args.kwargs["json"]
        assert payload["short_description"] == "SMBv1 on 10.0.0.5"
        assert payload["description"] == "details"

    def test_authenticates_with_the_stored_secret(self):
        with patch.object(n.httpx, "post", return_value=MagicMock()) as post:
            n._send_servicenow(self._config(), "tok", "s", "b")
        assert post.call_args.kwargs["auth"] == ("svc_vedha", "tok")

    def test_target_table_is_configurable(self):
        """Not every org files security work as `incident`."""
        cfg = {**self._config(), "SERVICENOW_TABLE": "sn_si_incident"}
        with patch.object(n.httpx, "post", return_value=MagicMock()) as post:
            n._send_servicenow(cfg, "tok", "s", "b")
        assert post.call_args[0][0].endswith("/api/now/table/sn_si_incident")

    def test_http_failure_propagates_to_deliver(self):
        """deliver() owns the catch-and-log policy; the sender must not swallow
        errors itself or a failed ticket would look like a filed one."""
        resp = MagicMock()
        resp.raise_for_status.side_effect = RuntimeError("503")
        with patch.object(n.httpx, "post", return_value=resp):
            with pytest.raises(RuntimeError):
                n._send_servicenow(self._config(), "tok", "s", "b")

    def test_deliver_routes_servicenow_and_reports_failure(self):
        """End of the path: a broken integration returns False, never raises."""
        def _boom(*a, **k):
            raise ValueError("servicenow integration missing URL/USERNAME/token")
        assert n.deliver("servicenow", {}, None, "s", "b",
                         senders={"servicenow": _boom}) is False
