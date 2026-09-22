#!/usr/bin/env python3
"""
EXP-FRONTIER-35773143736 EXECUTE — sequenced synthetic LEARNED-gate experiment for C-SEMANTIC-RESOLVE.

Frozen design: learned GRPO/System-One critique-reconstruct adapter (RECONSTRUCTION-LEARNED),
trained ONLY on the synthetic orthogonal single-channel train split (21 standard tasks,
families 0-2, is_heldout=False; 0/9 held-out forms, 0/10 mixed templates), 3 seeds 42/43/44,
model-derived calibrated confidence (softmax over learned scores, gated UNKNOWN<0.80, std>0.05),
must match RECONSTRUCTION-RULE (validated parent proxy) within 0.10 correct and 0.05 ECE
on synthetic pooled alias-OOD (40 = 30 orthogonal + 10 mixed) as gate G0, then conditional
live BrowserGym 0.14.3 1280x720 WebShop/ALFWorld (structural substrate probe performed;
packages absent -> exploratory bound with disclosure, NOT MEASUREMENT_INVALID).

B-RAG-EMBED (sentence-transformers all-MiniLM-L6-v2, offline, deterministic) is a REAL
retrieval-only baseline in this run (parent had to mark it unavailable).

Forbidden keys never enter features (derive_state whitelist asserts). RULE reconstruct_resolve
reuses the parent (EXP-FRONTIER-35766532429, audit PASS) implementation verbatim.
The task fixture is regenerated with the parent generator (seed 42) and must be byte-
identical to the parent fixture tasks.json (sha256 4abf1487...).

RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT separation: this script only measures and
writes raw/derived artifacts + derived_metrics.json. result.json/report.md/provenance.json are
authored separately from these measurements.

Code roots: research/frontier (allowed). No src/ edits. No git operations.
"""
import json, math, random, re, sys, hashlib, time, glob, os
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from spider.kernel import SpiderKernel, _bind, _template_slots
from spider.models import Mechanism, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry

SEED = 42
random.seed(SEED)
rng = np.random.RandomState(SEED)

EXP_ID = "EXP-FRONTIER-35773143736"
OUT_DIR = Path("/home/runner/work/Spider/Spider/research/experiments") / EXP_ID
PARENT_DIR = Path("/home/runner/work/Spider/Spider/research/experiments") / "EXP-FRONTIER-35766532429"

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
        mechanism_id=mid, intent=intent, preconditions={},
        action_template=template, postconditions={}, parameter_slots=[],
        applicability_guards={}, confidence=confidence,
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
        "url": observed_url, "method": method, "url_path": url_path,
        "url_query": dict(url_query), "url_segments": list(url_segments),
        "headers_observed": dict(observed_headers), "body_observed": dict(observed_body),
        "ax_tree_snapshot": None, "ax_nodes_count": None, "viewport_observed": None,
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
    """Return list of (channel, key, tv) for all adoptable keys not in registry (RULE enumeration)."""
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
    for k, v in sorted(obs_query.items(), key=lambda kv: kv[0].lower()):
        if k in cand_query_keys:
            continue
        tv = adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("query", k, tv))
    for k, v in sorted(obs_hdr.items(), key=lambda kv: kv[0].lower()):
        if k in cand_hdr_keys or norm_key(k).lower() in STANDARD_HEADERS:
            continue
        tv = adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("headers", k, tv))
    for k, v in sorted(obs_bdy.items(), key=lambda kv: kv[0].lower()):
        if k in cand_bdy_keys:
            continue
        if not isinstance(v, str) or not v:
            continue
        tv = adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("body", k, tv))
    return adoptions

def rewrite_template_multi(base, adoptions, derived):
    """Rewrite base template incorporating all adoptions (header+body+query)."""
    comps = template_components(base.action_template)
    obs_hdr = derived["headers_observed"] or {}
    obs_bdy = derived["body_observed"] or {}
    obs_query = derived["url_query"] or {}
    base_path = comps["url_path"]
    query_adopts = [(k, tv) for ch, k, tv in adoptions if ch == "query"]
    header_adopts = [(k, tv) for ch, k, tv in adoptions if ch == "headers"]
    body_adopts = [(k, tv) for ch, k, tv in adoptions if ch == "body"]
    qparts = []
    for qk in comps["qkeys"]:
        if qk in obs_query:
            qs = comps["query_str"]
            for kv in qs.split("&"):
                if "=" in kv:
                    kk, vv = kv.split("=", 1)
                    if kk == qk:
                        qparts.append(f"{qk}={vv}")
                        break
                elif kv == qk:
                    qparts.append(qk)
                    break
    for k, tv in query_adopts:
        if k not in [p.split("=")[0] for p in qparts]:
            qparts.append(f"{k}={tv}")
    url = base_path + ("?" + "&".join(qparts) if qparts else "")
    new_headers = {}
    for k, tv in comps["headers"].items():
        if k in obs_hdr:
            new_headers[k] = tv
    for k, tv in header_adopts:
        new_headers[k] = tv
    new_body = {}
    for k, tv in comps["body"].items():
        if k in obs_bdy:
            new_body[k] = tv
    for k, tv in body_adopts:
        new_body[k] = tv
    out = {"url": url}
    if new_headers:
        out["headers"] = new_headers
    if new_body:
        out["body"] = new_body
    return out

def reconstruct_resolve(intent, derived_context, retrieved_candidates, params,
                        use_channels=("url", "headers", "body")):
    """Genuine non-oracle reconstruction adapter (RULE proxy, RULE branch) — parent verbatim."""
    if not retrieved_candidates:
        score = 0.05 + (int(sha1_hex(intent), 16) % 10) * 0.002
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          "no applicable mechanism - abstain", confidence=float(score))
    work = dict(derived_context)
    work["headers_observed"] = dict(derived_context["headers_observed"] or {}) if "headers" in use_channels else {}
    work["body_observed"] = dict(derived_context["body_observed"] or {}) if "body" in use_channels else {}
    scores = [candidate_score(m, work, use_channels=use_channels) for m in retrieved_candidates]
    best_sel = int(np.argmax(scores))
    adoptions = choose_adoptions(work, retrieved_candidates, params)
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

# ================================================================ TASK GENERATION  (parent verbatim, seed 42)
tasks = []

def add_task(task_id, stratum, family, intent, derived, params, registry, hidden,
             expected_outcome, is_heldout):
    tasks.append({
        "task_id": task_id, "stratum": stratum, "family": family, "intent": intent,
        "derived_context": derived, "params": params, "registry": registry,
        "hidden_expected": hidden, "expected_outcome": expected_outcome,
        "is_heldout": is_heldout,
    })

def observed_request_for(template, params):
    bound = _bind(template, params)
    return bound

def make_alias_task(fam, idx, is_heldout, template, train_tmpl, dist_tmpl, low_tmpl, intent,
                    derived, params, hidden):
    m_train = make_mechanism(f"m-{fam}-{idx}-train", intent, train_tmpl, 0.9)
    m_dist = make_mechanism(f"m-{fam}-{idx}-dist", intent, dist_tmpl, 0.9)
    m_low = make_mechanism(f"m-{fam}-{idx}-low", intent, low_tmpl, 0.8)
    registry = [m_train, m_dist, m_low]
    expected_bound = _bind(template, params)
    hidden = dict(hidden)
    hidden["expected_template"] = template
    hidden["expected_bound"] = expected_bound
    add_task(f"alias-{fam}-{idx}", "alias-OOD", fam, intent, derived, params, registry,
             hidden, "correct", is_heldout)

def with_base(tmpl, base):
    out = {"url": tmpl["url"].replace("{BASE}", base)}
    if "headers" in tmpl:
        out["headers"] = dict(tmpl["headers"])
    if "body" in tmpl:
        out["body"] = dict(tmpl["body"])
    return out

HDR_DOC = [
    {"url": "{BASE}", "headers": {"ApiKey": "${token}"}},
    {"url": "{BASE}", "headers": {"X-Reset-Token": "${token}"}},
    {"url": "{BASE}", "headers": {"Authorization": "Bearer ${token}"}},
]
HDR_NOVEL = [
    {"url": "{BASE}", "headers": {"X-Api-Key": "${token}"}},
    {"url": "{BASE}", "headers": {"X-Auth-Key": "${token}"}},
    {"url": "{BASE}", "headers": {"Api-Token": "${token}"}},
]
BDY_DOC = [
    {"url": "{BASE}", "body": {"apiKey": "${token}"}},
    {"url": "{BASE}", "body": {"key": "${token}"}},
    {"url": "{BASE}", "body": {"token": "${token}"}},
]
BDY_NOVEL = [
    {"url": "{BASE}", "body": {"api_token": "${token}"}},
    {"url": "{BASE}", "body": {"authToken": "${token}"}},
    {"url": "{BASE}", "body": {"access_key": "${token}"}},
]
AUTH_DOC = [
    {"url": "{BASE}?scope=read"},
    {"url": "{BASE}?admin_scope=${perm}"},
    {"url": "{BASE}", "headers": {"X-Permission": "${perm}"}},
]
AUTH_NOVEL = [
    {"url": "{BASE}?permission=read"},
    {"url": "{BASE}?access_scope=read"},
    {"url": "{BASE}", "headers": {"X-Scope": "${perm}"}},
]
DOCS = [HDR_DOC, BDY_DOC, AUTH_DOC]
NOVELS = [HDR_NOVEL, BDY_NOVEL, AUTH_NOVEL]
INTENT_F = ["fetch_user_hdr", "create_item_body", "grant_access_auth"]
SLOT_F = ["token", "token", "perm"]
STANDARD_BASES = [
    "/api/data", "/api/users", "/v2/items", "/v1/orders",
    "/admin/settings", "/api/reports", "/v3/audit",
]
HELDOUT_BASES = ["/api/data", "/api/v2/data", "/api/v3/data"]

for fam in range(3):
    doc = DOCS[fam]
    novel = NOVELS[fam]
    slot = SLOT_F[fam]
    for i in range(7):
        base = STANDARD_BASES[i]
        tmpl = with_base(doc[2], base)
        intent = f"{INTENT_F[fam]}_{i}"
        params = {"token": f"tok_{fam}_{i}"} if slot == "token" else {"perm": "read"}
        bound = observed_request_for(tmpl, params)
        derived = derive_state(bound["url"], bound.get("headers", {}), bound.get("body", {}))
        make_alias_task(fam, i, False, tmpl, with_base(doc[0], base),
                        with_base(doc[1], base), with_base(novel[0], base), intent, derived,
                        params, {"alias_family": fam, "is_heldout": False,
                                 "train_template": with_base(doc[0], base),
                                 "dist_template": with_base(doc[1], base)})
    for j in range(3):
        i = 7 + j
        base = HELDOUT_BASES[j]
        tmpl = with_base(novel[j], base)
        intent = f"{INTENT_F[fam]}_{i}"
        params = {"token": f"tok_{fam}_{i}"} if slot == "token" else {"perm": "read"}
        bound = observed_request_for(tmpl, params)
        derived = derive_state(bound["url"], bound.get("headers", {}), bound.get("body", {}))
        make_alias_task(fam, i, True, tmpl, with_base(doc[0], base),
                        with_base(doc[1], base), with_base(doc[2], base), intent, derived,
                        params, {"alias_family": fam, "is_heldout": True,
                                 "train_template": with_base(doc[0], base),
                                 "dist_template": with_base(doc[1], base)})

MIXED_BASES = ["/api/data", "/api/users", "/v2/items", "/v1/orders", "/admin/settings",
               "/api/reports", "/v3/audit", "/api/v2/data", "/api/v3/data", "/v2/audit"]
