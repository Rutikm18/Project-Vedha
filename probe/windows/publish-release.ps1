<#
  Vedha - build, sign and publish the Windows agent with ONE command.   RUN THIS ON A WINDOWS PC (yours).

  After it finishes, any Windows machine installs the agent with one command copied from
  Fleet -> Add agent -> Windows. This script is the "vendor side" of that: it does everything
  that used to be steps 1 to 6 by hand.

  Usage (PowerShell, from the repository root or from probe\windows):

    powershell -ExecutionPolicy Bypass -File probe\windows\publish-release.ps1 `
        -Server ubuntu@YOUR_SERVER -ManagerUrl https://api.vedhasec.com -ConfigureManager

  What it does, in order (each step stops the script if it fails):
    1  checks this PC (Windows, Python 3.10-3.12, ssh/scp) and prepares the build environment
    2  creates the release signing keys the first time (kept in %USERPROFILE%\.vedha; back them up)
    3  builds the compiled Windows agent                      (15-35 minutes the first time)
    4  packages it for the manager (no address baked in: the Fleet command supplies it)
    5  builds and signs the release, then verifies the signature it just made
    6  uploads it to the manager server (ssh + scp)            [needs -Server]
    7  with -ConfigureManager: puts the two PUBLIC keys in the manager's .env (a dated backup is kept)
       and restarts the api container                         [needs -Server and -ManagerUrl]
    8  asks the manager for its manifest and confirms the Windows package is being served

  Without -Server it stops after step 5 and tells you what is left. -DryRun prints the plan and
  runs nothing. -SkipBuild reuses the agent already built in probe\windows\dist\vedha-agent.

  A release version can be published once. To publish a newer one, change the VERSION file or
  pass -Version 1.0.404 (the agent's own version comes from the package, not from this).

  ASCII only, on purpose: Windows PowerShell 5.1 reads a BOM-less file in the ANSI code page.
#>
[CmdletBinding()]
param(
  [string]$Server = '',                 # user@host of the manager server (ssh)
  [string]$ManagerUrl = '',             # https://api.example.com  (MANAGER_PUBLIC_URL, and the final check)
  [string]$RemoteReleaseDir = '/opt/Project-Vedha/manager/agent-releases',
  [string]$RemoteComposeDir = '',       # folder with docker-compose.yml and .env (default: the release folder's parent)
  [string]$KeyDir = '',                 # default %USERPROFILE%\.vedha
  [string]$Version = '',                # default: the VERSION file
  [switch]$ConfigureManager,            # edit the manager's .env and restart the api (opt in)
  [switch]$SkipBuild,
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Pure helpers (no side effects; unit-tested by tests\Test-PublishRelease.ps1)
# ---------------------------------------------------------------------------

function Test-VedhaServerSpec {
  # user@host or host; letters, digits, dots, dashes, underscores only (it goes to ssh and scp).
  param([string]$Value)
  return [bool]($Value -match '^([A-Za-z0-9._-]+@)?[A-Za-z0-9.-]+$')
}

function Test-VedhaRemotePath {
  # An absolute POSIX path of safe characters (it is placed inside single quotes in a shell script).
  param([string]$Value)
  return [bool]($Value -match '^/[A-Za-z0-9_./-]+$') -and ($Value -notmatch '\.\.')
}

function Test-VedhaHttpsUrl {
  param([string]$Value)
  return [bool]($Value -match '^https://[A-Za-z0-9.-]+(:[0-9]{1,5})?/?$')
}

function Test-VedhaKeyLine {
  # NAME=base64 (the public keys; base64 characters only, so single quoting is safe).
  param([string]$Value)
  return [bool]($Value -match '^AGENT_RELEASE_(P256_)?PUBLIC_KEY=[A-Za-z0-9+/=]{20,}$')
}

function Get-VedhaParentPath {
  param([string]$Path)
  $trim = $Path.TrimEnd('/')
  $i = $trim.LastIndexOf('/')
  if ($i -le 0) { return '/' }
  return $trim.Substring(0, $i)
}

function New-VedhaRemoteConfigScript {
  # The POSIX shell script that sets the release keys in the manager's .env and restarts the api.
  # Idempotent: it removes the old copies of these settings first, keeps a dated backup, and
  # rewrites .env in place so its owner and permissions stay as they were. umask 077 makes the
  # temporary copy and the backup private to the user: .env holds every secret of the manager, and
  # a default umask would have left both world-readable.
  param([string]$ComposeDir, [string[]]$Lines)
  if (-not (Test-VedhaRemotePath $ComposeDir)) { throw "Not a safe folder path on the server: '$ComposeDir'" }
  foreach ($l in $Lines) {
    if (-not ((Test-VedhaKeyLine $l) -or ($l -match '^AGENT_RELEASE_REQUIRE_SIGNATURE=true$') -or ($l -match '^MANAGER_PUBLIC_URL=https://[A-Za-z0-9.-]+(:[0-9]{1,5})?$'))) {
      throw "Refusing to write an unexpected line to the manager's .env: '$l'"
    }
  }
  $quoted = ($Lines | ForEach-Object { "'" + $_ + "'" }) -join ' '
  $sh = @(
    'set -eu',
    'umask 077',            # .env holds the manager's secrets: nothing this script writes may be readable by others
    "cd '$ComposeDir'",
    'test -f .env || { echo ".env not found in $(pwd)" >&2; exit 1; }',
    'cp -p .env ".env.bak.$(date +%Y%m%d%H%M%S)"',
    "grep -v -E '^(AGENT_RELEASE_PUBLIC_KEY|AGENT_RELEASE_P256_PUBLIC_KEY|AGENT_RELEASE_REQUIRE_SIGNATURE|MANAGER_PUBLIC_URL)=' .env > .env.new || true",
    "printf '%s\n' $quoted >> .env.new",
    'cat .env.new > .env',
    'rm -f .env.new',
    'echo "[manager] .env updated (backup kept as .env.bak.*)"',
    'docker compose up -d api',
    'echo "[manager] api restarted"'
  ) -join "`n"
  return $sh + "`n"
}

