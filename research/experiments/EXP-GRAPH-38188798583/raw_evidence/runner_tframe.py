#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38188798583 (design_contract_version 2).
# Arm A = T-FRAME: shared deterministic lexical selection (B-LEX-STRONG) +
# explicit structural frame-completeness abstention predicate with named clauses
# C1-SUBOP, C3-NO-REFERENCE, C4-COMPLEMENT, C5-SET-QUANT, C6-SOURCE.
# Arm B (retrieval/embedding) is a prerequisite-blocked comparator (BLOCKED).
# Stdlib only for the claim-bearing path. Usage: python runner_tframe.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38188798583"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
PARENT = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38188798583 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75

DET = {"a", "an", "the", "this", "that", "these", "those", "one", "two", "my", "your", "his", "her",
       "its", "our", "their", "each", "every", "any", "some", "all", "no", "another", "other"}
REF = {"id", "identifier", "identified", "number", "numbered", "named", "called", "titled", "referred",
       "labelled", "labeled"}
QUANT = {"all", "every", "each", "any", "some", "several", "many", "both", "whole", "entire",
         "multiple", "batch", "bulk"}
POLITE = {"please", "kindly", "can", "could", "would", "will", "i", "want", "need", "help", "lets", "let"}
SOURCE = {"from", "into", "onto"}
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
    """Shared deterministic selector (B-LEX-STRONG): longest key-set + homograph guard."""
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
    """Explicit, independently checkable frame-completeness clauses. Fires => ABSTAIN."""
    t = r["t"]; cl = {}
    h = 0
    while h < len(t) and t[h] in POLITE:
        h += 1
    head = t[h] if h < len(t) else None
    # C1-SUBOP: an operation is bound but the main (head) verb is a different token and
    # the operation sits behind a subordinating marker -> compound/derived instruction.
    fire = False
    if r["op"]:
        spans = [(s, e) for o, s, e, L in r["osp"] if o == r["op"]]
        if spans:
            osx = min(s for s, _ in spans)
            if head is not None and head != t[osx] and any(i < osx and t[i] in SUBORD for i in range(len(t))):
                fire = True
    cl["C1-SUBOP"] = fire
    # C3-NO-REFERENCE: READ/UPDATE/DELETE must bind an identifier/reference slot.
    cl["C3-NO-REFERENCE"] = bool(r["op"] in ("READ", "UPDATE", "DELETE") and not r["hasref"])
    # C4-COMPLEMENT: an ungoverned content complement after the object NP.
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
    # C5-SET-QUANT: a set quantifier cannot bind a definite/singular frame.
    cl["C5-SET-QUANT"] = any(w in QUANT for w in t)
    return cl


def analyze(text: str, lex: dict):
    r = comp(text, lex)
    cl = frame(r)
    r["clauses"] = cl
    r["S"] = r["famNONE"] + r["opNONE"] + r["opTIE"] + r["noslot"] + r["quant"]
    return r


