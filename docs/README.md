# Vedha Documentation

Central docs map. Each topic lives in its own directory so guides stay
discoverable instead of piling up in the repo root.

## Directory scheme

| Directory | Holds | Examples |
|-----------|-------|----------|
| [`deployment/`](deployment/) | How to run Vedha in an environment | [AWS deployment](deployment/aws-deployment.md) |
| [`architecture/`](architecture/) | System design, component boundaries, reviews | architecture overview, design reviews |
| [`runbooks/`](runbooks/) | Operational procedures for a running system | probe runbook, VA runbook, troubleshooting |
| [`testing/`](testing/) | Test strategy, manual test plans | test plan, probe testing |
| [`planning/`](planning/) | Roadmaps, implementation plans, learning notes | implementation plan, future optimizations |
| [`superpowers/`](superpowers/) | Generated plans/specs from the superpowers workflow | (tool-managed) |

## Current documents

### Deployment
- [AWS deployment](deployment/aws-deployment.md) — single EC2 + Docker Compose + Caddy auto-TLS.

### Guides
- [Client prerequisites](CLIENT_PREREQUISITES.md) — what a client provides before an engagement.

## Migration note

Several docs still live at the repo root and should move into the scheme above
(via `git mv`, updating any links in `README.md` / `CLAUDE.md`):

| Root file | Target |
|-----------|--------|
| `ARCHITECTURE.md`, `ARCHITECTURE_REVIEW.md`, `SYSTEM_DESIGN_SWE_CHECK.md` | `architecture/` |
| `PROBE_RUNBOOK.md`, `VA_RUNBOOK.md`, `TROUBLESHOOTING.md` | `runbooks/` |
| `TESTING_PLAN.md`, `Probe_testing.md`, `test-probe.md`, `test_probe.md`, `prod_test.md` | `testing/` |
| `IMPLEMENTATION_PLAN.md`, `LEARNING_PLAN.md`, `learning.md`, `thresis_future_optimizations.md` | `planning/` |

`README.md`, `CLAUDE.md`, and `AGENTS.md` stay at the root by convention (tools
and GitHub expect them there).
