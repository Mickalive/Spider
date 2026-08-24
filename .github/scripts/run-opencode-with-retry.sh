#!/usr/bin/env bash
set -uo pipefail

REAL="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
MAX_ATTEMPTS="${OPENCODE_MAX_ATTEMPTS:-6}"
RETRY_DELAY="${OPENCODE_RETRY_DELAY_SECONDS:-300}"
LOG="$(mktemp)"
CONTROL_ACTIVE=false

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
  # Safe because prepare_control_plane refuses to overlay if any of these paths
  # were dirty beforehand. This removes files that exist on main but not on the
  # persistent lane, preventing accidental governance-file commits.
  git clean -fdq -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
  CONTROL_ACTIVE=false
}

cleanup() {
  restore_control_plane
  rm -f "$LOG"
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

prepare_control_plane

for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
  : > "$LOG"
  echo "OpenCode/Ox attempt ${attempt}/${MAX_ATTEMPTS}."

  set +e
  "$REAL" "$@" 2>&1 | tee "$LOG"
  rc=${PIPESTATUS[0]}
  set -e

  if [[ "$rc" -eq 0 ]]; then
    exit 0
  fi

  if ! grep -Eiq '(network_error|NetworkError|network error|fetch failed|APIConnectionError|ECONNRESET|ECONNREFUSED|EAI_AGAIN|ENETUNREACH|ENOTFOUND|ETIMEDOUT|timed out|timeout|socket hang up|connection (reset|refused|closed|error)|upstream.*(reset|closed|unavailable|error)|HTTP[^0-9]*(429|500|502|503|504)|status[^0-9]*(429|500|502|503|504)|too many requests|rate.?limit|service unavailable|bad gateway|gateway timeout|temporar(y|ily) unavailable|TLS|SSL.*error)' "$LOG"; then
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
