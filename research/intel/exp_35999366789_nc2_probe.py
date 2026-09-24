"""
EXP-INTEL-35999366789 NC2-TRUNCATED empirical probe (post-freeze measurement control).
Re-captures a SUBSET of pages (2 WebArena + PC-A synthetic) storing the RAW stripped
outerHTML before/after mutation, then computes:
  - full-tree mutation sensitivity (hash of full stripped content changes)
  - tokens[:20]-truncated mutation sensitivity (hash of first 20 whitespace tokens
    of the stripped content changes)
  - delta_vs_truncated = full_sensitivity - truncated_sensitivity
Matched to frozen B-TRUNCATED-20 (tokens[:20]) semantics on the SAME strip grammar
(research/intel/grammar_fulltree_358885.py). Does NOT overwrite ax_captures.jsonl.
"""
from __future__ import annotations
import asyncio, json, hashlib, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grammar_fulltree_358885 as g

OUT = Path(__file__).resolve().parent.parent / "experiments/EXP-INTEL-35999366789/artifacts/derived/truncation_control.json"

PRODUCT_URLS = [
    ("fam136", "http://localhost:7770/ostent-16gb-memory-card-stick-storage-for-sony-ps-vita-psv1000-2000-pch-z081-z161-z321-z641.html"),
    ("fam222", "http://localhost:7770/epson-workforce-wf-3620-wifi-direct-all-in-one-color-inkjet-printer-copier-scanner-amazon-dash-replenishment-ready.html"),
]

MUTATION_SELECTORS = [".price", "h1 span", ".product-name", "h1", ".product-info-price .price"]

FIXTURE_HTML = """<!doctype html><html><head><title>PC-A Product</title></head>
<body><header class="site-header"><h1>Acme Widget 3000</h1></header>
<main id="maincontent"><div class="product-info"><span class="price">$1.00</span>
<button id="product-addtocart-button">Add to Cart</button></div></main>
<footer class="contentinfo">Copyright Acme 2026</footer></body></html>"""


def trunc_hash_of(content: str, n: int = 20) -> str:
    toks = content.split()[:n]
    return hashlib.sha256(" ".join(toks).encode()).hexdigest()


def compare(before_stripped: str, after_stripped: str) -> dict:
    full_before = hashlib.sha256(before_stripped.encode()).hexdigest()
    full_after = hashlib.sha256(after_stripped.encode()).hexdigest()
    tr_before = trunc_hash_of(before_stripped, 20)
    tr_after = trunc_hash_of(after_stripped, 20)
    return {
        "full_sensitive": full_before != full_after,
        "truncated_sensitive": tr_before != tr_after,
        "full_before_hash": full_before,
        "full_after_hash": full_after,
        "truncated_before_hash": tr_before,
        "truncated_after_hash": tr_after,
        "full_before_len": len(before_stripped),
    }


async def web_page(page, cdp, fam, url):
    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(2000)
    before = g.strip_dynamic_tokens(await page.content())
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
    after = g.strip_dynamic_tokens(await page.content())
    comp = compare(before, after)
    comp.update({"family": fam, "url": url, "mutation": mutated,
                 "selector_hit": mutated.get("selector")})
    return comp


async def pc_a(page, cdp):
    from flask import Flask
    import threading, time
    app = Flask("pc_a_nc2")
    @app.route("/")
    def idx():
        return FIXTURE_HTML
    t = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=8898, debug=False, use_reloader=False), daemon=True)
    t.start()
    time.sleep(1.5)
    await page.goto("http://127.0.0.1:8898/", wait_until="domcontentloaded", timeout=30000)
    await page.wait_for_timeout(800)
    before = g.strip_dynamic_tokens(await page.content())
    await page.evaluate("""() => { const p = document.querySelector('.price'); p.textContent = p.textContent.replace('$1.00','$2.00'); }""")
    await page.wait_for_timeout(500)
    after = g.strip_dynamic_tokens(await page.content())
    comp = compare(before, after)
    comp.update({"family": "PC-A-SYNTHETIC-FIXTURE", "url": "http://127.0.0.1:8898/",
                 "mutation": {"selector": ".price", "found": True}, "selector_hit": ".price"})
    return comp


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        recs = []
        for fam, url in PRODUCT_URLS:
            try:
                r = await web_page(page, cdp, fam, url)
                recs.append(r)
                print(f"{fam} {url[:55]} full_sens={r['full_sensitive']} trunc_sens={r['truncated_sensitive']} hit={r.get('selector_hit')}")
            except Exception as e:
                recs.append({"family": fam, "url": url, "error": f"{type(e).__name__}: {e}"})
                print(f"{fam} ERROR {type(e).__name__}: {e}")
        r2 = await pc_a(page, cdp)
        recs.append(r2)
        print(f"PC-A full_sens={r2['full_sensitive']} trunc_sens={r2['truncated_sensitive']}")
        await browser.close()

    full_sens = sum(1 for r in recs if r.get("full_sensitive")) / len(recs)
    trunc_sens = sum(1 for r in recs if r.get("truncated_sensitive")) / len(recs)
    out = {
        "experiment_id": "EXP-INTEL-35999366789",
        "control": "NC2-TRUNCATED",
        "semantics": "tokens[:20] of stripped outerHTML (same grammar as full-tree) vs full stripped outerHTML SHA256",
        "n": len(recs),
        "full_tree_mutation_sensitivity": round(full_sens, 4),
        "truncated_mutation_sensitivity": round(trunc_sens, 4),
        "delta_vs_truncated": round(full_sens - trunc_sens, 4),
        "delta_ge_0_20": (full_sens - trunc_sens) >= 0.20,
        "per_record": recs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    s = json.dumps(out, sort_keys=True, indent=1)
    OUT.write_text(s + "\n")
    print("wrote", OUT)
    print("sha256:", hashlib.sha256(s.encode()).hexdigest())
    print("summary:", {k: out[k] for k in ("n", "full_tree_mutation_sensitivity", "truncated_mutation_sensitivity", "delta_vs_truncated", "delta_ge_0_20")})


if __name__ == "__main__":
    asyncio.run(main())