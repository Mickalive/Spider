#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38816768796 (design_contract_version 2).
# Tau-rule-sensitivity packet: BLIND-JAC-1NN (genuinely blind: no LEXICON-* read
# at any stage) with a PRE-REGISTERED NON-LOWEST-TAU-WINS SELECT rule
# (feasibility-plus-maximum-FA-slack: argmax over SELECT-feasible taus of
# (FA_TARGET - SELECT pooled_false_accept), tie-break HIGHER tau wins),
# on the frozen banks, against gold T-FRAME+ and honest B-RETRIEVAL-OOS.
# Single-variable ablation vs EXP-GRAPH-38666634300: ONLY the blind tau-selection
# rule changes (ascending-tau first-max -> max-FA-slack); every other byte of
# analysis logic is identical apart from EXP_ID/SEED constants.
# Arm A-gold = T-FRAME+ : shared deterministic lexical selection (B-LEX-STRONG, frozen)
#   + structural frame-completeness abstention clauses C1/C3/C4/C5/C6 (frozen)
#   + C7-CREATE-OBLIQUE (zero tunable parameters). Analysis functions byte-identical to the
#   audited EXP-GRAPH-38530149021 runner lineage; constants re-frozen below; pre-declared
#   blind-leg additions only (blind 1-NN block, blind fork helper, reincluded-scope
#   liveness, continuity tripwires, settled-XSURF-leg removal). NO clause-refit path exists.
# Arm B-OOS = B-RETRIEVAL-OOS : stdlib TF-IDF nearest-class-centroid retrieval with
#   IDF+centroids fit on pooled calibration FIT-TRAIN, gate (tau,mu) selected on
#   disjoint pooled FIT-SELECT under hard mu>0, applied frozen to screened AND reincluded tests.
#   Resubstitution (train==select), mu==0 gates, and any screened-or-reincluded TEST-row use
#   in fit/select are FORBIDDEN and force BLOCKED/measurement-invalid (never silent reuse).
# BLIND-JAC-1NN = treatment: word-unigram Jaccard 1-NN over pooled FIT-TRAIN exemplars,
#   single tau on FIT-SELECT, no LEXICON-* in scope at any stage (see blindness contract
#   in code comments below). Same pooled rows by ablation design (mechanism-given-data).
# Stdlib only. Usage: python runner_blind_resolver.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, os, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38816768796"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
G1G2SRC = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
G3SRC = ROOT / "research/experiments" / "EXP-GRAPH-38291080992"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38816768796 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75
N_TRAIN_FROZEN = 102
N_SELECT_APP_FROZEN = 34
N_SELECT_OOS_FROZEN = 60

# Parent-published flagged TEST gids (tripwire values, from EXP-GRAPH-38530149021/result.json#reincluded_test_gids)
EXPECTED_FLAGGED_TEST = {
    "AXIS-G3-NEW": ["app_026", "app_030", "app_036", "app_076"],
    "AXIS-G2-RETEST": [],
    "AXIS-G1-PRIMARY": ["app_004", "app_052", "app_076", "app_100", "oos_024", "oos_026"],
    "AXIS-G1-ALTLEX": ["app_004", "app_052", "app_076", "app_100", "oos_024", "oos_026"],
}
EXPECTED_GOLD_REINCL = {"AXIS-G3-NEW": True, "AXIS-G2-RETEST": False, "AXIS-G1-PRIMARY": True, "AXIS-G1-ALTLEX": True}
EXPECTED_GOLD_SCREENED = {"AXIS-G3-NEW": True, "AXIS-G2-RETEST": False, "AXIS-G1-PRIMARY": True, "AXIS-G1-ALTLEX": True}

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
    """C7-CREATE-OBLIQUE. Zero tunable parameters. FROZEN (identical to parent)."""
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
    if mode == "tframe_frozen":
        return r["mech"] is not None and not any(v for k, v in r["clauses"].items() if k != "C7-CREATE-OBLIQUE")
    return r["mech"] is not None and not any(r["clauses"].values())


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
    flaggedset = set(flagged)
    bound = [r for r in rows if r["gid"] not in flaggedset]
    flagged_test = [r for r in rows if r["gid"] in flaggedset and r["split"]]
    return bound, flagged, flagged_test


