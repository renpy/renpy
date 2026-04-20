#!/bin/bash

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

"$ROOT/.venv/bin/python" -m unittest discover -s "$ROOT/tests/unit" -t "$ROOT"
