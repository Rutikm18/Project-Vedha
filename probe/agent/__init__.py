"""
agent — the probe transport: register → heartbeat → poll → scan → submit.

Wraps scanner_module's scan engine (scanner/ + workflow/) with the manager
protocol ported from the platform's probe agent. Ships RAW FACTS (ScanResult
dicts) upstream; never emits a CVE — detection runs on the manager.
"""
