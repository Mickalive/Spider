# EXP-PHYSICS-35774039080 — EXECUTE Report

**Lane**: physics · **Claim**: C-WEB-DYNAMICS (HYPOTHESIS) · **Status**: `MEASUREMENT_INVALID` (substrate_insufficient) · **Outcome**: `INCONCLUSIVE`

## 1. Identity and frozen contract

- Experiment: EXP-PHYSICS-35774039080, Global Research Director PIVOT (cycle 35773306702) off the Gate0-blocked history-conditioned CMI program into an orthogonal timescale-separation / barrier-committor program on *existing* TodoMVC/BrowserGym trajectories **without requiring new Gate0 SPAs** (request.json `director_mandate`, `parent_handoff_disposition: SUPERSEDE`).
- Pre-execution hash verification: `prereg.md` 185b7642…, `request.json` b0e6eeac…, `spec.json` 8eeebec9… all MATCH `freeze.json` before any computation. Frozen inputs were not modified.
- Reused substrate: 10 TodoMVC raw trajectory files from EXP-PHYSICS-35209110569 (5 variants × raw + topup). All 10 sha256 MATCH the artifacts recorded in that experiment's `result.json` (10/10).

## 2. What was executed (frozen plan, step-by-step)

Per the frozen analysis plan (prereg §15 steps 1–7) the first action is the **relaxed substrate gate**, with an explicit halt rule: *"compute relaxed gate table — halt if Q==0 with MEASUREMENT_INVALID"* (prereg §15.1, §13 Relaxed_substrate; spec.json `decision_rule` first clause).

1. **Hash verification** — PASS: freeze hashes match; 10/10 reused raw files match recorded hashes.
2. **WebShop/BrowserGym scan** — absent: no `research/intel/`, no `/tmp/browsergym_cache`, no browsergym/webshop/webarena/miniwob file anywhere under `research/`. Proceed with TodoMVC only, as the frozen spec explicitly permits ("if WebShop absent, proceed with TodoMVC only and document").
3. **Gate table** (per dataset, frozen definitions): computed `NL`, `strata_count` (URL_before, H_K=3 actions, Action; ≥3 per stratum), `singleton_SA_rate`, `leakage_validOnly`, `dom_bytes` coverage, `a11y` coverage, `unique_titles`. Output: `gate_table.json` (sha256 fe0474a0…).

### Gate results (all 5 variants)

| site | NL | strata (≥3) | singleton | leakage_validOnly | dom_bytes cov | a11y cov | qualifies |
|---|---|---|---|---|---|---|---|
| vanillajs | 93 | 21 (12) | 0.0 | 0.285 | **0.0** | **0.0** | NO |
| react | 93 | 21 (12) | 0.0 | 0.285 | **0.0** | **0.0** | NO |
| vue | 85 | 21 (13) | 0.0 | 0.213 | **0.0** | **0.0** | NO |
| angular | 107 | 22 (13) | 0.0 | 0.177 | **0.0** | **0.0** | NO |
| svelte | 93 | 21 (12) | 0.0 | 0.285 | **0.0** | **0.0** | NO |

**Q = 0.** Every quantitative sub-gate that is expressible from the reused files passes (NL ≥ 50, strata ≥ 5 with ≥ 3 each, singleton < 70%, leakage < 60%). The binding failure is identical across all five datasets: **dom_bytes coverage 0.0 and a11y coverage 0.0**, both required ≥ 0.80 by the frozen relaxed-sufficiency rule.

## 3. Raw evidence: why coverage is 0.0

The reused TodoMVC trajectories were produced by `EXP-PHYSICS-35209110569/collect_spa_survey.py`, which records per transition only `site, session, url_before, url_after, title_before, title_after, action_primitive, action_target, timestamp, error`. **No DOM snapshot (visibleText / innerText / dom_bytes) and no accessibility tree (a11y_tree / accessibility_roles) was ever captured for these trajectories.** The 0.0 coverage values are field absence, not a measured small-DOM value.

Consequences for the two prongs and the mandatory baseline:

- **H_T (timescale)** uses `S_primary = SHA256(norm(url_after) | norm(title_after))` — computable from the reused files (TodoMVC title is constant, so S reduces to hash-URL over 3–4 hash fragments). But the frozen gate explicitly blocks primary testing at Q==0 ("do not test H_T/H_B", spec decision_rule; prereg §13), and the frozen primary condition additionally requires `ACF_obs(3) > B-DOM-SIMILARITY ACF_sim(3) + 0.05`.
- **B-DOM-SIMILARITY (mandatory per director mandate)** is a kNN/TF-IDF similarity predictor over **DOM visible_text (R1) and a11y text (R2)** — impossible to construct from this substrate regardless of gate status.
- **H_B (barrier/committor)** defines states `x = (URL_before_normalized, DOM_before_hash R1 or R2)` — DOM_before hashes cannot be computed without DOM snapshots.

