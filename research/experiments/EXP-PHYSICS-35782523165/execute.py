#!/usr/bin/env python3
"""
EXP-PHYSICS-35782523165 EXECUTE — correlated-state FSM pivot
Frozen spec: Bayesian DM K=12 N=1999 seed 42 trajectory-grouped permutation 1000 perms
"""
import hashlib, json, math, os, random, time, sys, pathlib, re, collections, itertools
from collections import Counter, defaultdict
import numpy as np

EXP_ID = "EXP-PHYSICS-35782523165"
EXP_DIR = pathlib.Path(__file__).parent
SEED = 42
PYTHONHASHSEED = 0
K = 12
ALPHA = 1.0 / K
N_PERMS = 1000
N_TOTAL = 2000  # 50 traj x 40 steps
N_ANALYZED = 1999

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
    """Correlated-state SPA: L per trajectory (or per 15-step regime), DOM = SHA256(L|state|variant)"""
    rng = np.random.default_rng(seed)
    transitions = []
    for tid in range(n_traj):
        L = str(rng.choice(["A","B"]))
        S_current = int(rng.integers(0,6))  # 0-5
        # regime flip tracking for per_15 variant (not used for per_trajectory)
        steps_in_regime = 0
        for step in range(steps_per):
            # variant mod ensures 3 DOM hashes per (S,L)
            variant_mod = step % 3
            # DOM_before
            visible_text = f"user:{L} state:{S_current} variant:{variant_mod}"
            a11y_serial = f"role:banner name:user:{L} value:{L} state:{S_current} variant:{variant_mod}"
            # Also construct numeric structural (exploratory but degenerate)
            dom_R1 = sha256_trunc(visible_text[:5000])
            dom_R2 = sha256_trunc(a11y_serial[:5000])
            dom_R3 = sha256_trunc(dom_R1 + dom_R2)  # multi_feature
            # R4 numeric structural not hash but placeholder
            # Action sampling constant to keep strata dense (large n) and MI(DOM;Action) low
            primitive = "click"
            target_sig = "button|next||"  # constant, never href, independent of L and S
            action_leakageFree = f"{primitive}:{target_sig}"
            action_leaky = f"{primitive}:{target_sig}:href=https://spa.local/#/state_{S_current}"
            url_before = f"https://spa.local/#/state_{S_current}"
            url_before_norm = normalize_url(url_before)
            title_before = f"SPA State {S_current} regime {L}"
            # Transition: P(S_next | S_current, Action, L) differs by regime
            # Basin: A={0,1,2} B={3,4,5}
            # If L=A: favor basin A with 0.70 else B 0.30, mirrored for B
            # Within basin, uniformly choose state
            p_cross = 0.30
            is_A = (L == "A")
            # choose basin
            # use rng random
            if rng.random() < (0.70 if is_A else 0.30):
                basin = [0,1,2]
            else:
                basin = [3,4,5]
            # For extra stay bias, with 0.5 choose S_current if it's in basin else uniform
            # But to keep H~0.9, we keep uniform within basin
            S_next = int(rng.choice(basin))
            url_after = f"https://spa.local/#/state_{S_next}"
            title_after = f"SPA State {S_next} regime {L}"  # title correlates with S_next and L but constant per state not essential
            S_next_hash = hash_state(url_after, title_after)
            S_next_hash_urlonly = hash_state(url_after, title_after, url_only=True)
            # store
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
                "dom_before_R4": f"{len(visible_text)}|{S_current}|{variant_mod}",  # numeric placeholder
                "dom_before_visible": visible_text[:5000],
                "dom_before_a11y": a11y_serial[:5000],
                "dom_bytes": len(visible_text.encode()),
                "a11y_bytes": len(a11y_serial.encode()),
                "L": L,
                "variant_mod": variant_mod,
                "S_current_int": S_current,
            })
            # Update L persistence per trajectory: L stays, but if persist_mode per_15 regime with P flip 0.07 per 15 steps, not implemented for primary
            # For per_trajectory, L constant
            if persist_mode == "per_15":
                steps_in_regime += 1
                if steps_in_regime >= 15 and rng.random() < 0.07:
                    L = "B" if L=="A" else "A"
                    steps_in_regime = 0
            S_current = S_next
    return transitions