def is_executed(r: dict, mode: str) -> bool:
    if mode == "gatefree":
        return r["mech"] is not None
    if mode == "incumbent":
        return r["mech"] is not None and r["S"] <= 0
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

    axes = {}
    for nm, (app, oos, lex, sm, priors) in {
        "AXIS-PRIMARY": (g1_app, g1_oos, lex_g1, 6, prior_full),
        "AXIS-ALTLEX": (g1_app, g1_oos, lex_alt, 6, prior_full),
        "AXIS-HELDOUT": (g2_app, g2_oos, lex_ho, 4, gg + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]),
    }.items():
        bound, flagged = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, cal=cal, test=test,
                        cal_metrics={m: metrics(cal, m) for m in ("tframe", "incumbent", "gatefree")})
        if not args.mechanics_only:
            axes[nm]["test_metrics"] = {m: metrics(test, m) for m in ("tframe", "incumbent", "gatefree")}
            axes[nm]["shuffled_selection"] = shuffled_selection(test, "tframe", SEED)
            axes[nm]["random_role_selection"] = random_role_selection(test, "tframe", SEED)
            axes[nm]["ctrl_random_gate"] = matched_random_gate(test, "tframe", SEED)

    # Arm B prerequisite probe (embedding/trained retrieval). Recorded, never fatal.
    try:
        import numpy  # noqa
        import sentence_transformers  # noqa
        embedding_status = "STACK-PRESENT-ARM-B-STILL-REQUIRES-TRAINED-GOALS"
    except Exception as exc:
        embedding_status = f"BLOCKED: {type(exc).__name__}: {exc}"

    if args.mechanics_only:
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
                                 cal_n=[sum(1 for r in v["cal"] if r["app"]), sum(1 for r in v["cal"] if not r["app"])],
                                 cal_metrics=v["cal_metrics"],
                                 cal_feasible_tframe=gate_met(v["cal_metrics"]["tframe"])) for k, v in axes.items()},
                   liveness=dict(tframe_cal_executed=axes["AXIS-PRIMARY"]["cal_metrics"]["tframe"]["executed"],
                                 tframe_cal_unresolved=axes["AXIS-PRIMARY"]["cal_metrics"]["tframe"]["unresolved_applicable"]),
                   embedding_status=embedding_status)
        print(json.dumps(out, indent=2))
        return

    prim = axes["AXIS-PRIMARY"]["test_metrics"]["tframe"]
    gates = {a: gate_met(v["test_metrics"]["tframe"]) for a, v in axes.items()}
    sels = {a: v["test_metrics"]["tframe"]["selective_acc"] for a, v in axes.items()}
    selection_preserved = all(s is not None and s >= SEL_TARGET for s in sels.values())
    live = (0 < prim["executed_app"] < sum(1 for r in axes["AXIS-PRIMARY"]["test"] if r["app"]))
    invalid_reasons = []
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-PRIMARY test executed_app == 0 or == all applicable")
    for a, v in axes.items():
        if v["test_metrics"]["tframe"]["unknown_precision"] is None:
            invalid_reasons.append(f"{a}: unknown_precision undefined (no resolved abstention on test)")
    status = "MEASUREMENT_INVALID" if invalid_reasons else "COMPLETE"
    if invalid_reasons:
        decision = None
    elif gates.get("AXIS-PRIMARY") and selection_preserved and gates.get("AXIS-ALTLEX") and gates.get("AXIS-HELDOUT"):
        decision = "DECIDE_SHIP_A"
    elif gates.get("AXIS-PRIMARY") and selection_preserved:
        decision = "DECIDE_SHIP_A_SCOPED"
    else:
        decision = "DECIDE_REQUIRE_B"
    out = dict(status=status, experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
               invalid_reasons=invalid_reasons,
               decision=decision,
               gates=gates, selection={a: sels[a] for a in sels}, selection_preserved=selection_preserved,
               selection_rule="B-LEX-STRONG",
               test_metrics={a: v["test_metrics"] for a, v in axes.items()},
               test_n={a: [sum(1 for r in v["test"] if r["app"]), sum(1 for r in v["test"] if not r["app"])] for a, v in axes.items()},
               cal_metrics={a: v["cal_metrics"] for a, v in axes.items()},
               execution_vectors={a: {r["gid"]: {"split": "test" if r["split"] else "cal",
                                                 "app": r["app"], "mech": r["mech"], "target": r["target"],
                                                 "text_sha256": hashlib.sha256(r["text"].encode()).hexdigest(),
                                                 "clauses": r["clauses"], "S": r["S"],
                                                 "executed": is_executed(r, "tframe")} for r in v["bound"]}
                                 for a, v in axes.items()},
               controls={a: dict(shuffled_selection=v["shuffled_selection"], random_role_selection=v["random_role_selection"],
                                 ctrl_random_gate=v["ctrl_random_gate"],
                                 b_lex_strong=v["test_metrics"]["tframe"]["selective_acc"],
                                 b_lex_only=v["test_metrics"]["gatefree"]["selective_acc"],
                                 b_incumbent_kernel=0.0,
                                 ctrl_exec_all_fa=v["test_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_abstain_all_cov=0.0, ctrl_abstain_all_up=1.0) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()},
               embedding_status=embedding_status)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
