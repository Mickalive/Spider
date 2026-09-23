# EXP-GRAPH-35932480731 — EXECUTE report

**Lane:** graph | **Claim:** C-PARAM-INHERIT | **Frozen question:** does a durably-committed corrected `distill_parameterized()` in `src/spider/kernel.py`, verified by grep/sha/diff/unit-tests, and a durable WebArena-Verified v2 census (>=10 valid zero-overlap B tasks), achieve EXECUTABLE>=0.75 (Wilson lower>=0.65) and binding>=0.90 (lower>=0.80) with zero unsubstituted templates, false_accept<=0.10, UNKNOWN in [0.00,0.15], ECE<=0.15 on held-out single-family add_to_cart B tasks?

**Status:** MEASUREMENT_INVALID — frozen substrate gates failed before any outcome-bearing measurement.
**Outcome:** NOT_APPLICABLE — no scientific claim measured; this is infrastructure/substrate failure, not falsification.

---

## 1. What was executed (frozen procedure)

Per frozen `spec.json` measurement_validity #1–#2 and `prereg.md` §5.1, the first action of EXECUTE is the *durability gate*, verified **before** any B measurement. The prereg is explicit: *"No outcome-bearing B measurement until gate passes. If any fails → MEASUREMENT_INVALID, no B inference."* The run therefore executed exactly the gate stage, terminated at the gate (as the frozen design requires), and did **not** touch held-out B tasks, distill, resolve/bind/verify, controls, or baselines.

All frozen inputs were hash-verified against `freeze.json` before execution (matched; inputs immutable).

## 2. RAW EVIDENCE → OBSERVATION → DERIVED MEASUREMENT

Raw evidence artifacts (sha256 in `result.json.artifacts`):

| Evidence file | Content |
|---|---|
| `raw_evidence/kernel_check.json` | HEAD sha, kernel path/lines/sha256, per-symbol grep counts, diff line counts vs base 219d24ae and legacy 98b40ef4 |
| `raw_evidence/unit_tests_check.json` | test file existence, tests dir listing, pytest outputs with/without PYTHONPATH |
| `raw_evidence/census_check.json` | data/ existence, webarena_verified_v2.json existence, Docker image persistence and run-probe exit |
| `raw_evidence/environment.json` | Python/pytest/docker versions, API-key presence, git state |
| `raw_evidence/refs_check.json` | symbol/test/data presence on HEAD, origin/main, origin/lab2/product |
| `raw_evidence/transient_harnesses.json` | symbol counts inside 4 old `run_experiment.py` harness copies |

**Observations (direct, uninterpreted):**

