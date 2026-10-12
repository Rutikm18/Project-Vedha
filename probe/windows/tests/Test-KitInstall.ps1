<#
  Unit tests for the pure helpers in kit-install.ps1 (no framework):  pwsh -NoProfile -File windows/tests/Test-KitInstall.ps1
#>
$ErrorActionPreference = 'Stop'
$script:Passed = 0
$script:Failed = @()
. (Join-Path $PSScriptRoot '..\kit-install.ps1')

function Assert-True  { param($Value, [string]$Name) if ($Value) { $script:Passed++ } else { $script:Failed += "$Name (expected true)" } }
function Assert-False { param($Value, [string]$Name) if (-not $Value) { $script:Passed++ } else { $script:Failed += "$Name (expected false)" } }
function Assert-Equal { param($Actual, $Expected, [string]$Name) if ("$Actual" -ceq "$Expected") { $script:Passed++ } else { $script:Failed += "$Name`n  expected [$Expected]`n  actual   [$Actual]" } }
function Assert-Throws { param([scriptblock]$Block, [string]$Pattern, [string]$Name)
  try { & $Block | Out-Null; $script:Failed += "$Name (did not throw)" } catch { if ($_.Exception.Message -match $Pattern) { $script:Passed++ } else { $script:Failed += "$Name`n  message: $($_.Exception.Message)" } } }

# --- values are checked before they reach a command -------------------------------------------
foreach ($ok in 'ubuntu@16.4.75.44', 'ec2-user@ec2-1-2-3-4.compute.amazonaws.com', 'server.example.com', 'me@host') { Assert-True (Test-KitServer $ok) "server ok: $ok" }
foreach ($bad in 'ubuntu@host; calc', 'a b', 'ubuntu@', '', 'u@h$(x)', "u@h'x") { Assert-False (Test-KitServer $bad) "server refused: [$bad]" }
Assert-True  (Test-KitManagerUrl 'https://api.vedhasec.com') 'manager url ok'
Assert-True  (Test-KitManagerUrl 'https://api.vedhasec.com/') 'manager url: a trailing slash is fine'
Assert-True  (Test-KitManagerUrl 'https://10.0.0.5:8443') 'manager url: host and port'
foreach ($bad in 'http://x.com', 'https://x.com/path', "https://x.com'; calc", 'api.example.com', 'https://', 'https://x y') { Assert-False (Test-KitManagerUrl $bad) "manager url refused: [$bad]" }
Assert-True  (Test-KitRemoteDir '/opt/Project-Vedha/manager') 'remote dir ok'
foreach ($bad in 'opt/x', '/opt/x y', '/opt/../etc', "/opt/x'; rm -rf /; '", '/opt/$(x)', '') { Assert-False (Test-KitRemoteDir $bad) "remote dir refused: [$bad]" }
Assert-True  (Test-KitKeyPath 'C:\Users\WZ\keys\server.pem') 'key path ok'
Assert-True  (Test-KitKeyPath 'C:\Users\Some One\.ssh\id_rsa') 'key path: spaces ok'
foreach ($bad in 'server.pem', 'C:\k\..\x.pem', "C:\k\a'b.pem", 'C:\k\a;b.pem', '') { Assert-False (Test-KitKeyPath $bad) "key path refused: [$bad]" }

# --- Python ----------------------------------------------------------------------------------------
foreach ($v in 'Python 3.10.11', 'Python 3.11.9', 'Python 3.12.4', "  Python 3.12.1`r`n") { Assert-True (Test-KitPythonOutput $v) "python ok: [$($v.Trim())]" }
foreach ($v in 'Python 3.9.13', 'Python 3.13.0', 'Python 2.7.18', '', 'python is not recognized', 'Python 3.1.2') { Assert-False (Test-KitPythonOutput $v) "python refused: [$v]" }

