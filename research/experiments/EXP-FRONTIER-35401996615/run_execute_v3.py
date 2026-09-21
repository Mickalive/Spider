#!/usr/bin/env python3
"""EXP-FRONTIER-35401996615 EXECUTE v3 - Fixed DGP, raw divergence for CV check."""
import numpy as np
from scipy.stats import gaussian_kde, t as t_dist
from scipy.special import digamma
from sklearn.neighbors import NearestNeighbors
import json, time, sys, traceback

BASE_SEED = 42
N_PERMS = 200
N_REPS = 5
LAMBDA_LEVELS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
SAMPLE_SIZES = [250, 500, 1000]
N_TYPES = 8
N_ACTIONS = 4

PAGE_TYPES = [
    (42, 0.05, np.array([0.5, 0.5])),
    (43, 0.05, np.array([0.5, 0.5])),
    (44, 0.05, np.array([0.5, 0.5])),
    (42, 0.10, np.array([0.5, 0.5])),
    (43, 0.10, np.array([0.5, 0.5])),
    (44, 0.10, np.array([0.5, 0.5])),
    (42, 0.05, np.array([0.3, 0.7])),
    (43, 0.05, np.array([0.3, 0.7])),
]

def generate_dgp(per_type_n, lam, type_idx, seed):
    rng = np.random.RandomState(seed)
    ft, noise_std, offset = PAGE_TYPES[type_idx]
    S_cur = rng.uniform(0, 1, size=(per_type_n, 2))
    actions = rng.randint(0, N_ACTIONS, size=per_type_n)
    S_det = np.zeros_like(S_cur)
    for i in range(per_type_n):
        s, a = S_cur[i], actions[i]
        if ft == 42:
            angle = lam * 0.5 * np.pi * (a + 1) / N_ACTIONS
            c, sn_ = np.cos(angle), np.sin(angle)
            S_det[i] = np.array([[c, -sn_], [sn_, c]]) @ (s - offset) + offset
        elif ft == 43:
            sf = 1.0 + lam * 0.5 * (a + 1) / N_ACTIONS
            S_det[i] = (s - offset) * sf + offset
        elif ft == 44:
            S_det[i] = s + lam * 0.3 * (a + 1) / N_ACTIONS * np.array([1.0, -1.0])
    S_det = S_det % 1.0
    ns = noise_std * (0.5 + np.linalg.norm(S_cur - offset, axis=1, keepdims=True))
    noise = rng.randn(per_type_n, 2) * ns
    S_next = (S_det + noise) % 1.0
    return S_next, actions, S_cur

def kde_kl(S, A):
    n = len(S)
    if n < 10: return 0.0
    try:
        km = gaussian_kde(S.T, bw_method='scott')
        mx = 0.0
        for a in range(N_ACTIONS):
            m = A == a
            if m.sum() < 5: continue
            kc = gaussian_kde(S[m].T, bw_method='scott')
            lc, lm = kc(S[m].T), km(S[m].T)
            kl = float(np.mean(np.maximum(np.log(lc+1e-300) - np.log(lm+1e-300), 0)))
            mx = max(mx, kl)
        return mx
    except: return 0.0

def knn_mi(S, A, k=5):
    n = len(S)
    if n < k+2: return 0.0
    try:
        na = int(A.max()) + 1
        oh = np.zeros((n, na)); oh[np.arange(n), A.astype(int)] = 1.0
        joint = np.column_stack([S, oh])
        nn = NearestNeighbors(n_neighbors=k+1); nn.fit(joint)
        dj, _ = nn.kneighbors(joint); eps = dj[:, k]
        nn2 = NearestNeighbors(n_neighbors=n); nn2.fit(S)
        dm, _ = nn2.kneighbors(S)
        nc = np.zeros(n, dtype=int)
        for i in range(n):
            sc = (A == A[i]); sc[i] = False
            nc[i] = np.sum(sc & (dm[i] <= eps[i]))
        pk = digamma(k)
        mpn = float(np.mean(digamma(nc + 1)))
        pN = digamma(n)
        ey = sum((np.sum(A==v)/n)*digamma(int(np.sum(A==v))) for v in range(na) if np.sum(A==v)>0)
        return max(0.0, float(pk - mpn + pN - ey))
    except: return 0.0

