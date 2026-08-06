# Verifies that a built APK contains the configured default kiosk URL string.
# Usage: .\verify_url_in_apk.ps1 <path-to-apk> <url-fragment-to-find>
# Example: .\verify_url_in_apk.ps1 .\app-generic-geckoIncluded-arm64-v8a-release.apk "example.com:8080"
param(
    [Parameter(Mandatory = $true)] [string] $apk,
    [Parameter(Mandatory = $true)] [string] $needle
)

if (-not (Test-Path $apk)) {
    Write-Host "APK not found: $apk"
    exit 1
}

$tmp = Join-Path $env:TEMP 'dv_apk_check'
if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
New-Item -ItemType Directory $tmp | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($apk)
foreach ($entry in $zip.Entries) {
    if ($entry.Name -match '^classes.*\.dex$') {
        $dest = Join-Path $tmp $entry.Name
        [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $dest, $true)
    }
}
$zip.Dispose()

$found = $false
Get-ChildItem $tmp -Filter *.dex | ForEach-Object {
    $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
    $text = [System.Text.Encoding]::ASCII.GetString($bytes)
    if ($text.Contains($needle)) {
        Write-Host ('FOUND "' + $needle + '" in ' + $_.Name)
        $found = $true
    }
}
if (-not $found) { Write-Host 'NOT FOUND - check failed!' }
Remove-Item $tmp -Recurse -Force
