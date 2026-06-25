# SPC Leather Costing Workspace Setup Script
# Checks python and configures local .venv

Write-Host "--- Starting Open Code AI Workspace Setup ---" -ForegroundColor Cyan

# 1. Check Python
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}

if ($pythonCmd) {
    $pythonVersion = & $pythonCmd --version
    Write-Host "Found Python executable '$pythonCmd': $pythonVersion" -ForegroundColor Green
} else {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.8+ first."
    Exit 1
}

# 2. Create Virtual Environment
if (Test-Path ".venv") {
    Write-Host "Virtual environment '.venv' already exists. Skipping creation." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment '.venv' using $pythonCmd..." -ForegroundColor Cyan
    & $pythonCmd -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    } else {
        Write-Error "Failed to create virtual environment."
        Exit 1
    }
}

# 3. Upgrade pip and Install Dependencies
Write-Host "Installing dependencies in virtual environment..." -ForegroundColor Cyan
& ".\.venv\Scripts\pip.exe" install --upgrade pip
& ".\.venv\Scripts\pip.exe" install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "All dependencies installed successfully." -ForegroundColor Green
    Write-Host "Setup Complete. Active environment by running: .venv\Scripts\Activate.ps1" -ForegroundColor Cyan
} else {
    Write-Error "Failed to install dependencies."
    Exit 1
}
