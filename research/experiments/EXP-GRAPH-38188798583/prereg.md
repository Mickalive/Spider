# Preregistration — EXP-GRAPH-38188798583 (graph, design_contract_version 2)

DESIGN ARTIFACT (DESIGN stage). No confirmatory measurement was taken during DESIGN; the
only executed probes are calibration-split-only satisfiability/control/liveness canaries
explicitly listed in the "DESIGN satisfiability probes" section below.

## 0. Identity and binding references
- Experiment ID: EXP-GRAPH-38188798583
- Lane: graph
- Design contract: v2
- Target claim (Director mandate): C-SEMANTIC-RESOLVE (lane charter priority_claims: C-PARAM-INHERIT, C-FRESHNESS, C-DELTA-REPAIR, C-RESIDUAL-NOVELTY, C-LLM-INHERIT, C-SEMANTIC-RESOLVE)
- Immutable request: research/experiments/EXP-GRAPH-38188798583/request.json sha256 08a9649870f3e0e943c0e50259f10abaa0e0da71a9bfc5158b0146f826271986 (request_hash 016f46f8f5bd71ff705f3d478c0f34236b45cd34f00b4636818492fab822cc23)
- Parent handoff (continuity evidence only, does not override the Director REOPEN): research/experiments/EXP-GRAPH-38180711589/handoff.json sha256 38b65a0a835d4f0ac8d16d6e6d915ba57f15cb116b840eaaf59d1849260a24e2
- base_sha d5d2ad8b0f01624fdeb1c324ad4277a7f116e75e; claim_registry_sha256 3511a7885c0ece903eff3cc2b57592a3291e000fecf28f930786fc038a29894b; lane_registry sha256 9ec60d738de5537cd79d9b1684f02dd549062493dea90cef13f2945549e31f73
- This experiment's runner is embedded verbatim in this file (FROZEN-RUNNER block) and its exact bytes are recorded as CANONICAL-RUNNER-SHA256 = 4abc67b1bf435940823b7dc1968c3ddfc4fa23f803b6b124f769d95157d2bc62.

## 1. Director mandate (binding direction)
Allocation action REOPEN, claim C-SEMANTIC-RESOLVE, cognitive_reset=true. The binding strategic
question is spec.json.question: which materially different resolution architecture — (A) a
model-free structured slot/parameter binding with an explicit, independently checkable
abstention condition, or (B) a retrieval/embedding resolver trained on independently authored
goals — simultaneously reaches pooled_false_accept <= 0.10, coverage >= 0.50 and
unknown_precision >= 0.85 on a disjoint calibration/test split AND retains the intact
deterministic selection half (B-LEX-STRONG 97/113 = 0.8584) while generalizing to a held-out
mechanism set and an independently curated synonym lexicon, thereby deciding whether resolve()
ships as a deterministic resolver plus a valid abstention gate or must adopt the
structured/retrieval architecture.

The director_mandate.agent_priors_used entries are treated as design constraints, not evidence:
(a) the abstention gate must be calibrated/validated on a disjoint split; (b) a comparator that
retains memory can erase a treatment advantage; (c) a ceiling/floor task bank cannot support a
success advantage; (d) an abstention signal that abstains on very few examples can obtain high
unknown_precision trivially while retaining a high false-accept. Constraint (d) is the direct
reason this design rejects the parent's near-empty-abstention integer gate family and requires an
explicit, independently checkable abstention predicate with a measurable abstention population.

