#!/usr/bin/env python3
"""EXP-INTEL-36287179392 phase A -- frozen raw fetch (prereg 5.2, 5.3, 6.1).

CONFORMING RUN. The first attempt (raw/../attempt1_nonconforming/) was discarded
before any outcome metric was computed because its page discovery did not match
frozen prereg 5.3:
  (a) it resolved "same-origin" as same-REGISTRABLE-DOMAIN, so
      en.wikipedia.org walked onto 300+ sibling language Wikipedias
      (400 distinct request hosts across a 20-site sample);
  (b) it applied a Content-Type filter that frozen prereg 5.3 does not list,
      discarding 540 valid 200-OK Wikipedia HTML pages whose responses carried
      no Content-Type header.
Both are implementation defects against the frozen text, not design changes.
The frozen sample, seeds, limits, rate limit and decision rule are unchanged.

Fetches the 20 pre-registered public sites over credential-free HTTP(S) GET,
respects robots.txt, rate-limits to <=1 req/sec per host, and records one raw
response record per request. No credentials, registry auth, browser binary or
model API key is used.

Outputs (raw evidence, under the experiment packet directory):
  raw/robots_records.jsonl      one record per robots.txt fetch
  raw/raw_responses.jsonl       one record per page GET (prereg 14)
  raw/bodies/<sha256>.html.gz   gzip of the exact response body bytes
  raw/fetch_manifest.json       per-site page inventory + discovery decisions
"""
from __future__ import annotations

import gzip
import json
import os
import sys
import threading
from collections import deque
from urllib.parse import urlsplit, urlunsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bs4 import BeautifulSoup  # noqa: E402

from exp_36287179392_pipeline import (  # noqa: E402
    ACCEPT, MAX_PAGES_PER_SITE, MIN_PAGES_PER_SITE, SITE_SAMPLE, USER_AGENT,
    RateLimitedSession, absolutize, etld1, link_candidate_ok, make_robot_parser,
    sha256_bytes,
)

EXP_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "experiments", "EXP-INTEL-36287179392",
)
RAW = os.path.join(EXP_DIR, "raw")
BODIES = os.path.join(RAW, "bodies")

_write_lock = threading.Lock()


def record_path(url, status, headers, body, latency_ms, timestamp, kind, site_key):
    return {
        "url": url,
        "status": status,
        "headers": headers,
        "body_sha256": sha256_bytes(body) if body else None,
        "bytes": len(body),
        "latency_ms": latency_ms,
        "timestamp": timestamp,
        "kind": kind,
        "site_key": site_key,
    }


def canonicalize(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path or "/", parts.query, ""))


