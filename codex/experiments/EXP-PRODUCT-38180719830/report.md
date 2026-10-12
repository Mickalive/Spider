# EXP-PRODUCT-38180719830 — Execution Report

**Lane:** product — **Claim:** `C-PARAM-INHERIT` — **Status:** COMPLETE — **Outcome:** SUPPORTS

This report interprets the frozen certificate measured by `harness/run_certificate.py`
(the FROZEN RUNNER materialized byte-exact from `prereg.md` section 14). It stays inside
the frozen claim and decision rule. It does **not** advance `C-PARAM-INHERIT` (it remains
`EXPERIMENTAL` in the claim registry in every branch of the frozen decision rule), does
**not** promote the carrier into Product Core, and does **not** compare COLD,
INSTRUCTIONS or RETRIEVAL arms (the four-arm `C-LLM-INHERIT` benchmark was explicitly
excluded by the Director mandate) and does **not** measure economics.

---

## 1. Frozen scope (what this transaction is)

| Element | Frozen value |
|---|---|
| Treatment | carrier kernel `src/spider/kernel.py` — byte-identical to git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` (sha256 `718efa6a...`) |
| First-run precondition | shipped literal kernel (blob `cfec98660b...`, sha256 `46929b3a...`) — observed pre-install |
| Instrument | FROZEN RUNNER (sha256 `a114804c391aa8360d0616fa27a4b217783abea4f005a29f87d22f7566daf2f3`) |
| Decision rule (prereg §17) | `SUPPORTS` iff D0–D4 AND V8 all PASS; `FALSIFIES` iff any D-clause FAILs with V8 held; `BLOCKED`/`MEASUREMENT_INVALID` iff V8 or identity preconditions fail |
| Enforced scope | certificate gate for a pending promotion; no claim advance, no VALIDATED, no economics, no four-arm benchmark |
| Run mode | EXECUTE, `probe_mode=false`, `sources_are_git=true`, repo root auto-detected upward, **no `EXP_*` environment overrides** |

## 2. RAW EVIDENCE (verbatim, uninterpreted)

Stored at `run_certificate.out.json` (sha256 `17c442b0...`, 7718 bytes) and
`run_certificate.log` (sha256 `50e0b058...`).

- Runner exit code `0`. stdout is one JSON document; stderr contains only the unittest
  banner `Ran 3 tests in 0.002s` / `OK` (regression output is routed to stderr).
- Identity facts in the certificate JSON:
  - `pre_install_sha256 = 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`
    (== shipped literal; the D0 precondition "first run on the literal" held).
  - `carrier_source_sha256 = 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`,
    `carrier_git_blob = b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`.
  - `post_install_sha256 = 718efa6a...`, `post_install_git_blob = b15ed848...`
    — installed file byte-identical to the frozen carrier blob.
- Positive probe: unseen `item-007` → `ResolutionStatus.EXECUTABLE` @ confidence `0.9`,
  bound action `GET http://127.0.0.1:33173/api/items/item-007`, fixture returned status
  `200`, `verify == true`. Mechanism `mech-783a6a3f99ee47b8`, slots `["item"]`,
  induced support `{"item": "^item\\-00[0-9]{1}$"}`.
- Negative probes (7/7 with `bound_action == null`): `item-010`/`item-999`/`item-xyz` →
  `EXPLORE` ("parameter 'item' outside inferred support"); `{}` and `{"wrong_key":"x"}` →
  `EXPLORE` ("missing required parameter 'item'"); `delete_item` and `never_seen_intent` →
  exactly `UNKNOWN` ("no applicable validated mechanism").
- Counters at the frozen snapshot: `retrieval_calls 9`, `verification_calls 1`,
  `repair_attempts 1`, `model_calls 0`, `model_tokens 0`, `http_requests 0`; equal to the
  invocation transcript at that point (`expected_from_transcript` `9/1/1`).
- Controls: literal ablation `has_distill_parameterized == false`; PC-EXACT-REPLAY 5/5
  `EXECUTABLE` (item-001..005); regression suite `tests_run 3, failures 0, errors 0`.
- V8 binding: `prereg_sha_matches true`, `runner_source_matches_frozen_block true`,
  `artifact_hashes_match true`.

## 3. OBSERVATIONS (what the runner did, directly observed)

1. V8 was enforced in EXECUTE mode: `freeze.json` was present and readable; prerеg hash,
   runner-source equality and all five freeze artifact hashes matched.
2. First-run identity held: the installed pre-run kernel was the shipped literal
   (sha `46929b3a...`), so the D0 first-run precondition was satisfied and no
   substitution/stop-trigger path fired.
3. The literal kernel ablated cleanly: in a hermetic temp package with the same
   `models.py`/`registry.py`/`__init__.py`, the literal has no `distill_parameterized`.
4. The instrument replaced `src/spider/kernel.py` with the carrier bytes; file `cmp` ==
   blob `b15ed848...` and sha `718efa6a...`.
