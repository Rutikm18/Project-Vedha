# One command to install the agent: which operating systems, and how to host it

Goal: on any machine, the user types **one command**. That command downloads **one small installer script**
from your manager; the script then downloads the agent itself (with the one-time token), checks it, installs it
and connects it. The user never downloads, unzips or copies anything by hand.

Written 11 Oct 2026 from the code, and rehearsed locally with the real release tool, the real manager
distribution router and the real installer script. What was and was not run is in section 8.

---

## 1. Which operating systems the agent is built for

| OS | What you ship | How it runs | Status |
|---|---|---|---|
| **Windows 10 / Server 2016 or newer, 64-bit (x64)** | a compiled package `vedha-agent-win.zip` (no Python needed) | Scheduled Task `VedhaAgent`, SYSTEM, starts at boot | built and installable; **needs the steps in section 3** |
| **Linux, x86-64 and ARM64** | a Docker image per CPU, plus `install.sh` | one container, non-root, read-only, `--cap-drop ALL`, restarts by itself | built by `make agent-release`; needs Docker on the host |
| **macOS** | no package | `install.sh` can run the agent in **Docker Desktop**, or from source with Python 3.8+ (`install.sh connect --manager …`). Unit tests run on macOS in CI | works, but not a packaged product |
| **32-bit Windows, Windows before 10 / Server 2016** | nothing | the installer refuses them (it checks for 64-bit and build 10.0.14393 or newer) | not supported |
| **Windows on ARM64** | nothing built for it | the installer's checks would pass it; whether the x64 program runs there under emulation has not been tried | unknown |
| **Android, iOS, network appliances** | nothing | they are scan *targets* (the ADB and iOS-lockdown checks), not places the agent runs | not agents |

What each OS can scan with:

