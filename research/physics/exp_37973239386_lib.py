"""EXP-PHYSICS-37973239386 EXECUTE library.

Frozen design: research/experiments/EXP-PHYSICS-37973239386/{spec.json,prereg.md,request.json}.
Implements, exactly and without retuning after outcomes:
  * credential-free stdlib-HTTP fresh-session collection of the frozen 57-endpoint universe,
  * the frozen action-gating taxonomy and admission criterion,
  * the frozen 11-rule armed family + 3 baseline predictors,
  * the frozen calibrated irreducibility null and planted positive-control batteries,
  * the site-clustered bootstrap and the frozen branch precedence.

Only stdlib. No JavaScript, no credentials, no non-GET, no third-party packages.
"""

from __future__ import annotations

import base64
import hashlib
import http.cookiejar
import json
import random
import re
import time
import urllib.error
import urllib.request
import uuid
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Frozen constants (mirrored verbatim from spec.json / prereg.md)
# ---------------------------------------------------------------------------

MASTER_SEED = 2450671238  # int(request_hash[:8],16); request_hash 92124686...

# Fixed User-Agent (spec requires a single fixed UA; exact string is an EXECUTE
# implementation choice). A plain identifying research UA is used deliberately:
# full browser-like UAs are rejected 403/406 by Cloudflare on gitlab.gnome.org,
# codeberg.org and others, while research-style UAs are served routinely.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; research) "
    "SPIDER-Research2.0/EXP-PHYSICS-37973239386"
)

K_SESSIONS = 8
J_REQUESTS = 3
N_MIN_OBS = 4
BODY_CAP = 600000
TIMEOUT = 20.0

P_FLOOR = 0.10
P_HI = 0.25
ALPHA_RULE = 0.05
PC_POWER_MIN = 0.8
NULL_FP_MAX = 0.05
DELTA_MEM = 0.10
M_MIN_FIELDS = 20
S_MIN_SITES = 8
TRANSPORT_ERROR_MAX = 0.30
BOOTSTRAP_RESAMPLES = 10000

TAXONOMY = {
    "SESSION": re.compile(
        r"session|sessid|sid|jsessionid|phpsessid|asp.net_sessionid|connect\.sid|"
        r"_forum_session|authsession|auth_session|laravel_session|ci_session|"
        r"codeigniter|symfony|rack\.session|gitea|i_like_gitea|play_session",
        re.IGNORECASE,
    ),
    "CSRF": re.compile(
        r"csrf|xsrf|_token|authenticity|csrftoken|csrfmiddlewaretoken|"
        r"__RequestVerificationToken",
        re.IGNORECASE,
    ),
    "TOKEN": re.compile(r"token", re.IGNORECASE),
    "NONCE": re.compile(r"nonce", re.IGNORECASE),
}

EXCLUDED = re.compile(
    r"_ga|_gid|_gat|_gcl|_fbp|_fbc|__cf_bm|_cfuvid|ajs_|atlcohort|_abck|bm_sz|"
    r"^cid$|euid|_v-visitor|GU_|gu_|WMF-Uniq|LAST_NEWS|kndctr|cfz_|X-Experiments|"
    r"Optanon|CookieConsent|cookieyes|moove_|_hp2|_uet|_pin_unauth|_pinterest|"
    r"IDE|NID|1P_JAR|CONSENT|_twpid|mp_|_mkto|__hstc|__hssc|__hssrc|hubspotutk|"
    r"intercom|amplitude|ajs_user|segment|mixpanel|heap|_clck|_clsk",
    re.IGNORECASE,
)

BASELINE_IDS = ["B_MEMORY_REPEAT", "B_MARKOV1", "B_CONSTANT_MODE", "B_IRREDUCIBILITY_NULL"]
PC_ID = "PC_PLANTED_CLASSES"
NULL_ID = "NC_PLANTED_RANDOM_PLUS_LIVE"

ARMED_RULES = [
    "R_INT_INCR",
    "R_HEX_INCR",
    "R_B62_INCR",
    "R_PREFIX_COUNTER",
    "R_ORDER_LINEAR",
    "R_SESSION_BIND",
    "R_HASH_BIND",
    "R_WALLCLOCK_DEC",
    "R_WALLCLOCK_HEX",
    "R_WALLCLOCK_B64",
    "R_CONST_SUBSTRING",
]

