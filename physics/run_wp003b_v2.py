"""WP-003B-v2: action-conditioned next-state structural prediction.

Preregistered analysis (reports/physics/wp003b_v2_preregistration.md, frozen
before data collection). Target = coarse structural signature of s_{t+1}
defined a priori; predictors = mechanics-only Z(s_t) + imposed action a_t;
holdout unit = website (leave-one-site-out); uncertainty = trajectory-grouped
bootstrap; strong nulls include conditional-frequency and nearest-neighbour
memory baselines. No post-hoc class filtering: class space is fixed by design
thresholds, and all preprocessing is fit on TRAIN folds only.
"""
import argparse
import hashlib
import json
import os
import subprocess
from collections import Counter, defaultdict

import numpy as np

from physics.run_wp003 import FEATURES, onehot, softmax_reg, balanced_acc, validate_rows

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_IN = "/tmp/opencode/spider_data/wp003b_v2_transitions.jsonl"
RAW_DIR = "/tmp/opencode/spider_data/raw"
RESULTS_DIR = os.path.join(REPO, "results", "physics")
N_BOOT = 2000
BOOT_SEED = 20260824


# ---------------------------------------------------------------- loading
def load_rows(path, skip_chaining=False):
    """skip_chaining=True is ONLY for counterfactual control corpora (e.g.
    permuted-action E-1) where trajectory chaining is intentionally broken.
    Real collected data must always use the default full validation."""
    total = 0
    excluded = 0
    kept = []
    raw = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            total += 1
            # Deviation D2 (documented pre-analysis): the collector persists
            # `any_ok` and chain length but not per-action ok flags, so the
            # frozen rule "exclude if FIRST action failed" is operationalized
            # as "exclude single-action chains whose only action failed"
            # (unambiguous first-action failure). Multi-chain rows with
            # any_ok=False are retained and flagged as a limitation.
            labs = r.get("action_labels") or []
            drop = len(labs) == 1 and not r.get("any_ok", True)
            for k in FEATURES:
                assert k in r.get("pre", {}), f"pre-state field absent: {k}"
            assert "post" in r and r["post"], "row without post-state"
            r["x"] = [r["pre"][k] for k in FEATURES]
            raw.append(r)
            if drop:
                excluded += 1
            else:
                kept.append(r)

    # Integrity assertions run on the FULL collected corpus (exclusions must
    # never mask collection defects), then filtering applies for analysis.
    if skip_chaining:
        from physics.run_wp003 import FEATURES as _F
        assert raw
        for r in raw:
            missing = {"site", "trajectory_id", "step_id", "target_action",
                       "prev_action_label", "primary_action", "pre", "post"} - set(r)
            assert not missing, f"missing fields {missing}"
            assert r["target_action"] == r["primary_action"]
    else:
        validate_rows(raw)

    # v2 anti-leak guard: predictors derive from pre-state + intended action
    # only; both are fixed strictly before the outcome exists.
    for r in kept:
        assert r["primary_action"] in ("click_link", "click_button", "fill_text",
                                       "fill_password", "select_option",
                                       "check_box"), r["primary_action"]
        chain_len = len(r.get("action_labels") or [])
        assert chain_len >= 1
    stats = {"total_lines": total,
             "excluded_first_action_failed": excluded,
             "usable": len(kept),
             "n_trajectories": len({r["trajectory_id"] for r in kept})}
    return kept, stats


# ---------------------------------------------------------------- targets
def t1_signature(post):
    return f"lb{post['link_bucket']}.f{1 if post['form_bucket'] > 0 else 0}"


COMPONENT_TARGETS = {
    "link_bucket": lambda p: f"lb{p['link_bucket']}",
    "form_present": lambda p: "1" if p["form_bucket"] > 0 else "0",
    "text_input_bucket": lambda p: f"ib{p['text_input_bucket']}",
    "has_password": lambda p: str(p["has_password"]),
}


def alt_signature(counts_post):
    """Representation ablation target: alternate legitimate thresholds."""
    n = counts_post["links"]
    lb = 0 if n < 5 else (1 if n < 30 else 2)
    return f"alb{lb}.f{1 if counts_post['forms'] > 0 else 0}"


