<#
  Build vedha-agent.exe from probe/agent/agent.py (the daemon entrypoint;
  agent.py defaults argv to "run"). RUN THIS ON A WINDOWS MACHINE.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1                 # PyInstaller (simplest)
    powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1 -Tool nuitka    # Nuitka (IP-sealed; needs a C compiler)

  Output: probe\windows\dist\vedha-agent.exe
  Note: Nuitka also fixes the sealed-build dep gap by including impacket/ldap3/dns.
#>
[CmdletBinding()]
param(
  [ValidateSet('pyinstaller','nuitka')] [string]$Tool = 'pyinstaller',
  [string]$OutDir = "$PSScriptRoot\dist"
)
$ErrorActionPreference = 'Stop'

$probeRoot = Split-Path $PSScriptRoot -Parent      # ...\probe
Set-Location $probeRoot
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# Isolated build venv (kept inside probe\windows so .gitignore covers it).
$venv = Join-Path $PSScriptRoot '.venv-win'
if (-not (Test-Path (Join-Path $venv 'Scripts\python.exe'))) { python -m venv $venv }
$py = Join-Path $venv 'Scripts\python.exe'

& $py -m pip install --upgrade pip
& $py -m pip install -r (Join-Path $probeRoot 'requirements-runtime.txt')

if ($Tool -eq 'pyinstaller') {
  & $py -m pip install pyinstaller
  & $py -m PyInstaller --onefile --name vedha-agent --noconfirm `
      --paths $probeRoot `
      --collect-submodules scanner --collect-submodules workflow --collect-submodules agent `
      --collect-all impacket --collect-all ldap3 --collect-all dns `
      --distpath $OutDir --workpath (Join-Path $OutDir '_work') --specpath (Join-Path $OutDir '_spec') `
      (Join-Path $probeRoot 'agent\agent.py')
}
else {
  & $py -m pip install nuitka
  & $py -m nuitka --onefile --standalone --assume-yes-for-downloads --follow-imports `
      --include-package=scanner --include-package=workflow --include-package=agent `
      --include-package=impacket --include-package=ldap3 --include-package=dns `
      --include-package=cryptography --include-package=httpx --include-package=websockets `
      --python-flag=no_docstrings --python-flag=no_asserts `
      --output-dir=$OutDir --output-filename=vedha-agent.exe `
      (Join-Path $probeRoot 'agent\agent.py')
}

$exe = Join-Path $OutDir 'vedha-agent.exe'
if (Test-Path $exe) {
  Write-Host ''
  Write-Host "Built: $exe" -ForegroundColor Green
  Write-Host 'Smoke test:  .\dist\vedha-agent.exe hostid   (should print a host id and exit)'
} else {
  Write-Error "Build finished but $exe was not produced. If a scanner is 'not found' at runtime, add it to --collect-submodules / --include-package."
}
