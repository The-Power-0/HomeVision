$sdk = Join-Path $env:LOCALAPPDATA 'Android\Sdk'
if (-not (Test-Path $sdk)) { $sdk = 'C:\Android\Sdk' }
Write-Host ("SDK: " + $sdk)
$bt = Join-Path $sdk 'build-tools'
if (Test-Path $bt) {
    Get-ChildItem $bt -Directory | Sort-Object Name -Descending | Select-Object -First 3 | ForEach-Object { Write-Host $_.FullName }
} else {
    Write-Host 'build-tools not found'
}
$ks = Join-Path $env:USERPROFILE '.android\debug.keystore'
Write-Host ("debug.keystore exists: " + (Test-Path $ks))
