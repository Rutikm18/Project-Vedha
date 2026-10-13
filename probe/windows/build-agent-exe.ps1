<#
  Build the Windows agent: the agent's own code, compiled with Nuitka into a folder
  (no readable Python source or bytecode). RUN THIS ON A WINDOWS MACHINE (the CI
  job .github/workflows/agent-windows-build.yml does).

  What is compiled is the agent's import closure only (tools/agent_closure.py): the
  agent, the scanners it uses and the workflow engine. Never scanner/findings.py
  (the vulnerability judgement rules stay on the manager), the campaign runner,
  accuracy gates, main_scripts/, cve/ or tests. The build fails if any of those
  would be included, or if the output holds Python source/bytecode of ours.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1

  Output: probe\windows\dist\vedha-agent\vedha-agent.exe  (+ the libraries beside it)
  Needs: Python 3.10-3.12 on PATH and a C compiler (Nuitka offers to fetch MinGW).
#>
[CmdletBinding()]
param(
  [string]$OutDir = ''
)
$ErrorActionPreference = 'Stop'

# $PSScriptRoot is empty inside a param() default under some Windows PowerShell hosts,
# which turned this into "\dist" (the drive root). Resolve it here, as an absolute path.
if (-not $OutDir) { $OutDir = Join-Path $PSScriptRoot 'dist' }
$OutDir = [System.IO.Path]::GetFullPath($OutDir)

$probeRoot = Split-Path $PSScriptRoot -Parent      # ...\probe
Set-Location $probeRoot
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# Isolated build venv (kept inside probe\windows so .gitignore covers it).
$venv = Join-Path $PSScriptRoot '.venv-win'
if (-not (Test-Path (Join-Path $venv 'Scripts\python.exe'))) { python -m venv $venv }
$py = Join-Path $venv 'Scripts\python.exe'
& $py -m pip install --quiet --upgrade pip
& $py -m pip install --quiet -r (Join-Path $probeRoot 'requirements-runtime.txt') nuitka

# 1) Only the agent's closure goes to the compiler. --check fails on a blocked
#    module or a dynamic import (which a compiler cannot follow).
& $py tools\agent_closure.py --check
if ($LASTEXITCODE -ne 0) { throw 'agent closure check failed' }
$stage = Join-Path $env:TEMP 'vedha-agent-src'
if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
& $py tools\agent_closure.py --export $stage
if ($LASTEXITCODE -ne 0) { throw 'agent closure export failed' }

# 2) Compile to a standalone folder. Docstrings and asserts are stripped; the
#    optional credential collectors (paramiko, winrm) are left out on purpose.
#    MinGW gcc (--mingw64), not MSVC: cl.exe dies with C1002 "out of heap space" on
#    impacket's large generated RPC modules (srvs, tsts, ...); gcc handles them.
#    websockets IS compiled whole: it loads websockets.asyncio.client lazily by name, which
#    Nuitka cannot follow, so without this the agent registers and then cannot open its live
#    connection (seen on the first real install). `runtime-check` now exercises that path.
#
#    impacket is NOT compiled whole: --include-package=impacket pulls in huge generated
#    modules (e.g. dcerpc.v5.tsts) that run MSVC out of heap space (C1002). Only the
#    modules the scanners import are built; `vedha-agent runtime-check` verifies them.
$dist = Join-Path $OutDir 'vedha-agent'
if (Test-Path $dist) { Remove-Item $dist -Recurse -Force }

# Nuitka rejects any version info unless a numeric file/product version is given too.
$versionFile = Join-Path (Split-Path $probeRoot -Parent) 'VERSION'
$agentVersion = if (Test-Path $versionFile) { (Get-Content $versionFile -TotalCount 1).Trim() } else { '' }
if ($agentVersion -notmatch '^\d+(\.\d+){0,3}$') { $agentVersion = '0.0.0' }

Push-Location $stage
try {
  & $py -m nuitka --standalone --mingw64 --assume-yes-for-downloads --follow-imports `
      --python-flag=no_docstrings --python-flag=no_asserts `
      --include-package=agent --include-package=scanner --include-package=workflow `
      --include-package=ldap3 --include-package=dns `
      --include-package=websockets `
      --include-module=impacket.smbconnection --include-module=impacket.uuid `
      --include-module=impacket.dcerpc.v5.transport --include-module=impacket.dcerpc.v5.samr `
      --include-module=impacket.dcerpc.v5.lsat --include-module=impacket.dcerpc.v5.lsad `
      --include-module=impacket.dcerpc.v5.rrp --include-module=impacket.dcerpc.v5.epm `
      --include-module=impacket.dcerpc.v5.rpcrt --include-module=impacket.dcerpc.v5.dtypes `
      --nofollow-import-to=impacket.examples --nofollow-import-to=impacket.dcerpc.v5.tsts `
      --nofollow-import-to=paramiko --nofollow-import-to=winrm `
      --nofollow-import-to=pytest --nofollow-import-to=unittest `
      --windows-console-mode=force --company-name=Vedha --product-name='Vedha Agent' `
      "--file-version=$agentVersion" "--product-version=$agentVersion" `
      --file-description='Vedha network assessment agent' `
      "--output-dir=$OutDir" --output-filename=vedha-agent.exe --remove-output `
      agent\agent.py
  if ($LASTEXITCODE -ne 0) { throw 'Nuitka build failed' }
} finally {
  Pop-Location
  Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
}
Rename-Item (Join-Path $OutDir 'agent.dist') 'vedha-agent'

# 3) Nothing readable of ours may ship.
$leftover = Get-ChildItem $dist -Recurse -File -Include *.py, *.pyc |
  Where-Object { $_.FullName.Substring($dist.Length + 1) -match '^(agent|scanner|workflow|main_scripts|cve|tests)\\' }
if ($leftover) {
  $leftover | ForEach-Object { Write-Warning "source/bytecode shipped: $($_.FullName)" }
  throw 'build output contains Python source or bytecode of our packages'
}

# 4) Every module the agent can load lazily must be inside the compiled binary.
$exe = Join-Path $dist 'vedha-agent.exe'
if (-not (Test-Path $exe)) { throw "Build finished but $exe was not produced." }
& $exe runtime-check
if ($LASTEXITCODE -ne 0) { throw 'compiled runtime-check failed (a module was left out of the build)' }

Write-Host ''
Write-Host "Built: $exe" -ForegroundColor Green
Write-Host 'Smoke test:  .\dist\vedha-agent\vedha-agent.exe hostid   (prints a host id and exits)'
