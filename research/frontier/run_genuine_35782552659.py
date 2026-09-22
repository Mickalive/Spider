#!/usr/bin/env python3
"""
EXP-FRONTIER-35782552659 EXECUTE — hierarchical decoupling-before-aggregation retrieval
complementarity vs flat top-5 RAG (TFIDF/embed) and vs verbatim replay, for C-SEMANTIC-RESOLVE.

Frozen design (spec.json / prereg.md / request.json director_mandate, PIVOT, SUPERSEDE):
  H-HIERARCHICAL-XMEMORY  : episode -> semantic component -> theme (agglomerative Jaccard
                            threshold 0.6, revisable grouping disclosed-not-exercised),
                            top-down complementary selection expanding only while
                            softmax-entropy > 0.4 OR distinct component coverage < 2,
                            adaptive k in [2,5], max 2 mechanisms per theme,
                            TFIDF theme centroids fit on TRAIN registry only (63 episodes
                            = 21 standard alias tasks x 3 mechanisms), query serialized as
                            "intent url_path header_keys body_keys".
  Baselines: B-EXACT-MATCH (kernel exact intent), B-VERBATIM-REPLAY (verbatim bind),
             B-FLAT-RAG-TFIDF-K5 (+reconstruction), B-FLAT-RAG-EMBED-K5 (+reconstruction,
             all-MiniLM-L6-v2), B-FLAT-RAG-EMBED-K1 (embed top-1 + verbatim bind ablation),
             B-RANDOM-K5 (+reconstruction).
  Downstream for retrieval pipelines: parent RECONSTRUCTION-RULE (choose_adoptions +
  rewrite_template_multi) copied verbatim from EXP-FRONTIER-35773143736 (audit PASS) —
  non-oracle, identical across pipelines to isolate the retrieval effect.
  Retrieval pool per task = the task's own registry mechanisms (registry contains 3
  mechanisms per alias task; intent held equal isolates aliasing).
  Fixture: byte-identical reuse of parent tasks.json (sha256 4abf148721...); NO new
  BrowserGym SPAs per Director rationale (0/4 envs after 12 attempts); no src/ edits;
  no git operations. Code root: research/frontier.

Decision rule (frozen, prereg §7 / spec.decision_rule): PC/NC must pass else
MEASUREMENT_INVALID; SURVIVES iff S1-S6 (S6 = coverage gain >= 0.15 over best flat with
family-blocked bootstrap 2000 CI lower > 0.05, p < 0.05, AND density gain > 0 bootstrap
p < 0.05); if S1-S5 pass but S6 fails -> MIXED; FALSIFIED-IN-SETTING if S1 severe fail,
S2 fail, or S5 domination fail.

RAW EVIDENCE -> OBSERVATION -> DERIVED MEASUREMENT separation: this script writes only
raw evidence + derived measurements + index manifest. result.json/report.md/
provenance.json are authored separately from these artifacts.
"""
import json, math, random, re, sys, hashlib, time, os, platform
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from spider.kernel import SpiderKernel, _bind, _template_slots
from spider.models import Mechanism, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from scipy.stats import binom as scipy_binom
from scipy.stats import chi2 as chi2dist

SEED = 42
random.seed(SEED)
rng = np.random.RandomState(SEED)

EXP_ID = "EXP-FRONTIER-35782552659"
OUT_DIR = Path("/home/runner/work/Spider/Spider/research/experiments") / EXP_ID
PARENT_DIR = Path("/home/runner/work/Spider/Spider/research/experiments") / "EXP-FRONTIER-35773143736"
FROZEN_FIXTURE_SHA256 = "4abf148721fdee9dfe56ac776f6b3112344821a4ea80d183c5313adeced1f35e"

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

# ------------------------------------------------------------------ helpers (parent verbatim)
def to_native(o):
    if isinstance(o, dict):
        return {k: to_native(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
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

def template_text(template):
    return json.dumps(template, sort_keys=True)

# ------------------------------------------------- template introspection + reconstruction (parent verbatim RULE)
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

def choose_adoptions(derived, candidates, params):
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
    """Genuine non-oracle reconstruction (parent RULE verbatim)."""
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

# ------------------------------------------------------------------ fixture load (byte-identical parent reuse)
OUT_DIR.mkdir(parents=True, exist_ok=True)
src_fixture = PARENT_DIR / "tasks.json"
assert src_fixture.exists(), "parent fixture missing"
src_sha = sha256_file(src_fixture)
assert src_sha == FROZEN_FIXTURE_SHA256, f"parent fixture sha mismatch {src_sha}"
dst_fixture = OUT_DIR / "tasks.json"
if not dst_fixture.exists() or sha256_file(dst_fixture) != src_sha:
    dst_fixture.write_bytes(src_fixture.read_bytes())
assert sha256_file(dst_fixture) == FROZEN_FIXTURE_SHA256

fixture = json.loads(src_fixture.read_text("utf-8"))
assert len(fixture) == 70
tasks = []
for t in fixture:
    registry = [make_mechanism(m["mechanism_id"], m["intent"], m["template"], m["confidence"])
                for m in t["registry"]]
    tasks.append({
        "task_id": t["task_id"], "stratum": t["stratum"], "family": t["family"],
        "intent": t["intent"], "derived_context": dict(t["derived_context"]),
        "params": dict(t["params"]), "hidden_expected": dict(t["hidden_expected"]),
        "expected_outcome": t["expected_outcome"], "is_heldout": bool(t["is_heldout"]),
        "registry": registry,
    })

# ---- oracle/leak audits at load (NC-ORACLE-LEAK part 1)
forbidden_in_derived = []
for t in tasks:
    extra = set(t["derived_context"].keys()) - ALLOWED_STATE_KEYS
    assert not extra, f"derived context extra keys {extra} in {t['task_id']}"
    fb = FORBIDDEN_KEYS & set(t["derived_context"].keys())
    assert not fb, f"forbidden keys in derived context {fb} in {t['task_id']}"
    for k, v in t["derived_context"].items():
        if isinstance(v, dict):
            for kk in v:
                if kk in FORBIDDEN_KEYS:
                    forbidden_in_derived.append((t["task_id"], kk))
registry_leak = 0
for t in tasks:
    if t["stratum"] != "alias-OOD":
        continue
    exp = t["hidden_expected"]["expected_template"]
    for m in t["registry"]:
        if m.action_template == exp:
            registry_leak += 1
assert registry_leak == 0

assert len([t for t in tasks if t["stratum"] == "alias-OOD"]) == 40
assert len([t for t in tasks if t["stratum"] == "exact-match"]) == 12
assert len([t for t in tasks if t["stratum"] == "no-applicable"]) == 12
assert len([t for t in tasks if t["stratum"] == "empty-registry"]) == 6
print(f"fixture loaded: 70 tasks, sha {src_sha[:16]}..., registry_leak {registry_leak}, forbidden_in_derived {len(forbidden_in_derived)}")

# ------------------------------------------------------------------ TRAIN REGISTRY (frozen: standard non-heldout orthogonal only)
train_tasks = [t for t in tasks if t["stratum"] == "alias-OOD" and t["family"] in (0, 1, 2)
               and not t["is_heldout"]]
assert len(train_tasks) == 21, len(train_tasks)
train_episodes = []   # (episode_id, mechanism, task_id, family)
for t in sorted(train_tasks, key=lambda x: x["task_id"]):
    for m in sorted(t["registry"], key=lambda x: x.mechanism_id):
        train_episodes.append((f"{t['task_id']}::{m.mechanism_id}", m, t["task_id"],
                               t["family"]))
assert len(train_episodes) == 63, len(train_episodes)

heldout9_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD"
                and t["family"] in (0, 1, 2) and t["is_heldout"]]
mixed_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] == 3]
assert len(heldout9_ids) == 9 and len(mixed_ids) == 10

