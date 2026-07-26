#!/usr/bin/env python3
"""selftest_live.py — run the REAL probe engine against an in-process fixture
and ASSERT every fact, so you can see each function actually works (PASS/FAIL).

No Docker, no external services, no network beyond localhost. It:
  1. starts a controllable HTTP server on localhost with planted values,
  2. scans it via agent.engine.run_scan() — the exact manager-job code path,
  3. checks the returned facts against the known ground truth,
  4. verifies scope + exclusion refusals and the UDP wiring,
  5. prints PASS/FAIL per function and exits non-zero if any fail (CI-friendly).

Run:  ./.venv/bin/python selftest_live.py     (or ./showcase.sh --selftest)
"""
from __future__ import annotations

import http.server
import socket
import sys
import threading

from agent.engine import run_scan

FIXTURE_TITLE = "VA-SCANNER-FIXTURE"
FIXTURE_SERVER = "FixtureHTTP/1.0"
WEB_CANDIDATES = [8081, 8000, 8888, 9000]  # all inside the probe's WEB_PORTS set


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s

OK = _c("32", "PASS")
NO = _c("31", "FAIL")
BOLD = lambda s: _c("1", s)

_results: list[bool] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    _results.append(bool(ok))
    line = f"  [{OK if ok else NO}] {name}"
    if detail:
        line += f"  — {detail}"
    print(line)


class _Handler(http.server.BaseHTTPRequestHandler):
    server_version = FIXTURE_SERVER
    sys_version = ""

    def log_message(self, *a):  # silence
        pass

    def do_GET(self):
        body = (f"<html><title>{FIXTURE_TITLE}</title>"
                f"<body>ok</body></html>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Allow", "GET, HEAD, POST, PUT, DELETE, OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()


def _free_port() -> int | None:
    for p in WEB_CANDIDATES:
        s = socket.socket()
        try:
            s.bind(("127.0.0.1", p))
            s.close()
            return p
        except OSError:
            s.close()
    return None


def _fact(result: dict, scanner: str | None = None, port: int | None = None) -> dict | None:
    for f in result.get("facts", []):
        if scanner and f.get("scanner") != scanner:
            continue
        if port is not None and f.get("port") != port:
            continue
        return f
    return None


def main() -> int:
    port = _free_port()
    if port is None:
        print("No free fixture port among", WEB_CANDIDATES)
        return 2

    httpd = http.server.HTTPServer(("127.0.0.1", port), _Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(BOLD(f"\nFixture HTTP server on 127.0.0.1:{port} "
               f"(title={FIXTURE_TITLE!r}, server={FIXTURE_SERVER!r})\n"))

    try:
        print(BOLD("web_scan — fingerprint a real service"))
        r = run_scan("web_scan", {"targets": ["127.0.0.1"], "profile": "it"},
                     validated_scope=["127.0.0.1/32"])
        wf = _fact(r, scanner="web_scan", port=port)
        check("web_scan finds the fixture service", wf is not None)
        if wf:
            d = wf.get("data", {})
            check("reads the page <title>", d.get("title") == FIXTURE_TITLE,
                  f"title={d.get('title')!r}")
            check("reads the Server header", (d.get("server") or "").startswith("FixtureHTTP"),
                  f"server={d.get('server')!r}")
            am, dm = d.get("allowed_methods", []), d.get("dangerous_methods", [])
            check("Task5: allowed_methods captured (OPTIONS)", "GET" in am and "POST" in am,
                  f"allowed={am}")
            check("Task5: dangerous methods flagged", "PUT" in dm and "DELETE" in dm,
                  f"dangerous={dm}")

        print(BOLD("\nscope safety — the whole point of a scanner"))
        r2 = run_scan("discovery", {"targets": ["8.8.8.8"], "profile": "it"},
                      validated_scope=["127.0.0.1/32"])
        check("out-of-scope target (8.8.8.8) refused",
              r2.get("error_code") == "no_authorized_targets"
              and not (r2.get("run_stats") or {}).get("scanners_run"),
              f"error_code={r2.get('error_code')}")

        r3 = run_scan("discovery", {"targets": ["127.0.0.1"], "profile": "it"},
                      validated_scope=["127.0.0.0/8"], validated_excludes=["127.0.0.1/32"])
        check("excluded target (127.0.0.1) refused",
              r3.get("error_code") == "no_authorized_targets",
              f"error_code={r3.get('error_code')}")

        print(BOLD("\nudp wiring — Task 4 amplifier ports reach the engine"))
        r4 = run_scan("udp_scan", {"targets": ["127.0.0.1"], "profile": "it"},
                      validated_scope=["127.0.0.1/32"])
        udp_ports = {f.get("port") for f in r4.get("facts", []) if f.get("scanner") == "udp_scan"}
        check("Task4: udp_scan probes memcached (11211)", 11211 in udp_ports,
              f"probed={sorted(udp_ports)}")

    finally:
        httpd.shutdown()

    passed, total = sum(_results), len(_results)
    print(BOLD(f"\n{passed}/{total} checks passed\n"))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
