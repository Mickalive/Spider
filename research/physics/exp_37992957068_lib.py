"""EXP-PHYSICS-37992957068 EXECUTE library.

Frozen design: research/experiments/EXP-PHYSICS-37992957068/{spec.json,prereg.md,request.json},
freeze.json. Implements, exactly and without retuning after outcomes:

  * credential-free stdlib-HTTP collection of the frozen 57-endpoint universe with the
    frozen 4 arms (A_RETRY / A_RETRY_SPACED / A_FRESH / A_ADAPT) and block-randomized
    arm assignment (seed 37992957068),
  * the frozen response-intrinsic classifier (pure function of a single response's fields),
  * the live oracles (PC_BARRIER_ORACLE / NC_CLEAN_ORACLE) and the offline synthetic
    controls (PC_SYNTHETIC_DYNAMICS / NC_SYNTHETIC_MEMORYLESS),
  * the frozen M_HISTORY / M_HISTORY_NOID models, the four nulls
    (B_CONSTANT / B_ENDPOINT_CONST / B_MEMORY_PERSIST / B_RATE_ONLY),
  * leave-one-session-out CV, endpoint(registrable-domain)-clustered bootstrap with
    10000 resamples (seed 37992957068), and the frozen branch precedence.

Only stdlib for collection. numpy is used only as a numerical accelerator for the
analysis (a documented EXECUTE implementation choice; recorded in provenance.json).
No JavaScript, no credentials, no non-GET, no model calls.
"""

from __future__ import annotations

import http.cookiejar
import json
import math
import random
import re
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter
from urllib.parse import urlparse

import numpy as np

# ---------------------------------------------------------------------------
# Frozen constants, mirrored verbatim from spec.json / prereg.md
# ---------------------------------------------------------------------------

EXPERIMENT_ID = "EXP-PHYSICS-37992957068"
LANE = "physics"
CLAIM_IDS = ["C-WEB-DYNAMICS"]

SEED_ASSIGNMENT = 37992957068
SEED_BOOTSTRAP = 37992957068
SEED_PC_SYNTHETIC = 37992957068
SEED_NC_SYNTHETIC = 37992957069

J_MAX = 5
SESSIONS_PER_ENDPOINT = 12
ARMS = ["A_RETRY", "A_RETRY_SPACED", "A_FRESH", "A_ADAPT"]

DELTA_SKILL_NATS = 0.05
ALPHA = 0.05
MARGIN_SUCCESS = 0.05
PC_POWER_MIN = 0.80
NC_FP_MAX = 0.05
MIN_BARRIER_EXPOSED_ENDPOINTS = 3
MIN_SCHEDULER_BARRIER_EVENTS = 30

BOOTSTRAP_N = 10000
RIDGE_LAMBDA = 1.0  # L2 penalty on standardised (non-intercept) coefficients
IRLS_MAX_ITERS = 60
IRLS_TOL = 1e-8
PROB_EPS = 1e-9

# Frozen (EXECUTE-recorded) single request identity; no credentials, GET only.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; research) "
    "SPIDER-Research2.0/EXP-PHYSICS-37992957068"
)
ACCEPT_HEADER = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
HTTP_TIMEOUT_S = 15.0

# Frozen intrinsic classifier: challenge-marker regex recorded here by EXECUTE
# (prereg.md delegates the literal regex to EXECUTE as "the frozen challenge-marker
# regex recorded in prereg.md"; the semantic content is the Cloudflare interstitial /
# captcha family).
CHALLENGE_MARKER_RE = re.compile(
    r"(?i)("
    r"just a moment"
    r"|cf-browser-verification"
    r"|cf[-_]chl[-_]"
    r"|challenge-platform"
    r"|cf-challenge"
    r"|cdn-cgi/challenge"
    r"|attention required"
    r"|checking your browser"
    r"|enable javascript and cookies"
    r"|verify you are human"
    r"|please complete the security check"
    r"|g-recaptcha"
    r"|hcaptcha"
    r"|recaptcha"
    r"|cf-turnstile"
    r"|<title>\s*just a moment"
    r")"
)

CLASS_CLEAN = "CLEAN"
CLASS_RATE_LIMIT_429 = "RATE_LIMIT_429"
CLASS_BLOCK_403_CHALLENGE = "BLOCK_403_CHALLENGE"
CLASS_UNAVAILABLE_403 = "UNAVAILABLE_403"
CLASS_TRANSPORT_ERROR = "TRANSPORT_ERROR"
CLASS_OTHER_NONBARRIER = "OTHER_NONBARRIER"

ALL_CLASSES = [
    CLASS_CLEAN,
    CLASS_RATE_LIMIT_429,
    CLASS_BLOCK_403_CHALLENGE,
    CLASS_UNAVAILABLE_403,
    CLASS_TRANSPORT_ERROR,
    CLASS_OTHER_NONBARRIER,
]
BARRIER_SET = {CLASS_RATE_LIMIT_429, CLASS_BLOCK_403_CHALLENGE, CLASS_TRANSPORT_ERROR}
ORDINARY_UNAVAILABILITY_SET = {CLASS_UNAVAILABLE_403, CLASS_OTHER_NONBARRIER}
PREV_LABEL_CATEGORIES = [CLASS_CLEAN, CLASS_RATE_LIMIT_429, CLASS_BLOCK_403_CHALLENGE,
                         CLASS_UNAVAILABLE_403, CLASS_TRANSPORT_ERROR,
                         CLASS_OTHER_NONBARRIER, "NONE"]

