"""SPIDER TEAM PHYSICS — random-walk transition collector.

Uniform-random policy over internal actionable elements (incl. typed form
interactions). Event-driven snapshots only. Output: JSONL transitions with
mechanics-only features + raw snapshot refs (raw kept in /tmp, not committed).
"""
import gzip, hashlib, json, os, random, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.browser import Session

import sys as _sys
OUT = ("/tmp/opencode/spider_data/wp003_" +
       (_sys.argv[_sys.argv.index("--site")+1] if "--site" in _sys.argv
        else "all") + ".jsonl")
RAW_DIR = "/tmp/opencode/spider_data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

WALKS = [
    {"site": "books",       "start": "https://books.toscrape.com/",            "n": 90},
    {"site": "quotes",      "start": "https://quotes.toscrape.com/",           "n": 90},
    {"site": "internet",    "start": "https://the-internet.herokuapp.com/",    "n": 90},
    {"site": "wikipedia",   "start": "https://en.wikipedia.org/wiki/Spider",   "n": 90,
     "allow_prefix": "/wiki/", "deny_prefixes": ("/wiki/Special:", "/wiki/File:",
        "/wiki/Talk", "/wiki/Help:", "/wiki/Portal:", "/wiki/Wikipedia:",
        "/wiki/Category:", "/wiki/Template", "/wiki/Main_Page")},
    {"site": "hackernews",  "start": "https://news.ycombinator.com/",          "n": 90},
    {"site": "gutenberg",   "start": "https://www.gutenberg.org/ebooks/bookshelf/1", "n": 90},
    {"site": "openlibrary", "start": "https://openlibrary.org/subjects/science","n": 90,
     "allow_host": True},
]

FILL_USER = ["spiderbot", "research@example.com"]
FILL_PASS = "notasecret-42"


def bucket_link(n): return 0 if n < 10 else (1 if n < 50 else 2)
def bucket3(n): return 0 if n == 0 else (1 if n <= 3 else 2)
def bucket_depth(path): return 0 if path.count("/") <= 1 else (1 if path.count("/") <= 3 else 2)
def bucket_q(n): return 0 if n == 0 else (1 if n == 1 else 2)


