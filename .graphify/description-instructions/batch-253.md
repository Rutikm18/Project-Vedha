# Node Description Batch 254 of 380

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

- "main_scripts_scanner_base_rationale_750": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/main_scripts/scanner_base.py:L750 | neighbors=[main_entrypoint()] | lang=en
- "main_scripts_scanner_base_rationale_771": "Just the candidate IP strings for `target`, in RFC-6724 order, de-duplicated." | kind=entity | source=probe/main_scripts/scanner_base.py:L771 | neighbors=[resolve_ip_candidates()] | lang=en
- "main_scripts_scanner_base_rationale_778": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/main_scripts/scanner_base.py:L778 | neighbors=[run_cli()] | lang=en
- "main_scripts_scanner_base_rationale_786": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/main_scripts/scanner_base.py:L786 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_rationale_79": "A per-probe delay of `base` seconds ± up to `jitter` fraction of random     vari" | kind=entity | source=probe/main_scripts/scanner_base.py:L79 | neighbors=[jittered_delay()] | lang=en
- "main_scripts_scanner_base_rationale_808": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/main_scripts/scanner_base.py:L808 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_rationale_819": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/main_scripts/scanner_base.py:L819 | neighbors=[async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_837": "Run a scanner CLI's body with consistent, operator-friendly error handling." | kind=entity | source=probe/main_scripts/scanner_base.py:L837 | neighbors=[main_entrypoint()] | lang=en
- "main_scripts_scanner_base_rationale_841": "Send one UDP datagram and await the first reply — fully on the event loop." | kind=entity | source=probe/main_scripts/scanner_base.py:L841 | neighbors=[async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_850": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/main_scripts/scanner_base.py:L850 | neighbors=[async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_rationale_86": "Current time as an AWARE datetime in the project timezone." | kind=entity | source=probe/main_scripts/scanner_base.py:L86 | neighbors=[project_now()] | lang=en
- "main_scripts_scanner_base_rationale_865": "Wire argparse args into a scanner instance and execute it." | kind=entity | source=probe/main_scripts/scanner_base.py:L865 | neighbors=[run_cli()] | lang=en
- "main_scripts_scanner_base_rationale_869": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/main_scripts/scanner_base.py:L869 | neighbors=[bracket_host()] | lang=en
- "main_scripts_scanner_base_rationale_872": "`async_udp_probe` with bounded per-port retransmit.      Returns on the FIRST de" | kind=entity | source=probe/main_scripts/scanner_base.py:L872 | neighbors=[async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_rationale_881": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/main_scripts/scanner_base.py:L881 | neighbors=[parse_ports()] | lang=pt
- "main_scripts_scanner_base_rationale_891": "Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.     'h" | kind=entity | source=probe/main_scripts/scanner_base.py:L891 | neighbors=[bracket_host()] | lang=en
- "main_scripts_scanner_base_rationale_90": "Heuristic: is this host a tarpit / honeypot / ACK-everything middlebox?      Suc" | kind=entity | source=probe/main_scripts/scanner_base.py:L90 | neighbors=[assess_tarpit()] | lang=en
- "main_scripts_scanner_base_rationale_903": "Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)." | kind=entity | source=probe/main_scripts/scanner_base.py:L903 | neighbors=[parse_ports()] | lang=pt
- "main_scripts_scanner_base_rationale_91": "ISO-8601 instant in the project timezone: 2026-09-03T23:15:05+05:30." | kind=entity | source=probe/main_scripts/scanner_base.py:L91 | neighbors=[project_timestamp()] | lang=en
- "main_scripts_scanner_base_rationale_917": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/main_scripts/scanner_base.py:L917 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_rationale_939": "Writes ScanResult objects as JSONL to a file and/or stdout." | kind=entity | source=probe/main_scripts/scanner_base.py:L939 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_rationale_947": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/main_scripts/scanner_base.py:L947 | neighbors=[BaseScanner] | lang=pt
- "main_scripts_scanner_base_rationale_96": "Compact project-local stamp for FILE and DIRECTORY names.      Deliberately carr" | kind=entity | source=probe/main_scripts/scanner_base.py:L96 | neighbors=[project_file_stamp()] | lang=en
- "main_scripts_scanner_base_rationale_969": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/main_scripts/scanner_base.py:L969 | neighbors=[BaseScanner] | lang=pt
- "main_scripts_scanner_base_rationale_99": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/main_scripts/scanner_base.py:L99 | neighbors=[classify_os_error()] | lang=en
- "main_scripts_scanner_base_resultwriter_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L941 | neighbors=[ResultWriter] | lang=en
- "main_scripts_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L295 | neighbors=[ScanResult] | lang=en
- "main_scripts_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L363 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L327 | neighbors=[ScopeGuard] | lang=en
- "main_scripts_scanner_base_sendpacer_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L583 | neighbors=[SendPacer] | lang=en
- "main_scripts_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L1119 | neighbors=[scanner_base.py] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L834 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L820 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L824 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L817 | neighbors=[_UDPProbeProtocol] | lang=en
- "main_scripts_scanner_registry_info": "info()" | kind=code-symbol | source=probe/main_scripts/scanner_registry.py:L103 | neighbors=[scanner_registry.py] | lang=en
- "main_scripts_scanner_registry_rationale_1": "scanner_registry.py — the single source of truth for WHICH scanners are trusted." | kind=entity | source=probe/main_scripts/scanner_registry.py:L1 | neighbors=[scanner_registry.py] | lang=en
- "main_scripts_scanner_registry_rationale_108": "The scanner-module trust view: which scanners are verified vs experimental," | kind=entity | source=probe/main_scripts/scanner_registry.py:L108 | neighbors=[verification_report()] | lang=en
- "main_scripts_scanner_registry_rationale_98": "True only for a scanner explicitly on the verified (trusted) list. Unknown     s" | kind=entity | source=probe/main_scripts/scanner_registry.py:L98 | neighbors=[is_verified()] | lang=en
- "main_scripts_scanner_registry_scannerinfo": "ScannerInfo" | kind=code-symbol | source=probe/main_scripts/scanner_registry.py:L27 | neighbors=[scanner_registry.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-253.json

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