# class attribution priority (frozen)
CLASS_PRIORITY = [
    ("R_SESSION_BIND", "SESSION_BIND"),
    ("R_HASH_BIND", "HASH_BIND"),
    ("R_WALLCLOCK_B64", "WALLCLOCK_B64"),
    ("R_WALLCLOCK_HEX", "WALLCLOCK_HEX"),
    ("R_WALLCLOCK_DEC", "WALLCLOCK_DEC"),
    ("R_INT_INCR", "INT_INCR"),
    ("R_PREFIX_COUNTER", "PREFIX_COUNTER"),
    ("R_HEX_INCR", "HEX_INCR"),
    ("R_ORDER_LINEAR", "ORDER_LINEAR"),
    ("R_B62_INCR", "B62_INCR"),
    ("R_CONST_SUBSTRING", "CONST_SUBSTRING"),
]

B62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
NULL_REGIMES = ["uuid4", "hex32", "hex64", "b64_16", "b64_32", "b62_20", "b62_43", "dec16"]
NULL_N_FIELDS_PER_REGIME = 200
NULL_N_OBS = 12
NULL_EPOCH0 = 1760000000
NULL_SEED_BASE = 9000
PC_N_TRIALS = 200
PC_SEED_BASE = 5000
PC_N_OBS_CHOICES = [8, 10, 12]


# ---------------------------------------------------------------------------
# HTML parsing
# ---------------------------------------------------------------------------


class _FieldHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.inputs: list[dict] = []
        self.metas: list[dict] = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): v for k, v in attrs}
        if tag == "input" and (a.get("type") or "").lower() == "hidden":
            self.inputs.append({"name": a.get("name"), "value": a.get("value")})
        elif tag == "meta":
            self.metas.append({"name": a.get("name"), "content": a.get("content")})


def parse_html_fields(body_bytes: bytes) -> dict:
    """Extract hidden inputs and meta name->content fields.

    Multiple elements with the same name are collapsed to the FIRST occurrence in
    document order (deterministic representation choice; documented as loss).
    """
    try:
        text = body_bytes.decode("utf-8", "replace")
    except Exception:
        text = body_bytes.decode("latin-1", "replace")
    p = _FieldHTMLParser()
    try:
        p.feed(text)
    except Exception:
        pass
    out = {"input.hidden": {}, "meta": {}}
    for e in p.inputs:
        n = e.get("name")
        v = e.get("value")
        if n and v is not None and n not in out["input.hidden"]:
            out["input.hidden"][n] = v
    for e in p.metas:
        n = e.get("name")
        v = e.get("content")
        if n and v is not None and n not in out["meta"]:
            out["meta"][n] = v
    return out


# ---------------------------------------------------------------------------
# Taxonomy / admission
# ---------------------------------------------------------------------------


def name_class(locator_type: str, name: str):
    """Return frozen action-gating class or None. NONCE is meta-only in practice."""
    if EXCLUDED.search(name):
        return None
    if locator_type == "cookie":
        for cls in ("SESSION", "CSRF", "TOKEN"):
            if TAXONOMY[cls].search(name):
                return cls
        return None
    if locator_type == "input.hidden":
        for cls in ("CSRF", "TOKEN", "SESSION"):
            if TAXONOMY[cls].search(name):
                return cls
        return None
    if locator_type == "meta":
        for cls in ("CSRF", "NONCE", "TOKEN", "SESSION"):
            if TAXONOMY[cls].search(name):
                return cls
        return None
    return None


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------