for i in range(10):
    base = MIXED_BASES[i]
    tmpl = {
        "url": f"{base}?permission=${{perm}}",
        "headers": {"X-Api-Key": "${token}"},
        "body": {"api_token": "${token}"}
    }
    intent = f"mixed_intent_{i}"
    params = {"token": f"tok_mix_{i}", "perm": "read"}
    bound = observed_request_for(tmpl, params)
    derived = derive_state(bound["url"], bound.get("headers", {}), bound.get("body", {}))
    train_tmpl = {"url": base, "headers": {"ApiKey": "${token}"}}
    dist_tmpl = {"url": base, "body": {"apiKey": "${token}"}}
    low_tmpl = {"url": f"{base}?admin_scope=${{perm}}"}
    make_alias_task(3, i, False, tmpl, train_tmpl, dist_tmpl, low_tmpl, intent, derived, params,
                    {"alias_family": 3, "is_heldout": False, "is_mixed": True,
                     "train_template": train_tmpl, "dist_template": dist_tmpl})

for t in tasks:
    if t["family"] == 3:
        idx = t["task_id"].split("-")[-1]
        t["task_id"] = f"mixed-{idx}"
        for m in t["registry"]:
            m.mechanism_id = m.mechanism_id.replace("m-3-", "m-mixed-")

exact_tmpls = [
    {"url": "/api/data", "headers": {"ApiKey": "${token}"}},
    {"url": "/api/data", "body": {"apiKey": "${token}"}},
    {"url": "/api/auth?scope=read"},
    {"url": "/api/auth", "headers": {"X-Scope": "${perm}"}},
    {"url": "/api/data", "headers": {"X-Reset-Token": "${token}"}},
    {"url": "/api/data", "body": {"key": "${token}"}},
    {"url": "/api/auth?admin_scope=${perm}"},
    {"url": "/api/data", "headers": {"Authorization": "Bearer ${token}"}},
    {"url": "/api/data", "body": {"token": "${token}"}},
    {"url": "/api/data", "headers": {"X-Api-Key": "${token}"}},
    {"url": "/api/data", "body": {"api_token": "${token}"}},
    {"url": "/api/auth", "headers": {"X-Permission": "${perm}"}},
]
for i, tmpl in enumerate(exact_tmpls):
    if "body" in tmpl:
        fam = 1
    elif "headers" in tmpl:
        fam = 0
    else:
        fam = 2
    intent = f"exact_intent_{i}"
    if "${perm}" in str(tmpl):
        params = {"perm": "read"}
    else:
        params = {"token": f"tok_x{i}"}
    if "${token}" in str(tmpl) and "${perm}" not in str(tmpl):
        params = {"token": f"tok_x{i}"}
    bound = _bind(tmpl, params)
    derived = derive_state(bound["url"], bound.get("headers", {}), bound.get("body", {}))
    m = make_mechanism(f"m-exact-{i}", intent, tmpl, 0.9)
    hidden = {"expected_template": tmpl, "expected_bound": bound}
    add_task(f"exact-{i}", "exact-match", fam, intent, derived, params, [m], hidden, "correct", False)

for i in range(12):
    fam = i % 3
    if fam == 0:
        t1 = {"url": "/api/data", "headers": {"ApiKey": "${token}"}}
        t2 = {"url": "/api/data", "headers": {"X-Reset-Token": "${token}"}}
    elif fam == 1:
        t1 = {"url": "/api/data", "body": {"apiKey": "${token}"}}
        t2 = {"url": "/api/data", "body": {"key": "${token}"}}
    else:
        t1 = {"url": "/api/auth?scope=read"}
        t2 = {"url": "/api/auth", "headers": {"X-Scope": "${perm}"}}
    intent = f"noapp_intent_{i}_xyz"
    m1 = make_mechanism(f"m-noapp-{i}-a", f"report_summary_{i}", t1, 0.9)
    m2 = make_mechanism(f"m-noapp-{i}-b", f"list_users_{i}", t2, 0.9)
    params = {"token": f"tok_n{i}", "perm": "read"}
    derived = derive_state("/api/unknown", {"Host": "api.example.com"}, {})
    hidden = {"expected_template": None, "expected_bound": None}
    add_task(f"noapp-{i}", "no-applicable", fam, intent, derived, params, [m1, m2],
             hidden, "unknown", False)

for i in range(6):
    intent = f"empty_intent_{i}"
    params = {"token": "val", "perm": "read"}
    derived = derive_state("/api/unknown", {"Host": "api.example.com"}, {})
    hidden = {"expected_template": None, "expected_bound": None}
    add_task(f"empty-{i}", "empty-registry", None, intent, derived, params, [], hidden,
             "unknown", False)

# ---- leakage and oracle checks (0/40 template leak; registry intent-equality leak 0/40)
leak = 0
for t in tasks:
    if t["stratum"] == "alias-OOD":
        exp = t["hidden_expected"]["expected_template"]
        for m in t["registry"]:
            if m.action_template == exp:
                leak += 1
assert leak == 0, f"template leak {leak}"
assert len([t for t in tasks if t["stratum"] == "alias-OOD"]) == 40
assert len([t for t in tasks if t["stratum"] == "exact-match"]) == 12
assert len([t for t in tasks if t["stratum"] == "no-applicable"]) == 12
assert len([t for t in tasks if t["stratum"] == "empty-registry"]) == 6
print(f"tasks {len(tasks)} template_leak {leak}")

def tasks_serialized():
    out = []
    for t in tasks:
        out.append({
            "task_id": t["task_id"], "stratum": t["stratum"], "family": t["family"],
            "intent": t["intent"], "derived_context": t["derived_context"],
            "params": t["params"], "hidden_expected": t["hidden_expected"],
            "expected_outcome": t["expected_outcome"], "is_heldout": t["is_heldout"],
            "registry": [{"mechanism_id": m.mechanism_id, "intent": m.intent,
                          "template": m.action_template, "confidence": m.confidence}
                         for m in t["registry"]],
        })
    return out

_ser = json.dumps(tasks_serialized(), sort_keys=True)
if PARENT_DIR.joinpath("tasks.json").exists():
    parent_fixture = json.dumps(json.load(open(PARENT_DIR / "tasks.json")), sort_keys=True)
    fixture_identical = (_ser == parent_fixture)
    print("fixture_identical_to_parent_tasks_json:", fixture_identical)
else:
    fixture_identical = False
    print("parent fixture not found; cannot compare")

# ================================================================ LEARNED TRAIN SPLIT (frozen: single-channel orthogonal, is_heldout=False)
train_split = [t for t in tasks if t["stratum"] == "alias-OOD" and t["family"] in (0, 1, 2) and not t["is_heldout"]]
heldout9_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] in (0, 1, 2) and t["is_heldout"]]
mixed_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] == 3]

def observed_template_text(t):
    ht = json.dumps(t["hidden_expected"]["expected_template"], sort_keys=True)
    return ht

train_observed_set = {observed_template_text(t) for t in train_split}
heldout_leak_in_train = [tid for tid in heldout9_ids
                         if observed_template_text(next(t for t in tasks if t["task_id"] == tid)) in train_observed_set]
mixed_leak_in_train = [tid for tid in mixed_ids
                       if observed_template_text(next(t for t in tasks if t["task_id"] == tid)) in train_observed_set]
assert len(heldout_leak_in_train) == 0, f"held-out forms leaked into train {heldout_leak_in_train}"
assert len(mixed_leak_in_train) == 0, f"mixed templates leaked into train {mixed_leak_in_train}"
print(f"train_split n={len(train_split)} heldout_leak_in_train={len(heldout_leak_in_train)} mixed_leak_in_train={len(mixed_leak_in_train)}")

train_split_inventory = {
    "n_train_tasks": len(train_split),
    "task_ids": [t["task_id"] for t in train_split],
    "families": sorted({t["family"] for t in train_split}),
    "observed_templates_in_train": sorted(train_observed_set),
    "heldout9_ids_excluded": heldout9_ids,
    "mixed_ids_excluded": mixed_ids,
    "heldout9_templates_in_train": heldout_leak_in_train,
    "mixed_templates_in_train": mixed_leak_in_train,
    "leak_0_of_9": len(heldout_leak_in_train) == 0,
    "leak_0_of_10": len(mixed_leak_in_train) == 0,
    "note": "train split = synthetic orthogonal single-channel tasks (families 0-2, is_heldout=False) only",
}

# ================================================================ LEARNED GRPO ADAPTER (torch, CPU)
import torch
import torch.nn as nn
import torch.nn.functional as F

MAX_CAND = 3
MAX_ADOPT = 4
CONF_GATE = 0.80

def _candidate_feature_cache(m, derived):
    s_all = candidate_score(m, derived, use_channels=("url", "headers", "body"))
    s_u = candidate_score(m, derived, use_channels=("url",))
    s_uh = candidate_score(m, derived, use_channels=("url", "headers"))
    s_ub = candidate_score(m, derived, use_channels=("url", "body"))
    comps = template_components(m.action_template)
    return [s_all, s_u, s_uh, s_ub,
            float(bool(comps["qkeys"])), float(bool(comps["headers"])), float(bool(comps["body"])),
            float(len(comps["static"])), float(len(comps["qkeys"])),
            float(len(comps["headers"])), float(len(comps["body"]))]

def build_feature_vector(intent, derived, candidates, params):
    """46-dim structural feature vector. Uses ONLY allowed observation-derived fields + intent + candidate templates."""
    obs_query = derived.get("url_query") or {}
    obs_hdr = derived.get("headers_observed") or {}
    obs_bdy = derived.get("body_observed") or {}
    feats = []
    feats.append(float(len(intent)))
    feats.append(float(len(derived.get("url_segments") or [])))
    feats.append(float(len(obs_query)))
    feats.append(float(len(obs_hdr)))
    feats.append(float(len(obs_bdy)))
    comps_all = [template_components(m.action_template) for m in candidates]
    cand_q = set(); cand_h = set(); cand_b = set()
    for c in comps_all:
        cand_q |= set(c["qkeys"]); cand_h |= set(c["headers"]); cand_b |= set(c["body"])
    adopt_q = [k for k in obs_query if k not in cand_q]
    adopt_h = [k for k in obs_hdr if norm_key(k).lower() not in STANDARD_HEADERS and k not in cand_h]
    adopt_b = [k for k in obs_bdy if k not in cand_b and isinstance(obs_bdy[k], str) and obs_bdy[k]]
    feats.append(float(len(adopt_q)))
    feats.append(float(len(adopt_h)))
    feats.append(float(len(adopt_b)))
    feats.append(float(len(candidates)))
    feats.append(float(any(m.intent == intent for m in candidates)))
    for i in range(MAX_CAND):
        if i < len(candidates):
            m = candidates[i]
            feats.extend(_candidate_feature_cache(m, derived))
            feats.append(float(m.intent == intent))
        else:
            feats.extend([0.0] * 12)
    assert len(feats) == 46, len(feats)
    extra = set(derived.keys()) - ALLOWED_STATE_KEYS
    assert not extra
    return np.array(feats, dtype=np.float32)

def filtered_candidates(task):
    """Candidate set passed to adapters: intent-matching + slot-available registry mechanisms."""
    cands = [m for m in task["registry"] if m.intent == task["intent"]]
    out = []
    for m in cands:
        required = set(m.parameter_slots) | _template_slots(m.action_template)
        if all(slot in task["params"] for slot in required):
            out.append(m)
    return out

