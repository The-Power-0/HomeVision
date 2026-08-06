# Signs all unsigned release APKs with the local debug keystore (for quick installs).
# For public releases use a proper release keystore via the Gradle signing config.
# Portable: locates apksigner via ANDROID_HOME / local.properties / common paths.

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot

function Find-SdkRoot {
    if ($env:ANDROID_HOME -and (Test-Path $env:ANDROID_HOME)) { return $env:ANDROID_HOME }
    $localProps = Join-Path $root 'local.properties'
    if (Test-Path $localProps) {
        $line = Get-Content $localProps | Where-Object { $_ -match '^sdk\.dir=' } | Select-Object -First 1
        if ($line) {
            $p = ($line -replace '^sdk\.dir=', '').Trim()
            if (Test-Path $p) { return $p }
        }
    }
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA 'Android\Sdk'),
        'C:\Android\Sdk'
    )
    foreach ($c in $candidates) { if ($c -and (Test-Path $c)) { return $c } }
    throw 'Android SDK not found. Set ANDROID_HOME or create local.properties with sdk.dir'
}

$sdk = Find-SdkRoot
$buildTools = Get-ChildItem (Join-Path $sdk 'build-tools') -Directory |
    Sort-Object { [version]($_.Name -replace '[^0-9.]', '') } | Select-Object -Last 1
$apksigner = Join-Path $buildTools.FullName 'apksigner.bat'
if (-not (Test-Path $apksigner)) { $apksigner = Join-Path $buildTools.FullName 'apksigner' }

$keystore = Join-Path $env:USERPROFILE '.android\debug.keystore'
if (-not (Test-Path $keystore)) { throw "Debug keystore not found: $keystore" }

$dirs = @(
    (Join-Path $root 'app\build\outputs\apk\genericGeckoIncluded\release'),
    (Join-Path $root 'app\build\outputs\apk\genericGeckoExcluded\release')
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) { continue }
    Get-ChildItem $dir -Filter '*-unsigned.apk' | ForEach-Object {
        $out = $_.FullName -replace '-unsigned\.apk$', '.apk'
        Write-Host "Signing $($_.Name)"
        & $apksigner sign --ks $keystore --ks-pass pass:android --key-pass pass:android `
            --ks-key-alias androiddebugkey --out $out $_.FullName
        $size = [math]::Round((Get-Item $out).Length / 1MB, 1)
        Write-Host "  -> $([System.IO.Path]::GetFileName($out))  ($size MB)"
    }
}
Write-Host 'Done.'
