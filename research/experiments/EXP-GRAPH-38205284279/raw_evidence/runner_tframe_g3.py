#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38205284279 (design_contract_version 2).
# Arm A = T-FRAME+ : shared deterministic lexical selection (B-LEX-STRONG, frozen)
#   + structural frame-completeness abstention clauses C1-SUBOP, C3-NO-REFERENCE,
#   C4-COMPLEMENT, C5-SET-QUANT, C6-SOURCE (frozen) + the NEW pre-declared,
#   zero-tunable-parameter clause C7-CREATE-OBLIQUE (this experiment).
# Arm B = B-RETRIEVAL-TFIDF : stdlib pure-Python TF-IDF nearest-class-centroid
#   retrieval resolver with a calibration-fitted abstention gate (comparator).
# Stdlib only (argparse, hashlib, json, math, re, random, sys, pathlib).
# Usage: python runner_tframe_g3.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, os, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38205284279"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
PARENT = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38205284279 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75

DET = {"a", "an", "the", "this", "that", "these", "those", "one", "two", "my", "your", "his", "her",
       "its", "our", "their", "each", "every", "any", "some", "all", "no", "another", "other"}
REF = {"id", "identifier", "identified", "number", "numbered", "named", "called", "titled", "referred",
       "labelled", "labeled", "code", "badge"}
QUANT = {"all", "every", "each", "any", "some", "several", "many", "both", "whole", "entire",
         "multiple", "batch", "bulk"}
POLITE = {"please", "kindly", "can", "could", "would", "will", "i", "want", "need", "help", "lets", "let"}
SOURCE = {"from", "into", "onto"}
OBLIQUE = {"to", "on", "onto", "into", "in", "at", "from", "by", "upon", "toward", "towards", "with"}
REL = {"whose", "which", "who", "that", "where", "matching", "containing"}
SUBORD = {"to", "that", "which", "who", "so", "then"}
PREP = {"of", "with", "by", "using", "for", "about", "from", "in", "to", "on", "at", "into", "onto",
        "under", "over", "across", "via", "through", "as", "per", "within", "without", "against",
        "between", "among", "upon", "toward", "towards", "near", "around", "behind", "before",
        "after", "during", "inside", "outside"}


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def self_sha() -> str:
    try:
        return sha_file(Path(__file__))
    except Exception:
        return "UNKNOWN"


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
    return {x[i:i + 3] for i in range(len(x) - 2)}


def comp(text: str, lex: dict):
    """Shared deterministic selector (B-LEX-STRONG): longest key-set + homograph guard. FROZEN."""
    t = tokens(text)
    fam_first = {p.split()[0] for ph in lex["family_nouns"].values() for p in ph}
    fsp = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]
    osp = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(t, p)
           if not (t[s] in fam_first and s > 0 and t[s - 1] in DET)]
    fmax = max([L for _, _, _, L in fsp], default=0); omax = max([L for _, _, _, L in osp], default=0)
    fkm = {f for f, _, _, L in fsp if L == fmax}; okm = {o for o, _, _, L in osp if L == omax}
    fst = "NONE" if not fsp else ("UNIQUE" if len(fkm) == 1 else "TIE")
    ost = "NONE" if not osp else ("UNIQUE" if len(okm) == 1 else "TIE")
    fam = list(fkm)[0] if fst == "UNIQUE" else None
    op = list(okm)[0] if ost == "UNIQUE" else None
    r1 = None
    if fam:
        s0 = min(s for f, s, _, _ in fsp if f == fam); e0 = max(e for f, _, e, _ in fsp if f == fam)
        rem = t[:s0] + t[e0:]
        ors = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(rem, p)
               if not (rem[s] in fam_first and s > 0 and rem[s - 1] in DET)]
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
    hasref = any(w in REF for w in t)
    return dict(t=t, fsp=fsp, osp=osp, hasref=hasref,
                mech=None if res is None else f"mech_{res[0]}_{res[1].lower()}",
                fam=None if res is None else res[0], op=None if res is None else res[1],
                famNONE=int(fst == "NONE"), famTIE=int(fst == "TIE"),
                opNONE=int(ost == "NONE"), opTIE=int(ost == "TIE"),
                noslot=1 if (res is not None and res[1] in ("READ", "UPDATE", "DELETE") and not hasref) else 0,
                quant=1 if any(w in QUANT for w in t) else 0)