# Frozen 57-endpoint universe (verbatim from spec.json.frozen_universe.endpoints).
ENDPOINTS = [
    "https://gitlab.com/users/sign_in",
    "https://gitlab.gnome.org/users/sign_in",
    "https://invent.kde.org/users/sign_in",
    "https://salsa.debian.org/users/sign_in",
    "https://gitlab.freedesktop.org/users/sign_in",
    "https://gitlab.archlinux.org/users/sign_in",
    "https://codeberg.org/user/login",
    "https://gitea.com/user/login",
    "https://git.disroot.org/user/login",
    "https://discuss.python.org/",
    "https://community.openai.com/",
    "https://discuss.elastic.co/",
    "https://community.cloudflare.com/",
    "https://forum.freecodecamp.org/",
    "https://discuss.hashicorp.com/",
    "https://discuss.kubernetes.io/",
    "https://community.home-assistant.io/",
    "https://discourse.julialang.org/",
    "https://discuss.rubyonrails.org/",
    "https://discussion.fedoraproject.org/",
    "https://forum.manjaro.org/",
    "https://forum.endeavouros.com/",
    "https://en.wikipedia.org/w/index.php?title=Special:UserLogin",
    "https://wiki.archlinux.org/index.php?title=Special:UserLogin",
    "https://wiki.gentoo.org/index.php?title=Special:UserLogin",
    "https://wiki.openstreetmap.org/w/index.php?title=Special:UserLogin",
    "https://www.mediawiki.org/w/index.php?title=Special:UserLogin",
    "https://www.wikidata.org/w/index.php?title=Special:UserLogin",
    "https://www.djangoproject.com/accounts/login/",
    "https://www.djangoproject.com/admin/login/",
    "https://pypi.org/account/login/",
    "https://docs.djangoproject.com/",
    "https://bitbucket.org/account/signin/",
    "https://rubygems.org/session/new",
    "https://www.reddit.com/login/",
    "https://news.ycombinator.com/login",
    "https://basecamp.com/",
    "https://pragprog.com/",
    "https://www.npmjs.com/login",
    "https://dev.to/enter",
    "https://start.spring.io/",
    "https://spring.io/",
    "https://wordpress.org/wp-login.php",
    "https://wordpress.com/log-in",
    "https://www.phpbb.com/community/",
    "https://discuss.flarum.org/",
    "https://community.nodebb.org/",
    "https://community.invisioncommunity.com/",
    "https://www.joomla.org/",
    "https://www.concretecms.org/",
    "https://craftcms.com/",
    "https://www.okta.com/login/",
    "https://auth0.com/",
    "https://login.microsoftonline.com/",
    "https://duckduckgo.com/html/?q=test",
    "https://www.bing.com/search?q=test",
    "https://search.brave.com/search?q=test",
]

# Pre-freeze fixed candidate stratum (spec.json.scheduler_strata.stratum_pre_freeze_candidates)
PRE_FREEZE_CANDIDATES = [
    "https://gitlab.com/users/sign_in",
    "https://community.cloudflare.com/",
    "https://www.npmjs.com/login",
    "https://wordpress.com/log-in",
    "https://www.phpbb.com/community/",
    "https://community.invisioncommunity.com/",
    "https://search.brave.com/search?q=test",
    "https://www.djangoproject.com/admin/login/",
    "https://www.djangoproject.com/accounts/login/",
    "https://auth0.com/",
    "https://community.home-assistant.io/",
]
RATE_LIMIT_CAPABLE = [
    "https://www.djangoproject.com/admin/login/",
    "https://www.djangoproject.com/accounts/login/",
    "https://auth0.com/",
    "https://search.brave.com/search?q=test",
    "https://community.home-assistant.io/",
]

TWO_LEVEL_TLDS = {
    "co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "net.au", "org.au",
    "co.jp", "co.nz", "com.br", "co.in", "com.cn", "org.cn", "co.kr",
}


def registrable_domain(url_or_host: str) -> str:
    host = url_or_host
    if "://" in host:
        host = urlparse(host).netloc
    host = host.split(":")[0].lower()
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    if ".".join(parts[-2:]) in TWO_LEVEL_TLDS:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


# ---------------------------------------------------------------------------
# Frozen intrinsic classifier: a pure function of a single response's fields
# ---------------------------------------------------------------------------

def body_marker_matched(body_bytes: bytes) -> bool:
    if not body_bytes:
        return False
    try:
        text = body_bytes[:262144].decode("utf-8", "ignore")
    except Exception:
        return False
    return bool(CHALLENGE_MARKER_RE.search(text))


