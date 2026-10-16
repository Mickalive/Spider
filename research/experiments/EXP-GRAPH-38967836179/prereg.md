# EXP-GRAPH-38967836179 preregistration — first-party persistence economics

## 0. Mandate, inherited state, and legacy position

- Director mandate (NEW governed, `request.json#director_mandate`, action REOPEN, target claim `C-SEMANTIC-RESOLVE`, `parent_handoff_disposition SUPERSEDE`, cognitive reset applied): measure at what write/read hit-rate economics — persistence hit rate `h(N)`, write cost `Cwrite`, miss cost `Cmiss` — persisted graph memory with the calibrated abstention boundary pays for itself end-to-end versus cold resolution on matched tasks with fully-loaded counterfactual costs (cold re-derivation, literal replay, empty-registry ablation, retrieval-shaped comparator), abstention precision/coverage held at the shipped conservative boundary, reporting the `h*(w)` locus as the denominator `C-PRODUCT-ECON` consumes. Smallest decisive batch: one matched task family with controlled recurrence at two N points. Stop trigger: non-discriminating ceiling or unmeasurable `Cwrite`/`Cmiss` → PARK, never re-parameterize the resolver.
- Parent handoff (`EXP-GRAPH-38835183404/handoff.json`) preserved as continuity evidence under SUPERSEDE (it does not override the mandate): `established` — valid v2 transaction, held-out rule emitted `tau*=0.4286`, blind gate false at `tau*` (FA 0.10-bar pass at 0.0, coverage 0.375 and UP 0.4444 fail, selective 0.1333 vs permuted 0.0667), third-family failure terminating the blind Jaccard-1NN thread; `rejected` — H1 held-out-axis blind viability for the (word-unigram Jaccard-1NN + three calibration rules) family at the gold-lexicon-conditional bound; `unknown` — the economics locus `h(N)/Cwrite/Cmiss` (this packet's question; no measurement exists yet); `do_not_assume` — all nine guards carried forward, in particular: no further tau/refit variant of Jaccard-1NN blind resolution (this packet performs NO calibration, NO refit, NO new surface: `TAU_STAR=0.4286` frozen from parent `result.json#blind_select_tau`), blind failure bounded to its mechanism-plus-calibration class, no claim elevation, no generalization beyond frozen banks, infrastructure never reads as science.
- Legacy position (`LEGACY: DISTINCT_EXTENSION`): `P2-REPLAY-COST` (pre2 artifact 4.114, sha `9687ff787f2d74460bb7006826008852f5b4416b`: matched 1.002x replay, decisions saved not runtime) never measured an `h(N)/Cwrite/Cmiss` locus with a calibrated abstention boundary and fully-loaded counterfactuals; `P2-BLIND-COMPOSITION` (artifact 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`: 3/3 unseen compositions under keyword/oracle/weak baselines) never measured cost-per-verified-success economics. The observable here (counter-instrumented break-even locus on a matched stream) was measured in neither generation. Guards inherited: matched tasks, fully-loaded counterfactual costs, never frame scripted replay as real-agent economics.
- This is not a 13th resolver variant: zero calibration parameters are fitted (SELECT scoring does not exist in the runner), the abstention boundary is held fixed, and every NEW observable is a cost/ledger quantity.

## 1. Hypotheses (single frozen texts)

- H1 (memory economics proposition): persisted exemplar memory with the frozen calibrated abstention boundary (`MEM-HIER`: hierarchical centroid-probe + within-class 1-NN resolution at `TAU_STAR=0.4286`, zero refit, predicted-class writes, §2) pays for itself end-to-end versus cold resolution on the matched G3-NEW reincluded stream when recurrence exceeds the measured break-even locus (`h2 >= h*_AO`), at matched correctness (app success-rate within 1/20 of `E-COLD`) with the abstention FA boundary held (<=0.10).
- Continuity expectations (NOT hypotheses, disclosed non-evidence): `E-COLD` reproduces the audited parent blind leg (`executed==15, fa==0.0, coverage==0.375, up_excl==20/45, selective==2/15`); flagged-TEST gid sets reproduce parent-published lists; construction bars hold (102/34/60 + disjointness). Any drift is bank/code invalidity, not science.
- Expectation from accepted evidence (NOT results): unit costs separate structurally (cold 104 REO/task fixed; hit path ~`ncls+k+2`; miss path pays probe + full scan + write overhead); recurrence separates by DESIGN label census (reverse-canonical preload covers ~0.70/1.00 of stream classes at N1=20/N2=60); correctness, FA, and centroid-routing behavior on hierarchical paths are UNMEASURED anywhere, so `ECON-PAYS` and `ECON-NEVER-PAYS` are both reachable and neither entailed. Claim ceiling: RETAIN-HYPOTHESIS-IN-ALL-VALID-BRANCHES (economics denominator evidence, never resolution-viability evidence; §7).

## 2. Treatment: MEM-HIER (frozen, no tunable parameters)

- Persisted registry maps class → exemplar token-sets, seeded from the frozen preload (TRAIN-app rows carry TRUE targets: legitimate prior distillate) and extended by within-stream writes that store PREDICTED classes (no oracle writes; oracle used only for VERIFY accounting charged uniformly at 1 REO).
- Per stream task in fixed canonical order: (1) probe: one Jaccard CMP per resident class (canonical sorted order) against the class-union token set; (2a) if top centroid score >= `TAU_STAR`: resolve by 1-NN within the top class only (strict-greater, earliest-wins determinism), second GATE on the within-class score, VERIFY; path `M` (memory), no write; (2b) else: full cold scan over the 102 TRAIN exemplars, GATE, VERIFY, WRITE (2 REO) under the predicted class iff executed; path `C` (cold fallback). No re-fallback, no repair, no refit.
- Structural recurrence `h_task = 1[target class resident BEFORE the task]` (preload ∪ earlier stream writes keyed by stored class). Behavioral hit = `path==M AND executed` (diagnostic only; `h*` uses structural `h` per the mandate definition).
- Two preload points by one pre-registered canonical rule (no TEST-label input): `P-N1` = last N1=20 rows of canonical TRAIN-app order, `P-N2` = last N2=60 (reverse-canonical = recurrence-maximizing canonical direction; forward order yields `h=0` at both points per DESIGN census and is declined on record). Measured `h1/h2` are the dynamic stream means (preload ∪ stream-write residence).

## 3. Comparators (frozen; matched tasks, fully-loaded costs)

- `E-COLD` (cold re-derivation): full-TRAIN-pool (102) unigram-Jaccard 1-NN at `TAU_STAR`, no persistence, no writes; per-task cost exactly 104 REO (102 CMP + GATE + VERIFY). Identical mechanics and gate to the treatment, differing ONLY by persistence — the strongest fair baseline, never a strawman.
- `E-EMPTY` (empty-registry ablation): MEM-HIER machinery with empty preload; only stream writes accumulate. Separates preload benefit from write benefit.
- `E-REPLAY` (literal replay): exact-text cache over preload + stream-written texts; hit = text membership (LOOKUP + VERIFY, no scan, executed with stored prediction); miss = cold scan + GATE + VERIFY + WRITE(2) if executed.
- `E-RETR` (retrieval-shaped): stdlib TF-IDF uni+bigram nearest-class-centroid with IDF+centroids fit on TRAIN-app only and the frozen gate (`TAU_B=0.4156, MU_B=0.0005`); per-task `ncent` cosine CMPs + 2 GATEs + VERIFY; never writes. Mechanism distance from MEM-HIER: sublinear-tf*IDF weighting vs raw sets; uni+bigram vs unigram-only; per-class L2 centroid vs exemplar 1-NN; cosine vs Jaccard; (tau,mu) margin gate vs single-tau; global comparison vs hierarchical short-circuit. Shared by design: the SAME TRAIN rows (mechanism-given-data ablation).
- Gold correctness anchor (reference only, never cost-ranked): parent `gold_g3_reincl` vector quoted (FA 0.10/cov 1.0/UP 1.0/selective 1.0); excluded from cost ranking as lexicon-carried.

## 4. Banks, priors, screen (reuse by reference; no new collection)

- Identical frozen sources as the parent packet: `GOAL-BANK-G3`/`OOS-BANK-G3` from `EXP-GRAPH-38291080992/prereg.md`; `GOAL-BANK-G1`/`OOS-BANK-G1`/`GOAL-BANK-G2`/`OOS-BANK-G2` from `EXP-GRAPH-38180711589/prereg.md`; `PRIOR-PARENT-BANK-TEXTS` from `EXP-GRAPH-38175554380/prereg.md`; `INTENTS/PARAPHRASES/NO_APPLICABLE_TEMPLATES/OOD_PARAPHRASES` from `research/harness/goal_generator.py` (read-only import). No lexicon block is read at any stage (lexicon-free packet; econ arms use text+target pairs only).
- Row construction, splitmods (G3 4 / G2 4 / G1 6), screen (`TOK_BAND=0.60, TRI_BAND=0.75` vs the same priors), and fit-pool formulas are byte-equivalent to the parent runner minus gold-analysis fields (no `mech`/clauses computed; rows carry gid/text/app/target/split only).
- Forbidden (violation = BLOCKED or MEASUREMENT_INVALID, never silent reuse): any tau/gate/clause/centroid fitting on any pool; any new surface, bank, or lexicon; any TEST-row use outside the single scored stream pass; resubstitution of ancestor values for live legs.

## 5. Stream, N points, fit bars (frozen)

- Scored stream `S` = AXIS-G3-NEW `test_reincl` (screened TEST + flagged TEST) in canonical bound order (60 rows: 40 app + 20 OOS per the audited parent; exact counts re-verified by the runner, never assumed).
- Fit bars (failure = MEASUREMENT_INVALID): `N_TRAIN==102, SELECT_APP==34, SELECT_OOS==60`; `TRAIN ∩ SELECT = ∅`; `(TRAIN ∪ SELECT) ∩ (screened TEST ∪ reincluded TEST) = ∅` at exact text-sha over all three axes. SELECT rows are never scored (no SELECT machinery exists in the runner).
- Flagged-TEST gid tripwires (failure = INVALID): G3 `["app_026","app_030","app_036","app_076"]`, G1 six gids, G2 empty — parent-published values.
- N points: N1=20, N2=60 via the §2 preload rule. Separation premise from DESIGN label census (counts only, no resolver scoring): reverse-canonical preload covers ~0.70 (N1) / ~1.00 (N2) of the 20 stream classes; forward order covers 0.00 at every N (declined). Separation bar `h2-h1 >= 1/20` runner-enforced (else INCONCLUSIVE points-collapsed).

## 6. Metrics, gates, controls (stable identifiers)

- Cost unit REO, VAR-LIT primary (all integers): CMP=1, GATE=1, VERIFY=1, WRITE=2, LOOKUP=1. M-path task = `probe_n + k + 2 + 1`; C-path = `probe_n + 102 + 1 + 1 (+2 if executed)`; cold = 104; replay-hit = 2; replay-miss = 104 (+2); retr = `ncent + 2 + 1`. VAR-MAN sensitivity: CMP costs `len(q)+len(p)` token-volume units; WRITE costs `1+len(new set)`; GATE/VERIFY/LOOKUP cost 1.
- Per-arm ledger metrics: `M-TOTAL-{COLD,MEM1,MEM2,EMPTY,REPLAY,RETR}` (LIT totals), `M-CPS-{arm}` = total/verified (verified = app-correct + oos-abstained; null iff zero), `M-SUCCRATE-{arm}` (app-correct/40), `M-FA-{arm}` (executed-oos/20), coverage/UP/selective (exclusive==inclusive by construction for memory arms).
- Economics metrics (Fractions, exact): `M-H-N1/M-H-N2` (dynamic structural recurrence means), `M-BEH-HIT-N1/N2` (behavioral memory-path-executed fractions), `M-E-COLD` (=104), `M-E-WARM-N1/N2` (M-path mean cost; null iff no M-path), `M-CWRITE` (=2), `M-CMISS` (=E_cold), `M-W-OVER-COLD` (w), `M-FSTAR-N2` (f* or DIVERGENT), `M-HSTAR-AO-N2/M-HSTAR-PR-N2/M-HSTAR-AO-N1` (loci; AO amortizes all stream writes over stream tasks, PR amortizes distinct stream-written keys — preload keys are sunk prior distillate, excluded from both write counts), `M-N-WRITES-*/M-N-KEYS-*/M-N-NEWKEYS-*`, `M-MISLABEL-N1/N2`, MAN-locus twins (`MAN-*`), `M-TRANSFER-RELPRED` (N1 totals predicted from N2-pool unit costs; diagnostic).
- Controls: `PC-ALGEBRA` (toy §14: f*=1, h*=1/2, predicted=40; gating); `NC-DIVERGENT` (swapped-cost toy E 10/12 must classify DIVERGENT; gating); `NC-CONVENTION` (skewed-write toy must yield AO=3/4 vs PR=1/2 with inequality; gating); `PC-COLD-REPRO` (E-COLD five values == §1 tripwire within 1e-9; gating); `NC-EMPTY-RESIDENT` (E-EMPTY task-0 resident==0 and probe_n==0; gating); `CTRL-LITERAL-SUBSET` (every replay text-hit has its stored class resident at hit time... precisely: hit text was written earlier, hence its stored class is resident; violation = INVALID); `CTRL-MICRO-LIVEPATH` (synthetic identical-text micro probe must take the M-path executed; gating instrument-liveness proof, no bank data); `CTRL-H-SEPARATION` (h2-h1>=1/20 else points-collapsed INCONCLUSIVE).

## 7. Decision rule and product consequences (frozen cascade)

- Runner evaluates (exact integer/Fraction arithmetic; floats never gate): INVALID (`status=MEASUREMENT_INVALID, outcome=NOT_APPLICABLE, decision=null`) on any §5 bar/tripwire failure, any gating-control failure, `h2==0`, MEM-N2 writes==0, self-sha mismatch, or non-byte-identical canaries. BLOCKED (`status=BLOCKED, outcome=NOT_APPLICABLE`) iff `Cwrite==0 or E_cold==0`. CEILING-PARK (`status=COMPLETE, outcome=NOT_APPLICABLE, decision=CEILING-PARK`) iff all five arms pairwise-equal in totals AND success rates (mandate stop trigger). Else: `E_warm_N2` null → `COMPLETE/FALSIFIES, NEVER-PAYS reason=no-memory-path`. Else `h2-h1<1/20` → `COMPLETE/INCONCLUSIVE reason=points-collapsed`. Else either CPS null → `COMPLETE/FALSIFIES, NEVER-PAYS reason=no-verified-success`. Else `ECON-PAYS` (`COMPLETE/SUPPORTS`) iff the conjunction holds: `total_mem2<total_cold` AND `cps_mem2<cps_cold` (cross-multiplied) AND `(app_ok_mem2-app_ok_cold)>=-2` AND `exo_mem2<=2` (FA<=1/10) AND `h*_AO(N2)<=h2` (DIVERGENT fails here as `structural-divergent`). Else `COMPLETE/FALSIFIES, NEVER-PAYS` with first-true reason in `[structural-divergent, boundary-violation, accuracy-regression, locus-above-range, cost-regression]` and every failing conjunct listed in `reason_detail`.
- Transcription rule: EXECUTE copies `run_output.json` into `result.json` per the metric/control identifiers above (Fractions as `{num,den,float}`), sets `status/outcome` from `econ_status/econ_outcome`, `metrics/decisions` verbatim, and writes `report.md/provenance.json` from `run_output.json` only. No renaming, no extra labels.
- Consequences: PAYS → quantitative admission policy + first-party denominator for C-PRODUCT-ECON (both conventions + MAN sensitivity travel in the handoff); NEVER-PAYS → calibrated-memory path falsified-in-setting, budget to compilation-bypass/adapter, keep shipped boundary; INCONCLUSIVE/PARK/BLOCKED → park without resolver re-parameterization. Claim ceiling: RETAIN-HYPOTHESIS-IN-ALL-VALID-BRANCHES for C-SEMANTIC-RESOLVE (verdict text records the locus; no VALIDATED/REJECTED/PRODUCT_CORE from economics evidence). This packet promotes nothing.

## 8. Design satisfiability probes (accepted evidence + read-only counts only; the frozen runner was NEVER executed in DESIGN — not even mechanics-only)

- **8.1 Measurement prerequisites (PASS).** Python 3.12.15 verified; `import numpy` raises ModuleNotFoundError (stdlib-only); the four freeze-artifact files exist with DESIGN shas exactly equal to the parent `freeze.json` artifact hashes (`5a64e90d…/dc90bf71…/5a9cc119…/cb5218de…`, verified by `sha256sum`); bank block sizes read without scoring: GOAL/OOS banks 80/40 (G3), 120/40 (G1), 80/40 (G2); no network/model/browser/credential anywhere in the design. B3 explicitly NOT_APPLICABLE (counter-only REO economics).
- **8.2 Label census (counts only, no resolver scoring, no gate evaluation).** 20 stream classes (drivers/fares/routes/stops/vehicles × CRUD — a genuinely new surface vs TRAIN families); all 40 stream app-targets occur in the TRAIN inventory; reverse-canonical preload covers ~0.70 (N1=20) / ~1.00 (N2=60) of stream classes while forward order covers 0.00 at every N (hence the §2 rule). Census used `[a-z0-9]+` tokenization and is therefore approximate (±rows); every decision uses EXECUTE-measured values only.
- **8.3 Cost-scale separation (PASS, arithmetic).** Cold task cost is the constant 104 REO; M-path cost is `probe_n+k+3` with `probe_n<=~62` resident classes; C-path pays probe + 104 + write overhead. `Cwrite=2>0`, `E_cold=104>0` structurally, so the BLOCKED branch is a declared guard with a provably-present scale; CEILING-PARK requires five-way integer equality against these separated constructions (drift guard class).
- **8.4 Treatment liveness (PASS).** Preload seeds ~14/40 resident classes (census); the parent full-pool leg executed 15/60 stream rows proving resolution activity; runner liveness bars (MEM-N2 writes>0 else INVALID; micro M-path self-test else INVALID) separate instrument death (INVALID) from genuine non-engagement (valid NEVER-PAYS).
- **8.5 Baseline/comparator identity (PASS).** Five distinct implementations over identical rows in identical order (cold full-scan vs hierarchical probe+within-class vs exact-membership vs centroid-global vs empty-start); disjoint fitted statistics (none fitted); same-rows-by-ablation; replay-subset and empty-resident relations pre-declared and gated.
- **8.6 Control sensitivity (PASS).** Every gating control can fire: toys assert exact rationals (any code deviation → INVALID); PC-COLD-REPRO pins five published values; NC-DIVERGENT exercises the `g<=0` branch on synthetic costs; micro self-test exercises the M-path without bank data.
- **8.7 Prerequisite ordering (PASS).** Stronger than SELECT-before-TEST: the runner contains no SELECT scoring and no fitting of any kind; `TAU_STAR/TAU_B/MU_B` are numeric constants transcribed from audited packets, never computed.
- **8.8 Mutable artifacts bound (PASS).** Exactly the four listed files; everything else (constants, toys, tripwires, rules) is embedded in §13 and hashed via this prereg.
- **8.9 Self-attack (declared threats, not failures).** (i) Locus-condition weakness (DISCLOSED): `Cwrite=2` vs `E_cold=104` makes `h*` small by construction, so the locus conjunct rarely binds — the test bites on totals/CPS/correctness/FA instead; the locus REMAINS the reported product (admission policy), not the binding constraint, and this asymmetry is stated so a PAYS is read as cost/correctness evidence, not locus drama. (ii) Small success numerators (DISCLOSED): cold-equivalent app-correct ≈2/40 expected; the dual totals+CPS agreement plus the ±2-row δ gate keep the comparison honest; MAN and per-task secondaries travel as diagnostics. (iii) E-COLD outcome entailment (DISCLOSED, handled): the cold correctness vector is parent-published, so only costs/locus are NEW — the information-gain claim (§9) rests solely on never-measured ledger quantities. (iv) Routing-confound asymmetry (DISCLOSED): MEM correctness may differ from COLD through centroid misrouting — that is the experiment (persistence changes resolution), gated by δ/FA, never smoothed. (v) Post-hoc-knowledge contamination (MITIGATED): DESIGN knows parent blind aggregates; mitigation is structural — no fitted parameter exists to steer, and every gating tripwire is an equality the runner must satisfy, not a direction DESIGN could tune. (vi) Replay-degeneracy (PRE-HANDLED): ~zero replay hits is a valid control outcome proving treatment≠replay, never invalidity. (vii) Re-running any parent tau/refit design would be DUPLICATE — not done (no calibration exists here).
- **8.10 Empty-branch / identity / ceiling audit (PASS — active disproof attempt recorded).** Attacked and cleared: (i) no empty decision branch — synthetic enumeration reaches PAYS/NEVER-PAYS(×7 reasons)/INCONCLUSIVE/PARK/BLOCKED/INVALID; PAYS requires five jointly-open conjuncts; NEVER-PAYS has live cost, correctness, boundary, locus, and engagement failures; (ii) no treatment/comparator identity — §8.5 plus gated subset/resident relations; (iii) no ceiling baseline — cold at 15/60 executed with selective 2/15 is not a ceiling, and counters separate by construction; (iv) no insensitive control — §8.6; (v) no missing prerequisite — §8.1/8.7 (B3 explicitly excused); (vi) no unbound mutable artifact — §8.8/§12; (vii) no pre-2.0 outcome identity — §0 legacy position (economics locus never measured in either generation).

## 9. Cost and expected information gain

- Cost: no model calls/network/browser/packages/authorship; one deterministic run over ~380 bank rows (frozen screen) + five ledger arms over the 60-row stream + retrieval centroid fit on 102 rows + three synthetic toys; seconds of CPU.
- Gain: the first measured `h(N)/Cwrite/Cmiss/f*/h*(w)` locus with fully-loaded counterfactuals on matched tasks. PAYS and NEVER-PAYS both change Graph/Product budget and admission decisions per the mandate counterfactual (denominator for C-PRODUCT-ECON vs falsified-in-setting redirect); PARK/BLOCKED/INCONCLUSIVE stop spend without resolver churn. Screened/bank/cold-reproduction legs are disclosed non-evidence; NEW evidence is every ledger quantity, the locus under both conventions, and the MAN sensitivity.

## 10. Environment and EXECUTE command

- Python 3.12.15, stdlib only (`argparse/hashlib/json/math/re/sys/fractions/pathlib` + one read-only `goal_generator` import for priors). EXECUTE extracts `FROZEN-RUNNER-ECON` (§13) to `raw_evidence/runner_econ.py` (block bytes + exactly one trailing newline; sha256 must equal `CANONICAL-RUNNER-SHA256 = e36e95b40f34dc7acf01c2eb2847868e0b345264cd0e0fecd3e2f7440e3fe237`), then:
  `python3 research/experiments/EXP-GRAPH-38967836179/raw_evidence/runner_econ.py --mechanics-only` (twice; byte-identical required; stream arms never scored) →
  `python3 research/experiments/EXP-GRAPH-38967836179/raw_evidence/runner_econ.py > research/experiments/EXP-GRAPH-38967836179/raw_evidence/run_output.json`
- Determinism: no RNG of any kind (fixed canonical orders; strict-greater earliest-wins ties). EXECUTE transcribes `result.json/report.md/provenance.json` from `run_output.json` only, preserving §6 identifiers and the §7 transcription rule.

## 11. Runner identity and environment notes

- `CANONICAL-RUNNER-SHA256 = e36e95b40f34dc7acf01c2eb2847868e0b345264cd0e0fecd3e2f7440e3fe237` is the sha256 of the extracted runner file (FROZEN-RUNNER-ECON block + one trailing newline), computed at DESIGN end from the frozen block bytes (hash computation + `py_compile` syntax check only; the runner was never executed in DESIGN). EXECUTE verifies the extracted file hash (`runner_self_sha`) and AUDIT re-verifies with byte-identical reruns plus an independent ledger reimplementation. No ancestor runner is reused: this is a new economics instrument on frozen banks (LEGACY DISTINCT_EXTENSION, §0).

## 12. Freeze artifacts (v2)

- `research/experiments/EXP-GRAPH-38180711589/prereg.md` (G1/G2 banks; DESIGN sha `5a64e90da4d1c13b4a290b988cc6096838119d09869abd69512d095cd9318cb0`, matches parent freeze hash)
- `research/experiments/EXP-GRAPH-38175554380/prereg.md` (prior-bank texts; DESIGN sha `dc90bf71ed03a2329b641d46c1f4f70a53dbeef95ebd6d688645f697868aff9b`, matches parent freeze hash)
- `research/experiments/EXP-GRAPH-38291080992/prereg.md` (G3 banks, reuse by reference; DESIGN sha `5a9cc1190674ffa5a8e6d604f6735ae6a9e2e27ffc9358c82d263f51b43d5735`, matches parent freeze hash)
- `research/harness/goal_generator.py` (contamination priors; DESIGN sha `cb5218de6a992cf29e26eee8fd5be4b4d7a50084ac3b885587a8ee1da20ace5f`, matches parent freeze hash)
All other inputs (constants, frozen taus, toy expectations, tripwire values) are embedded in §13 and hashed via this prereg.

## 13. FROZEN-RUNNER-ECON (the exact frozen economics instrument; hashed at freeze)

<!-- BEGIN FROZEN-RUNNER-ECON -->
#!/usr/bin/env python3
# FROZEN RUNNER-ECON for EXP-GRAPH-38967836179 (design_contract_version 2).
# First-party persistence economics on the frozen banks. Stdlib only. No RNG.
# REO cost model (VAR-LIT primary, integers): CMP=1 per pairwise Jaccard,
# GATE=1 per threshold compare, VERIFY=1 per oracle check, WRITE=2
# (token-build + insert), LOOKUP=1 per exact-text membership test.
# VAR-MAN sensitivity: CMP costs len(q)+len(p); WRITE costs 1+len(new set).
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from fractions import Fraction
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38967836179"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
G1G2SRC = ROOT / "research/experiments" / "EXP-GRAPH-38180711589"
G3SRC = ROOT / "research/experiments" / "EXP-GRAPH-38291080992"
GRANDPARENT = ROOT / "research/experiments" / "EXP-GRAPH-38175554380"

TAU_STAR = 0.4286
TAU_B = 0.4156
MU_B = 0.0005
FA_TARGET = 0.10
TOK_BAND = 0.60
TRI_BAND = 0.75
N_TRAIN_FROZEN = 102
N_SELECT_APP_FROZEN = 34
N_SELECT_OOS_FROZEN = 60
N1 = 20
N2 = 60

EXPECTED_FLAGGED_TEST = {
    "AXIS-G3-NEW": ["app_026", "app_030", "app_036", "app_076"],
    "AXIS-G2-RETEST": [],
    "AXIS-G1-PRIMARY": ["app_004", "app_052", "app_076", "app_100", "oos_024", "oos_026"],
}
COLD_TRIP = dict(executed=15, fa=0.0, coverage=0.375, up_excl=20.0 / 45.0, selective=2.0 / 15.0)


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
        raise SystemExit("missing block %s" % name)
    return m.group(1)


def jlines(block: str):
    return [json.loads(l) for l in block.splitlines() if l.strip()]


def tokens(s: str):
    return re.findall(r"[a-z]+", s.lower())


def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def trigrams(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i + 3] for i in range(len(x) - 2)}


def text_sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def target_of(goal):
    return "mech_%s_%s" % (goal["family"], goal["op"].lower())


def _blind_token_set(text):
    return set(tokens(text))


def blind_jac_predict(tok_sets_targets, text):
    q = _blind_token_set(text)
    best_cls, best_s = None, -1.0
    for toks, cls in tok_sets_targets:
        inter = len(q & toks)
        union = len(q | toks)
        s = inter / union if union else 0.0
        if s > best_s:
            best_s, best_cls = s, cls
    return best_cls, best_s


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


def build_rows(app, oos, sm, priors):
    rows = []
    for i, g in enumerate(app):
        rows.append(dict(gid="app_%03d" % (i + 1), text=g["text"], app=1,
                         target=target_of(g), split=((i % sm) in (1, 3, 5))))
    for i, g in enumerate(oos):
        rows.append(dict(gid="oos_%03d" % (i + 1), text=g["text"], app=0,
                         target=None, split=((i % sm) in (1, 3, 5))))
    flagged = []
    for r in rows:
        tj = tokens(r["text"])
        tg = trigrams(r["text"])
        hit = False
        for p in priors:
            if jaccard(tj, tokens(p)) >= TOK_BAND or jaccard(tg, trigrams(p)) >= TRI_BAND:
                hit = True
                break
        if hit:
            flagged.append(r["gid"])
    fs = set(flagged)
    bound = [r for r in rows if r["gid"] not in fs]
    flagged_test = [r for r in rows if r["gid"] in fs and r["split"]]
    return bound, flagged, flagged_test


def load_inputs():
    g3_text = (G3SRC / "prereg.md").read_text(encoding="utf-8")
    g3_app = jlines(extract_block(g3_text, "GOAL-BANK-G3"))
    g3_oos = jlines(extract_block(g3_text, "OOS-BANK-G3"))
    g1g2_text = (G1G2SRC / "prereg.md").read_text(encoding="utf-8")
    g1_app = jlines(extract_block(g1g2_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(g1g2_text, "OOS-BANK-G1"))
    g2_app = jlines(extract_block(g1g2_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(g1g2_text, "OOS-BANK-G2"))
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
    return dict(g3_app=g3_app, g3_oos=g3_oos, g1_app=g1_app, g1_oos=g1_oos,
                g2_app=g2_app, g2_oos=g2_oos, prior_full=prior_full,
                priors_g3=priors_g3, priors_g2=priors_g2)


def build_pools(inp):
    axes = {}
    spec = {
        "AXIS-G3-NEW": (inp["g3_app"], inp["g3_oos"], 4, inp["priors_g3"]),
        "AXIS-G2-RETEST": (inp["g2_app"], inp["g2_oos"], 4, inp["priors_g2"]),
        "AXIS-G1-PRIMARY": (inp["g1_app"], inp["g1_oos"], 6, inp["prior_full"]),
    }
    for nm, (app, oos, sm, priors) in spec.items():
        bound, flagged, flagged_test = build_rows(app, oos, sm, priors)
        cal = [r for r in bound if not r["split"]]
        test = [r for r in bound if r["split"]]
        axes[nm] = dict(bound=bound, flagged=flagged, flagged_test=flagged_test,
                        cal=cal, test=test, test_reincl=test + flagged_test)
    pool_app, pool_oos = [], []
    for nm in ("AXIS-G1-PRIMARY", "AXIS-G2-RETEST", "AXIS-G3-NEW"):
        for r in axes[nm]["cal"]:
            (pool_app if r["app"] else pool_oos).append((nm, r))
    train, sel_app = [], []
    for i, item in enumerate(pool_app):
        (sel_app if (i % 4 == 3) else train).append(item)
    return axes, train, sel_app, pool_oos


def fit_centroids(train):
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
    for cls in list(cent):
        v = cent[cls]
        n = math.sqrt(sum(y * y for y in v.values())) or 1.0
        cent[cls] = {f: x / n for f, x in v.items()}
    return idf, cent


def class_union(exs):
    u = set()
    for t in exs:
        u |= t
    return u


def summarize(stream, recs):
    n_app = sum(1 for r in stream if r["app"])
    n_oos = len(stream) - n_app
    exa = exo = app_ok = ab = abRo = 0
    for r, d in zip(stream, recs):
        if d["executed"]:
            if r["app"]:
                exa += 1
                if d["pred"] == r["target"]:
                    app_ok += 1
            else:
                exo += 1
        else:
            ab += 1
            if not r["app"]:
                abRo += 1
    fa = exo / n_oos if n_oos else None
    cov = exa / n_app if n_app else 0.0
    up = abRo / ab if ab else None
    sel = app_ok / exa if exa else None
    succ = app_ok / n_app if n_app else 0.0
    verified = app_ok + abRo
    return dict(n_app=n_app, n_oos=n_oos, executed=exa + exo, executed_app=exa,
                executed_oos=exo, abstained=ab, fa=fa, coverage=cov, up_excl=up,
                selective=sel, app_ok=app_ok, succ_rate=succ, verified=verified)


def run_cold(pool_pairs, stream):
    n_pool = len(pool_pairs)
    recs = []
    tot = 0
    man = 0
    for r in stream:
        pred, score = blind_jac_predict(pool_pairs, r["text"])
        executed = score >= TAU_STAR
        tot += n_pool + 1 + 1
        q = _blind_token_set(r["text"])
        mv = sum(len(q) + len(t) for t, _ in pool_pairs)
        man += mv + 1 + 1
        recs.append(dict(pred=pred if executed else None, executed=executed))
    return dict(recs=recs, total=tot, man=man)


def run_mem(pool_pairs, stream, preload_rows):
    mem = {}
    for _, r in preload_rows:
        mem.setdefault(r["target"], []).append(_blind_token_set(r["text"]))
    n_pool = len(pool_pairs)
    recs = []
    tot = 0
    man = 0
    writes = 0
    w_man = 0
    new_keys = 0
    keys_ever = set(mem.keys())
    m_path = 0
    m_cost = 0
    m_man = 0
    mislabeled = 0
    h_num = 0
    for r in stream:
        resident = set(mem.keys())
        h_task = 1 if (r["app"] and r["target"] in resident) else 0
        h_num += h_task
        q = _blind_token_set(r["text"])
        top_cls, top_s = None, -1.0
        probe_n = 0
        probe_mv = 0
        for cls in sorted(resident):
            u = class_union(mem[cls])
            inter = len(q & u)
            union = len(q | u)
            s = inter / union if union else 0.0
            probe_n += 1
            probe_mv += len(q) + len(u)
            if s > top_s:
                top_s, top_cls = s, cls
        if top_s >= TAU_STAR:
            best_s = -1.0
            k = 0
            kv = 0
            for toks in mem[top_cls]:
                inter = len(q & toks)
                union = len(q | toks)
                s = inter / union if union else 0.0
                k += 1
                kv += len(q) + len(toks)
                if s > best_s:
                    best_s = s
            executed = best_s >= TAU_STAR
            pred = top_cls if executed else None
            tot += probe_n + k + 2 + 1
            man += probe_mv + kv + 2 + 1
            m_path += 1
            m_cost += probe_n + k + 3
            m_man += probe_mv + kv + 3
            recs.append(dict(pred=pred, executed=executed, path="M", h=h_task, wrote=False))
        else:
            pred_c, score_c = blind_jac_predict(pool_pairs, r["text"])
            executed = score_c >= TAU_STAR
            pred = pred_c if executed else None
            kv = len(q) * 0
            for toks, _ in pool_pairs:
                kv += len(q) + len(toks)
            tot += probe_n + n_pool + 1 + 1
            man += probe_mv + kv + 1 + 1
            wrote = False
            if executed:
                if pred not in resident:
                    new_keys += 1
                mem.setdefault(pred, []).append(q)
                keys_ever.add(pred)
                writes += 1
                wrote = True
                tot += 2
                man += 1 + len(q)
                w_man += 1 + len(q)
                if r["app"] and pred != r["target"]:
                    mislabeled += 1
            recs.append(dict(pred=pred, executed=executed, path="C", h=h_task, wrote=wrote))
    return dict(recs=recs, total=tot, man=man, writes=writes, w_man=w_man, keys=len(keys_ever),
                new_keys=new_keys, m_path=m_path, m_cost=m_cost, m_man=m_man, mislabeled=mislabeled, h_num=h_num)


def run_replay(pool_pairs, stream, preload_rows):
    mem_texts = {}
    for _, r in preload_rows:
        mem_texts[r["text"]] = r["target"]
    n_pool = len(pool_pairs)
    recs = []
    tot = 0
    man = 0
    writes = 0
    hits = 0
    for r in stream:
        if r["text"] in mem_texts:
            pred = mem_texts[r["text"]]
            tot += 1 + 1
            man += 1 + 1
            hits += 1
            recs.append(dict(pred=pred, executed=True, behav_hit=1))
        else:
            pred_c, score_c = blind_jac_predict(pool_pairs, r["text"])
            executed = score_c >= TAU_STAR
            pred = pred_c if executed else None
            q = _blind_token_set(r["text"])
            kv = sum(len(q) + len(t) for t, _ in pool_pairs)
            tot += n_pool + 1 + 1
            man += kv + 1 + 1
            if executed:
                mem_texts[r["text"]] = pred
                writes += 1
                tot += 2
                man += 1 + len(q)
            recs.append(dict(pred=pred, executed=executed, behav_hit=0))
    return dict(recs=recs, total=tot, man=man, writes=writes, hits=hits)


def run_retr(idf, cent, stream):
    classes = sorted(cent.keys())
    ncent = len(classes)
    recs = []
    tot = 0
    man = 0
    for r in stream:
        v = _vec(_feats(r["text"]), idf)
        sims = sorted(((_cos(v, c), cls) for cls, c in cent.items()), reverse=True)
        top = sims[0][0] if sims else 0.0
        margin = (sims[0][0] - sims[1][0]) if len(sims) > 1 else 1.0
        executed = (top >= TAU_B and margin >= MU_B)
        pred = sims[0][1] if executed else None
        tot += ncent + 2 + 1
        man += ncent + 2 + 1
        recs.append(dict(pred=pred, executed=executed))
    return dict(recs=recs, total=tot, man=man, ncent=ncent)


def micro_selftest():
    mem = {"mech_probe_ok": [_blind_token_set("alpha beta gamma")]}
    q = _blind_token_set("alpha beta gamma")
    u = class_union(mem["mech_probe_ok"])
    s = len(q & u) / len(q | u)
    if not (s == 1.0 and s >= TAU_STAR):
        return False
    best_s = -1.0
    for toks in mem["mech_probe_ok"]:
        ss = len(q & toks) / len(q | toks)
        if ss > best_s:
            best_s = ss
    return bool(best_s == 1.0 and best_s >= TAU_STAR)


def toy_algebra():
    Ec = Fraction(10)
    Ew = Fraction(4)
    Cw = Fraction(6)
    W = 2
    T = 4
    h = Fraction(1, 2)
    f = Cw / (Ec - Ew)
    hs = f * Fraction(W, T)
    pred = T * (h * Ew + (1 - h) * Ec) + W * Cw
    return dict(f=f, hstar=hs, pred=pred)


def toy_divergent():
    Ec = Fraction(10)
    Ew = Fraction(12)
    return dict(divergent=not (Ew < Ec))


def toy_convention():
    Ec = Fraction(10)
    Ew = Fraction(4)
    Cw = Fraction(6)
    W = 3
    K = 2
    T = 4
    f = Cw / (Ec - Ew)
    return dict(ao=f * Fraction(W, T), pr=f * Fraction(K, T))


def fr(x):
    if x is None:
        return None
    return dict(num=x.numerator, den=x.denominator, float=float(x))


def economics(pool_n, stream_n, h_frac, e_cold, e_warm, cwrite, writes, keys):
    if e_warm is None or not (e_warm < e_cold):
        return dict(divergent=True, f=None, h_ao=None, h_pr=None, pred_total=None)
    f = cwrite / (e_cold - e_warm)
    h_ao = f * Fraction(writes, stream_n)
    h_pr = f * Fraction(keys, stream_n)
    pred = stream_n * ((1 - h_frac) * e_cold + h_frac * e_warm) + writes * cwrite
    return dict(divergent=False, f=f, h_ao=h_ao, h_pr=h_pr, pred_total=pred)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    out = dict(exp_id=EXP_ID, runner_self_sha=self_sha(), mechanics_only=bool(args.mechanics_only))
    invalid = []
    inp = load_inputs()
    axes, train, sel_app, pool_oos = build_pools(inp)
    train_shas = {text_sha(r["text"]) for _, r in train}
    sel_shas = {text_sha(r["text"]) for _, r in sel_app} | {text_sha(r["text"]) for _, r in pool_oos}
    test_union_shas = {text_sha(r["text"]) for a, v in axes.items() for r in v["test"] + v["flagged_test"]}
    construction_ok = (len(train) == N_TRAIN_FROZEN and len(sel_app) == N_SELECT_APP_FROZEN
                       and len(pool_oos) == N_SELECT_OOS_FROZEN
                       and not (train_shas & sel_shas) and not ((train_shas | sel_shas) & test_union_shas))
    out["construction"] = dict(n_fit_train=len(train), n_select_app=len(sel_app), n_select_oos=len(pool_oos),
                               train_select_disjoint=not (train_shas & sel_shas),
                               fit_test_disjoint=not ((train_shas | sel_shas) & test_union_shas),
                               bars_met=construction_ok)
    if not construction_ok:
        invalid.append("fit-pool-construction-failed")
    trip_ok = True
    trip_detail = {}
    for nm, want in EXPECTED_FLAGGED_TEST.items():
        got = sorted(r["gid"] for r in axes[nm]["flagged_test"])
        ok = (got == sorted(want))
        trip_detail[nm] = dict(ok=ok, got=got, want=sorted(want))
        trip_ok = trip_ok and ok
    out["flagged_tripwire"] = trip_detail
    if not trip_ok:
        invalid.append("flagged-gid-tripwire-failed")
    try:
        ta = toy_algebra()
        toy_a_ok = (ta["f"] == 1 and ta["hstar"] == Fraction(1, 2) and ta["pred"] == 40)
    except Exception:
        toy_a_ok = False
    try:
        toy_d_ok = bool(toy_divergent()["divergent"])
    except Exception:
        toy_d_ok = False
    try:
        tc = toy_convention()
        toy_c_ok = (tc["ao"] == Fraction(3, 4) and tc["pr"] == Fraction(1, 2) and tc["ao"] != tc["pr"])
    except Exception:
        toy_c_ok = False
    out["toys"] = dict(pc_algebra=toy_a_ok, nc_divergent=toy_d_ok, nc_convention=toy_c_ok,
                       algebra_echo=dict(f=str(ta["f"]) if toy_a_ok else None),
                       convention_echo=dict(ao=str(tc["ao"]) if toy_c_ok else None,
                                            pr=str(tc["pr"]) if toy_c_ok else None))
    if not (toy_a_ok and toy_d_ok and toy_c_ok):
        invalid.append("toy-algebra-failed")
    try:
        micro_ok = bool(micro_selftest())
    except Exception:
        micro_ok = False
    out["micro_livepath"] = micro_ok
    if not micro_ok:
        invalid.append("micro-livepath-failed")
    train_app = [(nm, r) for nm, r in train]
    stream = axes["AXIS-G3-NEW"]["test_reincl"]
    stream_gids = [r["gid"] for r in stream]
    out["stream"] = dict(n=len(stream), n_app=sum(1 for r in stream if r["app"]),
                         n_oos=sum(1 for r in stream if not r["app"]), gids=stream_gids)
    n_stream_app = sum(1 for r in stream if r["app"])
    if not stream or not n_stream_app:
        invalid.append("stream-empty-or-no-app")
        out["invalid_reasons"] = invalid
        out["econ"] = dict(status="MEASUREMENT_INVALID", outcome="NOT_APPLICABLE", decision=None,
                           reason="invalid", reason_detail=invalid)
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    rev = list(reversed(train_app))
    pre1 = rev[:N1]
    pre2 = rev[:N2]
    out["preload"] = dict(n1=N1, n2=N2, n1_classes=len({r["target"] for _, r in pre1}),
                          n2_classes=len({r["target"] for _, r in pre2}),
                          train_app_n=len(train_app),
                          gids_n1=["%s:%s" % (nm, r["gid"]) for nm, r in pre1],
                          gids_n2=["%s:%s" % (nm, r["gid"]) for nm, r in pre2])
    pre1_targets = {r["target"] for _, r in pre1}
    pre2_targets = {r["target"] for _, r in pre2}
    census_h1 = sum(1 for r in stream if r["app"] and r["target"] in pre1_targets)
    census_h2 = sum(1 for r in stream if r["app"] and r["target"] in pre2_targets)
    n_stream_app = sum(1 for r in stream if r["app"])
    out["census_h"] = dict(h1_static=fr(Fraction(census_h1, n_stream_app) if n_stream_app else Fraction(0)),
                           h2_static=fr(Fraction(census_h2, n_stream_app) if n_stream_app else Fraction(0)))
    if args.mechanics_only:
        out["invalid_reasons"] = invalid
        out["valid"] = not invalid
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    pool_pairs = [(_blind_token_set(r["text"]), r["target"]) for _, r in train]
    idf, cent = fit_centroids(train)
    cold = run_cold(pool_pairs, stream)
    mem1 = run_mem(pool_pairs, stream, pre1)
    mem2 = run_mem(pool_pairs, stream, pre2)
    empty = run_mem(pool_pairs, stream, [])
    replay = run_replay(pool_pairs, stream, pre2)
    retr = run_retr(idf, cent, stream)
    s_cold = summarize(stream, cold["recs"])
    s_m1 = summarize(stream, mem1["recs"])
    s_m2 = summarize(stream, mem2["recs"])
    s_empty = summarize(stream, empty["recs"])
    s_replay = summarize(stream, replay["recs"])
    s_retr = summarize(stream, retr["recs"])
    out["arms"] = dict(
        cold=dict(total=cold["total"], man=cold["man"], summary=s_cold),
        mem1=dict(total=mem1["total"], man=mem1["man"], summary=s_m1, writes=mem1["writes"],
                  w_man=mem1["w_man"], keys=mem1["keys"], new_keys=mem1["new_keys"], m_path=mem1["m_path"], m_cost=mem1["m_cost"],
                  m_man=mem1["m_man"], mislabeled=mem1["mislabeled"], h_num=mem1["h_num"]),
        mem2=dict(total=mem2["total"], man=mem2["man"], summary=s_m2, writes=mem2["writes"],
                  w_man=mem2["w_man"], keys=mem2["keys"], new_keys=mem2["new_keys"], m_path=mem2["m_path"], m_cost=mem2["m_cost"],
                  m_man=mem2["m_man"], mislabeled=mem2["mislabeled"], h_num=mem2["h_num"]),
        empty=dict(total=empty["total"], man=empty["man"], summary=s_empty, writes=empty["writes"],
                   keys=empty["keys"], m_path=empty["m_path"], first_path=empty["recs"][0]["path"] if empty["recs"] else None),
        replay=dict(total=replay["total"], man=replay["man"], summary=s_replay,
                    writes=replay["writes"], hits=replay["hits"]),
        retr=dict(total=retr["total"], man=retr["man"], summary=s_retr, ncent=retr["ncent"]))
    fa_obs = s_cold["fa"] if s_cold["fa"] is not None else -1.0
    up_obs = s_cold["up_excl"] if s_cold["up_excl"] is not None else -1.0
    sel_obs = s_cold["selective"] if s_cold["selective"] is not None else -1.0
    cold_trip_ok = (s_cold["executed"] == COLD_TRIP["executed"]
                    and abs(fa_obs - COLD_TRIP["fa"]) < 1e-9
                    and abs(s_cold["coverage"] - COLD_TRIP["coverage"]) < 1e-9
                    and abs(up_obs - COLD_TRIP["up_excl"]) < 1e-9
                    and abs(sel_obs - COLD_TRIP["selective"]) < 1e-9)
    out["cold_tripwire"] = dict(ok=cold_trip_ok, observed=dict(
        executed=s_cold["executed"], fa=s_cold["fa"], coverage=s_cold["coverage"],
        up_excl=s_cold["up_excl"], selective=s_cold["selective"]))
    if not cold_trip_ok:
        invalid.append("cold-repro-failed")
    empty_first_path = empty["recs"][0]["path"] if empty["recs"] else None
    nc_empty_ok = (empty_first_path == "C")
    out["nc_empty_resident"] = dict(ok=nc_empty_ok, first_path=empty_first_path)
    if not nc_empty_ok:
        invalid.append("nc-empty-failed")
    pre_texts = {r["text"] for _, r in pre2}
    seen = set(pre_texts)
    subset_ok = True
    for r, d in zip(stream, replay["recs"]):
        if d["behav_hit"] == 1 and r["text"] not in seen:
            subset_ok = False
        seen.add(r["text"])
    out["literal_subset"] = dict(ok=subset_ok, replay_hits=replay["hits"])
    if not subset_ok:
        invalid.append("literal-subset-failed")
    h1 = Fraction(mem1["h_num"], s_m1["n_app"]) if s_m1["n_app"] else Fraction(0)
    h2 = Fraction(mem2["h_num"], s_m2["n_app"]) if s_m2["n_app"] else Fraction(0)
    out["h"] = dict(h1=fr(h1), h2=fr(h2), sep=fr(h2 - h1))
    if h2 == 0:
        invalid.append("no-recurrence-h2-zero")
    if mem2["writes"] == 0:
        invalid.append("instrument-dead-no-writes")
    e_cold = Fraction(cold["total"], len(stream))
    cwrite = Fraction(2)
    e_warm2 = Fraction(mem2["m_cost"], mem2["m_path"]) if mem2["m_path"] else None
    e_warm1 = Fraction(mem1["m_cost"], mem1["m_path"]) if mem1["m_path"] else None
    econ2 = economics(len(pool_pairs), len(stream), h2, e_cold, e_warm2, cwrite, mem2["writes"], mem2["new_keys"])
    econ1 = economics(len(pool_pairs), len(stream), h1, e_cold, e_warm1, cwrite, mem1["writes"], mem1["new_keys"])
    out["unit_costs"] = dict(e_cold=fr(e_cold), cwrite=fr(cwrite), cmiss=fr(e_cold),
                             e_warm_n1=fr(e_warm1), e_warm_n2=fr(e_warm2),
                             w=fr(cwrite / e_cold) if e_cold else None)
    out["locus"] = dict(
        n2=dict(divergent=econ2["divergent"], f=fr(econ2["f"]), h_ao=fr(econ2["h_ao"]),
                h_pr=fr(econ2["h_pr"]), pred_total=fr(econ2["pred_total"])),
        n1=dict(divergent=econ1["divergent"], f=fr(econ1["f"]), h_ao=fr(econ1["h_ao"]),
                h_pr=fr(econ1["h_pr"]), pred_total=fr(econ1["pred_total"])))
    beh1 = sum(1 for d in mem1["recs"] if d["path"] == "M" and d["executed"])
    beh2 = sum(1 for d in mem2["recs"] if d["path"] == "M" and d["executed"])
    out["behavioral"] = dict(beh_hit_n1=fr(Fraction(beh1, len(stream))),
                             beh_hit_n2=fr(Fraction(beh2, len(stream))))
    e_cold_man = Fraction(cold["man"], len(stream))
    e_warm_man2 = Fraction(mem2["m_man"], mem2["m_path"]) if mem2["m_path"] else None
    cwrite_man2 = Fraction(mem2["w_man"], mem2["writes"]) if mem2["writes"] else None
    if e_warm_man2 is not None and cwrite_man2 is not None and e_cold_man != 0:
        econ_man2 = economics(len(pool_pairs), len(stream), h2, e_cold_man, e_warm_man2,
                              cwrite_man2, mem2["writes"], mem2["new_keys"])
        man_agree = bool(mem2["man"] < cold["man"])
    else:
        econ_man2 = dict(divergent=None, f=None, h_ao=None, h_pr=None, pred_total=None)
        man_agree = None
    out["man_locus"] = dict(
        n2=dict(divergent=econ_man2["divergent"], f=fr(econ_man2["f"]), h_ao=fr(econ_man2["h_ao"]),
                h_pr=fr(econ_man2["h_pr"])),
        e_cold_man=fr(e_cold_man), e_warm_man2=fr(e_warm_man2), cwrite_man2=fr(cwrite_man2),
        direction_agrees_with_lit=man_agree)
    if e_warm2 is not None and not econ2["divergent"]:
        pred_n1 = len(stream) * ((1 - h1) * e_cold + h1 * e_warm2) + mem1["writes"] * cwrite
        relerr = abs(float(pred_n1 - mem1["total"]) / mem1["total"]) if mem1["total"] else None
        out["transfer"] = dict(pred_n1_from_n2_pool=fr(pred_n1), observed_n1=mem1["total"], relerr=relerr)
    else:
        out["transfer"] = dict(pred_n1_from_n2_pool=None, observed_n1=mem1["total"], relerr=None)
    if invalid:
        out["invalid_reasons"] = invalid
        out["econ"] = dict(status="MEASUREMENT_INVALID", outcome="NOT_APPLICABLE", decision=None,
                           reason="invalid", reason_detail=invalid)
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    if cwrite == 0 or e_cold == 0:
        out["econ"] = dict(status="BLOCKED", outcome="NOT_APPLICABLE", decision=None,
                           reason="unmeasurable-cost-scale", reason_detail=["unmeasurable-cost-scale"])
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    totals = dict(cold=cold["total"], mem1=mem1["total"], mem2=mem2["total"],
                  empty=empty["total"], replay=replay["total"], retr=retr["total"])
    rates = dict(cold=s_cold["succ_rate"], mem1=s_m1["succ_rate"], mem2=s_m2["succ_rate"],
                 empty=s_empty["succ_rate"], replay=s_replay["succ_rate"], retr=s_retr["succ_rate"])
    out["totals"] = totals
    out["rates"] = rates
    if len(set(totals.values())) == 1 and len(set(rates.values())) == 1:
        out["econ"] = dict(status="COMPLETE", outcome="NOT_APPLICABLE", decision="CEILING-PARK",
                           reason="non-discriminating-ceiling", reason_detail=["non-discriminating-ceiling"])
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    if e_warm2 is None:
        out["econ"] = dict(status="COMPLETE", outcome="FALSIFIES", decision="ECON-NEVER-PAYS",
                           reason="no-memory-path", reason_detail=["no-memory-path"])
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    if (h2 - h1) < Fraction(1, 20):
        out["econ"] = dict(status="COMPLETE", outcome="INCONCLUSIVE", decision=None,
                           reason="points-collapsed", reason_detail=["points-collapsed"])
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    cps = {}
    for k, (t, s) in dict(cold=(cold["total"], s_cold["verified"]),
                          mem1=(mem1["total"], s_m1["verified"]),
                          mem2=(mem2["total"], s_m2["verified"]),
                          empty=(empty["total"], s_empty["verified"]),
                          replay=(replay["total"], s_replay["verified"]),
                          retr=(retr["total"], s_retr["verified"])).items():
        cps[k] = (Fraction(t, s) if s else None)
    out["cps"] = dict([(k, fr(v)) for k, v in cps.items()])
    if cps["cold"] is None or cps["mem2"] is None:
        out["econ"] = dict(status="COMPLETE", outcome="FALSIFIES", decision="ECON-NEVER-PAYS",
                           reason="no-verified-success", reason_detail=["no-verified-success"])
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    conj = dict(
        totals=bool(mem2["total"] < cold["total"]),
        cps=bool(Fraction(mem2["total"]) * s_cold["verified"] < Fraction(cold["total"]) * s_m2["verified"]),
        matched=bool((s_m2["app_ok"] - s_cold["app_ok"]) >= -2),
        boundary=bool(s_m2["executed_oos"] * 10 <= s_m2["n_oos"]),
        locus=bool((not econ2["divergent"]) and econ2["h_ao"] is not None and econ2["h_ao"] <= h2))
    out["conjunction"] = conj
    if all(conj.values()):
        out["econ"] = dict(status="COMPLETE", outcome="SUPPORTS", decision="ECON-PAYS",
                           reason="all-conjuncts-met", reason_detail=[])
        print(json.dumps(out, indent=2, sort_keys=True))
        return
    detail = []
    if econ2["divergent"]:
        detail.append("structural-divergent")
    if not conj["boundary"]:
        detail.append("boundary-violation")
    if not conj["matched"]:
        detail.append("accuracy-regression")
    if not econ2["divergent"] and econ2["h_ao"] is not None and not (econ2["h_ao"] <= h2):
        detail.append("locus-above-range")
    if not conj["totals"] or not conj["cps"]:
        detail.append("cost-regression")
    if not detail:
        detail = ["cost-regression"]
    out["econ"] = dict(status="COMPLETE", outcome="FALSIFIES", decision="ECON-NEVER-PAYS",
                       reason=detail[0], reason_detail=detail)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
<!-- END FROZEN-RUNNER-ECON -->

## 14. Toy ledger appendix (hand-computed expectations; §13 asserts these exactly)

- `toy_algebra` (PC-ALGEBRA): `Ec=10, Ew=4, Cw=6, W=2, T=4, h=1/2` → `f = 6/(10-4) = 1`; `h* = 1·(2/4) = 1/2`; `pred = 4·(0.5·4 + 0.5·10) + 2·6 = 4·7 + 12 = 40`. Runner asserts `f==1, hstar==1/2, pred==40`.
- `toy_divergent` (NC-DIVERGENT): `Ec=10, Ew=12` → `Ew<Ec` false → `divergent=True`. Runner asserts True (the `g<=0` branch is live code).
- `toy_convention` (NC-CONVENTION): `Ec=10, Ew=4, Cw=6, W=3, K=2, T=4` → `f=1`; `AO = 1·(3/4) = 3/4`; `PR = 1·(2/4) = 1/2`; `AO != PR`. Runner asserts all three (convention sensitivity is live).
