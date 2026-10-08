<#
  Vedha agent - remove it. Kept so older instructions still work; it simply runs install.ps1 -Uninstall.
  Add -Purge to also delete the agent's identity, settings and logs.
#>
[CmdletBinding()]
param([switch]$Purge)
& (Join-Path $PSScriptRoot 'install.ps1') -Uninstall -Purge:$Purge
exit $LASTEXITCODE