def alt_state_feats(rec):
    """Alternate legitimate predictor re-binning from raw counts (prereg S-B).

    links {<5,5-29,>=30}; buttons/text_inputs/forms {0,1-2,>=3}. All other
    state dimensions identical to the primary representation."""
    cp = rec["counts_pre"]
    b3 = lambda n: 0 if n == 0 else (1 if n <= 2 else 2)
    x = list(rec["x"])  # primary 13 dims
    # indices in FEATURES: 0 link_bucket,1 button_bucket,2 text_input_bucket,8 form_bucket
    x[0] = 0 if cp["links"] < 5 else (1 if cp["links"] < 30 else 2)
    x[1] = b3(cp["buttons"])
    x[2] = b3(cp["text_inputs"])
    x[8] = b3(cp["forms"])
    return x


def alt_onehot(X):
    """One-hot for alternate representation: buckets at cols 0,1,2,8,9,10,12
    have 3 levels each (same spec as primary), rest numeric."""
    cols, names = [], []
    spec = {0: 3, 1: 3, 2: 3, 8: 3, 9: 3, 10: 3, 12: 3}
    for i in range(X.shape[1]):
        if i in spec:
            for k in range(spec[i]):
                cols.append([1.0 if row[i] == k else 0.0 for row in X])
                names.append(f"c{i}={k}")
        else:
            cols.append([float(row[i]) for row in X])
            names.append(f"c{i}")
    return np.array(cols).T, names


# ---------------------------------------------------------------- design matrix
def action_cols(rows):
    classes = sorted({r["primary_action"] for r in rows})
    idx = {a: i for i, a in enumerate(classes)}
    Z = np.zeros((len(rows), len(classes) + 1))
    for i, r in enumerate(rows):
        Z[i, idx[r["primary_action"]]] = 1.0
        Z[i, -1] = 1.0 if len(r.get("action_labels") or []) > 1 else 0.0
    names = [f"a={a}" for a in classes] + ["chain_gt1"]
    return Z, names


def build_X(rows, feats=None):
    if feats is None:
        src = [r["x"] for r in rows]
    else:
        src = feats
    Xs, names = onehot(src)
    Xa, anames = action_cols(rows)
    X = np.concatenate([Xs, Xa], axis=1)
    return X, names + anames, Xs.shape[1]


# ---------------------------------------------------------------- nulls
def null_predictions(rows_tr, rows_te, ytr, n_te):
    """Return dict of null prediction arrays on test rows (fit on train only)."""
    n_te = int(n_te)
    maj = Counter(ytr.tolist()).most_common(1)[0][0]

    # N0 global train majority
    p0 = np.full(n_te, maj, dtype=int)

    # N3 action-conditional train majority
    by_act = defaultdict(Counter)
    for r, y in zip(rows_tr, ytr):
        by_act[r["primary_action"]][y] += 1
    p3 = []
    for r in rows_te:
        c = by_act.get(r["primary_action"])
        p3.append(c.most_common(1)[0][0] if c else maj)
    p3 = np.array(p3, dtype=int)

    # N5 coarse conditional frequency: cell=(depth_bucket, link_bucket, action)
    cell = defaultdict(Counter)
    by_act_b = defaultdict(Counter)
    for r, y in zip(rows_tr, ytr):
        k = (r["pre"]["depth_bucket"], r["pre"]["link_bucket"], r["primary_action"])
        cell[k][y] += 1
        by_act_b[r["primary_action"]][y] += 1
    p5 = []
    for r in rows_te:
        k = (r["pre"]["depth_bucket"], r["pre"]["link_bucket"], r["primary_action"])
        c = cell.get(k) or by_act_b.get(r["primary_action"])
        p5.append(c.most_common(1)[0][0] if c else maj)
    p5 = np.array(p5, dtype=int)
    return {"N0_majority": p0, "N3_action_cond": p3, "N5_cellfreq": p5}


