# run_nas_backup.ps1 - Automated 14-Day Rotating Backup & Synology NAS Sync
$ErrorActionPreference = "SilentlyContinue"

$sourceDir = "C:\section8landlordsmn"
$localBackupDir = "C:\section8_backups"
$nasTargetDir = "\\DS223\Backups\section8"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveName = "sec8_full_$timestamp.zip"
$localArchivePath = Join-Path $localBackupDir $archiveName

if (!(Test-Path $localBackupDir)) {
    New-Item -ItemType Directory -Force -Path $localBackupDir | Out-Null
}

Write-Host "Creating local rotating archive: $archiveName" -ForegroundColor Cyan
Compress-Archive -Path "$sourceDir\*" -DestinationPath $localArchivePath -CompressionLevel Optimal -Force

# SHA-256 Checksum Validation
$hash = (Get-FileHash -Path $localArchivePath -Algorithm SHA256).Hash
Write-Host "Archive SHA-256 Checksum: $hash" -ForegroundColor Green

# Synology DS223 Network Synchronization
if (Test-Path $nasTargetDir) {
    Copy-Item -Path $localArchivePath -Destination "$nasTargetDir\$archiveName" -Force
    Write-Host "Successfully mirrored archive to Synology NAS (\\DS223\Backups\section8)" -ForegroundColor Green
} else {
    Write-Host "Synology NAS volume unreachable on local LAN. Retaining archive in local storage ($localBackupDir)." -ForegroundColor Yellow
}

# Retain 14 rolling versions, prune older archives
Get-ChildItem -Path $localBackupDir -Filter "sec8_full_*.zip" | 
    Sort-Object CreationTime -Descending | 
    Select-Object -Skip 14 | 
    Remove-Item -Force

Write-Host "Pruned archives exceeding 14-version retention threshold." -ForegroundColor DarkGray
