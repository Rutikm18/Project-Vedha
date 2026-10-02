<#
  Vedha Agent - LAB / DEVELOPMENT setup (SOURCE mode; ships readable Python).

  NOT FOR CUSTOMER SITES. This path ships source, installs Python and (with
  -DefenderExcludePython) weakens Microsoft Defender. Customer installs use the
  compiled, signed agent from Fleet -> Add agent (docs/probe/CUSTOMER_AGENT_INSTALL.md).
  Kept here for the lab only.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File setup.ps1 -Manager https://api.your-domain.com -Foreground
    powershell -ExecutionPolicy Bypass -File setup.ps1 -Manager https://api.your-domain.com
  Options:
    -Manager <url>            REQUIRED, e.g. https://api.your-domain.com
    -Scope <cidr>             default = auto-detect this host's /24
    -Update                   git pull before setting up
    -DefenderExcludePython    opt-in: exclude python.exe from Defender (lab only;
                              a customer security team must never allow this)
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Manager,
  [string]$Scope   = '',
  [switch]$Foreground,
  [switch]$Update,
  [switch]$DefenderExcludePython
)
$ErrorActionPreference = 'Stop'
Write-Warning 'setup.ps1 is the LAB source-mode path (ships readable Python). For customer sites use the compiled agent from Fleet -> Add agent.'
$probeRoot = Split-Path $PSScriptRoot -Parent      # ...\probe

# Admin? (affects Python install scope + the background-task install)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($Update) {
  if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host 'Updating from git...'
    git -C $probeRoot pull --ff-only
  } else {
    Write-Warning 'git not found - skipping -Update (re-download the ZIP to update, or install Git).'
  }
}

# ── Find or AUTO-INSTALL Python (fresh machine: nothing preinstalled) ─────────
function Get-PythonExe {
  # Real python 3.8+ on PATH (skips the Windows Store stub, which fails -c).
  foreach ($c in @('python','py')) {
    $cmd = Get-Command $c -ErrorAction SilentlyContinue
    if ($cmd) {
      try {
        $v = & $cmd.Source -c "import sys;print('%d.%d'%sys.version_info[:2])" 2>$null
        if ($LASTEXITCODE -eq 0 -and [version]$v -ge [version]'3.8') { return $cmd.Source }
      } catch {}
    }
  }
  # PATH may not be refreshed in this process right after an install - check known dirs.
  foreach ($pat in @(
      "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe",
      "$env:ProgramFiles\Python3*\python.exe",
      "C:\Python3*\python.exe")) {
    $f = Get-ChildItem $pat -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1
    if ($f) { return $f.FullName }
  }
  return $null
}

function Install-Python {
  Write-Host 'Python not found - installing Python 3.12 automatically...'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  # Prefer winget (Win10 1809+/Win11); silent, handles PATH.
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    $scope = if ($isAdmin) { 'machine' } else { 'user' }
    try { winget install --id Python.Python.3.12 -e --scope $scope --accept-package-agreements --accept-source-agreements --silent | Out-Null } catch {}
    $p = Get-PythonExe; if ($p) { return $p }
  }
  # Fallback: official silent installer - works with nothing else installed.
  $ver = '3.12.7'
  $installer = Join-Path $env:TEMP "python-$ver-amd64.exe"
  Write-Host "Downloading python-$ver-amd64.exe ..."
  Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$ver/python-$ver-amd64.exe" -OutFile $installer -UseBasicParsing
  $allUsers = if ($isAdmin) { '1' } else { '0' }   # all-users needs admin; per-user otherwise
  Write-Host 'Installing Python (silent; ~1 min)...'
  Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=$allUsers PrependPath=1 Include_pip=1 Include_test=0" -Wait
  Remove-Item $installer -ErrorAction SilentlyContinue
  return (Get-PythonExe)
}

$python = Get-PythonExe
if (-not $python) { $python = Install-Python }
if (-not $python) { Write-Error 'Could not find or install Python. Install Python 3.10+ from https://python.org and re-run.'; exit 1 }
Write-Host "Using Python: $python"

# 2) venv + deps (idempotent; venv lives in probe\windows so .gitignore covers it)
$venv = Join-Path $PSScriptRoot '.venv-win'
$vpy  = Join-Path $venv 'Scripts\python.exe'

