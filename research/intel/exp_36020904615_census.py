"""
EXP-INTEL-36020904615 Module A2: primary census + Hard258 census derivation +
deterministic family sampling executed TWICE per census (MV2/MV4).

Primary census: byte-identical pinned manifest SHA
d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (927596 bytes).

Hard258 census: upstream `webarna-verfied-hard.json` (258 tasks, fetched this experiment,
2 genuine GitHub-raw attempts logged) is a task_id subset of the pinned 812 manifest
(all 258 task_ids present; only the `eval` evaluator schema differs from base).  The
Hard258 slice used for measurement is therefore derived BY SELECTION from the pinned
base bytes (SHA d6527566), i.e. a byte-identical hard slice of the durable pin, with the
upstream file recorded as hardness provenance.

Deterministic sampling (frozen MV4), executed exactly twice per census:
    random.Random(35725763380).sample(sorted_families_ge3, 10)
with independent seed reset for S1 and S2, on BOTH the primary census and the Hard258
census.  Both draws are logged per census.

PC-D (Hard258 fixture): a synthetic hard-task manifest fixture is parsed by the identical
census parser and must yield families_ge3 >= 2.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # <repo>/research
EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
RAW = EXP / "artifacts" / "raw"
DERIVED = EXP / "artifacts" / "derived"
RAW.mkdir(parents=True, exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)

EXP_ID = "EXP-INTEL-36020904615"
SEED = 35725763380
BASE_MANIFEST = ROOT / "experiments" / "EXP-INTEL-35725763380" / "artifacts" / "raw" / "webarena-verified.json"
HARD_FILE = RAW / "webarena_verfied_hard.json"
MANIFEST_SHA = "d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30"
NON_PRODUCT_RE = re.compile(r"(checkout|cart|search|account|customer|catalogsearch|wishlist/index|signin|login)", re.I)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def is_product_url(u: str) -> bool:
    if not u:
        return False
    p = u.replace("__SHOPPING__", "").strip("/")
    return p.endswith(".html") and not NON_PRODUCT_RE.search(p)


def census_from(tasks: list, label: str) -> dict:
    """Census statistics for a task list. Families = intent_template_id buckets on the
    shopping site with >=3 tasks (identical rule to prior accepted censuses)."""
    by_site = {}
    for t in tasks:
        by_site[t["sites"][0]] = by_site.get(t["sites"][0], 0) + 1
    shopping = [t for t in tasks if t["sites"][0] == "shopping"]
    by_tpl: dict[int, list] = {}
    for t in shopping:
        by_tpl.setdefault(t["intent_template_id"], []).append(t)
    fam_sizes = {k: len(v) for k, v in by_tpl.items()}
    families_ge3 = sorted(k for k, v in fam_sizes.items() if v >= 3)
    hist: dict[int, int] = {}
    for k in families_ge3:
        hist[fam_sizes[k]] = hist.get(fam_sizes[k], 0) + 1

    product_page_families, family_product_urls, product_tasks = [], {}, 0
    for fid in families_ge3:
        urls = []
        n_prod_tasks = 0
        for t in by_tpl[fid]:
            tus = [u for u in (t.get("start_urls") or []) if is_product_url(u)]
            if tus:
                n_prod_tasks += 1
            for u in tus:
                resolved = "http://localhost:7770" + u.replace("__SHOPPING__", "")
                if resolved not in urls:
                    urls.append(resolved)
        if urls:
            product_page_families.append(fid)
            family_product_urls[str(fid)] = urls
        product_tasks += n_prod_tasks

    # homepage-only start URLs for every families_ge3 family (probe expansion)
    family_start_urls = {}
    for fid in families_ge3:
        for t in by_tpl[fid]:
            su = t.get("start_urls") or []
            if su:
                raw = su[0]
                if raw == "__SHOPPING__":
                    url = "http://localhost:7770/"
                elif raw.startswith("__SHOPPING__/"):
                    url = "http://localhost:7770" + raw[len("__SHOPPING__"):]
                else:
                    url = raw
                family_start_urls.setdefault(str(fid), url)

    all_site_families = {}
    for t in tasks:
        all_site_families.setdefault(t["intent_template_id"], 0)
        all_site_families[t["intent_template_id"]] += 1
    all_site_ge3 = sorted(k for k, v in all_site_families.items() if v >= 3)

    return {
        "census_label": label,
        "total_tasks": len(tasks),
        "first_site_counts": by_site,
        "shopping_tasks": len(shopping),
        "families_ge3_shopping": len(families_ge3),
        "families_ge3_ids": families_ge3,
        "family_size_histogram": {str(k): v for k, v in sorted(hist.items())},
        "families_ge3_all_sites_count": len(all_site_ge3),
        "product_page_families": product_page_families,
        "product_page_tasks": product_tasks,
        "family_product_urls": family_product_urls,
        "family_start_urls": family_start_urls,
    }


def deterministic_sample(families_ge3: list, label: str) -> dict:
    r1 = random.Random(SEED)
    s1 = r1.sample(families_ge3, 10)
    r2 = random.Random(SEED)
    s2 = r2.sample(families_ge3, 10)
    return {
        "census_label": label,
        "seed": SEED,
        "operator": "random.Random(35725763380).sample(sorted_families_ge3, 10)",
        "sorted_families_ge3": families_ge3,
        "S1": s1,
        "S2": s2,
        "S1_equals_S2": s1 == s2,
        "unique_S1_union_S2": sorted(set(s1) | set(s2)),
        "n_unique": len(set(s1) | set(s2)),
    }


def main() -> None:
    base_sha = sha256_file(BASE_MANIFEST)
    assert base_sha == MANIFEST_SHA, f"pinned manifest sha mismatch: {base_sha}"
    base = json.loads(BASE_MANIFEST.read_bytes())

    primary = census_from(base, "primary_webarena_verified_v2_812")
    primary.update({
        "experiment_id": EXP_ID,
        "dataset": "WebArena-Verified v2 (812 tasks)",
        "manifest_sha256": base_sha,
        "manifest_bytes": BASE_MANIFEST.stat().st_size,
        "manifest_path": str(BASE_MANIFEST.relative_to(ROOT.parent)),
        "source_cross_check": "GitHub raw ServiceNow/WebArena-Verified (2 attempts this experiment, byte-identical, "
                              "artifacts/raw/github_cross_source_attempts.json); HF source 401 x2 -> UNAVAILABLE",
        "hf_cross_source_status": "UNAVAILABLE_HF_401",
        "diverse_etld_plus1": None,
        "diverse_etld_plus1_note": "WebGym 292k manifest not acquirable: HF 401 x2 this experiment "
                                   "(hf_webgym_manifest_attempts.json). Explicitly UNAVAILABLE, not zero.",
        "duplication_prevalence": None,
        "threshold_sweep": None,
        "threshold_sweep_note": "Requires WebGym 292k manifest (HF_TOKEN). UNAVAILABLE this experiment.",
    })
    (DERIVED / "webarena_census.json").write_text(json.dumps(primary, indent=1))

    # ---------------- Hard258 ----------------
    hard = json.loads(HARD_FILE.read_bytes())
    hard_sha = sha256_file(HARD_FILE)
    base_by_id = {t["task_id"]: t for t in base}
    hard_ids = [t["task_id"] for t in hard]
    in_base = [i for i in hard_ids if i in base_by_id]
    missing = [i for i in hard_ids if i not in base_by_id]

    diff_fields: dict[str, int] = {}
    for t in hard:
        b = base_by_id.get(t["task_id"])
        if b is None:
            continue
        for k in set(t) | set(b):
            if t.get(k) != b.get(k):
                diff_fields[k] = diff_fields.get(k, 0) + 1

    # Derive the measured Hard258 slice FROM THE PINNED BASE BYTES (byte-identical derivation)
    hard_slice = [base_by_id[i] for i in hard_ids if i in base_by_id]
    slice_bytes = json.dumps(hard_slice, indent=None, separators=(",", ":")).encode()
    hard_census = census_from(hard_slice, "hard258_slice_derived_from_pinned_base")
    hard_census.update({
        "experiment_id": EXP_ID,
        "hard_filter_provenance": {
            "upstream_file": "ServiceNow/WebArena-Verified assets/dataset/webarna-verfied-hard.json (upstream typo preserved)",
            "fetched_this_experiment": True,
            "fetch_attempts": "artifacts/raw/github_cross_source_attempts.json (2 genuine attempts, HTTP 200, timeout 300s configured)",
            "upstream_sha256": hard_sha,
            "upstream_bytes": HARD_FILE.stat().st_size,
            "upstream_task_count": len(hard),
            "task_ids_present_in_pinned_base": len(in_base),
            "task_ids_missing_from_pinned_base": missing,
            "field_differences_vs_base": diff_fields,
            "derivation": "Hard258 slice = pinned base tasks (SHA d6527566...) whose task_id appears in the upstream "
                          "hard file; only the `eval` evaluator schema differs between upstream hard file and base, "
                          "all task-defining fields (sites/start_urls/intent/template) are identical, so the slice is "
                          "a byte-identical hard subset of the durable pin.",
            "difficulty_definition": "upstream `hard` dataset partition (webarna-verfied-hard.json), NOT a locally "
                                     "invented hardness heuristic; documented filter = membership in upstream hard file "
                                     "intersected with the pinned 812 manifest.",
        },
        "hard_slice_sha256_of_canonical_json": hashlib.sha256(slice_bytes).hexdigest(),
        "manifest_sha256_base": base_sha,
        "hf_hard258_status": "UNAVAILABLE_HF_401 (2 genuine attempts logged); GitHub raw used as documented fallback",
    })
    (RAW / "hard258_census.json").write_text(json.dumps(hard_census, indent=1))
    (DERIVED / "hard258_census.json").write_text(json.dumps(hard_census, indent=1))

    # ---------------- deterministic sampling, BOTH censuses, TWICE each ----------------
    s_primary = deterministic_sample(primary["families_ge3_ids"], "primary_webarena_verified_v2_812")
    s_hard = deterministic_sample(hard_census["families_ge3_ids"], "hard258_slice_derived_from_pinned_base")
    for s, cen in ((s_primary, primary), (s_hard, hard_census)):
        s["product_page_families"] = cen["product_page_families"]
        s["sample_product_page_families"] = sorted(set(s["unique_S1_union_S2"]) & set(cen["product_page_families"]))
        s["sample_families_without_product_urls"] = sorted(
            f for f in s["unique_S1_union_S2"] if not cen["family_product_urls"].get(str(f)))
    samples = {
        "experiment_id": EXP_ID,
        "seed": SEED,
        "operator": "random.Random(35725763380).sample(sorted_families_ge3, 10) executed twice per census",
        "primary": s_primary,
        "hard258": s_hard,
        "union_unique_families": sorted(set(s_primary["unique_S1_union_S2"]) | set(s_hard["unique_S1_union_S2"])),
        "union_sample_product_page_families": sorted(
            set(s_primary["sample_product_page_families"]) | set(s_hard["sample_product_page_families"])),
        "canonical_families": [136, 145, 196, 222],
    }
    (DERIVED / "deterministic_family_samples.json").write_text(json.dumps(samples, indent=1))

    # ---------------- PC-D: Hard258 fixture parse ----------------
    fixture = [
        {"sites": ["shopping"], "task_id": 900001, "intent_template_id": 901,
         "start_urls": ["__SHOPPING__/fixture-widget-alpha.html"], "intent": "fixture alpha",
         "eval": [], "intent_template": "fixture", "instantiation_dict": {}, "revision": 2},
        {"sites": ["shopping"], "task_id": 900002, "intent_template_id": 901,
         "start_urls": ["__SHOPPING__/fixture-widget-beta.html"], "intent": "fixture alpha 2",
         "eval": [], "intent_template": "fixture", "instantiation_dict": {}, "revision": 2},
        {"sites": ["shopping"], "task_id": 900003, "intent_template_id": 901,
         "start_urls": ["__SHOPPING__"], "intent": "fixture alpha 3",
         "eval": [], "intent_template": "fixture", "instantiation_dict": {}, "revision": 2},
        {"sites": ["shopping"], "task_id": 900004, "intent_template_id": 902,
         "start_urls": ["__SHOPPING__/fixture-gadget-one.html"], "intent": "fixture beta",
         "eval": [], "intent_template": "fixture", "instantiation_dict": {}, "revision": 2},
        {"sites": ["shopping"], "task_id": 900005, "intent_template_id": 902,
         "start_urls": ["__SHOPPING__/fixture-gadget-two.html"], "intent": "fixture beta 2",
         "eval": [], "intent_template": "fixture", "instantiation_dict": {}, "revision": 2},
        {"sites": ["shopping"], "task_id": 900006, "intent_template_id": 902,
         "start_urls": ["__SHOPPING__"], "intent": "fixture beta 3",
         "eval": [], "intent_template": "fixture", "instantiation_dict": {}, "revision": 2},
    ]
    fixture_census = census_from(fixture, "PC-D_hard258_fixture")
    pc_d = {
        "experiment_id": EXP_ID,
        "control_id": "PC-D",
        "fixture_task_count": len(fixture),
        "families_ge3": fixture_census["families_ge3_shopping"],
        "families_ge3_ids": fixture_census["families_ge3_ids"],
        "product_page_families": fixture_census["product_page_families"],
        "pass": fixture_census["families_ge3_shopping"] >= 2,
        "expected": "families_ge3 >= 2 on fixture data",
    }
    (DERIVED / "pc_d_hard258_fixture.json").write_text(json.dumps(pc_d, indent=1))

    summary = {
        "experiment_id": EXP_ID,
        "primary": {k: primary[k] for k in ("total_tasks", "shopping_tasks", "families_ge3_shopping",
                                            "product_page_families", "product_page_tasks", "manifest_sha256")},
        "hard258": {k: hard_census[k] for k in ("total_tasks", "shopping_tasks", "families_ge3_shopping",
                                                "families_ge3_ids", "product_page_families", "product_page_tasks")},
        "hard258_gates": {
            "total_ge_200": hard_census["total_tasks"] >= 200,
            "families_ge3_ge_10": hard_census["families_ge3_shopping"] >= 10,
            "task_ids_subset_of_base": not missing,
        },
        "samples": {c: {"S1": s["S1"], "S2": s["S2"], "equal": s["S1_equals_S2"],
                        "sample_product_page_families": s["sample_product_page_families"]}
                    for c, s in (("primary", s_primary), ("hard258", s_hard))},
        "union_sample_product_page_families": samples["union_sample_product_page_families"],
        "pc_d": pc_d,
    }
    (DERIVED / "census_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
