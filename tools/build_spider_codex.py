#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "SPIDER_CODEX_ULTIME.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "Mickalive/Spider")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
MAX_BYTES = 90 * 1024 * 1024

TEXT_EXTS = {".md", ".json", ".txt", ".csv", ".tsv", ".yaml", ".yml", ".log"}
KEYWORDS = re.compile(
    r"(^|/)(experiment|experiments|result|results|report|reports|audit|audits|gate|gates|verdict|verdicts|metric|metrics|benchmark|benchmarks|measurement|measurements|finding|findings|ledger|ledgers|decision|decisions|handoff|handoffs|program|programs|claim|claims|evidence|test|tests)(/|_|-|\\.|$)",
    re.I,
)
TOP_AREAS = {"graph", "physics", "intel", "runtime", "product", "frontier", "state", ".spider", "docs", "evidence", "results", "reports"}


def sh(*args: str, check: bool = True) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        raise RuntimeError(f"command failed: {' '.join(args)}\n{p.stderr}")
    return p.stdout


def candidate(path: str) -> bool:
    p = path.replace("\\", "/")
    if p.startswith((".github/", ".opencode/", "archive/codex/")):
        return False
    ext = Path(p).suffix.lower()
    if ext not in TEXT_EXTS:
        return False
    if p.startswith("evidence/run-memory/"):
        return True
    if p.startswith(("results/", "reports/")):
        return True
    if p == "docs/EXPERIMENTS.md" or p.startswith(("docs/experiments/", "docs/results/", "docs/evidence/")):
        return True
    first = p.split("/", 1)[0]
    if first not in TOP_AREAS:
        return False
    return bool(KEYWORDS.search(p))


def fence_for(text: str) -> str:
    longest = 3
    for m in re.finditer(r"~+", text):
        longest = max(longest, len(m.group(0)) + 1)
    return "~" * longest