def adoption_slots(task):
    """Adoptable-key slots (max MAX_ADOPT), same enumeration as RULE's choose_adoptions."""
    cands = filtered_candidates(task)
    slots = choose_adoptions(task["derived_context"], cands, task["params"])
    return slots[:MAX_ADOPT]

SLOT_FEAT_DIM = 8

def slot_feature(channel, key, tv, params):
    """Per-slot observation-derived features (channel one-hot, key/value shape, param coupling)."""
    cq = 1.0 if channel == "query" else 0.0
    ch_ = 1.0 if channel == "headers" else 0.0
    cb = 1.0 if channel == "body" else 0.0
    nk = float(len(norm_key(key)))
    nl = float(min(len(str(tv)), 40.0) / 40.0)
    kv = float(any(str(pv) in str(tv) for pv in params.values()))
    lit = float(str(tv) in LITERAL_SET)
    std = float(norm_key(key) in {norm_key(h) for h in STANDARD_HEADERS})
    return [cq, ch_, cb, nk / 20.0, nl, kv, lit, std]

def slot_features_tensor(task):
    slots = adoption_slots(task)
    feats = np.zeros((MAX_ADOPT, SLOT_FEAT_DIM), dtype=np.float32)
    for i, (ch, k, tv) in enumerate(slots):
        feats[i] = slot_feature(ch, k, tv, task["params"])
    return {"slots": slots, "feats": torch.from_numpy(feats).unsqueeze(0), "n": len(slots)}

class GRPOAdapter(nn.Module):
    """Compact critiquer-reconstructor: temperature-scaled softmax policy (candidate + rewrite-gate
    logits), SHARED per-slot adoption head (slot-invariant: can compose multi-slot adoption across
    channels), model-derived calibrated confidence = softmax over learned scores (candidate logits +
    rewrite logit when rewriting) with learned inverse temperature, gated UNKNOWN<0.80 (frozen spec:
    'softmax/budget-derived, gated UNKNOWN when max_score<0.80')."""
    def __init__(self, D=46, hid=128):
        super().__init__()
        self.fc1 = nn.Linear(D, hid)
        self.fc2 = nn.Linear(hid, hid // 2)
        self.cand_logits = nn.Linear(hid // 2, MAX_CAND)
        self.rewrite_logit = nn.Linear(hid // 2, 1)
        self.slot_head = nn.Linear(hid // 2 + SLOT_FEAT_DIM, 1)
        self.inv_temp = nn.Parameter(torch.tensor(1.0))

    def tau(self):
        return torch.clamp(F.softplus(self.inv_temp), min=0.05, max=8.0)

    def forward(self, x, slot_feats):
        # x: (1, D); slot_feats: (1, MAX_ADOPT, SLOT_FEAT_DIM)
        h = torch.relu(self.fc1(x))
        h = torch.relu(self.fc2(h))
        cl = self.cand_logits(h)
        rl = self.rewrite_logit(h)
        zz = h.unsqueeze(1).expand(-1, MAX_ADOPT, -1)
        inp = torch.cat([zz, slot_feats], dim=-1)
        al = self.slot_head(inp).squeeze(-1)  # (1, MAX_ADOPT)
        return {"cand_logits": cl, "rewrite_logit": rl, "adopt_logits": al}

def action_confidence(model, cand_logits_masked, rewrite_logit, n_cands, rewrite, tau):
    """Model-derived softmax confidence over learned scores (max_score), mapped to [0.02,0.98].
    No-candidate tasks handled by caller with structural abstain confidence (RULE-mirror)."""
    if n_cands <= 0:
        return None
    if rewrite:
        scores = torch.cat([cand_logits_masked[0, :n_cands], rewrite_logit[0]])
    else:
        scores = cand_logits_masked[0, :n_cands]
    p = torch.softmax(scores / tau, dim=0)
    return float(0.02 + 0.96 * float(p.max()))

def structural_abstain_confidence(intent):
    return float(0.05 + (int(sha1_hex(intent), 16) % 10) * 0.002)

def mask_cand_logits(cl, n_cands):
    m = torch.full_like(cl, -1e9)
    if n_cands > 0:
        m[..., :n_cands] = cl[..., :n_cands]
    return m

def learned_resolution_from_action(task, cand_idx, rewrite, adopt_mask, conf):
    """Deterministic resolution given learned decisions (shared train/eval mechanics; no oracle)."""
    cands = filtered_candidates(task)
    if not cands:
        return Resolution(ResolutionStatus.UNKNOWN, None, "learned: no applicable mechanism", confidence=conf)
    m = cands[cand_idx]
    if rewrite:
        slots = adoption_slots(task)
        adoptions = [slots[i] for i in range(len(slots)) if adopt_mask[i] == 1]
        new_template = rewrite_template_multi(m, adoptions, task["derived_context"]) if adoptions else None
        if new_template is not None:
            required = _template_slots(new_template)
            if all(s in task["params"] for s in required):
                bound = _bind(new_template, task["params"])
                return Resolution(ResolutionStatus.EXECUTABLE, m.mechanism_id,
                                  f"learned rewrite adopting {len(adoptions)} keys", bound_action=bound, confidence=conf)
    required = _template_slots(m.action_template)
    if all(s in task["params"] for s in required):
        bound = _bind(m.action_template, task["params"])
        return Resolution(ResolutionStatus.EXECUTABLE, m.mechanism_id,
                          "learned selection", bound_action=bound, confidence=conf)
    return Resolution(ResolutionStatus.UNKNOWN, None, "learned: cannot bind", confidence=conf)

def gated_learned_resolution(task, cand_idx, rewrite, adopt_mask, conf):
    """Apply frozen UNKNOWN gate conf<0.80: gated resolution is the adapter's observable output."""
    res = learned_resolution_from_action(task, cand_idx, rewrite, adopt_mask, conf)
    if conf < CONF_GATE:
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          f"learned gated confidence {conf:.3f} abstain", confidence=conf)
    return res

def task_label(task):
    exp = task["expected_outcome"]
    expected_bound = task["hidden_expected"]["expected_bound"]
    def label(res):
        if exp == "unknown":
            if res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE):
                return "correct_unknown", False
            return "false_accept", True
        if res.status == ResolutionStatus.EXECUTABLE:
            if res.bound_action == expected_bound:
                return "correct", False
            return "false_accept", True
        return "unknown", False  # abstained on a correct-expected task
    return label

def group_rewards(task, actions, confs):
    """GRPO reward = correct - 0.75*false_accept + 0.25*calibration_bonus per frozen spec."""
    out = []
    for (cand_idx, rewrite, adopt_mask), conf in zip(actions, confs):
        res = gated_learned_resolution(task, cand_idx, rewrite, adopt_mask, float(conf))
        kind, fa = task_label(task)(res)
        correct = 1.0 if kind == "correct" else 0.0
        fa_v = 1.0 if fa else 0.0
        calib = 1.0 - abs(conf - correct)
        r = correct - 0.75 * fa_v + 0.25 * calib
        out.append(r)
    return np.array(out, dtype=np.float32)

def train_learned_seed(seed, train_tasks, epochs=120, group=8, lr=5e-4, weight_entropy=0.005, weight_calib=0.1):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    model = GRPOAdapter()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    X = [torch.from_numpy(build_feature_vector(t["intent"], t["derived_context"], filtered_candidates(t), t["params"])).unsqueeze(0)
         for t in train_tasks]
    SF = [slot_features_tensor(t) for t in train_tasks]
    n_cands = [len(filtered_candidates(t)) for t in train_tasks]
    t0 = time.time()
    history = []
    for ep in range(epochs):
        ep_rew = []
        for xi, sft, t, nc in zip(X, SF, train_tasks, n_cands):
            sc = sft["n"]
            probs = model(xi, sft["feats"])
            tau = model.tau()
            cl_masked = mask_cand_logits(probs["cand_logits"], nc)
            p_cand = torch.softmax(cl_masked / tau, dim=-1)
            p_rew = torch.sigmoid(probs["rewrite_logit"])
            p_adopt = torch.sigmoid(probs["adopt_logits"])
            # sample group actions
            cand_idx = torch.multinomial(p_cand.expand(group, -1), 1).squeeze(-1).tolist()
            rew = torch.bernoulli(p_rew.expand(group, 1)).squeeze(-1).tolist()
            adopt_rows = torch.bernoulli(p_adopt.expand(group, -1)).tolist()
            adopt_masked = [[int(a) if s < sc else 0 for s, a in enumerate(row)] for row in adopt_rows]
            actions = list(zip(cand_idx, [int(r) for r in rew], [tuple(a) for a in adopt_masked]))
            # model-derived softmax confidence per member (depends on the rewrite decision)
            confs = [action_confidence(model, cl_masked, probs["rewrite_logit"], nc, rw, tau)
                     for rw in rew]
            confs = [c if c is not None else structural_abstain_confidence(t["intent"]) for c in confs]
            rewards = group_rewards(t, actions, confs)
            R = torch.from_numpy(rewards)
            adv = (R - R.mean()) / (R.std() + 1e-8)
            # per-member log-prob of the sampled action (vectorized over group)
            lps = torch.zeros(group)
            p_rew0 = p_rew[0, 0].clamp(min=1e-9, max=1 - 1e-9)
            for a, (ci, rw, ad) in enumerate(actions):
                lp = torch.log(p_cand[0, ci].clamp(min=1e-9))
                lp = lp + (torch.log(p_rew0) if rw == 1 else torch.log(1 - p_rew0))
                for s in range(sc):
                    pa = p_adopt[0, s].clamp(min=1e-9, max=1 - 1e-9)
                    lp = lp + (torch.log(pa) if ad[s] == 1 else torch.log(1 - pa))
                lps[a] = lp
            # entropy bonus
            H = torch.distributions.Categorical(probs=p_cand).entropy().mean()
            h_rew = -(p_rew * torch.log(p_rew.clamp(min=1e-9)) + (1 - p_rew) * torch.log((1 - p_rew).clamp(min=1e-9))).mean()
            h_adopt = 0.0
            for s in range(sc):
                pa = p_adopt[0, s].clamp(min=1e-9, max=1 - 1e-9)
                h_adopt += -(pa * torch.log(pa) + (1 - pa) * torch.log(1 - pa)).item()
            H = H + h_rew + h_adopt
            # calibration objective: conf of chosen actions vs empirical group correctness
            target = torch.tensor([float(rewards.mean() > 0.0)], dtype=torch.float32)
            calib_loss = torch.nn.functional.mse_loss(
                torch.tensor(confs, dtype=torch.float32), target.expand(group))
            loss = -(adv.detach() * lps).mean() - weight_entropy * H + weight_calib * calib_loss
            opt.zero_grad()
            loss.backward()
            opt.step()
            ep_rew.append(float(rewards.mean()))
        history.append(float(np.mean(ep_rew)))
    wall = time.time() - t0
    return model, history, wall

def evaluate_learned_model(model, tasks_all):
    """Deterministic argmax evaluation (no sampling) over all frozen tasks."""
    rows = []
    with torch.no_grad():
        for t in tasks_all:
            cands = filtered_candidates(t)
            x = torch.from_numpy(build_feature_vector(t["intent"], t["derived_context"], cands, t["params"])).unsqueeze(0)
            sft = slot_features_tensor(t)
            probs = model(x, sft["feats"])
            tau = model.tau()
            cl_masked = mask_cand_logits(probs["cand_logits"], len(cands))
            cand_idx = int(torch.argmax(cl_masked, dim=-1)[0])
            rewrite = 1 if float(torch.sigmoid(probs["rewrite_logit"])[0, 0]) > 0.5 else 0
            adopt_mask = [1 if float(torch.sigmoid(probs["adopt_logits"])[0, s]) > 0.5 and s < sft["n"] else 0
                          for s in range(MAX_ADOPT)]
            conf = action_confidence(model, cl_masked, probs["rewrite_logit"], len(cands), rewrite, tau)
            if conf is None:
                conf = structural_abstain_confidence(t["intent"])
            res = gated_learned_resolution(t, cand_idx, rewrite, adopt_mask, conf)
            rows.append({"resolution": res, "conf": conf, "cand_idx": cand_idx, "rewrite": rewrite,
                         "adopt_mask": adopt_mask})
    return rows

LEARNED_SEEDS = [42, 43, 44]
print("LEARNED seeds:", LEARNED_SEEDS)
learned_models = {}
learned_history = {}
learned_wall = {}
learned_evals = {}   # seed -> list of rows aligned with `tasks`
for seed in LEARNED_SEEDS:
    model, hist, wall = train_learned_seed(seed, train_split)
    learned_models[seed] = model
    learned_history[seed] = hist
    learned_wall[seed] = wall
    learned_evals[seed] = evaluate_learned_model(model, tasks)
    print(f"seed {seed}: train_wall {wall:.1f}s final_mean_reward {hist[-1]:.3f}")

# per-seed pooled correct on alias-OOD 40 (for stability/CV)
def seed_rows_to_records(seed):
    recs = []
    for t, ev in zip(tasks, learned_evals[seed]):
        res = ev["resolution"]
        exp = t["expected_outcome"]
        expected_bound = t["hidden_expected"]["expected_bound"]
        if exp == "unknown":
            is_unknown = res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE)
            is_correct = False
            is_false_accept = not is_unknown
        else:
            if res.status == ResolutionStatus.EXECUTABLE:
                is_correct = (res.bound_action == expected_bound)
                is_false_accept = not is_correct
                is_unknown = False
            elif res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE):
                is_unknown = True
                is_correct = False
                is_false_accept = False
            else:
                is_false_accept = True
                is_correct = False
                is_unknown = False
        recs.append({
            "task_id": t["task_id"], "stratum": t["stratum"], "family": t["family"],
            "method": f"RECONSTRUCTION-LEARNED",
            "intent": t["intent"], "expected_outcome": exp,
            "expected_bound": expected_bound,
            "observed_status": res.status.value, "observed_bound": res.bound_action,
            "observed_confidence": float(res.confidence == conf if False else res.confidence),
            "is_correct": is_correct, "is_false_accept": is_false_accept, "is_unknown": is_unknown,
            "reason": res.reason, "registry_size": len(t["registry"]),
            "is_heldout": t["is_heldout"], "method_available": True,
            "learned_seed": seed,
        })
    return recs

