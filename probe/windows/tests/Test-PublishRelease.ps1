<#
  Unit tests for the pure helpers in publish-release.ps1 and for its argument checks. Runs on
  Windows PowerShell 5.1 and PowerShell 7 (any OS), no test framework needed:

      pwsh -NoProfile -File windows/tests/Test-PublishRelease.ps1

  The steps that need Windows, a compiler and a server (build, sign, upload, restart) are run by
  a person; -DryRun is what is exercised here.
#>
$ErrorActionPreference = 'Stop'
$script:Passed = 0
$script:Failed = @()
$script = Join-Path $PSScriptRoot '..\publish-release.ps1'
. $script

function Assert-Equal { param($Actual, $Expected, [string]$Name) if ("$Actual" -ceq "$Expected") { $script:Passed++ } else { $script:Failed += "$Name`n      expected: [$Expected]`n      actual  : [$Actual]" } }
function Assert-True  { param($Value, [string]$Name) if ($Value) { $script:Passed++ } else { $script:Failed += "$Name (expected true)" } }
function Assert-False { param($Value, [string]$Name) if (-not $Value) { $script:Passed++ } else { $script:Failed += "$Name (expected false)" } }
function Assert-Throws {
  param([scriptblock]$Block, [string]$Pattern, [string]$Name)
  try { & $Block | Out-Null; $script:Failed += "$Name (did not throw)" }
  catch { if ($_.Exception.Message -match $Pattern) { $script:Passed++ } else { $script:Failed += "$Name`n      message: $($_.Exception.Message)`n      wanted : $Pattern" } }
}

# --- server, path, url ---------------------------------------------------------
Assert-True  (Test-VedhaServerSpec 'ubuntu@203.0.113.10')      'server: user@ip'
Assert-True  (Test-VedhaServerSpec 'deploy@api.example.com')   'server: user@host'
Assert-True  (Test-VedhaServerSpec 'api.example.com')          'server: bare host'
Assert-False (Test-VedhaServerSpec 'a b@host')                 'server: space refused'
Assert-False (Test-VedhaServerSpec 'u@h;rm -rf /')             'server: shell characters refused'
Assert-False (Test-VedhaServerSpec 'u@h -oProxyCommand=x')     'server: option injection refused'
Assert-False (Test-VedhaServerSpec '')                          'server: empty refused'

Assert-True  (Test-VedhaRemotePath '/opt/Project-Vedha/manager/agent-releases') 'path: normal'
Assert-False (Test-VedhaRemotePath 'relative/path')            'path: must be absolute'
Assert-False (Test-VedhaRemotePath '/opt/a b')                 'path: space refused'
Assert-False (Test-VedhaRemotePath "/opt/a'; rm -rf /; '")     'path: quote refused'
Assert-False (Test-VedhaRemotePath '/opt/../etc')              'path: .. refused'
Assert-Equal (Get-VedhaParentPath '/opt/Project-Vedha/manager/agent-releases') '/opt/Project-Vedha/manager' 'parent: normal'
Assert-Equal (Get-VedhaParentPath '/opt/Project-Vedha/manager/agent-releases/') '/opt/Project-Vedha/manager' 'parent: trailing slash'
Assert-Equal (Get-VedhaParentPath '/agent-releases') '/' 'parent: top level'

Assert-True  (Test-VedhaHttpsUrl 'https://api.vedhasec.com')   'url: https'
Assert-True  (Test-VedhaHttpsUrl 'https://api.vedhasec.com:8443/') 'url: port and slash'
Assert-False (Test-VedhaHttpsUrl 'http://api.vedhasec.com')    'url: http refused'
Assert-False (Test-VedhaHttpsUrl 'https://a.com/path')         'url: path refused'
Assert-False (Test-VedhaHttpsUrl 'MANAGER')                    'url: placeholder refused'

$ed   = 'AGENT_RELEASE_PUBLIC_KEY=' + ('A' * 43) + '='
$p256 = 'AGENT_RELEASE_P256_PUBLIC_KEY=' + ('B' * 90) + '=='
Assert-True  (Test-VedhaKeyLine $ed)   'key line: Ed25519'
Assert-True  (Test-VedhaKeyLine $p256) 'key line: P-256'
Assert-False (Test-VedhaKeyLine 'AGENT_RELEASE_PUBLIC_KEY=abc')                 'key line: too short'
Assert-False (Test-VedhaKeyLine "AGENT_RELEASE_PUBLIC_KEY=$('A' * 30)'; rm x")   'key line: quote refused'
Assert-False (Test-VedhaKeyLine 'OTHER=AAAAAAAAAAAAAAAAAAAAAAAAAAAA')            'key line: other name refused'

