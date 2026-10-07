<#
  Unit tests for the pure helpers in install.ps1. Runs on Windows PowerShell 5.1 and PowerShell 7
  (any OS), with no test framework to install:

      pwsh -NoProfile -File windows/tests/Test-Install.ps1

  Exit code 0 = all passed. The Windows-only steps (scheduled task, permissions, enrolment) are
  exercised by the Windows CI job against the real compiled agent, not here.
#>
$ErrorActionPreference = 'Stop'
$script:Passed = 0
$script:Failed = @()

# Load the installer's functions without running it.
. (Join-Path $PSScriptRoot '..\install.ps1')

function Assert-Equal {
  param($Actual, $Expected, [string]$Name)
  if ("$Actual" -ceq "$Expected") { $script:Passed++ } else { $script:Failed += "$Name`n      expected: [$Expected]`n      actual  : [$Actual]" }
}
function Assert-True  { param($Value, [string]$Name) if ($Value) { $script:Passed++ } else { $script:Failed += "$Name (expected true)" } }
function Assert-False { param($Value, [string]$Name) if (-not $Value) { $script:Passed++ } else { $script:Failed += "$Name (expected false)" } }
function Assert-Throws {
  param([scriptblock]$Block, [string]$Pattern, [string]$Name)
  try { & $Block | Out-Null; $script:Failed += "$Name (did not throw)" }
  catch { if ($_.Exception.Message -match $Pattern) { $script:Passed++ } else { $script:Failed += "$Name`n      message: $($_.Exception.Message)`n      wanted : $Pattern" } }
}

# --- install token ------------------------------------------------------------
Assert-True  (Test-VedhaToken 'vet_AbCdEf123456_-xyz') 'token: a real-looking token is accepted'
Assert-False (Test-VedhaToken '')                     'token: empty is refused'
Assert-False (Test-VedhaToken 'vet_short')            'token: too short is refused'
Assert-False (Test-VedhaToken 'vpat_AbCdEf123456xyz') 'token: a different credential type is refused'
Assert-False (Test-VedhaToken 'vet_has space1234')    'token: spaces are refused'
Assert-False (Test-VedhaToken 'vet_x;calc1234567')    'token: shell characters are refused'

# --- manager address ------------------------------------------------------------
Assert-Equal (Resolve-VedhaManager -Given 'https://api.vedhasec.com/' -Baked '__VEDHA_MANAGER_URL__') 'https://api.vedhasec.com' 'manager: given wins and loses the trailing slash'
Assert-Equal (Resolve-VedhaManager -Given '' -Baked 'https://baked.example.com') 'https://baked.example.com' 'manager: baked value is the default'
Assert-Equal (Resolve-VedhaManager -Given '' -Baked '__VEDHA_MANAGER_URL__' -Existing 'https://old.example.com') 'https://old.example.com' 'manager: an existing install keeps its manager'
Assert-Equal (Resolve-VedhaManager -Given 'https://m.example.com:8443' -Baked '') 'https://m.example.com:8443' 'manager: a port is allowed'
Assert-Throws { Resolve-VedhaManager -Given '' -Baked '__VEDHA_MANAGER_URL__' } 'does not carry a manager address' 'manager: an unconfigured package asks for -Manager'
Assert-Throws { Resolve-VedhaManager -Given '' -Baked 'https://api.example.invalid' } 'placeholder' 'manager: the CI placeholder is refused'
Assert-Throws { Resolve-VedhaManager -Given 'http://m.example.com' -Baked '' } 'must look like https' 'manager: plain http is refused'
Assert-Throws { Resolve-VedhaManager -Given 'https://m.example.com/some/path' -Baked '' } 'must look like https' 'manager: a path is refused'
Assert-Throws { Resolve-VedhaManager -Given 'manager.example.com' -Baked '' } 'must look like https' 'manager: a bare host name is refused'