def classify(status, error, cf_mitigated, marker_matched: bool) -> str:
    """Pure deterministic function of a single response's STORED fields:
    (status, error, cf_mitigated, marker_matched). AUDIT can recompute it exactly."""
    if error is not None or status is None:
        return CLASS_TRANSPORT_ERROR
    if status == 403:
        if (cf_mitigated or "").strip().lower() == "challenge":
            return CLASS_BLOCK_403_CHALLENGE
        if marker_matched:
            return CLASS_BLOCK_403_CHALLENGE
        return CLASS_UNAVAILABLE_403
    if status == 429:
        return CLASS_RATE_LIMIT_429
    if 200 <= status <= 299:
        if marker_matched:
            # SPEC: CLEAN requires "body does not contain a challenge marker"; a 2xx
            # carrying a challenge marker is neither CLEAN nor a 403 block, so it is
            # classified OTHER_NONBARRIER (non-barrier, non-clean).
            return CLASS_OTHER_NONBARRIER
        return CLASS_CLEAN
    return CLASS_OTHER_NONBARRIER


def is_barrier(cls: str) -> bool:
    return cls in BARRIER_SET


# ---------------------------------------------------------------------------
# Live collection
# ---------------------------------------------------------------------------

def _new_opener():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def _fetch(opener, url: str, timeout: float):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": ACCEPT_HEADER,
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    })
    t0 = time.time()
    status = None
    error = None
    headers = {}
    body = b""
    try:
        resp = opener.open(req, timeout=timeout)
        status = resp.getcode()
        headers = {k.lower(): v for k, v in resp.headers.items()}
        body = resp.read(1_048_576)
    except urllib.error.HTTPError as e:
        status = e.code
        headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        try:
            body = e.read(1_048_576)
        except Exception:
            body = b""
    except Exception as e:  # DNS / connect / TLS / timeout
        error = f"{type(e).__name__}: {e}"
    elapsed_ms = int((time.time() - t0) * 1000)
    return status, headers, body, error, elapsed_ms


# Response-driven AADAPT action, pure function of (class, attempt, retry_after).
def adapt_action(cls: str, retry_after_hdr):
    """Return (action, wait_s, fresh_jar). action in {'stop','retry'}."""
    if cls == CLASS_CLEAN:
        return ("stop", 0.0, False)
    if cls == CLASS_RATE_LIMIT_429:
        wait = 8.0
        if retry_after_hdr:
            try:
                wait = min(max(float(str(retry_after_hdr).strip()), 0.0), 30.0)
            except Exception:
                wait = 8.0
        return ("retry", wait, False)
    if cls == CLASS_BLOCK_403_CHALLENGE:
        return ("stop", 0.0, False)
    if cls in (CLASS_UNAVAILABLE_403, CLASS_OTHER_NONBARRIER):
        return ("stop", 0.0, False)
    if cls == CLASS_TRANSPORT_ERROR:
        return ("retry_once_fresh", 3.0, True)
    return ("stop", 0.0, False)


def run_episode(endpoint: str, arm: str, session_idx: int) -> list:
    """Run one episode (endpoint x fresh-cookie-jar session) and return its request records."""
    opener = _new_opener()
    recs = []
    transport_retried = False
    next_gap = 0.0
    next_fresh = True  # j == 0 always uses a newly created jar
    j = 0
    while j < J_MAX:
        # ---- wait / (re)create jar according to the frozen arm policy ----
        if j > 0:
            if next_gap > 0:
                time.sleep(next_gap)
            if next_fresh:
                opener = _new_opener()
        gap_s = next_gap
        fresh = 1 if next_fresh else 0
        issue_ts = time.time()
        status, headers, body, error, elapsed_ms = _fetch(opener, endpoint, HTTP_TIMEOUT_S)
        recv_ts = time.time()
        marker = body_marker_matched(body)
        cls = classify(status, error, headers.get("cf-mitigated"), marker)
        rec = {
            "endpoint": endpoint,
            "domain": registrable_domain(endpoint),
            "arm": arm,
            "session_idx": session_idx,
            "j": j,
            "scheduled_gap_s": gap_s,
            "session_fresh": fresh,
            "status": status,
            "error": error,
            "cf_mitigated": headers.get("cf-mitigated"),
            "server_header": headers.get("server"),
            "retry_after": headers.get("retry-after"),
            "body_sha256": __import__("hashlib").sha256(body).hexdigest(),
            "body_len": len(body),
            "challenge_marker_matched": marker,
            "elapsed_ms": elapsed_ms,
            "intrinsic_class": cls,
            "ts_issue": issue_ts,
            "ts_recv": recv_ts,
        }
        recs.append(rec)
        j += 1

        # ---- termination / next action ----
        if cls == CLASS_CLEAN:
            break
        if arm in ("A_RETRY", "A_RETRY_SPACED", "A_FRESH"):
            next_gap = 0.5 if arm == "A_RETRY" else 4.0
            next_fresh = (arm == "A_FRESH")
            continue
        # A_ADAPT (response-driven): CLEAN stop; 429 wait+retry same session; 403 stop;
        # UNAVAILABLE_403/OTHER stop; TRANSPORT_ERROR retry ONCE after 3.0s fresh jar then stop.
        if cls == CLASS_TRANSPORT_ERROR:
            if not transport_retried:
                transport_retried = True
                next_gap = 3.0
                next_fresh = True
                continue
            break
        action, wait_s, fresh_flag = adapt_action(cls, headers.get("retry-after"))
        if action.startswith("retry"):
            next_gap = wait_s
            next_fresh = fresh_flag
            continue
        break
    return recs


def session_id(endpoint: str, session_idx: int) -> str:
    return f"{endpoint}#s{session_idx}"


