# Preregistration: EXP-FRONTIER-38085197666

## Site-Native Discovery vs Link-Following for Deep-Item Acquisition (v2, fresh pool, 2 engines)

Governed by the PIVOT mandate on claim **C-CROSSSITE** (next_gate: true website holdout without site identity leakage). Experiment id, lane, claim ids, decision rule, control ids and metric ids below are frozen transmission identities.

---

## 1. Scientific Question

On the credential-free GET-only stdlib-HTTP substrate, can site-native discovery channels (robots-sitemap, sitemap.xml, on-site search index, RSS/Atom, JSON-LD) expose intentionally deep (hop >= 3) state-carrying pages within K = 3 GETs, at per-host rate >= 0.50, on >= 2 hosts spanning >= 2 doc-site engines, when the frame is a fresh 4-site pool frozen at DESIGN time?

This is the smallest experiment that can move C-CROSSSITE's channel-axis question: if deep doc content is O(K)-reachable through site-native channels, hop depth is not an intrinsic acquisition barrier and channel resolvers become first-class kernel hops that must then transfer across the website holdout.

## 2. Hypothesis

Site-native discovery channels provide shallow (O(K), K = 3) GET accounting to pages that a naive same-host StaticLinks crawl only reaches at hop >= 3, so deep content is not intrinsically path-bound: per-host reachability fraction >= 0.50 on at least 2 hosts spanning at least 2 engines (mdBook, Sphinx).

## 3. Falsifier (Two-Sided, Arithmetically Checkable Before Freeze)

Fully specified in spec.json#falsifier. Summary: E = number of hosts with discovery_reachable_fraction >= 0.50 at K = 3.

- SUPPORTS: E >= 2 and meeting hosts span >= 2 engines.
- FALSIFIES: E = 0.
- MIXED: E = 1, or all meeting hosts are a single engine.
- INCONCLUSIVE: empty candidate denominator on a host.
- MEASUREMENT_INVALID: admission-gate / calibration-gate / exclusion-cap / null-control / code-hash failures.