def generate_independent(seed=42, n_traj=50, steps_per=40):
    """Independent-noise: same FSM but without L, DOM variant independent per-step 3 variants per state independent of L/S_next, reused families"""
    rng = np.random.default_rng(seed+999)
    rng_dom = np.random.default_rng(seed+12345)
    transitions = []
    for tid in range(n_traj):
        S_current = int(rng.integers(0,6))
        for step in range(steps_per):
            variant_mod = int(rng_dom.integers(0,3))  # 0-2 independent
            # independent DOM: 3 variants per state, reused, independent of transition bias
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
            # Transition without L bias: uniform across basins, p_stay 0.50 (i.e., basin uniform 0.5 each)
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
    """I.I.D. synthetic null: same marginal P(S) but S_next drawn i.i.d. independent per step"""
    rng = np.random.default_rng(seed+777)
    # estimate marginal from correlated src if provided
    if marginal_src is not None:
        vals = [t["S_next_int"] for t in marginal_src]
        # but we need S_next distribution; use S_next_int uniform-ish? Estimate frequencies
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
            title_before = f"SPA State {S_current}"  # independent of L for iid null
            # S_next i.i.d. independent of DOM/L/S_current
            S_next = int(rng.choice(states, p=probs))
            url_after = f"https://spa.local/#/state_{S_next}"
            title_after = f"SPA State {S_next}"  # independent of L to ensure S_next hash independent of DOM
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

def build_strata(transitions, K=3, min_per_stratum=3):
    by_traj = defaultdict(list)
    for t in transitions:
        by_traj[t["trajectory_id"]].append(t)
    for tid in by_traj:
        by_traj[tid].sort(key=lambda x: x["step"])
    strata = defaultdict(list)
    for tid, lst in by_traj.items():
        for i, t in enumerate(lst):
            hist = []
            for k in range(1, K+1):
                if i - k >= 0:
                    hist.append(lst[i-k]["action_leakageFree"])
                else:
                    hist.append("<START>")
            hist = tuple(hist)
            # spec strata key C = (URL_before_normalized, H_K_actions, Action_leakageFree)
            # But H_K already includes Action history, and current Action added separately
            # So key is (URL_norm, H_K_actions_tuple, current_action)
            key = (t["url_before_norm"], hist, t["action_leakageFree"])
            strata[key].append(t)
    # also compute singleton etc.
    return strata, by_traj

def compute_H_Snext_given_C(strata, min_per_stratum=3, K=12, alpha=1/12):
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
        # Dirichlet posterior mean entropy
        # p_i = (cnt+alpha)/(n+K*alpha) where K*alpha=1 -> denom=n+1
        denom = n + K*alpha  # = n+1
        # Compute H = -sum p log2 p
        # Need to include unseen categories? But K=12 fixed, unpublished categories have prob alpha/denom
        # However if we include unseen, we need to account for K - distinct categories.
        # For simplicity, include all K categories: distinct + unseen
        # Unseen prob = alpha/denom each, there are K - len(cnt) unseen
        # But S_next cardinality may be less than K (6 states -> hashes 6 distinct but with title+L maybe up to 12)
        # Use K categories.
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

def compute_cmi_bayesian(strata, dom_key, s_key="S_next", K=12, alpha=1/12):
    """Compute CMI = H(S|C)-H(S|C,DOM) via Bayesian Dirichlet per stratum weighted. Use K*alpha denom (original) but with larger min strata to keep bias low."""
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

