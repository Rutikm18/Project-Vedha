<#
  publish-bootstrap.ps1 - ONE command to build + sign + upload the Windows agent.

  Run this on a Windows PC (yours, or a throwaway VM) from an ordinary PowerShell.
  It fetches only the source the build needs (probe/ + scripts/, shallow), builds
  the compiled agent with Nuitka, signs the release, and uploads it to your manager
  - the same thing B1 + B2 did, in a single command. Nothing persists on the PC
  except the small work folder, which you can delete afterwards.

  It needs on this PC: git, Python 3.10-3.12 on PATH, the OpenSSH client (ssh/scp),
  and SSH access to the manager server.

  Example:
    powershell -ExecutionPolicy Bypass -File publish-bootstrap.ps1 `
        -Server ubuntu@16.4.75.44 -ManagerUrl https://get.vedhasec.com

  The two PUBLIC keys it prints at the end go into the server with
  deploy/aws/set-release-keys.sh (the one script for the server side).

  Re-publishing an installer-only change (no agent code change) is fast: add
  -SkipBuild to reuse the compiled agent already in the work folder.

  ASCII only, on purpose (Windows PowerShell 5.1 reads a BOM-less file as ANSI).
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Server,          # user@host of the manager server (ssh)
  [Parameter(Mandatory = $true)][string]$ManagerUrl,      # https://get.vedhasec.com (the facade)
  [string]$ReleaseDir = '/opt/vedha/manager/agent-releases',
  [string]$Branch = 'main',                                 # the zero-knowledge install work is merged into main
  [string]$RepoUrl = 'https://github.com/Rutikm18/Project-Vedha.git',
  [string]$WorkDir = '',
  [switch]$SkipBuild,     # reuse the compiled agent already in the work folder (installer-only re-publish)
  [switch]$KeepClone      # keep the work folder afterwards (default: a note tells you how to remove it)
)
$ErrorActionPreference = 'Stop'

function Write-Step { param([string]$Text) Write-Host ''; Write-Host "[bootstrap] $Text" -ForegroundColor Cyan }

if ($env:OS -ne 'Windows_NT') { throw 'Run this on Windows: the agent is compiled for Windows.' }
foreach ($tool in 'git', 'python', 'ssh', 'scp') {
  if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
    throw "$tool was not found on PATH. Install it and run this again (ssh/scp: Settings > Apps > Optional features > OpenSSH Client)."
  }
}
if (-not $WorkDir) { $WorkDir = Join-Path $env:USERPROFILE 'vedha-build' }

# 1) minimal source: only probe/ + scripts/, shallow, no blobs until needed.
if (Test-Path (Join-Path $WorkDir '.git')) {
  Write-Step "reusing the source in $WorkDir"
  Push-Location $WorkDir
} else {
  Write-Step "fetching minimal source into $WorkDir (probe + scripts only)"
  git clone --filter=blob:none --depth 1 --no-checkout $RepoUrl $WorkDir
  if ($LASTEXITCODE -ne 0) { throw 'git clone failed.' }
  Push-Location $WorkDir
  git sparse-checkout init --cone
  git sparse-checkout set probe scripts
}
try {
  git fetch origin $Branch --depth 1
  if ($LASTEXITCODE -ne 0) { throw "git fetch of $Branch failed." }
  git checkout FETCH_HEAD
  if ($LASTEXITCODE -ne 0) { throw 'git checkout failed.' }

  # 2) build + sign + upload (publish-release.ps1 does the vendor side).
  Write-Step 'building, signing and uploading the release (15-35 min the first time)'
  $publish = Join-Path $WorkDir 'probe\windows\publish-release.ps1'
  $arguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $publish,
                 '-Server', $Server, '-ManagerUrl', $ManagerUrl, '-RemoteReleaseDir', $ReleaseDir)
  if ($SkipBuild) { $arguments += '-SkipBuild' }
  & (Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe') @arguments
  if ($LASTEXITCODE -ne 0) { throw "publish-release.ps1 exited with code $LASTEXITCODE." }
} finally {
  Pop-Location
}

Write-Host ''
Write-Host '[bootstrap] DONE on the Windows side.' -ForegroundColor Green
Write-Host '  Next: copy the two PUBLIC keys printed above into the server, in one command:'
Write-Host "    on the server:  ./deploy/aws/set-release-keys.sh --ed25519 '<pub>' --p256 '<pub>'"
if (-not $KeepClone) {
  Write-Host ''
  Write-Host "  When you are done, delete the work folder:  Remove-Item -Recurse -Force '$WorkDir'"
  Write-Host '  (Keep it if you plan to re-publish an installer-only change soon with -SkipBuild.)'
}