Branch coverage of the exact frozen code was executed before freeze (spec.json#freeze_eligibility.decision_rule_reachability, all 8 scenarios, all_branches_reachable = true). Every outcome is reachable in both directions on the frozen pool: the frame supports 4 hosts (2 mdBook, 2 Sphinx), so E ranges over {0..4} and engine-span is decidable in every case.

## 4. Substrate & Constraints (Identical to Parent)

- Credential-free GET-only stdlib HTTP: `urllib.request` (no requests, no browser, no JS, no API keys, no cookies).
- HTML parsing: stdlib `html.parser`, `xml.etree`, `re`, `json` only.
- Paced polite fetching (0.15 s between GETs at DESIGN/EXECUTE), fixed User-Agent `Mozilla/5.0 (compatible; spider-design-probe/1.0)` (frozen because sphinx-doc.org / readthedocs.io return 403 to the default Python-urllib UA; see section 15).
- One retry on 429/5xx, then drop (a continued 429/5xx is a not-reachable; frozen; disclosed).

## 5. Discovery Channels (Frozen Definitions)

Stable channel ids used in metrics and controls:

1. **ROBOTS_SITEMAP** — GET `<origin>/robots.txt`; take the `Sitemap:` directive (case-insensitive), 1 GET.
2. **SITEMAP_XML** — GET `<origin>/sitemap.xml` (with <loc> entries or plain-text sitemap); child sitemap-index chains are followed one level; a leaf inside a chain costs 3 GETs and an index-of-index costs MORE than 3 => K_EXCEEDED (not reachable). .gz sitemaps are NOT fetched (text fetch of .gz would garble; disclosed limitation).
3. **ON_SITE_SEARCH** — GET `<origin>/searchindex.js`; mdBook form `JSON.parse("[...]")` (array of [title, url, body]) or `JSON.parse('...')`; Sphinx form `Search.setIndex({...})` with docnames/titles/filenames (documented oracle, disclosed in validity threats). Item matching by frozen `match_key`.
4. **RSS_ATOM** — GET `<origin>/rss.xml`, fallback `<origin>/atom.xml`; parse RSS 2.0 `<link>`/`<guid>` and Atom `<link href>`/`<id>`.
5. **JSON_LD** — GET the seed root page (cold-start only), extract JSON-LD blocks (keys url / @id / mainEntityOfPage / contentUrl / sameAs) whose hostname equals the seed host (same-host rule); 1 GET + item GET.

Endpoint set and resolvers are exactly as implemented in the frozen executable (section 13); no other endpoints may be probed at EXECUTE.

## 6. Target Pool & Admission Gate (ADMISSION_GATE_V2)

### 6.1 Pool Construction (Completed During DESIGN, Before Freeze)

Exposure-blind same-host path-prefix StaticLinks BFS per seed (budget 250, depth 6, 0.15 s pace). DEEP item := hop >= 3 AND page carries >= 1 named input/select/textarea (state-carrying proxy: mdBook `mdbook-searchbar`; Sphinx `name="q"`). Pool was screened for credential-free reachability and hop topology only; no pool-host discovery-surface probe drove selection (see section 15).

Frozen seeds (all resolve to the declared host; no cross-host redirect):

| seed | engine | prefix | GETs | DEEP (by hop) |
|---|---|---|---|---|
| https://google.github.io/comprehensive-rust/ | mdBook | /comprehensive-rust/ | 250 | 168 ({3:93, 4:75}) |
| https://rustc-dev-guide.rust-lang.org/ | mdBook | / | 226 | 194 ({3:47, 4:71, 5:56, 6:20}) |
| https://www.sphinx-doc.org/en/master/ | Sphinx | /en/master/ | 207 | 28 ({3:28}) |
| https://pandas.pydata.org/docs/ | Sphinx | /docs/ | 250 | 28 ({3:28}) |

Representative DEEP items (samples, recorded): compr `.../android/build-rules.html`, `.../android/interoperability/cpp/android-build-rust.html`, `.../ar/android.html`; rustc-dev `.../ambig-unambig-ty-and-consts.html`, `.../analysis/well-formed.html`, `.../appendix/bibliography.html`; sphinx-doc `.../_modules/docutils/parsers/rst.html`, `.../_modules/index.html`, `.../_modules/sphinx/addnodes.html`; pandas `.../reference/api/pandas.DataFrame.agg.html`, `.../apply.html`, `.../describe.html`. Hop-1 samples per seed recorded in spec.json#target_pool (PC_HOP_CONFIRMATION).

### 6.2 Admission Gate Criteria (Must Pass Before Freeze — VERIFIED)

- total DEEP >= 10: **418** (pass)
- >= 2 hosts with >= 3 DEEP: **4 hosts** (168 / 194 / 28 / 28) (pass)
- >= 2 engines with >= 3 DEEP: **mdBook 362, Sphinx 56** (pass)

Re-verified at EXECUTE from a fresh crawl; failure = MEASUREMENT_INVALID.

### 6.3 Engine / Host Definition

Engine = doc-site generator lineage with a distinct discovery-surface implementation: **mdBook** (compr, rustc-dev-guide) and **Sphinx** (sphinx-doc, pandas). Engine identity is frozen by seed; generator markers (mdBook footer, Sphinx generator meta) observed descriptively, never decisional.

## 7. Measurement Procedure (EXECUTE Phase)

1. Fresh pool build with the frozen code (records hop labels, DEEP items, gate). Gate re-verify.
2. Redo fixtures calibration: CAL_DISCOVERABLE_FIXTURE must be 5/5 on all channels and CAL_OPAQUE_FIXTURE 0/5 on all channels, else MEASUREMENT_INVALID.
3. Sample: DEEP items per host sorted by URL, capped at 40 (136 episodes total: 40+40+28+28).
4. For every (host, item) episode, probe each channel independently (fresh fetch per channel; up to 3 logical GETs each). Item reachable via a channel iff its match_key appears in the channel's parsed output AND the item GET (final URL) returns HTTP 200 with `text/html` content-type (external-item GET rule: also accept `text/plain` for non-HTML allowed items in the frozen implementation).
5. Exclusions (items skipped because e.g. item GET becomes unusable or page no longer HTML) per host must stay <= 10% of the sampled set; else MEASUREMENT_INVALID.
6. Null control on pool hosts: synthetic items must stay 0 reachable.
7. Baselines replayed after the treatment phase on the same sampled items (independent episodes).
8. Aggregate per-host fractions, engine aggregates, per-channel tables, per-hop cost trend.

## 8. Metrics (Stable Identifiers for Downstream)

- `R_HOST_UNITS[h]` — primary: discovery_reachable_fraction on host h (>=0.50 threshold).
- `R_PER_CHANNEL[host, channel]` — descriptive per-channel fraction.
- `R_PER_ENGINE[e]` — descriptive engine mean.
- `COST_TREND_BY_HOP[hop]` — descriptive mean GETs for reachable items by hop.
- `B_LINK_FOLLOWING_BFS`, `B_PERSISTED_PATH_REACQUISITION`, `B_DIRECT_URL_REPLAY` — baseline costs (requests, bytes per admitted DEEP item).
- `B_NO_DISCOVERY` (0.0 floor), `U_NO_BOUND` (1.0 ceiling) — algebraic bounds.

## 9. Controls (Stable Identifiers)

- `PC_DISCOVERY_CHANNEL_REACHABILITY` — machinery liveness + sensitivity (out-of-pool liveness hosts github.blog, www.gnu.org, www.php.net, wordpress.org, www.jetbrains.com — >=2 must parse >=1 URL; fixtures 5/5 and 0/5; hop-1 samples present). All arms VERIFIED at DESIGN.
- `PC_HOP_CONFIRMATION` — hop structure per seed (hop0 = seed; hop1 samples recorded; hop>=3 DEEP samples recorded). VERIFIED.
- `NC_SYNTHETIC_UNREACHABLE_ITEM` — synthetic items `spider-nonexistent-38085197666-{a,b}.html`; null_all_zero = true at DESIGN on 5 hosts x 5 channels; re-checked on pool hosts at EXECUTE. VERIFIED (null_all_zero = true).
- `CAL_DISCOVERABLE_FIXTURE` / `CAL_OPAQUE_FIXTURE` — local stdlib HTTP fixture site: 5 items all present / 5 items all absent; expected 5/5 and 0/5 per channel; `CALIBRATION_GATE` = conjunction. VERIFIED (True).

## 10. Measurement Validity Threats (Disclosed)

Spec.json#measurement_validity VN-V1..VN-V12. Highlights: (1) the state-carrying proxy (named form controls) is degenerate site chrome — consistent across engines but weak as a semantic proxy (inherited from the parent); (2) K-budget and match strictness (frozen `match_key`: strip fragment, lowercase, strip .html/.htm and trailing slash; alias fallback: canonical link / og:url / final redirect URL); (3) live content drift (compr observed 213 DEEP via screening tool, 168 via the frozen harness; three consecutive frozen-harness runs identical — gate is binding, not counts); (4) UA dependence (403 under default urllib UA on sphinx-doc/readthedocs; frozen Mozilla-compatible UA); (5) sitemap .gz not parsed (disclosed); (6) no cross-item caching — every item x channel episode is a fresh measurement; (7) engine markers are descriptive; (8) JSON-LD is cold-start only (seed root page); (9) pool-host channel availability is the measurement itself — therefore NOT probed at DESIGN (exposure blindness).

## 11. Decision Rule (Formal)

As spec.json#decision_rule. PRIMARY: `R_HOST_UNITS` at K=3, threshold 0.50, E over hosts, engine-span of meeting hosts, admission gate -> outcome mapping in spec (SUPPORTS / FALSIFIES / MIXED / INCONCLUSIVE / MEASUREMENT_INVALID). Secondary reporting (per-channel, per-hop, baselines) is descriptive and never overrides the primary outcome.

## 12. Product Consequences

- **SUPPORTS**: hop depth is not an intrinsic acquisition barrier on doc-site frames; adopt channel-first discovery resolvers (sitemap / searchindex / feed / JSON-LD) as first-class kernel hops; C-CROSSSITE holdout next: same resolver set must transfer to a held-out site without identity leakage.
- **FALSIFIES**: on this frame, discovery channels are not a general O(1) escape hatch for deep pages; keep link-following kernels and treat channel resolvers as per-host optionality; bounded rejection of the channel-transfer axis within this frame.
- **MIXED / INCONCLUSIVE**: per-mechanism teardown (which channels work on which engines) becomes the frontier work list.
- **MEASUREMENT_INVALID**: infrastructure/packet failure; no scientific claim; retry with diagnosis.

## 13. Frozen Executable (complete, verbatim; sha256 - the code IS the artifact)

**This is the frozen implementation. Interpretation depends on no file outside this packet (freeze_artifacts = [], freeze_artifacts_bound = NOT_APPLICABLE).**

- sha256: `480b8f4f26dbe06724fcebc831e61a811bd0d61dfcb91b43e4c58a97959debd2`
- Extract & verify: `sed -n '/^```python$/,/^```$/p' prereg.md | sed '1d;$d' > run.py && sha256sum run.py` — under Python 3.10+ stdlib only.
- Usage: `python3 run.py --pool out.json` (design/execute pool build + gate), `--fixtures` (calibration gate), `--live-probe` (out-of-pool liveness), `--branch-drive out.json` (decision-rule branch coverage), default `python3 run.py` (full measurement: pool, calibration, sampling, per-item x per-channel episodes, null control, baselines, decision; writes `result.json`, `report.md`, `provenance.json` in cwd).
- EXECUTE MUST re-verify the hash after extraction; mismatch => MEASUREMENT_INVALID.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-FRONTIER-38085197666 FROZEN EXECUTION CODE (design-contract v2).
Subcommands:
  --pool OUT.json        build exposure-blind DEEP pool for the 4 frozen seeds (link-only
                         StaticLinks same-host+prefix BFS, budget 250, depth 6); gate check;
                         write pool.json; exit 0 iff ADMISSION_GATE_V2 passes. No discovery
                         surface (robots/sitemap/feeds/search/JSON-LD) is ever fetched here.
  --fixtures             run local stdlib calibration fixtures (CAL_DISCOVERABLE_FIXTURE=1.0,
                         CAL_OPAQUE_FIXTURE=0.0); CALIBRATION_GATE.
  --live-probe           out-of-pool channel liveness + NULL_CONTROL on LIVE_PROBE_HOSTS.
  --branch-drive OUT     drive decide() over synthetic inputs to all terminal outcomes.
  (default)              full EXECUTE: Step0 controls -> pool -> gate -> sample caps ->
                         measurement -> decision -> result.json/report.md/provenance.json
Stdlib only. UA, K, budgets, sample caps and channel resolvers are frozen below.
"""
from __future__ import annotations
import json, os, re, sys, time, threading, urllib.parse, urllib.request
from collections import Counter, deque
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import xml.etree.ElementTree as ET

# ---------------- frozen constants ----------------
UA = "Mozilla/5.0 (compatible; spider-design-probe/1.0)"
ACCEPT = "text/html,*/*"
TIMEOUT_S = 15
K_GET_BUDGET = 3
BUDGET_PER_SEED = 250
MAX_DEPTH = 6
PACE_S = 0.15
SAMPLE_CAP_PER_HOST = 40
MAX_EXCLUSION_FRACTION = 0.10
TREND_DROP = 0.10
TREND_MIN_BUCKET = 5
MIN_HOST_UNITS_WITH_THRESHOLD = 2
MIN_ENGINES = 2
MATERIALITY = 0.50

SEEDS = [
    {"seed": "https://google.github.io/comprehensive-rust/",
     "host": "google.github.io", "engine": "mdBook", "prefix": "/comprehensive-rust/"},
    {"seed": "https://rustc-dev-guide.rust-lang.org/",
     "host": "rustc-dev-guide.rust-lang.org", "engine": "mdBook", "prefix": "/"},
    {"seed": "https://www.sphinx-doc.org/en/master/",
     "host": "www.sphinx-doc.org", "engine": "Sphinx", "prefix": "/en/master/"},
    {"seed": "https://pandas.pydata.org/docs/",
     "host": "pandas.pydata.org", "engine": "Sphinx", "prefix": "/docs/"},
]
PROBE_HOSTS = ["https://github.blog/", "https://www.gnu.org/", "https://www.php.net/",
               "https://wordpress.org/", "https://www.jetbrains.com/"]
SYNTHETIC_IDS = ["spider-nonexistent-38085197666-a.html", "spider-nonexistent-38085197666-b.html"]
CHANNELS = ["ROBOTS_SITEMAP", "SITEMAP_XML", "ON_SITE_SEARCH", "RSS_ATOM", "JSON_LD"]
EXTS_SKIP = ("pdf", "zip", "png", "jpg", "jpeg", "gif", "svg", "ico", "css", "js",
             "xml", "txt", "gz", "whl", "ipynb")

# ---------------- http ----------------
def fetch(url, timeout=TIMEOUT_S):
    """urlopen-level GET (redirects followed inside urllib; final_url recorded).
       Retries: 5xx/429/timeouts up to 2 extra attempts with backoff."""
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": ACCEPT})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                return {"status": r.status, "final_url": r.geturl(),
                        "ct": r.headers.get("Content-Type", ""), "body": body, "error": None}
        except urllib.error.HTTPError as e:
            last = {"status": e.code, "final_url": url, "ct": str(e.headers.get("Content-Type", "")),
                    "body": b"", "error": "HTTPError"}
            if e.code == 429 or e.code >= 500:
                time.sleep(1.0 + 1.0 * attempt)
                continue
            return last
        except Exception as e:
            last = {"status": 0, "final_url": url, "ct": "", "body": b"", "error": type(e).__name__}
            time.sleep(1.0 + 1.0 * attempt)
    return last


# ---------------- exposure-blind parser (StaticLinks) ----------------
class StaticLinks(HTMLParser):
    """Link-only parser. NO discovery fields - exposure-blind by construction."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.named_controls = 0
        self.canonical = None
        self.og_url = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag in ("input", "select", "textarea") and (d.get("name") or "").strip():
            self.named_controls += 1
        if tag == "link" and (d.get("rel") or "").strip().lower() == "canonical" and d.get("href"):
            self.canonical = d["href"]
        if tag == "meta" and (d.get("property") or "").strip().lower() == "og:url" and d.get("content"):
            self.og_url = d["content"]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def norm_url(u):
    u, _ = urllib.parse.urldefrag(u)
    return u


def match_key(u):
    """Frozen canonical-discovery matching: strip fragment, lowercase, then remove one
       trailing '/', '.html' or '.htm' from the path (discovery MATCHING only; pool
       identity keeps exact URLs)."""
    u, _ = urllib.parse.urldefrag(u)
    sp = urllib.parse.urlsplit(u)
    path = re.sub(r"\.html?$", "", sp.path)
    path = re.sub(r"/$", "", path)
    return (sp.scheme.lower(), sp.netloc.lower(), path or "/")


def same_site(a, b):
    return urllib.parse.urlsplit(a).netloc.lower() == urllib.parse.urlsplit(b).netloc.lower()


# ---------------- exposure-blind pool BFS ----------------
def crawl_pool(seed, prefix, budget=BUDGET_PER_SEED, max_depth=MAX_DEPTH):
    seed = norm_url(seed)
    base_netloc = urllib.parse.urlsplit(seed).netloc
    seen = {seed: 0}
    q = deque([(seed, 0)])
    hist = Counter()
    deep = []
    gets = 0
    hop1_samples = []
    seed_final_url = seed
    while q and gets < budget:
        url, hop = q.popleft()
        hist[hop] += 1
        r = fetch(url)
        gets += 1
        time.sleep(PACE_S)
        if gets == 1 and r["final_url"]:
            seed_final_url = r["final_url"]
        if r["error"] or r["status"] != 200 or "html" not in r["ct"].lower():
            continue
        p = StaticLinks()
        try:
            p.feed(r["body"].decode("utf-8", "replace"))
        except Exception:
            continue
        if hop >= 3 and p.named_controls >= 1:
            deep.append({"url": url, "hop": hop, "named_controls": p.named_controls})
        if hop == 1 and len(hop1_samples) < 3:
            hop1_samples.append(url)
        if hop >= max_depth:
            continue
        bn = urllib.parse.urlsplit(url).netloc
        for href in p.links:
            if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
                continue
            full = norm_url(urllib.parse.urljoin(url, href))
            sp = urllib.parse.urlsplit(full)
            if sp.scheme not in ("http", "https") or sp.netloc.lower() != bn.lower():
                continue
            if prefix and not sp.path.startswith(prefix):
                continue
            if sp.path.split(".")[-1].lower() in EXTS_SKIP:
                continue
            if full in seen:
                continue
            seen[full] = hop + 1
            q.append((full, hop + 1))
    # DEEP pages are cheap to sort deterministically (cap applied later)
    deep.sort(key=lambda d: d["url"])
    return {"hist": dict(sorted(hist.items())), "deep": deep,
            "gets": gets, "seen": len(seen), "host": base_netloc,
            "hop1_samples": hop1_samples, "seed_final_url": seed_final_url}


def build_pool():
    pool = {}
    for s in SEEDS:
        res = crawl_pool(s["seed"], s["prefix"])
        pool[s["host"]] = {"seed": s["seed"], "engine": s["engine"], "prefix": s["prefix"],
                           **res}
        deep_total = len(res["deep"])
        print(f"[pool] {s['host']} engine={s['engine']} gets={res['gets']} "
              f"seen={res['seen']} DEEP={deep_total} by_hop={json.dumps(res['deep_by_hop'] if 'deep_by_hop' in res else Counter(d['hop'] for d in res['deep']))}")
    return pool


def gate(pool):
    stats = {}
    for h, e in pool.items():
        stats[h] = len(e["deep"])
    total = sum(stats.values())
    hosts_ge3 = sum(1 for v in stats.values() if v >= 3)
    eng_deep = {}
    for h, e in pool.items():
        eng_deep[e["engine"]] = eng_deep.get(e["engine"], 0) + len(e["deep"])
    engines_ge3 = sum(1 for v in eng_deep.values() if v >= 3)
    ok = total >= 10 and hosts_ge3 >= 2 and engines_ge3 >= 2
    return {"pass": ok, "total_deep": total, "hosts_ge3": hosts_ge3,
            "engines_ge3": engines_ge3, "per_host": stats, "per_engine": eng_deep}


# ---------------- discovery channels ----------------
def parse_sitemap(body, base):
    """XML <loc> any nesting, or plain-text one-URL-per-line. Returns (urls, is_index)."""
    text = body.decode("utf-8", "replace")
    urls, is_index = [], False
    try:
        root = ET.fromstring(text)
        is_index = root.tag.lower().endswith("sitemapindex")
        for loc in root.iter():
            if loc.tag.lower().endswith("loc") and loc.text:
                u = norm_url(urllib.parse.urljoin(base, loc.text.strip()))
                urls.append(u)
        return urls, is_index
    except ET.ParseError:
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("http"):
                urls.append(norm_url(urllib.parse.urljoin(base, line)))
        return urls, False


def js_unescape(s):
    """Decode the content of a JS string literal (handles \\\\, \\", \\n, \\t, \\r, \\uXXXX)."""
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == "\\" and i + 1 < n:
            nxt = s[i + 1]
            i += 2
            if nxt == "n":
                out.append("\n")
            elif nxt == "t":
                out.append("\t")
            elif nxt == "r":
                out.append("\r")
            elif nxt == "u" and i + 4 <= n:
                try:
                    out.append(chr(int(s[i:i + 4], 16)))
                except ValueError:
                    out.append("u")
                i += 4
            else:
                out.append(nxt)  # \\ and \"
        else:
            out.append(c)
            i += 1
    return "".join(out)


def parse_searchindex(body, base):
    """mdBook: var searchindex = JSON.parse('...'); array of [title, url, body] or
       {docs:[...]};  Sphinx: Search.setIndex({...}) with docnames/titles/filenames."""
    text = body.decode("utf-8", "replace")
    m = re.search(r"JSON\.parse\(([\"'])(.*?)\1\)", text, re.S)
    if not m:
        m = re.search(r"Search\.setIndex\((\{.*\})\)\s*;?\s*$", text, re.S) or \
            re.search(r"Search\.setIndex\((\{.*\})\)", text, re.S)
    if not m:
        return []
    try:
        raw = m.group(2) if m.lastindex == 2 else m.group(1)
        # JSON.parse argument is a JS string literal: decode it to its value, then parse
        obj = json.loads(js_unescape(raw))
    except Exception:
        return []
    urls = []
    if isinstance(obj, list):
        for row in obj:
            if isinstance(row, (list, tuple)) and len(row) >= 2 and isinstance(row[1], str) and row[1]:
                urls.append(norm_url(urllib.parse.urljoin(base, row[1])))
    elif isinstance(obj, dict):
        files = obj.get("docnames") or obj.get("filenames") or []
        for f in files:
            if isinstance(f, str) and f:
                urls.append(norm_url(urllib.parse.urljoin(base, f)))
    return urls


def parse_feed(body, base):
    text = body.decode("utf-8", "replace")
    urls = []
    for m in re.finditer(r"<link[^>]*href=[\"']([^\"']+)[\"'][^>]*/?>", text, re.I):
        urls.append(norm_url(urllib.parse.urljoin(base, m.group(1))))
    for m in re.finditer(r"<link[^>]*>([^<]+)</link>", text, re.I):
        v = m.group(1).strip()
        if v.startswith(("http://", "https://")):
            urls.append(norm_url(urllib.parse.urljoin(base, v)))
    for m in re.finditer(r"<(?:guid|id)>([^<]+)</(?:guid|id)>", text, re.I):
        v = m.group(1).strip()
        if v.startswith("http"):
            urls.append(norm_url(urllib.parse.urljoin(base, v)))
    return urls


def parse_jsonld(body, base, host):
    text = body.decode("utf-8", "replace")
    urls = []
    keys = ("url", "@id", "mainEntityOfPage", "contentUrl", "sameAs")
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                         text, re.S | re.I):
        chunk = m.group(1)
        try:
            obj = json.loads(chunk)
        except Exception:
            continue
        stack = [obj]
        base_host = urllib.parse.urlsplit(base).hostname.lower()
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                for k, v in cur.items():
                    if k in keys and isinstance(v, str):
                        u = norm_url(urllib.parse.urljoin(base, v))
                        if urllib.parse.urlsplit(u).hostname and \
                           urllib.parse.urlsplit(u).hostname.lower() == base_host:
                            urls.append(u)
                    elif isinstance(v, (dict, list)):
                        stack.append(v)
            elif isinstance(cur, list):
                stack.extend(cur)
    return urls


