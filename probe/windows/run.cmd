@echo off
rem ── Vedha Agent — attended run (no admin needed) ─────────────────────────────
rem Double-click to see the agent connect to the manager and wait for jobs.
rem Close the window to stop. For a permanent install, use install.cmd instead.
setlocal
cd /d "%~dp0"

set "PLATFORM_URL=http://13.127.147.205:18080"
set "VERIFY_TLS=true"
set "PROBE_NAME=%COMPUTERNAME%-probe"
set "STATE_FILE=%ProgramData%\vedha-agent\state.json"
set "RESULT_SPOOL_DIR=%ProgramData%\vedha-agent\spool"
if not exist "%ProgramData%\vedha-agent\spool" mkdir "%ProgramData%\vedha-agent\spool"

rem Local scan ceiling = this host's /24 (empty = the manager sends no jobs).
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "$c=Get-NetIPConfiguration ^| Where-Object {$_.IPv4DefaultGateway -and $_.NetAdapter.Status -eq 'Up'} ^| Select-Object -First 1; if($c -and $c.IPv4Address.IPAddress){($c.IPv4Address.IPAddress -replace '\.\d+$','.0')+'/24'}"`) do set "PROBE_NETWORK_SEGMENTS=%%i"

echo(
echo    Manager : %PLATFORM_URL%
echo    Scope   : %PROBE_NETWORK_SEGMENTS%
echo    State   : %STATE_FILE%
echo(
if "%PROBE_NETWORK_SEGMENTS%"=="" echo    WARNING: no local /24 detected - the probe will connect but get NO jobs.
echo Starting vedha-agent (close this window to stop)...
echo(
"%~dp0vedha-agent.exe" run
endlocal
