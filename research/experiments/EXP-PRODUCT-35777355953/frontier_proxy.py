#!/usr/bin/env python3
"""
R-FRONTIER-RULE-PROXY for EXP-PRODUCT-35777355953.

VERBATIM SNAPSHOT of the audit-PASS Frontier RECONSTRUCTION-RULE adapter from
EXP-FRONTIER-35766532429 harness (reference file sha256
4db542a727d35b5fee7c36cb842e6abff61ba6c51f5a1fa7f1c67a884d24da6f),
extracted mechanically (lines 28-441 of the reference harness) so that the
"reference frontier RECONSTRUCTION-RULE" baseline executed by this experiment is the
exact reference code text, not a retyping. Imports from the product kernel exactly as
the reference did (spider.kernel._bind, spider.kernel._template_slots).

This file is experiment evidence input for the C8 port-fidelity gate, not product code.
"""
import json, math, random, re, sys, hashlib, time
from pathlib import Path
import numpy as np

from spider.models import Mechanism, Resolution, ResolutionStatus
from spider.kernel import _bind, _template_slots  # as in the reference harness

PARAM_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

FORBIDDEN_KEYS = {
    "alias_family", "query_key", "target_prefix", "routing_prefix", "target_style",
    "path_style", "header_key", "body_field", "auth_scope", "expected_template",
    "resource", "train_template", "dist_template",
}
ALLOWED_STATE_KEYS = {
    "url", "method", "url_path", "url_query", "url_segments",
    "headers_observed", "body_observed",
    "ax_tree_snapshot", "ax_nodes_count", "viewport_observed",
}
STANDARD_HEADERS = {
    "host", "user-agent", "accept", "accept-encoding", "accept-language",
    "connection", "content-length", "content-type", "referer", "origin", "cache-control",
}

