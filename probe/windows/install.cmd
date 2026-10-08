@echo off
rem Vedha agent installer for Windows.
rem   install.cmd -Token vet_XXXXXXXX        install and connect (token from Fleet > Add agent)
rem   install.cmd -Repair                    re-apply and re-check an existing installation
rem   install.cmd -Uninstall [-Purge]        remove the agent
rem Options such as -Proxy, -CaBundle, -Scope, -Name are passed straight through (see README.txt).
rem The execution policy is bypassed for this one script; install.ps1 asks for administrator rights itself.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
exit /b %ERRORLEVEL%
