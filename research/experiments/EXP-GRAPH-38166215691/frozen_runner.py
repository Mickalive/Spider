#!/usr/bin/env python3
"""
Frozen orchestration script for EXP-GRAPH-38166215691 (engine: big-pickle, DESIGN).

Binding-only measurement: no HTTP server, no LLM calls, no browser, no external task traffic.
The single external interaction is the pinned embedding-model download from HuggingFace Hub.

This script is a verbatim transcription embedded in prereg.md section 14; EXECUTE records its
sha256 in provenance.json. All outcome-bearing modules are bound by freeze.json.artifact_hashes
(V12-FREEZE-BINDING). It writes derived/measurements.json, derived/predictions.json and
derived/contamination.json and exits 0 with the status carried inside measurements.json.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
HARNESS = REPO / "research" / "harness"
SRC = REPO / "src"
OUT = HERE / "derived"

EXP_ID = "EXP-GRAPH-38166215691"
BANK_SHA = "fb4d3246990731c95f4cf4cfa5870ac7f02da8832eed324580be5f75b1456c6e"
SEED32 = 3806477323  # 38166215691 % 2**32
CONTAM_T = 0.60
CONTAM_MAX_FLAGGED = 20
PRIMARY_MIN = 80
FLOOR_MAX = 0.35
NC_LABEL_MAX = 0.20
NC_RANDOM_MAX = 0.25
AB_FA_MAX = 0.10
AB_PREC_MIN = 0.85
AB_COV_MIN = 0.50
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REV = "c9745ed1d9f207416be6d2e6f8de32d1f161f9bf"
BOUND_FILES = [
    "research/harness/candidate_resolver.py",
    "research/harness/goal_generator.py",
    "research/harness/http_server.py",
    "research/harness/experiment_runner.py",
    "src/spider/kernel.py",
    "src/spider/registry.py",
    "src/spider/models.py",
    "src/spider/__init__.py",
]


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _jaccard(a: str, b: str) -> float:
    A = set(a.lower().split())
    B = set(b.lower().split())
    return len(A & B) / len(A | B) if (A | B) else 0.0


def _select_index(scores) -> int:
    """Shared argmax-over-20 rule (first-max tie-break), used by the embed and random pipelines."""
    best = 0
    for i in range(1, len(scores)):
        if scores[i] > scores[best]:
            best = i
    return best


def _credit(idx: int, goal: dict, mech_ids) -> bool:
    """Shared mechanism-identity credit rule; never credits an abstention."""
    return (
        goal["applicable"]
        and goal["target_mechanism_id"] != ""
        and mech_ids[idx] == goal["target_mechanism_id"]
    )


def _abort(status: str, reason: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "measurements.json").write_text(
        json.dumps(
            {"experiment_id": EXP_ID, "status": status, "outcome": "INCONCLUSIVE", "reason": reason},
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[runner] {status}: {reason}")
    sys.exit(0)


def main() -> None:
    out = {
        "experiment_id": EXP_ID,
        "status": "COMPLETE",
        "outcome": "INCONCLUSIVE",
        "reason": None,
        "gates": {},
        "metrics": {},
        "controls": {},
        "observations": [],
        "validity_notes": [],
        "artifacts": [],
        "env": {},
        "abstention": {},
    }

    # ---------------- V12-FREEZE-BINDING ----------------
    freeze = HERE / "freeze.json"
    if not freeze.exists():
        _abort("MEASUREMENT_INVALID", "V12: freeze.json missing; experiment is not bound")
    freeze_json = json.loads(freeze.read_text(encoding="utf-8"))
    expected = freeze_json.get("artifact_hashes", {})
    bound = {}
    v12 = True
    for rel in BOUND_FILES:
        p = REPO / rel
        h = _sha_file(p) if p.exists() else None
        bound[rel] = h
        if h is None or expected.get(rel) != h:
            v12 = False
    out["gates"]["V12-FREEZE-BINDING"] = v12
    out["artifacts"].append({"path": "freeze.json", "role": "freeze", "sha256": _sha_file(freeze)})
    for rel in sorted(bound):
        out["artifacts"].append({"path": rel, "role": "code", "sha256": bound[rel]})

    # ---------------- V4-AUTHORSHIP-PROVENANCE (bank fingerprint) ----------------
    prereg_text = (HERE / "prereg.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- BEGIN GOAL BANK -->\n(.*?)\n<!-- END GOAL BANK -->", prereg_text, re.S)
    if not m:
        _abort("MEASUREMENT_INVALID", "V4: goal-bank markers not found in prereg.md")
    bank_block = m.group(1) + "\n"
    if _sha_text(bank_block) != BANK_SHA:
        _abort("MEASUREMENT_INVALID", "V4: goal bank sha256 mismatch: " + _sha_text(bank_block))
    try:
        goals = [json.loads(line) for line in bank_block.splitlines() if line.strip()]
    except Exception as e:  # noqa: BLE001
        _abort("MEASUREMENT_INVALID", f"V4: bank JSON parse error: {e!r}")
    if len(goals) != 140:
        _abort("MEASUREMENT_INVALID", f"V4: expected 140 goals, got {len(goals)}")
    out["gates"]["V4-AUTHORSHIP-PROVENANCE"] = True
    out["artifacts"].append(
        {"path": "prereg.md", "role": "prereg", "sha256": _sha_text(prereg_text), "bank_sha256": BANK_SHA}
    )
    out["env"]["python"] = sys.version.split()[0]
    out["env"]["seed32"] = SEED32

    # ---------------- environment prerequisites ----------------
    try:
        import numpy as np

        out["env"]["numpy"] = np.__version__
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"numpy unavailable: {e!r}")
    try:
        import sklearn

        out["env"]["sklearn"] = sklearn.__version__
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"sklearn unavailable: {e!r}")
    try:
        import torch

        out["env"]["torch"] = torch.__version__
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"torch unavailable: {e!r}")
    try:
        import sentence_transformers

        out["env"]["sentence_transformers"] = sentence_transformers.__version__
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"sentence_transformers unavailable: {e!r}")

    # ---------------- harness import (experiment_runner chdir side effect handled) ----------------
    start_cwd = os.getcwd()
    sys.path.insert(0, str(HARNESS))
    sys.path.insert(0, str(SRC))
    try:
        from candidate_resolver import (  # noqa: F401
            EmbeddingArgmaxResolver,
            InternalIdOracle,
            LexicalOverlapResolver,
            RandomRoleResolver,
            create_fixture,
        )
        from experiment_runner import compute_ece, paired_bootstrap  # noqa: F401
        from goal_generator import (  # noqa: F401
            INTENTS,
            NO_APPLICABLE_TEMPLATES,
            OOD_PARAPHRASES,
            PARAPHRASES,
        )
        from spider.kernel import SpiderKernel
        from spider.models import Mechanism as KernelMechanism
        from spider.registry import MechanismRegistry
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"harness import failed: {e!r}")
    os.chdir(start_cwd)

    # ---------------- embedding model ----------------
    try:
        from sentence_transformers import SentenceTransformer

        try:
            model = SentenceTransformer(MODEL_NAME, revision=MODEL_REV)
            model_revision = MODEL_REV
        except Exception:  # noqa: BLE001
            model = SentenceTransformer(MODEL_NAME)
            model_revision = None
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"embedding model load failed: {e!r}")
    out["env"]["model"] = MODEL_NAME
    out["env"]["model_revision"] = model_revision

    # ---------------- fixture ----------------
    mechs = create_fixture()
    mech_ids = [mm.mechanism_id for mm in mechs]
    intents = [mm.intent for mm in mechs]
    n_mech = len(mechs)
    if n_mech != 20:
        _abort("MEASUREMENT_INVALID", f"V1: fixture has {n_mech} mechanisms, expected 20")

    # ---------------- V3-CONTAM-SCREEN (against every prior authoring surface) ----------------
    prior_texts = (
        list(intents)
        + [v for vs in PARAPHRASES.values() for v in vs]
        + list(NO_APPLICABLE_TEMPLATES)
        + list(OOD_PARAPHRASES)
    )
    contamination = {}
    flagged = set()
    for g in goals:
        mix = max(_jaccard(g["text"], it) for it in intents)
        mpx = max(_jaccard(g["text"], pt) for pt in prior_texts)
        contamination[g["goal_id"]] = {
            "max_intent_jaccard": round(mix, 4),
            "max_prior_jaccard": round(mpx, 4),
        }
        if mpx >= CONTAM_T:
            flagged.add(g["goal_id"])
    n_flagged = len(flagged)
    out["metrics"]["M-N-CONTAM-FLAGGED"] = n_flagged
    out["metrics"]["M-CONTAM-FLAGGED-IDS"] = sorted(flagged)
    v3 = n_flagged <= CONTAM_MAX_FLAGGED
    out["gates"]["V3-CONTAM-SCREEN"] = v3

    # ---------------- primary set and splits ----------------
    primary = [g for g in goals if g["applicable"] and g["goal_id"] not in flagged]
    cal = [g for g in goals if g["split"] == "calibration" and g["goal_id"] not in flagged]
    test = [g for g in goals if g["split"] == "test" and g["goal_id"] not in flagged]
    cal_app = [g for g in cal if g["applicable"]]
    cal_oos = [g for g in cal if not g["applicable"]]
    test_app = [g for g in test if g["applicable"]]
    test_oos = [g for g in test if not g["applicable"]]
    out["metrics"]["M-N-PRIMARY"] = len(primary)
    out["metrics"]["M-N-CAL"] = {"applicable": len(cal_app), "oos": len(cal_oos)}
    out["metrics"]["M-N-TEST"] = {"applicable": len(test_app), "oos": len(test_oos)}
    v2 = len(primary) >= PRIMARY_MIN
    out["gates"]["V2-PRIMARY-SET"] = v2
    if len(primary) == 0:
        _abort("MEASUREMENT_INVALID", "V2: empty primary set; nothing to measure")

    # ---------------- arm construction ----------------
    embed = EmbeddingArgmaxResolver(mechs, model)
    lexical = LexicalOverlapResolver(mechs)
    random_role = RandomRoleResolver(mechs, seed=4242)
    oracle = InternalIdOracle(mechs)

    # kernel registry distilled from the 20 verbatim intents (incumbent baseline + PC sub-check ii)
    kernel_reg_path = OUT / "kernel_registry.jsonl"
    kernel_mechs = [
        KernelMechanism(
            mechanism_id=mm.mechanism_id,
            intent=mm.intent,
            preconditions={},
            action_template={},
            postconditions={},
            parameter_slots=list(mm.parameter_slots),
            confidence=1.0,
        )
        for mm in mechs
    ]
    kernel_reg = MechanismRegistry(kernel_reg_path)
    kernel_reg.replace(kernel_mechs)
    kernel = SpiderKernel(kernel_reg, min_confidence=0.8)

    # ---------------- resolution loop (all 140 goals; selection scored on primary) ----------------
    predictions = {}
    for g in goals:
        goal_id = g["goal_id"]
        er = embed.resolve(g)
        lr = lexical.resolve(g)
        rr = random_role.resolve(g)
        oo = oracle.resolve(g)
        predictions[goal_id] = {
            "goal_id": goal_id,
            "text": g["text"],
            "applicable": g["applicable"],
            "target_mechanism_id": g["target_mechanism_id"],
            "family": g.get("family"),
            "split": g["split"],
            "embed_mechanism_id": er.mechanism_id,
            "embed_confidence": float(er.confidence),
            "lexical_mechanism_id": lr.mechanism_id,
            "lexical_confidence": float(lr.confidence),
            "random_mechanism_id": rr.mechanism_id,
            "oracle_mechanism_id": oo.mechanism_id,
        }

    def acc_of(preds, key: str, gs) -> tuple[int, int]:
        nums = 0
        for g in gs:
            if preds[g["goal_id"]][key] == g["target_mechanism_id"]:
                nums += 1
        return nums, len(gs)

    embed_c, embed_d = acc_of(predictions, "embed_mechanism_id", primary)
    lex_c, lex_d = acc_of(predictions, "lexical_mechanism_id", primary)
    rand_c, rand_d = acc_of(predictions, "random_mechanism_id", primary)
    orac_c, orac_d = acc_of(predictions, "oracle_mechanism_id", primary)

    # incumbent kernel on primary (exact-intent match; by construction 0)
    inc_c = 0
    for g in primary:
        res = kernel.resolve(g["text"], {})
        if res.mechanism_id is not None and res.mechanism_id == g["target_mechanism_id"]:
            inc_c += 1
    inc_d = len(primary)

    out["metrics"]["M-MECH-ACC-EMBED"] = {"value": embed_c / embed_d, "numerator": embed_c, "denominator": embed_d}
    out["metrics"]["M-MECH-ACC-LEXICAL"] = {"value": lex_c / lex_d, "numerator": lex_c, "denominator": lex_d}
    out["metrics"]["M-MECH-ACC-RANDOM"] = {"value": rand_c / rand_d, "numerator": rand_c, "denominator": rand_d}
    out["metrics"]["M-MECH-ACC-INCUMBENT"] = {"value": inc_c / inc_d, "numerator": inc_c, "denominator": inc_d}
    out["metrics"]["M-MECH-ACC-ORACLE"] = {"value": orac_c / orac_d, "numerator": orac_c, "denominator": orac_d}

    # V1-METRIC-DEFINITION: every arm denominator equals |primary| (>= 1)
    v1 = (
        len(primary) > 0
        and embed_d == len(primary)
        and lex_d == len(primary)
        and rand_d == len(primary)
        and orac_d == len(primary)
    )
    out["gates"]["V1-METRIC-DEFINITION"] = v1

    # ---------------- primary bootstrap (V11) ----------------
    np.random.seed(SEED32)
    fams = np.array([g["family"] for g in primary])
    embed_scores = np.array([1.0 if predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    lex_scores = np.array([1.0 if predictions[g["goal_id"]]["lexical_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    obs_diff, lower_ci, upper_ci = paired_bootstrap(embed_scores, lex_scores, fams, n_resamples=10000, alpha=0.05)
    n_fams = int(len(np.unique(fams)))
    out["metrics"]["M-PAIRED-DIFF-EMBED-MINUS-LEXICAL"] = {
        "obs_diff": float(obs_diff),
        "lower_ci": float(lower_ci),
        "upper_ci": float(upper_ci),
    }
    out["metrics"]["M-BOOTSTRAP-ARGS"] = {
        "n_resamples": 10000,
        "alpha": 0.05,
        "seed": SEED32,
        "n_families": n_fams,
    }
    v11 = n_fams == 5
    out["gates"]["V11-BOOTSTRAP-SEED"] = v11
    out["metrics"]["M-N-FAMILIES"] = n_fams

    # ---------------- V9-NON-TAUTOLOGY ----------------
    disagree = sum(
        1
        for g in primary
        if predictions[g["goal_id"]]["embed_mechanism_id"] != predictions[g["goal_id"]]["lexical_mechanism_id"]
    )
    v9 = disagree >= 1 and (lex_c / lex_d) < 0.99
    out["gates"]["V9-NON-TAUTOLOGY"] = v9
    out["metrics"]["M-NON-TAUTOLOGY"] = {
        "disagreement_count": disagree,
        "lexical_accuracy": lex_c / lex_d,
    }

    # ---------------- V7-TREATMENT-LIVENESS ----------------
    embed_selected = [predictions[g["goal_id"]]["embed_mechanism_id"] for g in primary]
    distinct_embed = len(set(embed_selected))
    valid_embed = all(sid in mech_ids for sid in embed_selected)
    v7 = distinct_embed >= 2 and valid_embed
    out["gates"]["V7-TREATMENT-LIVENESS"] = v7
    out["metrics"]["M-EMBED-DISTINCT-SELECTIONS"] = distinct_embed

    # ---------------- V6-ORACLE-CEILING, V8-FLOOR-SANITY ----------------
    v6 = (orac_c / orac_d) == 1.0
    v8 = (rand_c / rand_d) <= FLOOR_MAX
    out["gates"]["V6-ORACLE-CEILING"] = v6
    out["gates"]["V8-FLOOR-SANITY"] = v8
    out["metrics"]["M-ORACLE-CEILING"] = {"value": orac_c / orac_d, "numerator": orac_c, "denominator": orac_d}
    out["metrics"]["M-FLOOR-RANDOM"] = {"value": rand_c / rand_d, "numerator": rand_c, "denominator": rand_d}

    # ---------------- V5-PC-LIVENESS-AND-INTEGRITY ----------------
    pc_fixture_unique = (len(set(mech_ids)) == 20) and (len(set(intents)) == 20)
    pc_incumbent = 0
    for k, mm in enumerate(mechs):
        params = {slot: f"v_{slot}" for slot in mm.parameter_slots}
        res = kernel.resolve(mm.intent, {}, params)
        if res.status.value == "EXECUTABLE" and res.mechanism_id == mm.mechanism_id:
            pc_incumbent += 1
    pc_lex_self = 0
    pc_emb_self = 0
    for k, mm in enumerate(mechs):
        g = {"goal_id": f"self_{k}", "text": mm.intent, "target_mechanism_id": mm.mechanism_id, "applicable": True}
        lr = lexical.resolve(g)
        er = embed.resolve(g)
        if lr.mechanism_id == mm.mechanism_id:
            pc_lex_self += 1
        if er.mechanism_id == mm.mechanism_id:
            pc_emb_self += 1
    v5 = pc_fixture_unique and pc_incumbent == 20 and pc_lex_self == 20 and pc_emb_self == 20
    out["gates"]["V5-PC"] = v5
    out["metrics"]["M-PC-LIVENESS-AND-INTEGRITY"] = {
        "fixture_unique": pc_fixture_unique,
        "incumbent_verbatim": pc_incumbent,
        "lexical_self": pc_lex_self,
        "embed_self": pc_emb_self,
    }
    out["controls"]["PC-LIVENESS-AND-INTEGRITY"] = {
        "expected": "fixture 20/20 unique ids and intents; incumbent verbatim 20/20 EXECUTABLE at correct id; lexical_self 20/20; embed_self 20/20",
        "observed": f"fixture_unique={pc_fixture_unique}, incumbent_verbatim={pc_incumbent}/20, lexical_self={pc_lex_self}/20, embed_self={pc_emb_self}/20",
        "pass": v5,
        "evidence_ref": "derived/predictions.json",
    }

    # ---------------- V10-NC-SHUFFLE ----------------
    rng_shuf = np.random.RandomState(SEED32 + 100)
    while True:
        perm = rng_shuf.permutation(20)
        if all(perm[i] != i for i in range(20)):
            break
    nc_label_c = 0
    for g in primary:
        ti = mech_ids.index(g["target_mechanism_id"])
        shifted = int(perm[ti])
        # score the embed selection against the deranged label (chance = 1/20)
        sel = predictions[g["goal_id"]]["embed_mechanism_id"]
        if sel in mech_ids and mech_ids.index(sel) == shifted:
            nc_label_c += 1
    nc_label = nc_label_c / len(primary)
    rng_rand = np.random.RandomState(SEED32 + 101)
    nc_rand_c = 0
    for g in primary:
        scores = rng_rand.uniform(size=20)
        idx = _select_index(scores)
        if _credit(idx, g, mech_ids):
            nc_rand_c += 1
    nc_rand = nc_rand_c / len(primary)
    v10 = nc_label <= NC_LABEL_MAX and nc_rand <= NC_RANDOM_MAX
    out["gates"]["V10-NC-SHUFFLE"] = v10
    out["metrics"]["M-NC-SHUFFLED"] = {
        "nc_shuffled_label": round(nc_label, 4),
        "nc_random_score": round(nc_rand, 4),
        "bounds": {"nc_shuffled_label_max": NC_LABEL_MAX, "nc_random_score_max": NC_RANDOM_MAX},
    }
    out["controls"]["NC-SHUFFLED-LABEL"] = {
        "expected": f"<= {NC_LABEL_MAX}",
        "observed": f"{nc_label:.4f}",
        "pass": nc_label <= NC_LABEL_MAX,
        "evidence_ref": "derived/predictions.json",
    }
    out["controls"]["NC-RANDOM-SCORE"] = {
        "expected": f"<= {NC_RANDOM_MAX}",
        "observed": f"{nc_rand:.4f}",
        "pass": nc_rand <= NC_RANDOM_MAX,
        "evidence_ref": "derived/predictions.json",
    }

    # ---------------- D-ABSTENTION (secondary, non-gating) ----------------
    embed_conf = {gid: predictions[gid]["embed_confidence"] for gid in predictions}

    def abstention_report(gs):
        app = [g for g in gs if g["applicable"]]
        oos = [g for g in gs if not g["applicable"]]
        if not app or not oos:
            return None
        ts = sorted({embed_conf[g["goal_id"]] for g in gs})
        feasible = []
        for t in ts:
            exec_oos = sum(1 for g in oos if embed_conf[g["goal_id"]] >= t)
            abst_all = [g for g in gs if embed_conf[g["goal_id"]] < t]
            abst_oos = sum(1 for g in oos if embed_conf[g["goal_id"]] < t)
            fa = exec_oos / len(oos)
            prec = abst_oos / len(abst_all) if abst_all else None
            if fa <= AB_FA_MAX and prec is not None and prec >= AB_PREC_MIN:
                feasible.append(t)
        if feasible:
            feasible_flag = True
            t_star = feasible[0]
        else:
            feasible_flag = False
            cand = []
            for t in ts:
                exec_oos = sum(1 for g in oos if embed_conf[g["goal_id"]] >= t)
                abst_all = [g for g in gs if embed_conf[g["goal_id"]] < t]
                abst_oos = sum(1 for g in oos if embed_conf[g["goal_id"]] < t)
                fa = exec_oos / len(oos)
                prec = abst_oos / len(abst_all) if abst_all else None
                if prec is not None and prec >= AB_PREC_MIN:
                    cand.append((abs(fa - AB_FA_MAX), t))
            t_star = min(cand)[1] if cand else 1.0
        return {"feasible": feasible_flag, "t_star": float(t_star)}

    cal_report = abstention_report(cal)
    if cal_report is None:
        out["abstention"] = {"class": "AB-MEASUREMENT-INVALID", "reason": "cal split missing an applicable or oos class"}
    else:
        t_star = cal_report["t_star"]
        exec_oos = sum(1 for g in test_oos if embed_conf[g["goal_id"]] >= t_star)
        exec_app = sum(1 for g in test_app if embed_conf[g["goal_id"]] >= t_star)
        abst_all = [g for g in test if embed_conf[g["goal_id"]] < t_star]
        abst_oos = sum(1 for g in test_oos if embed_conf[g["goal_id"]] < t_star)
        abst_app = sum(1 for g in test_app if embed_conf[g["goal_id"]] < t_star)
        coverage = exec_app / len(test_app)
        fa = exec_oos / len(test_oos)
        prec = abst_oos / len(abst_all) if abst_all else None
        ab_met = (
            fa <= AB_FA_MAX
            and prec is not None
            and prec >= AB_PREC_MIN
            and coverage >= AB_COV_MIN
        )
        out["abstention"] = {
            "class": "AB-MET" if ab_met else "AB-NOT-MET",
            "cal_feasible": cal_report["feasible"],
            "t_star": float(t_star),
            "test_coverage": round(coverage, 4),
            "test_pooled_false_accept": round(fa, 4),
            "test_unknown_precision": None if prec is None else round(prec, 4),
            "test_exec_app": exec_app,
            "test_exec_oos": exec_oos,
            "test_abst_app": abst_app,
            "test_abst_oos": abst_oos,
            "targets": {"coverage_min": AB_COV_MIN, "fa_max": AB_FA_MAX, "precision_min": AB_PREC_MIN},
        }
    out["metrics"]["M-ABSTENTION"] = out["abstention"]

    # ---------------- ECE (descriptive only, NOT gated) ----------------
    ece_confs = np.array([embed_conf[g["goal_id"]] for g in primary])
    ece_accs = np.array([
        1.0 if predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"] else 0.0
        for g in primary
    ])
    out["metrics"]["M-ECE-GLOBAL"] = {"value": compute_ece(ece_confs, ece_accs), "note": "descriptive, NOT gated"}

    # ---------------- overall status / outcome ----------------
    gated = [k for k, v in out["gates"].items() if not v]
    if gated:
        out["status"] = "MEASUREMENT_INVALID"
        out["outcome"] = "INCONCLUSIVE"
        out["reason"] = "validity gates failed: " + ", ".join(gated)
    else:
        out["status"] = "COMPLETE"
        if obs_diff <= 0:
            out["outcome"] = "FALSIFIES"
        elif lower_ci > 0:
            out["outcome"] = "SUPPORTS"
        else:
            out["outcome"] = "MIXED"

    out["observations"] = [
        "OBS-AUTHOR-INDEPENDENCE: goal bank authored by two fresh-context processes that never saw the 20 registry intents or any repository file (provenance record in prereg.md section 5)",
        f"OBS-CONTAMINATION: {n_flagged}/140 goals flagged at max prior-text Jaccard >= {CONTAM_T}; ids={sorted(flagged)}",
        f"OBS-PRIMARY-SET: |primary|={len(primary)} (cal {len(cal_app)} applicable/{len(cal_oos)} oos; test {len(test_app)} applicable/{len(test_oos)} oos)",
        f"OBS-ACCURACIES: embed={embed_c}/{embed_d}, lexical={lex_c}/{lex_d}, random={rand_c}/{rand_d}, incumbent={inc_c}/{inc_d}, oracle={orac_c}/{orac_d}",
        f"OBS-PAIRED-DIFF: obs={obs_diff:.4f} CI=[{lower_ci:.4f},{upper_ci:.4f}] (families={n_fams}, B=10000, alpha=0.05, seed={SEED32})",
        "OBS-ABSTENTION: " + json.dumps(out["abstention"]),
    ]
    out["validity_notes"] = [
        "VN-01: binding-only measurement; no HTTP server started, no LLM calls, no task traffic; single HuggingFace model download (pinned revision recorded).",
        "VN-02: mechanism-identity correctness ignores parameter binding; parameter binding is out of scope for this packet.",
        "VN-03: bootstrap covers resampling variability only (family-blocked, seed 3806477323); single embedding model, no ensemble.",
        "VN-04: contamination screen tokenises like B-LEXICAL-OVERLAP (lowercase whitespace split, set Jaccard) and screens against the union of the 20 intents, PARAPHRASES, NO_APPLICABLE_TEMPLATES and OOD_PARAPHRASES from the bound goal_generator.py.",
        "VN-05: ECE is descriptive only and NOT a gate (mandate item iii; prior EXP-GRAPH-36287167610 audit VF-06 unattainability).",
        "VN-06: vectorized barrier: sentence_transformers, torch, numpy, scikit-learn must be importable; failure => BLOCKED.",
    ]
    out["artifacts"].extend(
        [
            {"path": "derived/predictions.json", "role": "raw"},
            {"path": "derived/contamination.json", "role": "derived"},
            {"path": "derived/measurements.json", "role": "derived"},
        ]
    )

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "predictions.json").write_text(json.dumps(predictions, indent=2), encoding="utf-8")
    (OUT / "contamination.json").write_text(json.dumps(contamination, indent=2), encoding="utf-8")
    (OUT / "measurements.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": out["status"],
                "outcome": out["outcome"],
                "gates_failed": gated,
                "obs_diff": float(obs_diff),
                "lower_ci": float(lower_ci),
                "embed_acc": embed_c / embed_d,
                "lexical_acc": lex_c / lex_d,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        import traceback

        traceback.print_exc()
        _abort("BLOCKED", f"runner crashed: {e!r}")