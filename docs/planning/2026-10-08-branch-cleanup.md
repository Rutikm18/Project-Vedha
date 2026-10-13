# Branch cleanup after the `dev` integration (2026-10-08)

`dev` contains every open PR (#2 to #11) plus the unmerged work that was still required.
Each branch below was checked against `dev` (an ancestor of it, or its commits are present
under other SHAs), so deleting it loses nothing.

## 1. Publish main (and dev)

`main` now contains everything in `dev` (all PRs #2 to #12, `cool-cannon`, the laughing-pasteur work). `origin/main` is an ancestor of it, so both pushes are fast-forwards. Local `main` is checked out in a scratch worktree; if git refuses to switch to it, run `git worktree list` and `git worktree remove` the scratch one first.

```bash
git push origin main
git push -u origin dev
```

## 2. Local branches fully contained in dev (60)

Run from a checkout where `dev` is checked out, so `-d` can verify the merge.

```bash
git branch -d 1209_system_ui_backend_level_changes 2809firsttest addcapabilities-fable agents/greeting-introduction backup-before-secret-removal codex/customer-portal-parity cross-os-agent-installer cross-os-vedha-agent-install docs/agent-install-approach docs/aws-ports-install docs/aws-troubleshooting docs/deployment-agent-review docs/probe-run-steps docs/status-refresh feat/agent-install feat/aggressive-enterprise feat/autonomous-offensive-agent feat/complete-pending-work feat/coverage-gated-auto-resolution feat/engagement-detail-uiux feat/findings-grouping-os-copy feat/intel-tags-domain-ai feat/make-admin-creds feat/nvd-vuln-detection-and-ingest-hardening feat/operator-deep-scan feat/per-scan-findings feat/portal-plan-locks feat/portal-poc-entitlements feat/remediation-ai-plans feat/reporting-boardroom-redesign feat/syn-scanner-osfp-adaptive feat/technical-finding-report feat/va-maturity-gaps fix/aggressive-scan-and-queue fix/ai-brain-env-loading fix/ai-provider-error-legibility-and-gemini fix/build-image-race fix/caddy-frontend-health fix/ci-async-plugin fix/install-deps fix/install-neo4j-buildx fix/install-swap-bake fix/probe-already-enrolled-409 fix/probe-ws-ssl fix/report-export fix/review-followups fix/starlette-422-constant fix/wave-e-followups integrate/agent-install-to-main integrate/reports-to-main integration/all-branches integration/all-prs-2026-10-08 manager_pipeline_enhancement security/p0-fixes spike/probe-go test testing/all-features ui-ux-backend-updates0109 updatedvedha2409 worktree-fleet-already-downloaded-cmd
```

## 3. Remote branches fully contained in dev

```bash
git push origin --delete claude/agent-client-distribution claude/deploy-hardening claude/elegant-noether-ggdafj claude/fervent-brahmagupta-o0g44u claude/laughing-pasteur-isijb5 claude/platform-security-settings claude/serene-bardeen-1uqxzq claude/adoring-maxwell-uz71b2 claude/cool-cannon-l598dk integration/all-prs-full codex/expert-ui-ux-enhancements feat/per-scan-findings fix/ai-brain-env-loading fix/starlette-422-constant integration/all-prs reportingwork0510 test
```

Deleting a branch behind an open PR closes that PR. That is intended here: after step 1 their
work is in `dev`, so open one PR from `dev` into `main` instead.

## 4. Obsolete local branches that need a force delete

Their only unique commits are already in `dev` under other SHAs, were judged stale (an older
status rewrite), or are redundant (the migration port that `dev` makes unnecessary).

```bash
git branch -D docs/network-va-usecases docs/status-attack-chain feat/make-prod-heal fix/migrate-port-0055-0058 integrate/all-to-main
```

`docs/network-va-usecases-clean` is checked out in the main working tree with uncommitted
planning docs. Switch to `dev` first, then `git branch -D docs/network-va-usecases-clean`.

## 5. Kept on purpose (your decision)

| Branch | Why |
| --- | --- |
| `origin/codex/customer-portal-engagement-parity` | Not merged, deliberately: based on 9 Sep, 482 commits behind, 87 of its 103 files have newer edits on `main`, and its remediation workspace is already ported. Merging would overwrite newer work. Delete it once you agree. |
| local `main` | Now includes the `0055-0058` migration port plus everything in `dev`. |