function Get-VedhaPlan {
  # The ordered list of steps for the given options (also what -DryRun prints).
  param([bool]$HasServer, [bool]$Configure, [bool]$HasUrl, [bool]$Skip)
  $steps = @('check this PC and prepare the build environment', 'create the signing keys if they do not exist yet')
  if ($Skip) { $steps += 'reuse the agent already built (-SkipBuild)' } else { $steps += 'build the compiled Windows agent (15-35 minutes the first time)' }
  $steps += 'package it for the manager'
  $steps += 'build and sign the release, then verify it'
  if ($HasServer) { $steps += 'upload the release to the manager server' }
  if ($HasServer -and $Configure) { $steps += "set the public keys in the manager's .env and restart the api" }
  if ($HasServer -and $HasUrl) { $steps += 'ask the manager for its manifest and confirm it serves the Windows package' }
  return $steps
}

# ---------------------------------------------------------------------------
# Doing the work
# ---------------------------------------------------------------------------

function Write-Step { param([string]$N, [string]$Text) Write-Host ''; Write-Host "[$N] $Text" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Text) Write-Host "    OK  $Text" -ForegroundColor Green }
function Write-Note { param([string]$Text) Write-Host "    ... $Text" }

function Invoke-Native {
  # Run a program; stop the whole script when it fails.
  param([string]$File, [string[]]$Arguments, [string]$What)
  & $File @Arguments
  if ($LASTEXITCODE -ne 0) { throw "$What failed (exit code $LASTEXITCODE)." }
}

