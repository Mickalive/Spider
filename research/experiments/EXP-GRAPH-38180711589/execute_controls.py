#!/usr/bin/env python3
"""EXECUTE-side control and validity harness for EXP-GRAPH-38180711589.

The frozen FROZEN-RUNNER block (runner_frozen.py) computes the claim-bearing
D-PRIMARY gate triplet, the CTRL-EXEC-ALL / CTRL-ABSTAIN-ALL / CTRL-RANDOM-GATE
boundary controls and the axes. The frozen spec additionally REQUIRES the
positive control (PC-LIVENESS-AND-INTEGRITY), the null controls
(NC-SHUFFLED-LABEL / NC-CONSTANT-SIGNAL), the strong baselines
(B-LEXTOK-JACCARD / B-RANDOM-ROLE / B-INCUMBENT-KERNEL / B-INTERNAL-ID-ORACLE),
the contamination maxima and the V5-V10/V13 validity gates. The frozen runner
does not emit those, so EXECUTE computes them here from the SAME frozen blocks,
the SAME frozen runner functions (imported, not re-derived) and the SAME
model-free arm logic that is defined in the hash-bound
research/harness/candidate_resolver.py.

candidate_resolver.py imports numpy/scikit-learn/sentence-transformers at module
top; the sentence-embedding stack is unavailable at EXECUTE (retention arms are
BLOCKED by design). The model-free arm classes (LexicalOverlapResolver,
RandomRoleResolver, InternalIdOracle) and create_fixture are therefore
transcribed verbatim in behaviour from that frozen source, not re-designed.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path("/home/runner/work/Spider/Spider")
EXP = ROOT / "research/experiments/EXP-GRAPH-38180711589"
PARENT_PREREG = ROOT / "research/experiments" / "EXP-GRAPH-38175554380/prereg.md"

# import the frozen runner module to reuse its exact comp/S/build_axis/metrics/calibrate
spec = importlib.util.spec_from_file_location("runner_frozen", EXP / "runner_frozen.py")
rf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rf)

prereg_text = (EXP / "prereg.md").read_text(encoding="utf-8")
g1_app = rf.jlines(rf.extract_block(prereg_text, "GOAL-BANK-G1"))
g1_oos = rf.jlines(rf.extract_block(prereg_text, "OOS-BANK-G1"))
lex_g1 = json.loads(rf.extract_block(prereg_text, "LEXICON-G1"))
parent_text = PARENT_PREREG.read_text(encoding="utf-8")
prior_parent = json.loads(rf.extract_block(parent_text, "PRIOR-PARENT-BANK-TEXTS"))

import sys
sys.path.insert(0, str(ROOT / "research/harness"))
from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES, PARAM_SLOTS
gg = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
     list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
prior_full = gg + list(prior_parent)

# ---------------------------------------------------------------- primary axis
bound, flagged = rf.build_axis(g1_app, g1_oos, lex_g1, 6, prior_full)
cal = [r for r in bound if not r["split"]]
test = [r for r in bound if r["split"]]
app_all = [r for r in bound if r["app"]]
oos_all = [r for r in bound if not r["app"]]
tstar, cal_class = rf.calibrate(cal)

out = {}

# ---------------------------------------------------------------- set sizes
out["M-N-PRIMARY-APPLICABLE"] = len(app_all)
out["M-N-PRIMARY-OOS"] = len(oos_all)
out["M-N-CAL"] = {"applicable": len([r for r in cal if r["app"]]), "oos": len([r for r in cal if not r["app"]])}
out["M-N-TEST"] = {"applicable": len([r for r in test if r["app"]]), "oos": len([r for r in test if not r["app"]])}
out["M-FLAGGED-IDS"] = flagged
out["M-N-CONTAM-FLAGGED"] = len(flagged)

# contamination maxima over the AXIS-PRIMARY all rows vs prior_full
def max_jac(rows):
    mt, mg = 0.0, 0.0
    for r in rows:
        for p in prior_full:
            mt = max(mt, rf.jaccard(rf.tokens(r["text"]), rf.tokens(p)))
            mg = max(mg, rf.jaccard(rf.trigrams(r["text"]), rf.trigrams(p)))
    return mt, mg
mt, mg = max_jac(app_all + oos_all)
out["M-CONTAM-MAX-JACCARD"] = {"max_token_jaccard": mt, "max_trigram_jaccard": mg,
                               "thresholds": {"token": rf.TOK_BAND, "trigram": rf.TRI_BAND}}

# ---------------------------------------------------------------- B-LEX-STRONG det accuracy
def det_correct(rows):
    a = [r for r in rows if r["app"]]
    return sum(1 for r in a if r["mech"] == r["target"]), len(a)
det_all, det_all_d = det_correct(app_all)
det_test, det_test_d = det_correct(test)
out["M-DET-ACC-PRIMARY"] = {"value": det_all / det_all_d if det_all_d else None, "numerator": det_all, "denominator": det_all_d}
out["M-DET-ACC-PRIMARY-TEST"] = {"value": det_test / det_test_d if det_test_d else None, "numerator": det_test, "denominator": det_test_d}

# ---------------------------------------------------------------- fixture (20 mechanisms)
FAMILIES = ["users", "posts", "comments", "albums", "photos"]
OPS = ["create", "read", "update", "delete"]
FIXTURE = [{"mechanism_id": f"mech_{fam}_{op}", "intent": INTENTS[f"mech_{fam}_{op}"],
            "parameter_slots": PARAM_SLOTS[f"mech_{fam}_{op}"], "role": op, "family": fam, "verb": op.upper()}
           for fam in FAMILIES for op in OPS]
fix_ids = [m["mechanism_id"] for m in FIXTURE]
fix_intents = [m["intent"] for m in FIXTURE]
fix_by_id = {m["mechanism_id"]: m for m in FIXTURE}

# ---------------------------------------------------------------- PC (i)+(ii)+(iii)
pc_unique_ids = len(set(fix_ids)) == 20 and len(fix_ids) == 20
pc_unique_intents = len(set(fix_intents)) == 20 and len(fix_intents) == 20

# (ii) incumbent verbatim via shipped src/spider kernel over a 20-intent registry
sys.path.insert(0, str(ROOT / "src"))
from spider.kernel import SpiderKernel
from spider.registry import MechanismRegistry
from spider.models import Mechanism as KMechanism

reg_path = EXP / "derived" / "kernel_registry.jsonl"
reg = MechanismRegistry(reg_path)
reg.replace([KMechanism(
    mechanism_id=m["mechanism_id"], intent=m["intent"],
    preconditions={}, action_template={}, postconditions={},
    confidence=0.95) for m in FIXTURE])
kernel = SpiderKernel(reg, min_confidence=0.8)
pc_incumbent = 0
for m in FIXTURE:
    res = kernel.resolve(m["intent"], {})
    if str(res.status).endswith("EXECUTABLE") and res.mechanism_id == m["mechanism_id"]:
        pc_incumbent += 1

# (iii) B-LEX-STRONG self-match on the 20 verbatim intents
pc_selfmatch = 0
for m in FIXTURE:
    r = rf.comp(m["intent"], lex_g1)
    if r["mech"] == m["mechanism_id"]:
        pc_selfmatch += 1

out["M-PC-LIVENESS-AND-INTEGRITY"] = {
    "fixture_unique_ids": pc_unique_ids, "fixture_unique_intents": pc_unique_intents,
    "incumbent_verbatim": pc_incumbent, "resolver_self_match": pc_selfmatch,
    "n_fixture": 20,
    "subcheck_i_pass": bool(pc_unique_ids and pc_unique_intents),
    "subcheck_ii_pass": pc_incumbent == 20,
    "subcheck_iii_pass": pc_selfmatch == 20,
    "pass": bool(pc_unique_ids and pc_unique_intents and pc_incumbent == 20 and pc_selfmatch == 20),
}

# ---------------------------------------------------------------- B-INCUMBENT-KERNEL on primary
inc_correct = 0
for r in app_all:
    res = kernel.resolve(r["text"], {})
    if str(res.status).endswith("EXECUTABLE") and res.mechanism_id == r["target"]:
        inc_correct += 1
out["M-MECH-ACC-INCUMBENT"] = {"value": inc_correct / len(app_all), "numerator": inc_correct, "denominator": len(app_all)}

# ---------------------------------------------------------------- B-INTERNAL-ID-ORACLE on primary
ora_correct = 0
for r in app_all:
    tid = r["target"]
    if tid and tid in fix_by_id:
        sel = tid
    else:
        sel = ""
    if sel == tid:
        ora_correct += 1
out["M-MECH-ACC-ORACLE"] = {"value": ora_correct / len(app_all), "numerator": ora_correct, "denominator": len(app_all)}

# ---------------------------------------------------------------- B-RANDOM-ROLE on primary (candidate_resolver RandomRoleResolver, seed 4242)
rng = np.random.RandomState(4242)
ROLE_KEYWORDS = {
    "create": ["create", "add", "new", "make", "register", "publish", "write", "upload"],
    "read": ["get", "retrieve", "fetch", "look up", "find", "show", "view"],
    "update": ["update", "edit", "modify", "change", "alter"],
    "delete": ["delete", "remove", "erase", "delete", "take down", "drop"],
}
ROLE_KEYS = ["create", "read", "update", "delete"]  # insertion order of mechanism_by_role
fam_by_role = {op: [f"mech_{fam}_{op}" for fam in FAMILIES] for op in OPS}

def infer_role(text):
    low = text.lower()
    scores = {role: sum(1 for kw in kws if kw in low) for role, kws in ROLE_KEYWORDS.items()}
    if max(scores.values()) == 0:
        return rng.choice(ROLE_KEYS)
    return max(scores, key=scores.get)

rand_correct = 0
for r in app_all:
    role = infer_role(r["text"])
    cands = fam_by_role.get(role, fix_ids)
    sel = rng.choice(cands)
    if sel == r["target"]:
        rand_correct += 1
out["M-MECH-ACC-RANDOM"] = {"value": rand_correct / len(app_all), "numerator": rand_correct, "denominator": len(app_all),
                            "rng": "numpy.random.RandomState(4242)"}

# ---------------------------------------------------------------- B-LEXTOK-JACCARD on primary (LexicalOverlapResolver)
def tok_set(s):
    return set(s.lower().split())
def lex_jac(a, b):
    A, B = tok_set(a), tok_set(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0
lex_correct = 0
for r in app_all:
    scores = [lex_jac(r["text"], intent) for intent in fix_intents]
    idx = int(np.argmax(scores))
    if fix_ids[idx] == r["target"]:
        lex_correct += 1
out["M-MECH-ACC-LEXTOK"] = {"value": lex_correct / len(app_all), "numerator": lex_correct, "denominator": len(app_all)}

# ---------------------------------------------------------------- NC-SHUFFLED-LABEL
SEED = 38180711589 % (2 ** 32)  # 3820973221
rng2 = np.random.RandomState(SEED)
targets = [r["target"] for r in app_all]
n = len(targets)
perm = list(range(n))
for _ in range(100000):
    perm = list(rng2.permutation(n))
    if all(perm[i] != i for i in range(n)):
        break
shuffled = [targets[perm[i]] for i in range(n)]
nc_shuf_correct = sum(1 for r, t in zip(app_all, shuffled) if r["mech"] == t)
out["M-NC-SHUFFLED"] = {"value": nc_shuf_correct / n, "numerator": nc_shuf_correct, "denominator": n,
                        "derangement": "rejection-sampled fixed derangement of the applicable target list",
                        "seed": SEED, "is_derangement": all(perm[i] != i for i in range(n))}

# ---------------------------------------------------------------- NC-CONSTANT-SIGNAL through the SAME calibrate-then-evaluate pipeline
_saved_S = rf.S
rf.S = lambda r: 0
try:
    tstar_c, cal_class_c = rf.calibrate(cal)   # (t*, class) -- do NOT transpose
    const_cal = rf.metrics(cal, tstar_c)
    const_test = rf.metrics(test, tstar_c)
finally:
    rf.S = _saved_S
out["M-NC-CONSTANT-SIGNAL"] = {
    "t_star": tstar_c, "cal_class": cal_class_c,
    "cal_metrics": const_cal, "test_metrics": const_test,
    "unknown_precision_defined": const_test["unknown_precision"] is not None,
    "unknown_precision": const_test["unknown_precision"],
    "at_prevalence_note": "signal-driven abstention precision under a constant signal; prevalence of oos among resolved goals",
    "prevalence_oos_resolved_test": (sum(1 for r in test if not r["app"] and r["mech"] is not None) /
                                     max(1, sum(1 for r in test if r["mech"] is not None))),
}

# ---------------------------------------------------------------- V7 treatment liveness + non-tautology
exec_app_all = sum(1 for r in app_all if r["mech"] is not None and rf.S(r) <= tstar)
out["M-GATE-TREATMENT-VECTOR"] = {
    "t_star": tstar,
    "executed_applicable": exec_app_all,
    "executed_total": sum(1 for r in bound if r["mech"] is not None and rf.S(r) <= tstar),
    "abstained_resolved": sum(1 for r in bound if r["mech"] is not None and rf.S(r) > tstar),
    "unresolved_applicable": sum(1 for r in bound if r["app"] and r["mech"] is None),
    "n_primary_applicable": len(app_all),
}
disagree = sum(1 for r in bound if (r["mech"] is not None) != (r["mech"] is not None and rf.S(r) <= tstar))
out["M-NON-TAUTOLOGY"] = {
    "b_lex_only_vs_t_lex_ambig_disagreement_count": disagree,
    "primary_path_embedder_tokens": None,  # filled below by static inspection
}

# static inspection of the frozen runner: embedder tokens must not occur in the primary decision path
runner_src = (EXP / "runner_frozen.py").read_text(encoding="utf-8")
lines = runner_src.splitlines()
retention_idx = next(i for i, l in enumerate(lines) if "from sentence_transformers import" in l)
primary_prefix = "\n".join(lines[:retention_idx])
tokens_present = [t for t in ("sentence_transformers", "torch", "EmbeddingArgmaxResolver") if t in primary_prefix]
out["M-NON-TAUTOLOGY"]["primary_path_embedder_tokens"] = tokens_present
out["M-NON-TAUTOLOGY"]["retention_block_first_embedder_line"] = retention_idx + 1

# ---------------------------------------------------------------- gates V5-V13 (D-PRIMARY invalidating)
gates = {}
gates["V2-PRIMARY-SET"] = len(app_all) >= 80
gates["V3-CONTAM-SCREEN"] = len(flagged) <= 20
gates["V5-PC"] = out["M-PC-LIVENESS-AND-INTEGRITY"]["pass"]
gates["V6-ORACLE-CEILING"] = abs(out["M-MECH-ACC-ORACLE"]["value"] - 1.0) < 1e-12
gates["V7-TREATMENT-LIVENESS"] = 0 < exec_app_all < len(app_all)
gates["V8-FLOOR-SANITY"] = out["M-MECH-ACC-RANDOM"]["value"] <= 0.35
gates["V9-NON-TAUTOLOGY"] = (len(tokens_present) == 0) and (disagree >= 1)
gates["V10-NC"] = (out["M-NC-SHUFFLED"]["value"] <= 0.20) and (not (out["M-NC-CONSTANT-SIGNAL"]["unknown_precision_defined"]
                                                                     and out["M-NC-CONSTANT-SIGNAL"]["unknown_precision"] >= 0.85))
gates["V13-GATE-VALIDITY"] = cal_class != "GATE-INVALID"
out["gates"] = {k: bool(v) for k, v in gates.items()}

# ---------------------------------------------------------------- secondary axes (deterministic side) and runner controls from RAW evidence
raw = json.loads((EXP / "raw_evidence" / "runner_result_raw.json").read_text(encoding="utf-8"))
out["M-RAW-RUNNER-OUTCOME"] = raw["outcome"]
out["M-RAW-EMBEDDING-STATUS"] = raw["embedding_status"]
for nm in ("AXIS-ALTLEX", "AXIS-HELDOUT"):
    a = raw["axes"][nm]
    out[f"M-GATE-TRIPLET-{nm.split('-')[1]}"] = {
        "t_star": a["tstar"], "class": a["cal_class"],
        "coverage": a["test_metrics"]["coverage"],
        "pooled_false_accept": a["test_metrics"]["pooled_false_accept"],
        "unknown_precision": a["test_metrics"]["unknown_precision"],
        "unknown_precision_inclusive": a["test_metrics"]["unknown_precision_inclusive"],
    }
    out[f"M-DET-ACC-{nm.split('-')[1]}"] = {"cal": a["det_acc_cal"], "test": a["det_acc_test"]}
out["M-EMB-ACC-ALTLEX"] = None
out["M-EMB-ACC-HELDOUT"] = None
out["M-PAIRED-DIFF-DET-MINUS-EMB-ALTLEX"] = None
out["M-PAIRED-DIFF-DET-MINUS-EMB-HELDOUT"] = None
# B-LEX-ONLY (gate-free) == CTRL-EXEC-ALL decision vector on primary test
out["M-B-LEX-ONLY"] = dict(raw["controls"]["CTRL-EXEC-ALL"], note="gate-free resolver; equals CTRL-EXEC-ALL (t=maxS+1)")
out["M-CONTROL-EXEC-ALL"] = raw["controls"]["CTRL-EXEC-ALL"]
out["M-CONTROL-ABSTAIN-ALL"] = raw["controls"]["CTRL-ABSTAIN-ALL"]
out["M-CONTROL-RANDOM-GATE"] = raw["controls"]["CTRL-RANDOM-GATE"]
# primary gate triplet at t* (frozen runner)
out["M-GATE-TRIPLET-PRIMARY"] = dict(raw["primary"]["test_metrics"], t_star=raw["primary"]["tstar"],
                                     cal_class=raw["primary"]["cal_class"],
                                     cal_metrics=raw["primary"]["cal_metrics"])

# ---------------------------------------------------------------- write derived
(EXP / "derived").mkdir(parents=True, exist_ok=True)
(EXP / "derived" / "controls.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
print(json.dumps(out, indent=2, default=str))
