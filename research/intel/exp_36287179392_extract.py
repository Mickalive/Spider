#!/usr/bin/env python3
"""EXP-INTEL-36287179392 phase B -- structural extraction and representation cost.

Implements frozen prereg 6.2 (minimal structural representation), 6.3
(baseline representations), 6.4 (minimal serialization), 7.1 (structural
signatures) and 10 (per-observation cost accounting) for every page actually
fetched in the conforming run, plus the frozen positive control of prereg 11
and the non-frozen 4-site power extension used to give the positive control a
permutation null of demonstrated power.

Outputs (under the experiment packet directory):
  raw/extracted_structures.jsonl   one record per page (prereg 14)
  raw/control_structures.json      positive-control synthetic structures
"""
from __future__ import annotations

import gzip
import json
import os
import sys
import traceback
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bs4 import BeautifulSoup  # noqa: E402

from exp_36287179392_pipeline import (  # noqa: E402
    BASE_URL_HOLDER, MIN_PAGES_PER_SITE, SEED_POSITIVE_CONTROL, a11y_tree,
    canonical_key, compact_json, extract_actions, extract_details, extract_forms,
    extract_lists, extract_nav, extract_pagination, extract_search,
    full_dom_serialized, ntok, sha256_bytes, signatures_for_page, slot_canonical_key,
)

EXP_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "experiments", "EXP-INTEL-36287179392",
)
RAW = os.path.join(EXP_DIR, "raw")
BODIES = os.path.join(RAW, "bodies")


def structures_for(html_bytes: bytes, page_url: str) -> dict:
    soup = BeautifulSoup(html_bytes, "html.parser")
    BASE_URL_HOLDER[0] = page_url
    forms = extract_forms(soup, page_url)
    navs = extract_nav(soup, page_url)
    lists = extract_lists(soup, page_url)
    return {
        "forms": forms,
        "navs": navs,
        "lists": lists,
        "searches": extract_search(forms),
        "paginations": extract_pagination(soup, page_url),
        "details": extract_details(soup, page_url),
        "actions": extract_actions(soup, page_url),
    }


def representations(html_bytes: bytes, page_url: str, structures: dict) -> dict:
    """prereg 6.3 / 6.4 / 10: all four representations and their cost."""
    soup = BeautifulSoup(html_bytes, "html.parser")
    BASE_URL_HOLDER[0] = page_url

    raw_text = html_bytes.decode("utf-8", "replace")
    full_dom = full_dom_serialized(soup)
    a11y = a11y_tree(soup)
    a11y_json = compact_json(a11y)
    minimal_json = compact_json(structures)

    return {
        "raw": {
            "bytes": len(html_bytes),
            "tokens": ntok(raw_text),
            "sha256": sha256_bytes(html_bytes),
        },
        "full_dom": {
            "bytes": len(full_dom.encode("utf-8")),
            "tokens": ntok(full_dom),
            "sha256": sha256_bytes(full_dom.encode("utf-8")),
        },
        "a11y": {
            "bytes": len(a11y_json.encode("utf-8")),
            "tokens": ntok(a11y_json),
            "n_nodes": a11y["n"],
        },
        "minimal": {
            "bytes": len(minimal_json.encode("utf-8")),
            "tokens": ntok(minimal_json),
        },
        "minimal_json": minimal_json,
        "a11y_json": a11y_json,
    }


# ---------------------------------------------------------------------------
# Frozen positive control (prereg 11.1) and its power extension
# ---------------------------------------------------------------------------

PC_PAGE_A = """<!doctype html><html><head><title>Store A</title></head><body>
<header><nav><a href="/">Home</a><a href="/item/1">Item 1</a><a href="/item/2">Item 2</a></nav></header>
<main>
<form action="/search" method="get"><input type="text" name="q" placeholder="find"><input type="submit" value="Go"></form>
<ul><li><a href="/item/123">Widget 123</a></li><li><a href="/item/456">Widget 456</a></li><li><a href="/item/789">Widget 789</a></li></ul>
<nav><a href="/item/list?page=1" rel="next">Next</a><a href="/item/list?page=1">1</a><a href="/item/list?page=2" rel="next">2</a></nav>
<button type="submit">Buy</button>
</main></body></html>"""

PC_PAGE_B = """<!doctype html><html><head><title>Store B</title></head><body>
<header><nav><a href="/">Home</a><a href="/item/9">Item 9</a><a href="/item/8">Item 8</a></nav></header>
<main>
<form action="/search" method="get"><input type="text" name="q" placeholder="locate"><input type="submit" value="Go"></form>
<ul><li><a href="/item/321">Gadget 321</a></li><li><a href="/item/654">Gadget 654</a></li><li><a href="/item/987">Gadget 987</a></li></ul>
<nav><a href="/item/list?page=1" rel="next">Next</a><a href="/item/list?page=1">1</a><a href="/item/list?page=2" rel="next">2</a></nav>
<button type="submit">Purchase</button>
</main></body></html>"""

# NOT FROZEN. Added only so the positive-control null has the >=3 groups needed
# for a permutation null to be non-degenerate. Deliberately unrelated structure.
PC_PAGE_C = """<!doctype html><html><head><title>Zoo</title></head><body>
<header><nav><a href="/home">Home</a><a href="/animals/mammals">Mammals</a><a href="/animals/birds">Birds</a></nav></header>
<main><table><tr><td>Sea Otter</td></tr><tr><td>Axolotl</td></tr><tr><td>Pangolin</td></tr></table></main>
</body></html>"""

