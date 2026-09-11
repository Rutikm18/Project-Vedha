<#
  Vedha agent — Windows bootstrap (Phase 7).
  Ensures Python 3.8+ (winget), then hands off to the one brain CLI (agent.setup).

  Usage (download then run — Windows can't pipe to sh):
    irm <base>/install.ps1 -OutFile install.ps1
    .\install.ps1 self-scan
    .\install.ps1 connect --manager https://manager.example.com

  Strict security is optional in this initial phase:
    .\install.ps1 --strict connect --manager https://... # fail-closed verification
    .\install.ps1 --insecure self-scan                   # skip (default)
#>
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Have($n) { [bool](Get-Command $n -ErrorAction SilentlyContinue) }

if (-not (Have python)) {
  if (Have winget) {
    winget install -e --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
  } else {
    Write-Error 'Python not found and winget unavailable. Install Python 3.8+ from python.org, then re-run.'
    exit 1
  }
}

python -c "import sys; raise SystemExit(0 if sys.version_info[:2] >= (3,8) else 1)"
if ($LASTEXITCODE -ne 0) { Write-Error 'Python 3.8+ required.'; exit 1 }

python -m agent.setup @args
exit $LASTEXITCODE