5. Exactly one fixture HTTP request was made (the D1 bound-action execute); the kernel's
   `http_requests` counter reads 0 because `TrajectoryCounters` does not auto-increment it
   (documented in prereg §10) and the certificate does not gate on it.
6. After the run the working tree intentionally contains the carrier at
   `src/spider/kernel.py` — the treatment outcome per prereg §16 step 6; nothing was
   reverted or committed.

## 4. DERIVED MEASUREMENTS (clause verdicts)

| Clause | Verdict | Key evidence |
|---|---|---|
| V8_FREEZE_BINDING | PASS | all three binding clauses true; runner sha `a114804c...` |
| D0_IDENTITY | PASS | pre=literal `46929b3a...`, source=carrier `718efa6a...`, post=carrier blob byte-identical |
| D1_POSITIVE | PASS | unseen in-support id bound EXECUTABLE@0.9; action URL carries the id; fixture 200; verify true |
| D2_NEGATIVE | PASS | 7/7 refusals: null action, recorded reason, status≠EXECUTABLE; EXPLORE for OOS/missing (correct reason class); exactly UNKNOWN for wrong-intent/no-applicable |
| D3_COUNTERS | PASS | 9/1/1 counters == transcript at snapshot; model_calls=0, model_tokens=0 |
| D4_CONTROLS | PASS | ablation absent; replay 5/5; regression 3/3 green |
| **Certificate** | **PASS → status COMPLETE / outcome SUPPORTS** | all clauses above |

Confidence `0.9` and the support regex are deterministic arithmetic outputs of the 5
induction observations (prereg §7, V1), not stochastic estimates.

## 5. INTERPRETATION (bounded, per frozen decision rule)

This transaction certifies exactly what it was frozen to certify:

- The carrier kernel, byte-pinned to blob `b15ed848...` and installed on top of the
  verified shipped literal, resolves a held-out identifier inside its induced support to an
  executable bound action (verified against the fixture), refuses everything outside the
  induced support or missing the required parameter correctly (EXPLORE), and answers
  EXACTLY UNKNOWN for wrong or absent intent — with inheritance-path counters (retrieval 9,
  verification 1, repair 1) matching the recorded transcript and zero model calls on the
  path.
- The literal kernel cannot produce this behavior (ablation control), so attribution of the
  certificate to the installed carrier is supported; the 5/5 exact-replay and 3/3 pruning
  regression confirm the carrier preserves inherited behavior on the trained set.
- Therefore the frozen promotion GATE is enabled: `certificate PASS` on `C-PARAM-INHERIT`
  with V8 enforced. **The carrier is still NOT promoted**: per prereg §17, promotion
  additionally requires the mandate's independent audit PASS on this certificate and the
  DIRECTOR's verdict. `C-PARAM-INHERIT` remains `EXPERIMENTAL`; this packet explicitly does
  not claim VALIDATED, does not endorse a Product Core mechanism, and takes no position on
  the four-arm benchmark deferred to `EXP-LLM-INHERIT-*`.

Consequences were pre-committed in prereg §17 and are unchanged:
- Positive (this run): the promotion gate is satisfied for the frozen carrier identity;
  the DIRECTOR may, after an independent audit PASS, promote the byte-pinned carrier or
  book SUPPORTS evidence for `C-PARAM-INHERIT` at the promotion gate without further
  product-lane measurement on this transaction.
- Had D0–D4 not all passed with V8 held, this report would have recorded `FALSIFIES` (or
  `MEASUREMENT_INVALID`/`BLOCKED` for binding/identity failure) and the gate would remain
  closed; no such branch fired.

## 6. Validity and limitations (unchanged from prereg §11; no new threats observed)

- Deterministic stdlib-loopback substrate; no RNG, network egress, credentials, browser or
  model calls (V1, V2).
- Three-part identity binding held end-to-end; V8 enforced at runtime (V3, V8).
- Held-out id sits inside the induced support; the audited failure-mode id `item-010`
  (two-digit suffix) is used as an out-of-support negative exactly as frozen (V5).
- The certificate's `http_requests` counter is 0 by construction (runner-side; prereg §10);
  the actual fixture request count (1) is recorded in observations.
- Disclosed limits: conservative support induction (item codes must match the induced
  grammar — the bank exploits this deliberately); execution correctness verified only for
  the GET/JSON shape the induction encodes; latent pretrained knowledge of the carrier's
  source cannot be excluded — attribution rests on the byte-pinned blob identity plus the
  literal ablation, not authorship.
- Coupled with this bounded certificate, the inherited `do_not_assume` from the parent
  handoff (`EXP-PRODUCT-37989728440`, SUPERSEDE) remains in force: no inference about the
  four-arm `C-LLM-INHERIT` properties, no economics claim, and no generalization beyond the
  carrier's induced support.

## 7. Artifacts

See `result.json#artifacts` and `provenance.json` for exact paths and sha256 hashes of the
runner source (`a114804c...`), raw stdout (`17c442b0...`), raw stderr (`50e0b058...`) and
the treatment outcome file `src/spider/kernel.py` (`718efa6a...`).