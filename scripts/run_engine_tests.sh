#!/bin/bash

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TESTCASE="${1:-global}"

shift || true

"$ROOT/run.sh" "$ROOT/tests/engine" test "$TESTCASE" "$@"
