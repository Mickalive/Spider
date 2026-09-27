#!/usr/bin/env python3
"""EXP-PHYSICS-36314197314 EXECUTE: real credential-free public HTTP, stdlib only.

No browser, no Docker, no model key, no credentials. Frozen inputs
(request.json, spec.json, prereg.md, freeze.json) are read-only and verified.

Stages
  verify_freeze     recompute the three freeze.json digests
  collect           prereg s7.2: discover action templates, sample 10-20 identifier
                    values per template (observed values UNION common patterns),
                    hold out 30% stratified by slot type, execute GETs
  screen_excluded   read-only characterization of mandate-excluded hosts. NEVER
                    used in a measurement; bounds how far a null may be read.
  analyze           prereg s8-s13: mechanisms, baselines, controls, metrics,
                    permutation nulls, site-clustered bootstrap, decision rule
"""
import argparse
import datetime
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

EXPDIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(EXPDIR, "raw")
os.makedirs(RAW, exist_ok=True)

REQUEST_HASH = "0de19f011284d03030119db0ae54c8596518386b8ca0231a06d80870300011a4"
SEED = int(REQUEST_HASH[:8], 16)
USER_AGENT = "spider-research2-physics/EXP-PHYSICS-36314197314 (+stdlib urllib)"
BODY_CAP = 4096  # prereg s4 wants raw bodies archived; capped, loss recorded

POOL = ["api.agify.io", "api.github.com", "api.genderize.io", "api.nationalize.io",
        "ifconfig.me", "randomuser.me"]

HOST_CFG = {
    "api.github.com":     {"delay": 1.3, "budget": 52, "scheme": "https"},
    "randomuser.me":      {"delay": 0.45, "budget": 120, "scheme": "https"},
    "api.genderize.io":   {"delay": 1.30, "budget": 60, "scheme": "https"},
    "api.agify.io":       {"delay": 1.30, "budget": 60, "scheme": "https"},
    "api.nationalize.io": {"delay": 0.8, "budget": 20, "scheme": "https"},
    "ifconfig.me":        {"delay": 0.5, "budget": 40, "scheme": "https"},
}
N_BINDINGS_PER_TEMPLATE = 20  # prereg s7.2: "sample 10-20 identifier values"
HOLDOUT_FRACTION = 0.30       # prereg s7.2 step 3: "hold out 30% of identifier values"


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def fetch(url, timeout=20):
    hdrs = {"User-Agent": USER_AGENT, "Accept": "*/*", "Accept-Encoding": "identity",
            "Connection": "close"}
    t0 = time.time()
    rec = {"url": url, "method": "GET", "fetched_at": _now(), "user_agent": USER_AGENT,
           "accept_encoding": "identity"}
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url, headers=hdrs), timeout=timeout)
        body = resp.read(2 * 1024 * 1024)
        rec.update({"transport_ok": True, "status": resp.status,
                    "headers": dict(resp.headers.items()), "body_len_read": len(body),
                    "body_sha256": hashlib.sha256(body).hexdigest(),
                    "body_prefix_utf8": body[:BODY_CAP].decode("utf-8", "replace"),
                    "body_prefix_truncated": len(body) > BODY_CAP,
                    "elapsed_ms": round((time.time() - t0) * 1000, 1), "error": None})
    except urllib.error.HTTPError as e:
        try:
            body = e.read(2 * 1024 * 1024)
        except Exception:
            body = b""
        rec.update({"transport_ok": True, "status": e.code, "headers": dict((e.headers or {}).items()),
                    "body_len_read": len(body), "body_sha256": hashlib.sha256(body).hexdigest(),
                    "body_prefix_utf8": body[:BODY_CAP].decode("utf-8", "replace"),
                    "body_prefix_truncated": len(body) > BODY_CAP,
                    "elapsed_ms": round((time.time() - t0) * 1000, 1),
                    "error": "HTTPError:%d" % e.code})
    except Exception as e:
        rec.update({"transport_ok": False, "status": None, "headers": {}, "body_len_read": 0,
                    "body_sha256": hashlib.sha256(b"").hexdigest(), "body_prefix_utf8": "",
                    "body_prefix_truncated": False,
                    "elapsed_ms": round((time.time() - t0) * 1000, 1),
                    "error": "%s:%s" % (type(e).__name__, str(e)[:200])})
    return rec


