<#
  Vedha Agent - persistent install (Windows Scheduled Task, runs as SYSTEM).
  Registers a reboot-surviving background task named "VedhaAgent".
  Run via install.cmd (which elevates), or:  powershell -ExecutionPolicy Bypass -File install.ps1
#>
[CmdletBinding()]
param(
  [string]$Manager = '__VEDHA_MANAGER_URL__',
  [string]$Scope   = '',   # CIDR; empty = auto-detect this host's /24
  [string]$Token   = '',   # install token (vet_...) from Fleet -> Add agent: enrols this agent without a pairing code
  [int]$EnrolWaitSeconds = 120   # how long to wait for the token enrolment before reporting it as pending
)
$ErrorActionPreference = 'Stop'
if ($Manager -like '__*') { Write-Error 'No manager address. Re-create the package with package-zip.ps1 -Manager https://api.your-domain.com, or pass -Manager.'; exit 1 }
if ($Token -and $Token -notmatch '^vet_[A-Za-z0-9_\-]+$') { Write-Error 'The install token is malformed (expected vet_...). Copy it again from Fleet -> Add agent.'; exit 1 }

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) { Write-Error 'Administrator required. Right-click install.cmd -> Run as administrator.'; exit 1 }

$installDir = Join-Path $env:ProgramData 'vedha-agent'
$logDir     = Join-Path $installDir 'logs'
$spoolDir   = Join-Path $installDir 'spool'
$tokenFile  = Join-Path $installDir 'enroll.token'
$stateFile  = Join-Path $installDir 'state.json'
New-Item -ItemType Directory -Force -Path $installDir, $logDir, $spoolDir | Out-Null

# The agent's identity key (state.json) and the install token live here, and the folder holds
# code that runs as SYSTEM: only SYSTEM and Administrators may touch it. Well-known SIDs, so this
# works on any display language. (To run run.cmd as a normal user afterwards, use an
# administrator prompt, or point STATE_FILE somewhere of your own.)
& icacls.exe $installDir /inheritance:r /grant:r '*S-1-5-18:(OI)(CI)F' '*S-1-5-32-544:(OI)(CI)F' | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Error "Could not restrict permissions on $installDir"; exit 1 }

# Idempotent: stop + remove any existing task so the exe can be replaced cleanly.
if (Get-ScheduledTask -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue) {
  Stop-ScheduledTask   -TaskName 'VedhaAgent' -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName 'VedhaAgent' -Confirm:$false -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 1
}

# The compiled agent is a folder (vedha-agent\vedha-agent.exe + its libraries).
$appDir = Join-Path $installDir 'app'
if (Test-Path $appDir) { Remove-Item $appDir -Recurse -Force }
Copy-Item (Join-Path $PSScriptRoot 'vedha-agent') $appDir -Recurse -Force

# Local scan ceiling (empty => the manager will not dispatch jobs).
if (-not $Scope) {
  try {
    $cfg = Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -and $_.NetAdapter.Status -eq 'Up' } | Select-Object -First 1
    if ($cfg -and $cfg.IPv4Address.IPAddress) { $Scope = ($cfg.IPv4Address.IPAddress -replace '\.\d+$', '.0') + '/24' }
  } catch {}
}
if (-not $Scope) { Write-Warning 'Could not auto-detect the local /24. The probe will connect but be DENIED all jobs. Re-run install.cmd with -Scope <CIDR>.' }

# One-time install token: kept in the locked folder, never in the wrapper or on a command
# line, and removed as soon as the agent has enrolled (below, and again at every start).
if ($Token) {
  Set-Content -Path $tokenFile -Value $Token -Encoding ASCII
} elseif (Test-Path $tokenFile) {
  Remove-Item $tokenFile -Force   # a token from an earlier, abandoned install must not linger
}

# Service wrapper - a Scheduled Task has no console, so set env + log to a file.
$wrapper = @"
@echo off
rem Once enrolled, the install token is spent: delete it. Until then, offer it to the agent.
if exist "$stateFile" findstr /c:"device_refresh_secret" "$stateFile" >nul 2>&1 && del /q "$tokenFile" >nul 2>&1
if exist "$tokenFile" set /p PROBE_ENROLL_TOKEN=<"$tokenFile"
set "PLATFORM_URL=$Manager"
set "VERIFY_TLS=true"
rem The compiled agent is not host-sealed: the manager controls access (install token, expiry, revoke).
set "LICENSE_ENFORCED=false"
set "PROBE_NAME=%COMPUTERNAME%-probe"
set "PROBE_NETWORK_SEGMENTS=$Scope"
set "STATE_FILE=$installDir\state.json"
set "RESULT_SPOOL_DIR=$spoolDir"
cd /d "$installDir"
"$appDir\vedha-agent.exe" run >> "$logDir\agent.log" 2>&1
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

# With a token the agent enrols itself within seconds; wait for it so a failure is reported here
# and the spent token is removed straight away.
$enrolled = $false
if ($Token) {
  Write-Host 'Waiting for the agent to enrol with the manager ...'
  for ($i = 0; $i -lt [math]::Ceiling($EnrolWaitSeconds / 2) -and -not $enrolled; $i++) {
    Start-Sleep -Seconds 2
    # state.json is replaced atomically by the agent; a read that races it just retries.
    try { $enrolled = (Test-Path $stateFile) -and [bool](Select-String -Path $stateFile -Pattern 'device_refresh_secret' -Quiet) } catch { $enrolled = $false }
  }
  if ($enrolled) { Remove-Item $tokenFile -Force -ErrorAction SilentlyContinue }
}

Write-Host ''
Write-Host 'VedhaAgent installed and started.' -ForegroundColor Green
Write-Host "  Manager : $Manager"
Write-Host "  Scope   : $Scope"
Write-Host "  Logs    : $logDir\agent.log"
Write-Host ''
if ($Token -and $enrolled) {
  Write-Host 'Enrolled. The agent shows as connected in Manager -> Fleet within a minute.' -ForegroundColor Green
} elseif ($Token) {
  Write-Warning "The agent has not enrolled yet. Check $logDir\agent.log; the install token stays (access-restricted) and is retried at every start until it works or expires."
} else {
  Write-Host 'If the manager requires approval, approve this probe in Manager -> Fleet (see the log for a pairing code).'
}
