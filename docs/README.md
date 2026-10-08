# Vedha Documentation

Central docs map. All documentation now lives here — the repo root is clean.

**Project status — what is done, what is open, what needs the owner: [STATUS.md](STATUS.md).**

## Directory structure

| Directory | Holds |
|-----------|-------|
| [`adr/`](adr/) | Architecture Decision Records (numbered, permanent) |
| [`architecture/`](architecture/) | System design, component boundaries, design reviews |
| [`deployment/`](deployment/) | How to run Vedha in an environment |
| [`learning/`](learning/) | Learning plan and personal notes |
| [`operations/`](operations/) | Operational runbooks, troubleshooting |
| [`planning/`](planning/) | Roadmaps, implementation plans, future work |
| [`pm/`](pm/) | Product management — market, personas, roadmap, GTM |
| [`probe/`](probe/) | Probe-specific runbooks and function references |
| [`design/`](design/) | Design docs for a single feature or system (design system, agent version management) |
| [`reports/`](reports/) | Dated reports (bring-up, validation) and [`samples/`](reports/samples/) of scan output |
| [`research/`](research/) | Deep research and strategy memos |
| [`superpowers/`](superpowers/) | Generated specs and plans (tool-managed) |
| [`testing/`](testing/) | Test strategy and manual test plans |
| [`archive/`](archive/) | Historical / stale docs kept for reference |

## Key documents

### Architecture
- [System Architecture](architecture/system-architecture.md) — component boundaries, probe/manager split
- [Architecture Review](architecture/architecture-review.md) — staff-level scalability audit
- [System Design Check](architecture/system-design-check.md) — SWE review (2026-07-15)
- [ADR-0001](adr/0001-manager-detection-pipeline.md) — manager detection pipeline decisions
- [ADR-0002](adr/0002-detection-architecture.md) — detection architecture decisions
- [ADR-0005](adr/0005-windows-agent-delivery.md) — Windows agent delivery: a zip, one command, self-diagnosing; open findings F-1..F-3

### Deployment
- [AWS Deployment](deployment/aws-deployment.md) — EC2 + Docker Compose + Caddy auto-TLS
- [Client Prerequisites](deployment/CLIENT_PREREQUISITES.md) — what a client provides before an engagement

### Operations
- [Branch merge assessment (3 Oct)](planning/2026-10-03-branch-merge-assessment.md) — what is on the integration branch, what is not (Codex branch) and why
- [Hosting the Windows agent on S3: one-command install](operations/WINDOWS_AGENT_HOSTING.md) — set up S3 + CloudFront, publish a release, the customer's one line, troubleshooting
- [Agent distribution runbook](operations/AGENT_DISTRIBUTION.md) — sign + publish agent releases from the build machine, how Fleet → Add agent works, on-prem encrypted bundles
- [Debugging the Agent](operations/DEBUGGING_THE_AGENT.md) — log verbosity, where logs/state are stored per platform, diagnostic subcommands, symptom→fix table, Windows agent
- [Troubleshooting](operations/TROUBLESHOOTING.md) — scanner error codes and operator actions
- [VA Runbook](operations/VA_RUNBOOK.md)

### Probe
- [Sending the Windows agent to a customer](probe/WINDOWS_AGENT_INSTALL.md) — operator guide: build, mint a token, hand over, troubleshoot, what is verified
- [Windows agent reference](probe/WINDOWS_AGENT_REFERENCE.md) — package, files, `agent.env` settings, commands, status states, exit codes
- [Installing the Vedha agent (customer guide)](probe/CUSTOMER_AGENT_INSTALL.md) — the supported path: Fleet → Add agent, one command, proxy/TLS options
- [Agent Install & Run Guide (all OS)](probe/AGENT_INSTALL_GUIDE.md) — step-by-step install for Linux/macOS/Windows with commands
- [Probe Runbook](probe/RUNBOOK.md)
- [Step-by-Step Run Guide](probe/step-by-step-run.md) — network/firewall model + first scan
- [Main Scripts Function Reference](probe/main-scripts-function-run.md)

### Design and reports
- [Agent version management](design/agent-version-management.md) — two version numbers, the CI gate, the update-check API, what is not built
- [Windows agent bring-up report (7 Oct)](reports/2026-10-07-windows-agent-bringup-report.md) — what was built, the 10 defects found, what is proven

### Testing
- [Master Test Plan & Checklist](testing/MASTER_TEST_PLAN.md) — umbrella: every test type (project + platform lens), tools, gates
- [Testing Plan](testing/TESTING_PLAN.md) — probe+manager layered plan, safety gate, new-feature TDD matrix
- [Windows agent: CI and the real-install test](testing/windows-agent-ci-and-e2e.md) — the 22 checks, how to run them, gotchas
- [Probe Testing Guide](testing/probe-testing.md) — two-machine lab (Mac + Windows) e2e procedure

### Planning
- [Windows agent pipeline (7 Oct)](planning/2026-10-07-windows-agent-pipeline.md) — what is parked, in order, with the decisions needed
- [Windows-first agent quick wins (2 Oct)](planning/2026-10-02-windows-agent-quick-wins.md) — status of each quick win
- [Pending Work (Aug 30)](planning/pending-work-aug30.md)
- [Probe Follow-up Plan](planning/probe-followup-plan.md)
- [Remediation AI Plan](planning/remediation-ai-plan.md)
- [AI-Native Thesis](planning/ai-native-thesis.md)
- [Future Optimizations](planning/future-optimizations-thesis.md)

### Research
- [Windows agent: friction points and what other vendors teach (7 Oct)](research/2026-10-07-windows-agent-friction-and-competitors.md)
- [Pipeline Hardening](research/pipeline-hardening.md)
- [Platform Architecture Strategy](research/platform-architecture-strategy.md)

### Product Management
- [Executive Summary](pm/00-executive-summary.md)
- [Market & Competitive Landscape](pm/01-market-and-competitive-landscape.md)
- [Customer Personas](pm/02-customer-personas-and-pain-points.md)
- [USPs & Value Proposition](pm/03-usps-and-value-proposition.md)
- [Product Roadmap](pm/04-product-improvement-roadmap.md)
- [Go-to-Market](pm/05-go-to-market.md)
