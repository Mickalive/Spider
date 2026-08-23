"""SPIDER shared instrumentation: Playwright driver + raw observation capture.

Used by both TEAM GRAPH (goal-directed exploration) and TEAM PHYSICS
(random-walk dynamics collection). Raw observables are preserved;
derived state is computed downstream, never here.
"""
import gzip, hashlib, json, time, random, os
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/tmp/opencode/ms-playwright")
from playwright.sync_api import sync_playwright

SNAPSHOT_JS = r"""
() => {
  const vis = el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  const cssPath = el => {
    const seg = [];
    while (el && el.nodeType === 1 && seg.length < 10) {
      let s = el.tagName.toLowerCase();
      if (el.id) { seg.unshift(s + '#' + CSS.escape(el.id)); break; }
      const sib = [...el.parentNode.children].filter(c => c.tagName === el.tagName);
      const ix = sib.indexOf(el) + 1;
      if (sib.length > 1) s += ':nth-of-type(' + ix + ')';
      seg.unshift(s);
      el = el.parentElement;
    }
    return seg.join('>');
  };
  const sel = 'a[href], button, input, select, textarea, [role="button"], [onclick]';
  const els = [];
  document.querySelectorAll(sel).forEach((el, i) => {
    let tag = el.tagName.toLowerCase();
    if (!vis(el)) return;
    const rect = el.getBoundingClientRect();
    let hrefAbs = ''; let ext = 0;
    if (tag === 'a') {
      try {
        const u = new URL(el.href, location.href);
        ext = (u.origin === location.origin) ? 0 : 1;
        hrefAbs = u.pathname.slice(0,180);
      } catch(e){}
    }
    els.push({
      i: els.length,
      tag,
      type: el.getAttribute('type') || '',
      role: el.getAttribute('role') || '',
      name: (el.getAttribute('name') || '').slice(0,40),
      aria: (el.getAttribute('aria-label') || '').slice(0,60),
      ph: (el.getAttribute('placeholder') || '').slice(0,40),
      text: ((el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') ? '' :
             ((el.innerText || '') + '').replace(/\s+/g,' ').trim().slice(0,80)),
      href: hrefAbs, ext,
      cls: (el.className && el.className.baseVal !== undefined ? '' : String(el.className)).split(/\s+/).filter(Boolean).slice(0,3).join(' '),
      xp: cssPath(el),
      x: Math.round(rect.x), y: Math.round(rect.y),
      enabled: !el.disabled
    });
    if (els.length >= 400) return;
  });
  const forms = [];
  document.querySelectorAll('form').forEach(f => {
    const fields = [...f.querySelectorAll('input,select,textarea')].map(x => ({
      t: x.tagName.toLowerCase(), ty: x.getAttribute('type') || '', n: (x.name||'').slice(0,30)
    }));
    forms.push({fields, method: (f.method||'get').toLowerCase(),
                action: (f.getAttribute('action')||'').slice(0,120)});
  });
  return {elements: els, forms,
          n_links: document.querySelectorAll('a[href]').length,
          page_text: (document.body ? document.body.innerText : '')
                     .replace(/\s+/g,' ').slice(0,4000)};
}
"""

def _url_shape(url: str) -> str:
    """Structural shape of URL with literal segments replaced by tokens."""
    from urllib.parse import urlsplit
    u = urlsplit(url)
    segs = ['*' if s and not s.replace('.', '').replace('-', '').isdigit() else '#'
            for s in u.path.split('/')]
    return f"{u.netloc}/{'/'.join(segs)}"

class Session:
    """One browser session; yields raw snapshots around performed actions."""

    def __init__(self, headless=True):
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch(headless=headless)
        self.page = self.browser.new_page(
            user_agent="SpiderResearchBot/0.1 (+autonomous-lab)",
            viewport={"width": 1280, "height": 800})
        self.net_log = []

    def close(self):
        try: self.browser.close()
        finally: self._pw.stop()

    def __enter__(self): return self
    def __exit__(self, *a): self.close()

    # ---------- observation ----------
    def snapshot(self, site: str, settle_ms=350) -> dict:
        time.sleep(settle_ms / 1000)
        p = self.page
        p.wait_for_load_state("domcontentloaded", timeout=20000)
        js = p.evaluate(SNAPSHOT_JS)
        html = p.content()
        h = hashlib.sha256(html.encode()).hexdigest()
        snap = {
            "ts_ms": int(time.time() * 1000),
            "site": site,
            "url": p.url,
            "title": (p.title() or "")[:120],
            "load_ms": None,
            "url_shape": _url_shape(p.url),
            "elements": js["elements"],
            "forms": js["forms"],
            "n_links": js["n_links"],
            "page_text": js.get("page_text", ""),
            "dom_sha256": h,
            "dom_bytes": len(html),
        }
        return snap

    def goto(self, url: str, site: str) -> dict:
        t0 = time.time()
        self.page.goto(url, timeout=30000, wait_until="domcontentloaded")
        s = self.snapshot(site)
        s["load_ms"] = int((time.time() - t0) * 1000)
        return s

    # ---------- primitive actions ----------
    def act(self, snap: dict, action: dict) -> dict:
        """Execute action against element index in snap. Returns post-snapshot."""
        kind = action["kind"]; idx = action.get("target")
        p = self.page
        ok, err = True, ""
        try:
            if kind == "goto":
                self.goto(action["value"], snap["site"])
                kind_out = "navigate"
            else:
                el = snap["elements"][idx]
                loc = self._locate(el)
                if kind == "click":
                    loc.click(timeout=8000)
                    p.wait_for_load_state("domcontentloaded", timeout=15000)
                elif kind == "fill":
                    loc.fill(str(action["value"]), timeout=8000)
                elif kind == "select":
                    loc.select_option(label=str(action["value"])) if action["value"] \
                        else loc.select_option(index=0)
                elif kind == "check":
                    loc.check(timeout=8000)
                elif kind == "press":
                    p.keyboard.press(action["value"])
                elif kind == "submit_enter":
                    loc.press("Enter", timeout=8000)
                    p.wait_for_load_state("domcontentloaded", timeout=15000)
                else:
                    raise ValueError(kind)
        except Exception as e:
            ok, err = False, f"{type(e).__name__}: {e}"[:160]
        post = self.snapshot(snap["site"]) if kind != "fill" and kind != "check" \
            else self.snapshot(snap["site"], settle_ms=80)
        post["last_action"] = {"kind": kind, **{k: v for k, v in action.items() if k != 'kind'},
                               "ok": ok, "error": err}
        return post

    def _locate(self, el: dict):
        p = self.page
        # primary: stable CSS path captured at snapshot time
        try:
            loc = p.locator(el["xp"]).first
            if loc.count():
                return loc
        except Exception:
            pass
        if el["name"]:
            try:
                loc = p.locator(f'{el["tag"]}[name="{el["name"]}"]').first
                if loc.count(): return loc
            except Exception: pass
        return p.locator(el["tag"]).first