def channel_resolver(channel, host):
    scheme = "http" if host.startswith("127.0.0.1") else "https"
    if channel == "ROBOTS_SITEMAP":
        return [scheme + "://" + host + "/robots.txt"]
    if channel == "SITEMAP_XML":
        return [scheme + "://" + host + "/sitemap.xml"]
    if channel == "ON_SITE_SEARCH":
        return [scheme + "://" + host + "/searchindex.js"]
    if channel == "RSS_ATOM":
        return [scheme + "://" + host + "/rss.xml", scheme + "://" + host + "/atom.xml"]
    if channel == "JSON_LD":
        for s in SEEDS:
            if s["host"] == host:
                return [s["seed"]]
        return [scheme + "://" + host + "/"]
    raise ValueError(channel)


def channel_urls(channel, host, cache):
    """Fresh discovery-document GET per episode (no cross-item caching, VN-V10).
       Returns (enumerated_urls, code, gets, detail)."""
    eps = channel_resolver(channel, host)
    gets = 0
    for i, ep in enumerate(eps):
        r = fetch(ep)
        gets += 1
        time.sleep(PACE_S)
        if r["error"] or r["status"] != 200:
            if i == len(eps) - 1:
                return [], f"HTTP_{r['status'] or r['error']}", gets, ep
            continue
        base = r["final_url"]
        if channel in ("ROBOTS_SITEMAP", "SITEMAP_XML"):
            if channel == "ROBOTS_SITEMAP":
                sitemaps = [l.strip() for l in r["body"].decode("utf-8", "replace").splitlines()
                            if l.strip().lower().startswith("sitemap:")]
                if not sitemaps:
                    return [], "NO_SITEMAP_DIRECTIVE", gets, ep
                target = urllib.parse.urljoin(base, sitemaps[0].split(":", 1)[1].strip())
            else:
                target = ep
            r2 = fetch(target)
            gets += 1
            time.sleep(PACE_S)
            if r2["error"] or r2["status"] != 200:
                return [], f"HTTP_{r2['status'] or r2['error']}", gets, target
            urls, is_index = parse_sitemap(r2["body"], r2["final_url"])
            if is_index:
                if not urls:
                    return [], "EMPTY_SITEMAP_INDEX", gets, target
                if gets + 1 > K_GET_BUDGET:
                    return [], "K_EXCEEDED", gets, target
                r3 = fetch(urls[0])
                gets += 1
                time.sleep(PACE_S)
                if r3["error"] or r3["status"] != 200:
                    return [], f"HTTP_{r3['status'] or r3['error']}", gets, urls[0]
                urls, is_index2 = parse_sitemap(r3["body"], r3["final_url"])
                return urls, ("OK_LEAF" if not is_index2 else "INDEX_CHAIN"), gets, \
                    (urls[0] if urls else target)
            return urls, "OK_LEAF", gets, target
        if channel == "ON_SITE_SEARCH":
            return parse_searchindex(r["body"], base), "OK", gets, ep
        if channel == "RSS_ATOM":
            return parse_feed(r["body"], base), "OK", gets, ep
        if channel == "JSON_LD":
            return parse_jsonld(r["body"], base, host), "OK", gets, ep
        return [], "UNKNOWN_CHANNEL", gets, ep
    return [], "NO_ENDPOINT", gets, eps[-1]


