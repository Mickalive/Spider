"""WP-003b (secondary, exploratory): is the next-page STRUCTURAL CLASS
predictable cross-site even though next-action-class is not?
Same corpus, same LOO-website protocol. Cannot rescue primary verdict.
"""
import json, os, sys
import numpy as np
from collections import Counter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from physics.run_wp003 import load, onehot, softmax_reg

IN = "/tmp/opencode/spider_data/wp003_transitions.jsonl"


def run():
    rows = [r for r in load() if r["target_action"] not in ("", "abandon")]
    # target B: structural class of the NEXT page
    for r in rows:
        p = r["post"]
        r["yb"] = f"d{p['depth_bucket']}.pw{p['has_password']}.lb{p['link_bucket']}.ib{p['text_input_bucket']}"
    classes = sorted({r["yb"] for r in rows})
    keep = {c for c, n in Counter(r["yb"] for r in rows).items() if n >= 8}
    rows = [r for r in rows if r["yb"] in keep]
    A = {c: i for i, c in enumerate(sorted(keep))}
    Xall, _ = onehot([r["x"] for r in rows])
    sites = sorted({r["site"] for r in rows})
    out = {"classes_kept": len(keep), "folds": {}}
    diffs, wins = [], 0
    for hold in sites:
        tr = [i for i, r in enumerate(rows) if r["site"] != hold]
        te = [i for i, r in enumerate(rows) if r["site"] == hold]
        if len(te) < 20:
            continue
        ytr = np.array([A[rows[i]["yb"]] for i in tr])
        yte = np.array([A[rows[i]["yb"]] for i in te])
        W = softmax_reg(Xall[tr], ytr, len(A))
        acc_m1 = float(((Xall[te] @ W).argmax(1) == yte).mean())
        maj = Counter(ytr.tolist()).most_common(1)[0][0]
        acc_n0 = float((yte == maj).mean())
        mu, sd = Xall[tr].mean(0), Xall[tr].std(0) + 1e-9
        Xt, Xs = (Xall[tr] - mu) / sd, (Xall[te] - mu) / sd
        pred_nn = np.array([ytr[int((((Xt - x) ** 2).sum(1)).argmin())] for x in Xs])
        acc_n4 = float((pred_nn == yte).mean())
        rng = np.random.default_rng(5)
        shuf = [float((rng.permutation(yte) == yte).mean()) for _ in range(300)]
        best_null = max(acc_n0, acc_n4, float(np.percentile(shuf, 95)))
        d = acc_m1 - best_null
        diffs.append(d)
        wins += d > 0
        out["folds"][hold] = {"n": len(te), "M1": round(acc_m1, 3),
                              "N0": round(acc_n0, 3), "N4": round(acc_n4, 3),
                              "shuffle_p95": round(float(np.percentile(shuf, 95)), 3),
                              "diff": round(d, 3)}
    out["mean_diff"] = round(float(np.mean(diffs)), 4)
    out["wins"] = f"{wins}/{len(diffs)}"
    print(json.dumps(out, indent=1))
    with open(os.path.join(os.path.dirname(__file__), "..", "results",
                           "physics", "wp003b_targetB.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    run()
