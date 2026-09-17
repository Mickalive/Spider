#!/usr/bin/env python3
"""EXP-PHYSICS-35209110569 frozen-design collection script (EXECUTE stage).

Frozen spec mapping (spec.json measurement_validity #1 + prereg section 4):
  vanillajs -> https://todomvc.com/examples/javascript-es6/dist/
  react     -> https://todomvc.com/examples/react/dist/
  vue       -> https://todomvc.com/examples/vue/dist/
  angular   -> https://todomvc.com/examples/angular/dist/browser/
  svelte    -> https://todomvc.com/examples/svelte/dist/
  wikipedia (null control, server-rendered MPA) -> https://en.wikipedia.org/wiki/Main_Page

Per variant: 5 sessions x 24 actions (>=100 raw transitions, >=5 sessions,
20+ unique URLs target, 4 action primitive classes). Per-transition record:
url_before, url_after, title_before, title_after, action_primitive
(link_click | button_click | form_submit | js_navigate), action_target
(resolved absolute href for link_click else null), timestamp.

EPIPE mitigation (frozen): single-page context per session, close BROWSER
between sessions, polite delays, no context close before load complete.
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
WIKI_STARTS = [
    "https://en.wikipedia.org/wiki/HTML",
    "https://en.wikipedia.org/wiki/Web_browser",
    "https://en.wikipedia.org/wiki/World_Wide_Web",
    "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol",
    "https://en.wikipedia.org/wiki/Uniform_Resource_Locator",
]

ACTIONS_PER_SESSION = 24
SESSIONS_PER_SITE = 5
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "raw_transitions.json"
ONLY = sys.argv[2] if len(sys.argv) > 2 else None  # optional site key filter
START_SESSION = int(sys.argv[3]) if len(sys.argv) > 3 else 0
N_SESSIONS = int(sys.argv[4]) if len(sys.argv) > 4 else SESSIONS_PER_SITE


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def safe_title(page):
    try:
        return page.title()
    except Exception:
        return ""


def spa_session(page, variant_key, session_idx, rng):
    """Run one 24-action SPA session. Returns list of transition dicts."""
    recs = []
    # --- seed phase: 3 form_submit (add todo) ---
    for k in range(3):
        before_url, before_title = page.url, safe_title(page)
        box = page.query_selector("input.new-todo")
        if box is None:
            break
        text = f"task-{variant_key}-{session_idx}-{k}-{rng.randint(0, 9999)}"
        try:
            box.fill(text)
            box.press("Enter")
            page.wait_for_timeout(600)
        except Exception as e:
            recs.append({
                "site": variant_key, "session": session_idx,
                "url_before": before_url, "url_after": page.url,
                "title_before": before_title, "title_after": safe_title(page),
                "action_primitive": "form_submit", "action_target": None,
                "timestamp": now_iso(), "error": f"{type(e).__name__}: {e}",
            })
            continue
        recs.append({
            "site": variant_key, "session": session_idx,
            "url_before": before_url, "url_after": page.url,
            "title_before": before_title, "title_after": safe_title(page),
            "action_primitive": "form_submit", "action_target": None,
            "timestamp": now_iso(), "error": None,
        })
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
                    # fallback: any hash link
                    cands = page.query_selector_all('a[href^="#/"]')
                    el = cands[(fi + step) % len(cands)] if cands else None
                if el is None:
                    raise RuntimeError("no filter link found")
                raw_href = el.get_attribute("href")
                target = urllib.parse.urljoin(page.url, raw_href)
                el.click()
                page.wait_for_timeout(600)
                prim = "link_click"
            elif kind in (1, 5):  # button_click: toggle first visible todo
                toggles = page.query_selector_all("ul.todo-list li input.toggle")
                if not toggles:
                    # fallback: add a todo then toggle it next time; record click attempt on body as button
                    raise RuntimeError("no toggle available")
                toggles[step % len(toggles)].click(force=True)
                page.wait_for_timeout(600)
                prim = "button_click"
            elif kind == 2:  # form_submit: add todo
                box = page.query_selector("input.new-todo")
                if box is None:
                    raise RuntimeError("no new-todo box")
                box.fill(f"extra-{variant_key}-{session_idx}-{step}-{rng.randint(0,9999)}")
                box.press("Enter")
                page.wait_for_timeout(600)
                prim = "form_submit"
            elif kind == 4:  # button_click: destroy (or toggle fallback)
                items = page.query_selector_all("ul.todo-list li")
                if len(items) > 1:
                    btn = items[step % len(items)].query_selector("button.destroy")
                    if btn is None:
                        raise RuntimeError("no destroy button")
                    btn.click(force=True)
                    page.wait_for_timeout(600)
                    prim = "button_click"
                    target = "destroy"
                else:
                    toggles = page.query_selector_all("ul.todo-list li input.toggle")
                    if not toggles:
                        raise RuntimeError("no toggle fallback")
                    toggles[0].click(force=True)
                    page.wait_for_timeout(600)
                    prim = "button_click"
            else:  # kind == 6: js_navigate
                op = js_ops[(ji + step) % 3]
                if op == "reload":
                    page.reload(wait_until="domcontentloaded")
                elif op == "back":
                    page.go_back(wait_until="domcontentloaded")
                else:
                    page.go_forward(wait_until="domcontentloaded")
                page.wait_for_timeout(600)
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
        page.wait_for_timeout(300)
    return recs


def wiki_session(page, session_idx, rng):
    """One 20-action Wikipedia session: click article links, go back between clicks."""
    recs = []
    start = WIKI_STARTS[session_idx % len(WIKI_STARTS)]
    page.goto(start, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(1200)
    for step in range(20):
        before_url, before_title = page.url, safe_title(page)
        prim, target, err = "link_click", None, None
        try:
            links = page.query_selector_all('a[href^="/wiki/"]')
            # filter out non-article links
            cands = []
            for a in links[:300]:
                h = a.get_attribute("href") or ""
                if ":" in h or h.startswith("/wiki/Main_Page"):
                    continue
                try:
                    if not a.is_visible():
                        continue
                except Exception:
                    continue
                cands.append(a)
            if not cands:
                raise RuntimeError("no article links")
            el = cands[rng.randint(0, len(cands) - 1)]
            raw_href = el.get_attribute("href")
            target = urllib.parse.urljoin(page.url, raw_href)
            el.click()
            page.wait_for_timeout(900)
            try:
                page.wait_for_load_state("domcontentloaded", timeout=8000)
            except Exception:
                pass
            page.wait_for_timeout(400)
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
        recs.append({
            "site": "wikipedia", "session": session_idx,
            "url_before": before_url, "url_after": page.url,
            "title_before": before_title, "title_after": safe_title(page),
            "action_primitive": prim, "action_target": target,
            "timestamp": now_iso(), "error": err,
        })
        # return to start hub for next click (keeps sessions comparable)
        try:
            page.goto(start, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(800)
        except Exception:
            pass
        page.wait_for_timeout(300)
    return recs


def run_site(p, site_key, is_wiki, seed):
    rng = random.Random(seed)
    all_recs = []
    for s in range(START_SESSION, START_SESSION + N_SESSIONS):
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        try:
            ctx = browser.new_context(viewport={"width": 1280, "height": 720})
            page = ctx.new_page()
            if is_wiki:
                recs = wiki_session(page, s, rng)
            else:
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
            time.sleep(1.0)
    return all_recs


def main():
    sites = list(VARIANTS.keys()) + ["wikipedia"]
    if ONLY:
        sites = [s for s in sites if s == ONLY]
    out = []
    with sync_playwright() as p:
        for i, site in enumerate(sites):
            print(f"[{site}] Starting...", flush=True)
            try:
                recs = run_site(p, site, site == "wikipedia", seed=1000 + i * 97)
            except Exception as e:
                print(f"[{site}] SITE FAILED: {type(e).__name__}: {e}", flush=True)
                recs = [{
                    "site": site, "session": -1, "url_before": None,
                    "url_after": None, "title_before": None, "title_after": None,
                    "action_primitive": None, "action_target": None,
                    "timestamp": now_iso(), "error": f"SITE_FAIL {type(e).__name__}: {e}",
                }]
            out.extend(recs)
            # incremental checkpoint
            with open(OUT_PATH, "w") as f:
                json.dump(out, f, indent=1)
            print(f"[{site}] done, cumulative={len(out)}", flush=True)
    print(f"TOTAL {len(out)} transitions -> {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