seed_records = {s: seed_rows_to_records(s) for s in LEARNED_SEEDS}
def seed_pooled_correct(recs):
    sub = [r for r in recs if r["stratum"] == "alias-OOD"]
    return sum(1 for r in sub if r["is_correct"]) / len(sub), len(sub)
per_seed_pooled = {s: seed_pooled_correct(seed_records[s])[0] for s in LEARNED_SEEDS}
median_seed = sorted(LEARNED_SEEDS, key=lambda s: (per_seed_pooled[s], -seed_pooled_correct(seed_records[s])[0]))[1] if False else \
    int(sorted(LEARNED_SEEDS, key=lambda s: per_seed_pooled[s])[len(LEARNED_SEEDS) // 2])
print("per_seed_pooled_correct:", per_seed_pooled, "median_seed:", median_seed)

# ================================================================ BASELINES
TMP_REG = Path(f"/tmp/spider_test_registry_{EXP_ID}.jsonl")

def evaluate_exact_match(task):
    reg = MechanismRegistry(TMP_REG)
    reg.replace(task["registry"])
    kernel = SpiderKernel(reg, min_confidence=0.8)
    return kernel.resolve(task["intent"], task["derived_context"], task["params"])

def evaluate_verbatim(task):
    candidates = [m for m in task["registry"] if m.intent == task["intent"]]
    eligible = []
    for m in candidates:
        required = set(m.parameter_slots) | _template_slots(m.action_template)
        if all(slot in task["params"] for slot in required):
            eligible.append(m)
    if not eligible:
        return Resolution(ResolutionStatus.UNKNOWN, None, "no eligible", confidence=0.0)
    best = eligible[0]
    bound = _bind(best.action_template, task["params"])
    return Resolution(ResolutionStatus.EXECUTABLE, best.mechanism_id, "verbatim replay",
                      bound_action=bound, confidence=best.confidence)

def template_text(template):
    return json.dumps(template, sort_keys=True)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_tfidf(task, threshold=0.2):
    if not task["registry"]:
        return Resolution(ResolutionStatus.UNKNOWN, None, "empty registry", confidence=0.0)
    docs = [f"{m.intent} {template_text(m.action_template)}" for m in task["registry"]]
    query = task["intent"]
    vec = TfidfVectorizer()
    tfidf = vec.fit_transform(docs)
    q_vec = vec.transform([query])
    sims = cosine_similarity(q_vec, tfidf).flatten()
    best_idx = int(np.argmax(sims))
    best_score = float(sims[best_idx])
    best = task["registry"][best_idx]
    if best_score < threshold:
        return Resolution(ResolutionStatus.UNKNOWN, None, "tfidf below threshold", confidence=best_score)
    required = set(best.parameter_slots) | _template_slots(best.action_template)
    if any(slot not in task["params"] for slot in required):
        return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots", confidence=best_score)
    bound = _bind(best.action_template, task["params"])
    return Resolution(ResolutionStatus.EXECUTABLE, best.mechanism_id, "tfidf", bound_action=bound,
                      confidence=best_score)

# ---- B-RAG-EMBED (real offline sentence-transformer retriever, deterministic CPU)
_embed_model = None
_embed_cache = {}
def get_embed_model():
    global _embed_model
    if _embed_model is None:
        from sentence_transformers import SentenceTransformer
        _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        _embed_model.eval()
    return _embed_model

EMBED_AVAILABLE = True
EMBED_MSG = "sentence-transformers all-MiniLM-L6-v2"
try:
    get_embed_model()
except Exception as e:
    EMBED_AVAILABLE = False
    EMBED_MSG = f"sentence-transformers unavailable: {type(e).__name__}: {e}"

def embed_encode(texts):
    global _embed_cache
    needed = []
    for t in texts:
        if t not in _embed_cache:
            needed.append(t)
    if needed:
        import torch as _t
        with _t.no_grad():
            embs = get_embed_model().encode(needed, normalize_embeddings=True, convert_to_numpy=True)
        for t, e in zip(needed, embs):
            _embed_cache[t] = e
    return np.stack([_embed_cache[t] for t in texts])

def evaluate_embed(task, threshold=0.60):
    if not task["registry"]:
        return Resolution(ResolutionStatus.UNKNOWN, None, "empty registry", confidence=0.0)
    docs = [f"{m.intent} {template_text(m.action_template)}" for m in task["registry"]]
    query = task["intent"]
    doc_e = embed_encode(docs)
    q_e = embed_encode([query])[0]
    sims = doc_e @ q_e
    best_idx = int(np.argmax(sims))
    best_score = float(sims[best_idx])
    best = task["registry"][best_idx]
    if best_score < threshold:
        return Resolution(ResolutionStatus.UNKNOWN, None, "embed below threshold", confidence=best_score)
    required = set(best.parameter_slots) | _template_slots(best.action_template)
    if any(slot not in task["params"] for slot in required):
        return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots", confidence=best_score)
    bound = _bind(best.action_template, task["params"])
    return Resolution(ResolutionStatus.EXECUTABLE, best.mechanism_id, "embed", bound_action=bound,
                      confidence=best_score)

def evaluate_random(task):
    eligible = []
    for m in task["registry"]:
        if m.intent != task["intent"]:
            continue
        required = set(m.parameter_slots) | _template_slots(m.action_template)
        if all(slot in task["params"] for slot in required):
            eligible.append(m)
    if not eligible:
        return Resolution(ResolutionStatus.UNKNOWN, None, "no eligible", confidence=0.0)
    chosen = random.choice(eligible)
    bound = _bind(chosen.action_template, task["params"])
    return Resolution(ResolutionStatus.EXECUTABLE, chosen.mechanism_id, "random",
                      bound_action=bound, confidence=0.5)

def evaluate_reconstruction(task, use_channels=("url", "headers", "body")):
    candidates = [m for m in task["registry"] if m.intent == task["intent"]]
    filtered = []
    for m in candidates:
        required = set(m.parameter_slots) | _template_slots(m.action_template)
        if all(slot in task["params"] for slot in required):
            filtered.append(m)
    return reconstruct_resolve(task["intent"], task["derived_context"], filtered, task["params"],
                               use_channels=use_channels)

# ================================================================ AVAILABILITY PROBES (live substrate)
def probe_browsergym():
    out = {}
    try:
        import browsergym
        out["browsergym_import"] = ("ok", getattr(browsergym, "__version__", "?"))
    except Exception as e:
        out["browsergym_import"] = (False, f"{type(e).__name__}: {e}")
    try:
        import browsergym.webshop
        out["webshop_module"] = ("ok", "import ok")
    except Exception as e:
        out["webshop_module"] = (False, f"{type(e).__name__}: {e}")
    try:
        import browsergym.alfworld
        out["alfworld_module"] = ("ok", "import ok")
    except Exception as e:
        out["alfworld_module"] = (False, f"{type(e).__name__}: {e}")
    try:
        import gymnasium as gym
        specs = [s for s in gym.envs.registry.keys() if str(s).startswith("browsergym")]
        out["browsergym_envs_registered"] = specs
    except Exception as e:
        out["browsergym_envs_registered"] = f"{type(e).__name__}: {e}"
    pw = glob.glob(os.path.expanduser("~/.cache/ms-playwright/*"))
    out["playwright_browser_dirs"] = pw
    return out

BG = probe_browsergym()
LIVE_ENV_NOTES = [
    "browsergym.webshop / browsergym.alfworld modules absent (ModuleNotFoundError) in installed browsergym 0.14.3 base.",
    "pip download browsergym-webshop / browsergym-alfworld -> 'ERROR: Could not find a version that satisfies the requirement ... (from versions: none)' / 'ERROR: No matching distribution found for ...' (no PyPI distributions).",
    "gymnasium registry contains no 'browsergym/*' environments (base browsergym registers none).",
    "playwright 1.44.0 installed but ~/.cache/ms-playwright has no browser binaries; CDP AX-tree launch impossible.",
    "ALFWorld additionally requires Java/textworld server + docker fixture; absent.",
    "=> PC-BROWSERGYM-HEALTH could not be exercised (0 attempted). Frozen spec: live stratum exploratory, claim bounds to synthetic pooled+mixed with disclosure; NOT MEASUREMENT_INVALID.",
]

# ================================================================ EVALUATION (7 methods x 70 tasks, paired)
methods = [
    "B-EXACT-MATCH", "B-VERBATIM-REPLAY", "B-RAG-TFIDF", "B-RAG-EMBED",
    "B-RANDOM", "RECONSTRUCTION-RULE", "RECONSTRUCTION-LEARNED",
]
raw_evidence = []
harness_errors = []

# economics counters
CNT = {m: {"tasks": 0, "ok": 0, "latency_s": 0.0, "scoring_calls": 0,
           "rewrite_ops": 0, "bind_ops": 0, "retrieval_candidates": 0,
           "embed_encodings": 0, "policy_forwards": 0} for m in methods}

for task in tasks:
    for mname in methods:
        t_start = time.perf_counter()
        res = None
        avail = True
        try:
            if mname == "B-EXACT-MATCH":
                res = evaluate_exact_match(task)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            elif mname == "B-VERBATIM-REPLAY":
                res = evaluate_verbatim(task)
                CNT[mname]["retrieval_candidates"] += len([m for m in task["registry"] if m.intent == task["intent"]])
            elif mname == "B-RAG-TFIDF":
                res = evaluate_tfidf(task)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            elif mname == "B-RAG-EMBED":
                if EMBED_AVAILABLE:
                    res = evaluate_embed(task)
                    CNT[mname]["retrieval_candidates"] += len(task["registry"])
                    if task["registry"]:
                        CNT[mname]["embed_encodings"] += len(task["registry"]) + 1
                else:
                    avail = False
            elif mname == "B-RANDOM":
                res = evaluate_random(task)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            elif mname == "RECONSTRUCTION-RULE":
                res = evaluate_reconstruction(task)
                cands = [m for m in task["registry"] if m.intent == task["intent"]]
                CNT[mname]["retrieval_candidates"] += len(cands)
                CNT[mname]["scoring_calls"] += len(cands)
                adv = choose_adoptions(task["derived_context"],
                                       [m for m in cands if all(s in task["params"] for s in (set(m.parameter_slots) | _template_slots(m.action_template)))],
                                       task["params"])
                CNT[mname]["rewrite_ops"] += len(adv)
            elif mname == "RECONSTRUCTION-LEARNED":
                ev = learned_evals[median_seed][tasks.index(task)]
                res = ev["resolution"]
                cands = filtered_candidates(task)
                CNT[mname]["retrieval_candidates"] += len(cands)
                CNT[mname]["scoring_calls"] += len(cands)
                slots = adoption_slots(task)
                CNT[mname]["rewrite_ops"] += sum(1 for i, s in enumerate(slots) if ev["adopt_mask"][i] == 1 and ev["rewrite"])
                CNT[mname]["policy_forwards"] += 1
            else:
                res = None
                avail = False
        except Exception as e:
            harness_errors.append({"task_id": task["task_id"], "method": mname, "error": str(e)})
            res = None
            avail = False
        latency = time.perf_counter() - t_start
        CNT[mname]["tasks"] += 1
        CNT[mname]["latency_s"] += latency
        if res is not None and res.status == ResolutionStatus.EXECUTABLE:
            CNT[mname]["bind_ops"] += 1
        expected_outcome = task["expected_outcome"]
        expected_bound = task["hidden_expected"]["expected_bound"]
        is_correct = None
        is_false_accept = None
        is_unknown = None
        reason = None
        observed_status = None
        observed_bound = None
        observed_confidence = None
        if res is not None:
            observed_status = res.status.value
            observed_bound = res.bound_action
            observed_confidence = float(res.confidence)
            reason = res.reason
            if expected_outcome == "unknown":
                if res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE):
                    is_unknown = True
                    is_correct = False
                    is_false_accept = False
                else:
                    is_false_accept = True
                    is_correct = False
                    is_unknown = False
            else:
                if res.status == ResolutionStatus.EXECUTABLE:
                    if res.bound_action == expected_bound:
                        is_correct = True
                        is_false_accept = False
                        is_unknown = False
                    else:
                        is_false_accept = True
                        is_correct = False
                        is_unknown = False
                elif res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE):
                    is_unknown = True
                    is_correct = False
                    is_false_accept = False
                else:
                    is_false_accept = True
                    is_correct = False
                    is_unknown = False
        if is_correct:
            CNT[mname]["ok"] += 1
        raw_evidence.append({
            "task_id": task["task_id"], "stratum": task["stratum"], "family": task["family"],
            "method": mname, "intent": task["intent"], "expected_outcome": expected_outcome,
            "expected_bound": expected_bound, "observed_status": observed_status,
            "observed_bound": observed_bound, "observed_confidence": observed_confidence,
            "is_correct": is_correct, "is_false_accept": is_false_accept,
            "is_unknown": is_unknown, "reason": reason,
            "registry_size": len(task["registry"]), "is_heldout": task["is_heldout"],
            "method_available": avail, "latency_s": latency,
        })

