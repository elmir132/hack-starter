#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${HACK_STARTER_PORT:-8765}"
LOG_FILE="$(mktemp "${TMPDIR:-/tmp}/hack-starter.XXXXXX")"
SERVER_PID=""

cleanup() {
  if [[ -n "$SERVER_PID" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  rm -f "$LOG_FILE"
}
trap cleanup EXIT INT TERM

cd "$ROOT_DIR"
if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON="$ROOT_DIR/.venv/bin/python"
else
  PYTHON="${PYTHON:-python3}"
fi
if ! "$PYTHON" -c "import fastapi, uvicorn" 2>/dev/null; then
  echo "FastAPI or uvicorn is not installed for $PYTHON." >&2
  echo "Run: python3 -m venv .venv && .venv/bin/python -m pip install -e '.[dev]'" >&2
  exit 1
fi
"$PYTHON" -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT" >"$LOG_FILE" 2>&1 &
SERVER_PID=$!
API_URL="http://127.0.0.1:$PORT"

READY=""
for _ in $(seq 1 40); do
  if curl --silent --fail "$API_URL/api/health" >/dev/null; then
    READY=1
    break
  fi
  sleep 0.25
done

if [[ -z "$READY" ]]; then
  cat "$LOG_FILE"
  echo "FastAPI did not start on port $PORT." >&2
  exit 1
fi

echo "Health response:"
curl --silent --show-error --fail "$API_URL/api/health" | python3 -m json.tool
echo
echo "Example brief response:"
curl --silent --show-error --fail \
  -H 'Content-Type: application/json' \
  --data-binary @scripts/demo_payload.json \
  "$API_URL/api/brief" | python3 -m json.tool