A partial URL|title-only run of H_T would (a) violate the frozen halt rule, and (b) still not satisfy the frozen primary condition because the mandatory similarity baseline cannot be computed. The honest frozen outcome is therefore the halt: MEASUREMENT_INVALID substrate_insufficient.

## 4. Interpretation (kept distinct from observations)

- **RAW EVIDENCE**: field sets of the 10 reused files; coverage values 0.0; hash matches; substrate scan; gate rows (§2/§3, `gate_table.json`).
- **DERIVED MEASUREMENT**: Q = 0 qualifying datasets under the frozen gate.
- **INTERPRETATION**: This is **substrate insufficiency**, not falsification and not a null result. The frozen rules classify Q==0 as `MEASUREMENT_INVALID substrate_insufficient`, publish gate table, test nothing, and hand off the gap. C-WEB-DYNAMICS receives **no claim update** (remains HYPOTHESIS; no update in codex terms is justified by this packet).

## 5. Frozen decision-rule outcome

```
Relaxed substrate: 0 qualifying datasets (dom_bytes>=500 on >=80% and a11y non-empty
on >=80% fail on all 5 TodoMVC variants; WebShop absent)
=> MEASUREMENT_INVALID substrate_insufficient
=> no H_T/H_B testing, no positive/null pipeline gates (they gate the primary stage only),
   no C-WEB-DYNAMICS update
```

Positive controls (PC-METASTABLE, PC-BARRIER) and null controls (NC-IID, NC-GROUPED-PERM) and the Markov/shuffle/random-dwell/trajectory-memory baselines were **not run**, because the frozen analysis plan halts at step 1 when Q==0; they cannot alter the frozen result and running them would exceed the frozen scope. Frozen control identifiers are preserved in `result.json.controls` with `NOT_RUN`/`unknown` status and exact reasons, so AUDIT and DIRECTOR can verify the gating logic.

## 6. Validity notes (summary; full list in result.json)

- A valid lab notebook entry: this run is re-executable from the frozen commit via `PYTHONHASHSEED=0 python3 research/experiments/EXP-PHYSICS-35774039080/execute.py` (stdlib only; no RNG; produces byte-identical `gate_table.json`).
- Leakage executed under *this* experiment's frozen normalization (lowercase, strip query, **preserve** SPA hash fragment, strip trailing slash). Prior EXP-PHYSICS-35209110569 used a fragment-*stripping* normalization in its own frozen rule; counts differ only for angular (23 vs 37 leaky) and change no gate outcome. Documented in result.json observations/validity_notes.
- Execution environment: Python 3.12.14, stdlib only (numpy/scipy/sklearn/playwright not installed). Gate path needed no third-party packages; the primary pipeline would require them for any retry on qualifying substrate.
- Representation loss: none introduced by this run (no hashing/truncation performed beyond sha256 state diagnostics in the gate; S_primary hashing was implemented in the gate code but only used for singleton counting — TodoMVC title is constant so S=hash(url) over 3–4 fragments).

## 7. Consequences per frozen product_consequence (MEASUREMENT_INVALID branch)

Per prereg §14 and spec `product_consequence_*`: **no claim update; no product action is authorized by this packet.** The MEASUREMENT_INVALID branch requires the exact gap be documented and the smallest unblocking step proposed:

1. **Re-collect trajectories with DOM observables** (visibleText innerText + `Accessibility.getFullAXTree` serialization, target_sig fields role/name/testId/aria-label) on TodoMVC variants and/or BrowserGym WebShop — under a new freeze — to satisfy dom_bytes≥500/a11y coverage ≥80% and to enable R1/R2 DOM_before hashes and B-DOM-SIMILARITY.
2. **Or intel supplies BrowserGym/AgentLab trajectories** (research/intel/ is currently absent; director mandate dependencies already list intel as the production-SPA channel).
3. **Or Director re-freezes** a substrate gate for URL|title-only state definitions — this would drop the director-mandated B-DOM-SIMILARITY requirement unless DOM becomes available, so it is a Director decision, not an EXECUTE-level adaptation.

This result is informative in the specific sense anticipated by the design: it confirms the orthogonal timescale/barrier program **cannot yet be tested** because the reused "existing trajectories" lack the DOM observables the frozen design itself requires — while every gate sub-criterion that *can* be evaluated from the reused files passes, so the substrate is *almost* sufficient (85–107 NL, adequate strata, negligible singleton, leakage < 30%) and a DOM-bearing re-collection is the single smallest unblocking step. It is NOT evidence about whether slow timescales or barrier/committor structure exist in Web dynamics.