function Invoke-Main {
  $winDir = $PSScriptRoot
  $repo = [System.IO.Path]::GetFullPath((Join-Path $winDir '..\..'))
  if (-not $Version) {
    $vf = Join-Path $repo 'VERSION'
    if (Test-Path -LiteralPath $vf) { $Version = (Get-Content -LiteralPath $vf -TotalCount 1).Trim() }
  }
  if ($Version -notmatch '^[0-9A-Za-z][0-9A-Za-z._-]{0,63}$') { throw "Release version '$Version' is not valid (use -Version 1.0.404)." }

  # ---- arguments ----
  if ($Server) {
    if (-not (Test-VedhaServerSpec $Server)) { throw "-Server must look like ubuntu@203.0.113.10 (got '$Server')." }
    if (-not (Test-VedhaRemotePath $RemoteReleaseDir)) { throw "-RemoteReleaseDir must be an absolute folder path on the server (got '$RemoteReleaseDir')." }
  }
  if ($ManagerUrl) {
    if (-not (Test-VedhaHttpsUrl $ManagerUrl)) { throw "-ManagerUrl must look like https://api.example.com (got '$ManagerUrl')." }
    $ManagerUrl = $ManagerUrl.TrimEnd('/')
  }
  if ($ConfigureManager -and -not ($Server -and $ManagerUrl)) { throw '-ConfigureManager needs both -Server and -ManagerUrl.' }
  if (-not $RemoteComposeDir -and $Server) { $RemoteComposeDir = Get-VedhaParentPath $RemoteReleaseDir }

  $plan = Get-VedhaPlan -HasServer ([bool]$Server) -Configure ([bool]$ConfigureManager) -HasUrl ([bool]$ManagerUrl) -Skip ([bool]$SkipBuild)
  Write-Host "Vedha release $Version - plan:" -ForegroundColor Cyan
  $i = 0; foreach ($s in $plan) { $i++; Write-Host ("  {0}. {1}" -f $i, $s) }
  if ($DryRun) { Write-Host ''; Write-Host 'Dry run: nothing was done.'; return 0 }

  # ---- 1. this PC ----
  Write-Step '1' 'Checking this PC'
  if ($env:OS -ne 'Windows_NT') { throw 'Run this on Windows: the agent is compiled for Windows.' }
  if (-not $KeyDir) { $KeyDir = Join-Path $env:USERPROFILE '.vedha' }
  $venv = Join-Path $winDir '.venv-win'
  $py = Join-Path $venv 'Scripts\python.exe'
  if (-not (Test-Path -LiteralPath $py)) {
    $sys = Get-Command python -ErrorAction SilentlyContinue
    if (-not $sys) { throw 'Python was not found. Install Python 3.10 to 3.12 from python.org (tick "Add python.exe to PATH") and run this again.' }
    $v = (& python -c 'import sys; print("%d.%d" % sys.version_info[:2])').Trim()
    if ($v -notmatch '^3\.(10|11|12)$') { throw "Python $v found; the Windows build needs 3.10, 3.11 or 3.12." }
    Write-Note 'creating the build environment (first time only)'
    Invoke-Native 'python' @('-m', 'venv', $venv) 'Creating the build environment'
  }
  Invoke-Native $py @('-m', 'pip', 'install', '--quiet', '--upgrade', 'pip', 'cryptography') 'Installing the signing library'
  Write-Ok 'Python and the signing library are ready'
  if ($Server) {
    foreach ($t in 'ssh', 'scp') { if (-not (Get-Command $t -ErrorAction SilentlyContinue)) { throw "$t was not found. Install it: Settings > Apps > Optional features > OpenSSH Client." } }
    Write-Note "checking that ssh works to $Server (it may ask for your password or key passphrase)"
    Invoke-Native 'ssh' @('-o', 'ConnectTimeout=15', $Server, 'echo vedha-ssh-ok') "ssh to $Server"
    Write-Ok "ssh to $Server works"
  }

  # ---- 2. keys ----
  Write-Step '2' 'Signing keys'
  $edKey = Join-Path $KeyDir 'agent-release-key.pem'
  $p256Key = Join-Path $KeyDir 'agent-release-p256-key.pem'
  $tool = Join-Path $repo 'scripts\agent_release.py'
  New-Item -ItemType Directory -Force -Path $KeyDir | Out-Null
  $missing = @()
  if (-not (Test-Path -LiteralPath $edKey)) { $missing += @('--out', $edKey) }
  if (-not (Test-Path -LiteralPath $p256Key)) { $missing += @('--p256-out', $p256Key) }
  if ($missing.Count -gt 0) {
    Invoke-Native $py (@($tool, 'keygen') + $missing) 'Creating the signing keys'
    Write-Host ''
    Write-Host "    IMPORTANT: copy the folder $KeyDir to a USB stick or password manager NOW." -ForegroundColor Yellow
    Write-Host '    Anyone holding those two files can sign agents your customers will trust, and if you' -ForegroundColor Yellow
    Write-Host '    lose them you cannot publish updates that existing installs accept.' -ForegroundColor Yellow
  } else {
    Write-Ok "using the keys in $KeyDir"
  }
  $pub = @(& $py $tool 'pubkey' '--key' $edKey '--p256-key' $p256Key)
  if ($LASTEXITCODE -ne 0 -or $pub.Count -ne 2) { throw 'Could not read the public keys.' }
  $pub = @($pub | ForEach-Object { "$_".Trim() })
  foreach ($l in $pub) { if (-not (Test-VedhaKeyLine $l)) { throw 'The public key output was not in the expected form.' } }
  $edPublic = $pub[0].Substring($pub[0].IndexOf('=') + 1)
  $p256Public = $pub[1].Substring($pub[1].IndexOf('=') + 1)

  # ---- 3-4. build + package ----
  $zip = Join-Path $winDir 'dist\vedha-agent-win.zip'
  if ($SkipBuild) {
    Write-Step '3' 'Reusing the built agent (-SkipBuild)'
    if (-not (Test-Path -LiteralPath (Join-Path $winDir 'dist\vedha-agent\vedha-agent.exe'))) { throw 'No built agent found in probe\windows\dist\vedha-agent. Run without -SkipBuild.' }
  } else {
    Write-Step '3' 'Building the Windows agent (this is the long step)'
    Invoke-Native 'powershell' @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $winDir 'build-agent-exe.ps1')) 'The agent build'
    Write-Ok 'agent built'
  }
  Write-Step '4' 'Packaging'
  Invoke-Native 'powershell' @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $winDir 'package-zip.ps1'), '-Release') 'Packaging'
  if (-not (Test-Path -LiteralPath $zip)) { throw "The package was not created at $zip." }
  Write-Ok $zip

  # ---- 5. release ----
  Write-Step '5' 'Building and signing the release'
  $out = Join-Path $repo 'dist\agent-release'
  $local = Join-Path $out $Version
  if (Test-Path -LiteralPath $local) { Remove-Item -LiteralPath $local -Recurse -Force }   # local build output only
  Invoke-Native $py @($tool, 'build', '--key', $edKey, '--arch=', '--p256-key', $p256Key, '--windows-zip', $zip, '--out', $out, '--version', $Version) 'Building the release'
  Invoke-Native $py @($tool, 'verify', $local, '--public-key', $edPublic, '--p256-public-key', $p256Public) 'Verifying the release'
  Write-Ok "release $Version is signed and verified: $local"

  if (-not $Server) {
    Write-Host ''
    Write-Host 'Built and signed locally. To publish it, run this again with  -Server ubuntu@YOUR_SERVER -ManagerUrl https://api.YOURDOMAIN -ConfigureManager' -ForegroundColor Yellow
    return 0
  }

  # ---- 6. upload ----
  Write-Step '6' "Uploading to $Server"
  Invoke-Native $py @($tool, 'publish', $local, '--to', "${Server}:${RemoteReleaseDir}") 'Uploading the release'
  Write-Ok "uploaded to ${RemoteReleaseDir}"

  # ---- 7. manager configuration ----
  if ($ConfigureManager) {
    Write-Step '7' "Setting the release keys on the manager ($RemoteComposeDir\.env) and restarting the api"
    $lines = @($pub[0], $pub[1], 'AGENT_RELEASE_REQUIRE_SIGNATURE=true', ('MANAGER_PUBLIC_URL=' + $ManagerUrl))
    $script = New-VedhaRemoteConfigScript -ComposeDir $RemoteComposeDir -Lines $lines
    $tmp = Join-Path $env:TEMP ('vedha-config-' + [guid]::NewGuid().ToString('N') + '.sh')
    [System.IO.File]::WriteAllText($tmp, $script, (New-Object System.Text.UTF8Encoding($false)))   # LF line endings, no BOM
    $remote = '/tmp/' + (Split-Path $tmp -Leaf)
    Push-Location (Split-Path $tmp -Parent)      # relative name: scp reads "C:" as a host
    try {
      Invoke-Native 'scp' @((Split-Path $tmp -Leaf), "${Server}:$remote") 'Copying the configuration script'
      Invoke-Native 'ssh' @($Server, "sh $remote; rc=`$?; rm -f $remote; exit `$rc") 'Configuring the manager'
    } finally {
      Pop-Location
      Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
    Write-Ok 'the manager has the keys and was restarted'
  } else {
    Write-Step '7' 'Manager configuration (not done: -ConfigureManager was not given)'
    Write-Host '    Put these lines in the manager''s .env, then run: docker compose up -d api' -ForegroundColor Yellow
    foreach ($l in $pub) { Write-Host "      $l" }
    Write-Host '      AGENT_RELEASE_REQUIRE_SIGNATURE=true'
    if ($ManagerUrl) { Write-Host "      MANAGER_PUBLIC_URL=$ManagerUrl" } else { Write-Host '      MANAGER_PUBLIC_URL=https://api.YOURDOMAIN' }
  }

  # ---- 8. check from outside ----
  if ($ManagerUrl) {
    Write-Step '8' "Asking $ManagerUrl for its manifest"
    $ok = $false
    for ($try = 1; $try -le 12 -and -not $ok; $try++) {
      try {
        $m = Invoke-RestMethod -Uri ($ManagerUrl + '/agent/manifest.json') -UseBasicParsing -TimeoutSec 15
        if ("$($m.version)" -eq $Version -and ($m.packages | Where-Object { $_.os -eq 'windows' })) { $ok = $true } else { Write-Note "the manager serves release '$($m.version)' for now" }
      } catch { Write-Note "not answering yet ($($_.Exception.Message))" }
      if (-not $ok) { Start-Sleep -Seconds 5 }
    }
    if ($ok) {
      Write-Ok "the manager serves release $Version with the Windows package"
    } elseif (-not $ConfigureManager) {
      Write-Host '    The manager does not serve it yet: it needs the two keys (step 7) and a restart of the api.' -ForegroundColor Yellow
    } else {
      throw "The manager did not serve release $Version within a minute. Check: ssh $Server 'cd $RemoteComposeDir && docker compose logs --tail 50 api'"
    }
  }

  Write-Host ''
  Write-Host 'DONE. Now, for each Windows machine:' -ForegroundColor Green
  Write-Host '  1. In the console: Fleet -> Add agent -> choose the engagement -> Generate install command -> Windows.'
  Write-Host '  2. Run that one command in an Administrator PowerShell on the machine. That is all.'
  return 0
}

# Run only when executed, not when dot-sourced by the tests.
if ($MyInvocation.InvocationName -ne '.') {
  try { exit ([int](@(Invoke-Main) | Select-Object -Last 1)) }
  catch { Write-Host ''; Write-Host ('FAILED: ' + $_.Exception.Message) -ForegroundColor Red; exit 1 }
}
