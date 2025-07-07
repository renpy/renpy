# Download and install uv if not present
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

# Create/update venv and install dependencies
Write-Host "Setting up development environment..."
# XXX: There is no way to check if it succeeded.
uv sync --extra dev --no-install-project
Write-Host "Development environment ready!"
