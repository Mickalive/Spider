"""
EXP-INTEL-35999366789 Module A2b: deterministic family constructibility probe (MV3/MV4).

- Browser: Playwright 1.63.0 / Chromium 153 (MV3), viewport exactly 1280x720.
- AX: CDP Accessibility.getFullAXTree (snapshot fallback = invalid).
- SHA: outerHTML -> grammar strip (9 base + expanded fotorama\\d{6,} + body regex DOTALL)
  recomputed AFTER page.content()+AX; live grammar hash logged per capture.
- Anchoring (node_count>1, NOT AXNode bbox — Chromium153 fact 0/16 bbox): anchored
  Runtime.evaluate scan of heading/price/add-to-cart/main/contentinfo; node_count =
  matched-subtree element count (descendants + self); selector-count also logged.
- SHA stability both directions: reload re-capture identical; visible textContent
  mutation changes.
- Probe set = canonical families 136/145/196/222, product URLs derived deterministically
  from pinned census (first 3 unique product-page start_urls per family, census order).
  Sampled families without product URLs in census (137,153,162,163,180,191,197,213)
  are recorded not-constructible WITHOUT probe (homepage/template captures rejected by
  parent audit as product-page proxies, 18/20 identical) — documented per family.
- PC-A positive control: synthetic Flask product fixture x3 (validates CDP AX pipeline).
"""
from __future__ import annotations
import asyncio, json, hashlib, sys, os, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grammar_fulltree_358885 as g

EXP = Path(__file__).resolve().parent.parent / "experiments/EXP-INTEL-35999366789"
RAW = EXP / "artifacts/raw"
DERIVED = EXP / "artifacts/derived"
RAW.mkdir(parents=True, exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)
CAPTURE_LOG = RAW / "ax_captures.jsonl"
PROTOCOL_DUMP = RAW / "ax_protocol_dump.json"
FAMILY_ANCHORING = DERIVED / "family_anchoring.json"
AX_ANALYSIS = DERIVED / "ax_analysis.json"
SETTINGS = {"viewport": "1280x720", "browser": "chromium", "ax_mode": "CDP Accessibility.getFullAXTree"}

PRODUCT_URLS = {  # deterministic: first 3 unique product-page start_urls per family (census order)
    136: ["http://localhost:7770/ostent-16gb-memory-card-stick-storage-for-sony-ps-vita-psv1000-2000-pch-z081-z161-z321-z641.html",
          "http://localhost:7770/mineralogie-all-natural-lip-gloss-ruby-rose.html",
          "http://localhost:7770/sensodyne-repair-protect-whitening-toothpaste-with-fluoride-3-4-oz-pack-of-3.html"],
    145: ["http://localhost:7770/tall-pink-taper-candles-4-piece-orange-colored-tapered-candles-gradient-candles-10-6-inches-tall-tie-dye-candle-set-large-dripless-long-burning-candlesticks-two-color-taper-candles-candlesticks.html",
          "http://localhost:7770/spaas-white-taper-candles-4-pack-10-inch-tall-candles-scent-free-premium-wax-candle-sticks-8-hour-long-burning-white-candlesticks-for-home-decoration-wedding-holiday-and-parties.html",
          "http://localhost:7770/ciclon-energy-drink-regular-24-cans-8-3oz.html"],
    196: ["http://localhost:7770/elmwood-inn-fine-teas-orange-vanilla-caffeine-free-fruit-infusion-16-ounce-pouch.html",
          "http://localhost:7770/skinit-decal-gaming-skin-compatible-with-xbox-one-s-console-and-controller-bundle-officially-licensed-nfl-baltimore-ravens-design.html",
          "http://localhost:7770/sceptre-e195bd-srr-19-inch-720p-led-tv-true-black-2017.html"],
    222: ["http://localhost:7770/6s-wireless-headphones-over-ear-noise-canceling-hi-fi-bass-foldable-stereo-wireless-kid-headsets-earbuds-with-built-in-mic-micro-sd-tf-fm-for-iphone-samsung-ipad-pc-black-gold.html",
          "http://localhost:7770/fujifilm-finepix-z200fd-10mp-digital-camera-with-5x-optical-dual-image-stabilized-zoom-black.html",
          "http://localhost:7770/3-pack-samsung-galaxy-s6-screen-protector-nearpow-tempered-glass-screen-protector-with-9h-hardness-crystal-clear-easy-bubble-free-installation-scratch-resist.html"],
}
MUTATION_SELECTORS = [".price", "h1 span", ".product-name", "h1", ".product-info-price .price"]

