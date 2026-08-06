"""
agent — the probe transport layer (sealed, push-driven, hardware-bound).

Architecture (Phase 1–2):
    agent.py          — thin main loop: startup gauntlet → WS push or HTTP poll
    transport.py      — HTTP + WebSocket manager communication (Phase 2)
    task_runner.py    — job lifecycle: validate → scan → submit
    scope_validator.py — defense-in-depth scope re-validation
    result_spool.py   — local spool with upload retry (crash-safe)
    scope_crypt.py    — X25519 + AES-256-GCM scope encryption (Phase 4)
    hw_bind.py        — hardware fingerprinting for binary host-binding (Phase 3)
    license.py        — host-locked Ed25519 vendor license verification
    engine.py         — scan execution dispatch (→ scanner/ + workflow/)
    use_cases.py      — finite, pre-defined library of scan scenarios

The probe is compiled to a single native binary via Nuitka (build_probe.sh).
No Python, no readable bytecode ships to the client.
"""
