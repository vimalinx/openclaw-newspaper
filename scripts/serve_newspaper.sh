#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"$(dirname "$0")/.." && pwd)"
PORT="${1:-39117}"
HOST="127.0.0.1"

cd "$ROOT"
echo "[OpenClaw-Newspaper] serving $ROOT at http://$HOST:$PORT/site/index.html"
exec python -m http.server "$PORT" --bind "$HOST"
