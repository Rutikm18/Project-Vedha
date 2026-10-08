<#
  Tests for hosting\get.ps1: its helper functions, and the whole download -> verify -> unpack path
  against a throw-away web server on this computer (127.0.0.1). Nothing is installed.

      pwsh -NoProfile -File probe/windows/hosting/tests/Test-Get.ps1
      powershell -NoProfile -ExecutionPolicy Bypass -File probe\windows\hosting\tests\Test-Get.ps1   (Windows PowerShell 5.1)

  Needs Python on the PATH (python3 or python) for the throw-away server.
#>
$ErrorActionPreference = 'Stop'
$script:Passed = 0
$script:Failed = @()
function Assert-True  { param($Value, [string]$Name) if ($Value) { $script:Passed++ } else { $script:Failed += "$Name (expected true)" } }
function Assert-False { param($Value, [string]$Name) if (-not $Value) { $script:Passed++ } else { $script:Failed += "$Name (expected false)" } }
function Assert-Equal { param($Actual, $Expected, [string]$Name) if ("$Actual" -ceq "$Expected") { $script:Passed++ } else { $script:Failed += "$Name (expected '$Expected', got '$Actual')" } }
function Assert-Throws {
  param([scriptblock]$Body, [string]$Pattern, [string]$Name)
  try { & $Body | Out-Null; $script:Failed += "$Name (did not throw)" }
  catch { if ($_.Exception.Message -match $Pattern) { $script:Passed++ } else { $script:Failed += "$Name (wrong message: $($_.Exception.Message))" } }
}

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$getScript = Join-Path (Split-Path -Parent $here) 'get.ps1'
. $getScript          # dot-sourcing defines the functions and runs nothing

# --- address ----------------------------------------------------------------------------------
Assert-Equal (Resolve-GetBaseUrl 'https://downloads.example.com/windows/') 'https://downloads.example.com/windows' 'base url: https, trailing slash removed'
Assert-Equal (Resolve-GetBaseUrl 'http://127.0.0.1:8765/windows') 'http://127.0.0.1:8765/windows' 'base url: http is allowed for this computer'
Assert-Equal (Resolve-GetBaseUrl 'http://localhost:9/x') 'http://localhost:9/x' 'base url: http://localhost is allowed'
Assert-Throws { Resolve-GetBaseUrl 'http://downloads.example.com/windows' } 'https' 'base url: http to another host is refused'
Assert-Throws { Resolve-GetBaseUrl 'ftp://x/y' } 'https' 'base url: other schemes are refused'
Assert-Throws { Resolve-GetBaseUrl 'https://x.example.com/a b' } 'https' 'base url: spaces are refused'
Assert-Throws { Resolve-GetBaseUrl '__VEDHA_DOWNLOAD_BASE__' } 'does not say where' 'base url: an unfilled placeholder is refused'
Assert-Throws { Resolve-GetBaseUrl '' } 'does not say where' 'base url: empty is refused'

# --- values -------------------------------------------------------------------------------------
Assert-True  (Test-GetSha256Text ('a' * 64))                       'sha256 text: 64 hex'
Assert-True  (Test-GetSha256Text ('A1' * 32))                      'sha256 text: upper case is fine'
Assert-False (Test-GetSha256Text ('a' * 63))                       'sha256 text: 63 is not'
Assert-False (Test-GetSha256Text ('g' * 64))                       'sha256 text: not hex'
Assert-True  (Test-GetVersionText '2.2.2')                         'version: x.y.z'
Assert-True  (Test-GetVersionText '10.0')                          'version: x.y'
Assert-False (Test-GetVersionText 'latest')                        'version: a word is not a version'
Assert-False (Test-GetVersionText '2.2.2/../x')                    'version: a path is not a version'
Assert-True  (Test-GetTokenText 'vet_AbCdEf123456_-xyz')           'token: shape ok'
Assert-False (Test-GetTokenText 'vet_short')                       'token: too short'
Assert-False (Test-GetTokenText 'vet_abc def123456')               'token: space'
Assert-False (Test-GetTokenText 'vet_abcdef123456&calc')           'token: shell characters'

