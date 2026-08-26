#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
mkdir -p results

CATALOG_ROWS="$(mktemp)"
WORKTREES=()
cleanup() {
  for wt in "${WORKTREES[@]:-}"; do
    git worktree remove --force "$wt" >/dev/null 2>&1 || true
    rm -rf "$wt" >/dev/null 2>&1 || true
  done
  rm -f "$CATALOG_ROWS"
}
trap cleanup EXIT

publish_path() {
  local branch="$1"
  local source_path="$2"
  local dest_path="$3"
  local kind="$4"

  if ! git ls-remote --exit-code --heads origin "refs/heads/$branch" >/dev/null 2>&1; then
    return 0
  fi

  local safe wt sha count
  safe="${branch//\//_}"
  wt="/tmp/spider_publish_${safe}_$$"
  git fetch -q origin "$branch:refs/remotes/origin/$branch"
  git worktree add --detach "$wt" "origin/$branch" >/dev/null
  WORKTREES+=("$wt")
  sha="$(git rev-parse "origin/$branch")"

  if [[ -d "$wt/$source_path" ]]; then
    mkdir -p "$dest_path"
    cp -a "$wt/$source_path/." "$dest_path/"
    count="$(find "$wt/$source_path" -type f | wc -l | tr -d ' ')"
  else
    count=0
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$kind" "$branch" "$sha" "$dest_path" "$count" >> "$CATALOG_ROWS"
}

for lane in graph physics intel runtime product cto; do
  publish_path "lab/$lane" "results/$lane" "results/$lane" "core"
done

while IFS= read -r ref; do
  [[ -n "$ref" ]] || continue
  branch="${ref#refs/heads/}"
  team="${branch#lab/frontier/}"
  [[ -n "$team" && "$team" != "$branch" ]] || continue
  publish_path "$branch" "results/frontier/$team" "results/frontier/$team" "frontier"
done < <(git ls-remote --heads origin 'refs/heads/lab/frontier/*' | awk '{print $2}' | sort)

python3 - "$CATALOG_ROWS" <<'PY'
import json
import sys
from pathlib import Path

rows = []
for line in Path(sys.argv[1]).read_text().splitlines():
    if not line.strip():
        continue
    kind, branch, sha, path, count = line.split("\t")
    rows.append({
        "kind": kind,
        "source_branch": branch,
        "source_sha": sha,
        "published_path": path,
        "source_file_count": int(count),
    })
rows.sort(key=lambda r: (r["kind"], r["published_path"], r["source_branch"]))
Path("results/CATALOG.json").write_text(json.dumps({
    "schema_version": 1,
    "policy": "main/results is a non-destructive catalog copied from accepted lab/* branches; lab branches remain scientific sources of truth",
    "sources": rows,
}, indent=2, sort_keys=False) + "\n")
PY

# Safety invariant: publication may add/update accepted results and the catalog,
# but it must never delete an existing main/results history entry.
if git diff --name-status -- results | awk '$1 == "D" {found=1} END {exit found ? 0 : 1}'; then
  echo "::error::Accepted-result publisher attempted to delete historical main/results files."
  git diff --name-status -- results
  exit 1
fi
