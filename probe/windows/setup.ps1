<#
  Vedha Agent - one-shot automated setup (SOURCE mode; no exe build needed).
  Pull the repo, run this, done. It creates a venv, installs deps, detects the
  local scan scope, and either runs the agent now or installs it as a background
  task that survives reboot.

  Usage (from probe\windows):
    powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground   # run now, no admin (test)
    powershell -ExecutionPolicy Bypass -File setup.ps1               # install background task (admin)
  Options:
    -Manager <url>   default http://13.127.147.205:18080
    -Scope <cidr>    default = auto-detect this host's /24
    -Update          git pull before setting up
#>
[CmdletBinding()]
param(
  [string]$Manager = 'http://13.127.147.205:18080',
  [string]$Scope   = '',
  [switch]$Foreground,
  [switch]$Update
)
$ErrorActionPreference = 'Stop'
$probeRoot = Split-Path $PSScriptRoot -Parent      # ...\probe

if ($Update) {
  Write-Host 'Updating from git...'
  git -C $probeRoot pull --ff-only
}

# 1) Find Python
$python = $null
foreach ($c in @('python','py')) {
  $cmd = Get-Command $c -ErrorAction SilentlyContinue
  if ($cmd) { $python = $cmd.Source; break }
}
if (-not $python) { Write-Error 'Python 3.8+ not found. Install from https://python.org (tick "Add to PATH"), then re-run.'; exit 1 }

# 2) venv + deps (idempotent; venv lives in probe\windows so .gitignore covers it)
$venv = Join-Path $PSScriptRoot '.venv-win'
$vpy  = Join-Path $venv 'Scripts\python.exe'
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

# 5b) PERSISTENT - background task (needs admin)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
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