# --- the script sent to the manager ----------------------------------------------
$lines = @($ed, $p256, 'AGENT_RELEASE_REQUIRE_SIGNATURE=true', 'MANAGER_PUBLIC_URL=https://api.vedhasec.com')
$sh = New-VedhaRemoteConfigScript -ComposeDir '/opt/Project-Vedha/manager' -Lines $lines
Assert-True  ($sh.EndsWith("`n") -and $sh -notmatch "`r") 'remote script: LF line endings only (a CR would break sh)'
Assert-True  ($sh.StartsWith("set -eu`n")) 'remote script: stops on the first error'
Assert-True  ($sh.StartsWith("set -eu`numask 077`n")) 'remote script: files it creates are private (umask 077) before anything is written'
Assert-True  ($sh -match 'cp -p \.env') 'remote script: the backup keeps the original permissions'
Assert-True  ($sh.IndexOf('umask 077') -lt $sh.IndexOf('.env.new')) 'remote script: the umask is set before the temporary copy of .env exists'
Assert-True  ($sh -match "cd '/opt/Project-Vedha/manager'") 'remote script: goes to the compose folder'
Assert-True  ($sh -match '\.env\.bak\.') 'remote script: keeps a dated backup first'
Assert-True  ($sh.IndexOf('cp .env') -lt $sh.IndexOf('grep -v')) 'remote script: backup happens before any change'
Assert-True  ($sh -match "grep -v -E '\^\(AGENT_RELEASE_PUBLIC_KEY\|AGENT_RELEASE_P256_PUBLIC_KEY\|AGENT_RELEASE_REQUIRE_SIGNATURE\|MANAGER_PUBLIC_URL\)='") 'remote script: removes only the four settings it owns'
Assert-True  ($sh -match [regex]::Escape("'$ed'")) 'remote script: writes the Ed25519 key'
Assert-True  ($sh -match [regex]::Escape("'$p256'")) 'remote script: writes the P-256 key'
Assert-True  ($sh -match 'cat \.env\.new > \.env') 'remote script: rewrites in place (keeps owner and mode)'
Assert-True  ($sh.TrimEnd().EndsWith('echo "[manager] api restarted"')) 'remote script: restarts the api last'
Assert-True  ($sh.IndexOf('docker compose up -d api') -gt $sh.IndexOf('cat .env.new > .env')) 'remote script: restart comes after the write'
$shT = New-VedhaRemoteConfigScript -ComposeDir '/opt/Project-Vedha/manager' -Lines ($lines + 'AGENT_ALLOW_TOKENLESS_INSTALL=true')
Assert-True  ($shT -match "AGENT_ALLOW_TOKENLESS_INSTALL=true'") 'remote script: writes the tokenless switch when asked'
Assert-True  ($shT -match "MANAGER_PUBLIC_URL\|AGENT_ALLOW_TOKENLESS_INSTALL\)='") 'remote script: removes the old tokenless line only when it is writing one'
Assert-False ($sh -match 'AGENT_ALLOW_TOKENLESS_INSTALL') 'remote script: without the switch the tokenless setting is neither written nor removed'
Assert-Throws { New-VedhaRemoteConfigScript -ComposeDir '/opt/x' -Lines @('AGENT_ALLOW_TOKENLESS_INSTALL=false') } 'unexpected line' 'remote script: only the value true can be written'
Assert-Throws { New-VedhaRemoteConfigScript -ComposeDir '/opt/x y' -Lines $lines } 'safe folder' 'remote script: unsafe folder refused'
Assert-Throws { New-VedhaRemoteConfigScript -ComposeDir '/opt/x' -Lines @("FOO=bar") } 'unexpected line' 'remote script: only the expected settings are written'
Assert-Throws { New-VedhaRemoteConfigScript -ComposeDir '/opt/x' -Lines @("MANAGER_PUBLIC_URL=https://a.com'; rm -rf /") } 'unexpected line' 'remote script: injection in a value refused'

# --- the ssh key option ------------------------------------------------------------
Assert-True  (Test-VedhaSshKeyPath 'C:\Users\WZ\keys\server.pem') 'ssh key: a normal Windows path is accepted'
Assert-True  (Test-VedhaSshKeyPath 'C:\Users\Some One\.ssh\id_rsa') 'ssh key: spaces and dots in folder names are fine'
Assert-False (Test-VedhaSshKeyPath 'server.pem') 'ssh key: a relative path is refused'
Assert-False (Test-VedhaSshKeyPath 'C:\keys\a.pem; calc') 'ssh key: shell characters are refused'
Assert-False (Test-VedhaSshKeyPath 'C:\keys\..\x.pem') 'ssh key: .. is refused'
Assert-False (Test-VedhaSshKeyPath "C:\keys\a'b.pem") 'ssh key: quotes are refused'
Assert-Equal ((Get-VedhaSshArgs 'C:\k\s.pem') -join ' ') '-i C:\k\s.pem -o StrictHostKeyChecking=accept-new' 'ssh key: -i, the path, then the trust option'
Assert-Equal ((Get-VedhaSshArgs '') -join ' ') '-o StrictHostKeyChecking=accept-new' 'ssh key: with no key only the trust option (no host-key question)'

