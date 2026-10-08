@echo off
rem Remove the Vedha agent. Add -Purge to also delete its identity, settings and logs.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Uninstall %*
exit /b %ERRORLEVEL%
