# EXP-RUNTIME-38115361581 preregistration (DESIGN)

**Experiment ID:** EXP-RUNTIME-38115361581  
**Lane:** runtime  
**Claim:** C-MEAS-VALID  
**Design contract:** v2  
**Status:** DESIGN (not frozen)

## 1. Research question

Can a non-degenerate asymmetric-discovery task bank be certified arithmetically BEFORE freeze - with cold re-derivation and a retrieval-shaped comparator demonstrably below the success ceiling at high residual novelty (B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one task family, matched correctness >= 0.80 for all arms), a real treatment/comparator behavioural distinction, honest per-condition counters (http_requests + retrieval_calls + verification_calls + repair_attempts) and a preregistered contamination/dynamic-range certificate - and be delivered as a reusable substrate that unblocks the flagship inheritance benchmark (B2)?

## 2. Hypothesis

There exists a credential-free asymmetric-discovery task bank (multi-task sessions where one-time session/resource/schema discovery is amortized or cached across tasks, i.e. NOT the mandatory-discovery deterministic REST class) such that B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED show success_rate < 0.95 at novelty>=0.5 on >=1 task family, with matched correctness>=0.80 for all arms. If no such bank exists among tested credential-free substrates, the certificate is unsatisfiable and the correct outcome is a bounded substrate-class negative.

## 3. Parent handoff and Director mandate

This experiment inherits from EXP-RUNTIME-37973247935 handoff: measurement was invalid due to response-fingerprint volatility (hop-by-hop 'Connection' header) and gate predicate mismatch; out-of-surface transfer remains untested. The Director mandate (director_mandate in request.json) is binding: treat target claim C-MEAS-VALID and strategic question as given; cognitive reset performed; parent_handoff_disposition SUPERSEDE in effect for the chosen direction. We explicitly do not repeat the mandatory-discovery deterministic REST certificate (fourth re-run excluded). The focus is B2 substrate dynamic range.

## 4. Exclusions

- Do NOT repeat EXP-RUNTIME-37973247935's out-of-surface composite-oracle measurement (separately repairable). This design addresses the B2 readiness question (dynamic range of task bank).
- Do NOT test the mandatory-discovery deterministic REST class.
- Do NOT inspect outcome measurements during DESIGN (only cheap arithmetic satisfiability probes allowed).

## 5. Baselines

- **B-COLD-RE-DERIVE**: cold start; no persistent parameterization/procedure cache carried over across independent cold trials. Within-session amortization of session/resource/schema discovery is allowed if it matches realistic cold-rederive semantics.
- **B-RETRIEVAL-SHAPED**: retrieval-shaped comparator with relevant artifacts but without treatment's parameterization/distillation path; must be plausibly strong but sub-ceiling at novelty>=0.5.

Both must achieve matched correctness >= 0.80 on evaluation set.

## 6. Controls

- **Positive control**: synthetic sanity task family (or inclusion that would show sensitivity) — confirms instrument sensitivity. If bank cannot produce any sub-ceiling case, confirms "no dynamic range" class.
- **Null control**: contamination controls - cross-arm identity isolation, no index leakage, session cache scoping prevents cross-trial carryover, identifier canonicalization prevents trivial matches. Explicit contamination audit required.
- **Contamination bounds**: index/task-id hashed and uncorrelated across arms; no shared mutable state that leaks solutions between arms.

## 7. Certificate arithmetic (preregistered)

Define for each task family f and novelty bucket n>=0.5:
- s_cold(f,n) = success_rate(B-COLD-RE-DERIVE, f,n)
- s_ret(f,n) = success_rate(B-RETRIEVAL-SHAPED, f,n)
- c_arm = correctness of each arm on full set

Certificate PASS if exists f,n>=0.5 with s_cold(f,n) < 0.95 and s_ret(f,n) < 0.95 AND c_arm >= 0.80 for all arms AND treatment/comparators show real behavioural distinction (not identical traces/counters) on >=1 certified family AND honest per-condition counters recorded AND contamination audit passes AND substrate != mandatory-discovery deterministic REST class.

