# EXP-FRONTIER-36306528608 — EXECUTE report

- **Lane**: frontier
- **Claim**: C-CROSSSITE
- **GitHub run id**: 36306528608
- **Status**: `MEASUREMENT_INVALID`
- **Outcome**: `INCONCLUSIVE`
- **Frozen inputs**: unmodified. `freeze.json`'s three hashes match `prereg.md`, `request.json` and `spec.json` on disk, verified before and after execution.

This report explains and interprets `result.json`. Where it states a number, that number is
in `result.json` under the same name. It does not exceed the frozen claim.

---

## 1. What was executed, in one paragraph

The frozen design was executed as written: the prereg §4.1 calibration procedure, then the
screen over all 15 frozen candidate sites in the frozen order with no substitution, then
action-gating object detection and the §11 re-derivable classification, then the arm-phase
gate. 299 HTTP GET requests were issued to 16 hosts. **Zero non-GET requests were sent**, so
no write leg was exercised and no third-party system was mutated. The arm phase did not run,
because the frozen design admits it only on a qualifying site set and the screen admitted
zero sites. Every arm metric is therefore `null` — not `0.0`, and not "passing".

---

## 2. The primary result: the frozen primary metric is missing, and must stay missing

`rederivable_fraction`, the frozen primary metric, is **`null`**. It is not 0.0, not 1.0, not
anywhere in between. It is unmeasured, for two independent reasons that are themselves raw
observations:

**(a) The calibration anchor is factually wrong.** The prereg froze `https://httpbin.org/forms/post`
as a *known positive* and stated that it "returns an HTML form with a CSRF-like token
(`<input name="csrf_token" ...>`)" whose "csrf_token rotates or is session-bound". As served
on 2026-09-27 it contains no such input. Its single POST form is the HTML5-spec pizza-order
example, with inputs `comments, custemail, custname, custtel, delivery, size, topping`. It
fails C2, C3, C4 and C5. The prereg was frozen at 08:40 UTC the same day this ran, so the
anchor was already wrong **at freeze time** — this is a DESIGN-phase error, not substrate
drift during the run.

This matters more than a single failed site, because the calibration gate is the only thing
that was supposed to certify the screen can detect action-gating structure when it is
present. Without it, "0 of 15 sites qualify" cannot be distinguished from "the screen is
incapable of detecting gating structure". That is a false-zero risk, and this packet cannot
exclude it.

**(b) The conjunction is strict and the Web did not satisfy all of it.** Per-criterion pass
counts over the 15 frozen candidates: C1 13, C2 4, C3 2, C4 4, C5 2, C6 14, C7 14. The two
sites that pass C3 (real CSRF token gates) both fail C5. The two that pass C5 both fail C3.
No site in the pool is simultaneously token-gated, multi-hop and state-dependent.

---

## 3. The decision rule: the mechanical branch is reported, and deliberately not applied as a falsification

The frozen §14 decision table selects **ROW_1** mechanically (`< 3 qualifying sites`), and
that selection is preserved verbatim in
`metrics.decision_rule_branch_mechanically_selected` so an auditor can recompute it.

ROW_1 is **not** encoded as `outcome=FALSIFIES`. Its stated interpretation in prereg §4.4 is
*"Re-derivable surface = 1.0 (or unmeasurably high) in this substrate class because no
action-gating structure exists to require cross-episode state."*

**This run's own raw evidence contradicts that premise.** 25 action-gating objects were
detected on 8 credential-free sites. Four of them are server-minted-CSRF-token-gated POST
objects, on two sites, and their tokens are provably not re-derivable (§4 below). So the
precondition ROW_1 relies on — that no action-gating structure exists — is false here.

`research/EXPERIMENT_PACKET.md` §1 forbids converting a missing measurement into a negative
result. ROW_1's branch label was derived from a *count* (0 qualifying sites) that this run
demonstrates is not a valid indicator of the thing the branch *asserts*. The honest encoding
is `INCONCLUSIVE`, with the mechanical branch reported separately. **This is the single most
important thing in this packet, and it is a finding about the instrument, not about C-CROSSSITE.**

A second-order point: the frozen design's own text contains the protection. §4.4 forbids
substituting always-200 read-only JSON endpoints, which is exactly the substitution that
would have produced a confident, wrong `FALSIFIES`. That constraint did its job here.

---

## 4. The positive finding: real, non-re-derivable action gates exist on credential-free sites

This is the substantive new evidence, and it is a bounded positive about the *substrate*, not
about any mechanism.

The screen's C3 criterion — a declared non-GET form with an input named
`csrf|token|nonce|_token` — fired on two real, publicly reachable, credential-free sites:

