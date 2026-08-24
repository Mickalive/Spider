#!/usr/bin/env bash
set -uo pipefail

REAL="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
MAX_ATTEMPTS="${OPENCODE_MAX_ATTEMPTS:-6}"
RETRY_DELAY="${OPENCODE_RETRY_DELAY_SECONDS:-300}"
NETWORK_STALL_SECONDS="${OPENCODE_NETWORK_STALL_SECONDS:-300}"
LOG="$(mktemp)"
STALL_FLAG="$(mktemp)"
CONTROL_ACTIVE=false
CHILD_PID=""
MONITOR_PID=""

NETWORK_RE='(network_error|NetworkError|network error|fetch failed|APIConnectionError|ECONNRESET|ECONNREFUSED|EAI_AGAIN|ENETUNREACH|ENOTFOUND|ETIMEDOUT|timed out|timeout|socket hang up|connection (reset|refused|closed|error)|upstream.*(reset|closed|unavailable|error)|HTTP[^0-9]*(429|500|502|503|504)|status[^0-9]*(429|500|502|503|504)|too many requests|rate.?limit|service unavailable|bad gateway|gateway timeout|temporar(y|ily) unavailable|TLS|SSL.*error)'

# Shared governance/control-plane files are temporarily overlaid from main so
# persistent lab/* branches never execute stale role definitions. Lane-owned
# scientific directives stay on their own branches.
CONTROL_PATHS=(
  ".opencode/agents"
  "docs/roles"
  "SPIDER_MASTER_PROMPT.md"
  "directives/AUDITOR.md"
  "directives/LANE_DIRECTOR.md"
  "directives/LAB_DIRECTOR.md"
  "directives/INTEL_REPRO.md"
  "directives/INTEL_AUDITOR.md"
  "directives/INTEL_DIRECTOR.md"
  "directives/PRODUCT_DIRECTOR.md"
  "intel/competitor_seed.json"
)

restore_control_plane() {
  if [[ "$CONTROL_ACTIVE" != true ]]; then
    return 0
  fi
  git reset -q HEAD -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
  git checkout -q -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
  git clean -fdq -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
  CONTROL_ACTIVE=false
}

stop_children() {
  if [[ -n "$MONITOR_PID" ]] && kill -0 "$MONITOR_PID" 2>/dev/null; then
    kill "$MONITOR_PID" 2>/dev/null || true
    wait "$MONITOR_PID" 2>/dev/null || true
  fi
  MONITOR_PID=""
  if [[ -n "$CHILD_PID" ]] && kill -0 "$CHILD_PID" 2>/dev/null; then
    kill -TERM "$CHILD_PID" 2>/dev/null || true
    sleep 2
    kill -KILL "$CHILD_PID" 2>/dev/null || true
    wait "$CHILD_PID" 2>/dev/null || true
  fi
  CHILD_PID=""
}

cleanup() {
  stop_children
  restore_control_plane
  rm -f "$LOG" "$STALL_FLAG"
}

on_int() {
  trap - INT TERM EXIT
  cleanup
  exit 130
}

on_term() {
  trap - INT TERM EXIT
  cleanup
  exit 143
}

trap cleanup EXIT
trap on_int INT
trap on_term TERM

prepare_control_plane() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return 0
  fi

  local dirty
  dirty="$(git status --porcelain -- "${CONTROL_PATHS[@]}" 2>/dev/null || true)"
  if [[ -n "$dirty" ]]; then
    echo "::warning::SPIDER control-plane paths are locally dirty; refusing temporary main overlay." >&2
    printf '%s\n' "$dirty" >&2
    return 0
  fi

  if ! git fetch -q origin main; then
    echo "::warning::Could not fetch origin/main control plane; using branch-local role definitions for this call." >&2
    return 0
  fi

  if ! git checkout -q origin/main -- "${CONTROL_PATHS[@]}"; then
    echo "::warning::Could not overlay full origin/main control plane; restoring branch-local files." >&2
    git reset -q HEAD -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
    git checkout -q -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
    git clean -fdq -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
    return 0
  fi

  CONTROL_ACTIVE=true
  echo "SPIDER control plane: using current origin/main agent definitions and formal job descriptions for this invocation."
}