def to_native(o):
    if isinstance(o, dict):
        return {k: to_native(v) for k, v in o.items()}
    if isinstance(o, list):
        return [to_native(v) for v in o]
    if isinstance(o, tuple):
        return [to_native(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (str, int, float, bool, type(None))):
        return o
    return str(o)

def sha1_hex(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def norm_key(k: str) -> str:
    return re.sub(r"[^a-z0-9]", "", k.lower())

def make_mechanism(mid, intent, template, confidence):
    return Mechanism(
        mechanism_id=mid,
        intent=intent,
        preconditions={},
        action_template=template,
        postconditions={},
        parameter_slots=[],
        applicability_guards={},
        confidence=confidence,
    )

# ---------------------------------------------------------------- derive_state (whitelist only)
def derive_state(observed_url: str, observed_headers: dict, observed_body: dict):
    method = "GET"
    if "?" in observed_url:
        path_part, query_part = observed_url.split("?", 1)
        url_path = path_part
        url_query = {}
        for kv in query_part.split("&"):
            if not kv:
                continue
            if "=" in kv:
                k, v = kv.split("=", 1)
                url_query[k] = v
            else:
                url_query[kv] = ""
    else:
        url_path = observed_url
        url_query = {}
    url_segments = [s for s in url_path.split("/") if s]
    derived = {
        "url": observed_url,
        "method": method,
        "url_path": url_path,
        "url_query": dict(url_query),
        "url_segments": list(url_segments),
        "headers_observed": dict(observed_headers),
        "body_observed": dict(observed_body),
        "ax_tree_snapshot": None,
        "ax_nodes_count": None,
        "viewport_observed": None,
    }
    extra = set(derived.keys()) - ALLOWED_STATE_KEYS
    assert not extra, f"derived state leaks keys {extra}"
    fb = FORBIDDEN_KEYS & set(derived.keys())
    assert not fb, f"forbidden keys leaked into derived state {fb}"
    for v in derived.values():
        if isinstance(v, dict):
            for k in v:
                assert k not in FORBIDDEN_KEYS, f"forbidden key in channel {k}"
    return derived

# ---------------------------------------------------------------- template introspection
def template_components(template: dict):
    url = template.get("url", "")
    headers = template.get("headers", {})
    body = template.get("body", {})
    url_path = url.split("?", 1)[0] if "?" in url else url
    query_str = url.split("?", 1)[1] if "?" in url else ""
    qkeys = []
    if query_str:
        for kv in query_str.split("&"):
            if not kv:
                continue
            k = kv.split("=", 1)[0] if "=" in kv else kv
            qkeys.append(k)
    segs = [s for s in url_path.split("/") if s]
    static = [s for s in segs if not PARAM_RE.search(s)]
    return {"url": url, "url_path": url_path, "query_str": query_str, "qkeys": qkeys,
            "segs": segs, "static": static, "headers": dict(headers), "body": dict(body)}

def value_shape_ok(template_value: str, observed_value):
    if not isinstance(observed_value, str):
        return False
    slots = PARAM_RE.findall(template_value)
    if slots:
        m = PARAM_RE.search(template_value)
        prefix = template_value[: m.start()]
        if len(observed_value) <= len(prefix):
            return False
        return observed_value.startswith(prefix) and not PARAM_RE.fullmatch(observed_value)
    return observed_value == template_value

def channel_present(cand_keys_vals, observed_raw_to_val):
    if not cand_keys_vals:
        return True, True
    all_present = True
    any_signal = False
    for raw_k, tv in cand_keys_vals.items():
        if raw_k in observed_raw_to_val:
            any_signal = True
            if not value_shape_ok(tv, observed_raw_to_val[raw_k]):
                all_present = False
        else:
            all_present = False
    return all_present, any_signal

def candidate_present(m, derived):
    comps = template_components(m.action_template)
    hdr = comps["headers"]
    bdy = comps["body"]
    qkeys = comps["qkeys"]
    obs_hdr_raw = derived["headers_observed"] or {}
    obs_bdy_raw = derived["body_observed"] or {}
    obs_query_raw = derived["url_query"] or {}
    h_ok, h_sig = channel_present(hdr, obs_hdr_raw)
    b_ok, b_sig = channel_present(bdy, obs_bdy_raw)
    q_ok = True
    for qk in qkeys:
        if qk not in obs_query_raw:
            q_ok = False
    return h_ok and b_ok and q_ok

def candidate_score(m, derived, use_channels=("url", "headers", "body")):
    comps = template_components(m.action_template)
    derived_hdr = derived["headers_observed"] or {}
    derived_bdy = derived["body_observed"] or {}
    derived_query = derived["url_query"] or {}
    use_url = "url" in use_channels
    use_hdr = "headers" in use_channels
    use_bdy = "body" in use_channels
    if use_url and comps["qkeys"]:
        obs_norms = {norm_key(k): k for k in derived_query}
        cand_norms = {norm_key(k) for k in comps["qkeys"]}
        if cand_norms:
            inter = len(cand_norms & set(obs_norms))
            union = len(cand_norms | set(obs_norms))
            query_hit = inter / union
        else:
            query_hit = 1.0
    else:
        query_hit = 1.0
    if use_url:
        obs_segs = derived["url_segments"]
        t_static = comps["static"]
        if not t_static and not obs_segs:
            path_score = 1.0
        elif not t_static or not obs_segs:
            path_score = 0.0
        else:
            inter = len(set(t_static) & set(obs_segs))
            union = len(set(t_static) | set(obs_segs))
            jacc = inter / union if union else 0
            seq = 0
            for a, b in zip(t_static, obs_segs):
                if a == b:
                    seq += 1
                else:
                    break
            seq_score = seq / max(len(t_static), len(obs_segs)) if max(len(t_static), len(obs_segs)) else 0
            path_score = 0.6 * jacc + 0.4 * seq_score
    else:
        path_score = 1.0
    url_score = 0.5 * query_hit + 0.5 * path_score
    def chan_score(cand_vals, obs_raw):
        if not cand_vals:
            return None
        scores = []
        for raw_k, tv in cand_vals.items():
            if raw_k in obs_raw and value_shape_ok(tv, obs_raw[raw_k]):
                scores.append(1.0)
            else:
                scores.append(0.0)
        return float(np.mean(scores))
    h_score = chan_score(comps["headers"], derived_hdr) if use_hdr else None
    b_score = chan_score(comps["body"], derived_bdy) if use_bdy else None
    w_url = 0.35
    w_hdr = 0.35 if h_score is not None else 0.0
    w_bdy = 0.30 if b_score is not None else 0.0
    total_w = w_url + w_hdr + w_bdy
    if total_w == 0:
        return 0.5
    num = w_url * url_score
    if h_score is not None:
        num += w_hdr * h_score
    if b_score is not None:
        num += w_bdy * b_score
    return num / total_w

def softmax(arr, temp=0.15):
    a = np.array(arr, dtype=float) / temp
    m = np.max(a)
    e = np.exp(a - m)
    return e / e.sum()

def deterministic_jitter(intent, derived):
    j = ((int(sha1_hex(derived["url"]), 16) % 7) * 0.003 +
         ((len(derived["url_segments"])) % 3) * 0.002 +
         (int(sha1_hex(intent), 16) % 5) * 0.001)
    return j

LITERAL_SET = {"read", "admin", "write", "owner"}

def adoption_value_template(observed_value, params):
    if not isinstance(observed_value, str):
        return None
    ordered = sorted(params.items(), key=lambda kv: -len(str(kv[1]))) if params else []
    tv = observed_value
    for pk, pv in ordered:
        pvs = str(pv)
        if pvs and pvs in tv:
            tv = tv.replace(pvs, "${%s}" % pk)
    return tv

# ----- multi-channel adoption

def choose_adoptions(derived, candidates, params):
    """Return list of (channel, key, tv) for all adoptable keys not in registry."""
    comps_all = [template_components(m.action_template) for m in candidates]
    cand_hdr_keys = set()
    cand_bdy_keys = set()
    cand_query_keys = set()
    for c in comps_all:
        cand_hdr_keys |= set(c["headers"].keys())
        cand_bdy_keys |= set(c["body"].keys())
        cand_query_keys |= set(c["qkeys"])
    obs_hdr = derived["headers_observed"] or {}
    obs_bdy = derived["body_observed"] or {}
    obs_query = derived["url_query"] or {}
    adoptions = []
    # query
    for k, v in sorted(obs_query.items(), key=lambda kv: kv[0].lower()):
        if k in cand_query_keys:
            continue
        tv = adoption_value_template(v, params)
        if tv is not None:
            # also handle literal case where v == "read" etc without param
            # if tv == v and not any param value in v, keep as is if v in LITERAL_SET
            if tv == v and v not in LITERAL_SET and not any(str(pv) in v for pv in params.values()):
                # if literal not in set, still allow if it's exact expected literal? allow read as literal
                # we will still adopt literal permission queries with literal value
                # need to ensure query with literal read is adopted: keep tv as v
                pass
            adoptions.append(("query", k, tv))
    # headers
    for k, v in sorted(obs_hdr.items(), key=lambda kv: kv[0].lower()):
        if k in cand_hdr_keys or norm_key(k).lower() in STANDARD_HEADERS:
            continue
        tv = adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("headers", k, tv))
    # body
    for k, v in sorted(obs_bdy.items(), key=lambda kv: kv[0].lower()):
        if k in cand_bdy_keys:
            continue
        if not isinstance(v, str) or not v:
            continue
        tv = adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("body", k, tv))
    # For literal query values like "read" where tv == "read" and no param substitution, we need to handle
    # If perm param is "read", then tv for query "read" will be "${perm}" after substitution, good.
    # If not, ensure literal query "read" without param is still adopted as "read"
    return adoptions