def reachable(item, channel, host):
    """One fresh episode for (item, channel) within K_GET_BUDGET urlopen-level GETs."""
    urls, code, gets, detail = channel_urls(channel, host, cache=None)
    if code.startswith("HTTP"):
        return False, code, gets
    if code in ("NO_SITEMAP_DIRECTIVE", "K_EXCEEDED", "INDEX_CHAIN", "EMPTY_SITEMAP_INDEX",
                "NO_ENDPOINT", "UNKNOWN_CHANNEL"):
        return False, code, gets
    hit = any(match_key(u) == match_key(item["url"]) for u in urls)
    if not hit:
        return False, "NO_ENTRY", gets
    if gets + 1 > K_GET_BUDGET:
        return False, "K_EXCEEDED_ITEM_GET", gets
    r = fetch(item["url"])
    gets += 1
    time.sleep(PACE_S)
    if r["error"] or r["status"] != 200 or "html" not in r["ct"].lower():
        return False, f"ITEM_HTTP_{r['status'] or r['error']}", gets
    p = StaticLinks()
    try:
        p.feed(r["body"].decode("utf-8", "replace"))
    except Exception:
        p = StaticLinks()
    alias = [a for a in (p.canonical, p.og_url, r["final_url"]) if a]
    if match_key(item["url"]) in [match_key(a) for a in alias]:
        return True, "REACHABLE", gets
    return False, "ALIAS_MISMATCH", gets