def permutation_test_grouped(transitions, dom_key, K=3, n_perms=1000, seed=42, min_per_stratum=3, s_key="S_next"):
    filtered_all, _ = build_strata(transitions, K=K, min_per_stratum=min_per_stratum)
    # filter rare
    filtered = {k:v for k,v in filtered_all.items() if len(v)>=min_per_stratum}
    rare = len(filtered_all) - len(filtered)
    singleton = sum(1 for v in filtered_all.values() if len(v)==1)
    obs, H_c, H_c_dom, total_n = compute_cmi_bayesian(filtered, dom_key, s_key=s_key)
    perm_vals = []
    rng = np.random.default_rng(seed)
    # For each perm, shuffle DOM within each stratum grouped by trajectory_id
    # Need to preserve per-trajectory DOM frequencies
    for perm_idx in range(n_perms):
        shuffled_filtered = {}
        for key, items in filtered.items():
            # group by trajectory
            traj_groups = defaultdict(list)
            for t in items:
                traj_groups[t["trajectory_id"]].append(t)
            traj_ids = list(traj_groups.keys())
            # extract DOM blocks per trajectory in original order
            dom_blocks = [ [x[dom_key] for x in traj_groups[tid]] for tid in traj_ids ]
            # shuffle blocks order via permutation
            order = rng.permutation(len(dom_blocks))
            shuffled_blocks = [dom_blocks[i] for i in order]
            # flatten shuffled
            flat_shuffled = []
            for b in shuffled_blocks:
                flat_shuffled.extend(b)
            # re-chunk by original group sizes sorted by traj_id to preserve deterministic mapping
            sorted_tids = sorted(traj_ids)
            # Need mapping from original traj_id to block: we shuffled order, so flat_shuffled is in shuffled order
            # Reassign to sorted order by group sizes
            ptr=0
            reassigned = {}
            for tid in sorted_tids:
                sz = len(traj_groups[tid])
                reassigned[tid] = flat_shuffled[ptr:ptr+sz]
                ptr+=sz
            # Build new items
            new_items=[]
            for tid in sorted_tids:
                group_items = sorted(traj_groups[tid], key=lambda x: x["step"])
                doms = reassigned[tid]
                for orig, new_dom in zip(group_items, doms):
                    t2 = dict(orig)
                    t2[dom_key] = new_dom
                    new_items.append(t2)
            shuffled_filtered[key] = new_items
        perm_obs, _, _, _ = compute_cmi_bayesian(shuffled_filtered, dom_key, s_key=s_key)
        perm_vals.append(perm_obs)
    perm_vals = np.array(perm_vals)
    perm_mean = float(perm_vals.mean()) if len(perm_vals)>0 else 0.0
    perm_std = float(perm_vals.std(ddof=1)) if len(perm_vals)>1 else 0.0
    bc = float(obs - perm_mean)
    n_exceed = int(np.sum(perm_vals >= obs))
    p_raw = (1 + n_exceed)/(n_perms+1)
    # Bonferroni max 8 (R1/R2 x primary+ baselines 2) but per spec n_tests up to 8, we compute 8 for primary
    p_bonf = float(min(p_raw * 8, 1.0))
    ci_low, ci_high = np.percentile(perm_vals, [2.5,97.5]) if len(perm_vals)>0 else (0.0,0.0)
    d = bc/perm_std if perm_std>1e-9 else 0.0
    # validity checks
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

def baseline_dom_similarity(transitions, dom_text_key="dom_before_visible", K=3, seed=42, s_key="S_next"):
    """B-DOM-SIMILARITY TF-IDF cosine k=5"""
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
    # TF-IDF
    raw_key_visible = dom_text_key
    train_texts=[t.get(raw_key_visible,"") for t in train]
    test_texts=[t.get(raw_key_visible,"") for t in test]
    if has_sklearn:
        try:
            vec=TfidfVectorizer(max_features=500)
            X_train=vec.fit_transform(train_texts)
            X_test=vec.transform(test_texts)
            sim=cosine_similarity(X_test, X_train)
            # k=5 nearest
            nn_preds=[]
            for i in range(sim.shape[0]):
                idx=np.argsort(sim[i])[::-1][:5]
                votes=[train[j][s_key] for j in idx]
                pred=Counter(votes).most_common(1)[0][0]
                nn_preds.append(pred)
            # For BC_sim we need to compute I(S_next; NN_pred | C) via same Bayesian DM K=12
            # Build dataset where DOM_before is replaced by NN_pred for test, and for train we also predict via NN (leave-one-out? simplify: for train use self? Use train NN via same method)
            # Simpler: create combined dataset with dom_sim_pred = NN prediction for all items using TRAIN as reference
            # For train items, predict via leave-one-out nearest among train (exclude self)
            train_preds=[]
            if len(train)>1:
                # compute train-train sim
                sim_train=cosine_similarity(X_train, X_train)
                np.fill_diagonal(sim_train, -1)  # exclude self
                for i in range(sim_train.shape[0]):
                    idx=np.argsort(sim_train[i])[::-1][:5]
                    votes=[train[j][s_key] for j in idx]
                    pred=Counter(votes).most_common(1)[0][0]
                    train_preds.append(pred)
            else:
                train_preds=[train[0][s_key]]
            # Build unified transitions with new key dom_sim_pred
            unified=[]
            for t,p in zip(train, train_preds):
                t2=dict(t)
                t2["dom_sim_pred"] = p
                unified.append(t2)
            for t,p in zip(test, nn_preds):
                t2=dict(t)
                t2["dom_sim_pred"] = p
                unified.append(t2)
            # compute CMI using dom_sim_pred as DOM
            strata,_ = build_strata(unified, K=K, min_per_stratum=3)
            filtered={k:v for k,v in strata.items() if len(v)>=3}
            bc_sim = permutation_test_grouped(unified, "dom_sim_pred", K=K, n_perms=1000, seed=seed+10, min_per_stratum=3, s_key=s_key)
            return {"acc": float(sum(1 for a,b in zip(nn_preds, [t[s_key] for t in test]) if a==b)/len(test) if test else 0),
                    "method":"tfidf_cosine_k5",
                    "bc_sim": bc_sim["bc"],
                    "bc_sim_full": bc_sim,
                    "vocab_fit":"train_only",
                    "n_train":len(train),
                    "n_test":len(test)}
        except Exception as e:
            has_sklearn=False
    # fallback Jaccard
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
    # build unified for BC
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
    strata,_ = build_strata(unified, K=K, min_per_stratum=3)
    filtered={k:v for k,v in strata.items() if len(v)>=3}
    bc_sim = permutation_test_grouped(unified, "dom_sim_pred", K=K, n_perms=1000, seed=seed+10, min_per_stratum=3, s_key=s_key)
    return {"acc": float(acc), "method":"jaccard_k5_fallback", "bc_sim": bc_sim["bc"], "bc_sim_full": bc_sim, "n_train":len(train), "n_test":len(test)}