# ---------------------------------------------------------------------------
# Feature pipeline (shared by real data and synthetic controls)
# ---------------------------------------------------------------------------

CLEAN_IDX = ALL_CLASSES.index(CLASS_CLEAN)


def _row_features(prev_recs, cur, endpoint_idx, n_endpoints):
    """Build the M_HISTORY feature dict for predicting `cur`'s barrier label."""
    j = cur["j"]
    if prev_recs:
        last = prev_recs[-1]
        prev_label = last["intrinsic_class"]
        n_barrier = sum(1 for r in prev_recs if is_barrier(r["intrinsic_class"]))
        last_barrier_ts = None
        for r in reversed(prev_recs):
            if is_barrier(r["intrinsic_class"]):
                last_barrier_ts = r["ts_recv"]
                break
        if last_barrier_ts is not None:
            time_since = max(0.0, cur["ts_issue"] - last_barrier_ts) if cur["ts_issue"] else 0.0
        else:
            time_since = -1.0
        session_start = prev_recs[0]["ts_recv"]
        n_prior = len(prev_recs)
        elapsed = max(0.0, (cur["ts_issue"] - session_start)) if cur["ts_issue"] else 0.0
        gaps = [r["scheduled_gap_s"] for r in prev_recs[1:]] if n_prior >= 2 else []
        burstiness = statistics.pstdev(gaps) if len(gaps) >= 2 else 0.0
        rate = n_prior / max(elapsed, 1.0)
    else:
        prev_label = "NONE"
        n_barrier = 0
        time_since = -1.0
        n_prior = 0
        elapsed = 0.0
        burstiness = 0.0
        rate = 0.0
    return {
        "arm": cur["arm"],
        "j": j,
        "gap": cur["scheduled_gap_s"],
        "fresh": cur["session_fresh"],
        "prev_label": prev_label,
        "n_barrier_so_far": n_barrier,
        "time_since_last_barrier": time_since,
        "endpoint_idx": endpoint_idx,
        "n_endpoints": n_endpoints,
        "rate": rate,
        "burstiness": burstiness,
        "elapsed": elapsed,
    }


M_HISTORY_FEATURES = ["arm", "j", "gap", "fresh", "prev_label", "n_barrier_so_far",
                      "time_since_last_barrier", "endpoint_idx"]
M_NOID_FEATURES = ["arm", "j", "gap", "fresh", "prev_label", "n_barrier_so_far",
                   "time_since_last_barrier"]
RATE_ONLY_FEATURES = ["rate", "burstiness", "elapsed", "gap"]
CONTINUOUS_FEATURES = {"j", "gap", "fresh", "n_barrier_so_far", "time_since_last_barrier",
                       "rate", "burstiness", "elapsed"}


def build_design(feature_names, rows, n_endpoints, extra_cat=None):
    """Return float matrix X and names. `rows` are dicts already from _row_features."""
    cols = []
    names = []
    for f in feature_names:
        if f == "arm":
            for a in ARMS:
                cols.append(np.array([1.0 if r["arm"] == a else 0.0 for r in rows]))
                names.append(f"arm={a}")
        elif f == "prev_label":
            for c in PREV_LABEL_CATEGORIES:
                cols.append(np.array([1.0 if r["prev_label"] == c else 0.0 for r in rows]))
                names.append(f"prev={c}")
        elif f == "endpoint_idx":
            for k in range(n_endpoints):
                cols.append(np.array([1.0 if r["endpoint_idx"] == k else 0.0 for r in rows]))
                names.append(f"ep={k}")
        else:
            cols.append(np.array([float(r[f]) for r in rows]))
            names.append(f)
    X = np.column_stack(cols) if cols else np.zeros((len(rows), 0))
    return X, names


def fit_logistic(X, y, lam=None, max_iters=IRLS_MAX_ITERS):
    if lam is None:
        lam = RIDGE_LAMBDA
    n, p = X.shape
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd < 1e-12] = 1.0
    Xs = (X - mu) / sd
    Xd = np.column_stack([np.ones(n), Xs])
    w = np.zeros(p + 1)
    penalty = np.full(p + 1, lam)
    penalty[0] = 0.0
    for it in range(max_iters):
        z = Xd @ w
        p_hat = 1.0 / (1.0 + np.exp(-z))
        p_hat = np.clip(p_hat, 1e-12, 1 - 1e-12)
        # Objective = SUM negative log-likelihood + (lambda/2)||w||^2
        # (standard sum-scale ridge; lambda=1.0 is mild for n~1e3, cf. sklearn C=1).
        grad = Xd.T @ (p_hat - y) + penalty * w
        W = p_hat * (1 - p_hat)
        H = (Xd.T * W) @ Xd + np.diag(penalty)
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, grad, rcond=None)[0]
        w_new = w - step
        if np.max(np.abs(w_new - w)) < IRLS_TOL:
            w = w_new
            break
        w = w_new
    def predict(Xq):
        Xqs = (Xq - mu) / sd
        Xqd = np.column_stack([np.ones(Xq.shape[0]), Xqs])
        z = Xqd @ w
        return 1.0 / (1.0 + np.exp(-z))
    return predict


def logloss(p, y):
    p = np.clip(p, PROB_EPS, 1 - PROB_EPS)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