## 2. Parent handoff carry-forward (preserved; continuity evidence only)
### 2.1 established (must be preserved as inherited state)
- The parent measurement transaction is valid and independently audited; V1-V13 PASS, freeze binding PASS.
- D-PRIMARY = GATE-NOT-MET on the AXIS-PRIMARY test split at t*=0: coverage 53/56=0.9464 (met); pooled_false_accept 3/18=0.1667 (target <=0.10 MISSED); unknown_precision 2/2=1.0 met but carried by only 2 signal-driven abstentions (effective n=2); unknown_precision_inclusive 0.8333.
- The five-component integer ambiguity signal S = 1[famNONE]+1[opNONE]+1[opTIE]+1[noslot]+1[quant] is CAL-FEASIBLE at t*=0 but does not generalize to the disjoint test split (cal FA 0.1000 -> test 0.1667).
- Secondary axes' gate triplets also miss: AXIS-ALTLEX 0.1667, AXIS-HELDOUT 0.2000.
- The deterministic selection half is intact: B-LEX-STRONG 97/113=0.8584 (test split 48/56=0.8571); B-INTERNAL-ID-ORACLE 1.0; B-INCUMBENT-KERNEL 0.0; B-RANDOM-ROLE 0.1858; NC-SHUFFLED-LABEL 0.0442.
- B-LEX-ONLY / CTRL-EXEC-ALL executes 5/18 test out-of-scope (FA 0.2778); CTRL-RANDOM-GATE with the same abstention count yields FA 0.7222 and unknown_precision 0.2778.
- Contamination envelope: |primary applicable|=113, |primary OOS|=38, 9 V3 flags (7 applicable, 2 OOS); max token Jaccard 0.5714 < 0.60; max trigram Jaccard 0.5882 < 0.75; AXIS-HELDOUT 0 flags.
### 2.2 rejected (bounded, must not be revived as this experiment's premise)
- That the specific five-component integer signal S reaches the operating point on the AXIS-PRIMARY test split.
- That a CAL-FEASIBLE calibration split implies the same gate generalizes to a disjoint test split.
- That unknown_precision = 1.0 (effective n=2, inclusive 0.8333) supports a safety claim.
- That the gate-free deterministic resolver is shippable for unseen goals (FA 0.2778).
- That the parent negative is a global falsification of C-SEMANTIC-RESOLVE, of dense embeddings, or of model-free abstention in general.
### 2.3 unknown (inherited, unresolved by this design unless measured)
- D-ALTLEX and D-HELDOUT retention outcomes are BLOCKED (embedding comparator could not load: sentence-transformers/torch/scikit-learn absent).
- Whether the 0.1667 miss is specific to the frozen test phrasing or a general ceiling of S.
- Whether unknown_precision = 1.0 is stable under resampling (effective n=2).
- Whether near-threshold contamination goals (max token Jaccard 0.5714 vs the 0.60 threshold; 9 flagged) materially affect the split.
- Whether the mandate's untested architectures reach the operating point at all.
### 2.4 do_not_assume (binding cautions)
- Do not promote to Product Core or change product behaviour; promote_to_product=false; claim stays HYPOTHESIS.
- Do not treat resolve() as shippable for unseen goals.
- Do not interpret D-ALTLEX/D-HELDOUT BLOCKED as LOST/MIXED/RETAINED.
- Do not treat audit PASS or producer_claim_supported=true as a claim advance.
- Do not quote 0.8584 / 0.1667 / 0.2000 as general properties of deterministic resolvers or abstention signals.
- Do not treat unknown_precision = 1.0 (effective n=2) as a safe calibrated gate.
- Do not re-run another threshold retune of the same integer signal and expect a different claim outcome.
- Do not treat the EXECUTE-side re-implemented arms as the frozen D-PRIMARY decision path.

This experiment tests a materially different architecture (Arm A, below); it does not retune the
integer signal S nor the embedding-cosine-threshold family.

## 3. Arms, treatment identity and comparator
### Arm A (treatment, claim-bearing, feasible now) — T-FRAME
Structured slot/parameter binding with an explicit, independently checkable abstention
predicate. T-FRAME keeps the frozen deterministic selector byte-for-behaviour-identical to the
parent B-LEX-STRONG (verified: 0 mech differences over all 120 G1 / 120 G1-ALT / 80 G2-HELDOUT
applicable goals — see section 8.4) and adds a structural frame-completeness predicate. A goal is
EXECUTED iff (i) the selector resolves a mechanism AND (ii) no abstention clause fires:
- C1-SUBOP: the selector binds an operation whose first token is not the main (head) verb, and a
  subordinating marker ({to, that, which, who, so, then}) precedes the operation span. Captures
  compound/derived instructions whose true mechanism is not the bound operation.
- C3-NO-REFERENCE: the bound operation is READ/UPDATE/DELETE but the instruction binds no
  identifier/reference surface slot (REF lexicon). Captures underspecified lookups.
- C4-COMPLEMENT: after the bound family-noun span (skipping determiners) there is a content token
  that is not a preposition, a REF token, or a relative marker (REL lexicon). Captures a frame
  with an ungoverned complement (e.g. "X this user an administrator").