# ---- reduced-state diagnostics (exploratory, non-gated): channel isolation (RULE)
for task in tasks:
    if task["stratum"] != "alias-OOD":
        continue
    for variant, channels in [("RULE-URL-ONLY", ("url",)),
                              ("RULE-BODY-ONLY", ("url", "body")),
                              ("RULE-HEADERS-ONLY", ("url", "headers"))]:
        res = evaluate_reconstruction(task, use_channels=channels)
        expected_bound = task["hidden_expected"]["expected_bound"]
        if res.status == ResolutionStatus.EXECUTABLE and res.bound_action == expected_bound:
            is_correct, is_false_accept, is_unknown = True, False, False
        elif res.status == ResolutionStatus.EXECUTABLE:
            is_correct, is_false_accept, is_unknown = False, True, False
        else:
            is_correct, is_false_accept, is_unknown = False, False, True
        raw_evidence.append({
            "task_id": task["task_id"], "stratum": "alias-OOD-diagnostic",
            "family": task["family"], "method": variant, "intent": task["intent"],
            "expected_outcome": "correct", "expected_bound": expected_bound,
            "observed_status": res.status.value, "observed_bound": res.bound_action,
            "observed_confidence": float(res.confidence), "is_correct": is_correct,
            "is_false_accept": is_false_accept, "is_unknown": is_unknown,
            "reason": res.reason, "registry_size": len(task["registry"]),
            "is_heldout": task["is_heldout"], "method_available": True,
        })

# ================================================================ METRICS
def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    lower = (center - margin) / denom
    upper = (center + margin) / denom
    return (max(0.0, lower), min(1.0, upper))

def rows(method, stratum):
    return [r for r in raw_evidence if r["method"] == method and r["stratum"] == stratum
            and r["method_available"]]

def compute_rates(method, stratum):
    subset = rows(method, stratum)
    n = len(subset)
    correct = sum(1 for r in subset if r["is_correct"])
    false_accept = sum(1 for r in subset if r["is_false_accept"])
    unknown = sum(1 for r in subset if r["is_unknown"])
    return {
        "n": n, "correct": correct, "false_accept": false_accept, "unknown": unknown,
        "correct_rate": correct / n if n else None,
        "false_accept_rate": false_accept / n if n else None,
        "unknown_rate": unknown / n if n else None,
        "wilson_correct": [wilson_ci(correct, n)[0], wilson_ci(correct, n)[1]],
        "wilson_false": [wilson_ci(false_accept, n)[0], wilson_ci(false_accept, n)[1]],
    }

def unknown_precision(method, stratum):
    subset = rows(method, stratum)
    tp = sum(1 for r in subset if r["is_unknown"])
    fp = sum(1 for r in subset if r["is_false_accept"])
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0

def compute_ece(method, stratum=None, evidence=None):
    src = raw_evidence if evidence is None else evidence
    subset = [r for r in src if r["method"] == method and r["method_available"]
              and (stratum is None or r["stratum"] == stratum)]
    if not subset:
        return None, []
    bins = np.linspace(0, 1, 6)
    ece = 0.0
    total = len(subset)
    bin_stats = []
    for b in range(5):
        lo, hi = bins[b], bins[b + 1]
        if b == 4:
            bin_recs = [r for r in subset if lo <= r["observed_confidence"] <= hi]
        else:
            bin_recs = [r for r in subset if lo <= r["observed_confidence"] < hi]
        if not bin_recs:
            bin_stats.append({"bin": b, "count": 0, "acc": 0.0, "avg_conf": 0.0,
                              "edges": [float(lo), float(hi)]})
            continue
        acc = sum(1 for r in bin_recs if r["is_correct"]) / len(bin_recs)
        avg_conf = float(np.mean([r["observed_confidence"] for r in bin_recs]))
        ece += len(bin_recs) / total * abs(acc - avg_conf)
        bin_stats.append({"bin": b, "count": len(bin_recs), "acc": float(acc),
                          "avg_conf": avg_conf, "edges": [float(lo), float(hi)]})
    return float(ece), bin_stats

def bootstrap_ece_ci(method, n_resamples=2000):
    tids = sorted(set(r["task_id"] for r in raw_evidence if r["method"] == method
                      and r["method_available"]))
    eces = []
    for _ in range(n_resamples):
        sampled_ids = rng.choice(tids, size=len(tids), replace=True)
        sampled = []
        for tid in sampled_ids:
            sampled.extend([r for r in raw_evidence if r["method"] == method
                            and r["method_available"] and r["task_id"] == tid])
        total = len(sampled)
        if total == 0:
            eces.append(0.0)
            continue
        bins = np.linspace(0, 1, 6)
        ece = 0.0
        for b in range(5):
            lo, hi = bins[b], bins[b + 1]
            bin_recs = [r for r in sampled if (lo <= r["observed_confidence"] <= hi if b == 4
                                               else lo <= r["observed_confidence"] < hi)]
            if not bin_recs:
                continue
            acc = sum(1 for r in bin_recs if r["is_correct"]) / len(bin_recs)
            avg_conf = float(np.mean([r["observed_confidence"] for r in bin_recs]))
            ece += len(bin_recs) / total * abs(acc - avg_conf)
        eces.append(ece)
    lo, hi = np.percentile(eces, [2.5, 97.5])
    return float(np.mean(eces)), float(lo), float(hi)

from scipy.stats import binom as scipy_binom
from scipy.stats import chi2 as chi2dist

def binomial_p(k, n, p0=0.10):
    if k <= 0:
        return 1.0
    return float(scipy_binom.sf(k - 1, n, p0))

def mcnemar_p(a_list, b_list):
    b = c = 0
    for a, bb in zip(a_list, b_list):
        if a and not bb:
            b += 1
        elif not a and bb:
            c += 1
    if b + c == 0:
        return {"b": b, "c": c, "chi2": 0.0, "p": 1.0}
    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
    p = 1 - chi2dist.cdf(chi2, 1)
    return {"b": b, "c": c, "chi2": float(chi2), "p": float(p)}

STRATA = ["alias-OOD", "exact-match", "no-applicable", "empty-registry"]
METHODS_METRIC = ["B-EXACT-MATCH", "B-VERBATIM-REPLAY", "B-RAG-TFIDF", "B-RAG-EMBED",
                  "B-RANDOM", "RECONSTRUCTION-RULE", "RECONSTRUCTION-LEARNED"]

metrics = {}
for m in METHODS_METRIC:
    for s in STRATA:
        metrics[f"{m}::{s}"] = compute_rates(m, s)

rec_alias = metrics["RECONSTRUCTION-RULE::alias-OOD"]
exact_rows_alias = metrics["B-EXACT-MATCH::alias-OOD"]
verbatim_alias = metrics["B-VERBATIM-REPLAY::alias-OOD"]
tfidf_alias = metrics["B-RAG-TFIDF::alias-OOD"]
embed_alias = metrics["B-RAG-EMBED::alias-OOD"]
random_alias = metrics["B-RANDOM::alias-OOD"]
learned_alias = metrics["RECONSTRUCTION-LEARNED::alias-OOD"]
pc_exact_recon = metrics["RECONSTRUCTION-RULE::exact-match"]
pc_exact_baseline = metrics["B-EXACT-MATCH::exact-match"]
pc_exact_learned = metrics["RECONSTRUCTION-LEARNED::exact-match"]

