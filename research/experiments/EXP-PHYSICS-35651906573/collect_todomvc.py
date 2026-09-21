#!/usr/bin/env python3
"""EXP-PHYSICS-35651906573 — browser collection for real TodoMVC hash-SPA transitions.

Frozen design mapping (spec.json measurement_validity #1-#6, prereg "Data Collection"):

  Variants (spec shorthand -> live dist URL; same five frameworks as parent
  EXP-PHYSICS-35209110569, whose frozen collection used these exact dist URLs;
  bare /examples/{name}/ paths now 404 on todomvc.com):
    vanillajs -> https://todomvc.com/examples/javascript-es6/dist/
    react     -> https://todomvc.com/examples/react/dist/
    vue       -> https://todomvc.com/examples/vue/dist/
    angular   -> https://todomvc.com/examples/angular/dist/browser/
    svelte    -> https://todomvc.com/examples/svelte/dist/

  Per variant: >=5 distinct browsing sessions with different starting points and
  action sequences (session-indexed filter/JS offsets, unique task names).
  Per-transition record: url_before, url_after, title_before, title_after,
  action_primitive (link_click | button_click | form_submit | js_navigate),
  action_target (resolved absolute href for link_click else None), timestamp, error.

  Target >=100 raw transitions per variant so that >=50 non-leakage transitions
  are achievable at the parent-validated leakage 0.21-0.28 (6 sessions x 24 actions
  = 144 raw).

  Leakage definition (frozen, same as parent): action_target == url_after under
  normalize() = strip fragment, rstrip '/', unquote.
"""
import json
import sys
import time
import random
import urllib.parse
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

VARIANTS = {
    "vanillajs": "https://todomvc.com/examples/javascript-es6/dist/",
    "react": "https://todomvc.com/examples/react/dist/",
    "vue": "https://todomvc.com/examples/vue/dist/",
    "angular": "https://todomvc.com/examples/angular/dist/browser/",
    "svelte": "https://todomvc.com/examples/svelte/dist/",
}

ACTIONS_PER_SESSION = 24  # 3 seed form_submits + 21 mixed actions
SESSIONS_PER_SITE = 6
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "raw_transitions.json"
ONLY = sys.argv[2] if len(sys.argv) > 2 else None


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def safe_title(page):
    try:
        return page.title()
    except Exception:
        return ""


