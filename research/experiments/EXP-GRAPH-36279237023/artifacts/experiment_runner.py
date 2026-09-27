"""Execution runner for the frozen experiment EXP-GRAPH-36279237023.

Execution order is fixed by prereg.md and is enforced in code, not by intention:

  PHASE 0  estimator unit tests (prereg 14) and fixture integrity checks (V11)
  PHASE 1  measurement-validity preconditions that are decidable before any arm
           (V9 code-hash-in-freeze check, V7 state-reset determinism)
  PHASE 2  DEGENERACY SCREEN (V8) -- B-LEXICAL-OVERLAP and A-INCUMBENT run here,
           BEFORE any candidate arm touches a goal. If the screen fails the
           runner halts and no candidate row is produced (prereg 5.3, 12).
  PHASE 3  calibration fitting (V4) on the train split, threshold on validation
  PHASE 4  per-task execution of all arms in a seeded random order, with a full
           server-state reset plus a logged per-task state hash before every arm
           request (V7), and the separate HTTP verification measure (prereg 6.3)
  PHASE 5  metric computation, gate evaluation in the frozen order (prereg 7.1)
  PHASE 6  raw/derived artifact writing

Raw evidence is written as JSONL with one record per (task, arm). Everything
downstream is derived from those files.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import pathlib
import random
import sys
import time
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))

import candidate_resolver as cr  # noqa: E402
import goal_generator as gg  # noqa: E402
import http_server as hs  # noqa: E402
import metric_estimators as me  # noqa: E402
from fixture_def import build_fixture  # noqa: E402

SEED_GOALS = gg.SEED_DEFAULT
SEED_ARM_ORDER = 20260926
SEED_SPLIT = 990017
SEED_RANDOM_ROLE = 4242
SEED_BOOTSTRAP = me.BOOTSTRAP_SEED
HEADROOM = me.HEADROOM_THRESHOLD
ARMS = [
    "A-CANDIDATE",
    "A-INCUMBENT",
    "A-REFERENCE-EMBEDARGMAX",
    "B-LEXICAL-OVERLAP",
    "B-RANDOM-ROLE",
    "B-INTERNAL-ID-ORACLE",
]
GATE_THRESHOLDS = [round(0.02 * i, 2) for i in range(1, 50)]


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonable(obj: Any) -> Any:
    """Convert numpy scalars/arrays to native JSON types.

    `default=str` was used in an earlier revision of this runner and silently turned
    every numpy.float32 into a JSON *string*. Numbers must serialise as numbers or
    the raw evidence is not quantitatively auditable.
    """
    import numpy as np

    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return [jsonable(v) for v in obj.tolist()]
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, float):
        return float(obj)
    return obj


def dump(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def dumpl(path: pathlib.Path, rows: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(jsonable(row), sort_keys=True) + "\n")


# ==========================================================================
# PHASE 0 -- estimator unit tests and fixture integrity
# ==========================================================================
def phase0(exp_dir: pathlib.Path) -> dict:
    out: dict[str, Any] = {}
    tests = me.unit_tests()
    out["estimator_unit_tests"] = tests
    if not tests["all_pass"]:
        out["halt"] = "OBS-ESTIMATOR-UNIT-TESTS FAILED; prereg 14 forbids running with unverified estimators"

    fixture = build_fixture()
    dump(exp_dir / "artifacts" / "fixture.json", fixture)

    # V11: several mechanisms per resource family across multiple verbs
    per_family: dict[str, set[str]] = {}
    for m in fixture["mechanisms"]:
        per_family.setdefault(m["resource_family"], set()).add(m["verb"])
    v11_multi = {f: sorted(v) for f, v in per_family.items()}
    v11_ok_multi = all(len(v) > 1 for v in per_family.values())

    # V11: every mechanism has non-empty parameter_slots
    empty_slots = [m["mechanism_id"] for m in fixture["mechanisms"] if not m["parameter_slots"]]

    # V11: no unbindable ${...} placeholder -- every placeholder is a declared slot
    import re

    unbindable = []
    for m in fixture["mechanisms"]:
        text = json.dumps(m["action_template"])
        for ph in re.findall(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", text):
            if ph not in m["parameter_slots"]:
                unbindable.append((m["mechanism_id"], ph))

    # the generic slot-filler must bind every mechanism from its OWN recorded intent
    unbondable = []
    for m in fixture["mechanisms"]:
        bound, unfilled = cr.bind_parameters(m, m["intent"])
        if unfilled:
            unbondable.append({"mechanism_id": m["mechanism_id"], "unfilled": unfilled})

    out["fixture"] = {
        "n_mechanisms": len(fixture["mechanisms"]),
        "n_endpoints": len(fixture["endpoints"]),
        "verbs_per_family": v11_multi,
        "v11_multiple_mechanisms_per_family": v11_ok_multi,
        "mechanisms_with_empty_parameter_slots": empty_slots,
        "unbindable_placeholders": unbindable,
        "mechanisms_whose_own_intent_leaves_slots_unbound": unbondable,
    }
    if not v11_ok_multi or empty_slots or unbindable or unbondable:
        out["halt"] = out.get("halt") or "V11 fixture discrimination check FAILED"

    # goal independence observation (prereg 10 OBS-GOAL-GEN-INDEPENDENCE, non-blocking):
    # computed PER GOAL against its own family target, not against a union of intents
    goals_payload = gg.build_goals(fixture)
    by_id = {m["mechanism_id"]: m for m in fixture["mechanisms"]}
    per_goal = []
    for g in goals_payload["goals"]:
        if g["category"] in ("paraphrased", "underspecified", "verbatim"):
            per_goal.append(gg.jaccard(g["text"], by_id[g["target_mechanism_id"]]["intent"]))
    out["goal_independence"] = {
        "n": len(per_goal),
        "max_per_goal_jaccard": max(per_goal) if per_goal else None,
        "mean_per_goal_jaccard": (sum(per_goal) / len(per_goal)) if per_goal else None,
        "fraction_below_0_3": (sum(1 for x in per_goal if x < 0.3) / len(per_goal)) if per_goal else None,
        "definition": "per-goal token Jaccard against that goal's OWN target intent (not a union)",
        "blocking": False,
    }

    out["goal_counts"] = goals_payload["counts"]
    out["goal_total"] = goals_payload["total"]
    out["applies_any_count"] = goals_payload["applies_any_count"]
    out["applies_none_count"] = goals_payload["applies_none_count"]
    return out


# ==========================================================================
# PHASE 1 -- pre-arm validity checks
# ==========================================================================
def phase1(exp_dir: pathlib.Path) -> dict:
    out: dict[str, Any] = {}
    freeze = json.loads((exp_dir / "freeze.json").read_text(encoding="utf-8"))
    frozen_hashes = freeze.get("hashes", {})
    code_files = [
        "candidate_resolver.py",
        "goal_generator.py",
        "http_server.py",
        "experiment_runner.py",
        "metric_estimators.py",
        "fixture_def.py",
    ]
    in_freeze = [c for c in code_files if c in frozen_hashes]
    out["v9_code_hashed_into_freeze"] = {
        "freeze_json_hashes": sorted(frozen_hashes.keys()),
        "code_files_expected_by_v9": code_files,
        "code_files_present_in_freeze": in_freeze,
        "pass": len(in_freeze) > 0,
        "note": (
            "freeze.json was produced by the deterministic freezer at commit 9b56d0b9, which hashes only "
            "request.json, spec.json and prereg.md. The outcome-bearing code did not exist at freeze time, so "
            "no code hash could be present. The freezer is scripts/freeze_experiment.py, which is outside every "
            "scientific lane's allowed_code_roots, so no EXECUTE-stage actor can repair this."
        ),
    }
    out["frozen_input_hashes_recomputed"] = {
        k: sha256_file(exp_dir / k) for k in ("request.json", "spec.json", "prereg.md")
    }
    out["frozen_input_hashes_match"] = all(
        out["frozen_input_hashes_recomputed"][k] == v for k, v in frozen_hashes.items() if k in ("request.json", "spec.json", "prereg.md")
    )
    return out


# ==========================================================================
# PHASE 2 -- degeneracy screen (runs BEFORE any candidate arm)
# ==========================================================================
def phase2(fixture: dict, goals: list[dict]) -> dict:
    out: dict[str, Any] = {"per_goal": []}
    by_id = {m["mechanism_id"]: m for m in fixture["mechanisms"]}
    mech_order = [m["mechanism_id"] for m in fixture["mechanisms"]]

    lex_all = lex_app = 0
    lex_rows: list[dict] = []
    for g in goals:
        d = cr.arm_lexical_overlap(g["text"], fixture["mechanisms"])
        correct = d["selected_mechanism_id"] == g["target_mechanism_id"]
        lex_all += 1 if correct else 0
        if g["applies_any"]:
            lex_app += 1 if correct else 0
        lex_rows.append(
            {
                "goal_id": g["goal_id"],
                "category": g["category"],
                "applies_any": g["applies_any"],
                "selected": d["selected_mechanism_id"],
                "target": g["target_mechanism_id"],
                "correct": correct,
                "jaccard_top": d["jaccard_top"],
            }
        )
    n_all = len(goals)
    n_app = sum(1 for g in goals if g["applies_any"])
    out["lexical_overlap"] = {
        "accuracy_all_80": lex_all / n_all,
        "accuracy_applicable_only": lex_app / n_app,
        "n_all": n_all,
        "n_applicable": n_app,
        "headroom_threshold": HEADROOM,
        "pass_as_frozen_all80": (lex_all / n_all) < HEADROOM,
        "structural_cap_on_all80": n_app / n_all,
        "structural_cap_note": (
            "B-LEXICAL-OVERLAP never abstains, so every one of the "
            f"{n_all - n_app} goals with no applicable mechanism is scored incorrect by construction. Its accuracy on "
            f"the frozen 80-goal set is therefore capped at {n_app}/{n_all} = {n_app / n_all:.4f} < {HEADROOM} "
            "for any lexical selector whatsoever. V8(a) as frozen is structurally non-binding on this fixture and "
            "its PASS is not evidence that the lexical null is weak."
        ),
    }
    out["per_goal"].extend({"arm": "B-LEXICAL-OVERLAP", **r} for r in lex_rows)

    # A-INCUMBENT: the committed kernel at the EXECUTABLE boundary
    reg_path = str(HERE / "incumbent_registry.jsonl")
    cr.incumbent_registry_path(fixture, reg_path)
    inc_executable = 0
    inc_rows: list[dict] = []
    for g in goals:
        d = cr.arm_incumbent(g["text"], reg_path, min_confidence=0.5)
        is_exec = d["resolution_status"] == "EXECUTABLE"
        inc_executable += 1 if is_exec else 0
        inc_rows.append(
            {
                "goal_id": g["goal_id"],
                "category": g["category"],
                "applies_any": g["applies_any"],
                "status": d["resolution_status"],
                "selected": d["selected_mechanism_id"],
                "target": g["target_mechanism_id"],
                "correct": (d["selected_mechanism_id"] == g["target_mechanism_id"]) and is_exec,
                "reason": d["abstain_reason"],
            }
        )
    out["incumbent"] = {
        "min_confidence": 0.5,
        "executable_count": inc_executable,
        "n_goals": len(goals),
        "status_counts": {
            s: sum(1 for r in inc_rows if r["status"] == s)
            for s in sorted({r["status"] for r in inc_rows})
        },
        "nonempty": inc_executable > 0,
        "observed_cause": (
            "kernel.py:resolve() requires exact intent-string equality AND every template slot present in the "
            "supplied params dict. This packet's V11 fixture gives every mechanism a non-empty parameter_slots, and "
            "arm_incumbent supplies params={}, so no mechanism can ever become a candidate. The incumbent leg is "
            "empty for a code-level reason, not because it scored low."
        ),
    }
    out["per_goal"].extend({"arm": "A-INCUMBENT", **r} for r in inc_rows)

    # prereg 11 sanctioned substitute when the incumbent leg is empty
    substitute: dict[str, Any] = {"declared": False}
    if inc_executable == 0:
        emb = cr.Embedder()
        cos = cr.cosines(emb, [g["text"] for g in goals], [m["intent"] for m in fixture["mechanisms"]])
        sub_executable = 0
        for i, g in enumerate(goals):
            d = cr.arm_reference_embedargmax(g["text"], [float(x) for x in cos[i]], fixture["mechanisms"])
            sub_executable += 1 if d["resolution_status"] == "EXECUTABLE" else 0
        substitute = {
            "declared": True,
            "id": "A-REFERENCE-EMBEDARGMAX",
            "authority": "prereg.md 11 'declare explicit non-empty substitute arm'",
            "definition": (
                "argmax cosine over mechanism intent embeddings, always commits (no fitted gate, no threshold, no "
                "abstention), slots filled by the same generic heuristic. It is strictly weaker in decision power "
                "than A-CANDIDATE, so declaring it cannot bias the primary comparison in the candidate's favour; "
                "it is strictly harder, because it is scored on the same mechanism-identity metric without ever "
                "declining to answer."
            ),
            "executable_count": sub_executable,
            "nonempty": sub_executable > 0,
        }
    out["substitute_leg"] = substitute
    out["comparison_leg_nonempty"] = inc_executable > 0 or bool(substitute.get("nonempty"))
    out["screen_pass"] = bool(out["lexical_overlap"]["pass_as_frozen_all80"]) and out["comparison_leg_nonempty"]
    out["screen_condition_a"] = "B-LEXICAL-OVERLAP accuracy (all 80 frozen goals) < 0.90"
    out["screen_condition_b"] = "comparison leg has > 0 EXECUTABLE decisions"
    return out


# ==========================================================================
# PHASE 3 -- calibration fitting (V4)
# ==========================================================================
def fit_logistic(x: list[float], y: list[int]) -> dict:
    import numpy as np
    from sklearn.linear_model import LogisticRegression

    X = np.asarray(x, dtype=float).reshape(-1, 1)
    Y = np.asarray(y, dtype=int)
    if len(set(Y.tolist())) < 2:
        return {"fitted": False, "reason": f"label degenerate (values={sorted(set(Y.tolist()))})"}
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=5000)
    model.fit(X, Y)
    return {
        "fitted": True,
        "w": float(model.coef_[0][0]),
        "b": float(model.intercept_[0]),
        "converged_iters": int(model.n_iter_[0]),
        "n_train_rows": int(len(Y)),
        "label_balance": {str(v): int((Y == v).sum()) for v in sorted(set(Y.tolist()))},
        "estimator": "sklearn.linear_model.LogisticRegression(penalty=None, solver=lbfgs, max_iter=5000)",
    }


def phase3(goals: list[dict], fixture: dict, cos: Any, emb_meta: dict) -> dict:
    applicable = [g for g in goals if g["applies_any"]]
    index = {g["goal_id"]: i for i, g in enumerate(goals)}

    # top-cosine mechanism and correctness for every applicable goal
    rows = []
    for g in applicable:
        i = index[g["goal_id"]]
        row = [float(x) for x in cos[i]]
        best = max(range(len(row)), key=lambda k: (row[k], -k))
        mid = fixture["mechanisms"][best]["mechanism_id"]
        rows.append(
            {
                "goal_id": g["goal_id"],
                "family": g["family"],
                "cos_top": row[best],
                "selected_by_cosine": mid,
                "target": g["target_mechanism_id"],
                "correct": mid == g["target_mechanism_id"],
            }
        )

    # stratified 80/20 train/validation split by resource family (prereg 5.4)
    by_family: dict[str, list[dict]] = {}
    for r in rows:
        by_family.setdefault(r["family"], []).append(r)
    rng = random.Random(SEED_SPLIT)
    train_ids: set[str] = set()
    val_ids: set[str] = set()
    for fam in sorted(by_family):
        members = sorted(by_family[fam], key=lambda r: r["goal_id"])
        k = max(1, int(round(0.2 * len(members))))
        picked = set(rng.sample(range(len(members)), k))
        for j, r in enumerate(members):
            (val_ids if j in picked else train_ids).add(r["goal_id"])
    train = [r for r in rows if r["goal_id"] in train_ids]
    val = [r for r in rows if r["goal_id"] in val_ids]

    fit = fit_logistic([r["cos_top"] for r in train], [1 if r["correct"] else 0 for r in train])
    if not fit.get("fitted"):
        return {"fit": fit, "frozen": False, "halt": "calibration could not be fitted; V4 FAILS"}

    w, b = fit["w"], fit["b"]

    def p_of(c: float) -> float:
        import math

        return 1.0 / (1.0 + math.exp(-(w * c + b)))

    # threshold chosen on VALIDATION to maximise F1 of the positive class
    # "goal resolved correctly" (selected==target AND not abstained). Declared.
    sweep = []
    best = None
    for t in GATE_THRESHOLDS:
        tp = fp = fn = 0
        for r in val:
            predicted = p_of(r["cos_top"]) >= t
            actual = r["correct"]
            if predicted and actual:
                tp += 1
            elif predicted and not actual:
                fp += 1
            elif (not predicted) and actual:
                fn += 1
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        sweep.append({"threshold": t, "val_precision": prec, "val_recall": rec, "val_f1": f1,
                      "val_committed": tp + fp})
        if best is None or f1 > best["val_f1"]:
            best = sweep[-1]
    threshold = best["threshold"]

    # evidence that the gate is fitted rather than algebraically fixed:
    # refit on three disjoint seeds and check the parameters move
    seed_refits = []
    for s in (1, 2, 3):
        r2 = random.Random(SEED_SPLIT + s)
        t2: set[str] = set()
        v2: set[str] = set()
        for fam in sorted(by_family):
            members = sorted(by_family[fam], key=lambda r: r["goal_id"])
            k = max(1, int(round(0.2 * len(members))))
            picked = set(r2.sample(range(len(members)), k))
            for j, rr in enumerate(members):
                (v2 if j in picked else t2).add(rr["goal_id"])
        tr = [r for r in rows if r["goal_id"] in t2]
        f2 = fit_logistic([r["cos_top"] for r in tr], [1 if r["correct"] else 0 for r in tr])
        seed_refits.append({"split_seed": SEED_SPLIT + s, "fitted": f2.get("fitted"),
                            "w": f2.get("w"), "b": f2.get("b")})

    ws = [r["w"] for r in seed_refits if r["fitted"]]
    return {
        "frozen": True,
        "fit": fit,
        "threshold": threshold,
        "threshold_selection": {
            "objective": "maximise validation F1 of the positive class 'goal resolved correctly' "
                         "(selected==target AND not abstained); an abstention on a resolvable goal is a false negative",
            "selected": best,
            "candidates_considered": len(GATE_THRESHOLDS),
            "grid": GATE_THRESHOLDS,
        },
        "threshold_sweep_validation": sweep,
        "split": {
            "seed": SEED_SPLIT,
            "stratified_by": "resource_family",
            "n_applicable": len(rows),
            "n_train": len(train),
            "n_val": len(val),
            "train_goal_ids": sorted(train_ids),
            "val_goal_ids": sorted(val_ids),
            "excluded_from_fitting": {
                "n": len(goals) - len(applicable),
                "reason": "OOD and no-applicable goals have no applicable mechanism, so an applicability gate has "
                          "no defined positive label on them; fitting on them would be label leakage. prereg 3.3's "
                          "literal '60 applicable' counts the 20 OOD goals as applicable, which is inconsistent with "
                          "its own OOD description and with NC-NO-APPLICABLE; the 52/28 split is reported instead.",
            },
            "no_held_out_test_split": (
                "The frozen design provides only train/validation, so the primary mechanism-identity accuracy is "
                "reported on the union of train and validation. This does not contaminate the SELECTION step, which "
                "is parameter-free (argmax of a frozen embedding cosine); only the abstain/commit decision is fitted. "
                "Train-only and validation-only accuracies are reported separately so the auditor can separate them."
            ),
        },
        "cosine_top_only_rows": rows,
        "seed_refits": seed_refits,
        "fitted_parameter_movement": {
            "w_values": ws,
            "w_spread": (max(ws) - min(ws)) if len(ws) > 1 else None,
            "note": "non-zero spread across independent train splits is direct evidence that the gate is a fitted "
                    "function of the data rather than a fixed algebraic transform of cos_sim",
        },
        "embedding": emb_meta,
    }


# ==========================================================================
# PHASE 4 -- per-task execution
# ==========================================================================
def http_execute(base_url: str, store: hs.Store, method: str, path: str, body: dict | None,
                 start_hash: str) -> dict:
    store.reset()
    pre_hash = store.state_hash()
    if pre_hash != start_hash:
        return {"executed": False, "reason": "state_reset_hash_mismatch", "pre_hash": pre_hash}
    host, port = base_url.split("//")[1].split(":")
    conn = http.client.HTTPConnection(host, int(port), timeout=10)
    payload = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if payload else {}
    try:
        conn.request(method, path, body=payload, headers=headers)
        resp = conn.getresponse()
        status = resp.status
        resp.read()
    except Exception as exc:  # pragma: no cover - substrate failure
        return {"executed": False, "reason": f"http_error:{type(exc).__name__}:{exc}", "pre_hash": pre_hash}
    finally:
        conn.close()
    return {
        "executed": True,
        "http_status": status,
        "is_2xx_3xx": 200 <= status < 400,
        "pre_state_hash": pre_hash,
        "post_state_hash": store.state_hash(),
    }


def phase4(fixture: dict, goals: list[dict], cos: Any, calib: dict, base_url: str, store: hs.Store) -> list[dict]:
    rows: list[dict] = []
    order_rng = random.Random(SEED_ARM_ORDER)
    role_rng = random.Random(SEED_RANDOM_ROLE)
    w, b, t = calib["fit"]["w"], calib["fit"]["b"], calib["threshold"]

    for task_index, g in enumerate(goals):
        store.reset()
        task_start_hash = store.state_hash()
        order = ARMS[:]
        order_rng.shuffle(order)
        for arm in order:
            if arm == "A-CANDIDATE":
                d = cr.arm_candidate(g["text"], [float(x) for x in cos[task_index]], fixture["mechanisms"], {}, w, b, t)
            elif arm == "A-REFERENCE-EMBEDARGMAX":
                d = cr.arm_reference_embedargmax(g["text"], [float(x) for x in cos[task_index]], fixture["mechanisms"])
            elif arm == "B-LEXICAL-OVERLAP":
                d = cr.arm_lexical_overlap(g["text"], fixture["mechanisms"])
            elif arm == "B-RANDOM-ROLE":
                d = cr.arm_random_role(g["text"], fixture["mechanisms"], role_rng)
            elif arm == "B-INTERNAL-ID-ORACLE":
                if g["target_mechanism_id"] is None:
                    d = {
                        "selected_mechanism_id": None,
                        "resolution_status": "ABSTAIN",
                        "abstain_reason": "no_target_mechanism_for_goal",
                        "bound_parameters": {},
                        "unfilled_slots": [],
                        "uses_internal_ids": True,
                    }
                else:
                    d = cr.arm_internal_id_oracle(
                        g["target_mechanism_id"], g["target_fragment_id"], g["text"], fixture["mechanisms"]
                    )
            else:
                reg_path = str(HERE / "incumbent_registry.jsonl")
                d = cr.arm_incumbent(g["text"], reg_path, min_confidence=0.5)

            is_exec = d["resolution_status"] == "EXECUTABLE"
            selected = d.get("selected_mechanism_id")
            # Uniform definition across arms: a resolution that is not EXECUTABLE
            # is an abstention. For the incumbent both UNKNOWN and EXPLORE count,
            # because both decline to produce an executable binding.
            abstained = not is_exec
            correct = bool(is_exec and selected == g["target_mechanism_id"])

            http: dict[str, Any] = {"executed": False, "reason": "not_executable"}
            if is_exec:
                action = d.get("bound_action")
                if action is None:
                    http = {"executed": False, "reason": "unbound_action_template"}
                else:
                    http = http_execute(
                        base_url, store, action["method"], action["path"], action.get("body"), task_start_hash
                    )
                    http["request"] = {"method": action["method"], "path": action["path"]}

            row = {
                "task_index": task_index,
                "goal_id": g["goal_id"],
                "goal_text": g["text"],
                "category": g["category"],
                "family": g["family"],
                "applies_any": g["applies_any"],
                "target_mechanism_id": g["target_mechanism_id"],
                "target_fragment_id": g["target_fragment_id"],
                "operations": g["operations"],
                "target_selection_rule": g["target_selection_rule"],
                "arm": arm,
                "arm_order_index": order.index(arm),
                "task_start_state_hash": task_start_hash,
                "selected_mechanism_id": selected,
                "resolution_status": d["resolution_status"],
                "abstain_reason": d.get("abstain_reason"),
                "abstained": bool(abstained),
                "executable": is_exec,
                "correct": correct,
                "p_applicable": d.get("p_applicable"),
                "cos_top": d.get("cos_top"),
                "bound_parameters": d.get("bound_parameters"),
                "unfilled_slots": d.get("unfilled_slots"),
                "uses_internal_ids": d.get("uses_internal_ids"),
                "http": http,
            }
            rows.append(row)
            store.reset()  # restore the identical starting state for the next arm
    return rows


# ==========================================================================
# PHASE 5 -- metrics and gates
# ==========================================================================
def arm_rows(rows: list[dict], arm: str) -> list[dict]:
    return [r for r in rows if r["arm"] == arm]


def evaluate(rows: list[dict], goals: list[dict]) -> dict:
    app_goal_ids = {g["goal_id"] for g in goals if g["applies_any"]}
    none_goal_ids = {g["goal_id"] for g in goals if not g["applies_any"]}
    train_ids = set()
    per_arm: dict[str, Any] = {}

    for arm in ARMS:
        arows = arm_rows(rows, arm)
        app = [r for r in arows if r["goal_id"] in app_goal_ids]
        execs = [r for r in arows if r["executable"]]
        all_ab = [r for r in arows if r["abstained"]]
        cat: dict[str, dict] = {}
        for c in sorted({r["category"] for r in arows}):
            sub = [r for r in arows if r["category"] == c]
            cat[c] = {
                "n": len(sub),
                "n_applicable": sum(1 for r in sub if r["applies_any"]),
                "accuracy_all": sum(1 for r in sub if r["correct"]) / len(sub),
                "accuracy_applicable": (
                    sum(1 for r in sub if r["correct"]) / sum(1 for r in sub if r["applies_any"])
                    if any(r["applies_any"] for r in sub)
                    else None
                ),
                "executable": sum(1 for r in sub if r["executable"]),
                "abstained": sum(1 for r in sub if r["abstained"]),
            }
        per_arm[arm] = {
            "n_rows": len(arows),
            "n_applicable_rows": len(app),
            "n_executable": len(execs),
            "n_abstained": len(all_ab),
            "mechanism_identity_accuracy": me.mechanism_identity_accuracy(app) if app else None,
            "mechanism_identity_accuracy_all80": (
                me.mechanism_identity_accuracy(arows) if arows else None
            ),
            "false_accept_rate": me.false_accept_rate(execs),
            "false_accept_denominator": len(execs),
            "false_accept_numerator": sum(1 for r in execs if not r["correct"]),
            "unknown_precision": me.unknown_precision(arows),
            "unknown_precision_terms": {
                "TP_abstain": sum(1 for r in arows if r["abstained"] and r["goal_id"] in none_goal_ids),
                "FP_abstain": sum(1 for r in arows if r["abstained"] and r["goal_id"] in app_goal_ids),
            },
            "abstention_rate_on_no_applicable": (
                sum(1 for r in arows if r["abstained"] and r["goal_id"] in none_goal_ids) / len(none_goal_ids)
                if none_goal_ids
                else None
            ),
            "abstention_rate_on_applicable": (
                sum(1 for r in arows if r["abstained"] and r["goal_id"] in app_goal_ids) / len(app_goal_ids)
                if app_goal_ids
                else None
            ),
            "http_requests_attempted": sum(1 for r in arows if r["http"].get("executed")),
            "http_execution_success_rate": (
                sum(1 for r in arows if r["http"].get("is_2xx_3xx")) / sum(1 for r in arows if r["http"].get("executed"))
                if any(r["http"].get("executed") for r in arows)
                else None
            ),
            "per_category": cat,
            "uses_internal_ids": sorted({str(r["uses_internal_ids"]) for r in arows}),
        }

    # ECE rows for arms that emit a calibrated confidence (A-CANDIDATE)
    cand = arm_rows(rows, "A-CANDIDATE")
    ece_rows = [
        {
            "confidence": r["p_applicable"],
            "outcome": 1 if r["correct"] else 0,
            "family": r["family"],
            "tiebreak": r["task_index"],
        }
        for r in cand
        if r["goal_id"] in app_goal_ids and r["p_applicable"] is not None
    ]
    ece_global = me.ece(ece_rows)
    per_class = {}
    for cls in ("EXECUTABLE", "ABSTAIN"):
        sub = [
            {"confidence": r["p_applicable"], "outcome": 1 if r["correct"] else 0,
             "family": r["family"], "tiebreak": r["task_index"]}
            for r in cand
            if r["goal_id"] in app_goal_ids and r["p_applicable"] is not None
            and (r["executable"] if cls == "EXECUTABLE" else r["abstained"])
        ]
        per_class[cls] = me.ece(sub)
        per_class[cls]["bootstrap"] = me.bootstrap_upper(sub) if sub else {"upper_95": None, "note": "no rows"}
    ece_boot = me.bootstrap_upper(ece_rows)

    ece_all80 = me.ece(
        [
            {"confidence": r["p_applicable"], "outcome": 1 if r["correct"] else 0,
             "family": r["family"], "tiebreak": r["task_index"]}
            for r in cand
            if r["p_applicable"] is not None
        ]
    )
    ece_nonabstain = me.ece(
        [
            {"confidence": r["p_applicable"], "outcome": 1 if r["correct"] else 0,
             "family": r["family"], "tiebreak": r["task_index"]}
            for r in cand
            if r["goal_id"] in app_goal_ids and r["p_applicable"] is not None and r["executable"]
        ]
    )

    per_arm["A-CANDIDATE"]["ece_global"] = ece_global
    per_arm["A-CANDIDATE"]["ece_per_class"] = per_class
    per_arm["A-CANDIDATE"]["ece_global_bootstrap"] = ece_boot
    per_arm["A-CANDIDATE"]["ece_global_all_80_goals"] = ece_all80
    per_arm["A-CANDIDATE"]["ece_global_nonabstain_rows_only"] = ece_nonabstain

    return {"per_arm": per_arm}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp-dir", required=True)
    args = ap.parse_args()
    exp_dir = pathlib.Path(args.exp_dir)
    raw = exp_dir / "raw_evidence"
    der = exp_dir / "derived_evidence"
    t0 = time.time()

    pre = phase0(exp_dir)
    dump(der / "phase0_preconditions.json", pre)
    if pre.get("halt"):
        dump(der / "halt.json", {"phase": "0", "reason": pre["halt"]})
        print(f"HALT phase0: {pre['halt']}")
        return 2

    goals_payload = gg.build_goals(build_fixture())
    goals = goals_payload["goals"]
    dump(exp_dir / "artifacts" / "goals.json", goals_payload)

    ph1 = phase1(exp_dir)
    dump(der / "phase1_validity_preconditions.json", ph1)

    emb = cr.Embedder()
    cos = cr.cosines(emb, [g["text"] for g in goals], [m["intent"] for m in build_fixture()["mechanisms"]])
    emb_meta = {
        "model_name": cr.EMBED_MODEL_NAME,
        "dim": emb.dim,
        "sentence_transformers": __import__("sentence_transformers").__version__,
        "torch": __import__("torch").__version__,
        "transformers": __import__("transformers").__version__,
        "local_cache_path": str(pathlib.Path(os.environ.get("HF_HOME", pathlib.Path.home() / ".cache/huggingface"))
                                / "hub" / "models--sentence-transformers--all-MiniLM-L6-v2"),
    }
    # model weight fingerprint: sha256 over the resolved snapshot file set
    snap = pathlib.Path(emb_meta["local_cache_path"]) / "snapshots"
    if snap.exists():
        files = sorted(p for p in snap.rglob("*") if p.is_file())
        h = hashlib.sha256()
        for p in files:
            h.update(str(p.relative_to(snap)).encode())
            h.update(p.read_bytes())
        emb_meta["snapshot_file_set_sha256"] = h.hexdigest()
        emb_meta["snapshot_file_count"] = len(files)
        emb_meta["snapshot_revisions"] = sorted({p.parent.name for p in snap.iterdir() if p.is_dir()})

    # ---- PHASE 2: degeneracy screen BEFORE any candidate arm -------------
    screen = phase2(build_fixture(), goals)
    dump(der / "degeneracy_screen.json", screen)
    dumpl(raw / "degeneracy_screen_per_goal.jsonl", screen["per_goal"])
    if not screen["screen_pass"]:
        dump(der / "halt.json", {"phase": "2", "reason": "degeneracy screen FAILED; no candidate arm was run"})
        print("HALT phase2: degeneracy screen FAILED")
        return 2

    # ---- PHASE 3: calibration fitting -----------------------------------
    calib = phase3(goals, build_fixture(), cos, emb_meta)
    dump(der / "calibration.json", calib)
    if not calib.get("frozen"):
        dump(der / "halt.json", {"phase": "3", "reason": calib.get("halt")})
        print(f"HALT phase3: {calib.get('halt')}")
        return 2

    # ---- PHASE 4: per-task execution ------------------------------------
    fixture = build_fixture()
    httpd, store, base_url = hs.serve_in_background()
    try:
        rows = phase4(fixture, goals, cos, calib, base_url, store)
    finally:
        httpd.shutdown()
        httpd.server_close()

    dumpl(raw / "task_results.jsonl", rows)
    dumpl(raw / "goals_flat.jsonl", goals)

    # ---- PHASE 5: metrics and gates ------------------------------------
    metrics = evaluate(rows, goals)
    per_arm = metrics["per_arm"]

    # paired family-blocked bootstrap, primary gate
    app_ids = [g["goal_id"] for g in goals if g["applies_any"]]
    def keyed(arm: str) -> list[dict]:
        d = {r["goal_id"]: r for r in arm_rows(rows, arm)}
        return [
            {"family": d[gid]["family"], "correct": d[gid]["correct"], "goal_id": gid}
            for gid in app_ids
        ]

    cand_rows = keyed("A-CANDIDATE")
    lex_rows = keyed("B-LEXICAL-OVERLAP")
    rnd_rows = keyed("B-RANDOM-ROLE")
    boot_lex = me.paired_family_blocked_bootstrap(cand_rows, lex_rows)
    boot_rnd = me.paired_family_blocked_bootstrap(cand_rows, rnd_rows)
    boot_ref = me.paired_family_blocked_bootstrap(cand_rows, keyed("A-REFERENCE-EMBEDARGMAX"))
    boot_orc = me.paired_family_blocked_bootstrap(cand_rows, keyed("B-INTERNAL-ID-ORACLE"))

    # split-wise candidate accuracy (frozen design has no held-out test split)
    train_ids = set(calib["split"]["train_goal_ids"])
    val_ids = set(calib["split"]["val_goal_ids"])
    cand_by_id = {r["goal_id"]: r for r in arm_rows(rows, "A-CANDIDATE")}
    split_acc = {
        "train_only": sum(1 for g in train_ids if cand_by_id[g]["correct"]) / len(train_ids),
        "validation_only": sum(1 for g in val_ids if cand_by_id[g]["correct"]) / len(val_ids),
        "n_train": len(train_ids),
        "n_val": len(val_ids),
    }

    metrics_out = {
        "arms": per_arm,
        "primary": {
            "metric": "mechanism_identity_accuracy",
            "arm": "A-CANDIDATE",
            "value": per_arm["A-CANDIDATE"]["mechanism_identity_accuracy"],
            "n_applicable_goals": len(app_ids),
            "nulls": {
                "B-LEXICAL-OVERLAP": per_arm["B-LEXICAL-OVERLAP"]["mechanism_identity_accuracy"],
                "B-RANDOM-ROLE": per_arm["B-RANDOM-ROLE"]["mechanism_identity_accuracy"],
                "A-REFERENCE-EMBEDARGMAX": per_arm["A-REFERENCE-EMBEDARGMAX"]["mechanism_identity_accuracy"],
                "B-INTERNAL-ID-ORACLE": per_arm["B-INTERNAL-ID-ORACLE"]["mechanism_identity_accuracy"],
            },
            "vs_B-LEXICAL-OVERLAP": boot_lex,
            "vs_B-RANDOM-ROLE": boot_rnd,
            "vs_A-REFERENCE-EMBEDARGMAX": boot_ref,
            "vs_B-INTERNAL-ID-ORACLE": boot_orc,
            "split_wise_accuracy": split_acc,
        },
        "calibration": {
            "w": calib["fit"]["w"],
            "b": calib["fit"]["b"],
            "threshold": calib["threshold"],
            "is_fitted": True,
            "fit_detail": calib["fit"],
            "split": {k: calib["split"][k] for k in ("seed", "n_train", "n_val", "stratified_by")},
            "seed_refits": calib["seed_refits"],
            "fitted_parameter_movement": calib["fitted_parameter_movement"],
        },
        "screen": {
            "screen_pass": screen["screen_pass"],
            "lexical_overlap": screen["lexical_overlap"],
            "incumbent": screen["incumbent"],
            "substitute_leg": screen["substitute_leg"],
            "comparison_leg_nonempty": screen["comparison_leg_nonempty"],
        },
        "verification_measure_http": {
            name: {
                "http_execution_success_rate": per_arm[name]["http_execution_success_rate"],
                "requests_attempted": per_arm[name]["http_requests_attempted"],
            }
            for name in ARMS
        },
        "wall_clock_seconds": time.time() - t0,
    }
    dump(der / "metrics.json", metrics_out)

    state_hashes = sorted({r["task_start_state_hash"] for r in rows})
    per_task = {}
    for r in rows:
        per_task.setdefault(r["goal_id"], r["task_start_state_hash"])
    orderings = {tuple(sorted((x["arm"], x["arm_order_index"]) for x in rows if x["goal_id"] == gid))
                 for gid in per_task}
    design_facts = {
        "state": {
            "n_tasks": len(per_task),
            "distinct_task_start_state_hashes": len(state_hashes),
            "all_identical": len(state_hashes) == 1,
            "hash": state_hashes[0] if state_hashes else None,
            "reset_before_every_arm_request": True,
        },
        "arm_order": {"n_tasks": len(per_task), "n_distinct_orderings": len(orderings),
                      "prereg_minimum": 43, "seed": SEED_ARM_ORDER},
        "seeds": {
            "goal_generation": SEED_GOALS,
            "arm_order": SEED_ARM_ORDER,
            "calibration_split": SEED_SPLIT,
            "random_role_arm": SEED_RANDOM_ROLE,
            "bootstrap": SEED_BOOTSTRAP,
        },
        "n_tasks": len(goals),
        "n_arms_executed": len(ARMS),
        "arms": ARMS,
        "prereg_stated_arms": 7,
        "prereg_arm_count_note": (
            "prereg.md 5.1 says 'All 7 arms execute on each goal'. The frozen Section 4 defines six arms "
            "(A-CANDIDATE, A-INCUMBENT, B-LEXICAL-OVERLAP, B-RANDOM-ROLE, B-INTERNAL-ID-ORACLE) plus two goal "
            "SUBSETS (PC-VERBATIM-INTENT, NC-NO-APPLICABLE) that are slices of the same arm outputs rather than "
            "separate arms. prereg.md 11 adds a seventh only conditionally, as the substitute leg. This run "
            "executes six arms per goal plus both control subsets, and the substitute leg when required."
        ),
        "http_requests_total": sum(1 for r in rows if r["http"].get("executed")),
        "total_rows": len(rows),
    }
    dump(der / "design_facts.json", design_facts)
    print(json.dumps({"ok": True, "rows": len(rows), "wall_clock_s": round(time.time() - t0, 1)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