alias_ids = sorted(set(r["task_id"] for r in raw_evidence
                       if r["stratum"] == "alias-OOD" and r["method_available"]))
def paired_lists(method_a, method_b, field):
    a_list, b_list = [], []
    for tid in alias_ids:
        ra = [r for r in raw_evidence if r["task_id"] == tid and r["method"] == method_a][0]
        rb = [r for r in raw_evidence if r["task_id"] == tid and r["method"] == method_b][0]
        a_list.append(ra[field])
        b_list.append(rb[field])
    return a_list, b_list

rec_correct_list, exact_correct_list = paired_lists("RECONSTRUCTION-RULE", "B-EXACT-MATCH", "is_correct")
rec_fa_list, verbatim_fa_list = paired_lists("RECONSTRUCTION-RULE", "B-VERBATIM-REPLAY", "is_false_accept")
learn_correct_list, _ = paired_lists("RECONSTRUCTION-LEARNED", "B-EXACT-MATCH", "is_correct")
learn_fa_list, _ = paired_lists("RECONSTRUCTION-LEARNED", "B-VERBATIM-REPLAY", "is_false_accept")

orthogonal_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] in [0, 1, 2]]
mixed_ids_all = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] == 3]
def subset_rate(method, ids, field="is_correct"):
    n = len(ids)
    k = sum(1 for tid in ids for r in raw_evidence if r["task_id"] == tid and r["method"] == method and r[field])
    return k, n, (k / n if n else None)

orth_cor, orth_n, orth_rate = subset_rate("RECONSTRUCTION-RULE", orthogonal_ids)
mix_cor, mix_n, mix_rate = subset_rate("RECONSTRUCTION-RULE", mixed_ids_all)
mix_fa, _, mix_fa_rate = subset_rate("RECONSTRUCTION-RULE", mixed_ids_all, "is_false_accept")
learn_orth_cor, _, learn_orth_rate = subset_rate("RECONSTRUCTION-LEARNED", orthogonal_ids)
learn_mix_cor, _, learn_mix_rate = subset_rate("RECONSTRUCTION-LEARNED", mixed_ids_all)
learn_mix_fa, _, learn_mix_fa_rate = subset_rate("RECONSTRUCTION-LEARNED", mixed_ids_all, "is_false_accept")

p_binom = binomial_p(rec_alias["correct"], rec_alias["n"], 0.10)
p_binom_orth = binomial_p(orth_cor, orth_n, 0.10)
mcnemar_rec_vs_exact = mcnemar_p(rec_correct_list, exact_correct_list)
mcnemar_fa = mcnemar_p(rec_fa_list, verbatim_fa_list)
mcnemar_learn_vs_exact = mcnemar_p(learn_correct_list, exact_correct_list)
mcnemar_learn_fa = mcnemar_p(learn_fa_list, verbatim_fa_list)
p_binom_learn = binomial_p(learned_alias["correct"], learned_alias["n"], 0.10)
p_binom_learn_orth = binomial_p(learn_orth_cor, orth_n, 0.10)

ece_recon, bins_recon = compute_ece("RECONSTRUCTION-RULE")
ece_learn, bins_learn = compute_ece("RECONSTRUCTION-LEARNED")
ece_learn_alias, _ = compute_ece("RECONSTRUCTION-LEARNED", "alias-OOD")
ece_learn_noapp, _ = compute_ece("RECONSTRUCTION-LEARNED", "no-applicable")
boot_mean, boot_lo, boot_hi = bootstrap_ece_ci("RECONSTRUCTION-RULE", 2000)

conf_recon = [r["observed_confidence"] for r in raw_evidence
              if r["method"] == "RECONSTRUCTION-RULE" and r["method_available"]]
conf_std = float(np.std(conf_recon)) if conf_recon else None
conf_learn = [r["observed_confidence"] for r in raw_evidence
              if r["method"] == "RECONSTRUCTION-LEARNED" and r["method_available"]]
conf_learn_std = float(np.std(conf_learn)) if conf_learn else None

# per-seed learned stats
per_seed_stats = {}
for s in LEARNED_SEEDS:
    recs = seed_records[s]
    pooled_corr = sum(1 for r in recs if r["stratum"] == "alias-OOD" and r["is_correct"])
    ece_s, _ = compute_ece(f"RECONSTRUCTION-LEARNED", None, [dict(r, method="RECONSTRUCTION-LEARNED") for r in recs])
    confs_s = [r["observed_confidence"] for r in recs]
    orth_s = sum(1 for r in recs if r["task_id"] in orthogonal_ids and r["is_correct"])
    mix_s = sum(1 for r in recs if r["task_id"] in mixed_ids_all and r["is_correct"])
    per_seed_stats[s] = {
        "pooled_correct": pooled_corr,
        "pooled_correct_rate": pooled_corr / 40,
        "orthogonal_correct": orth_s,
        "orthogonal_rate": orth_s / 30,
        "mixed_correct": mix_s,
        "mixed_rate": mix_s / 10,
        "ece_overall": ece_s,
        "conf_std_overall": float(np.std(confs_s)) if confs_s else None,
        "train_wall_s": learned_wall[s],
        "history": learned_history[s],
    }
per_seed_pooled_rates = [per_seed_stats[s]["pooled_correct_rate"] for s in LEARNED_SEEDS]
learned_cv = (float(np.std(per_seed_pooled_rates)) / float(np.mean(per_seed_pooled_rates))
              if np.mean(per_seed_pooled_rates) > 0 else None)
learned_pooled_median = float(np.median(per_seed_pooled_rates))
learned_conf_std_min = min(per_seed_stats[s]["conf_std_overall"] for s in LEARNED_SEEDS)

# --------- controls
pc_pass = (pc_exact_baseline["correct_rate"] >= 0.90 and pc_exact_recon["correct_rate"] >= 0.90
           and pc_exact_baseline["false_accept_rate"] <= 0.10
           and pc_exact_recon["false_accept_rate"] <= 0.10)
pc_learned_pass = (pc_exact_learned["correct_rate"] is not None and pc_exact_learned["correct_rate"] >= 0.85
                   and pc_exact_learned["false_accept_rate"] <= 0.15)
nc_prec_recon = unknown_precision("RECONSTRUCTION-RULE", "no-applicable")
nc_fa_recon = metrics["RECONSTRUCTION-RULE::no-applicable"]["false_accept_rate"]
nc_prec_learn = unknown_precision("RECONSTRUCTION-LEARNED", "no-applicable")
nc_fa_learn = metrics["RECONSTRUCTION-LEARNED::no-applicable"]["false_accept_rate"]
nc_prec_all = {m: (unknown_precision(m, "no-applicable") if rows(m, "no-applicable") else None)
               for m in METHODS_METRIC}
nc_fa_all = {m: metrics[f"{m}::no-applicable"]["false_accept_rate"] for m in METHODS_METRIC}
nc_empty_recon = metrics["RECONSTRUCTION-RULE::empty-registry"]
nc_empty_ok = nc_empty_recon["unknown_rate"] == 1.0
nc_empty_all = all(metrics[f"{m}::empty-registry"]["unknown_rate"] == 1.0 for m in METHODS_METRIC
                   if metrics[f"{m}::empty-registry"]["n"] > 0)
nc_pass_recon = nc_prec_recon >= 0.90 and nc_fa_recon <= 0.10
nc_pass_learn = nc_prec_learn >= 0.90 and nc_fa_learn <= 0.10
nc_pass_all = True
for m in METHODS_METRIC:
    p = nc_prec_all[m]
    f = nc_fa_all[m]
    if p is None or f is None:
        continue
    if p < 0.90 or f > 0.10:
        nc_pass_all = False

# --------- S gates (RULE)
s1_correct = rec_alias["correct_rate"] >= 0.50
s1_binom = p_binom < 0.05
s1_mcnemar = mcnemar_rec_vs_exact["p"] < 0.05
s1_orth = orth_rate >= 0.50 if orth_rate is not None else False
s1_mixed = mix_rate >= 0.40 if mix_rate is not None else False
s1_pass = s1_correct and s1_binom and s1_mcnemar and s1_orth and s1_mixed
s2_fa = rec_alias["false_accept_rate"] <= 0.15
s2_diff = (verbatim_alias["false_accept_rate"] - rec_alias["false_accept_rate"]) >= 0.15
s2_mcnemar = mcnemar_fa["p"] < 0.05
s2_pass = s2_fa and s2_diff and s2_mcnemar
s3_pass = pc_exact_recon["correct_rate"] >= 0.90
s4_prec = nc_prec_recon >= 0.85
s4_ece = (ece_recon is not None and ece_recon <= 0.15)
s4_pass = s4_prec and s4_ece
best_rag = max(tfidf_alias["correct_rate"] or 0.0, embed_alias["correct_rate"] or 0.0)
s5_not_dominated = (rec_alias["correct_rate"] + 0.10) >= best_rag
s5_pass = s5_not_dominated
rule_s1_s7 = s1_pass and s2_pass and s3_pass and s4_pass and s5_pass

# --------- G0 (learned gate, median seed) + learned S gates
def learned_row_for(tid, method="RECONSTRUCTION-LEARNED"):
    return [r for r in raw_evidence if r["task_id"] == tid and r["method"] == method][0]

g0_gap_correct = (rec_alias["correct_rate"] - learned_alias["correct_rate"]) if learned_alias["correct_rate"] is not None else None
g0_gap_ece = abs(ece_recon - ece_learn) if (ece_recon is not None and ece_learn is not None) else None
g0_cv = learned_cv
g0_conf_std = learned_conf_std_min
g0_pooled_ge_50 = learned_alias["correct_rate"] is not None and learned_alias["correct_rate"] >= 0.50
g0_binom = p_binom_learn < 0.05
g0_mcnemar = mcnemar_learn_vs_exact["p"] < 0.05
g0_gap_ok = g0_gap_correct is not None and g0_gap_correct <= 0.10
g0_ece_ok = g0_gap_ece is not None and g0_gap_ece <= 0.05
g0_cv_ok = g0_cv is not None and g0_cv <= 0.5
g0_conf_ok = g0_conf_std is not None and g0_conf_std > 0.05
g0_orth_ok = learn_orth_rate is not None and learn_orth_rate >= 0.50
g0_mixed_ok = learn_mix_rate is not None and learn_mix_rate >= 0.40
g0_pass = (g0_gap_ok and g0_ece_ok and g0_cv_ok and g0_conf_ok and g0_pooled_ge_50
           and g0_binom and g0_mcnemar)
learned_s1 = g0_pooled_ge_50 and g0_binom and g0_mcnemar and g0_orth_ok and g0_mixed_ok
learned_s2 = (learned_alias["false_accept_rate"] is not None and learned_alias["false_accept_rate"] <= 0.15
              and (verbatim_alias["false_accept_rate"] - learned_alias["false_accept_rate"]) >= 0.15
              and mcnemar_learn_fa["p"] < 0.05)
learned_s3 = pc_learned_pass
learned_s4 = (nc_prec_learn >= 0.85 and ece_learn is not None and ece_learn <= 0.15)
learned_s5 = (learned_alias["correct_rate"] is not None and (learned_alias["correct_rate"] + 0.10) >= best_rag)
# falsifier-style absolute checks (frozen): >0.15 below RULE, ECE >0.10 above RULE or >0.25, orth <0.40
g0_falsified_by_gap = g0_gap_correct is not None and g0_gap_correct > 0.15
g0_falsified_by_ece = (g0_gap_ece is not None and g0_gap_ece > 0.10) or (ece_learn is not None and ece_learn > 0.25)
g0_falsified_by_cv = g0_cv is not None and g0_cv > 0.5
g0_falsified_by_conf = g0_conf_std is not None and g0_conf_std <= 0.05
g0_falsified_by_orth = learn_orth_rate is not None and learn_orth_rate < 0.40
g0_falsified_any = (g0_falsified_by_gap or g0_falsified_by_ece or g0_falsified_by_cv
                    or g0_falsified_by_conf or g0_falsified_by_orth)