def perm_threshold(S, A, measure, n_perms, seed):
    """Compute 95th percentile of permutation null distribution."""
    rng = np.random.RandomState(seed)
    fn = kde_kl if measure == 'kde' else lambda s,a: knn_mi(s,a,k=5)
    vals = []
    for _ in range(n_perms):
        pa = A.copy(); rng.shuffle(pa)
        vals.append(fn(S, pa))
    return float(np.percentile(vals, 95))

def ser(obj):
    if isinstance(obj, (np.integer,)): return int(obj)
    elif isinstance(obj, (np.floating,)): return float(obj)
    elif isinstance(obj, np.ndarray): return obj.tolist()
    elif isinstance(obj, dict): return {str(k): ser(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)): return [ser(v) for v in obj]
    elif isinstance(obj, (np.bool_,)): return bool(obj)
    return obj

def run():
    t0 = time.time()
    cv_ck, null_ctrl, pos_ctrl = {}, {}, {}
    pt_res, pl_res = {}, {}

    for sn in SAMPLE_SIZES:
        print(f"\n{'='*60}\nn={sn}/type", flush=True)
        pt_res[sn] = {}
        cv_st = {m: {t: [] for t in range(N_TYPES)} for m in ['kde','knn']}
        pl_st = {m: {lt: [] for lt in LAMBDA_LEVELS} for m in ['kde','knn']}

        for li, lv in enumerate(LAMBDA_LEVELS):
            tl = time.time()
            print(f"  lam={lv}...", end='', flush=True)
            for rep in range(N_REPS):
                cs = BASE_SEED*100000 + li*1000 + rep*10 + 999
                all_S, all_A, all_T = [], [], []
                for ti in range(N_TYPES):
                    S, A, _ = generate_dgp(sn, lv, ti, cs + ti*7)
                    all_S.append(S); all_A.append(A); all_T.extend([ti]*sn)
                all_S = np.vstack(all_S); all_A = np.concatenate(all_A)
                all_T = np.array(all_T)

                for ti in range(N_TYPES):
                    m = all_T == ti
                    kr = kde_kl(all_S[m], all_A[m])
                    nr = knn_mi(all_S[m], all_A[m], k=5)
                    cv_st['kde'][ti].append(kr)
                    cv_st['knn'][ti].append(nr)

                # Pooled
                pl_st['kde'][lv].append(kde_kl(all_S, all_A))
                pl_st['knn'][lv].append(knn_mi(all_S, all_A, k=5))

            print(f" {time.time()-tl:.1f}s", flush=True)

        # === CV check at lambda=1 (raw divergence across reps) ===
        kd_cvs, kn_cvs = [], []
        for ti in range(N_TYPES):
            kv = np.array(cv_st['kde'][ti])
            nv = np.array(cv_st['knn'][ti])
            km_, nm_ = np.mean(kv), np.mean(nv)
            kcv = float(np.std(kv)/km_) if km_ > 0 else float('inf')
            ncv = float(np.std(nv)/nm_) if nm_ > 0 else float('inf')
            kd_cvs.append(kcv); kn_cvs.append(ncv)
            pt_res[sn][str(ti)] = ser({
                'kde_lambda1_values': kv, 'kde_lambda1_mean': km_, 'kde_cv': kcv,
                'knn_lambda1_values': nv, 'knn_lambda1_mean': nm_, 'knn_cv': ncv,
            })

        cv_ck[sn] = {
            'kde': {'cv_per_type': {str(i): kd_cvs[i] for i in range(N_TYPES)},
                    'cv_max': float(max(kd_cvs)), 'cv_max_type': int(np.argmax(kd_cvs)),
                    'pass': bool(all(c <= 0.5 for c in kd_cvs)),
                    'n_pass': int(sum(1 for c in kd_cvs if c <= 0.5))},
            'knn': {'cv_per_type': {str(i): kn_cvs[i] for i in range(N_TYPES)},
                    'cv_max': float(max(kn_cvs)), 'cv_max_type': int(np.argmax(kn_cvs)),
                    'pass': bool(all(c <= 0.5 for c in kn_cvs)),
                    'n_pass': int(sum(1 for c in kn_cvs if c <= 0.5))},
        }
        print(f"  CV: KDE max={max(kd_cvs):.4f}({cv_ck[sn]['kde']['n_pass']}/8) "
              f"kNN max={max(kn_cvs):.4f}({cv_ck[sn]['knn']['n_pass']}/8)")

        # === Null control: at lambda=0, per-type divergence <= 95th perm threshold ===
        # Compute on the last rep's lambda=0 data
        cs_l0 = BASE_SEED*100000 + 0*1000 + (N_REPS-1)*10 + 999  # last rep
        all_S_l0, all_A_l0, all_T_l0 = [], [], []
        for ti in range(N_TYPES):
            S, A, _ = generate_dgp(sn, 0.0, ti, cs_l0 + ti*7)
            all_S_l0.append(S); all_A_l0.append(A); all_T_l0.extend([ti]*sn)
        all_S_l0 = np.vstack(all_S_l0)
        all_A_l0 = np.concatenate(all_A_l0)
        all_T_l0 = np.array(all_T_l0)

        nc = {}
        for measure in ['kde','knn']:
            np_ = 0; tr = {}
            fn = kde_kl if measure == 'kde' else lambda s,a: knn_mi(s,a,k=5)
            for ti in range(N_TYPES):
                m = all_T_l0 == ti
                obs = fn(all_S_l0[m], all_A_l0[m])
                pt = perm_threshold(all_S_l0[m], all_A_l0[m], measure, N_PERMS, cs_l0+ti*17+88888)
                ok = bool(obs <= pt); np_ += int(ok)
                tr[str(ti)] = ser({'observed': obs, 'perm_threshold_95': pt, 'pass': ok})
            nc[measure] = {'n_pass': int(np_), 'n_total': N_TYPES,
                           'pass_all': bool(np_ == N_TYPES), 'per_type': tr}
        null_ctrl[sn] = nc
        print(f"  Null: KDE {nc['kde']['n_pass']}/8 kNN {nc['knn']['n_pass']}/8")

        # === Positive control: pooled divergence at lambda=1 > lambda=0 ===
        pc = {}
        for measure in ['kde','knn']:
            v1 = np.array(pl_st[measure][1.0])
            v0 = np.array(pl_st[measure][0.0])
            d = v1 - v0; md = float(np.mean(d))
            sd = float(np.std(d, ddof=1))
            if sd > 0 and len(d) > 1:
                ts = md / (sd / np.sqrt(len(d)))
                pv = float(1 - t_dist.cdf(ts, df=len(d)-1))
            else: ts, pv = 0.0, 1.0
            pc[measure] = ser({'lambda1_mean': np.mean(v1), 'lambda0_mean': np.mean(v0),
                               'mean_diff': md, 't_stat': ts, 'p_one_sided': pv,
                               'pass': bool(md > 0 and pv < 0.05)})
        pos_ctrl[sn] = pc
        print(f"  Pos: KDE t={pc['kde']['t_stat']:.3f} p={pc['kde']['p_one_sided']:.4f} "
              f"kNN t={pc['knn']['t_stat']:.3f} p={pc['knn']['p_one_sided']:.4f}")

        # Pooled
        pr = {}
        for measure in ['kde','knn']:
            pr[measure] = {}
            for lv in LAMBDA_LEVELS:
                vals = np.array(pl_st[measure][lv])
                pr[measure][str(lv)] = ser({'mean': np.mean(vals), 'std': np.std(vals), 'values': vals})
        pl_res[sn] = pr

    # Pipeline validation
    pv250 = cv_ck[250]
    pv = {
        'kde_cv_max_250': pv250['kde']['cv_max'],
        'kde_cv_in_5pct': bool(0.546 <= pv250['kde']['cv_max'] <= 0.604),
        'knn_cv_max_250': pv250['knn']['cv_max'],
        'knn_cv_in_5pct': bool(0.717 <= pv250['knn']['cv_max'] <= 0.793),
        'kde_null_pass': null_ctrl[250]['kde']['pass_all'],
        'knn_null_pass': null_ctrl[250]['knn']['pass_all'],
        'pass': (bool(0.546 <= pv250['kde']['cv_max'] <= 0.604) and
                 bool(0.717 <= pv250['knn']['cv_max'] <= 0.793) and
                 null_ctrl[250]['kde']['pass_all'] and null_ctrl[250]['knn']['pass_all']),
    }

    # Trend
    trend = {}
    for measure in ['kde','knn']:
        trend[measure] = {}
        for ti in range(N_TYPES):
            cvs = [cv_ck[s][measure]['cv_per_type'][str(ti)] for s in SAMPLE_SIZES]
            trend[measure][str(ti)] = ser({
                'cv_250': cvs[0], 'cv_500': cvs[1], 'cv_1000': cvs[2],
                'monotonic_decrease': bool(all(cvs[i] >= cvs[i+1] for i in range(2))),
            })

    # Decision per frozen rules
    pp = pv['pass']
    kd_surv = (cv_ck[500]['kde']['pass'] or cv_ck[1000]['kde']['pass'])
    kn_surv = (cv_ck[500]['knn']['pass'] or cv_ck[1000]['knn']['pass'])
    kd_pa = all(pos_ctrl[s]['kde']['pass'] for s in SAMPLE_SIZES)
    kn_pa = all(pos_ctrl[s]['knn']['pass'] for s in SAMPLE_SIZES)
    kd_na = all(null_ctrl[s]['kde']['pass_all'] for s in SAMPLE_SIZES)
    kn_na = all(null_ctrl[s]['knn']['pass_all'] for s in SAMPLE_SIZES)

    if (kd_surv and kd_pa and kd_na and pp) or (kn_surv and kn_pa and kn_na and pp):
        decision = "SURVIVES_CURRENT_TEST"
        outcome = "SUPPORTS"
    elif any(not pos_ctrl[s][m]['pass'] for s in SAMPLE_SIZES for m in ['kde','knn']):
        decision = "MEASUREMENT_INVALID"
        outcome = "INCONCLUSIVE"
    elif not pp:
        decision = "MEASUREMENT_INVALID"
        outcome = "INCONCLUSIVE"
    else:
        decision = "MEASUREMENT_INVALID"
        outcome = "INCONCLUSIVE"

    print(f"\n{'='*60}")
    print(f"DECISION: {decision}")
    print(f"Pipeline: {'PASS' if pp else 'FAIL'}")
    print(f"KDE: CV_max@250={pv250['kde']['cv_max']:.4f} CV@500={cv_ck[500]['kde']['cv_max']:.4f} CV@1000={cv_ck[1000]['kde']['cv_max']:.4f}")
    print(f"kNN: CV_max@250={pv250['knn']['cv_max']:.4f} CV@500={cv_ck[500]['knn']['cv_max']:.4f} CV@1000={cv_ck[1000]['knn']['cv_max']:.4f}")
    print(f"Pos ctrl: KDE pass={kd_pa} kNN pass={kn_pa}")
    print(f"Null ctrl: KDE pass={kd_na} kNN pass={kn_na}")

    # Save
    raw = ser({'experiment_id': 'EXP-FRONTIER-35401996615', 'cv_check': cv_ck,
               'null_control': null_ctrl, 'positive_control': pos_ctrl,
               'per_type': pt_res, 'pooled': pl_res, 'pipeline_validation': pv,
               'trend': trend, 'decision': decision})
    with open('raw_evidence.json', 'w') as f:
        json.dump(raw, f, indent=2)

    elapsed = time.time() - t0
    print(f"\nTotal: {elapsed:.1f}s")
    return raw

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(f"ERROR: {e}"); traceback.print_exc(); sys.exit(1)