def same_origin(url: str, origin_netloc: str) -> bool:
    """Frozen prereg 5.3: same-origin links only (scheme-relative / base host)."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return parts.netloc.lower() == origin_netloc.lower()


def store_body(body: bytes) -> str:
    h = sha256_bytes(body)
    path = os.path.join(BODIES, h + ".html.gz")
    if not os.path.exists(path):
        with gzip.open(path, "wb") as fh:
            fh.write(body)
    return h


def fetch_site(session, ordinal, site_key, base_url, category,
               robots_records, response_records, body_lock):
    site_info = {
        "ordinal": ordinal, "site_key": site_key, "base_url": base_url,
        "category": category, "pages": [], "discovered_blocked": [],
        "discovered_filtered": [], "errors": [], "notes": [],
    }
    rp, robots_url = make_robot_parser(session, base_url, robots_records)
    site_info["robots_url"] = robots_url
    site_info["robots_status"] = robots_records[-1]["status"] if robots_records else None

    homepage = session.get(base_url)
    with body_lock:
        response_records.append(record_path(
            homepage["url_requested"], homepage["status"], homepage["headers"],
            homepage["body"], homepage["latency_ms"], homepage["timestamp"],
            "homepage", site_key))
    if not homepage["body"]:
        site_info["errors"].append(f"homepage_fetch_failed: {homepage['error']}")
        return site_info
    if homepage["status"] != 200:
        site_info["notes"].append(f"homepage_status_{homepage['status']}")

    final_url = homepage["url_final"] or base_url
    origin_netloc = urlsplit(final_url).netloc.lower()
    derived = etld1(origin_netloc)
    site_info["origin_netloc"] = origin_netloc
    site_info["derived_registrable_domain"] = derived
    site_info["prereg_label_is_registrable_domain"] = (derived == site_key)
    if derived != site_key:
        site_info["notes"].append(
            f"prereg_label_{site_key}_is_not_registrable_domain;derived_{derived}")
    if origin_netloc.lower() != urlsplit(base_url).netloc.lower():
        site_info["notes"].append("homepage_crossed_host:" + origin_netloc)

    with body_lock:
        bh = store_body(homepage["body"])
    site_info["pages"].append({
        "url": final_url, "url_requested": base_url, "status": homepage["status"],
        "content_type": homepage["headers"].get("Content-Type", ""),
        "body_sha256": bh, "bytes": len(homepage["body"]),
        "latency_ms": homepage["latency_ms"], "discovered_from": None, "depth": 0,
    })

    # prereg 5.3: same-origin BFS, frozen exclusion filter, <= 10 pages/site.
    # Bodies already fetched are reused for link discovery (no re-fetch).
    queue = deque([(final_url, homepage["body"], 0)])
    seen = {canonicalize(final_url)}
    n_discovered_same_origin = 0
    while queue and len(site_info["pages"]) < MAX_PAGES_PER_SITE:
        parent, parent_body, depth = queue.popleft()
        try:
            soup = BeautifulSoup(parent_body, "html.parser")
        except Exception:
            continue
        hrefs = []
        for a in soup.find_all("a", href=True):
            h = a.get("href") or ""
            if not link_candidate_ok(h, parent):
                continue
            absu = absolutize(h, parent)
            if not absu or not same_origin(absu, origin_netloc):
                continue
            hrefs.append(absu)
        for absu in hrefs:
            if len(site_info["pages"]) >= MAX_PAGES_PER_SITE:
                site_info["notes"].append("page_cap_reached_10")
                break
            canon = canonicalize(absu)
            if canon in seen:
                continue
            seen.add(canon)
            n_discovered_same_origin += 1
            if not rp.can_fetch(USER_AGENT, absu):
                site_info["discovered_blocked"].append({"url": absu, "reason": "robots_disallow"})
                continue
            rec = session.get(absu)
            with body_lock:
                response_records.append(record_path(
                    rec["url_requested"], rec["status"], rec["headers"], rec["body"],
                    rec["latency_ms"], rec["timestamp"], "discovered", site_key))
            if rec["status"] != 200 or not rec["body"]:
                site_info["discovered_filtered"].append(
                    {"url": absu, "reason": f"status_{rec['status']}", "error": rec["error"]})
                continue
            with body_lock:
                bh = store_body(rec["body"])
            site_info["pages"].append({
                "url": rec["url_final"] or absu, "url_requested": absu,
                "status": rec["status"],
                "content_type": rec["headers"].get("Content-Type", ""),
                "body_sha256": bh, "bytes": len(rec["body"]),
                "latency_ms": rec["latency_ms"], "discovered_from": parent,
                "depth": depth + 1,
            })
            queue.append((rec["url_final"] or absu, rec["body"], depth + 1))

    site_info["n_discovered_same_origin"] = n_discovered_same_origin
    if len(site_info["pages"]) < MIN_PAGES_PER_SITE:
        site_info["notes"].append(
            f"fewer_than_min_pages: {len(site_info['pages'])} < {MIN_PAGES_PER_SITE}")
    return site_info


def main():
    os.makedirs(BODIES, exist_ok=True)
    session = RateLimitedSession()
    robots_records, response_records = [], []
    body_lock = threading.Lock()
    results = {}
    lock = threading.Lock()

    def worker(item):
        ordinal, site_key, base_url, category = item
        info = fetch_site(session, ordinal, site_key, base_url, category,
                          robots_records, response_records, body_lock)
        with lock:
            results[site_key] = info
            print(f"[{ordinal:02d}/20] {site_key:24s} pages={len(info['pages']):2d} "
                  f"same_origin_found={info.get('n_discovered_same_origin', 0):3d} "
                  f"robots_blocked={len(info['discovered_blocked']):2d} "
                  f"non200={len(info['discovered_filtered']):3d} "
                  f"notes={';'.join(info['notes']) or '-'}", flush=True)

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(worker, SITE_SAMPLE))

    with open(os.path.join(RAW, "robots_records.jsonl"), "w") as fh:
        for r in robots_records:
            fh.write(json.dumps({
                "url": r["url_requested"], "status": r["status"],
                "body_sha256": sha256_bytes(r["body"]) if r["body"] else None,
                "bytes": r["bytes"], "latency_ms": r["latency_ms"],
                "timestamp": r["timestamp"], "error": r["error"],
            }) + "\n")

    with open(os.path.join(RAW, "raw_responses.jsonl"), "w") as fh:
        for r in sorted(response_records, key=lambda x: (str(x["site_key"]), str(x["url"]))):
            fh.write(json.dumps(r) + "\n")

    distinct_hosts = {urlsplit(r["url"]).netloc.lower() for r in response_records}
    manifest = {
        "experiment_id": "EXP-INTEL-36287179392",
        "run": "conforming",
        "user_agent": USER_AGENT,
        "accept": ACCEPT,
        "per_host_min_interval_s": 1.05,
        "max_pages_per_site": MAX_PAGES_PER_SITE,
        "n_sites_preregistered": len(SITE_SAMPLE),
        "n_sites_attempted": len(results),
        "n_http_requests_total": len(response_records) + len(robots_records),
        "n_distinct_request_hosts": len(distinct_hosts),
        "n_page_records": sum(len(v["pages"]) for v in results.values()),
        "n_sites_ge_min_pages": sum(1 for v in results.values() if len(v["pages"]) >= MIN_PAGES_PER_SITE),
        "total_body_bytes_stored": sum(p["bytes"] for v in results.values() for p in v["pages"]),
        "sites": {k: results[k] for k in sorted(results)},
    }
    with open(os.path.join(RAW, "fetch_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)

    print(json.dumps({k: v for k, v in manifest.items() if k != "sites"}, indent=1))


if __name__ == "__main__":
    main()
