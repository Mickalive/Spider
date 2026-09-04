#!/usr/bin/env bash
set -euo pipefail

# Never rewrite the script file underneath a running Bash process when restoring the
# lane snapshot. Re-exec an ephemeral copy first.
if [[ "${SPIDER_CHECKPOINT_REEXEC:-0}" != "1" ]]; then
  TMP_CHECKPOINT="/tmp/spider-checkpoint-${GITHUB_RUN_ID:-local}-${RANDOM}.sh"
  cp "$0" "$TMP_CHECKPOINT"
  chmod +x "$TMP_CHECKPOINT"
  SPIDER_CHECKPOINT_REEXEC=1 exec bash "$TMP_CHECKPOINT" "$@"
fi

STAGE=${1:?stage}
LANE=${2:?lane}
EXP_ID=${3:?experiment id}
MSG=${4:-"SPIDER R2 checkpoint"}
EXP="research/experiments/$EXP_ID"
HELPER=${SPIDER_CONTROL_HELPER:-/tmp/spider-control-plane.py}
ROOT=${GITHUB_WORKSPACE:-$PWD}

[[ -f "$HELPER" ]] || { echo "::error::missing control-plane helper $HELPER"; exit 69; }

paths=()
case "$STAGE" in
  init)
    paths+=("$EXP/request.json" "$EXP/spec.json" "$EXP/prereg.md" "research/lanes/$LANE/state.json")
    ;;
  design)
    paths+=("$EXP/spec.json" "$EXP/prereg.md" "$EXP/freeze.json" "$EXP/failure.json" "$EXP/model_design.json" "research/lanes/$LANE/state.json")
    ;;
  execution-base)
    paths+=("$EXP/execution_checkpoint.json" "research/lanes/$LANE/state.json")
    ;;
  execute)
    paths+=("$EXP" "research/lanes/$LANE/state.json")
    while IFS= read -r p; do [[ -n "$p" ]] && paths+=("$p"); done < <(jq -r --arg lane "$LANE" '.lanes[$lane].allowed_code_roots[]?' research/lanes/registry.json)
    ;;
  audit)
    paths+=("$EXP/audit.json" "$EXP/failure.json" "$EXP/model_audit.json" "research/lanes/$LANE/state.json")
    ;;
  director)
    paths+=("$EXP/verdict.json" "$EXP/handoff.json" "$EXP/failure.json" "$EXP/model_director.json" "research/lanes/$LANE/state.json")
    if [[ "$LANE" == product ]]; then
      while IFS= read -r p; do [[ -n "$p" ]] && paths+=("$p"); done < <(jq -r '.lanes.product.allowed_code_roots[]?' research/lanes/registry.json)
    fi
    ;;
  failure)
    paths+=("$EXP/failure.json" "research/lanes/$LANE/state.json")
    ;;
  *) echo "unknown checkpoint stage: $STAGE" >&2; exit 64 ;;
esac

# Canonical control files are a live overlay from main, never lane evidence.
# Restore the lane's own control-plane bytes before staging, then reapply main on exit.
python "$HELPER" restore --root "$ROOT"
restage_control() { python "$HELPER" stage --root "$ROOT" >/dev/null 2>&1 || true; }
trap restage_control EXIT

for p in "${paths[@]}"; do
  git add -u -- "$p" 2>/dev/null || true
  if [[ -e "$p" || -L "$p" ]]; then git add -- "$p"; fi
done

if git diff --cached --quiet; then
  echo "SPIDER_CHECKPOINT_NOOP stage=$STAGE"
  exit 0
fi

git commit -m "$MSG"
git push origin "HEAD:refs/heads/lab2/$LANE"
echo "SPIDER_CHECKPOINT_OK stage=$STAGE lane=$LANE"
