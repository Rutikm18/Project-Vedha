# Vedha Documentation

Central docs map. All documentation now lives here — the repo root is clean.

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
| [`reports/samples/`](reports/samples/) | Example scan output reports |
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

### Deployment
- [AWS Deployment](deployment/aws-deployment.md) — EC2 + Docker Compose + Caddy auto-TLS
- [Client Prerequisites](deployment/CLIENT_PREREQUISITES.md) — what a client provides before an engagement

### Operations
- [Troubleshooting](operations/TROUBLESHOOTING.md)
- [VA Runbook](operations/VA_RUNBOOK.md)

### Probe
- [Probe Runbook](probe/RUNBOOK.md)
- [Step-by-Step Run Guide](probe/step-by-step-run.md)
- [Main Scripts Function Reference](probe/main-scripts-function-run.md)

### Testing
- [Testing Plan](testing/TESTING_PLAN.md)
- [Probe Testing Guide](testing/probe-testing.md)

### Planning
- [Pending Work (Aug 30)](planning/pending-work-aug30.md)
- [Probe Follow-up Plan](planning/probe-followup-plan.md)
- [Remediation AI Plan](planning/remediation-ai-plan.md)
- [AI-Native Thesis](planning/ai-native-thesis.md)
- [Future Optimizations](planning/future-optimizations-thesis.md)

### Research
- [Pipeline Hardening](research/pipeline-hardening.md)
- [Platform Architecture Strategy](research/platform-architecture-strategy.md)

### Product Management
- [Executive Summary](pm/00-executive-summary.md)
- [Market & Competitive Landscape](pm/01-market-and-competitive-landscape.md)
- [Customer Personas](pm/02-customer-personas-and-pain-points.md)
- [USPs & Value Proposition](pm/03-usps-and-value-proposition.md)
- [Product Roadmap](pm/04-product-improvement-roadmap.md)
- [Go-to-Market](pm/05-go-to-market.md)
