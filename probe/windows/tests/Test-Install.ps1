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
Assert-Equal $cfg['PROBE_RESULT_DIR'] 'C:\ProgramData\vedha-agent\results' 'config: scan results are archived in the locked data folder'
Assert-Equal $cfg['LICENSE_ENFORCED'] 'false' 'config: licence setting for the unsealed build'
Assert-Equal $cfg['PROBE_KEEP_RETRYING'] 'true' 'config: the agent keeps retrying an unreachable manager instead of exiting'
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
  Assert-Equal (Get-VedhaSha256 -Path (Join-Path $tmp 'a.txt')) $hashA 'hash: .NET SHA-256 matches Get-FileHash'
  Assert-Equal (Get-VedhaSha256 -Path (Join-Path $tmp 'b.txt')) $hashB 'hash: .NET SHA-256 matches Get-FileHash (second file)'
  Assert-Equal (Get-VedhaSha256 -Path (Join-Path $tmp 'a.txt')).Length 64 'hash: 64 lower-case hex characters'
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

# --- folder removal and module path ---------------------------------------------------------
$doomed = Join-Path ([System.IO.Path]::GetTempPath()) ("vedha-rm-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path (Join-Path $doomed 'logs') -Force | Out-Null
Set-Content -LiteralPath (Join-Path $doomed 'logs\x.log') -Value 'x'
Assert-True (Remove-VedhaFolder -Path $doomed) 'remove folder: a folder with files is removed'
Assert-False (Test-Path -LiteralPath $doomed) 'remove folder: it is really gone'
Assert-True (Remove-VedhaFolder -Path $doomed) 'remove folder: a folder that is already gone counts as removed'

$modulePathBefore = $env:PSModulePath
Reset-WindowsPowerShellModulePath
if ($PSVersionTable.PSEdition -eq 'Desktop') {
  Assert-True  ($env:PSModulePath -like "*$PSHOME*") 'module path: Windows PowerShell gets its own folder back'
  Assert-False ($env:PSModulePath -match '\\PowerShell\\7') 'module path: PowerShell 7 folders are not inherited'
} else {
  Assert-Equal $env:PSModulePath $modulePathBefore 'module path: PowerShell 7 is left alone'
}
$env:PSModulePath = $modulePathBefore

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

# --- updating an agent that is already installed ------------------------------------------------
# Seen in the field: a download folder holding agent 2.2.0 was run over a working newer agent and
# replaced it with a build that cannot open its live connection. Nothing compared versions.
Assert-Equal (Get-VedhaVersionNumber 'Vedha Probe 2.2.0') '2.2.0' 'version: read from the agent''s own output'
Assert-Equal (Get-VedhaVersionNumber "Vedha Probe 2.10.3`r`n") '2.10.3' 'version: two digits compare as numbers, not text'
Assert-Equal (Get-VedhaVersionNumber 'Vedha agent 2.2.7-rc1 on win32') '2.2.7' 'version: a suffix is ignored'
Assert-True  ($null -eq (Get-VedhaVersionNumber 'Unknown command: version')) 'version: no number is $null'
Assert-True  ($null -eq (Get-VedhaVersionNumber '')) 'version: empty text is $null'
Assert-True  ([version]'2.10.0' -gt [version]'2.9.0') 'version: 2.10.0 is newer than 2.9.0'

$v220 = [version]'2.2.0'; $v223 = [version]'2.2.3'
$p = Get-VedhaUpdatePlan -InstalledPresent $false -Installed $null -Package $v223
Assert-Equal $p.Kind 'fresh' 'plan: nothing installed is a fresh install'
Assert-True  $p.Allowed 'plan: a fresh install is allowed'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed $v220 -Package $v223
Assert-Equal $p.Kind 'upgrade' 'plan: a newer package is an update'
Assert-True  ($p.Allowed -and $p.Message -match '2\.2\.0 -> 2\.2\.3') 'plan: an update says from which version to which'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed $v223 -Package $v223
Assert-Equal $p.Kind 'same' 'plan: the same version is a re-apply'
Assert-True  $p.Allowed 'plan: re-applying the same version is allowed'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed $v223 -Package $v220
Assert-Equal $p.Kind 'downgrade' 'plan: an older package is a downgrade'
Assert-False $p.Allowed 'plan: a downgrade is refused by default'
Assert-True  ($p.Message -match 'OLDER than the installed agent') 'plan: the refusal explains itself'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed $v223 -Package $v220 -AllowDowngrade
Assert-Equal $p.Kind 'downgrade' 'plan: -AllowDowngrade is still reported as a downgrade'
Assert-True  ($p.Allowed -and $p.Message -match 'AllowDowngrade') 'plan: -AllowDowngrade permits it and says why'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed ([version]'2.2.10') -Package ([version]'2.2.9')
Assert-False $p.Allowed 'plan: 2.2.10 is newer than 2.2.9, so installing 2.2.9 is a downgrade'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed $null -Package $v223
Assert-Equal $p.Kind 'unknown' 'plan: an installed agent whose version cannot be read'
Assert-True  $p.Allowed 'plan: a broken installed program may be replaced'
$p = Get-VedhaUpdatePlan -InstalledPresent $true -Installed $v223 -Package $null
Assert-True  ($p.Kind -eq 'unknown' -and $p.Allowed) 'plan: an unreadable package version does not block'

# --- settings the operator added by hand survive an update --------------------------------------
$oldCfg = (New-VedhaAgentConfig -ManagerUrl 'https://old.example.com' -DataDir 'C:\ProgramData\vedha-agent' -AgentName 'PC1-probe' `
  -ScopeValue '192.168.1.0/24' -InstallToken 'vet_AbCdEf123456') + "PROBE_DEBUG=1`r`n# my note`r`nPROBE_MAX_FULL_SCAN_SECONDS=86400`r`nNO_PROXY=a.example.com,b.example.com`r`nWEIRD=x=y`r`n"
$extra = @(Get-VedhaExtraSettingLines -ExistingText $oldCfg)
Assert-Equal $extra.Count 4 'extras: only the hand-added settings are picked'
Assert-True  ($extra -contains 'PROBE_DEBUG=1') 'extras: PROBE_DEBUG kept'
Assert-True  ($extra -contains 'PROBE_MAX_FULL_SCAN_SECONDS=86400') 'extras: the deep-scan ceiling kept'
Assert-True  ($extra -contains 'WEIRD=x=y') 'extras: a value containing = is kept whole'
Assert-False ($extra -match 'PLATFORM_URL|PROBE_NAME|PROBE_ENROLL_TOKEN|vet_') 'extras: managed settings and the used token are not carried over'
$fresh = New-VedhaAgentConfig -ManagerUrl 'https://new.example.com' -DataDir 'C:\ProgramData\vedha-agent' -AgentName 'PC1-probe' -ScopeValue '10.0.0.0/24'
$merged = Add-VedhaExtraSettings -ConfigText $fresh -ExtraLines $extra
$mc = Read-VedhaConfig -Text $merged
Assert-Equal $mc['PLATFORM_URL'] 'https://new.example.com' 'merge: a managed setting takes the NEW value'
Assert-Equal $mc['PROBE_NETWORK_SEGMENTS'] '10.0.0.0/24' 'merge: scope takes the new value'
Assert-Equal $mc['PROBE_DEBUG'] '1' 'merge: the hand-added setting is still there'
Assert-Equal $mc['NO_PROXY'] 'a.example.com,b.example.com' 'merge: a list value is intact'
Assert-False ($mc.ContainsKey('PROBE_ENROLL_TOKEN')) 'merge: no install token is resurrected'
$again = Add-VedhaExtraSettings -ConfigText $fresh -ExtraLines @(Get-VedhaExtraSettingLines -ExistingText $merged)
Assert-Equal $again $merged 'merge: repeating the update changes nothing (no duplicates)'
Assert-Equal (Add-VedhaExtraSettings -ConfigText $fresh -ExtraLines @()) $fresh 'merge: nothing to keep leaves the text untouched'
Assert-Equal @(Get-VedhaExtraSettingLines -ExistingText '').Count 0 'extras: an empty file has none'

# --- scan results kept inside the old program folder are saved, not deleted ----------------------
$root = Join-Path ([System.IO.Path]::GetTempPath()) ("vedha-legacy-" + [guid]::NewGuid().ToString('N'))
try {
  $old = Join-Path $root 'Vedha Agent.old\result'
  $data = Join-Path $root 'data'
  New-Item -ItemType Directory -Force -Path (Join-Path $old 'job1'), $data | Out-Null
  Set-Content -LiteralPath (Join-Path $old 'job1\a.json') -Value '{"a":1}'
  Set-Content -LiteralPath (Join-Path $old 'b.json') -Value '{"b":2}'
  Assert-Equal (Copy-VedhaLegacyResults -LegacyDir (Join-Path $root 'nowhere') -DataDir $data) 0 'results: no old folder means nothing to save'
  $saved = Copy-VedhaLegacyResults -LegacyDir $old -DataDir $data
  Assert-Equal $saved 2 'results: every file is counted, including those in sub-folders'
  $copies = @(Get-ChildItem -LiteralPath (Join-Path $data 'results') -Recurse -File)
  Assert-Equal $copies.Count 2 'results: both files arrived in the data folder'
  Assert-True  ($copies | Where-Object { $_.Name -eq 'a.json' -and $_.FullName -match 'from-program-files-' }) 'results: kept in a dated folder, sub-folders preserved'
  Assert-Equal (@(Get-ChildItem -LiteralPath $old -Recurse -File).Count) 2 'results: the source is untouched until the caller removes it'
  $empty = Join-Path $root 'empty'; New-Item -ItemType Directory -Path $empty | Out-Null
  Assert-Equal (Copy-VedhaLegacyResults -LegacyDir $empty -DataDir $data) 0 'results: an empty folder means nothing to save'
} finally { Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue }

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
