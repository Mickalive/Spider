"""WP-003 corrected control analysis.

This remains a policy/action-choice control, not the preferred Web-physics
target. It exists to repair the historical protocol honestly. Primary future
physics work should prefer action-conditioned next-state dynamics.
"""
import json, os
import numpy as np
from collections import Counter, defaultdict

IN = "/tmp/opencode/spider_data/wp003_transitions.jsonl"
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "physics",
                   "wp003_corrected_results.json")

FEATURES = ["link_bucket", "button_bucket", "text_input_bucket",
            "has_password", "has_select", "has_checkbox", "has_file",
            "has_textarea", "form_bucket", "depth_bucket", "query_bucket",
            "login_capable", "internal_ratio_bucket"]


def load():
    rows = []
    with open(IN) as f:
        for line in f:
            r = json.loads(line)
            if r.get("target_action") in ("", "abandon", None):
                continue
            r["x"] = [r["pre"][k] for k in FEATURES]
            rows.append(r)
    validate_rows(rows)
    return rows


def validate_rows(rows):
    """Hard pre-analysis invariants. Fail closed on legacy/leaky datasets."""
    assert rows, "empty dataset"
    required = {"site", "trajectory_id", "step_id", "target_action",
                "prev_action_label", "primary_action", "pre", "post"}
    for r in rows:
        missing = required - set(r)
        assert not missing, f"missing fields {missing}; legacy dataset is invalid"
        assert r["target_action"] == r["primary_action"], "target definition drift"
        assert isinstance(r["step_id"], int) and r["step_id"] >= 0

    by_traj = defaultdict(list)
    for r in rows:
        by_traj[r["trajectory_id"]].append(r)
    assert len(by_traj) >= 2, "need independent trajectories for grouped uncertainty"

    for tid, rs in by_traj.items():
        rs.sort(key=lambda x: x["step_id"])
        assert rs[0]["step_id"] == 0, (tid, "trajectory must start at step 0")
        assert rs[0]["prev_action_label"] == "<START>", (tid, "bad start previous action")
        for prev, cur in zip(rs, rs[1:]):
            assert cur["step_id"] == prev["step_id"] + 1, (tid, "non-contiguous steps")
            assert cur["prev_action_label"] == prev["primary_action"], (
                tid, cur["step_id"], "prev_action leakage/misalignment")

    # Diagnostic guard for the exact run-1 failure mode. Equality is legal on
    # some real adjacent repeated actions, but cannot be structurally forced on
    # nearly every non-start row.
    nonstart = [r for r in rows if r["prev_action_label"] != "<START>"]
    if nonstart:
        eq = sum(r["prev_action_label"] == r["target_action"] for r in nonstart) / len(nonstart)
        assert eq < 0.98, f"suspicious prev==target rate {eq:.3f}; possible target leakage"


def onehot(X):
    cols, names = [], []
    spec = {0: 3, 1: 3, 2: 3, 8: 3, 9: 3, 10: 3, 12: 3}
    for i in range(len(FEATURES)):
        if i in spec:
            for k in range(spec[i]):
                cols.append([1.0 if row[i] == k else 0.0 for row in X])
                names.append(f"{FEATURES[i]}={k}")
        else:
            cols.append([float(row[i]) for row in X])
            names.append(FEATURES[i])
    return np.array(cols).T, names


def softmax_reg(X, y_idx, C, iters=800, lr=0.5, l2=1e-3):
    n, d = X.shape
    W = np.zeros((d, C))
    Y = np.eye(C)[y_idx]
    for _ in range(iters):
        logits = X @ W
        logits -= logits.max(1, keepdims=True)
        P = np.exp(logits)
        P /= P.sum(1, keepdims=True)
        W -= lr * (X.T @ (P - Y) / n + l2 * W)
    return W


def balanced_acc(y_true, y_pred, classes):
    recalls = []
    for c in classes:
        m = y_true == c
        if m.sum():
            recalls.append(float((y_pred[m] == c).mean()))
    return float(np.mean(recalls)) if recalls else float("nan")