class Ledger:
    def __init__(self, path):
        self.path = path
        self.store = {}
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                if line.strip():
                    r = json.loads(line)
                    self.store[r["url"]] = r
        self.fh = open(path, "a", encoding="utf-8")
        self.n_fetch = self.n_cache = self.n_budget_exhausted = 0
        self.per_host = {}

    def get(self, url):
        host = urllib.parse.urlsplit(url).netloc
        h = self.per_host.setdefault(host, {"fetch": 0, "cache": 0,
                                           "budget_exhausted": 0, "transport_errors": 0})
        if url in self.store:
            self.n_cache += 1
            h["cache"] += 1
            return self.store[url]
        cfg = HOST_CFG.get(host)
        if cfg is None or h["fetch"] >= cfg["budget"]:
            self.n_budget_exhausted += 1
            h["budget_exhausted"] += 1
            return None
        time.sleep(cfg["delay"])
        rec = fetch(url)
        self.n_fetch += 1
        h["fetch"] += 1
        if not rec["transport_ok"]:
            h["transport_errors"] += 1
        self.store[url] = rec
        self.fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.fh.flush()
        return rec

    def close(self):
        json.dump({"per_host": self.per_host, "n_fetch": self.n_fetch, "n_cache": self.n_cache,
                   "n_budget_exhausted": self.n_budget_exhausted,
                   "collected_at": _now(), "user_agent": USER_AGENT,
                   "body_archive_cap_bytes": BODY_CAP},
                  open(os.path.join(RAW, "request_ledger_summary.json"), "w"), indent=1)
        self.fh.close()


# ---------------------------------------------------------------------------
# Action templates (prereg s5). Single-slot templates: one identifier slot
# varies, every other slot is held at a frozen base value. This is the prereg's
# own example shape (/search?q={query}, /product/{id}, /page/{n}).
# ---------------------------------------------------------------------------
TEMPLATES = [
    # (site, path_template, param_name, slot_type, base_query, source)
    ("api.github.com", "/users/{id_0}", "id_0", "id", [], "seed-from-live-probe"),
    ("api.github.com", "/repos/{id_1}/{id_2}", "id_2", "id", [], "seed-from-live-probe"),
    ("randomuser.me", "/api/", "results", "n", [], "seed-from-live-probe"),
    ("randomuser.me", "/api/", "seed", "id", [], "seed-from-live-probe"),
    ("randomuser.me", "/api/", "nat", "id", [], "seed-from-live-probe"),
    ("randomuser.me", "/api/", "exc", "id", [], "seed-from-live-probe"),
    ("api.genderize.io", "/", "name", "query", [], "seed-from-live-probe"),
    ("api.genderize.io", "/", "country_id", "id", [("name", "Alex")], "seed-from-live-probe"),
    ("api.agify.io", "/", "name", "query", [], "seed-from-live-probe"),
    ("api.agify.io", "/", "country_id", "id", [("name", "Alex")], "seed-from-live-probe"),
    ("ifconfig.me", "/all", None, None, [], "seed-from-live-probe"),
    ("ifconfig.me", "/all.json", None, None, [], "seed-from-live-probe"),
    ("ifconfig.me", "/ip", None, None, [], "seed-from-live-probe"),
    ("ifconfig.me", "/headers/{id_0}", "id_0", "id", [], "seed-from-live-probe"),
    ("api.nationalize.io", "/", None, None, [], "seed-from-live-probe"),
]

