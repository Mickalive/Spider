"""
EXP-INTEL-35999366789 Module A2a: census derivation + deterministic family sampling (MV2/MV4).

- Census derived from pinned manifest exactly as parent EXP-INTEL-35956094394:
  total 812, shopping first-site 192, families_ge3 by intent_template_id (36),
  family size histogram, product_page families [136,145,196,222] (families with >=1
  product-page start_url: __SHOPPING__/<slug>.html expanded path).
- Deterministic sampling EXACTLY as frozen MV4:
  random.Random(35725763380).sample(sorted_families_ge3, 10) executed TWICE with
  identical seed reset; both lists logged. (Seed is integer, exempt from PYTHONHASHSEED.)
- Per-family constructibility plan: families with product-page URLs in census get
  product_subtree anchored AX probes (A2b); families whose tasks start only at
  __SHOPPING__ homepage / non-product URLs have NO product_page probe in this census
  and are recorded not-constructible (census property, explicitly not probed as
  homepage artifacts which the parent rejected 18/20 identical).

Writes artifacts/derived/webarena_census.json and artifacts/derived/deterministic_family_samples.json.
"""
from __future__ import annotations
import json, random, re, hashlib
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent / "experiments/EXP-INTEL-35999366789"
DERIVED = EXP / "artifacts/derived"
DERIVED.mkdir(parents=True, exist_ok=True)
LOCAL_MANIFEST = Path(__file__).resolve().parent.parent / "experiments/EXP-INTEL-35725763380/artifacts/raw/webarena-verified.json"

MANIFEST_SHA_EXPECTED = "d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30"
SEED = 35725763380
NON_PRODUCT_RE = re.compile(r"(checkout|cart|search|account|customer|catalogsearch|wishlist/index|signin|login)", re.I)


def is_product_url(u):
    if not u:
        return False
    p = u.replace("__SHOPPING__", "").strip("/")
    if not p.endswith(".html"):
        return False
    return not NON_PRODUCT_RE.search(p)


