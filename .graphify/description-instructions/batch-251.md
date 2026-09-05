# Node Description Batch 252 of 336

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
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

- "scanner_port_scanner_rationale_129": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=probe/scanner/port_scanner.py:L129 | neighbors=[resolve_profile()] | lang=pt
- "scanner_port_scanner_rationale_131": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=probe/scanner/port_scanner.py:L131 | neighbors=[resolve_profile()] | lang=pt
- "scanner_port_scanner_rationale_154": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=probe/scanner/port_scanner.py:L154 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_rationale_155": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=probe/scanner/port_scanner.py:L155 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_rationale_157": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=probe/scanner/port_scanner.py:L157 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_rationale_176": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L176 | neighbors=[_family_of()] | lang=en
- "scanner_port_scanner_rationale_182": "Tally exactly one terminal per-port observation." | kind=entity | source=probe/scanner/port_scanner.py:L182 | neighbors=[.record()] | lang=en
- "scanner_port_scanner_rationale_183": "Tally exactly one terminal per-port observation." | kind=entity | source=probe/scanner/port_scanner.py:L183 | neighbors=[.record()] | lang=en
- "scanner_port_scanner_rationale_185": "Tally exactly one terminal per-port observation." | kind=entity | source=probe/scanner/port_scanner.py:L185 | neighbors=[.record()] | lang=en
- "scanner_port_scanner_rationale_191": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/scanner/port_scanner.py:L191 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_199": "Emit a non-open result only when report_closed is on." | kind=entity | source=probe/scanner/port_scanner.py:L199 | neighbors=[._maybe()] | lang=en
- "scanner_port_scanner_rationale_201": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=probe/scanner/port_scanner.py:L201 | neighbors=[.missing_ports()] | lang=en
- "scanner_port_scanner_rationale_202": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=probe/scanner/port_scanner.py:L202 | neighbors=[.missing_ports()] | lang=en
- "scanner_port_scanner_rationale_204": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=probe/scanner/port_scanner.py:L204 | neighbors=[.missing_ports()] | lang=en
- "scanner_port_scanner_rationale_208": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=probe/scanner/port_scanner.py:L208 | neighbors=[.duplicate_ports()] | lang=pt
- "scanner_port_scanner_rationale_209": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=probe/scanner/port_scanner.py:L209 | neighbors=[.duplicate_ports()] | lang=pt
- "scanner_port_scanner_rationale_211": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=probe/scanner/port_scanner.py:L211 | neighbors=[.duplicate_ports()] | lang=pt
- "scanner_port_scanner_rationale_214": "Resolve a named scan profile to a concrete, de-duplicated port list.      'full'" | kind=entity | source=probe/scanner/port_scanner.py:L214 | neighbors=[resolve_profile()] | lang=pt
- "scanner_port_scanner_rationale_240": "Per-target scan accounting — the completeness + self-health record.      It lets" | kind=entity | source=probe/scanner/port_scanner.py:L240 | neighbors=[ScanMetrics] | lang=en
- "scanner_port_scanner_rationale_268": "Tally exactly one terminal per-port observation." | kind=entity | source=probe/scanner/port_scanner.py:L268 | neighbors=[.record()] | lang=en
- "scanner_port_scanner_rationale_287": "Requested ports that were never recorded — the silent-skip proof." | kind=entity | source=probe/scanner/port_scanner.py:L287 | neighbors=[.missing_ports()] | lang=en
- "scanner_port_scanner_rationale_294": "Ports recorded more than once (a port must get exactly one verdict)." | kind=entity | source=probe/scanner/port_scanner.py:L294 | neighbors=[.duplicate_ports()] | lang=pt
- "scanner_port_scanner_rationale_301": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/scanner/port_scanner.py:L301 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_313": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/scanner/port_scanner.py:L313 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_326": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/scanner/port_scanner.py:L326 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_367": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L367 | neighbors=[.scan_target()] | lang=en
- "scanner_port_scanner_rationale_391": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L391 | neighbors=[.scan_target()] | lang=en
- "scanner_port_scanner_rationale_405": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L405 | neighbors=[.scan_target()] | lang=en
- "scanner_port_scanner_rationale_451": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/scanner/port_scanner.py:L451 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_462": "One connect() and its classification. Always returns a ScanResult         (open" | kind=entity | source=probe/scanner/port_scanner.py:L462 | neighbors=[._attempt()] | lang=en
- "scanner_port_scanner_rationale_522": "One port's terminal result, gated by the rate limiter and (when         enabled)" | kind=entity | source=probe/scanner/port_scanner.py:L522 | neighbors=[._scan_port()] | lang=en
- "scanner_port_scanner_rationale_533": "One port's terminal result, gated by the rate limiter and (when         enabled)" | kind=entity | source=probe/scanner/port_scanner.py:L533 | neighbors=[._scan_port()] | lang=en
- "scanner_port_scanner_rationale_570": "True for the one state a retry can legitimately change: silence." | kind=entity | source=probe/scanner/port_scanner.py:L570 | neighbors=[._is_ambiguous()] | lang=en
- "scanner_port_scanner_rationale_576": "Gentle second look at ports that stayed silent through the main sweep." | kind=entity | source=probe/scanner/port_scanner.py:L576 | neighbors=[._reprobe_ambiguous()] | lang=en
- "scanner_port_scanner_rationale_584": "Record one probe and answer: is the PATH still delivering?          WHY THIS EXI" | kind=entity | source=probe/scanner/port_scanner.py:L584 | neighbors=[._note_probe_outcome()] | lang=en
- "scanner_port_scanner_rationale_603": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L603 | neighbors=[.scan_target()] | lang=en
- "scanner_port_scanner_rationale_615": "True for the one state a retry can legitimately change: silence." | kind=entity | source=probe/scanner/port_scanner.py:L615 | neighbors=[._is_ambiguous()] | lang=en
- "scanner_port_scanner_rationale_621": "Gentle second look at ports that stayed silent through the main sweep." | kind=entity | source=probe/scanner/port_scanner.py:L621 | neighbors=[._reprobe_ambiguous()] | lang=en
- "scanner_port_scanner_rationale_648": "Bounded worker-pool scan of every requested port.          A fixed pool of `conc" | kind=entity | source=probe/scanner/port_scanner.py:L648 | neighbors=[.scan_target()] | lang=en
- "scanner_port_scanner_rationale_90": "Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)." | kind=entity | source=probe/scanner/port_scanner.py:L90 | neighbors=[_family_of()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-251.json

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
