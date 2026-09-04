# Accuracy corpora

Input for `main_scripts/accuracy_gate.py`, which scores the findings engine and
port-state model against labeled data and fails CI when a change makes the
scanner worse. This closes roadmap item **#4** in
`main_scripts/RESEARCH_IMPROVEMENTS.md`.

Run the gate:

```bash
python -m main_scripts.accuracy_gate probe/tests/fixtures/accuracy_corpus
```

## The two kinds of corpus — do not confuse them

Every corpus MUST declare `provenance`. The gate refuses to score one that does
not, because an unlabeled corpus passes vacuously.

| `provenance` | What it proves | Counts as accuracy evidence |
|---|---|---|
| `self_regression` | Behaviour has not **drifted** since the baseline was taken | **No** |
| `nmap` | Scored against nmap from the same vantage | Yes |
| `manual_remote_validation` | An operator verified the state remotely by hand | Yes |
| `second_vantage` | A second probe acted as the independent validator | Yes |
| `vendor_documented` | The target's own documented exposure | Yes |

A `self_regression` corpus is labeled with **this engine's current output**. If
the engine is wrong today, the corpus enshrines the wrong answer — it can only
catch a later change, never a present defect. The corpora shipped here are all
`self_regression`, so the gate prints a warning saying exactly that.

## Ground-truth discipline

From `accuracy.py`'s own docstring, and it is the single easiest thing to get
wrong: **a port a host is LISTENing on locally is not necessarily OPEN
remotely.** Host firewalls, network ACLs, routing and vantage all intervene.

So ground truth must be the **remote-validated state from the scanner's
vantage** — never a local `ss -ltn` / `netstat` dump. Labeling from a local
listener list miscounts every firewalled-but-listening port as a false negative
and makes the recall number meaningless.

## Building a real ground-truth corpus

Use an independent implementation as the validator, from the same vantage, at
roughly the same time. `nmap` is the reference:

```bash
# 1. Independent validator (same vantage, same port set)
nmap -Pn -sS -p- --reason -oX truth.xml <TARGET>

# 2. This scanner, same ports
python -m main_scripts.port_scanner <TARGET> -A --report-closed -o scan.jsonl
```

Then write a corpus file:

```json
{
  "name": "lab_<target>",
  "provenance": "nmap",
  "validator": "nmap 7.95, same vantage, <UTC timestamp>",
  "facts": [ ... contents of scan.jsonl ... ],
  "ground_truth_states": { "<TARGET>:22": "open", "<TARGET>:23": "closed" },
  "expected_findings": [["RULE-ID", "<TARGET>", 445]]
}
```

`ground_truth_states` keys are `"target:port"`; values use the canonical state
model (`open` / `closed` / `filtered` / `open|filtered` / `unreachable`).

Only put a host you are authorized to scan in a corpus, and keep real customer
addresses out of the repository — use lab ranges.

## Thresholds

Defaults live in `accuracy_gate.DEFAULT_THRESHOLDS` and are overridable per run:

| Threshold | Default | Why |
|---|---|---|
| `min_open_precision` | 0.98 | A phantom OPEN port is the worst single defect — it sends an operator chasing a service that isn't there |
| `min_precision` | 0.95 | False-positive findings destroy trust fastest |
| `min_open_recall` | 0.95 | Missed open ports are missed attack surface |
| `min_recall` | 0.90 | |
| `min_state_accuracy` | 0.95 | |

A dimension with no labels is skipped rather than scored as a perfect 1.0.