# --- saved settings: only well-formed values survive ------------------------------------------------
$json = ConvertTo-KitSettingsJson 'ubuntu@1.2.3.4' 'C:\k\s.pem' 'https://api.example.com' '/opt/x/manager' $true
$back = ConvertFrom-KitSettingsJson $json
Assert-Equal $back.server 'ubuntu@1.2.3.4' 'settings round trip: server'
Assert-Equal $back.ssh_key 'C:\k\s.pem' 'settings round trip: key'
Assert-Equal $back.manager_url 'https://api.example.com' 'settings round trip: manager'
Assert-Equal $back.remote_compose_dir '/opt/x/manager' 'settings round trip: folder'
Assert-True  $back.tokenless 'settings round trip: tokenless'
$evil = ConvertFrom-KitSettingsJson '{"server":"a; calc","ssh_key":"..\\x","manager_url":"http://x","remote_compose_dir":"/a b","tokenless":"yes"}'
Assert-Equal $evil.server '' 'settings: a bad server is dropped'
Assert-Equal $evil.ssh_key '' 'settings: a bad key path is dropped'
Assert-Equal $evil.manager_url '' 'settings: a bad manager url is dropped'
Assert-Equal $evil.remote_compose_dir '' 'settings: a bad folder is dropped'
Assert-False $evil.tokenless 'settings: tokenless must be exactly true'
$broken = ConvertFrom-KitSettingsJson '{not json'
Assert-Equal $broken.server '' 'settings: damaged file gives empty values, not an error'
Assert-True  ((Get-KitSettingsPath ([System.IO.Path]::GetTempPath())) -like '*.vedha*kit-settings.json') 'settings path is under .vedha'
Assert-False ($json -match 'password|passphrase|BEGIN') 'settings never hold secrets'

# --- the command run on the server -------------------------------------------------------------------
$cmd = Get-KitRemoteLayoutCommand '/opt/Project-Vedha/manager'
Assert-True  ($cmd -match "^d='/opt/Project-Vedha/manager'; ") 'layout command: the folder is single-quoted'
Assert-True  ($cmd -match 'docker ps' -and $cmd -match 'docker-compose.yml' -and $cmd -match '\.env') 'layout command checks compose file, .env and docker'
Assert-Throws { Get-KitRemoteLayoutCommand "/opt/x'; rm -rf /; '" } 'safe folder' 'layout command: a folder that could break out is refused'
$facts = Get-KitRemoteFacts "compose-file-ok`nenv-file-ok`ndocker-ok`n"
Assert-True ($facts.ComposeFile -and $facts.EnvFile -and $facts.Docker) 'facts: all ok'
$facts = Get-KitRemoteFacts "compose-file-ok`nenv-file-missing`ndocker-denied`n"
Assert-True ($facts.ComposeFile -and -not $facts.EnvFile -and -not $facts.Docker) 'facts: partly missing'
Assert-False (Get-KitRemoteFacts 'something-else').ComposeFile 'facts: unrelated output is not success'

# --- the publish arguments ----------------------------------------------------------------------------
$a = Get-KitPublishArguments -Server 'ubuntu@h' -SshKey 'C:\k\s.pem' -ManagerUrl 'https://api.example.com/' -ComposeDir '/opt/x/manager' -ReleaseDir '/opt/x/manager/agent-releases' -Tokenless $true -DryRun $false -SkipBuild $false
Assert-Equal ($a -join ' ') '-Server ubuntu@h -SshKey C:\k\s.pem -ManagerUrl https://api.example.com -ConfigureManager -RemoteComposeDir /opt/x/manager -RemoteReleaseDir /opt/x/manager/agent-releases -AllowTokenlessInstall' 'publish args: full'
$a = Get-KitPublishArguments -Server 'ubuntu@h' -SshKey '' -ManagerUrl 'https://api.example.com' -ComposeDir '' -ReleaseDir '' -Tokenless $false -DryRun $true -SkipBuild $true
Assert-Equal ($a -join ' ') '-Server ubuntu@h -ManagerUrl https://api.example.com -ConfigureManager -DryRun -SkipBuild' 'publish args: minimal'

# --- what ships must be safe for Windows PowerShell 5.1 -----------------------------------------------
$bytes = [System.IO.File]::ReadAllBytes((Join-Path $PSScriptRoot '..\kit-install.ps1'))
Assert-Equal @($bytes | Where-Object { $_ -gt 127 }).Count 0 'kit-install.ps1 is plain ASCII'
$cmdBytes = [System.IO.File]::ReadAllBytes((Join-Path $PSScriptRoot '..\kit-install.cmd'))
Assert-True ([System.Text.Encoding]::ASCII.GetString($cmdBytes).Contains("`r`n")) 'kit-install.cmd uses Windows line endings'

Write-Host ''
if ($script:Failed.Count -eq 0) { Write-Host "All $script:Passed checks passed." -ForegroundColor Green; exit 0 }
Write-Host "$($script:Failed.Count) FAILED, $script:Passed passed:" -ForegroundColor Red
$script:Failed | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
exit 1
