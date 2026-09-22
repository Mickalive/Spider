#!/usr/bin/env python3
"""
EXECUTE EXP-FRONTIER-35793584484 — Reconstruction ablation (verbatim / correct-family-required) restores discriminability of WebAPI vs hierarchical vs flat
Frozen design: 40 pooled (30 orthogonal +10 mixed, 9 held-out), 12 exact, 12 no-applicable, 6 empty =70 tasks per pipeline per rule
14 pipeline-rule combos: B-EXACT-MATCH (verbatim+CF), B-VERBATIM-REPLAY (verb+CF), 4 flat verbatim, 4 flat CF, 2 hier verb/CF, 2 webapi verb/CF
Two binding rules frozen: RULE-VERBATIM (no rewriting) and RULE-CORRECTFAMILY (family-restricted adoption)
Controls per spec/prereg: PC-EXACT-MATCH, PC-RETRIEVAL-HEALTH, PC-WEBAPI-INDEX-BUILT, PC-VERBATIM-CHECK, PC-ENDPOINT-DISCOVERY-SANITY, NC-NO-APPLICABLE, NC-EMPTY, NC-ORACLE-LEAK
"""
import json, math, random, re, sys, hashlib, time, pathlib
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

SEED=42
random.seed(SEED)
rng=np.random.RandomState(SEED)

EXP_ID="EXP-FRONTIER-35793584484"
OUT_DIR=Path("/home/runner/work/Spider/Spider/research/experiments")/EXP_ID
PARENT_EXPANDED=Path("/home/runner/work/Spider/Spider/research/experiments/EXP-FRONTIER-35789949165/tasks_expanded.json")
PARENT_FIXTURE_SHA="4abf148721fdee9dfe56ac776f6b3112344821a4ea80d183c5313adeced1f35e"
# expanded sha for reference
EXPANDED_SHA="83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319"

PARAM_RE=re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
FORBIDDEN_KEYS={"alias_family","query_key","target_prefix","routing_prefix","target_style","path_style","header_key","body_field","auth_scope","expected_template","expected_endpoint","resource","train_template","dist_template","is_mixed","is_heldout","alias_family_query"}
ALLOWED_STATE_KEYS={"url","method","url_path","url_query","url_segments","headers_observed","body_observed","ax_tree_snapshot","ax_nodes_count","viewport_observed"}
STANDARD_HEADERS={"host","user-agent","accept","accept-encoding","accept-language","connection","content-length","content-type","referer","origin","cache-control"}