| | Connect scan (any port) | SYN scan (fast, stealthy) | OS fingerprint by ICMP/TTL | Layer-2 / ARP discovery |
|---|---|---|---|---|
| Windows | yes (closed ports are fast since agent 2.2.6) | no | no (needs Npcap) | no |
| Linux, **native** (root or `CAP_NET_RAW`) | yes | **yes** | yes | yes |
| Linux, **Docker** (what `install.sh` installs) | yes | **no** (`SYN scan: no` in its log) | no | no (bridge network, behind NAT) |
| macOS | yes | no (raw sockets on macOS cannot receive TCP, per the scanner's own check) | not checked | not checked |

So "run it on Linux" does not by itself mean SYN scanning: the shipped Docker agent cannot do it.

---

## 2. What the user will type (the goal)

| User's machine | The one command (Fleet → Add agent prints it with the real address and token) |
|---|---|
| Windows, PowerShell as Administrator | `powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm 'https://api.vedhasec.com/agent/install.ps1'))) -Manager 'https://api.vedhasec.com' -Token 'vet_…'"` |
| Windows, Command Prompt (it asks for admin itself) | `curl.exe --proto =https --tlsv1.2 -fsSL "https://api.vedhasec.com/agent/install.cmd" -o "%TEMP%\vedha-install.cmd" && "%TEMP%\vedha-install.cmd" "https://api.vedhasec.com" "vet_…"` |
| Linux | `curl --proto '=https' --tlsv1.2 -fsSL https://api.vedhasec.com/agent/install.sh \| sudo sh -s -- --manager https://api.vedhasec.com --token vet_…` |

Copy it from Fleet; do not retype it. **The address in it must be the API's** (`api.…`), not the dashboard's
(`app.…`): only the API serves `/agent/…`. A leftover placeholder such as `MANAGER` is a common mistake.

How it works, so you know what you are hosting:

```
user's machine                                        your manager (api.vedhasec.com)
--------------                                        ------------------------------
curl install.ps1 | install.cmd | install.sh   --->    GET /agent/install.*       public, ~20 KB script
script fetches the signed manifest            --->    GET /agent/manifest.json (+ .sig, .p256.sig)   public
script checks the signature with the key baked into the script it just downloaded
script downloads the package with the token   --->    GET /agent/package/windows   needs the vet_ token
script checks size + SHA-256 against the signed manifest, then installs
```

Nothing is installed if any check fails. Nothing on the manager is secret except the **private** signing keys, which
never leave your build machine.

---

## 3. Hosting it, step by step (Windows first: it works today without Docker)

The manager already serves `/agent/install.*`; it only needs a **signed release** in its release folder. A release
that contains only the Windows package is valid (`images: []`), so you do not need to build Linux images.

### Step 1: create the signing keys (once, on your build machine, not on the server)

```bash
make agent-keygen          # Ed25519, for Linux installs  -> prints AGENT_RELEASE_PUBLIC_KEY=…
make agent-keygen-p256     # P-256, for Windows installs  -> prints AGENT_RELEASE_P256_PUBLIC_KEY=…
```

They are written to `~/.vedha/` (mode 600). Back both private files up offline: anyone holding one can sign agents
your customers will trust. Neither command overwrites an existing key. Copy the two printed public values.
(The tool needs Python with the `cryptography` package; the backend's virtualenv has it.)

### Step 2: tell the manager the public keys (once)

On the manager host, in its `.env`:

```
AGENT_RELEASE_PUBLIC_KEY=<the Ed25519 value>
AGENT_RELEASE_P256_PUBLIC_KEY=<the P-256 value>
AGENT_RELEASE_REQUIRE_SIGNATURE=true
MANAGER_PUBLIC_URL=https://api.vedhasec.com
```

Then recreate the API container so it reads them: `docker compose up -d api` (or `make full`). In production the
manager refuses to serve a release that is unsigned or does not verify against these keys.

### Step 3: get the Windows package

You need `vedha-agent-win.zip` **and** the `vedha-agent-win.release.json` that was written next to it. Keep the two
files together; the next step reads the second one.

* **Quickest, no build:** the stored build from the last green run (agent **2.2.3**):
  https://github.com/Rutikm18/Project-Vedha/actions/runs/37739768094 → *Artifacts* → `vedha-agent-windows`.
  It lacks every change after 2.2.3 (see the handbook, section 5).
* **Build your own** on a Windows machine with Python 3.10 to 3.12 (the first compile is slow, 15 to 35 minutes):
  ```powershell
  git clone https://github.com/Rutikm18/Project-Vedha.git ; cd Project-Vedha\probe\windows
  powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1
  powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Release
  ```
  `-Release` leaves the manager address out of the package, because the command passes it at install time.
  The result is `dist\vedha-agent-win.zip` and `dist\vedha-agent-win.release.json`. Copy both to your build
  machine.

### Step 4: build and sign the release (Windows only, no Docker)

On the build machine, in the repository root:

```bash
make agent-release AGENT_ARCH= WINDOWS_ZIP=/path/to/vedha-agent-win.zip
```

(`AGENT_ARCH=` with nothing after it means "no Linux images". The result is `dist/agent-release/<VERSION>/`.)

* The tool reads the agent version **from the package's own `.release.json`**, so the manifest names the agent that
  is really in the zip. If the zip does not match its record it refuses. Without a `.release.json` it falls back to
  the version of the checkout you run it from and prints a warning; then make sure the zip was built from that
  checkout.
* A release version is **immutable**: building the same `VERSION` twice fails with "already exists". For a second
  release either bump the `VERSION` file or pass `--version`, for example:
  `python3 scripts/agent_release.py build --key ~/.vedha/agent-release-key.pem --arch "" --p256-key ~/.vedha/agent-release-p256-key.pem --windows-zip /path/vedha-agent-win.zip --version 1.0.404`
* For Linux as well, leave `AGENT_ARCH` at its default (`amd64,arm64`); that builds Docker images, so it needs
  Docker and takes much longer.

### Step 5: verify it before you publish it

```bash
make agent-verify PUB=<AGENT_RELEASE_PUBLIC_KEY> P256_PUB=<AGENT_RELEASE_P256_PUBLIC_KEY>
```

Expected: `OK: release 1.0.403 (windows/amd64) is signed by key … and intact`.

### Step 6: publish it to the manager

```bash
make agent-publish TO=ubuntu@<manager-host>:/opt/Project-Vedha/manager/agent-releases
```

The folder must be the one the API mounts read-only at `/var/lib/vedha/agent-releases`; on the manager host run
`docker compose config | grep agent-releases` to see it (default `./agent-releases` beside the compose file).
The manager notices the new version on its next request; no restart is needed for this step.

### Step 7: check it from outside

```bash
curl -sI https://api.vedhasec.com/agent/install.ps1 | grep -i "^HTTP\|x-vedha-release"
curl -s  https://api.vedhasec.com/agent/manifest.json | head -20      # "images": [] and a "packages" entry
curl -s -o /dev/null -w "%{http_code}\n" https://api.vedhasec.com/agent/package/windows     # 401: needs a token, as designed
```

Then in the console: **Fleet → Add agent** now offers a **Windows** tab (it appears only when a release with a
Windows package is published and signed). If it does not, see section 7.

### Step 8: give one user their command

1. Fleet → Add agent → pick the engagement → **Generate**. Choose **Windows**, copy the PowerShell or Command Prompt
   line. It already contains the manager address and the token.
2. Send it **by a different channel** from the rest of the engagement details (phone or chat), with this note: run it
   in an Administrator PowerShell, or in Command Prompt (which asks for admin by itself).
3. Watch Fleet: the agent appears when it connects. To confirm on the machine:
   `"C:\Program Files\Vedha Agent\vedha-agent.exe" version` and `status`.

For many machines, remember the enrolment rules: one token installs one agent, and an engagement holds one agent
([handbook, section 5](WINDOWS_AGENT_MANAGEMENT.md#putting-the-agent-on-other-computers)). The pairing-code route
(run the installer with no token and approve it in Fleet) avoids creating a token per machine.

### Doing steps 1 to 6 from a Windows PC only (no `make`, no Linux)

`make` is not needed: the Makefile only calls `scripts/agent_release.py`, which is plain Python. You need, on the
Windows PC: Python 3.10 to 3.12 (python.org, tick "Add to PATH"), `pip install cryptography`, Git, and the
**OpenSSH Client** (Settings, Apps, Optional features) for the publish step. Run in PowerShell, in the repository root:

```powershell
$k = "$env:USERPROFILE\.vedha"
# Step 1: both keys. Prints AGENT_RELEASE_PUBLIC_KEY=... and AGENT_RELEASE_P256_PUBLIC_KEY=... (copy them)
python scripts\agent_release.py keygen --out "$k\agent-release-key.pem" --p256-out "$k\agent-release-p256-key.pem"

# Steps 3-4: package built by probe\windows\package-zip.ps1 -Release (keep the .release.json beside the zip)
python scripts\agent_release.py build --key "$k\agent-release-key.pem" --arch "" `
  --p256-key "$k\agent-release-p256-key.pem" --windows-zip "C:\path\vedha-agent-win.zip"

# Step 5
python scripts\agent_release.py verify dist\agent-release --public-key "<ED25519 value>" --p256-public-key "<P-256 value>"

# Step 6: no rsync on Windows, so the tool uses ssh + scp (it copies the version first, then switches CURRENT)
python scripts\agent_release.py publish dist\agent-release --to ubuntu@<manager-host>:/opt/Project-Vedha/manager/agent-releases
```

Step 2 (the manager's `.env`) is done on the manager host, over SSH. Notes: Windows does not enforce the `600` mode the
tool asks for, so keep the key files in your own profile folder (not a shared or synced one) and back them up offline;
`publish` refuses to overwrite a version that already exists on the manager. Rehearsed on Linux only (key creation,
build, local publish, and the ssh/scp command sequence under test with the commands faked); **not run on Windows**.

---

## 4. Updating later

Build a new package (step 3), a new release (step 4, a new `VERSION`), verify and publish it (steps 5 and 6). Then on
each machine run the same Fleet command again with a fresh token, or `install.cmd -Repair` from the new package. The
installer compares versions, keeps the agent's identity, settings and saved scan results, removes the old program
files, and refuses an older package unless you add `-AllowDowngrade`
([handbook, section 5](WINDOWS_AGENT_MANAGEMENT.md#5-update-to-a-newer-agent)). Agents do not update themselves.

---

## 5. Linux and macOS

* **Linux (one curl):** needs the Docker images in the release: `make agent-release` with the default `AGENT_ARCH`
  (builds amd64 and arm64 on the build machine, which needs Docker), then steps 5 to 8 as above. The user runs the
  Linux line from section 2. The host needs Docker. Details and the signing model:
  [AGENT_DISTRIBUTION](AGENT_DISTRIBUTION.md), [SHARING_THE_AGENT](SHARING_THE_AGENT.md).
* **Both in one release:** `make agent-release WINDOWS_ZIP=/path/vedha-agent-win.zip` builds the Linux images and the
  Windows package into the same release, so one manager serves all three commands.
* **macOS:** no packaged one-liner. Use the Linux command on a Mac with Docker Desktop (it scans from behind
  Docker's NAT), or run from source: `sh install.sh connect --manager https://api.vedhasec.com --token vet_…`.
* **GitHub Releases instead of building by hand:** pushing a tag `agent-v<VERSION>` makes the `agent-release`
  workflow build, sign and publish a release; `make agent-pull REPO=Rutikm18/Project-Vedha TO=…` on the manager then
  installs it. **That workflow has never run, and GitHub Actions is currently blocked by billing**, so the manual
  steps above are the route that works today.

---

## 6. If you do not want to use the manager at all

`probe/windows/hosting/` holds a Windows-only alternative: the package goes to S3 behind CloudFront and the user runs a
`get.ps1` command that pins the version and the package's SHA-256
([WINDOWS_AGENT_HOSTING](WINDOWS_AGENT_HOSTING.md)). It also gives "one command, one script", but it needs an AWS
account, has not been deployed, and does not use signed releases or Fleet's update information. The manager route
above is the recommended one.

---

## 7. When it does not work

| You see | Cause | Fix |
|---|---|---|
| `irm : The remote name could not be resolved` | a placeholder (`MANAGER`) or a wrong host in the command | copy the command from Fleet; use the API host (`api.…`) |
| The URL returns the dashboard's HTML page | you used the dashboard host (`app.…`) | use the API host |
| Fleet has no **Windows** tab; `install.ps1` returns a script that prints "not available on this manager right now" | no release is published, or its Windows part is withheld | `curl -s https://api.…/agent/manifest.json` (404/503 = nothing published). With a release present: `AGENT_RELEASE_P256_PUBLIC_KEY` missing or wrong in `.env`, or the API was not recreated after editing it. Operators see the reason in Fleet → Add agent |
| `manifest signature does not verify` | the keys in `.env` are not the pair that signed this release | use the public keys printed for the private keys you signed with |
| `already exists - releases are immutable; bump VERSION` | that release version was built already | bump `VERSION` or pass `--version` |
| `… does not match its … .release.json` | the zip was changed, or you paired the zip with another build's record | copy the two files from the same build |
| Package download answers `401` | token missing, used, expired or revoked | make a new token in Fleet |
| Package download answers `429` | more than 20 downloads a minute from one address | wait a minute |
| The window closes at once / the command is blocked | endpoint protection dislikes "download and run" | give them the inspect-first form: download the script with `curl.exe -o`, read it, run it; or send the zip |

---

## 8. What was and was not run

**Run on 11 Oct 2026 (a rehearsal on Linux, with throw-away keys and a stand-in zip):**
a Windows-only release built with the real tool (`--arch ""`), verified by the real verifier, loaded by the real
manager code, and served by the real `agent_distribution` router over a socket. Results: `install.ps1`,
`install.cmd`, `manifest.json`, `manifest.json.sig`, `manifest.json.p256.sig` and `install.sh` answered 200 without a
login; the package answered 401 without a token and 200 with one, byte-identical to the file that was signed (SHA-256
matched the manifest); the served `install.ps1` carried the release's P-256 key and version; and the real
`install.ps1` run in PowerShell fetched the manifest from that server. The new package-record check has 5 tests; 4 of
them fail without the change (the fifth guards a case that must keep working); the existing 205 release and
distribution tests still pass.

**Not run:**
* The installer's **P-256 signature check and everything after it**, because it uses Windows cryptography (CNG) that
  PowerShell on Linux does not have. The code is exercised by the `windows-verify` job in `agent-release.yml`,
  which cannot run while GitHub Actions is blocked. Do step 8 once on a clean Windows VM with a test token.
* A real install from a manager-served release on Windows; reboot persistence; the Fleet **Windows** tab in a browser.
* Linux image builds and the Linux one-liner (they need Docker; the logic is covered by existing tests).
* An endpoint-protection product's reaction to the in-memory command.
