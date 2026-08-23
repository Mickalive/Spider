"""SPIDER TEAM PHYSICS — audited transition collector.

Collect action-conditioned environment transitions on live sites. Every row
carries deterministic trajectory/step identity and a true previous-transition
action label. Raw observables stay in /tmp; derived compact rows are analyzed
downstream.
"""
import gzip, hashlib, json, os, random, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.browser import Session

OUTDIR = "/tmp/opencode/spider_data"
RAW_DIR = os.path.join(OUTDIR, "raw")
STEM = os.environ.get("OUTNAME", "wp003_transitions.jsonl").replace(".jsonl", "")
os.makedirs(RAW_DIR, exist_ok=True)

WALKS = [
    {"site": "books", "start": "https://books.toscrape.com/", "n": 90},
    {"site": "quotes", "start": "https://quotes.toscrape.com/", "n": 90},
    {"site": "internet", "start": "https://the-internet.herokuapp.com/", "n": 90},
    {"site": "wikipedia", "start": "https://en.wikipedia.org/wiki/Spider", "n": 90,
     "allow_prefix": "/wiki/", "deny_prefixes": ("/wiki/Special:", "/wiki/File:",
        "/wiki/Talk", "/wiki/Help:", "/wiki/Portal:", "/wiki/Wikipedia:",
        "/wiki/Category:", "/wiki/Template", "/wiki/Main_Page")},
    {"site": "hackernews", "start": "https://news.ycombinator.com/", "n": 90},
    {"site": "gutenberg", "start": "https://www.gutenberg.org/ebooks/bookshelf/1", "n": 90},
    {"site": "openlibrary", "start": "https://openlibrary.org/subjects/science", "n": 90,
     "allow_host": True},
]

FILL_USER = ["spiderbot", "research@example.com"]
FILL_PASS = "notasecret-42"
DEFAULT_TRAJECTORIES = 6


def stable_site_offset(site: str) -> int:
    """Stable across Python processes; do not use Python's salted hash()."""
    return int(hashlib.sha256(site.encode()).hexdigest()[:8], 16)


def bucket_link(n): return 0 if n < 10 else (1 if n < 50 else 2)
def counts_of(snap):
    """Raw element counts kept alongside buckets to allow legitimate
    alternative representations downstream (WP-003B-v2 prereg §9 S-B)."""
    els = snap["elements"]
    return {
        "links": sum(1 for e in els if e["tag"] == "a" and not e.get("ext")),
        "buttons": sum(1 for e in els if e["tag"] == "button" or e["type"] == "submit"),
        "text_inputs": sum(1 for e in els if e["tag"] == "input"
                           and e["type"] in ("", "text", "email")),
        "forms": len(snap["forms"]),
    }
def bucket3(n): return 0 if n == 0 else (1 if n <= 3 else 2)
def bucket_depth(path): return 0 if path.count("/") <= 1 else (1 if path.count("/") <= 3 else 2)
def bucket_q(n): return 0 if n == 0 else (1 if n == 1 else 2)


def features(snap):
    els = snap["elements"]
    from urllib.parse import urlsplit
    u = urlsplit(snap["url"])
    links = [e for e in els if e["tag"] == "a" and not e.get("ext")]
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
    """Uniform-ish over actionable classes; returns a primitive action chain."""
    els = snap["elements"]
    links = [e for e in els if internal_ok(snap, e, cfg) and e["tag"] == "a"]
    buttons = [e for e in els if e["enabled"] and
               (e["tag"] == "button" or e["type"] == "submit")]
    texts = [e for e in els if e["tag"] == "input" and
             e["type"] in ("", "text", "email") and e["enabled"]]
    passes = [e for e in els if e["tag"] == "input" and e["type"] == "password" and e["enabled"]]
    selects = [e for e in els if e["tag"] == "select" and e["enabled"]]
    boxes = [e for e in els if e["tag"] == "input" and e["type"] == "checkbox" and e["enabled"]]
    pool = ([("click_link", links)] if links else []) + \
           ([("click_button", buttons)] if buttons else []) + \
           ([("fill_text", texts)] if texts else []) + \
           ([("fill_password", passes)] if passes else []) + \
           ([("select_option", selects)] if selects else []) + \
           ([("check_box", boxes)] if boxes else [])
    if not pool:
        return []
    kind, group = rng.choice(pool)
    el = rng.choice(group)
    val = ""
    if kind == "fill_text":
        val = rng.choice(FILL_USER) if "email" in el["type"] else "spider walk"
    elif kind == "fill_password":
        val = FILL_PASS
    if kind.startswith("fill") and buttons and rng.random() < 0.6:
        sub = rng.choice(buttons)
        return [(kind, el["i"], val), ("click_button", sub["i"], "")]
    return [(kind, el["i"], val)]