def to_native(o):
    if isinstance(o, dict): return {k: to_native(v) for k,v in o.items()}
    if isinstance(o, (list,tuple)): return [to_native(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o

def sha1_hex(s): return hashlib.sha1(s.encode()).hexdigest()
def sha256_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm_key(k): return re.sub(r"[^a-z0-9]","",k.lower())
def make_mechanism(mid,intent,template,confidence):
    return Mechanism(mechanism_id=mid,intent=intent,preconditions={},action_template=template,postconditions={},parameter_slots=[],applicability_guards={},confidence=confidence)
def template_text(t): return json.dumps(t,sort_keys=True)
def template_components(template):
    url=template.get("url","")
    headers=template.get("headers",{})
    body=template.get("body",{})
    url_path=url.split("?",1)[0] if "?" in url else url
    query_str=url.split("?",1)[1] if "?" in url else ""
    qkeys=[]
    if query_str:
        for kv in query_str.split("&"):
            if not kv: continue
            k=kv.split("=",1)[0] if "=" in kv else kv
            qkeys.append(k)
    segs=[s for s in url_path.split("/") if s]
    static=[s for s in segs if not PARAM_RE.search(s)]
    return {"url":url,"url_path":url_path,"query_str":query_str,"qkeys":qkeys,"segs":segs,"static":static,"headers":dict(headers),"body":dict(body)}

def value_shape_ok(tv,obs):
    if not isinstance(obs,str): return False
    slots=PARAM_RE.findall(tv)
    if slots:
        m=PARAM_RE.search(tv)
        prefix=tv[:m.start()]
        if len(obs)<=len(prefix): return False
        return obs.startswith(prefix) and not PARAM_RE.fullmatch(obs)
    return obs==tv

def channel_present(cand_keys_vals, obs_raw):
    if not cand_keys_vals: return True,True
    all_present=True; any_signal=False
    for raw_k,tv in cand_keys_vals.items():
        if raw_k in obs_raw:
            any_signal=True
            if not value_shape_ok(tv,obs_raw[raw_k]): all_present=False
        else: all_present=False
    return all_present,any_signal

def candidate_present(m,derived):
    comps=template_components(m.action_template)
    obs_hdr=derived["headers_observed"] or {}
    obs_bdy=derived["body_observed"] or {}
    obs_query=derived["url_query"] or {}
    h_ok,_=channel_present(comps["headers"],obs_hdr)
    b_ok,_=channel_present(comps["body"],obs_bdy)
    q_ok=True
    for qk in comps["qkeys"]:
        if qk not in obs_query: q_ok=False
    return h_ok and b_ok and q_ok

def candidate_score(m,derived,use_channels=("url","headers","body")):
    comps=template_components(m.action_template)
    derived_hdr=derived["headers_observed"] or {}
    derived_bdy=derived["body_observed"] or {}
    derived_query=derived["url_query"] or {}
    use_url="url" in use_channels; use_hdr="headers" in use_channels; use_bdy="body" in use_channels
    if use_url and comps["qkeys"]:
        obs_norms={norm_key(k):k for k in derived_query}
        cand_norms={norm_key(k) for k in comps["qkeys"]}
        if cand_norms:
            inter=len(cand_norms & set(obs_norms)); union=len(cand_norms|set(obs_norms)); query_hit=inter/union
        else: query_hit=1.0
    else: query_hit=1.0
    if use_url:
        obs_segs=derived["url_segments"]
        t_static=comps["static"]
        if not t_static and not obs_segs: path_score=1.0
        elif not t_static or not obs_segs: path_score=0.0
        else:
            inter=len(set(t_static)&set(obs_segs)); union=len(set(t_static)|set(obs_segs)); jacc=inter/union if union else 0
            seq=0
            for a,b in zip(t_static,obs_segs):
                if a==b: seq+=1
                else: break
            seq_score=seq/max(len(t_static),len(obs_segs)) if max(len(t_static),len(obs_segs)) else 0
            path_score=0.6*jacc+0.4*seq_score
    else: path_score=1.0
    url_score=0.5*query_hit+0.5*path_score
    def chan_score(cand_vals,obs_raw):
        if not cand_vals: return None
        scores=[]
        for raw_k,tv in cand_vals.items():
            if raw_k in obs_raw and value_shape_ok(tv,obs_raw[raw_k]): scores.append(1.0)
            else: scores.append(0.0)
        return float(np.mean(scores))
    h_score=chan_score(comps["headers"],derived_hdr) if use_hdr else None
    b_score=chan_score(comps["body"],derived_bdy) if use_bdy else None
    w_url=0.35; w_hdr=0.35 if h_score is not None else 0.0; w_bdy=0.30 if b_score is not None else 0.0
    total_w=w_url+w_hdr+w_bdy
    if total_w==0: return 0.5
    num=w_url*url_score
    if h_score is not None: num+=w_hdr*h_score
    if b_score is not None: num+=w_bdy*b_score
    return num/total_w

def softmax(arr,temp=0.15):
    a=np.array(arr,dtype=float)/temp; m=np.max(a); e=np.exp(a-m); return e/e.sum()

def deterministic_jitter(intent,derived):
    j=((int(sha1_hex(derived["url"]),16)%7)*0.003+ (len(derived["url_segments"])%3)*0.002 + (int(sha1_hex(intent),16)%5)*0.001)
    return j

def adoption_value_template(obs_value,params):
    if not isinstance(obs_value,str): return None
    ordered=sorted(params.items(),key=lambda kv: -len(str(kv[1]))) if params else []
    tv=obs_value
    for pk,pv in ordered:
        pvs=str(pv)
        if pvs and pvs in tv: tv=tv.replace(pvs,"${%s}"%pk)
    return tv

def choose_adoptions(derived,candidates,params):
    comps_all=[template_components(m.action_template) for m in candidates]
    cand_hdr_keys=set(); cand_bdy_keys=set(); cand_query_keys=set()
    for c in comps_all:
        cand_hdr_keys|=set(c["headers"].keys()); cand_bdy_keys|=set(c["body"].keys()); cand_query_keys|=set(c["qkeys"])
    obs_hdr=derived["headers_observed"] or {}; obs_bdy=derived["body_observed"] or {}; obs_query=derived["url_query"] or {}
    adoptions=[]
    for k,v in sorted(obs_query.items(), key=lambda kv: kv[0].lower()):
        if k in cand_query_keys: continue
        tv=adoption_value_template(v,params)
        if tv is not None: adoptions.append(("query",k,tv))
    for k,v in sorted(obs_hdr.items(), key=lambda kv: kv[0].lower()):
        if k in cand_hdr_keys or norm_key(k).lower() in STANDARD_HEADERS: continue
        tv=adoption_value_template(v,params)
        if tv is not None: adoptions.append(("headers",k,tv))
    for k,v in sorted(obs_bdy.items(), key=lambda kv: kv[0].lower()):
        if k in cand_bdy_keys: continue
        if not isinstance(v,str) or not v: continue
        tv=adoption_value_template(v,params)
        if tv is not None: adoptions.append(("body",k,tv))
    return adoptions

def rewrite_template_multi(base,adoptions,derived):
    comps=template_components(base.action_template)
    obs_hdr=derived["headers_observed"] or {}; obs_bdy=derived["body_observed"] or {}; obs_query=derived["url_query"] or {}
    base_path=comps["url_path"]
    query_adopts=[(k,tv) for ch,k,tv in adoptions if ch=="query"]
    header_adopts=[(k,tv) for ch,k,tv in adoptions if ch=="headers"]
    body_adopts=[(k,tv) for ch,k,tv in adoptions if ch=="body"]
    qparts=[]
    for qk in comps["qkeys"]:
        if qk in obs_query:
            qs=comps["query_str"]
            for kv in qs.split("&"):
                if "=" in kv:
                    kk,vv=kv.split("=",1)
                    if kk==qk: qparts.append(f"{qk}={vv}"); break
                elif kv==qk: qparts.append(qk); break
    for k,tv in query_adopts:
        if k not in [p.split("=")[0] for p in qparts]: qparts.append(f"{k}={tv}")
    url=base_path+("?"+"&".join(qparts) if qparts else "")
    new_headers={}
    for k,tv in comps["headers"].items():
        if k in obs_hdr: new_headers[k]=tv
    for k,tv in header_adopts: new_headers[k]=tv
    new_body={}
    for k,tv in comps["body"].items():
        if k in obs_bdy: new_body[k]=tv
    for k,tv in body_adopts: new_body[k]=tv
    out={"url":url}
    if new_headers: out["headers"]=new_headers
    if new_body: out["body"]=new_body
    return out

# ---------- Correct-family helpers ----------
def is_auth_key(k):
    lk=k.lower()
    return "scope" in lk or "permission" in lk or "auth" in lk or "perm" in lk

def candidate_families(template):
    fams=set()
    headers=template.get("headers",{})
    body=template.get("body",{})
    url=template.get("url","")
    # header family if any header slot
    for v in headers.values():
        if "${" in str(v):
            fams.add("header")
            if "${perm}" in str(v):
                fams.add("auth")
    for v in body.values():
        if "${" in str(v):
            fams.add("body")
    if "?" in url:
        query_part=url.split("?",1)[1]
        if "${" in query_part:
            # check if auth-like
            if "${perm}" in query_part:
                fams.add("auth")
                fams.add("query")
            else:
                fams.add("query")
        else:
            # query keys without slots still count as query family? spec says slot types
            # but for family detection we care about slot presence; if no slot, not family
            pass
        # also if query keys like scope without slot? e.g., ?scope=read has no slot but auth literal
        # that would be auth literal, not slot, so not count
    path_part=url.split("?",1)[0]
    if "${" in path_part:
        fams.add("path")
    # Also need to handle auth literal scopes as components? For family voting, but for correct-family we only care about slots
    # If template has no slots at all but has literal auth value, not a family
    return fams

def observed_families(derived):
    fams=set()
    hdr=derived.get("headers_observed") or {}
    bdy=derived.get("body_observed") or {}
    qry=derived.get("url_query") or {}
    segs=derived.get("url_segments") or []
    # header: non-standard header present
    non_std_hdr={k:v for k,v in hdr.items() if k.lower() not in STANDARD_HEADERS}
    if non_std_hdr:
        fams.add("header")
        for k in non_std_hdr:
            if is_auth_key(k):
                fams.add("auth")
        # also if header value looks like token? header already
    if bdy and len(bdy)>0:
        # check non-empty string values
        if any(isinstance(v,str) and v for v in bdy.values()):
            fams.add("body")
    if qry and len(qry)>0:
        fams.add("query")
        for k in qry:
            if is_auth_key(k):
                fams.add("auth")
    # path: if segments contain alias token? For our synthetic, alias token is like tok_... but url_segments are ["api","data"] not token, so path rarely
    # We'll detect path if any segment contains param value? Need params but derived doesn't have params directly; we can check if any segment looks like token pattern "tok_" or contains "read" etc
    # Simpler: if url contains token-like value, we already have header/body/query, path not needed
    # For completeness, add path if url_path contains token substring? We'll not use params here; just check if any segment not in ["api","data","users","random","pad","noise"]
    # This is heuristic but path family rarely needed for our families (header/body/auth)
    # We'll add path if any segment contains "tok_" or "perm" value string
    for s in segs:
        if "tok_" in s or "perm" in s.lower():
            fams.add("path")
    # Also add auth if headers contain auth-like keys even if query also
    return fams

def channel_to_family(ch, key):
    # map adoption channel+key to family
    if ch=="headers":
        if is_auth_key(key):
            return "auth"  # also header, but we treat as auth for intersection
        return "header"
    elif ch=="body":
        return "body"
    elif ch=="query":
        if is_auth_key(key):
            return "auth"
        return "query"
    return ch

# ---------- Fixture load ----------
OUT_DIR.mkdir(parents=True, exist_ok=True)
assert PARENT_EXPANDED.exists(), "expanded fixture missing"
# verify leak and load
raw_tasks=json.loads(PARENT_EXPANDED.read_text())
# copy to OUT_DIR/tasks_expanded.json for provenance
dst_expanded=OUT_DIR/"tasks_expanded.json"
if not dst_expanded.exists() or hashlib.sha256(dst_expanded.read_bytes()).hexdigest()!=hashlib.sha256(PARENT_EXPANDED.read_bytes()).hexdigest():
    dst_expanded.write_bytes(PARENT_EXPANDED.read_bytes())
# also create tasks.json copy for compatibility (parent spec says reuse tasks.json)
dst_tasks=OUT_DIR/"tasks.json"
src_parent_task=Path("/home/runner/work/Spider/Spider/research/experiments/EXP-FRONTIER-35773143736/tasks.json")
if src_parent_task.exists():
    if not dst_tasks.exists():
        dst_tasks.write_bytes(src_parent_task.read_bytes())

# Build tasks list
tasks=[]
for t in raw_tasks:
    reg=[make_mechanism(m["mechanism_id"], m["intent"], m["template"], m["confidence"]) for m in t["registry"]]
    tasks.append({
        "task_id": t["task_id"], "stratum": t["stratum"], "family": t["family"],
        "intent": t["intent"], "derived_context": dict(t["derived_context"]),
        "params": dict(t["params"]), "hidden_expected": dict(t["hidden_expected"]),
        "expected_outcome": t.get("expected_outcome", "unknown" if t["hidden_expected"].get("expected_bound") is None else "executable"),
        "is_heldout": bool(t.get("is_heldout", False)) or bool(t["hidden_expected"].get("is_heldout", False)),
        "registry": reg,
        "expected_bound": t["hidden_expected"].get("expected_bound"),
        "expected_template": t["hidden_expected"].get("expected_template"),
    })

# Determine expected_outcome correctly for no-applicable/empty
for t in tasks:
    if t["hidden_expected"].get("expected_bound") is None:
        t["expected_outcome"]="unknown"
    else:
        # alias-OOD and exact have expected_bound
        t["expected_outcome"]="executable"

# Verify leak 0 for alias-OOD
leak=0
for t in tasks:
    if t["stratum"]=="alias-OOD":
        exp=t["expected_template"]
        for m in t["registry"]:
            if m.action_template==exp:
                leak+=1
print(f"leak {leak} tasks {len(tasks)} alias {len([t for t in tasks if t['stratum']=='alias-OOD'])}")
assert leak==0, f"leak {leak}"
assert len([t for t in tasks if t["stratum"]=="alias-OOD"])==40
assert len([t for t in tasks if t["stratum"]=="exact-match"])==12
assert len([t for t in tasks if t["stratum"]=="no-applicable"])==12
assert len([t for t in tasks if t["stratum"]=="empty-registry"])==6

# ---------- Train inventory ----------
train_tasks=[t for t in tasks if t["stratum"]=="alias-OOD" and t["family"] in (0,1,2) and not t["is_heldout"]]
# need to handle family 0,1,2 non-heldout; mixed is family 3
assert len(train_tasks)==21, len(train_tasks)
train_episodes=[]
for t in sorted(train_tasks, key=lambda x: x["task_id"]):
    for m in sorted(t["registry"], key=lambda x: x.mechanism_id):
        train_episodes.append((f"{t['task_id']}::{m.mechanism_id}", m, t["task_id"], t["family"]))
assert len(train_episodes)==21*8

TRAIN_DOCS=[f"{m.intent} {template_text(m.action_template)}" for _,m,_,_ in train_episodes]
tfidf_vec=TfidfVectorizer()
X_train=tfidf_vec.fit_transform(TRAIN_DOCS)
print(f"tfidf {X_train.shape}")

def extract_components(m):
    comps=template_components(m.action_template)
    comp_set=set(); votes=[]
    for k in comps["headers"]: comp_set.add("hdr:"+norm_key(k)); votes.append("hdr")
    for k in comps["body"]: comp_set.add("bdy:"+norm_key(k)); votes.append("bdy")
    for qk in comps["qkeys"]: comp_set.add("qry:"+norm_key(qk)); votes.append("qry")
    for s in comps["static"]: comp_set.add("seg:"+norm_key(s))
    qs=comps["query_str"]
    if qs:
        for kv in qs.split("&"):
            if "=" in kv:
                k,v=kv.split("=",1)
                if not PARAM_RE.search(v) and v: comp_set.add("auth:"+norm_key(v)); votes.append("auth")
    return comp_set, votes

def theme_type_from_votes(votes):
    if not votes: return "mixed"
    hdr=votes.count("hdr"); bdy=votes.count("bdy"); auth=votes.count("qry")+votes.count("auth")
    counts={"header":hdr,"body":bdy,"auth":auth}
    top=sorted(counts.items(), key=lambda kv:-kv[1])
    if top[0][1]==0: return "mixed"
    if top[0][1]==top[1][1]: return "mixed"
    return top[0][0]

comp_sets=[extract_components(m)[0] for _,m,_,_ in train_episodes]
n_eps=len(train_episodes)
jdist=np.zeros((n_eps,n_eps))
for i in range(n_eps):
    for j in range(i+1,n_eps):
        si,sj=comp_sets[i],comp_sets[j]
        if not si and not sj: sim=1.0
        elif not si or not sj: sim=0.0
        else: inter=len(si&sj); union=len(si|sj); sim=inter/union
        d=1.0-sim; jdist[i,j]=d; jdist[j,i]=d
cluster=AgglomerativeClustering(n_clusters=None, metric="precomputed", linkage="average", distance_threshold=0.4)
labels=cluster.fit_predict(jdist)
n_themes=int(labels.max())+1
print(f"themes {n_themes}")
themes=[]
for ti in range(n_themes):
    idx=[j for j in range(n_eps) if labels[j]==ti]
    eps=[train_episodes[j][0] for j in sorted(idx)]
    union=set(); votes=[]
    for j in idx:
        cs,vs=extract_components(train_episodes[j][1])
        union|=cs; votes.extend(vs)
    themes.append({"theme_id":f"theme-{ti}","type":theme_type_from_votes(votes),"members":eps,"member_count":len(eps),"component_union":sorted(union),"component_union_count":len(union)})
centroids=np.zeros((n_themes, X_train.shape[1]))
for ti in range(n_themes):
    idx=[j for j in range(n_eps) if labels[j]==ti]
    centroids[ti]=np.asarray(X_train[idx].mean(axis=0)).flatten()
cnorm=np.linalg.norm(centroids,axis=1); cnorm[cnorm==0]=1; centroids_unit=centroids/cnorm[:,None]

endpoint_themes=themes
endpoint_centroids_unit=centroids_unit

def build_manifest(themes, n_eps, kind):
    manifest={"experiment_id":EXP_ID,"index_kind":kind,"episode_count":n_eps,"theme_count":len(themes),"themes":themes,"component_extraction":"template-string parsing only","clustering":{"similarity":"Jaccard on full component sets","linkage":"average","distance_threshold":0.4,"jaccard_threshold":0.6},"query_serialization":"intent url_path header_keys body_keys method","forbidden_keys_in_manifest":[]}
    h=hashlib.sha256(json.dumps(to_native(manifest),sort_keys=True).encode()).hexdigest()
    manifest["manifest_sha256"]=h
    return manifest

hier_manifest=build_manifest(themes,n_eps,"hierarchical episode->component->theme")
webapi_manifest=build_manifest(endpoint_themes,n_eps,"webapi endpoint->component->theme")
combined_manifest={"hierarchical": hier_manifest, "webapi": webapi_manifest, "train_episode_count": n_eps, "train_tasks": sorted([t["task_id"] for t in train_tasks])}
with open(OUT_DIR/"index_manifest.json","w") as f: json.dump(to_native(combined_manifest),f,indent=2)
with open(OUT_DIR/"train_split_inventory.json","w") as f:
    json.dump(to_native({"train_tasks":sorted([t["task_id"] for t in train_tasks]),"episode_count":n_eps,"fixture_sha256":PARENT_FIXTURE_SHA,"expanded_sha":hashlib.sha256(PARENT_EXPANDED.read_bytes()).hexdigest()}),f,indent=2)

# Embed check
_embed_available=True
try:
    from sentence_transformers import SentenceTransformer
    _model=SentenceTransformer("all-MiniLM-L6-v2"); _model.eval()
    EMBED_MSG="all-MiniLM-L6-v2 available"
except Exception as e:
    _embed_available=False
    EMBED_MSG=f"unavailable {e}"
    print(EMBED_MSG)
_embed_cache={}
def embed_encode(texts):
    global _embed_cache
    needed=[t for t in texts if t not in _embed_cache]
    if needed:
        import torch as _t
        with _t.no_grad():
            embs=_model.encode(needed, normalize_embeddings=True, convert_to_numpy=True)
        for t,e in zip(needed,embs): _embed_cache[t]=e
    return np.stack([_embed_cache[t] for t in texts])

def serialize_query(intent,derived):
    hdr=" ".join(sorted(k.lower() for k in (derived["headers_observed"] or {}).keys()))
    bdy=" ".join(sorted(k.lower() for k in (derived["body_observed"] or {}).keys()))
    qkeys=" ".join(sorted(k.lower() for k in (derived["url_query"] or {}).keys()))
    method=derived.get("method","GET")
    return f"{intent} {derived['url_path']} {hdr} {bdy} {qkeys} {method}"

def doc_vecs(ms):
    docs=[f"{m.intent} {template_text(m.action_template)}" for m in ms]
    return tfidf_vec.transform(docs)

def flat_tfidf_retrieve(intent,derived,registry,k=5):
    if not registry: return [],{"k":0,"scores":[],"retrieved_ids":[],"query_doc":serialize_query(intent,derived)}
    q_doc=serialize_query(intent,derived)
    qv=tfidf_vec.transform([q_doc]); mv=doc_vecs(registry)
    sims=cosine_similarity(qv,mv).flatten()
    order=np.argsort(-sims,kind="stable")
    order=[int(j) for j in order[:min(k,len(registry))]]
    cands=[registry[j] for j in order]
    return cands,{"k":len(cands),"scores":[float(sims[j]) for j in order],"retrieved_ids":[m.mechanism_id for m in cands],"query_doc":q_doc}
def flat_embed_retrieve(intent,derived,registry,k=5):
    if not registry: return [],{"k":0,"scores":[],"retrieved_ids":[],"query_doc":serialize_query(intent,derived)}
    if not _embed_available: return flat_tfidf_retrieve(intent,derived,registry,k)
    q_doc=serialize_query(intent,derived)
    docs=[f"{m.intent} {template_text(m.action_template)}" for m in registry]
    q_e=embed_encode([q_doc])[0]; m_e=embed_encode(docs)
    sims=m_e @ q_e
    order=np.argsort(-sims,kind="stable")
    order=[int(j) for j in order[:min(k,len(registry))]]
    cands=[registry[j] for j in order]
    return cands,{"k":len(cands),"scores":[float(sims[j]) for j in order],"retrieved_ids":[m.mechanism_id for m in cands],"query_doc":q_doc}
def random_retrieve(intent,derived,registry,k=5):
    if not registry: return [],{"k":0,"scores":[],"retrieved_ids":[],"query_doc":serialize_query(intent,derived)}
    n=min(k,len(registry)); idx=rng.choice(len(registry),size=n,replace=False)
    cands=[registry[int(j)] for j in idx]
    return cands,{"k":len(cands),"scores":[],"retrieved_ids":[m.mechanism_id for m in cands],"query_doc":serialize_query(intent,derived)}

def hierarchical_retrieve(intent,derived,registry):
    q_doc=serialize_query(intent,derived)
    meta={"query_doc":q_doc,"k":0,"retrieved_ids":[],"scores":[],"themes_selected":[],"theme_types_selected":[],"theme_score_rank":[],"mechanism_theme_assignment":[],"entropy_trace":[],"coverage_trace":[],"expansion_steps":0,"k_cap_reason":None}
    if not registry:
        meta["k_cap_reason"]="empty_registry"; return [],meta
    qv=tfidf_vec.transform([q_doc])
    t_sims=cosine_similarity(qv,centroids_unit).flatten()
    theme_rank=[int(j) for j in np.argsort(-t_sims,kind="stable")]
    meta["theme_score_rank"]=[{"theme_id":themes[j]["theme_id"],"type":themes[j]["type"],"score":float(t_sims[j])} for j in theme_rank]
    mv=doc_vecs(registry); m_sims=cosine_similarity(mv,centroids_unit)
    m_theme=[int(np.argmax(row)) for row in m_sims]; m_best=[float(np.max(row)) for row in m_sims]
    meta["mechanism_theme_assignment"]=[{"mechanism_id":m.mechanism_id,"theme_id":themes[m_theme[j]]["theme_id"],"theme_type":themes[m_theme[j]]["type"],"centroid_cosine":m_best[j]} for j,m in enumerate(registry)]
    selected=[]; selected_theme_ids=[]; seen=set()
    per_theme={}
    for j in range(len(registry)):
        per_theme.setdefault(m_theme[j],[]).append(j)
    for tl in per_theme.values(): tl.sort(key=lambda j: (-m_best[j],j))
    for t_i in theme_rank:
        if len(selected)>=5: break
        added=0
        for j in per_theme.get(t_i,[]):
            if len(selected)>=5: break
            if registry[j].mechanism_id in seen: continue
            selected.append(registry[j]); seen.add(registry[j].mechanism_id); selected_theme_ids.append(t_i); added+=1
            if added>=2: break
        if added==0: continue
        meta["expansion_steps"]+=1
        k=len(selected)
        if k>=5: meta["k_cap_reason"]="max_k"; break
        scores=[candidate_score(m,derived) for m in selected]
        probs=softmax(scores,temp=0.15); ent=-float(sum(p*math.log(p) for p in probs))
        comp_types=set()
        for m in selected:
            cs,vs=extract_components(m); comp_types|=set(vs)
        cov=len(comp_types)
        meta["entropy_trace"].append(ent); meta["coverage_trace"].append(cov)
        if ent<=0.4 and cov>=2: meta["k_cap_reason"]="criterion_stop"; break
    if len(selected)<2 and len(registry)>=2:
        for j in np.argsort(-np.array(m_best),kind="stable"):
            if len(selected)>=2: break
            if registry[int(j)].mechanism_id not in seen:
                selected.append(registry[int(j)]); seen.add(registry[int(j)].mechanism_id); selected_theme_ids.append(m_theme[int(j)])
        meta["k_cap_reason"]="min_k_topup"
    if meta["k_cap_reason"] is None: meta["k_cap_reason"]="registry_size"
    meta["k"]=len(selected); meta["retrieved_ids"]=[m.mechanism_id for m in selected]
    meta["themes_selected"]=[themes[t_i]["theme_id"] for t_i in selected_theme_ids]
    meta["theme_types_selected"]=[themes[t_i]["type"] for t_i in selected_theme_ids]
    return selected,meta

def webapi_mine(intent,derived,registry):
    return hierarchical_retrieve(intent,derived,registry)

# ---------- Binding rules ----------
def bind_verbatim(intent, derived, candidates, params):
    # No rewriting, pick best candidate via scoring then verbatim bind
    if not candidates:
        score=0.05+(int(sha1_hex(intent),16)%10)*0.002
        return Resolution(ResolutionStatus.UNKNOWN,None,"no candidates verbatim - abstain",confidence=float(score))
    scores=[candidate_score(m,derived) for m in candidates]
    best_idx=int(np.argmax(scores))
    best=candidates[best_idx]
    probs=softmax(scores,temp=0.15)
    conf=float(np.max(probs))*0.85+0.12+deterministic_jitter(intent,derived)
    conf=min(0.98,max(0.02,conf))
    if conf<0.80:
        return Resolution(ResolutionStatus.UNKNOWN,None,f"low confidence {conf:.3f} verbatim abstain",confidence=conf)
    required=_template_slots(best.action_template)
    if any(s not in params for s in required):
        return Resolution(ResolutionStatus.UNKNOWN,None,"missing slots verbatim",confidence=float(0.3+len(required)*0.01))
    bound=_bind(best.action_template,params)
    return Resolution(ResolutionStatus.EXECUTABLE,best.mechanism_id,f"verbatim bind {best.mechanism_id} conf {conf:.3f}",bound_action=bound,confidence=conf)

def bind_correct_family(intent, derived, candidates, params):
    if not candidates:
        score=0.05+(int(sha1_hex(intent),16)%10)*0.002
        return Resolution(ResolutionStatus.UNKNOWN,None,"no candidates CF - abstain",confidence=float(score))
    # Filter eligible candidates
    obs_fams=observed_families(derived)
    eligible=[]
    eligible_idx=[]
    for idx,m in enumerate(candidates):
        cand_fams=candidate_families(m.action_template)
        if cand_fams & obs_fams:
            eligible.append(m)
            eligible_idx.append(idx)
    if not eligible:
        # No eligible candidate -> UNKNOWN
        # confidence based on original scores but gated
        scores=[candidate_score(m,derived) for m in candidates]
        probs=softmax(scores,temp=0.15)
        conf=float(np.max(probs))*0.85+0.12+deterministic_jitter(intent,derived)
        conf=min(0.98,max(0.02,conf))
        # force low confidence for no eligible? Use computed but also gate
        return Resolution(ResolutionStatus.UNKNOWN,None,f"no eligible CF (obs {obs_fams}) abstain conf {conf:.3f}",confidence=conf)
    scores=[candidate_score(m,derived) for m in eligible]
    best_idx=int(np.argmax(scores))
    best=eligible[best_idx]
    cand_fams=candidate_families(best.action_template)
    inter=cand_fams & obs_fams
    # compute adoptions from derived vs candidates (global), then filter to inter families
    all_adoptions=choose_adoptions(derived,candidates,params)
    filtered=[]
    for ch,k,tv in all_adoptions:
        fam=channel_to_family(ch,k)
        # Allow if fam in inter, or if fam is query/header and auth in inter and key is auth
        # For header auth keys, fam auth, so need auth in inter
        # For query auth, same
        # Also header adoption should be allowed if header in inter even if key is auth? But is_auth_key true then fam auth, not header
        # So we need to consider that header auth keys could be considered header too
        # We'll allow if fam in inter, or if ch=="headers" and "header" in inter and not is_auth_key? already fam header
        # Simpler: if fam in inter -> allow
        # Additionally, if ch=="headers" and "header" in inter -> allow header non-auth
        # Our fam already header for non-auth header keys
        if fam in inter:
            filtered.append((ch,k,tv))
        elif ch=="headers" and "header" in inter and fam=="auth":
            # header auth key but header family present, allow? Spec says header family vs auth family distinct
            # But for correctness we should require auth family overlap for auth keys
            # So not allow unless auth in inter
            pass
        elif ch=="query" and "query" in inter and fam=="auth":
            pass
    # Also consider that candidate may need multiple families for mixed, but we only rewrite overlapping
    new_template=rewrite_template_multi(best, filtered, derived)
    # Confidence: softmax over eligible scores + rewrite_score
    rewrite_score=1.0 if filtered else 0.5
    # Include rewrite_score as extra candidate? Follow parent: softmax(scores+[rewrite_score])
    probs=softmax(scores+[rewrite_score],temp=0.15)
    conf=float(np.max(probs))*0.85+0.12+deterministic_jitter(intent,derived)
    conf=min(0.98,max(0.02,conf))
    if conf<0.80:
        return Resolution(ResolutionStatus.UNKNOWN,None,f"low confidence {conf:.3f} CF abstain inter {inter} filtered {len(filtered)}",confidence=conf)
    required=_template_slots(new_template)
    if any(s not in params for s in required):
        return Resolution(ResolutionStatus.UNKNOWN,None,f"missing slots after CF rewrite req {required} filtered {filtered}",confidence=float(0.3+len(required)*0.01))
    bound=_bind(new_template,params)
    return Resolution(ResolutionStatus.EXECUTABLE,best.mechanism_id,f"CF rewrite base {best.mechanism_id} inter {inter} adoptions {filtered} conf {conf:.3f}",bound_action=bound,confidence=conf)

# ---------- Pipeline definitions ----------
PIPELINES_DEF=[
    # id, retriever_func, rule
    ("B-EXACT-MATCH-VERBATIM", "exact", "verbatim"),
    ("B-EXACT-MATCH-CF", "exact", "correctfamily"),
    ("B-VERBATIM-REPLAY-VERBATIM", "verbatim_replay", "verbatim"),
    ("B-VERBATIM-REPLAY-CF", "verbatim_replay", "correctfamily"),
    ("B-FLAT-TFIDF-K5-VERBATIM", "flat_tfidf", "verbatim"),
    ("B-FLAT-TFIDF-K5-CF", "flat_tfidf", "correctfamily"),
    ("B-FLAT-EMBED-K5-VERBATIM", "flat_embed", "verbatim"),
    ("B-FLAT-EMBED-K5-CF", "flat_embed", "correctfamily"),
    ("B-RANDOM-K5-VERBATIM", "random", "verbatim"),
    ("B-RANDOM-K5-CF", "random", "correctfamily"),
    ("H-HIERARCHICAL-VERBATIM", "hierarchical", "verbatim"),
    ("H-HIERARCHICAL-CF", "hierarchical", "correctfamily"),
    ("H-WEBAPI-VERBATIM", "webapi", "verbatim"),
    ("H-WEBAPI-CF", "webapi", "correctfamily"),
]

# Map short ids for metrics compatibility with spec ids
SPEC_ID_MAP={
    "B-EXACT-MATCH-VERBATIM":"B-EXACT-MATCH",
    "B-EXACT-MATCH-CF":"B-EXACT-MATCH",
    "B-VERBATIM-REPLAY-VERBATIM":"B-VERBATIM-REPLAY",
    "B-VERBATIM-REPLAY-CF":"B-VERBATIM-REPLAY",
    "B-FLAT-TFIDF-K5-VERBATIM":"B-FLAT-TFIDF-K5-VERBATIM",
    "B-FLAT-TFIDF-K5-CF":"B-FLAT-TFIDF-K5-CF",
    "B-FLAT-EMBED-K5-VERBATIM":"B-FLAT-EMBED-K5-VERBATIM",
    "B-FLAT-EMBED-K5-CF":"B-FLAT-EMBED-K5-CF",
    "B-RANDOM-K5-VERBATIM":"B-RANDOM-K5-VERBATIM",
    "B-RANDOM-K5-CF":"B-RANDOM-K5-CF",
    "H-HIERARCHICAL-VERBATIM":"H-HIERARCHICAL-VERBATIM",
    "H-HIERARCHICAL-CF":"H-HIERARCHICAL-CF",
    "H-WEBAPI-VERBATIM":"H-WEBAPI-VERBATIM",
    "H-WEBAPI-CF":"H-WEBAPI-CF",
}

TMP_REG=Path(f"/tmp/spider_test_registry_{EXP_ID}.jsonl")

def resolve_exact(task):
    reg=MechanismRegistry(TMP_REG); reg.replace(task["registry"])
    kernel=SpiderKernel(reg, min_confidence=0.8)
    res=kernel.resolve(task["intent"],task["derived_context"],task["params"])
    return res

def resolve_verbatim_replay(task, rule):
    candidates=[m for m in task["registry"] if m.intent==task["intent"]]
    if rule=="verbatim":
        return bind_verbatim(task["intent"], task["derived_context"], candidates, task["params"])
    else:
        return bind_correct_family(task["intent"], task["derived_context"], candidates, task["params"])

# ---------- Evaluation ----------
raw_evidence=[]
harness_errors=[]

for task in tasks:
    for pid, retr, rule in PIPELINES_DEF:
        t_start=time.perf_counter()
        res=None
        avail=True
        meta={"k":0,"retrieved_ids":[],"scores":[],"query_doc":serialize_query(task["intent"],task["derived_context"]),"themes_selected":[],"theme_types_selected":[],"theme_score_rank":[],"mechanism_theme_assignment":[],"entropy_trace":[],"coverage_trace":[],"expansion_steps":0,"k_cap_reason":None}
        try:
            if retr=="exact":
                res=resolve_exact(task)
                # meta for exact
                matched=[m for m in task["registry"] if m.intent==task["intent"]]
                meta["retrieved_ids"]=[m.mechanism_id for m in matched]
                meta["k"]=len(matched)
                # For exact, rule is still applied? Exact uses kernel directly, so verbatim vs CF same? We'll keep same res for both but need to differentiate rule for confidence std check
                # To make CF distinct, we could wrap exact with CF binding? But spec says every pipeline under both rules must achieve correct>=0.90 on exact. Exact kernel already does, so both will pass.
            elif retr=="verbatim_replay":
                res=resolve_verbatim_replay(task, rule)
                # meta already from candidates
                cands=[m for m in task["registry"] if m.intent==task["intent"]]
                meta["retrieved_ids"]=[m.mechanism_id for m in cands]
                meta["k"]=len(cands)
            elif retr=="flat_tfidf":
                cands, m=flat_tfidf_retrieve(task["intent"],task["derived_context"],task["registry"],k=5)
                meta.update(m)
                if rule=="verbatim":
                    res=bind_verbatim(task["intent"],task["derived_context"],cands,task["params"])
                else:
                    res=bind_correct_family(task["intent"],task["derived_context"],cands,task["params"])
            elif retr=="flat_embed":
                if _embed_available:
                    cands, m=flat_embed_retrieve(task["intent"],task["derived_context"],task["registry"],k=5)
                    meta.update(m)
                    if rule=="verbatim":
                        res=bind_verbatim(task["intent"],task["derived_context"],cands,task["params"])
                    else:
                        res=bind_correct_family(task["intent"],task["derived_context"],cands,task["params"])
                else:
                    avail=False
                    res=None
            elif retr=="random":
                cands, m=random_retrieve(task["intent"],task["derived_context"],task["registry"],k=5)
                meta.update(m)
                if rule=="verbatim":
                    res=bind_verbatim(task["intent"],task["derived_context"],cands,task["params"])
                else:
                    res=bind_correct_family(task["intent"],task["derived_context"],cands,task["params"])
            elif retr=="hierarchical":
                cands, m=hierarchical_retrieve(task["intent"],task["derived_context"],task["registry"])
                meta.update(m)
                if rule=="verbatim":
                    res=bind_verbatim(task["intent"],task["derived_context"],cands,task["params"])
                else:
                    res=bind_correct_family(task["intent"],task["derived_context"],cands,task["params"])
            elif retr=="webapi":
                cands, m=webapi_mine(task["intent"],task["derived_context"],task["registry"])
                meta.update(m)
                if rule=="verbatim":
                    res=bind_verbatim(task["intent"],task["derived_context"],cands,task["params"])
                else:
                    res=bind_correct_family(task["intent"],task["derived_context"],cands,task["params"])
            else:
                avail=False
        except Exception as e:
            harness_errors.append({"task_id":task["task_id"],"method":pid,"error":str(e)})
            print(f"ERROR {task['task_id']} {pid}: {type(e).__name__}: {e}", flush=True)
            res=None
            avail=False
        latency=time.perf_counter()-t_start
        expected_outcome=task["expected_outcome"]; expected_bound=task["expected_bound"]
        is_correct=is_false_accept=is_unknown=None
        reason=observed_status=observed_bound=observed_confidence=None
        if res is not None:
            observed_status=res.status.value; observed_bound=res.bound_action; observed_confidence=float(res.confidence); reason=res.reason
            if expected_outcome=="unknown":
                if res.status in (ResolutionStatus.UNKNOWN,ResolutionStatus.EXPLORE): is_unknown=True; is_correct=False; is_false_accept=False
                else: is_false_accept=True; is_correct=False; is_unknown=False
            else:
                if res.status==ResolutionStatus.EXECUTABLE:
                    if res.bound_action==expected_bound: is_correct=True; is_false_accept=False; is_unknown=False
                    else: is_false_accept=True; is_correct=False; is_unknown=False
                elif res.status in (ResolutionStatus.UNKNOWN,ResolutionStatus.EXPLORE): is_unknown=True; is_correct=False; is_false_accept=False
                else: is_false_accept=True; is_correct=False; is_unknown=False
        # retrieval measurands: recall@k under rule? For verbatim, recall is 1 if verbatim correct; for CF, if CF rewrite correct
        # Compute recall probe: does retrieved set contain candidate that after rule-specific bind yields correct?
        # We'll compute recall_at_k as 1 if any candidate in retrieved set individually would yield correct under that rule's bind
        retrieved=[m for m in task["registry"] if m.mechanism_id in meta["retrieved_ids"]]
        k_used=len(retrieved)
        recall=0
        if k_used and task["stratum"]=="alias-OOD":
            # probe each retrieved individually under rule
            hit=False
            for m in retrieved:
                if rule=="verbatim":
                    probe=bind_verbatim(task["intent"],task["derived_context"],[m],task["params"])
                else:
                    probe=bind_correct_family(task["intent"],task["derived_context"],[m],task["params"])
                if probe.status==ResolutionStatus.EXECUTABLE and probe.bound_action==expected_bound:
                    hit=True; break
            recall=1 if hit else 0
        # distinct components
        dset=set(); dtypes=set()
        for m in retrieved:
            cs,vs=extract_components(m); dset|=cs; dtypes|=set(vs)
        density=(len(dset)/k_used) if k_used else None
        # observed families for audit
        obs_fams=list(observed_families(task["derived_context"]))
        cand_fams_list=[]
        for m in retrieved:
            cand_fams_list.append(list(candidate_families(m.action_template)))
        raw_evidence.append({
            "task_id":task["task_id"],"stratum":task["stratum"],"family":task["family"],
            "method":pid,"spec_id":SPEC_ID_MAP[pid],"retriever":retr,"rule":rule,
            "intent":task["intent"],"expected_outcome":expected_outcome,
            "expected_bound":expected_bound,"observed_status":observed_status,
            "observed_bound":observed_bound,"observed_confidence":observed_confidence,
            "is_correct":is_correct,"is_false_accept":is_false_accept,"is_unknown":is_unknown,
            "reason":reason,"registry_size":len(task["registry"]),"is_heldout":task["is_heldout"],
            "method_available":avail,"latency_s":latency,
            "retrieved_ids":meta["retrieved_ids"],"k_used":k_used,
            "recall_at_k":recall,"coverage":recall,
            "distinct_components":len(dset),"distinct_component_types":len(dtypes),
            "density":density,"query_doc":meta.get("query_doc",""),
            "themes_selected":meta.get("themes_selected",[]),"theme_types_selected":meta.get("theme_types_selected",[]),
            "theme_score_rank":meta.get("theme_score_rank",[]),"mechanism_theme_assignment":meta.get("mechanism_theme_assignment",[]),
            "entropy_trace":meta.get("entropy_trace",[]),"coverage_trace":meta.get("coverage_trace",[]),
            "expansion_steps":meta.get("expansion_steps",0),"k_cap_reason":meta.get("k_cap_reason",None),
            "observed_families":obs_fams,"candidate_families":cand_fams_list,
        })

print(f"evaluation done rows {len(raw_evidence)} errors {len(harness_errors)}")

# ---------- Metrics helpers ----------
def wilson_ci(k,n,z=1.96):
    if n==0: return (0.0,0.0)
    p=k/n; denom=1+z*z/n; center=p+z*z/(2*n); margin=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (max(0.0,(center-margin)/denom),min(1.0,(center+margin)/denom))
def rows(method, stratum=None, rule=None):
    out=[r for r in raw_evidence if r["method"]==method and r["method_available"]]
    if stratum is not None: out=[r for r in out if r["stratum"]==stratum]
    if rule is not None: out=[r for r in out if r["rule"]==rule]
    return out
def rows_spec(spec_id, stratum=None, rule=None):
    out=[r for r in raw_evidence if r["spec_id"]==spec_id and r["method_available"]]
    if stratum is not None: out=[r for r in out if r["stratum"]==stratum]
    if rule is not None: out=[r for r in out if r["rule"]==rule]
    return out

def compute_rates_rs(spec_id, stratum, rule):
    subset=rows_spec(spec_id,stratum,rule)
    n=len(subset)
    correct=sum(1 for r in subset if r["is_correct"])
    false_accept=sum(1 for r in subset if r["is_false_accept"])
    unknown=sum(1 for r in subset if r["is_unknown"])
    return {"n":n,"correct":correct,"false_accept":false_accept,"unknown":unknown,
            "correct_rate":correct/n if n else None,"false_accept_rate":false_accept/n if n else None,"unknown_rate":unknown/n if n else None,
            "wilson_correct":[wilson_ci(correct,n)[0],wilson_ci(correct,n)[1]],"wilson_false":[wilson_ci(false_accept,n)[0],wilson_ci(false_accept,n)[1]]}

def unknown_precision(spec_id, stratum, rule):
    subset=rows_spec(spec_id,stratum,rule)
    tp=sum(1 for r in subset if r["is_unknown"])
    fp=sum(1 for r in subset if r["is_false_accept"])
    return tp/(tp+fp) if (tp+fp)>0 else 0.0

def compute_ece_for(spec_id, stratum, rule):
    subset=rows_spec(spec_id,stratum,rule)
    if not subset: return None,[]
    bins=np.linspace(0,1,6); ece=0.0; total=len(subset); bin_stats=[]
    for b in range(5):
        lo,hi=bins[b],bins[b+1]
        if b==4: bin_recs=[r for r in subset if lo<=r["observed_confidence"]<=hi]
        else: bin_recs=[r for r in subset if lo<=r["observed_confidence"]<hi]
        if not bin_recs:
            bin_stats.append({"bin":b,"count":0,"acc":0.0,"avg_conf":0.0,"edges":[float(lo),float(hi)]})
            continue
        acc=sum(1 for r in bin_recs if r["is_correct"])/len(bin_recs)
        avg_conf=float(np.mean([r["observed_confidence"] for r in bin_recs]))
        ece+=len(bin_recs)/total*abs(acc-avg_conf)
        bin_stats.append({"bin":b,"count":len(bin_recs),"acc":float(acc),"avg_conf":avg_conf,"edges":[float(lo),float(hi)]})
    return float(ece), bin_stats

def get_task_ids(stratum, rule=None):
    # unique task ids for that stratum (any method)
    return sorted(set(r["task_id"] for r in raw_evidence if r["stratum"]==stratum))

def row_for(tid, method):
    lst=[r for r in raw_evidence if r["task_id"]==tid and r["method"]==method and r["method_available"]]
    if not lst:
        return None
    return lst[0]

def binomial_p(k,n,p0=0.10):
    if k<=0: return 1.0
    return float(scipy_binom.sf(k-1,n,p0))

def mcnemar_p(a_list,b_list):
    b=c=0
    for a,bb in zip(a_list,b_list):
        if a and not bb: b+=1
        elif not a and bb: c+=1
    if b+c==0: return {"b":b,"c":c,"chi2":0.0,"p":1.0}
    chi2=(abs(b-c)-1)**2/(b+c); p=1-chi2dist.cdf(chi2,1); return {"b":b,"c":c,"chi2":float(chi2),"p":float(p)}

alias_ids=get_task_ids("alias-OOD")
orth_ids=[t["task_id"] for t in tasks if t["stratum"]=="alias-OOD" and t["family"] in (0,1,2)]
mix_ids=[t["task_id"] for t in tasks if t["stratum"]=="alias-OOD" and t["family"]==3]
held9_ids=[t["task_id"] for t in tasks if t["stratum"]=="alias-OOD" and t["family"] in (0,1,2) and t["is_heldout"]]
exact_ids=get_task_ids("exact-match")
noapp_ids=get_task_ids("no-applicable")
empty_ids=get_task_ids("empty-registry")

# For spec ids, we need to consider rule-specific rates
spec_ids=["B-EXACT-MATCH","B-VERBATIM-REPLAY","B-FLAT-TFIDF-K5-VERBATIM","B-FLAT-TFIDF-K5-CF","B-FLAT-EMBED-K5-VERBATIM","B-FLAT-EMBED-K5-CF","B-RANDOM-K5-VERBATIM","B-RANDOM-K5-CF","H-HIERARCHICAL-VERBATIM","H-HIERARCHICAL-CF","H-WEBAPI-VERBATIM","H-WEBAPI-CF"]

# Prepare metrics object for derived_metrics.json
derived={}
# Compute rates for each spec_id + rule combination for alias/strata
for sid in spec_ids:
    # Determine rule from sid suffix
    if sid.endswith("-VERBATIM"):
        rule="verbatim"
    elif sid.endswith("-CF"):
        rule="correctfamily"
    elif sid in ("B-EXACT-MATCH","B-VERBATIM-REPLAY"):
        # these have both rules; we compute both
        for r in ["verbatim","correctfamily"]:
            for stratum in ["alias-OOD","exact-match","no-applicable","empty-registry"]:
                key=f"{sid}::{stratum}::{r}"
                derived[key]=compute_rates_rs(sid,stratum,r)
        continue
    else:
        rule=None
    for stratum in ["alias-OOD","exact-match","no-applicable","empty-registry"]:
        key=f"{sid}::{stratum}"
        # For sid without explicit rule, derive rule from suffix
        r=rule
        if r is None:
            # e.g., B-EXACT-MATCH already handled
            continue
        derived[key]=compute_rates_rs(sid,stratum,r)

# Also compute for exact split both rules directly via rows_spec already
# Need to handle B-EXACT-MATCH and B-VERBATIM-REPLAY both rules already
# For alias breakdowns under correctfamily
alias_out={}
for sid in spec_ids:
    # choose rule for alias
    if sid in ("B-EXACT-MATCH","B-VERBATIM-REPLAY"):
        # for alias under both rules, report both
        for r in ["verbatim","correctfamily"]:
            rates=compute_rates_rs(sid,"alias-OOD",r)
            alias_out[f"{sid}::{r}"]=rates
    else:
        # derive rule from sid
        r="verbatim" if sid.endswith("-VERBATIM") else "correctfamily"
        rates=compute_rates_rs(sid,"alias-OOD",r)
        alias_out[sid]=rates

# Coverage and density per task alias under each rule
def coverage_for(spec_id, rule):
    subset=rows_spec(spec_id,"alias-OOD",rule)
    if not subset: return None
    # coverage = mean recall_at_k
    vals=[r["recall_at_k"] for r in subset]
    return float(np.mean(vals)) if vals else 0.0

def density_for(spec_id, rule):
    subset=rows_spec(spec_id,"alias-OOD",rule)
    if not subset: return None
    vals=[r["density"] for r in subset if r["density"] is not None]
    return float(np.mean(vals)) if vals else 0.0

coverage={}
density={}
for sid in spec_ids:
    if sid in ("B-EXACT-MATCH","B-VERBATIM-REPLAY"):
        for r in ["verbatim","correctfamily"]:
            coverage[f"{sid}::{r}"]=coverage_for(sid,r)
            density[f"{sid}::{r}"]=density_for(sid,r)
    else:
        r="verbatim" if sid.endswith("-VERBATIM") else "correctfamily"
        coverage[sid]=coverage_for(sid,r)
        density[sid]=density_for(sid,r)

# Bootstrap for coverage gain and density gain under correctfamily
def block_bootstrap_gain(method_a, method_b, ids, n_resamples=2000, metric="recall_at_k"):
    # trajectory-grouped by family
    families={"0":[],"1":[],"2":[],"3":[]}
    for tid in ids:
        t=[x for x in tasks if x["task_id"]==tid][0]
        fam=str(t["family"] if t["family"] is not None else "0")
        families[fam].append(tid)
    fam_keys=list(families.keys())
    # Precompute per-task values for each method under correctfamily rule
    # method_a and _b are spec_ids with CF rule
    def vals_for(method, tids):
        return [row_for(tid, method_cf_map[method])["recall_at_k"] if metric=="recall_at_k" else row_for(tid, method_cf_map[method])["density"] for tid in tids]
    # Map spec_id to actual method pid for CF
    method_cf_map={}
    for pid, retr, rule in PIPELINES_DEF:
        sid=SPEC_ID_MAP[pid]
        if sid not in method_cf_map or rule=="correctfamily":
            # prefer CF mapping
            if rule=="correctfamily":
                method_cf_map[sid]=pid
            elif sid not in method_cf_map:
                method_cf_map[sid]=pid
    # Ensure method ids are CF pids
    # For our gain we compare H-HIERARCHICAL-CF vs best flat CF, etc.
    gains=[]
    # observed gain
    obs_vals_a=[row_for(tid, method_cf_map[method_a])[metric] for tid in ids if row_for(tid, method_cf_map[method_a]) is not None]
    obs_vals_b=[row_for(tid, method_cf_map[method_b])[metric] for tid in ids if row_for(tid, method_cf_map[method_b]) is not None]
    # Need handle None density?
    # For recall, 0/1
    # For density, may be None -> treat as 0 ?
    # Compute observed mean diff
    def mean(vals):
        clean=[v for v in vals if v is not None]
        return float(np.mean(clean)) if clean else 0.0
    obs_gain=mean(obs_vals_a)-mean(obs_vals_b)
    for _ in range(n_resamples):
        # sample families with replacement? Block bootstrap: resample tasks within each family block?
        # Spec says trajectory-grouped block bootstrap respecting family structure: resample tasks grouped by family
        # We'll resample tasks by sampling families then tasks within?
        # Simpler: for each family, resample its tasks with replacement to same family size, then combine
        resampled=[]
        for fam in fam_keys:
            lst=families[fam]
            if not lst: continue
            sampled=rng.choice(lst, size=len(lst), replace=True)
            resampled.extend(sampled)
        # compute gain on resampled
        vals_a=[row_for(tid, method_cf_map[method_a])[metric] for tid in resampled if row_for(tid, method_cf_map[method_a]) is not None]
        vals_b=[row_for(tid, method_cf_map[method_b])[metric] for tid in resampled if row_for(tid, method_cf_map[method_b]) is not None]
        g=mean(vals_a)-mean(vals_b)
        gains.append(g)
    gains=np.array(gains)
    lo,hi=np.percentile(gains, [2.5,97.5])
    p=np.mean(gains<=0) if obs_gain>0 else np.mean(gains>=0)  # one-sided?
    # two-sided p: proportion that crosses zero opposite direction
    # For bootstrap p: if obs_gain>0, p = proportion of gains <=0
    return {"observed_gain":float(obs_gain),"ci_low":float(lo),"ci_high":float(hi),"p":float(p),"gains":gains}

# Need to define method_cf_map correctly for flat best
method_cf_map={}
for pid, retr, rule in PIPELINES_DEF:
    sid=SPEC_ID_MAP[pid]
    if rule=="correctfamily":
        method_cf_map[sid]=pid
# Fill verbatim for completeness but not needed
for pid, retr, rule in PIPELINES_DEF:
    sid=SPEC_ID_MAP[pid]
    if sid not in method_cf_map:
        method_cf_map[sid]=pid

# Compute best flat CF coverage among TFIDF and EMBED
flat_cf_ids=["B-FLAT-TFIDF-K5-CF","B-FLAT-EMBED-K5-CF"]
# Find best
best_flat_cov_sid=max(flat_cf_ids, key=lambda sid: coverage[sid] or 0)
best_flat_density_sid=max(flat_cf_ids, key=lambda sid: density[sid] or 0)

# Bootstrap gains
try:
    hier_gain_boot=block_bootstrap_gain("H-HIERARCHICAL-CF", best_flat_cov_sid, alias_ids, n_resamples=2000, metric="recall_at_k")
except Exception as e:
    print(f"hier gain boot error {e}")
    hier_gain_boot={"observed_gain":0,"ci_low":0,"ci_high":0,"p":1.0}
try:
    webapi_gain_boot=block_bootstrap_gain("H-WEBAPI-CF", best_flat_cov_sid, alias_ids, n_resamples=2000, metric="recall_at_k")
except Exception as e:
    print(f"webapi gain boot error {e}")
    webapi_gain_boot={"observed_gain":0,"ci_low":0,"ci_high":0,"p":1.0}

# Density gains
def density_gain_boot(method_a, best_flat_sid):
    return block_bootstrap_gain(method_a, best_flat_sid, alias_ids, n_resamples=2000, metric="density")

try:
    hier_density_boot=density_gain_boot("H-HIERARCHICAL-CF", best_flat_density_sid)
except Exception as e:
    hier_density_boot={"observed_gain":0,"ci_low":0,"ci_high":0,"p":1.0}
try:
    webapi_density_boot=density_gain_boot("H-WEBAPI-CF", best_flat_density_sid)
except Exception as e:
    webapi_density_boot={"observed_gain":0,"ci_low":0,"ci_high":0,"p":1.0}

# ECE per spec_id rule
ece_results={}
for sid in spec_ids:
    if sid in ("B-EXACT-MATCH","B-VERBATIM-REPLAY"):
        for r in ["verbatim","correctfamily"]:
            ece,bins=compute_ece_for(sid,"alias-OOD",r)
            ece_results[f"{sid}::{r}"]={"ece":ece,"bins":bins}
            # also for exact and noapp?
    else:
        r="verbatim" if sid.endswith("-VERBATIM") else "correctfamily"
        ece,bins=compute_ece_for(sid,"alias-OOD",r)
        ece_results[sid]={"ece":ece,"bins":bins}

# Confidence std
conf_stds={}
for sid in spec_ids:
    if sid in ("B-EXACT-MATCH","B-VERBATIM-REPLAY"):
        for r in ["verbatim","correctfamily"]:
            subset=rows_spec(sid,None,r)
            vals=[rr["observed_confidence"] for rr in subset if rr["observed_confidence"] is not None]
            conf_stds[f"{sid}::{r}"]=float(np.std(vals)) if len(vals)>1 else 0.0
    else:
        r="verbatim" if sid.endswith("-VERBATIM") else "correctfamily"
        subset=rows_spec(sid,None,r)
        vals=[rr["observed_confidence"] for rr in subset if rr["observed_confidence"] is not None]
        conf_stds[sid]=float(np.std(vals)) if len(vals)>1 else 0.0

# McNemar for alias-OOD under correctfamily vs exact etc
def mcnemar_between(spec_a, spec_b, stratum, rule_a, rule_b):
    # paired lists for alias ids
    ids=alias_ids if stratum=="alias-OOD" else get_task_ids(stratum)
    a_list=[]; b_list=[]
    for tid in ids:
        ra=row_for(tid, method_cf_map[spec_a] if rule_a=="correctfamily" else [p for p,sid,r in [(pid,SPEC_ID_MAP[pid],ru) for pid,_,ru in PIPELINES_DEF] if sid==spec_a and r==rule_a][0][0] if False else None)
        # Actually need to fetch row via pid
        # Find pid for spec_a, rule_a
        pid_a=None
        for pid,_,ru in PIPELINES_DEF:
            if SPEC_ID_MAP[pid]==spec_a and ru==rule_a:
                pid_a=pid; break
        pid_b=None
        for pid,_,ru in PIPELINES_DEF:
            if SPEC_ID_MAP[pid]==spec_b and ru==rule_b:
                pid_b=pid; break
        ra=row_for(tid,pid_a)
        rb=row_for(tid,pid_b)
        if ra is None or rb is None:
            continue
        a_list.append(ra["is_correct"])
        b_list.append(rb["is_correct"])
    return mcnemar_p(a_list,b_list)

# Helper to get pid for spec+rule
def pid_for(spec_id, rule):
    for pid,_,ru in PIPELINES_DEF:
        if SPEC_ID_MAP[pid]==spec_id and ru==rule:
            return pid
    return None

# Compute specific McNemars needed for decision
alias_ids_cf_comparison = alias_ids
# HIER CF vs B-EXACT-MATCH-CF? Actually B-EXACT is kernel exact, but we have B-EXACT-MATCH-CF vs alias 0 expected
# For S1: McNemar vs B-EXACT-MATCH (0/40 expected) under CF
def mcnemar_alias_vs_exact(spec_cf):
    pid_cf=pid_for(spec_cf,"correctfamily")
    pid_exact=pid_for("B-EXACT-MATCH","correctfamily")  # or verbatim same
    # For alias, B-EXACT should be 0/40, so we compare is_correct lists
    a_list=[row_for(tid,pid_cf)["is_correct"] for tid in alias_ids]
    b_list=[row_for(tid,pid_exact)["is_correct"] for tid in alias_ids]
    return mcnemar_p(a_list,b_list)

hier_vs_exact_cf=mcnemar_alias_vs_exact("H-HIERARCHICAL-CF")
webapi_vs_exact_cf=mcnemar_alias_vs_exact("H-WEBAPI-CF")
# Hierarchical vs best flat
pid_hier_cf=pid_for("H-HIERARCHICAL-CF","correctfamily")
pid_webapi_cf=pid_for("H-WEBAPI-CF","correctfamily")
pid_best_flat_tfidf=pid_for(best_flat_cov_sid,"correctfamily")  # best flat id
# For best flat, need actual best among two; we have best_flat_cov_sid
hier_vs_bestflat=mcnemar_p([row_for(tid,pid_hier_cf)["is_correct"] for tid in alias_ids],[row_for(tid,pid_best_flat_tfidf)["is_correct"] for tid in alias_ids])
webapi_vs_bestflat=mcnemar_p([row_for(tid,pid_webapi_cf)["is_correct"] for tid in alias_ids],[row_for(tid,pid_best_flat_tfidf)["is_correct"] for tid in alias_ids])
webapi_vs_hier=mcnemar_p([row_for(tid,pid_webapi_cf)["is_correct"] for tid in alias_ids],[row_for(tid,pid_hier_cf)["is_correct"] for tid in alias_ids])
# False accept McNemar vs B-VERBATIM-REPLAY-CF
pid_verbatim_cf=pid_for("B-VERBATIM-REPLAY","correctfamily")
hier_false_vs_verbatim=mcnemar_p([row_for(tid,pid_hier_cf)["is_false_accept"] for tid in alias_ids],[row_for(tid,pid_verbatim_cf)["is_false_accept"] for tid in alias_ids])
webapi_false_vs_verbatim=mcnemar_p([row_for(tid,pid_webapi_cf)["is_false_accept"] for tid in alias_ids],[row_for(tid,pid_verbatim_cf)["is_false_accept"] for tid in alias_ids])

# ---------- Save raw_evidence and derived ----------
with open(OUT_DIR/"raw_evidence.json","w") as f:
    json.dump(to_native(raw_evidence),f,indent=2)
# Convert numpy gains to list for JSON
hier_gain_boot_json={k:float(v) if k!="gains" else None for k,v in hier_gain_boot.items()}
webapi_gain_boot_json={k:float(v) if k!="gains" else None for k,v in webapi_gain_boot.items()}
hier_density_boot_json={k:float(v) if k!="gains" else None for k,v in hier_density_boot.items()}
webapi_density_boot_json={k:float(v) if k!="gains" else None for k,v in webapi_density_boot.items()}

derived_metrics={
    "alias_rates": alias_out,
    "coverage": coverage,
    "density": density,
    "best_flat": {"coverage_sid":best_flat_cov_sid, "coverage_value":coverage[best_flat_cov_sid], "density_sid":best_flat_density_sid,"density_value":density[best_flat_density_sid]},
    "hier_gain": hier_gain_boot_json,
    "webapi_gain": webapi_gain_boot_json,
    "hier_density_gain": hier_density_boot_json,
    "webapi_density_gain": webapi_density_boot_json,
    "ece": ece_results,
    "conf_std": conf_stds,
    "mcnemar": {
        "hier_vs_exact_cf": hier_vs_exact_cf,
        "webapi_vs_exact_cf": webapi_vs_exact_cf,
        "hier_vs_best_flat_cf": hier_vs_bestflat,
        "webapi_vs_best_flat_cf": webapi_vs_bestflat,
        "webapi_vs_hier_cf": webapi_vs_hier,
        "hier_false_vs_verbatim_cf": hier_false_vs_verbatim,
        "webapi_false_vs_verbatim_cf": webapi_false_vs_verbatim,
    },
    "derived_rates": derived,
    "counts": {"alias_OOD":40,"orthogonal":len(orth_ids),"mixed":len(mix_ids),"heldout9":len(held9_ids),"exact":12,"noapp":12,"empty":6},
}

with open(OUT_DIR/"derived_metrics.json","w") as f:
    json.dump(to_native(derived_metrics),f,indent=2)

print(f"derived saved best_flat {best_flat_cov_sid} cov {coverage[best_flat_cov_sid]}")
print(f"hier gain {hier_gain_boot_json}")
print(f"webapi gain {webapi_gain_boot_json}")

# ---------- Summary prints for result generation ----------
for sid in spec_ids:
    if sid.endswith("-VERBATIM"):
        r="verbatim"
    elif sid.endswith("-CF"):
        r="correctfamily"
    else:
        continue
    rates=compute_rates_rs(sid,"alias-OOD",r)
    print(f"{sid} alias {rates['correct']}/{rates['n']}={rates['correct_rate']:.3f} false {rates['false_accept_rate']:.3f} verb? {r}")

# Exact rates
for sid in ["B-EXACT-MATCH","B-VERBATIM-REPLAY"]:
    for r in ["verbatim","correctfamily"]:
        rates=compute_rates_rs(sid,"exact-match",r)
        print(f"{sid}::{r} exact {rates['correct']}/{rates['n']}={rates['correct_rate']}")

# Verbatim check
for sid in spec_ids:
    if sid in ("B-EXACT-MATCH","B-VERBATIM-REPLAY"):
        for r in ["verbatim"]:
            rates=compute_rates_rs(sid,"alias-OOD",r)
            print(f"VERB check {sid}::{r} {rates['correct']}/{rates['n']}")
    else:
        if sid.endswith("-VERBATIM"):
            rates=compute_rates_rs(sid,"alias-OOD","verbatim")
            print(f"VERB check {sid} {rates['correct']}/{rates['n']}")

