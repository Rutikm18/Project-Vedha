# Agent version management

Status: **built** (version management only) on `claude/fervent-brahmagupta-o0g44u`, not merged.
**Not built:** the automatic download and apply. Date: 2026-10-07.
Related: [ADR-0005](../adr/0005-windows-agent-delivery.md) (D10) · runbook section
[Agent versions and the update check](../operations/AGENT_DISTRIBUTION.md#agent-versions-and-the-update-check) ·
[pipeline](../planning/2026-10-07-windows-agent-pipeline.md).

## 1. The problem

Before this work the manager could not tell which release an agent ran, an agent could not learn
that a newer one existed, and an enrolled agent had no authorized way to download an update.
The owner's goal: when an agent is started, it checks whether a newer agent exists, tells a person,
and (later) updates itself; the manager knows what every agent runs. Scope agreed with the owner:
**version management now; the download and apply later.**

## 2. Two version numbers, on purpose

| Number | Where | Meaning | Who bumps it |
|---|---|---|---|
| Platform release | repo-root `VERSION` | names a release directory on the manager | the commit hook |
| **Agent version** | `probe/agent/version.py` (`AGENT_VERSION`) | the agent's own number | **by hand**, when the agent's code changes |

A manager release that does not touch the agent keeps the same agent version, so it never looks
like an agent update. Today: `2.2.1`. Version `2.2.0` reached a real machine with a defect (a
missing WebSocket module), which is why a fix moved it to `2.2.1`: **once a build has been
installed somewhere, a changed build gets a new number.**

## 3. How the number stays honest (CI)

`.github/workflows/agent-version-gate.yml` runs `probe/tools/check_agent_version.py` on every pull
request. If anything the agent ships (its import closure from `tools/agent_closure.py`, or
`requirements-runtime.txt`) changed against the base branch and `AGENT_VERSION` did not go up,
the pull request fails. Locally: `python probe/tools/check_agent_version.py --base origin/main`.

## 4. What travels where

```
 build machine                         manager                                agent
 -------------                         -------                                -----
 make agent-release  --agent_version-> signed manifest (agent_version)
                                       GET /agent/release (admin: version,
                                       arches, signed?, agent_version)
                                                         <--- heartbeat (HTTP and WebSocket) ---- agent_version
                                       agents.agent_version  (stored per agent; migration 0018)
                                                         <--- POST /agents/update-check -------- {agent_id, agent_version,
                                                                                                  platform, architecture}
                                       update_offer(release, reported) ----------------------->  {update_available, current,
                                                                                                  latest, manager_release, message}
```

- **The release carries the number.** `scripts/agent_release.py` reads `AGENT_VERSION` and writes it
  into the manifest as `agent_version` (optional, so older releases still load). The manager rejects
  a malformed value; the manifest is signed, so an edited value breaks the release.
- **The manager learns what runs.** The agent sends `agent_version` on every heartbeat, over HTTP and
  over the WebSocket, and in each update check. The manager stores it on the agent row
  (`agents.agent_version`, a column that has existed since migration 0018, so there is no migration).
  Fleet's agent list returns it (`GET /agents` -> `agent_version`). A Fleet "update available" badge is
  **not built**.
- **The update check** is `POST /agents/update-check`. It is behind the agent's own credential (listed in
  `agent_jwt_path_allows`; the same ownership check as the heartbeat), so an expired or revoked agent
  is refused before it reaches the handler. Body: `agent_id`, `agent_version` (1-64 chars), `platform`,
  `architecture`. Reply, always a normal 200 and never an error for "nothing to offer":

  | Field | Meaning |
  |---|---|
  | `update_available` | true only when the manager's release states an agent version strictly newer than the reported one |
  | `current` | what the agent reported |
  | `latest` | the manager's agent version (null when there is no release or it states none) |
  | `manager_release` | the platform release the manager serves (null when none) |
  | `message` | a sentence for a person |

  Nothing is downloaded by this route.

## 5. What the agent does (`probe/agent/update_check.py`)

| When | What | Who sees it |
|---|---|---|
| every start | asks the manager | if a newer agent exists **and a person is at the terminal**: "Update now? [y/N]" (30 s timeout, default no). A service or container only logs it |
| every 6 h while running (jittered by 10 %) | asks again | logged once per new version; never prompts |
| every heartbeat | reports `agent_version` | Fleet shows what is really running, even after an upgrade |

Rules built in:

- **Best effort.** A check never raises into the agent and never delays a scan. A manager without the
  route (404/401) or without a release simply yields "nothing to offer".
- **The agent re-validates the reply.** A version that is not strictly newer than its own is ignored, so
  a stale or hostile reply cannot cause a downgrade. A malformed version is ignored, never guessed at.
- **An unattended agent is never blocked on a prompt.**
- **Switches:** `PROBE_UPDATE_CHECK=off`; `PROBE_UPDATE_CHECK_INTERVAL_HOURS` (1-168).
- **No credential refresh** is triggered by a failed check, so a manager that predates the route
  cannot push the agent into re-enrolling.

Answering "yes" today prints the manual step: re-run `install.cmd` (Windows) or the installer
(Linux); both upgrade in place and keep the agent's identity. The single place to add the automatic
download is `request_update` in `update_check.py` (currently a placeholder).

## 6. Compatibility

| Manager | Agent 2.2.x behaviour |
|---|---|
| This branch | full: version recorded, offers returned |
| An older manager (`main` today) | works: the extra `agent_version` field in heartbeats is ignored (the heartbeat model does not forbid extra fields; the WebSocket handler reads keys by name); `/agents/update-check` is not found or refused and the agent treats that as "nothing to offer" |

## 7. Not built: download and apply (the design to follow)

Why it is a separate step: an enrolled agent has no enrolment token left, and the existing download
route (`/agent/image/{arch}`) is authorized by one. Updating also has to survive an update that
breaks the agent. Lessons from other agents are in the
[research memo](../research/2026-10-07-windows-agent-friction-and-competitors.md).

1. **An update download route authenticated by the agent's own credential**, serving only the release
   the manager has decided that agent may have (so the manager, not the agent, chooses the version;
   this is also how channels and a staged rollout come: per-agent or per-group targets, and a pause).
2. **Verify on the agent before running anything**: the manifest signature (Ed25519 against a key
   built into the agent, not fetched), the file's SHA-256, and that the version is newer (anti-rollback).
   Windows PowerShell cannot check Ed25519, so this is the agent's job, in the compiled agent.
3. **Apply with a way back.** Windows will not replace a running executable: a small helper (or the
   installer, run by the agent) stops the task, swaps the folder (the previous one is kept as `.old`,
   as `install.ps1` already does), starts the task, waits for `online`, and restores the old folder
   if the new agent does not report `online` within a deadline.
4. **The Windows package becomes a manager-served artifact** (a `windows-amd64` entry in the signed
   release manifest) and is Authenticode-signed.
5. **Fleet shows it**: the version per agent, an "update available" badge, and the rollout state.

## 8. Tests

`probe/tests/test_update_check.py` (version parsing, strictly-newer, re-validation, prompt rules,
periodic checker), `probe/tests/test_check_agent_version.py` (the CI gate),
`manager/backend/tests/test_agent_update_check.py` (route, offers, auth, storing the version),
`manager/backend/tests/test_agent_release_tool.py` (the manifest field).