def frame(r: dict):
    """Frozen structural frame-completeness clauses (FROZEN, fires => ABSTAIN)."""
    t = r["t"]; cl = {}
    h = 0
    while h < len(t) and t[h] in POLITE:
        h += 1
    head = t[h] if h < len(t) else None
    fire = False
    if r["op"]:
        spans = [(s, e) for o, s, e, L in r["osp"] if o == r["op"]]
        if spans:
            osx = min(s for s, _ in spans)
            if head is not None and head != t[osx] and any(i < osx and t[i] in SUBORD for i in range(len(t))):
                fire = True
    cl["C1-SUBOP"] = fire
    cl["C3-NO-REFERENCE"] = bool(r["op"] in ("READ", "UPDATE", "DELETE") and not r["hasref"])
    cl["C4-COMPLEMENT"] = False
    cl["C6-SOURCE"] = False
    if r["fam"]:
        spans = [(s, e) for f, s, e, L in r["fsp"] if f == r["fam"]]
        if spans:
            after = t[max(e for _, e in spans):]
            idx = 0
            while idx < len(after) and after[idx] in DET:
                idx += 1
            if idx < len(after) and after[idx] not in PREP and after[idx] not in REF and after[idx] not in REL:
                cl["C4-COMPLEMENT"] = True
            if r["op"] == "CREATE" and any(w in SOURCE for w in after):
                cl["C6-SOURCE"] = True
    cl["C5-SET-QUANT"] = any(w in QUANT for w in t)
    return cl


def clause_c7(r: dict) -> bool:
    """NEW pre-declared clause C7-CREATE-OBLIQUE. Zero tunable parameters.
    Fires for a bound CREATE operation when either:
      (a) a source/extraction preposition {from, into, onto} occurs anywhere in the instruction
          (the object being created/imported is placed from/onto/into a host resource); or
      (b) a placement preposition {to,on,onto,into,in,at,from,by,upon,toward,towards,with} occurs
          strictly between the end of the matched CREATE verb phrase and the start of the first
          bound-family noun phrase (the resource sits in an oblique argument, so the created
          entity is a non-resource object attached to it).
    Both triggers are structural and threshold-free."""
    if r["op"] != "CREATE":
        return False
    t = r["t"]
    if any(w in SOURCE for w in t):
        return True
    osp = [(s, e) for o, s, e, L in r["osp"] if o == "CREATE"]
    if not osp:
        return False
    osx = min(e for _, e in osp)
    fs = [s for f, s, e, L in r["fsp"] if f == r["fam"] and s >= osx] if r["fam"] else []
    if fs and any(t[i] in OBLIQUE for i in range(osx, min(fs))):
        return True
    return False


def analyze(text: str, lex: dict):
    r = comp(text, lex)
    cl = frame(r)
    cl["C7-CREATE-OBLIQUE"] = clause_c7(r)
    r["clauses"] = cl
    r["S"] = r["famNONE"] + r["opNONE"] + r["opTIE"] + r["noslot"] + r["quant"]
    return r


def is_executed(r: dict, mode: str) -> bool:
    if mode == "gatefree":
        return r["mech"] is not None
    if mode == "incumbent":
        return r["mech"] is not None and r["S"] <= 0
    if mode == "tframe_frozen":  # existing 5 clauses, WITHOUT C7 (diagnostic only)
        return r["mech"] is not None and not any(v for k, v in r["clauses"].items() if k != "C7-CREATE-OBLIQUE")
    return r["mech"] is not None and not any(r["clauses"].values())  # tframeplus (Arm A)


def target_of(goal):
    return f"mech_{goal['family']}_{goal['op'].lower()}"