ANCHOR_JS = """() => {
    const find = (sels) => { for (const s of sels) { const e = document.querySelector(s); if (e) return e; } return null; };
    const subtree = (el) => el ? (el.querySelectorAll('*').length + 1) : 0;
    const selcount = (sels) => sels.reduce((n, s) => n + document.querySelectorAll(s).length, 0);
    const heading = find(['h1', '.page-title', '.product-name']);
    const price = find(['.price-box', '.product-info-price .price', '.price', '.product-info-price']);
    const add = find(['#product-addtocart-button', '.tocart', 'button[title*=Cart]', '.add-to-cart button']);
    const main = find(['main', '.main', '#maincontent']);
    const cinfo = find(['footer', '.contentinfo', '.page-footer']);
    const r = {};
    for (const [k, el] of Object.entries({heading, price, add_to_cart: add, main, contentinfo: cinfo})) {
        r[k] = {present: !!el,
                node_count_subtree: subtree(el),
                selector_match_count: k === 'heading' ? selcount(['h1','.page-title','.product-name'])
                          : k === 'price' ? selcount(['.price-box','.product-info-price .price','.price','.product-info-price'])
                          : k === 'add_to_cart' ? selcount(['#product-addtocart-button','.tocart','button[title*=Cart]','.add-to-cart button'])
                          : k === 'main' ? selcount(['main','.main','#maincontent'])
                          : selcount(['footer','.contentinfo','.page-footer'])};
        if (el) { const b = el.getBoundingClientRect(); r[k].bbox = {x:b.x,y:b.y,w:b.width,h:b.height};
                  const cs = getComputedStyle(el); r[k].cs = {display:cs.display, visibility:cs.visibility}; }
    }
    return r;
}"""


async def full_capture(page, cdp, label):
    ax = await cdp.send("Accessibility.getFullAXTree")
    nodes = ax.get("nodes", [])
    content = await page.content()
    stripped = g.strip_dynamic_tokens(content)
    h = hashlib.sha256(stripped.encode("utf-8")).hexdigest()
    bbox_fields = sum(1 for n in nodes if n.get("boundingBox"))
    return {"label": label, "ax_nodes": len(nodes), "dom_bytes": len(content),
            "title": await page.title(), "hash": h, "hash_grammar_stripped": True,
            "bbox_fields_in_ax": bbox_fields, "grammar_hash_live": g.recompute_grammar_hash(),
            "ax_mode": "CDP Accessibility.getFullAXTree", "viewport": "1280x720"}