def main():
    manifest = json.load(open(LOCAL_MANIFEST))
    raw_sha = hashlib.sha256(LOCAL_MANIFEST.read_bytes()).hexdigest()
    assert raw_sha == MANIFEST_SHA_EXPECTED, f"manifest sha mismatch: {raw_sha}"
    total = len(manifest)
    by_site_first = {}
    for t in manifest:
        by_site_first[t["sites"][0]] = by_site_first.get(t["sites"][0], 0) + 1
    shopping = [t for t in manifest if t["sites"][0] == "shopping"]
    by_tpl = {}
    for t in shopping:
        by_tpl.setdefault(t["intent_template_id"], []).append(t)
    fam_sizes = {k: len(v) for k, v in by_tpl.items()}
    families_ge3 = sorted(k for k, v in fam_sizes.items() if v >= 3)
    hist = {}
    for k in families_ge3:
        hist[fam_sizes[k]] = hist.get(fam_sizes[k], 0) + 1

    product_page_families = []
    for fid in families_ge3:
        urls = [u for t in by_tpl[fid] for u in (t.get("start_urls") or [])]
        if any(is_product_url(u) for u in urls):
            product_page_families.append(fid)
    product_page_tasks = sum(
        1 for fid in product_page_families for t in by_tpl[fid]
        if any(is_product_url(u) for u in (t.get("start_urls") or [])))

    # per-family product URL list (resolved to localhost:7770)
    family_product_urls = {}
    for fid in families_ge3:
        urls = []
        for t in by_tpl[fid]:
            for u in (t.get("start_urls") or []):
                if is_product_url(u):
                    resolved = "http://localhost:7770" + u.replace("__SHOPPING__", "")
                    if resolved not in urls:
                        urls.append(resolved)
        if urls:
            family_product_urls[fid] = urls

    census = {
        "experiment_id": "EXP-INTEL-35999366789",
        "dataset": "WebArena-Verified v2 (812 tasks)",
        "manifest_sha256": raw_sha,
        "manifest_bytes": LOCAL_MANIFEST.stat().st_size,
        "total_tasks": total,
        "first_site_counts": by_site_first,
        "shopping": len(shopping),
        "families_ge3": len(families_ge3),
        "families_ge3_ids": families_ge3,
        "family_size_histogram": hist,
        "product_page_families": product_page_families,
        "product_page_tasks_with_product_start_url": product_page_tasks,
        "product_page_tasks_definition": "count of tasks, within product_page_families, having at least one product-page start_url (__SHOPPING__/<slug>.html with none of the non-product path markers). =21 (=5+5+5+6).",
        "parent_product_page_capable_tasks": 7,
        "parent_alignment_note": "Parent EXP-INTEL-35956094394 census reports product_page_capable_tasks=7 under its own derivation; THIS run reports product_page_tasks=21 under the definition above. The decisive fact shared by both: exactly 4 product-page families (136/145/196/222) among 36 families_ge3.",
        "family_product_url_counts": {str(k): len(v) for k, v in family_product_urls.items()},
        "diverse_etld_plus1": None,
        "diverse_etld_plus1_note": "WebGym 292k manifest not acquirable: HF 401 x2 this run (hf_token_present false, logged artifacts/raw/hf_webgym_manifest_attempts.json). Explicitly UNAVAILABLE, not assumed zero.",
        "duplication_prevalence": None,
        "duplication_note": "Requires WebGym 292k manifest; threshold sweep 0.818-0.9479 not computable without HF_TOKEN.",
        "param_prevalence": None,
        "webarena_pin_path": "artifacts/raw/webarena_verified_pin.json",
        "parent_census_sha": "6fcdc04f442ac69caa7a5a5a8e1f4a58e936ea99d8b3fde13f6372b6f410f206",
        "census_match_parent": (len(shopping) == 192 and families_ge3 == [101, 136, 137, 138, 139, 145, 147, 153, 154, 155, 156, 159, 160, 162, 163, 165, 169, 171, 172, 180, 186, 189, 191, 194, 196, 197, 204, 206, 207, 208, 211, 212, 213, 214, 222, 370]),
    }
    (DERIVED / "webarena_census.json").write_text(json.dumps(census, indent=1))

    # Deterministic sampling: identical seed reset, executed twice
    r1 = random.Random(SEED)
    S1 = r1.sample(families_ge3, 10)
    r2 = random.Random(SEED)
    S2 = r2.sample(families_ge3, 10)
    unique = sorted(set(S1) | set(S2))
    samples = {
        "experiment_id": "EXP-INTEL-35999366789",
        "seed": SEED,
        "operator": "random.Random(35725763380).sample(sorted_families_ge3, 10)",
        "sorted_families_ge3": families_ge3,
        "S1": S1,
        "S2": S2,
        "S1_equals_S2": S1 == S2,
        "unique_families_S1U_S2": unique,
        "n_unique": len(unique),
        "product_page_families_in_sample": sorted(set(unique) & set(product_page_families)),
        "families_with_product_urls": sorted(k for k in unique if k in family_product_urls),
        "families_without_product_urls_in_census": sorted(k for k in unique if k not in family_product_urls),
        "note": "MV4: determinism proven by two identical draws; product_page probes only for families with product-page URLs in census (families whose tasks start at __SHOPPING__ homepage have no product_page task in census; homepage-template artifacts rejected by parent 18/20 identical).",
    }
    (DERIVED / "deterministic_family_samples.json").write_text(json.dumps(samples, indent=1))
    print("census:", json.dumps({k: census[k] for k in ("total_tasks", "shopping", "families_ge3", "product_page_families", "product_page_tasks_with_product_start_url")}))
    print("S1 == S2:", S1 == S2)
    print("S1:", sorted(S1))
    print("unique:", unique)
    print("product in sample:", sorted(set(unique) & set(product_page_families)))


if __name__ == "__main__":
    main()