def _collect_one_session(endpoint: str, session_index: int) -> dict:
    """K sessions are independent; each session issues J GETs of the same URL."""
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    observations = []
    for req_index in range(J_REQUESTS):
        rec = {
            "endpoint": endpoint,
            "session_index": session_index,
            "request_index": req_index,
            "transport_error": None,
            "status": None,
            "epoch": time.time(),
            "final_url": endpoint,
            "body_sha256": None,
            "fields": [],
            "cookies": {},
        }
        try:
            req = urllib.request.Request(endpoint, method="GET", headers={"User-Agent": USER_AGENT})
            with opener.open(req, timeout=TIMEOUT) as resp:
                body = resp.read(BODY_CAP)
                rec["status"] = resp.status
                rec["final_url"] = resp.geturl()
            rec["body_sha256"] = hashlib.sha256(body).hexdigest()
            parsed = parse_html_fields(body)
            fields = []
            for lt in ("input.hidden", "meta"):
                for n, v in parsed[lt].items():
                    if name_class(lt, n):
                        fields.append({"locator_type": lt, "name": n, "value": v})
            # cookie fields from the jar after processing the response
            cookies = {}
            if jar is not None:
                for c in jar:
                    cookies[c.name] = c.value
            for n, v in cookies.items():
                if name_class("cookie", n):
                    fields.append({"locator_type": "cookie", "name": n, "value": v})
            rec["fields"] = fields
            rec["cookies"] = cookies
        except urllib.error.HTTPError as e:  # an HTTP response, not a transport error
            try:
                body = e.read(BODY_CAP)
            except Exception:
                body = b""
            rec["status"] = e.code
            rec["body_sha256"] = hashlib.sha256(body).hexdigest()
            parsed = parse_html_fields(body)
            fields = []
            for lt in ("input.hidden", "meta"):
                for n, v in parsed[lt].items():
                    if name_class(lt, n):
                        fields.append({"locator_type": lt, "name": n, "value": v})
            cookies = {}
            for c in jar:
                cookies[c.name] = c.value
            for n, v in cookies.items():
                if name_class("cookie", n):
                    fields.append({"locator_type": "cookie", "name": n, "value": v})
            rec["fields"] = fields
            rec["cookies"] = cookies
        except Exception as e:  # transport / timeout / TLS / DNS
            rec["transport_error"] = f"{type(e).__name__}: {str(e)[:200]}"
        observations.append(rec)
    return {"endpoint": endpoint, "session_index": session_index, "observations": observations}


# ---------------------------------------------------------------------------
# Rule family
# ---------------------------------------------------------------------------


def _parse_int_dec(s):
    if isinstance(s, int):
        return s
    if not isinstance(s, str):
        return None
    t = s.strip()
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    return None


def _parse_int_hex(s):
    if not isinstance(s, str):
        return None
    t = s.strip()
    if re.fullmatch(r"[0-9a-fA-F]+", t):
        return int(t, 16)
    return None


def decode_b62(s):
    if not isinstance(s, str) or not s:
        return None
    v = 0
    for ch in s:
        idx = B62_ALPHABET.find(ch)
        if idx < 0:
            return None
        v = v * 62 + idx
    return v


def _constant_delta_frac(ints):
    n = len(ints)
    if n < 2:
        return None
    deltas = [ints[i] - ints[i - 1] for i in range(1, n)]
    d = deltas[0]
    if d == 0:
        return None
    if all(x == d for x in deltas):
        return 1.0
    return None


def _wallclock_bound(sub, epoch):
    try:
        val = int(sub)
    except Exception:
        return False
    for scale in (1.0, 1000.0):
        try:
            if abs(val / scale - epoch) <= 3600.0:
                return True
        except Exception:
            pass
    return False


def _filtered_cookie_maps(cookie_maps, field_name, locator_type):
    """Drop the field's OWN cookie identity so SESSION_BIND/HASH_BIND are not
    circular for cookie fields. A session cookie trivially equals itself; the rule
    is meant to detect a value bound to a DIFFERENT same-session cookie."""
    if locator_type != "cookie" or not field_name:
        return cookie_maps
    return [{k: v for k, v in cm.items() if k != field_name} for cm in cookie_maps]