# --- scan scope -------------------------------------------------------------------
$r = ConvertTo-NetworkCidr -Address '192.168.1.77' -PrefixLength 24
Assert-Equal $r.Cidr '192.168.1.0/24' 'scope: /24 host'
Assert-Equal $r.Note '' 'scope: /24 needs no note'
Assert-Equal (ConvertTo-NetworkCidr -Address '10.20.35.200' -PrefixLength 23).Cidr '10.20.34.0/23' 'scope: /23 is kept as it is'
Assert-Equal (ConvertTo-NetworkCidr -Address '10.20.35.200' -PrefixLength 22).Cidr '10.20.32.0/22' 'scope: /22 is the widest kept as it is'
$wide = ConvertTo-NetworkCidr -Address '10.20.35.200' -PrefixLength 16
Assert-Equal $wide.Cidr '10.20.35.0/24' 'scope: a /16 is narrowed to the host''s /24'
Assert-True  ($wide.Note -match '-Scope') 'scope: narrowing says how to widen'
Assert-Equal (ConvertTo-NetworkCidr -Address '10.1.2.3' -PrefixLength 8).Cidr '10.1.2.0/24' 'scope: a /8 is narrowed too'
Assert-Equal (ConvertTo-NetworkCidr -Address '172.16.5.130' -PrefixLength 26).Cidr '172.16.5.128/26' 'scope: a /26 subnet'
Assert-Equal (ConvertTo-NetworkCidr -Address '172.16.5.130' -PrefixLength 30).Cidr '172.16.5.128/30' 'scope: a /30 link'
$single = ConvertTo-NetworkCidr -Address '172.16.5.130' -PrefixLength 32
Assert-Equal $single.Cidr '172.16.5.130/32' 'scope: /32 is that single address'
Assert-True  ($single.Note.Length -gt 0) 'scope: /32 explains itself'
Assert-Equal (ConvertTo-NetworkCidr -Address '200.100.50.25' -PrefixLength 24).Cidr '200.100.50.0/24' 'scope: high first octet does not overflow'
Assert-Throws { ConvertTo-NetworkCidr -Address 'not-an-ip' -PrefixLength 24 } 'Not an IPv4' 'scope: a bad address is refused'
Assert-Throws { ConvertTo-NetworkCidr -Address 'fe80::1' -PrefixLength 64 } 'Not an IPv4' 'scope: IPv6 is refused'
Assert-Throws { ConvertTo-NetworkCidr -Address '10.0.0.1' -PrefixLength 0 } 'Bad prefix' 'scope: prefix 0 is refused'

Assert-True  (Test-VedhaScope '192.168.1.0/24')                  'scope check: one network'
Assert-True  (Test-VedhaScope '192.168.1.0/24, 10.0.0.0/22')     'scope check: several networks'
Assert-True  (Test-VedhaScope '10.1.1.5')                        'scope check: a single address'
Assert-False (Test-VedhaScope '192.168.1.0/33')                  'scope check: prefix too large'
Assert-False (Test-VedhaScope '300.1.1.0/24')                    'scope check: octet too large'
Assert-False (Test-VedhaScope 'corporate-lan')                   'scope check: a name is refused'
Assert-False (Test-VedhaScope '192.168.1.0/24;rm')               'scope check: junk is refused'

# --- the settings file ------------------------------------------------------------
$text = New-VedhaAgentConfig -ManagerUrl 'https://m.example.com' -DataDir 'C:\ProgramData\vedha-agent' -AgentName 'PC1-probe' `
  -ScopeValue '192.168.1.0/24' -ProxyUrl 'http://proxy:3128' -CaBundlePath 'C:\ProgramData\vedha-agent\ca-bundle.pem' `
  -InstallToken 'vet_AbCdEf123456' -InstallerVersion '1.0.380' -BuildDigest 'abc123'
