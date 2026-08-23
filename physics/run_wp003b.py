"""WP-003B corrected: cross-site next-state structural prediction.

Target: coarse structural class of s_{t+1}.
Inputs: mechanics-only state s_t PLUS imposed/current action a_t.
This is closer to environment dynamics P(s' | s, a) than the historical
next-action target. Uses true website holdout and trajectory-grouped bootstrap.
"""
import json, os
import numpy as np
from collections import Counter
from physics.run_wp003 import load, onehot, softmax_reg, balanced_acc

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "physics",
                   "wp003b_corrected_targetB.json")


def action_onehot(rows, action_classes):
    A = {a: i for i, a in enumerate(action_classes)}
    z = np.zeros((len(rows), len(A)))
    for i, r in enumerate(rows):
        z[i, A[r["primary_action"]]] = 1.0
    return z


def target_label(r):
    p = r["post"]
    return f"d{p['depth_bucket']}.pw{p['has_password']}.lb{p['link_bucket']}.ib{p['text_input_bucket']}"


def grouped_bootstrap(raw, classes, n_boot=1000, seed=17):
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        ds = []
        for y, pm, p0, pnn, tids in raw.values():
            uniq = sorted(set(tids.tolist()))
            chosen = rng.choice(uniq, size=len(uniq), replace=True)
            idx = np.concatenate([np.flatnonzero(tids == t) for t in chosen])
            yb = y[idx]
            m = balanced_acc(yb, pm[idx], classes)
            n0 = balanced_acc(yb, p0[idx], classes)
            nn = balanced_acc(yb, pnn[idx], classes)
            ds.append(m - max(n0, nn))
        vals.append(float(np.mean(ds)))
    return np.percentile(vals, [2.5, 97.5]).tolist()


def run():
    rows = load()
    counts = Counter(target_label(r) for r in rows)
    keep = {c for c, n in counts.items() if n >= 12}
    rows = [r for r in rows if target_label(r) in keep]
    assert rows and len(keep) >= 2, "insufficient target-B class support"

    classes_lbl = sorted(keep)
    Y = {c: i for i, c in enumerate(classes_lbl)}
    yall = np.array([Y[target_label(r)] for r in rows])
    Xstate, names = onehot([r["x"] for r in rows])
    actions = sorted({r["primary_action"] for r in rows})
    X = np.concatenate([Xstate, action_onehot(rows, actions)], axis=1)
    feature_names = names + [f"action={a}" for a in actions]
    sites = sorted({r["site"] for r in rows})
    classes = np.arange(len(Y))

    folds, raw = {}, {}
    for hold in sites:
        tr = np.array([i for i, r in enumerate(rows) if r["site"] != hold])
        te = np.array([i for i, r in enumerate(rows) if r["site"] == hold])
        if len(te) < 20:
            continue
        ytr, yte = yall[tr], yall[te]
        W = softmax_reg(X[tr], ytr, len(Y))
        pm = (X[te] @ W).argmax(1)
        maj = Counter(ytr.tolist()).most_common(1)[0][0]
        p0 = np.full_like(yte, maj)
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        Xt, Xs = (X[tr] - mu) / sd, (X[te] - mu) / sd
        pnn = np.array([ytr[int((((Xt - x) ** 2).sum(1)).argmin())] for x in Xs])
        tids = np.array([rows[i]["trajectory_id"] for i in te], dtype=object)
        raw[hold] = (yte, pm, p0, pnn, tids)

        m = balanced_acc(yte, pm, classes)
        n0 = balanced_acc(yte, p0, classes)
        nn = balanced_acc(yte, pnn, classes)
        best = max(n0, nn)
        folds[hold] = {
            "n": len(te),
            "n_trajectories": len(set(tids.tolist())),
            "M_state_plus_action": round(m, 4),
            "N0_majority": round(n0, 4),
            "N4_nearest_neighbor": round(nn, 4),
            "diff": round(m - best, 4),
        }

    diffs = [v["diff"] for v in folds.values()]
    wins = sum(d > 0 for d in diffs)
    ci = grouped_bootstrap(raw, classes)
    enough = bool(folds) and all(v["n"] >= 20 and v["n_trajectories"] >= 4 for v in folds.values())
    if not enough:
        verdict = "DATA_INSUFFICIENT"
    elif ci[0] > 0 and wins >= max(1, (len(folds) + 1) // 2):
        verdict = "SURVIVES_CURRENT_TEST"
    else:
        verdict = "FALSIFIED"

    out = {
        "analysis_status": "CORRECTED_ACTION_CONDITIONED_TARGET_B",
        "target": "coarse next-state structural class",
        "conditioning": "mechanics-only s_t + current action a_t",
        "classes_kept": classes_lbl,
        "feature_names": feature_names,
        "folds": folds,
        "mean_diff": round(float(np.mean(diffs)), 4) if diffs else None,
        "wins": f"{wins}/{len(diffs)}",
        "trajectory_grouped_bootstrap_ci95": [round(float(x), 4) for x in ci],
        "verdict": verdict,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
