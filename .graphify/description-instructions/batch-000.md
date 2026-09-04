# Node Description Batch 1 of 332

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "commit:repo:github.com/Rutikm18/Project-Vedha@d1b4dd3ee73bfd2dd10b7d9b682b5e3cb4d2f7d5": "d1b4dd3 trim frontend to 7 core pages; add use-case library, scope re-validatio…" | kind=Commit | source=git | neighbors=[0510df3 going to build prompt and conne…, adcs.py, asreproast.py, bloodhound.py, findings.py, __init__.py]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@298a9d489c8ecbabc70d474cce518d1295aa66cd": "298a9d4 trim frontend to 7 core pages; add use-case library, scope re-validatio…" | kind=Commit | source=git | neighbors=[0510df3 going to build prompt and conne…, adcs.py, asreproast.py, bloodhound.py, findings.py, __init__.py]
- "models_enums_findingseverity": "FindingSeverity" | kind=code-symbol | source=manager/backend/app/models/enums.py:L47 | neighbors=[enums.py, str, ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, Principals with an enrollment ExtendedR…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@10dfc80b4b96bacfbdc8a5d3116907e88c9e25ab": "10dfc80 Add comprehensive probe testing guide with step-by-step instructions- D…" | kind=Commit | source=git | neighbors=[route.ts, agent.py, cli.py, engine.py, hw_bind.py, __init__.py]
- "findings_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 3c9062a refactor: Update dashboard comp…, 41b692a Update project files, 42f4e28 feat: enhance security operatio…]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@2885afab48ed2cf48cc14de457e9730f9d14b08b": "2885afa Add comprehensive probe testing guide with step-by-step instructions- D…" | kind=Commit | source=git | neighbors=[0557559 scanner: real use-case library,…, route.ts, agent.py, cli.py, engine.py, hw_bind.py]
- "branch:repo:github.com/Rutikm18/Project-Vedha#main": "main" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 0236a60 fix(detection): full EPSS catal…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …]
- "branch:repo:github.com/Rutikm18/Project-Vedha#addcapabilities-fable": "addcapabilities-fable" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 0236a60 fix(detection): full EPSS catal…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …]
- "branch:repo:github.com/Rutikm18/Project-Vedha#ui-ux-backend-updates0109": "ui-ux-backend-updates0109" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 0236a60 fix(detection): full EPSS catal…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/nvd-vuln-detection-and-ingest-hardening": "feat/nvd-vuln-detection-and-ingest-hardening" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 0236a60 fix(detection): full EPSS catal…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …]
- "models_enums_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/backend/app/models/enums.py:L55 | neighbors=[enums.py, str, ADConnectionError, ADError, DependencyMissingError, Shared building blocks for the Active D…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#fix/probe-already-enrolled-409": "fix/probe-already-enrolled-409" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…]
- "models_engagement_engagement": "Engagement" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L12 | neighbors=[engagement.py, Base, TimestampMixin, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, Raises SafetyViolationError if module o…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/complete-pending-work": "feat/complete-pending-work" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@22701eac5f56fcb6c026fcba3f0aee458b7a45e0": "22701ea Add tests for scanner parity and enhance use case resolution- Introduce…" | kind=Commit | source=git | neighbors=[agent.py, engine.py, __init__.py, task_runner.py, use_cases.py, dependencies.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@f4731730b8a44c981c1fe959f2e17f801be64e2a": "f473173 merge: network VA accuracy, KEV exploitability, console parity (addcapa…" | kind=Commit | source=git | neighbors=[6bb51ab feat: add detection-explain end…, 7a637eb feat: network VA accuracy, KEV …, engine.py, explain_plan.py, page.tsx, layout.tsx]
- "reports_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, 6b41065 probe fixed, 7a637eb feat: network VA accuracy, KEV …]
- "commit:repo:github.com/Rutikm18/Project-Vedha@8f6bf49a772d45589953b440df3b81342f019095": "8f6bf49 Refactor code structure and remove redundant sections for improved read…" | kind=Commit | source=git | neighbors=[2c38782 docs: spec CVE-breadth phase — …, agent.py, cli.py, engine.py, task_runner.py, transport.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1fe16c8ae308d129d848d84656ca57d9ac472939": "1fe16c8 stable but some dead code, need to optimize" | kind=Commit | source=git | neighbors=[route.ts, agent.py, cli.py, engine.py, scope_validator.py, task_runner.py]
- "models_finding_finding": "Finding" | kind=code-symbol | source=manager/backend/app/models/finding.py:L13 | neighbors=[finding.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#integration/all-branches": "integration/all-branches" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/engagement-detail-uiux": "feat/engagement-detail-uiux" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#testing/all-features": "testing/all-features" | kind=Branch | source=git | neighbors=[00c6648 feat(settings): editable email/…, 01f4398 feat(probe): IoT survey reaches…, 027f4e4 feat(integrations): per-tenant …, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…]
- "models_asset_asset": "Asset" | kind=code-symbol | source=manager/backend/app/models/asset.py:L12 | neighbors=[asset.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/autonomous-offensive-agent": "feat/autonomous-offensive-agent" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…]
- "scanner_scanner_base": "scanner_base.py" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1 | neighbors=[cli.py, engine.py, explain_plan.py, local_run.py, task_runner.py, 10dfc80 Add comprehensive probe testing…]
- "models_scan_job_scanjob": "ScanJob" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L12 | neighbors=[scan_job.py, Base, TimestampMixin, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[ActivityItem, ADAssessRequest, Neo4jConfig, AgentBootstrapRequest, AgentRefreshRequest, AgentRegisterRequest]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/remediation-ai-plans": "feat/remediation-ai-plans" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/syn-scanner-osfp-adaptive": "feat/syn-scanner-osfp-adaptive" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/user-portal-reskin-scan-request": "feat/user-portal-reskin-scan-request" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@4d0377d8515df5e6d968b7b06a2da2dae5654fbf": "4d0377d Add unit tests for SMB scanner, SYN scanner, and TLS functionality- Imp…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commands_interactive": "interactive.ts" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1 | neighbors=[agent.py, auth.ts, apiFetch(), clearSession(), loadSession(), requireAuth()]
- "engine_tool_runners": "tool-runners.ts" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, bin(), binName()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6e2818f5652b90046de972acedd99b64fc6b97d8": "6e2818f Add support for additional service scans and enhance routing logic- Int…" | kind=Commit | source=git | neighbors=[agent.py, cli.py, engine.py, use_cases.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…]
- "models_service_service": "Service" | kind=code-symbol | source=manager/backend/app/models/service.py:L10 | neighbors=[service.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "agent_agent": "agent.py" | kind=code-symbol | source=probe/agent/agent.py:L1 | neighbors=[AgentDeps, AgentOpts, _bounded_env_int(), _check_anti_debug(), _classify_connection_error(), configure_logging()]
- "branch:repo:github.com/Rutikm18/Project-Vedha#feat/coverage-gated-auto-resolution": "feat/coverage-gated-auto-resolution" | kind=Branch | source=git | neighbors=[01f4398 feat(probe): IoT survey reaches…, 02b6341 feat(active-validation): pure e…, 045c9ae fix(posture): normalize run_at …, 0510df3 going to build prompt and conne…, 08e0594 deployement ready, 0b7bcb8 feat: probe bootstrap key — sel…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@7a637ebe0685305ffefa921a6d3663c60b62878d": "7a637eb feat: network VA accuracy, KEV exploitability, and console parity" | kind=Commit | source=git | neighbors=[engine.py, explain_plan.py, page.tsx, page.tsx, addcapabilities-fable, main]
- "models_enums_scanjobtype": "ScanJobType" | kind=code-symbol | source=manager/backend/app/models/enums.py:L91 | neighbors=[enums.py, str, ScanJob, ADAssessRequest, Neo4jConfig, Active Directory assessment API.  POST …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-000.json

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