| Site | Form page | Hops from root | Token field |
|---|---|---|---|
| `gitlab.com` | `/-/trial_registrations/new/` | 1 | `authenticity_token` |
| `en.wikipedia.org` | `auth.wikimedia.org/enwiki/w/index.php?title=Special:CreateAccount` | 2 | `wpCreateaccountToken`, `wpEditToken` |

A named token field is not a token. The prereg §11 protocol asks whether the token *value*
is obtainable from one unconditional GET of the root, so the value was measured directly, by
probing each target from **3 independent fresh sessions** (new opener, new cookie jar, no
reuse):

| Target | Field | Sessions | Distinct token values |
|---|---|---|---|
| `gitlab.com/-/trial_registrations/new/` | `authenticity_token` | 3 | **3** |
| `auth.wikimedia.org/.../Special:CreateAccount` | `wpCreateaccountToken` | 3 | **3** |

Response body hashes also differed in 3 of 3 sessions on both targets. So these tokens are
minted per request/session and **cannot** be obtained by re-deriving from a root observation.
They are exactly the kind of object over which cross-episode state would have value, and
they are reachable with stdlib HTTP and no credentials.

Two boundaries on this finding, stated plainly:

- It establishes that a **server-minted, non-re-derivable gate exists and is visible** to a
  credential-free stdlib HTTP client. It does **not** establish that the correct token
  authorizes the action. No write was exercised, deliberately — submitting those forms would
  create real accounts and trial subscriptions on third-party production systems.
- It does **not** overturn the parent packet's `0.000` session-scoped identifiers. That was
  measured on five always-200 read-only JSON APIs. Different sample, different answer. Neither
  packet establishes a program-level prevalence, and this packet's denominator is objects on
  2 of 14 reachable sites, which is not comparable to any registry statistic.

Identifier inventory, for the record: 1696 instances (1643 `json_id_field`, 24 `url_path_id`,
14 `named_token_input`, 9 `hidden_form_token`, 6 `server_minted_csrf_token`), of which 23 are
session-scoped and occur on exactly 2 sites.

---

## 5. The diagnostic prevalence number, and why it is not the answer

Applying the frozen §11 protocol to the 25 detected objects:

```
rederivable_fraction (diagnostic) = 1 / 25 = 0.04
95% CI, site-clustered bootstrap, 10000 resamples, seed 36306528608 = [0.0, 0.2]
equal-weight per-site mean = 0.167 across the 6 sites that produced objects
```

Both numerator and denominator are span counts, so the units are consistent — this repairs
the parent packet's distinct-identifier-keys-over-spans ratio, whose same data gave 0.060 or
0.50 depending only on the denominator.

**It is not the frozen primary metric and the frozen thresholds must not be read against it.**
It is computed over every object detected on all reachable frozen candidates, not over a
qualifying site set, and it rests on 6 sites with a wide interval. It happens to sit on the
H1 side of 0.3; that is a coincidence of a diagnostic sample and confers no support on H1,
which remains unevaluated.

---

## 6. Cost basis

The frozen prereg §8 body-sensitive observation was measured **on this substrate**, not
imported: mean **2278.4** cl100k_base tokens per page observation over 232 observations
(median 2120, min 151, max 10089, total 528578), host means from 151 on small pages to
6208.2 on `en.wikipedia.org`.

This is **not** comparable to the parent packet's 119 tokens/observation: that was measured on
tiny JSON APIs with a body-omitting representation. The two are different quantities on
different substrates and must not be differenced. The parent handoff's warning that 119 is
not reconcilable with the 763.06-token floor still holds, and this packet adds that neither
figure should be treated as a program-wide per-observation cost.

Token-to-latency and token-to-dollar remain **UNKNOWN** by explicit declaration. No economic
claim is made.

---

## 7. Reproducibility

The Web is dynamic and candidate roots redirect off-host, so a single pass cannot distinguish
"this site has N objects" from "this visit landed on N of them". A second independent live
pass over the 6 object-yielding sites reproduced the first **exactly**: identical object
counts (8, 3, 9, 3, 1, 0), identical C1–C7 results, stable qualifying set of 0.

An earlier development pass showed an apparent run-to-run difference (36 spans vs 25). That
was traced to the producer's own instrument — a first object detector that wrongly counted
shallow non-GET forms with no token and no state — and **not** to Web nondeterminism. That
detector was corrected to implement the frozen C2 (a)(b)(c) logic, and its output was
discarded rather than retained. **No claim in this packet rests on the discarded pass.** Slow
drift over weeks remains uncontrolled.

---

## 8. Three screen defects found at source (for whoever repairs the instrument)

