#!/usr/bin/env bash
set -euo pipefail

SAFE_BRANCH="${SPIDER_MAIN_SAFETY_BRANCH:-safety/main-lkg}"
MAIN_REMOTE_REF="refs/remotes/origin/main"
SAFE_REMOTE_REF="refs/remotes/origin/${SAFE_BRANCH}"

# Read fresh remote state. A transient fetch failure is harmless: subsequent
# rev-parse/push operations fail closed rather than rewriting any protected ref.
git fetch origin \
  '+refs/heads/main:refs/remotes/origin/main' \
  "+refs/heads/${SAFE_BRANCH}:refs/remotes/origin/${SAFE_BRANCH}" \
  --no-tags || true

MAIN_SHA=$(git rev-parse "$MAIN_REMOTE_REF")

if git show-ref --verify --quiet "$SAFE_REMOTE_REF"; then
  SAFE_SHA=$(git rev-parse "$SAFE_REMOTE_REF")

  if [[ "$SAFE_SHA" == "$MAIN_SHA" ]]; then
    echo "SPIDER_MAIN_SAFETY_CURRENT main=$MAIN_SHA safe=$SAFE_SHA"
  elif git merge-base --is-ancestor "$SAFE_SHA" "$MAIN_SHA"; then
    # Deliberately non-forced. If the rescue pointer changed concurrently,
    # GitHub rejects the update and the old rescue point remains intact.
    git push origin "$MAIN_SHA:refs/heads/${SAFE_BRANCH}"
    echo "SPIDER_MAIN_SAFETY_ADVANCED from=$SAFE_SHA to=$MAIN_SHA"
  elif git merge-base --is-ancestor "$MAIN_SHA" "$SAFE_SHA"; then
    echo "::error::MAIN HISTORY REGRESSION DETECTED. main=$MAIN_SHA is behind ${SAFE_BRANCH}=$SAFE_SHA. Rescue pointer preserved."
    exit 1
  else
    echo "::error::MAIN HISTORY DIVERGENCE DETECTED. main=$MAIN_SHA ${SAFE_BRANCH}=$SAFE_SHA. Rescue pointer preserved."
    exit 1
  fi
else
  # Bootstrap only when the rescue pointer truly does not exist. Never rewrite it.
  git push origin "$MAIN_SHA:refs/heads/${SAFE_BRANCH}"
  echo "SPIDER_MAIN_SAFETY_BOOTSTRAPPED safe=$MAIN_SHA"
fi

# A second, low-churn recovery layer: one immutable snapshot tag per UTC day.
# It is never moved or overwritten. This protects against an accidental deletion
# of the rolling rescue branch without generating a tag for every Codex commit.
DAY_TAG="spider-main-daily-$(date -u +%Y%m%d)"
if git ls-remote --exit-code --tags origin "refs/tags/${DAY_TAG}" >/dev/null 2>&1; then
  echo "SPIDER_MAIN_DAILY_SNAPSHOT_EXISTS tag=$DAY_TAG"
else
  git tag "$DAY_TAG" "$MAIN_SHA"
  git push origin "refs/tags/${DAY_TAG}"
  echo "SPIDER_MAIN_DAILY_SNAPSHOT_CREATED tag=$DAY_TAG sha=$MAIN_SHA"
fi
