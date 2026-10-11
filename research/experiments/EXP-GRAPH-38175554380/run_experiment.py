#!/usr/bin/env python3
"""Frozen orchestration script for EXP-GRAPH-38175554380 (graph lane).

Binding-only measurement: embeddings vs a strong deterministic operation-synonym +
resource-noun resolver on an independently authored unseen-goal bank, plus a
disjoint-calibrated two-feature applicability gate. No browser, no server, no LLM.
"""
from __future__ import annotations
import json
import hashlib
import re
import sys
import os
from pathlib import Path

# ---------------------------------------------------------------- environment
EXP = Path(os.environ.get("SPIDER_EXP_DIR", Path(__file__).resolve().parent))
REPO = EXP.parents[2]
HARNESS = REPO / "research" / "harness"
SRC = REPO / "src"
OUT = EXP / "derived"

SEED32 = 38175554380 % (2 ** 32)          # = 3815816012
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REV = "c9745ed1d9f207416be6d2e6f8de32d1f161f9bf"
PRIMARY_MIN = 80
CONTAM_TOK_T = 0.60
CONTAM_TRI_T = 0.75
CONTAM_MAX_FLAGGED = 20
FLOOR_MAX = 0.35
NC_LABEL_MAX = 0.20
NC_RANDOM_MAX = 0.25
AB_FA_MAX = 0.10
AB_COV_MIN = 0.50
AB_PREC_MIN = 0.85

out = {
    "schema_version": 1,
    "experiment_id": "EXP-GRAPH-38175554380",
    "lane": "graph",
    "status": None,
    "outcome": None,
    "metrics": {},
    "controls": {},
    "artifacts": [],
    "observations": [],
    "validity_notes": [],
    "unresolved": [],
    "gates": {},
    "env": {},
}

def _abort(status, reason):
    out["status"] = status
    out["outcome"] = "INCONCLUSIVE"
    out["reason"] = reason
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "measurements.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"status": status, "reason": reason}, indent=2))
    sys.exit(0)

# ---------------------------------------------------------------- prerag blocks
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        _abort("MEASUREMENT_INVALID", f"prereg block {name} not found")
    return m.group(1)

CANON = json.loads(_extract((EXP / "prereg.md").read_text(encoding="utf-8"), "CANONICAL-HASHES"))

# ---------------------------------------------------------------- freeze binding
def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---------------------------------------------------------------- pure-string resolver
OP_SYNONYMS = json.loads(_extract((EXP / "prereg.md").read_text(encoding="utf-8"), "LEXICON"))["op_synonyms"]
FAMILY_NOUNS = json.loads(_extract((EXP / "prereg.md").read_text(encoding="utf-8"), "LEXICON"))["family_nouns"]

def tokens(s):
    return re.findall(r"[a-z]+", s.lower())

def _spans(t, phrase, plural=False):
    pt = phrase.split()
    L = len(pt)
    res = []
    for i in range(len(t) - L + 1):
        ok = True
        for k, p in enumerate(pt):
            x = t[i + k]
            if x == p:
                continue
            if plural and (x == p + "s" or x + "s" == p):
                continue
            ok = False
            break
        if ok:
            res.append((i, i + L, L))
    return res

def _unique_longest(cands):
    if not cands:
        return None, None, None
    m = max(c[3] for c in cands)
    top = [c for c in cands if c[3] == m]
    if len({c[0] for c in top}) != 1:
        return None, None, m
    top.sort(key=lambda c: (c[1], c[2]))
    return top[0][0], top[0][1], top[0][2]

def _fam_cands(t):
    return [(f, s, e, L) for f, ph in FAMILY_NOUNS.items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]

def _op_cands(t):
    return [(o, s, e, L) for o, ph in OP_SYNONYMS.items() for p in ph for (s, e, L) in _spans(t, p)]

def b_lex_strong(text):
    """Return mechanism id string, or None to abstain. Pure string computation."""
    t = tokens(text)
    fam, fs, fe = _unique_longest(_fam_cands(t))
    r1 = None
    if fam is not None:
        op, _, _ = _unique_longest(_op_cands(t[:fs] + t[fe:]))
        if op is not None:
            r1 = (fam, op)
    op2, os_, oe = _unique_longest(_op_cands(t))
    r2 = None
    if op2 is not None:
        fam2, _, _ = _unique_longest(_fam_cands(t[:os_] + t[oe:]))
        if fam2 is not None:
            r2 = (fam2, op2)
    if r1 and r2:
        res = r1 if r1 == r2 else None
    else:
        res = r1 or r2
    return None if res is None else f"mech_{res[0]}_{res[1].lower()}"