def nn_predictions(Xtr, ytr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xt, Xs = (Xtr - mu) / sd, (Xte - mu) / sd
    idx = np.array([int((((Xt - x) ** 2).sum(1)).argmin()) for x in Xs])
    return ytr[idx]


# ---------------------------------------------------------------- fold engine
def add_interactions(X, n_state_cols):
    """Exploratory interaction-augmented design: action indicators × state
    one-hot columns (linear model cannot express conjunctions otherwise)."""
    acts = X[:, n_state_cols:-1]  # action block without chain flag
    state = X[:, :n_state_cols]
    inter = np.einsum("ni,nj->nij", acts, state).reshape(len(X), -1)
    return np.concatenate([X, inter], axis=1)


def run_folds(rows, target_fn, feats_fn=None, onehot_fn=onehot,
              interactions=False, row_level_target=False):
    """Website-holdout evaluation. Returns folds detail + bootstrap raw."""
    lab_of = (target_fn if row_level_target else (lambda r: target_fn(r["post"])))
    labels = sorted({lab_of(r) for r in rows})
    Y = {c: i for i, c in enumerate(labels)}
    yall = np.array([Y[lab_of(r)] for r in rows])
    if feats_fn is None:
        X, feat_names, n_state_cols = build_X(rows)
    else:
        Xraw = np.array([feats_fn(i, r) for i, r in enumerate(rows)], dtype=float)
        Xs, names = onehot_fn(Xraw)
        Xa, anames = action_cols(rows)
        X = np.concatenate([Xs, Xa], axis=1)
        feat_names = names + anames
        n_state_cols = Xs.shape[1]
    if interactions:
        n_before = X.shape[1]
        X = add_interactions(X, n_state_cols)
        feat_names = feat_names + [f"ix_{i}" for i in range(X.shape[1] - n_before)]
    sites = sorted({r["site"] for r in rows})
    classes = np.arange(len(labels))

    folds, fold_raw = {}, []
    for hold in sites:
        te = np.array([i for i, r in enumerate(rows) if r["site"] == hold])
        tr = np.array([i for i, r in enumerate(rows) if r["site"] != hold])
        rows_te = [rows[i] for i in te]
        rows_tr = [rows[i] for i in tr]
        tids = np.array([r["trajectory_id"] for r in rows_te], dtype=object)
        fold = {
            "n_test": int(len(te)),
            "n_train": int(len(tr)),
            "n_trajectories": int(len(set(tids.tolist()))),
        }
        yte, ytr = yall[te], yall[tr]

        W = softmax_reg(X[tr], ytr, len(labels))
        pm = (X[te] @ W).argmax(1)
        nulls = null_predictions(rows_tr, rows_te, ytr, len(te))
        nulls["N4_nearest_neighbor"] = nn_predictions(X[tr], ytr, X[te])

        scores_m = balanced_acc(yte, pm, classes)
        scores_n = {k: balanced_acc(yte, p, classes) for k, p in nulls.items()}
        best_null = max(scores_n, key=scores_n.get)
        best_val = scores_n[best_null]
        fold.update({
            "M_model": round(float(scores_m), 4),
            **{k: round(float(v), 4) for k, v in scores_n.items()},
            "best_null_name": best_null,
            "best_null": round(float(best_val), 4),
            "d_effect": round(float(scores_m - best_val), 4),
            "test_class_counts": {labels[c]: int((yte == c).sum())
                                  for c in np.unique(yte)},
        })
        percls = {}
        for c in np.unique(yte):
            m = yte == c
            percls[labels[int(c)]] = {
                "support": int(m.sum()),
                "recall_M": round(float((pm[m] == c).mean()), 4),
                **{k: round(float((nulls[k][m] == c).mean()), 4) for k in nulls},
            }
        fold["per_class"] = percls
        folds[hold] = fold
        fold_raw.append({"yte": yte, "pm": pm,
                         "nulls": {k: v for k, v in nulls.items()},
                         "tids": tids, "classes": classes})
    return folds, fold_raw, labels


def fold_diff(fr):
    m = balanced_acc(fr["yte"], fr["pm"], fr["classes"])
    best = max(balanced_acc(fr["yte"], p, fr["classes"]) for p in fr["nulls"].values())
    return m - best


def grouped_bootstrap(fold_raw, n_boot=N_BOOT, seed=BOOT_SEED):
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_boot):
        ds = []
        for fr in fold_raw:
            uniq = sorted(set(fr["tids"].tolist()))
            pick = rng.choice(len(uniq), size=len(uniq), replace=True)
            idx = np.concatenate(
                [np.flatnonzero(fr["tids"] == uniq[p]) for p in pick])
            sub = {"yte": fr["yte"][idx], "pm": fr["pm"][idx],
                   "nulls": {k: v[idx] for k, v in fr["nulls"].items()},
                   "classes": fr["classes"]}
            ds.append(fold_diff(sub))
        means.append(float(np.mean(ds)))
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi)