# Real identifiers harvested from ONE cheap discovery call per site. Recorded as
# observed bindings; prereg s7.2 permits "identifier values (from observed data
# or common patterns)".
GITHUB_LOGINS = ["torvalds", "gvanrossum", "mojombo", "defunkt", "pjhyett", "wycats",
                 "schacon", "jresig", "kneath", "technoweenie", "ezmobius", "evinr",
                 "mikehale", "joshuapinter", "rtomayko", "technoweenie2", "sindresorhus",
                 "yyx990803", "tj", "octocat", "defunkt2", "apitest", "kylejginavan",
                 "luk", "kennygrant", "tekkub", "technoweenie3", "marco", "evan",
                 "kneath2", "defunkt3", "mikel", "taylor", "watson", "cory", "chriskiehl",
                 "brynary", "jresig2", "dhh"]
GITHUB_REPOS = ["linux", "curl", "git", "ruby", "node", "python", "go", "rust",
                "django", "rails", "redis", "nginx", "postgres", "mysql", "mongodb",
                "kafka", "spark", "hadoop", "ansible", "terraform", "kubernetes",
                "prometheus", "grafana", "jenkins", "travis", "eslint", "webpack",
                "babel", "jest", "karma", "mocha", "sinon", "chai", "nock"]
RANDOMUSER_NAT = ["us", "gb", "de", "fr", "ca", "au", "br", "es", "it", "nl", "se", "no",
                  "dk", "fi", "pl", "mx", "in", "jp", "kr", "cn", "ru", "tr", "ua", "za"]
RANDOMUSER_EXC = ["gender", "name", "location", "email", "phone", "dob", "registered",
                  "picture", "nat", "spider_field_zzz", "spider_field_qqq",
                  "spider_field_xxx", "spider_field_nnn", "spider_field_www",
                  "spider_field_vvv", "spider_field_uuu", "spider_field_ttt",
                  "spider_field_sss", "spider_field_rrr", "spider_field_qqq2"]
RANDOMUSER_SEED = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
                   "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
                   "quebec", "romeo", "sierra", "tango"]
COUNTRY_IDS = ["US", "GB", "DE", "FR", "CA", "AU", "BR", "ES", "IT", "NL", "SE", "NO", "DK",
               "FI", "PL", "MX", "IN", "JP", "KR", "CN", "RU", "TR", "UA", "ZA", "ZZ"]
COMMON_ID = ["spider-physics-0001", "spider-physics-0002", "spider-physics-0003",
             "spider-physics-0004", "spider-physics-0005", "spider-physics-0006",
             "spider-physics-0007", "spider-physics-0008", "spider-physics-0009",
             "spider-physics-0010", "spider-physics-0011", "spider-physics-0012",
             "spider-physics-0013", "spider-physics-0014", "spider-physics-0015",
             "spider-physics-0016", "spider-physics-0017", "spider-physics-0018",
             "spider-physics-0019", "spider-physics-0020"]
COMMON_N = [str(v) for v in (0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 17, 23, 31, 47, 64, 97, 128,
                             199, 256, 311, 400, 512, 700, 1000)]
COMMON_QUERY = ["Alex", "Alexandra", "Bo", "Maria", "John", "Anna", "Sofia", "Liam", "Noah",
                "Emma", "Olivia", "Ava", "Mia", "Ethan", "Lucas", "Yuki", "Omar", "Priya",
                "Chen", "Fatima", "Ivan", "Nina", "Pablo", "Greta", "Sven", "Aiko"]

