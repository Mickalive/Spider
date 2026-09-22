#!/usr/bin/env python3
"""
EXP-PHYSICS-35787698409 EXECUTE — Physics Correlated-State FSM Recalibrated (REOPEN)

Frozen spec: Bayesian Dirichlet-Multinomial RECALIBRATED to K=24 alpha=1/K, N=1999,
trajectory-grouped permutation 1000 perms seed 42, resampling unit trajectory_id.

Changes vs parent EXP-PHYSICS-35782523165 (audit-accepted pipeline, execute.py
sha256 9cb24333adb124a19ab3a74185cde1c4a6ad28448070305f86725518448f9a6d):
  1. K: 12 -> 24, ALPHA = 1/K (1/24), per director mandate recalibration.
     All Bayesian DM CMI/H computations use K=24 alpha=1/24 explicitly.
  2. Independent-noise replication RECALIBRATED: DOM variants per state 3 -> 6
     (rng_dom.integers(0,6) per step, independent of S_next), seed documented.
  3. Decision gates G1-G4 applied in frozen order; G3 (iid null miscentered) is
     now a gate per frozen decision_rule (parent reported it but did not gate).
  4. B-TRAJECTORY-MEMORY and B-SITE-LEAKAGE-DIAGNOSTIC baselines computed per
     frozen spec baselines (non-gating diagnostics).
  5. S_URLonly sensitivity probe (non-gating, per spec measurement_validity).

Unchanged frozen construction:
  - Correlated-state primary: 6-state FSM, L per trajectory (A/B), basin bias
    0.70/0.30, DOM_before = SHA256(L||state||variant%3) => 36 hashes, |R|/N 0.018,
    50 trajectories x 40 steps = 2000 transitions, N=1999 analyzed, seed 42.
  - IID synthetic null: same marginal P(S), S_next i.i.d. per step, seed 42+777.
  - Strata C = (URL_before_normalized, H_K=3 actions, Action_leakageFree).
  - B-DOM-SIMILARITY TF-IDF k5 fit TRAIN only 70/30 by trajectory_id.
  - B-MARKOV-1 / B-MARKOV-K3 MLE fit TRAIN only.
  - 1000 trajectory-grouped permutations of DOM_before labels within each C
    stratum, grouped by trajectory_id, seed 42, no Gaussian jitter.
  - p_bonf = min(1, p_raw * n_tests) with n_tests=8 (R1/R2 x primary+2 baselines,
    max 8, conservative; matches parent frozen implementation, audit-accepted),
    floor p_raw 1/1001 at 1000 perms, alpha 0.01.

Outputs: raw_transitions_{correlated,independent,iid}.json, raw_results.json.
Deterministic: PYTHONHASHSEED=0, numpy seeds fixed; re-executable byte-identical
aside from elapsed.
"""
import hashlib, json, math, os, random, time, sys, pathlib, re, collections, itertools
from collections import Counter, defaultdict
import numpy as np

EXP_ID = "EXP-PHYSICS-35787698409"
EXP_DIR = pathlib.Path(__file__).parent
SEED = 42
PYTHONHASHSEED = 0
K = 24                      # RECALIBRATED Dirichlet categories (was 12)
ALPHA = 1.0 / K             # 1/24
N_PERMS = 1000
N_TOTAL = 2000              # 50 traj x 40 steps
N_ANALYZED = 1999
N_TESTS_PBONF = 8           # Bonferroni n_tests max 8 (R1/R2 x primary+2 baselines)

random.seed(SEED)
np.random.seed(SEED)

def normalize_url(url: str) -> str:
    url = url.lower()
    # strip query ?session= ?token=
    url = re.sub(r'[?&](session|token)=[^&]*', '', url)
    if '#' in url:
        base, frag = url.split('#', 1)
        base = base.rstrip('/')
        # preserve hash fragment case
        url = base + '#' + frag
    else:
        url = url.rstrip('/')
    return url

def normalize_title(title: str) -> str:
    return title.strip().lower()[:200]

def hash_state(url_after, title_after, url_only=False):
    if url_only:
        s = normalize_url(url_after)
    else:
        s = normalize_url(url_after) + '|' + normalize_title(title_after)
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def sha256_trunc(s, n=16):
    return hashlib.sha256(s.encode()).hexdigest()[:n]

# === Dataset generation ===

def generate_correlated(seed=42, n_traj=50, steps_per=40, persist_mode="per_trajectory"):
    """Correlated-state SPA: L per trajectory (or per 15-step regime), DOM = SHA256(L|state|variant).
    FROZEN construction identical to parent EXP-PHYSICS-35782523165 (byte-identical expected)."""
    rng = np.random.default_rng(seed)
    transitions = []
    for tid in range(n_traj):
        L = str(rng.choice(["A","B"]))
        S_current = int(rng.integers(0,6))  # 0-5
        steps_in_regime = 0
        for step in range(steps_per):
            variant_mod = step % 3
            visible_text = f"user:{L} state:{S_current} variant:{variant_mod}"
            a11y_serial = f"role:banner name:user:{L} value:{L} state:{S_current} variant:{variant_mod}"
            dom_R1 = sha256_trunc(visible_text[:5000])
            dom_R2 = sha256_trunc(a11y_serial[:5000])
            dom_R3 = sha256_trunc(dom_R1 + dom_R2)
            primitive = "click"
            target_sig = "button|next||"
            action_leakageFree = f"{primitive}:{target_sig}"
            action_leaky = f"{primitive}:{target_sig}:href=https://spa.local/#/state_{S_current}"
            url_before = f"https://spa.local/#/state_{S_current}"
            url_before_norm = normalize_url(url_before)
            title_before = f"SPA State {S_current} regime {L}"
            is_A = (L == "A")
            if rng.random() < (0.70 if is_A else 0.30):
                basin = [0,1,2]
            else:
                basin = [3,4,5]
            S_next = int(rng.choice(basin))
            url_after = f"https://spa.local/#/state_{S_next}"
            title_after = f"SPA State {S_next} regime {L}"
            S_next_hash = hash_state(url_after, title_after)
            S_next_hash_urlonly = hash_state(url_after, title_after, url_only=True)
            transitions.append({
                "trajectory_id": f"corr_traj_{tid:02d}",
                "step": step,
                "S_current": S_current,
                "S_next": S_next_hash,
                "S_next_urlonly": S_next_hash_urlonly,
                "S_next_raw": f"{url_after}|{title_after}",
                "S_next_int": S_next,
                "url_before": url_before,
                "url_before_norm": url_before_norm,
                "url_after": url_after,
                "title_before": title_before,
                "title_after": title_after,
                "action_primitive": primitive,
                "target_sig": target_sig,
                "action_leakageFree": action_leakageFree,
                "action_leaky": action_leaky,
                "dom_before_R1_raw": visible_text[:5000],
                "dom_before_R1": dom_R1,
                "dom_before_R2_raw": a11y_serial[:5000],
                "dom_before_R2": dom_R2,
                "dom_before_R3": dom_R3,
                "dom_before_R4": f"{len(visible_text)}|{S_current}|{variant_mod}",
                "dom_before_visible": visible_text[:5000],
                "dom_before_a11y": a11y_serial[:5000],
                "dom_bytes": len(visible_text.encode()),
                "a11y_bytes": len(a11y_serial.encode()),
                "L": L,
                "variant_mod": variant_mod,
                "S_current_int": S_current,
            })
            if persist_mode == "per_15":
                steps_in_regime += 1
                if steps_in_regime >= 15 and rng.random() < 0.07:
                    L = "B" if L=="A" else "A"
                    steps_in_regime = 0
            S_current = S_next
    return transitions