1. HEAD = `0133f3bf70c4babd85f8d8c3eff92429e9f960c6` ("R2 graph: execution base EXP-GRAPH-35932480731"), branch `lab2/graph`.
2. `src/spider/kernel.py` = 132 lines, sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` — the same sha the independent audit of EXP-GRAPH-35918640311 found at HEAD 7dc6bd27 (literal-only kernel).
3. `grep -c` = 0 for all 8 required symbols (`distill_parameterized`, `_common_prefix_and_suffix`, `_extract_varying_values`, `_structure_similarity`, `_is_allowed_path`, `_ALLOWED_PREFIXES`, `_field_path_to_slot_name`, `_sanitize_slot`).
4. `git diff 219d24ae..HEAD -- src/spider/kernel.py` = 0 lines; legacy `git diff 98b40ef4..HEAD` = 0 lines.
5. `tests/test_kernel_param_inherit.py` absent (`tests/` has only `test_kernel.py`).
6. `data/` absent; `data/webarena_verified_v2.json` absent; no `data/` tree entries on HEAD, origin/main, or origin/lab2/product.
7. Docker server 28.0.4 present, but after `docker pull` the pinned image is not in `docker images`; `docker run ... am1n3e/webarena-verified-shopping@sha256:3e8cb9b9... -c 'echo IMAGE_OK; ls /'` timed out at 110 s (exit 124) and stderr shows a fresh registry pull on each invocation.
8. `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` absent.
9. `PYTHONPATH=src python -m pytest tests/test_kernel.py` → **3 passed** (literal kernel functional); without PYTHONPATH → collection error `ModuleNotFoundError: No module named 'spider'`.
10. `distill_parameterized` appears only in 4 old transient `run_experiment.py` harness copies (EXP-GRAPH-35784823623, 35864745180, 35793560957, 35798169917), incomplete relative to the frozen spec (e.g. `_ALLOWED_PREFIXES` 0 in 3/4) and none is a durable `src` commit.

**Derived measurement (from the observations, per frozen gates):**

| Gate (frozen id) | Required | Observed | Result |
|---|---|---|---|
| GATE-KERNEL-DURABILITY | grep>=1 each of 8 symbols; sha matches claimed fixed kernel; diff 219d24ae..HEAD nonempty | 0/8 symbols; sha = parent-invalid kernel; diff 0 lines | **FAIL** |
| GATE-UNIT-TESTS-PARAM-INHERIT | test file exists and passes B1/B4/D1/E1/C2/B2/B3/B5 | file absent | **FAIL** |
| GATE-CENSUS-DURABLE | data/webarena_verified_v2.json pre-existing OR pinned Docker source OR static export; >=10 valid zero-overlap B | no file; Docker image not durably usable (probe timeout, no persistence) | **FAIL** |
| GATE-LLM-SUBSTRATE | API key for F3/F4 branch | absent | NOT_APPLICABLE (frozen) |
| PC/NC/B-LITERAL control measurement | after gates pass | not run (gates failed first) | NOT_RUN |
| CHECK-EXISTING-LITERAL-TESTS (informational) | literal kernel tests pass | 3/3 pass with PYTHONPATH=src | PASS (localizes the gap) |

## 3. INTERPRETATION

The frozen decision rule (spec.json `decision_rule`; prereg §8) triggers **MEASUREMENT_INVALID** on two independent clauses:

- **(i) kernel not durably committed**: grep 0 for every required symbol, sha256 identical to the kernel that the prior audit already proved invalid (EXP-GRAPH-35918640311 audit: `kernel_sha_actual 46929b3a`, `kernel_diff_actual false`), `git diff base..HEAD` empty, unit test file missing. The kernel at HEAD is still the 132-line literal-only kernel — *nothing changed since the parent's MEASUREMENT_INVALID audit*.
- **(ii) census not durably provisioned**: neither the pre-existing file path, a usable pinned Docker source, nor a verified static export exists in this environment; >=10 valid zero-overlap B tasks cannot even be constructed, so the adequacy gate is uncheckable.

Because the gates failed *before* outcome measurement (prereg §5.1), **zero B tasks were measured**. This is why `result.json.metrics` are `null` (explicitly not available), `PC/NC/B-LITERAL` are `NOT_RUN`, and the LLM baselines plus all economics metrics are `NOT_APPLICABLE` (absent API key per frozen semantics — api_key_absent makes C4/F3/F4 NOT_APPLICABLE but preserves F1/F2 as primary; here F1/F2 are invalid for kernel/census reasons, not LLM reasons).

**This is not a scientific negative.** Per EXPERIMENT_PACKET §9 and AGENTS.md failure discipline, substrate failure must never be encoded as falsification. C-PARAM-INHERIT remains EXPERIMENTAL at the previously accepted narrow synthetic ceilings (EXP-PRODUCT-33528829801 10/10 single-param with 5.42% saving; EXP-PRODUCT-33741671686 21/21 harness-only multi-param). The live WebArena-Verified v2 family-holdout question remains untested — this run adds no evidence for or against the hypothesis that the corrected induction achieves EXECUTABLE/binding on held-out B. What it does establish is a crisp, hash-pinned diagnostic: the two durability prerequisites are still absent **at the repo level** (not only at the experimental-dir level), the Docker census path is currently not runnable in this CI environment, and the failure is precisely localized (existing literal kernel tests pass 3/3).

## 4. Smallest unblocking actions (next run prerequisites)

1. **Durable kernel commit** (Product scope, `src/spider/kernel.py`): port/implement `distill_parameterized` with single-prefix `_common_prefix_and_suffix`, `_extract_varying_values` restricted to url/path + body.* + headers.* via `_is_allowed_path`/`_ALLOWED_PREFIXES`, `_structure_similarity` Jaccard>=0.75 constant-anchor, distinct slots via `_field_path_to_slot_name`/`_sanitize_slot`, confidence 0.90; commit it so `grep>=1` each, sha256 matches HEAD, `git diff 219d24ae..HEAD` nonempty. The 4 old harness copies are partial and cannot substitute (parent handoff do_not_assume #9).
2. **Unit tests**: provision `tests/test_kernel_param_inherit.py` passing B1/B4/D1/E1/C2/B2/B3/B5 (run with `PYTHONPATH=src` or installed package; the repo currently fails collection without PYTHONPATH).
3. **Durable census**: provision `data/webarena_verified_v2.json` (pre-existing committed file) or a verified static export with pinned sha256; alternatively make the pinned Docker image durable in CI (persistent pull, runnable within budget — the 110 s container probe timed out here).
4. **Re-execute the identical frozen binding gate** (EXECUTABLE/binding/zero-template/false_accept/UNKNOWN/ECE via deterministic `_matches` + PC1/PC2 + NC1/NC2 + B-LITERAL) on >=10 zero-overlap B tasks before any 60-task multi-family spend.
5. LLM economics (F3/F4) additionally require an API key and the runtime honest-cost sum-counters harness (trajectory-grouped B=5000, |rho_shuffled|<0.20).

`continue` decision and next direction belong to the independent AUDIT → DIRECTOR chain; EXECUTE makes no recommendation beyond the frozen production consequence: "If MEASUREMENT_INVALID … fix durable src integration + file-based census before re-testing economics; LLM absence alone preserves binding information."