# --- release information ------------------------------------------------------------------------
$good = '{"schema":1,"version":"2.2.2","sha256":"' + ('ab' * 32) + '","zip":"2.2.2/vedha-agent-win.zip"}'
$rel = ConvertFrom-GetRelease $good
Assert-Equal $rel.Version '2.2.2' 'release: version'
Assert-Equal $rel.Zip '2.2.2/vedha-agent-win.zip' 'release: zip path'
Assert-Throws { ConvertFrom-GetRelease 'not json' } 'not valid' 'release: not JSON'
Assert-Throws { ConvertFrom-GetRelease ('{"version":"x","sha256":"' + ('ab' * 32) + '","zip":"a.zip"}') } 'valid version' 'release: bad version'
Assert-Throws { ConvertFrom-GetRelease '{"version":"1.0.0","sha256":"zz","zip":"a.zip"}' } 'valid SHA-256' 'release: bad hash'
foreach ($bad in 'https://evil.example/x.zip', '../x.zip', '/etc/x.zip', 'a\b.zip', 'C:/x.zip', 'a.exe') {
  Assert-Throws { ConvertFrom-GetRelease ('{"version":"1.0.0","sha256":"' + ('ab' * 32) + '","zip":"' + ($bad -replace '\\', '\\') + '"}') } 'unsafe file' "release: unsafe zip path '$bad'"
}

# --- installer arguments --------------------------------------------------------------------------
$a = Get-InstallerArguments -Token 'vet_AbCdEf123456' -Manager 'https://m.example.com' -Scope '10.0.0.0/24' -Proxy '' -CaBundle '' -Name 'PC 1' -TokenFile '' -Rest @('-SkipPreflight', '-NoWait')
Assert-Equal ($a -join '|') '-Token|vet_AbCdEf123456|-Manager|https://m.example.com|-Scope|10.0.0.0/24|-Name|PC 1|-SkipPreflight|-NoWait' 'arguments: built in order, empty ones left out'
$none = Get-InstallerArguments -Token '' -Manager '' -Scope '' -Proxy '' -CaBundle '' -Name '' -TokenFile '' -Rest @()
Assert-Equal $none.Count 0 'arguments: nothing given, nothing passed'
Assert-Throws { Get-InstallerArguments -Token 'notatoken' -Manager '' -Scope '' -Proxy '' -CaBundle '' -Name '' -TokenFile '' -Rest @() } 'install token' 'arguments: a bad token is refused'
Assert-Throws { Get-InstallerArguments -Token '' -Manager 'https://m"x' -Scope '' -Proxy '' -CaBundle '' -Name '' -TokenFile '' -Rest @() } 'not allowed' 'arguments: a quote in a value is refused'

