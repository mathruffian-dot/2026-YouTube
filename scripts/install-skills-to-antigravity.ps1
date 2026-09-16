<#
.SYNOPSIS
  Install and sync YouTube workflow skills into the local Antigravity environment.
.DESCRIPTION
  Copies skills from the repo into $HOME\.gemini\config\skills
#>

[CmdletBinding()]
param(
    [string]$TargetDir = "$HOME\.gemini\config\skills"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillsSource = Join-Path $RepoRoot "skills"

if (-not (Test-Path $SkillsSource)) {
    Write-Error "Cannot find skills directory at: $SkillsSource"
}

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$skills = @(
    "antigravity-youtube-video-workflow",
    "smart-cut",
    "audio-to-srt",
    "short-video-workflow",
    "video-editing-and-subtitles",
    "chatgpt-youtube-video-workflow",
    "cover-image"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Installing YouTube Skills to Antigravity" -ForegroundColor Cyan
Write-Host "  Target: $TargetDir" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

foreach ($s in $skills) {
    $src = Join-Path $SkillsSource $s
    $dst = Join-Path $TargetDir $s
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $dst -Recurse -Force
        Write-Host "  [OK] Installed: $s" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] Not found in repo: $s" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "--- Checking Environment ---" -ForegroundColor Cyan

# Check Python
try {
    $pyVer = python --version 2>&1
    Write-Host "  [OK] Python: $pyVer" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] Python not found on PATH" -ForegroundColor Red
}

# Check ffmpeg
try {
    $ffVer = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "  [OK] ffmpeg: $ffVer" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] ffmpeg not found on PATH (winget install Gyan.FFmpeg)" -ForegroundColor Red
}

# Check Groq key
$groqKeyFile = Join-Path $HOME ".groq_api_key"
if ($env:GROQ_API_KEY -or (Test-Path $groqKeyFile)) {
    Write-Host "  [OK] Groq API Key found" -ForegroundColor Green
} else {
    Write-Host "  [NOTE] Groq API Key missing. Please set ~/.groq_api_key or GROQ_API_KEY" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "All set! You can now use /antigravity-youtube-video-workflow in Antigravity." -ForegroundColor Green
