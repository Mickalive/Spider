#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38180711589 (design_contract_version 2).
# Model-free primary; embedding arm optional (secondary retention checks).
# Usage: python runner_frozen.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, re, sys, platform
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38180711589"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
PREREG = EXP_DIR / "prereg.md"
PARENT_PREREG = ROOT / "research/experiments" / "EXP-GRAPH-38175554380" / "prereg.md"
FREEZE_PATH = EXP_DIR / "freeze.json"
RESULT_PATH = EXP_DIR / "result.json"
REPORT_PATH = EXP_DIR / "report.md"
PROV_PATH = EXP_DIR / "provenance.json"

SEED = 38180711589 % (2 ** 32)
N_BOOT = 10000
ALPHA = 0.05
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
TOK_BAND = 0.60
TRI_BAND = 0.75
MAX_FLAGGED = 20

FAMILIES_G1 = ["users", "posts", "comments", "albums", "photos"]
FAMILIES_G2 = ["teams", "projects", "events", "tickets", "files"]
OPS = ["CREATE", "READ", "UPDATE", "DELETE"]
DET = {"a","an","the","this","that","these","those","one","two","my","your","his","her","its","our","their","each","every","any","some","all","no","another","other"}
REF = {"id","identifier","identified","number","numbered","named","called","titled","referred","labelled","labeled"}
QUANT = {"all","every","each","any","some","several","many","both","whole","entire","multiple","batch","bulk"}

# ------------------------------------------------------------------ helpers
def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def canon_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def extract_block(text: str, name: str) -> str:
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise SystemExit(f"missing block {name}")
    return m.group(1)

def jlines(block: str):
    return [json.loads(l) for l in block.splitlines() if l.strip()]

def tokens(s: str):
    return re.findall(r"[a-z]+", s.lower())

def _spans(t, phrase, plural=False):
    pt = phrase.split(); L = len(pt); res = []
    for i in range(len(t) - L + 1):
        ok = True
        for k, p in enumerate(pt):
            x = t[i + k]
            if x == p:
                continue
            if plural and (x == p + "s" or x + "s" == p):
                continue
            ok = False; break
        if ok:
            res.append((i, i + L, L))
    return res

def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0

def trigrams(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i+3] for i in range(len(x) - 2)}

# ------------------------------------------------------------------ resolver
def comp(text: str, lex: dict):
    """B-LEX-STRONG key-set longest resolver with noun-homograph disambiguation.
    Returns dict(mech, famNONE, famTIE, opNONE, opTIE, dis, noslot, quant)."""
    t = tokens(text)
    fam_tokens = {p.split()[0] for ph in lex["family_nouns"].values() for p in ph}
    fsp = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]
    osp = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(t, p)
           if not (t[s] in fam_tokens and s > 0 and t[s - 1] in DET)]
    fmax = max([L for _, _, _, L in fsp], default=0)
    omax = max([L for _, _, _, L in osp], default=0)
    fkm = {f for f, _, _, L in fsp if L == fmax}
    okm = {o for o, _, _, L in osp if L == omax}
    fst = "NONE" if not fsp else ("UNIQUE" if len(fkm) == 1 else "TIE")
    ost = "NONE" if not osp else ("UNIQUE" if len(okm) == 1 else "TIE")
    fam = list(fkm)[0] if fst == "UNIQUE" else None
    op = list(okm)[0] if ost == "UNIQUE" else None
    r1 = None
    if fam:
        s0 = min(s for f, s, _, _ in fsp if f == fam); e0 = max(e for f, _, e, _ in fsp if f == fam)
        rem = t[:s0] + t[e0:]
        ors = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(rem, p)
               if not (rem[s] in fam_tokens and s > 0 and rem[s - 1] in DET)]
        om = max([L for _, _, _, L in ors], default=0); okm2 = {o for o, _, _, L in ors if L == om}
        if len(okm2) == 1:
            r1 = (fam, list(okm2)[0])
    r2 = None
    if op:
        s0 = min(s for o, s, _, _ in osp if o == op); e0 = max(e for o, _, e, _ in osp if o == op)
        rem = t[:s0] + t[e0:]
        frs = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(rem, p, plural=True)]
        fm = max([L for _, _, _, L in frs], default=0); fkm2 = {f for f, _, _, L in frs if L == fm}
        if len(fkm2) == 1:
            r2 = (list(fkm2)[0], op)
    res = (r1 if r1 == r2 else None) if (r1 and r2) else (r1 or r2)
    dis = 1 if (r1 and r2 and r1 != r2) else 0
    hasref = any(w in REF for w in t)
    noslot = 1 if (res is not None and res[1] in ("READ", "UPDATE", "DELETE") and not hasref) else 0
    q = 1 if any(w in QUANT for w in t) else 0
    return dict(mech=None if res is None else f"mech_{res[0]}_{res[1].lower()}",
                famNONE=int(fst == "NONE"), famTIE=int(fst == "TIE"), opNONE=int(ost == "NONE"),
                opTIE=int(ost == "TIE"), dis=dis, noslot=noslot, quant=q)

