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
START_HEAD=""
REPAIR_INTENT=false

NETWORK_RE='(network_error|NetworkError|network error|fetch failed|APIConnectionError|ECONNRESET|ECONNREFUSED|EAI_AGAIN|ENETUNREACH|ENOTFOUND|ETIMEDOUT|timed out|timeout|socket hang up|connection (reset|refused|closed|error)|upstream.*(reset|closed|unavailable|error)|HTTP[^0-9]*(429|500|502|503|504)|status[^0-9]*(429|500|502|503|504)|too many requests|rate.?limit|service unavailable|bad gateway|gateway timeout|temporar(y|ily) unavailable|TLS|SSL.*error)'

# Shared governance/control-plane files are temporarily overlaid from main so
# persistent lab/* branches never execute stale role definitions. Lane-owned
# scientific directives stay on their own branches.
CONTROL_PATHS=(
  "AGENTS.md"
  ".opencode/agents"
  "docs/agents"
  "docs/roles"
  "SPIDER_MASTER_PROMPT.md"
  "SPIDER_ARCHITECTURE_V2.md"
  "SPIDER_ARCHITECTURE_V3.md"
  "directives/CAPABILITY_CAPSULE.md"
  "directives/AUDITOR.md"
  "directives/LANE_DIRECTOR.md"
  "directives/LAB_DIRECTOR.md"
  "directives/INTEL_REPRO.md"
  "directives/INTEL_AUDITOR.md"
  "directives/INTEL_DIRECTOR.md"
  "directives/PRODUCT_DIRECTOR.md"
  "directives/PRODUCT_OPTIMIZATION.md"
  "intel/competitor_seed.json"
)

restore_path_from_head() {
  local path="$1"
  git reset -q HEAD -- "$path" 2>/dev/null || true

  if git cat-file -e "HEAD:$path" 2>/dev/null; then
    git checkout -q -- "$path" 2>/dev/null || true
  else
    rm -rf -- "$path"
  fi

  git clean -fdq -- "$path" 2>/dev/null || true
}

restore_control_plane() {
  if [[ "$CONTROL_ACTIVE" != true ]]; then
    return 0
  fi
  for path in "${CONTROL_PATHS[@]}"; do
    restore_path_from_head "$path"
  done
  CONTROL_ACTIVE=false

  local residue=""
  for path in "${CONTROL_PATHS[@]}"; do
    if [[ -n "$(git status --porcelain -- "$path" 2>/dev/null || true)" ]]; then
      residue+="$path "
    fi
  done
  if [[ -n "$residue" ]]; then
    echo "::error::Control-plane restoration left residue in: $residue" >&2
    return 1
  fi
}

cleanup() {
  if [[ -n "$MONITOR_PID" ]]; then
    kill "$MONITOR_PID" 2>/dev/null || true
  fi
  if [[ -n "$CHILD_PID" ]]; then
    kill "$CHILD_PID" 2>/dev/null || true
  fi
  restore_control_plane || true
  rm -f "$LOG" "$STALL_FLAG"
}
trap cleanup EXIT INT TERM

stage_control_plane() {
  local source_ref="origin/main"
  if ! git fetch -q origin main; then
    echo "::warning::Unable to refresh origin/main control plane; using workflow checkout definitions."
    source_ref="${GITHUB_SHA:-HEAD}"
  fi

  for path in "${CONTROL_PATHS[@]}"; do
    if git cat-file -e "$source_ref:$path" 2>/dev/null; then
      git checkout -q "$source_ref" -- "$path"
    fi
  done
  CONTROL_ACTIVE=true

  rm -rf /tmp/spider_control
  mkdir -p /tmp/spider_control
  for path in AGENTS.md .opencode/agents docs/agents docs/roles SPIDER_MASTER_PROMPT.md SPIDER_ARCHITECTURE_V2.md SPIDER_ARCHITECTURE_V3.md directives/CAPABILITY_CAPSULE.md directives/AUDITOR.md directives/LANE_DIRECTOR.md directives/LAB_DIRECTOR.md directives/INTEL_REPRO.md directives/INTEL_AUDITOR.md directives/INTEL_DIRECTOR.md directives/PRODUCT_DIRECTOR.md directives/PRODUCT_OPTIMIZATION.md; do
    if [[ -e "$path" ]]; then
      mkdir -p "/tmp/spider_control/$(dirname "$path")"
      cp -a "$path" "/tmp/spider_control/$path"
    fi
  done
}