# NOT FROZEN. Also deliberately unrelated to A/B/C. Nav depth differs from C
# so that the extension's negative groups share no template structure.
PC_PAGE_D = """<!doctype html><html><head><title>Reef</title></head><body>
<header><nav><a href="/portal">Portal</a><a href="/weather/marine/tides">Tides</a><a href="/weather/marine/winds">Winds</a></nav></header>
<main><ol><li><a href="/reports/2026-03-01">March report</a></li><li><a href="/reports/2026-04-01">April report</a></li></ol></main>
</body></html>"""


def build_control_records() -> dict:
    import random
    random.seed(SEED_POSITIVE_CONTROL)
    frozen = {
        "PC-SYNTHETIC-ALIAS": [
            ("PC-SITE-A", "https://pc-a.example/search?q=python", PC_PAGE_A),
            ("PC-SITE-B", "https://pc-b.example/search?q=rust", PC_PAGE_B),
        ],
    }
    power_extension = {
        "PC-SYNTHETIC-ALIAS-4SITE-POWER-EXTENSION": [
            ("PC-SITE-A", "https://pc-a.example/search?q=python", PC_PAGE_A),
            ("PC-SITE-B", "https://pc-b.example/search?q=rust", PC_PAGE_B),
            ("PC-SITE-C", "https://pc-c.example/home", PC_PAGE_C),
            ("PC-SITE-D", "https://pc-d.example/portal", PC_PAGE_D),
        ],
    }
    out = {}
    for cid, pages in list(frozen.items()) + list(power_extension.items()):
        recs = []
        for site_key, url, html in pages:
            raw = html.encode("utf-8")
            st = structures_for(raw, url)
            rep = representations(raw, url, st)
            sigs = signatures_for_page(st)
            recs.append({
                "control_id": cid, "site_key": site_key, "url": url,
                "raw": rep["raw"], "full_dom": rep["full_dom"], "a11y": rep["a11y"],
                "minimal": rep["minimal"], "structures": st,
                "signatures": sigs,
                "signature_keys": [canonical_key(s) for s in sigs],
                "signature_keys_slotted": [k for k in (slot_canonical_key(s) for s in sigs) if k],
            })
        out[cid] = recs
    return out


def main():
    manifest = json.load(open(os.path.join(RAW, "fetch_manifest.json")))
    records = []
    n_struct_fail = 0
    for site_key in sorted(manifest["sites"]):
        info = manifest["sites"][site_key]
        for p in info["pages"]:
            path = os.path.join(BODIES, p["body_sha256"] + ".html.gz")
            if not os.path.exists(path):
                n_struct_fail += 1
                continue
            html_bytes = gzip.open(path, "rb").read()
            if sha256_bytes(html_bytes) != p["body_sha256"]:
                n_struct_fail += 1
                continue
            try:
                st = structures_for(html_bytes, p["url"])
                rep = representations(html_bytes, p["url"], st)
                sigs = signatures_for_page(st)
            except Exception as exc:
                n_struct_fail += 1
                records.append({
                    "site_key": site_key, "url": p["url"], "body_sha256": p["body_sha256"],
                    "extraction_error": f"{type(exc).__name__}: {exc}",
                    "extraction_traceback": traceback.format_exc()[-1200:],
                })
                continue
            records.append({
                "site_key": site_key,
                "site_ordinal": info["ordinal"],
                "category": info["category"],
                "derived_registrable_domain": info.get("derived_registrable_domain"),
                "prereg_label_is_registrable_domain": info.get("prereg_label_is_registrable_domain"),
                "url": p["url"],
                "depth": p["depth"],
                "status": p["status"],
                "body_sha256": p["body_sha256"],
                "http_bytes": p["bytes"],
                "structures": st,
                "signatures": sigs,
                "signature_keys": [canonical_key(s) for s in sigs],
                "signature_keys_slotted": [k for k in (slot_canonical_key(s) for s in sigs) if k],
                "raw": rep["raw"],
                "full_dom": rep["full_dom"],
                "a11y": rep["a11y"],
                "minimal": rep["minimal"],
                "minimal_json": rep["minimal_json"],
                "a11y_json": rep["a11y_json"],
                "extraction_error": None,
            })

    with open(os.path.join(RAW, "extracted_structures.jsonl"), "w") as fh:
        for r in sorted(records, key=lambda x: (str(x["site_key"]), str(x["url"]))):
            fh.write(json.dumps(r) + "\n")

    controls = build_control_records()
    with open(os.path.join(RAW, "control_structures.json"), "w") as fh:
        json.dump(controls, fh, indent=1)

    per_site = {}
    for r in records:
        if r.get("extraction_error"):
            continue
        per_site.setdefault(r["site_key"], []).append(r)
    print(json.dumps({
        "n_page_records": len(records),
        "n_extraction_failures": n_struct_fail,
        "n_sites": len(per_site),
        "n_sites_ge_min_pages": sum(1 for v in per_site.values() if len(v) >= MIN_PAGES_PER_SITE),
        "total_signatures": sum(len(v.get("signature_keys", [])) for v in records if not v.get("extraction_error")),
        "total_signatures_slotted": sum(len(v.get("signature_keys_slotted", [])) for v in records if not v.get("extraction_error")),
        "mean_tokens_raw": round(sum(v["raw"]["tokens"] for v in records if not v.get("extraction_error")) / max(1, len(records) - n_struct_fail), 1),
        "mean_tokens_minimal": round(sum(v["minimal"]["tokens"] for v in records if not v.get("extraction_error")) / max(1, len(records) - n_struct_fail), 1),
        "control_ids": sorted(controls),
    }, indent=1))


if __name__ == "__main__":
    main()