def metrics(rows, mode):
    ex = [r for r in rows if is_executed(r, mode)]
    exo = sum(1 for r in ex if not r["app"]); exa = sum(1 for r in ex if r["app"])
    co = sum(1 for r in rows if not r["app"]); ca = sum(1 for r in rows if r["app"])
    abR = [r for r in rows if r["mech"] is not None and not is_executed(r, mode)]
    abRo = sum(1 for r in abR if not r["app"])
    ab_all = [r for r in rows if not is_executed(r, mode)]
    sel = sum(1 for r in ex if r["app"] and r["mech"] == r["target"])
    return dict(coverage=exa / ca if ca else None, pooled_false_accept=exo / co if co else None,
                unknown_precision_exclusive=abRo / len(abR) if abR else None,
                unknown_precision_inclusive=(sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None,
                unknown_precision=abRo / len(abR) if abR else None,
                executed=len(ex), executed_oos=exo, executed_app=exa, abstained_resolved=len(abR),
                selective_acc=sel / exa if exa else None,
                unresolved_applicable=sum(1 for r in rows if r["app"] and r["mech"] is None))


def gate_met(m):
    return bool(m["pooled_false_accept"] is not None and m["pooled_false_accept"] <= FA_TARGET
                and m["coverage"] is not None and m["coverage"] >= COV_TARGET
                and m["unknown_precision_exclusive"] is not None and m["unknown_precision_exclusive"] >= PREC_TARGET)


def arm_gate(g):
    """Gate check for retrieval/blind test_gate entries (screened or reincluded)."""
    return bool(g is not None
                and g["pooled_false_accept"] is not None and g["pooled_false_accept"] <= FA_TARGET
                and g["coverage"] is not None and g["coverage"] >= COV_TARGET
                and g["unknown_precision_exclusive"] is not None and g["unknown_precision_exclusive"] >= PREC_TARGET)


def fork_of(g3_gate, armb_g3_met, feasible):
    if not feasible:
        return "RETRIEVAL_INFEASIBLE_OOS"
    if armb_g3_met and not g3_gate:
        return "RETRIEVAL_DOMINATES_G3"
    if g3_gate and not armb_g3_met:
        return "TFRAME_DOMINATES_G3"
    if g3_gate and armb_g3_met:
        return "BOTH_PASS_G3"
    return "NEITHER_PASSES_G3"


def blind_fork_of(gold_g3_met, blind_g3_met):
    if blind_g3_met and not gold_g3_met:
        return "BLIND_DOMINATES_G3"
    if gold_g3_met and not blind_g3_met:
        return "GOLD_DOMINATES_BLIND_G3"
    if gold_g3_met and blind_g3_met:
        return "BOTH_PASS_G3"
    return "NEITHER_PASSES_G3"


def abstain_all_metrics(rows):
    """NC-ABSTAIN-ALL, EXECUTED (no placeholders): abstain on everything resolved."""
    res = [r for r in rows if r["mech"] is not None]
    abRo = sum(1 for r in res if not r["app"])
    ab_all = list(rows)
    return dict(coverage=0.0, pooled_false_accept=None,
                unknown_precision_exclusive=abRo / len(res) if res else None,
                unknown_precision_inclusive=(sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None,
                unknown_precision=abRo / len(res) if res else None,
                executed=0, executed_oos=0, executed_app=0, abstained_resolved=len(res),
                selective_acc=None,
                unresolved_applicable=sum(1 for r in rows if r["app"] and r["mech"] is None))


# ---------------- Arm B-OOS : honest pooled retrieval (non-resubstitution, mu>0) ----------------
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


def build_fit_pool(axes):
    """Pool calibration rows across G1-PRIMARY/G2-RETEST/G3-NEW (one G1 axis only:
    ALTLEX shares G1 texts and would duplicate them). Deterministic global order."""
    pool_app, pool_oos = [], []
    for nm in ("AXIS-G1-PRIMARY", "AXIS-G2-RETEST", "AXIS-G3-NEW"):
        for r in axes[nm]["cal"]:
            (pool_app if r["app"] else pool_oos).append((nm, r))
    train, sel_app = [], []
    for i, item in enumerate(pool_app):
        (sel_app if (i % 4 == 3) else train).append(item)
    return train, sel_app, pool_oos


def text_sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def arm_b_oos(train, sel_app, sel_oos, tests, tests_reincl):
    """IDF+centroids on TRAIN app rows; gate (tau,mu>0) on SELECT; frozen apply to
    screened tests AND reincluded tests. Returns (result_dict, construction_flags).
    Any forbidden fallback -> feasible False with reason; caller maps persistent
    infeasibility to RETRIEVAL_INFEASIBLE_OOS on both forks."""
    fit = [r for _, r in train]
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
    cent = {cls: {f: x / (math.sqrt(sum(y * y for y in v.values())) or 1.0) for f, x in v.items()} for cls, v in cent.items()}

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
        up = abRo / len(ab) if ab else None
        return dict(coverage=exa / ca if ca else 0.0, pooled_false_accept=exo / co if co else None,
                    unknown_precision_exclusive=up, unknown_precision_inclusive=up, unknown_precision=up,
                    selective_acc=sel / exa if exa else None,
                    executed=len(ex), executed_app=exa, executed_oos=exo, abstained=len(ab))

    sel_rows = [r for _, r in sel_app] + [r for _, r in sel_oos]
    sel_scored = score(sel_rows)
    taus = sorted({round(s, 4) for _, _, s, _ in sel_scored})
    mus = sorted({round(m, 4) for _, _, _, m in sel_scored if round(m, 4) > 0.0})
    if not mus:
        empty = {a: None for a in tests}
        return dict(feasible=False, reason="no-positive-margin-candidate-on-SELECT",
                    tau=None, mu=None, select_gate=None, n_fit_train=N,
                    n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                    classes=sorted(cent.keys()), test_gate=empty, test_gate_reincl=dict(empty)), True
    best = None
    for tau in taus:
        for mu in mus:
            gm = gate_metrics(sel_scored, tau, mu)
            feasible = (gm["pooled_false_accept"] is not None and gm["pooled_false_accept"] <= FA_TARGET
                        and gm["coverage"] >= COV_TARGET
                        and gm["unknown_precision_exclusive"] is not None and gm["unknown_precision_exclusive"] >= PREC_TARGET)
            key = (1 if feasible else 0, gm["coverage"] if gm["coverage"] else 0.0)
            if best is None or key > best[0]:
                best = (key, (tau, mu), gm)
    tau, mu = best[1]
    select_gate = best[2]
    fit_feasible = bool(best[0][0])
    out_tests = {}
    for a, trows in tests.items():
        out_tests[a] = gate_metrics(score(trows), tau, mu) if fit_feasible else None
    out_reincl = {}
    for a, trows in tests_reincl.items():
        out_reincl[a] = gate_metrics(score(trows), tau, mu) if fit_feasible else None
    return dict(feasible=fit_feasible, reason=None if fit_feasible else "no-feasible-mu-positive-gate-on-SELECT",
                tau=tau, mu=mu, select_gate=select_gate, n_fit_train=N,
                n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                classes=sorted(cent.keys()), test_gate=out_tests, test_gate_reincl=out_reincl), True


# ---------------- BLIND-JAC-1NN : genuinely blind resolver (NEW treatment) ----------------
# BLINDNESS CONTRACT (auditable): these functions accept ONLY (text, target) exemplar
# pairs from the pooled FIT-TRAIN pool. No LEXICON-* object is in scope here: no lex
# parameter exists, no lexicon block is read, no surface-form dictionary is consulted.
# Resolution = 1-nearest TRAIN exemplar by word-unigram Jaccard; abstention = single
# threshold tau on the 1-NN Jaccard score, fitted on FIT-SELECT only.
# Mechanism distance from B-RETRIEVAL-OOS (identifiability): (1) features unigram-only
# vs uni+bigram; (2) no IDF/term weighting (raw sets) vs sublinear-tf*IDF; (3) 1-NN
# exemplar vs per-class L2 centroid; (4) Jaccard vs cosine; (5) single-tau gate vs
# (tau,mu) margin gate. Shared by design: the SAME pooled FIT-TRAIN/FIT-SELECT rows
# (the separator is mechanism-given-data, the standard ablation shape).
def _blind_token_set(text):
    return set(tokens(text))


def blind_jac_predict(tok_sets_targets, text):
    """1-NN by unigram Jaccard over pooled TRAIN exemplars. Deterministic: fixed TRAIN
    order, strict-greater replacement, so ties resolve to the earliest TRAIN row."""
    q = _blind_token_set(text)
    best_cls, best_s = None, -1.0
    for toks, cls in tok_sets_targets:
        inter = len(q & toks)
        union = len(q | toks)
        s = inter / union if union else 0.0
        if s > best_s:
            best_s, best_cls = s, cls
    return best_cls, best_s


def blind_gate_metrics(scored, tau):
    """Same gate formula as retrieval (every scored row is decision-conditional, so
    exclusive==inclusive by construction). scored = [(row, pred_cls, score)]."""
    ex = [(r, c) for r, c, s in scored if s >= tau]
    ab = [(r, c, s) for r, c, s in scored if not (s >= tau)]
    exo = sum(1 for r, c in ex if not r["app"]); exa = sum(1 for r, c in ex if r["app"])
    co = sum(1 for r in scored if not r[0]["app"]); ca = sum(1 for r in scored if r[0]["app"])
    abRo = sum(1 for r, c, s in ab if not r["app"])
    sel = sum(1 for r, c in ex if r["app"] and c == r["target"])
    up = abRo / len(ab) if ab else None
    return dict(coverage=exa / ca if ca else 0.0, pooled_false_accept=exo / co if co else None,
                unknown_precision_exclusive=up, unknown_precision_inclusive=up, unknown_precision=up,
                selective_acc=sel / exa if exa else None,
                executed=len(ex), executed_app=exa, executed_oos=exo, abstained=len(ab))


def arm_blind_oos(train, sel_app, sel_oos, tests, tests_reincl, permute_seed=None, frozen_tau=None):
    """Blind 1-NN fit on TRAIN exemplar texts; single tau selected on SELECT
    by the frozen max-FA-slack rule (argmax over feasible of FA_TARGET - SELECT FA,
    tie-break higher tau; explicitly NOT lowest-tau-wins);
    frozen tau applied to screened AND reincluded tests. permute_seed is not None only
    for CTRL-BLIND-PERMUTED (TRAIN targets shuffled by Random(permute_seed); the REAL
    frozen tau passed via frozen_tau is applied unchanged, so the execute/abstain
    partition equals the real blind partition by construction and only the predicted
    labels differ). Never reads TEST rows in fit/select; never reads any lexicon."""
    fit_pairs = [(_blind_token_set(r["text"]), r["target"]) for _, r in train]
    if permute_seed is not None:
        rng = random.Random(permute_seed)
        tgts = [c for _, c in fit_pairs]
        rng.shuffle(tgts)
        fit_pairs = [(t, c) for (t, _), c in zip(fit_pairs, tgts)]
        assert frozen_tau is not None, "permuted null requires the real frozen tau"

    def score(rows):
        out = []
        for r in rows:
            cls, s = blind_jac_predict(fit_pairs, r["text"])
            out.append((r, cls, s))
        return out

    sel_rows = [r for _, r in sel_app] + [r for _, r in sel_oos]
    sel_scored = score(sel_rows)
    if frozen_tau is not None:
        tau = frozen_tau
        select_gate = blind_gate_metrics(sel_scored, tau)
        fit_feasible = arm_gate(select_gate)
        select_slack = ((FA_TARGET - select_gate["pooled_false_accept"])
                        if select_gate["pooled_false_accept"] is not None else None)
    else:
        # PRE-REGISTERED NON-LOWEST-TAU-WINS RULE (max-FA-slack):
        # among SELECT-feasible taus maximise (FA_TARGET - SELECT FA);
        # tie-break HIGHER tau wins (explicitly not lowest-tau-wins).
        # Key is fully ordered (taus distinct), so strict-greater picks the
        # unique maximum regardless of iteration order.
        taus = sorted({round(s, 4) for _, _, s in sel_scored})
        best = None
        for tau in taus:
            gm = blind_gate_metrics(sel_scored, tau)
            feasible = (gm["pooled_false_accept"] is not None and gm["pooled_false_accept"] <= FA_TARGET
                        and gm["coverage"] >= COV_TARGET
                        and gm["unknown_precision_exclusive"] is not None and gm["unknown_precision_exclusive"] >= PREC_TARGET)
            slack = (FA_TARGET - gm["pooled_false_accept"]) if feasible else -1.0
            key = (1 if feasible else 0, slack, tau)
            if best is None or key > best[0]:
                best = (key, tau, gm)
        tau = best[1]
        select_gate = best[2]
        fit_feasible = bool(best[0][0])
        select_slack = best[0][1] if fit_feasible else None
    out_tests = {}
    for a, trows in tests.items():
        out_tests[a] = blind_gate_metrics(score(trows), tau)
    out_reincl = {}
    for a, trows in tests_reincl.items():
        out_reincl[a] = blind_gate_metrics(score(trows), tau)
    return dict(feasible=fit_feasible, reason=None if fit_feasible else "no-feasible-tau-gate-on-SELECT",
                tau=tau, select_rule="max-slack-fa-tiebreak-higher-tau", select_slack=select_slack,
                select_gate=select_gate, n_fit_train=len(fit_pairs),
                n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                permuted=bool(permute_seed is not None),
                test_gate=out_tests, test_gate_reincl=out_reincl)


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


def load_banks():
    g3_text = (G3SRC / "prereg.md").read_text(encoding="utf-8")
    g3_app = jlines(extract_block(g3_text, "GOAL-BANK-G3"))
    g3_oos = jlines(extract_block(g3_text, "OOS-BANK-G3"))
    lex_g3 = json.loads(extract_block(g3_text, "LEXICON-G3"))
    g1g2_text = (G1G2SRC / "prereg.md").read_text(encoding="utf-8")
    g1_app = jlines(extract_block(g1g2_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(g1g2_text, "OOS-BANK-G1"))
    lex_g1 = json.loads(extract_block(g1g2_text, "LEXICON-G1"))
    lex_alt = json.loads(extract_block(g1g2_text, "LEXICON-G1-ALT"))
    g2_app = jlines(extract_block(g1g2_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(g1g2_text, "OOS-BANK-G2"))
    lex_ho = json.loads(extract_block(g1g2_text, "LEXICON-G2-HELDOUT"))
    grand = (GRANDPARENT / "prereg.md").read_text(encoding="utf-8")
    prior_parent = json.loads(extract_block(grand, "PRIOR-PARENT-BANK-TEXTS"))
    sys.path.insert(0, str(ROOT / "research/harness"))
    from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES
    gg_only = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
        list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
    prior_full = gg_only + list(prior_parent)
    priors_g3 = gg_only + list(prior_parent) + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos] + \
        [g["text"] for g in g2_app] + [g["text"] for g in g2_oos]
    priors_g2 = gg_only + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]
    return dict(g3_app=g3_app, g3_oos=g3_oos, lex_g3=lex_g3, g1_app=g1_app, g1_oos=g1_oos,
                lex_g1=lex_g1, lex_alt=lex_alt, g2_app=g2_app, g2_oos=g2_oos, lex_ho=lex_ho,
                prior_full=prior_full, priors_g3=priors_g3, priors_g2=priors_g2)


def build_axes(banks):
    axes = {}
    spec = {
        "AXIS-G3-NEW": (banks["g3_app"], banks["g3_oos"], banks["lex_g3"], 4, banks["priors_g3"]),
        "AXIS-G2-RETEST": (banks["g2_app"], banks["g2_oos"], banks["lex_ho"], 4, banks["priors_g2"]),
        "AXIS-G1-PRIMARY": (banks["g1_app"], banks["g1_oos"], banks["lex_g1"], 6, banks["prior_full"]),
        "AXIS-G1-ALTLEX": (banks["g1_app"], banks["g1_oos"], banks["lex_alt"], 6, banks["prior_full"]),
    }
    for nm, (app, oos, lex, sm, priors) in spec.items():
        bound, flagged, flagged_test = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, flagged_test=flagged_test, cal=cal, test=test,
                        test_reincl=test + flagged_test,
                        cal_metrics={m: metrics(cal, m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")})
    return axes


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    banks = load_banks()
    axes = build_axes(banks)
    train, sel_app, sel_oos = build_fit_pool(axes)
    train_shas = {text_sha(r["text"]) for _, r in train}
    sel_shas = {text_sha(r["text"]) for _, r in sel_app} | {text_sha(r["text"]) for _, r in sel_oos}
    test_shas = {text_sha(r["text"]) for a, v in axes.items() for r in v["test"] + v["flagged_test"]}
    construction_ok = (len(train) == N_TRAIN_FROZEN and len(sel_app) == N_SELECT_APP_FROZEN
                       and len(sel_oos) == N_SELECT_OOS_FROZEN
                       and not (train_shas & sel_shas) and not ((train_shas | sel_shas) & test_shas))
    construction = dict(n_fit_train=len(train), n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                        train_select_disjoint=not (train_shas & sel_shas),
                        fit_test_disjoint=not ((train_shas | sel_shas) & test_shas),
                        bars_met=construction_ok,
                        train_gids=[f"{a}:{r['gid']}" for a, r in train],
                        select_gids=[f"{a}:{r['gid']}" for a, r in sel_app] + [f"{a}:{r['gid']}" for a, r in sel_oos])

    if args.mechanics_only:
        fit_res, _ = arm_b_oos(train, sel_app, sel_oos, {}, {})
        blind_res = arm_blind_oos(train, sel_app, sel_oos, {}, {})
        # CAL-only blind probes (no TEST rows read or scored here):
        sel_rows = [r for _, r in sel_app] + [r for _, r in sel_oos]
        cal_rows = [r for a, v in axes.items() for r in v["cal"]]
        fit_pairs = [(_blind_token_set(r["text"]), r["target"]) for _, r in train]
        btau = blind_res["tau"]
        cal_scored = []
        for r in cal_rows:
            cls, s = blind_jac_predict(fit_pairs, r["text"])
            cal_scored.append((r, cls, s))
        cal_gm = blind_gate_metrics(cal_scored, btau)
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   seed=SEED,
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
                                 flagged_test_gids=[r["gid"] for r in v["flagged_test"]],
                                 flagged_test_match_expected=([r["gid"] for r in v["flagged_test"]] == EXPECTED_FLAGGED_TEST[k]),
                                 cal_n=[sum(1 for r in v["cal"] if r["app"]), sum(1 for r in v["cal"] if not r["app"])],
                                 cal_metrics=v["cal_metrics"],
                                 cal_feasible_tframeplus=gate_met(v["cal_metrics"]["tframeplus"])) for k, v in axes.items()},
                   c7_firing={k: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                      oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                              for k, v in axes.items()},
                   fit_pool=construction,
                   retrieval_select=dict(feasible=fit_res["feasible"], reason=fit_res["reason"],
                                         tau=fit_res["tau"], mu=fit_res["mu"],
                                         mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                                         select_gate=fit_res["select_gate"]),
                   blind_select=dict(feasible=blind_res["feasible"], reason=blind_res["reason"],
                                     tau=blind_res["tau"], select_rule=blind_res["select_rule"],
                                     select_slack=blind_res["select_slack"],
                                     select_gate=blind_res["select_gate"]),
                   blind_cal_probe=dict(select_executed=blind_res["select_gate"]["executed"],
                                        select_abstained=blind_res["select_gate"]["abstained"],
                                        cal_executed=cal_gm["executed"], cal_abstained=cal_gm["abstained"],
                                        cal_coverage=cal_gm["coverage"],
                                        cal_selective=cal_gm["selective_acc"],
                                        cal_up=cal_gm["unknown_precision_exclusive"]),
                   blind_lexicon_guard=dict(
                       lex_params_in_blind_scope=False,
                       note="arm_blind_oos/blind_jac_predict accept only (text,target) pairs; no lexicon object in scope"),
                   test_not_scored=True)
        print(json.dumps(out, indent=2))
        return

    for a, v in axes.items():
        v["test_metrics"] = {m: metrics(v["test"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
        v["reincl_metrics"] = {m: metrics(v["test_reincl"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
        v["abstain_all"] = abstain_all_metrics(v["test"])
        v["abstain_all_reincl"] = abstain_all_metrics(v["test_reincl"])
        v["shuffled_selection"] = shuffled_selection(v["test"], "tframeplus", SEED)
        v["random_role_selection"] = random_role_selection(v["test"], "tframeplus", SEED)
        v["ctrl_random_gate"] = matched_random_gate(v["test"], "tframeplus", SEED)
        v["shuffled_selection_reincl"] = shuffled_selection(v["test_reincl"], "tframeplus", SEED)
        v["random_role_selection_reincl"] = random_role_selection(v["test_reincl"], "tframeplus", SEED)
        v["ctrl_random_gate_reincl"] = matched_random_gate(v["test_reincl"], "tframeplus", SEED)
    tests = {a: v["test"] for a, v in axes.items()}
    tests_reincl = {a: v["test_reincl"] for a, v in axes.items()}
    fit_res, _ = arm_b_oos(train, sel_app, sel_oos, tests, tests_reincl)
    blind_res = arm_blind_oos(train, sel_app, sel_oos, tests, tests_reincl)
    blind_perm = arm_blind_oos(train, sel_app, sel_oos, tests, tests_reincl, permute_seed=SEED + 1,
                              frozen_tau=blind_res["tau"])

    gates = {a: gate_met(v["test_metrics"]["tframeplus"]) for a, v in axes.items()}
    gates_reincl = {a: gate_met(v["reincl_metrics"]["tframeplus"]) for a, v in axes.items()}
    sels_reincl = {a: v["reincl_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    selection_reincl = all(s is not None and s >= SEL_TARGET for s in sels_reincl.values())
    # gold liveness on the REINCLUDED G3 TEST (scope-adapted from the parent screened rule)
    g3tr = axes["AXIS-G3-NEW"]["test_reincl"]
    prim_reincl = axes["AXIS-G3-NEW"]["reincl_metrics"]["tframeplus"]
    g3tr_abstained_resolved = sum(1 for r in g3tr if r["mech"] is not None and not is_executed(r, "tframeplus"))
    live = ((0 < prim_reincl["executed"] < len(g3tr))
            and (prim_reincl["executed_app"] >= 1)
            and (g3tr_abstained_resolved >= 1))
    arm_g3 = (fit_res["test_gate"] or {}).get("AXIS-G3-NEW")
    armb_g3_met = arm_gate(arm_g3)
    armr_g3 = (fit_res["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    armr_g3_met = arm_gate(armr_g3)
    retrieval_fork = fork_of(gates.get("AXIS-G3-NEW"), armb_g3_met, fit_res["feasible"])
    retrieval_fork_reincl = fork_of(gates_reincl.get("AXIS-G3-NEW"), armr_g3_met, fit_res["feasible"])
    blind_g3 = (blind_res["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    blind_g3_met = arm_gate(blind_g3)
    blind_gates_reincl = {a: arm_gate((blind_res["test_gate_reincl"] or {}).get(a)) for a in axes}
    blind_gates_screened = {a: arm_gate((blind_res["test_gate"] or {}).get(a)) for a in axes}
    blind_perm_g3 = (blind_perm["test_gate_reincl"] or {}).get("AXIS-G3-NEW")
    blind_inert = bool(blind_g3 is not None and (blind_g3["executed"] == 0 or blind_g3["abstained"] == 0))
    bfork = blind_fork_of(gates_reincl.get("AXIS-G3-NEW"), blind_g3_met)
    invalid_reasons = []
    if not construction_ok:
        invalid_reasons.append("fit-pool-construction-failed: N_TRAIN==102 AND SELECT_APP==34 AND SELECT_OOS==60 AND train/select/test-union disjointness required; resubstitution fallback forbidden")
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-G3-NEW gold-reincluded test non-degenerate execution failed (need 0 < executed_total < n_total_test AND executed_app >= 1 AND abstained_resolved >= 1)")
    for a, v in axes.items():
        if v["reincl_metrics"]["tframeplus"]["unknown_precision_exclusive"] is None:
            invalid_reasons.append(f"{a}: unknown_precision_exclusive undefined on gold-reincluded test (no resolved abstention)")
    if not gates_reincl.get("AXIS-G1-ALTLEX"):
        invalid_reasons.append("positive-control-failed: PC-AXIS-G1-ALTLEX gold-reincluded gate-met false (runner-enforced invalidity)")
    if gates != EXPECTED_GOLD_SCREENED:
        invalid_reasons.append("screened-reproduction-failed: gold-screened gate vector != parent {G3 met, G1 met, ALTLEX met, G2 false}")
    g2m = axes["AXIS-G2-RETEST"]["test_metrics"]["tframeplus"]
    if not (g2m["pooled_false_accept"] is not None and g2m["pooled_false_accept"] <= FA_TARGET
            and g2m["coverage"] is not None and g2m["coverage"] >= COV_TARGET):
        invalid_reasons.append("screened-reproduction-failed: G2 screened FA/COV bars not passing (false-solely-on-UP required)")
    if retrieval_fork != "TFRAME_DOMINATES_G3":
        invalid_reasons.append("screened-fork-reproduction-failed: screened fork != TFRAME_DOMINATES_G3")
    if any(arm_gate((fit_res["test_gate"] or {}).get(a)) for a in axes):
        invalid_reasons.append("screened-retrieval-reproduction-failed: screened retrieval meets a TEST gate (parent: all four fail)")
    if gates_reincl != EXPECTED_GOLD_REINCL:
        invalid_reasons.append("gold-drift: gold-reincluded gate vector != audited parent reincluded vector (bank drift, not science)")
    if any([r["gid"] for r in v["flagged_test"]] != EXPECTED_FLAGGED_TEST[a] for a, v in axes.items()):
        invalid_reasons.append("screen-drift: reincluded TEST gid sets != parent-published flagged sets")
    if retrieval_fork_reincl != "TFRAME_DOMINATES_G3":
        invalid_reasons.append("fork-drift: reincluded gold-vs-retrieval fork != TFRAME_DOMINATES_G3")
    if any(arm_gate((fit_res["test_gate_reincl"] or {}).get(a)) for a in axes):
        invalid_reasons.append("retrieval-drift: reincluded retrieval meets a TEST gate (parent: all four fail)")
    status = "MEASUREMENT_INVALID" if invalid_reasons else "COMPLETE"
    if invalid_reasons:
        decision = None
    elif not blind_res["feasible"]:
        # Pre-registered mandate stop trigger: the feasibility predicate is byte-identical
        # to the parent packet (9 SELECT-feasible taus published), so on identical banks
        # this branch is a drift guard only. Bank drift must never read as mechanism failure.
        status = "BLOCKED"
        decision = "TAU_RULE_INFEASIBLE"
    elif blind_g3_met:
        decision = "BLIND_SURVIVES"
    else:
        decision = "BLIND_FAILS"
    out = dict(status=status, experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
               invalid_reasons=invalid_reasons, decision=decision, blind_fork_reincl=bfork,
               blind_g3_met=blind_g3_met, blind_inert=blind_inert,
               blind_gates_screened=blind_gates_screened, blind_gates_reincl=blind_gates_reincl,
               gates=gates, gates_reincl=gates_reincl,
               selection_reincl={a: sels_reincl[a] for a in sels_reincl}, selection_reincl_preserved=selection_reincl,
               retrieval_fork=retrieval_fork, retrieval_fork_reincl=retrieval_fork_reincl,
               retrieval_oos_feasible=fit_res["feasible"], retrieval_oos_reason=fit_res["reason"],
               arm_b_oos=dict(tau=fit_res["tau"], mu=fit_res["mu"],
                              mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                              n_fit_train=fit_res["n_fit_train"], n_select_app=fit_res["n_select_app"],
                              n_select_oos=fit_res["n_select_oos"], classes=fit_res["classes"],
                              select_gate=fit_res["select_gate"], test_gate=fit_res["test_gate"],
                              test_gate_reincl=fit_res["test_gate_reincl"]),
               arm_blind_oos=dict(tau=blind_res["tau"], select_rule=blind_res["select_rule"],
                                  select_slack=blind_res["select_slack"],
                                  feasible=blind_res["feasible"], reason=blind_res["reason"],
                                  n_fit_train=blind_res["n_fit_train"], n_select_app=blind_res["n_select_app"],
                                  n_select_oos=blind_res["n_select_oos"],
                                  select_gate=blind_res["select_gate"], test_gate=blind_res["test_gate"],
                                  test_gate_reincl=blind_res["test_gate_reincl"],
                                  permuted_selective=(blind_perm["select_gate"] or {}).get("selective_acc"),
                                  permuted_test_gate=blind_perm["test_gate"],
                                  permuted_test_gate_reincl=blind_perm["test_gate_reincl"],
                                  permuted_g3_met=arm_gate(blind_perm_g3)),
               fit_pool=construction,
               test_metrics={a: v["test_metrics"] for a, v in axes.items()},
               test_reincl_metrics={a: v["reincl_metrics"] for a, v in axes.items()},
               test_n={a: [sum(1 for r in v["test"] if r["app"]), sum(1 for r in v["test"] if not r["app"])] for a, v in axes.items()},
               test_n_reincl={a: [sum(1 for r in v["test_reincl"] if r["app"]), sum(1 for r in v["test_reincl"] if not r["app"])] for a, v in axes.items()},
               reincluded_gids={a: [r["gid"] for r in v["flagged_test"]] for a, v in axes.items()},
               cal_metrics={a: v["cal_metrics"] for a, v in axes.items()},
               c7_firing={a: dict(app=sum(1 for r in v["bound"] if r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]),
                                  oos=sum(1 for r in v["bound"] if not r["app"] and r["clauses"]["C7-CREATE-OBLIQUE"]))
                           for a, v in axes.items()},
               controls={a: dict(shuffled_selection=v["shuffled_selection"], random_role_selection=v["random_role_selection"],
                                 ctrl_random_gate=v["ctrl_random_gate"],
                                 shuffled_selection_reincl=v["shuffled_selection_reincl"],
                                 random_role_selection_reincl=v["random_role_selection_reincl"],
                                 ctrl_random_gate_reincl=v["ctrl_random_gate_reincl"],
                                 b_lex_strong=v["test_metrics"]["tframeplus"]["selective_acc"],
                                 b_lex_strong_reincl=v["reincl_metrics"]["tframeplus"]["selective_acc"],
                                 b_lex_only=v["test_metrics"]["gatefree"]["selective_acc"],
                                 b_lex_only_reincl=v["reincl_metrics"]["gatefree"]["selective_acc"],
                                 b_incumbent_kernel=v["test_metrics"]["incumbent"]["selective_acc"],
                                 b_incumbent_kernel_reincl=v["reincl_metrics"]["incumbent"]["selective_acc"],
                                 incumbent_fa=v["test_metrics"]["incumbent"]["pooled_false_accept"],
                                 incumbent_fa_reincl=v["reincl_metrics"]["incumbent"]["pooled_false_accept"],
                                 ctrl_exec_all_fa=v["test_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_exec_all_fa_reincl=v["reincl_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_abstain_all_cov=v["abstain_all"]["coverage"],
                                 ctrl_abstain_all_up=v["abstain_all"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_up_inclusive=v["abstain_all"]["unknown_precision_inclusive"],
                                 ctrl_abstain_all_reincl_cov=v["abstain_all_reincl"]["coverage"],
                                 ctrl_abstain_all_reincl_up=v["abstain_all_reincl"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_reincl_up_inclusive=v["abstain_all_reincl"]["unknown_precision_inclusive"]) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