def rule_fire(values, epochs, cookie_maps, field_name=None, locator_type=None):
    """Return {rule_id: detection_fraction} for every FIRING armed rule.

    detection_fraction is the rule's per-observation precision (fraction of the
    field's ordered observations on which the rule's own criterion holds). This is
    the quantity compared against B_MEMORY_REPEAT held-out accuracy.
    """
    n = len(values)
    fired = {}
    if n < 2:
        return fired
    cookie_maps = _filtered_cookie_maps(cookie_maps, field_name, locator_type)

    # R_INT_INCR
    ints = [_parse_int_dec(v) for v in values]
    if all(x is not None for x in ints):
        f = _constant_delta_frac(ints)
        if f is not None:
            fired["R_INT_INCR"] = f

    # R_HEX_INCR
    hx = [_parse_int_hex(v) for v in values]
    if all(x is not None for x in hx):
        f = _constant_delta_frac(hx)
        if f is not None:
            fired["R_HEX_INCR"] = f

    # R_B62_INCR
    b62 = [decode_b62(v) for v in values]
    if all(x is not None for x in b62):
        f = _constant_delta_frac(b62)
        if f is not None:
            fired["R_B62_INCR"] = f

    # R_PREFIX_COUNTER
    f = _prefix_counter_frac(values)
    if f is not None:
        fired["R_PREFIX_COUNTER"] = f

    # R_ORDER_LINEAR
    f = _order_linear_frac(ints)
    if f is not None:
        fired["R_ORDER_LINEAR"] = f

    # R_SESSION_BIND
    f = _session_bind_frac(values, cookie_maps)
    if f is not None:
        fired["R_SESSION_BIND"] = f

    # R_HASH_BIND
    f = _hash_bind_frac(values, cookie_maps)
    if f is not None:
        fired["R_HASH_BIND"] = f

    # Wallclock rules
    f = _wallclock_frac(values, epochs, r"\d{10,}", _wallclock_bound)
    if f is not None:
        fired["R_WALLCLOCK_DEC"] = f
    f = _wallclock_frac(values, epochs, r"[0-9a-fA-F]{8,}", _wallclock_bound)
    if f is not None:
        fired["R_WALLCLOCK_HEX"] = f
    f = _wallclock_b64_frac(values, epochs)
    if f is not None:
        fired["R_WALLCLOCK_B64"] = f

    # R_CONST_SUBSTRING
    if _const_substring_fires(values):
        fired["R_CONST_SUBSTRING"] = 1.0

    return fired


def _prefix_counter_frac(values):
    n = len(values)
    if n < 2 or any(not isinstance(v, str) for v in values):
        return None
    min_len = min(len(v) for v in values)
    if min_len < 1:
        return None
    # longest common prefix / suffix
    pref = 0
    for i in range(min_len):
        if all(v[i] == values[0][i] for v in values):
            pref += 1
        else:
            break
    suf = 0
    for i in range(min_len):
        if all(v[len(v) - 1 - i] == values[0][len(values[0]) - 1 - i] for v in values):
            suf += 1
        else:
            break
    best = None
    for p in range(pref, -1, -1):
        for q in range(suf, -1, -1):
            if p + q >= min_len:
                continue
            shell = p + q
            if shell < max(4, 0.25 * min_len):
                continue
            mids = []
            ok = True
            for v in values:
                m = v[p: len(v) - q]
                if not re.fullmatch(r"-?\d+", m):
                    ok = False
                    break
                mids.append(int(m))
            if not ok or len(mids) < 2:
                continue
            f = _constant_delta_frac(mids)
            if f is not None:
                best = f
                break
        if best is not None:
            break
    return best


def _order_linear_frac(ints):
    if any(x is None for x in ints):
        return None
    v = ints
    n = len(v)
    if n < 4:
        return None
    half = n // 2
    first = v[:half]
    if len(first) < 2:
        return None
    if first[-1] == first[0]:
        return None
    num = first[-1] - first[0]
    den = len(first) - 1
    if num % den != 0:
        return None
    b = num // den
    if b == 0:
        return None
    a = first[0]
    correct = sum(1 for i in range(n) if a + b * i == v[i])
    if correct == n:
        return 1.0
    # "reproduce the held-out second half exactly" must hold to fire
    second_ok = all(a + b * i == v[i] for i in range(half, n))
    if not second_ok:
        return None
    return correct / n


def _session_bind_value(v, cookie_values):
    for cv in cookie_values:
        if not cv:
            continue
        if v == cv:
            return True
        if v.startswith(cv) or v.endswith(cv):
            return True
        if len(cv) >= 8 and cv in v:
            return True
    return False


def _session_bind_frac(values, cookie_maps):
    bound = 0
    for v, cv in zip(values, cookie_maps):
        if _session_bind_value(v, list(cv.values())):
            bound += 1
    frac = bound / len(values)
    return frac if frac >= 0.75 else None