def api_json(url: str):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def all_action_runs() -> list[dict]:
    runs: list[dict] = []
    page = 1
    while True:
        data = api_json(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=100&page={page}")
        batch = data.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 100:
            raise RuntimeError("Actions pagination exceeded 10,000 runs; refusing silent truncation")
    return runs


def historical_seed() -> str:
    return r'''## A. Historical experiments preserved from the pre-autonomous SPIDER record

These results predate or sit outside the present GitHub evidence machinery. They are included so the Codex does not silently lose the local SPIDER/Web Physics experimental history.

### WP-000 — mechanics-only

- TASKS: 200
- SITES: 56
- RULE DIM-ACC: 0.6595
- RULE EXACT: 0.1603
- NN DIM-ACC: 0.5761

Claim ceiling: early mechanics-only evidence; not proof of universal Web physics.

### WP-001 — robustness over 100 splits

- Splits: 100
- RULE – SHUFFLE DIM: +0.0505
- empirical 95% interval: [+0.0249, +0.0756]

Claim ceiling: the tested rule advantage over shuffle persisted under this resampling protocol.

### WP-002 — raw next-state route

- Status: BLOCKED
- Required raw_dump access was unavailable because the source path depended on Globus / university-login infrastructure.
- This is an infrastructure/data-access block, not negative scientific evidence.
- Historical durable audit name: WP002_RAW_AUDIT.json.

### WP-002B — WebWorldData true next-state

- Dataset/source: Qwen/WebWorldData, public Hugging Face route
- TRAJECTORIES: 300
- TRANSITIONS: 901
- REPEATED TRAJECTORY HOLDOUTS: 100
- TRUE NEXT-STATE: YES
- WEBSITE HOLDOUT CLAIM: NO
- MEAN RULE DIM-ACC: 0.6238
- MEAN NN DIM-ACC: 0.6295
- MEAN SHUFFLE DIM-ACC: 0.5706
- RULE - SHUFFLE DIM: mean +0.0532 | median +0.0523 | empirical 95% [+0.0363, +0.0710]

Claim ceiling: true next-state evidence on this dataset/subset; explicitly no website-holdout claim.

### Mind2Web V0.40 — real-data route/composition baseline

- VALID: 176
- HARD: 66
- NOVEL: 149/176 (0.8466)
- HARD NOVEL: 56/66 (0.8485)
- RETRIEVAL: 47/176 (0.267)

### Mind2Web V0.50 — falsification gate

RAW TASKS: 1009
ACTION EXTRACTION: 3843/6766 (0.568)

STRICT RECONSTRUCTION
- PLAN FOUND: 176/176 (1)
- EXACT HUMAN ROUTE: 6/176 (0.0341)
- SAME OPERATIONS (ANY ORDER): 40/176 (0.2273)
- HARD EXACT HUMAN ROUTE: 4/66 (0.0606)
- HARD SAME OPERATIONS: 19/66 (0.2879)
- OPERATION MICRO-F1: 0.7893
- MEAN LCS / HUMAN ROUTE: 0.5178

CAUSALITY
- CAUSALLY LINKED COMPOSITION: 23/176 (0.1307)
- STRICT CAUSAL CHAIN: 4/176 (0.0227)
- HARD CAUSAL COMPOSITION: 15/66 (0.2273)
- GT ROUTES WITH ANY CAUSAL DEPENDENCY: 16/176 (0.0909)

Claim ceiling: falsification-oriented benchmark evidence. Operation-level reconstruction is materially easier than exact human-route reconstruction in this slice; strict causal-composition support is sparse.

Binding rule: positive, negative, blocked, invalid and inconclusive outcomes remain visible. Provider/network/infrastructure failures are never promoted into scientific evidence.
'''


def main() -> None:
    sh("git", "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*", "+refs/tags/*:refs/tags/*", "--force", "--prune")

    refs_raw = sh("git", "for-each-ref", "--format=%(refname)\t%(objectname)", "refs/remotes/origin", "refs/tags")
    refs = []
    for line in refs_raw.splitlines():
        if not line.strip() or line.startswith("refs/remotes/origin/HEAD"):
            continue
        ref, sha = line.split("\t", 1)
        refs.append((ref, sha))

    # Candidate blob inventory across every object reachable from every ref, not only current heads.
    object_lines = sh("git", "rev-list", "--objects", "--all").splitlines()
    path_by_oid: dict[str, set[str]] = defaultdict(set)
    for line in object_lines:
        if " " not in line:
            continue
        oid, path = line.split(" ", 1)
        if candidate(path):
            path_by_oid[oid].add(path)

    # Batch object typing so commit/tree OIDs never get mistaken for blobs.
    proc = subprocess.Popen(["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"], cwd=ROOT, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert proc.stdin and proc.stdout
    for oid in path_by_oid:
        proc.stdin.write(oid + "\n")
    proc.stdin.close()
    object_meta: dict[str, tuple[str, int]] = {}
    for line in proc.stdout:
        parts = line.rstrip().split(" ")
        if len(parts) >= 3:
            object_meta[parts[0]] = (parts[1], int(parts[2]))
    proc.wait()

    blob_paths: dict[str, set[str]] = {}
    for oid, paths in path_by_oid.items():
        typ, _size = object_meta.get(oid, ("", 0))
        if typ == "blob":
            blob_paths[oid] = paths

    # Exact current-head provenance for candidate blobs.
    provenance: dict[str, set[str]] = defaultdict(set)
    for ref, sha in refs:
        tree = sh("git", "ls-tree", "-r", sha, check=False)
        for line in tree.splitlines():
            try:
                meta, path = line.split("\t", 1)
                oid = meta.split()[2]
            except Exception:
                continue
            if oid in blob_paths and candidate(path):
                provenance[oid].add(f"{ref}:{path}")

    runs = all_action_runs()

    durable_run_ids = set()
    tombstone_ids = set()
    for paths in blob_paths.values():
        for p in paths:
            m = re.fullmatch(r"evidence/run-memory/runs/(\d+)\.json", p)
            if m:
                durable_run_ids.add(int(m.group(1)))
            m = re.fullmatch(r"evidence/run-memory/deleted/(\d+)\.json", p)
            if m:
                tombstone_ids.add(int(m.group(1)))

    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    parts: list[str] = []
    parts.append("# SPIDER CODEX ULTIME — COMPLETE PRE-2.0 EVIDENCE ARCHIVE\n")
    parts.append(f"Generated deterministically: {generated}\n")
    parts.append(f"Repository: `{REPO}`\n")
    parts.append("\nPurpose: freeze the complete reachable SPIDER experimental/evidence record before architecture 2.0. This document is an archive, not a claim upgrader and not an architecture proposal.\n")
    parts.append("\nEpistemic invariant: content is reproduced without summarizing the underlying stored result artifacts. Identical Git blobs are deduplicated by SHA while every known path/ref provenance is retained. Contradictions, falsifications, BLOCKED states, invalid measurements and negative results stay visible.\n\n")
    parts.append(historical_seed())

    parts.append("\n## B. Coverage manifest\n\n")
    parts.append(f"- Reachable refs inventoried: **{len(refs)}**\n")
    parts.append(f"- Unique result/evidence text blobs selected across full reachable Git history: **{len(blob_paths)}**\n")
    parts.append(f"- GitHub Actions runs currently accessible through the API: **{len(runs)}**\n")
    parts.append(f"- Durable per-run records found: **{len(durable_run_ids)}**\n")
    parts.append(f"- Deleted-run tombstones found: **{len(tombstone_ids)}**\n")
    actions_only = [r for r in runs if int(r.get("id", 0)) not in durable_run_ids and int(r.get("id", 0)) not in tombstone_ids]
    parts.append(f"- Actions runs without a per-run memory record or tombstone: **{len(actions_only)}** (listed explicitly below; their branch/history result artifacts are still captured when reachable)\n")

    parts.append("\n### B1. Ref / branch heads\n\n| Ref | Head SHA |\n|---|---|\n")
    for ref, sha in sorted(refs):
        parts.append(f"| `{ref}` | `{sha}` |\n")

    parts.append("\n### B2. GitHub Actions run inventory\n\n| Run | Workflow | Event | Branch | Conclusion/status | Created | Head SHA | Coverage |\n|---:|---|---|---|---|---|---|---|\n")
    for r in sorted(runs, key=lambda x: int(x.get("id", 0))):
        rid = int(r.get("id", 0))
        coverage = "RUN_MEMORY" if rid in durable_run_ids else ("TOMBSTONE" if rid in tombstone_ids else "ACTIONS_ONLY")
        name = str(r.get("name", "")).replace("|", "\\|")
        event = str(r.get("event", ""))
        branch = str(r.get("head_branch", "") or "").replace("|", "\\|")
        conclusion = str(r.get("conclusion") or r.get("status") or "")
        created = str(r.get("created_at", ""))
        head_sha = str(r.get("head_sha", ""))
        parts.append(f"| {rid} | {name} | {event} | `{branch}` | {conclusion} | {created} | `{head_sha}` | {coverage} |\n")

    parts.append("\n### B3. Actions-only coverage gaps\n\nThese runs are not silently discarded. They are listed here precisely so architecture 2.0 cannot mistake missing run-memory distillation for absence of activity. Where they wrote result/evidence files to reachable Git history, those files are reproduced verbatim in section C.\n\n")
    for r in actions_only:
        parts.append(f"- Run {r.get('id')} — {r.get('name')} — {r.get('event')} — branch `{r.get('head_branch')}` — {r.get('conclusion') or r.get('status')} — {r.get('html_url')}\n")

    parts.append("\n## C. Verbatim result/evidence corpus from complete reachable Git history\n\n")
    parts.append("Each subsection below is one unique Git blob. Repeated identical copies are not duplicated; all discovered historical paths and current-head ref/path occurrences are shown. The blob body itself is reproduced verbatim.\n\n")

    for i, oid in enumerate(sorted(blob_paths, key=lambda o: (sorted(blob_paths[o])[0], o)), 1):
        raw = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        try:
            text = raw.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            # Result corpus is defined as text. Binary/non-UTF8 candidates are explicitly surfaced rather than silently mangled.
            parts.append(f"### C{i}. Non-UTF8 candidate `{oid}`\n\n")
            parts.append(f"Historical paths: {', '.join(f'`{p}`' for p in sorted(blob_paths[oid]))}\n\n")
            parts.append(f"Size: {len(raw)} bytes. Content not text-decodable; retained in Git by blob SHA and not altered.\n\n")
            continue
        paths = sorted(blob_paths[oid])
        prov = sorted(provenance.get(oid, set()))
        parts.append(f"### C{i}. Blob `{oid}`\n\n")
        parts.append("Historical path(s): " + ", ".join(f"`{p}`" for p in paths) + "\n\n")
        if prov:
            parts.append("Current-head provenance: " + ", ".join(f"`{p}`" for p in prov) + "\n\n")
        else:
            parts.append("Current-head provenance: none; blob survives through reachable Git history.\n\n")
        parts.append(f"Encoding: {encoding}; bytes: {len(raw)}\n\n")
        fence = fence_for(text)
        parts.append(fence + "\n" + text)
        if not text.endswith("\n"):
            parts.append("\n")
        parts.append(fence + "\n\n")

        if sum(len(p.encode("utf-8")) for p in parts) > MAX_BYTES:
            raise RuntimeError("Codex exceeded 90 MiB. Refusing silent truncation; split strategy requires explicit human decision.")

    parts.append("\n## D. Archive reading rules for architecture 2.0\n\n")
    parts.append("1. This Codex is the historical evidence floor, not a product specification.\n")
    parts.append("2. A GitHub workflow success is not automatically a scientific PASS; independent audit/gate semantics remain authoritative.\n")
    parts.append("3. `BLOCKED`, `MEASUREMENT_INVALID`, `INCONCLUSIVE`, negative and falsified results are first-class retained knowledge.\n")
    parts.append("4. Infrastructure/provider failures are operational evidence only.\n")
    parts.append("5. Product architecture 2.0 must be derived from what this evidence says can be made useful to an external agent, not from the historical organizational structure of the lanes.\n")

    data = "".join(parts).encode("utf-8")
    if len(data) > MAX_BYTES:
        raise RuntimeError("Codex exceeded 90 MiB. Refusing silent truncation.")
    OUT.write_bytes(data)
    print(json.dumps({"out": str(OUT), "bytes": len(data), "refs": len(refs), "blobs": len(blob_paths), "actions_runs": len(runs), "run_memory": len(durable_run_ids), "tombstones": len(tombstone_ids), "actions_only": len(actions_only)}, indent=2))


if __name__ == "__main__":
    main()