def verdict_from(folds, ci):
    adequate = {s: f for s, f in folds.items()
                if f["n_test"] >= 45 and f["n_trajectories"] >= 4}
    S = len(adequate)
    total = sum(f["n_test"] for f in adequate.values())
    info = {"adequate_folds": sorted(adequate), "S": S, "usable_in_adequate": total}
    if S < 5 or total < 400:
        info["verdict"] = "DATA_INSUFFICIENT"
        return info
    d = [adequate[s]["d_effect"] for s in adequate]
    wins = sum(x > 0 for x in d)
    info["wins"] = f"{wins}/{S}"
    info["mean_d_adequate"] = round(float(np.mean(d)), 4)
    lo, hi = ci
    if lo is None:
        info["verdict"] = "NOT_EVALUATED_NO_BOOTSTRAP"
        return info
    if lo > 0 and wins >= (S + 1) // 2:
        info["verdict"] = "SURVIVES_CURRENT_TEST"
    elif hi < 0:
        info["verdict"] = "FALSIFIED"
    else:
        info["verdict"] = "INCONCLUSIVE"
    return info


# ---------------------------------------------------------------- analyses
def git_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    except Exception:
        return "unknown"


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def analyze(path, out_name, target_fn, feats_fn=None, onehot_fn=onehot,
            boot=True, interactions=False, row_level_target=False,
            skip_chaining=False):
    rows, stats = load_rows(path, skip_chaining=skip_chaining)
    folds, fold_raw, labels = run_folds(rows, target_fn, feats_fn, onehot_fn,
                                        interactions=interactions,
                                        row_level_target=row_level_target)
    ci = grouped_bootstrap(fold_raw) if boot else [None, None]
    info = verdict_from(folds, tuple(ci) if boot else (None, None))
    out = {
        "analysis": out_name,
        "input_file": path,
        "input_sha256": file_sha256(path),
        "git_commit_at_analysis": git_commit(),
        "dataset_stats": stats,
        "target_classes": labels,
        "folds": folds,
        "bootstrap": {"method": "trajectory-grouped within site, paired diff vs max null",
                      "n_boot": N_BOOT if boot else 0, "seed": BOOT_SEED,
                      "ci95_mean_effect": [round(x, 4) for x in ci] if boot else None},
        "decision": info,
        "verdict_rule": ("DATA_INSUFFICIENT if <5 adequate folds or <400 usable; "
                         "SURVIVES_CURRENT_TEST iff CI.lower>0 and wins>=ceil(S/2); "
                         "FALSIFIED iff CI.upper<0; else INCONCLUSIVE"),
        "preregistration": "reports/physics/wp003b_v2_preregistration.md",
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, f"{out_name}.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"analysis": out_name, "verdict": info.get("verdict"),
                      "mean_d": info.get("mean_d_adequate"),
                      "wins": info.get("wins"), "ci95": out["bootstrap"]["ci95_mean_effect"]},
                     indent=1))
    return out