def generate_independent(seed=42, n_traj=50, steps_per=40):
    """Independent-noise replication RECALIBRATED: same 6-state FSM without L, DOM variant
    independent per-step draw among 6 variants per state (was 3). rng_dom
    np.random.default_rng(seed+12345) draws integers(0,6) per step; transition rng
    np.random.default_rng(seed+999). Constant action keeps strata dense; DOM independent
    of S_next by construction -> BC ~ 0 with higher null_std than parent (3 variants)."""
    rng = np.random.default_rng(seed+999)
    rng_dom = np.random.default_rng(seed+12345)
    transitions = []
    for tid in range(n_traj):
        S_current = int(rng.integers(0,6))
        for step in range(steps_per):
            variant_mod = int(rng_dom.integers(0,6))  # RECALIBRATED: 6 variants per state
            visible_text = f"state:{S_current} variant:{variant_mod}"
            a11y_serial = f"role:banner name:state_{S_current} variant:{variant_mod}"
            dom_R1 = sha256_trunc(visible_text[:5000])
            dom_R2 = sha256_trunc(a11y_serial[:5000])
            dom_R3 = sha256_trunc(dom_R1+dom_R2)
            primitive = "click"
            target_sig = "button|next||"
            action_leakageFree = f"{primitive}:{target_sig}"
            action_leaky = f"{primitive}:{target_sig}:href=https://spa.local/#/state_{S_current}"
            url_before = f"https://spa.local/#/state_{S_current}"
            url_before_norm = normalize_url(url_before)
            title_before = f"SPA State {S_current}"
            if rng.random() < 0.5:
                basin = [0,1,2]
            else:
                basin = [3,4,5]
            S_next = int(rng.choice(basin))
            url_after = f"https://spa.local/#/state_{S_next}"
            title_after = f"SPA State {S_next}"
            S_next_hash = hash_state(url_after, title_after)
            S_next_hash_urlonly = hash_state(url_after, title_after, url_only=True)
            transitions.append({
                "trajectory_id": f"ind_traj_{tid:02d}",
                "step": step,
                "S_current": S_current,
                "S_next": S_next_hash,
                "S_next_urlonly": S_next_hash_urlonly,
                "S_next_raw": f"{url_after}|{title_after}",
                "S_next_int": S_next,
                "url_before": url_before,
                "url_before_norm": url_before_norm,
                "url_after": url_after,
                "title_before": title_before,
                "title_after": title_after,
                "action_primitive": primitive,
                "target_sig": target_sig,
                "action_leakageFree": action_leakageFree,
                "action_leaky": action_leaky,
                "dom_before_R1_raw": visible_text[:5000],
                "dom_before_R1": dom_R1,
                "dom_before_R2_raw": a11y_serial[:5000],
                "dom_before_R2": dom_R2,
                "dom_before_R3": dom_R3,
                "dom_before_R4": f"{len(visible_text)}|{S_current}|{variant_mod}",
                "dom_before_visible": visible_text[:5000],
                "dom_before_a11y": a11y_serial[:5000],
                "dom_bytes": len(visible_text.encode()),
                "a11y_bytes": len(a11y_serial.encode()),
                "L": "NA",
                "variant_mod": variant_mod,
                "S_current_int": S_current,
            })
            S_current = S_next
    return transitions

def generate_iid(seed=42, n_traj=50, steps_per=40, marginal_src=None):
    """I.I.D. synthetic null: same marginal P(S) but S_next drawn i.i.d. independent per step.
    FROZEN construction identical to parent (seed+777)."""
    rng = np.random.default_rng(seed+777)
    if marginal_src is not None:
        vals = [t["S_next_int"] for t in marginal_src]
        uniq, counts = np.unique(vals, return_counts=True)
        probs = counts / counts.sum()
        states = uniq.tolist()
    else:
        states = [0,1,2,3,4,5]
        probs = [1/6]*6
    transitions = []
    for tid in range(n_traj):
        S_current = int(rng.choice(states, p=probs))
        L = str(rng.choice(["A","B"]))  # phantom L for DOM
        for step in range(steps_per):
            variant_mod = step % 3
            visible_text = f"user:{L} state:{S_current} variant:{variant_mod}"
            a11y_serial = f"role:banner name:user:{L} value:{L} state:{S_current} variant:{variant_mod}"
            dom_R1 = sha256_trunc(visible_text[:5000])
            dom_R2 = sha256_trunc(a11y_serial[:5000])
            dom_R3 = sha256_trunc(dom_R1+dom_R2)
            primitive = "click"
            target_sig = "button|next||"
            action_leakageFree = f"{primitive}:{target_sig}"
            action_leaky = f"{primitive}:{target_sig}:href=https://spa.local/#/state_{S_current}"
            url_before = f"https://spa.local/#/state_{S_current}"
            url_before_norm = normalize_url(url_before)
            title_before = f"SPA State {S_current}"
            S_next = int(rng.choice(states, p=probs))
            url_after = f"https://spa.local/#/state_{S_next}"
            title_after = f"SPA State {S_next}"
            S_next_hash = hash_state(url_after, title_after)
            S_next_hash_urlonly = hash_state(url_after, title_after, url_only=True)
            transitions.append({
                "trajectory_id": f"iid_traj_{tid:02d}",
                "step": step,
                "S_current": S_current,
                "S_next": S_next_hash,
                "S_next_urlonly": S_next_hash_urlonly,
                "S_next_raw": f"{url_after}|{title_after}",
                "S_next_int": S_next,
                "url_before": url_before,
                "url_before_norm": url_before_norm,
                "url_after": url_after,
                "title_before": title_before,
                "title_after": title_after,
                "action_primitive": primitive,
                "target_sig": target_sig,
                "action_leakageFree": action_leakageFree,
                "action_leaky": action_leaky,
                "dom_before_R1_raw": visible_text[:5000],
                "dom_before_R1": dom_R1,
                "dom_before_R2_raw": a11y_serial[:5000],
                "dom_before_R2": dom_R2,
                "dom_before_R3": dom_R3,
                "dom_before_R4": f"{len(visible_text)}|{S_current}|{variant_mod}",
                "dom_before_visible": visible_text[:5000],
                "dom_before_a11y": a11y_serial[:5000],
                "dom_bytes": len(visible_text.encode()),
                "a11y_bytes": len(a11y_serial.encode()),
                "L": L,
                "variant_mod": variant_mod,
                "S_current_int": S_current,
            })
            S_current = S_next
    return transitions

# === Strata and entropy ===