def rewrite_template_multi(base, adoptions, derived):
    """Rewrite base template incorporating all adoptions (header+body+query)."""
    comps = template_components(base.action_template)
    obs_hdr = derived["headers_observed"] or {}
    obs_bdy = derived["body_observed"] or {}
    obs_query = derived["url_query"] or {}
    base_path = comps["url_path"]
    # collect query adoptions and existing base query
    query_adopts = [(k,tv) for ch,k,tv in adoptions if ch=="query"]
    header_adopts = [(k,tv) for ch,k,tv in adoptions if ch=="headers"]
    body_adopts = [(k,tv) for ch,k,tv in adoptions if ch=="body"]
    # build query parts: keep base query keys that are present in observed (exact key)
    qparts = []
    # existing base query keys that are still valid (exact match in observed)
    for qk in comps["qkeys"]:
        if qk in obs_query:
            # need original template value for that key; extract from base url query string
            # parse base query string to get value
            qs = comps["query_str"]
            for kv in qs.split("&"):
                if "=" in kv:
                    kk,vv = kv.split("=",1)
                    if kk == qk:
                        qparts.append(f"{qk}={vv}")
                        break
                elif kv == qk:
                    qparts.append(qk)
                    break
    # add query adoptions (if not already present)
    for k,tv in query_adopts:
        if k not in [p.split("=")[0] for p in qparts]:
            qparts.append(f"{k}={tv}")
    url = base_path + ("?" + "&".join(qparts) if qparts else "")
    # headers
    new_headers = {}
    for k,tv in comps["headers"].items():
        if k in obs_hdr:
            new_headers[k]=tv
    for k,tv in header_adopts:
        new_headers[k]=tv
    # body
    new_body = {}
    for k,tv in comps["body"].items():
        if k in obs_bdy:
            new_body[k]=tv
    for k,tv in body_adopts:
        new_body[k]=tv
    out = {"url": url}
    if new_headers:
        out["headers"]=new_headers
    if new_body:
        out["body"]=new_body
    return out