# ---------------------------------------------------------------------------
# Null predictors (training-set statistics; no per-fold logistic fit)
# ---------------------------------------------------------------------------

def predict_endpoint_const(train_rows, test_rows):
    """Endpoint-identity null (probabilistic form of the modal barrier label):
    Laplace-smoothed training barrier rate per endpoint, global fallback."""
    glob = (sum(1 for r in train_rows if r["y"] == 1) + 1.0) / (len(train_rows) + 2.0)
    cnt = {}
    tot = {}
    for r in train_rows:
        k = r["endpoint_idx"]
        tot[k] = tot.get(k, 0) + 1
        cnt[k] = cnt.get(k, 0) + r["y"]
    p = []
    for r in test_rows:
        k = r["endpoint_idx"]
        if tot.get(k, 0) > 0:
            p.append((cnt.get(k, 0) + glob * 2.0) / (tot[k] + 2.0))
        else:
            p.append(glob)
    return np.array(p)


def predict_memory_persist(train_rows, test_rows):
    """Persistence null (probabilistic form of 'repeat the previous label'):
    Laplace-smoothed training P(y=1 | prev_label), global fallback for NONE."""
    glob = (sum(1 for r in train_rows if r["y"] == 1) + 1.0) / (len(train_rows) + 2.0)
    cnt = {}
    tot = {}
    for r in train_rows:
        k = r["prev_label"]
        tot[k] = tot.get(k, 0) + 1
        cnt[k] = cnt.get(k, 0) + r["y"]
    p = []
    for r in test_rows:
        k = r["prev_label"]
        if tot.get(k, 0) > 0:
            p.append((cnt.get(k, 0) + glob * 2.0) / (tot[k] + 2.0))
        else:
            p.append(glob)
    return np.array(p)


def predict_constant(train_rows, test_rows):
    glob = (sum(1 for r in train_rows if r["y"] == 1) + 1.0) / (len(train_rows) + 2.0)
    return np.full(len(test_rows), glob)


# ---------------------------------------------------------------------------
# Cross-validated skill
# ---------------------------------------------------------------------------

def loso_predictions(rows, feature_names, n_endpoints):
    """Leave-one-session-out held-out predictions of M_HISTORY-style model."""
    X, names = build_design(feature_names, rows, n_endpoints)
    y = np.array([r["y"] for r in rows], dtype=float)
    sessions = sorted({r["session"] for r in rows})
    preds = np.full(len(rows), np.nan)
    for s in sessions:
        test_idx = [i for i, r in enumerate(rows) if r["session"] == s]
        train_idx = [i for i, r in enumerate(rows) if r["session"] != s]
        if not train_idx or not test_idx:
            continue
        predict = fit_logistic(X[train_idx], y[train_idx])
        preds[test_idx] = predict(X[test_idx])
    return preds


def loso_null_predictions(rows, kind):
    y = np.array([r["y"] for r in rows], dtype=float)
    sessions = sorted({r["session"] for r in rows})
    preds = np.full(len(rows), np.nan)
    for s in sessions:
        test_idx = [i for i, r in enumerate(rows) if r["session"] == s]
        train_idx = [i for i, r in enumerate(rows) if r["session"] != s]
        train_rows = [rows[i] for i in train_idx]
        test_rows = [rows[i] for i in test_idx]
        if kind == "B_CONSTANT":
            p = predict_constant(train_rows, test_rows)
        elif kind == "B_ENDPOINT_CONST":
            p = predict_endpoint_const(train_rows, test_rows)
        elif kind == "B_MEMORY_PERSIST":
            p = predict_memory_persist(train_rows, test_rows)
        preds[test_idx] = p
    return preds


def rate_only_loso(rows):
    X, _ = build_design(RATE_ONLY_FEATURES, rows, 1)
    y = np.array([r["y"] for r in rows], dtype=float)
    sessions = sorted({r["session"] for r in rows})
    preds = np.full(len(rows), np.nan)
    for s in sessions:
        test_idx = [i for i, r in enumerate(rows) if r["session"] == s]
        train_idx = [i for i, r in enumerate(rows) if r["session"] != s]
        if not train_idx or not test_idx:
            continue
        predict = fit_logistic(X[train_idx], y[train_idx])
        preds[test_idx] = predict(X[test_idx])
    return preds


