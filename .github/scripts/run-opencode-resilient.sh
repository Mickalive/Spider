#!/usr/bin/env bash
set -uo pipefail
ROLE=${1:?role}
RECEIPT=${2:?receipt path}
shift 2
REAL="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
MAX_ATTEMPTS="${SPIDER_MODEL_MAX_ATTEMPTS:-7}"
RETRY_DELAY="${SPIDER_MODEL_RETRY_DELAY_SECONDS:-25}"
STALL_SECONDS="${SPIDER_MODEL_STALL_SECONDS:-600}"
NETWORK_RE='(network_error|NetworkError|network error|fetch failed|APIConnectionError|ECONNRESET|ECONNREFUSED|EAI_AGAIN|ENETUNREACH|ENOTFOUND|ETIMEDOUT|timed out|socket hang up|connection (reset|refused|closed|error)|upstream.*(reset|closed|unavailable|error)|HTTP[^0-9]*(429|500|502|503|504)|status[^0-9]*(429|500|502|503|504)|too many requests|rate.?limit|service unavailable|bad gateway|gateway timeout|temporar(y|ily) unavailable|TLS|SSL.*error|internal server error|FreeUsageLimitError|provider error|model.*(unavailable|not found)|HTTP[^0-9]*403)'
LOG=$(mktemp)
STALL_FLAG=$(mktemp)
START_HEAD=$(git rev-parse HEAD)
START_BRANCH=$(git branch --show-current)
CHILD_PID=""; MONITOR_PID=""

mkdir -p "$(dirname "$RECEIPT")"
cleanup(){ [[ -z "$MONITOR_PID" ]] || kill "$MONITOR_PID" 2>/dev/null || true; [[ -z "$CHILD_PID" ]] || kill "$CHILD_PID" 2>/dev/null || true; rm -f "$LOG" "$STALL_FLAG"; }
trap cleanup EXIT INT TERM

mapfile -t CONFIGURED < <(jq -r --arg role "$ROLE" '.roles[$role][]? // empty' config/models.json)
DISCOVERED=()
if [[ -x "$REAL" ]]; then
  while IFS= read -r m; do [[ -n "$m" ]] && DISCOVERED+=("$m"); done < <("$REAL" models opencode 2>/dev/null | grep -Eo 'opencode/[A-Za-z0-9._:-]*free[A-Za-z0-9._:-]*' | sort -u || true)
fi
mapfile -t MODELS < <(printf '%s\n' "${CONFIGURED[@]}" "${DISCOVERED[@]}" | awk 'NF && !seen[$0]++')
if [[ -n "${SPIDER_EXCLUDE_MODEL:-}" ]]; then
  mapfile -t MODELS < <(printf '%s\n' "${MODELS[@]}" | grep -Fxv "$SPIDER_EXCLUDE_MODEL" || true)
fi
(( ${#MODELS[@]} > 0 )) || { echo "::error::No model candidates role=$ROLE"; exit 75; }

write_receipt(){
  local status="$1" model="$2" attempt="$3" rc="$4" category="$5"
  python - "$RECEIPT" "$status" "$model" "$attempt" "$rc" "$category" <<'PY'
import json, os, sys
from datetime import datetime, timezone
path,status,model,attempt,rc,category=sys.argv[1:]
with open(path,"w",encoding="utf-8") as f:
    json.dump({"status":status,"model":model,"attempt":int(attempt),"exit_code":int(rc),"category":category,"github_run_id":os.getenv("GITHUB_RUN_ID"),"github_run_attempt":os.getenv("GITHUB_RUN_ATTEMPT"),"recorded_at":datetime.now(timezone.utc).isoformat()},f,indent=2)
    f.write("\n")
PY
}

restore_agent_commits(){
  local head branch
  head=$(git rev-parse HEAD 2>/dev/null || true)
  branch=$(git branch --show-current 2>/dev/null || true)
  if [[ "$branch" != "$START_BRANCH" ]]; then
    echo "::error::Agent changed git branch from $START_BRANCH to $branch" >&2
    return 68
  fi
  if [[ "$head" != "$START_HEAD" ]]; then
    echo "::warning::Agent created commits; converting them back to workflow-owned worktree changes"
    git reset --mixed "$START_HEAD" >/dev/null || return 68
  fi
  return 0
}

run_once(){
  local model="$1"; shift
  : > "$LOG"; rm -f "$STALL_FLAG"
  local -a src=("$@") routed=()
  if [[ "${src[0]:-}" == run ]]; then routed=(run --model "$model" "${src[@]:1}"); else routed=("${src[@]}" --model "$model"); fi
  "$REAL" "${routed[@]}" > >(tee -a "$LOG") 2> >(tee -a "$LOG" >&2) & CHILD_PID=$!
  (
    last_size=0; last_change=$(date +%s)
    while kill -0 "$CHILD_PID" 2>/dev/null; do
      sleep 15
      size=$(wc -c < "$LOG" 2>/dev/null || echo 0); now=$(date +%s)
      if [[ "$size" -ne "$last_size" ]]; then last_size="$size"; last_change="$now";
      elif (( now-last_change >= STALL_SECONDS )) && grep -Eiq "$NETWORK_RE" "$LOG"; then
        echo "SPIDER_MODEL_NETWORK_STALL model=$model" | tee -a "$LOG" >&2
        touch "$STALL_FLAG"; kill "$CHILD_PID" 2>/dev/null || true; sleep 3; kill -9 "$CHILD_PID" 2>/dev/null || true; exit 0
      fi
    done
  ) & MONITOR_PID=$!
  wait "$CHILD_PID"; rc=$?
  kill "$MONITOR_PID" 2>/dev/null || true; wait "$MONITOR_PID" 2>/dev/null || true
  CHILD_PID=""; MONITOR_PID=""
  [[ -f "$STALL_FLAG" ]] && return 75
  return "$rc"
}

attempt=1; index=0
while (( attempt <= MAX_ATTEMPTS )); do
  model="${MODELS[$index]}"
  echo "SPIDER_MODEL_ATTEMPT=$attempt/$MAX_ATTEMPTS role=$ROLE model=$model"
  run_once "$model" "$@"; rc=$?
  restore_agent_commits; git_rc=$?
  if [[ "$git_rc" -ne 0 ]]; then write_receipt failure "$model" "$attempt" "$git_rc" control; exit "$git_rc"; fi
  if [[ "$rc" -eq 0 ]]; then write_receipt success "$model" "$attempt" 0 ok; echo "SPIDER_MODEL_SUCCESS model=$model"; exit 0; fi
  if [[ "$rc" -eq 75 ]] || grep -Eiq "$NETWORK_RE" "$LOG"; then
    write_receipt retry "$model" "$attempt" "$rc" transient
    if (( index + 1 < ${#MODELS[@]} )); then index=$((index+1)); else index=0; fi
    attempt=$((attempt+1)); sleep "$RETRY_DELAY"; continue
  fi
  write_receipt failure "$model" "$attempt" "$rc" substantive
  echo "::error::OpenCode failed without retryable provider/network signature rc=$rc model=$model" >&2
  exit "$rc"
done
write_receipt failure "${MODELS[$index]}" "$attempt" 75 transient-pool-exhausted
echo "::error::SPIDER_TRANSIENT_MODEL_POOL_EXHAUSTED" >&2
exit 75