# --- the python option ----------------------------------------------------------------
Assert-True  (Test-VedhaPythonExe 'C:\Users\WZ\AppData\Local\Programs\Python\Python312\python.exe') 'python exe: a normal path is accepted'
Assert-True  (Test-VedhaPythonExe 'C:\Program Files\Python312\python.exe') 'python exe: Program Files is fine'
foreach ($bad in 'python', 'C:\p\python.bat', 'C:\p\..\python.exe', "C:\p'q\python.exe", 'C:\p;calc\python.exe', 'python.exe') { Assert-False (Test-VedhaPythonExe $bad) "python exe refused: [$bad]" }

# --- the plan ------------------------------------------------------------------
$full = Get-VedhaPlan -HasServer $true -Configure $true -HasUrl $true -Skip $false
Assert-Equal $full.Count 8 'plan: all eight steps when everything is given'
$local = Get-VedhaPlan -HasServer $false -Configure $false -HasUrl $false -Skip $false
Assert-Equal $local.Count 5 'plan: five steps without a server'
Assert-True  ((Get-VedhaPlan -HasServer $true -Configure $false -HasUrl $false -Skip $true) -contains 'reuse the agent already built (-SkipBuild)') 'plan: -SkipBuild is shown'
Assert-False ((Get-VedhaPlan -HasServer $true -Configure $false -HasUrl $true -Skip $false) -match 'restart the api') 'plan: no restart step without -ConfigureManager'

# --- running it: argument checks and -DryRun (nothing is executed) ----------------
function Invoke-Script { param([string[]]$Arguments)
  $out = & pwsh -NoProfile -File $script @Arguments 2>&1 | Out-String
  return @{ Code = $LASTEXITCODE; Out = $out } }
$r = Invoke-Script @('-DryRun', '-Server', 'ubuntu@203.0.113.10', '-ManagerUrl', 'https://api.vedhasec.com', '-ConfigureManager')
Assert-Equal $r.Code 0 'dry run: succeeds'
Assert-True  ($r.Out -match 'Dry run: nothing was done') 'dry run: says it did nothing'
Assert-True  ($r.Out -match '8\. ask the manager') 'dry run: lists all eight steps'
$r = Invoke-Script @('-DryRun')
Assert-True  ($r.Code -eq 0 -and $r.Out -match '5\. build and sign the release') 'dry run: without a server it plans to stop after signing'
$r = Invoke-Script @('-DryRun', '-Server', 'a b@c')
Assert-True  ($r.Code -eq 1 -and $r.Out -match 'FAILED: -Server must look like') 'bad server is refused with a sentence'
$r = Invoke-Script @('-DryRun', '-Server', 'u@h', '-ManagerUrl', 'http://api.example.com')
Assert-True  ($r.Code -eq 1 -and $r.Out -match 'https://') 'http manager address is refused'
$r = Invoke-Script @('-DryRun', '-ConfigureManager', '-Server', 'u@h')
Assert-True  ($r.Code -eq 1 -and $r.Out -match 'needs both -Server and -ManagerUrl') '-ConfigureManager needs a server and an address'
$r = Invoke-Script @('-DryRun', '-Version', 'bad version')
Assert-True  ($r.Code -eq 1 -and $r.Out -match 'not valid') 'a bad version is refused'
if ($env:OS -ne 'Windows_NT') {
  $r = Invoke-Script @('-Server', 'u@h')
  Assert-True ($r.Code -eq 1 -and $r.Out -match 'Run this on Windows') 'on a non-Windows machine it stops before doing anything'
}

# --- the file itself ------------------------------------------------------------
$bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $script))
Assert-True  (-not ($bytes | Where-Object { $_ -gt 127 })) 'file is ASCII only (Windows PowerShell 5.1 reads BOM-less files as ANSI)'
$errors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $script), [ref]$null, [ref]$errors)
Assert-Equal $errors.Count 0 'file parses'
$ast = [System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $script), [ref]$null, [ref]$null)
$ps7 = $ast.FindAll({ param($n) $n.GetType().Name -in @('PipelineChainAst', 'TernaryExpressionAst', 'NullConditionalMemberExpressionAst') -or
                       ($n -is [System.Management.Automation.Language.BinaryExpressionAst] -and "$($n.Operator)" -match 'QuestionQuestion') }, $true)
Assert-Equal @($ps7).Count 0 'file avoids PowerShell 7-only syntax (&&, ||, ?:, ??, ?.)'

Write-Host ''
if ($script:Failed.Count -gt 0) {
  Write-Host "FAILED ($($script:Failed.Count)):" -ForegroundColor Red
  $script:Failed | ForEach-Object { Write-Host "  - $_" }
  exit 1
}
Write-Host "All $($script:Passed) checks passed." -ForegroundColor Green
exit 0
