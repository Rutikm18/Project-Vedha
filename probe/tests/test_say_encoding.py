"""Regression: agent output must never crash on non-ASCII glyphs.

The agent prints UI glyphs (warnings ``⚠``, checks ``✓``, arrows ``→``) during
startup. On a Windows cp1252 console those used to raise UnicodeEncodeError from
inside ``say()`` and kill the process mid-preflight — a cosmetic warning line
taking down the whole agent before it could connect. ``say()`` must degrade the
glyph instead of raising, on any console encoding.
"""
from __future__ import annotations

import io

from agent.agent import say


def test_say_survives_non_ascii_on_a_cp1252_stream(monkeypatch):
    # Simulate a Windows console that cannot encode ⚠ / ✓ / →. Critically, this
    # wrapper exposes NO reconfigure(), so we exercise say()'s own guard, not the
    # module-level stream reconfigure.
    class _Cp1252Stream(io.TextIOWrapper):
        def reconfigure(self, *a, **k):  # noqa: D401 - block the escape hatch
            raise OSError("cannot reconfigure this stream")

    buf = _Cp1252Stream(io.BytesIO(), encoding="cp1252")
    monkeypatch.setattr("sys.stdout", buf)

    # The exact line that crashed the agent in the field — must not raise.
    say("⚠ This probe is on 10.0.0.5, but PROBE_NETWORK_SEGMENTS does not include it.", 1)
    say("✓ ok → next", 0)

    buf.flush()
    written = buf.buffer.getvalue().decode("cp1252")
    # The surrounding ASCII text survives; the unencodable glyph is replaced, not fatal.
    assert "This probe is on 10.0.0.5" in written
    assert "ok" in written and "next" in written


def test_say_plain_ascii_is_unchanged(capsys):
    say("hello", 1)
    assert capsys.readouterr().out == "  hello\n"