def skill_and_ci(rows, ll_m, ll_nulls, domains, n_resamples=BOOTSTRAP_N, seed=SEED_BOOTSTRAP,
                 restricted_idx=None):
    """SKILL_LL = min_k LL_null_k - LL_M_HISTORY over the given row set, with
    domain-clustered percentile bootstrap CI."""
    y = np.array([r["y"] for r in rows], dtype=float)
    if restricted_idx is not None:
        idx = np.array(restricted_idx)
    else:
        idx = np.arange(len(rows))
    n_total = len(idx)
    ll_m_vec = -np.array([_ll_point(ll_m[i], y[i]) for i in idx])
    null_mat = np.array([[-_ll_point(lls[i], y[i]) for i in idx] for lls in ll_nulls.values()])
    # cluster by domain
    dom_list = sorted(set(domains))
    dom_index = {d: i for i, d in enumerate(dom_list)}
    row_dom = np.array([dom_index[domains[i]] for i in idx])
    n_dom = len(dom_list)
    # per-domain sums
    def dom_sums(vec):
        out = np.zeros(n_dom)
        np.add.at(out, row_dom, vec)
        return out
    def dom_counts():
        out = np.zeros(n_dom)
        np.add.at(out, row_dom, np.ones(len(idx)))
        return out
    s_m = dom_sums(ll_m_vec)
    s_null = np.array([dom_sums(null_mat[k]) for k in range(null_mat.shape[0])])
    c = dom_counts()
    def skill_from_counts(counts):
        tot = float(np.dot(counts, c))
        if tot <= 0:
            return None
        m = float(np.dot(counts, s_m)) / tot
        nulls = [float(np.dot(counts, s_null[k])) / tot for k in range(s_null.shape[0])]
        return min(nulls) - m
    skill = skill_from_counts(np.ones(n_dom))
    rng = np.random.default_rng(seed)
    boot = np.empty(n_resamples)
    for b in range(n_resamples):
        counts = rng.integers(0, n_dom, size=n_dom)
        boot[b] = skill_from_counts(counts)
    lo = float(np.percentile(boot, 100 * ALPHA / 2))
    hi = float(np.percentile(boot, 100 * (1 - ALPHA / 2)))
    return skill, lo, hi, boot


def _ll_point(p, y):
    p = min(max(p, PROB_EPS), 1 - PROB_EPS)
    return y * math.log(p) + (1 - y) * math.log(1 - p)


# ---------------------------------------------------------------------------
# Synthetic controls
# ---------------------------------------------------------------------------

def _sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


# EXECUTE-calibrated positive-control generator constants (non-outcome-bearing; chosen
# before any real collection). The planted effect is the mutual information between the
# label and the schedule-history drivers (request index j = recent-rate proxy, and
# time-since-last-barrier ts, in units of the fixed 1.0 s synthetic gap); it realises
# MI ~= 0.19 nats, i.e. the frozen planted_effect_size_nats ~= 0.20.
PC_PLANT_A = -1.0
PC_PLANT_B = 1.0
PC_PLANT_C = 0.3
PC_GAP_S = 1.0
SYNTH_SEQUENCES = 114
SYNTH_SEQ_LEN = 6
SYNTH_ENDPOINTS = 19  # 114/19 = 6 sequences per synthetic endpoint


def gen_pc_sequences(rng, n_seq=SYNTH_SEQUENCES, seq_len=SYNTH_SEQ_LEN,
                     n_endpoints=SYNTH_ENDPOINTS):
    """PC_SYNTHETIC_DYNAMICS: planted schedule-dependent hazard

        logit p = A + B * time_since_last_barrier + C * j

    where time_since_last_barrier is in synthetic steps (-1 when no barrier yet),
    endpoint identities carry NO constant barrier propensity, and the same feature
    pipeline / splitter / model as the real data is used downstream.
    """
    seqs = []
    for s in range(n_seq):
        ep = s % n_endpoints
        last_barrier = None
        labels = []
        for j in range(seq_len):
            ts = (j - last_barrier) if last_barrier is not None else -1.0
            p = _sigmoid(PC_PLANT_A + PC_PLANT_B * ts + PC_PLANT_C * j)
            y = 1 if rng.random() < p else 0
            labels.append(y)
            if y == 1:
                last_barrier = j
        seqs.append((ep, labels))
    return seqs


def gen_nc_sequences(rng, n_seq=SYNTH_SEQUENCES, seq_len=SYNTH_SEQ_LEN,
                     n_endpoints=SYNTH_ENDPOINTS):
    """NC_SYNTHETIC_MEMORYLESS: per-endpoint constant propensity beta(0.5,0.5),
    i.i.d. Bernoulli, no schedule dependence."""
    props = {}
    for e in range(n_endpoints):
        props[e] = rng.betavariate(0.5, 0.5)
    seqs = []
    for s in range(n_seq):
        ep = s % n_endpoints
        labels = [1 if rng.random() < props[ep] else 0 for _ in range(seq_len)]
        seqs.append((ep, labels))
    return seqs


def synthetic_rows(seqs, gap=1.0):
    """Convert (endpoint_idx, label list) into analysis rows through the SAME feature
    pipeline."""
    rows = []
    for si, (ep, labels) in enumerate(seqs):
        prev_recs = []
        t = 0.0
        for j, y in enumerate(labels):
            cur = {"arm": "A_RETRY", "j": j, "scheduled_gap_s": (0.0 if j == 0 else gap),
                   "session_fresh": 1 if j == 0 else 0,
                   "ts_issue": t, "ts_recv": t + 0.1}
            f = _row_features(prev_recs, cur, ep, n_endpoints=None)
            f["y"] = y
            f["session"] = f"synthetic#{si}"
            f["endpoint_idx"] = ep
            f["domain"] = f"synthetic_ep{ep}"
            rows.append(f)
            prev_recs.append({"intrinsic_class": (CLASS_CLEAN if y == 0 else CLASS_BLOCK_403_CHALLENGE),
                              "ts_recv": t + 0.1, "scheduled_gap_s": (0.0 if j == 0 else gap)})
            t += gap
    return rows


def _loso_by_session(rows, X, y, sessions, session_to_idx):
    preds = np.full(len(rows), np.nan)
    for s in sessions:
        te = session_to_idx[s]
        tr = [i for i in range(len(rows)) if i not in set(te)]
        if not tr or not te:
            continue
        preds[te] = fit_logistic(X[tr], y[tr])(X[te])
    return preds


