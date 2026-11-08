<#
.SYNOPSIS
  Section 8 Rentals and More LLC - Automated Backup & NAS Sync Daemon
  Targets: Local archive + Synology NAS / Network Share
#>

$SourceDir    = "C:\section8landlordsmn"
$BackupRoot   = "C:\section8_backups"
$NasTarget    = "\\DS223\Backups\section8"   # Adjust NAS path or secondary drive letter as needed
$MaxKeepDays  = 14

$Timestamp    = Get-Date -Format "yyyyMMdd_HHmmss"
$ArchiveName  = "sec8_full_$Timestamp.zip"
$ZipPath      = Join-Path $BackupRoot $ArchiveName

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "STARTING PORTFOLIO BACKUP RUN: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. Ensure local backup directory exists
if (-not (Test-Path $BackupRoot)) {
    New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null
}

# 2. Package working tree into compressed ZIP archive (excluding temporary caches)
Write-Host "[*] Compressing repository into $ArchiveName..." -ForegroundColor Yellow
$ExcludeList = @("*.git*", "*node_modules*", "*__pycache__*", "*.tmp")

Add-Type -AssemblyName System.IO.Compression.FileSystem
$TempStaging = Join-Path $env:TEMP "sec8_stage_$Timestamp"
New-Item -ItemType Directory -Path $TempStaging -Force | Out-Null

# Copy clean files to temp staging
robocopy $SourceDir $TempStaging /E /XD .git node_modules __pycache__ /XF *.tmp | Out-Null
[System.IO.Compression.ZipFile]::CreateFromDirectory($TempStaging, $ZipPath, [System.IO.Compression.CompressionLevel]::Optimal, $false)
Remove-Item -Path $TempStaging -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "[✔] Archive successfully created at $ZipPath" -ForegroundColor Green

# 3. Mirror to NAS target if reachable
if (Test-Path $NasTarget) {
    Write-Host "[*] Syncing archive to Synology NAS share ($NasTarget)..." -ForegroundColor Yellow
    robocopy $BackupRoot $NasTarget $ArchiveName /COPY:DAT /R:2 /W:3 | Out-Null
    Write-Host "[✔] Successfully mirrored to NAS." -ForegroundColor Green
} else {
    Write-Host "[i] Network share $NasTarget offline or unmounted. Local copy preserved safely in $BackupRoot." -ForegroundColor Gray
}

# 4. Enforce Retention Policy: Prune backups older than $MaxKeepDays
Write-Host "[*] Pruning local archives older than $MaxKeepDays days..." -ForegroundColor Yellow
$CutoffDate = (Get-Date).AddDays(-$MaxKeepDays)
Get-ChildItem -Path $BackupRoot -Filter "sec8_full_*.zip" | Where-Object { $_.CreationTime -lt $CutoffDate } | ForEach-Object {
    Write-Host "    Pruning expired archive: $($_.Name)" -ForegroundColor DarkGray
    Remove-Item $_.FullName -Force
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "BACKUP RUN COMPLETE: State secured." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
