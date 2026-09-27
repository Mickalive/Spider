"""Frozen site-selection screen for EXP-FRONTIER-36306528608 (prereg sections 4-7, 11).

This is a transcription of the FROZEN preregistration into executable form. It performs:

  * 4.1  calibration procedure on the frozen calibration site, which must PASS all of
    4.2 before TEST site screening may begin;
  * 4.2  criteria C1-C7, each with the operational test and pass condition written in
    the prereg table;
  * 4.3  the frozen candidate site pool, in the frozen order, with no substitution;
  * 4.4  the fallback record (exact site list, per-criterion failure, missing ingredient);
  * 7.    action-gating object detection with required_action, gating_type and a
    ground_truth_verifier name;
  * 11.   the deterministic re-derivable / requires-cross-episode-state classification,
    with numerator and denominator in the same unit (span counts).

No arm logic. No outcome measurement. Every HTTP transaction is written to
raw/http.jsonl; every page observation to raw/pages.jsonl; every classified object to
raw/objects.jsonl; every identifier to raw/identifiers.jsonl.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from harness_36306528608 import (  # noqa: E402
    EXPERIMENT_ID,
    RAW_DIR,
    HttpSubstrate,
    JsonlWriter,
    ResponseCache,
    file_sha256,
    observe,
    parse_forms,
    parse_links,
    same_site,
    script_form_hints,
    sha256_hex,
    NONGET_METHODS,
)

# --------------------------------------------------------------------------- #
# FROZEN constants, transcribed verbatim from prereg.md
# --------------------------------------------------------------------------- #

CALIBRATION_SITE = "https://httpbin.org/forms/post"          # prereg 4.1
CALIBRATION_ROOT = "https://httpbin.org/forms/post"
CANDIDATE_POOL = [                                          # prereg 4.3, in order
    "https://httpbin.org",
    "https://httpbin.org/forms/post",
    "https://httpbin.org/cookies/set",
    "https://httpbin.org/post",
    "https://postman-echo.com",
    "https://api.publicapis.org",
    "https://reqres.in",
    "https://jsonplaceholder.typicode.com",
    "https://developer.mozilla.org",
    "https://docs.python.org",
    "https://en.wikipedia.org",
    "https://example.com",
    "https://github.com",
    "https://gitlab.com",
    "https://bitbucket.org",
]
MIN_QUALIFYING_SITES = 3                                    # prereg 4.2 / spec
MIN_GATING_OBJECTS = 3                                      # prereg 4.2 C2
MIN_TOKEN_NAME_MATCHES = 1                                  # prereg 4.2 C3
MAX_DEPTH = 3                                               # prereg 4.2 C4 ">=2 hops"
FANOUT_CAP = 10
PAGE_CAP = 30
MIN_OBJECT_MULTISTEP_HOPS = 2                               # prereg 4.2 C4

ASSET_RE = re.compile(r"\.(css|js|png|jpe?g|gif|svg|ico|woff2?|ttf|mp4|webm|pdf|zip|gz)$", re.IGNORECASE)
LOGIN_RE = re.compile(r"(login|signin|sign_in|oauth|auth/|authorize|sso)", re.IGNORECASE)


def root_of(url: str) -> str:
    p = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((p.scheme, p.netloc, "/", "", "", ""))


# --------------------------------------------------------------------------- #
# Action-gating object detection (prereg section 7)
# --------------------------------------------------------------------------- #

def detect_objects(pages: list[dict[str, Any]], root_url: str) -> list[dict[str, Any]]:
    """One candidate action-gating object per (page, form) or per state-bearing page.

    A page/form becomes an action-gating object if and only if it satisfies at least one
    of the three frozen prereg 4.2 C2 branches:

      (a) a non-GET verb WITH token/state  -> gating_type csrf_token | session_cookie
      (b) BFS depth >= 2 from the root     -> gating_type multi_step
      (c) a state-dependent response       -> gating_type state_dependent

    A non-GET form with no token, no state and a shallow path satisfies none of the
    three branches and is therefore NOT an action-gating object. Counting it would
    inflate C2, so it is recorded as a non-gating write action instead.

    gating_type vocabulary is exactly the prereg 7 list:
    "csrf_token" | "session_cookie" | "multi_step" | "state_dependent" | "rotating_handle"
    """
    objects: list[dict[str, Any]] = []
    root_norm = root_url.rstrip("/")
    non_gating_writes: list[dict[str, Any]] = []

    for page in pages:
        url = page["url"]
        depth = page["depth"]
        path_from_root = url.rstrip("/") == root_norm
        set_cookies = sorted(page.get("set_cookies") or [])

        for form in page.get("forms", []):
            method = form["method"]
            token_fields = form.get("token_fields") or []
            is_nonget = method in NONGET_METHODS
            deep = depth >= MIN_OBJECT_MULTISTEP_HOPS

            branch_a = bool(is_nonget and (token_fields or set_cookies))
            branch_b = bool(deep)
            if not (branch_a or branch_b):
                if is_nonget:
                    non_gating_writes.append({
                        "page_url": url, "path_length": depth, "method": method,
                        "action": form["action"],
                        "why_not_gating": "non-GET verb with no token-named field, no session "
                                          "state, and BFS depth < 2: satisfies none of C2 (a)(b)(c)",
                    })
                continue

            if token_fields:
                gating_type = "csrf_token"
            elif is_nonget and set_cookies:
                gating_type = "session_cookie"
            elif deep:
                gating_type = "multi_step"
            else:
                gating_type = "multi_step"

            objects.append({
                "object_id": f"{page['host']}|form{form['form_index']}|{'+'.join(sorted(token_fields)) or ('session' if set_cookies else 'deep')}",
                "root_url": root_of(url),
                "page_url": url,
                "path_length": depth,
                "gating_type": gating_type,
                "c2_branches_satisfied": sorted(
                    (["a_token_or_state"] if branch_a else []) + (["b_multihop"] if branch_b else [])
                ),
                "required_action": {
                    "method": method,
                    "url_template": form["action"],
                    "required_fields": form["input_names"],
                    "token_fields": token_fields,
                    "state_dependencies": set_cookies,
                },
                "ground_truth_verifier": "form_echo_token_match" if token_fields else "form_echo_field_match",
                "form_html_sha256": form["html_sha256"],
                "declared_in_root_observation": path_from_root,
                "detected_from": f"bfs_depth_{depth}",
            })

        # (c) state-dependent response: same URL, different content on repeat GET inside
        # one session. Cookie-setting alone is NOT a state-dependent response, so a page
        # is only registered here when the repeat hash actually differs.
        if page.get("repeat_hash_differs"):
            objects.append({
                "object_id": f"{page['host']}|state|{page['body_sha256'][:12]}",
                "root_url": root_of(url),
                "page_url": url,
                "path_length": depth,
                "gating_type": "state_dependent",
                "c2_branches_satisfied": ["c_state_dependent"],
                "required_action": {
                    "method": "GET",
                    "url_template": url,
                    "required_fields": [],
                    "token_fields": [],
                    "state_dependencies": set_cookies,
                },
                "ground_truth_verifier": "repeat_get_content_state_match",
                "form_html_sha256": "",
                "declared_in_root_observation": path_from_root,
                "detected_from": f"bfs_depth_{depth}_state",
            })

    best: dict[str, dict[str, Any]] = {}
    for o in objects:
        cur = best.get(o["object_id"])
        if cur is None or o["path_length"] < cur["path_length"]:
            best[o["object_id"]] = o
    out = list(best.values())
    out.sort(key=lambda o: (o["path_length"], o["object_id"]))
    for i, o in enumerate(out):
        o["object_index"] = i
    detect_objects.last_non_gating_writes = non_gating_writes  # type: ignore[attr-defined]
    return out


# --------------------------------------------------------------------------- #
# prereg 11: deterministic re-derivable classification
# --------------------------------------------------------------------------- #

def classify_rederivable(obj: dict[str, Any], root_page: dict[str, Any]) -> dict[str, Any]:
    """Can `required_action` be constructed from ONE unconditional GET of the root alone?

    Frozen protocol, prereg section 11 steps 1-5. The classification is fixed per object
    and is identical for every arm and every episode.
    """
    root_url = root_page["url"]
    root_forms = root_page.get("forms", [])
    root_html = root_page.get("html", "")
    reasons: list[str] = []
    rederivable = True

    page_is_root = obj["page_url"].rstrip("/") == root_url.rstrip("/")
    if not page_is_root:
        rederivable = False
        reasons.append(
            f"action is declared on {obj['page_url']} at BFS depth {obj['path_length']}; "
            "a single unconditional GET of the root does not contain this URL"
        )

    method = obj["required_action"]["method"]
    if method in NONGET_METHODS:
        root_matches = [
            f for f in root_forms
            if f["method"] == method and f["action"].rstrip("/") == obj["required_action"]["url_template"].rstrip("/")
        ]
        if not root_matches and not page_is_root:
            rederivable = False
            reasons.append(
                f"non-GET action {method} {obj['required_action']['url_template']} is not declared in the root document"
            )
        elif root_matches:
            reasons.append(f"non-GET action {method} is declared as a <form> in the root observation")

    # Token values: a named token field is not enough. The VALUE must be in the root body.
    for tf in obj["required_action"].get("token_fields") or []:
        if not page_is_root:
            rederivable = False
            reasons.append(f"token field {tf!r} is only obtainable from a non-root page")
            continue
        m = re.search(
            r"<input[^>]*name=[\"']" + re.escape(tf) + r"[\"'][^>]*value=[\"']([^\"']*)[\"']",
            root_html, re.IGNORECASE,
        )
        if m and m.group(1).strip():
            reasons.append(f"token field {tf!r} carries a literal value in the root body")
        else:
            rederivable = False
            reasons.append(
                f"token field {tf!r} has no value in the root body; its value is minted server-side "
                "and cannot be obtained from one unconditional GET of the root"
            )

    # Session-cookie state dependencies.
    for dep in obj["required_action"].get("state_dependencies") or []:
        name = dep.split("=", 1)[0].strip()
        if not page_is_root:
            rederivable = False
            reasons.append(
                f"state dependency {name!r} is set by a request other than the root GET"
            )
        elif obj["gating_type"] == "state_dependent" and not rederivable:
            reasons.append(f"state dependency {name!r} is minted per-session, not derivable from the root")
        else:
            reasons.append(f"state dependency {name!r} is set by the root GET itself")

    if rederivable and not reasons:
        reasons.append("required_action fully constructible from a single unconditional GET of the root")

    return {
        "object_id": obj["object_id"],
        "gating_type": obj["gating_type"],
        "path_length": obj["path_length"],
        "method": obj["required_action"]["method"],
        "rederivable": bool(rederivable),
        "reasons": reasons,
    }


# --------------------------------------------------------------------------- #
# prereg 4.2: the screen
# --------------------------------------------------------------------------- #

def screen_site(url: str, http_pages: JsonlWriter, http_raw: JsonlWriter, cache: ResponseCache,
                label: str, root_obs: str | None = None) -> dict[str, Any]:
    """Apply C1-C7 to one site and return the per-criterion record.

    `root_obs` is the URL treated as "the root observation" from which re-derivability is
    judged (prereg 11). It defaults to the host root. For the frozen calibration site the
    prereg's own section 4.1 describes https://httpbin.org/forms/post as the endpoint that
    itself "returns an HTML form", so there root_obs is that URL, not the host root.
    """
    root = root_obs or root_of(url)
    sess = HttpSubstrate(cookies=True, label=label, cache=cache, cache_key_prefix=f"{label}|session")
    stateless = HttpSubstrate(cookies=False, label=label + "-stateless")
    pages: list[dict[str, Any]] = []
    visited: set[str] = set()
    notes: list[str] = []

    def record(resp, kind: str) -> None:
        ev = resp.evidence()
        ev["kind"] = kind
        http_raw.write(ev)
        cache.put(resp, f"{label}:{kind}")

    # --- root fetch ------------------------------------------------------- #
    r_root = sess.fetch(root)
    record(r_root, "root")
    reachable = r_root.status_code is not None
    c6 = {
        "reachable": reachable,
        "status_code": r_root.status_code,
        "content_type": r_root.content_type,
        "is_html": ("html" in r_root.content_type) or r_root.text.lstrip()[:1] == "<",
        "error": r_root.error,
        "pass": bool(reachable and r_root.status_code == 200
                     and (("html" in r_root.content_type) or r_root.text.lstrip()[:1] == "<")),
    }

    out: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "url": url,
        "root_url": root,
        "label": label,
        "C6": c6,
        "C7": None,
        "C1": None, "C2": None, "C3": None, "C4": None, "C5": None,
        "qualifies": False,
        "pages_fetched": 0,
        "http_requests": 0,
        "notes": notes,
        "error": r_root.error,
    }

    if not reachable or not c6["is_html"]:
        notes.append(
            f"C6 FAIL: root not usable as an HTML observation "
            f"(status={r_root.status_code}, content_type={r_root.content_type!r}, error={r_root.error!r})"
        )
        for c in ("C1", "C2", "C3", "C4", "C5"):
            out[c] = {"pass": False, "reason": "C6 failed; criteria evaluated on an unusable root observation"}
        out["C7"] = {"pass": False, "reason": "C6 failed"}
        out["http_requests"] = sess.requests
        return out

    host = urllib.parse.urlparse(root).netloc.lower()

    # --- C1: root returns parseable HTML with a form or actionable link ----- #
    root_forms = parse_forms(r_root.text, r_root.final_url)
    root_links = parse_links(r_root.text, r_root.final_url)
    actionable = [l for l in root_links if not ASSET_RE.search(l["href"])]
    out["C1"] = {
        "forms_found": len(root_forms),
        "links_found": len(root_links),
        "actionable_links": len(actionable),
        "pass": bool(root_forms or actionable),
        "reason": (
            f"{len(root_forms)} <form> element(s), {len(root_links)} <a> href(s) "
            f"({len(actionable)} non-asset) in the root observation"
        ),
    }

    # --- C7: no auth required --------------------------------------------- #
    login_wall = bool(redirected_to_login(r_root.final_url)) or bool(
        re.search(r"(login|sign\s*in|authenticate)", r_root.text[:2000], re.IGNORECASE)
        and r_root.status_code in (401, 403)
    )
    out["C7"] = {
        "pass": bool(r_root.status_code == 200 and not login_wall),
        "authorization_header_sent": False,
        "final_url": r_root.final_url,
        "login_wall_detected": login_wall,
        "reason": "root reachable with no Authorization header and no login redirect"
        if r_root.status_code == 200 and not login_wall
        else f"root status {r_root.status_code}, login wall {login_wall}",
    }

    # --- BFS to discover deeper structure (C2/C4/C5) ----------------------- #
    queue: list[tuple[str, int]] = [(root, 0)]
    while queue and len(pages) < PAGE_CAP:
        cur, depth = queue.pop(0)
        if cur in visited:
            continue
        visited.add(cur)
        if depth == 0:
            resp = r_root
        else:
            resp = sess.fetch(cur)
            record(resp, f"bfs{depth}")
        body = resp.text
        forms = parse_forms(body, resp.final_url)
        links = parse_links(body, resp.final_url)
        set_cookies = []
        for k, v in resp.headers.items():
            if k.lower() == "set-cookie":
                set_cookies.append(v.split("=", 1)[0])
        hints = script_form_hints(body)
        page = {
            "experiment_id": EXPERIMENT_ID,
            "url": resp.final_url or cur,
            "requested_url": cur,
            "host": host,
            "depth": depth,
            "status_code": resp.status_code,
            "content_type": resp.content_type,
            "body_sha256": resp.body_sha256,
            "body_bytes": len(resp.body),
            "n_forms": len(forms),
            "n_links": len(links),
            "form_methods": sorted({f["method"] for f in forms}),
            "token_fields": sorted({t for f in forms for t in f["token_fields"]}),
            "set_cookies": sorted(set(set_cookies)),
            "cookie_names_after": sess.cookie_names(),
            "script_hints": hints,
            "html": body,
            "forms": [{**f, "set_cookie_on_page": sorted(set(set_cookies))} for f in forms],
        }

        # C5 probe: repeat GET of the same URL, second time inside the same session.
        if len(pages) < 6:  # bound the extra request budget
            r2 = sess.fetch(resp.final_url or cur)
            record(r2, "c5_repeat")
            page["repeat_status"] = r2.status_code
            page["repeat_hash"] = r2.body_sha256
            page["repeat_hash_differs"] = (r2.body_sha256 != resp.body_sha256)
        else:
            page["repeat_status"] = None
            page["repeat_hash"] = None
            page["repeat_hash_differs"] = None

        obs = observe(resp)
        page_record = {k: v for k, v in page.items() if k not in ("html", "forms")}
        page_record["observation_tokens"] = obs.tokens
        page_record["observation"] = obs.to_dict()
        http_pages.write(page_record)
        pages.append(page)

        if depth < MAX_DEPTH:
            n = 0
            for l in links:
                if n >= FANOUT_CAP:
                    break
                if ASSET_RE.search(l["href"]) or LOGIN_RE.search(l["href"]):
                    continue
                if not same_site(l["href"], root):
                    continue
                if l["href"].split("#")[0] in visited:
                    continue
                queue.append((l["href"].split("#")[0], depth + 1))
                n += 1

    # --- object detection (prereg 7) -------------------------------------- #
    objects = detect_objects(pages, root)
    for o in objects:
        o["site_url"] = url

    nonget_token_forms = [f for p in pages for f in p["forms"]
                          if f["method"] in NONGET_METHODS and f["has_token_field"]]
    nonget_forms = [f for p in pages for f in p["forms"] if f["method"] in NONGET_METHODS]
    deep_objects = [o for o in objects if o["path_length"] >= MIN_OBJECT_MULTISTEP_HOPS]
    state_objects = [o for o in objects if o["gating_type"] in ("state_dependent", "session_cookie", "rotating_handle")]

    out["C3"] = {
        "nonget_forms": len(nonget_forms),
        "nonget_forms_with_token_named_input": len(nonget_token_forms),
        "token_field_names": sorted({t for f in nonget_token_forms for t in f["token_fields"]}),
        "pass": bool(len(nonget_token_forms) >= MIN_TOKEN_NAME_MATCHES),
        "reason": (
            f"{len(nonget_token_forms)} form(s) declare a non-GET verb AND an input named "
            f"csrf|token|nonce|_token; token field names seen: "
            f"{sorted({t for f in nonget_token_forms for t in f['token_fields']}) or 'none'}"
        ),
    }
    out["C4"] = {
        "deep_objects": len(deep_objects),
        "max_depth_reached": max([p["depth"] for p in pages], default=0),
        "pass": bool(len(deep_objects) >= 1),
        "reason": (
            f"{len(deep_objects)} action-gating object(s) sit at BFS depth >= {MIN_OBJECT_MULTISTEP_HOPS} "
            f"from the root; BFS reached depth {max([p['depth'] for p in pages], default=0)}"
        ),
    }
    repeat_probes = [p for p in pages if p.get("repeat_hash_differs") is not None]
    c5_pass = any(p["repeat_hash_differs"] for p in repeat_probes)
    strict = [p for p in repeat_probes if p["repeat_hash_differs"] and p["set_cookies"]]
    out["C5"] = {
        "probes": len(repeat_probes),
        "hash_differs_count": sum(1 for p in repeat_probes if p["repeat_hash_differs"]),
        "pass": bool(c5_pass),
        "strict_pass_cookie_and_differs": bool(strict),
        "strict_pass_urls": [p["url"] for p in strict],
        "reason": (
            f"{sum(1 for p in repeat_probes if p['repeat_hash_differs'])}/{len(repeat_probes)} "
            "same-URL repeat GETs returned a different body sha256 within one session; "
            f"{len(strict)} of those pages also set a cookie (strict state-dependent variant)"
        ),
    }
    by_type = {t: sum(1 for o in objects if o["gating_type"] == t)
               for t in sorted({o["gating_type"] for o in objects})}
    out["C2"] = {
        "objects_detected": len(objects),
        "threshold": MIN_GATING_OBJECTS,
        "by_type": by_type,
        "state_or_session_objects": len(state_objects),
        "pass": bool(len(objects) >= MIN_GATING_OBJECTS),
        "reason": (
            f"{len(objects)} action-gating object(s) detected (threshold {MIN_GATING_OBJECTS}); "
            f"by gating_type: {by_type or '{}'}"
        ),
    }

    out["qualifies"] = all(out[c]["pass"] for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"))
    out["pages_fetched"] = len(pages)
    out["http_requests"] = sess.requests
    out["page_urls"] = [p["url"] for p in pages]
    out["depths"] = [p["depth"] for p in pages]
    out["object_count"] = len(objects)

    missing = []
    if not out["C3"]["pass"]:
        missing.append("a declared non-GET form with an input named csrf|token|nonce|_token")
    if not out["C4"]["pass"]:
        missing.append("an action-gating object at >= 2 hops from the root")
    if not out["C5"]["pass"]:
        missing.append("a same-URL content change on repeat GET within one session")
    if not out["C2"]["pass"]:
        missing.append(f"{MIN_GATING_OBJECTS} or more action-gating objects")
    out["missing_ingredients"] = missing
    out["non_gating_write_actions"] = getattr(detect_objects, "last_non_gating_writes", [])
    out["_objects"] = objects
    out["_pages"] = pages
    return out


def redirected_to_login(url: str) -> bool:
    return bool(LOGIN_RE.search(urllib.parse.urlparse(url).path or ""))


# --------------------------------------------------------------------------- #
# Identifier inventory (prereg: identifier_classification_log)
# --------------------------------------------------------------------------- #

IDENT_PATTERNS = {
    "hidden_form_token": re.compile(
        r"<input[^>]*type=[\"']?hidden[\"']?[^>]*name=[\"']([^\"']*(?:csrf|token|nonce|authenticity)[^\"']*)[\"'][^>]*value=[\"']([^\"']*)[\"']",
        re.IGNORECASE),
    "named_token_input": re.compile(
        r"<input[^>]*name=[\"']([^\"']*(?:csrf|token|nonce)[^\"']*)[\"'][^>]*value=[\"']([^\"']*)[\"']",
        re.IGNORECASE),
    "session_cookie": re.compile(r"(?:^|[\s,;])([A-Za-z0-9_]+)=([^;,\s]+)"),
    "url_path_id": re.compile(r"/(?:id|item|post|doc|resource|user)/([A-Za-z0-9._-]{4,})"),
    "json_id_field": re.compile(r"\"(?:id|uuid|token|key|session|nonce)\"\s*:\s*\"([^\"]{4,})"),
}


def classify_identifiers(pages: list[dict[str, Any]], site_url: str, episode: str,
                         writer: JsonlWriter) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for page in pages:
        html = page.get("html", "")
        for kind, pat in IDENT_PATTERNS.items():
            if kind == "session_cookie":
                continue
            for m in pat.finditer(html):
                name, val = (m.group(1), m.group(2)) if m.lastindex and m.lastindex >= 2 else ("", m.group(1))
                if not val:
                    continue
                key = (kind, val)
                if key in seen:
                    continue
                seen.add(key)
                rec = {
                    "experiment_id": EXPERIMENT_ID,
                    "site": site_url,
                    "episode": episode,
                    "page_url": page["url"],
                    "page_depth": page["depth"],
                    "identifier_type": kind,
                    "subtype": name[:80],
                    "value_sha256": sha256_hex(val),
                    "value_prefix": val[:24],
                    "value_len": len(val),
                    "source": "root" if page["depth"] == 0 else f"bfs_depth_{page['depth']}",
                    "in_root_observation": page["depth"] == 0,
                    "stability": "session_scoped" if kind in ("hidden_form_token", "named_token_input", "session_cookie")
                    else "site_resource_id",
                }
                found.append(rec)
                writer.write(rec)
    return found