TRAIN_INVENTORY = {
    "train_tasks": [t["task_id"] for t in sorted(train_tasks, key=lambda x: x["task_id"])],
    "episodes": [e[0] for e in train_episodes],
    "episode_count": len(train_episodes),
    "excluded": {
        "heldout9": heldout9_ids,
        "mixed10": mixed_ids,
        "note": "index/centroid fit on train registry ONLY (standard orthogonal alias tasks); held-out forms and mixed compositions held out from theme training per spec",
    },
    "fixture_sha256": FROZEN_FIXTURE_SHA256,
    "registry_leak": registry_leak,
}
with open(OUT_DIR / "train_split_inventory.json", "w") as f:
    json.dump(to_native(TRAIN_INVENTORY), f, indent=2)

# ------------------------------------------------------------------ TFIDF + embed indices (train-fit only)
TRAIN_DOCS = [f"{m.intent} {template_text(m.action_template)}" for _, m, _, _ in train_episodes]
tfidf_vec = TfidfVectorizer()
X_train = tfidf_vec.fit_transform(TRAIN_DOCS)          # 63 x V
print(f"train tfidf fit: {X_train.shape[0]} episodes x {X_train.shape[1]} vocab")

# -------------------------------------------------- component extraction (template parsing only)
def extract_components(m):
    """Deterministic template-only parsing. Returns (component_set, channel_votes).
    component_set labels: hdr:<key>, bdy:<key>, qry:<key>, seg:<token>, auth:<literal>.
    channel_votes: channel letters for hdr/bdy/qry/auth components only (seg excluded from
    theme-type voting, but seg tokens remain part of the Jaccard component sets per spec:
    'url_segments, query_keys, header_keys, body_fields, auth_scopes' are all components)."""
    comps = template_components(m.action_template)
    comp_set = set()
    votes = []
    for k in comps["headers"]:
        comp_set.add("hdr:" + norm_key(k)); votes.append("hdr")
    for k in comps["body"]:
        comp_set.add("bdy:" + norm_key(k)); votes.append("bdy")
    for qk in comps["qkeys"]:
        comp_set.add("qry:" + norm_key(qk)); votes.append("qry")
    for s in comps["static"]:
        comp_set.add("seg:" + norm_key(s))
    qs = comps["query_str"]
    if qs:
        for kv in qs.split("&"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                if not PARAM_RE.search(v) and v:
                    comp_set.add("auth:" + norm_key(v)); votes.append("auth")
    return comp_set, votes

def theme_type_from_votes(votes):
    """Spec theme names: header / body / auth / mixed. Query channel votes (qry|auth) count
    as auth (this substrate's auth manifests as query scope + X-Scope/X-Permission headers)."""
    if not votes:
        return "mixed"
    hdr = votes.count("hdr"); bdy = votes.count("bdy"); auth = votes.count("qry") + votes.count("auth")
    counts = {"header": hdr, "body": bdy, "auth": auth}
    top = sorted(counts.items(), key=lambda kv: -kv[1])
    if top[0][1] == 0:
        return "mixed"
    if top[0][1] == top[1][1]:
        return "mixed"
    return top[0][0]

# -------------------------------------------------- agglomerative clustering (Jaccard >= 0.6 => distance <= 0.4)
comp_sets = [extract_components(m)[0] for _, m, _, _ in train_episodes]
n_eps = len(train_episodes)
jaccard_dist = np.zeros((n_eps, n_eps))
for i in range(n_eps):
    for j in range(i + 1, n_eps):
        si, sj = comp_sets[i], comp_sets[j]
        if not si and not sj:
            sim = 1.0
        elif not si or not sj:
            sim = 0.0
        else:
            inter = len(si & sj)
            union = len(si | sj)
            sim = inter / union
        d = 1.0 - sim
        jaccard_dist[i, j] = d
        jaccard_dist[j, i] = d
cluster = AgglomerativeClustering(n_clusters=None, metric="precomputed",
                                  linkage="average", distance_threshold=0.4)
labels = cluster.fit_predict(jaccard_dist)
n_themes = int(labels.max()) + 1
print(f"agglomerative Jaccard>=0.6 average linkage -> {n_themes} themes over {n_eps} episodes")

themes = []
for ti in range(n_themes):
    idx = [j for j in range(n_eps) if labels[j] == ti]
    eps = [train_episodes[j][0] for j in sorted(idx)]
    union_comp = set()
    votes_all = []
    for j in idx:
        cs, vs = extract_components(train_episodes[j][1])
        union_comp |= cs
        votes_all.extend(vs)
    themes.append({
        "theme_id": f"theme-{ti}",
        "type": theme_type_from_votes(votes_all),
        "members": eps,
        "member_count": len(eps),
        "component_union": sorted(union_comp),
        "component_union_count": len(union_comp),
    })
centroids = np.zeros((n_themes, X_train.shape[1]))
for ti in range(n_themes):
    idx = [j for j in range(n_eps) if labels[j] == ti]
    centroids[ti] = np.asarray(X_train[idx].mean(axis=0)).flatten()
# normalize centroids to unit vectors for cosine scoring
cnorm = np.linalg.norm(centroids, axis=1)
cnorm[cnorm == 0] = 1.0
centroids_unit = centroids / cnorm[:, None]

H_MANIFEST = {
    "experiment_id": EXP_ID,
    "index_kind": "hierarchical episode->component->theme (xMemory-style, static/revisable-disclosed)",
    "episode_count": n_eps,
    "train_registry_episodes": [e[0] for e in train_episodes],
    "theme_count": n_themes,
    "themes": themes,
    "component_extraction": "template-string parsing only (regex ${slot} + '/' '?' '&' ':' splitting); no hidden_expected access",
    "forbidden_keys_in_manifest": [],
    "clustering": {"similarity": "Jaccard on full component sets (url_segments+query_keys+header_keys+body_fields+auth_scopes)",
                   "agglomerative_linkage": "average", "distance_threshold": 0.4, "jaccard_threshold": 0.6},
    "query_serialization": "intent url_path header_keys body_keys",
    "theme_scoring": "cosine(mean TFIDF member centroid, train-fit vectorizer)",
    "selection": {"expand_while": "softmax_entropy>0.4 OR distinct_component_type_coverage<2",
                  "adaptive_k_range": [2, 5], "max_per_theme": 2},
    "episodes_have_forbidden_keys": 0,
}
manifest_hash = hashlib.sha256(json.dumps(to_native(H_MANIFEST), sort_keys=True).encode("utf-8")).hexdigest()
H_MANIFEST["manifest_sha256"] = manifest_hash
with open(OUT_DIR / "index_manifest.json", "w") as f:
    json.dump(to_native(H_MANIFEST), f, indent=2)

# -------------------------------------------------- embed (real offline, available)
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

# -------------------------------------------------- retrieval functions (auditable signatures)
PIPELINES = ["B-EXACT-MATCH", "B-VERBATIM-REPLAY", "B-FLAT-RAG-TFIDF-K5", "B-FLAT-RAG-EMBED-K5",
             "B-FLAT-RAG-EMBED-K1", "B-RANDOM-K5", "H-HIERARCHICAL-XMEMORY"]

def serialize_query(intent, derived):
    hdr = " ".join(sorted(k.lower() for k in (derived["headers_observed"] or {}).keys()))
    bdy = " ".join(sorted(k.lower() for k in (derived["body_observed"] or {}).keys()))
    return f"{intent} {derived['url_path']} {hdr} {bdy}"

def doc_vecs(ms):
    docs = [f"{m.intent} {template_text(m.action_template)}" for m in ms]
    return tfidf_vec.transform(docs)

def flat_tfidf_retrieve(intent, derived, registry, k=5):
    """Flat TF-IDF cosine top-k over the task's own registry (vectorizer fit on train registry only)."""
    if not registry:
        return [], {"k": 0, "scores": [], "retrieved_ids": [], "query_doc": serialize_query(intent, derived)}
    q_doc = serialize_query(intent, derived)
    qv = tfidf_vec.transform([q_doc])
    mv = doc_vecs(registry)
    sims = cosine_similarity(qv, mv).flatten()
    order = np.argsort(-sims, kind="stable")
    order = [int(j) for j in order[: min(k, len(registry))]]
    cands = [registry[j] for j in order]
    return cands, {"k": len(cands), "scores": [float(sims[j]) for j in order],
                   "retrieved_ids": [m.mechanism_id for m in cands],
                   "query_doc": q_doc}

def flat_embed_retrieve(intent, derived, registry, k=5):
    """Flat all-MiniLM-L6-v2 cosine top-k over task registry (frozen strong retrieval baseline)."""
    if not registry:
        return [], {"k": 0, "scores": [], "retrieved_ids": [], "query_doc": serialize_query(intent, derived)}
    q_doc = serialize_query(intent, derived)
    docs = [f"{m.intent} {template_text(m.action_template)}" for m in registry]
    q_e = embed_encode([q_doc])[0]
    m_e = embed_encode(docs)
    sims = m_e @ q_e
    order = np.argsort(-sims, kind="stable")
    order = [int(j) for j in order[: min(k, len(registry))]]
    cands = [registry[j] for j in order]
    return cands, {"k": len(cands), "scores": [float(sims[j]) for j in order],
                   "retrieved_ids": [m.mechanism_id for m in cands],
                   "query_doc": q_doc}

def random_retrieve(intent, derived, registry, k=5):
    if not registry:
        return [], {"k": 0, "scores": [], "retrieved_ids": [], "query_doc": serialize_query(intent, derived)}
    n = min(k, len(registry))
    idx = rng.choice(len(registry), size=n, replace=False)
    cands = [registry[int(j)] for j in idx]
    return cands, {"k": len(cands), "scores": [], "retrieved_ids": [m.mechanism_id for m in cands],
                   "query_doc": serialize_query(intent, derived)}

def hierarchical_retrieve(intent, derived, registry):
    """Decoupling-before-aggregation hierarchical retrieval, per frozen spec."""
    q_doc = serialize_query(intent, derived)
    meta = {"query_doc": q_doc, "k": 0, "retrieved_ids": [], "scores": [],
            "themes_selected": [], "theme_types_selected": [], "theme_score_rank": [],
            "mechanism_theme_assignment": [], "entropy_trace": [], "coverage_trace": [],
            "expansion_steps": 0, "k_cap_reason": None}
    if not registry:
        meta["k_cap_reason"] = "empty_registry"
        return [], meta
    qv = tfidf_vec.transform([q_doc])
    t_sims = cosine_similarity(qv, centroids_unit).flatten()
    theme_rank = [int(j) for j in np.argsort(-t_sims, kind="stable")]
    meta["theme_score_rank"] = [{"theme_id": themes[j]["theme_id"], "type": themes[j]["type"],
                                 "score": float(t_sims[j])} for j in theme_rank]
    mv = doc_vecs(registry)
    m_sims = cosine_similarity(mv, centroids_unit)          # R x T
    m_theme = [int(np.argmax(row)) for row in m_sims]       # deterministic argmax (ties -> first)
    m_best = [float(np.max(row)) for row in m_sims]
    meta["mechanism_theme_assignment"] = [
        {"mechanism_id": m.mechanism_id, "theme_id": themes[m_theme[j]]["theme_id"],
         "theme_type": themes[m_theme[j]]["type"], "centroid_cosine": m_best[j]}
        for j, m in enumerate(registry)]
    selected = []
    selected_theme_ids = []
    seen_ids = set()
    # mechanisms available per theme, preordered by per-mechanism centroid cosine desc
    per_theme = {}
    for j in range(len(registry)):
        per_theme.setdefault(m_theme[j], []).append(j)
    for tl in per_theme.values():
        tl.sort(key=lambda j: (-m_best[j], j))
    for t_i in theme_rank:
        if len(selected) >= 5:
            break
        added = 0
        for j in per_theme.get(t_i, []):
            if len(selected) >= 5:
                break
            if registry[j].mechanism_id in seen_ids:
                continue
            selected.append(registry[j])
            seen_ids.add(registry[j].mechanism_id)
            selected_theme_ids.append(t_i)
            added += 1
            if added >= 2:
                break
        if added == 0:
            continue
        meta["expansion_steps"] += 1
        k = len(selected)
        if k >= 5:
            meta["k_cap_reason"] = "max_k"
            break
        # frozen expansion criterion: expand to next theme only while
        # softmax-entropy > 0.4 OR distinct component-type coverage < 2
        scores = [candidate_score(m, derived) for m in selected]
        probs = softmax(scores, temp=0.15)
        ent = -float(sum(p * math.log(p) for p in probs))
        comp_types = set()
        for m in selected:
            cs, vs = extract_components(m)
            comp_types |= set(vs)
        cov = len(comp_types)
        meta["entropy_trace"].append(ent)
        meta["coverage_trace"].append(cov)
        if ent <= 0.4 and cov >= 2:
            meta["k_cap_reason"] = "criterion_stop"
            break
    # min-k guarantee: if k == 1 and more mechanisms available, top-up by centroid cosine
    if len(selected) < 2 and len(registry) >= 2:
        for j in np.argsort(-np.array(m_best), kind="stable"):
            if len(selected) >= 2:
                break
            if registry[int(j)].mechanism_id not in seen_ids:
                selected.append(registry[int(j)])
                seen_ids.add(registry[int(j)].mechanism_id)
                selected_theme_ids.append(m_theme[int(j)])
        meta["k_cap_reason"] = "min_k_topup"
    if meta["k_cap_reason"] is None:
        meta["k_cap_reason"] = "registry_size"
    meta["k"] = len(selected)
    meta["retrieved_ids"] = [m.mechanism_id for m in selected]
    meta["themes_selected"] = [themes[t_i]["theme_id"] for t_i in selected_theme_ids]
    meta["theme_types_selected"] = [themes[t_i]["type"] for t_i in selected_theme_ids]
    return selected, meta

# -------------------------------------------------- pipeline resolvers
TMP_REG = Path(f"/tmp/spider_test_registry_{EXP_ID}.jsonl")

def resolve_exact_match(task, meta):
    reg = MechanismRegistry(TMP_REG)
    reg.replace(task["registry"])
    kernel = SpiderKernel(reg, min_confidence=0.8)
    res = kernel.resolve(task["intent"], task["derived_context"], task["params"])
    matched = [m for m in task["registry"] if m.intent == task["intent"]]
    meta["retrieved_ids"] = [m.mechanism_id for m in matched]
    meta["k"] = len(matched)
    return res

def resolve_verbatim(task, meta):
    candidates = [m for m in task["registry"] if m.intent == task["intent"]]
    meta["retrieved_ids"] = [m.mechanism_id for m in candidates]
    meta["k"] = len(candidates)
    eligible = []
    for m in candidates:
        required = set(m.parameter_slots) | _template_slots(m.action_template)
        if all(slot in task["params"] for slot in required):
            eligible.append(m)
    if not eligible:
        return Resolution(ResolutionStatus.UNKNOWN, None, "no eligible", confidence=0.0), meta
    best = eligible[0]
    bound = _bind(best.action_template, task["params"])
    return Resolution(ResolutionStatus.EXECUTABLE, best.mechanism_id, "verbatim replay",
                      bound_action=bound, confidence=best.confidence), meta

def resolve_flat_tfidf(task, k=5):
    cands, meta = flat_tfidf_retrieve(task["intent"], task["derived_context"], task["registry"], k=k)
    res = reconstruct_resolve(task["intent"], task["derived_context"], cands, task["params"])
    return res, meta

def resolve_flat_embed(task, k=5, verbatim=False):
    cands, meta = flat_embed_retrieve(task["intent"], task["derived_context"], task["registry"], k=k)
    if verbatim:
        if not cands:
            return Resolution(ResolutionStatus.UNKNOWN, None, "no candidates", confidence=0.0), meta
        required = set(cands[0].parameter_slots) | _template_slots(cands[0].action_template)
        if not all(slot in task["params"] for slot in required):
            return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots verbatim",
                              confidence=float(meta["scores"][0]) if meta["scores"] else 0.0), meta
        bound = _bind(cands[0].action_template, task["params"])
        conf = max(0.1, min(0.99, meta["scores"][0]))
        return Resolution(ResolutionStatus.EXECUTABLE, cands[0].mechanism_id,
                          "embed top-1 verbatim bind (ablation)",
                          bound_action=bound, confidence=conf), meta
    res = reconstruct_resolve(task["intent"], task["derived_context"], cands, task["params"])
    return res, meta