# ---------------------------------------------------------------- contamination
def _jtok(a, b):
    A, B = set(tokens(a)), set(tokens(b))
    return len(A & B) / len(A | B) if (A | B) else 0.0

def _tri(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i + 3] for i in range(len(x) - 2)}

def _jtri(a, b):
    A, B = _tri(a), _tri(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0

def _select_index(scores):
    import numpy as np
    return int(np.argmax(scores))

def _credit(idx, goal, mech_ids):
    return idx < len(mech_ids) and mech_ids[idx] == goal["target_mechanism_id"]

# ================================================================ MAIN
def main():
    start_cwd = os.getcwd()
    sys.path.insert(0, str(HARNESS))
    sys.path.insert(0, str(SRC))
    try:
        from candidate_resolver import (  # noqa: F401
            EmbeddingArgmaxResolver, InternalIdOracle, LexicalOverlapResolver,
            RandomRoleResolver, create_fixture,
        )
        from experiment_runner import compute_ece, paired_bootstrap, convert_to_native  # noqa: F401
        from goal_generator import (  # noqa: F401
            INTENTS, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES, PARAPHRASES,
        )
        from spider.kernel import SpiderKernel
        from spider.models import Mechanism as KernelMechanism
        from spider.registry import MechanismRegistry
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"harness import failed: {e!r}")
    os.chdir(start_cwd)

    # ---- frozen inputs: bind prereg bytes to freeze, then blocks to CANON ----
    prereg = (EXP / "prereg.md").read_text(encoding="utf-8")
    try:
        freeze_obj = json.loads((EXP / "freeze.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"freeze.json unavailable: {e!r}")
    # V12-A: the whole prereg.md (orchestration script + data blocks) is bound by freeze.hashes
    if freeze_obj.get("hashes", {}).get("prereg.md") != hashlib.sha256(prereg.encode()).hexdigest():
        _abort("MEASUREMENT_INVALID", "V12 prereg.md hash does not match freeze.json")
    spec = json.loads((EXP / "spec.json").read_text(encoding="utf-8"))
    freeze_art = freeze_obj.get("artifact_hashes", {})
    mismatches = [rel for rel in spec["freeze_artifacts"]
                  if freeze_art.get(rel) != sha256_file(REPO / rel)]
    if mismatches:
        _abort("MEASUREMENT_INVALID", f"V12 freeze artifact hash mismatch: {mismatches}")
    out["gates"]["V12-FREEZE-BINDING"] = True

    goal_block = _extract(prereg, "GOAL BANK")
    oos_block = _extract(prereg, "OOS BANK")
    lex_block = _extract(prereg, "LEXICON")
    ppb_block = _extract(prereg, "PRIOR-PARENT-BANK-TEXTS")
    prompts_block = _extract(prereg, "AUTHOR-PROMPTS")
    blocks = {"GOAL BANK": goal_block, "OOS BANK": oos_block, "LEXICON": lex_block,
              "PRIOR-PARENT-BANK-TEXTS": ppb_block, "AUTHOR-PROMPTS": prompts_block}
    for name, blk in blocks.items():
        if hashlib.sha256(blk.encode()).hexdigest() != CANON["blocks"][name]:
            _abort("MEASUREMENT_INVALID", f"V4 block hash mismatch: {name}")
    # V12-B: the running source must equal the frozen FROZEN RUNNER block of the hash-bound prereg
    _block_runner = _extract(prereg, "FROZEN RUNNER")
    _me = Path(__file__).read_text(encoding="utf-8")
    if _me.replace("\r\n", "\n").rstrip("\n") != _block_runner.replace("\r\n", "\n").rstrip("\n"):
        _abort("MEASUREMENT_INVALID", "V12 runner source does not match the frozen FROZEN RUNNER block")

    # ---- embedding + numeric stack (load failure => BLOCKED, never FALSIFIES) ----
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"sentence_transformers import failed: {e!r}")
    try:
        import numpy as np
        from sklearn.linear_model import LogisticRegression
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"numpy/sklearn import failed: {e!r}")
    try:
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
    try:
        _cfg = getattr(getattr(model[0], "auto_model", None), "config", None)
        _resolved_commit = getattr(_cfg, "_commit_hash", None)
    except Exception:  # noqa: BLE001
        _resolved_commit = None
    out["env"]["model_revision_requested"] = MODEL_REV
    out["env"]["model_revision_resolved"] = _resolved_commit
    out["env"]["seed"] = SEED32
    # V4 TRANSCRIPT-BLIND: prompts contain no exact intent string and are far from all prior surfaces
    from goal_generator import INTENTS as _I, PARAPHRASES as _P, NO_APPLICABLE_TEMPLATES as _N, OOD_PARAPHRASES as _O
    _intents = list(_I.values())
    _prior = (list(_I.values()) + [v for vs in _P.values() for v in vs] + list(_N) + list(_O))
    for _line in prompts_block.splitlines():
        for _s in _intents:
            if _s and _s in _line.lower():
                _abort("MEASUREMENT_INVALID", f"V4 prompt leaks intent string: {_s!r}")
    if max(_jtok(prompts_block, q) for q in _prior) >= CONTAM_TOK_T:
        _abort("MEASUREMENT_INVALID", "V4 prompt block too close to a prior surface")
    out["gates"]["V4-AUTHORSHIP-PROVENANCE"] = True

    app_raw = [json.loads(l) for l in goal_block.splitlines() if l.strip()]
    oos_raw = [json.loads(l) for l in oos_block.splitlines() if l.strip()]
    if len(app_raw) != 120 or len(oos_raw) != 40:
        _abort("MEASUREMENT_INVALID", f"bank size wrong: app={len(app_raw)} oos={len(oos_raw)}")
    _intent_lc = {v.lower() for v in _intents}
    for _g in app_raw + oos_raw:
        # V4: raw bank output may not be (or contain) an exact registry intent string
        if _g["text"].strip().lower() in _intent_lc:
            _abort("MEASUREMENT_INVALID", f"V4 raw bank leaks exact intent: {_g['text']!r}")

    goals = []
    for i, g in enumerate(app_raw):
        goals.append({
            "goal_id": f"app_{i+1:03d}", "text": g["text"],
            "target_mechanism_id": f"mech_{g['family']}_{g['op'].lower()}",
            "applicable": True, "family": g["family"], "verb": g["op"],
            "split": "test" if (i % 6) in (1, 3, 5) else "calibration",
        })
    for i, g in enumerate(oos_raw):
        goals.append({
            "goal_id": f"oos_{i+1:03d}", "text": g["text"], "target_mechanism_id": "",
            "applicable": False, "family": g.get("family", ""), "verb": "",
            "split": "test" if (i % 6) in (1, 3, 5) else "calibration",
        })

    mechs = create_fixture()
    mech_ids = [mm.mechanism_id for mm in mechs]
    intents = [mm.intent for mm in mechs]
    if len(mechs) != 20:
        _abort("MEASUREMENT_INVALID", f"V1 fixture has {len(mechs)} mechanisms, expected 20")

    # V3 screen (token OR trigram)
    prior = (list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs]
             + list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES))
    prior_parent = json.loads(ppb_block)
    prior += prior_parent
    contamination = {}
    flagged = set()
    for g in goals:
        mt = max(_jtok(g["text"], q) for q in prior)
        mtri = max(_jtri(g["text"], q) for q in prior)
        contamination[g["goal_id"]] = {"max_token_jaccard": round(mt, 4),
                                       "max_trigram_jaccard": round(mtri, 4)}
        if mt >= CONTAM_TOK_T or mtri >= CONTAM_TRI_T:
            flagged.add(g["goal_id"])
    n_flagged = len(flagged)
    out["metrics"]["M-N-CONTAM-FLAGGED"] = n_flagged
    out["metrics"]["M-CONTAM-FLAGGED-IDS"] = sorted(flagged)
    out["metrics"]["M-CONTAM-MAX-JACCARD"] = {
        "max_token_jaccard": round(max(v["max_token_jaccard"] for v in contamination.values()), 4),
        "max_trigram_jaccard": round(max(v["max_trigram_jaccard"] for v in contamination.values()), 4),
        "thresholds": {"token": CONTAM_TOK_T, "trigram": CONTAM_TRI_T},
    }
    out["gates"]["V3-CONTAM-SCREEN"] = n_flagged <= CONTAM_MAX_FLAGGED

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
    out["gates"]["V2-PRIMARY-SET"] = len(primary) >= PRIMARY_MIN
    if not primary:
        _abort("MEASUREMENT_INVALID", "V2 empty primary set")

    # arms
    embed = EmbeddingArgmaxResolver(mechs, model)
    lexical = LexicalOverlapResolver(mechs)
    random_role = RandomRoleResolver(mechs, seed=4242)
    oracle = InternalIdOracle(mechs)

    kernel_reg_path = OUT / "kernel_registry.jsonl"
    kernel_reg = MechanismRegistry(kernel_reg_path)
    kernel_reg.replace([
        KernelMechanism(mechanism_id=mm.mechanism_id, intent=mm.intent, preconditions={},
                        action_template={}, postconditions={},
                        parameter_slots=list(mm.parameter_slots), confidence=1.0)
        for mm in mechs
    ])
    kernel = SpiderKernel(kernel_reg, min_confidence=0.8)

    # B-LEX-STRONG-LEARNED: op/family lexeme map from calibration applicable labels only
    tok_op = {}
    tok_fam = {}
    for g in cal_app:
        op = g["verb"]; fam = g["family"]
        for w in set(tokens(g["text"])):
            tok_op.setdefault(w, {})
            tok_op[w][op] = tok_op[w].get(op, 0) + 1
            tok_fam.setdefault(w, {})
            tok_fam[w][fam] = tok_fam[w].get(fam, 0) + 1

    def b_lex_learned(text):
        t = tokens(text)
        op = None
        for w in t:
            for k, n in tok_op.get(w, {}).items():
                if n >= 2 and (op is None or n > op[1]):
                    op = (k, n)
        fam = None
        for w in t:
            for k, n in tok_fam.get(w, {}).items():
                if n >= 2 and (fam is None or n > fam[1]):
                    fam = (k, n)
        if op and fam:
            return f"mech_{fam[0]}_{op[0].lower()}"
        return None

    predictions = {}
    for g in goals:
        gid = g["goal_id"]
        er = embed.resolve(g)
        lr = lexical.resolve(g)
        rr = random_role.resolve(g)
        oo = oracle.resolve(g)
        strong = b_lex_strong(g["text"])
        learned = b_lex_learned(g["text"])
        # embedding features: top1 and margin
        ge = model.encode([g["text"]], convert_to_numpy=True, normalize_embeddings=True)[0]
        sims = np.dot(embed.mechanism_embeddings, ge)
        order = np.argsort(sims)[::-1]
        c1 = float(sims[order[0]]); c2 = float(sims[order[1]]) if len(order) > 1 else 0.0
        predictions[gid] = {
            "goal_id": gid, "text": g["text"], "applicable": g["applicable"],
            "target_mechanism_id": g["target_mechanism_id"], "family": g.get("family"),
            "split": g["split"],
            "embed_mechanism_id": er.mechanism_id, "embed_confidence": float(er.confidence),
            "lexical_mechanism_id": lr.mechanism_id, "random_mechanism_id": rr.mechanism_id,
            "oracle_mechanism_id": oo.mechanism_id,
            "stronglex_mechanism_id": strong if strong is not None else "",
            "learned_mechanism_id": learned if learned is not None else "",
            "max_cos": c1, "margin": c1 - c2,
        }

    def acc_of(preds, key, gs):
        c = sum(1 for g in gs if preds[g["goal_id"]][key] == g["target_mechanism_id"])
        return c, len(gs)

    embed_c, embed_d = acc_of(predictions, "embed_mechanism_id", primary)
    strong_c, strong_d = acc_of(predictions, "stronglex_mechanism_id", primary)
    learned_c, learned_d = acc_of(predictions, "learned_mechanism_id", primary)
    lex_c, lex_d = acc_of(predictions, "lexical_mechanism_id", primary)
    rand_c, rand_d = acc_of(predictions, "random_mechanism_id", primary)
    orac_c, orac_d = acc_of(predictions, "oracle_mechanism_id", primary)
    inc_c = 0
    for g in primary:
        res = kernel.resolve(g["text"], {})
        if res.status.value == "EXECUTABLE" and res.mechanism_id == g["target_mechanism_id"]:
            inc_c += 1
    inc_d = len(primary)
    strong_abst = sum(1 for g in primary if predictions[g["goal_id"]]["stronglex_mechanism_id"] == "")
    strong_oos_fa = sum(1 for g in goals if (not g["applicable"]) and g["goal_id"] not in flagged
                        and predictions[g["goal_id"]]["stronglex_mechanism_id"] != "")

    out["metrics"]["M-MECH-ACC-EMBED"] = {"value": embed_c / embed_d, "numerator": embed_c, "denominator": embed_d}
    out["metrics"]["M-MECH-ACC-STRONGLEX"] = {"value": strong_c / strong_d, "numerator": strong_c,
                                              "denominator": strong_d, "abstentions": strong_abst,
                                              "oos_false_accepts_unflagged": strong_oos_fa}
    out["metrics"]["M-MECH-ACC-LEARNED"] = {"value": learned_c / learned_d, "numerator": learned_c, "denominator": learned_d}
    out["metrics"]["M-MECH-ACC-LEXTOK"] = {"value": lex_c / lex_d, "numerator": lex_c, "denominator": lex_d}
    out["metrics"]["M-MECH-ACC-RANDOM"] = {"value": rand_c / rand_d, "numerator": rand_c, "denominator": rand_d}
    out["metrics"]["M-MECH-ACC-ORACLE"] = {"value": orac_c / orac_d, "numerator": orac_c, "denominator": orac_d}
    out["metrics"]["M-MECH-ACC-INCUMBENT"] = {"value": inc_c / inc_d, "numerator": inc_c, "denominator": inc_d}

    v1 = (len(primary) > 0 and embed_d == strong_d == learned_d == lex_d == rand_d == orac_d == inc_d == len(primary))
    out["gates"]["V1-METRIC-DEFINITION"] = v1

    # primary bootstrap (V11)
    np.random.seed(SEED32)
    fams = np.array([g["family"] for g in primary])
    embed_scores = np.array([1.0 if predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    strong_scores = np.array([1.0 if predictions[g["goal_id"]]["stronglex_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    learned_scores = np.array([1.0 if predictions[g["goal_id"]]["learned_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    obs_diff, lower_ci, upper_ci = paired_bootstrap(embed_scores, strong_scores, fams, n_resamples=10000, alpha=0.05)
    n_fams = int(len(np.unique(fams)))
    out["metrics"]["M-PAIRED-DIFF-EMBED-MINUS-STRONGLEX"] = {
        "obs_diff": float(obs_diff), "lower_ci": float(lower_ci), "upper_ci": float(upper_ci)}
    np.random.seed(SEED32)
    ldiff, llow, lup = paired_bootstrap(embed_scores, learned_scores, fams, n_resamples=10000, alpha=0.05)
    out["metrics"]["M-PAIRED-DIFF-EMBED-MINUS-LEARNED"] = {
        "obs_diff": float(ldiff), "lower_ci": float(llow), "upper_ci": float(lup)}
    out["metrics"]["M-BOOTSTRAP-ARGS"] = {"n_resamples": 10000, "alpha": 0.05, "seed": SEED32, "n_families": n_fams}
    out["gates"]["V11-BOOTSTRAP-SEED"] = n_fams == 5

    # V9 structural non-tautology: the STRONG comparator path references no embedder
    runner_src = Path(__file__).read_text(encoding="utf-8")
    strong_src = runner_src.split("def b_lex_strong")[1].split("def _jtok")[0]
    v9 = ("sentence_transformers" not in strong_src) and ("model" not in strong_src) and ("embed" not in strong_src)
    disagree = sum(1 for g in primary if predictions[g["goal_id"]]["embed_mechanism_id"] != predictions[g["goal_id"]]["stronglex_mechanism_id"])
    v9 = v9 and (disagree >= 1 or strong_abst >= 1)
    out["gates"]["V9-NON-TAUTOLOGY"] = v9
    out["metrics"]["M-NON-TAUTOLOGY"] = {"disagreement_count": disagree, "stronglex_accuracy": strong_c / strong_d}

    # V7 treatment liveness
    embed_selected = [predictions[g["goal_id"]]["embed_mechanism_id"] for g in primary]
    v7 = len(set(embed_selected)) >= 2 and all(s in mech_ids for s in embed_selected)
    out["gates"]["V7-TREATMENT-LIVENESS"] = v7
    out["metrics"]["M-EMBED-DISTINCT-SELECTIONS"] = len(set(embed_selected))

    # V5 PC
    pc_fx = (len(set(mech_ids)) == 20) and (len(set(intents)) == 20)
    pc_inc = 0
    for mm in mechs:
        params = {slot: f"v_{slot}" for slot in mm.parameter_slots}
        res = kernel.resolve(mm.intent, {}, params)
        if res.status.value == "EXECUTABLE" and res.mechanism_id == mm.mechanism_id:
            pc_inc += 1
    pc_emb = 0
    for k, mm in enumerate(mechs):
        g = {"goal_id": f"self_{k}", "text": mm.intent, "target_mechanism_id": mm.mechanism_id, "applicable": True}
        if embed.resolve(g).mechanism_id == mm.mechanism_id:
            pc_emb += 1
    v5 = pc_fx and pc_inc == 20 and pc_emb == 20
    out["gates"]["V5-PC"] = v5
    out["metrics"]["M-PC-LIVENESS-AND-INTEGRITY"] = {"fixture_unique": pc_fx, "incumbent_verbatim": pc_inc, "embed_self": pc_emb}
    out["controls"]["PC-LIVENESS-AND-INTEGRITY"] = {
        "expected": "fixture 20/20 unique; incumbent verbatim 20/20; embed_self 20/20",
        "observed": f"fixture_unique={pc_fx}, incumbent_verbatim={pc_inc}/20, embed_self={pc_emb}/20",
        "pass": v5, "evidence_ref": "derived/predictions.json"}

    # V6, V8
    out["gates"]["V6-ORACLE-CEILING"] = (orac_c / orac_d) == 1.0
    out["gates"]["V8-FLOOR-SANITY"] = (rand_c / rand_d) <= FLOOR_MAX

    # V10 NC
    rng_shuf = np.random.RandomState(SEED32 + 100)
    while True:
        perm = rng_shuf.permutation(20)
        if all(perm[i] != i for i in range(20)):
            break
    nc_label_c = 0
    for g in primary:
        ti = mech_ids.index(g["target_mechanism_id"])
        shifted = int(perm[ti])
        sel = predictions[g["goal_id"]]["embed_mechanism_id"]
        if sel in mech_ids and mech_ids.index(sel) == shifted:
            nc_label_c += 1
    nc_label = nc_label_c / len(primary)
    rng_rand = np.random.RandomState(SEED32 + 101)
    nc_rand_c = 0
    for g in primary:
        scores = rng_rand.uniform(size=20)
        if _credit(_select_index(scores), g, mech_ids):
            nc_rand_c += 1
    nc_rand = nc_rand_c / len(primary)
    out["gates"]["V10-NC-SHUFFLE"] = (nc_label <= NC_LABEL_MAX and nc_rand <= NC_RANDOM_MAX)
    out["metrics"]["M-NC-SHUFFLED"] = {"nc_shuffled_label": round(nc_label, 4), "nc_random_score": round(nc_rand, 4)}
    out["controls"]["NC-SHUFFLED-LABEL"] = {"expected": f"<= {NC_LABEL_MAX}", "observed": f"{nc_label:.4f}", "pass": nc_label <= NC_LABEL_MAX, "evidence_ref": "derived/predictions.json"}
    out["controls"]["NC-RANDOM-SCORE"] = {"expected": f"<= {NC_RANDOM_MAX}", "observed": f"{nc_rand:.4f}", "pass": nc_rand <= NC_RANDOM_MAX, "evidence_ref": "derived/predictions.json"}

    # ---------------- D-GATE ----------------
    def gate_eval(feats):
        X = np.array([feats[g["goal_id"]] for g in cal])
        y = np.array([1 if g["applicable"] else 0 for g in cal])
        if len(set(y.tolist())) < 2:
            return None
        clf = LogisticRegression(random_state=42, max_iter=1000)
        clf.fit(X, y)

        def score(g):
            return float(clf.predict_proba(np.array([feats[g["goal_id"]]]))[0][1])

        cal_scores = {g["goal_id"]: score(g) for g in cal}
        test_scores = {g["goal_id"]: score(g) for g in test}
        cal_oos_ids = [g["goal_id"] for g in cal_oos]
        cal_all_ids = [g["goal_id"] for g in cal]

        def metrics_at(t):
            exec_oos = sum(1 for gidv in cal_oos_ids if cal_scores[gidv] >= t)
            abst = [gidv for gidv in cal_all_ids if cal_scores[gidv] < t]
            abst_oos = sum(1 for gidv in cal_oos_ids if cal_scores[gidv] < t)
            fa = exec_oos / len(cal_oos_ids) if cal_oos_ids else None
            prec = abst_oos / len(abst) if abst else None
            return fa, prec

        thresholds = sorted(set(cal_scores.values()))
        feasible = [t for t in thresholds
                    if (lambda m: m[0] is not None and m[0] <= AB_FA_MAX and m[1] is not None
                        and m[1] >= AB_PREC_MIN)(metrics_at(t))]
        if feasible:
            tstar = feasible[0]
            cal_feasible = True
        else:
            cal_feasible = False
            cand = [t for t in thresholds
                    if metrics_at(t)[0] is not None and metrics_at(t)[1] is not None
                    and metrics_at(t)[1] >= AB_PREC_MIN]
            tstar = min(cand, key=lambda t: abs(metrics_at(t)[0] - AB_FA_MAX)) if cand else 1.0
        exec_oos = sum(1 for g in test_oos if test_scores[g["goal_id"]] >= tstar)
        exec_app = sum(1 for g in test_app if test_scores[g["goal_id"]] >= tstar)
        abst_all = [g for g in test if test_scores[g["goal_id"]] < tstar]
        abst_oos = sum(1 for g in test_oos if test_scores[g["goal_id"]] < tstar)
        abst_app = sum(1 for g in test_app if test_scores[g["goal_id"]] < tstar)
        coverage = exec_app / len(test_app) if test_app else None
        fa = exec_oos / len(test_oos) if test_oos else None
        prec = abst_oos / len(abst_all) if abst_all else None
        sel_correct = sum(1 for g in test_app
                          if test_scores[g["goal_id"]] >= tstar
                          and predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"])
        selective_acc = sel_correct / exec_app if exec_app else None
        met = (fa is not None and fa <= AB_FA_MAX and prec is not None and prec >= AB_PREC_MIN
               and coverage is not None and coverage >= AB_COV_MIN)
        return {"feasible": cal_feasible, "t_star": float(tstar), "test_coverage": coverage,
                "test_selective_accuracy": selective_acc,
                "test_pooled_false_accept": fa, "test_unknown_precision": prec,
                "test_exec_app": exec_app, "test_exec_oos": exec_oos,
                "test_abst_app": abst_app, "test_abst_oos": abst_oos,
                "class": "GATE-MET" if met else "GATE-NOT-MET"}

    feats2 = {gid: [predictions[gid]["max_cos"], predictions[gid]["margin"]] for gid in predictions}
    feats1 = {gid: [predictions[gid]["max_cos"]] for gid in predictions}
    if not cal_app or not cal_oos or not test_app or not test_oos:
        out["metrics"]["M-GATE-LOGISTIC-2F"] = {"class": "GATE-INVALID", "reason": "empty calibration or test class"}
        out["metrics"]["M-GATE-GLOBAL-THRESHOLD"] = {"class": "GATE-INVALID"}
        out["gates"]["V13-GATE-VALIDITY"] = False
    else:
        g2 = gate_eval(feats2)
        g1 = gate_eval(feats1)
        out["metrics"]["M-GATE-LOGISTIC-2F"] = g2
        out["metrics"]["M-GATE-GLOBAL-THRESHOLD"] = g1
        out["gates"]["V13-GATE-VALIDITY"] = g2 is not None
        out["observations"].append("OBS-D-GATE(2F): " + json.dumps(g2))
        out["observations"].append("OBS-D-GATE(global): " + json.dumps(g1))

    # ECE descriptive
    ece_confs = np.array([predictions[g["goal_id"]]["embed_confidence"] for g in primary])
    ece_accs = np.array([1.0 if predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    out["metrics"]["M-ECE-GLOBAL"] = {"value": compute_ece(ece_confs, ece_accs), "note": "descriptive, NOT gated"}

    # overall
    gated = [k for k, v in out["gates"].items() if (v is False and k != "V13-GATE-VALIDITY")]
    if gated:
        out["status"] = "MEASUREMENT_INVALID"; out["outcome"] = "INCONCLUSIVE"
        out["reason"] = "validity gates failed: " + ", ".join(gated)
    else:
        out["status"] = "COMPLETE"
        if upper_ci <= 0:
            out["outcome"] = "FALSIFIES"
        elif lower_ci > 0:
            out["outcome"] = "SUPPORTS"
        else:
            out["outcome"] = "MIXED"

    out["observations"] += [
        f"OBS-CONTAMINATION: {n_flagged}/160 flagged (token>={CONTAM_TOK_T} or trigram>={CONTAM_TRI_T}); ids={sorted(flagged)}",
        f"OBS-PRIMARY-SET: |primary|={len(primary)} (cal {len(cal_app)}app/{len(cal_oos)}oos; test {len(test_app)}app/{len(test_oos)}oos)",
        f"OBS-ACCURACIES: embed={embed_c}/{embed_d}, stronglex={strong_c}/{strong_d} (abstain {strong_abst}), learned={learned_c}/{learned_d}, lextok={lex_c}/{lex_d}, random={rand_c}/{rand_d}, incumbent={inc_c}/{inc_d}, oracle={orac_c}/{orac_d}",
        f"OBS-PAIRED-DIFF-STRONGLEX: obs={obs_diff:.4f} CI=[{lower_ci:.4f},{upper_ci:.4f}] (families={n_fams}, B=10000, seed={SEED32})",
        f"OBS-D-RESOLVER: {out['outcome']}",
    ]
    out["validity_notes"] += [
        "VN-01: binding-only; no HTTP server, no task traffic; one HuggingFace model download (revision recorded).",
        "VN-02: mechanism-identity correctness ignores parameter binding (out of scope).",
        "VN-03: bootstrap covers resampling variability only (family-blocked, 5 blocks); one model.",
        "VN-04: contamination screen uses token-set Jaccard (>=0.60) OR char-trigram Jaccard (>=0.75) against goal_generator surfaces plus the parent 140-goal bank; the trigram representation differs from every arm.",
        "VN-05: ECE descriptive only, not gated.",
        "VN-06: B-LEX-STRONG-LEARNED is a sensitivity bound, not the claim-bearing comparator.",
        "VN-07: residual authorship limitation: the fresh-context authors had no file/tool access and their prompts contained no intent strings, but latent pretrained knowledge cannot be cryptographically excluded (see prereg V4).",
        "VN-08: checkpoint identity: the frozen revision is requested but, as in the parent packet (which could not fetch it and resolved to 1110a243fdf4706b3f48f1d95db1a4f5529b4d41), an unpinned fallback is recorded in env.model_revision/model_revision_resolved; results are interpretable only for the actually-resolved checkpoint (continuity with parent UNRES-04).",
        "VN-09: in derived/predictions.json a resolver that ABSTAINS is stored as the empty string '' (not null) for stronglex_mechanism_id/learned_mechanism_id/lexical_mechanism_id; the abstention count is also recorded explicitly in M-MECH-ACC-STRONGLEX.abstentions. An abstention scores as incorrect in all accuracy metrics.",
    ]
    out["artifacts"] += [
        {"path": "derived/predictions.json", "role": "raw"},
        {"path": "derived/contamination.json", "role": "derived"},
        {"path": "derived/measurements.json", "role": "derived"},
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "predictions.json").write_text(json.dumps(convert_to_native(predictions), indent=2), encoding="utf-8")
    (OUT / "contamination.json").write_text(json.dumps(contamination, indent=2), encoding="utf-8")
    (OUT / "measurements.json").write_text(json.dumps(convert_to_native(out), indent=2), encoding="utf-8")
    print(json.dumps({"status": out["status"], "outcome": out["outcome"],
                      "obs_diff": float(obs_diff), "lower_ci": float(lower_ci), "upper_ci": float(upper_ci),
                      "embed_acc": embed_c / embed_d, "stronglex_acc": strong_c / strong_d,
                      "learned_acc": learned_c / learned_d,
                      "gate2f": out["metrics"].get("M-GATE-LOGISTIC-2F", {}).get("class")}, indent=2))

if __name__ == "__main__":
    main()