def spa_session(page, variant_key, session_idx, rng, seed_actions=3):
    """One session: 3 form_submit seeds + 21 mixed actions (parent 7-step cycle)."""
    recs = []
    # --- seed phase: form_submit (add todos) ---
    for k in range(seed_actions):
        before_url, before_title = page.url, safe_title(page)
        box = page.query_selector("input.new-todo")
        if box is None:
            break
        text = f"task-{variant_key}-{session_idx}-{k}-{rng.randint(0, 9999)}"
        try:
            box.fill(text)
            box.press("Enter")
            page.wait_for_timeout(500)
            err = None
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
        recs.append({
            "site": variant_key, "session": session_idx,
            "url_before": before_url, "url_after": page.url,
            "title_before": before_title, "title_after": safe_title(page),
            "action_primitive": "form_submit", "action_target": None,
            "timestamp": now_iso(), "error": err,
        })
        page.wait_for_timeout(200)
    # --- mixed phase: 21 actions cycling 7-step pattern ---
    filters = ["#/", "#/active", "#/completed"]
    fi = session_idx % 3
    js_ops = ["reload", "back", "forward"]
    ji = session_idx % 3
    for step in range(21):
        kind = step % 7
        before_url, before_title = page.url, safe_title(page)
        prim, target, err = None, None, None
        try:
            if kind in (0, 3):  # link_click on filter links
                href = filters[(fi + step) % 3]
                el = page.query_selector(f'a[href="{href}"]')
                if el is None:
                    cands = page.query_selector_all('a[href^="#/"]')
                    el = cands[(fi + step) % len(cands)] if cands else None
                if el is None:
                    raise RuntimeError("no filter link found")
                raw_href = el.get_attribute("href")
                target = urllib.parse.urljoin(page.url, raw_href)
                el.click(force=True)
                page.wait_for_timeout(500)
                prim = "link_click"
            elif kind in (1, 5):  # button_click: toggle a visible todo
                toggles = page.query_selector_all("ul.todo-list li input.toggle")
                if not toggles:
                    raise RuntimeError("no toggle available")
                toggles[step % len(toggles)].click(force=True)
                page.wait_for_timeout(500)
                prim = "button_click"
            elif kind == 2:  # form_submit: add todo
                box = page.query_selector("input.new-todo")
                if box is None:
                    raise RuntimeError("no new-todo box")
                box.fill(f"extra-{variant_key}-{session_idx}-{step}-{rng.randint(0,9999)}")
                box.press("Enter")
                page.wait_for_timeout(500)
                prim = "form_submit"
            elif kind == 4:  # button_click: destroy (or toggle fallback)
                items = page.query_selector_all("ul.todo-list li")
                if len(items) > 1:
                    btn = items[step % len(items)].query_selector("button.destroy")
                    if btn is None:
                        raise RuntimeError("no destroy button")
                    btn.click(force=True)
                    page.wait_for_timeout(500)
                    prim = "button_click"
                    target = "destroy"
                else:
                    toggles = page.query_selector_all("ul.todo-list li input.toggle")
                    if not toggles:
                        raise RuntimeError("no toggle fallback")
                    toggles[0].click(force=True)
                    page.wait_for_timeout(500)
                    prim = "button_click"
            else:  # kind == 6: js_navigate
                op = js_ops[(ji + step) % 3]
                if op == "reload":
                    page.reload(wait_until="domcontentloaded")
                elif op == "back":
                    page.go_back(wait_until="domcontentloaded")
                else:
                    page.go_forward(wait_until="domcontentloaded")
                page.wait_for_timeout(500)
                prim = "js_navigate"
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            prim = prim or ("link_click" if kind in (0, 3) else
                            "form_submit" if kind == 2 else
                            "js_navigate" if kind == 6 else "button_click")
        recs.append({
            "site": variant_key, "session": session_idx,
            "url_before": before_url, "url_after": page.url,
            "title_before": before_title, "title_after": safe_title(page),
            "action_primitive": prim, "action_target": target,
            "timestamp": now_iso(), "error": err,
        })
        page.wait_for_timeout(200)
    return recs


def run_site(p, site_key, seed):
    rng = random.Random(seed)
    all_recs = []
    for s in range(SESSIONS_PER_SITE):
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        try:
            ctx = browser.new_context(viewport={"width": 1280, "height": 720})
            page = ctx.new_page()
            page.goto(VARIANTS[site_key], timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            recs = spa_session(page, site_key, s, rng)
            all_recs.extend(recs)
            print(f"[{site_key}] session {s}: {len(recs)} transitions", flush=True)
            ctx.close()
        except Exception as e:
            print(f"[{site_key}] session {s} FAILED: {type(e).__name__}: {e}", flush=True)
            all_recs.append({
                "site": site_key, "session": s, "url_before": None,
                "url_after": None, "title_before": None, "title_after": None,
                "action_primitive": None, "action_target": None,
                "timestamp": now_iso(), "error": f"SESSION_FAIL {type(e).__name__}: {e}",
            })
        finally:
            try:
                browser.close()
            except Exception:
                pass
            time.sleep(0.8)
    return all_recs


def main():
    sites = list(VARIANTS.keys())
    if ONLY:
        sites = [s for s in sites if s == ONLY]
    out = []
    with sync_playwright() as p:
        for i, site in enumerate(sites):
            print(f"[{site}] Starting...", flush=True)
            try:
                recs = run_site(p, site, seed=2000 + i * 97)
            except Exception as e:
                print(f"[{site}] SITE FAILED: {type(e).__name__}: {e}", flush=True)
                recs = [{
                    "site": site, "session": -1, "url_before": None,
                    "url_after": None, "title_before": None, "title_after": None,
                    "action_primitive": None, "action_target": None,
                    "timestamp": now_iso(), "error": f"SITE_FAIL {type(e).__name__}: {e}",
                }]
            out.extend(recs)
            with open(OUT_PATH, "w") as f:
                json.dump(out, f, indent=1)
            print(f"[{site}] done, cumulative={len(out)}", flush=True)
    print(f"TOTAL {len(out)} transitions -> {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()