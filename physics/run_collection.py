"""Run each site walk in a hard-capped subprocess; hangs cost one site, not all."""
import json, os, subprocess, sys, time

import os
SITES = os.environ.get("SITES", "books,quotes,internet,wikipedia,hackernews,openlibrary").split(",")
RESUME = os.environ.get("RESUME") == "1"
OUTDIR = "/tmp/opencode/spider_data"
OUT = os.path.join(OUTDIR, "wp003_transitions.jsonl")
LOG = "/tmp/opencode/spider_data/collector_sites.log"
PER_SITE_CAP_S = 420
SEED = 20260823

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if not RESUME:
    for s_ in SITES:
        p_ = os.path.join(OUTDIR, f"wp003_{s_}.jsonl")
        open(p_, "w").close()
status = {}
for site in SITES:
    t0 = time.time()
    try:
        r = subprocess.run(
            [sys.executable, "physics/collector.py", "--site", site,
             "--seed", str(SEED)],
            timeout=PER_SITE_CAP_S, capture_output=True, text=True)
        ok = r.returncode == 0
        tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    except subprocess.TimeoutExpired as e:
        ok = False
        tail = [f"HARD TIMEOUT after {PER_SITE_CAP_S}s"]
    status[site] = {"ok": ok, "wall_s": round(time.time() - t0), "tail": tail}
    print(site, status[site], flush=True)

from collections import Counter
c = Counter()
with open(OUT, "w") as merged:
    for s_ in SITES:
        p_ = os.path.join(OUTDIR, f"wp003_{s_}.jsonl")
        try:
            for line in open(p_):
                line = line.strip()
                if line:
                    merged.write(line + "\n")
                    c[json.loads(line)["site"]] += 1
        except FileNotFoundError:
            pass
status["_counts"] = dict(c)
with open(LOG.replace(".log", "_status.json"), "w") as f:
    json.dump(status, f, indent=1)
print("COUNTS", dict(c))