def gate(path):
    """WP-004 identifiability gate (prereg §9 S-C)."""
    rows, stats = load_rows(path)
    labels = sorted({t1_signature(r["post"]) for r in rows})

    def url_shape_of(rec):
        p = os.path.join(RAW_DIR, f"{rec['pre_raw']}.json.gz")
        import gzip
        with gzip.open(p, "rt") as f:
            snap = json.load(f)
        return snap["url_shape"]

    groups = defaultdict(list)
    cache = {}
    for r in rows:
        tid = r["trajectory_id"]
        if tid not in cache:
            cache[tid] = url_shape_of(r)
        key = (r["site"], cache[tid], tuple(r["x"]))
        groups[key].append((tid, r["step_id"],
                            r["primary_action"], t1_signature(r["post"])))

    def independent(visits):
        kept = []
        for tid, step, *_ in visits:
            if any(tid == t and abs(step - s2) < 2 for t, s2, *_ in kept):
                continue
            kept.append((tid, step))
        return len(kept)

    g1 = g2 = 0
    detail = []
    for key, visits in groups.items():
        n_ind = independent(visits)
        if n_ind < 3:
            continue
        g1 += 1
        acts = {v[2] for v in visits}
        outs = {v[3] for v in visits}
        if len(acts) >= 2 and len(outs) >= 2:
            g2 += 1
            detail.append({"key": key[:2], "visits": len(visits),
                           "actions": sorted(acts), "outcomes": sorted(outs)})
    passed = g1 >= 50 and g2 >= 20
    out = {
        "analysis": "wp003b_v2_wp004_identifiability_gate",
        "gate_definition": ("state key=(site,url_shape,tuple(Z)); independent visit="
                            "distinct trajectory or same trajectory >=2 steps apart"),
        "pass_rule": "G1(#keys with >=3 indep visits) >= 50 AND G2(#those with >=2 actions and >=2 outcomes) >= 20",
        "G1_state_groups_with_ge3_independent_visits": g1,
        "G2_of_those_with_ge2_actions_and_ge2_outcomes": g2,
        "state_keys_total": len(groups),
        "gate_passed": bool(passed),
        "consequence": ("committor/barrier estimation MAY proceed to design review"
                        if passed else
                        "WP-004 remains BLOCKED; verdict DATA_INSUFFICIENT for committor feasibility on this corpus"),
        "examples": detail[:20],
        "git_commit_at_analysis": git_commit(),
    }
    with open(os.path.join(RESULTS_DIR, "wp003b_v2_gate.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in ("G1_state_groups_with_ge3_independent_visits",
                                          "G2_of_those_with_ge2_actions_and_ge2_outcomes",
                                          "gate_passed", "consequence")}, indent=1))
    return out


def policy_report(path):
    rows, stats = load_rows(path)
    per_site = defaultdict(Counter)
    for r in rows:
        per_site[r["site"]][r["primary_action"]] += 1
    out = {
        "analysis": "wp003b_v2_policy_marginals",
        "note": "documented input distribution of the crawler policy (§16 separation)",
        "per_site_first_action_counts": {s: dict(c) for s, c in sorted(per_site.items())},
        "overall": dict(sum(per_site.values(), Counter())),
        "chain_length_distribution": dict(Counter(len(r["action_labels"]) for r in rows)),
        "git_commit_at_analysis": git_commit(),
    }
    with open(os.path.join(RESULTS_DIR, "wp003b_v2_policy.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out["overall"], indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["primary", "components", "ablation", "gate",
                                     "policy", "interact", "all"])
    ap.add_argument("--in", dest="inp", default=DEFAULT_IN)
    args = ap.parse_args()

    def comps(path):
        for name, fn in COMPONENT_TARGETS.items():
            analyze(path, f"wp003b_v2_component_{name}", fn, boot=False)

    if args.what in ("primary", "all"):
        analyze(args.inp, "wp003b_v2_results", t1_signature)
    if args.what in ("components", "all"):
        comps(args.inp)
    if args.what in ("ablation", "all"):
        analyze(args.inp, "wp003b_v2_ablation_altrepr",
                lambda r: alt_signature(r["counts_post"]),
                feats_fn=lambda i, r: alt_state_feats(r), onehot_fn=alt_onehot,
                row_level_target=True)
    if args.what in ("interact", "all"):
        # preregistered EXPLORATORY arm (cannot alter the primary verdict)
        analyze(args.inp, "wp003b_v2_interactions_exploratory", t1_signature,
                interactions=True)
    if args.what in ("gate", "all"):
        gate(args.inp)
    if args.what in ("policy", "all"):
        policy_report(args.inp)


if __name__ == "__main__":
    main()
