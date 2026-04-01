param(
    [switch]$SkipConda,
    [switch]$SkipNpm,
    [switch]$SkipPip,
    [switch]$SkipTemp,
    [switch]$SkipCodeCache,
    [switch]$SkipDownloadsPartial
)

$ErrorActionPreference = "Continue"

function Get-DirSizeBytes {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return 0
    }

    $sum = (Get-ChildItem -LiteralPath $Path -Recurse -Force -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum).Sum

    if ($null -eq $sum) {
        return 0
    }

    return [int64]$sum
}

function Format-Size {
    param(
        [Parameter(Mandatory = $true)]
        [double]$Bytes
    )

    if ($Bytes -ge 1GB) { return "{0:N2} GB" -f ($Bytes / 1GB) }
    if ($Bytes -ge 1MB) { return "{0:N2} MB" -f ($Bytes / 1MB) }
    if ($Bytes -ge 1KB) { return "{0:N2} KB" -f ($Bytes / 1KB) }
    return "{0:N0} B" -f $Bytes
}

function Show-Section {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Title
    )

    Write-Host ""
    Write-Host $Title -ForegroundColor Cyan
}

$pipCache = Join-Path $env:LOCALAPPDATA "pip\Cache"
$npmCache = Join-Path $env:LOCALAPPDATA "npm-cache"
$windowsTemp = "C:\Windows\Temp"
$localTemp = Join-Path $env:LOCALAPPDATA "Temp"
$codeCache = Join-Path $env:APPDATA "Code\Cache"
$codeCachedData = Join-Path $env:APPDATA "Code\CachedData"
$downloads = Join-Path $env:USERPROFILE "Downloads"
$partialDownloads = @()

if (Test-Path -LiteralPath $downloads) {
    $partialDownloads = Get-ChildItem -LiteralPath $downloads -Force -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -in @(".crdownload", ".part", ".partial") }
}

$plan = @()

if (-not $SkipPip) {
    $plan += [pscustomobject]@{
        Name = "pip cache"
        Target = $pipCache
        EstimatedBytes = Get-DirSizeBytes -Path $pipCache
    }
}

if (-not $SkipNpm) {
    $plan += [pscustomobject]@{
        Name = "npm cache"
        Target = $npmCache
        EstimatedBytes = Get-DirSizeBytes -Path $npmCache
    }
}

if (-not $SkipTemp) {
    $plan += [pscustomobject]@{
        Name = "Windows temp"
        Target = $windowsTemp
        EstimatedBytes = Get-DirSizeBytes -Path $windowsTemp
    }
    $plan += [pscustomobject]@{
        Name = "Local temp"
        Target = $localTemp
        EstimatedBytes = Get-DirSizeBytes -Path $localTemp
    }
}

if (-not $SkipCodeCache) {
    $plan += [pscustomobject]@{
        Name = "VS Code cache"
        Target = $codeCache
        EstimatedBytes = Get-DirSizeBytes -Path $codeCache
    }
    $plan += [pscustomobject]@{
        Name = "VS Code cached data"
        Target = $codeCachedData
        EstimatedBytes = Get-DirSizeBytes -Path $codeCachedData
    }
}

if (-not $SkipDownloadsPartial) {
    $partialBytes = ($partialDownloads | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $partialBytes) {
        $partialBytes = 0
    }
    $plan += [pscustomobject]@{
        Name = "Partial downloads"
        Target = $downloads
        EstimatedBytes = [int64]$partialBytes
    }
}

Show-Section "Cleanup Plan"
$plan | Select-Object Name, Target, @{Name = "Estimated"; Expression = { Format-Size $_.EstimatedBytes } } |
    Format-Table -AutoSize

if (-not $SkipConda) {
    Write-Host ""
    Write-Host "Conda cleanup will be delegated to 'conda clean --all -y' if Conda is available." -ForegroundColor Yellow
}

Write-Host ""
$reply = Read-Host "Proceed with cleanup? Type Y to continue"
if ($reply -notin @("Y", "y")) {
    Write-Host "Cleanup cancelled."
    exit 0
}

$beforeFree = (Get-PSDrive -Name C).Free
$log = New-Object System.Collections.Generic.List[string]

Show-Section "Running"

if (-not $SkipPip) {
    $pipCmd = Get-Command pip -ErrorAction SilentlyContinue
    if ($pipCmd) {
        $result = & pip cache purge 2>&1
        $log.Add("pip: $($result -join ' ')")
    } else {
        $result = & python -m pip cache purge 2>&1
        $log.Add("python -m pip: $($result -join ' ')")
    }
}

if (-not $SkipNpm) {
    $npmCmd = Get-Command npm -ErrorAction SilentlyContinue
    if ($npmCmd) {
        $result = & npm cache clean --force 2>&1
        $log.Add("npm: $($result -join ' ')")
    } else {
        $log.Add("npm: skipped, npm not found on PATH")
    }
}

if (-not $SkipConda) {
    $condaCmd = Get-Command conda -ErrorAction SilentlyContinue
    if ($condaCmd) {
        $result = & conda clean --all -y 2>&1
        $log.Add("conda: $($result -join ' ')")
    } else {
        $log.Add("conda: skipped, conda not found on PATH")
    }
}

if (-not $SkipTemp) {
    foreach ($target in @($windowsTemp, $localTemp)) {
        if (Test-Path -LiteralPath $target) {
            Get-ChildItem -LiteralPath $target -Force -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            $log.Add("temp: cleaned $target")
        }
    }
}

if (-not $SkipCodeCache) {
    foreach ($target in @($codeCache, $codeCachedData)) {
        if (Test-Path -LiteralPath $target) {
            Get-ChildItem -LiteralPath $target -Force -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            $log.Add("code: cleaned $target")
        }
    }
}

if (-not $SkipDownloadsPartial) {
    foreach ($file in $partialDownloads) {
        if (Test-Path -LiteralPath $file.FullName) {
            Remove-Item -LiteralPath $file.FullName -Force -ErrorAction SilentlyContinue
            $log.Add("downloads: removed $($file.FullName)")
        }
    }
}

$afterFree = (Get-PSDrive -Name C).Free
$freedBytes = $afterFree - $beforeFree

Show-Section "Summary"
Write-Host ("Freed on C: {0}" -f (Format-Size $freedBytes)) -ForegroundColor Green
Write-Host ("C: free space now: {0}" -f (Format-Size $afterFree))

Show-Section "Log"
$log | ForEach-Object { Write-Host $_ }

Write-Host ""
Read-Host "Press Enter to close"
