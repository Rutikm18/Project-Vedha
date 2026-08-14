# Sealing the probe (protecting your scanner IP)

## TL;DR — your flow

```bash
# 1) edit your scanners freely
vim main_scripts/port_scanner.py       # main_scripts/ = the source of truth

# 2) run ONE command → a sealed, native-binary image (no source, no bytecode)
./seal-probe.sh                        # or: ./seal-probe.sh --hostid <HOST_ID>

# 3) issue a license for a customer and ship the image
python tools/issue_license.py issue --hostid <id> --customer "Acme" --days 365
```

## What "sealed" means here (and why it beats encrypting .py)

The sealed build (`Dockerfile.sealed`, driven by `seal-probe.sh`) compiles the
**entire probe** — scanners, workflow engine, agent — from Python → C → **native
machine code** with Nuitka. The runtime image is a single binary on `debian-slim`:
**no Python interpreter, no `.py`, no `.pyc`.**

> You asked about "encrypt the scripts + a custom decoder." Be aware that is
> **strictly weaker** than what you already have. An encrypted `.py` must be
> decrypted back into source to run, so an attacker with the box just dumps it
> from memory (or hooks the loader). A Nuitka binary has **no source to dump** —
> the Python is gone. So we mature the native-compile path instead of building a
> weaker decoder.

Three layers stack on top of the binary:

| Layer | File | What it stops |
|-------|------|---------------|
| **Native compile** (Nuitka) | `Dockerfile.sealed` | Reading/reusing your source or bytecode |
| **Vendor-signed license** (Ed25519) | `agent/license.py` + `tools/issue_license.py` | Running the probe without a license **you** minted |
| **Host binding** | `agent/hw_bind.py` | Copying the probe to a different machine |
| **mTLS** (optional) | build-arg certs | An unauthorized probe talking to your Manager |

**Only you can mint a license.** The vendor **private** key
(`tools/vendor_private.key`, gitignored) never leaves your machine; the probe
embeds only the **public** key and can *verify* a license but never *forge* one.
A host-locked license won't validate on any other machine.

## The honest threat model (set expectations)

Code that runs on a machine the adversary controls can, with enough effort, be
reverse-engineered — this is the same reason DRM is imperfect. Sealing **raises
the bar enormously** (from "unzip and read the .py" to "reverse a stripped,
LTO'd, docstring-free native binary and defeat a signed host-locked license") but
it is **deter, not prevent.** Two honest caveats:

- Free Nuitka still leaves **string/number constants** (port catalogs, rule text)
  recoverable. Nuitka **Commercial** encrypts constants + adds anti-debugging if
  those are sensitive.
- The single biggest protection is **not shipping the crown jewels at all.** Your
  most valuable logic — CVE matching, correlation, risk scoring, detection rules —
  already runs **Manager-side** (`manager/detection_engine`, `app/detection`). The
  probe's scanners (TCP connect, banner grab) are comparatively generic. So the IP
  actually exposed on the probe is modest; keep it that way, and the seal protects
  the small remainder.

## Key management (do this once, guard it forever)

```bash
python tools/issue_license.py keygen     # writes tools/vendor_private.key (MASTER SECRET)
```
- `tools/vendor_private.key` is your **master secret** — it's gitignored; **back
  it up privately** (a password manager / offline store). Anyone who has it can
  license probes as you. Losing it means you can never issue new licenses for the
  currently-built binaries (rebuild with a new key).
- `seal-probe.sh` bakes the matching **public** key into every sealed binary
  automatically (via `issue_license.py pubkey`).

## What goes in git

Decide based on who can see this repo:

- **Repo is private (you/your team only), customers get only the built image** —
  the normal case. Keep `main_scripts/` + `scanner/` in git as usual; the
  protection is 100% in the **sealed image** you ship. Nothing else to do.
- **Repo is shared with untrusted parties** — then also keep the plaintext
  scanners out of it: move `main_scripts/` to a **private** repo/submodule (don't
  merely `.gitignore` a source-of-truth you have no other copy of — that risks
  losing it). `seal-probe.sh` still consumes `main_scripts/` locally to build.

## Running a sealed probe

```bash
docker run --rm vedha-probe:sealed hostid          # → the machine's Host ID
# issue a license for that host, save it as license.token, then:
docker run -d --name vedha-probe \
  -e PLATFORM_URL=https://manager.example.com \
  -e PROBE_LICENSE_FILE=/lic/license.token -e LICENSE_ENFORCED=true \
  -v "$PWD/license.token:/lic/license.token:ro" \
  -v vedha-probe-state:/var/lib/vedha-probe \
  vedha-probe:sealed run
```

Dev builds skip the gate with `LICENSE_ENFORCED=false` (use the plain
`Dockerfile`, not the sealed one).
