"""
notifications.py — deliver a message to a tenant's configured integrations
(email / Slack / Jira). The per-channel senders are injectable (`senders=`) so the
dispatch/fan-out logic is unit-tested without real SMTP/HTTP. Consumed by the
outbox `notify` handler; producers call `enqueue_notification`.

Delivery is best-effort per channel: a failing channel is logged and skipped, never
raised, so one broken integration can't block the others.
"""
from __future__ import annotations

import smtplib
from email.mime.text import MIMEText
from typing import Any, Callable

import httpx
import structlog
from sqlalchemy import select

from app.models.integration import Integration
from app.services.credential_crypto import decrypt_credential

logger = structlog.get_logger()

Sender = Callable[[dict, str | None, str, str], None]


def _send_email(config: dict, secret: str | None, subject: str, body: str) -> None:
    host = config.get("SMTP_HOST")
    port = int(config.get("SMTP_PORT") or 587)
    user = config.get("SMTP_USER")
    sender = config.get("SMTP_FROM") or user
    recipients = [t.strip() for t in (config.get("SMTP_TO") or "").split(",") if t.strip()]
    if not (host and sender and recipients):
        raise ValueError("email integration missing SMTP_HOST/SMTP_FROM/SMTP_TO")
    msg = MIMEText(body)
    msg["Subject"], msg["From"], msg["To"] = subject, sender, ", ".join(recipients)
    with smtplib.SMTP(host, port, timeout=15) as smtp:
        smtp.starttls()
        if user and secret:
            smtp.login(user, secret)
        smtp.sendmail(sender, recipients, msg.as_string())


def _send_slack(config: dict, secret: str | None, subject: str, body: str) -> None:
    if not secret:
        raise ValueError("slack integration missing webhook URL")
    resp = httpx.post(secret, json={"text": f"*{subject}*\n{body}"}, timeout=15)
    resp.raise_for_status()


def _send_jira(config: dict, secret: str | None, subject: str, body: str) -> None:
    url = (config.get("JIRA_URL") or "").rstrip("/")
    email = config.get("JIRA_EMAIL")
    project = config.get("JIRA_PROJECT_KEY")
    if not (url and email and secret and project):
        raise ValueError("jira integration missing URL/EMAIL/token/PROJECT_KEY")
    resp = httpx.post(
        f"{url}/rest/api/2/issue", auth=(email, secret),
        json={"fields": {"project": {"key": project}, "summary": subject,
                         "description": body, "issuetype": {"name": "Task"}}},
        timeout=20,
    )
    resp.raise_for_status()


_SENDERS: dict[str, Sender] = {"email": _send_email, "slack": _send_slack, "jira": _send_jira}


def deliver(kind: str, config: dict, secret: str | None, subject: str, body: str, *,
            senders: dict[str, Sender] | None = None) -> bool:
    """Send via one integration. True on success; False on any handled failure
    (logged, never raised)."""
    send = (senders or _SENDERS).get(kind)
    if send is None:
        logger.warning("notify.unknown_kind", kind=kind)
        return False
    try:
        send(config, secret, subject, body)
        return True
    except Exception as exc:                    # noqa: BLE001 — one channel must not break others
        logger.warning("notify.delivery_failed", kind=kind, error=str(exc))
        return False


async def notify_tenant(db: Any, tenant_id: Any, subject: str, body: str, *,
                        senders: dict[str, Sender] | None = None) -> int:
    """Deliver to every ENABLED integration for the tenant. Returns the count sent."""
    rows = (await db.execute(
        select(Integration).where(Integration.tenant_id == tenant_id,
                                  Integration.enabled.is_(True))
    )).scalars().all()
    sent = 0
    for row in rows:
        if deliver(row.kind, dict(row.config or {}), decrypt_credential(row.secret_enc),
                   subject, body, senders=senders):
            sent += 1
    return sent


def enqueue_notification(db: Any, tenant_id: Any, subject: str, body: str):
    """Producer API: enqueue a durable notify event (commits with the caller's txn)."""
    from app.models.outbox import TOPIC_NOTIFY
    from app.workers.outbox import enqueue
    return enqueue(db, TOPIC_NOTIFY,
                   payload={"tenant_id": str(tenant_id), "subject": subject, "body": body})
