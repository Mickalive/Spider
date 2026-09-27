"""Repeat-screen stability pass for EXP-FRONTIER-36306528608.

The primary screen pass showed per-site object counts that depend on live Web dynamics
(for example en.wikipedia.org/wiki/Special:Random resolves to a different random article
on every visit, and gitlab.com 302-redirects to about.gitlab.com). A single pass therefore
cannot distinguish "this site has N action-gating objects" from "this visit happened to
land on N of them".

This pass re-screens the object-yielding sites a second time, live, and writes both passes
to raw/repeat_screen.jsonl so the run-to-run variance is a recorded quantity rather than an
anecdote. No criterion, threshold or classification is modified. Read-only GET only.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import screen_36306528608 as S  # noqa: E402
from harness_36306528608 import EXPERIMENT_ID, RAW_DIR, JsonlWriter, ResponseCache  # noqa: E402

REPEAT_SITES = [
    "https://en.wikipedia.org",
    "https://gitlab.com",
    "https://bitbucket.org",
    "https://docs.python.org",
    "https://reqres.in",
    "https://github.com",
]


def main() -> int:
    os.makedirs(RAW_DIR, exist_ok=True)
    pages_w = JsonlWriter(os.path.join(RAW_DIR, "pages_pass2.jsonl"))
    http_w = JsonlWriter(os.path.join(RAW_DIR, "http_pass2.jsonl"))
    rep_w = JsonlWriter(os.path.join(RAW_DIR, "repeat_screen.jsonl"))
    cache = ResponseCache()

    for i, url in enumerate(REPEAT_SITES):
        # Fresh cache_key_prefix => every request is a live re-fetch, never a cache hit.
        try:
            rec = S.screen_site(url, pages_w, http_w, cache, f"pass2_{i:02d}")
        except Exception as exc:
            rep_w.write({"experiment_id": EXPERIMENT_ID, "url": url, "pass": 2,
                         "error": f"{type(exc).__name__}: {exc}", "objects_detected": None})
            continue
        rep_w.write({
            "experiment_id": EXPERIMENT_ID,
            "pass": 2, "url": url,
            "criteria_pass": {c: rec[c]["pass"] for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7")},
            "qualifies": rec["qualifies"],
            "objects_detected": len(rec["_objects"]),
            "by_type": rec["C2"]["by_type"],
            "c5_hash_differs_count": rec["C5"]["hash_differs_count"],
            "c5_probes": rec["C5"]["probes"],
            "pages_fetched": rec["pages_fetched"],
            "http_requests": rec["http_requests"],
            "page_urls": rec.get("page_urls", []),
        })
        print(f"[pass2] {url}: objects={len(rec['_objects'])} qualifies={rec['qualifies']} "
              f"by_type={rec['C2']['by_type']} c5={rec['C5']['hash_differs_count']}/{rec['C5']['probes']}",
              flush=True)

    cache.flush_keys()
    cache.flush_index()
    for w in (pages_w, http_w, rep_w):
        w.close()
    print("[pass2] done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