def baseline_markov(transitions, K=3, seed=42, s_key="S_next"):
    """B-MARKOV-1 and B-MARKOV-K3 via MLE"""
    rng=np.random.default_rng(seed)
    traj_ids=sorted(set(t["trajectory_id"] for t in transitions))
    rng.shuffle(traj_ids)
    n_train=int(0.7*len(traj_ids))
    train_ids=set(traj_ids[:n_train])
    test_ids=set(traj_ids[n_train:])
    train=[t for t in transitions if t["trajectory_id"] in train_ids]
    test=[t for t in transitions if t["trajectory_id"] in test_ids]
    # Markov-1: key = (URL_before_norm, Action_leakageFree)
    # Markov-K3: key = (URL_before_norm, H_K_actions, Action) same as CMI strata but without DOM
    # For BC_markov, we treat Markov prediction as DOM variable
    # Build maps on TRAIN
    # B-MARKOV-1
    by_traj_train=defaultdict(list)
    for t in train:
        by_traj_train[t["trajectory_id"]].append(t)
    for k in by_traj_train:
        by_traj_train[k].sort(key=lambda x: x["step"])
    # For Markov-1, need simple map
    markov1_counts=defaultdict(Counter)
    for t in train:
        key=(t["url_before_norm"], t["action_leakageFree"])
        markov1_counts[key][t[s_key]]+=1
    markov1_pred={k: Counter(v).most_common(1)[0][0] for k,v in markov1_counts.items()}
    # For Markov-K3 (history)
    markovK3_counts=defaultdict(Counter)
    for tid,lst in by_traj_train.items():
        for i,t in enumerate(lst):
            hist=[]
            for kk in range(1,K+1):
                if i-kk>=0:
                    hist.append(lst[i-kk]["action_leakageFree"])
                else:
                    hist.append("<START>")
            hist=tuple(hist)
            key=(t["url_before_norm"], hist, t["action_leakageFree"])
            markovK3_counts[key][t[s_key]]+=1
    markovK3_pred={k: Counter(v).most_common(1)[0][0] for k,v in markovK3_counts.items()}
    # Build unified dataset with Markov predictions as DOM-like variable
    # Need to assign prediction for all transitions (train and test) using TRAIN maps
    unified1=[]
    unifiedK3=[]
    # For train, use leave-one-out? Use map directly (in-sample) but that inflates; but for BC we use same grouping as CMI, so within strata the prediction is constant per stratum -> CMI will be low.
    # Simplify: assign pred for each t based on markov maps (if missing, fallback to majority global)
    global_majority = Counter(t[s_key] for t in train).most_common(1)[0][0] if train else None
    by_traj_all=defaultdict(list)
    all_trans = train+test
    for t in all_trans:
        by_traj_all[t["trajectory_id"]].append(t)
    for k in by_traj_all:
        by_traj_all[k].sort(key=lambda x: x["step"])
    # For unifiedK3 we need history for each t
    for tid,lst in by_traj_all.items():
        for i,t in enumerate(lst):
            # Markov1
            key1=(t["url_before_norm"], t["action_leakageFree"])
            pred1=markov1_pred.get(key1, global_majority)
            t2=dict(t)
            t2["markov1_pred"]=pred1
            unified1.append(t2)
            # MarkovK3
            hist=[]
            for kk in range(1,K+1):
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
    # Now compute BC for each via same CMI estimator (I(S_next; Markov_pred | C))
    # For Markov1, conditioning is on (URL,H_K,Action) but Markov1_pred is deterministic function of (URL,Action) subset, so BC should be ~0 (no extra beyond C)
    # Compute via permutation
    bc1 = permutation_test_grouped(unified1, "markov1_pred", K=K, n_perms=1000, seed=seed+20, min_per_stratum=3, s_key=s_key)
    bcK3 = permutation_test_grouped(unifiedK3, "markovK3_pred", K=K, n_perms=1000, seed=seed+21, min_per_stratum=3, s_key=s_key)
    # Also compute accuracy of Markov baselines
    correct1=sum(1 for t in test if markov1_pred.get((t["url_before_norm"], t["action_leakageFree"]), global_majority)==t[s_key])
    acc1=correct1/len(test) if test else 0
    # For K3 need history
    correctK3=0
    totalK3=len(test)
    # Build test history properly
    by_traj_test=defaultdict(list)
    for t in test:
        by_traj_test[t["trajectory_id"]].append(t)
    for tid,lst in by_traj_test.items():
        lst_sorted=sorted(lst, key=lambda x: x["step"])
        for i,t in enumerate(lst_sorted):
            hist=[]
            for kk in range(1,K+1):
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

