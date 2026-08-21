#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON="python3"
[[ -x "$ROOT_DIR/.venv/bin/python" ]] && PYTHON="$ROOT_DIR/.venv/bin/python"
"$PYTHON" -m compileall -q app scripts eval
"$PYTHON" -m pytest -q
"$PYTHON" scripts/evaluate.py
