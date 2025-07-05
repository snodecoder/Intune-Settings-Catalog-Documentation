# Create a Python virtual environment named 'venv' and activate it

# Ensure Python is installed and available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not available in PATH."
    exit 1
}

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
$venvActivateScript = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvActivateScript) {
    & $venvActivateScript
    Write-Host "Virtual environment 'venv' activated."
} else {
    Write-Error "Failed to activate the virtual environment. Ensure it was created successfully."
}

python.exe -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