controls_pass = pc_pass and nc_pass_recon and nc_empty_ok

if not controls_pass:
    status = "MEASUREMENT_INVALID"
    outcome = "NOT_APPLICABLE"
    outcome_reason = "controls (PC/NC) failed -> MEASUREMENT_INVALID per frozen decision rule"
elif rule_s1_s7 and g0_pass and learned_s1 and learned_s2 and learned_s3 and learned_s4 and learned_s5:
    status = "COMPLETE"
    outcome = "SUPPORTS"
    outcome_reason = "SEQUENCED SURVIVES_CURRENT_TEST: G0 learned gate + RULE S1-S7 + learned S1-S5 all pass; live exploratory bound to synthetic pooled+mixed"
elif rule_s1_s7 and not g0_pass:
    status = "COMPLETE"
    outcome = "MIXED"
    outcome_reason = ("RULE proxy synthetic ceiling SURVIVES (S1-S7 pass); RECONSTRUCTION-LEARNED gate "
                      "fails -> bounded falsification of learned GRPO adapter per frozen sequencing")
elif not rule_s1_s7:
    status = "COMPLETE"
    outcome = "FALSIFIES"
    outcome_reason = "pooled synthetic S1-S7 falsified per frozen decision rule"
else:
    status = "COMPLETE"
    outcome = "MIXED"
    outcome_reason = "mixed gates outcome (see components)"

live_attempted = 0
live_healthy = 0
pc_bg_health = False

metrics_out = to_native(metrics)

def per_family_rates(method):
    out = {}
    for fam in [0, 1, 2, 3]:
        for is_h, label in [(False, "standard"), (True, "heldout")]:
            if fam == 3:
                subset = []
            else:
                subset = [r for r in rows(method, "alias-OOD") if r["family"] == fam
                          and r["is_heldout"] == is_h]
            n = len(subset)
            corr = sum(1 for r in subset if r["is_correct"])
            fa = sum(1 for r in subset if r["is_false_accept"])
            out[f"fam{fam}_{label}"] = {"n": n,
                                        "correct_rate": corr / n if n else None,
                                        "fa_rate": fa / n if n else None}
        subset = [r for r in rows(method, "alias-OOD") if r["family"] == fam]
        n = len(subset)
        corr = sum(1 for r in subset if r["is_correct"])
        out[f"fam{fam}_overall"] = {"n": n, "correct_rate": corr / n if n else None}
        if fam == 3:
            fa = sum(1 for r in subset if r["is_false_accept"])
            out[f"fam{fam}_overall"]["fa_rate"] = fa / n if n else None
    subset = [r for r in rows(method, "alias-OOD") if r["is_heldout"]]
    n = len(subset)
    corr = sum(1 for r in subset if r["is_correct"])
    fa = sum(1 for r in subset if r["is_false_accept"])
    out["heldout_9"] = {"n": n, "correct_rate": corr / n if n else None,
                        "fa_rate": fa / n if n else None}
    mixed_subset = [r for r in rows(method, "alias-OOD") if r["family"] == 3]
    n = len(mixed_subset)
    corr = sum(1 for r in mixed_subset if r["is_correct"])
    fa = sum(1 for r in mixed_subset if r["is_false_accept"])
    out["mixed_10"] = {"n": n, "correct_rate": corr / n if n else None, "fa_rate": fa / n if n else None}
    orth_subset = [r for r in rows(method, "alias-OOD") if r["family"] in [0, 1, 2]]
    n = len(orth_subset)
    corr = sum(1 for r in orth_subset if r["is_correct"])
    out["orthogonal_30"] = {"n": n, "correct_rate": corr / n if n else None}
    return out

heldout_metrics_rule = per_family_rates("RECONSTRUCTION-RULE")
heldout_metrics_learn = per_family_rates("RECONSTRUCTION-LEARNED")

def diag_rates(method):
    subset = [r for r in raw_evidence if r["stratum"] == "alias-OOD-diagnostic"
              and r["method"] == method]
    n = len(subset)
    corr = sum(1 for r in subset if r["is_correct"])
    return {"n": n, "correct_rate": corr / n if n else None}

diag = {m: diag_rates(m) for m in ["RULE-URL-ONLY", "RULE-BODY-ONLY", "RULE-HEADERS-ONLY"]}
for m in ["RULE-URL-ONLY", "RULE-BODY-ONLY", "RULE-HEADERS-ONLY"]:
    d = {}
    for fam in [0, 1, 2, 3]:
        subset = [r for r in raw_evidence if r["stratum"] == "alias-OOD-diagnostic"
                  and r["method"] == m and r["family"] == fam]
        n = len(subset)
        corr = sum(1 for r in subset if r["is_correct"])
        d[f"fam{fam}"] = {"n": n, "correct_rate": corr / n if n else None}
    diag[m]["per_family"] = d

# economics summary
econ = {}
for m in METHODS_METRIC:
    c = CNT[m]
    alias_sub = [r for r in raw_evidence if r["method"] == m and r["stratum"] == "alias-OOD" and r["method_available"]]
    n_corr = sum(1 for r in alias_sub if r["is_correct"])
    econ[m] = {
        "total_latency_s": round(c["latency_s"], 6),
        "tasks": c["tasks"],
        "alias_ood_correct": n_corr,
        "mean_latency_per_task_s": round(c["latency_s"] / c["tasks"], 6) if c["tasks"] else None,
        "latency_per_successful_alias_task_s": round(c["latency_s"] / n_corr, 6) if n_corr else None,
        "scoring_calls": c["scoring_calls"],
        "rewrite_ops": c["rewrite_ops"],
        "bind_ops": c["bind_ops"],
        "retrieval_candidates": c["retrieval_candidates"],
        "embed_encodings": c["embed_encodings"],
        "policy_forwards": c["policy_forwards"],
    }