monitor_network_stall() {
  local pid="$1"
  local last_size=0
  local last_change
  local now size
  local network_pending=false
  local network_seen_at=0
  local network_size=0
  last_change=$(date +%s)

  while kill -0 "$pid" 2>/dev/null; do
    now=$(date +%s)
    size=$(stat -c%s "$LOG" 2>/dev/null || echo 0)

    if [[ "$size" -ne "$last_size" ]]; then
      last_size="$size"
      last_change="$now"
    fi

    if [[ "$network_pending" == false ]] && grep -Eiq "$NETWORK_RE" "$LOG" 2>/dev/null; then
      network_pending=true
      network_seen_at="$now"
      network_size="$size"
      last_change="$now"
      echo "::warning::OpenCode/Ox network signature detected; watching for a ${NETWORK_STALL_SECONDS}s stall before aborting the call." >&2
    elif [[ "$network_pending" == true && "$size" -gt "$network_size" && $((now - network_seen_at)) -ge 30 ]]; then
      # Sustained output after the network error strongly suggests the process
      # recovered. Clear the pending stall condition rather than killing valid work.
      network_pending=false
    fi

    if [[ "$network_pending" == true && $((now - last_change)) -ge "$NETWORK_STALL_SECONDS" ]]; then
      echo "SPIDER_NETWORK_STALL_ABORT" > "$STALL_FLAG"
      echo "::warning::OpenCode/Ox produced a network error and then no output for ${NETWORK_STALL_SECONDS}s; terminating only this stalled call so the bounded retry loop can proceed." >&2
      kill -TERM "$pid" 2>/dev/null || true
      sleep 10
      if kill -0 "$pid" 2>/dev/null; then
        kill -KILL "$pid" 2>/dev/null || true
      fi
      return 0
    fi

    sleep 5
  done
}

prepare_control_plane

for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
  : > "$LOG"
  : > "$STALL_FLAG"
  echo "OpenCode/Ox attempt ${attempt}/${MAX_ATTEMPTS}."

  # Process substitution keeps live logs visible while giving us the real
  # OpenCode PID, so the monitor can terminate a genuinely stalled call only.
  "$REAL" "$@" > >(tee "$LOG") 2>&1 &
  CHILD_PID=$!
  monitor_network_stall "$CHILD_PID" &
  MONITOR_PID=$!

  wait "$CHILD_PID" 2>/dev/null
  rc=$?
  CHILD_PID=""

  if [[ -n "$MONITOR_PID" ]] && kill -0 "$MONITOR_PID" 2>/dev/null; then
    kill "$MONITOR_PID" 2>/dev/null || true
  fi
  wait "$MONITOR_PID" 2>/dev/null || true
  MONITOR_PID=""
  sleep 1

  if grep -Fq 'SPIDER_NETWORK_STALL_ABORT' "$STALL_FLAG" 2>/dev/null; then
    rc=75
  fi

  if [[ "$rc" -eq 0 ]]; then
    exit 0
  fi

  if ! grep -Eiq "$NETWORK_RE" "$LOG" 2>/dev/null && ! grep -Fq 'SPIDER_NETWORK_STALL_ABORT' "$STALL_FLAG" 2>/dev/null; then
    echo "::error::SPIDER_OX_NONTRANSIENT exit=$rc; watchdog will not retry this failure." >&2
    exit "$rc"
  fi

  if [[ "$attempt" -eq "$MAX_ATTEMPTS" ]]; then
    echo "::error::SPIDER_TRANSIENT_OX_EXHAUSTED attempts=$MAX_ATTEMPTS exit=$rc" >&2
    exit "$rc"
  fi

  echo "::warning::Transient OpenCode/Ox outage; retrying in ${RETRY_DELAY}s." >&2
  sleep "$RETRY_DELAY"
done

exit 1