def reconstruct_resolve(intent, derived_context, retrieved_candidates, params,
                        use_channels=("url", "headers", "body")):
    """Genuine non-oracle reconstruction adapter with multi-channel support."""
    if not retrieved_candidates:
        score = 0.05 + (int(sha1_hex(intent), 16) % 10) * 0.002
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          "no applicable mechanism - abstain", confidence=float(score))
    work = dict(derived_context)
    work["headers_observed"] = dict(derived_context["headers_observed"] or {}) if "headers" in use_channels else {}
    work["body_observed"] = dict(derived_context["body_observed"] or {}) if "body" in use_channels else {}
    scores = [candidate_score(m, work, use_channels=use_channels) for m in retrieved_candidates]
    best_sel = int(np.argmax(scores))
    # check if rewriting needed: any adoptable keys exist
    adoptions = choose_adoptions(work, retrieved_candidates, params)
    # if no adoptions needed and candidate_present -> selection branch
    if not adoptions and candidate_present(retrieved_candidates[best_sel], work):
        m = retrieved_candidates[best_sel]
        probs = softmax(scores, temp=0.15)
        conf = float(np.max(probs))
        jitter = deterministic_jitter(intent, work)
        conf = min(0.98, max(0.02, conf * 0.85 + 0.12 + jitter))
        if conf < 0.80:
            return Resolution(ResolutionStatus.UNKNOWN, None,
                              f"low confidence {conf:.3f} abstain", confidence=conf)
        required = _template_slots(m.action_template)
        if any(s not in params for s in required):
            return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots after selection",
                              confidence=float(0.3 + len(required) * 0.01))
        bound = _bind(m.action_template, params)
        return Resolution(ResolutionStatus.EXECUTABLE, m.mechanism_id,
                          f"selected structurally matching candidate score {scores[best_sel]:.3f} conf {conf:.3f}",
                          bound_action=bound, confidence=conf)
    # rewrite branch: need to adopt observed keys
    if not adoptions:
        conf = 0.2 + (int(sha1_hex(intent), 16) % 10) * 0.01
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          "cannot reconstruct - no adoptable signal", confidence=float(conf))
    base = retrieved_candidates[best_sel]
    new_template = rewrite_template_multi(base, adoptions, work)
    rewrite_score = 1.0
    probs = softmax(scores + [rewrite_score], temp=0.15)
    conf = float(np.max(probs))
    jitter = deterministic_jitter(intent, work)
    conf = min(0.98, max(0.02, conf * 0.85 + 0.12 + jitter))
    if conf < 0.80:
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          f"low confidence {conf:.3f} abstain", confidence=conf)
    required = _template_slots(new_template)
    if any(s not in params for s in required):
        return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots after rewrite",
                          confidence=float(0.3 + len(required) * 0.01))
    bound = _bind(new_template, params)
    return Resolution(ResolutionStatus.EXECUTABLE, base.mechanism_id,
                      f"rewrote base template adopting {len(adoptions)} observed keys {adoptions} conf {conf:.3f}",
                      bound_action=bound, confidence=conf)

# ================================================================ TASK GENERATION
tasks = []

