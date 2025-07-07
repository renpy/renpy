#!/bin/bash
set -e

# Download and install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create/update venv and install dependencies
echo "Setting up development environment..."
# XXX: There is no way to check if it succeeded.
uv sync --extra dev --no-install-project
echo "Development environment ready!"