PRIM = {"click_link": "click", "click_button": "click",
        "fill_text": "fill", "fill_password": "fill",
        "select_option": "select", "check_box": "check"}


def store_raw(snap):
    h = hashlib.sha256(json.dumps(snap, sort_keys=True).encode()).hexdigest()[:20]
    with gzip.open(os.path.join(RAW_DIR, f"{h}.json.gz"), "wt") as f:
        json.dump(snap, f)
    return h


def collect_trajectory(session, cfg, rng, out, trajectory_id, target_steps):
    site = cfg["site"]
    cur = session.goto(cfg["start"], site)
    prev_primary = "<START>"
    written = 0
    tries = 0
    while written < target_steps and tries < target_steps * 8:
        tries += 1
        pre_feat = features(cur)
        chain = choose_action(cur, rng, cfg)
        if not chain or any(idx >= len(cur["elements"]) for _, idx, _ in chain):
            break
        acts = []
        ok_all = True
        t0 = time.time()
        post = cur
        for kind, idx, val in chain:
            el = dict(post["elements"][idx]) if idx < len(post["elements"]) else None
            if el is None:
                ok_all = False
                break
            post = session.act(post, {"kind": PRIM[kind], "target": idx, "value": val})
            acts.append({"label": kind,
                         "ok": bool(post["last_action"]["ok"]),
                         "error": post["last_action"].get("error", "")[:80]})
            if not acts[-1]["ok"]:
                ok_all = False
                break
        if not acts:
            break
        post_feat = features(post)
        primary = acts[0]["label"]
        rec = {
            "site": site,
            "trajectory_id": trajectory_id,
            "step_id": written,
            "pre": pre_feat,
            "post": post_feat,
            "counts_pre": counts_of(cur),
            "counts_post": counts_of(post),
            "next_page_class": next_page_class(post_feat),
            "prev_action_label": prev_primary,
            "action_labels": [a["label"] for a in acts],
            "any_ok": ok_all,
            "primary_action": primary,
            "target_action": primary,
            "url_changed": post["url"] != cur["url"],
            "load_ms": int((time.time() - t0) * 1000),
            "ts": int(time.time()),
            "pre_raw": store_raw(cur),
            "post_raw": store_raw(post),
        }
        out.write(json.dumps(rec) + "\n")
        out.flush()
        written += 1
        prev_primary = primary
        cur = post
        time.sleep(rng.uniform(0.25, 0.7))
    return written


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=None)
    ap.add_argument("--seed", type=int, default=20260823)
    ap.add_argument("--trajectories", type=int, default=DEFAULT_TRAJECTORIES)
    args = ap.parse_args()
    cfgs = [c for c in WALKS if args.site in (None, c["site"])]
    total = 0
    with Session(headless=True) as session:
        for cfg in cfgs:
            site = cfg["site"]
            out_path = os.path.join(OUTDIR, f"{STEM}_{site}.jsonl")
            site_total = 0
            with open(out_path, "w") as out:
                ntraj = max(2, args.trajectories)
                base = cfg["n"] // ntraj
                rem = cfg["n"] % ntraj
                for j in range(ntraj):
                    target_steps = base + (1 if j < rem else 0)
                    seed = args.seed + stable_site_offset(site) + j * 10007
                    rng = random.Random(seed)
                    tid = f"{site}-seed{args.seed}-r{j:02d}"
                    try:
                        n = collect_trajectory(session, cfg, rng, out, tid, target_steps)
                    except Exception as e:
                        print(f"[{site}] {tid} failed: {type(e).__name__}: {e}", flush=True)
                        n = 0
                    site_total += n
            print(f"[{site}] transitions={site_total}", flush=True)
            total += site_total
    print("TOTAL", total)


if __name__ == "__main__":
    main()