def _hash_bind_frac(values, cookie_maps):
    bound = 0
    for v, cv in zip(values, cookie_maps):
        hit = False
        for cvalue in cv.values():
            b = cvalue.encode("utf-8", "replace")
            for h in (hashlib.md5(b).hexdigest(), hashlib.sha1(b).hexdigest(), hashlib.sha256(b).hexdigest()):
                if v == h or v.startswith(h) or v.endswith(h):
                    hit = True
                    break
            if hit:
                break
        if hit:
            bound += 1
    frac = bound / len(values)
    return frac if frac >= 0.75 else None


def _wallclock_frac(values, epochs, pattern, bound_fn):
    fracs = []
    for v, ep in zip(values, epochs):
        if not isinstance(v, str):
            fracs.append(False)
            continue
        hit = False
        for m in re.finditer(pattern, v):
            if bound_fn(m.group(0), ep):
                hit = True
                break
        fracs.append(hit)
    frac = sum(fracs) / len(fracs)
    return frac if frac >= 0.75 else None


_B64_RE = re.compile(r"[A-Za-z0-9+/]{4,}={0,2}")


def _b64_window_hits_epoch(raw, ep):
    for off in range(0, len(raw) - 3):
        w = raw[off:off + 4]
        for order in ("big", "little"):
            val = int.from_bytes(w, order)
            for scale in (1.0, 1000.0):
                if abs(val / scale - ep) <= 3600.0:
                    return True
    return False


def _wallclock_b64_frac(values, epochs):
    fracs = []
    for v, ep in zip(values, epochs):
        if not isinstance(v, str):
            fracs.append(False)
            continue
        hit = False
        for m in _B64_RE.finditer(v):
            cand = m.group(0)
            try:
                raw = base64.b64decode(cand + "=" * (-len(cand) % 4), validate=False)
            except Exception:
                continue
            if len(raw) >= 4 and _b64_window_hits_epoch(raw, ep):
                hit = True
                break
        fracs.append(hit)
    frac = sum(fracs) / len(fracs)
    return frac if frac >= 0.75 else None


def _longest_common_substring_len(strs):
    if not strs:
        return 0
    s0 = strs[0]
    n = len(s0)
    best = 0
    # binary search on length for efficiency
    def ok(L):
        if L == 0:
            return True
        subs = {s0[i:i + L] for i in range(n - L + 1)}
        for s in strs[1:]:
            cur = {s[i:i + L] for i in range(len(s) - L + 1)}
            subs &= cur
            if not subs:
                return False
        return True

    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def _const_substring_fires(values):
    if len(values) < 2:
        return False
    if len(set(values)) < 2:
        return False
    min_len = min(len(v) for v in values)
    if min_len == 0:
        return False
    lcs = _longest_common_substring_len(list(values))
    return lcs >= max(6, 0.40 * min_len)


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------


def b_memory_repeat_acc(values):
    n = len(values)
    if n < 2:
        return 0.0
    correct = sum(1 for i in range(1, n) if values[i] == values[i - 1])
    return correct / (n - 1)


def _train_test_split(values):
    n = len(values)
    cut = max(1, int(round(0.70 * n)))
    if cut >= n:
        cut = n - 1
    return values[:cut], values[cut:]


def b_memory_repeat_holdout(values):
    train, test = _train_test_split(values)
    if not test:
        return 0.0
    correct = 0
    for i, v in enumerate(test):
        prev = test[i - 1] if i > 0 else train[-1]
        if v == prev:
            correct += 1
    return correct / len(test)


def b_markov1_acc(values):
    train, test = _train_test_split(values)
    if not test:
        return 0.0
    succ = {}
    for i in range(len(train) - 1):
        succ[train[i]] = train[i + 1]
    # training mode fallback
    mode = None
    if train:
        from collections import Counter

        mode = Counter(train).most_common(1)[0][0]
    correct = 0
    prev = train[-1]
    for v in test:
        pred = succ.get(prev, mode)
        if pred == v:
            correct += 1
        prev = v
    return correct / len(test)


def b_constant_mode_acc(values):
    train, test = _train_test_split(values)
    if not test or not train:
        return 0.0
    from collections import Counter

    mode = Counter(train).most_common(1)[0][0]
    return sum(1 for v in test if v == mode) / len(test)


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------


def _rand_hex(rng, n):
    return "".join(rng.choice("0123456789abcdef") for _ in range(n))


