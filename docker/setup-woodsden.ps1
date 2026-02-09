# WoodsDen Infrastructure Setup Script
# The Continuum Report - Local Deployment
#
# Run as Administrator:
#   powershell -ExecutionPolicy Bypass -File setup-woodsden.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  The Continuum Report - WoodsDen Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Step 1: Create directory structure on Z: drive
Write-Host "[1/5] Creating directory structure on Z: drive..." -ForegroundColor Yellow

$directories = @(
    "Z:\paperless",
    "Z:\paperless\data",
    "Z:\paperless\media",
    "Z:\paperless\export",
    "Z:\paperless\consume",
    "Z:\paperless\redis",
    "Z:\paperless\pgdata",
    "Z:\continuum-sources",
    "Z:\backups"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor Gray
    }
}

# Step 2: Check for Docker
Write-Host ""
Write-Host "[2/5] Checking for Docker Desktop..." -ForegroundColor Yellow

$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerPath) {
    $dockerVersion = docker --version
    Write-Host "  Docker found: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "  Docker NOT FOUND" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Please install Docker Desktop:" -ForegroundColor Yellow
    Write-Host "  https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  After installation:" -ForegroundColor Yellow
    Write-Host "  1. Enable WSL2 backend in Docker settings" -ForegroundColor White
    Write-Host "  2. Restart this script" -ForegroundColor White
    Write-Host ""

    # Offer to open download page
    $response = Read-Host "Open Docker Desktop download page? (y/n)"
    if ($response -eq 'y') {
        Start-Process "https://www.docker.com/products/docker-desktop/"
    }
    exit 0
}

# Step 3: Check Docker is running
Write-Host ""
Write-Host "[3/5] Checking Docker is running..." -ForegroundColor Yellow

try {
    docker info | Out-Null
    Write-Host "  Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  Docker is installed but not running" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and run this script again" -ForegroundColor Yellow
    exit 1
}

# Step 4: Start services
Write-Host ""
Write-Host "[4/5] Starting Continuum services..." -ForegroundColor Yellow

$composeFile = "$PSScriptRoot\docker-compose.woodsden.yml"
if (Test-Path $composeFile) {
    Write-Host "  Using: $composeFile" -ForegroundColor Gray
    Set-Location $PSScriptRoot
    docker-compose -f docker-compose.woodsden.yml up -d
} else {
    Write-Host "  ERROR: docker-compose.woodsden.yml not found" -ForegroundColor Red
    exit 1
}

# Step 5: Display status
Write-Host ""
Write-Host "[5/5] Services status:" -ForegroundColor Yellow
docker-compose -f docker-compose.woodsden.yml ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Access your services:" -ForegroundColor Yellow
Write-Host "  - Paperless:  http://localhost:8040" -ForegroundColor White
Write-Host "    Username:   admin" -ForegroundColor Gray
Write-Host "    Password:   continuum2026" -ForegroundColor Gray
Write-Host ""
Write-Host "  - Website:    http://localhost:8081" -ForegroundColor White
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor Yellow
Write-Host "  1. Configure Cloudflare tunnel" -ForegroundColor White
Write-Host "  2. Upload documents to Z:\paperless\consume\" -ForegroundColor White
Write-Host "  3. Set up BNIS pipeline" -ForegroundColor White
Write-Host ""
