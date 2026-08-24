#!/usr/bin/env bash
set -uo pipefail

REAL="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
MAX_ATTEMPTS="${OPENCODE_MAX_ATTEMPTS:-6}"
RETRY_DELAY="${OPENCODE_RETRY_DELAY_SECONDS:-300}"
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT

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