def _rand_b62(rng, n):
    return "".join(rng.choice(B62_ALPHABET) for _ in range(n))


def generate_null_field(regime, rng, epoch0, n_obs):
    vals, epochs = [], []
    for i in range(n_obs):
        ep = epoch0 + 30 * i
        if regime == "uuid4":
            v = str(uuid.UUID(int=rng.getrandbits(128), version=4))
        elif regime == "hex32":
            v = _rand_hex(rng, 32)
        elif regime == "hex64":
            v = _rand_hex(rng, 64)
        elif regime == "b64_16":
            v = base64.b64encode(bytes(rng.getrandbits(8) for _ in range(16))).decode()
        elif regime == "b64_32":
            v = base64.b64encode(bytes(rng.getrandbits(8) for _ in range(32))).decode()
        elif regime == "b62_20":
            v = _rand_b62(rng, 20)
        elif regime == "b62_43":
            v = _rand_b62(rng, 43)
        elif regime == "dec16":
            v = str(rng.randint(10**15, 10**16 - 1))
        else:
            raise ValueError(regime)
        vals.append(v)
        epochs.append(ep)
    # independent same-session cookie values (must not equal the field's own values)
    cookie_maps = [{"_null_session": _rand_hex(rng, 32)} for _ in range(n_obs)]
    return vals, epochs, cookie_maps


def run_null_battery():
    """Re-run the frozen irreducibility null battery. Returns per-regime fires."""
    per_regime = {}
    total_fields = 0
    total_fired = 0
    fired_by_rule = {r: 0 for r in ARMED_RULES}
    for ri, regime in enumerate(NULL_REGIMES):
        rng = random.Random(NULL_SEED_BASE + ri)
        fired = 0
        for _ in range(NULL_N_FIELDS_PER_REGIME):
            vals, epochs, cookies = generate_null_field(regime, rng, NULL_EPOCH0, NULL_N_OBS)
            fr = rule_fire(vals, epochs, cookies)
            if fr:
                fired += 1
                for r in fr:
                    fired_by_rule[r] += 1
            total_fields += 1
        per_regime[regime] = {"fields": NULL_N_FIELDS_PER_REGIME, "fields_fired": fired}
        total_fired += fired
    per_rule_fp = {r: fired_by_rule[r] / total_fields for r in ARMED_RULES}
    armed = {r: (per_rule_fp[r] <= ALPHA_RULE) for r in ARMED_RULES}
    return {
        "fields_total": total_fields,
        "fields_fired": total_fired,
        "aggregate_fp": total_fired / total_fields,
        "per_rule_fp": per_rule_fp,
        "armed": armed,
        "all_armed": all(armed.values()),
        "per_regime": per_regime,
    }


def _planted_field(cls, rng, n_obs):
    vals, epochs = [], []
    sess_cookie = "cook" + _rand_hex(rng, 20)
    base_epoch = NULL_EPOCH0 + rng.randint(0, 10**6)
    start = rng.randint(10**6, 10**9)
    shell = "PFX" + _rand_b62(rng, 5)
    for i in range(n_obs):
        ep = base_epoch + 30 * i
        if cls == "P_INT_INCR":
            v = str(start + 7 * i)
        elif cls == "P_HEX_INCR":
            v = format(start + 3 * i, "x")
        elif cls == "P_PREFIX_COUNTER":
            v = f"{shell}{start + 5 * i:08d}END"
        elif cls == "P_DEC_TS":
            v = str(base_epoch + 30 * i)
        elif cls == "P_HEX_TS":
            v = format(base_epoch + 30 * i, "x")
        elif cls == "P_B64_TS":
            v = base64.b64encode((base_epoch + 30 * i).to_bytes(6, "big")).decode()
        elif cls == "P_SESSION_BIND":
            v = sess_cookie
        elif cls == "P_HASH_BIND":
            v = hashlib.sha256(sess_cookie.encode()).hexdigest()
        else:
            raise ValueError(cls)
        vals.append(v)
        epochs.append(ep)
    cookies = [{"cookie": sess_cookie} for _ in range(n_obs)]
    return vals, epochs, cookies


PC_CLASSES = [
    "P_INT_INCR",
    "P_HEX_INCR",
    "P_PREFIX_COUNTER",
    "P_DEC_TS",
    "P_HEX_TS",
    "P_B64_TS",
    "P_SESSION_BIND",
    "P_HASH_BIND",
]


