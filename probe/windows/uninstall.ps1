<#
  Vedha Agent — remove the Scheduled Task. Add -Purge to also delete the
  identity/state/logs under C:\ProgramData\vedha-agent.
#>
[CmdletBinding()]
param([switch]$Purge)
$ErrorActionPreference = 'SilentlyContinue'

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) { Write-Error 'Administrator required. Right-click uninstall.cmd -> Run as administrator.'; exit 1 }

Stop-ScheduledTask       -TaskName 'VedhaAgent'
Unregister-ScheduledTask -TaskName 'VedhaAgent' -Confirm:$false
Write-Host 'VedhaAgent task removed.'

if ($Purge) {
  Remove-Item (Join-Path $env:ProgramData 'vedha-agent') -Recurse -Force
  Write-Host 'Purged C:\ProgramData\vedha-agent (identity + logs deleted).'
} else {
  Write-Host 'Kept C:\ProgramData\vedha-agent (identity/logs). Re-run with -Purge to delete.'
}