validate_agent_card() {
  local requested=""
  local prev=""
  local arg
  local registry="docs/agents/AGENT_CARDS.md"

  if [[ ! -f "$registry" ]]; then
    echo "::error::Missing canonical SPIDER agent registry: $registry" >&2
    return 64
  fi

  # Every configured custom agent must have exactly one operating card.
  local bad=0
  local file id count
  while IFS= read -r file; do
    id="${file#.opencode/agents/}"
    id="${id%.md}"
    count=$(grep -Fc "<!-- AGENT_CARD: ${id} " "$registry" || true)
    if [[ "$count" -ne 1 ]]; then
      echo "::error::Agent '${id}' has ${count} canonical cards; expected exactly 1." >&2
      bad=1
    fi
  done < <(find .opencode/agents -type f -name '*.md' | sort)

  # Every card must correspond to an actual custom-agent definition.
  while IFS= read -r id; do
    [[ -n "$id" ]] || continue
    if [[ ! -f ".opencode/agents/${id}.md" ]]; then
      echo "::error::Canonical card '${id}' has no matching .opencode agent definition." >&2
      bad=1
    fi
  done < <(grep '^<!-- AGENT_CARD:' "$registry" | awk '{print $3}')

  [[ "$bad" -eq 0 ]] || return 66

  for arg in "$@"; do
    if [[ "$prev" == "--agent" ]]; then
      requested="$arg"
      break
    fi
    case "$arg" in
      --agent=*) requested="${arg#--agent=}"; break ;;
    esac
    prev="$arg"
  done

  # Some OpenCode invocations intentionally use a built-in/default agent.
  [[ -n "$requested" ]] || return 0

  local marker
  marker=$(grep -F "<!-- AGENT_CARD: ${requested} " "$registry" | head -n1 || true)
  if [[ -z "$marker" ]]; then
    echo "::error::Agent '${requested}' has no canonical operating card. Refusing role improvisation." >&2
    return 64
  fi

  if [[ "$marker" == *"status=LEGACY_DISABLED"* && "${SPIDER_ALLOW_LEGACY_AGENT:-0}" != "1" ]]; then
    echo "::error::Agent '${requested}' is LEGACY_DISABLED in the canonical registry. Explicit reactivation is required." >&2
    return 65
  fi

  echo "SPIDER_AGENT_CARD_OK agent=${requested} registry=complete"
}

# Same-cycle repairs are not allowed to silently succeed with no durable work.
# OpenCode has been observed to return rc=0 after an auto-rejected permission
# request on a retry. Detect repair intent from the explicit workflow prompt;
# callers may also force the invariant with SPIDER_REQUIRE_DELTA=1.
for arg in "$@"; do
  if [[ "$arg" == REPAIR\ * || "$arg" == *" REPAIR "* ]]; then
    REPAIR_INTENT=true
    break
  fi
done
[[ "${SPIDER_REQUIRE_DELTA:-0}" == "1" ]] && REPAIR_INTENT=true

stage_control_plane
START_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "")
validate_agent_card "$@"
rc=$?
if [[ "$rc" -ne 0 ]]; then
  restore_control_plane || true
  exit "$rc"
fi

run_once() {
  : > "$LOG"
  rm -f "$STALL_FLAG"

  # Re-pin every retry to the real Actions workspace. A previous Runtime retry
  # drifted to the parent directory and triggered an external_directory denial.
  local workdir="${GITHUB_WORKSPACE:-$PWD}"
  (
    cd "$workdir" || exit 70
    "$REAL" "$@"
  ) > >(tee -a "$LOG") 2> >(tee -a "$LOG" >&2) &
  CHILD_PID=$!

  (
    local last_size=0 last_change now size
    last_change=$(date +%s)
    while kill -0 "$CHILD_PID" 2>/dev/null; do
      sleep 15
      size=$(wc -c < "$LOG" 2>/dev/null || echo 0)
      now=$(date +%s)
      if [[ "$size" -ne "$last_size" ]]; then
        last_size="$size"
        last_change="$now"
      elif (( now - last_change >= NETWORK_STALL_SECONDS )); then
        if grep -Eiq "$NETWORK_RE" "$LOG"; then
          echo "SPIDER_NETWORK_STALL_DETECTED after ${NETWORK_STALL_SECONDS}s" | tee -a "$LOG" >&2
          touch "$STALL_FLAG"
          kill "$CHILD_PID" 2>/dev/null || true
          sleep 5
          kill -9 "$CHILD_PID" 2>/dev/null || true
          exit 0
        fi
        last_change="$now"
      fi
    done
  ) &
  MONITOR_PID=$!

  wait "$CHILD_PID"
  local rc=$?
  kill "$MONITOR_PID" 2>/dev/null || true
  wait "$MONITOR_PID" 2>/dev/null || true
  CHILD_PID=""
  MONITOR_PID=""

  if [[ -f "$STALL_FLAG" ]]; then
    return 75
  fi
  return "$rc"
}

attempt=1
while (( attempt <= MAX_ATTEMPTS )); do
  echo "SPIDER_OPENCODE_ATTEMPT=$attempt/$MAX_ATTEMPTS"
  run_once "$@"
  rc=$?

  if [[ "$rc" -eq 0 ]]; then
    if ! restore_control_plane; then
      exit 1
    fi

    if [[ "$REPAIR_INTENT" == true ]]; then
      CURRENT_HEAD=$(git rev-parse HEAD 2>/dev/null || echo "")
      WORKTREE_DELTA=$(git status --porcelain 2>/dev/null || true)
      if [[ "$CURRENT_HEAD" == "$START_HEAD" && -z "$WORKTREE_DELTA" ]]; then
        echo "::error::SPIDER_ZERO_DELTA_REPAIR: OpenCode reported success but produced no durable repair delta." >&2
        echo "A same-cycle repair must change scoped artifacts or persist an explicit blocker record; zero-delta success is invalid." >&2
        exit 67
      fi
    fi
    exit 0
  fi

  if [[ "$rc" -eq 75 ]] || grep -Eiq "$NETWORK_RE" "$LOG"; then
    if (( attempt < MAX_ATTEMPTS )); then
      echo "::warning::Transient OpenCode/network failure on attempt $attempt; retrying after ${RETRY_DELAY}s."
      sleep "$RETRY_DELAY"
      attempt=$((attempt + 1))
      continue
    fi
    echo "SPIDER_TRANSIENT_OX_EXHAUSTED attempts=$MAX_ATTEMPTS" >&2
    restore_control_plane || true
    exit 75
  fi

  echo "OpenCode failed without a defensible transient-network signature; preserving failure (rc=$rc)." >&2
  restore_control_plane || true
  exit "$rc"
done

restore_control_plane || true
exit 75
