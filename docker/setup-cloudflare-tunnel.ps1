# Cloudflare Tunnel Setup for WoodsDen
# The Continuum Report
#
# Run as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cloudflare Tunnel Setup - WoodsDen" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for cloudflared
$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflared) {
    Write-Host "Installing cloudflared..." -ForegroundColor Yellow
    winget install Cloudflare.cloudflared --accept-package-agreements --accept-source-agreements

    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

Write-Host ""
Write-Host "[1/5] Logging into Cloudflare..." -ForegroundColor Yellow
Write-Host "  A browser window will open. Log in to your Cloudflare account." -ForegroundColor Gray
cloudflared tunnel login

Write-Host ""
Write-Host "[2/5] Creating tunnel..." -ForegroundColor Yellow
$tunnelName = "continuum-woodsden"
cloudflared tunnel create $tunnelName

Write-Host ""
Write-Host "[3/5] Getting tunnel info..." -ForegroundColor Yellow
$tunnelInfo = cloudflared tunnel list | Select-String $tunnelName
Write-Host $tunnelInfo

Write-Host ""
Write-Host "[4/5] Routing DNS..." -ForegroundColor Yellow
Write-Host "  This will point thecontinuumreport.com to this tunnel" -ForegroundColor Gray
cloudflared tunnel route dns $tunnelName thecontinuumreport.com
cloudflared tunnel route dns $tunnelName www.thecontinuumreport.com

Write-Host ""
Write-Host "[5/5] Next Steps" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Edit cloudflared-config.yml and replace TUNNEL_ID_HERE with your tunnel ID" -ForegroundColor White
Write-Host "  2. Start the tunnel:" -ForegroundColor White
Write-Host "     cloudflared tunnel --config cloudflared-config.yml run" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Or run as Windows service:" -ForegroundColor White
Write-Host "     cloudflared service install" -ForegroundColor Cyan
Write-Host "     cloudflared service start" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
