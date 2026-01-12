@echo off
REM The Continuum Report - Pipeline Runner for WoodsDen
REM Run this on WoodsDen where Claude CLI is installed
REM
REM Prerequisites:
REM   - Python 3.11+ with pip
REM   - Claude CLI installed and authenticated
REM   - Network share mounted: \\192.168.1.139\continuum as T:
REM
REM Usage:
REM   run_pipeline_local.bat          - Start pipeline
REM   run_pipeline_local.bat --dry-run - Dry run mode
REM   run_pipeline_local.bat --status  - Check status

echo ============================================================
echo THE CONTINUUM REPORT - LOCAL PIPELINE RUNNER
echo ============================================================
echo.

REM Check if running from correct location
if not exist "T:\continuum\scripts\pipeline_watcher.py" (
    echo ERROR: T:\continuum not found
    echo Mount \\192.168.1.139\continuum as T: drive first
    echo.
    echo net use T: \\192.168.1.139\continuum
    exit /b 1
)

REM Check Claude CLI
where claude >nul 2>&1
if errorlevel 1 (
    echo ERROR: Claude CLI not found in PATH
    echo Install with: npm install -g @anthropic-ai/claude-code
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    exit /b 1
)

REM Install dependencies if needed
echo Checking Python dependencies...
pip show watchdog >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install watchdog pydantic-settings requests
)

REM Change to scripts directory
cd /d T:\continuum\scripts

REM Run pipeline watcher (watches files and triggers stages)
echo.
echo Starting pipeline watcher...
echo Press Ctrl+C to stop
echo.

python pipeline_watcher.py %*