def run_synthetic_control(seqs, n_endpoints, n_resamples_ci=1000, seed=SEED_BOOTSTRAP):
    rows = synthetic_rows(seqs)
    return run_analysis_core(rows, n_endpoints, n_resamples_ci=n_resamples_ci, seed=seed)


def run_analysis_core(rows, n_endpoints, n_resamples_ci=BOOTSTRAP_N, seed=SEED_BOOTSTRAP,
                      feature_names=None):
    """Cross-validated next-request barrier skill for the model on `feature_names`
    (default M_HISTORY) vs the four nulls."""
    if feature_names is None:
        feature_names = M_HISTORY_FEATURES
    y = np.array([r["y"] for r in rows], dtype=float)
    Xh, _ = build_design(feature_names, rows, n_endpoints)
    Xr, _ = build_design(RATE_ONLY_FEATURES, rows, 1)
    sessions = sorted({r["session"] for r in rows})
    session_to_idx = {}
    for i, r in enumerate(rows):
        session_to_idx.setdefault(r["session"], []).append(i)
    ll_m = _loso_by_session(rows, Xh, y, sessions, session_to_idx)
    ll_rate = _loso_by_session(rows, Xr, y, sessions, session_to_idx)
    ll_nulls = {}
    for kind in ("B_CONSTANT", "B_ENDPOINT_CONST", "B_MEMORY_PERSIST"):
        pred = np.full(len(rows), np.nan)
        for s in sessions:
            te = session_to_idx[s]
            tr = [i for i in range(len(rows)) if i not in set(te)]
            train_rows = [rows[i] for i in tr]
            test_rows = [rows[i] for i in te]
            if kind == "B_CONSTANT":
                p = predict_constant(train_rows, test_rows)
            elif kind == "B_ENDPOINT_CONST":
                p = predict_endpoint_const(train_rows, test_rows)
            else:
                p = predict_memory_persist(train_rows, test_rows)
            pred[te] = p
        ll_nulls[kind] = pred
    ll_nulls["B_RATE_ONLY"] = ll_rate
    domains = [r["domain"] for r in rows]
    skill, lo, hi, boot = skill_and_ci(rows, ll_m, ll_nulls, domains,
                                       n_resamples=n_resamples_ci, seed=seed)
    # log-losses for reporting
    lls = {"M_HISTORY": logloss(ll_m, y)}
    for k, v in ll_nulls.items():
        lls[k] = logloss(v, y)
    ba = {"M_HISTORY": balanced_accuracy(ll_m, y)}
    for k, v in ll_nulls.items():
        ba[k] = balanced_accuracy(v, y)
    best_null = min(lls[k] for k in ("B_CONSTANT", "B_ENDPOINT_CONST",
                                     "B_MEMORY_PERSIST", "B_RATE_ONLY"))
    skill_ba = ba["M_HISTORY"] - max(ba[k] for k in ("B_CONSTANT", "B_ENDPOINT_CONST",
                                                     "B_MEMORY_PERSIST", "B_RATE_ONLY"))
    _ = best_null
    return {
        "SKILL_LL": skill, "LO": lo, "HI": hi, "n_rows": len(rows),
        "logloss": lls, "balanced_accuracy": ba, "SKILL_BA": skill_ba,
    }


def balanced_accuracy(p, y):
    p = np.asarray(p)
    y = np.asarray(y)
    pos = p[y == 1] >= 0.5
    neg = p[y == 0] >= 0.5
    tpr = float(np.mean(pos)) if len(pos) else 0.0
    tnr = float(np.mean(~neg)) if len(neg) else 0.0
    return 0.5 * (tpr + tnr)


# ---------------------------------------------------------------------------
# Q4 separability: barrier_set vs ordinary_unavailability_set (CLEAN excluded)
# ---------------------------------------------------------------------------

def separability_skill(rows, n_endpoints, n_resamples_ci=BOOTSTRAP_N, seed=SEED_BOOTSTRAP):
    """Held-out skill of a M_HISTORY-feature model separating barrier_set from
    ordinary_unavailability_set on the subset of requests whose true class is in
    either set (CLEAN excluded)."""
    sub = [dict(r) for r in rows if r.get("intrinsic_class") in (BARRIER_SET | ORDINARY_UNAVAILABILITY_SET)]
    for r in sub:
        r["y"] = 1 if r["intrinsic_class"] in BARRIER_SET else 0
    if not sub:
        return {"SKILL_LL": None, "LO": None, "HI": None, "n_rows": 0, "note": "empty subset"}
    return run_analysis_core(sub, n_endpoints, n_resamples_ci=n_resamples_ci, seed=seed)


# ---------------------------------------------------------------------------
# Scheduler economy on the barrier-exposed stratum
# ---------------------------------------------------------------------------

def episode_metrics(recs):
    classes = [r["intrinsic_class"] for r in recs]
    return {
        "n_requests": len(recs),
        "success": 1 if any(c == CLASS_CLEAN for c in classes) else 0,
        "first_request_clean": 1 if classes and classes[0] == CLASS_CLEAN else 0,
        "barrier_events": sum(1 for c in classes if c in BARRIER_SET),
        "terminal_class": classes[-1] if classes else None,
    }