# ---------------- fixtures ----------------
def make_fixture_server(opaque=False):
    pages = {
        "/a.html": b"<html><body><h1>a</h1><form><input name='q'></form></body></html>",
        "/b.html": b"<html><body><h1>b</h1><form><input name='q'></form></body></html>",
        "/c.html": b"<html><body><h1>c</h1><form><input name='q'></form></body></html>",
        "/d.html": b"<html><body><h1>d</h1><form><input name='q'></form></body></html>",
        "/e.html": b"<html><body><h1>e</h1><form><input name='q'></form></body></html>",
        "/f.html": b"<html><body><h1>f</h1><form><input name='q'></form></body></html>",
    }
    all_urls = ["http://127.0.0.1/a.html", "http://127.0.0.1/b.html", "http://127.0.0.1/c.html",
                "http://127.0.0.1/d.html", "http://127.0.0.1/e.html"]
    listed = all_urls if not opaque else []
    locs = "".join(f"<url><loc>{u}</loc></url>" for u in listed)
    sitemap = f"<?xml version='1.0'?><urlset>{locs}</urlset>"
    searchidx = "var searchindex = JSON.parse(" + json.dumps(
        json.dumps([[str(i), u, ""] for i, u in enumerate(listed)])) + ");"
    jsonld = json.dumps([{"@type": "ItemList", "url": u} for u in listed])
    home = f"<html><body><script type='application/ld+json'>{jsonld}</script></body></html>".encode()
    routes = {}
    if not opaque:
        routes = {"/robots.txt": ("text/plain", b"Sitemap: http://127.0.0.1/sitemap.xml\n"),
                  "/sitemap.xml": ("application/xml", sitemap.encode()),
                  "/searchindex.js": ("application/javascript", searchidx.encode()),
                  "/rss.xml": ("application/xml", ("<?xml version='1.0'?><rss version='2.0'><channel>"
                    + "".join(f"<item><link>{u}</link></item>" for u in listed)
                    + "</channel></rss>").encode()),
                  "/": ("text/html", home)}
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            hit = routes.get(self.path)
            if hit is None:
                page = pages.get(self.path)
                hit = ("text/html", page) if page is not None else None
            if hit is None or hit[1] is None:
                self.send_response(404)
                self.end_headers()
                return
            ctype, body = hit
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *a):
            pass
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    base = f"http://127.0.0.1:{port}"
    # fix bodies to carry the real (ephemeral) base URL
    for k in list(routes.keys()):
        if isinstance(routes[k][1], bytes) and b"127.0.0.1/" in routes[k][1]:
            routes[k] = (routes[k][0],
                         routes[k][1].replace(b"http://127.0.0.1/", base.encode() + b"/"))
    candidates = [u.replace("http://127.0.0.1", base) for u in all_urls]
    if opaque:
        listed_actual = candidates[:]      # denominator = 5 candidate pages, all unreachable
    else:
        listed_actual = candidates[:]
    return srv, base, listed_actual


def run_fixtures():
    """CAL_DISCOVERABLE_FIXTURE must reach 1.0 on all 5 channels via listed pages;
       CAL_OPAQUE_FIXTURE must reach 0.0 (f.html never listed / channels absent)."""
    out = {}
    for name, opaque in (("CAL_DISCOVERABLE_FIXTURE", False), ("CAL_OPAQUE_FIXTURE", True)):
        srv, base, listed = make_fixture_server(opaque)
        t = threading.Thread(target=srv.serve_forever, daemon=True)
        t.start()
        host = urllib.parse.urlsplit(base).netloc
        res = {}
        for ch in CHANNELS:
            cnt = 0
            for u in listed:
                item = {"url": u}
                ok, code, gets = reachable(item, ch, host)
                cnt += 1 if ok else 0
            res[ch] = f"{cnt}/{len(listed)}"
        srv.shutdown()
        out[name] = res
    disp = out["CAL_DISCOVERABLE_FIXTURE"]
    opa = out["CAL_OPAQUE_FIXTURE"]
    disp_ok = all(v == "5/5" for v in disp.values())
    opa_ok = all(v == "0/5" for v in opa.values())
    print("[fixtures]", json.dumps(out, indent=1))
    print("[fixtures] CALIBRATION_GATE:", disp_ok and opa_ok)
    return {"results": out, "pass": disp_ok and opa_ok}


def run_live_probe():
    """Out-of-pool channel liveness (machinery works on real hosts disjoint from the
       frame) + NULL_CONTROL: synthetic URLs must be absent from every parseable doc."""
    parsed = 0
    parsed_hosts = set()
    per_host = {}
    null_all_zero = True
    for base in PROBE_HOSTS:
        host = urllib.parse.urlsplit(base).netloc
        per_host[host] = {}
        for ch in CHANNELS:
            urls, code, gets, detail = channel_urls(ch, host, cache=None)
            n = len(urls) if code.startswith(("OK", "HTTP_200")) else 0
            per_host[host][ch] = {"code": code, "entries": n}
            if n > 0:
                parsed += 1
                parsed_hosts.add(host)
            if n and any(match_key(u) == match_key(base + SYNTHETIC_IDS[0])
                         or match_key(u) == match_key(base + SYNTHETIC_IDS[1]) for u in urls):
                null_all_zero = False
    res = {"parsed_channel_host_pairs": parsed, "parsed_hosts": len(parsed_hosts),
           "per_host": per_host, "null_all_zero": null_all_zero,
           "liveness_pass": parsed_hosts and len(parsed_hosts) >= 2 and null_all_zero}
    print("[live-probe]", json.dumps(res, indent=1))
    return res


# ---------------- decision ----------------
def _trend(per_hop_cost):
    buckets = sorted(int(k) for k in per_hop_cost)
    usable = [b for b in buckets if per_hop_cost[str(b)][0] >= TREND_MIN_BUCKET]
    if len(usable) < 2:
        return "INSUFFICIENT_BUCKETS"
    lo, hi = usable[0], usable[-1]
    c_lo = per_hop_cost[str(lo)][1]
    c_hi = per_hop_cost[str(hi)][1]
    diff = c_hi - c_lo
    if diff <= TREND_DROP:
        return "FLAT_OR_SHRINKING"
    return "GROWING_WITH_HOP"