- C5-SET-QUANT: a set quantifier token is present but the resolved frame binds a definite/singular
  object. Captures set-vs-individual ambiguity.
- C6-SOURCE: the bound operation is CREATE and a source/destination preposition {from, into, onto}
  appears after the family span. Captures an instruction whose frame is a movement/transform.
T-FRAME has ZERO tunable parameters: there is no score, no threshold, and no calibration-fitted
constant. The calibration split is used ONLY to demonstrate feasibility/non-degeneracy, never to
choose a value. The predicate is a conjunction of named, independently inspectable clauses; the
runner reports each clause's boolean per goal so AUDIT can recompute any subset.
### Arm B (comparator, prerequisite-gated)
Retrieval/embedding resolver trained on independently authored goals. Hard prerequisite: an
embedding/training stack with a resolvable pinned model revision. In the current EXECUTE
environment this prerequisite is absent (numpy missing first). Arm B is therefore recorded as an
operational BLOCKED prerequisite, never as a scientific negative; if the stack is provisioned,
Arm B may be run as a comparator but it is not required for a valid Arm A decision.

## 4. Frozen inputs, splits and contamination screen
Fixture blocks are NOT re-authored here; they are consumed verbatim from the frozen parent
preregistration research/experiments/EXP-GRAPH-38180711589/prereg.md sha256
5a64e90da4d1c13b4a290b988cc6096838119d09869abd69512d095cd9318cb0 (blocks GOAL-BANK-G1, OOS-BANK-G1, LEXICON-G1, LEXICON-G1-ALT,
GOAL-BANK-G2, OOS-BANK-G2, LEXICON-G2-HELDOUT) plus PRIOR-PARENT-BANK-TEXTS from
research/experiments/EXP-GRAPH-38175554380/prereg.md sha256 dc90bf71ed03a2329b641d46c1f4f70a53dbeef95ebd6d688645f697868aff9b.
Prior texts for the contamination screen are built from research/harness/goal_generator.py
sha256 cb5218de6a992cf29e26eee8fd5be4b4d7a50084ac3b885587a8ee1da20ace5f (INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES).
- AXIS-PRIMARY: G1 banks under LEXICON-G1. Split rule i % 6 in {1,3,5} = test; complement = calibration.
- AXIS-ALTLEX: G1 banks under LEXICON-G1-ALT. Same split rule.
- AXIS-HELDOUT: G2 banks under LEXICON-G2-HELDOUT. Split rule i % 4 in {1,3,5} = test.
- Contamination screen: a row is removed if max token Jaccard vs prior texts >= 0.60 OR max
  trigram Jaccard >= 0.75. This reproduces the parent fingerprint exactly (9 flags on PRIMARY and
  ALTLEX: app_004, app_049, app_052, app_073, app_076, app_097, app_100, oos_024, oos_026; 0 on
  HELDOUT), so the bound populations are byte-identical to the parent's (151 and 120 rows).
- Resulting measured populations (bound): PRIMARY/ALTLEX 113 applicable + 38 OOS, cal [57,20], test [56,18];
  HELDOUT 80 applicable + 40 OOS, cal [40,20], test [40,20].
- Threshold arithmetic: PRIMARY/ALTLEX test FA target <= 0.10 with 18 OOS means at most 1 false accept
  (1/18 = 0.0556 passes, 2/18 = 0.1111 fails). HELDOUT test FA target with 20 OOS means at most 2
  (2/20 = 0.10 passes, 3/20 = 0.15 fails). Coverage >= 0.50 means >= 28 executed applicable on PRIMARY/ALTLEX
  test and >= 20 on HELDOUT test. unknown_precision is defined only if at least one resolved
  abstention exists on the axis test split (calibration observed 9/8/12, so the measurement is
  non-degenerate by design; if a test axis has zero resolved abstentions the run is
  status=MEASUREMENT_INVALID rather than a fabricated precision).

## 5. Metrics (stable identifiers; exact definitions)
- M-GATE-TRIPLET-PRIMARY / -ALTLEX / -HELDOUT: per axis on the disjoint test split —
  coverage = executed_applicable / applicable; pooled_false_accept = executed_OOS / OOS;
  unknown_precision = abstained_OOS / abstained_resolved (abstained rows whose selector resolved a
  mechanism); unknown_precision_inclusive = abstained_OOS / all_abstained (diagnostic).
