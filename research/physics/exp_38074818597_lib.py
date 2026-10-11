"""EXP-PHYSICS-38074818597 EXECUTE library.

Python 3.12 standard library ONLY. numpy is deliberately NOT imported.

This module is a literal realization of the interpretation-determining constants
embedded in the frozen spec.json / prereg.md of
research/experiments/EXP-PHYSICS-38074818597. It contains:
  * the frozen intrinsic classifier (status + cf-mitigated + CHALLENGE_RE over a
    response body prefix);
  * a stdlib-only single-GET HTTP client (frozen User-Agent, no retries, <=5
    redirects, TLS verification on);
  * estimator primitives: plug-in binary MI, the global endpoint-permutation
    null (B_EXCHANGE), and the endpoint-clustered bootstrap;
  * offline synthetic generators and the EXACT frozen branch rule used by the
    PC_SYNTHETIC_STATIONARY / NC_SYNTHETIC_EXCHANGEABLE controls.

freeze_artifacts = [] : this file is EXECUTE-authored code, not an
interpretation dependency; its sha256 is recorded in provenance.json.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------
# frozen classifier
# --------------------------------------------------------------------------
CHALLENGE_RE_LITERAL = (
    r"(?i)(just a moment|cf-browser-verification|cf[-_]chl[-_]|challenge-platform|"
    r"cf-challenge|cdn-cgi/challenge|attention required|checking your browser|"
    r"enable javascript and cookies|verify you are human|please complete the security check|"
    r"g-recaptcha|hcaptcha|recaptcha|cf-turnstile|<title>\s*just a moment)"
)
CHALLENGE_RE = re.compile(CHALLENGE_RE_LITERAL)
BODY_SCOPE_BYTES = 262144
BODY_STORE_CHARS = 8192

USER_AGENT = "SPIDER-research2/1.0 (+credential-free access-state persistence probe)"
ACCEPT = "*/*"
MAX_REDIRECTS = 5
TIMEOUT_S = 30

CLEAN = "CLEAN"
RATE_LIMIT_429 = "RATE_LIMIT_429"
BLOCK_403_CHALLENGE = "BLOCK_403_CHALLENGE"
UNAVAILABLE_403 = "UNAVAILABLE_403"
TRANSPORT_ERROR = "TRANSPORT_ERROR"
OTHER_NONBARRIER = "OTHER_NONBARRIER"

BARRIER_SET = [RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR]
ORDINARY_UNAVAILABILITY_SET = [UNAVAILABLE_403, OTHER_NONBARRIER]
INTRINSIC_CLASSES = [BLOCK_403_CHALLENGE, TRANSPORT_ERROR]
ALL_CLASSES = [CLEAN, RATE_LIMIT_429, BLOCK_403_CHALLENGE, UNAVAILABLE_403, TRANSPORT_ERROR, OTHER_NONBARRIER]
SEVERITY_RANK = {
    TRANSPORT_ERROR: 5,
    RATE_LIMIT_429: 4,
    BLOCK_403_CHALLENGE: 3,
    UNAVAILABLE_403: 2,
    OTHER_NONBARRIER: 1,
    CLEAN: 0,
}


def classify_record(status, cf_mitigated, challenge_matched):
    """Pure deterministic classifier from stored fields only."""
    if status is None:
        return TRANSPORT_ERROR
    if status == 429:
        return RATE_LIMIT_429
    if status == 403:
        cf = (cf_mitigated or "").lower() == "challenge"
        return BLOCK_403_CHALLENGE if (cf or challenge_matched) else UNAVAILABLE_403
    if 200 <= status <= 299:
        return OTHER_NONBARRIER if challenge_matched else CLEAN
    return OTHER_NONBARRIER


def classify_stored(rec):
    return classify_record(rec.get("status"), rec.get("cf_mitigated"), bool(rec.get("challenge_matched")))


# --------------------------------------------------------------------------
# HTTP client
# --------------------------------------------------------------------------
class _MaxRedirects(urllib.request.HTTPRedirectHandler):
    max_redirections = MAX_REDIRECTS


def build_opener():
    ctx = ssl.create_default_context()
    https = urllib.request.HTTPSHandler(context=ctx)
    opener = urllib.request.build_opener(_MaxRedirects, https)
    opener.addheaders = [("User-Agent", USER_AGENT), ("Accept", ACCEPT)]
    return opener


def fetch(opener, url, timeout=TIMEOUT_S):
    """One GET, one attempt, no retry. Returns a raw evidence record."""
    rec = {
        "url": url,
        "status": None,
        "cf_mitigated": None,
        "retry_after": None,
        "server": None,
        "content_length": None,
        "body_sha256": None,
        "body_len": None,
        "body_prefix": None,
        "challenge_matched": False,
        "challenge_match_span": None,
        "error": None,
        "final_url": None,
        "elapsed_ms": None,
        "class": None,
        "t_start": None,
        "t_end": None,
    }
    t0 = time.monotonic()
    rec["t_start"] = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": ACCEPT}, method="GET")
        resp = opener.open(req, timeout=timeout)
        try:
            raw = resp.read(BODY_SCOPE_BYTES)
            rec["status"] = int(resp.status)
            rec["final_url"] = resp.geturl()
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
        finally:
            resp.close()
        _fill_body(rec, raw)
        _fill_headers(rec, hdrs)
    except urllib.error.HTTPError as e:
        try:
            raw = e.read(BODY_SCOPE_BYTES)
        except Exception:
            raw = b""
        try:
            rec["final_url"] = e.geturl()
        except Exception:
            rec["final_url"] = url
        rec["status"] = int(e.code)
        hdrs = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        _fill_body(rec, raw)
        _fill_headers(rec, hdrs)
    except Exception as e:  # DNS/connect/TLS/timeout/redirect-limit
        rec["error"] = f"{type(e).__name__}: {e}"
        rec["status"] = None
    rec["t_end"] = time.time()
    rec["elapsed_ms"] = (time.monotonic() - t0) * 1000.0
    rec["class"] = classify_stored(rec)
    return rec


def _fill_body(rec, raw):
    rec["body_len"] = len(raw)
    rec["body_sha256"] = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="ignore")
    m = CHALLENGE_RE.search(text)
    if m:
        rec["challenge_matched"] = True
        rec["challenge_match_span"] = [m.start(), m.end()]
    rec["body_prefix"] = text[:BODY_STORE_CHARS]


def _fill_headers(rec, hdrs):
    rec["cf_mitigated"] = hdrs.get("cf-mitigated")
    rec["retry_after"] = hdrs.get("retry-after")
    rec["server"] = hdrs.get("server")
    rec["content_length"] = hdrs.get("content-length")


# --------------------------------------------------------------------------
# estimator primitives
# --------------------------------------------------------------------------
def mi_binary_counts(n, n1_, n_1, n11):
    """Plug-in MI in nats for a 2x2 table with fixed marginals and overlap n11."""
    if n <= 0:
        return 0.0
    n10 = n1_ - n11
    n01 = n_1 - n11
    n00 = n - n11 - n10 - n01
    row1, row0 = n1_, n - n1_
    col1, col0 = n_1, n - n_1
    total = 0.0
    for cnt, r, c in ((n11, row1, col1), (n10, row1, col0), (n01, row0, col1), (n00, row0, col0)):
        if cnt > 0:
            p = cnt / n
            total += p * math.log((cnt * n) / (r * c))
    if total < 0 and total > -1e-12:
        total = 0.0
    return total


def binary_arrays(classes, class_list):
    b = {c: 0 for c in class_list}
    b.update({c: 1 for c in class_list})
    return [1 if c in BARRIER_SET else 0 for c in classes]


def intrinsic_array(classes):
    return [1 if c in INTRINSIC_CLASSES else 0 for c in classes]


def mi_binary(a, b):
    n = len(a)
    n1_ = int(sum(a))
    n_1 = int(sum(b))
    n11 = int(sum(1 for x, y in zip(a, b) if x and y))
    return mi_binary_counts(n, n1_, n_1, n11)


def mi_general(xs, ys):
    """Plug-in mutual information in nats for two label sequences."""
    n = len(xs)
    if n == 0:
        return 0.0
    joint = {}
    mx = {}
    my = {}
    for x, y in zip(xs, ys):
        joint[(x, y)] = joint.get((x, y), 0) + 1
        mx[x] = mx.get(x, 0) + 1
        my[y] = my.get(y, 0) + 1
    total = 0.0
    for (x, y), c in joint.items():
        if c > 0:
            total += (c / n) * math.log((c * n) / (mx[x] * my[y]))
    return total


def perm_test_binary(anchor_b, lag_b, permutations, rng):
    """B_EXCHANGE: global uniform permutation of the lag indicator; returns (obs_mi, p)."""
    n = len(anchor_b)
    n1_ = int(sum(anchor_b))
    n_1 = int(sum(lag_b))
    n11 = int(sum(1 for x, y in zip(anchor_b, lag_b) if x and y))
    obs = mi_binary_counts(n, n1_, n_1, n11)
    anchor_pos = [i for i, x in enumerate(anchor_b) if x]
    anchor_set = set(anchor_pos)
    ge = 0
    k = n_1
    for _ in range(permutations):
        if k == 0:
            perm_mi = 0.0
        else:
            sample = rng.sample(range(n), k)
            overlap = 0
            for i in sample:
                if i in anchor_set:
                    overlap += 1
            perm_mi = mi_binary_counts(n, n1_, k, overlap)
        if perm_mi >= obs - 1e-15:
            ge += 1
    p = (ge + 1) / (permutations + 1)
    return obs, p


def registrable_domain(url):
    host = urllib.parse.urlsplit(url).hostname or ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


def cluster_bootstrap_ci(anchor_b, lag_b, urls, resamples, rng, lo=2.5, hi=97.5):
    """Endpoint-clustered bootstrap percentile CI of plug-in binary MI.

    Cluster = registrable_domain. Clusters are resampled with replacement; each
    selected cluster contributes all of its endpoints.
    """
    domains = [registrable_domain(u) for u in urls]
    clusters = {}
    for i, d in enumerate(domains):
        clusters.setdefault(d, []).append(i)
    keys = list(clusters.keys())
    m = len(keys)
    if m == 0:
        return [None, None]
    vals = []
    for _ in range(resamples):
        idx = []
        for _ in range(m):
            idx.extend(clusters[keys[rng.randrange(m)]])
        a = [anchor_b[i] for i in idx]
        b = [lag_b[i] for i in idx]
        vals.append(mi_binary(a, b))
    vals.sort()
    def pct(q):
        if not vals:
            return None
        pos = (len(vals) - 1) * (q / 100.0)
        f = int(math.floor(pos))
        c = min(f + 1, len(vals) - 1)
        return vals[f] + (vals[c] - vals[f]) * (pos - f)
    return [pct(lo), pct(hi)]


# --------------------------------------------------------------------------
# offline synthetic worlds and the frozen branch rule
# --------------------------------------------------------------------------
def frozen_branch(classes_t0, classes_lag, urls, rng, permutations, boot_resamples):
    """Apply the EXACT frozen branch rule to one ambient class pair.

    Returns a dict with all decision quantities and the selected branch.
    """
    n = len(classes_t0)
    barrier_t0 = [1 if c in BARRIER_SET else 0 for c in classes_t0]
    barrier_lag = [1 if c in BARRIER_SET else 0 for c in classes_lag]
    intr_t0 = [1 if c in INTRINSIC_CLASSES else 0 for c in classes_t0]
    intr_lag = [1 if c in INTRINSIC_CLASSES else 0 for c in classes_lag]

    n_t0_intrinsic = int(sum(intr_t0))
    n_t0_barrier = int(sum(barrier_t0))

    # per-class persistence for intrinsic classes present at T0
    class_persistence = {}
    for c in INTRINSIC_CLASSES:
        denom = sum(1 for x in classes_t0 if x == c)
        if denom > 0:
            num = sum(1 for x, y in zip(classes_t0, classes_lag) if x == c and y == c)
            class_persistence[c] = num / denom
    intrinsic_persistence_pooled = None
    if n_t0_intrinsic > 0:
        same = sum(1 for x, y in zip(classes_t0, classes_lag) if x in INTRINSIC_CLASSES and y == x)
        intrinsic_persistence_pooled = same / n_t0_intrinsic
    intrinsic_persistent = (n_t0_intrinsic >= 3) and all(v >= 0.80 for v in class_persistence.values())

    denom_fa = n_t0_intrinsic
    denom_fr = n - n_t0_intrinsic
    fa = (sum(1 for x, y in zip(intr_t0, intr_lag) if x == 1 and y == 0) / denom_fa) if denom_fa else None
    fr = (sum(1 for x, y in zip(intr_t0, intr_lag) if x == 0 and y == 1) / denom_fr) if denom_fr else None
    denylist_valid = (fa is not None and fr is not None and fa <= 0.20 and fr <= 0.20)

    obs_mi, p_perm = perm_test_binary(barrier_t0, barrier_lag, permutations, rng)
    ci = cluster_bootstrap_ci(barrier_t0, barrier_lag, urls, boot_resamples, rng)
    stat_sig = (obs_mi >= 0.05) and (p_perm < 0.05) and (ci[0] is not None and ci[0] > 0)
    s1 = bool(intrinsic_persistent and denylist_valid and stat_sig)
    branch = "S1_STATIONARY" if s1 else "S0_NON_STATIONARY"
    change_classes = []
    if not s1:
        if not intrinsic_persistent:
            change_classes.append("intrinsic_break")
        if not denylist_valid:
            change_classes.append("intrinsic_denylist_violation")
        if not stat_sig:
            change_classes.append("no_anchor_information")
    return {
        "branch": branch,
        "intrinsic_persistent": intrinsic_persistent,
        "denylist_valid": denylist_valid,
        "stat_sig": stat_sig,
        "stationarity_skill": obs_mi,
        "perm_p": p_perm,
        "ci": ci,
        "class_persistence": class_persistence,
        "intrinsic_persistence_pooled": intrinsic_persistence_pooled,
        "n_t0_intrinsic": n_t0_intrinsic,
        "n_t0_barrier": n_t0_barrier,
        "false_accept": fa,
        "false_reject": fr,
        "change_classes": change_classes,
    }


PILOT_MARGINAL6 = ([CLEAN] * 46) + ([BLOCK_403_CHALLENGE] * 5) + ([TRANSPORT_ERROR] * 1) + ([OTHER_NONBARRIER] * 5)


def gen_planted(rng, marginal, n, rho):
    anchor = [marginal[rng.randrange(len(marginal))] for _ in range(n)]
    lag = []
    for a in anchor:
        if rng.random() < rho:
            lag.append(a)
        else:
            lag.append(marginal[rng.randrange(len(marginal))])
    return anchor, lag


def gen_exchangeable(rng, marginal, n):
    anchor = [marginal[rng.randrange(len(marginal))] for _ in range(n)]
    lag = [marginal[rng.randrange(len(marginal))] for _ in range(n)]
    return anchor, lag


def synthetic_power(rng, marginal, n, rho, replications, permutations, boot_resamples, label, log):
    s1 = 0
    perm_sig = 0
    mi_sum = 0.0
    s1_fixed = 0
    fixed = 0
    for r in range(replications):
        anchor, lag = gen_planted(rng, marginal, n, rho)
        res = frozen_branch(anchor, lag, [f"https://e{i}.example{i}.com/" for i in range(n)], rng, permutations, boot_resamples)
        mi_sum += res["stationarity_skill"]
        if res["perm_p"] < 0.05:
            perm_sig += 1
        if res["branch"] == "S1_STATIONARY":
            s1 += 1
        if res["n_t0_intrinsic"] >= 3:
            fixed += 1
            if res["branch"] == "S1_STATIONARY":
                s1_fixed += 1
        if (r + 1) % 50 == 0:
            log(f"[{label}] rep {r+1}/{replications} S1={s1} perm_sig={perm_sig}")
    R = replications
    return {
        "replications": R,
        "rho": rho,
        "S1_fraction": s1 / R,
        "S1_fraction_given_n_t0_intrinsic_ge_3": (s1_fixed / fixed) if fixed else None,
        "reps_with_n_t0_intrinsic_ge_3": fixed,
        "perm_sig_rate": perm_sig / R,
        "mi_mean_nats": mi_sum / R,
    }


def synthetic_false_positive(rng, marginal, n, replications, permutations, label, log):
    perm_sig = 0
    s1 = 0
    mi_sum = 0.0
    for r in range(replications):
        anchor, lag = gen_exchangeable(rng, marginal, n)
        # exchangeable: only the permutation test is needed for the NC gate,
        # but the exact rule is applied for completeness.
        res = frozen_branch(anchor, lag, [f"https://e{i}.example{i}.com/" for i in range(n)], rng, permutations, 0)
        mi_sum += res["stationarity_skill"]
        if res["perm_p"] < 0.05:
            perm_sig += 1
        if res["branch"] == "S1_STATIONARY":
            s1 += 1
        if (r + 1) % 50 == 0:
            log(f"[{label}] rep {r+1}/{replications} perm_sig={perm_sig} S1={s1}")
    return {
        "replications": replications,
        "perm_sig_fraction": perm_sig / replications,
        "S1_fraction": s1 / replications,
        "mi_mean_nats": mi_sum / replications,
    }


# --------------------------------------------------------------------------
# misc
# --------------------------------------------------------------------------
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_spec(root):
    exp = Path(root) / "research/experiments/EXP-PHYSICS-38074818597"
    return json.loads((exp / "spec.json").read_text())


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=False) + "\n")


def append_jsonl(path, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
