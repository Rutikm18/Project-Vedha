@echo off
rem Elevate (UAC) and run install.ps1 with the execution policy bypassed.
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','\"%~dp0install.ps1\"'"