def build_axis(app, oos, lex, splitmod, prior_texts):
    rows = []
    for i, g in enumerate(app):
        rows.append(dict(gid=f"app_{i+1:03d}", text=g["text"], app=1, target=target_of(g), split=(i % splitmod) in (1, 3, 5)))
    for i, g in enumerate(oos):
        rows.append(dict(gid=f"oos_{i+1:03d}", text=g["text"], app=0, target=None, split=(i % splitmod) in (1, 3, 5)))
    flagged = []
    for r in rows:
        r.update(analyze(r["text"], lex))
        if max(jaccard(tokens(r["text"]), tokens(p)) for p in prior_texts) >= TOK_BAND or \
           max(jaccard(trigrams(r["text"]), trigrams(p)) for p in prior_texts) >= TRI_BAND:
            flagged.append(r["gid"])
    bound = [r for r in rows if r["gid"] not in flagged]
    return bound, flagged


def metrics(rows, mode):
    ex = [r for r in rows if is_executed(r, mode)]
    exo = sum(1 for r in ex if not r["app"]); exa = sum(1 for r in ex if r["app"])
    co = sum(1 for r in rows if not r["app"]); ca = sum(1 for r in rows if r["app"])
    abR = [r for r in rows if r["mech"] is not None and not is_executed(r, mode)]
    abRo = sum(1 for r in abR if not r["app"])
    ab_all = [r for r in rows if not is_executed(r, mode)]
    sel = sum(1 for r in ex if r["app"] and r["mech"] == r["target"])
    return dict(coverage=exa / ca if ca else None, pooled_false_accept=exo / co if co else None,
                unknown_precision=abRo / len(abR) if abR else None,
                unknown_precision_inclusive=(sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None,
                executed=len(ex), executed_oos=exo, executed_app=exa, abstained_resolved=len(abR),
                selective_acc=sel / exa if exa else None,
                unresolved_applicable=sum(1 for r in rows if r["app"] and r["mech"] is None))


def gate_met(m):
    return bool(m["pooled_false_accept"] is not None and m["pooled_false_accept"] <= FA_TARGET
                and m["coverage"] is not None and m["coverage"] >= COV_TARGET
                and m["unknown_precision"] is not None and m["unknown_precision"] >= PREC_TARGET)


# ---------------- Arm B : stdlib TF-IDF nearest-centroid retrieval ----------------
def _feats(text):
    t = tokens(text)
    bg = [t[i] + "_" + t[i + 1] for i in range(len(t) - 1)]
    return t + bg


def _vec(fs, idf):
    v = {}
    for f in fs:
        v[f] = v.get(f, 0.0) + 1.0
    for f in list(v):
        v[f] = (1.0 + math.log(v[f])) * idf.get(f, 0.0)
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {f: x / n for f, x in v.items()}


def _cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(f, 0.0) for f, x in a.items())