def resolve_random(task, k=5):
    cands, meta = random_retrieve(task["intent"], task["derived_context"], task["registry"], k=k)
    res = reconstruct_resolve(task["intent"], task["derived_context"], cands, task["params"])
    return res, meta

def resolve_hierarchical(task):
    cands, meta = hierarchical_retrieve(task["intent"], task["derived_context"], task["registry"])
    res = reconstruct_resolve(task["intent"], task["derived_context"], cands, task["params"])
    return res, meta

# -------------------------------------------------- retrieval measurands (recall probe, density)
def probe_recall(mech, task):
    """recall@k probe: 1 if reconstruct_resolve on THIS single candidate yields expected_bound."""
    res = reconstruct_resolve(task["intent"], task["derived_context"], [mech], task["params"])
    if res.status == ResolutionStatus.EXECUTABLE and res.bound_action == task["hidden_expected"]["expected_bound"]:
        return True
    return False

def distinct_components_of(mechs):
    out = set()
    types = set()
    for m in mechs:
        cs, vs = extract_components(m)
        for c in cs:
            out.add(c)
        types |= set(vs)
    return out, types

# -------------------------------------------------- EVALUATION (7 pipelines x 70 tasks, paired)
TASK_STRATA = ["alias-OOD", "exact-match", "no-applicable", "empty-registry"]
raw_evidence = []
harness_errors = []
CNT = {m: {"tasks": 0, "ok": 0, "latency_s": 0.0, "scoring_calls": 0, "rewrite_ops": 0,
           "bind_ops": 0, "retrieval_candidates": 0, "embed_encodings": 0} for m in PIPELINES}

