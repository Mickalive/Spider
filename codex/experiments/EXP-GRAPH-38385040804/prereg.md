# EXP-GRAPH-38385040804 preregistration — Graph abstention-boundary retest (DESIGN, design_contract_version 2)

## 0. Mandate, inherited state, and legacy position

- Binding direction: `request.json#director_mandate` (cycle `38384697401`, Graph `CONTINUE`, cognitive_reset `true`, claim `C-SEMANTIC-RESOLVE`, parent_handoff_disposition `USE`). The Director's strategic question is converted here into the smallest rigorous falsifiable experiment; no drift to a nearby objective.
- Director question (binding): under a pre-registered abstention-precision definition fixing the exclusive-vs-inclusive denominator before any run, and against a retrieval comparator with a genuinely out-of-sample fit (larger fit set, non-resubstitution gate, active margin mu>0), does the AXIS-G2-RETEST unknown_precision shortfall persist as an intrinsic no-refit structural bound, or does the ship/no-ship branch flip, and what abstention boundary should Product keep?
- Smallest batch per mandate: single retest leg on the frozen axes (no new anchor/surface collection). Stop trigger honored: if no larger fit set is constructible at DESIGN time, this packet records the blocker and PARKs rather than re-running resubstitution. DESIGN probe (§8.7) shows a 139-row pooled calibration fit pool IS constructible (3.5x parent n_fit=39), so the experiment proceeds.
- Parent handoff preserved (`research/experiments/EXP-GRAPH-38291080992/handoff.json`, sha `07049d2c...941fd`): `established` (validity repair LIVE=True 38/56; frozen bound G3-met/G2-false-solely-on-UP-10/12; fork BOTH_PASS_G3 at gate level; Product keeps conservative boundary), `rejected` (applicable-only liveness predicate; ship branches on that vector; strict Arm-B domination), `unknown` (UP denominator choice; no-refit reducibility; honest-retrieval fork; third surface forbidden here; C7 authorship exposure; H1-scope divergence), and `do_not_assume` (all eight guards, incl. RQF-01 scope qualifier, RQF-02 one-row denominator fragility, RQF-03 placeholder control, RQF-04 byte-identical reproduction disclosure, RQF-05 gate-level-only fork) are carried forward unchanged. This packet closes RQF-01/02/03/05/06 by construction (see §6/§7/§8.10); RQF-04 is honored by explicit reproduction disclosure (§10).
- Legacy position (`LEGACY: DISTINCT_EXTENSION`): DESIGN searched `codex/legacy_artifact_index.json` (1401 artifacts) for `abstention|unknown_precision|semantic resolve|retrieval comparator|t-frame|tframe`: **0 hits** — no pre-2.0 abstention-precision experiment exists. Nearest neighbors (Director-concurred): `P2-BLIND-COMPOSITION` (pre2 product summary artifact 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`: 3/3 unseen compositions vs 0/3 weak baselines, keyword/oracle confounds) and `P2-MIND2WEB` (archived Codex §1: 6/176 exact matches, 47/176 retrieval). Neither fixes an abstention-precision denominator nor fits an out-of-sample retrieval gate with an active margin; this packet adds both plus harmonized cross-arm denominators. Independent replication rationale with materially improved validity; not a duplicate. Absence of an index hit is not claimed as proof of absence from the full archive (brief guard).

## 1. Hypotheses (single frozen texts; closes parent RQF-01)

- H1 (no-refit structural bound; covers the realized G3-pass/G2-fail vector explicitly): on the frozen banks with the frozen zero-tunable-parameter clause set (treatment logic identical to the audited parent runner), T-FRAME+ reproduces the parent gate vector under the pre-registered EXCLUSIVE definition: `AXIS-G3-NEW` gate-met, `AXIS-G1-PRIMARY` gate-met, `AXIS-G1-ALTLEX` gate-met, `selection_preserved=true`, and `AXIS-G2-RETEST` gate-false SOLELY on `unknown_precision_exclusive<0.85` (parent-published 10/12=0.8333; FA 0.0 and coverage 0.925 pass).
- H2 (honest retrieval viability): `B-RETRIEVAL-OOS` — centroids+IDF fit on pooled calibration FIT-TRAIN (n>=78, >=2x parent n_fit=39), gate `(tau,mu)` selected on disjoint pooled FIT-SELECT under hard `mu>0`, applied frozen to every axis test — is feasible, and its `AXIS-G3-NEW` fork against T-FRAME+ (with G2 viability reported) decides whether Product's retrieval-B requirement stands as specified.
- Expectation from parent-published evidence (NOT a result): H1 reproduces deterministically (bound persists); the honest fork and mu-feasibility are genuinely open (parent mu=0.0-class fits are INFEASIBLE by construction here).
- Falsifier (frozen): H1 SUPPORTED iff the gate vector reproduces the parent exactly at gate level as above. H1 FALSIFIED (branch flips) if `AXIS-G2-RETEST` is gate-met under the exclusive definition, or `AXIS-G3-NEW` is gate-false, or any G1 gate flips vs parent, or `selection_preserved` is false. H2 decided by the frozen fork (§7). Gating any decision on `unknown_precision_inclusive` is pre-declared invalid: on identical parent rows inclusive emits BROAD without new evidence (audit RQF-02), so inclusive is sensitivity-only (§6).

## 2. Treatment: T-FRAME+ (frozen, disclosed reproduction)

- Arm A = `B-LEX-STRONG` shared deterministic selector + structural abstention clauses `C1-SUBOP/C3-NO-REFERENCE/C4-COMPLEMENT/C5-SET-QUANT/C6-SOURCE` + `C7-CREATE-OBLIQUE`, all zero tunable parameters. Analysis logic (`comp/frame/clause_c7/is_executed/metrics`) is identical to the audited parent `CANONICAL-RUNNER-SHA256 11fa24673a0d7ceb4c06252a6495dc6a11fcc5e47350c6ccbff7ced24edc7508` lineage; only experiment constants, bank sources, the retrieval arm, the abstain-all control, and the PC trigger differ (all pre-declared here).
- Per parent RQF-04: the T-FRAME+ leg re-executes deterministically on frozen banks and is EXPECTED to reproduce parent test metrics byte-for-byte. This packet states upfront it is a validity-transaction reproduction for Arm A; NEW evidence comes from (a) the pre-fixed exclusive denominator decision and (b) the honest-retrieval leg. EXECUTE must re-emit every metric, never inherit parent numbers.
- Liveness (repaired scope, unchanged from parent): `LIVE = (0<executed_total_test<n_total_test) AND (executed_app_test>=1) AND (abstained_resolved_test>=1)` on `AXIS-G3-NEW` TEST only.

## 3. Comparator: Arm B-OOS (honest, larger, non-resubstitution, margin-active)

- Mechanism (stdlib only): word unigram + adjacent-bigram features; IDF from FIT-TRAIN app rows only; per-class L2-normalised centroids; prediction = nearest centroid; confidence = top cosine; margin = top minus second. Distinct implementation from Arm A; shares no fitted state; never the cost denominator of Arm A.
- FIT pool (frozen construction, calibration rows only): pool = `AXIS-G1-PRIMARY` cal + `AXIS-G2-RETEST` cal + `AXIS-G3-NEW` cal (one G1 axis only, avoiding duplicate texts with ALTLEX). Pooled cal-app = 60+40+39 = **139 rows** (3.5x parent n_fit=39); pooled cal-OOS = 20+20+20 = **60 rows**. Nested split: every 4th pooled-app row (global order G1,G2,G3; `idx%4==3`) to FIT-SELECT (~35 app rows); remainder to FIT-TRAIN (~104 app rows); ALL pooled cal-OOS to FIT-SELECT. Gate `(tau,mu)` searched on FIT-SELECT only (lexicographic maximise-feasibility-then-coverage, same rule as parent), hard constraint `mu>0` (candidate `round(margin,4)>0` only). Frozen gate applied unchanged to each axis test.
- Fairness disclosure (pre-registered, for AUDIT): the three surfaces are disjoint domains (G1 users/posts/comments/albums/photos; G2 teams/projects/events/tickets/files; G3 routes/vehicles/drivers/stops/fares), so pooled TRAIN contains same-surface classes for every test axis (incl. all G3 test classes via the 39 G3 cal rows) plus cross-domain distractors. Dilution biases AGAINST retrieval: viability found under pooling is robust evidence; collapse carries the dilution caveat and vacates the retrieval-B requirement *as specified* without falsifying retrieval in general.
- Forbidden fallbacks (violation = BLOCKED, never silent reuse): refitting deterministic clauses; gate search touching TRAIN rows as select rows or any TEST row; `mu==0` gate; ancestor resubstitution values substituted for the OOS leg.
- Infeasibility is informative, not invalid: if no `(tau,mu>0)` is feasible on SELECT, the arm emits `RETRIEVAL_INFEASIBLE_OOS` (fork value, §7) and the T-FRAME cascade still decides.

## 4. Banks, lexicons, priors (reuse by reference; no new collection)

- G3: `LEXICON-G3`, `GOAL-BANK-G3`, `OOS-BANK-G3` read at runtime from frozen `research/experiments/EXP-GRAPH-38291080992/prereg.md` §13.1–13.3. DESIGN verified byte-identical to `research/experiments/EXP-GRAPH-38205284279/prereg.md` (3834/6357/3672 chars identical). Blind-authorship property inherited by identity.
- G1/G2: `GOAL-BANK-G1/OOS-BANK-G1/LEXICON-G1/LEXICON-G1-ALT/GOAL-BANK-G2/OOS-BANK-G2/LEXICON-G2-HELDOUT` from frozen `research/experiments/EXP-GRAPH-38180711589/prereg.md` (every block verified present in DESIGN).
- Priors: `PRIOR-PARENT-BANK-TEXTS` from frozen `research/experiments/EXP-GRAPH-38175554380/prereg.md` + `research/harness/goal_generator.py` vocabularies.
- Contamination screen (frozen, unchanged): token Jaccard>=0.60 OR trigram Jaccard>=0.75 vs frozen priors+banks drops rows from binding (recorded in `flagged`, not counted). Parent G3 effect: 5 applicable rows dropped → binding 115 (75 app, 40 OOS).

## 5. Axes, splits, and the frozen fit-pool contract

- Split rule (frozen, deterministic, unchanged): row `i` is test iff `(i%splitmod) in (1,3,5)`; `splitmod` 4 (G3, G2-HELDOUT) / 6 (G1, ALT). Same four axes and roles as parent (G3 primary generalization; G2-RETEST primary bound axis; G1-PRIMARY regression; G1-ALTLEX positive control). Bound counts: G3 115 (cal 39+20 / test 36+20 post-screen); G2 120 (cal 40+20 / test 40+20); G1/ALT 151 each.
- Fit-pool validity bars (frozen; failure = MEASUREMENT_INVALID/BLOCKED, §7): `N_TRAIN>=78` (2x parent 39; DESIGN arithmetic: ~104), `SELECT_APP>=20` (~35), `SELECT_OOS>=20` (60), `TRAIN∩SELECT=∅`, `(TRAIN∪SELECT)∩any-TEST=∅` (text-sha verified at runtime). No TEST row is ever read by Arm A, any clause, the screen, or the retrieval fit/select.

## 6. Metrics, gates, controls (stable identifiers; RQF-02/03/05 closed)

- Frozen constants: `FA_TARGET=0.10, COV_TARGET=0.50, PREC_TARGET=0.85, SEL_TARGET=0.80, TOK_BAND=0.60, TRI_BAND=0.75, SEED=38385040804%(2**32)`.
- Per (axis, mode): `coverage, pooled_false_accept, unknown_precision_exclusive (=OOS among resolved-then-abstained / resolved-abstained; null if none → invalidity trigger), unknown_precision_inclusive (=OOS among all non-executed / all non-executed; SENSITIVITY ONLY, never gated), selective_acc, executed, executed_oos, executed_app, abstained_resolved, unresolved_applicable`.
- PRIMARY gate (sole decision gate, pre-fixed): `pooled_false_accept<=0.10 AND coverage>=0.50 AND unknown_precision_EXCLUSIVE>=0.85`. `selection_preserved = selective_acc>=0.80` on all four axes. Cross-arm harmonization (closes RQF-05d): Arm B-OOS gates on the same exclusive-formula precision (for retrieval every scored row is decision-conditional, so exclusive==inclusive by construction; both reported).
- Controls (stable ids, all executed):
  - `PC-AXIS-G1-ALTLEX`: must remain gate-met; failure is runner-enforced MEASUREMENT_INVALID (closes RQF-06), never a science negative.
  - `NC-EXEC-ALL` (`gatefree`): must pool materially more FA than Arm A (parent test 0.2778–0.50 vs 0.0–0.10).
  - `NC-ABSTAIN-ALL`: EXECUTED (closes RQF-03; no placeholders): executes nothing → `coverage=0.0`, `pooled_false_accept=null` (no executes), `unknown_precision_exclusive=OOS_resolved/all_resolved` (informative, not 1.0 by construction). Proves the abstention instrument reaches the floor while treatment holds 0.925–1.0 coverage.
  - `CTRL-SHUFFLED-SELECTION`, `CTRL-RANDOM-ROLE`: near chance.
  - `CTRL-RANDOM-GATE`: volume-matched random abstention (parent FA 0.65–0.75).
  - `CTRL-B-LEX-ONLY` (gatefree selective_acc), `CTRL-INCUMBENT` (shipped lexical gate FA/selective_acc, incl. real `b_incumbent_kernel`=incumbent selective_acc — no placeholder).

## 7. Decision rule and product consequences (frozen cascade)

- `MEASUREMENT_INVALID` (`decision=null`) if: repaired G3-TEST liveness fails; Arm-A exclusive UP undefined on any axis; `PC-AXIS-G1-ALTLEX` fails (runner-enforced); fit-pool validity bars fail; any forbidden fallback (resubstitution/mu==0/test-touch) detected. Retrieval-OOS infeasibility is NOT invalid → `fork=RETRIEVAL_INFEASIBLE_OOS`, cascade still emits.
- Else: `G3&G2&selection_preserved → DECIDE_SHIP_TFRAME_BROAD`; `G2&selection_preserved → DECIDE_SHIP_TFRAME_SCOPED`; else `DECIDE_REQUIRE_RETRIEVAL_B`.
- Fork on `AXIS-G3-NEW` (G2 viability co-reported): `RETRIEVAL_DOMINATES_G3 / TFRAME_DOMINATES_G3 / BOTH_PASS_G3 / NEITHER_PASSES_G3 / RETRIEVAL_INFEASIBLE_OOS` (gate-level statements only; selective_acc, n_fit, cal→test gap, mu, lexicon asymmetry, and dilution caveat co-reported per RQF-05).
- Positive: BROAD retires the no-refit claim and reopens EXPERIMENTAL via a Product-lane promotion experiment; SCOPED bounds consideration to shipped surfaces; REQUIRE+BOTH_PASS/RETRIEVAL_DOMINATES keeps the retrieval-B requirement and conservative boundary strengthened. Negative: REQUIRE+TFRAME_DOMINATES/NEITHER/INFEASIBLE strengthens the structural bound but VACATES the retrieval-B requirement as specified — boundary/architecture returns to the Director; HYPOTHESIS retained with narrowed ceiling. INVALID/BLOCKED retires or parks the family per the mandate stop rule. This packet promotes nothing itself.

## 8. Design satisfiability probes (synthetic + frozen-count + parent-published evidence only; NO test outcome of THIS experiment computed in DESIGN)

**8.1 Treatment liveness, repaired scope (PASS).** Predicate evaluated on `AXIS-G3-NEW` TEST only (parent scope defect closed by construction). Non-outcome-bearing probes: (a) frozen analysis path (`comp/frame/clause_c7/is_executed/metrics`) is identical to the audited parent path that executed validly (two byte-identical canaries + scored run, exit 0); (b) repaired LIVE=True on parent-published G3-test counts (38 executed of 56; 36 applicable; 7 resolved abstentions) while the defective applicable-only predicate evaluated False — the repair flips exactly the defective trigger; (c) execute-all (`abstained_resolved=0`), abstain-all (`executed_total=0`), selector-degenerate analogues all LIVE=False; (d) calibration non-degeneracy retained (38/39 app, coverage 0.9744).

**8.2 C7 non-vacuity and zero applicable cost (PASS, parent-published structural facts quoted, not re-measured).** C7 fires on 0 applicable rows every axis; 2 G3 / 4 G2 / 2 G1 / 1 ALT OOS rows; strictly reduces G3 test FA 0.20→0.10 and G2 test FA 0.10→0.00. Zero tunable parameters.

**8.3 Decision-rule reachability (PASS).** Frozen `if/elif/else` cascade enumerated over all input combinations: all four decision outcomes (incl. null-invalid) reachable; all five fork values reachable (four gate orderings + infeasible). Liveness True/False cases as in 8.1c. G2 exclusive flip needs 11/12 vs published 10/12 — one-row margin, so H1-support and H1-falsify branches are adjacent, not empty.

**8.4 Arithmetic attainability (PASS).** G3 gate needs ≤2/20 OOS executes, ≥18/36 app executes, UP≥0.85 — attainable, non-ceiling (gatefree FA 0.45 G3 / 0.50 G2 proves headroom). Fit-pool bars attainable: N_TRAIN~104≥78, SELECT_APP~35≥20, SELECT_OOS=60≥20.

**8.5 Baseline / comparator identity (PASS).** Five arms are distinct implementations (deterministic structure ± C7; lexical incumbent; execute-all; pooled-centroid retrieval with disjoint fit/select/test); ancestors resub/embedding are non-decision identities. Comparator liveness is genuinely open: parent mu=0.0-class fits are INFEASIBLE under the new mu>0 rule, so both feasible and infeasible branches are live.

**8.6 Control sensitivity (PASS, parent values quoted + RQF-03/06 repairs).** NC-EXEC-ALL gap 0.2222–0.50; random-gate 0.65–0.75; shuffled/random near chance; abstain-all now executed at the floor (coverage 0.0) so both degeneracy directions are live; PC runner-enforced. No insensitive control.

**8.7 Measurement prerequisites (PASS).** Verified in DESIGN without outcome measurement: Python 3.12.15; runner imports stdlib-only (`argparse/hashlib/json/math/os/re/random/sys/pathlib/__future__`) + one repo-local `goal_generator` import inside `main()`; numpy/sklearn/sentence_transformers absent; `goal_generator` exposes INTENTS(20)/PARAPHRASES/NO_APPLICABLE_TEMPLATES/OOD_PARAPHRASES; every runtime-read block verified present in its exact file (G1/G2/lexicons in `38180711589/prereg.md`; `PRIOR-PARENT-BANK-TEXTS` in `38175554380/prereg.md`; G3 blocks in `38291080992/prereg.md`); fit-pool counts derived from frozen bank sizes only (139/60 → 104/35/60); no network/model/browser/credential.

**8.8 Freeze artifacts bounded (PASS).** Exactly the four mutable local interpretation dependencies in `spec.json#freeze_artifacts` (§12); runner, banks, lexicons otherwise bound via this prereg's hash (§13) + runtime self-hash.

**8.9 Self-attack (declared threats, not failures).** C7 triggers could over-abstain on unseen benign idioms (0 such rows in frozen banks; would surface as reduced coverage, not FA). G3 applicable bank structurally simple by construction — fairness test of abstention, not hard parsing; OOS half is discriminating (gatefree FA 0.45). Screen drops 5 G3 app rows; can only lower the executed denominator. Pooled-retrieval dilution biases against retrieval (disclosed §3; audit to adjudicate collapse readings).

**8.10 Empty-branch / identity / ceiling audit (PASS).** BROAD/SCOPED expected-unreachable under deterministic no-refit reproduction = predicted valid negative (bounds the resolver, keeps the boundary), not an empty branch: all outcomes arithmetically reachable and synthetically enumerated, and the live honest-fork/mu/margin measurement changes the product decision on every branch. No treatment/comparator identity (disjoint code + disjoint fitted/test data). No ceiling baseline (gatefree headroom proven). No insensitive control. No missing prerequisite. No unbound mutable artifact. Gating on inclusive would manufacture BROAD without evidence — forbidden by the falsifier. Re-running the parent resubstitution fit would repeat a confounded design — forbidden (BLOCKED).

## 9. Cost and expected information gain

- Cost: no model calls/network/browser/packages/authorship; one deterministic run over ~500 bound rows + pooled fit (~199 cal rows) + nested gate search; seconds of CPU.
- Gain: one batch decides the Director's falsifier. Predicted VALID `DECIDE_REQUIRE_RETRIEVAL_B` with an honest fork replaces the resubstitution-confounded BOTH_PASS_G3 with an interpretable bound (requirement kept if retrieval viable under mu>0; vacated-as-specified if it collapses or is infeasible, with the structural bound strengthened either way). A flipped G2 exclusive gate retires the no-refit claim and moves the boundary. A second INVALID retires the family. T-FRAME reproduction is disclosed non-evidence (RQF-04); every branch still changes the claim or product state.

## 10. Environment and EXECUTE command

- Python 3.12.15, stdlib only. EXECUTE extracts `FROZEN-RUNNER` (§13) to `raw_evidence/runner_tframe_g3_oos.py` (block bytes + exactly one trailing newline; sha256 must equal `CANONICAL-RUNNER-SHA256 = 7816fbd2660c7d67a07704a9f35e00c3331b38ebd707f9a7a5ec3187c1ed2c9b`), then:
  `python3 research/experiments/EXP-GRAPH-38385040804/raw_evidence/runner_tframe_g3_oos.py --mechanics-only` (twice; byte-identical required; TEST rows never scored) →
  `python3 research/experiments/EXP-GRAPH-38385040804/raw_evidence/runner_tframe_g3_oos.py > research/experiments/EXP-GRAPH-38385040804/raw_evidence/run_output.json`
- Determinism: fixed `SEED`; no wall-clock/RNG-dependent state beyond `random.Random(SEED)`. EXECUTE writes `result.json/report.md/provenance.json` from `run_output.json` only.

## 11. Runner identity and environment notes

- `CANONICAL-RUNNER-SHA256 = 7816fbd2660c7d67a07704a9f35e00c3331b38ebd707f9a7a5ec3187c1ed2c9b` is the sha256 of the extracted runner file (FROZEN-RUNNER block + one trailing newline), computed at DESIGN end from the frozen block bytes; EXECUTE verifies it (`runner_self_sha`) and AUDIT re-verifies with byte-identical reruns.
- `SPIDER_PREREG` env override (default: this experiment's `prereg.md`) is reserved for byte-identity checks only; the scored run uses the default.

## 12. Freeze artifacts (v2)

`spec.json#freeze_artifacts` lists the exact repository-relative mutable files whose identity can change the interpretation; each MUST be hashed into `freeze.json.artifact_hashes` and is immutable for the EXECUTE transaction:
- `research/experiments/EXP-GRAPH-38180711589/prereg.md` (G1/G2 banks + lexicons)
- `research/experiments/EXP-GRAPH-38175554380/prereg.md` (prior-bank texts)
- `research/experiments/EXP-GRAPH-38291080992/prereg.md` (G3 banks + lexicon, reuse by reference)
- `research/harness/goal_generator.py` (contamination priors)
All other inputs (runner, constants, rules) are embedded in §13 and hashed via this prereg.

## 13. FROZEN-RUNNER (the exact frozen treatment + honest comparator; hashed at freeze)

<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38385040804 (design_contract_version 2).
# Arm A = T-FRAME+ : shared deterministic lexical selection (B-LEX-STRONG, frozen)
#   + structural frame-completeness abstention clauses C1/C3/C4/C5/C6 (frozen)
#   + C7-CREATE-OBLIQUE (zero tunable parameters). Analysis logic identical to the
#   audited EXP-GRAPH-38291080992 runner lineage; constants re-frozen below.
# Arm B-OOS = B-RETRIEVAL-OOS : stdlib TF-IDF nearest-class-centroid retrieval with
#   IDF+centroids fit on pooled calibration FIT-TRAIN, gate (tau,mu) selected on
#   disjoint pooled FIT-SELECT under hard mu>0, applied frozen to every axis test.
#   Resubstitution (train==select), mu==0 gates, and any TEST-row use in fit/select
#   are FORBIDDEN and force BLOCKED/measurement-invalid (never silent reuse).
# Stdlib only. Usage: python runner_tframe_g3_oos.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, os, re, random, sys
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38385040804"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
G1G2SRC = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
G3SRC = ROOT / "research/experiments" / "EXP-GRAPH-38291080992"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

SEED = 38385040804 % (2 ** 32)
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
SEL_TARGET = 0.80
TOK_BAND = 0.60
TRI_BAND = 0.75
N_TRAIN_MIN = 78
N_SELECT_APP_MIN = 20
N_SELECT_OOS_MIN = 20

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


def arm_b_oos(train, sel_app, sel_oos, tests):
    """IDF+centroids on TRAIN app rows; gate (tau,mu>0) on SELECT; frozen apply to tests.
    Returns (result_dict, construction_flags). Any forbidden fallback -> feasible False
    with reason; caller maps persistent infeasibility to RETRIEVAL_INFEASIBLE_OOS."""
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
        return dict(feasible=False, reason="no-positive-margin-candidate-on-SELECT",
                    tau=None, mu=None, select_gate=None, n_fit_train=N,
                    n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                    classes=sorted(cent.keys()), test_gate={a: None for a in tests}), True
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
    return dict(feasible=fit_feasible, reason=None if fit_feasible else "no-feasible-mu-positive-gate-on-SELECT",
                tau=tau, mu=mu, select_gate=select_gate, n_fit_train=N,
                n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                classes=sorted(cent.keys()), test_gate=out_tests), True


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
    for nm, (app, oos, lex, sm, priors) in {
        "AXIS-G3-NEW": (banks["g3_app"], banks["g3_oos"], banks["lex_g3"], 4, banks["priors_g3"]),
        "AXIS-G2-RETEST": (banks["g2_app"], banks["g2_oos"], banks["lex_ho"], 4, banks["priors_g2"]),
        "AXIS-G1-PRIMARY": (banks["g1_app"], banks["g1_oos"], banks["lex_g1"], 6, banks["prior_full"]),
        "AXIS-G1-ALTLEX": (banks["g1_app"], banks["g1_oos"], banks["lex_alt"], 6, banks["prior_full"]),
    }.items():
        bound, flagged = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, cal=cal, test=test,
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
    test_shas = {text_sha(r["text"]) for a, v in axes.items() for r in v["test"]}
    construction_ok = (len(train) >= N_TRAIN_MIN and len(sel_app) >= N_SELECT_APP_MIN
                       and len(sel_oos) >= N_SELECT_OOS_MIN
                       and not (train_shas & sel_shas) and not ((train_shas | sel_shas) & test_shas))
    construction = dict(n_fit_train=len(train), n_select_app=len(sel_app), n_select_oos=len(sel_oos),
                        train_select_disjoint=not (train_shas & sel_shas),
                        fit_test_disjoint=not ((train_shas | sel_shas) & test_shas),
                        bars_met=construction_ok,
                        train_gids=[f"{a}:{r['gid']}" for a, r in train],
                        select_gids=[f"{a}:{r['gid']}" for _, r in sel_app] + [f"{a}:{r['gid']}" for _, r in sel_oos])

    if args.mechanics_only:
        fit_res, _ = arm_b_oos(train, sel_app, sel_oos, {})
        out = dict(status="DESIGN-MECHANICS-ONLY", experiment_id=EXP_ID, lane="graph", runner_self_sha=self_sha(),
                   axes={k: dict(bound=len(v["bound"]), flagged=v["flagged"],
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
                   liveness=dict(g3_cal_executed=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["executed"],
                                 g3_cal_unresolved=axes["AXIS-G3-NEW"]["cal_metrics"]["tframeplus"]["unresolved_applicable"]),
                   test_not_scored=True)
        print(json.dumps(out, indent=2))
        return

    for a, v in axes.items():
        v["test_metrics"] = {m: metrics(v["test"], m) for m in ("tframeplus", "tframe_frozen", "incumbent", "gatefree")}
        v["abstain_all"] = abstain_all_metrics(v["test"])
        v["shuffled_selection"] = shuffled_selection(v["test"], "tframeplus", SEED)
        v["random_role_selection"] = random_role_selection(v["test"], "tframeplus", SEED)
        v["ctrl_random_gate"] = matched_random_gate(v["test"], "tframeplus", SEED)
    tests = {a: v["test"] for a, v in axes.items()}
    fit_res, _ = arm_b_oos(train, sel_app, sel_oos, tests)

    prim = axes["AXIS-G3-NEW"]["test_metrics"]["tframeplus"]
    gates = {a: gate_met(v["test_metrics"]["tframeplus"]) for a, v in axes.items()}
    sels = {a: v["test_metrics"]["tframeplus"]["selective_acc"] for a, v in axes.items()}
    selection_preserved = all(s is not None and s >= SEL_TARGET for s in sels.values())
    g3t = axes["AXIS-G3-NEW"]["test"]
    g3t_total = len(g3t)
    g3t_abstained_resolved = sum(1 for r in g3t if r["mech"] is not None and not is_executed(r, "tframeplus"))
    live = ((0 < prim["executed"] < g3t_total)
            and (prim["executed_app"] >= 1)
            and (g3t_abstained_resolved >= 1))
    invalid_reasons = []
    if not construction_ok:
        invalid_reasons.append("fit-pool-construction-failed: N_TRAIN>=78 AND SELECT_APP>=20 AND SELECT_OOS>=20 AND train/select/test disjointness required; resubstitution fallback forbidden")
    if not live:
        invalid_reasons.append("treatment-not-live: AXIS-G3-NEW test non-degenerate execution failed (need 0 < executed_total < n_total_test AND executed_app >= 1 AND abstained_resolved >= 1)")
    for a, v in axes.items():
        if v["test_metrics"]["tframeplus"]["unknown_precision_exclusive"] is None:
            invalid_reasons.append(f"{a}: unknown_precision_exclusive undefined (no resolved abstention on test)")
    if not gates.get("AXIS-G1-ALTLEX"):
        invalid_reasons.append("positive-control-failed: PC-AXIS-G1-ALTLEX gate-met false (runner-enforced invalidity)")
    g3_gate = gates.get("AXIS-G3-NEW"); g2_gate = gates.get("AXIS-G2-RETEST")
    arm_g3 = (fit_res["test_gate"] or {}).get("AXIS-G3-NEW")
    arm_g2 = (fit_res["test_gate"] or {}).get("AXIS-G2-RETEST")
    armb_g3_met = bool(fit_res["feasible"] and arm_g3 is not None
                       and arm_g3["pooled_false_accept"] is not None and arm_g3["pooled_false_accept"] <= FA_TARGET
                       and arm_g3["coverage"] >= COV_TARGET
                       and arm_g3["unknown_precision_exclusive"] is not None and arm_g3["unknown_precision_exclusive"] >= PREC_TARGET)
    armb_g2_met = bool(fit_res["feasible"] and arm_g2 is not None
                       and arm_g2["pooled_false_accept"] is not None and arm_g2["pooled_false_accept"] <= FA_TARGET
                       and arm_g2["coverage"] >= COV_TARGET
                       and arm_g2["unknown_precision_exclusive"] is not None and arm_g2["unknown_precision_exclusive"] >= PREC_TARGET)
    if not fit_res["feasible"]:
        retrieval_fork = "RETRIEVAL_INFEASIBLE_OOS"
    elif armb_g3_met and not g3_gate:
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
               retrieval_fork=retrieval_fork,
               retrieval_oos_feasible=fit_res["feasible"], retrieval_oos_reason=fit_res["reason"],
               arm_b_oos_gate_met={"g3": armb_g3_met, "g2": armb_g2_met},
               arm_b_oos=dict(tau=fit_res["tau"], mu=fit_res["mu"],
                              mu_active=bool(fit_res["mu"] is not None and fit_res["mu"] > 0),
                              n_fit_train=fit_res["n_fit_train"], n_select_app=fit_res["n_select_app"],
                              n_select_oos=fit_res["n_select_oos"], classes=fit_res["classes"],
                              select_gate=fit_res["select_gate"], test_gate=fit_res["test_gate"]),
               fit_pool=construction,
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
                                 b_incumbent_kernel=v["test_metrics"]["incumbent"]["selective_acc"],
                                 incumbent_fa=v["test_metrics"]["incumbent"]["pooled_false_accept"],
                                 ctrl_exec_all_fa=v["test_metrics"]["gatefree"]["pooled_false_accept"],
                                 ctrl_abstain_all_cov=v["abstain_all"]["coverage"],
                                 ctrl_abstain_all_up=v["abstain_all"]["unknown_precision_exclusive"],
                                 ctrl_abstain_all_up_inclusive=v["abstain_all"]["unknown_precision_inclusive"]) for a, v in axes.items()},
               flagged={a: v["flagged"] for a, v in axes.items()})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER -->