W = {"famNONE": 1, "opNONE": 1, "opTIE": 1, "noslot": 1, "quant": 1}
def S(r): return sum(w * r[k] for k, w in W.items())

# ------------------------------------------------------------------ fingerprint / gate
def target_of(goal): return f"mech_{goal['family']}_{goal['op'].lower()}"

def build_axis(app, oos, lex, splitmod, prior_texts):
    rows = []
    for i, g in enumerate(app):
        rows.append(dict(gid=f"app_{i+1:03d}", text=g["text"], app=1, target=target_of(g),
                         split=(i % splitmod) in (1, 3, 5)))
    for i, g in enumerate(oos):
        rows.append(dict(gid=f"oos_{i+1:03d}", text=g["text"], app=0, target=None,
                         split=(i % splitmod) in (1, 3, 5)))
    flagged = []
    for r in rows:
        r.update(comp(r["text"], lex))
        if max(jaccard(tokens(r["text"]), tokens(p)) for p in prior_texts) >= TOK_BAND or \
           max(jaccard(trigrams(r["text"]), trigrams(p)) for p in prior_texts) >= TRI_BAND:
            flagged.append(r["gid"])
    bound = [r for r in rows if r["gid"] not in flagged]
    return bound, flagged

def metrics(rows, t):
    ex = [r for r in rows if r["mech"] is not None and S(r) <= t]
    exo = sum(1 for r in ex if not r["app"]); exa = sum(1 for r in ex if r["app"])
    co = sum(1 for r in rows if not r["app"]); ca = sum(1 for r in rows if r["app"])
    abR = [r for r in rows if r["mech"] is not None and S(r) > t]
    abRo = sum(1 for r in abR if not r["app"])
    unres_app = sum(1 for r in rows if r["app"] and r["mech"] is None)
    ab_all = [r for r in rows if not (r["mech"] is not None and S(r) <= t)]
    fa = exo / co if co else None
    cov = exa / ca if ca else None
    precR = abRo / len(abR) if abR else None
    precI = (sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None
    sel_ex = sum(1 for r in ex if r["app"] and r["mech"] == r["target"])
    return dict(t=t, coverage=cov, pooled_false_accept=fa, unknown_precision=precR,
                unknown_precision_inclusive=precI, abstained_resolved=len(abR),
                executed=len(ex), executed_oos=exo, executed_app=exa,
                selective_acc=(sel_ex / exa) if exa else None,
                unresolved_applicable=unres_app)

def calibrate(cal):
    co = [r for r in cal if not r["app"]]; ca = [r for r in cal if r["app"]]
    if not co or not ca:
        return None, "GATE-INVALID"
    cands = sorted({S(r) for r in cal})
    feas = [t for t in cands if (lambda m: m["pooled_false_accept"] is not None and m["pooled_false_accept"] <= FA_TARGET
                                 and m["unknown_precision"] is not None and m["unknown_precision"] >= PREC_TARGET)(metrics(cal, t))]
    if feas:
        return min(feas), "CAL-FEASIBLE"
    # predeclared fallback: min |cal_fa-0.10| subject to cal_precR>=0.85, else abstain-all
    sub = [(abs(metrics(cal, t)["pooled_false_accept"] - FA_TARGET), t) for t in cands
           if metrics(cal, t)["pooled_false_accept"] is not None and metrics(cal, t)["unknown_precision"] is not None
           and metrics(cal, t)["unknown_precision"] >= PREC_TARGET]
    if sub:
        return min(sub)[1], "CAL-FALLBACK"
    return max(cands) + 1, "CAL-ABSTAIN-ALL"

def selection_acc(rows):
    ca = [r for r in rows if r["app"]]
    return (sum(1 for r in ca if r["mech"] == r["target"]) / len(ca)) if ca else None

# ------------------------------------------------------------------ bootstrap
def paired_family_bootstrap(diff_by_family, seed):
    """diff_by_family: {family: [paired diffs]}; percentile CI."""
    try:
        import numpy as np
    except Exception:
        return None
    np.random.seed(seed)
    fams = sorted(diff_by_family)
    boots = []
    for _ in range(N_BOOT):
        vals = []
        for fam in fams:
            arr = diff_by_family[fam]
            idx = np.random.randint(0, len(arr), len(arr))
            vals.extend([arr[i] for i in idx])
        boots.append(float(np.mean(vals)) if vals else float("nan"))
    boots = np.array([b for b in boots if not math.isnan(b)])
    if boots.size == 0:
        return None
    return dict(obs=float(np.mean([v for vs in diff_by_family.values() for v in vs])),
                lower=float(np.percentile(boots, 100 * ALPHA / 2)),
                upper=float(np.percentile(boots, 100 * (1 - ALPHA / 2))),
                n_resamples=int(boots.size), alpha=ALPHA, n_families=len(fams), seed=seed)

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    prereg_text = PREREG.read_text(encoding="utf-8")
    g1_app = jlines(extract_block(prereg_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(prereg_text, "OOS-BANK-G1"))
    lex_g1 = json.loads(extract_block(prereg_text, "LEXICON-G1"))
    g2_app = jlines(extract_block(prereg_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(prereg_text, "OOS-BANK-G2"))
    lex_ho = json.loads(extract_block(prereg_text, "LEXICON-G2-HELDOUT"))
    lex_alt = json.loads(extract_block(prereg_text, "LEXICON-G1-ALT"))
    g2_intents = jlines(extract_block(prereg_text, "G2-HELDOUT-INTENTS"))
    parent_text = PARENT_PREREG.read_text(encoding="utf-8")
    prior_parent = json.loads(extract_block(parent_text, "PRIOR-PARENT-BANK-TEXTS")) if "PRIOR-PARENT-BANK-TEXTS" in parent_text else []

    sys.path.insert(0, str(ROOT / "research/harness"))
    from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES
    gg = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
         list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
    prior_full = gg + list(prior_parent)

    axes = {}
    for nm, (app, oos, lex, sm, priors) in {
        "AXIS-PRIMARY": (g1_app, g1_oos, lex_g1, 6, prior_full),
        "AXIS-ALTLEX": (g1_app, g1_oos, lex_alt, 6, prior_full),
        "AXIS-HELDOUT": (g2_app, g2_oos, lex_ho, 4, gg + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]),
    }.items():
        bound, flagged = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        tstar, cls = calibrate(cal)
        cal_m = metrics(cal, tstar)
        axes[nm] = dict(bound=len(bound), flagged=flagged, cal=cal, test=test, tstar=tstar,
                        cal_class=cls, cal_metrics=cal_m,
                        det_acc_cal=selection_acc(cal), det_acc_test=selection_acc(test))

    # ---- primary decision
    p = axes["AXIS-PRIMARY"]
    test_m = metrics(p["test"], p["tstar"]) if not args.mechanics_only else None
    gate_out = ("GATE-INVALID" if p["cal_class"] == "GATE-INVALID" else
                "GATE-MET" if (test_m is not None and test_m["pooled_false_accept"] is not None and test_m["pooled_false_accept"] <= FA_TARGET
                               and test_m["unknown_precision"] is not None and test_m["unknown_precision"] >= PREC_TARGET
                               and test_m["coverage"] is not None and test_m["coverage"] >= COV_TARGET)
                else "GATE-NOT-MET")
    if args.mechanics_only:
        print(json.dumps(dict(status="DESIGN-MECHANICS-ONLY",
                              axes={k: dict(bound=v["bound"], flagged=v["flagged"], tstar=v["tstar"],
                                            cal_class=v["cal_class"], cal_metrics=v["cal_metrics"])
                                    for k, v in axes.items()}), indent=2))
        return
    # boundary / matched-coverage controls on PRIMARY test
    def boundary(name, t, rows):
        return {name: metrics(rows, t)}
    ctrl = {}
    maxS = max(S(r) for r in p["cal"] + p["test"])
    ctrl.update(boundary("CTRL-EXEC-ALL", maxS + 1, p["test"]))
    ctrl.update(boundary("CTRL-ABSTAIN-ALL", -1, p["test"]))
    # matched-coverage random gate: abstain same count as treatment, randomly, seed fixed
    treated = metrics(p["test"], p["tstar"])
    import random
    rng = random.Random(SEED)
    idx = list(range(len(p["test"]))); rng.shuffle(idx)
    ab_n = sum(1 for r in p["test"] if not (r["mech"] is not None and S(r) <= p["tstar"]))
    abset = set(idx[:ab_n])
    ab_rows = [r for i, r in enumerate(p["test"]) if i in abset]
    ex_rows = [r for i, r in enumerate(p["test"]) if i not in abset]
    ctrl["CTRL-RANDOM-GATE"] = dict(
        pooled_false_accept=(sum(1 for r in ex_rows if not r["app"]) / sum(1 for r in p["test"] if not r["app"])) if any(not r["app"] for r in p["test"]) else None,
        unknown_precision=(sum(1 for r in ab_rows if not r["app"]) / len(ab_rows)) if ab_rows else None,
        matched_abstention_count=ab_n)

    # ---- retention arms (embedding comparator; optional)
    retention = {}
    embedding_status = "NOT_ATTEMPTED"
    try:
        import numpy as np  # noqa
        from sentence_transformers import SentenceTransformer
        from candidate_resolver import EmbeddingArgmaxResolver, create_fixture
        from types import SimpleNamespace
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        g1_mechs = create_fixture()
        g1_embed = EmbeddingArgmaxResolver(g1_mechs, model)
        ho_mechs = [SimpleNamespace(mechanism_id=f"mech_{d['family']}_{d['op'].lower()}", intent=d["intent"]) for d in g2_intents]
        ho_embed = EmbeddingArgmaxResolver(ho_mechs, model)
        for nm, embed in (("AXIS-ALTLEX", g1_embed), ("AXIS-HELDOUT", ho_embed)):
            rows = axes[nm]["test"]
            diffs = {}
            cor = {"det": 0, "emb": 0, "n": 0}
            for r in rows:
                if not r["app"]:
                    continue
                emb = embed.resolve({"text": r["text"], "goal_id": r["gid"]})
                d = 1 if (r["mech"] == r["target"]) else 0
                e = 1 if (emb.mechanism_id == r["target"]) else 0
                cor["det"] += d; cor["emb"] += e; cor["n"] += 1
                fam = r["target"].split("_")[1]
                diffs.setdefault(fam, []).append(d - e)
            boot = paired_family_bootstrap(diffs, SEED)
            retention[nm] = dict(det_correct=cor["det"], emb_correct=cor["emb"], n=cor["n"],
                                 det_acc=cor["det"] / cor["n"] if cor["n"] else None,
                                 emb_acc=cor["emb"] / cor["n"] if cor["n"] else None, paired_diff=boot)
        embedding_status = "OK"
    except Exception as exc:  # noqa
        embedding_status = f"BLOCKED: {type(exc).__name__}: {exc}"

    ret_out = {}
    for nm in ("AXIS-ALTLEX", "AXIS-HELDOUT"):
        r = retention.get(nm)
        if r and r["paired_diff"]:
            ret_out[nm] = "RETAINED" if r["paired_diff"]["lower"] > 0 else ("LOST" if r["paired_diff"]["upper"] <= 0 else "MIXED")
        else:
            ret_out[nm] = "BLOCKED"

    out = dict(schema_version=1, experiment_id=EXP_ID, lane="graph",
               status="DESIGN-MECHANICS-ONLY" if args.mechanics_only else "COMPLETE",
               outcome={"D-PRIMARY": gate_out, "D-HELDOUT": ret_out["AXIS-HELDOUT"], "D-ALTLEX": ret_out["AXIS-ALTLEX"]},
               primary=dict(tstar=p["tstar"], cal_class=p["cal_class"], cal_metrics=p["cal_metrics"], test_metrics=test_m),
               controls=ctrl,
               axes={k: dict(bound=v["bound"], flagged=v["flagged"], tstar=v["tstar"], cal_class=v["cal_class"],
                             cal_metrics=v["cal_metrics"], det_acc_cal=v["det_acc_cal"], det_acc_test=v["det_acc_test"],
                             test_metrics=metrics(v["test"], v["tstar"]))
                     for k, v in axes.items()},
               retention=retention, embedding_status=embedding_status)
    print(json.dumps(out, indent=2))
    if not args.mechanics_only:
        RESULT_PATH.write_text(json.dumps(out, indent=2) + "\n")

if __name__ == "__main__":
    main()