for task in tasks:
    for mname in PIPELINES:
        t_start = time.perf_counter()
        res = None
        avail = True
        retrie_meta = {"k": 0, "retrieved_ids": [], "scores": [], "query_doc": "",
                       "themes_selected": [], "theme_types_selected": [], "theme_score_rank": [],
                       "mechanism_theme_assignment": [], "entropy_trace": [], "coverage_trace": [],
                       "expansion_steps": 0, "k_cap_reason": None}
        try:
            if mname == "B-EXACT-MATCH":
                res = resolve_exact_match(task, retrie_meta)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            elif mname == "B-VERBATIM-REPLAY":
                res, retrie_meta = resolve_verbatim(task, retrie_meta)
                CNT[mname]["retrieval_candidates"] += len([m for m in task["registry"] if m.intent == task["intent"]])
            elif mname == "B-FLAT-RAG-TFIDF-K5":
                res, retrie_meta = resolve_flat_tfidf(task, k=5)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            elif mname == "B-FLAT-RAG-EMBED-K5":
                if EMBED_AVAILABLE:
                    res, retrie_meta = resolve_flat_embed(task, k=5, verbatim=False)
                    CNT[mname]["retrieval_candidates"] += len(task["registry"])
                    if task["registry"]:
                        CNT[mname]["embed_encodings"] += len(task["registry"]) + 1
                else:
                    avail = False
            elif mname == "B-FLAT-RAG-EMBED-K1":
                if EMBED_AVAILABLE:
                    res, retrie_meta = resolve_flat_embed(task, k=1, verbatim=True)
                    CNT[mname]["retrieval_candidates"] += min(1, len(task["registry"]))
                    if task["registry"]:
                        CNT[mname]["embed_encodings"] += len(task["registry"]) + 1
                else:
                    avail = False
            elif mname == "B-RANDOM-K5":
                res, retrie_meta = resolve_random(task, k=5)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            elif mname == "H-HIERARCHICAL-XMEMORY":
                res, retrie_meta = resolve_hierarchical(task)
                CNT[mname]["retrieval_candidates"] += len(task["registry"])
            else:
                res = None
                avail = False
        except Exception as e:
            harness_errors.append({"task_id": task["task_id"], "method": mname, "error": str(e)})
            print(f"DEBUG-ERROR {task['task_id']} {mname}: {type(e).__name__}: {e}", flush=True)
            res = None
            avail = False
        latency = time.perf_counter() - t_start
        CNT[mname]["tasks"] += 1
        CNT[mname]["latency_s"] += latency
        if res is not None and res.status == ResolutionStatus.EXECUTABLE:
            CNT[mname]["bind_ops"] += 1
        expected_outcome = task["expected_outcome"]
        expected_bound = task["hidden_expected"]["expected_bound"]
        is_correct = is_false_accept = is_unknown = None
        reason = observed_status = observed_bound = None
        observed_confidence = None
        if res is not None:
            observed_status = res.status.value
            observed_bound = res.bound_action
            observed_confidence = float(res.confidence)
            reason = res.reason
            if expected_outcome == "unknown":
                if res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE):
                    is_unknown = True; is_correct = False; is_false_accept = False
                else:
                    is_false_accept = True; is_correct = False; is_unknown = False
            else:
                if res.status == ResolutionStatus.EXECUTABLE:
                    if res.bound_action == expected_bound:
                        is_correct = True; is_false_accept = False; is_unknown = False
                    else:
                        is_false_accept = True; is_correct = False; is_unknown = False
                elif res.status in (ResolutionStatus.UNKNOWN, ResolutionStatus.EXPLORE):
                    is_unknown = True; is_correct = False; is_false_accept = False
                else:
                    is_false_accept = True; is_correct = False; is_unknown = False
        assert "retrieved_ids" in retrie_meta, ("MISSING-KEY", mname, task["task_id"], sorted(retrie_meta.keys()))
        cands_for_ec = [m for m in task["registry"] if m.mechanism_id in retrie_meta["retrieved_ids"]]
        if mname in ("B-FLAT-RAG-TFIDF-K5", "B-FLAT-RAG-EMBED-K5", "B-RANDOM-K5",
                     "H-HIERARCHICAL-XMEMORY"):
            CNT[mname]["scoring_calls"] += len(cands_for_ec)
            CNT[mname]["rewrite_ops"] += len(choose_adoptions(task["derived_context"],
                                                              cands_for_ec, task["params"]))
        if is_correct:
            CNT[mname]["ok"] += 1
        # retrieval measurands
        retrieved = [m for m in task["registry"] if m.mechanism_id in retrie_meta["retrieved_ids"]]
        k_used = len(retrieved)
        recall = 0
        if k_used and task["stratum"] == "alias-OOD":
            recall = 1 if any(probe_recall(m, task) for m in retrieved) else 0
        dset, dtypes = distinct_components_of(retrieved)
        density = (len(dset) / k_used) if k_used else None
        raw_evidence.append({
            "task_id": task["task_id"], "stratum": task["stratum"], "family": task["family"],
            "method": mname, "intent": task["intent"], "expected_outcome": expected_outcome,
            "expected_bound": expected_bound, "observed_status": observed_status,
            "observed_bound": observed_bound, "observed_confidence": observed_confidence,
            "is_correct": is_correct, "is_false_accept": is_false_accept,
            "is_unknown": is_unknown, "reason": reason,
            "registry_size": len(task["registry"]), "is_heldout": task["is_heldout"],
            "method_available": avail, "latency_s": latency,
            "retrieved_ids": retrie_meta["retrieved_ids"], "k_used": k_used,
            "recall_at_k": recall, "coverage": recall,
            "distinct_components": len(dset), "distinct_component_types": len(dtypes),
            "density": density,
            "query_doc": retrie_meta.get("query_doc", ""),
            "themes_selected": retrie_meta.get("themes_selected", []),
            "theme_types_selected": retrie_meta.get("theme_types_selected", []),
            "theme_score_rank": retrie_meta.get("theme_score_rank", []),
            "mechanism_theme_assignment": retrie_meta.get("mechanism_theme_assignment", []),
            "entropy_trace": retrie_meta.get("entropy_trace", []),
            "coverage_trace": retrie_meta.get("coverage_trace", []),
            "expansion_steps": retrie_meta.get("expansion_steps", 0),
            "k_cap_reason": retrie_meta.get("k_cap_reason", None),
        })

print(f"evaluation done: rows {len(raw_evidence)}, harness_errors {len(harness_errors)}")

# -------------------------------------------------- METRICS
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

def rows(method, stratum=None):
    out = [r for r in raw_evidence if r["method"] == method and r["method_available"]]
    if stratum is not None:
        out = [r for r in out if r["stratum"] == stratum]
    return out

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