def predictions_for_fold(rows, hold, A, Xall):
    tr = [i for i, r in enumerate(rows) if r["site"] != hold]
    te = [i for i, r in enumerate(rows) if r["site"] == hold]
    ytr = np.array([A[rows[i]["target_action"]] for i in tr])
    yte = np.array([A[rows[i]["target_action"]] for i in te])
    Xtr, Xte = Xall[tr], Xall[te]

    W = softmax_reg(Xtr, ytr, len(A))
    p_m1 = (Xte @ W).argmax(1)
    maj = Counter(ytr.tolist()).most_common(1)[0][0]
    p_n0 = np.full_like(yte, maj)

    big = defaultdict(Counter)
    for i in tr:
        pa = rows[i]["prev_action_label"]
        big[pa][A[rows[i]["target_action"]]] += 1
    p_n2 = np.array([(big[rows[i]["prev_action_label"]].most_common(1)[0][0]
                      if big.get(rows[i]["prev_action_label"]) else maj) for i in te])

    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xt, Xs = (Xtr - mu) / sd, (Xte - mu) / sd
    p_n4 = np.array([ytr[int((((Xt - xs) ** 2).sum(1)).argmin())] for xs in Xs])
    tids = np.array([rows[i]["trajectory_id"] for i in te], dtype=object)
    return yte, p_m1, p_n0, p_n2, p_n4, tids


def grouped_bootstrap(fold_raw, classes, n_boot=1000, seed=11):
    """Resample whole independent trajectories within each held-out site."""
    rng = np.random.default_rng(seed)
    samples = []
    for _ in range(n_boot):
        fold_diffs = []
        for raw in fold_raw.values():
            y, pm, p0, p2, p4, tids = raw
            unique = sorted(set(tids.tolist()))
            picked = rng.choice(unique, size=len(unique), replace=True)
            idx = np.concatenate([np.flatnonzero(tids == tid) for tid in picked])
            yb = y[idx]
            m = balanced_acc(yb, pm[idx], classes)
            nulls = [balanced_acc(yb, p[idx], classes) for p in (p0, p2, p4)]
            fold_diffs.append(m - max(nulls))
        samples.append(float(np.mean(fold_diffs)))
    return np.percentile(samples, [2.5, 97.5]).tolist()


def run():
    rows = load()
    sites = sorted({r["site"] for r in rows})
    acts = sorted({r["target_action"] for r in rows})
    A = {a: i for i, a in enumerate(acts)}
    classes = np.arange(len(acts))
    Xall, names = onehot([r["x"] for r in rows])

    folds, raw = {}, {}
    for hold in sites:
        y, pm, p0, p2, p4, tids = predictions_for_fold(rows, hold, A, Xall)
        raw[hold] = (y, pm, p0, p2, p4, tids)
        vals = {
            "M1": balanced_acc(y, pm, classes),
            "N0": balanced_acc(y, p0, classes),
            "N2": balanced_acc(y, p2, classes),
            "N4": balanced_acc(y, p4, classes),
        }
        best = max(vals[k] for k in ("N0", "N2", "N4"))
        folds[hold] = {"n_test": len(y), "n_trajectories": len(set(tids.tolist())),
                       **{k: round(v, 4) for k, v in vals.items()},
                       "best_null": round(best, 4),
                       "diff_M1_bestnull": round(vals["M1"] - best, 4)}

    diffs = [v["diff_M1_bestnull"] for v in folds.values()]
    wins = sum(d > 0 for d in diffs)
    ci = grouped_bootstrap(raw, classes)
    enough = all(v["n_test"] >= 45 and v["n_trajectories"] >= 4 for v in folds.values())
    if not enough:
        verdict = "DATA_INSUFFICIENT"
    elif ci[0] > 0 and wins >= max(1, (len(folds) + 1) // 2):
        verdict = "SURVIVES_CURRENT_TEST"
    else:
        verdict = "FALSIFIED"

    summary = {
        "analysis_status": "CORRECTED_PROTOCOL",
        "scientific_scope": "agent-policy next-action control; not primary Web-physics target",
        "n_transitions_total": len(rows),
        "n_trajectories": len({r["trajectory_id"] for r in rows}),
        "sites": {s: sum(r["site"] == s for r in rows) for s in sites},
        "action_classes": acts,
        "feature_names": names,
        "folds": folds,
        "mean_diff_M1_vs_bestnull": round(float(np.mean(diffs)), 4),
        "fold_wins": f"{wins}/{len(diffs)}",
        "trajectory_grouped_bootstrap_ci95": [round(float(x), 4) for x in ci],
        "verdict": verdict,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run()
