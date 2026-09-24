"""
EXP-INTEL-36020904615 Module A2b: product-family constructibility probes (MV3/MV4).

- Browser: Playwright 1.63.0 / Chromium 153, viewport exactly 1280x720.
- AX: CDP Accessibility.getFullAXTree via cdp session (snapshot fallback would be
  MEASUREMENT_INVALID; not used anywhere in this script).
- SHA: outerHTML -> body regex DOTALL + 9 base dynamic-token regexes + expanded
  {form_key,uenc,store,session,timestamp,nonce,fotorama\\d{6,}} stripping, applied BEFORE
  SHA256, recomputed AFTER page.content()+AX, in TWO independent implementations
  (Python grammar module AND an in-page page.evaluate pass) whose digests are compared.
  Grammar file hash recomputed live per capture.
- Anchoring (node_count>1): anchored Runtime.evaluate getBoundingClientRect scan of
  heading/price/add-to-cart/main/contentinfo (Chromium 153 AXNode has no boundingBox).
- SHA stability both directions: reload re-capture identical; visible textContent
  mutation changes the digest.
- Probe set: canonical product families 136/145/196/222 (3 census-derived product
  start_urls each = 12 captures) PLUS every family drawn by the frozen deterministic
  samples on BOTH censuses: families with a product-page start_url are probed on that
  product page; families whose tasks only start at the __SHOPPING__ homepage are probed
  on the expanded start URL for raw evidence and are classified by the frozen rule
  (constructible requires at least one product_page probe).
- PC-A: synthetic product fixture served on localhost:8899, x3 captures.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # <repo>/research
sys.path.insert(0, str(ROOT / "intel"))
import grammar_fulltree_358885 as g  # noqa: E402

EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
RAW = EXP / "artifacts" / "raw"
DERIVED = EXP / "artifacts" / "derived"
RAW.mkdir(parents=True, exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)
EXP_ID = "EXP-INTEL-36020904615"
VIEWPORT = {"width": 1280, "height": 720}
CANONICAL = [136, 145, 196, 222]

ANCHOR_JS = """() => {
    const find = (sels) => { for (const s of sels) { const e = document.querySelector(s); if (e) return e; } return null; };
    const subtree = (el) => el ? (el.querySelectorAll('*').length + 1) : 0;
    const heading = find(['h1', '.page-title', '.product-name']);
    const price = find(['.price-box', '.product-info-price .price', '.price', '.product-info-price']);
    const add = find(['#product-addtocart-button', '.tocart', 'button[title*=Cart]', '.add-to-cart button']);
    const main = find(['main', '.main', '#maincontent']);
    const cinfo = find(['footer', '.contentinfo', '.page-footer']);
    const r = {};
    for (const [k, el] of Object.entries({heading, price, add_to_cart: add, main, contentinfo: cinfo})) {
        r[k] = {present: !!el, node_count_subtree: subtree(el)};
        if (el) { const b = el.getBoundingClientRect();
                  r[k].bbox = {x:b.x,y:b.y,w:b.width,h:b.height};
                  const cs = getComputedStyle(el); r[k].cs = {display:cs.display, visibility:cs.visibility}; }
    }
    return r;
}"""

# In-page stripping implementation (independent of the Python grammar module).
STRIP_JS = r"""async () => {
    const html = document.documentElement.outerHTML;
    const bodyRe = /<body[^>]*>[\s\S]*?<\/body>/;
    const m = bodyRe.exec(html);
    let s = m ? m[0] : html;
    const pats = ["csrf[_-]?token","session[_-]?id","_token","timestamp","nonce","csrf value","sessionId",
                  "\\b\\d{13}\\b","\\b[a-f0-9]{32,}\\b"];
    for (const p of pats) s = s.replace(new RegExp(p,"gi"), "__STRIPPED__");
    const attr = ["\\b(?:form_key|uenc|store|session|timestamp|nonce)\\s*=\\s*\"[^\"]*\"",
                  "\\b(?:form_key|uenc|store|session|timestamp|nonce)\\s*=\\s*'[^']*'",
                  "\\bfotorama\\d{6,}\\b"];
    for (const p of attr) s = s.replace(new RegExp(p,"gi"), "__STRIPPED__");
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2,'0')).join('');
}"""

MUTATION_SELECTORS = [".price", "h1 span", ".product-name", "h1", ".product-info-price .price"]


def sha_of(content: str) -> str:
    return hashlib.sha256(g.strip_dynamic_tokens(content).encode("utf-8")).hexdigest()


async def full_capture(page, cdp, label) -> dict:
    ax = await cdp.send("Accessibility.getFullAXTree")
    nodes = ax.get("nodes", [])
    content = await page.content()
    sha_py = sha_of(content)
    try:
        sha_js = await page.evaluate(STRIP_JS)
    except Exception as e:  # noqa: BLE001
        sha_js = f"ERROR:{type(e).__name__}"
    return {
        "label": label,
        "ax_nodes": len(nodes),
        "dom_bytes": len(content),
        "title": await page.title(),
        "sha256_stripped_python": sha_py,
        "sha256_stripped_inpage_js": sha_js,
        "dual_impl_digest_match": sha_py == sha_js,
        "grammar_hash_live": g.recompute_grammar_hash(),
        "ax_mode": "CDP Accessibility.getFullAXTree",
        "viewport": "1280x720",
        "bbox_fields_in_ax": sum(1 for n in nodes if n.get("boundingBox")),
    }


async def capture_url(page, cdp, label, url, family, census_label, is_product_page) -> dict:
    rec = {"url": url, "family": family, "census": census_label,
           "is_product_page_probe": is_product_page,
           "viewport": "1280x720", "ax_mode": "CDP Accessibility.getFullAXTree"}
    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(2000)
    c1 = await full_capture(page, cdp, "before")
    await page.reload(wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(2000)
    c2 = await full_capture(page, cdp, "after")
    mutated = await page.evaluate(
        """(selectors) => {
            for (const s of selectors) {
                const el = document.querySelector(s);
                if (el) { el.textContent = el.textContent + ' [MUTATED-36020904615]'; return {selector: s, found: true}; }
            }
            return {selector: null, found: false};
        }""", MUTATION_SELECTORS)
    await page.wait_for_timeout(800)
    c3 = await full_capture(page, cdp, "mutated")
    geom = await page.evaluate(ANCHOR_JS)
    rec.update({
        "capture_before": c1, "capture_after": c2, "capture_mutated": c3,
        "mutation": mutated, "anchored": geom,
        "sha_stability_identical": c1["sha256_stripped_python"] == c2["sha256_stripped_python"],
        "sha_mutation_changed": c1["sha256_stripped_python"] != c3["sha256_stripped_python"],
    })
    return rec


async def synthetic_fixture(page, cdp, url) -> dict:
    rec = {"url": url, "family": "PC-A-SYNTHETIC-FIXTURE", "viewport": "1280x720",
           "ax_mode": "CDP Accessibility.getFullAXTree", "is_product_page_probe": True}
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(800)
    c1 = await full_capture(page, cdp, "before")
    await page.reload(wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(800)
    c2 = await full_capture(page, cdp, "after")
    await page.evaluate("""() => { const p = document.querySelector('.price'); p.textContent = p.textContent.replace('$1.00','$2.00'); }""")
    await page.wait_for_timeout(500)
    c3 = await full_capture(page, cdp, "mutated")
    geom = await page.evaluate(ANCHOR_JS)
    rec.update({"capture_before": c1, "capture_after": c2, "capture_mutated": c3, "anchored": geom,
                "sha_stability_identical": c1["sha256_stripped_python"] == c2["sha256_stripped_python"],
                "sha_mutation_changed": c1["sha256_stripped_python"] != c3["sha256_stripped_python"]})
    return rec


def anchoring_ok(anchored: dict) -> tuple[bool, dict]:
    counts = {k: v["node_count_subtree"] for k, v in anchored.items()}
    present = {k: v["present"] for k, v in anchored.items()}
    all_gt1 = all(v["present"] and v["node_count_subtree"] > 1 for v in anchored.values())
    return all_gt1, {"node_counts": counts, "present": present}


async def main() -> None:
    primary = json.loads((DERIVED / "webarena_census.json").read_text())
    hard = json.loads((DERIVED / "hard258_census.json").read_text())
    samples = json.loads((DERIVED / "deterministic_family_samples.json").read_text())

    # probe plan: family -> list of (url, census_label, is_product_page)
    plan: dict[int, list] = {}
    for fid in CANONICAL:
        urls = primary["family_product_urls"].get(str(fid), [])[:3]
        plan.setdefault(fid, [])
        for u in urls:
            plan[fid].append((u, "primary_webarena_verified_v2_812", True))
    # sampled families on each census
    for census_label, cen, key in (("primary_webarena_verified_v2_812", primary, "primary"),
                                   ("hard258_slice_derived_from_pinned_base", hard, "hard258")):
        smp = samples[key]["unique_S1_union_S2"]
        for fid in smp:
            plan.setdefault(fid, [])
            prod = cen["family_product_urls"].get(str(fid), [])
            if prod:
                for u in prod[:3]:
                    if (u, census_label, True) not in plan[fid]:
                        plan[fid].append((u, census_label, True))
            else:
                start = cen["family_start_urls"].get(str(fid))
                if start and (start, census_label, False) not in plan[fid]:
                    plan[fid].append((start, census_label, False))

    records = []
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport=VIEWPORT)
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        for fid in sorted(plan):
            for url, clabel, is_prod in plan[fid]:
                try:
                    rec = await capture_url(page, cdp, f"fam{fid}", url, fid, clabel, is_prod)
                    records.append(rec)
                    print(f"fam{fid} prod={is_prod} ax={rec['capture_before']['ax_nodes']} "
                          f"dom={rec['capture_before']['dom_bytes']} stable={rec['sha_stability_identical']} "
                          f"mut={rec['sha_mutation_changed']} dual={rec['capture_before']['dual_impl_digest_match']} {url[:70]}")
                except Exception as e:  # noqa: BLE001
                    records.append({"url": url, "family": fid, "census": clabel,
                                    "is_product_page_probe": is_prod, "error": f"{type(e).__name__}: {e}"})
                    print(f"fam{fid} ERROR {type(e).__name__}: {e}")
        await browser.close()

    # PC-A synthetic fixture x3
    FIXTURE_HTML = """<!doctype html><html><head><title>PC-A Product</title></head>