def scheduler_economy(episodes, stratum_endpoints, n_resamples_ci=BOOTSTRAP_N,
                      seed=SEED_BOOTSTRAP):
    """d_Req = mean_requests(A_ADAPT) - mean_requests(A_RETRY) on the stratum, with
    domain-clustered bootstrap CI; plus success metrics and the no-barrier baseline."""
    stratum_set = set(stratum_endpoints)
    eps = [e for e in episodes if e["endpoint"] in stratum_set]
    adapt = [e for e in eps if e["arm"] == "A_ADAPT"]
    retry = [e for e in eps if e["arm"] == "A_RETRY"]

    def mean(xs):
        return float(sum(xs) / len(xs)) if xs else None

    adapt_req = mean([e["n_requests"] for e in adapt])
    retry_req = mean([e["n_requests"] for e in retry])
    adapt_succ = mean([e["success"] for e in adapt])
    retry_succ = mean([e["success"] for e in retry])
    no_barrier = mean([e["first_request_clean"] for e in eps])
    d_req = (adapt_req - retry_req) if (adapt_req is not None and retry_req is not None) else None
    d_succ = (adapt_succ - retry_succ) if (adapt_succ is not None and retry_succ is not None) else None

    # domain-clustered bootstrap for d_Req
    d_req_lo = d_req_hi = d_req_ci_note = None
    if d_req is not None:
        doms = sorted({e["domain"] for e in eps})
        dom_idx = {d: i for i, d in enumerate(doms)}
        # per-domain sums and counts, separately per arm
        sums = {"A_ADAPT": np.zeros(len(doms)), "A_RETRY": np.zeros(len(doms))}
        cnts = {"A_ADAPT": np.zeros(len(doms)), "A_RETRY": np.zeros(len(doms))}
        for e in eps:
            if e["arm"] in sums:
                k = dom_idx[e["domain"]]
                sums[e["arm"]][k] += e["n_requests"]
                cnts[e["arm"]][k] += 1
        rng = np.random.default_rng(seed)
        boot = []
        n = len(doms)
        for _ in range(n_resamples_ci):
            counts = rng.integers(0, n, size=n)
            ca = float(np.dot(counts, cnts["A_ADAPT"]))
            cr = float(np.dot(counts, cnts["A_RETRY"]))
            if ca > 0 and cr > 0:
                sa = float(np.dot(counts, sums["A_ADAPT"])) / ca
                sr = float(np.dot(counts, sums["A_RETRY"])) / cr
                boot.append(sa - sr)
        if boot:
            d_req_lo = float(np.percentile(boot, 100 * ALPHA / 2))
            d_req_hi = float(np.percentile(boot, 100 * (1 - ALPHA / 2)))
        else:
            d_req_ci_note = "bootstrap produced no valid resample (arm empty in every draw)"
    return {
        "d_Req": d_req, "d_Req_ci_lo": d_req_lo, "d_Req_ci_hi": d_req_hi,
        "d_Req_ci_note": d_req_ci_note,
        "d_Succ": d_succ,
        "ADAPT_abs_requests": adapt_req, "RETRY_abs_requests": retry_req,
        "ADAPT_success": adapt_succ, "RETRY_success": retry_succ,
        "endpoint_no_barrier_success": no_barrier,
        "n_stratum_endpoints": len(stratum_set),
        "n_stratum_episodes": len(eps),
        "n_stratum_barrier_events": int(sum(e["barrier_events"] for e in eps)),
    }


# ---------------------------------------------------------------------------
# Branch decision
# ---------------------------------------------------------------------------

def decide_branch(skill_ll, lo, hi, d_req, d_req_hi, d_succ, adapt_succ,
                  endpoint_no_barrier_success):
    pred_pass = (skill_ll >= DELTA_SKILL_NATS) and (lo > 0)
    pred_fail = (skill_ll <= 0) and (hi < DELTA_SKILL_NATS)
    sched_pass = (d_req < 0 and d_req_hi < 0 and d_succ >= -MARGIN_SUCCESS
                  and adapt_succ >= endpoint_no_barrier_success - MARGIN_SUCCESS)
    sched_fail = (d_req >= 0) or (adapt_succ < endpoint_no_barrier_success - MARGIN_SUCCESS)
    pred_disposition = "PRED_PASS" if pred_pass else ("PRED_FAIL" if pred_fail else "PRED_AMBIG")
    sched_disposition = "SCHED_ECON_PASS" if sched_pass else (
        "SCHED_ECON_FAIL" if sched_fail else "SCHED_AMBIG")
    if pred_pass and sched_pass:
        branch = "S1_SUPPORTS"
    elif pred_fail and sched_fail:
        branch = "S0_FALSIFIES"
    elif (pred_pass and sched_fail) or (pred_fail and sched_pass):
        branch = "S2_MIXED"
    else:
        branch = "INCONCLUSIVE"
    return {
        "PRED_PASS": bool(pred_pass), "PRED_FAIL": bool(pred_fail),
        "SCHED_ECON_PASS": bool(sched_pass), "SCHED_ECON_FAIL": bool(sched_fail),
        "pred_disposition": pred_disposition, "sched_disposition": sched_disposition,
        "branch": branch,
    }
