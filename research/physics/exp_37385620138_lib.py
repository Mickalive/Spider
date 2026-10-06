#!/usr/bin/env python3
"""
EXP-PHYSICS-37385620138 — shared executor library (EXECUTE stage).

Implements ONLY what the frozen packet (request.json / spec.json / prereg.md,
freeze.json) specifies, in the frozen substrate:

  * stdlib urllib HTTPS GET, no browser, no Docker, no model key, no credentials,
    no cookies, no session state;
  * the frozen response-signature tuple (prereg s6.3);
  * the frozen signature distance (prereg s6.3), implemented LITERALLY as frozen
    and additionally as a corrected variant so that the consequence of the frozen
    form can be measured rather than argued;
  * the frozen mechanism declarations (prereg s6.1);
  * the frozen predictors (prereg s7.1 - s7.4);
  * the frozen metric (prereg s8.1, log_score(pred, obs) = -log(|pred - obs| + eps));
  * the frozen site-clustered bootstrap (prereg s11 step 8).

Nothing in this module reads an outcome to build a prediction. Every predictor
takes only the pre-intervention response, the intervention descriptor and its own
training split.

Scope note: physics lane allowed_code_roots = ["research/harness", "research/physics"].
This file lives in research/physics. No third-party package is imported: numpy,
scipy, flask, requests and bs4 are all absent from this environment, so every
computation below is pure standard library.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import socket
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode, urlencode

EXP_ID = "EXP-PHYSICS-37385620138"
EXP_DIR = Path(__file__).resolve().parent.parent / "experiments" / EXP_ID
RAW_DIR = EXP_DIR / "raw"
DERIVED_DIR = EXP_DIR / "derived"

# ---------------------------------------------------------------------------
# Frozen scalars (transcribed verbatim from the frozen packet; no retuning)
# ---------------------------------------------------------------------------

# prereg s5.1: master_seed = int(request_hash[:8], 16)
REQUEST_HASH = "1a877a6bcfa9c5c24258d4a86365c2b93f15342fa2db528204b2383639c66d"  # placeholder, see MASTER_SEED below
MASTER_SEED = None  # set by load_request()

# prereg s6.3: cache-relevant header fields inside the response signature
CACHE_HEADERS = ["ETag", "Last-Modified", "Cache-Control", "Vary", "Content-Length"]

# prereg s6.3: d(sig1, sig2) = 0.4*I(status) + 0.3*Jaccard(cache_headers)
#                           + 0.2*I(body_sha) + 0.1*I(structural)
W_STATUS = 0.4
W_JACCARD = 0.3
W_BODY = 0.2
W_STRUCT = 0.1

# prereg s8.1: log_score(pred, obs) = -log(|pred - obs| + EPS)
METRIC_EPS = 1e-10
# prereg s8.2: INERT_INTERVENTION_RATE = fraction with ||delta_treat|| < 0.01
INERT_EPS = 0.01

# prereg s5.2 / s6.1: the frozen mechanism table
MECHANISMS = [
    {
        "mechanism_id": "M_PAGINATION",
        "intervention_type": "query_param",
        "declared_semantic_effect": "Increases pagination offset",
        "parameter": "page",
        "values": ["1", "2", "3", "10", "100"],
    },
    {
        "mechanism_id": "M_SECTION",
        "intervention_type": "path_param",
        "declared_semantic_effect": "Selects document section",
        "parameter": "section",
        "values": ["intro", "methods", "results", "discussion", "appendix"],
    },
    {
        "mechanism_id": "M_ANCHOR",
        "intervention_type": "anchor_fragment",
        "declared_semantic_effect": "Scrolls to anchor target",
        "parameter": "id",
        "values": ["overview", "details", "examples", "references", "see-also"],
    },
]

# prereg s5.2 admission criteria
MIN_TRANSPORT_OK = 12          # of 15 probes
MIN_DISTINCT_SIGNATURES = 2
N_PROBES = 15

USER_AGENT = (
    "SPIDER-Research/2.0 (physics lane; experiment EXP-PHYSICS-37385620138; "
    "stdlib urllib; credential-free public HTML GET)"
)

# ---------------------------------------------------------------------------
# Hashing / IO helpers
# ---------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def write_json(path: Path, obj: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sha256_file(path)


def write_jsonl(path: Path, rows: Iterable[Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    return sha256_file(path)


def read_jsonl(path: Path) -> list:
    rows = []
    with Path(path).open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


# ---------------------------------------------------------------------------
# HTML structural hash  (prereg s6.3: "hash of parsed HTML DOM tree structure
# (tag names, nesting, id/class attrs)").  Implemented with stdlib html.parser
# over a tag-only stream: no text content is recorded, so the hash is a pure
# DOM-shape observable.
# ---------------------------------------------------------------------------


class _StructureHasher(HTMLParser):
    __slots__ = ("_h", "_depth", "_n")

    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._h = hashlib.sha256()
        self._depth = 0
        self._n = 0

    def _record(self, tag: str, depth: int, attrs: dict, closing: bool) -> None:
        ident = (attrs.get("id") or "").strip()
        cls = attrs.get("class") or ""
        classes = ",".join(sorted(c for c in cls.split() if c))
        self._n += 1
        self._h.update(
            f"{depth}|{'/' if closing else ''}{tag}|id={ident}|class={classes}\n".encode()
        )

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self._record(tag, self._depth, d, closing=False)
        if tag not in self.VOID:
            self._depth += 1

    def handle_startendtag(self, tag, attrs):
        self._record(tag, self._depth, dict(attrs), closing=False)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self._depth > 0:
            self._depth -= 1
        self._record(tag, self._depth, {}, closing=True)

    def digest(self) -> str:
        return self._h.hexdigest()

    @property
    def n_nodes(self) -> int:
        return self._n


def structural_hash(body: bytes) -> tuple[str, int]:
    """Return (structural_hash, n_tag_nodes). Never raises."""
    p = _StructureHasher()
    try:
        p.feed(body.decode("utf-8", "replace"))
        p.close()
    except Exception:  # malformed markup must not destroy a raw record
        p._h.update(b"|PARSE_ERROR|")
    return p.digest(), p.n_nodes


# ---------------------------------------------------------------------------
# HTTP  (stdlib urllib only)
# ---------------------------------------------------------------------------


def http_get(url: str, timeout: float = 20.0, extra_headers: dict | None = None) -> dict:
    """One credential-free GET. Returns a RAW record; never raises.

    Records status, all response headers, full-body length, full-body sha256 and
    the DOM structural hash.  Redirects are followed by urllib's default opener,
    so `url` (requested) and `final_url` differ when a redirect occurred; both are
    recorded so that a 3xx-mediated admission is auditable.
    """
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers, method="GET")
    t0 = time.perf_counter()
    rec: dict[str, Any] = {
        "url": url,
        "final_url": None,
        "status": None,
        "resp_headers": {},
        "body_len": 0,
        "body_sha256": None,
        "structural_hash": None,
        "structural_nodes": 0,
        "content_type": None,
        "elapsed_ms": None,
        "transport_error": None,
        "t_requested": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            rec["final_url"] = resp.geturl()
            rec["status"] = int(resp.status)
            rec["resp_headers"] = {k.lower(): v for k, v in resp.headers.items()}
            rec["content_type"] = rec["resp_headers"].get("content-type")
            rec["body_len"] = len(body)
            rec["body_sha256"] = hashlib.sha256(body).hexdigest()
            rec["structural_hash"], rec["structural_nodes"] = structural_hash(body)
    except urllib.error.HTTPError as exc:  # 4xx / 5xx are DATA, not failures
        body = b""
        try:
            body = exc.read()
        except Exception:
            pass
        rec["final_url"] = exc.geturl() if hasattr(exc, "geturl") else url
        rec["status"] = int(exc.code)
        rec["resp_headers"] = {k.lower(): v for k, v in (exc.headers or {}).items()}
        rec["content_type"] = rec["resp_headers"].get("content-type")
        rec["body_len"] = len(body)
        rec["body_sha256"] = hashlib.sha256(body).hexdigest()
        rec["structural_hash"], rec["structural_nodes"] = structural_hash(body)
    except Exception as exc:  # transport-level failure
        rec["transport_error"] = f"{type(exc).__name__}: {exc}"[:200]
    rec["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return rec


# ---------------------------------------------------------------------------
# Response signature and the FROZEN distance  (prereg s6.3)
# ---------------------------------------------------------------------------


def signature(rec: dict) -> dict:
    h = rec.get("resp_headers") or {}
    cache = {k: h.get(k.lower()) for k in CACHE_HEADERS}
    validator = (
        cache.get("ETag")
        or cache.get("Last-Modified")
        or cache.get("Content-Length")
        or "none"
    )
    return {
        "status": rec.get("status"),
        "cache_headers": cache,
        "body_sha256": rec.get("body_sha256"),
        "body_length": rec.get("body_len"),
        "structural_hash": rec.get("structural_hash"),
        "validator_identity": validator,
    }


def _cache_pairs(sig: dict) -> set:
    out = set()
    for k, v in (sig.get("cache_headers") or {}).items():
        if v is None:
            continue
        out.add(f"{k}={v}")
    return out


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def distance_literal(sig1: dict, sig2: dict) -> float:
    """The frozen formula EXACTLY as written: + 0.3 * Jaccard(cache_headers).

    Consequence (measured, not asserted): for two identical signatures this
    returns 0.3, not 0.  prereg calls this a "distance"; it is not one.
    """
    s = 1.0 if sig1.get("status") != sig2.get("status") else 0.0
    j = _jaccard(_cache_pairs(sig1), _cache_pairs(sig2))
    b = 1.0 if sig1.get("body_sha256") != sig2.get("body_sha256") else 0.0
    t = 1.0 if sig1.get("structural_hash") != sig2.get("structural_hash") else 0.0
    return W_STATUS * s + W_JACCARD * j + W_BODY * b + W_STRUCT * t


def distance_corrected(sig1: dict, sig2: dict) -> float:
    """0.3 * (1 - Jaccard), i.e. the only reading under which the frozen weights
    sum to a distance.  Reported as a robustness variant, never as the frozen
    metric."""
    s = 1.0 if sig1.get("status") != sig2.get("status") else 0.0
    j = _jaccard(_cache_pairs(sig1), _cache_pairs(sig2))
    b = 1.0 if sig1.get("body_sha256") != sig2.get("body_sha256") else 0.0
    t = 1.0 if sig1.get("structural_hash") != sig2.get("structural_hash") else 0.0
    return W_STATUS * s + W_JACCARD * (1.0 - j) + W_BODY * b + W_STRUCT * t


def signatures_identical(a: dict, b: dict) -> bool:
    """Componentwise signature equality.  Used as the executor's honest reading of
    prereg s6.2's "||delta_treat|| ~= 0", because the frozen distance cannot
    express zero.  Reported alongside the frozen reading, never instead of it."""
    return (
        a.get("status") == b.get("status")
        and a.get("body_sha256") == b.get("body_sha256")
        and a.get("structural_hash") == b.get("structural_hash")
        and _cache_pairs(a) == _cache_pairs(b)
    )


# ---------------------------------------------------------------------------
# Intervention URL construction  (prereg s6.1 mechanism table)
# ---------------------------------------------------------------------------


def intervention_url(doc_url: str, mechanism: dict, value: str) -> str:
    parts = urlsplit(doc_url)
    itype = mechanism["intervention_type"]
    if itype == "query_param":
        q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if k != mechanism["parameter"]]
        q.append((mechanism["parameter"], value))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q), ""))
    if itype == "path_param":
        path = parts.path.rstrip("/")
        return urlunsplit((parts.scheme, parts.netloc, f"{path}/{value}", parts.query, ""))
    if itype == "anchor_fragment":
        return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, value))
    raise ValueError(itype)


def request_target(url: str) -> str:
    """The request-target a client actually puts on the wire (prereg-relevant:
    RFC 9110 s7.1 excludes the fragment from the request target)."""
    p = urlsplit(url)
    target = p.path or "/"
    if p.query:
        target += "?" + p.query
    return target


# ---------------------------------------------------------------------------
# Predictors  (prereg s7.1 - s7.4)
# ---------------------------------------------------------------------------
#
# Every predictor returns a scalar prediction of the frozen quantity
# `observed_delta` = d(signature(post), signature(baseline)), computed WITHOUT
# access to the post-intervention response.  That scalar-against-scalar form is
# what prereg s8.1 feeds into log_score(pred, obs).
#
# MECHANISM_PRIOR is the executor's transcription of prereg s7.1 into numbers.
# prereg s7.1 states the treatment "uses the mechanism's declared semantic effect
# to predict how the signature should change" without fixing magnitudes, so the
# magnitudes are executor choices, fixed BEFORE any outcome was inspected, and
# derived from the declared semantics themselves:
#
#   * M_ANCHOR declares "Scrolls to anchor target".  A fragment is not part of the
#     HTTP request target (RFC 9110 s7.1), so no conforming server can respond
#     differently.  The semantically correct server-visible prediction is 0.
#   * M_PAGINATION / M_SECTION declare a server-side parameter effect on a
#     document body, so a non-zero body change is predicted, and a parameter that
#     is further from the first value is predicted to change the body more.
#
# The numeric values are therefore not fitted and cannot be fitted (prereg s7.1
# forbids the treatment from using training responses).  A sensitivity sweep over
# an alternative admissible prior is reported separately, because the choice is
# the single largest unidentifiable degree of freedom in the frozen metric.


MECHANISM_PRIOR = {
    # mechanism_id -> {param_value_rank (1-based): predicted observed_delta}
    "M_PAGINATION": {1: 0.30, 2: 0.35, 3: 0.40, 4: 0.45, 5: 0.50},
    "M_SECTION": {1: 0.40, 2: 0.45, 3: 0.50, 4: 0.55, 5: 0.60},
    "M_ANCHOR": {1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00, 5: 0.00},
}

# Alternative admissible prior, used ONLY for the executor's descriptive
# sensitivity sweep (never for the frozen decision reading).
MECHANISM_PRIOR_ALT = {
    "M_PAGINATION": {1: 0.50, 2: 0.50, 3: 0.50, 4: 0.50, 5: 0.50},
    "M_SECTION": {1: 0.50, 2: 0.50, 3: 0.50, 4: 0.50, 5: 0.50},
    "M_ANCHOR": {1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00, 5: 0.00},
}


def predict_mechanism_conditioned(instance: dict, prior: dict | None = None) -> float:
    """prereg s7.1 MECHANISM_CONDITIONED.

    Inputs used: the mechanism declaration (id, declared semantic effect) and the
    bound parameter value's rank within the frozen value list.
    Inputs NOT used: site identity, template identity, any response body, any
    training data, the observed outcome.
    """
    prior = prior or MECHANISM_PRIOR
    table = prior.get(instance["mechanism_id"], {})
    return float(table.get(instance["value_rank"], 0.0))


def predict_cache_revalidation(instance: dict) -> float:
    """prereg s7.2 B_CACHE_REVALIDATION.

    Rule set, derived from RFC 9111 semantics and applied to the request the
    intervention actually issues:

      R1  If the intervention's request-target differs from the baseline's, the
          client holds no stored response for it, so caching cannot alter the
          response and the cache-semantics prediction is 0.
      R2  If the request-target is identical and the baseline carries a usable
          validator, a revalidating client may be answered 304; the predicted
          distance is d(304-signature, baseline-signature), computed from the
          headers alone.
      R3  If the request-target is identical and the baseline carries no usable
          validator, the prediction is 0.
      R4  Vary: contributes only when the intervention changes a field named in
          Vary.  These interventions add no request headers, so contribution 0.

    Inputs used: pre-intervention response headers, intervention descriptor.
    Inputs NOT used: mechanism declaration, bound parameters, site identity,
    training data, observed outcome.
    """
    base = instance.get("baseline_signature")
    if base is None:
        return 0.0
    same_target = request_target(instance["url"]) == request_target(instance["baseline_url"])
    if not same_target:
        return 0.0  # R1
    h = base.get("cache_headers") or {}
    validator = h.get("ETag") or h.get("Last-Modified")
    if not validator:
        return 0.0  # R3
    hypothetical_304 = dict(base)
    hypothetical_304["status"] = 304
    hypothetical_304["cache_headers"] = dict(h)
    hypothetical_304["cache_headers"]["Content-Length"] = "0"
    hypothetical_304["body_sha256"] = None
    hypothetical_304["body_length"] = 0
    return float(distance_corrected(hypothetical_304, base))  # R2


def _empirical_mean(values: list[float], fallback: float) -> float:
    return sum(values) / len(values) if values else fallback


def build_site_memory(train_rows: list[dict], key_fn: Callable[[dict], str],
                      site_fn: Callable[[dict], str], global_fallback: float) -> dict:
    """prereg s7.3 B_SITE_TEMPLATE_MEMORY.

    Fitted on TRAIN rows only: mean observed_delta for each (site,
    action_template) key.  Recorded fallbacks are explicit so that a site-disjoint
    split can be seen to degenerate to a constant rather than hidden.
    """
    by_key: dict[str, list[float]] = defaultdict(list)
    by_site: dict[str, list[float]] = defaultdict(list)
    for row in train_rows:
        by_key[key_fn(row)].append(row["observed_delta"])
        by_site[site_fn(row)].append(row["observed_delta"])
    return {
        "by_key": {k: sum(v) / len(v) for k, v in by_key.items()},
        "key_counts": {k: len(v) for k, v in by_key.items()},
        "by_site": {k: sum(v) / len(v) for k, v in by_site.items()},
        "site_counts": {k: len(v) for k, v in by_site.items()},
        "global_mean": global_fallback,
        "n_key_cells": len(by_key),
        "n_site_cells": len(by_site),
    }


def predict_site_template_memory(instance: dict, model: dict) -> tuple[float, str]:
    key = instance["memory_key"]
    site = instance["site"]
    if key in model["by_key"]:
        return model["by_key"][key], "key"
    if site in model["by_site"]:
        return model["by_site"][site], "site_marginal"
    return model["global_mean"], "global_mean"


def combined_memory_tier(instance: dict, site_model: dict) -> str:
    """Which fallback B_COMBINED_NULL actually used: key, site_marginal or
    global_mean.  Recorded because a site-disjoint split can silently collapse the
    baseline to a constant, and that must be visible rather than implied."""
    return predict_site_template_memory(instance, site_model)[1]


def predict_combined_null(instance: dict, site_model: dict) -> float:
    """prereg s7.4 B_COMBINED_NULL: site-template memory, then a cache-semantics
    correction.  pred_combined = clip(pred_site_memory + pred_cache, 0, 1)."""
    site_pred, _tier = predict_site_template_memory(instance, site_model)
    cache_pred = predict_cache_revalidation(instance)
    return max(0.0, min(1.0, site_pred + cache_pred))


def predict_degenerate_zero(instance: dict) -> float:
    """Executor-added STRONG BASELINE (SB_DEGENERATE_ZERO).

    Predicts 0.0 for every instance.  Uses no mechanism, no site, no parameter, no
    data.  A predictor this trivial must not be able to clear a preregistered
    mechanism-semantic threshold; if it can, the frozen metric does not measure
    mechanism semantics.  NOT part of the frozen decision rule.
    """
    return 0.0


# ---------------------------------------------------------------------------
# The frozen metric  (prereg s8.1)
# ---------------------------------------------------------------------------


def log_score(pred: float, obs: float) -> float:
    return -math.log(abs(pred - obs) + METRIC_EPS)


def residual_effect_size_nats(rows: list[dict], treat_pred, combined_pred) -> dict:
    """residual_i = log_score(treatment, observed) - log_score(combined, observed).
    Aggregate = mean over held-out instances (prereg s8.1)."""
    per = []
    for r in rows:
        obs = r["observed_delta"]
        t = log_score(treat_pred(r), obs)
        c = log_score(combined_pred(r), obs)
        per.append({
            "instance_id": r["instance_id"],
            "site": r["site"],
            "mechanism_id": r["mechanism_id"],
            "observed_delta": obs,
            "pred_treatment": treat_pred(r),
            "pred_combined": combined_pred(r),
            "log_score_treatment": t,
            "log_score_combined": c,
            "residual": t - c,
        })
    n = len(per)
    mean = sum(p["residual"] for p in per) / n if n else None
    return {
        "n": n,
        "mean_residual_nats": mean,
        "mean_log_score_treatment": sum(p["log_score_treatment"] for p in per) / n if n else None,
        "mean_log_score_combined": sum(p["log_score_combined"] for p in per) / n if n else None,
        "per_instance": per,
    }


# ---------------------------------------------------------------------------
# Site-clustered bootstrap  (prereg s11 step 8: 10,000 site-clustered resamples)
# ---------------------------------------------------------------------------


def site_clustered_bootstrap(rows: list[dict], stat_rows: list[dict],
                              n_resamples: int, seed: int,
                              value_fn: Callable[[list[dict]], float | None]) -> dict:
    clusters = sorted({r["site"] for r in rows})
    by_site: dict[str, list[dict]] = defaultdict(list)
    idx_by_id = {r["instance_id"]: r for r in stat_rows}
    for r in stat_rows:
        by_site[r["site"]].append(r)
    if not clusters:
        return {
            "n_resamples": 0, "n_clusters": 0, "point_estimate": None,
            "ci95": [None, None], "n_distinct_cluster_resamples": 0,
            "note": "no test instances: the site-clustered bootstrap has no cluster to resample",
        }
    rng = random.Random(seed)
    draws: list[float] = []
    distinct: set[tuple] = set()
    for _ in range(n_resamples):
        pick = [clusters[rng.randrange(len(clusters))] for _ in range(len(clusters))]
        if len(distinct) < 200000:
            distinct.add(tuple(pick))
        sample: list[dict] = []
        for s in pick:
            sample.extend(by_site[s])
        v = value_fn(sample)
        if v is not None:
            draws.append(v)
    draws.sort()
    if not draws:
        return {
            "n_resamples": n_resamples, "n_clusters": len(clusters),
            "point_estimate": None, "ci95": [None, None],
            "n_distinct_cluster_resamples": len(distinct),
            "note": "all resamples produced an undefined statistic",
        }
    lo = draws[int(0.025 * (len(draws) - 1))]
    hi = draws[int(0.975 * (len(draws) - 1))]
    return {
        "n_resamples": n_resamples,
        "n_clusters": len(clusters),
        "clusters": clusters,
        "point_estimate": value_fn(stat_rows),
        "ci95": [lo, hi],
        "n_distinct_cluster_resamples": len(distinct),
    }


def mean_residual(sample: list[dict]) -> float | None:
    if not sample:
        return None
    return sum(r["residual"] for r in sample) / len(sample)


# ---------------------------------------------------------------------------
# prereg s9.2 null control: NC_PERMUTED_MECHANISM
# ---------------------------------------------------------------------------


def permuted_mechanism_null(rows: list[dict], n_permutations: int, seed: int,
                            treat_pred, combined_pred,
                            value_fn=mean_residual) -> dict:
    """Mechanism declaration and bound parameter values are permuted across
    intervention instances while (site, document, instant, intervention_type)
    are held fixed.  Implemented by permuting the (mechanism_id, value_rank)
    object across instances STRATIFIED BY intervention_type, which is what the
    frozen sentence says; the permuted object is then fed to the SAME frozen
    treatment predictor, so a non-degenerate null requires the declaration to
    change the prediction, which it does (prereg s9.2 non-degeneracy test)."""
    by_type: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        by_type[r["intervention_type"]].append(i)
    stats: list[float] = []
    rng = random.Random(seed)
    for _ in range(n_permutations):
        shuffled = list(rows)
        for _t, idxs in sorted(by_type.items()):
            objs = [(rows[i]["mechanism_id"], rows[i]["value_rank"]) for i in idxs]
            rng.shuffle(objs)
            for i, obj in zip(idxs, objs):
                permuted = dict(shuffled[i])
                permuted["mechanism_id"], permuted["value_rank"] = obj
                shuffled[i] = permuted
        res = residual_effect_size_nats(shuffled, treat_pred, combined_pred)
        if res["mean_residual_nats"] is not None:
            stats.append(res["mean_residual_nats"])
    distinct = sorted(set(stats))
    if not stats:
        return {
            "n_permutations": n_permutations, "n_distinct_values": 0,
            "degenerate": None, "note": "no instances: null not computable",
        }
    stats_sorted = sorted(stats)
    p95 = stats_sorted[int(0.95 * (len(stats_sorted) - 1))]
    return {
        "n_permutations": n_permutations,
        "draws": stats,
        "n_distinct_values": len(distinct),
        "degenerate": len(distinct) <= 1,
        "null_mean": sum(stats) / len(stats),
        "null_min": stats_sorted[0],
        "null_p95": p95,
        "null_max": stats_sorted[-1],
        "first_five": distinct[:5],
    }


def percentile_of(value: float, sample: list[float]) -> float:
    if not sample:
        return None
    below = sum(1 for s in sample if s <= value)
    return below / len(sample)


# ---------------------------------------------------------------------------
# Threaded collection with per-host politeness
# ---------------------------------------------------------------------------


def run_pool(fn: Callable[[Any], Any], items: list, workers: int = 8) -> list:
    """Deterministic-order execution with a fixed worker count.  Results are
    returned in the input order regardless of completion order."""
    out: list[Any] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fn, item): i for i, item in enumerate(items)}
        for fut, i in futures.items():
            pass
        for fut in futures:
            pass
        for fut in list(futures):
            i = futures[fut]
            out[i] = fut.result()
    return out


class HostThrottle:
    """One in-flight request per host at a time, with a minimum inter-request gap."""

    def __init__(self, gap: float = 0.35):
        self.gap = gap
        self._last: dict[str, float] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._guard = threading.Lock()

    def slot(self, host: str):
        with self._guard:
            lock = self._locks.setdefault(host, threading.Lock())
        return lock

    def wait(self, host: str) -> None:
        lock = self.slot(host)
        with lock:
            prev = self._last.get(host)
            if prev is not None:
                delta = time.time() - prev
                if delta < self.gap:
                    time.sleep(self.gap - delta)
            self._last[host] = time.time()


def eTLD1(host: str) -> str:
    """Operational eTLD+1 approximation over a frozen multi-part public-suffix
    sample (the frozen packet does not fix a public-suffix list).  Recorded as a
    stated simplification in the provenance record."""
    parts = host.lower().split(".")
    two = {"co.uk", "ac.uk", "org.uk", "gov.uk", "com.au", "co.jp", "co.nz",
           "org.au", "ac.jp", "com.br", "co.in", "com.cn", "co.za"}
    if len(parts) >= 3 and ".".join(parts[-2:]) in two:
        return ".".join(parts[-3:])
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host.lower()


# ---------------------------------------------------------------------------
# Frozen packet verification
# ---------------------------------------------------------------------------


def load_request() -> dict:
    global MASTER_SEED
    req = json.loads((EXP_DIR / "request.json").read_text())
    MASTER_SEED = int(req["request_hash"][:8], 16)
    return req


def verify_freeze() -> dict:
    fz = json.loads((EXP_DIR / "freeze.json").read_text())
    checks = {}
    for name, want in fz["hashes"].items():
        got = sha256_file(EXP_DIR / name)
        checks[name] = {"recorded": want, "on_disk": got, "match": want == got}
    declared = ["candidate_universe.json", "frozen_pool.json",
                "pilot_data.json", "power_calculation.json"]
    return {
        "freeze": fz,
        "freeze_sha256": sha256_file(EXP_DIR / "freeze.json"),
        "hash_checks": checks,
        "all_hashes_match": all(c["match"] for c in checks.values()),
        "prereg_declared_prefreeze_artifacts": {
            name: {
                "exists_on_disk": (EXP_DIR / name).exists(),
                "hashed_by_freeze": name in fz["hashes"],
            }
            for name in declared
        },
    }