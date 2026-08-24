"""Cycle 32670239235 measurement-validity tests (frozen before data collection).

1. Seed determinism: collector site offsets + RNG streams must be identical
   across processes with different PYTHONHASHSEED (the exact WP-003 defect).
2. Protocol sensitivity on SYNTHETIC corpora:
   - planted cross-site signal -> the fold engine must detect it;
   - pure-noise target        -> the fold engine must NOT "survive".
A protocol that cannot fail cannot inform; these tests keep the analysis
pipeline falsifiable in both directions.
"""
import os
import random
import subprocess
import sys
import unittest

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

from physics.run_wp003 import FEATURES, validate_rows
from physics.run_wp003b_v2 import run_folds

SYN_ACTIONS = ["click_link", "click_button", "fill_text", "select_option"]
LINK_SKEWS = [0.7, 0.05, 0.15, 0.5, 0.3, 0.02]


def synth_rows(seed, n_sites=6, trajs=6, steps=15, plant=False):
    """Synthetic corpus passing the same invariants as real collected rows."""
    rng = random.Random(seed)
    rows = []
    for s in range(n_sites):
        site = f"synsite{s}"
        link_skew = LINK_SKEWS[s % len(LINK_SKEWS)]
        for j in range(trajs):
            tid = f"{site}-r{j}"
            prev = "<START>"
            for step in range(steps):
                lb = 0 if rng.random() < link_skew else rng.choice([1, 2])
                pre = {"link_bucket": lb,
                       "button_bucket": rng.choice([0, 1, 2]),
                       "text_input_bucket": rng.choice([0, 1]),
                       "has_password": int(rng.random() < 0.2),
                       "has_select": int(rng.random() < 0.3),
                       "has_checkbox": int(rng.random() < 0.2),
                       "has_file": 0,
                       "has_textarea": int(rng.random() < 0.1),
                       "form_bucket": rng.choice([0, 1, 2]),
                       "depth_bucket": rng.choice([0, 1, 2]),
                       "query_bucket": rng.choice([0, 1, 2]),
                       "login_capable": int(rng.random() < 0.2),
                       "internal_ratio_bucket": rng.choice([0, 1, 2])}
                act = rng.choice(SYN_ACTIONS)
                if plant:
                    # identical latent channel on every site; LINEARLY
                    # representable in [Z ⊕ A] (the frozen model class);
                    # depends on dims the coarse cell-frequency null cannot
                    # condition on (has_password)
                    import math
                    score = (pre["has_password"] * 1.0
                             + (1 if act == "fill_text" else 0) * 0.9
                             + (1 if lb >= 1 else 0) * 0.7)
                    p = 1.0 / (1.0 + math.exp(-1.6 * (score - 1.2)))
                    y = 1 if rng.random() < p else 0
                else:
                    y = rng.randrange(4)
                post = dict(pre)
                post["link_bucket"] = max(0, min(2, lb + rng.choice([-1, 0, 0, 1])))
                post["syn_y"] = y
                rows.append({
                    "site": site, "trajectory_id": tid, "step_id": step,
                    "pre": pre, "post": post,
                    "x": [pre[k] for k in FEATURES],
                    "target_action": act, "primary_action": act,
                    "prev_action_label": prev,
                    "action_labels": [{"label": act, "ok": True, "error": ""}],
                    "any_ok": True, "next_page_class": (),
                })
                prev = act
    validate_rows(rows)
    return rows


def fold_effects(rows, target_fn):
    folds, _, _ = run_folds(rows, target_fn)
    return {s: f["d_effect"] for s, f in folds.items()}


class SeedDeterminismTests(unittest.TestCase):
    def test_site_offset_and_rng_stable_across_hash_seeds(self):
        code = (
            "import sys, random; sys.path.insert(0, %r);"
            "from physics.collector import stable_site_offset;"
            "o = stable_site_offset('wikipedia');"
            "rng = random.Random(20260823 + o + 10007);"
            "print(o, [round(rng.random(), 6) for _ in range(5)])" % (REPO,)
        )
        outs = []
        for hs in ("0", "1", "random"):
            env = dict(os.environ, PYTHONHASHSEED=hs)
            r = subprocess.run([sys.executable, "-c", code], env=env,
                               capture_output=True, text=True, check=True)
            outs.append(r.stdout.strip())
        self.assertEqual(len(set(outs)), 1,
                         f"seed mechanism not process-stable: {outs}")


class ProtocolSensitivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.planted_d = fold_effects(synth_rows(seed=11, plant=True),
                                     lambda p: f"y{p['syn_y']}")
        cls.noise_d = fold_effects(synth_rows(seed=12, plant=False),
                                   lambda p: f"y{p['syn_y']}")

    def test_planted_signal_is_detected(self):
        d = self.planted_d
        wins = sum(v > 0 for v in d.values())
        mean_d = float(np.mean(list(d.values())))
        self.assertGreater(mean_d, 0.02, f"missed planted signal: {d}")
        self.assertGreaterEqual(wins, 4, f"too few fold wins: {d}")

    def test_noise_target_does_not_survive(self):
        d = self.noise_d
        mean_d = float(np.mean(list(d.values())))
        wins = sum(v > 0 for v in d.values())
        self.assertLessEqual(mean_d, 0.03, f"model 'found' noise: {d}")
        self.assertLess(wins, 4, f"too many fluke wins: {d}")


if __name__ == "__main__":
    unittest.main()