$cfg = Read-VedhaConfig -Text $text
Assert-Equal $cfg['PLATFORM_URL'] 'https://m.example.com' 'config: manager'
Assert-Equal $cfg['VERIFY_TLS'] 'true' 'config: TLS verification is on'
Assert-Equal $cfg['LICENSE_ENFORCED'] 'false' 'config: licence setting for the unsealed build'
Assert-Equal $cfg['PROBE_NAME'] 'PC1-probe' 'config: name'
Assert-Equal $cfg['PROBE_NETWORK_SEGMENTS'] '192.168.1.0/24' 'config: scope'
Assert-Equal $cfg['STATE_FILE'] 'C:\ProgramData\vedha-agent\state.json' 'config: identity file location'
Assert-Equal $cfg['PROBE_LOG_FILE'] 'C:\ProgramData\vedha-agent\logs\agent.log' 'config: log file location'
Assert-Equal $cfg['PROBE_STATUS_FILE'] 'C:\ProgramData\vedha-agent\status.json' 'config: status file location'
Assert-Equal $cfg['HTTPS_PROXY'] 'http://proxy:3128' 'config: proxy'
Assert-Equal $cfg['PROBE_CA_BUNDLE'] 'C:\ProgramData\vedha-agent\ca-bundle.pem' 'config: CA bundle'
Assert-Equal $cfg['PROBE_ENROLL_TOKEN'] 'vet_AbCdEf123456' 'config: install token'
Assert-Equal $cfg['PROBE_INSTALLER_VERSION'] '1.0.380' 'config: installer version'
Assert-Equal $cfg['PROBE_BUILD_DIGEST'] 'abc123' 'config: build digest'

$bare = Read-VedhaConfig -Text (New-VedhaAgentConfig -ManagerUrl 'https://m.example.com' -DataDir 'D:\x' -AgentName 'n' -ScopeValue '')
Assert-False ($bare.ContainsKey('PROBE_ENROLL_TOKEN')) 'config: no token line when there is no token'
Assert-False ($bare.ContainsKey('HTTPS_PROXY'))        'config: no proxy line when there is no proxy'
Assert-False ($bare.ContainsKey('PROBE_CA_BUNDLE'))    'config: no CA line when there is none'

