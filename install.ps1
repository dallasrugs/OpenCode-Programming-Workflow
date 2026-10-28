# OpenCode Multi-Agent Starter - Windows PowerShell Installer
# Compatible with Windows PowerShell 5.1 and PowerShell 7+

[CmdletBinding(DefaultParameterSetName = 'Help')]
param(
    [Parameter(Mandatory = $true, ParameterSetName = 'Global')]
    [switch]$Global,

    [Parameter(Mandatory = $true, ParameterSetName = 'Project')]
    [string]$Project,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$sourceRoot = Join-Path $PSScriptRoot '.opencode'

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Source configuration directory not found: $sourceRoot"
}

if ($PSCmdlet.ParameterSetName -eq 'Global') {
    $destination = Join-Path $HOME '.config\opencode'
}
elseif ($PSCmdlet.ParameterSetName -eq 'Project') {
    if (-not (Test-Path -LiteralPath $Project -PathType Container)) {
        throw "Project directory does not exist: $Project"
    }

    $projectPath = (Get-Item -LiteralPath $Project).FullName
    $destination = Join-Path $projectPath '.opencode'
}
else {
    throw "Specify -Global or -Project <path>."
}

$agents = @(
    'planner',
    'consultant',
    'supervisor',
    'coder'
)

# Discover bundled skills automatically.
# Install only SKILL.md files from valid skill directories.
$skillsRoot = Join-Path $sourceRoot 'skills'

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
    throw "Skills directory not found: $skillsRoot"
}

$skills = @(
    Get-ChildItem -LiteralPath $skillsRoot -Directory |
        Where-Object {
            $_.Name -match '^[a-z0-9][a-z0-9-]*$' -and
            (Test-Path -LiteralPath (
                Join-Path $_.FullName 'SKILL.md'
            ) -PathType Leaf)
        } |
        Sort-Object -Property Name |
        ForEach-Object { $_.Name }
)

$files = @('opencode.json')

foreach ($agent in $agents) {
    $files += "agents/$agent.md"
}

foreach ($skill in $skills) {
    $files += "skills/$skill/SKILL.md"
}

# Validate source before making any changes.
foreach ($relative in $files) {
    $nativePath = $relative.Replace(
        '/',
        [System.IO.Path]::DirectorySeparatorChar
    )
    $sourceFile = Join-Path $sourceRoot $nativePath

    if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) {
        throw "Missing source file: $relative"
    }
}

Write-Host ""
Write-Host "OpenCode Multi-Agent Starter"
Write-Host "Source: $sourceRoot"
Write-Host "Destination: $destination"
Write-Host "Dry run: $DryRun"
Write-Host ""

$installed = 0
$skipped = 0

foreach ($relative in $files) {
    $nativePath = $relative.Replace(
        '/',
        [System.IO.Path]::DirectorySeparatorChar
    )

    $sourceFile = Join-Path $sourceRoot $nativePath
    $targetFile = Join-Path $destination $nativePath

    # Avoid introducing a competing JSON file if the
    # user already has an OpenCode JSONC configuration.
    if ($relative -eq 'opencode.json') {
        $existingJsonc = Join-Path $destination 'opencode.jsonc'

        if (Test-Path -LiteralPath $existingJsonc) {
            Write-Host "SKIP: opencode.json (existing JSONC config)"
            $skipped++
            continue
        }
    }

    if (Test-Path -LiteralPath $targetFile) {
        Write-Host "SKIP: $relative (already exists)"
        $skipped++
        continue
    }

    if ($DryRun) {
        Write-Host "WOULD INSTALL: $relative"
        $installed++
        continue
    }

    $parent = Split-Path -Parent $targetFile

    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force |
            Out-Null
    }

    # Explicitly disallow overwriting existing files.
    [System.IO.File]::Copy(
        $sourceFile,
        $targetFile,
        $false
    )

    Write-Host "INSTALLED: $relative"
    $installed++
}

Write-Host ""

if ($DryRun) {
    Write-Host "Dry run complete."
    Write-Host "$installed installable, $skipped existing."
    Write-Host "No files were changed."
}
else {
    Write-Host "Installation complete."
    Write-Host "$installed installed, $skipped skipped."
    Write-Host "Restart OpenCode or reload its configuration."
}

if ($skipped -gt 0) {
    Write-Host ""
    Write-Host "Existing files were preserved."
    Write-Host "Review configuration merging manually if needed."
}