def compute_ece(method, stratum=None):
    subset = rows(method, stratum)
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

def get_task_ids(stratum):
    return sorted(set(r["task_id"] for r in raw_evidence if r["stratum"] == stratum))

def row_for(tid, method):
    return [r for r in raw_evidence if r["task_id"] == tid and r["method"] == method
            and r["method_available"]][0]

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

alias_ids = get_task_ids("alias-OOD")
orth_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] in (0, 1, 2)]
mix_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] == 3]
held9_ids = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD"
             and t["family"] in (0, 1, 2) and t["is_heldout"]]
exact_ids = get_task_ids("exact-match")
noapp_ids = get_task_ids("no-applicable")
empty_ids = get_task_ids("empty-registry")

STRATA = TASK_STRATA
metrics = {}
for m in PIPELINES:
    for s in STRATA:
        metrics[f"{m}::{s}"] = compute_rates(m, s)

def paired_lists(method_a, method_b, field, ids=alias_ids):
    a_list, b_list = [], []
    for tid in ids:
        a_list.append(row_for(tid, method_a)[field])
        b_list.append(row_for(tid, method_b)[field])
    return a_list, b_list

def subset_rate(method, ids, field="is_correct"):
    n = len(ids)
    k = sum(1 for tid in ids if row_for(tid, method)[field])
    return k, n, (k / n if n else None)

# ---- per-method alias breakdowns
alias_out = {}
for m in PIPELINES:
    rates = metrics[f"{m}::alias-OOD"]
    orth = subset_rate(m, orth_ids)
    mix = subset_rate(m, mix_ids)
    held = subset_rate(m, held9_ids)
    fam = {}
    for f in (0, 1, 2, 3):
        fid = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] == f]
        kk, nn, rr = subset_rate(m, fid)
        fam[f"fam{f}"] = {"n": nn, "correct": kk, "correct_rate": rr}
    alias_out[m] = {
        "n": rates["n"], "correct": rates["correct"],
        "correct_rate": rates["correct_rate"],
        "false_accept_rate": rates["false_accept_rate"],
        "unknown_rate": rates["unknown_rate"],
        "wilson_correct": rates["wilson_correct"],
        "wilson_false": rates["wilson_false"],
        "binomial_p_vs_0.10": binomial_p(rates["correct"], rates["n"], 0.10),
        "orthogonal": {"n": orth[1], "correct": orth[0], "correct_rate": orth[2],
                       "wilson_ci": [wilson_ci(orth[0], orth[1])[0], wilson_ci(orth[0], orth[1])[1]],
                       "binomial_p_vs_0.10": binomial_p(orth[0], orth[1], 0.10)},
        "mixed": {"n": mix[1], "correct": mix[0], "correct_rate": mix[2],
                  "wilson_ci": [wilson_ci(mix[0], mix[1])[0], wilson_ci(mix[0], mix[1])[1]]},
        "heldout9": {"n": held[1], "correct": held[0], "correct_rate": held[2],
                     "wilson_ci": [wilson_ci(held[0], held[1])[0], wilson_ci(held[0], held[1])[1]]},
        "per_family": fam,
    }

HIER = "H-HIERARCHICAL-XMEMORY"
TFIDF_K5 = "B-FLAT-RAG-TFIDF-K5"
EMBED_K5 = "B-FLAT-RAG-EMBED-K5"
EMBED_K1 = "B-FLAT-RAG-EMBED-K1"
EXACT = "B-EXACT-MATCH"
VERB = "B-VERBATIM-REPLAY"
RAND = "B-RANDOM-K5"

# ---- McNemar (paired, alias-OOD)
mcnemar_hier_vs_exact = mcnemar_p(*paired_lists(HIER, EXACT, "is_correct"))
mcnemar_hier_vs_verbatim_fa = mcnemar_p(*paired_lists(HIER, VERB, "is_false_accept"))
flat_rates = {TFIDF_K5: alias_out[TFIDF_K5]["correct_rate"] or 0.0,
              EMBED_K5: alias_out[EMBED_K5]["correct_rate"] or 0.0}
best_flat_name = max(flat_rates, key=lambda k: flat_rates[k])
best_flat_rate = flat_rates[best_flat_name]
mcnemar_hier_vs_best_flat = mcnemar_p(*paired_lists(HIER, best_flat_name, "is_correct"))
mcnemar_flat_k1_fa_vs_hier = mcnemar_p(*paired_lists(EMBED_K1, HIER, "is_false_accept"))

# ---- ECE per pipeline (overall) + hierarchical stratified + bootstrap CI (family-blocked)
ece_out = {}
for m in PIPELINES:
    e_all, bins_all = compute_ece(m)
    e_alias, _ = compute_ece(m, "alias-OOD")
    e_noapp, _ = compute_ece(m, "no-applicable")
    ece_out[m] = {"overall": e_all, "bins_overall": bins_all, "alias_ood": e_alias,
                  "no_applicable": e_noapp}
# family-blocked bootstrap ECE CI for HIER (trajectory grouped by family)
def family_blocks():
    blocks = {}
    for f in (0, 1, 2, 3):
        blocks[f] = [t["task_id"] for t in tasks if t["stratum"] == "alias-OOD" and t["family"] == f]
    return blocks
BLOCKS = family_blocks()

def method_rows_for_tids(method, tids):
    tset = set(tids)
    return [r for r in raw_evidence if r["method"] == method and r["method_available"]
            and r["task_id"] in tset]

def ece_of_rows(subset):
    if not subset:
        return 0.0
    bins = np.linspace(0, 1, 6)
    ece = 0.0
    total = len(subset)
    for b in range(5):
        lo, hi = bins[b], bins[b + 1]
        bin_recs = [r for r in subset if (lo <= r["observed_confidence"] <= hi if b == 4
                                          else lo <= r["observed_confidence"] < hi)]
        if not bin_recs:
            continue
        acc = sum(1 for r in bin_recs if r["is_correct"]) / len(bin_recs)
        avg_conf = float(np.mean([r["observed_confidence"] for r in bin_recs]))
        ece += len(bin_recs) / total * abs(acc - avg_conf)
    return float(ece)

B = 2000
ece_resamples = []
for _ in range(B):
    chosen = []
    for _ in range(len(BLOCKS)):
        f = int(rng.choice(list(BLOCKS.keys())))
        chosen.extend(BLOCKS[f])
    ece_resamples.append(ece_of_rows(method_rows_for_tids(HIER, chosen)))
ece_hier_boot = {"mean": float(np.mean(ece_resamples)),
                 "ci95": [float(np.percentile(ece_resamples, 2.5)), float(np.percentile(ece_resamples, 97.5))]}

# ---- retrieval coverage / density (alias-OOD pooled) + family-blocked bootstrap gains
def cov_dens(method, tids):
    rs = method_rows_for_tids(method, tids)
    n = len(rs)
    cov = sum(1 for r in rs if r["coverage"]) / n if n else None
    dens_vals = [r["density"] for r in rs if r["density"] is not None]
    dens = float(np.mean(dens_vals)) if dens_vals else None
    kvals = [r["k_used"] for r in rs]
    nonempty = sum(1 for r in rs if r["k_used"] > 0)
    return {"n": n, "coverage": cov, "density": dens,
            "mean_k": float(np.mean(kvals)) if kvals else None,
            "median_k": float(np.median(kvals)) if kvals else None,
            "non_empty": nonempty, "non_empty_rate": nonempty / n if n else None}

retrieval_out = {m: cov_dens(m, alias_ids) for m in PIPELINES}

def block_resample_gain(method_a, method_b, metric="coverage", n_resamples=B):
    fam_ids = {f: BLOCKS[f] for f in BLOCKS}
    gains = []
    for _ in range(n_resamples):
        chosen = []
        for _ in range(len(BLOCKS)):
            f = int(rng.choice(list(fam_ids.keys())))
            chosen.extend(fam_ids[f])
        ga = cov_dens(method_a, chosen)[metric]
        gb = cov_dens(method_b, chosen)[metric]
        if ga is None or gb is None:
            gains.append(0.0)
        else:
            gains.append(ga - gb)
    gains = np.array(gains)
    return {"mean": float(np.mean(gains)),
            "ci95": [float(np.percentile(gains, 2.5)), float(np.percentile(gains, 97.5))],
            "p_gain_le_0": float(np.mean(gains <= 0.0)),
            "p_gain_lt_0": float(np.mean(gains < 0.0)),
            "fraction_gain_ge_0.15": float(np.mean(gains >= 0.15))}

