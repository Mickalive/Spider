"""
EXP-INTEL-35956094394 Module A2: AX fragment-repair probe.
- CDP Accessibility.getFullAXTree at 1280x720 (Playwright 1.63.0 / Chromium 153).
- outerHTML SHA256 with 9 base + bounded expanded + body-regex stripping, recomputed
  AFTER page.content() + AX call (grammar module hash recomputed live).
- SHA stability both directions: identical on re-capture; different after visible
  textContent mutation.
- Records richer-AX evidence: AXNode field inventory (protocol dump) + anchored-element
  boundingClientRect/computedStyle via Runtime.evaluate on the same capture cycle.
- Positive control PC-A: synthetic Flask product fixture with fixed ~20-node AX tree.
"""
from __future__ import annotations
import asyncio, json, hashlib, sys, os, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grammar_fulltree_358885 as g

CAPTURE_LOG = Path(__file__).resolve().parent.parent / "experiments/EXP-INTEL-35956094394/artifacts/raw/ax_captures.jsonl"
PROTOCOL_DUMP = Path(__file__).resolve().parent.parent / "experiments/EXP-INTEL-35956094394/artifacts/raw/ax_protocol_dump.json"

PRODUCT_URLS = [
    # family 136
    ("fam136", "http://localhost:7770/ostent-16gb-memory-card-stick-storage-for-sony-ps-vita-psv1000-2000-pch-z081-z161-z321-z641.html"),
    ("fam136", "http://localhost:7770/mineralogie-all-natural-lip-gloss-ruby-rose.html"),
    ("fam136", "http://localhost:7770/photosmart-plus-b209-clr-inkjetfb-p-s-c-usb-wrls-1.html"),
    # family 145
    ("fam145", "http://localhost:7770/35-ft-hdmi-cable-gearit-pro-series-hdmi-cable-35-feet-high-speed-ethernet-4k-resolution-3d-video-and-arc-audio-return-channel-hdmi-cable-white.html"),
    ("fam145", "http://localhost:7770/ciclon-energy-drink-regular-24-cans-8-3oz.html"),
    ("fam145", "http://localhost:7770/spaas-white-taper-candles-4-pack-10-inch-tall-candles-scent-free-premium-wax-candle-sticks-8-hour-long-burning-white-candlesticks-for-home-decoration-wedding-holiday-and-parties.html"),
    # family 196
    ("fam196", "http://localhost:7770/elmwood-inn-fine-teas-orange-vanilla-caffeine-free-fruit-infusion-16-ounce-pouch.html"),
    ("fam196", "http://localhost:7770/sceptre-e195bd-srr-19-inch-720p-led-tv-true-black-2017.html"),
    ("fam196", "http://localhost:7770/iphone-13-pro-max-case-neon-turtle-iphone-13-pro-max-cases-tempered-glass-back-soft-silicone-tpu-shock-protective-case-for-apple-iphone-13-pro-max.html"),
    # family 222
    ("fam222", "http://localhost:7770/6s-wireless-headphones-over-ear-noise-canceling-hi-fi-bass-foldable-stereo-wireless-kid-headsets-earbuds-with-built-in-mic-micro-sd-tf-fm-for-iphone-samsung-ipad-pc-black-gold.html"),
    ("fam222", "http://localhost:7770/fujifilm-finepix-z200fd-10mp-digital-camera-with-5x-optical-dual-image-stabilized-zoom-black.html"),
    ("fam222", "http://localhost:7770/epson-workforce-wf-3620-wifi-direct-all-in-one-color-inkjet-printer-copier-scanner-amazon-dash-replenishment-ready.html"),
    ("fam222", "http://localhost:7770/3-pack-samsung-galaxy-s6-screen-protector-nearpow-tempered-glass-screen-protector-with-9h-hardness-crystal-clear-easy-bubble-free-installation-scratch-resist.html"),
]

MUTATION_SELECTORS = [".price", "h1 span", ".product-name", "h1", ".product-info-price .price"]

async def full_capture(page, cdp, label):
    """Capture AX tree + outerHTML; returns dict with hashes AFTER content()+AX."""
    ax = await cdp.send("Accessibility.getFullAXTree")
    nodes = ax.get("nodes", [])
    content = await page.content()
    stripped = g.strip_dynamic_tokens(content)
    h = hashlib.sha256(stripped.encode("utf-8")).hexdigest()
    bbox_fields = sum(1 for n in nodes if n.get("boundingBox"))
    return {
        "label": label,
        "ax_nodes": len(nodes),
        "dom_bytes": len(content),
        "title": await page.title(),
        "hash": h,
        "bbox_fields_in_ax": bbox_fields,
        "grammar_hash_live": g.recompute_grammar_hash(),
    }