async def capture_page(page, cdp, fam, url):
    rec = {"url": url, "family": fam, "viewport": "1280x720", "ax_mode": "CDP Accessibility.getFullAXTree"}
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
                if (el) { el.textContent = el.textContent + ' [MUTATED-35999366789]'; return {selector: s, found: true}; }
            }
            return {selector: null, found: false};
        }""", MUTATION_SELECTORS)
    await page.wait_for_timeout(800)
    c3 = await full_capture(page, cdp, "mutated")
    geom = await page.evaluate(ANCHOR_JS)
    rec.update({"capture_before": c1, "capture_after": c2, "capture_mutated": c3,
                "mutation": mutated, "anchored": geom,
                "sha_stability_identical": c1["hash"] == c2["hash"],
                "sha_mutation_changed": c1["hash"] != c3["hash"]})
    return rec


async def synthetic_fixture(page, cdp, url):
    rec = {"url": url, "family": "PC-A-SYNTHETIC-FIXTURE", "viewport": "1280x720", "ax_mode": "CDP Accessibility.getFullAXTree"}
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
    rec.update({"capture_before": c1, "capture_after": c2, "capture_mutated": c3,
                "anchored": geom, "sha_stability_identical": c1["hash"] == c2["hash"],
                "sha_mutation_changed": c1["hash"] != c3["hash"]})
    return rec


async def protocol_dump():
    from playwright.async_api import async_playwright as apw
    import urllib.request as ur
    async with apw() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--remote-debugging-port=9335"])
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await ctx.new_page()
        await page.goto("http://localhost:7770/", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(800)
        proto = json.load(ur.urlopen("http://localhost:9335/json/protocol"))
        acc = [d for d in proto["domains"] if d["domain"] == "Accessibility"]
        axnode_type = None
        for t in acc[0].get("types", []):
            if t["id"] == "AXNode":
                axnode_type = {"type_id": t["id"], "properties": [{"name": pr["name"], "optional": pr.get("optional", False), "type": pr.get("type")} for pr in t.get("properties", [])]}
        getfull = None
        for m in acc[0].get("commands", []):
            if m["name"] == "getFullAXTree":
                getfull = {"name": m["name"], "params": [p2["name"] for p2 in m.get("parameters", [])]}
        dump = {"browser_version": browser.version, "axnode_type": axnode_type, "getFullAXTree": getfull,
                "bbox_present_in_axnode": any(p["name"] == "boundingBox" for p in (axnode_type or {}).get("properties", [])),
                "viewport": "1280x720"}
        PROTOCOL_DUMP.write_text(json.dumps(dump, indent=1))
        print("protocol dump:", json.dumps(dump, indent=1)[:800])
        await browser.close()


async def main():
    if os.environ.get("SKIP_PROTOCOL_DUMP") != "1":
        await protocol_dump()

    from playwright.async_api import async_playwright
    records = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        for fam in (136, 145, 196, 222):
            for url in PRODUCT_URLS[fam]:
                try:
                    rec = await capture_page(page, cdp, f"fam{fam}", url)
                    records.append(rec)
                    print(f"fam{fam} nodes={rec['capture_before']['ax_nodes']} dom={rec['capture_before']['dom_bytes']} "
                          f"stable={rec['sha_stability_identical']} mut={rec['sha_mutation_changed']}")
                except Exception as e:  # noqa: BLE001
                    records.append({"url": url, "family": f"fam{fam}", "error": f"{type(e).__name__}: {e}"})
                    print(f"fam{fam} {url[:60]} ERROR {type(e).__name__}: {e}")
        await browser.close()

    # PC-A synthetic fixture x3
    from flask import Flask
    app = Flask("pc_a_fixture_35999366789")
    FIXTURE_HTML = """<!doctype html><html><head><title>PC-A Product</title></head>
