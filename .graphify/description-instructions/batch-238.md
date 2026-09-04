# Node Description Batch 239 of 332

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

- "scan_page_cat": "Cat" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L140 | neighbors=[page.tsx] | lang=en
- "scan_page_cats": "CATS" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L139 | neighbors=[page.tsx] | lang=en
- "scan_page_dispatchreceipt": "DispatchReceipt()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L639 | neighbors=[page.tsx] | lang=en
- "scan_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L42 | neighbors=[page.tsx] | lang=en
- "scan_page_enginemanifest": "EngineManifest" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L75 | neighbors=[page.tsx] | lang=en
- "scan_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L185 | neighbors=[page.tsx] | lang=en
- "scan_page_fleetstrip": "FleetStrip()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L209 | neighbors=[page.tsx] | lang=en
- "scan_page_hudframe": "HudFrame()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L194 | neighbors=[page.tsx] | lang=en
- "scan_page_intensity": "Intensity" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L144 | neighbors=[page.tsx] | lang=en
- "scan_page_intensitydial": "IntensityDial()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L410 | neighbors=[page.tsx] | lang=en
- "scan_page_jobpanel": "JobPanel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L465 | neighbors=[page.tsx] | lang=en
- "scan_page_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L50 | neighbors=[page.tsx] | lang=en
- "scan_page_network_va_fallback": "NETWORK_VA_FALLBACK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L100 | neighbors=[page.tsx] | lang=en
- "scan_page_networkvahero": "NetworkVaHero()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L282 | neighbors=[page.tsx] | lang=en
- "scan_page_nva_stages": "NVA_STAGES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L280 | neighbors=[page.tsx] | lang=en
- "scan_page_phases": "PHASES" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L456 | neighbors=[page.tsx] | lang=en
- "scan_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L30 | neighbors=[page.tsx] | lang=en
- "scan_page_profile_badge": "PROFILE_BADGE" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L133 | neighbors=[page.tsx] | lang=en
- "scan_page_rec_st": "REC_ST" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L458 | neighbors=[page.tsx] | lang=en
- "scan_page_risk": "RISK" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L126 | neighbors=[page.tsx] | lang=en
- "scan_page_scannerrun": "ScannerRun" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L63 | neighbors=[page.tsx] | lang=en
- "scan_page_scanpage": "ScanPage()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L684 | neighbors=[page.tsx] | lang=en
- "scan_page_sectionlabel": "SectionLabel()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L174 | neighbors=[page.tsx] | lang=en
- "scan_page_uc_meta": "UC_META" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L110 | neighbors=[page.tsx] | lang=en
- "scan_page_usecase": "UseCase" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L20 | neighbors=[page.tsx] | lang=en
- "scan_page_usecasecard": "UseCaseCard()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L340 | neighbors=[page.tsx] | lang=en
- "scanner_accuracy_gate_rationale_101": "True when this corpus's labels can support an ACCURACY claim." | kind=entity | source=probe/scanner/accuracy_gate.py:L101 | neighbors=[is_independent()] | lang=en
- "scanner_accuracy_gate_rationale_106": "Threshold violations for one scored corpus (empty list = passed)." | kind=entity | source=probe/scanner/accuracy_gate.py:L106 | neighbors=[check_thresholds()] | lang=en
- "scanner_accuracy_gate_rationale_143": "Score every corpus in `directory` and collect threshold violations.      Returns" | kind=entity | source=probe/scanner/accuracy_gate.py:L143 | neighbors=[run_gate()] | lang=en
- "scanner_accuracy_gate_rationale_62": "A corpus is malformed or unlabeled — a gate failure, never a silent pass." | kind=entity | source=probe/scanner/accuracy_gate.py:L62 | neighbors=[CorpusError] | lang=pt
- "scanner_accuracy_gate_rationale_66": "Load and structurally validate one corpus file." | kind=entity | source=probe/scanner/accuracy_gate.py:L66 | neighbors=[load_corpus()] | lang=en
- "scanner_accuracy_gate_rationale_93": "Every *.json corpus in `directory`, sorted by name for stable reports." | kind=entity | source=probe/scanner/accuracy_gate.py:L93 | neighbors=[load_corpora()] | lang=en
- "scanner_accuracy_rationale_125": "Run the findings engine over a labeled corpus and score it.      corpus = {name," | kind=entity | source=probe/scanner/accuracy.py:L125 | neighbors=[evaluate_corpus()] | lang=en
- "scanner_accuracy_rationale_49": "Precision / recall / F1 of produced findings vs a labeled expected set.      Key" | kind=entity | source=probe/scanner/accuracy.py:L49 | neighbors=[score_findings()] | lang=en
- "scanner_accuracy_rationale_80": "(target, port) -> status, from port/syn/mass scan facts (last one wins)." | kind=entity | source=probe/scanner/accuracy.py:L80 | neighbors=[_observed_states()] | lang=en
- "scanner_accuracy_rationale_95": "OPEN precision/recall + overall state accuracy vs a remote-validated     ground" | kind=entity | source=probe/scanner/accuracy.py:L95 | neighbors=[score_port_states()] | lang=pt
- "scanner_adaptive_timeout_adaptivetimeout_init": ".__init__()" | kind=code-symbol | source=probe/scanner/adaptive_timeout.py:L21 | neighbors=[AdaptiveTimeout] | lang=en
- "scanner_adaptive_timeout_rationale_32": "Fold one round-trip sample (seconds) into the estimate. Ignores         missing/" | kind=entity | source=probe/scanner/adaptive_timeout.py:L32 | neighbors=[.observe()] | lang=en
- "scanner_adaptive_timeout_rationale_45": "Current timeout: base until we have a sample, then SRTT + 4*RTTVAR         clamp" | kind=entity | source=probe/scanner/adaptive_timeout.py:L45 | neighbors=[.timeout()] | lang=pt
- "scanner_adaptive_timeout_rationale_55": "Convenience: build an estimator and fold in a sequence of RTT samples." | kind=entity | source=probe/scanner/adaptive_timeout.py:L55 | neighbors=[from_rtts()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-238.json

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
