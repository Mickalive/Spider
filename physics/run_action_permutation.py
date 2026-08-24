"""E-1 (EXPLORATORY control, cycle 32670239235): permuted-action ablation for
the interaction-augmented arm.

Within each site, randomly permute the joint action descriptor
(primary_action, chain flag) across rows, keeping every site's state rows,
action marginals and outcome labels intact but destroying any genuine
action->outcome pairing. Then rerun the S-E interaction analysis.

Interpretation:
- effect collapses  -> the exploratory SURVIVES result depends on real
  action-conditioning (supports the P(s'|s,a) dynamics reading);
- effect persists   -> the signal is state-only structure that the action
  features merely help represent; the "dynamics" reading would be WRONG.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from physics.run_wp003b_v2 import DEFAULT_IN, RESULTS_DIR, git_commit, load_rows

SEED = 20260826


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IN
    rows, stats = load_rows(path, skip_chaining=True)
    rng = np.random.default_rng(SEED)

    from collections import defaultdict
    by_site = defaultdict(list)
    for i, r in enumerate(rows):
        by_site[r["site"]].append(i)
    for site, idxs in by_site.items():
        idxs = np.array(idxs)
        perm = rng.permutation(len(idxs))
        descs = [(rows[i]["primary_action"],
                  len(rows[i].get("action_labels") or []) > 1) for i in idxs]
        for pos, i in enumerate(idxs):
            a, chain = descs[perm[pos]]
            rows[i]["primary_action"] = a
            rows[i]["target_action"] = a  # keep record invariant consistent
            # downstream analysis only uses len(action_labels) > 1 as the
            # chain flag; keep it consistent with the permuted descriptor
            rows[i]["action_labels"] = [{"label": a}, {"label": a}] if chain \
                else [{"label": a}]
    tmp = "/tmp/opencode/spider_data/wp003b_v2_permA.jsonl"
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    import physics.run_wp003b_v2 as V
    out = V.analyze(tmp, "wp003b_v2_interact_permutedA_exploratory",
                    V.t1_signature, interactions=True, skip_chaining=True)
    out["control"] = {
        "what": "within-site permutation of (primary_action, chain flag)",
        "seed": SEED,
        "reading": ("effect collapse => exploratory survival depends on real "
                    "action-conditioning; persistence => state-only structure"),
    }
    with open(os.path.join(RESULTS_DIR,
                           "wp003b_v2_interact_permutedA_exploratory.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