Behavioral distinction requires that on >=1 certified family, at least one counter differs between arms or trace shape differs (e.g., http_requests/retrieval_calls/verification_calls/repair_attempts differ by >= preregistered epsilon, or path differs). "Identical traces" would invalidate distinction.

## 8. Measurement validity

- Counters: per-condition (http_requests, retrieval_calls, verification_calls, repair_attempts) recorded independently; logical sums verified.
- Novelty stratification: tasks stratified by novelty score [0,1]; certificate requires < 0.95 at novelty>=0.5.
- Matched correctness: shared definition, arm-blind evaluation.
- Contamination audit: explicit checklist items verified.
- Exclusion: reject mandatory-discovery deterministic REST class; document why excluded if candidate is similar.

## 9. Outcomes

- **CERTIFY (PASS)**: all conditions met → unblocks B2 with certified dynamic range. Record certified family(ies), novelty bucket(s), rates, counters summary, contamination audit.
- **BOUNDED_NEGATIVE**: cannot satisfy on any credential-free substrate tested → do NOT freeze degenerate bank. Record substrate-class negative (bounded to "asymmetric-discovery task bank for B2"), list tested substrates, why each failed (e.g., both arms >=0.95 at novelty>=0.5; matched correctness < 0.80; contamination fails; only mandatory-discovery REST fits). This is not a general downgrade of C-MEAS-VALID.
- **MEASUREMENT_INVALID**: infrastructure/substrate failure prevents certificate arithmetic (e.g., cannot run credential-free substrate reliably). Distinguish from scientific negative.
- **INCONCLUSIVE**: other cases not matching above.

## 10. Satisfiability probes (DESIGN only, cheap)

Allowed in DESIGN: static checks, small dry-runs on trivial fixtures, arithmetic feasibility, counter schema validation, stratification logic, contamination checks. No confirmatory outcome-bearing measurements of the full certificate on expensive runs.

## 11. Freeze artifacts (v2)

Mutable local artifacts bound:  
- research/runtime/task_banks/asymmetric_discovery/__init__.py  
- research/runtime/task_banks/asymmetric_discovery/schema.py  
- research/runtime/task_banks/asymmetric_discovery/families.py  
- research/runtime/task_banks/counters.py  
- research/runtime/task_banks/novelty.py  
- research/runtime/task_banks/contamination.py  
- research/runtime/task_banks/dynamic_range_cert.py  

These define bank, stratification, counters, contamination, and certificate arithmetic. Freezer will hash them into freeze.json.artifact_hashes.

## 12. v2 freeze eligibility

- decision_rule_reachability: NOT_APPLICABLE (design-stage arithmetic; probes only)
- measurement_prerequisites: PASS (all structures specifiable)
- baseline_identifiability: PASS (explicit baselines + constraints)
- control_sensitivity: PASS (constraints force < 0.95 and >=0.80; contamination control)
- treatment_liveness: NOT_APPLICABLE (no SPIDER treatment arm executed in this certificate; B2 treatment is separate)
- freeze_artifacts_bound: PASS (all mutable deps listed)

## 13. Attacks on design (self-critique)

- Ceiling trap: requiring < 0.95 at novelty>=0.5 is arithmetic guard; also matched correctness >=0.80 prevents degenerate "all fail" masking? If all fail but correctness is bad, we reject - correct to avoid meaningless comparisons.
- Treatment/comparator identity: behavioral distinction required - prevents identical traces.
- Mandatory-discovery REST exclusion: explicitly named to avoid repeating the degenerate class.
- Contamination: explicit audit prevents index leakage/cross-arm carryover.
- Bounded negative: outcome is class-bounded, not global C-MEAS-VALID downgrade - matches packet discipline.
- Counters honest: per-condition independence + logical sums required.

## 14. Relationship to packet discipline

- Preserve established/rejected/unknown/do_not_assume from parent handoff where relevant (we inherit the measurement-invalid diagnosis of prior packet; this is a different question).
- Use stable identities if EXECUTE/AUDIT reuse components later.
- Raw/derived/interpretation kept distinct; scientific negative (bounded class negative) is COMPLETE outcome if certificate arithmetic fails on all tested substrates, not infrastructure failure.
- Never turn infrastructure failure into scientific falsification; use MEASUREMENT_INVALID status appropriately.