coverage_gain = block_resample_gain(HIER, best_flat_name, "coverage")
density_gain_bt = block_resample_gain(HIER, best_flat_name, "density")

# ---- adaptive k distribution (hierarchical, alias-OOD)
hier_k = [row_for(tid, HIER)["k_used"] for tid in alias_ids]
k_hist = {}
for kk in sorted(set(hier_k)):
    k_hist[str(kk)] = hier_k.count(kk)
k_cap_counts = {}
for tid in alias_ids:
    rc = row_for(tid, HIER)["k_cap_reason"]
    k_cap_counts[rc] = k_cap_counts.get(rc, 0) + 1
hier_entropy_final = [row_for(tid, HIER)["entropy_trace"][-1] if row_for(tid, HIER)["entropy_trace"] else None
                      for tid in alias_ids]
hier_cov_final = [row_for(tid, HIER)["coverage_trace"][-1] if row_for(tid, HIER)["coverage_trace"] else None
                  for tid in alias_ids]
theme_type_counts = {}
for tid in alias_ids:
    for tt in row_for(tid, HIER)["theme_types_selected"]:
        theme_type_counts[tt] = theme_type_counts.get(tt, 0) + 1

# ---- confidence stats
conf_out = {}
for m in PIPELINES:
    confs = [r["observed_confidence"] for r in rows(m) if r["observed_confidence"] is not None]
    conf_out[m] = {"n": len(confs),
                   "std": float(np.std(confs)) if confs else None,
                   "mean": float(np.mean(confs)) if confs else None,
                   "min": float(np.min(confs)) if confs else None,
                   "max": float(np.max(confs)) if confs else None}
hier_conf_std = conf_out[HIER]["std"]

# -------------------------------------------------- CONTROLS
# PC-EXACT-MATCH: all pipelines correct>=0.90 and false<=0.10 on exact 12; hierarchical not >0.10 below B-EXACT-MATCH
pc_rows = {}
for m in PIPELINES:
    rates = metrics[f"{m}::exact-match"]
    pc_rows[m] = {"n": rates["n"], "correct_rate": rates["correct_rate"],
                  "false_accept_rate": rates["false_accept_rate"]}
pc_each = {m: (pc_rows[m]["correct_rate"] is not None and pc_rows[m]["correct_rate"] >= 0.90
               and pc_rows[m]["false_accept_rate"] is not None and pc_rows[m]["false_accept_rate"] <= 0.10)
           for m in PIPELINES}
pc_exact_all = all(pc_each.values())
pc_hier_regression = (pc_rows[HIER]["correct_rate"] is not None
                      and pc_rows[EXACT]["correct_rate"] is not None
                      and (pc_rows[EXACT]["correct_rate"] - pc_rows[HIER]["correct_rate"]) <= 0.10)
PC_EXACT_MATCH = {"per_pipeline": pc_rows, "pass_component": pc_each,
                  "pass_all_pipelines": bool(pc_exact_all),
                  "hier_no_regression_gt_0.10": bool(pc_hier_regression),
                  "pass": bool(pc_exact_all and pc_hier_regression)}

# PC-RETRIEVAL-HEALTH: non-empty >=90% on alias-OOD (hier + flats); hier distinct components >= flat on >=50% tasks
non_empty_alias = {m: retrieval_out[m]["non_empty_rate"] for m in PIPELINES}
health_pipelines = [HIER, TFIDF_K5, EMBED_K5]
health_nonempty_ok = all(non_empty_alias[m] is not None and non_empty_alias[m] >= 0.90
                         for m in health_pipelines)
ge_flat = 0
for tid in alias_ids:
    hc = row_for(tid, HIER)["distinct_components"]
    fc = max(row_for(tid, TFIDF_K5)["distinct_components"],
             row_for(tid, EMBED_K5)["distinct_components"])
    if hc >= fc:
        ge_flat += 1
PC_RETRIEVAL_HEALTH = {"non_empty_rate_alias_ood": {m: non_empty_alias[m] for m in health_pipelines},
                       "non_empty_ge_0.90": bool(health_nonempty_ok),
                       "hier_distinct_ge_flat_tasks": ge_flat,
                       "hier_distinct_ge_flat_rate": ge_flat / len(alias_ids),
                       "pass": bool(health_nonempty_ok and ge_flat / len(alias_ids) >= 0.50)}

# PC-HIERARCHICAL-INDEX-BUILT
pc_index_ok = (n_themes >= 3 and sum(t["component_union_count"] for t in themes) >= 6
               and n_eps == len(train_episodes) and len(H_MANIFEST["forbidden_keys_in_manifest"]) == 0)
PC_HIERARCHICAL_INDEX_BUILT = {"theme_count": n_themes, "episode_count": n_eps,
                               "expected_episodes": len(train_episodes),
                               "total_components_across_themes": sum(t["component_union_count"] for t in themes),
                               "forbidden_keys_in_manifest": H_MANIFEST["forbidden_keys_in_manifest"],
                               "manifest_sha256": manifest_hash,
                               "pass": bool(pc_index_ok)}

# NC-NO-APPLICABLE (frozen spec `null_control`): on no-applicable stratum "every
# retrieval+reconstruction pipeline must return UNKNOWN (or gated confidence<0.80)
# with UNKNOWN precision >=0.90 and false_accept <=0.10". Formalization: an ACCEPT is
# an EXECUTABLE decision with confidence >= 0.80 (ungated); every accept on
# no-applicable is a false accept; UNKNOWN or EXECUTABLE with confidence < 0.80
# counts as a correct gated/non-accept decision.
NC_GATE = 0.80
nc_prec_all = {m: unknown_precision(m, "no-applicable") for m in PIPELINES}
nc_fa_all = {m: metrics[f"{m}::no-applicable"]["false_accept_rate"] for m in PIPELINES}
nc_detail = {}
for m in PIPELINES:
    _na_rows = [r for r in raw_evidence if r["method"] == m and r["stratum"] == "no-applicable"]
    _n = len(_na_rows)
    _ungated = [r for r in _na_rows if r["observed_status"] == ResolutionStatus.EXECUTABLE.value
                and (r["observed_confidence"] or 0.0) >= NC_GATE]
    _gated = [r for r in _na_rows if r["observed_status"] == ResolutionStatus.EXECUTABLE.value
              and (r["observed_confidence"] or 0.0) < NC_GATE]
    _unknown = _n - len(_ungated) - len(_gated)
    _fa = len(_ungated) / _n if _n else None
    _prec = (_n - len(_ungated)) / _n if _n else None   # correctly non-accepting decisions
    nc_detail[m] = {"n": _n, "unknown": _unknown, "gated_conf_lt_08": len(_gated),
                    "ungated_false_accept": len(_ungated), "false_accept_rate_gated": _fa,
                    "gated_precision": _prec,
                    "strict_status_false_accept_rate": nc_fa_all[m],
                    "strict_status_unknown_precision": nc_prec_all[m],
                    "pass": bool(_fa is not None and _prec is not None and _prec >= 0.90 and _fa <= 0.10)}
NC_NO_APPLICABLE = {"per_pipeline": nc_detail,
                    "confidence_gate": NC_GATE,
                    "semantics": ("frozen null_control: accept = EXECUTABLE with confidence>=0.80; "
                                  "any accept on no-applicable is a false accept; UNKNOWN or gated(<0.80) "
                                  "counts as correct non-accept; strict status-only rates kept as diagnostics"),
                    "pass": bool(all(v["pass"] for v in nc_detail.values()))}

# NC-EMPTY-REGISTRY: 100% UNKNOWN all pipelines
nc_empty = {m: metrics[f"{m}::empty-registry"]["unknown_rate"] for m in PIPELINES}
NC_EMPTY_REGISTRY = {"per_pipeline_unknown_rate": nc_empty,
                     "pass": bool(all(v == 1.0 for v in nc_empty.values()))}