# Windows Defender flags impacket's example scripts as a HackTool and quarantines
# them mid-install -> pip dies with "[Errno 22] Invalid argument: ...DumpNTLMInfo.py",
# and it would also block the agent at runtime. Exclude the venv + state dir (admin only).
$agentDataDir = Join-Path $env:ProgramData 'vedha-agent'
if ($isAdmin) {
  # Path exclusions are scoped to the agent's own venv + state dir.
  foreach ($ex in @($venv, $agentDataDir)) { try { Add-MpPreference -ExclusionPath $ex -ErrorAction SilentlyContinue } catch {} }
  # Excluding python.exe PROCESS-WIDE weakens Defender for EVERY Python program on
  # the machine. Opt-in only, and never on a customer site.
  if ($DefenderExcludePython) {
    Write-Warning 'Excluding python.exe from Defender for the WHOLE machine (-DefenderExcludePython). Lab use only.'
    try { Add-MpPreference -ExclusionProcess 'python.exe' -ErrorAction SilentlyContinue } catch {}
  }
} else {
  Write-Warning 'Not admin: if pip fails on impacket (Errno 22) or the agent gets blocked, Windows Defender is the cause. Re-run elevated (setup.cmd), or add: Add-MpPreference -ExclusionPath "<repo folder>".'
}

if (-not (Test-Path $vpy)) { Write-Host 'Creating virtualenv...'; & $python -m venv $venv }
Write-Host 'Installing dependencies...'
& $vpy -m pip install --quiet --upgrade pip
& $vpy -m pip install --quiet -r (Join-Path $probeRoot 'requirements-runtime.txt')

# 3) Local scan ceiling (empty => manager sends no jobs)
if (-not $Scope) {
  try {
    $cfg = Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -and $_.NetAdapter.Status -eq 'Up' } | Select-Object -First 1
    if ($cfg -and $cfg.IPv4Address.IPAddress) { $Scope = ($cfg.IPv4Address.IPAddress -replace '\.\d+$','.0') + '/24' }
  } catch {}
}
if (-not $Scope) { Write-Warning 'No local /24 detected - the probe will connect but receive NO jobs until you pass -Scope <CIDR>.' }

# 4) State dirs (shared by foreground + service so identity is stable)
$stateDir = Join-Path $env:ProgramData 'vedha-agent'
New-Item -ItemType Directory -Force -Path $stateDir, (Join-Path $stateDir 'spool'), (Join-Path $stateDir 'logs') | Out-Null

# 5a) FOREGROUND - run now, no admin
if ($Foreground) {
  $env:PLATFORM_URL           = $Manager
  $env:VERIFY_TLS             = 'true'
  $env:LICENSE_ENFORCED       = 'false'   # source build: no baked HW fingerprint/license
  $env:PROBE_NAME             = "$env:COMPUTERNAME-probe"
  $env:PROBE_NETWORK_SEGMENTS = $Scope
  $env:STATE_FILE             = Join-Path $stateDir 'state.json'
  $env:RESULT_SPOOL_DIR       = Join-Path $stateDir 'spool'
  $env:PYTHONPATH             = $probeRoot
  Set-Location $probeRoot
  Write-Host ''
  Write-Host "Manager=$Manager  Scope=$Scope  (close window / Ctrl+C to stop)" -ForegroundColor Green
  & $vpy -m agent.agent run
  exit $LASTEXITCODE
}

# 5b) PERSISTENT - background task (needs admin; $isAdmin computed at top)
if (-not $isAdmin) { Write-Error 'Installing the background task needs Administrator. Run setup.cmd (it elevates), or use -Foreground to just run now.'; exit 1 }

if (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue) {
  Stop-ScheduledTask       -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName 'VedhaAgent' -Confirm:$false -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 1
}

$wrapper = @"
@echo off
set "PLATFORM_URL=$Manager"
set "VERIFY_TLS=true"
set "LICENSE_ENFORCED=false"
set "PROBE_NAME=%COMPUTERNAME%-probe"
set "PROBE_NETWORK_SEGMENTS=$Scope"
set "STATE_FILE=$stateDir\state.json"
set "RESULT_SPOOL_DIR=$stateDir\spool"
set "PYTHONPATH=$probeRoot"
cd /d "$probeRoot"
"$vpy" -m agent.agent run >> "$stateDir\logs\agent.log" 2>&1
"@
Set-Content (Join-Path $stateDir 'agent-service.cmd') $wrapper -Encoding ASCII

$action    = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$stateDir\agent-service.cmd`""
$trigger   = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable `
               -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
               -RestartInterval (New-TimeSpan -Minutes 1) -RestartCount 999 `
               -ExecutionTimeLimit (New-TimeSpan -Seconds 0)
Register-ScheduledTask -TaskName 'VedhaAgent' -Description 'Vedha network probe agent' `
  -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
Start-ScheduledTask -TaskName 'VedhaAgent'

Write-Host ''
Write-Host 'VedhaAgent installed and started (survives reboot).' -ForegroundColor Green
Write-Host "  Manager : $Manager"
Write-Host "  Scope   : $Scope"
Write-Host "  Logs    : $stateDir\logs\agent.log"