async def capture_page(page, cdp, ctx, fam, url):
    rec = {"url": url, "family": fam, "viewport": "1280x720"}
    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(2000)
    c1 = await full_capture(page, cdp, "before")
    # re-capture without mutation (reload + full cycle)
    await page.reload(wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(2000)
    c2 = await full_capture(page, cdp, "after")
    # mutation: change visible textContent of first matched element
    mutated = await page.evaluate(
        """(selectors) => {
            for (const s of selectors) {
                const el = document.querySelector(s);
                if (el) {
                    el.textContent = el.textContent + ' [MUTATED-35956094394]';
                    return {selector: s, found: true};
                }
            }
            return {selector: null, found: false};
        }""", MUTATION_SELECTORS)
    await page.wait_for_timeout(800)
    c3 = await full_capture(page, cdp, "mutated")
    # richer geometry of anchored elements (same capture cycle)
    geom = await page.evaluate(
        """() => {
            const anchors = {heading:null, price:null, add_to_cart:null, main:null, contentinfo:null};
            const q = (s) => document.querySelector(s);
            const heading = q('h1') || q('.page-title') || q('.product-name');
            const price = q('.price') || q('.product-info-price .price');
            const add = q('#product-addtocart-button, .tocart, button[title*=Cart], .add-to-cart button');
            const main = q('main') || q('.main') || q('#maincontent');
            const cinfo = q('footer, .contentinfo, .page-footer');
            const r = {};
            for (const [k, el] of Object.entries({heading, price, add_to_cart: add, main, contentinfo: cinfo})) {
                if (el) {
                    const b = el.getBoundingClientRect();
                    const cs = getComputedStyle(el);
                    r[k] = {bbox: {x:b.x,y:b.y,w:b.width,h:b.height}, cs: {display:cs.display, visibility:cs.visibility}};
                }
            }
            return r;
        }""")
    rec.update({
        "capture_before": c1, "capture_after": c2, "capture_mutated": c3,
        "mutation": mutated,
        "anchored_geometry": geom,
        "sha_stability_identical": c1["hash"] == c2["hash"],
        "sha_mutation_changed": c1["hash"] != c3["hash"],
    })
    return rec

async def synthetic_fixture(page, cdp, ctx, url):
    rec = {"url": url, "family": "PC-A-SYNTHETIC-FIXTURE", "viewport": "1280x720"}
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(800)
    c1 = await full_capture(page, cdp, "before")
    await page.reload(wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(800)
    c2 = await full_capture(page, cdp, "after")
    # mutate price $1.00 -> $2.00
    await page.evaluate("""() => { const p = document.querySelector('.price'); p.textContent = p.textContent.replace('$1.00','$2.00'); }""")
    await page.wait_for_timeout(500)
    c3 = await full_capture(page, cdp, "mutated")
    rec.update({"capture_before": c1, "capture_after": c2, "capture_mutated": c3,
                "sha_stability_identical": c1["hash"] == c2["hash"],
                "sha_mutation_changed": c1["hash"] != c3["hash"]})
    return rec

async def main():
    # protocol dump (AXNode field inventory) — first browser
    from playwright.async_api import async_playwright as apw
    import urllib.request as ur
    async with apw() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--remote-debugging-port=9334"])
        ctx = await browser.new_context(viewport={"width":1280,"height":720})
        page = await ctx.new_page()
        await page.goto("http://localhost:7770/", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(800)
        proto = json.load(ur.urlopen("http://localhost:9334/json/protocol"))
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
                "bbox_present_in_axnode": any(p["name"] == "boundingBox" for p in (axnode_type or {}).get("properties", []))}
        PROTOCOL_DUMP.parent.mkdir(parents=True, exist_ok=True)
        PROTOCOL_DUMP.write_text(json.dumps(dump, indent=1))
        print("protocol dump:", json.dumps(dump))

    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1280,"height":720})
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        records = []
        for fam, url in PRODUCT_URLS:
            try:
                rec = await capture_page(page, cdp, ctx, fam, url)
                records.append(rec)
                print(f"{fam} {url[:60]} nodes={rec['capture_before']['ax_nodes']} dom={rec['capture_before']['dom_bytes']} "
                      f"stable={rec['sha_stability_identical']} mut={rec['sha_mutation_changed']}")
            except Exception as e:
                records.append({"url": url, "family": fam, "error": f"{type(e).__name__}: {e}"})
                print(f"{fam} {url[:60]} ERROR {type(e).__name__}: {e}")
        await browser.close()

    # synthetic fixture (PC-A)
    from flask import Flask
    app = Flask("pc_a_fixture")
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
        ctx = await browser.new_context(viewport={"width":1280,"height":720})
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        for i in range(3):
            rec = await synthetic_fixture(page, cdp, ctx, "http://127.0.0.1:8899/")
            rec["repeat"] = i + 1
            records.append(rec)
            print(f"PC-A repeat {i+1}: nodes={rec['capture_before']['ax_nodes']} dom={rec['capture_before']['dom_bytes']} "
                  f"stable={rec['sha_stability_identical']} mut={rec['sha_mutation_changed']}")
        await browser.close()

    CAPTURE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CAPTURE_LOG.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print("wrote", CAPTURE_LOG, "records:", len(records))

if __name__ == "__main__":
    asyncio.run(main())