# NC-ORACLE-LEAK: derived whitelist ok; template-only parsing; no forbidden reads; confidence std>0.05
NC_ORACLE_LEAK = {
    "forbidden_in_derived_count": len(forbidden_in_derived),
    "registry_template_leak_alias_ood": registry_leak,
    "component_extraction": "template-string parsing only (regex + split); component labels derived from mechanism.action_template only",
    "confidence_std_hierarchical": hier_conf_std,
    "confidence_std_gt_0.05": bool(hier_conf_std is not None and hier_conf_std > 0.05),
    "pass": bool(len(forbidden_in_derived) == 0 and registry_leak == 0
                 and hier_conf_std is not None and hier_conf_std > 0.05),
}

# NC-FLAT-COLLAPSE-DIAGNOSTIC (exploratory, non-gating)
def flat_template_overlap(method):
    overlap_vals = []
    for tid in alias_ids:
        r = row_for(tid, method)
        ids = r["retrieved_ids"]
        if len(ids) < 2:
            overlap_vals.append(1.0 if ids else 0.0)
            continue
        tmpls = []
        for m in tasks_by_id(tid)["registry"]:
            if m.mechanism_id in ids:
                tmpls.append(template_text(m.action_template))
        # mean pairwise template-string Jaccard (token sets)
        vals = []
        for i in range(len(tmpls)):
            for j in range(i + 1, len(tmpls)):
                ti = set(re.findall(r"[A-Za-z0-9_]+", tmpls[i].lower()))
                tj = set(re.findall(r"[A-Za-z0-9_]+", tmpls[j].lower()))
                inter = len(ti & tj); union = len(ti | tj)
                vals.append(inter / union if union else 1.0)
        overlap_vals.append(float(np.mean(vals)) if vals else 1.0)
    return float(np.mean(overlap_vals)), len(overlap_vals)

def tasks_by_id(tid):
    return [t for t in tasks if t["task_id"] == tid][0]

tfidf_collapse, _n1 = flat_template_overlap(TFIDF_K5)
embed_collapse, _n2 = flat_template_overlap(EMBED_K5)
NC_FLAT_COLLAPSE = {"tfidf_k5_mean_pairwise_template_jaccard": tfidf_collapse,
                    "embed_k5_mean_pairwise_template_jaccard": embed_collapse,
                    "note": "pool size (3 mechanisms/task) <= k=5: every retriever retrieves the full registry; collapse diagnostic records overlap of the full-pool retrieval"}

controls_pass = (PC_EXACT_MATCH["pass"] and PC_RETRIEVAL_HEALTH["pass"]
                 and PC_HIERARCHICAL_INDEX_BUILT["pass"] and NC_NO_APPLICABLE["pass"]
                 and NC_EMPTY_REGISTRY["pass"] and NC_ORACLE_LEAK["pass"])

# -------------------------------------------------- DECISION (frozen rule, prereg §7 / spec.decision_rule)
H = alias_out[HIER]
s1_pooled_ge_50 = H["correct_rate"] is not None and H["correct_rate"] >= 0.50
s1_binom = H["binomial_p_vs_0.10"] < 0.05
s1_mcnemar = mcnemar_hier_vs_exact["p"] < 0.05
s1_orth = H["orthogonal"]["correct_rate"] is not None and H["orthogonal"]["correct_rate"] >= 0.50
s1_mixed_diag = H["mixed"]["correct_rate"] is not None and H["mixed"]["correct_rate"] >= 0.40
s1_held_diag = H["heldout9"]["correct_rate"] is not None and H["heldout9"]["correct_rate"] >= 0.50
S1_pass = s1_pooled_ge_50 and s1_binom and s1_mcnemar and s1_orth
S1_severe_fail = (H["correct_rate"] is not None and H["correct_rate"] < 0.40) or (not s1_binom) \
    or (not s1_mcnemar) or (H["orthogonal"]["correct_rate"] is not None and H["orthogonal"]["correct_rate"] < 0.40) \
    or ((H["mixed"]["correct_rate"] is not None and H["mixed"]["correct_rate"] < 0.30)
        and (H["correct_rate"] is not None and H["correct_rate"] < 0.50))

s2_fa_le_015 = H["false_accept_rate"] is not None and H["false_accept_rate"] <= 0.15
s2_below_verbatim = (alias_out[VERB]["false_accept_rate"] is not None and H["false_accept_rate"] is not None
                     and (alias_out[VERB]["false_accept_rate"] - H["false_accept_rate"]) >= 0.15)
s2_mcnemar = mcnemar_hier_vs_verbatim_fa["p"] < 0.05
S2_pass = s2_fa_le_015 and s2_below_verbatim and s2_mcnemar

S3_pass = (metrics[f"{HIER}::exact-match"]["correct_rate"] is not None
           and metrics[f"{HIER}::exact-match"]["correct_rate"] >= 0.90
           and not (pc_rows[EXACT]["correct_rate"] - pc_rows[HIER]["correct_rate"] > 0.10))

s4_prec = nc_detail[HIER]["gated_precision"] is not None and nc_detail[HIER]["gated_precision"] >= 0.85
s4_ece_val = ece_out[HIER]["overall"]
s4_ece = s4_ece_val is not None and s4_ece_val <= 0.15
s4_ece_boot_upper = ece_hier_boot["ci95"][1] <= 0.18
S4_pass = s4_prec and s4_ece and s4_ece_boot_upper

S5_pass = (H["correct_rate"] is not None and best_flat_rate is not None
           and (H["correct_rate"] + 0.10) >= best_flat_rate
           and (best_flat_rate > 0.0 or H["correct_rate"] > 0.0))

S6_gain_ge_015 = coverage_gain["mean"] >= 0.15
S6_ci_lower_gt_005 = coverage_gain["ci95"][0] > 0.05
S6_p = coverage_gain["p_gain_le_0"] < 0.05
S6_density_gain = density_gain_bt["mean"] > 0.0
S6_density_p = density_gain_bt["p_gain_le_0"] < 0.05
S6_pass = S6_gain_ge_015 and S6_ci_lower_gt_005 and S6_p and S6_density_gain and S6_density_p

if not controls_pass:
    status = "MEASUREMENT_INVALID"
    outcome = "NOT_APPLICABLE"
    outcome_reason = "controls (PC/NC) failed -> MEASUREMENT_INVALID per frozen decision rule"
elif S1_severe_fail:
    status = "COMPLETE"
    outcome = "FALSIFIES"
    outcome_reason = "FALSIFIED-IN-SETTING: S1 fails (pooled<0.40 or binomial p>=0.05 or McNemar p>=0.05 or orthogonal<0.40) per frozen rule"
elif not S2_pass:
    status = "COMPLETE"
    outcome = "FALSIFIES"
    outcome_reason = "FALSIFIED-IN-SETTING: S2 fails (false_accept>0.15 or not >=0.15 below verbatim or McNemar p>=0.05) per frozen rule"
elif not S5_pass:
    status = "COMPLETE"
    outcome = "FALSIFIES"
    outcome_reason = "FALSIFIED-IN-SETTING: S5 fails (hierarchical dominated by best flat retrieval by >0.10) per frozen rule"
elif S1_pass and S2_pass and S3_pass and S4_pass and S5_pass and S6_pass:
    status = "COMPLETE"
    outcome = "SUPPORTS"
    outcome_reason = "SURVIVES_CURRENT_TEST: S1-S6 all pass (hierarchical complementarity coverage gain >=0.15 + density gain with bootstrap p<0.05)"
elif S1_pass and S2_pass and S3_pass and S4_pass and S5_pass and not S6_pass:
    status = "COMPLETE"
    outcome = "MIXED"
    outcome_reason = ("MIXED: S1-S5 pass (hierarchical resolution does not regress and is not dominated) but S6 COMPLEMENTARITY "
                      "fails (coverage gain <0.15 / bootstrap p>=0.05 / density gain not significant) -> complementarity not demonstrated")
else:
    status = "COMPLETE"
    outcome = "MIXED"
    outcome_reason = "MIXED: partial S-gate pass (see decision_components)"

