#!/usr/bin/env python3
"""EXP-PHYSICS-35209110569 frozen-design analysis (EXECUTE stage).

Frozen leakage definition (prereg section 8):
  is_leakage = normalize(action_target) == normalize(state_after_url)
  normalize: strip fragment, strip trailing slash, unquote percent-encoding.

Frozen metrics (prereg section 6): leakage_rate (<40% viability),
unique_titles (>=2), achievable_NL = 500*(1-leakage) (>=50), raw>=100.
Secondary: per-type leakage, title entropy, URL entropy, action distribution.
"""
import json
import math
import sys
import urllib.parse
from collections import Counter

EXP = "research/experiments/EXP-PHYSICS-35209110569/"


def normalize_url(url):
    if not url:
        return None
    url = url.split("#")[0]
    url = url.rstrip("/")
    url = urllib.parse.unquote(url)
    return url


def is_leakage(target, after_url):
    if target is None or after_url is None:
        return False
    return normalize_url(target) == normalize_url(after_url)


def entropy(counter):
    n = sum(counter.values())
    if n == 0:
        return 0.0
    h = 0.0
    for c in counter.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def load_site(site):
    """Combine base + repair files. Wikipedia session-0 discovery failures
    (raw_wikipedia.json session 0) are superseded by raw_wikipedia_s0fix.json."""
    if site == "wikipedia":
        base = json.load(open(EXP + "raw_wikipedia.json"))
        base = [r for r in base if not (r.get("session") == 0)]
        fix = json.load(open(EXP + "raw_wikipedia_s0fix.json"))
        return base + fix
    recs = json.load(open(EXP + f"raw_{site}.json"))
    try:
        recs = recs + json.load(open(EXP + f"raw_{site}_topup.json"))
    except FileNotFoundError:
        pass
    return recs


def summarize(valid):
    n_raw = len(valid)
    n_leak = sum(1 for r in valid if is_leakage(r.get("action_target"), r.get("url_after")))
    leak_rate = n_leak / n_raw if n_raw else None
    titles = [r.get("title_after") or "" for r in valid]
    uniq_titles = sorted(set(titles))
    urls = [normalize_url(r.get("url_after")) for r in valid]
    uniq_urls = sorted(set(urls))
    sessions = sorted(set(r.get("session") for r in valid))
    prims = Counter(r.get("action_primitive") for r in valid)
    per_type = {}
    for prim in sorted(prims):
        sub = [r for r in valid if r.get("action_primitive") == prim]
        l = sum(1 for r in sub if is_leakage(r.get("action_target"), r.get("url_after")))
        per_type[prim] = {"n": len(sub), "n_leakage": l,
                          "leakage_rate": l / len(sub) if sub else None}
    return {
        "n_raw": n_raw,
        "n_sessions": len(sessions),
        "n_leakage": n_leak,
        "leakage_rate": leak_rate,
        "unique_titles": len(uniq_titles),
        "title_list": uniq_titles,
        "title_entropy_bits": entropy(Counter(titles)),
        "unique_urls_norm": len(uniq_urls),
        "url_entropy_bits": entropy(Counter(urls)),
        "achievable_NL_at_500": 500 * (1 - leak_rate) if leak_rate is not None else None,
        "action_distribution": dict(prims),
        "per_type_leakage": per_type,
        "n_transition_errors": sum(1 for r in valid if r.get("error")),
    }


def main():
    files = {
        "vanillajs": EXP + "raw_vanillajs.json",
        "react": EXP + "raw_react.json",
        "vue": EXP + "raw_vue.json",
        "angular": EXP + "raw_angular.json",
        "svelte": EXP + "raw_svelte.json",
        "wikipedia": EXP + "raw_wikipedia.json",
    }
    per_site = {}
    all_recs = []
    for site in files:
        recs = load_site(site)
        valid = [r for r in recs if r.get("url_after") and r.get("action_primitive")]
        ok = [r for r in valid if not r.get("error")]
        s_all = summarize(valid)
        s_ok = summarize(ok)
        s_all["n_valid_no_error"] = len(ok)
        s_all["valid_only"] = s_ok
        per_site[site] = s_all
        all_recs.extend(ok)
        print(f"{site}: raw={s_all['n_raw']} sess={s_all['n_sessions']} "
              f"leak_all={s_all['leakage_rate']:.4f} leak_valid={s_ok['leakage_rate']:.4f} "
              f"titles={s_all['unique_titles']} urls={s_all['unique_urls_norm']} "
              f"NL500_valid={s_ok['achievable_NL_at_500']:.1f} errors={s_all['n_transition_errors']}",
              flush=True)
    # frequency baseline: global action distribution
    freq = Counter(r.get("action_primitive") for r in all_recs
                   if r.get("site") != "wikipedia")
    nspa = sum(freq.values())
    print("SPA action marginal:", {k: v / nspa for k, v in freq.items()}, flush=True)
    with open(EXP + "analysis_results.json", "w") as f:
        json.dump({"per_site": per_site,
                   "spa_action_marginal": {k: v / nspa for k, v in freq.items()},
                   "leakage_definition": "normalize(action_target)==normalize(url_after); "
                   "normalize=strip-fragment,rstrip-slash,unquote"}, f, indent=1)
    print("wrote analysis_results.json", flush=True)


if __name__ == "__main__":
    main()
