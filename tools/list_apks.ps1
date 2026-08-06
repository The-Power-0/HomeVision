# Lists built release APKs with their sizes (relative to repo root).
$root = Split-Path -Parent $PSScriptRoot
$dirs = @(
    (Join-Path $root 'app\build\outputs\apk\genericGeckoIncluded\release'),
    (Join-Path $root 'app\build\outputs\apk\genericGeckoExcluded\release')
)
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) { continue }
    Write-Host "== $dir"
    Get-ChildItem $dir -Filter '*.apk' | ForEach-Object {
        $size = [math]::Round($_.Length / 1MB, 1)
        Write-Host ("  {0}  ({1} MB)" -f $_.Name, $size)
    }
}
