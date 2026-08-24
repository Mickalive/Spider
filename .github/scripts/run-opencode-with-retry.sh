#!/usr/bin/env bash
set -uo pipefail

REAL="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
MAX_ATTEMPTS="${OPENCODE_MAX_ATTEMPTS:-6}"
RETRY_DELAY="${OPENCODE_RETRY_DELAY_SECONDS:-300}"
LOG="$(mktemp)"
CONTROL_ACTIVE=false

# These files define roles/governance shared across persistent lanes. They are
# temporarily overlaid from origin/main for each OpenCode invocation so a
# long-lived lab/* branch can never execute a stale agent/job description.
# Lane-owned scientific directives (GRAPH.md, PHYSICS.md, INTEL.md) are
# deliberately excluded because their Directors evolve them on lab/*.
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

prepare_control_plane() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return 0
  fi

  # Never overwrite pre-existing local work in governance paths. In normal
  # GitHub jobs these paths are clean; a dirty path is treated conservatively.
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
    git clean -fdq -- .opencode/agents docs/roles 2>/dev/null || true
    return 0
  fi

  CONTROL_ACTIVE=true
  echo "SPIDER control plane: using current origin/main agent definitions and formal job descriptions for this invocation."
}

restore_control_plane() {
  if [[ "$CONTROL_ACTIVE" != true ]]; then
    return 0
  fi
  # Restore exactly the persistent lane's own tracked control files before the
  # caller snapshots/commits scientific work. Files that existed on main but
  # not on the lane become untracked after reset and are then removed.
  git reset -q HEAD -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
  git checkout -q -- "${CONTROL_PATHS[@]}" 2>/dev/null || true
  git clean -fdq -- .opencode/agents docs/roles 2>/dev/null || true
  CONTROL_ACTIVE=false
}

cleanup() {
  restore_control_plane
  rm -f "$LOG"
}
trap cleanup EXIT INT TERM

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