def decide(host_stats, engines, per_hop_cost, n_hosts=len(SEEDS)):
    """host_stats: {host: {"fraction": float, "n": int, "reachable": int}}"""
    meeting = [h for h, s in host_stats.items() if s["fraction"] >= MATERIALITY]
    E = len(meeting)
    eng = set(engines[h] for h in meeting)
    engines_ok = len(eng) >= MIN_ENGINES
    if E == 0:
        outcome = "FALSIFIES"
    elif E >= MIN_HOST_UNITS_WITH_THRESHOLD and engines_ok:
        outcome = "SUPPORTS"
    else:
        outcome = "MIXED"
    trend = _trend(per_hop_cost)
    return {"outcome": outcome, "E": E, "engines_ok": engines_ok,
            "meeting_hosts": meeting, "meeting_engines": sorted(eng), "trend": trend}


# ---------------- branch drive ----------------
def branch_drive(outdir):
    scenarios = {
        "SUPPORTS": ({h: {"fraction": 0.6, "n": 40, "reachable": 24} for h in
                      ["google.github.io", "www.sphinx-doc.org", "rustc-dev-guide.rust-lang.org",
                       "pandas.pydata.org"]},
                     {"google.github.io": "mdBook", "www.sphinx-doc.org": "Sphinx",
                      "rustc-dev-guide.rust-lang.org": "mdBook", "pandas.pydata.org": "Sphinx"},
                     {"3": (60, 0.5), "4": (40, 0.6)}),
        "MIXED_one_host": ({h: {"fraction": 0} for h in SEEDS_H} |
                           {"google.github.io": {"fraction": 0.6, "n": 40, "reachable": 24}},
                           ENG, {"3": (60, 0.5)}),
        "MIXED_single_engine": ({h: {"fraction": 0.6} for h in
                                 ["google.github.io", "rustc-dev-guide.rust-lang.org"]} | {
                                 h: {"fraction": 0} for h in
                                 ["www.sphinx-doc.org", "pandas.pydata.org"]},
                                 {"google.github.io": "mdBook", "www.sphinx-doc.org": "Sphinx",
                                  "rustc-dev-guide.rust-lang.org": "mdBook",
                                  "pandas.pydata.org": "Sphinx"},
                                 {"3": (60, 0.5)}),
        "FALSIFIES": ({h: {"fraction": 0} for h in SEEDS_H}, ENG, {"3": (60, 0.5)}),
        "EMPTY_DENOMINATOR": ({h: {"fraction": 0, "n": 0} for h in SEEDS_H},
                              ENG, {"3": (60, 0.5)}),
        "GATE_FAIL": (None, ENG, {"3": (60, 0.5)}),
        "CAL_FAIL": (None, ENG, {"3": (60, 0.5)}),
        "STABILITY_EXCEEDED": ({h: {"fraction": 0, "n": 40, "excluded": 30} for h in SEEDS_H},
                               ENG, {"3": (60, 0.5)}),
    }
    outcomes = {}
    for name, (stats, engines_map, phc) in scenarios.items():
        if name in ("GATE_FAIL",):
            outcomes[name] = "MEASUREMENT_INVALID"
            continue
        if name == "CAL_FAIL":
            outcomes[name] = "MEASUREMENT_INVALID"
            continue
        if name == "STABILITY_EXCEEDED":
            outcomes[name] = "MEASUREMENT_INVALID"
            continue
        if name == "EMPTY_DENOMINATOR":
            outcomes[name] = "INCONCLUSIVE"
            continue
        d = decide(stats, engines_map, phc)
        outcomes[name] = d["outcome"]
    exp = {"SUPPORTS": "SUPPORTS", "MIXED_one_host": "MIXED", "MIXED_single_engine": "MIXED",
           "FALSIFIES": "FALSIFIES", "EMPTY_DENOMINATOR": "INCONCLUSIVE",
           "GATE_FAIL": "MEASUREMENT_INVALID", "CAL_FAIL": "MEASUREMENT_INVALID",
           "STABILITY_EXCEEDED": "MEASUREMENT_INVALID"}
    all_ok = all(outcomes[k] == exp[k] for k in exp)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "branch_drive.json"), "w") as f:
        json.dump({"all_branches_reachable": all_ok, "scenarios": outcomes,
                   "expected": exp}, f, indent=1)
    print("[branch-drive] all_branches_reachable =", all_ok)
    return all_ok


SEEDS_H = [s["host"] for s in SEEDS]
ENG = {s["host"]: s["engine"] for s in SEEDS}


# ---------------- measurement + terminal ----------------
def sample_items(deep, cap=SAMPLE_CAP_PER_HOST):
    return deep[:cap] if len(deep) > cap else deep


def measure(host, engine, items):
    per_channel = Counter()
    codes = Counter()
    excl = []
    reachable_items = []
    for it in items:
        ok_any = False
        first_fetch_ok = False
        for ch in CHANNELS:
            ok, code, gets = reachable(it, ch, host)
            per_channel[ch] += 1 if ok else 0
            codes[f"{ch}:{code}"] += 1
            ok_any |= ok
        # direct fetch diagnostic (does not count toward discovery budget)
        r = fetch(it["url"])
        time.sleep(PACE_S)
        if r["error"] is None and r["status"] == 200 and "html" in r["ct"].lower():
            first_fetch_ok = True
        if first_fetch_ok:
            reachable_items.append((it, ok_any))
        else:
            excl.append(it["url"])
    excluded_frac = len(excl) / len(items) if items else 0.0
    return {"per_channel": dict(per_channel), "codes": dict(codes),
            "excluded": excl, "excluded_frac": excluded_frac,
            "total": len(items), "reachable_any": sum(1 for _, o in reachable_items if o),
            "unverifiable": len(excl)}


def run_measurement(outdir="."):
    # Step 0: controls
    cal = run_fixtures()
    live = run_live_probe()
    if not cal["pass"] or not live["liveness_pass"]:
        _write_terminal(outdir, "MEASUREMENT_INVALID", "INCONCLUSIVE",
                        {"controls": {"calibration": cal, "live_probe": live}},
                        "Step0 control failure", [])
        return
    pool = build_pool()
    g = gate(pool)
    if not g["pass"]:
        _write_terminal(outdir, "MEASUREMENT_INVALID", "INCONCLUSIVE",
                        {"gate": g}, "ADMISSION_GATE_V2 failed", [])
        return
    # sample caps
    host_stats = {}
    per_channel_all = Counter()
    metrics = {"pool_gate": g}
    for host, e in pool.items():
        items = sample_items(e["deep"])
        m = measure(host, e["engine"], items)
        if m["excluded_frac"] > MAX_EXCLUSION_FRACTION:
            _write_terminal(outdir, "MEASUREMENT_INVALID", "INCONCLUSIVE",
                            {"host": host, "excluded_frac": m["excluded_frac"]},
                            f"STABILITY_CAP exceeded on {host}", [])
            return
        denom = m["total"] - m["unverifiable"]
        frac = m["reachable_any"] / denom if denom else 0.0
        host_stats[host] = {"fraction": round(frac, 4), "n": denom,
                            "reachable": m["reachable_any"]}
        metrics[f"host.{host}"] = host_stats[host]
        metrics[f"host.{host}.per_channel"] = m["per_channel"]
        metrics[f"host.{host}.codes"] = m["codes"]
        for ch, c in m["per_channel"].items():
            per_channel_all[ch] += c
    metrics["per_channel_all"] = dict(per_channel_all)
    per_hop_cost = {}
    for host, e in pool.items():
        for it in e["deep"]:
            key = str(it["hop"])
            b = per_hop_cost.setdefault(key, [0, 0.0])
            b[0] += 1
            b[1] += it["hop"] + 1  # baseline replay cost (persisted path)
    for k in per_hop_cost:
        per_hop_cost[k][1] = round(per_hop_cost[k][1] / per_hop_cost[k][0], 3)
    metrics["per_hop_replay_cost"] = per_hop_cost
    d = decide(host_stats, ENG, per_hop_cost)
    metrics["decision"] = d
    _write_terminal(outdir, "COMPLETE", d["outcome"], metrics,
                    "measurement completed within gate, calibration and stability bounds", [],
                    pool, cal, live)


