@echo off
rem Elevate (UAC) and run uninstall.ps1. Pass -Purge to also delete state/identity.
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\"%~dp0uninstall.ps1\"'"