<body><header class="site-header"><h1>Acme Widget 3000</h1></header>
<main id="maincontent"><div class="product-info"><span class="price">$1.00</span>
<button id="product-addtocart-button">Add to Cart</button></div></main>
<footer class="contentinfo">Copyright Acme 2026</footer></body></html>"""

    @app.route("/")
    def idx():
        return FIXTURE_HTML

    import threading
    t = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=8899, debug=False, use_reloader=False), daemon=True)
    t.start()
    time.sleep(1.5)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        for i in range(3):
            rec = await synthetic_fixture(page, cdp, "http://127.0.0.1:8899/")
            rec["repeat"] = i + 1
            records.append(rec)
            print(f"PC-A repeat {i+1}: nodes={rec['capture_before']['ax_nodes']} dom={rec['capture_before']['dom_bytes']} "
                  f"stable={rec['sha_stability_identical']} mut={rec['sha_mutation_changed']}")
        await browser.close()

    with CAPTURE_LOG.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print("wrote", CAPTURE_LOG, "records:", len(records))

    # ---- family anchoring derivation ----
    anchoring = {}
    for fam in (136, 145, 196, 222):
        fam_recs = [r for r in records if r.get("family") == f"fam{fam}" and "error" not in r]
        per_url = []
        fam_anchor = False
        fam_sha = {"identical": None, "mutated": None}
        for r in fam_recs:
            a = r["anchored"]
            all_gt1 = all(v["present"] and v["node_count_subtree"] > 1 for v in a.values())
            per_url.append({"url": r["url"], "anchoring_all_categories_gt1": all_gt1,
                            "node_counts": {k: v["node_count_subtree"] for k, v in a.items()},
                            "present": {k: v["present"] for k, v in a.items()},
                            "sha_stability_identical": r["sha_stability_identical"],
                            "sha_mutation_changed": r["sha_mutation_changed"]})
            if all_gt1 and r["sha_stability_identical"] and r["sha_mutation_changed"]:
                fam_anchor = True
        fam_sha = {"identical": all(r["sha_stability_identical"] for r in fam_recs) if fam_recs else None,
                   "mutated": all(r["sha_mutation_changed"] for r in fam_recs) if fam_recs else None}
        anchoring[f"fam{fam}"] = {
            "family": fam, "product_urls_probed": [r["url"] for r in fam_recs],
            "n_probed": len(fam_recs), "per_url": per_url,
            "family_constructible": fam_anchor,
            "family_sha_identical_all": fam_sha["identical"], "family_sha_mutated_all": fam_sha["mutated"],
            "anchoring_definition": "product-subtree anchoring via anchored Runtime.evaluate getBoundingClientRect scan (NOT AXNode bbox, Chromium153 0/16 fact); category root selectors: heading h1/.page-title/.product-name; price .price-box/.product-info-price/.price; add_to_cart #product-addtocart-button/.tocart/add-to-cart button; main main/.main/#maincontent; contentinfo footer/.contentinfo/.page-footer. node_count = element-node count of anchored subtree root (descendants+self)."}

    # sampled families without product URLs in census -> recorded, not probed
    nonprod = sorted({137, 153, 162, 163, 180, 191, 197, 213})
    for fid in nonprod:
        anchoring[f"fam{fid}"] = {"family": fid, "product_urls_probed": [], "n_probed": 0,
                                  "family_constructible": False,
                                  "reason": "No product-page start_urls in pinned census (all tasks start at __SHOPPING__ homepage / non-product paths). Homepage/template captures rejected by parent audit as product-page proxies (18/20 identical); not probed."}
    FAMILY_ANCHORING.write_text(json.dumps(anchoring, indent=1))

    # ---- ax analysis ----
    web = [r for r in records if r.get("family", "").startswith("fam") and "error" not in r]
    pca = [r for r in records if r.get("family") == "PC-A-SYNTHETIC-FIXTURE" and "error" not in r]
    med = lambda xs: sorted(xs)[len(xs)//2] if xs else None
    analysis = {
        "experiment_id": "EXP-INTEL-35999366789",
        "viewport": "1280x720", "ax_mode": "CDP Accessibility.getFullAXTree",
        "web_product_captures": len(web), "pc_a_captures": len(pca),
        "ax_nodes_median_web": med([r["capture_before"]["ax_nodes"] for r in web]),
        "ax_nodes_min_web": min([r["capture_before"]["ax_nodes"] for r in web]) if web else None,
        "dom_bytes_median_web": med([r["capture_before"]["dom_bytes"] for r in web]),
        "dom_bytes_min_web": min([r["capture_before"]["dom_bytes"] for r in web]) if web else None,
        "sha_stability_identical_web": [r["sha_stability_identical"] for r in web],
        "sha_mutation_changed_web": [r["sha_mutation_changed"] for r in web],
        "sha_stability_identical_all_true": all(r["sha_stability_identical"] for r in web) if web else None,
        "sha_mutation_changed_all_true": all(r["sha_mutation_changed"] for r in web) if web else None,
        "ax_nodes_median_pc_a": med([r["capture_before"]["ax_nodes"] for r in pca]),
        "dom_bytes_median_pc_a": med([r["capture_before"]["dom_bytes"] for r in pca]),
        "sha_pc_a_identical_all_true": all(r["sha_stability_identical"] for r in pca) if pca else None,
        "sha_pc_a_mutated_all_true": all(r["sha_mutation_changed"] for r in pca) if pca else None,
        "anchored_geometry_via_evaluate_web_all5": sum(1 for r in web if all(v["present"] for v in r["anchored"].values())),
        "anchored_geometry_via_evaluate_web_total": len(web),
        "richer_bbox_via_evaluate": (sum(1 for r in web if all(v["present"] for v in r["anchored"].values())), len(web)),
        "max_anchor_subtree_node_counts": {f"fam{f}": {k: max((u.get("node_counts", {}).get(k, 0) for u in anchoring[f"fam{f}"].get("per_url", [])), default=0) for k in ("heading", "price", "add_to_cart", "main", "contentinfo")} for f in (136, 145, 196, 222)},
        "constructible_families": sorted(k for k, v in anchoring.items() if v["family_constructible"]),
        "constructible_count": sum(1 for v in anchoring.values() if v["family_constructible"]),
        "mv4_constructible_gate_10": sum(1 for v in anchoring.values() if v["family_constructible"]) >= 10,
        "non_product_sampled_families_recorded": nonprod,
        "settings": SETTINGS,
        "grammar_hash_live_last": web[-1]["capture_before"]["grammar_hash_live"] if web else None,
    }
    AX_ANALYSIS.write_text(json.dumps(analysis, indent=1))
    print("analysis:", json.dumps(analysis, indent=1)[:1200])


if __name__ == "__main__":
    asyncio.run(main())