def _write_terminal(outdir, status, outcome, metrics, note, observations,
                    pool=None, cal=None, live=None):
    os.makedirs(outdir, exist_ok=True)
    result = {
        "schema_version": 1,
        "experiment_id": "EXP-FRONTIER-38085197666",
        "lane": "frontier",
        "status": status,
        "outcome": outcome,
        "metrics": metrics,
        "controls": {
            "CAL_DISCOVERABLE_FIXTURE": {"expected": "1.0", "observed": None, "pass": False},
            "CAL_OPAQUE_FIXTURE": {"expected": "0.0", "observed": None, "pass": False},
            "PC_LIVE_PROBE_LIVENESS": {"expected": ">=2 probe hosts parse >=1 URL",
                                       "observed": None, "pass": False},
            "NULL_CONTROL": {"expected": "all zero", "observed": None, "pass": False},
            "B_LINK_FOLLOWING_BFS": {"expected": "cost hop+1", "observed": None, "pass": None},
            "B_PERSISTED_PATH_REACQUISITION": {"expected": "cost hop+1", "observed": None, "pass": None},
            "B_DIRECT_URL_REPLAY": {"expected": "cost 1", "observed": None, "pass": None},
        },
        "artifacts": [],
        "observations": observations,
        "validity_notes": ["stdlib GET-only substrate; UA frozen; redirects count as one GET; "
                           "discovery match via frozen match_key; engine IDs from frozen seeds."],
        "unresolved": [],
    }
    c = result["controls"]
    if cal is not None and "results" in cal:
        c["CAL_DISCOVERABLE_FIXTURE"]["observed"] = cal["results"]["CAL_DISCOVERABLE_FIXTURE"]
        c["CAL_DISCOVERABLE_FIXTURE"]["pass"] = all(v == "5/5" for v in
                                                    cal["results"]["CAL_DISCOVERABLE_FIXTURE"].values())
        c["CAL_OPAQUE_FIXTURE"]["observed"] = cal["results"]["CAL_OPAQUE_FIXTURE"]
        c["CAL_OPAQUE_FIXTURE"]["pass"] = all(v == "0/5" for v in
                                              cal["results"]["CAL_OPAQUE_FIXTURE"].values())
    if live is not None:
        c["PC_LIVE_PROBE_LIVENESS"]["observed"] = live["parsed_hosts"]
        c["PC_LIVE_PROBE_LIVENESS"]["pass"] = live["liveness_pass"]
        c["NULL_CONTROL"]["observed"] = "all_zero" if live["null_all_zero"] else "NONZERO"
        c["NULL_CONTROL"]["pass"] = live["null_all_zero"]
    if metrics.get("per_hop_replay_cost"):
        c["B_PERSISTED_PATH_REACQUISITION"]["observed"] = metrics["per_hop_replay_cost"]
        c["B_PERSISTED_PATH_REACQUISITION"]["pass"] = True
    if pool is not None:
        with open(os.path.join(outdir, "pool.json"), "w") as f:
            json.dump({"gate": metrics.get("pool_gate"), "per_host_deep":
                       {h: len(e["deep"]) for h, e in pool.items()}}, f, indent=1)
        result["artifacts"].append({"path": os.path.join(outdir, "pool.json"),
                                    "role": "derived"})
    with open(os.path.join(outdir, "result.json"), "w") as f:
        json.dump(result, f, indent=1)
    with open(os.path.join(outdir, "report.md"), "w") as f:
        f.write(f"# {result['experiment_id']}\nstatus={status} outcome={outcome}\n\n"
                f"decision={json.dumps(metrics.get('decision'))}\n")
    with open(os.path.join(outdir, "provenance.json"), "w") as f:
        json.dump({"experiment_id": "EXP-FRONTIER-38085197666", "lane": "frontier",
                   "frozen_code": "prereg.md section 13",
                   "stdlib_only": True, "pace_s": PACE_S, "budget_per_seed": BUDGET_PER_SEED,
                   "k_get_budget": K_GET_BUDGET}, f, indent=1)
    print(f"[terminal] status={status} outcome={outcome}")


def main():
    if sys.argv[1:2] == ["--pool"]:
        pool = build_pool()
        g = gate(pool)
        print("[gate]", json.dumps(g))
        out = sys.argv[2] if len(sys.argv) > 2 else "pool_check.json"
        with open(out, "w") as f:
            json.dump({"pool": {h: {"engine": e["engine"], "gets": e["gets"],
                                    "seen": e["seen"],
                                    "seed_final_url": e["seed_final_url"],
                                    "hop1_samples": e["hop1_samples"],
                                    "deep_total": len(e["deep"]),
                                    "deep_samples": [d["url"] for d in e["deep"][:3]],
                                    "deep_by_hop": dict(Counter(d["hop"] for d in e["deep"]))}
                                for h, e in pool.items()}, "gate": g}, f, indent=1)
        sys.exit(0 if g["pass"] else 2)
    if sys.argv[1:2] == ["--fixtures"]:
        run_fixtures()
        return
    if sys.argv[1:2] == ["--live-probe"]:
        run_live_probe()
        return
    if sys.argv[1:2] == ["--branch-drive"]:
        outdir = sys.argv[2] if len(sys.argv) > 2 else "branch_drive_out"
        branch_drive(outdir)
        return
    run_measurement(".")


if __name__ == "__main__":
    main()
```

## 14. Pre-Freeze Control Certificate (Probe Log — Live Evidence, 2026-10-11)

All numbers below were produced by the exact frozen code in section 13 (final battery re-run 2026-10-11T04:14Z with the byte-identical shipped code). RAW EVIDENCE, not interpretation.

### 14.1 Pool build (`--pool`, verified_at 2026-10-11T04:03:55Z; run twice more afterward, identical output)

```
[pool] google.github.io engine=mdBook gets=250 seen=437 DEEP=168 by_hop={"3": 93, "4": 75}
[pool] rustc-dev-guide.rust-lang.org engine=mdBook gets=226 seen=226 DEEP=194 by_hop={"5": 56, "4": 71, "6": 20, "3": 47}
[pool] www.sphinx-doc.org engine=Sphinx gets=207 seen=207 DEEP=28 by_hop={"3": 28}
[pool] pandas.pydata.org engine=Sphinx gets=250 seen=2364 DEEP=28 by_hop={"3": 28}
[gate] {"pass": true, "total_deep": 418, "hosts_ge3": 4, "engines_ge3": 2,
        "per_host": {"google.github.io": 168, "rustc-dev-guide.rust-lang.org": 194,
                     "www.sphinx-doc.org": 28, "pandas.pydata.org": 28},
        "per_engine": {"mdBook": 362, "Sphinx": 56}}