1. **C3 does not test credential-free executability.** C3 counts declared non-GET forms with
   a token-named input; C7 only tests the site *root*. A site can therefore pass C3 via a
   login-walled form. Both C3 passes here are account-creation and trial-registration forms —
   precisely the forms most likely to be credential-walled. Whether they are executable
   without credentials is untested.
2. **C7 can false-positive on an authorization wall.** C7 treats an HTTP 403 root as a login
   wall, but credential-free services commonly answer 403 to a default agent. Verified at
   source: `https://httpbin.org/status/403` returns 403 to an unauthenticated GET and would be
   scored as a login wall despite requiring no credentials. **Latent here, not active** — all
   14 reachable roots returned 200, so no C7 verdict was produced by a 403.
3. **Rooting at the host root can screen the wrong document.** The screen roots each site at
   its host root, so a candidate whose root redirects away from the surface of interest is
   evaluated on the redirect target. This is what happened to `https://postman-echo.com`, whose
   root now 302-redirects to `www.postman.com` while its `/get` API still returns 200; it was
   screened on a documentation page and failed C1. This is a specification ambiguity in the
   frozen design, resolved here by the most literal reading, and it is a candidate
   contributor to the 0-of-15 result.

---

## 9. Controls: what fired and what did not

| Control | Status |
|---|---|
| `SCREEN_CALIBRATION_GATE` | **FAIL** — anchor does not satisfy the frozen screen |
| `SITE_SELECTION_SCREEN` | **FAIL** — 0 of 15 admitted, minimum 3 |
| `SCREEN_REPEAT_PASS_REPRODUCIBILITY` | **PASS** — 6/6 sites reproduced exactly |
| `TOKEN_STABILITY_CROSS_SESSION_PROBE` | **PASS** — fires on both real targets |
| `NO_NEW_INFRASTRUCTURE_CONSTRAINT` | **PASS with disclosed deviation** — `pip install tiktoken` |
| `NO_POST_FREEZE_SITE_SUBSTITUTION` | **PASS** — all 15 frozen URLs screened in order |
| `SAME_UNIT_PREVALENCE_ESTIMATOR` | **PASS** — units repaired |
| `ONE_DECLARED_COST_BASIS` | **PASS** — body-sensitive, UNKNOWN declared |
| `PRODUCT_KERNEL_HARD_DEPENDENCY` | **FAIL** — not Frontier's to fix |
| `PRIMARY_ENDPOINT_DYNAMIC_RANGE` | **unknown** — endpoint never evaluated |
| `THRESHOLD_SATISFIABILITY` | **unknown** — no pilot was possible |
| 7 frozen arms | **NOT_RUN_GATED**, all metrics `null` |

The two PASS rows that matter most are the two that are *not* frozen controls:
`TOKEN_STABILITY_CROSS_SESSION_PROBE` is the only positive detection in the packet, and it
demonstrates that the re-derivability question **is** decidable on this substrate with stdlib
HTTP and no credentials. That is the reusable instrument result.

`PRODUCT_KERNEL_HARD_DEPENDENCY` was re-verified directly at HEAD `67e1393b`:
`src/spider/kernel.py:90` hard-codes `confidence=0.5` in `distill()` while `resolve()`
requires `min_confidence=0.8` (lines 59, 61, 114), and `distill_parameterized` is absent
under `src/`. Per the mandate, this packet records the surface measurement and **issues no
transfer verdict**.

---

## 10. Consequence for the program

The allocation asked whether there is anything for cross-episode inheritance to amortize
over. The bounded answer this run supports:

- The surface is **not zero**. Real, server-minted, non-re-derivable CSRF gates exist on
  credential-free public sites reachable with stdlib HTTP and no credentials, at 1–2 hops.
- The surface is **not measured** on a screen that has demonstrated its own detection power,
  because the calibration anchor was wrong at freeze.
- Therefore C-CROSSSITE transfer is **neither unblocked nor falsified** by this packet. It
  stays exactly where it was.

The cheapest next action is a **calibration repair, not another frontier run**: re-anchor the
screen on a site verified to contain the structure it is meant to detect, and fix defects 1
and 2 in §8 so the conjunction measures real gating rather than markup coincidence. That is
substrate and instrument work, allocated to Runtime as owner of `C-MEAS-VALID`; it is not a
seventh frontier packet on this axis.

**And one hard dependency remains upstream of any inheritance claim**: the product kernel
cannot execute an inherited mechanism. Until that lands, no amortization result on this
substrate — however well measured — can become a product claim. That is Product's allocation,
not Frontier's.

**What this packet explicitly does not do**: it does not record a bounded negative for
C-CROSSSITE; it does not close the Frontier lane, the C-CROSSSITE domain, or the inheritance
question; it does not re-enter the TERMINATED `C-RESIDUAL-NOVELTY` thread; and it updates no
other lane's claims.
