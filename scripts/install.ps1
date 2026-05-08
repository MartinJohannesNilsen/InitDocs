#Requires -Version 5.1
<#
.SYNOPSIS
    InitDocs install script for Windows.
    Downloads the latest InitDocs .exe to $HOME\.local\bin and adds it to your PATH.
.PARAMETER Release
    Install a specific release tag (e.g. v1.1.6). Defaults to the latest release.
.PARAMETER DryRun
    Preview what would happen without making any changes.
.EXAMPLE
    irm "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.ps1" | iex
.EXAMPLE
    & ([scriptblock]::Create((irm "https://raw.githubusercontent.com/martinjnilsen/initdocs/main/scripts/install.ps1"))) -DryRun
.EXAMPLE
    .\install.ps1 -Release v1.1.6
#>
[CmdletBinding()]
param(
    [string]$Release = "",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ReleasesUrl = "https://github.com/martinjnilsen/initdocs/releases"
$RepoUrl     = "https://github.com/martinjnilsen/initdocs"
$ApiUrl      = "https://api.github.com/repos/martinjnilsen/initdocs/releases/latest"
$InstallDir  = Join-Path $HOME ".local\bin"
$BinaryName  = "initdocs.exe"

# ── Helpers ───────────────────────────────────────────────────────────────────

function Write-Dry { param([string]$Msg) if ($DryRun) { Write-Host "[dry-run] $Msg" } }

if ($DryRun) { Write-Host "[dry-run] Previewing installation — no changes will be made.`n" }

# ── Resolve release tag ───────────────────────────────────────────────────────

if ($Release -ne "") {
    Write-Verbose "Using specified release: $Release"
    Write-Dry "Would use specified tag: $Release"
    $Tag = $Release
} else {
    Write-Verbose "Fetching latest release version..."
    if ($DryRun) {
        Write-Dry "Would fetch latest tag from GitHub API: $ApiUrl"
        $Tag = "v?.?.?"
    } else {
        $Latest = Invoke-RestMethod -Uri $ApiUrl -Headers @{ "User-Agent" = "initdocs-installer" }
        $Tag = $Latest.tag_name
        Write-Verbose "Latest version: $Tag"
    }
}

# ── Construct download URL ────────────────────────────────────────────────────

$Filename    = "initdocs_${Tag}_windows.exe"
$DownloadUrl = "$RepoUrl/releases/download/$Tag/$Filename"
Write-Verbose "Download URL: $DownloadUrl"

# ── Validate release exists ───────────────────────────────────────────────────

Write-Verbose "Validating release $Tag..."
if ($DryRun) {
    Write-Dry "Would validate release exists (HEAD $DownloadUrl)"
} else {
    try {
        $Req = [System.Net.HttpWebRequest]::Create($DownloadUrl)
        $Req.Method = "HEAD"
        $Req.AllowAutoRedirect = $true
        $Response = $Req.GetResponse()
        $Response.Close()
    } catch [System.Net.WebException] {
        $StatusCode = [int]$_.Exception.Response.StatusCode
        Write-Error "[error] Release $Tag not found (HTTP $StatusCode).`nCheck available releases at: $ReleasesUrl"
    }
}

# ── Create install directory ──────────────────────────────────────────────────

Write-Verbose "Preparing install directory: $InstallDir..."
if ($DryRun) {
    Write-Dry "Would create install directory: $InstallDir"
} else {
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir | Out-Null
    }
}

# ── Download binary ───────────────────────────────────────────────────────────

$InstallPath = Join-Path $InstallDir $BinaryName
Write-Verbose "Downloading initdocs $Tag for Windows..."
if ($DryRun) {
    Write-Dry "Would download $DownloadUrl -> $InstallPath"
} else {
    $TmpFile = [System.IO.Path]::GetTempFileName()
    try {
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $TmpFile -UseBasicParsing
        Move-Item -Path $TmpFile -Destination $InstallPath -Force
        Write-Verbose "Binary installed to: $InstallPath"
    } catch {
        Remove-Item -Path $TmpFile -ErrorAction SilentlyContinue
        Write-Error "[error] Download failed. Check your connection or visit:`n  $ReleasesUrl"
    }
}

# ── Add to user PATH ──────────────────────────────────────────────────────────

Write-Verbose "Checking PATH..."
if ($DryRun) {
    Write-Dry "Would add $InstallDir to user PATH (if not already present)"
} else {
    $UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($null -eq $UserPath) { $UserPath = "" }
    if ($UserPath -notlike "*$InstallDir*") {
        $NewPath = if ($UserPath) { "$InstallDir;$UserPath" } else { $InstallDir }
        [Environment]::SetEnvironmentVariable("PATH", $NewPath, "User")
        $env:PATH = "$InstallDir;$env:PATH"
        Write-Verbose "Added $InstallDir to user PATH."
    } else {
        Write-Verbose "$InstallDir already on PATH — skipping."
    }
}

# ── Done ──────────────────────────────────────────────────────────────────────

if ($DryRun) {
    Write-Host "`n[dry-run] Preview complete. Run without -DryRun to install."
} else {
    Write-Host "`n[info] initdocs $Tag installed to $InstallPath"
    Write-Host "[info] Open a new terminal and run: initdocs --help`n"
}
