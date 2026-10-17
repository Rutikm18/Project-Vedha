"""Gzip request bodies are inflated with a hard output cap.

GzipRequestMiddleware sits outside authentication. It used to call
gzip.decompress on the whole body and only then compare the result with the
128 MB ceiling, so ~32 MB of compressed zeros could expand to tens of GB in
memory before anything was rejected.
"""
from __future__ import annotations

import gzip
import json
import tracemalloc
import zlib

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.main import GzipRequestMiddleware, GzipTooLarge, bounded_gunzip


def _bomb(inflated_bytes: int) -> bytes:
    z = zlib.compressobj(9, zlib.DEFLATED, 16 + zlib.MAX_WBITS)
    block = b"\0" * (1 << 20)
    out = [z.compress(block) for _ in range(inflated_bytes // len(block))]
    out.append(z.flush())
    return b"".join(out)


class TestBoundedGunzip:
    def test_round_trip(self):
        assert bounded_gunzip(gzip.compress(b"hello"), 100) == b"hello"

    def test_multi_member_body_is_fully_inflated(self):
        data = gzip.compress(b"abc") + gzip.compress(b"def")
        assert bounded_gunzip(data, 100) == b"abcdef"

    def test_exactly_at_the_limit_is_allowed(self):
        assert bounded_gunzip(gzip.compress(b"x" * 64), 64) == b"x" * 64

    def test_one_byte_over_the_limit_is_refused(self):
        with pytest.raises(GzipTooLarge):
            bounded_gunzip(gzip.compress(b"x" * 65), 64)

    def test_limit_applies_across_members(self):
        with pytest.raises(GzipTooLarge):
            bounded_gunzip(gzip.compress(b"x" * 40) + gzip.compress(b"y" * 40), 64)

    def test_truncated_body_is_an_error(self):
        with pytest.raises(EOFError):
            bounded_gunzip(gzip.compress(b"hello world")[:-6], 100)

    def test_bomb_is_stopped_without_inflating_it(self):
        bomb = _bomb(256 << 20)          # 256 MB of zeros, ~250 KB on the wire
        tracemalloc.start()
        try:
            with pytest.raises(GzipTooLarge):
                bounded_gunzip(bomb, 1 << 20)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert peak < 16 << 20           # never anywhere near the 256 MB payload


def _client() -> TestClient:
    app = FastAPI()

    @app.post("/echo")
    async def echo(request: Request):
        return await request.json()

    app.add_middleware(GzipRequestMiddleware)
    return TestClient(app)


def test_gzipped_json_still_reaches_the_route():
    body = gzip.compress(json.dumps({"hosts": 3}).encode())
    r = _client().post("/echo", content=body,
                       headers={"Content-Encoding": "gzip", "Content-Type": "application/json"})
    assert r.status_code == 200 and r.json() == {"hosts": 3}


def test_oversized_inflation_is_413(monkeypatch):
    from app import main
    monkeypatch.setattr(main, "_GZIP_MAX_DECOMPRESSED_BYTES", 1 << 20)
    r = _client().post("/echo", content=_bomb(8 << 20), headers={"Content-Encoding": "gzip"})
    assert r.status_code == 413


def test_malformed_gzip_is_400():
    r = _client().post("/echo", content=b"not gzip at all", headers={"Content-Encoding": "gzip"})
    assert r.status_code == 400