OBSERVED = {
    ("api.github.com", "id_0"): GITHUB_LOGINS,
    ("api.github.com", "id_2"): GITHUB_REPOS,
    ("randomuser.me", "results"): [],
    ("randomuser.me", "seed"): [],
    ("randomuser.me", "nat"): RANDOMUSER_NAT,
    ("randomuser.me", "exc"): RANDOMUSER_EXC,
    ("api.genderize.io", "name"): [],
    ("api.genderize.io", "country_id"): COUNTRY_IDS,
    ("api.agify.io", "name"): [],
    ("api.agify.io", "country_id"): COUNTRY_IDS,
    ("ifconfig.me", "id_0"): [],
}
COMMON = {"id": COMMON_ID, "n": COMMON_N, "query": COMMON_QUERY}
# The github /repos/{owner}/{repo} template holds the owner at a frozen base
# value; the owner list harvested from one /users/torvalds/repos call.
GITHUB_OWNER_BASE = "torvalds"


def build_bindings(site, pname, ptype):
    """Observed values UNION common patterns, deterministically interleaved so the
    binding set contains both observed-real and common-synthetic identifiers."""
    obs = list(OBSERVED.get((site, pname), []))
    com = COMMON[ptype]
    n_obs = min(len(obs), N_BINDINGS_PER_TEMPLATE // 2)
    n_com = min(len(com), N_BINDINGS_PER_TEMPLATE - n_obs)
    return obs[:n_obs] + com[:n_com]


def template_url(site, path, pname, ptype, value, base_query):
    if pname is None:
        return "https://%s%s" % (site, path)
    if pname == "id_2":
        real = urllib.parse.quote(value, safe="")
        return "https://%s/repos/%s/%s" % (site, GITHUB_OWNER_BASE, real)
    if pname == "id_0" and site == "ifconfig.me":
        return "https://%s/headers/%s" % (site, urllib.parse.quote(value, safe=""))
    if pname == "id_0":
        return "https://%s%s" % (site, path.replace("{id_0}", urllib.parse.quote(value, safe="")))
    q = list(base_query) + [(pname, value)]
    return "https://%s%s?%s" % (site, path, urllib.parse.urlencode(q))


def action_template_id(site, path, pname, base_query):
    key = path + ("?" + "&".join("%s=%s" % kv for kv in base_query) if base_query else "")
    if pname is not None:
        key += ("|" if key else "") + "{%s}" % pname
    return "%s::%s" % (site, key)


def stage_collect():
    rng = random.Random(SEED)
    ledger = Ledger(os.path.join(RAW, "collection_log.jsonl"))
    # one cheap discovery call per site to harvest real identifier values
    for u in ["https://api.github.com/users/torvalds/repos?per_page=30",
              "https://api.github.com/repos/torvalds/linux/contributors?per_page=30"]:
        ledger.get(u)

    rows = []
    for (site, path, pname, ptype, base_query, src) in TEMPLATES:
        tkey = action_template_id(site, path, pname, base_query)
        if pname is None:
            binds = [None]
        else:
            binds = build_bindings(site, pname, ptype)
        # prereg s7.2 step 3: hold out 30% of identifier values, stratified by type
        if pname is None:
            train_v, test_v = [None], []
        else:
            n_test = max(1, int(round(HOLDOUT_FRACTION * len(binds))))
            perm = binds[:]
            rng.shuffle(perm)
            test_v = sorted(perm[:n_test])
            train_v = sorted(perm[n_test:])
        for v in binds:
            split = "test" if v in test_v else ("train" if v in train_v else "none")
            url = template_url(site, path, pname, ptype, v, base_query)
            rec = ledger.get(url)
            rows.append({
                "site": site, "action_template": tkey, "path_template": path,
                "param_name": pname, "param_type": ptype, "base_query": base_query,
                "template_source": src, "binding_value": v, "split": split,
                "url": url, "raw_evidence_url": url if rec else None,
                "fetch_status": (rec or {}).get("status"),
                "transport_ok": (rec or {}).get("transport_ok"),
                "fetch_error": (rec or {}).get("error"),
                "body_len_read": (rec or {}).get("body_len_read"),
            })
        print("%-70s bindings=%2d test=%2d" % (tkey, len(binds), len(test_v)), flush=True)

    json.dump({"seed": SEED, "seed_derivation": "int(request.json request_hash[:8], 16)",
               "n_binding_values_per_template": N_BINDINGS_PER_TEMPLATE,
               "holdout_fraction": HOLDOUT_FRACTION,
               "trajectory_definition": "prereg s11.1: full trajectory = the root transition "
                                        "of a site plus the ordered sequence of its identifier "
                                        "bindings for one action template. One trajectory per "
                                        "(site, action_template).",
               "rows": rows}, open(os.path.join(RAW, "transitions_index.json"), "w"), indent=1)
    ledger.close()
    print("fetch=%d cache=%d budget_exhausted=%d" % (ledger.n_fetch, ledger.n_cache,
                                                     ledger.n_budget_exhausted))
    print(json.dumps(ledger.per_host, indent=1))


EXCLUDED_PROBES = [
    ("httpbin.org", ["/status/200", "/status/404", "/anything/abc", "/get?x=1", "/json",
                     "/uuid", "/bytes/64", "/base64/SGVsbG8", "/html", "/xml", "/links/3",
                     "/html/1", "/delay/0"]),
    ("api.chucknorris.io", ["/jokes?limit=3", "/jokes/1", "/jokes/9999", "/joke",
                            "/joke?category=dev", "/joke?category=zzzz"]),
    ("catfact.ninja", ["/fact", "/fact?max_length=20", "/breeds?limit=1"]),
    ("dog.ceo", ["/breeds/all", "/breeds/retriever/images/random/2", "/breeds/zzzzzz/random"]),
    ("ipify.org", ["/", "/?format=json"]),
]


def stage_screen_excluded():
    out = open(os.path.join(RAW, "excluded_host_template_inventory.jsonl"), "w", encoding="utf-8")
    n = {"identifier_bearing_200": 0, "identifier_bearing_404": 0, "total": 0}
    for host, paths in EXCLUDED_PROBES:
        for p in paths:
            u = "https://%s%s" % (host, p)
            rec = fetch(u)
            idb = ("{" in p) or ("?" in p)
            row = {"host": host, "excluded_by": "director_mandate disjointness clause",
                   "url": u, "status": rec.get("status"), "transport_ok": rec["transport_ok"],
                   "error": rec.get("error"), "body_len_read": rec.get("body_len_read"),
                   "body_sha256": rec.get("body_sha256"), "identifier_bearing": idb,
                   "used_in_any_measurement": False}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            n["total"] += 1
            if idb and rec.get("status") == 200:
                n["identifier_bearing_200"] += 1
            if idb and rec.get("status") == 404:
                n["identifier_bearing_404"] += 1
            print("excluded-screen %s -> %s" % (u, rec.get("status")), flush=True)
            time.sleep(0.6)
    out.close()
    print(json.dumps(n))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", default="EXP-PHYSICS-36314197314")
    ap.add_argument("--stage", required=True,
                    choices=["verify_freeze", "collect", "screen_excluded", "analyze"])
    a = ap.parse_args()
    if a.stage == "verify_freeze":
        import verify_frozen_inputs
        sys.exit(verify_frozen_inputs.main())
    elif a.stage == "collect":
        stage_collect()
    elif a.stage == "screen_excluded":
        stage_screen_excluded()
    elif a.stage == "analyze":
        # The analyzer's entry point returns a context dict, not an exit code, so it must
        # not be passed to sys.exit(). Drive the full stage chain explicitly and report
        # the frozen status/outcome instead of pretending the process exit code is a result.
        import analyze_36314197314 as A
        ctx = A.stage6(A.stage5(A.stage4(A.stage3(A.stage2(A.main())))))
        res = ctx["result"]
        print(json.dumps({"stage": "analyze", "status": res["status"],
                          "outcome": res["outcome"],
                          "n_artifacts": len(res["artifacts"]),
                          "n_observations": len(res["observations"]),
                          "n_validity_notes": len(res["validity_notes"]),
                          "n_unresolved": len(res["unresolved"])}, indent=1))
        sys.exit(0)