def arm_b(cal, test, seed):
    fit = [r for r in cal if r["app"]]
    N = len(fit)
    df = {}
    docs = []
    for r in fit:
        fs = _feats(r["text"])
        docs.append((r["target"], fs))
        for f in set(fs):
            df[f] = df.get(f, 0) + 1
    idf = {f: math.log((1 + N) / (1 + d)) + 1.0 for f, d in df.items()}
    cent = {}
    for cls, fs in docs:
        v = _vec(fs, idf)
        c = cent.setdefault(cls, {})
        for f, x in v.items():
            c[f] = c.get(f, 0.0) + x
    cent = {cls: _vec([], {}) if not v else {f: x / (math.sqrt(sum(y * y for y in v.values())) or 1.0) for f, x in v.items()} for cls, v in cent.items()}

    def score(rows):
        out = []
        for r in rows:
            v = _vec(_feats(r["text"]), idf)
            sims = sorted(((_cos(v, c), cls) for cls, c in cent.items()), reverse=True)
            top = sims[0][0] if sims else 0.0
            margin = (sims[0][0] - sims[1][0]) if len(sims) > 1 else 1.0
            out.append((r, sims[0][1] if sims else None, top, margin))
        return out

    def gate_metrics(scored, tau, mu):
        ex = [(r, cls) for r, cls, s, m in scored if s >= tau and m >= mu]
        ab = [(r, cls, s, m) for r, cls, s, m in scored if not (s >= tau and m >= mu)]
        exo = sum(1 for r, c in ex if not r["app"]); exa = sum(1 for r, c in ex if r["app"])
        co = sum(1 for r in scored if not r[0]["app"]); ca = sum(1 for r in scored if r[0]["app"])
        abRo = sum(1 for r, c, s, m in ab if not r["app"])
        sel = sum(1 for r, c in ex if r["app"] and c == r["target"])
        return dict(coverage=exa / ca if ca else 0.0, pooled_false_accept=exo / co if co else None,
                    unknown_precision=abRo / len(ab) if ab else None, selective_acc=sel / exa if exa else None,
                    executed=len(ex), executed_app=exa, executed_oos=exo, abstained=len(ab))

    cal_scored = score(cal)
    taus = sorted({round(s, 4) for _, _, s, _ in cal_scored})
    mus = sorted({round(m, 4) for _, _, _, m in cal_scored})
    best = None
    for tau in taus:
        for mu in mus:
            gm = gate_metrics(cal_scored, tau, mu)
            feasible = (gm["pooled_false_accept"] is not None and gm["pooled_false_accept"] <= FA_TARGET
                        and gm["coverage"] >= COV_TARGET
                        and gm["unknown_precision"] is not None and gm["unknown_precision"] >= PREC_TARGET)
            key = (1 if feasible else 0, gm["coverage"] if gm["coverage"] else 0.0)
            if best is None or key > best[0]:
                best = (key, (tau, mu), gm)
    if best is None:
        return dict(tau=None, mu=None, cal_gate=None, cal_fit_feasible=False,
                    test_gate=gate_metrics([], 1.0, 1.0), classes=sorted(cent.keys()), n_fit=len(fit))
    tau, mu = best[1]
    cal_gate = best[2]
    fit_feasible = bool(best[0][0])
    test_rows = test
    test_scored = score(test_rows)
    test_gate = gate_metrics(test_scored, tau, mu)
    return dict(tau=tau, mu=mu, cal_gate=cal_gate, cal_fit_feasible=fit_feasible, test_gate=test_gate,
                classes=sorted(cent.keys()), n_fit=len(fit))


def shuffled_selection(rows, mode, seed):
    rng = random.Random(seed)
    ex = [r for r in rows if is_executed(r, mode) and r["app"]]
    if not ex:
        return None
    targets = [r["target"] for r in ex]
    rng.shuffle(targets)
    return sum(1 for r, t in zip(ex, targets) if r["mech"] == t) / len(ex)


def random_role_selection(rows, mode, seed):
    rng = random.Random(seed)
    mechs = sorted({r["target"] for r in rows if r["app"]})
    ex = [r for r in rows if is_executed(r, mode) and r["app"]]
    if not ex or not mechs:
        return None
    return sum(1 for r in ex if r["mech"] == rng.choice(mechs)) / len(ex)


