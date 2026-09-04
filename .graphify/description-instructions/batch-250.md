# Node Description Batch 251 of 330

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scanner_scanner_base_rationale_652": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L652 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_660": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L660 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_667": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L667 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_67": "The project timezone, degrading safely when tzdata is unavailable." | kind=entity | source=probe/scanner/scanner_base.py:L67 | neighbors=[_resolve_project_tz()] | lang=en
- "scanner_scanner_base_rationale_681": "Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and     h" | kind=entity | source=probe/scanner/scanner_base.py:L681 | neighbors=[resolve()] | lang=en
- "scanner_scanner_base_rationale_696": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L696 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_70": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L70 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_rationale_706": "EVERY distinct (family, sockaddr) for `target`, in getaddrinfo/RFC-6724 order." | kind=entity | source=probe/scanner/scanner_base.py:L706 | neighbors=[resolve_candidates()] | lang=en
- "scanner_scanner_base_rationale_726": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L726 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_749": "Just the candidate IP strings for `target`, in RFC-6724 order, de-duplicated." | kind=entity | source=probe/scanner/scanner_base.py:L749 | neighbors=[resolve_ip_candidates()] | lang=en
- "scanner_scanner_base_rationale_750": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L750 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_778": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L778 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_786": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L786 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_rationale_79": "A per-probe delay of `base` seconds ± up to `jitter` fraction of random     vari" | kind=entity | source=probe/scanner/scanner_base.py:L79 | neighbors=[jittered_delay()] | lang=en
- "scanner_scanner_base_rationale_819": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/scanner/scanner_base.py:L819 | neighbors=[async_udp_probe()] | lang=en
- "scanner_scanner_base_rationale_837": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/scanner/scanner_base.py:L837 | neighbors=[main_entrypoint()] | lang=en
- "scanner_scanner_base_rationale_850": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/scanner/scanner_base.py:L850 | neighbors=[async_udp_probe_retry()] | lang=en
- "scanner_scanner_base_rationale_86": "Current time as an AWARE datetime in the project timezone." | kind=entity | source=probe/scanner/scanner_base.py:L86 | neighbors=[project_now()] | lang=en
- "scanner_scanner_base_rationale_865": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/scanner/scanner_base.py:L865 | neighbors=[run_cli()] | lang=en
- "scanner_scanner_base_rationale_869": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/scanner/scanner_base.py:L869 | neighbors=[bracket_host()] | lang=en
- "scanner_scanner_base_rationale_881": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/scanner/scanner_base.py:L881 | neighbors=[parse_ports()] | lang=pt
- "scanner_scanner_base_rationale_90": "Heuristic: is this host a tarpit / honeypot / ACK-everything middlebox?      Suc" | kind=entity | source=probe/scanner/scanner_base.py:L90 | neighbors=[assess_tarpit()] | lang=en
- "scanner_scanner_base_rationale_91": "ISO-8601 instant in the project timezone: 2026-09-03T23:15:05+05:30." | kind=entity | source=probe/scanner/scanner_base.py:L91 | neighbors=[project_timestamp()] | lang=en
- "scanner_scanner_base_rationale_917": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/scanner/scanner_base.py:L917 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_rationale_947": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L947 | neighbors=[BaseScanner] | lang=pt
- "scanner_scanner_base_rationale_96": "Compact project-local stamp for FILE and DIRECTORY names.      Deliberately carr" | kind=entity | source=probe/scanner/scanner_base.py:L96 | neighbors=[project_file_stamp()] | lang=en
- "scanner_scanner_base_rationale_99": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/scanner/scanner_base.py:L99 | neighbors=[classify_os_error()] | lang=en
- "scanner_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L919 | neighbors=[ResultWriter] | lang=en
- "scanner_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L295 | neighbors=[ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L363 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L327 | neighbors=[ScopeGuard] | lang=en
- "scanner_scanner_base_sendpacer_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L561 | neighbors=[SendPacer] | lang=en
- "scanner_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1097 | neighbors=[scanner_base.py] | lang=en
- "scanner_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L812 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L798 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L802 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L795 | neighbors=[_UDPProbeProtocol] | lang=en
- "scanner_scanner_registry_info": "info()" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L103 | neighbors=[scanner_registry.py] | lang=en
- "scanner_scanner_registry_rationale_1": "scanner_registry.py — the single source of truth for WHICH scanners are trusted." | kind=entity | source=probe/scanner/scanner_registry.py:L1 | neighbors=[scanner_registry.py] | lang=en
- "scanner_scanner_registry_rationale_108": "The scanner-module trust view: which scanners are verified vs experimental," | kind=entity | source=probe/scanner/scanner_registry.py:L108 | neighbors=[verification_report()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-250.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
