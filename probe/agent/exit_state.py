"""exit_state.py — the wide exit-state channel (0b contract).

Replaces overloaded exit codes: the code carries only a BROAD class; the detail
(reason + remediation) rides `exit-state.json` and a structured stderr line the
supervisor parses. This is why "cert expired" is never confused with "manager
down". Pure — no IO except the tiny read/write helpers.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

CONTRACT_VERSION = "1.0.0"

# class name -> exit code (broad classes only)
CLASSES: dict[str, int] = {
    "success": 0,
    "retryable": 10,
    "fatal-config": 20,
    "fatal-identity": 30,
    "awaiting-approval": 40,
}
_CODE_TO_CLASS = {code: cls for cls, code in CLASSES.items()}

# concrete reason -> class (contract table)
REASON_CLASS: dict[str, str] = {
    "clean-shutdown": "success",
    "manager-503": "retryable",
    "manager-unreachable": "retryable",
    "dns-failed": "retryable",
    "no-interface-up": "retryable",
    "tls-transient": "retryable",
    "empty-scope": "fatal-config",
    "bad-manager-url": "fatal-config",
    "clock-skew-exceeds-ttl": "fatal-config",
    "contract-version-mismatch": "fatal-config",
    "cert-expired": "fatal-identity",
    "identity-revoked": "fatal-identity",
    "orphaned-identity": "fatal-identity",
    "pairing-pending": "awaiting-approval",
}


def class_for_reason(reason: str) -> str:
    # Unknown reasons default to retryable — never hard-stop on the unexpected;
    # the supervisor's restart cap bounds it.
    return REASON_CLASS.get(reason, "retryable")


def code_for_class(cls: str) -> int:
    return CLASSES.get(cls, 10)


def code_for_reason(reason: str) -> int:
    return code_for_class(class_for_reason(reason))


def class_for_code(code: int) -> str:
    return _CODE_TO_CLASS.get(code, "retryable")


@dataclass
class ExitState:
    reason: str
    cls: str
    code: int
    remediation: str = ""
    at_monotonic: float = 0.0
    contract_version: str = CONTRACT_VERSION


def make(reason: str, remediation: str = "", at_monotonic: float = 0.0) -> ExitState:
    cls = class_for_reason(reason)
    return ExitState(reason=reason, cls=cls, code=code_for_class(cls),
                     remediation=remediation, at_monotonic=at_monotonic)


def to_json(st: ExitState) -> str:
    return json.dumps({
        "contract_version": st.contract_version,
        "class": st.cls,
        "code": st.code,
        "reason": st.reason,
        "remediation": st.remediation,
        "at_monotonic": st.at_monotonic,
    })


def from_json(text: str) -> ExitState:
    d = json.loads(text)
    return ExitState(
        reason=d["reason"], cls=d["class"], code=int(d["code"]),
        remediation=d.get("remediation", ""), at_monotonic=float(d.get("at_monotonic", 0.0)),
        contract_version=d.get("contract_version", CONTRACT_VERSION),
    )


def write(path: str, st: ExitState) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(to_json(st))


def read(path: str) -> ExitState | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return from_json(fh.read())
    except (OSError, ValueError, KeyError):
        return None


def stderr_line(st: ExitState) -> str:
    return f"VEDHA-EXIT {st.cls} {st.reason} :: {st.remediation}"


def parse_stderr_line(line: str) -> tuple[str, str, str] | None:
    prefix = "VEDHA-EXIT "
    if not line.startswith(prefix):
        return None
    head, sep, rem = line[len(prefix):].partition(" :: ")
    parts = head.split(None, 1)
    if len(parts) < 2:
        return None
    return parts[0], parts[1].strip(), (rem.strip() if sep else "")