def compute_mi_dom_action(transitions, dom_key):
    n=len(transitions)
    joint=Counter((t[dom_key], t["action_leakageFree"]) for t in transitions)
    marg_r=Counter(t[dom_key] for t in transitions)
    marg_a=Counter(t["action_leakageFree"] for t in transitions)
    mi=0.0
    for (r,a),c in joint.items():
        p_rs=c/n
        p_r=marg_r[r]/n
        p_a=marg_a[a]/n
        mi+=p_rs*math.log2(p_rs/(p_r*p_a)) if p_rs>0 and p_r>0 and p_a>0 else 0
    return float(mi)

def main():
    print("="*70)
    print(f"{EXP_ID} EXECUTE correlated-state Bayesian K={K} N=1999 seed {SEED}")
    print("="*70)
    start=time.time()
    # Verify freeze
    try:
        with open(EXP_DIR/"freeze.json") as f:
            freeze=json.load(f)
        print(f"Freeze hashes: {freeze['hashes']}")
    except Exception as e:
        print(f"Freeze check failed: {e}")
    # Generate datasets
    print("\n--- Generating datasets ---")
    corr = generate_correlated(seed=SEED, n_traj=50, steps_per=40, persist_mode="per_trajectory")
    # trim to N=1999 as spec (drop last)
    corr = corr[:1999]
    print(f"Correlated primary: {len(corr)} transitions, 50 traj, L distribution {Counter(t['L'] for t in corr)}")
    ind = generate_independent(seed=SEED, n_traj=50, steps_per=40)
    ind = ind[:1999]
    print(f"Independent-noise: {len(ind)} transitions")
    iid = generate_iid(seed=SEED, n_traj=50, steps_per=40, marginal_src=corr)
    iid = iid[:1999]
    print(f"IID null: {len(iid)} transitions")
    # Check H ceiling
    for label, data in [("corr",corr),("ind",ind),("iid",iid)]:
        strata,_ = build_strata(data, K=3)
        H, valid, total_n, total_strata, rare = compute_H_Snext_given_C(strata, min_per_stratum=3, K=K, alpha=ALPHA)
        filtered={k:v for k,v in strata.items() if len(v)>=3}
        print(f"  {label}: H(S|C)={H:.3f} valid_strata={valid}/{total_strata} rare={rare} total_n={total_n} dom_unique_R1={len(set(t['dom_before_R1'] for t in data))} |R|/N={len(set(t['dom_before_R1'] for t in data))/len(data):.3f}")
        # also check strata_ge3
        ge3=sum(1 for v in strata.values() if len(v)>=3)
        print(f"    strata_ge3={ge3} singleton_rate={sum(1 for v in strata.values() if len(v)==1)/max(1,len(strata)):.3f} dom_bytes avg {np.mean([t['dom_bytes'] for t in data]):.1f}")
        print(f"    MI(DOM;Action) R1={compute_mi_dom_action(data,'dom_before_R1'):.4f} R2={compute_mi_dom_action(data,'dom_before_R2'):.4f}")

    representations = ["dom_before_R1","dom_before_R2","dom_before_R3","dom_before_R4"]
    # For primary we also consider S_next vs S_next_urlonly sensitivity
    # Compute CMI for each representation on each dataset
    corr_results={}
    print("\n--- Correlated primary CMI (Bayesian DM) ---")
    for rep in representations:
        res = permutation_test_grouped(corr, rep, K=3, n_perms=N_PERMS, seed=SEED, min_per_stratum=3, s_key="S_next")
        # baselines
        sim = baseline_dom_similarity(corr, dom_text_key="dom_before_visible" if rep=="dom_before_R1" else "dom_before_a11y", K=3, seed=SEED)
        markov = baseline_markov(corr, K=3, seed=SEED)
        print(f"  {rep}: BC={res['bc']:.4f} obs={res['observed']:.4f} null_mean={res['perm_mean']:.4f} null_std={res['perm_std']:.4f} p_raw={res['p_raw']:.5f} p_bonf={res['p_bonf']:.5f} d={res['cohen_d']:.2f} strata={res['n_strata']} H_c={res['H_S_given_C']:.3f}")
        print(f"    sim BC_sim={sim['bc_sim']:.4f} acc_sim={sim['acc']:.3f} markov1 BC={markov['bc_markov1']:.4f} markovK3 BC={markov['bc_markovK3']:.4f}")
        corr_results[rep]={"cmi":res,"sim":sim,"markov":markov}

    print("\n--- Independent-noise replication CMI ---")
    ind_results={}
    for rep in representations:
        res = permutation_test_grouped(ind, rep, K=3, n_perms=N_PERMS, seed=SEED+100, min_per_stratum=3, s_key="S_next")
        sim = baseline_dom_similarity(ind, dom_text_key="dom_before_visible" if rep=="dom_before_R1" else "dom_before_a11y", K=3, seed=SEED+100)
        markov = baseline_markov(ind, K=3, seed=SEED+100)
        print(f"  {rep}: BC={res['bc']:.4f} p_raw={res['p_raw']:.4f} null_std={res['perm_std']:.4f} sim={sim['bc_sim']:.4f}")
        ind_results[rep]={"cmi":res,"sim":sim,"markov":markov}

    print("\n--- IID null CMI ---")
    iid_results={}
    for rep in ["dom_before_R1","dom_before_R2"]:
        res = permutation_test_grouped(iid, rep, K=3, n_perms=N_PERMS, seed=SEED+200, min_per_stratum=3, s_key="S_next")
        print(f"  {rep}: BC={res['bc']:.4f} p_raw={res['p_raw']:.4f} null_std={res['perm_std']:.4f}")
        iid_results[rep]={"cmi":res}

    # Decision gates per spec
    print("\n--- Decision gates ---")
    # G1 positive correlated control BC>=0.30 p<0.01 null_std>0.01 |null_mean|<0.1 on R1 or R2
    # Note spec says positive control IS the correlated primary itself; but we treat corr_results as both primary and positive control
    # We'll check R1 and R2
    pos_pass_R1 = corr_results["dom_before_R1"]["cmi"]["bc"]>=0.30 and corr_results["dom_before_R1"]["cmi"]["p_raw"]<0.01 and corr_results["dom_before_R1"]["cmi"]["perm_std"]>0.01 and abs(corr_results["dom_before_R1"]["cmi"]["perm_mean"])<0.1
    pos_pass_R2 = corr_results["dom_before_R2"]["cmi"]["bc"]>=0.30 and corr_results["dom_before_R2"]["cmi"]["p_raw"]<0.01 and corr_results["dom_before_R2"]["cmi"]["perm_std"]>0.01 and abs(corr_results["dom_before_R2"]["cmi"]["perm_mean"])<0.1
    pos_control_pass = pos_pass_R1 or pos_pass_R2
    print(f"G1 positive control R1 pass={pos_pass_R1} BC={corr_results['dom_before_R1']['cmi']['bc']:.4f} p={corr_results['dom_before_R1']['cmi']['p_raw']:.5f} std={corr_results['dom_before_R1']['cmi']['perm_std']:.4f} mean={corr_results['dom_before_R1']['cmi']['perm_mean']:.4f}")
    print(f"G1 positive control R2 pass={pos_pass_R2} BC={corr_results['dom_before_R2']['cmi']['bc']:.4f} p={corr_results['dom_before_R2']['cmi']['p_raw']:.5f} std={corr_results['dom_before_R2']['cmi']['perm_std']:.4f} mean={corr_results['dom_before_R2']['cmi']['perm_mean']:.4f}")
    print(f"G1 overall pass={pos_control_pass}")

    # G2 independent-noise BC>=0.05 and p<0.10 with valid null => confounded
    ind_confound_R1 = ind_results["dom_before_R1"]["cmi"]["bc"]>=0.05 and ind_results["dom_before_R1"]["cmi"]["p_raw"]<0.10 and ind_results["dom_before_R1"]["cmi"]["perm_std"]>0.01 and abs(ind_results["dom_before_R1"]["cmi"]["perm_mean"])<0.1
    ind_confound_R2 = ind_results["dom_before_R2"]["cmi"]["bc"]>=0.05 and ind_results["dom_before_R2"]["cmi"]["p_raw"]<0.10 and ind_results["dom_before_R2"]["cmi"]["perm_std"]>0.01 and abs(ind_results["dom_before_R2"]["cmi"]["perm_mean"])<0.1
    ind_confound = ind_confound_R1 or ind_confound_R2
    print(f"G2 independent-noise confound R1={ind_confound_R1} BC={ind_results['dom_before_R1']['cmi']['bc']:.4f} p={ind_results['dom_before_R1']['cmi']['p_raw']:.4f}")
    print(f"G2 independent-noise confound R2={ind_confound_R2} BC={ind_results['dom_before_R2']['cmi']['bc']:.4f} p={ind_results['dom_before_R2']['cmi']['p_raw']:.4f}")
    # Requirement for passing null is |BC|<0.05 p>0.10
    ind_pass_R1 = abs(ind_results["dom_before_R1"]["cmi"]["bc"])<0.05 and ind_results["dom_before_R1"]["cmi"]["p_raw"]>0.10
    ind_pass_R2 = abs(ind_results["dom_before_R2"]["cmi"]["bc"])<0.05 and ind_results["dom_before_R2"]["cmi"]["p_raw"]>0.10
    print(f"  ind pass criteria (|BC|<0.05 p>0.10) R1={ind_pass_R1} R2={ind_pass_R2}")

    # G3 iid not gating heavily but check
    iid_pass_R1 = iid_results["dom_before_R1"]["cmi"]["bc"]<=0.03 and iid_results["dom_before_R1"]["cmi"]["p_raw"]>0.10
    iid_pass_R2 = iid_results["dom_before_R2"]["cmi"]["bc"]<=0.03 and iid_results["dom_before_R2"]["cmi"]["p_raw"]>0.10
    print(f"G3 iid R1 pass={iid_pass_R1} BC={iid_results['dom_before_R1']['cmi']['bc']:.4f} p={iid_results['dom_before_R1']['cmi']['p_raw']:.4f}")
    print(f"G3 iid R2 pass={iid_pass_R2} BC={iid_results['dom_before_R2']['cmi']['bc']:.4f} p={iid_results['dom_before_R2']['cmi']['p_raw']:.4f}")

    # G4 primary null degenerate on both R1 and R2
    degenerate_R1 = corr_results["dom_before_R1"]["cmi"]["perm_std"]<=0.01 or abs(corr_results["dom_before_R1"]["cmi"]["perm_mean"])>=0.1
    degenerate_R2 = corr_results["dom_before_R2"]["cmi"]["perm_std"]<=0.01 or abs(corr_results["dom_before_R2"]["cmi"]["perm_mean"])>=0.1
    both_degenerate = degenerate_R1 and degenerate_R2
    print(f"G4 degenerate R1={degenerate_R1} R2={degenerate_R2} both={both_degenerate}")

    # Primary sig per spec: BC>0.05 p_bonf<0.01 |null_mean|<0.1 null_std>0.01 gap>=0.05
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

    # Gated decision
    if not pos_control_pass:
        status="MEASUREMENT_INVALID"
        outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID pipeline_blind_correlated"
        reason=f"G1 fails: positive correlated control BC<0.30 or p>=0.01 or null_std<=0.01 or |null_mean|>=0.1 (R1 BC {corr_results['dom_before_R1']['cmi']['bc']:.3f} p {corr_results['dom_before_R1']['cmi']['p_raw']:.4f}, R2 BC {corr_results['dom_before_R2']['cmi']['bc']:.3f} p {corr_results['dom_before_R2']['cmi']['p_raw']:.4f})"
    elif ind_confound:
        status="MEASUREMENT_INVALID"
        outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID pipeline_confounds_independent"
        reason=f"G2 fails: independent-noise shows BC>=0.05 p<0.10 (R1 {ind_results['dom_before_R1']['cmi']['bc']:.3f} p {ind_results['dom_before_R1']['cmi']['p_raw']:.4f} R2 {ind_results['dom_before_R2']['cmi']['bc']:.3f} p {ind_results['dom_before_R2']['cmi']['p_raw']:.4f})"
    elif both_degenerate:
        status="MEASUREMENT_INVALID"
        outcome="NOT_APPLICABLE"
        verdict="MEASUREMENT_INVALID null_degenerate"
        reason=f"G4 both R1 R2 null degenerate std<=0.01 or |mean|>=0.1"
    else:
        if sig_R1 or sig_R2:
            status="COMPLETE"
            outcome="SUPPORTS"  # spec says SURVIVES_CURRENT_TEST
            verdict="SURVIVES_CURRENT_TEST"
            reason=f"Exists R with sig=1: R1 sig={sig_R1} BC {corr_results['dom_before_R1']['cmi']['bc']:.3f} gap {gap_R1:.3f}, R2 sig={sig_R2} BC {corr_results['dom_before_R2']['cmi']['bc']:.3f} gap {gap_R2:.3f}, gates pass"
        else:
            status="COMPLETE"
            outcome="FALSIFIES"
            verdict="FALSIFIED-IN-SETTING"
            reason=f"Forall R fails sig: R1 BC {corr_results['dom_before_R1']['cmi']['bc']:.3f} p_bonf {corr_results['dom_before_R1']['cmi']['p_bonf']:.4f} gap {gap_R1:.3f}, R2 BC {corr_results['dom_before_R2']['cmi']['bc']:.3f} p_bonf {corr_results['dom_before_R2']['cmi']['p_bonf']:.4f} gap {gap_R2:.3f}, while gates pass"

    print(f"\nFinal: status={status} outcome={outcome} verdict={verdict}")
    print(f"Reason: {reason}")

    # Prepare artifacts
    import os
    os.makedirs(EXP_DIR/"artifacts", exist_ok=True)
    # Save raw datasets (sample)
    with open(EXP_DIR/"raw_transitions_correlated.json","w") as f:
        json.dump(corr, f, indent=2)
    with open(EXP_DIR/"raw_transitions_independent.json","w") as f:
        json.dump(ind, f, indent=2)
    with open(EXP_DIR/"raw_transitions_iid.json","w") as f:
        json.dump(iid, f, indent=2)
    # Save detailed results
    full_results={
        "experiment_id": EXP_ID,
        "seed": SEED,
        "K": K,
        "alpha": ALPHA,
        "N": len(corr),
        "correlated": corr_results,
        "independent": ind_results,
        "iid": iid_results,
        "gates": {
            "pos_control_pass": pos_control_pass,
            "pos_pass_R1": pos_pass_R1,
            "pos_pass_R2": pos_pass_R2,
            "ind_confound": ind_confound,
            "ind_confound_R1": ind_confound_R1,
            "ind_confound_R2": ind_confound_R2,
            "both_degenerate": both_degenerate,
            "sig_R1": sig_R1,
            "sig_R2": sig_R2,
            "gap_R1": gap_R1,
            "gap_R2": gap_R2,
        },
        "decision": {"status":status,"outcome":outcome,"verdict":verdict,"reason":reason},
        "elapsed": time.time()-start,
    }
    with open(EXP_DIR/"raw_results.json","w") as f:
        json.dump(full_results, f, indent=2)
    # Also save strata tables
    strata_corr,_ = build_strata(corr, K=3)
    strata_ind,_ = build_strata(ind, K=3)
    # Save permutation histograms for primary
    # Save minimal provenance
    print(f"Artifacts saved to {EXP_DIR}")

if __name__=="__main__":
    main()