<body><header class="site-header"><h1>Acme Widget 3000</h1></header>
<main id="maincontent"><div class="product-info"><div class="price-box"><span class="price">$1.00</span></div>
<button id="product-addtocart-button">Add to Cart</button></div></main>
<footer class="contentinfo">Copyright Acme 2026</footer></body></html>"""
    try:
        from flask import Flask
        import threading
        app = Flask("pc_a_fixture_36020904615")
        app.add_url_rule("/", "idx", lambda: FIXTURE_HTML)
        t = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=8899, debug=False, use_reloader=False), daemon=True)
        t.start()
        time.sleep(1.5)
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            ctx = await browser.new_context(viewport=VIEWPORT)
            page = await ctx.new_page()
            cdp = await ctx.new_cdp_session(page)
            for i in range(3):
                rec = await synthetic_fixture(page, cdp, "http://127.0.0.1:8899/")
                rec["repeat"] = i + 1
                records.append(rec)
                print(f"PC-A repeat {i+1}: ax={rec['capture_before']['ax_nodes']} dom={rec['capture_before']['dom_bytes']} "
                      f"stable={rec['sha_stability_identical']} mut={rec['sha_mutation_changed']}")
            await browser.close()
    except Exception as e:  # noqa: BLE001
        records.append({"family": "PC-A-SYNTHETIC-FIXTURE", "error": f"{type(e).__name__}: {e}"})
        print("PC-A ERROR", e)

    with (RAW / "ax_captures.jsonl").open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print("wrote", RAW / "ax_captures.jsonl", "records:", len(records))

    # ---------- family anchoring derivation ----------
    anchoring: dict[str, dict] = {}
    for fid in sorted(plan):
        fam_recs = [r for r in records
                    if r.get("family") == fid and "error" not in r and r.get("is_product_page_probe")]
        home_recs = [r for r in records
                     if r.get("family") == fid and "error" not in r and not r.get("is_product_page_probe")]
        per_url, fam_ok = [], False
        for r in fam_recs:
            ok, detail = anchoring_ok(r["anchored"])
            row = {"url": r["url"], "census": r["census"], "anchoring_all_categories_gt1": ok,
                   **detail, "sha_stability_identical": r["sha_stability_identical"],
                   "sha_mutation_changed": r["sha_mutation_changed"],
                   "ax_nodes": r["capture_before"]["ax_nodes"],
                   "dom_bytes": r["capture_before"]["dom_bytes"]}
            per_url.append(row)
            if ok and r["sha_stability_identical"] and r["sha_mutation_changed"]:
                fam_ok = True
        per_home = []
        for r in home_recs:
            ok, detail = anchoring_ok(r["anchored"])
            per_home.append({"url": r["url"], "census": r["census"], "is_product_page_probe": False,
                             "anchoring_all_categories_gt1": ok, **detail,
                             "sha_stability_identical": r["sha_stability_identical"],
                             "sha_mutation_changed": r["sha_mutation_changed"],
                             "ax_nodes": r["capture_before"]["ax_nodes"],
                             "dom_bytes": r["capture_before"]["dom_bytes"]})
        entry = {
            "family": fid,
            "product_urls_probed": [r["url"] for r in fam_recs],
            "n_product_probes": len(fam_recs),
            "home_urls_probed": [r["url"] for r in home_recs],
            "n_home_probes": len(home_recs),
            "per_product_url": per_url,
            "per_home_url": per_home,
            "family_constructible": fam_ok,
            "classification_rule": "frozen MV4: constructible requires >=1 product_page probe with "
                                   "heading/price/add-to-cart/main/contentinfo node_count>1 AND SHA stability "
                                   "both directions (identical on reload, changed on visible mutation)",
        }
        if not fam_recs:
            entry["reason"] = ("No product-page start_url in this census for this family; only the expanded "
                               "__SHOPPING__ homepage start URL exists. Homepage probe recorded as raw evidence "
                               "and is NOT counted (frozen MV4 requires a product_page probe; parent audit "
                               "rejected homepage/template captures as product-page proxies, 18/20 identical).")
        anchoring[f"fam{fid}"] = entry
    (DERIVED / "family_anchoring.json").write_text(json.dumps(anchoring, indent=1))

    # ---------- analysis ----------
    web_prod = [r for r in records if isinstance(r.get("family"), int) and "error" not in r
                and r.get("is_product_page_probe")]
    web_home = [r for r in records if isinstance(r.get("family"), int) and "error" not in r
                and not r.get("is_product_page_probe")]
    pca = [r for r in records if r.get("family") == "PC-A-SYNTHETIC-FIXTURE" and "error" not in r]
    canon = [r for r in web_prod if r["family"] in CANONICAL]

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None

    constructible = sorted(fid for fid, v in anchoring.items() if v["family_constructible"])
    errors = [r for r in records if "error" in r]

    analysis = {
        "experiment_id": EXP_ID,
        "viewport": "1280x720",
        "ax_mode": "CDP Accessibility.getFullAXTree",
        "records_total": len(records),
        "errors": errors,
        "product_page_captures": len(web_prod),
        "homepage_captures": len(web_home),
        "pc_a_captures": len(pca),
        "canonical_product_captures": len(canon),
        "ax_nodes_median_canonical": med([r["capture_before"]["ax_nodes"] for r in canon]),
        "ax_nodes_min_canonical": min((r["capture_before"]["ax_nodes"] for r in canon), default=None),
        "dom_bytes_median_canonical": med([r["capture_before"]["dom_bytes"] for r in canon]),
        "dom_bytes_min_canonical": min((r["capture_before"]["dom_bytes"] for r in canon), default=None),
        "canonical_sha_identical_all": all(r["sha_stability_identical"] for r in canon) if canon else None,
        "canonical_sha_mutation_changed_all": all(r["sha_mutation_changed"] for r in canon) if canon else None,
        "canonical_dual_impl_digest_match_all": all(
            r["capture_before"]["dual_impl_digest_match"] for r in canon) if canon else None,
        "pc_a_ax_nodes_median": med([r["capture_before"]["ax_nodes"] for r in pca]),
        "pc_a_dom_bytes_median": med([r["capture_before"]["dom_bytes"] for r in pca]),
        "pc_a_sha_identical_all": all(r["sha_stability_identical"] for r in pca) if pca else None,
        "pc_a_sha_mutation_changed_all": all(r["sha_mutation_changed"] for r in pca) if pca else None,
        "pc_a_anchors_gt1_all": all(all(v["present"] and v["node_count_subtree"] > 1
                                        for v in r["anchored"].values()) for r in pca) if pca else None,
        "constructible_families": constructible,
        "constructible_count": len(constructible),
        "mv4_constructible_gate_10": len(constructible) >= 10,
        "grammar_hash_live_last": (web_prod[-1] if web_prod else {}).get("capture_before", {}).get("grammar_hash_live"),
        "settings": {"viewport": "1280x720", "browser": "chromium",
                     "ax_mode": "CDP Accessibility.getFullAXTree", "stripping": "body DOTALL + 9 base + expanded"},
    }
    (DERIVED / "ax_analysis.json").write_text(json.dumps(analysis, indent=1))
    print(json.dumps(analysis, indent=1)[:3000])


if __name__ == "__main__":
    asyncio.run(main())