decision_components = {
    "controls_pass": bool(controls_pass),
    "S1_pooled_ge_0.50": bool(s1_pooled_ge_50),
    "S1_binom_p_lt_0.05": bool(s1_binom),
    "S1_mcnemar_p_lt_0.05": bool(s1_mcnemar),
    "S1_orth_ge_0.50": bool(s1_orth),
    "S1_mixed_ge_0.40_diag": bool(s1_mixed_diag),
    "S1_heldout9_ge_0.50_diag": bool(s1_held_diag),
    "S1_pass": bool(S1_pass),
    "S1_severe_fail": bool(S1_severe_fail),
    "S2_fa_le_0.15": bool(s2_fa_le_015),
    "S2_below_verbatim_ge_0.15": bool(s2_below_verbatim),
    "S2_mcnemar_p_lt_0.05": bool(s2_mcnemar),
    "S2_pass": bool(S2_pass),
    "S3_exact_ge_0.90_no_regression": bool(S3_pass),
    "S4_precision_ge_0.85": bool(s4_prec),
    "S4_ece_le_0.15": bool(s4_ece),
    "S4_ece_boot_upper_le_0.18": bool(s4_ece_boot_upper),
    "S4_pass": bool(S4_pass),
    "S5_not_dominated": bool(S5_pass),
    "S5_best_flat_name": best_flat_name,
    "S5_best_flat_correct_rate": best_flat_rate,
    "S6_gain_ge_0.15": bool(S6_gain_ge_015),
    "S6_boot_ci_lower_gt_0.05": bool(S6_ci_lower_gt_005),
    "S6_boot_p_lt_0.05": bool(S6_p),
    "S6_density_gain_gt_0": bool(S6_density_gain),
    "S6_density_p_lt_0.05": bool(S6_density_p),
    "S6_pass": bool(S6_pass),
}

# -------------------------------------------------- economics summary
econ = {}
for m in PIPELINES:
    alias_sub = rows(m, "alias-OOD")
    n_corr = sum(1 for r in alias_sub if r["is_correct"])
    c = CNT[m]
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
    }

derived_metrics = {
    "experiment_id": EXP_ID,
    "pipelines": PIPELINES,
    "strata_rates": {f"{m}::{s}": metrics[f"{m}::{s}"] for m in PIPELINES for s in STRATA},
    "alias_ood": alias_out,
    "mcnemar": {
        "hier_vs_exact_correct": mcnemar_hier_vs_exact,
        "hier_vs_verbatim_false_accept": mcnemar_hier_vs_verbatim_fa,
        "hier_vs_best_flat_correct": mcnemar_hier_vs_best_flat,
        "embed_k1_fa_vs_hier": mcnemar_flat_k1_fa_vs_hier,
        "best_flat_name": best_flat_name,
    },
    "ece": ece_out,
    "ece_hierarchical_bootstrap_family_blocked_2000": ece_hier_boot,
    "retrieval": retrieval_out,
    "coverage_gain_hier_minus_best_flat": {
        "gain_point": float((retrieval_out[HIER]["coverage"] or 0.0) - (retrieval_out[best_flat_name]["coverage"] or 0.0)),
        "bootstrap_2000_family_blocked": coverage_gain,
    },
    "density_gain_hier_minus_best_flat": {
        "gain_point": float((retrieval_out[HIER]["density"] or 0.0) - (retrieval_out[best_flat_name]["density"] or 0.0)),
        "bootstrap_2000_family_blocked": density_gain_bt,
    },
    "hierarchical_adaptive_k": {
        "alias_ood_k_values": hier_k, "histogram": k_hist, "mean_k": float(np.mean(hier_k)),
        "median_k": float(np.median(hier_k)), "k_cap_reason_counts": k_cap_counts,
        "final_entropy_mean": float(np.nanmean([e for e in hier_entropy_final if e is not None])) if any(e is not None for e in hier_entropy_final) else None,
        "final_coverage_mean": float(np.mean([c for c in hier_cov_final if c is not None])) if any(c is not None for c in hier_cov_final) else None,
        "theme_type_selection_counts": theme_type_counts,
    },
    "confidence": conf_out,
    "controls": {
        "PC_EXACT_MATCH": PC_EXACT_MATCH,
        "PC_RETRIEVAL_HEALTH": PC_RETRIEVAL_HEALTH,
        "PC_HIERARCHICAL_INDEX_BUILT": PC_HIERARCHICAL_INDEX_BUILT,
        "NC_NO_APPLICABLE": NC_NO_APPLICABLE,
        "NC_EMPTY_REGISTRY": NC_EMPTY_REGISTRY,
        "NC_ORACLE_LEAK": NC_ORACLE_LEAK,
        "NC_FLAT_COLLAPSE_DIAGNOSTIC": NC_FLAT_COLLAPSE,
        "controls_pass": bool(controls_pass),
    },
    "decision_components": decision_components,
    "overall": {
        "status": status, "outcome": outcome, "outcome_reason": outcome_reason,
        "bounded_to": "synthetic orthogonal header/body/auth + mixed alias-OOD (40 pooled = 30 orth + 10 mixed, 9 held-out) with minimal derived dict; no BrowserGym (Director: no new SPAs); not VALIDATED/PRODUCT_CORE without live-browser + economics replication",
    },
    "harness_errors": harness_errors,
    "sample_counts": {s: len([t for t in tasks if t["stratum"] == s]) for s in STRATA},
    "fixture_sha256": FROZEN_FIXTURE_SHA256,
    "fixture_identical_to_parent": True,
    "embed_available": EMBED_AVAILABLE,
    "embed_message": EMBED_MSG,
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "sklearn": __import__("sklearn").__version__,
        "seed": SEED,
    },
}

with open(OUT_DIR / "raw_evidence.json", "w") as f:
    json.dump(to_native(raw_evidence), f, indent=2)
with open(OUT_DIR / "derived_metrics.json", "w") as f:
    json.dump(to_native(derived_metrics), f, indent=2)

print("=" * 120)
print(f"STATUS {status} OUTCOME {outcome}")
print(f"controls_pass={controls_pass}")
print(f"S1 {S1_pass} (severe_fail {S1_severe_fail}) S2 {S2_pass} S3 {S3_pass} S4 {S4_pass} S5 {S5_pass} S6 {S6_pass}")
print(f"hier alias pooled {H['correct_rate']} ({H['correct']}/{H['n']}) FA {H['false_accept_rate']} binom_p {H['binomial_p_vs_0.10']:.2e}")
print(f"hier orth {H['orthogonal']['correct_rate']} mixed {H['mixed']['correct_rate']} heldout9 {H['heldout9']['correct_rate']} per_family {H['per_family']}")
for m in PIPELINES:
    a = alias_out[m]
    print(f"  {m:24s} correct {a['correct_rate']} FA {a['false_accept_rate']} unknown {a['unknown_rate']} coverage {retrieval_out[m]['coverage']} density {retrieval_out[m]['density']} mean_k {retrieval_out[m]['mean_k']}")
print(f"best flat = {best_flat_name} rate {best_flat_rate}")
print(f"mcnemar hier_vs_exact {mcnemar_hier_vs_exact['p']:.2e} hier_vs_verbatim_fa {mcnemar_hier_vs_verbatim_fa['p']:.2e} hier_vs_best_flat {mcnemar_hier_vs_best_flat['p']:.2e}")
print(f"coverage_gain {coverage_gain}")
print(f"density_gain {density_gain_bt}")
print(f"ECE hier overall {ece_out[HIER]['overall']} boot {ece_hier_boot} | conf_std {hier_conf_std}")
print(f"themes {n_themes} (types {sorted(set(t['type'] for t in themes))}) manifest {manifest_hash[:16]}...")
print(f"k_hist {k_hist} k_cap {k_cap_counts}")
print(f"harness_errors {len(harness_errors)}")
print(f"fixture_sha {FROZEN_FIXTURE_SHA256[:16]}... embed_available {EMBED_AVAILABLE}")
print(f"econ latency_per_success: " + json.dumps({m: econ[m]['latency_per_successful_alias_task_s'] for m in PIPELINES}))
print("=" * 120)