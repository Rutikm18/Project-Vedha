@echo off
rem ---------------------------------------------------------------------------
rem Vedha Agent - one-command Windows install (cmd.exe).
rem
rem   curl.exe -fsSL "https://manager.example.com/agent/install.cmd" -o "%TEMP%\vedha-install.cmd" && "%TEMP%\vedha-install.cmd" "https://manager.example.com" "vet_..."
rem
rem Fleet -> Add agent prints this with your manager and token filled in.
rem Usage:  install.cmd <https-manager-url> <install-token> [scan-scope-cidr]
rem
rem This launcher only asks for administrator rights and starts PowerShell on the
rem installer the manager serves (/agent/install.ps1). That installer verifies the
rem signed release before it trusts or installs anything.
rem ---------------------------------------------------------------------------
setlocal EnableExtensions DisableDelayedExpansion

set "VEDHA_SELF=%~f0"
set "VEDHA_MANAGER=%~1"
set "VEDHA_TOKEN=%~2"
set "VEDHA_SCOPE=%~3"
set "VEDHA_ELEVATED=%~4"

if not defined VEDHA_MANAGER goto :usage
if not defined VEDHA_TOKEN goto :usage

rem The values travel to PowerShell through the environment, never spliced into a
rem command line, and PowerShell checks each against a strict pattern first.
powershell -NoProfile -ExecutionPolicy Bypass -Command "if (($env:VEDHA_MANAGER -notmatch '^https://[A-Za-z0-9.\-]+(:[0-9]{1,5})?$') -or ($env:VEDHA_TOKEN -notmatch '^vet_[A-Za-z0-9_\-]+$') -or ($env:VEDHA_SCOPE -and $env:VEDHA_SCOPE -notmatch '^[0-9A-Fa-f:.,/]+$')) { exit 2 }"
if errorlevel 1 (
  echo ERROR: the manager address, token or scope has an unexpected format. The manager must be an https:// address. Copy the command again from Fleet - Add agent.
  exit /b 2
)

rem fltmc succeeds only in an elevated prompt (unlike `net session`, it does not need the Server service).
fltmc >nul 2>&1
if errorlevel 1 (
  if defined VEDHA_ELEVATED (
    echo ERROR: administrator rights were not granted.
    exit /b 1
  )
  echo Requesting administrator rights ...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$q = [char]34; $a = '/c ' + $q + $q + $env:VEDHA_SELF + $q + ' ' + $q + $env:VEDHA_MANAGER + $q + ' ' + $q + $env:VEDHA_TOKEN + $q + ' ' + $q + $env:VEDHA_SCOPE + $q + ' elevated' + $q; Start-Process -FilePath $env:ComSpec -Verb RunAs -ArgumentList $a"
  exit /b %errorlevel%
)

rem Running elevated in a window of its own (we were relaunched): keep it open to show the result.
set "VEDHA_PAUSE="
if defined VEDHA_ELEVATED set "VEDHA_PAUSE=1"

powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $m = $env:VEDHA_MANAGER; $p = @{ Manager = $m; Token = $env:VEDHA_TOKEN }; if ($env:VEDHA_SCOPE) { $p.Scope = $env:VEDHA_SCOPE }; if ($env:VEDHA_PAUSE) { $p.PauseAtEnd = $true }; & ([scriptblock]::Create((irm ($m + '/agent/install.ps1')))) @p; exit $LASTEXITCODE"
exit /b %errorlevel%

:usage
echo Usage: %~nx0 ^<https-manager-url^> ^<install-token^> [scan-scope-cidr]
echo   Fleet - Add agent shows the exact command with both values filled in.
exit /b 1