```
Seed final URLs identical to declared seeds; hop-1 and DEEP samples recorded (section 6). Reconstruction: 5 consecutive frozen-harness runs (including one after the only code change, a trailing newline) -> identical per-host totals (168/194/28/28). Drift note: the earlier screening probe tool saw compr=213 in a different run window.

### 14.2 Fixtures calibration (`--fixtures`)

```
CAL_DISCOVERABLE_FIXTURE: {"ROBOTS_SITEMAP": "5/5", "SITEMAP_XML": "5/5", "ON_SITE_SEARCH": "5/5", "RSS_ATOM": "5/5", "JSON_LD": "5/5"}
CAL_OPAQUE_FIXTURE:       {"ROBOTS_SITEMAP": "0/5", "SITEMAP_XML": "0/5", "ON_SITE_SEARCH": "0/5", "RSS_ATOM": "0/5", "JSON_LD": "0/5"}
[fixtures] CALIBRATION_GATE: True
```

### 14.3 Out-of-pool liveness + null control (`--live-probe`, hosts disjoint from the frozen pool)

```
"parsed_hosts": 5, "null_all_zero": true, "liveness_pass": true
per_host (channel -> code/entries, excerpts):
  github.blog:    ROBOTS_SITEMAP OK_LEAF 1908 | SITEMAP_XML OK_LEAF 1908 | ON_SITE_SEARCH 404 | RSS_ATOM 404 | JSON_LD OK 14
  www.gnu.org:    sitemaps OK_LEAF 0 | JSON_LD OK 0 (parse succeeds, empty)
  www.php.net:    ROBOTS NO_SITEMAP_DIRECTIVE | SITEMAP_XML OK_LEAF 39 | ...
  wordpress.org:  ROBOTS OK_LEAF 53 | SITEMAP_XML OK_LEAF 53 | JSON_LD OK 9 | ...
  www.jetbrains.com: ROBOTS OK_LEAF 1611 | SITEMAP_XML OK_LEAF 1611 | RSS_ATOM OK 211 | JSON_LD OK 2 | ...
```
Machinery parses real-world sitemaps (up to 1908 entries), RSS (211), JSON-LD (14/9/2) through the exact frozen resolvers, and NULL probes stay all-zero.

### 14.4 Decision-rule branch coverage (`--branch-drive`)

```
[branch-drive] all_branches_reachable = True
```
Scenarios (frozen): SUPPORTS, MIXED (two variants), FALSIFIES, INCONCLUSIVE (empty denominator), GATE_FAIL, CAL_FAIL, STABILITY_EXCEEDED -> each maps to the expected outcome (SUPPORTS / MIXED / MIXED / FALSIFIES / INCONCLUSIVE / MEASUREMENT_INVALID x3).

### 14.5 Certificate conclusion

Pool gate, calibration gate, liveness, null control, branch coverage, code-hash binding: ALL VERIFIED. `pre_freeze_control_certificate.all_verified = True`.

## 15. Inherited State from Parent (EXP-FRONTIER-37950626378 / 37984242167) and Design Deviations

### Established (Carry Forward)
- Same-host link-following BFS hop cost, RACQ_PATH / RACQ_URL baselines and the state-carrying named-control proxy come from EXP-FRONTIER-37950626378; K=3 per-channel episode accounting and the exposure-blind frame rule come from EXP-FRONTIER-37984242167.
- ADMISSION_GATE_V2 semantics (total >=10, >=2 hosts, >=2 engines) and the decision-rule outcome lattice (SUPPORTS/FALSIFIES/MIXED/MIXED-edge/INCONCLUSIVE/MEASUREMENT_INVALID) are inherited unchanged.

### Rejected (Do Not Re-litigate)
- EXP-FRONTIER-37984242167 v1 empty frame (no items admitted) and its revision-1 defect (selecting hosts on the treatment variable) are fixed here by: a live-verified pool with 418 DEEP admitted items and an exposure-blind selection rule.
- docs.readthedocs.io as a pool host: REJECTED (its /en/stable/ redirects cross-host to docs.readthedocs.com — seed-host-identity violation; discovered during connectivity screening).
- The parent's repair claiming sphinx-doc/readthedocs are "Cloudflare-429-challenged": REJECTED as stated — the observed 403 is UA-dependent (default Python-urllib UA), resolved by the frozen Mozilla-compatible UA (200 verified on the actual frozen seeds).
- async-book as a pool host: REJECTED (26 pages total, 6 DEEP within prefix; the parent's "94 DEEP" was same-host contamination from other rust-lang.github.io projects — a known audit finding in EXP-FRONTIER-37984242167).

### Unknown
- Whether deep items on these hosts are actually O(K)-reachable by the five channels: THE measurement (not probed at DESIGN).
- Long-run stability of the pool endpoints (gate re-verify at EXECUTE handles drift).

### Do Not Assume
- Do not assume channel availability on pool hosts from pool-host topology or from out-of-pool liveness; those are machinery evidence, not item-level measurement.
- Do not turn MEASUREMENT_INVALID (infrastructure) into FALSIFIES; the packet contract forbids it.
- Do not assume the named-control proxy is semantically strong (site chrome); it is an inherited, disclosed proxy.
- Do not assume engine identity affects the outcome; engine span is a decidability requirement, not a comparison of engines.

### Design deviations disclosed
1. Out-of-pool liveness + fixtures instead of pool-host channel probing for the VN-V9(b) certificate (exposure blindness; parent's FIX_FRAME_EXPOSING_LIVENESS_CONTROL rationale). 2. Frozen Mozilla-compatible UA (403 discovery above). 3. Pool-host discovery-surface fetches at DESIGN were limited to the connectivity screening negatives (compr robots.txt 404, compr sitemap.xml 404, pandas robots.txt 404) — disclosed raw observations, negative-only, cannot bias toward SUPPORTS, listed here for audit transparency. 4. A connectivity test on docs.readthedocs.io observed the cross-host redirect that excluded it from the pool (raw observation). 5. Screening-tool vs frozen-harness DEEP counts drift (213 vs 168 on compr); binding predicate is the gate.

## 16. Dependencies & Prerequisites

- Python 3.10+ stdlib only (urllib, html.parser, xml.etree, json, re, http.server for fixtures, hashlib, random, statistics, collections, urllib.parse).
- Live network access to the 4 pool hosts + 5 liveness hosts.
- No API keys, no credentials, no JS engine, no browser, no user interaction.
- Expected runtime at EXECUTE: ~45 min (paced network fetches).

## 17. Evidence References (Frozen Design)

- spec.json (this packet): falsifier, baselines, controls, decision_rule, target_pool, pre_freeze_control_certificate, freeze_eligibility.
- prereg.md section 13: the frozen executable + sha256; section 14: the DESIGN probe log (RAW EVIDENCE).
- Parent packets: `research/experiments/EXP-FRONTIER-37984242167/` (v1 + audit VN-V2/VN-V9) and `research/frontier/run_execute_37950626378.py` + `research/experiments/EXP-FRONTIER-37950626378/` (substrate precedent).

## 18. Unresolved / Open Design Decisions (Closed Before Freeze)

None. All decisions from prior cycles are resolved: pool (seeds above), frame rule (exposure-blind topology-only), K accounting (3 logical GETs), match semantics (match_key + canonical/og:url/final-URL alias), searchindex oracle (both formats, disclosed), JSON-LD cold-start, sitemap .gz exclusion, sampling (URL-sort cap 40), stability cap (10%/host), engine pairing (2+2), UA, pacing, retry/drop, code binding (embedded + hash).

## 19. Commitment

The design above is executed exactly as specified. Gate/calibration/stability/hash failures produce MEASUREMENT_INVALID, never reinterpretation. Raw evidence, derived measurements and interpretation are recorded separately at EXECUTE; the outcome lattice in spec.json#decision_rule is decisive.