def build_strata(transitions, K_hist=3, min_per_stratum=3, action_key="action_leakageFree"):
    by_traj = defaultdict(list)
    for t in transitions:
        by_traj[t["trajectory_id"]].append(t)
    for tid in by_traj:
        by_traj[tid].sort(key=lambda x: x["step"])
    strata = defaultdict(list)
    for tid, lst in by_traj.items():
        for i, t in enumerate(lst):
            hist = []
            for k in range(1, K_hist+1):
                if i - k >= 0:
                    hist.append(lst[i-k][action_key])
                else:
                    hist.append("<START>")
            hist = tuple(hist)
            key = (t["url_before_norm"], hist, t[action_key])
            strata[key].append(t)
    return strata, by_traj

def compute_H_Snext_given_C(strata, min_per_stratum=3, K=24, alpha=1/24):
    total_n = 0
    total_ent = 0.0
    valid_strata = 0
    rare = 0
    for key, items in strata.items():
        if len(items) < min_per_stratum:
            rare += 1
            continue
        n = len(items)
        cnt = Counter(x["S_next"] for x in items)
        denom = n + K*alpha  # = n+1
        ent = 0.0
        for c in cnt.values():
            p = (c + alpha) / denom
            ent -= p * math.log2(p)
        unseen = K - len(cnt)
        if unseen > 0:
            p_unseen = alpha / denom
            if p_unseen>0:
                ent -= unseen * p_unseen * math.log2(p_unseen)
        total_ent += ent * n
        total_n += n
        valid_strata += 1
    if total_n==0:
        return 0.0, valid_strata, total_n, len(strata), rare
    return total_ent/total_n, valid_strata, total_n, len(strata), rare

def compute_cmi_bayesian(strata, dom_key, s_key="S_next", K=24, alpha=1/24):
    """CMI = H(S|C)-H(S|C,DOM) via Bayesian Dirichlet-Multinomial K=24 alpha=1/K per stratum."""
    total_n = 0
    total_cmi = 0.0
    H_cond = 0.0
    H_cond_dom = 0.0
    for key, items in strata.items():
        n = len(items)
        by_dom = defaultdict(list)
        for t in items:
            by_dom[t[dom_key]].append(t)
        cnt_s = Counter(x[s_key] for x in items)
        denom_s = n + K*alpha  # = n+1
        H_s_c = 0.0
        for c in cnt_s.values():
            p = (c+alpha)/denom_s
            H_s_c -= p*math.log2(p)
        unseen_s = K - len(cnt_s)
        if unseen_s>0:
            p_unseen = alpha/denom_s
            H_s_c -= unseen_s * p_unseen * math.log2(p_unseen) if p_unseen>0 else 0
        H_s_c_dom = 0.0
        for dom_val, dom_items in by_dom.items():
            n_dom = len(dom_items)
            p_dom = n_dom / n
            cnt_sd = Counter(x[s_key] for x in dom_items)
            denom_sd = n_dom + K*alpha
            H_sd = 0.0
            for c in cnt_sd.values():
                p = (c+alpha)/denom_sd
                H_sd -= p*math.log2(p)
            unseen_sd = K - len(cnt_sd)
            if unseen_sd>0:
                p_unseen = alpha/denom_sd
                H_sd -= unseen_sd * p_unseen * math.log2(p_unseen) if p_unseen>0 else 0
            H_s_c_dom += p_dom * H_sd
        cmi_stratum = H_s_c - H_s_c_dom
        total_cmi += cmi_stratum * n
        H_cond += H_s_c * n
        H_cond_dom += H_s_c_dom * n
        total_n += n
    if total_n==0:
        return 0.0, 0.0, 0.0, total_n
    return total_cmi/total_n, H_cond/total_n, H_cond_dom/total_n, total_n

def compute_cmi_simple_plugin(strata, dom_key, s_key="S_next"):
    """Diagnostic simple plug-in (unsmoothed) for comparison"""
    total_n=0
    total_cmi=0.0
    for key, items in strata.items():
        n=len(items)
        joint=Counter((t[dom_key], t[s_key]) for t in items)
        marg_r=Counter(t[dom_key] for t in items)
        marg_s=Counter(t[s_key] for t in items)
        mi=0.0
        for (r,s),c in joint.items():
            p_rs=c/n
            p_r=marg_r[r]/n
            p_s=marg_s[s]/n
            mi+=p_rs*math.log2(p_rs/(p_r*p_s)) if p_rs>0 and p_r>0 and p_s>0 else 0
        total_cmi+=mi*n
        total_n+=n
    return total_cmi/total_n if total_n>0 else 0.0

# === Permutation ===

def permutation_test_grouped(transitions, dom_key, K_hist=3, n_perms=1000, seed=42,
                             min_per_stratum=3, s_key="S_next", action_key="action_leakageFree"):
    """Trajectory-grouped permutation null: shuffle DOM_before blocks across trajectories
    within each C stratum, grouped by trajectory_id, preserving per-trajectory DOM
    frequencies. Bayesian DM K=24 alpha=1/K. Resampling unit = trajectory_id."""
    filtered_all, _ = build_strata(transitions, K_hist=K_hist, min_per_stratum=min_per_stratum, action_key=action_key)
    filtered = {k:v for k,v in filtered_all.items() if len(v)>=min_per_stratum}
    rare = len(filtered_all) - len(filtered)
    singleton = sum(1 for v in filtered_all.values() if len(v)==1)
    obs, H_c, H_c_dom, total_n = compute_cmi_bayesian(filtered, dom_key, s_key=s_key, K=K, alpha=ALPHA)
    perm_vals = []
    rng = np.random.default_rng(seed)
    for perm_idx in range(n_perms):
        shuffled_filtered = {}
        for key, items in filtered.items():
            traj_groups = defaultdict(list)
            for t in items:
                traj_groups[t["trajectory_id"]].append(t)
            traj_ids = list(traj_groups.keys())
            dom_blocks = [ [x[dom_key] for x in traj_groups[tid]] for tid in traj_ids ]
            order = rng.permutation(len(dom_blocks))
            shuffled_blocks = [dom_blocks[i] for i in order]
            flat_shuffled = []
            for b in shuffled_blocks:
                flat_shuffled.extend(b)
            sorted_tids = sorted(traj_ids)
            ptr=0
            reassigned = {}
            for tid in sorted_tids:
                sz = len(traj_groups[tid])
                reassigned[tid] = flat_shuffled[ptr:ptr+sz]
                ptr+=sz
            new_items=[]
            for tid in sorted_tids:
                group_items = sorted(traj_groups[tid], key=lambda x: x["step"])
                doms = reassigned[tid]
                for orig, new_dom in zip(group_items, doms):
                    t2 = dict(orig)
                    t2[dom_key] = new_dom
                    new_items.append(t2)
            shuffled_filtered[key] = new_items
        perm_obs, _, _, _ = compute_cmi_bayesian(shuffled_filtered, dom_key, s_key=s_key, K=K, alpha=ALPHA)
        perm_vals.append(perm_obs)
    perm_vals = np.array(perm_vals)
    perm_mean = float(perm_vals.mean()) if len(perm_vals)>0 else 0.0
    perm_std = float(perm_vals.std(ddof=1)) if len(perm_vals)>1 else 0.0
    bc = float(obs - perm_mean)
    n_exceed = int(np.sum(perm_vals >= obs))
    p_raw = (1 + n_exceed)/(n_perms+1)
    p_bonf = float(min(p_raw * N_TESTS_PBONF, 1.0))
    ci_low, ci_high = np.percentile(perm_vals, [2.5,97.5]) if len(perm_vals)>0 else (0.0,0.0)
    d = bc/perm_std if perm_std>1e-9 else 0.0
    null_std_ok = perm_std > 0.01
    null_mean_ok = abs(perm_mean) < 0.1
    return {
        "observed": float(obs),
        "H_S_given_C": float(H_c),
        "H_S_given_C_DOM": float(H_c_dom),
        "perm_mean": perm_mean,
        "perm_std": perm_std,
        "bc": bc,
        "p_raw": float(p_raw),
        "p_bonf": float(p_bonf),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "cohen_d": float(d),
        "perm_vals_sample": perm_vals.tolist()[:20],
        "perm_vals_all": perm_vals.tolist() if len(perm_vals)<=100 else perm_vals.tolist()[:100],
        "n_strata": len(filtered),
        "total_n": int(total_n),
        "rare_strata": int(rare),
        "singleton_strata": int(singleton),
        "n_strata_total": len(filtered_all),
        "null_std_ok": null_std_ok,
        "null_mean_ok": null_mean_ok,
        "resampling_unit": "trajectory_id",
        "K": K,
        "alpha": ALPHA,
        "min_per_stratum": min_per_stratum,
        "plugin_simple": float(compute_cmi_simple_plugin(filtered, dom_key, s_key)),
    }

