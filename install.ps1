#Requires -Version 5.1
<#
.SYNOPSIS
    One-liner installer for init-design-reference agent skill.
.DESCRIPTION
    Installs the init-design-reference skill into the designated agent skill directory.
    Supports Google Antigravity, Claude Code, Cursor, and custom targets.
    Supports both local execution and remote one-liner execution via Web.
.EXAMPLE
    # Remote one-liner (Google Antigravity on Windows)
    irm https://raw.githubusercontent.com/mmmphyun/init-design-reference/main/install.ps1 | iex
.EXAMPLE
    # Local execution
    .\install.ps1 -Agent antigravity
    .\install.ps1 -Agent claude
    .\install.ps1 -TargetDir "C:/custom/skills/init-design-reference" -Force
#>

[CmdletBinding()]
param (
    [ValidateSet("antigravity", "claude", "cursor", "custom")]
    [string]$Agent = "antigravity",

    [string]$TargetDir = "",

    [string]$Repo = $(if ($env:INIT_DESIGN_REF_REPO) { $env:INIT_DESIGN_REF_REPO } else { "mmmphyun/init-design-reference" }),

    [string]$Branch = "main",

    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Ensure TLS 1.2+ for older PowerShell environments
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12

# Resolve target installation directory
if (-not [string]::IsNullOrWhiteSpace($TargetDir)) {
    $installPath = [System.IO.Path]::GetFullPath($TargetDir)
} else {
    $homeDir = $env:USERPROFILE
    if (-not $homeDir) {
        $homeDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
    }

    switch ($Agent) {
        "antigravity" {
            $installPath = [System.IO.Path]::Combine($homeDir, ".gemini", "config", "skills", "init-design-reference")
        }
        "claude" {
            $installPath = [System.IO.Path]::Combine($homeDir, ".claude", "skills", "init-design-reference")
        }
        "cursor" {
            $installPath = [System.IO.Path]::Combine($homeDir, ".cursor", "skills", "init-design-reference")
        }
        "custom" {
            Write-Error "Error: -TargetDir must be specified when -Agent is set to 'custom'."
            exit 1
        }
    }
}

Write-Host "Target installation path: $installPath" -ForegroundColor Cyan

# Check if target already exists
if (Test-Path -LiteralPath $installPath) {
    if (-not $Force) {
        Write-Warning "Directory already exists: $installPath"
        Write-Host "Use -Force to overwrite existing installation." -ForegroundColor Yellow
        exit 0
    }
    Write-Host "Overwriting existing directory (-Force specified)..." -ForegroundColor Yellow
}

# Determine if running locally from cloned repo or remotely via web stream
$isLocal = $false
$scriptSourceDir = ""

if ($PSScriptRoot -and (Test-Path -LiteralPath (Join-Path $PSScriptRoot "SKILL.md"))) {
    $isLocal = $true
    $scriptSourceDir = $PSScriptRoot
} elseif ($MyInvocation.MyCommand.Path -and (Test-Path -LiteralPath (Join-Path (Split-Path $MyInvocation.MyCommand.Path) "SKILL.md"))) {
    $isLocal = $true
    $scriptSourceDir = Split-Path $MyInvocation.MyCommand.Path
}

if ($isLocal) {
    Write-Host "Installing from local repository: $scriptSourceDir" -ForegroundColor Green
    if (Test-Path -LiteralPath $installPath) {
        Remove-Item -LiteralPath $installPath -Recurse -Force
    }
    New-Item -ItemType Directory -Path $installPath -Force | Out-Null

    # Copy files and directories
    $itemsToCopy = @("SKILL.md", "README.md", "scripts", "templates")
    foreach ($item in $itemsToCopy) {
        $src = Join-Path $scriptSourceDir $item
        if (Test-Path -LiteralPath $src) {
            Copy-Item -Path $src -Destination $installPath -Recurse -Force
        }
    }
} else {
    Write-Host "Installing from remote repository: $Repo ($Branch branch)..." -ForegroundColor Green
    $tempZip = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "init-design-reference-$([System.Guid]::NewGuid()).zip")
    $tempExtract = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "init-design-reference-extract-$([System.Guid]::NewGuid())")

    try {
        $archiveUrl = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"
        Write-Host "Downloading $archiveUrl..."
        Invoke-WebRequest -Uri $archiveUrl -OutFile $tempZip -UseBasicParsing

        Write-Host "Extracting archive..."
        Expand-Archive -LiteralPath $tempZip -DestinationPath $tempExtract -Force

        $extractedRoot = Get-ChildItem -LiteralPath $tempExtract | Select-Object -First 1
        if (-not $extractedRoot) {
            throw "Failed to find extracted folder in $tempExtract"
        }

        if (Test-Path -LiteralPath $installPath) {
            Remove-Item -LiteralPath $installPath -Recurse -Force
        }
        New-Item -ItemType Directory -Path $installPath -Force | Out-Null

        $itemsToCopy = @("SKILL.md", "README.md", "scripts", "templates")
        foreach ($item in $itemsToCopy) {
            $src = Join-Path $extractedRoot.FullName $item
            if (Test-Path -LiteralPath $src) {
                Copy-Item -Path $src -Destination $installPath -Recurse -Force
            }
        }
    } finally {
        if (Test-Path -LiteralPath $tempZip) { Remove-Item -LiteralPath $tempZip -Force -ErrorAction SilentlyContinue }
        if (Test-Path -LiteralPath $tempExtract) { Remove-Item -LiteralPath $tempExtract -Recurse -Force -ErrorAction SilentlyContinue }
    }
}

Write-Host "`nInstallation successful!" -ForegroundColor Green
Write-Host "Skill installed at: $installPath"
Write-Host "Verify adapter execution:"
Write-Host "  python `"$([System.IO.Path]::Combine($installPath, 'scripts', 'adapter.py').Replace('\', '/'))`" `"reference`"" -ForegroundColor Cyan