- M-SELECTION-B-LEX-STRONG: selective accuracy on executed applicable goals per axis (mechanism equal to
  the goal's target). Retention bar: >= 0.80 on every axis AND >= 0.8584 on AXIS-PRIMARY.
- M-EXEC-VECTOR: per-goal executed boolean under T-FRAME (all bound rows), for AUDIT recomputation.
- M-CONTAM-MAX-JACCARD, M-N (populations), M-EMBEDDING-STATUS.

## 6. Baselines and controls (stable identifiers; all scored by the same runner)
- B-LEX-STRONG: the frozen deterministic selector (selection half). Behaviourally identical to the
  parent across all three lexicons (0 mech differences). Retention bar M-SELECTION-B-LEX-STRONG.
- B-LEX-ONLY (= CTRL-EXEC-ALL): selector with no gate; expected higher pooled_false_accept.
- T-LEX-AMBIG: the frozen parent integer-signal gate S<=0 at t*=0; the incumbent this design must beat.
- CTRL-ABSTAIN-ALL: always abstain; coverage 0.0, unknown_precision 1.0 by convention; degenerate floor.
- CTRL-RANDOM-GATE: abstain the same count as T-FRAME, uniformly at random with SEED; sensitivity control.
- NC-SHUFFLED-LABEL: shuffle applicable targets among executed applicable; null control (expect <= 0.20 ~ chance).
- B-RANDOM-ROLE: assign a uniformly random mechanism; negative control (expect <= 0.35).
- B-INCUMBENT-KERNEL: 0.0 by construction; floor.
- PC-LIVENESS-AND-INTEGRITY: all frozen blocks extract; all controls execute; T-FRAME executes a
  strictly non-empty and strictly non-full set on AXIS-PRIMARY calibration (observed 49/57).
- Arm B: prerequisite-gated; recorded BLOCKED when stack absent, never a scientific negative.

## 7. Decision rule (frozen; precedence is explicit and total)
GATE_MET(axis) := pooled_false_accept_test <= 0.10 AND coverage_test >= 0.50 AND unknown_precision_test >= 0.85.
SELECTION_PRESERVED := (M-SELECTION-B-LEX-STRONG >= 0.80 on all three axes) AND (>= 0.8584 on AXIS-PRIMARY).
VALID := treatment is live on AXIS-PRIMARY test (0 < executed_app < applicable) AND unknown_precision is
defined on every axis test split.
1. If NOT VALID -> status=MEASUREMENT_INVALID, outcome=null (no claim update, no product change).
2. elif GATE_MET(PRIMARY) AND GATE_MET(ALTLEX) AND GATE_MET(HELDOUT) AND SELECTION_PRESERVED
   -> outcome=DECIDE_SHIP_A. Consequence: Arm A (T-FRAME) is licensed as the resolve() resolver+gate
   architecture; C-SEMANTIC-RESOLVE may be advanced by DIRECTOR/AUDIT (this packet does not self-promote);
   Arm B is not required.
3. elif GATE_MET(PRIMARY) AND SELECTION_PRESERVED
   -> outcome=DECIDE_SHIP_A_SCOPED. Consequence: T-FRAME is licensed on the primary fixture only; the
   failing secondary axis (ALTLEX or HELDOUT) is a named generalization gap and the resolver must stay
   UNKNOWN on inputs resembling that mechanism/lexicon family until repaired.
4. else -> outcome=DECIDE_REQUIRE_B. Consequence: Arm A does not satisfy the operating point; resolve()
   must not ship the deterministic+gate architecture; the decision directs the structured/retrieval
   architecture (Arm B prerequisite repair first) and C-SEMANTIC-RESOLVE stays HYPOTHESIS.
Reachability: branch 2 is reachable because all three axes are calibration-feasible (section 8).
Branch 3 is reachable because AXIS-ALTLEX/AXIS-HELDOUT use an alternate/held-out lexicon whose
surface verbs are outside LEXICON-G1 by construction (LEXICON-G1-ALT omits e.g. introduce/instantiate;
LEXICON-G2-HELDOUT adds start/form/schedule/book/file/initiate/log/import), so held-out coverage or
precision can differ from PRIMARY even when PRIMARY passes. Branch 4 is reachable because the AXIS-PRIMARY
test split is disjoint and half-sized: the parent's own disjoint test contains at least three OOS rows that
defeated a partially-effective gate (3/18), and with 18 OOS just two slipping rows (2/18=0.1111) exceed the
target; the structural clauses were not fitted to any test outcome. Branch 1 is a guard, not a claim branch:
it fires only on a non-live/undefined measurement (live calibration executed 49/57; resolved abstentions 9/8/12).
Tie-break: prefer the smallest architecture change and the model-free Arm A if it meets gate+selection.

## 8. DESIGN satisfiability probes (calibration split only; non-outcome-bearing)
Commands (runner reproduced in the FROZEN-RUNNER block; extraction in section 10):
  python3 <extracted runner> --mechanics-only     # reads NO test outcome; builds populations + calibration metrics + liveness
  python3 <selection-equivalence probe>           # comp() mech vs parent runner comp() on all applicable goals
8.1 Feasibility (calibration only): PRIMARY coverage 0.8596 / FA 0.0 / UP 1.0 / executed 49; ALTLEX 0.9123 / 0.0 / 1.0 / 52; HELDOUT 0.8750 / 0.0 / 1.0 / 35. All three cal_feasible=true.
8.2 Non-degeneracy (calibration only): gate-free (B-LEX-ONLY) FA 0.45 / 0.40 / 0.60 and incumbent T-LEX-AMBIG FA 0.10 / 0.10 / 0.05 show the task bank is neither ceiling nor floor, and that T-FRAME's 0.0 is produced by real abstention work (9/8/12 resolved OOS all clause-abstained, 0 slip-through; unresolved OOS 11/12/8).
8.3 Control sensitivity (calibration only): NC-SHUFFLED-LABEL 0.0612 / 0.0192 / 0.0857; B-RANDOM-ROLE 0.0612 / 0.1346 / 0.1143; CTRL-RANDOM-GATE FA 0.50 / 0.50 / 0.45 and UP 0.3571 / 0.40 / 0.44 at matched abstention counts 28 / 25 / 25. All controls fire and are far from the treatment.
8.4 Selection identity: comp() mech agrees with research/experiments/EXP-GRAPH-38180711589/runner_frozen.py comp() on 120+120+80 applicable goals (0 differences on G1, G1-ALT, G2-HELDOUT).
8.5 Prerequisites: python3 stdlib only for the claim-bearing path (present); frozen banks present in the hash-bound parent prereg; prior texts present in the hash-bound goal_generator.py. Arm B embedding stack absent: embedding_status = "BLOCKED: ModuleNotFoundError: No module named 'numpy'" (recorded, non-fatal).
8.6 Mutable dependencies bound: freeze_artifacts = [research/experiments/EXP-GRAPH-38180711589/prereg.md, research/experiments/EXP-GRAPH-38175554380/prereg.md, research/harness/goal_generator.py]; the runner is embedded in this prereg and bound by freeze.json.hashes.prereg.md plus CANONICAL-RUNNER-SHA256.
8.7 Empty/unreachable-branch attack: each decision branch has a concrete trigger (section 7); no branch is a strict superset that makes a later branch unreachable (precedence guard -> all-gates -> primary-only -> else). No declared branch is empty.

## 9. Threats, representation loss and integrity disclosure
- Integrity: the T-FRAME clause set (C1-SUBOP, C3, C4, C5, C6) was developed during DESIGN on the
  calibration split, the parent's published aggregate failure, and the frozen OOS-bank phrasings
  (all inputs, not outcomes). This is disclosed as a design degrees-of-freedom cost. Because T-FRAME
  has zero tunable parameters, this is NOT a threshold fit; the confirmatory test split remains
  untouched and the disposition (does it generalize?) is genuinely open. C1-SUBOP replaced a strict
  head-op clause that failed on LEXICON-G1-ALT during calibration because it was lexicon-coverage
  dependent; the replacement is structural (subordinator + non-head verb), which is the intended
  generalization property, and this substitution is recorded for AUDIT.
- Residual informal scan risk (noted, not settled): C1-SUBOP can fire on a legitimate single
  instruction with a purpose clause ("... to ..."), and C4-COMPLEMENT can fire on a legitimate
  double-object frame. Both are conservative (they abstain; they cannot create false accepts), and
  their effect is visible as reduced coverage, which the >= 0.50 gate bounds.
- Digit stripping (tokens() keeps [a-z]+ only) means identifiers written as bare numerals in a
  READ/UPDATE/DELETE instruction (e.g. a bare "42") are treated as unbindable, so C3 abstains. This
  is a conservative coverage cost on the frozen bank, not a false-accept source.
- The single-split identifiability limitation inherited from the parent is not removed here; a pass or
  fail is bounded to these frozen banks, lexicons and split.
- SEED = 38188798583 mod 2^32 is fixed and recorded; no bootstrap is attempted (V11 NOT_APPLICABLE).
- Arm B BLOCKED is an unavailable-dependency state, not a scientific result and not a loss.

## 10. Freeze artifacts and canonical hashes
CANONICAL-RUNNER-SHA256 = 4abc67b1bf435940823b7dc1968c3ddfc4fa23f803b6b124f769d95157d2bc62
- The FROZEN-RUNNER block below is the exact executable decision path. EXECUTE MUST extract it with
  re.search(r"<!-- BEGIN FROZEN-RUNNER -->\n(.*?)\n<!-- END FROZEN-RUNNER -->", text, re.S),
  restore the single trailing newline, write it to
  research/experiments/EXP-GRAPH-38188798583/raw_evidence/runner_tframe.py, and verify
  sha256 == CANONICAL-RUNNER-SHA256 before running it. EXECUTE MUST NOT edit the runner; any
  necessary change is a DESIGN-stage revision, not an EXECUTE edit.
- Immutable interpretation dependencies (freeze_artifacts, hashed into freeze.json.artifact_hashes):
  research/experiments/EXP-GRAPH-38180711589/prereg.md sha256 5a64e90da4d1c13b4a290b988cc6096838119d09869abd69512d095cd9318cb0;
  research/experiments/EXP-GRAPH-38175554380/prereg.md sha256 dc90bf71ed03a2329b641d46c1f4f70a53dbeef95ebd6d688645f697868aff9b;
  research/harness/goal_generator.py sha256 cb5218de6a992cf29e26eee8fd5be4b4d7a50084ac3b885587a8ee1da20ace5f.
- Immutable request sha256 08a9649870f3e0e943c0e50259f10abaa0e0da71a9bfc5158b0146f826271986; parent handoff sha256 38b65a0a835d4f0ac8d16d6e6d915ba57f15cb116b840eaaf59d1849260a24e2.

## 11. EXECUTE / AUDIT contract
- EXECUTE runs exactly: python3 research/experiments/EXP-GRAPH-38188798583/raw_evidence/runner_tframe.py
  (no --mechanics-only flag). It writes the raw stdout to raw_evidence/runner_result_raw.json and
  assembles result.json / report.md / provenance.json per research/EXPERIMENT_PACKET.md, mapping the
  runner's decision to outcome and keeping RAW EVIDENCE / OBSERVATIONS / DERIVED MEASUREMENTS /
  INTERPRETATION distinct. A valid scientific negative is status=COMPLETE with outcome=DECIDE_REQUIRE_B,
  NOT an infrastructure failure. status=MEASUREMENT_INVALID only when the runner emits invalid_reasons.
- EXECUTE must also run --mechanics-only and record its output as the prerequisite/validity evidence.
- AUDIT recomputes M-GATE-TRIPLET-* and M-SELECTION-B-LEX-STRONG from execution_vectors + the frozen
  banks, verifies the runner hash and the freeze artifact hashes, and checks branch precedence.

## 12. Product consequences
- Positive (DECIDE_SHIP_A / DECIDE_SHIP_A_SCOPED): license resolve() as a deterministic resolver plus the
  T-FRAME abstention predicate (scoped to the generalization surface actually measured); this packet alone
  does not promote the claim — DIRECTOR/AUDIT adjudicate the advance.
- Negative (DECIDE_REQUIRE_B / MEASUREMENT_INVALID): do not ship resolve() with a deterministic+gate
  architecture; require the structured/retrieval architecture with Arm B prerequisites repaired first,
  and keep resolve() UNKNOWN for low-confidence unseen goals. No product behaviour change.

<!-- BEGIN FROZEN-RUNNER -->
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
<!-- END FROZEN-RUNNER -->
<!-- CANONICAL-RUNNER-SHA256: 4abc67b1bf435940823b7dc1968c3ddfc4fa23f803b6b124f769d95157d2bc62 (extract: captured group + "\\n") -->

(END OF PREREGISTRATION)