Assert-Equal (Read-VedhaConfig -Text ([string][char]0xFEFF + "PLATFORM_URL=https://bom.example.com`r`n"))['PLATFORM_URL'] 'https://bom.example.com' 'config: a byte-order mark does not corrupt the first key'
Assert-Equal (Read-VedhaConfig -Text "# comment`r`n`r`nA=`"x y`"`r`nB='z'")['A'] 'x y' 'config: quotes are removed'

$noToken = Remove-VedhaTokenLine -Text $text
Assert-False ($noToken -match 'PROBE_ENROLL_TOKEN') 'token removal: the line is gone'
Assert-False ($noToken -match 'vet_')               'token removal: the value is gone'
Assert-True  ($noToken -match 'PLATFORM_URL=https://m.example.com') 'token removal: other settings are kept'
Assert-True  ($noToken.EndsWith("`r`n")) 'token removal: file still ends with a newline'

# --- secrets in kept text ----------------------------------------------------------
Assert-Equal (Hide-VedhaSecrets 'run install.cmd -Token vet_AbCdEf123456_-xyz now') 'run install.cmd -Token vet_[removed] now' 'redaction: token in a log line'
Assert-Equal (Hide-VedhaSecrets 'nothing secret here') 'nothing secret here' 'redaction: ordinary text is untouched'

# --- package integrity ---------------------------------------------------------------
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("vedha-test-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tmp | Out-Null
try {
  Set-Content -LiteralPath (Join-Path $tmp 'a.txt') -Value 'alpha' -NoNewline
  Set-Content -LiteralPath (Join-Path $tmp 'b.txt') -Value 'beta' -NoNewline
  $hashA = (Get-FileHash -LiteralPath (Join-Path $tmp 'a.txt') -Algorithm SHA256).Hash.ToLower()
  $hashB = (Get-FileHash -LiteralPath (Join-Path $tmp 'b.txt') -Algorithm SHA256).Hash.ToLower()
  $sums = Join-Path $tmp 'SHA256SUMS.txt'
  Set-Content -LiteralPath $sums -Value @("$hashA  a.txt", "$hashB  b.txt")
  Assert-Equal (@(Test-PackageHashes -Root $tmp -SumsFile $sums)).Count 0 'integrity: an intact package passes'

  Set-Content -LiteralPath (Join-Path $tmp 'b.txt') -Value 'tampered' -NoNewline
  $bad = @(Test-PackageHashes -Root $tmp -SumsFile $sums)
  Assert-Equal $bad.Count 1 'integrity: one changed file is one problem'
  Assert-True  ($bad[0] -match 'Changed or damaged: b.txt') 'integrity: the changed file is named'

  Remove-Item -LiteralPath (Join-Path $tmp 'a.txt')
  $missing = @(Test-PackageHashes -Root $tmp -SumsFile $sums)
  Assert-True  ($missing -contains 'Missing: a.txt') 'integrity: a missing file is named'

  Assert-True  ((@(Test-PackageHashes -Root $tmp -SumsFile (Join-Path $tmp 'nope.txt')))[0] -match 'missing from the package') 'integrity: no sums file is a problem'
  Set-Content -LiteralPath $sums -Value @('this is not a hash line')
  Assert-True  ((@(Test-PackageHashes -Root $tmp -SumsFile $sums))[0] -match 'Unreadable line') 'integrity: a garbled sums file is a problem'
} finally { Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue }

# --- permissions check -------------------------------------------------------------------
$locked = @('C:\ProgramData\vedha-agent NT AUTHORITY\SYSTEM:(OI)(CI)(F)', '                   BUILTIN\Administrators:(OI)(CI)(F)', '', 'Successfully processed 1 files; Failed processing 0 files')
$open   = $locked + '                   BUILTIN\Users:(OI)(CI)(RX)'
$everyone = $locked + '                   Everyone:(OI)(CI)(R)'
Assert-True  (Test-AclLocked $locked)   'permissions: SYSTEM + Administrators only is locked'
Assert-False (Test-AclLocked $open)     'permissions: Users present is not locked'
Assert-False (Test-AclLocked $everyone) 'permissions: Everyone present is not locked'
Assert-False (Test-AclLocked @('NT AUTHORITY\SYSTEM:(F)')) 'permissions: Administrators missing is not accepted'

# --- progress text -------------------------------------------------------------------------
Assert-Equal (Get-StatusLine ([pscustomobject]@{ state = 'online' })) 'connected' 'status text: online'
Assert-True  ((Get-StatusLine ([pscustomobject]@{ state = 'retrying'; reason = 'no route' })) -match 'no route') 'status text: retrying shows the reason'
Assert-True  ((Get-StatusLine ([pscustomobject]@{ state = 'failed'; reason = 'gave up' })) -match 'gave up') 'status text: failed shows the reason'

# --- what ships to customers must be safe for Windows PowerShell 5.1 ---------------------------
foreach ($name in 'install.ps1', 'uninstall.ps1') {
  $bytes = [System.IO.File]::ReadAllBytes((Join-Path $PSScriptRoot "..\$name"))
  $nonAscii = @($bytes | Where-Object { $_ -gt 127 }).Count
  Assert-Equal $nonAscii 0 "$name is plain ASCII (Windows PowerShell 5.1 misreads anything else)"
}
$cmdBytes = [System.IO.File]::ReadAllBytes((Join-Path $PSScriptRoot '..\install.cmd'))
Assert-True ([System.Text.Encoding]::ASCII.GetString($cmdBytes).Contains("`r`n")) 'install.cmd uses Windows line endings'

# --- report ------------------------------------------------------------------------------------
Write-Host ''
Write-Host "install.ps1 helpers: $script:Passed passed, $($script:Failed.Count) failed"
foreach ($f in $script:Failed) { Write-Host "  FAIL: $f" -ForegroundColor Red }
exit ($(if ($script:Failed.Count -eq 0) { 0 } else { 1 }))