def features(snap):
    els = snap["elements"]
    from urllib.parse import urlsplit
    u = urlsplit(snap["url"])
    links = [e for e in els if e["tag"] == "a" and not e.get("ext")]
    ext_links = [e for e in els if e["tag"] == "a" and e.get("ext")]
    inputs = [e for e in els if e["tag"] == "input"]
    tot = max(1, len(els))
    return {
        "link_bucket": bucket_link(len(links)),
        "button_bucket": bucket3(sum(1 for e in els if e["tag"] == "button" or e["type"] == "submit")),
        "text_input_bucket": bucket3(sum(1 for e in inputs if e["type"] in ("", "text", "email"))),
        "has_password": int(any(e["type"] == "password" for e in inputs)),
        "has_select": int(any(e["tag"] == "select" for e in els)),
        "has_checkbox": int(any(e["type"] == "checkbox" for e in inputs)),
        "has_file": int(any(e["type"] == "file" for e in inputs)),
        "has_textarea": int(any(e["tag"] == "textarea" for e in els)),
        "form_bucket": bucket3(len(snap["forms"])),
        "depth_bucket": bucket_depth(u.path),
        "query_bucket": bucket_q(len(u.query.split("&")) if u.query else 0),
        "login_capable": int(any(f.get("fields") and
                                 any(x.get("ty") == "password" for x in f["fields"])
                                 for f in snap["forms"])),
        "internal_ratio_bucket": min(2, len(links) * 3 // tot),
        # NOTE: no text, no site id, no URL tokens (semantics ablated)
    }


def next_page_class(post_feat):
    return (post_feat["depth_bucket"], post_feat["has_password"],
            post_feat["link_bucket"], post_feat["text_input_bucket"])


def internal_ok(snap, el, cfg):
    if not el["enabled"]:
        return False
    if el["tag"] == "a":
        if el.get("ext"):
            return False
        href = el["href"] or ""
        if href in ("", "#"):
            return False
        ap = cfg.get("allow_prefix")
        if ap and not href.startswith(ap):
            return False
        for d in cfg.get("deny_prefixes", []):
            if href.startswith(d):
                return False
        return True
    return True


def choose_action(snap, rng, cfg):
    """Uniform-ish over classes; returns (kind, idx, value)."""
    els = snap["elements"]
    links = [e for e in els if internal_ok(snap, e, cfg) and e["tag"] == "a"]
    buttons = [e for e in els if e["enabled"] and
               (e["tag"] == "button" or e["type"] == "submit")]
    texts = [e for e in els if e["tag"] == "input" and
             e["type"] in ("", "text", "email") and e["enabled"]]
    passes = [e for e in els if e["tag"] == "input" and e["type"] == "password"]
    selects = [e for e in els if e["tag"] == "select" and e["enabled"]]
    boxes = [e for e in els if e["tag"] == "input" and e["type"] == "checkbox"]

    pool = ([("click_link", links)] if links else []) + \
           ([("click_button", buttons)] if buttons else []) + \
           ([("fill_text", texts)] if texts else []) + \
           ([("fill_password", passes)] if passes else []) + \
           ([("select_option", selects)] if selects else []) + \
           ([("check_box", boxes)] if boxes else [])
    if not pool:
        return ("none", [])
    kind, group = rng.choice(pool)
    el = rng.choice(group)
    val = ""
    if kind == "fill_text":
        val = rng.choice(FILL_USER) if "email" in el["type"] else "spider walk"
    elif kind == "fill_password":
        val = FILL_PASS
    # after filling a field, submit sometimes (generates form dynamics)
    if kind.startswith("fill") and buttons and rng.random() < 0.6:
        sub = rng.choice(buttons)
        return ("chain_submit", [(kind, el["i"], val), ("click_button", sub["i"], "")])
    return (kind, [(kind, el["i"], val)])


PRIM = {"click_link": "click", "click_button": "click",
        "fill_text": "fill", "fill_password": "fill",
        "select_option": "select", "check_box": "check"}


def store_raw(snap):
    h = hashlib.sha256(json.dumps(snap, sort_keys=True).encode()).hexdigest()[:20]
    with gzip.open(os.path.join(RAW_DIR, f"{h}.json.gz"), "wt") as f:
        json.dump(snap, f)
    return h


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=None)
    ap.add_argument("--seed", type=int, default=20260823)
    args = ap.parse_args()
    rng = random.Random(args.seed + (hash(args.site) % 1009 if args.site else 0))
    cfgs = [c for c in WALKS if args.site in (None, c["site"])]
    mode_w = "w" if args.site is None else "a"
    n_written = 0
    with open(OUT, mode_w) as out, Session(headless=True) as s:
      for cfg in cfgs:
        site = cfg["site"]
        print(f"[{site}] begin", flush=True)
        done = 0
        tries = 0
        try:
            cur = s.goto(cfg["start"], site)
        except Exception as e:
            print(f"[{site}] START FAIL {e}"); continue
        while done < cfg["n"] and tries < cfg["n"] * 6:
            tries += 1
            pre_feat = features(cur)
            choice = choose_action(cur, rng, cfg)
            chain = choice[1]
            if not chain or any(idx >= len(cur["elements"]) for _, idx, _ in chain):
                # dead state / stale indices: hop back to site start, no record
                try:
                    cur = s.goto(cfg["start"], site)
                except Exception:
                    pass
                continue
            acts = []
            ok_all = True
            t0 = time.time()
            post = cur
            for (kind, idx, val) in chain:
                el = dict(post["elements"][idx]) if idx < len(post["elements"]) else None
                if el is None:
                    ok_all = False; break
                a = {"kind": PRIM[kind], "target": idx, "value": val}
                post = s.act(post, a)
                acts.append({"label": kind,
                             "ok": bool(post["last_action"]["ok"]),
                             "error": post["last_action"].get("error", "")[:80]})
                if not acts[-1]["ok"]:
                    ok_all = False
                    break
            load_ms = int((time.time() - t0) * 1000)
            post_feat = features(post)
            rec = {
                "site": site, "pre": pre_feat, "post": post_feat,
                "page_class_pre": tuple(sorted(pre_feat.items())),
                "next_page_class": next_page_class(post_feat),
                "prev_action_label": acts[-1]["label"] if acts else "",
                "action_labels": [a["label"] for a in acts],
                "any_ok": ok_all,
                "primary_action": acts[0]["label"] if acts else "",
                "url_changed": post["url"] != cur["url"],
                "load_ms": load_ms,
                "ts": int(time.time()),
                "pre_raw": store_raw(cur), "post_raw": store_raw(post),
            }
            # primary target = first intended action of the chain
            rec["target_action"] = acts[0]["label"] if acts else "abandon"
            out.write(json.dumps(rec) + "\n")
            out.flush()
            done += 1; n_written += 1
            cur = post
            time.sleep(rng.uniform(0.25, 0.7))
        print(f"[{site}] transitions={done}", flush=True)
    print("TOTAL", n_written)


if __name__ == "__main__":
    main()