def matched_random_gate(rows, mode, seed):
    rng = random.Random(seed)
    ab_n = sum(1 for r in rows if not is_executed(r, mode))
    idx = list(range(len(rows))); rng.shuffle(idx)
    ab = set(idx[:ab_n])
    ex = [r for i, r in enumerate(rows) if i not in ab]
    co = [r for r in rows if not r["app"]]
    abr = [r for i, r in enumerate(rows) if i in ab]
    return dict(pooled_false_accept=(sum(1 for r in ex if not r["app"]) / len(co)) if co else None,
                unknown_precision=(sum(1 for r in abr if not r["app"]) / len(abr)) if abr else None,
                matched_abstention_count=ab_n)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    prereg_path = Path(os.environ.get("SPIDER_PREREG", str(EXP_DIR / "prereg.md")))
    self_text = prereg_path.read_text(encoding="utf-8")
    g3_app = jlines(extract_block(self_text, "GOAL-BANK-G3"))
    g3_oos = jlines(extract_block(self_text, "OOS-BANK-G3"))
    lex_g3 = json.loads(extract_block(self_text, "LEXICON-G3"))
    parent_text = (PARENT / "prereg.md").read_text(encoding="utf-8")
    g1_app = jlines(extract_block(parent_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(parent_text, "OOS-BANK-G1"))
    lex_g1 = json.loads(extract_block(parent_text, "LEXICON-G1"))
    lex_alt = json.loads(extract_block(parent_text, "LEXICON-G1-ALT"))
    g2_app = jlines(extract_block(parent_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(parent_text, "OOS-BANK-G2"))
    lex_ho = json.loads(extract_block(parent_text, "LEXICON-G2-HELDOUT"))
    grand = (GRANDPARENT / "prereg.md").read_text(encoding="utf-8")
    prior_parent = json.loads(extract_block(grand, "PRIOR-PARENT-BANK-TEXTS"))
    sys.path.insert(0, str(ROOT / "research/harness"))
    from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES
    gg = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
        list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
    prior_full = gg + list(prior_parent)
    priors_g3 = gg + list(prior_parent) + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos] + \
        [g["text"] for g in g2_app] + [g["text"] for g in g2_oos]

    axes = {}
    for nm, (app, oos, lex, sm, priors) in {
        "AXIS-G3-NEW": (g3_app, g3_oos, lex_g3, 4, priors_g3),
        "AXIS-G2-RETEST": (g2_app, g2_oos, lex_ho, 4, gg + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]),
        "AXIS-G1-PRIMARY": (g1_app, g1_oos, lex_g1, 6, prior_full),
        "AXIS-G1-ALTLEX": (g1_app, g1_oos, lex_alt, 6, prior_full),
    }.items():
        bound, flagged = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, cal=cal, test=test,
                        cal_metrics={m: metrics(cal, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")})
        if not args.mechanics_only:
            axes[nm]["test_metrics"] = {m: metrics(test, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
            axes[nm]["arm_b"] = arm_b(cal, test, SEED)
            axes[nm]["shuffled_selection"] = shuffled_selection(test, "tframeplus", SEED)
            axes[nm]["random_role_selection"] = random_role_selection(test, "tframeplus", SEED)
            axes[nm]["ctrl_random_gate"] = matched_random_gate(test, "tframeplus", SEED)

    if args.mechanics_only:
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
                                 cal_n=[sum(1 for r in v["cal"] if r["app"]), sum(1 for r in v["cal"] if not r["app"])],
                                 cal_metrics=v["cal_metrics"],
                                 cal_feasible_tframeplus=gate_met(v["cal_metrics"]["tframeplus"])) for k, v in axes.items()},
                   c7_firing={k: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                      oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                              for k, v in axes.items()},
                   liveness=dict(g3_cal_executed=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["executed"],
                                 g3_cal_unresolved=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["unresolved_applicable"]),
                   embedding_status="REPLACED-BY-B-RETRIEVAL-TFIDF-STDLIB")
        print(json.dumps(out, indent=2))
        return

    prim = axes["AXIS-G3-NEW"]["test_metrics"]["tframeplus"]
    gates = {a: gate_met(v["test_metrics"]["tframeplus"]) for a, v in axes.items()}
    sels = {a: v["test_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    selection_preserved = all(s is not None and s >= SEL_TARGET for s in sels.values())
    live = (0 < prim["executed_app"] < sum(1 for r in axes["AXIS-G3-NEW"]["test"] if r["app"]))
    invalid_reasons = []
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-G3-NEW test executed_app == 0 or == all applicable")
    for a, v in axes.items():
        if v["test_metrics"]["tframeplus"]["unknown_precision"] is None:
            invalid_reasons.append(f"{a}: unknown_precision undefined (no resolved abstention on test)")
    g3_gate = gates.get("AXIS-G3-NEW"); g2_gate = gates.get("AXIS-G2-RETEST")
    armb_g3 = axes["AXIS-G3-NEW"]["arm_b"]
    armb_g2 = axes["AXIS-G2-RETEST"]["arm_b"]
    armb_g3_met = (armb_g3["test_gate"]["pooled_false_accept"] is not None
                   and armb_g3["test_gate"]["pooled_false_accept"] <= FA_TARGET
                   and armb_g3["test_gate"]["coverage"] >= COV_TARGET
                   and armb_g3["test_gate"]["unknown_precision"] is not None
                   and armb_g3["test_gate"]["unknown_precision"] >= PREC_TARGET)
    armb_g2_met = (armb_g2["test_gate"]["pooled_false_accept"] is not None
                   and armb_g2["test_gate"]["pooled_false_accept"] <= FA_TARGET
                   and armb_g2["test_gate"]["coverage"] >= COV_TARGET
                   and armb_g2["test_gate"]["unknown_precision"] is not None
                   and armb_g2["test_gate"]["unknown_precision"] >= PREC_TARGET)
    if armb_g3_met and not g3_gate:
        retrieval_fork = "RETRIEVAL_DOMINATES_G3"
    elif g3_gate and not armb_g3_met:
        retrieval_fork = "TFRAME_DOMINATES_G3"
    elif g3_gate and armb_g3_met:
        retrieval_fork = "BOTH_PASS_G3"
    else:
        retrieval_fork = "NEITHER_PASSES_G3"
    status = "MEASUREMENT_INVALID" if invalid_reasons else "COMPLETE"
    if invalid_reasons:
        decision = None
    elif g3_gate and g2_gate and selection_preserved:
        decision = "DECIDE_SHIP_TFRAME_BROAD"
    elif g2_gate and selection_preserved:
        decision = "DECIDE_SHIP_TFRAME_SCOPED"
    else:
        decision = "DECIDE_REQUIRE_RETRIEVAL_B"
    out = dict(status=status, experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
               invalid_reasons=invalid_reasons, decision=decision,
               gates=gates, selection={a: sels[a] for a in sels}, selection_preserved=selection_preserved,
               selection_rule="B-LEX-STRONG + C7-CREATE-OBLIQUE",
               retrieval_fork=retrieval_fork, arm_b_gate_met={"g3": armb_g3_met, "g2": armb_g2_met},
               arm_b={"g3": armb_g3["test_gate"], "g2": armb_g2["test_gate"],
                      "g3_tau": armb_g3["tau"], "g3_mu": armb_g3["mu"],
                      "g3_cal_fit_feasible": armb_g3["cal_fit_feasible"]},
               test_metrics={a: v["test_metrics"] for a, v in axes.items()},
               test_n={a: [sum(1 for r in v["test"] if r["app"]), sum(1 for r in v["test"] if not r["app"])] for a, v in axes.items()},
               cal_metrics={a: v["cal_metrics"] for a, v in axes.items()},
               c7_firing={a: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                  oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                          for a, v in axes.items()},
               execution_vectors={a: {r["gid"]: {"split": "test" if r["split"] else "cal",
                                                 "app": r["app"], "mech": r["mech"], "target": r["target"],
                                                 "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
                                                 "clauses": r["clauses"], "S": r["S"],
                                                 "executed": is_executed(r, "tframeplus")} for r in v["bound"]}
                                 for a, v in axes.items()},
               controls={a: dict(shuffled_selection=v["shuffled_selection"], random_role_selection=v["random_role_selection"],
                                 ctrl_random_gate=v["ctrl_random_gate"],
                                 b_lex_strong=v["test_metrics"]["tframeplus"]["selective_acc"],
                                 b_lex_only=v["test_metrics"]["gatefree"]["selective_acc"],
                                 b_incumbent_kernel=0.0,
                                 ctrl_exec_all_fa=v["test_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_abstain_all_cov=0.0, ctrl_abstain_all_up=1.0) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
