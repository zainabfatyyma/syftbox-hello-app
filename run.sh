#!/bin/bash
set -euo pipefail

PID_FILE="server.pid"
LOG_FILE="logs/web.log"

mkdir -p logs

is_running() {
  local pid="$1"
  if [[ -z "$pid" ]]; then
    return 1
  fi
  ps -p "$pid" > /dev/null 2>&1
}

if [[ -f "$PID_FILE" ]]; then
  EXISTING_PID="$(cat "$PID_FILE")"
  if is_running "$EXISTING_PID"; then
    echo "Web interface already running (pid=$EXISTING_PID)"
    exit 0
  fi
fi

echo "Starting SyftBox Hello App web interface..."
nohup python3 main.py serve >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "Started (pid=$(cat "$PID_FILE"))"