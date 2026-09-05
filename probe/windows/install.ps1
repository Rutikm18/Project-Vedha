<#
  Vedha Agent — persistent install (Windows Scheduled Task, runs as SYSTEM).
  Registers a reboot-surviving background task named "VedhaAgent".
  Run via install.cmd (which elevates), or:  powershell -ExecutionPolicy Bypass -File install.ps1
#>
[CmdletBinding()]
param(
  [string]$Manager = 'http://13.127.147.205:18080',
  [string]$Scope   = ''    # CIDR; empty = auto-detect this host's /24
)
$ErrorActionPreference = 'Stop'

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) { Write-Error 'Administrator required. Right-click install.cmd -> Run as administrator.'; exit 1 }

$installDir = Join-Path $env:ProgramData 'vedha-agent'
$logDir     = Join-Path $installDir 'logs'
$spoolDir   = Join-Path $installDir 'spool'
New-Item -ItemType Directory -Force -Path $installDir, $logDir, $spoolDir | Out-Null

# Idempotent: stop + remove any existing task so the exe can be replaced cleanly.
if (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue) {
  Stop-ScheduledTask   -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName 'VedhaAgent' -Confirm:$false -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 1
}

Copy-Item (Join-Path $PSScriptRoot 'vedha-agent.exe') (Join-Path $installDir 'vedha-agent.exe') -Force

# Local scan ceiling (empty => the manager will not dispatch jobs).
if (-not $Scope) {
  try {
    $cfg = Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -and $_.NetAdapter.Status -eq 'Up' } | Select-Object -First 1
    if ($cfg -and $cfg.IPv4Address.IPAddress) { $Scope = ($cfg.IPv4Address.IPAddress -replace '\.\d+$', '.0') + '/24' }
  } catch {}
}
if (-not $Scope) { Write-Warning 'Could not auto-detect the local /24. The probe will connect but be DENIED all jobs. Re-run install.cmd with -Scope <CIDR>.' }

# Service wrapper — a Scheduled Task has no console, so set env + log to a file.
$wrapper = @"
@echo off
set "PLATFORM_URL=$Manager"
set "VERIFY_TLS=true"
set "PROBE_NAME=%COMPUTERNAME%-probe"
set "PROBE_NETWORK_SEGMENTS=$Scope"
set "STATE_FILE=$installDir\state.json"
set "RESULT_SPOOL_DIR=$spoolDir"
cd /d "$installDir"
"$installDir\vedha-agent.exe" run >> "$logDir\agent.log" 2>&1
"@
Set-Content -Path (Join-Path $installDir 'agent-service.cmd') -Value $wrapper -Encoding ASCII

$action    = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$installDir\agent-service.cmd`""
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
Write-Host 'VedhaAgent installed and started.' -ForegroundColor Green
Write-Host "  Manager : $Manager"
Write-Host "  Scope   : $Scope"
Write-Host "  Logs    : $logDir\agent.log"
Write-Host ''
Write-Host 'If the manager requires approval, approve this probe in Manager -> Fleet (see the log for a pairing code).'