# === Baselines ===

def baseline_dom_similarity(transitions, dom_text_key="dom_before_visible", K_hist=3, seed=42, s_key="S_next"):
    """B-DOM-SIMILARITY TF-IDF cosine k=5, vocab fit TRAIN trajectories only (70/30)."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        has_sklearn=True
    except Exception:
        has_sklearn=False
    rng=np.random.default_rng(seed)
    traj_ids=sorted(set(t["trajectory_id"] for t in transitions))
    rng.shuffle(traj_ids)
    n_train=int(0.7*len(traj_ids))
    train_ids=set(traj_ids[:n_train])
    test_ids=set(traj_ids[n_train:])
    train=[t for t in transitions if t["trajectory_id"] in train_ids]
    test=[t for t in transitions if t["trajectory_id"] in test_ids]
    if len(train)==0 or len(test)==0:
        return {"acc":0.0,"bc_sim":0.0,"perm_mean":0,"perm_std":0,"method":"no_split"}
    raw_key_visible = dom_text_key
    train_texts=[t.get(raw_key_visible,"") for t in train]
    test_texts=[t.get(raw_key_visible,"") for t in test]
    if has_sklearn:
        try:
            vec=TfidfVectorizer(max_features=500)
            X_train=vec.fit_transform(train_texts)
            X_test=vec.transform(test_texts)
            sim=cosine_similarity(X_test, X_train)
            nn_preds=[]
            for i in range(sim.shape[0]):
                idx=np.argsort(sim[i])[::-1][:5]
                votes=[train[j][s_key] for j in idx]
                pred=Counter(votes).most_common(1)[0][0]
                nn_preds.append(pred)
            train_preds=[]
            if len(train)>1:
                sim_train=cosine_similarity(X_train, X_train)
                np.fill_diagonal(sim_train, -1)
                for i in range(sim_train.shape[0]):
                    idx=np.argsort(sim_train[i])[::-1][:5]
                    votes=[train[j][s_key] for j in idx]
                    pred=Counter(votes).most_common(1)[0][0]
                    train_preds.append(pred)
            else:
                train_preds=[train[0][s_key]]
            unified=[]
            for t,p in zip(train, train_preds):
                t2=dict(t)
                t2["dom_sim_pred"] = p
                unified.append(t2)
            for t,p in zip(test, nn_preds):
                t2=dict(t)
                t2["dom_sim_pred"] = p
                unified.append(t2)
            bc_sim = permutation_test_grouped(unified, "dom_sim_pred", K_hist=K_hist, n_perms=1000, seed=seed+10, min_per_stratum=3, s_key=s_key)
            return {"acc": float(sum(1 for a,b in zip(nn_preds, [t[s_key] for t in test]) if a==b)/len(test) if test else 0),
                    "method":"tfidf_cosine_k5",
                    "bc_sim": bc_sim["bc"],
                    "bc_sim_full": bc_sim,
                    "vocab_fit":"train_only",
                    "n_train":len(train),
                    "n_test":len(test)}
        except Exception as e:
            has_sklearn=False
    def jaccard(a,b):
        sa=set(a.lower().split())
        sb=set(b.lower().split())
        if not sa and not sb:
            return 1.0
        return len(sa&sb)/len(sa|sb) if len(sa|sb)>0 else 0.0
    nn_preds=[]
    for t_test in test:
        sims=[]
        for t_train in train:
            s=jaccard(t_test.get(raw_key_visible,""), t_train.get(raw_key_visible,""))
            sims.append((s,t_train[s_key]))
        sims.sort(key=lambda x: x[0], reverse=True)
        top5=[v for _,v in sims[:5]]
        pred=Counter(top5).most_common(1)[0][0] if top5 else None
        nn_preds.append(pred)
    acc=sum(1 for p,t in zip(nn_preds,test) if p==t[s_key])/len(test) if test else 0
    train_preds=[]
    for i,t_test in enumerate(train):
        sims=[]
        for j,t_train in enumerate(train):
            if i==j: continue
            s=jaccard(t_test.get(raw_key_visible,""), t_train.get(raw_key_visible,""))
            sims.append((s,t_train[s_key]))
        sims.sort(key=lambda x: x[0], reverse=True)
        top5=[v for _,v in sims[:5]]
        pred=Counter(top5).most_common(1)[0][0] if top5 else train[0][s_key]
        train_preds.append(pred)
    unified=[]
    for t,p in zip(train, train_preds):
        t2=dict(t); t2["dom_sim_pred"]=p; unified.append(t2)
    for t,p in zip(test, nn_preds):
        t2=dict(t); t2["dom_sim_pred"]=p; unified.append(t2)
    bc_sim = permutation_test_grouped(unified, "dom_sim_pred", K_hist=K_hist, n_perms=1000, seed=seed+10, min_per_stratum=3, s_key=s_key)
    return {"acc": float(acc), "method":"jaccard_k5_fallback", "bc_sim": bc_sim["bc"], "bc_sim_full": bc_sim, "n_train":len(train), "n_test":len(test)}

def baseline_markov(transitions, K_hist=3, seed=42, s_key="S_next"):
    """B-MARKOV-1 and B-MARKOV-K3 via MLE fit TRAIN only (70/30 by trajectory_id)."""
    rng=np.random.default_rng(seed)
    traj_ids=sorted(set(t["trajectory_id"] for t in transitions))
    rng.shuffle(traj_ids)
    n_train=int(0.7*len(traj_ids))
    train_ids=set(traj_ids[:n_train])
    test_ids=set(traj_ids[n_train:])
    train=[t for t in transitions if t["trajectory_id"] in train_ids]
    test=[t for t in transitions if t["trajectory_id"] in test_ids]
    by_traj_train=defaultdict(list)
    for t in train:
        by_traj_train[t["trajectory_id"]].append(t)
    for k in by_traj_train:
        by_traj_train[k].sort(key=lambda x: x["step"])
    markov1_counts=defaultdict(Counter)
    for t in train:
        key=(t["url_before_norm"], t["action_leakageFree"])
        markov1_counts[key][t[s_key]]+=1
    markov1_pred={k: Counter(v).most_common(1)[0][0] for k,v in markov1_counts.items()}
    markovK3_counts=defaultdict(Counter)
    for tid,lst in by_traj_train.items():
        for i,t in enumerate(lst):
            hist=[]
            for kk in range(1,K_hist+1):
                if i-kk>=0:
                    hist.append(lst[i-kk]["action_leakageFree"])
                else:
                    hist.append("<START>")
            hist=tuple(hist)
            key=(t["url_before_norm"], hist, t["action_leakageFree"])
            markovK3_counts[key][t[s_key]]+=1
    markovK3_pred={k: Counter(v).most_common(1)[0][0] for k,v in markovK3_counts.items()}
    unified1=[]
    unifiedK3=[]
    global_majority = Counter(t[s_key] for t in train).most_common(1)[0][0] if train else None
    by_traj_all=defaultdict(list)
    all_trans = train+test
    for t in all_trans:
        by_traj_all[t["trajectory_id"]].append(t)
    for k in by_traj_all:
        by_traj_all[k].sort(key=lambda x: x["step"])
    for tid,lst in by_traj_all.items():
        for i,t in enumerate(lst):
            key1=(t["url_before_norm"], t["action_leakageFree"])
            pred1=markov1_pred.get(key1, global_majority)
            t2=dict(t)
            t2["markov1_pred"]=pred1
            unified1.append(t2)
            hist=[]
            for kk in range(1,K_hist+1):
                if i-kk>=0:
                    hist.append(lst[i-kk]["action_leakageFree"])
                else:
                    hist.append("<START>")
            hist=tuple(hist)
            keyK3=(t["url_before_norm"], hist, t["action_leakageFree"])
            predK3=markovK3_pred.get(keyK3, global_majority)
            t3=dict(t)
            t3["markovK3_pred"]=predK3
            unifiedK3.append(t3)
    bc1 = permutation_test_grouped(unified1, "markov1_pred", K_hist=K_hist, n_perms=1000, seed=seed+20, min_per_stratum=3, s_key=s_key)
    bcK3 = permutation_test_grouped(unifiedK3, "markovK3_pred", K_hist=K_hist, n_perms=1000, seed=seed+21, min_per_stratum=3, s_key=s_key)
    correct1=sum(1 for t in test if markov1_pred.get((t["url_before_norm"], t["action_leakageFree"]), global_majority)==t[s_key])
    acc1=correct1/len(test) if test else 0
    correctK3=0
    totalK3=len(test)
    by_traj_test=defaultdict(list)
    for t in test:
        by_traj_test[t["trajectory_id"]].append(t)
    for tid,lst in by_traj_test.items():
        lst_sorted=sorted(lst, key=lambda x: x["step"])
        for i,t in enumerate(lst_sorted):
            hist=[]
            for kk in range(1,K_hist+1):
                if i-kk>=0:
                    hist.append(lst_sorted[i-kk]["action_leakageFree"])
                else:
                    hist.append("<START>")
            hist=tuple(hist)
            key=(t["url_before_norm"], hist, t["action_leakageFree"])
            pred=markovK3_pred.get(key, global_majority)
            if pred==t[s_key]:
                correctK3+=1
    accK3=correctK3/totalK3 if totalK3 else 0
    return {"bc_markov1": bc1["bc"], "bc_markov1_full": bc1, "acc_markov1": float(acc1),
            "bc_markovK3": bcK3["bc"], "bc_markovK3_full": bcK3, "acc_markovK3": float(accK3),
            "n_train":len(train),"n_test":len(test)}

def baseline_trajectory_memory(transitions, K_hist=3, seed=42, s_key="S_next"):
    """B-TRAJECTORY-MEMORY (non-gating leakage diagnostic): exact key
    (URL_before_norm, H_K=3 actions, Action)->S_next memorization from TRAIN only.
    Reports memorization ambiguity (mean distinct S_next per seen key), test coverage
    and exact-match accuracy of pure memory."""
    rng=np.random.default_rng(seed)
    traj_ids=sorted(set(t["trajectory_id"] for t in transitions))
    rng.shuffle(traj_ids)
    n_train=int(0.7*len(traj_ids))
    train_ids=set(traj_ids[:n_train])
    test_ids=set(traj_ids[n_train:])
    train=[t for t in transitions if t["trajectory_id"] in train_ids]
    test=[t for t in transitions if t["trajectory_id"] in test_ids]
    mem=defaultdict(Counter)
    by_traj=defaultdict(list)
    for t in train:
        by_traj[t["trajectory_id"]].append(t)
    for k in by_traj:
        by_traj[k].sort(key=lambda x: x["step"])
    for tid,lst in by_traj.items():
        for i,t in enumerate(lst):
            hist=tuple(lst[i-kk]["action_leakageFree"] if i-kk>=0 else "<START>" for kk in range(1,K_hist+1))
            key=(t["url_before_norm"], hist, t["action_leakageFree"])
            mem[key][t[s_key]]+=1
    ambiguity=[len(v) for v in mem.values()]
    mean_amb = float(np.mean(ambiguity)) if ambiguity else 0.0
    unique_keys = sum(1 for v in mem.values() if len(v)==1)
    # test coverage + exact-match accuracy of pure memorization
    by_traj_test=defaultdict(list)
    for t in test:
        by_traj_test[t["trajectory_id"]].append(t)
    for k in by_traj_test:
        by_traj_test[k].sort(key=lambda x: x["step"])
    covered=0; correct=0; total=0
    for tid,lst in by_traj_test.items():
        for i,t in enumerate(lst):
            hist=tuple(lst[i-kk]["action_leakageFree"] if i-kk>=0 else "<START>" for kk in range(1,K_hist+1))
            key=(t["url_before_norm"], hist, t["action_leakageFree"])
            total+=1
            if key in mem:
                covered+=1
                if mem[key].most_common(1)[0][0]==t[s_key]:
                    correct+=1
    return {"n_keys": len(mem),
            "mean_distinct_S_per_key": float(mean_amb),
            "unique_key_fraction": float(unique_keys/len(mem)) if mem else 0.0,
            "test_coverage": float(covered/total) if total else 0.0,
            "test_exact_acc": float(correct/covered) if covered else None,
            "n_train": len(train), "n_test": len(test)}

def baseline_site_leakage(transitions, dom_key, K_hist=3, seed=42, s_key="S_next"):
    """B-SITE-LEAKAGE-DIAGNOSTIC (non-gating): BC_leaky (strata conditioned on
    Action_leaky with href) vs BC_leakageFree gap. Reports inflation if href leaks."""
    gap = permutation_test_grouped(transitions, dom_key, K_hist=K_hist, n_perms=1000,
                                   seed=seed, min_per_stratum=3, s_key=s_key,
                                   action_key="action_leaky")
    return gap

def compute_mi_dom_action(transitions, dom_key, action_key="action_leakageFree"):
    n=len(transitions)
    joint=Counter((t[dom_key], t[action_key]) for t in transitions)
    marg_r=Counter(t[dom_key] for t in transitions)
    marg_a=Counter(t[action_key] for t in transitions)
    mi=0.0
    for (r,a),c in joint.items():
        p_rs=c/n
        p_r=marg_r[r]/n
        p_a=marg_a[a]/n
        mi+=p_rs*math.log2(p_rs/(p_r*p_a)) if p_rs>0 and p_r>0 and p_a>0 else 0
    return float(mi)

def main():
    print("="*70)
    print(f"{EXP_ID} EXECUTE correlated-state Bayesian K={K} N=1999 seed {SEED} (RECALIBRATED K=24)")
    print("="*70)
    start=time.time()
    # Verify freeze
    try:
        with open(EXP_DIR/"freeze.json") as f:
            freeze=json.load(f)
        print(f"Freeze hashes: {freeze['hashes']}")
        for fn in ["prereg.md","request.json","spec.json"]:
            h = hashlib.sha256(open(EXP_DIR/fn,'rb').read()).hexdigest()
            print(f"  verify {fn}: {h} match={h==freeze['hashes'][fn]}")
    except Exception as e:
        print(f"Freeze check failed: {e}")
    # Generate datasets
    print("\n--- Generating datasets ---")
    corr = generate_correlated(seed=SEED, n_traj=50, steps_per=40, persist_mode="per_trajectory")
    corr = corr[:1999]
    print(f"Correlated primary: {len(corr)} transitions, 50 traj, L distribution {Counter(t['L'] for t in corr)}")
    ind = generate_independent(seed=SEED, n_traj=50, steps_per=40)
    ind = ind[:1999]
    print(f"Independent-noise RECALIBRATED: {len(ind)} transitions, variants/state=6")
    iid = generate_iid(seed=SEED, n_traj=50, steps_per=40, marginal_src=corr)
    iid = iid[:1999]
    print(f"IID null: {len(iid)} transitions")
    # Check H ceiling and data quality
    for label, data in [("corr",corr),("ind",ind),("iid",iid)]:
        strata,_ = build_strata(data, K_hist=3)
        H, valid, total_n, total_strata, rare = compute_H_Snext_given_C(strata, min_per_stratum=3, K=K, alpha=ALPHA)
        filtered={k:v for k,v in strata.items() if len(v)>=3}
        nR1=len(set(t['dom_before_R1'] for t in data))
        print(f"  {label}: H(S|C)={H:.3f} valid_strata={valid}/{total_strata} rare={rare} total_n={total_n} dom_unique_R1={nR1} |R|/N={nR1/len(data):.3f}")
        ge3=sum(1 for v in strata.values() if len(v)>=3)
        print(f"    strata_ge3={ge3} singleton_rate={sum(1 for v in strata.values() if len(v)==1)/max(1,len(strata)):.3f} dom_bytes avg {np.mean([t['dom_bytes'] for t in data]):.1f}")
        print(f"    MI(DOM;Action_free) R1={compute_mi_dom_action(data,'dom_before_R1'):.4f} R2={compute_mi_dom_action(data,'dom_before_R2'):.4f}")

    representations = ["dom_before_R1","dom_before_R2","dom_before_R3","dom_before_R4"]
    # Primary CMI per representation + baselines
    corr_results={}
    print("\n--- Correlated primary CMI (Bayesian DM K=24) ---")
    for rep in representations:
        res = permutation_test_grouped(corr, rep, K_hist=3, n_perms=N_PERMS, seed=SEED, min_per_stratum=3, s_key="S_next")
        sim = baseline_dom_similarity(corr, dom_text_key="dom_before_visible" if rep=="dom_before_R1" else "dom_before_a11y", K_hist=3, seed=SEED)
        markov = baseline_markov(corr, K_hist=3, seed=SEED)
        print(f"  {rep}: BC={res['bc']:.4f} obs={res['observed']:.4f} null_mean={res['perm_mean']:.4f} null_std={res['perm_std']:.4f} p_raw={res['p_raw']:.5f} p_bonf={res['p_bonf']:.5f} d={res['cohen_d']:.2f} strata={res['n_strata']} H_c={res['H_S_given_C']:.3f}")
        print(f"    sim BC_sim={sim['bc_sim']:.4f} acc_sim={sim['acc']:.3f} markov1 BC={markov['bc_markov1']:.4f} markovK3 BC={markov['bc_markovK3']:.4f}")
        corr_results[rep]={"cmi":res,"sim":sim,"markov":markov}

    print("\n--- Independent-noise replication RECALIBRATED CMI ---")
    ind_results={}
    for rep in representations:
        res = permutation_test_grouped(ind, rep, K_hist=3, n_perms=N_PERMS, seed=SEED+100, min_per_stratum=3, s_key="S_next")
        sim = baseline_dom_similarity(ind, dom_text_key="dom_before_visible" if rep=="dom_before_R1" else "dom_before_a11y", K_hist=3, seed=SEED+100)
        markov = baseline_markov(ind, K_hist=3, seed=SEED+100)
        print(f"  {rep}: BC={res['bc']:.4f} p_raw={res['p_raw']:.4f} null_std={res['perm_std']:.4f} null_mean={res['perm_mean']:.4f} sim={sim['bc_sim']:.4f}")
        ind_results[rep]={"cmi":res,"sim":sim,"markov":markov}

    print("\n--- IID null CMI ---")
    iid_results={}
    for rep in ["dom_before_R1","dom_before_R2"]:
        res = permutation_test_grouped(iid, rep, K_hist=3, n_perms=N_PERMS, seed=SEED+200, min_per_stratum=3, s_key="S_next")
        print(f"  {rep}: BC={res['bc']:.4f} p_raw={res['p_raw']:.4f} null_std={res['perm_std']:.4f} null_mean={res['perm_mean']:.4f}")
        iid_results[rep]={"cmi":res}

    # Sensitivity probes (non-gating)
    print("\n--- Sensitivity (non-gating) ---")
    sens_results={}
    # S_URLonly sensitivity on correlated R1/R2
    for rep in ["dom_before_R1","dom_before_R2"]:
        res = permutation_test_grouped(corr, rep, K_hist=3, n_perms=200, seed=SEED+300, min_per_stratum=3, s_key="S_next_urlonly")
        sens_results[f"S_URLonly_{rep}"]={"cmi":res}
        print(f"  S_URLonly {rep}: BC={res['bc']:.4f} p_raw={res['p_raw']:.4f}")
    # B-SITE-LEAKAGE-DIAGNOSTIC on correlated R1/R2
    for rep in ["dom_before_R1","dom_before_R2"]:
        gap = baseline_site_leakage(corr, rep, K_hist=3, seed=SEED+400, s_key="S_next")
        sens_results[f"site_leakage_{rep}"]={"cmi":gap}
        free_bc = corr_results[rep]["cmi"]["bc"]
        print(f"  B-SITE-LEAKAGE {rep}: BC_leaky={gap['bc']:.4f} BC_free={free_bc:.4f} gap={gap['bc']-free_bc:.4f}")
    # B-TRAJECTORY-MEMORY on correlated
    tm = baseline_trajectory_memory(corr, K_hist=3, seed=SEED)
    print(f"  B-TRAJECTORY-MEMORY: keys={tm['n_keys']} mean_distinct_S={tm['mean_distinct_S_per_key']:.3f} unique_frac={tm['unique_key_fraction']:.3f} test_cov={tm['test_coverage']:.3f} test_acc={tm['test_exact_acc']}")

    # === Decision gates (frozen order) ===
    print("\n--- Decision gates (frozen) ---")
    # G1 positive correlated control (R1 or R2): BC>=0.30 p_raw<0.01 null_std>0.01 |null_mean|<0.1
    pos_pass_R1 = corr_results["dom_before_R1"]["cmi"]["bc"]>=0.30 and corr_results["dom_before_R1"]["cmi"]["p_raw"]<0.01 and corr_results["dom_before_R1"]["cmi"]["perm_std"]>0.01 and abs(corr_results["dom_before_R1"]["cmi"]["perm_mean"])<0.1
    pos_pass_R2 = corr_results["dom_before_R2"]["cmi"]["bc"]>=0.30 and corr_results["dom_before_R2"]["cmi"]["p_raw"]<0.01 and corr_results["dom_before_R2"]["cmi"]["perm_std"]>0.01 and abs(corr_results["dom_before_R2"]["cmi"]["perm_mean"])<0.1
    pos_control_pass = pos_pass_R1 or pos_pass_R2
    print(f"G1 positive control R1 pass={pos_pass_R1} BC={corr_results['dom_before_R1']['cmi']['bc']:.4f} p={corr_results['dom_before_R1']['cmi']['p_raw']:.5f} std={corr_results['dom_before_R1']['cmi']['perm_std']:.4f} mean={corr_results['dom_before_R1']['cmi']['perm_mean']:.4f}")
    print(f"G1 positive control R2 pass={pos_pass_R2} BC={corr_results['dom_before_R2']['cmi']['bc']:.4f} p={corr_results['dom_before_R2']['cmi']['p_raw']:.5f} std={corr_results['dom_before_R2']['cmi']['perm_std']:.4f} mean={corr_results['dom_before_R2']['cmi']['perm_mean']:.4f}")

    # G2 independent-noise confound: BC>=0.05 and p<0.10 with valid null
    ind_confound_R1 = ind_results["dom_before_R1"]["cmi"]["bc"]>=0.05 and ind_results["dom_before_R1"]["cmi"]["p_raw"]<0.10 and ind_results["dom_before_R1"]["cmi"]["perm_std"]>0.01 and abs(ind_results["dom_before_R1"]["cmi"]["perm_mean"])<0.1
    ind_confound_R2 = ind_results["dom_before_R2"]["cmi"]["bc"]>=0.05 and ind_results["dom_before_R2"]["cmi"]["p_raw"]<0.10 and ind_results["dom_before_R2"]["cmi"]["perm_std"]>0.01 and abs(ind_results["dom_before_R2"]["cmi"]["perm_mean"])<0.1
    ind_confound = ind_confound_R1 or ind_confound_R2
    ind_pass_R1 = abs(ind_results["dom_before_R1"]["cmi"]["bc"])<0.05 and ind_results["dom_before_R1"]["cmi"]["p_raw"]>0.10
    ind_pass_R2 = abs(ind_results["dom_before_R2"]["cmi"]["bc"])<0.05 and ind_results["dom_before_R2"]["cmi"]["p_raw"]>0.10
    print(f"G2 ind confound R1={ind_confound_R1} BC={ind_results['dom_before_R1']['cmi']['bc']:.4f} p={ind_results['dom_before_R1']['cmi']['p_raw']:.4f}")
    print(f"G2 ind confound R2={ind_confound_R2} BC={ind_results['dom_before_R2']['cmi']['bc']:.4f} p={ind_results['dom_before_R2']['cmi']['p_raw']:.4f}")
    print(f"  ind pass criteria (|BC|<0.05 p>0.10) R1={ind_pass_R1} R2={ind_pass_R2}")

    # G3 iid null miscentered: BC>0.03 and p<0.10 with valid null
    iid_miscenter_R1 = iid_results["dom_before_R1"]["cmi"]["bc"]>0.03 and iid_results["dom_before_R1"]["cmi"]["p_raw"]<0.10 and iid_results["dom_before_R1"]["cmi"]["perm_std"]>0.01 and abs(iid_results["dom_before_R1"]["cmi"]["perm_mean"])<0.1
    iid_miscenter_R2 = iid_results["dom_before_R2"]["cmi"]["bc"]>0.03 and iid_results["dom_before_R2"]["cmi"]["p_raw"]<0.10 and iid_results["dom_before_R2"]["cmi"]["perm_std"]>0.01 and abs(iid_results["dom_before_R2"]["cmi"]["perm_mean"])<0.1
    iid_miscenter = iid_miscenter_R1 or iid_miscenter_R2
    iid_pass_R1 = iid_results["dom_before_R1"]["cmi"]["bc"]<=0.03 and iid_results["dom_before_R1"]["cmi"]["p_raw"]>0.10
    iid_pass_R2 = iid_results["dom_before_R2"]["cmi"]["bc"]<=0.03 and iid_results["dom_before_R2"]["cmi"]["p_raw"]>0.10
    print(f"G3 iid miscenter R1={iid_miscenter_R1} BC={iid_results['dom_before_R1']['cmi']['bc']:.4f} p={iid_results['dom_before_R1']['cmi']['p_raw']:.4f}")
    print(f"G3 iid miscenter R2={iid_miscenter_R2} BC={iid_results['dom_before_R2']['cmi']['bc']:.4f} p={iid_results['dom_before_R2']['cmi']['p_raw']:.4f}")
    print(f"  iid pass criteria (BC<=0.03 p>0.10) R1={iid_pass_R1} R2={iid_pass_R2}")

    # G4 primary null degenerate on BOTH R1 and R2
    degenerate_R1 = corr_results["dom_before_R1"]["cmi"]["perm_std"]<=0.01 or abs(corr_results["dom_before_R1"]["cmi"]["perm_mean"])>=0.1
    degenerate_R2 = corr_results["dom_before_R2"]["cmi"]["perm_std"]<=0.01 or abs(corr_results["dom_before_R2"]["cmi"]["perm_mean"])>=0.1
    both_degenerate = degenerate_R1 and degenerate_R2
    print(f"G4 degenerate R1={degenerate_R1} R2={degenerate_R2} both={both_degenerate}")

    # Primary sig per frozen decision_rule
    def sig(rep):
        cmi=corr_results[rep]["cmi"]
        sim_bc=corr_results[rep]["sim"]["bc_sim"]
        markov_bc=corr_results[rep]["markov"]["bc_markov1"]
        gap = cmi["bc"] - max(sim_bc, markov_bc)
        cond = cmi["bc"]>0.05 and cmi["p_bonf"]<0.01 and abs(cmi["perm_mean"])<0.1 and cmi["perm_std"]>0.01 and gap>=0.05
        return cond, gap, sim_bc, markov_bc
    sig_R1, gap_R1, sim_R1, markov_R1 = sig("dom_before_R1")
    sig_R2, gap_R2, sim_R2, markov_R2 = sig("dom_before_R2")
    print(f"Primary sig R1={sig_R1} gap={gap_R1:.4f} sim={sim_R1:.4f} markov1={markov_R1:.4f} BC={corr_results['dom_before_R1']['cmi']['bc']:.4f} p_bonf={corr_results['dom_before_R1']['cmi']['p_bonf']:.5f}")
    print(f"Primary sig R2={sig_R2} gap={gap_R2:.4f} sim={sim_R2:.4f} markov1={markov_R2:.4f} BC={corr_results['dom_before_R2']['cmi']['bc']:.4f} p_bonf={corr_results['dom_before_R2']['cmi']['p_bonf']:.5f}")

    # Gated decision chain (frozen order G1,G2,G3,G4 -> primary)
    if not pos_control_pass:
        status="MEASUREMENT_INVALID"; outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID pipeline_blind_or_miscalibrated"
        reason=(f"G1 fails: positive correlated control BC<0.30 or p>=0.01 or null_std<=0.01 or |null_mean|>=0.1 "
                f"(R1 BC {corr_results['dom_before_R1']['cmi']['bc']:.3f} p {corr_results['dom_before_R1']['cmi']['p_raw']:.4f} mean {corr_results['dom_before_R1']['cmi']['perm_mean']:.4f} std {corr_results['dom_before_R1']['cmi']['perm_std']:.4f}, "
                f"R2 BC {corr_results['dom_before_R2']['cmi']['bc']:.3f} p {corr_results['dom_before_R2']['cmi']['p_raw']:.4f} mean {corr_results['dom_before_R2']['cmi']['perm_mean']:.4f} std {corr_results['dom_before_R2']['cmi']['perm_std']:.4f})")
    elif ind_confound:
        status="MEASUREMENT_INVALID"; outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID pipeline_confounds_independent"
        reason=(f"G2 fails: independent-noise shows BC>=0.05 p<0.10 with valid null "
                f"(R1 {ind_results['dom_before_R1']['cmi']['bc']:.3f} p {ind_results['dom_before_R1']['cmi']['p_raw']:.4f} "
                f"R2 {ind_results['dom_before_R2']['cmi']['bc']:.3f} p {ind_results['dom_before_R2']['cmi']['p_raw']:.4f})")
    elif iid_miscenter:
        status="MEASUREMENT_INVALID"; outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID iid_null_miscentered"
        reason=(f"G3 fails: i.i.d. null shows BC>0.03 p<0.10 with valid null => null miscentered "
                f"(R1 {iid_results['dom_before_R1']['cmi']['bc']:.3f} p {iid_results['dom_before_R1']['cmi']['p_raw']:.4f} "
                f"R2 {iid_results['dom_before_R2']['cmi']['bc']:.3f} p {iid_results['dom_before_R2']['cmi']['p_raw']:.4f})")
    elif both_degenerate:
        status="MEASUREMENT_INVALID"; outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID null_degenerate"
        reason=(f"G4 fails: primary null degenerate on BOTH R1 and R2 (null_std<=0.01 or |null_mean|>=0.1) "
                f"R1 std {corr_results['dom_before_R1']['cmi']['perm_std']:.4f} mean {corr_results['dom_before_R1']['cmi']['perm_mean']:.4f} "
                f"R2 std {corr_results['dom_before_R2']['cmi']['perm_std']:.4f} mean {corr_results['dom_before_R2']['cmi']['perm_mean']:.4f}")
    else:
        if sig_R1 or sig_R2:
            status="COMPLETE"; outcome="SUPPORTS"; verdict="SURVIVES_CURRENT_TEST"
            reason=(f"Gates pass and EXISTS R with sig(R)=1: R1 sig={sig_R1} BC {corr_results['dom_before_R1']['cmi']['bc']:.3f} p_bonf {corr_results['dom_before_R1']['cmi']['p_bonf']:.4f} gap {gap_R1:.3f}, "
                    f"R2 sig={sig_R2} BC {corr_results['dom_before_R2']['cmi']['bc']:.3f} p_bonf {corr_results['dom_before_R2']['cmi']['p_bonf']:.4f} gap {gap_R2:.3f}")
        else:
            status="COMPLETE"; outcome="FALSIFIES"; verdict="FALSIFIED-IN-SETTING"
            reason=(f"Gates pass but FORALL R fails sig: R1 BC {corr_results['dom_before_R1']['cmi']['bc']:.3f} p_bonf {corr_results['dom_before_R1']['cmi']['p_bonf']:.4f} gap {gap_R1:.3f}, "
                    f"R2 BC {corr_results['dom_before_R2']['cmi']['bc']:.3f} p_bonf {corr_results['dom_before_R2']['cmi']['p_bonf']:.4f} gap {gap_R2:.3f}, while gates pass")

    gate_table = {
        "G1_positive_control": {"pass": pos_control_pass, "R1": pos_pass_R1, "R2": pos_pass_R2,
                                "required": "BC>=0.30 p_raw<0.01 null_std>0.01 |null_mean|<0.1 on R1 or R2"},
        "G2_independent_confound": {"pass": not ind_confound, "R1_confound": ind_confound_R1, "R2_confound": ind_confound_R2,
                                    "required": "NOT (BC>=0.05 and p_raw<0.10 with valid null)"},
        "G3_iid_miscentered": {"pass": not iid_miscenter, "R1": iid_miscenter_R1, "R2": iid_miscenter_R2,
                               "required": "NOT (BC>0.03 and p_raw<0.10 with valid null)"},
        "G4_primary_null_degenerate": {"pass": not both_degenerate, "R1_degenerate": degenerate_R1, "R2_degenerate": degenerate_R2,
                                       "required": "NOT (null_std<=0.01 or |null_mean|>=0.1 on BOTH R1 and R2)"},
    }

    print(f"\nFinal: status={status} outcome={outcome} verdict={verdict}")
    print(f"Reason: {reason}")

    # Artifacts
    with open(EXP_DIR/"raw_transitions_correlated.json","w") as f:
        json.dump(corr, f, indent=2)
    with open(EXP_DIR/"raw_transitions_independent.json","w") as f:
        json.dump(ind, f, indent=2)
    with open(EXP_DIR/"raw_transitions_iid.json","w") as f:
        json.dump(iid, f, indent=2)
    full_results={
        "experiment_id": EXP_ID,
        "seed": SEED,
        "K": K,
        "alpha": ALPHA,
        "N": len(corr),
        "n_tests_pbonf": N_TESTS_PBONF,
        "correlated": corr_results,
        "independent": ind_results,
        "iid": iid_results,
        "sensitivity": sens_results,
        "trajectory_memory": tm,
        "gate_table": gate_table,
        "decision": {"status":status,"outcome":outcome,"verdict":verdict,"reason":reason},
        "elapsed": time.time()-start,
    }
    with open(EXP_DIR/"raw_results.json","w") as f:
        json.dump(full_results, f, indent=2)
    print(f"Artifacts saved to {EXP_DIR}")
    print(f"Elapsed {time.time()-start:.1f}s")

if __name__=="__main__":
    main()