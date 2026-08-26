# CYCLE 8 REPAIR ROUND 3 — DELIVERY NOTE (run 32931388530, 2026-08-26)

NON-EVIDENCE documentary delivery. Descends from round-1 repro tip
`937c7a5` per RFIX-A of gate `CYCLE_32928978937_INTEL_GATE.json`.
Branch: `cycle/intel/32931388530/repro`. **Zero condition-level
observations exist in this tree; no confirmatory collection was
performed or attempted this round** (collection belongs to the next
dispatch under the once-extended CAP; hard closure whatever it returns).

## What round 2 was, and what this round fixes

Round 2 (run 32928978937) delivered NOTHING: the persisted snapshot was
byte-identical to the accepted-lane base `7a8182d`, so the entire
cycle-8 instrument was absent from that audited tree. The round-2 audit
certified honest non-delivery (no fabrication anywhere) and re-issued
the outstanding fixes as RFIX-A..D. This round delivers exactly those.

## Required-fixes delivery

| Fix | Delivery |
|---|---|
| RFIX-A non-empty delivery from `937c7a5`, self-verified before session end | This branch carries: `intel/experiments/unbrowse_ladder_c8/` (32 modules), `intel/prereg/cycle8_unbrowse_ladder_powered_prereg.md` (+ erratum E1), `results/intel/reproductions/cycle8/pre_freeze_phase0/` (now 6 files), rewritten `state/intel_reproduction.json`. Verification block below. |
| RFIX-B dated erratum below the frozen separator | Erratum **E1** appended BELOW the separator (commit `d1ce094`): (i) pre-collection attestation across rounds 0→1→2→(3) with run ids and ZERO condition-level observations anywhere; (ii) REFRESHED sha256 table for all 32 modules at the new freeze point (E1.3 supersedes frozen section 16 for integrity checks; five stale rows superseded with old values recorded); (iii) amended-file self-hash with a mechanically verifiable coverage definition (E1.4). The append makes the three in-code "repair-1 erratum" comment referents TRUE without any code edit and unblocks next-dispatch protocol step 1. Frozen text above the separator is byte-identical to freeze commit `18abd5a` (asserted programmatically at append time). |
| RFIX-C offline gates re-run once more, code untouched | ALL GREEN post-erratum: selftest **115/115**, phase0_fixtures prereg-text suite all-match, regression_lock bit-exact vs archived c7 figures, wiring_audit clean, ttl_rehearsal both directions, rehearsal_fullshape production shape, power tables byte-stable vs the section-10 embedding, sealed schedule regenerates `276132df…` exactly. Artifact: `pre_freeze_phase0/round3_gate_rerun.json` (includes hash-before/hash-after code-untouched proof). State file `preregistration.sha256` updated to the amended prereg's E1.4 self-hash. |
| RFIX-D truthful provenance rewrite | `state/intel_reproduction.json`: verified c7-lineage disposition (16/24 common modules byte-verbatim; eval_guard.py docstring-only; substantively modified: evaluate_rule.py, extract.py, run_all.py, specgen.py, stats.py, tasks_hosts.py + selftest.py extended; 8 new Phase-0 tooling modules — golden_fixtures.py counted as inherited byte-verbatim); repair-round ledger rounds 0→1→2→(3) with delivery status, artifact lists, timestamps and per-round changed-file enumerations; stale "selftest 99/99" corrected to 115/115; verdict_proposed remains null; status remains pending-collection. |

## Test-integrity statement

The preregistered test is UNCHANGED by this round in every respect:
frozen text above the separator byte-identical to `18abd5a`; pairs=12,
N_MIN_VALID=8, speedup>=2.0, one-sided Holm alpha=0.05, C3' two-variant
gates, invalidity conditions, verdict mapping — all untouched. Zero code
edits were made this round (proven by module hashes equal to the round-1
tip state before and after every gate rerun). The erratum only refreshes
integrity metadata below the separator, which the frozen text itself
designates as the sole permitted amendment channel.

## Persisted-output self-verification (RFIX-A)

- Branch tip descends from `937c7a5` (round-1 tip): YES.
- Deliverable files present on the branch that will be pushed: enumerated
  in `state/intel_reproduction.json.persisted_output_self_verification_rfix_a`.
- Protocol step 1 unblocked: `sha256sum -c` semantics against the E1.3
  refreshed table verify 32/32 on this tree (see `round3_gate_rerun.json`
  → `code_untouched_proof.module_hashes_equal_erratum_E1_3_table`).
- Self-hash one-liner (E1.4) reproduces the committed value: verified.

— INTEL_REPRODUCER, cycle 8 repair round 3, 2026-08-26
