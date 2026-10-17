@echo off
rem Vedha agent build kit - double-click this. It checks this PC and the server, then builds and publishes the agent.
rem Anything after the file name is passed through, for example:  install.cmd -CheckOnly
setlocal
set "KIT=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%KIT%probe\windows\kit-install.ps1" %*
exit /b %errorlevel%