def run_positive_control():
    classes = {}
    for cls in PC_CLASSES:
        detected = 0
        for t in range(PC_N_TRIALS):
            rng = random.Random(PC_SEED_BASE + t)
            n_obs = PC_N_OBS_CHOICES[t % len(PC_N_OBS_CHOICES)]
            vals, epochs, cookies = _planted_field(cls, rng, n_obs)
            if rule_fire(vals, epochs, cookies):
                detected += 1
        classes[cls] = {"trials": PC_N_TRIALS, "detected": detected, "power": detected / PC_N_TRIALS}
    return {
        "trials_per_class": PC_N_TRIALS,
        "classes": classes,
        "power_min": min(c["power"] for c in classes.values()),
    }


def run_live_null_uuid(k_sessions=8):
    """Out-of-author live random source: GET https://httpbin.org/uuid."""
    url = "https://httpbin.org/uuid"
    fields = []  # one field per session, >=12 values
    raw = []
    for s in range(k_sessions):
        vals = []
        errs = 0
        while len(vals) < 12 and errs < 6:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                    data = json.loads(r.read(4096).decode("utf-8", "replace"))
                u = data.get("uuid")
                if u:
                    vals.append(u)
                else:
                    errs += 1
            except Exception:
                errs += 1
        if len(vals) >= 12:
            epochs = [time.time() for _ in vals]
            # httpbin /uuid sets no cookies: the correct same-session cookie map is
            # empty. (An earlier construction that inserted each uuid as its own
            # cookie value self-bound R_SESSION_BIND vacuously; preserved in
            # derived/controls_initial_live_null_selfbind_bug.json.)
            cookies = [{} for _ in vals]
            fired = rule_fire(vals, epochs, cookies)
            fields.append({"session": s, "n": len(vals), "fired": bool(fired), "rules": list(fired)})
            raw.append(vals)
    n_fields = len(fields)
    fired_fields = sum(1 for f in fields if f["fired"])
    return {
        "url": url,
        "sessions_requested": k_sessions,
        "fields_collected": n_fields,
        "fields_fired": fired_fields,
        "fired_fraction": (fired_fields / n_fields) if n_fields else None,
        "per_session": fields,
    }


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def registrable_domain(host):
    host = host.lower().split(":")[0]
    labels = host.split(".")
    if len(labels) >= 2:
        return ".".join(labels[-2:])
    return host


def clustered_bootstrap(fields, n_resamples=BOOTSTRAP_RESAMPLES, seed=MASTER_SEED):
    """fields: list of dicts with 'cluster' and 'predictable' (0/1)."""
    clusters = {}
    for f in fields:
        clusters.setdefault(f["cluster"], []).append(f)
    keys = sorted(clusters.keys())
    n_clusters = len(keys)
    if n_clusters == 0:
        return {"point": None, "lo": None, "hi": None, "n_clusters": 0, "distinct_resamples": 0, "informative": False}
    if n_clusters == 1:
        vals = clusters[keys[0]]
        pred = sum(f["predictable"] for f in vals)
        point = pred / len(vals)
        return {"point": point, "lo": point, "hi": point, "n_clusters": 1, "distinct_resamples": 1, "informative": False}

    rng = random.Random(seed ^ 0xB007)
    point_num = sum(f["predictable"] for f in fields)
    point = point_num / len(fields)
    estimates = []
    seen = set()
    for _ in range(n_resamples):
        drawn = [keys[rng.randrange(n_clusters)] for _ in range(n_clusters)]
        seen.add(tuple(sorted(drawn)))
        num = 0
        den = 0
        for k in drawn:
            for f in clusters[k]:
                den += 1
                num += f["predictable"]
        estimates.append(num / den if den else 0.0)
    estimates.sort()
    lo = estimates[int(0.025 * len(estimates))]
    hi = estimates[min(len(estimates) - 1, int(0.975 * len(estimates)))]
    return {
        "point": point,
        "lo": lo,
        "hi": hi,
        "n_clusters": n_clusters,
        "distinct_resamples": len(seen),
        "informative": len(seen) >= 1000,
        "n_resamples": len(estimates),
    }