import platform as _platform
derived_metrics = {
    "alias_OOD": {
        "reconstruction_correct_resolution": rec_alias["correct_rate"],
        "reconstruction_correct_count": rec_alias["correct"],
        "reconstruction_false_accept": rec_alias["false_accept_rate"],
        "reconstruction_unknown": rec_alias["unknown_rate"],
        "reconstruction_n": rec_alias["n"],
        "wilson_correct_ci": rec_alias["wilson_correct"],
        "wilson_false_ci": rec_alias["wilson_false"],
        "exact_match_correct_rate": exact_rows_alias["correct_rate"],
        "verbatim_false_accept_rate": verbatim_alias["false_accept_rate"],
        "tfidf_correct_rate": tfidf_alias["correct_rate"],
        "embed_correct_rate": embed_alias["correct_rate"],
        "learned_correct_rate": learned_alias["correct_rate"],
        "learned_n": learned_alias["n"],
        "random_correct_rate": random_alias["correct_rate"],
        "binomial_p_vs_0.10": float(p_binom),
        "binomial_p_orthogonal_vs_0.10": float(p_binom_orth) if p_binom_orth is not None else None,
        "mcnemar_rec_vs_exact": mcnemar_rec_vs_exact,
        "mcnemar_fa_rec_vs_verbatim": mcnemar_fa,
        "mcnemar_learn_vs_exact": mcnemar_learn_vs_exact,
        "mcnemar_fa_learn_vs_verbatim": mcnemar_learn_fa,
        "binomial_p_learn_vs_0.10": float(p_binom_learn),
        "diff_verbatim_minus_recon_false_accept": float(verbatim_alias["false_accept_rate"]
                                                        - rec_alias["false_accept_rate"])
        if rec_alias["false_accept_rate"] is not None and verbatim_alias["false_accept_rate"] is not None
        else None,
        "per_family_and_heldout_rule": heldout_metrics_rule,
        "per_family_and_heldout_learned": heldout_metrics_learn,
        "channel_isolation_diagnostics": diag,
        "orthogonal_subset": {"n": orth_n, "correct": orth_cor, "correct_rate": orth_rate,
                              "wilson_ci": [wilson_ci(orth_cor, orth_n)[0], wilson_ci(orth_cor, orth_n)[1]]},
        "mixed_subset": {"n": mix_n, "correct": mix_cor, "correct_rate": mix_rate,
                         "false_accept_rate": mix_fa_rate,
                         "wilson_ci": [wilson_ci(mix_cor, mix_n)[0], wilson_ci(mix_cor, mix_n)[1]]},
        "learned_orthogonal_subset": {"n": orth_n, "correct": learn_orth_cor, "correct_rate": learn_orth_rate},
        "learned_mixed_subset": {"n": mix_n, "correct": learn_mix_cor, "correct_rate": learn_mix_rate,
                                 "false_accept_rate": learn_mix_fa_rate},
    },
    "exact_match": {
        "reconstruction_correct_rate": pc_exact_recon["correct_rate"],
        "exact_match_baseline_correct_rate": pc_exact_baseline["correct_rate"],
        "learned_correct_rate": pc_exact_learned["correct_rate"],
        "learned_false_accept_rate": pc_exact_learned["false_accept_rate"],
        "reconstruction_n": pc_exact_recon["n"],
        "wilson_ci_recon": pc_exact_recon["wilson_correct"],
    },
    "no_applicable": {
        "reconstruction_unknown_precision": float(nc_prec_recon),
        "reconstruction_false_accept_rate": float(nc_fa_recon),
        "learned_unknown_precision": float(nc_prec_learn),
        "learned_false_accept_rate": float(nc_fa_learn),
        "reconstruction_ece_over_all": ece_recon,
        "learned_ece_over_all": ece_learn,
        "ece_bootstrap_mean_rule": float(boot_mean),
        "ece_bootstrap_ci_rule": [float(boot_lo), float(boot_hi)],
        "ece_learned_alias": ece_learn_alias,
        "ece_learned_noapp": ece_learn_noapp,
        "all_methods_precision": {m: (float(nc_prec_all[m]) if nc_prec_all[m] is not None else None)
                                  for m in METHODS_METRIC},
        "all_methods_false_accept": {m: (float(nc_fa_all[m]) if nc_fa_all[m] is not None else None)
                                     for m in METHODS_METRIC},
        "empty_registry_unknown_rate": float(nc_empty_recon["unknown_rate"]),
        "empty_registry_all_methods_unknown": bool(nc_empty_all),
        "bins_reconstruction_rule": bins_recon,
        "bins_reconstruction_learned": bins_learn,
        "reconstruction_confidence_std": conf_std,
        "learned_confidence_std": conf_learn_std,
    },
    "controls": {
        "PC_EXACT_MATCH_pass": bool(pc_pass),
        "PC_EXACT_MATCH_learned_pass": bool(pc_learned_pass),
        "NC_NO_APPLICABLE_pass_recon": bool(nc_pass_recon),
        "NC_NO_APPLICABLE_pass_learned": bool(nc_pass_learn),
        "NC_ALL_pass": bool(nc_pass_all),
        "NC_EMPTY_pass": bool(nc_empty_ok),
        "PC_BROWSERGYM_HEALTH_pass": bool(pc_bg_health),
        "pc_baseline_correct": pc_exact_baseline["correct_rate"],
        "pc_recon_correct": pc_exact_recon["correct_rate"],
        "pc_learned_correct": pc_exact_learned["correct_rate"],
    },
    "live": {
        "attempted": live_attempted,
        "healthy": live_healthy,
        "exploratory_bound": True,
        "browsergym_probe": {k: v for k, v in BG.items()},
        "environment_notes": LIVE_ENV_NOTES,
    },
    "learned": {
        "model_class": "compact MLP (fc 46->128->64) GRPO policy + shared per-slot adoption head + softmax-learned-score confidence; NOT LLM-scale (CPU-only runner has no hosted/offline LLM; frozen spec allows System-One scoring/budget adapter; disclosed)",
        "params_approx": "~15k (46*128 + 128*64 + 64*(3+1+4+1) + biases)",
        "train_split_n": len(train_split),
        "train_split_ids": [t["task_id"] for t in train_split],
        "train_epochs": 120,
        "group_size": 8,
        "reward_definition": "GRPO: correct - 0.75*false_accept + 0.25*(1-|conf-correct|) ; group-relative advantage; aux MSE calibration head loss 0.1; entropy bonus 0.005",
        "confidence_definition": "conf = 0.02+0.96*softmax(learned cand_logits [+ rewrite_logit] / tau).max with learned tau=softplus(inv_temp); gated UNKNOWN when conf<0.80; no-candidate tasks use structural abstain conf 0.05+hash-jitter (RULE-mirror), disclosed",
        "per_seed": per_seed_stats,
        "per_seed_pooled_rates": per_seed_pooled_rates,
        "median_seed": median_seed,
        "cv_pooled_correct": learned_cv,
        "pooled_correct_median": learned_pooled_median,
        "conf_std_min_across_seeds": learned_conf_std_min,
        "train_wall_s_total": round(sum(learned_wall.values()), 3),
        "g0": {
            "gap_correct_rule_minus_learned": g0_gap_correct,
            "gap_ece_abs": g0_gap_ece,
            "cv": g0_cv,
            "conf_std_min": g0_conf_std,
            "pooled_ge_0.50": bool(g0_pooled_ge_50),
            "binomial_p_lt_0.05": bool(g0_binom),
            "mcnemar_p_lt_0.05": bool(g0_mcnemar),
            "gap_correct_ok": bool(g0_gap_ok),
            "ece_ok": bool(g0_ece_ok),
            "cv_ok": bool(g0_cv_ok),
            "conf_ok": bool(g0_conf_ok),
            "orth_ge_0.50": bool(g0_orth_ok),
            "mixed_ge_0.40": bool(g0_mixed_ok),
            "pass": bool(g0_pass),
            "falsified_by_gap_gt_0.15": bool(g0_falsified_by_gap),
            "falsified_by_ece_gt_0.10_or_gt_0.25": bool(g0_falsified_by_ece),
            "falsified_by_cv_gt_0.5": bool(g0_falsified_by_cv),
            "falsified_by_conf_std_le_0.05": bool(g0_falsified_by_conf),
            "falsified_by_orth_lt_0.40": bool(g0_falsified_by_orth),
            "falsified_any": bool(g0_falsified_any),
        },
        "learned_s_gates": {
            "S1_pooled_binom_mcnemar_orth_mixed": bool(learned_s1),
            "S2_fa": bool(learned_s2),
            "S3_exact": bool(learned_s3),
            "S4_noapp_prec_ece": bool(learned_s4),
            "S5_not_dominated": bool(learned_s5),
            "s2_fa_rate_le_0.15": learned_alias["false_accept_rate"] is not None and learned_alias["false_accept_rate"] <= 0.15,
            "s2_below_verbatim_ge_0.15": (verbatim_alias["false_accept_rate"] - (learned_alias["false_accept_rate"] or 0.0)) >= 0.15,
            "s2_mcnemar_p": mcnemar_learn_fa["p"],
            "ece_overall": ece_learn,
            "noapp_precision": float(nc_prec_learn),
        },
    },
    "economics": econ,
    "decision_components": {
        "controls_pass": bool(controls_pass),
        "S1_correct_ge_0.50": bool(s1_correct),
        "S1_binom_p_lt_0.05": bool(s1_binom),
        "S1_mcnemar_p_lt_0.05": bool(s1_mcnemar),
        "S1_orthogonal_ge_0.50": bool(s1_orth),
        "S1_mixed_ge_0.40": bool(s1_mixed),
        "S1_pass": bool(s1_pass),
        "S2_fa_le_0.15": bool(s2_fa),
        "S2_diff_ge_0.15": bool(s2_diff),
        "S2_mcnemar_p_lt_0.05": bool(s2_mcnemar),
        "S2_pass": bool(s2_pass),
        "S3_pass": bool(s3_pass),
        "S4_precision_ge_0.85": bool(s4_prec),
        "S4_ece_le_0.15": bool(s4_ece),
        "S4_pass": bool(s4_pass),
        "S5_not_dominated_by_retrieval": bool(s5_pass),
        "S5_best_rag_correct": float(best_rag),
        "rule_s1_s7_pass": bool(rule_s1_s7),
        "g0_pass": bool(g0_pass),
        "g0_falsified_any": bool(g0_falsified_any),
        "learned_s1_s5_all": bool(learned_s1 and learned_s2 and learned_s3 and learned_s4 and learned_s5),
    },
    "overall": {
        "status": status,
        "outcome": outcome,
        "outcome_reason": outcome_reason,
        "bounded_to": "synthetic pooled 40 (30 orthogonal +10 mixed); live BrowserGym stage exploratory (substrate unavailable: browsergym.webshop/alfworld packages not installable, no playwright browsers); LEARNED arm = compact MLP GRPO adapter (CPU-only runner, no LLM-scale GRPO)",
    },
    "harness_errors": harness_errors,
    "sample_counts": {s: len([t for t in tasks if t["stratum"] == s]) for s in STRATA},
    "fixture_identical_to_parent": bool(fixture_identical),
    "environment": {
        "python": _platform.python_version(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "torch_cuda_available": bool(torch.cuda.is_available()),
        "torch_device_count": torch.cuda.device_count(),
        "seed": SEED,
        "leaned_seeds": LEARNED_SEEDS,
    },
    "orthogonal_mixed_breakdown": {
        "orthogonal_n": orth_n, "orthogonal_correct": orth_cor, "orthogonal_rate": orth_rate,
        "mixed_n": mix_n, "mixed_correct": mix_cor, "mixed_rate": mix_rate, "mixed_fa_rate": mix_fa_rate,
        "learned_orthogonal_correct": learn_orth_cor, "learned_orthogonal_rate": learn_orth_rate,
        "learned_mixed_correct": learn_mix_cor, "learned_mixed_rate": learn_mix_rate,
        "learned_mixed_fa_rate": learn_mix_fa_rate,
    },
}

OUT_DIR.mkdir(parents=True, exist_ok=True)

raw_path = OUT_DIR / "raw_evidence.json"
with open(raw_path, "w") as f:
    json.dump(to_native(raw_evidence), f, indent=2)

derived_path = OUT_DIR / "derived_metrics.json"
with open(derived_path, "w") as f:
    json.dump(to_native(derived_metrics), f, indent=2)

with open(OUT_DIR / "tasks.json", "w") as f:
    json.dump(tasks_serialized(), f, indent=2)

with open(OUT_DIR / "train_split_inventory.json", "w") as f:
    json.dump(to_native(train_split_inventory), f, indent=2)

learned_report = {
    "per_seed": per_seed_stats,
    "median_seed": median_seed,
    "cv_pooled_correct": learned_cv,
    "params_description": derived_metrics["learned"]["params_approx"],
    "model_class_note": derived_metrics["learned"]["model_class"],
    "reward_definition": derived_metrics["learned"]["reward_definition"],
    "confidence_definition": derived_metrics["learned"]["confidence_definition"],
    "train_wall_s_total": derived_metrics["learned"]["train_wall_s_total"],
    "train_split_n": len(train_split),
    "train_epochs": 120,
    "group_size": 8,
    "history": {str(s): learned_history[s] for s in LEARNED_SEEDS},
}
with open(OUT_DIR / "learned_training_report.json", "w") as f:
    json.dump(to_native(learned_report), f, indent=2)

# per-seed raw rows (auditable evidence) — merge into a single file
with open(OUT_DIR / "raw_evidence_learned_seeds.json", "w") as f:
    merged = []
    for s in LEARNED_SEEDS:
        for r in seed_records[s]:
            merged.append(dict(r, method=f"RECONSTRUCTION-LEARNED-SEED{s}"))
    json.dump(to_native(merged), f, indent=2)

print("=" * 120)
print(f"STATUS {status} OUTCOME {outcome}")
print(f"controls_pass={controls_pass} rule_s1_s7={rule_s1_s7} g0_pass={g0_pass} g0_falsified_any={g0_falsified_any} learned_s1_s5_all={learned_s1 and learned_s2 and learned_s3 and learned_s4 and learned_s5}")
print(f"PC {pc_pass} (learned {pc_learned_pass}) NC recon {nc_pass_recon} (learn {nc_pass_learn}) NCempty {nc_empty_ok}")
print(f"S1 rule {s1_pass} S2 {s2_pass} S3 {s3_pass} S4 {s4_pass} S5 {s5_pass}")
print(f"RULE alias pooled {rec_alias['correct_rate']} ({rec_alias['correct']}/{rec_alias['n']}) FA {rec_alias['false_accept_rate']} unknown {rec_alias['unknown_rate']}")
print(f"LEARNED alias pooled {learned_alias['correct_rate']} ({learned_alias['correct']}/{learned_alias['n']}) FA {learned_alias['false_accept_rate']} unknown {learned_alias['unknown_rate']}")
print(f"orth {orth_cor}/{orth_n}={orth_rate} mixed {mix_cor}/{mix_n}={mix_rate} fa {mix_fa_rate} | learn orth {learn_orth_cor}/{orth_n}={learn_orth_rate} mixed {learn_mix_cor}/{mix_n}={learn_mix_rate} fa {learn_mix_fa_rate}")
print(f"verbatim FA {verbatim_alias['false_accept_rate']} tfidf {tfidf_alias['correct_rate']} embed {embed_alias['correct_rate']} exact {exact_rows_alias['correct_rate']} random {random_alias['correct_rate']}")
print(f"ECE rule {ece_recon} boot [{boot_lo:.4f},{boot_hi:.4f}] conf_std {conf_std} | ECE learned {ece_learn} conf_std {conf_learn_std}")
print(f"G0 gap {g0_gap_correct} ece_gap {g0_gap_ece} cv {g0_cv} conf_std_min {g0_conf_std} pooled_ge_50 {g0_pooled_ge_50} binom {p_binom_learn:.2e} mcnemar {mcnemar_learn_vs_exact['p']:.2e} orth_ok {g0_orth_ok} mixed_ok {g0_mixed_ok}")
print(f"per_seed_pooled {per_seed_pooled_rates} median_seed {median_seed}")
print(f"heldout9 rule {heldout_metrics_rule['heldout_9']} learn {heldout_metrics_learn['heldout_9']} | mixed10 rule {heldout_metrics_rule['mixed_10']} learn {heldout_metrics_learn['mixed_10']}")
print(f"diag {diag}")
print(f"harness_errors {len(harness_errors)}")
print(f"fixture_identical_to_parent {fixture_identical}")
print(f"browsergym_probe {BG}")
print(f"economics_latency_per_success_alias: " + json.dumps({m: econ[m]['latency_per_successful_alias_task_s'] for m in METHODS_METRIC}))
print("=" * 120)