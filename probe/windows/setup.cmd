@echo off
rem Vedha Agent - one-click automated install (elevates, then venv + deps + background task).
rem For a quick no-admin test instead, run:
rem   powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\"%~dp0setup.ps1\"'"