# --- hashing ----------------------------------------------------------------------------------------
$work = Join-Path ([System.IO.Path]::GetTempPath()) ('vedha-get-test-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $work | Out-Null
$server = $null
try {
  [System.IO.File]::WriteAllText((Join-Path $work 'x.txt'), 'alpha')
  Assert-Equal (Get-GetSha256 (Join-Path $work 'x.txt')) '8ed3f6ad685b959ead7022518e1af76cd816f8e8ec7ccdda1ed4018e8f2223f8' 'hash: SHA-256 of "alpha"'

  # --- the whole download, against a web server on this computer ------------------------------------
  $python = $null
  foreach ($candidate in 'python3', 'python') { if (-not $python -and (Get-Command $candidate -ErrorAction SilentlyContinue)) { $python = $candidate } }
  if (-not $python) {
    $script:Failed += 'no Python on the PATH for the throw-away web server'
  } else {
    $site = Join-Path $work 'site'
    New-Item -ItemType Directory -Path (Join-Path $site 'windows\9.9.9') | Out-Null
    # A tiny stand-in for the customer package: just needs install.ps1 and install.cmd.
    $pkgSrc = Join-Path $work 'pkgsrc'
    New-Item -ItemType Directory -Path $pkgSrc | Out-Null
    [System.IO.File]::WriteAllText((Join-Path $pkgSrc 'install.ps1'), '# stand-in installer')
    [System.IO.File]::WriteAllText((Join-Path $pkgSrc 'install.cmd'), '@echo off')
    $zip = Join-Path $site 'windows\9.9.9\vedha-agent-win.zip'
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($pkgSrc, $zip)
    $zipHash = Get-GetSha256 $zip
    $releaseJson = '{"schema":1,"version":"9.9.9","sha256":"' + $zipHash + '","zip":"9.9.9/vedha-agent-win.zip"}'
    [System.IO.File]::WriteAllText((Join-Path $site 'windows\latest.json'), $releaseJson)
    [System.IO.File]::WriteAllText((Join-Path $site 'windows\9.9.9\release.json'), $releaseJson)

    $port = Get-Random -Minimum 20000 -Maximum 40000
    $spArgs = @{ FilePath = $python; ArgumentList = @('-m', 'http.server', "$port", '--bind', '127.0.0.1', '--directory', $site); PassThru = $true
                 RedirectStandardOutput = (Join-Path $work 'server.out'); RedirectStandardError = (Join-Path $work 'server.err') }
    if ([Environment]::OSVersion.Platform -eq 'Win32NT') { $spArgs['WindowStyle'] = 'Hidden' }
    $server = Start-Process @spArgs
    $up = $false
    for ($i = 0; $i -lt 40 -and -not $up; $i++) {
      Start-Sleep -Milliseconds 250
      try { $c = New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1', $port); $c.Close(); $up = $true } catch { }
    }
    Assert-True $up 'test web server started'

    $shell = (Get-Process -Id $PID).Path
    $base = "http://127.0.0.1:$port/windows"
    function Run-Get {
      param([string[]]$GetArgs)
      $out = & $shell -NoProfile -ExecutionPolicy Bypass -File $getScript @GetArgs 2>&1 | Out-String
      return [pscustomobject]@{ Code = $LASTEXITCODE; Output = $out }
    }

    # 1. pinned hash + version: downloads, verifies, unpacks, stops (-DownloadOnly)
    $w1 = Join-Path $work 'w1'
    $r = Run-Get @('-DownloadOnly', '-WorkDir', $w1, '-BaseUrl', $base, '-Version', '9.9.9', '-Sha256', $zipHash)
    Assert-Equal $r.Code 0 'download: exit code 0'
    Assert-True  ($r.Output -match 'SHA-256 matches') 'download: says the hash matched'
    Assert-True  (Test-Path (Join-Path $w1 'package\install.ps1')) 'download: the package was unpacked'

    # 2. a wrong pinned hash is refused and nothing is unpacked
    $w2 = Join-Path $work 'w2'
    $r = Run-Get @('-DownloadOnly', '-WorkDir', $w2, '-BaseUrl', $base, '-Version', '9.9.9', '-Sha256', ('0' * 64))
    Assert-True  ($r.Code -ne 0) 'wrong hash: fails'
    Assert-True  ($r.Output -match 'does not match') 'wrong hash: says so'
    Assert-False (Test-Path (Join-Path $w2 'package')) 'wrong hash: nothing unpacked'

    # 3. no pinned hash is refused unless the hosted one is trusted on purpose
    $r = Run-Get @('-DownloadOnly', '-WorkDir', (Join-Path $work 'w3'), '-BaseUrl', $base, '-Version', '9.9.9')
    Assert-True  ($r.Code -ne 0 -and $r.Output -match "needs the package's SHA-256") 'no hash: refused'
    $w4 = Join-Path $work 'w4'
    $r = Run-Get @('-DownloadOnly', '-WorkDir', $w4, '-BaseUrl', $base, '-TrustHostedHash')
    Assert-Equal $r.Code 0 'trust hosted hash + latest: works'
    Assert-True  (Test-Path (Join-Path $w4 'package\install.cmd')) 'trust hosted hash + latest: unpacked'

    # 4. missing version, bad token, http to another host
    $r = Run-Get @('-DownloadOnly', '-WorkDir', (Join-Path $work 'w5'), '-BaseUrl', $base, '-Sha256', $zipHash)
    Assert-True  ($r.Code -ne 0 -and $r.Output -match 'needs the package version') 'no version: refused'
    $r = Run-Get @('-DownloadOnly', '-WorkDir', (Join-Path $work 'w6'), '-BaseUrl', $base, '-Version', '9.9.9', '-Sha256', $zipHash, '-Token', 'bad')
    Assert-True  ($r.Code -ne 0 -and $r.Output -match 'install token') 'bad token: refused before downloading'
    Assert-False (Test-Path (Join-Path $work 'w6\vedha-agent-win.zip')) 'bad token: nothing downloaded'
    $r = Run-Get @('-DownloadOnly', '-WorkDir', (Join-Path $work 'w7'), '-BaseUrl', 'http://downloads.example.com/windows', '-Version', '9.9.9', '-Sha256', $zipHash)
    Assert-True  ($r.Code -ne 0 -and $r.Output -match 'https') 'plain http to another host: refused'

    # 5. a file that is not on the server
    $r = Run-Get @('-DownloadOnly', '-WorkDir', (Join-Path $work 'w8'), '-BaseUrl', $base, '-Version', '9.9.8', '-Sha256', $zipHash)
    Assert-True  ($r.Code -ne 0 -and $r.Output -match 'Could not download') 'missing package: a clear message'
  }
} finally {
  if ($server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue }
  Start-Sleep -Milliseconds 300
  Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host ''
Write-Host "hosting get.ps1: $script:Passed passed, $($script:Failed.Count) failed"
foreach ($f in $script:Failed) { Write-Host "  FAIL: $f" -ForegroundColor Red }
exit ($(if ($script:Failed.Count -eq 0) { 0 } else { 1 }))
