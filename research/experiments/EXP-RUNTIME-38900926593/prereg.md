# EXP-RUNTIME-38900926593 — Preregistration (frozen before execution)

Lane: **runtime**. Target claim: **C-FRESHNESS**. Director mandate action: **REOPEN** (cognitive reset, `parent_handoff_disposition` **PARK**), `design_contract_version = 2`.

`spec.json` is the machine-binding source; where wording differs, `spec.json` governs. Do not edit after `freeze.json` exists.

## 0. Director mandate trace

The Global Research Director (cycle 38900534676) REOPENs the idle Runtime lane onto the shared freshness/denylist substrate instead of the parked delta-repair thread:

> "After parking the 12-cell delta-repair re-admission bar under its frozen stop rule (no third N increase on localhost), can Runtime deliver the shared freshness/denylist substrate: keyed to the frozen intrinsic classifier and window ladder, what is the measured validity horizon of an anchor-built intrinsic denylist (false-accept/false-reject with endpoint-clustered bounds) and what minimal second-egress support can Runtime provision or precisely block — thereby unblocking Physics Q2/Q3 and the freshness-guard calibration that first-party persistence economics consumes?"

Dependencies: `["intel"]` (discharged in §10, not re-tested). The inherited `parent_handoff` (EXP-RUNTIME-38835192343, PARK) is continuity evidence only: its stop rule is honored (§9), and no part of this design re-runs, varies, or re-admits the 12-cell localhost program. The mandate's fail-loud clause is implemented as frozen branches: if neither the horizon measurement nor egress support materializes, the packet records exact blockers and PARKs with no outcome-bearing re-run.

## 1. What is tested

Two coupled substrate questions, executed in frozen order (certificate first, ladder second):

- **Q-E (egress provision-or-block).** From this runner environment, can Runtime provision a minimal second independent egress for the frozen barrier/denylist substrate — or else certify with exact receipts that no second egress exists? The certificate enumerates local paths (interfaces, routes, proxy env, global IPv6) and observes the public egress IP via ≥3 independent echo services. Expected outcome per pre-freeze probe: **E_BLOCKED** (single IP `135.119.238.192` across httpbin/ipify/ifconfig; one NIC/default route; no proxy env; link-local-only IPv6). A surprise second path triggers the pre-registered **halt** (record, `INCONCLUSIVE`, no unfrozen science), never improvised cross-vantage work.
- **Q-H (validity horizon).** Keyed to the frozen intrinsic classifier (§2, verbatim incl. the 262144-byte search window) and the frozen window ladder (prefix rungs 0/300/900/1800) plus one pre-registered extension rung (3600): what is the measured validity horizon of an anchor-built intrinsic denylist — per-class `CLASS_PERSISTENCE`, `DENYLIST_FALSE_ACCEPT` / `DENYLIST_FALSE_REJECT` with endpoint-clustered bounds? Does validity hold through the S1 right-censoring limit (1800 s, replication prefix) and through 3600 s (extension)?

This design **replicates** EXP-PHYSICS-38074818597 (S1_STATIONARY, audit PASS) rung-for-rung on its 0–1800 prefix — same pool, same classifier, same estimator, same thresholds — with fresh lane/code/seeds and stronger body retention (§2.1), and **extends** it past the exact limitation S1 and the Physics handoff name (horizon right-censored at 1800 s; single vantage). The vantage axis itself is NOT varied here: extending the horizon is a distinct-extension measurement, not a substitute single-vantage run for the Physics vantage question (see §11).

### 1.1 Branch design (all branches reachable; calibration in §6)

- **S1_EXTENDED**: `READ_1800` (S1 conditions at delta_ref) AND `READ_3600` (S1 conditions at delta_ext). Horizon ≥ 3600 s, right-censored.
- **S1_HELD**: `READ_1800` holds but `READ_3600` fails (breaking class reported). Replicates S1 and bounds the horizon in (1800, 3600].
- **S0_BREAK**: measurement valid but `READ_1800` fails (breaking class among `intrinsic_break_1800` / `denylist_violation_1800` / `no_anchor_information_1800`). Bounded change evidence vs S1 on this window.
- **MEASUREMENT_INVALID**: reserved exclusively for prerequisite/control failure (§5, §7); never a science branch.
- **E_UNEXPECTED_PATH (halt)**: complete the certificate, record the second-path observation, take no S-branch read, return `COMPLETE`/`INCONCLUSIVE`.

## 2. Frozen intrinsic classifier (response-intrinsic, no history leakage)

Each response is classified from its own stored fields only (status, `cf-mitigated`, first 262144 body bytes, transport error string). The frozen challenge-marker regex is transcribed verbatim from EXP-PHYSICS-38074818597 §2:

```
CHALLENGE_RE_LITERAL = (?i)(just a moment|cf-browser-verification|cf[-_]chl[-_]|challenge-platform|cf-challenge|cdn-cgi/challenge|attention required|checking your browser|enable javascript and cookies|verify you are human|please complete the security check|g-recaptcha|hcaptcha|recaptcha|cf-turnstile|<title>\s*just a moment)
```

| class | rule |
|---|---|
| `CLEAN` | status 2xx AND body does not match `CHALLENGE_RE` (first 262144 bytes) |
| `RATE_LIMIT_429` | status == 429 |
| `BLOCK_403_CHALLENGE` | status == 403 AND (`cf-mitigated: challenge` OR body matches `CHALLENGE_RE`) |
| `UNAVAILABLE_403` | status == 403 without any challenge marker |
| `TRANSPORT_ERROR` | no HTTP response (DNS/connect/TLS/timeout); one attempt, no retries |
| `OTHER_NONBARRIER` | any other status, OR a 2xx carrying a challenge marker |

`barrier_set = {RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`; `intrinsic_classes = {BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`. All classes are functions of a single response's stored fields only, so conditioning on the anchor state is not label leakage.

**Implementation trap (found by the DESIGN probe, frozen as a requirement):** bare `urllib` raises `HTTPError` on 429/403/404/500. EXECUTE MUST catch `HTTPError` and capture code+body+headers as the response; recording error statuses as `TRANSPORT_ERROR` is an instrument defect and fails `NC_CLASSIFIER_REPRODUCIBILITY` by construction.

### 2.1 Body retention (Runtime validity upgrade over S1)

S1 stored body SHA-256/length only, so its challenge-marker arm is not exactly re-computable by AUDIT (cf. the EXP-GRAPH-37950584469 audit lesson: "packet stores only body_sha256 per record, no bodies"). This packet stores, for **every** observation, the **first 262144 body bytes** (base64 in `raw/records.jsonl.gz`; full body when shorter, plus full length and full-body SHA-256; bodies beyond the window flagged `truncated=true`). Because the classifier itself reads only the frozen 262144-byte window, AUDIT recomputation on stored bytes is **exact** for classification purposes on every observation. `NC_CLASSIFIER_REPRODUCIBILITY` gates on 0 mismatches.

## 3. Frozen sweep protocol, egress certificate, and strata

**Unit**: `(endpoint, sweep_index)`; anchor = sweep 0 (T0). The anchor-built denylist = the set of T0 intrinsic endpoints.

**E-certificate (runs FIRST, ~15 requests, no ladder commitment).** Frozen procedure: (1) enumerate local paths — interfaces, routes, `*PROXY*` env, global IPv6 route + test; (2) observe public egress IP via the 3 frozen echo services (+ best-effort ASN via ip-api, descriptive only); (3) `E_BLOCKED` iff a single enumerated path AND ≥2 echo services agree on one IP string; `E_UNRESOLVED` iff echo disagreement with no majority; unexpected distinct second-path IP → `E_UNEXPECTED_PATH` halt. Tor/VPN/WARP overlays are **excluded a priori and not attempted**: Tor exits are publicly listed and widely challenged/blocked, so overlay blocking would inject client-identity-dependent responses indistinguishable from endpoint-intrinsic barriers — a construct confound for this science, not a clean second vantage — and overlay routing is not minimal provisioning. Credential-requiring paths are out of scope (credential-free mandate).

**Ladder** (nominal offsets, seconds): `[0, 300, 900, 1800, 3600]`; `delta_ref = 1800` (S1-comparable primary), `delta_ext = 3600`. Rungs labeled nominal; per-endpoint actual deltas recorded. `delta_ref` actual must be ≥ 1500 s and `delta_ext` actual ≥ 3300 s or the run is `MEASUREMENT_INVALID`. One echo request per sweep records the sweep egress IP; any cross-sweep change (`EGRESS_ROTATION`) completes the ladder, preserves the raw, and returns `MEASUREMENT_INVALID` (fail-closed; the rotated ladder is preserved evidence, not a science read).

**Request policy** (verbatim-frozen): GET only, follow ≤ 5 redirects, 30 s timeout, TLS on, **no retries, one attempt per observation**. Frozen User-Agent `SPIDER-research2/1.0 (+credential-free intrinsic-denylist substrate probe)`, `Accept: */*`. No authentication, JavaScript, credentials, cookies (no cookie processor installed = fresh-jar-equivalent by construction). Python 3.12 **stdlib only**; no lane-module imports. Per-sweep probe order is a fresh seeded permutation (seed `38900926593`, not S1's), inter-endpoint gap 0.30 s.

**Induced probe dropped (explicit):** the burst/recovery probe of S1 Q3 is not carried forward — S1 settled class-conditional rate transience (`RATE_RECOVERY_HALF_LIFE` 2 s) and the mandate does not ask for it. Ambient 429 onset/recovery counts are kept as non-gating diagnostics. This removes ~65 load requests and the burst self-induction confound.

**Strata** (fixed, NOT outcome-selected; `stratum_stress` members are ordinary ambient members here): stress set (5 endpoints, §spec) and intrinsic-candidate set (6 endpoints, §spec) are reported diagnostic subgroups; primary inference is the full 57.

## 4. Metrics, baselines, controls, stable identifiers

- Primary `STATIONARITY_SKILL(delta)` = plug-in binary MI `I(B_T0; B_delta)` with `B_EXCHANGE` permutation p (10000 shuffles, seed 38900926593) and endpoint-clustered bootstrap 95% CI (cluster = `registrable_domain`, 10000 resamples, seed 38900926593).
- `CLASS_PERSISTENCE[c at delta]`, `INTRINSIC_PERSISTENT_*`, `DENYLIST_FALSE_ACCEPT/REJECT_*`, `DENYLIST_INTRINSIC_VALID_*`, `STAT_SIG_*`, `READ_1800`/`READ_3600` per `spec.json:decision_rule` (thresholds: persistence ≥ 0.80, FA/FR ≤ 0.20, SKILL ≥ 0.05 nats, p < 0.05, CI lower > 0, n_t0 ≥ 3 both sets).
- Secondaries: `STATIONARITY_SKILL_BY_RUNG`, `STATIONARITY_SKILL_NO_STRESS` (52-endpoint replica), `MI_CLASS`, `CLASS_PERSISTENCE` (all classes), `INTRINSIC_PERSISTENCE`, `DENYLIST_HORIZON` (contiguous valid prefix over {300,900,1800,3600}, censored at 3600), `DENYLIST_SKILL` (vs `B_CONSTANT_USABLE`, non-gating), `ANYBARRIER_FALSE_ACCEPT`, ambient 429 onset/recovery counts, anchor counts.
- Baselines: `B_EXCHANGE` (primary strong null), `B_CONSTANT_USABLE` (floor), `B_MARGINAL`, `B_LASTSWEEP` (diagnostics).
- Controls: `PC_SYNTHETIC_STATIONARY_EXTENDED` (power ≥ 0.80 at rho=0.98), `PC_ORACLE_BARRIER` (live 429/transport/403-plain), `NC_SYNTHETIC_EXCHANGEABLE` (FP ≤ 0.05), `NC_CLEAN_ORACLE` (live 200s), `NC_CLASSIFIER_REPRODUCIBILITY` (0 mismatches), `C_EGRESS_CERTIFICATE`, `C_EGRESS_STABILITY`, `C_PROBE_SELF_INDUCTION` (reported). Stable identifiers, e-states, policies and seeds in `spec.json` (seeds 38900926593; NC synthetic 38900926594).

## 5. Decision rule and thresholds

Frozen thresholds: `delta_ref = 1800` (actual ≥ 1500); `delta_ext = 3600` (actual ≥ 3300); persistence ≥ 0.80; `tau_FA = tau_FR = 0.20`; `alpha = 0.05`; `delta_SKILL = 0.05`; `pc_power_min = 0.80`; `nc_false_positive_max = 0.05`; `min_t0_intrinsic = min_t0_barrier = 3`; 10000 permutations/resamples. Branch precedence: (1) `MEASUREMENT_INVALID` on any prerequisite/control failure (incl. `E_UNRESOLVED`, rotation, unmet anchor floors, oracle failure, classifier mismatch, PC/NC failure); (2) `E_UNEXPECTED_PATH` halt; (3) `S1_EXTENDED` on `READ_1800 AND READ_3600`; (4) `S1_HELD` on `READ_1800 AND NOT READ_3600` (breaking 3600-class reported); (5) `S0_BREAK` otherwise (breaking 1800-class reported).

Claim ceiling: **C-FRESHNESS stays EXPERIMENTAL** in every science branch (already the effective status via EXP-GRAPH-37992949248); `S1_EXTENDED`/`S1_HELD` retain it with an extended/quantified horizon, `S0_BREAK` retains it with a bounded horizon. No `VALIDATED`/`PRODUCT_CORE`/promotion. No events for any other claim.

## 6. Null calibration (pre-freeze, non-outcome-bearing)

The mandated null `B_EXCHANGE` and the exact extended rule (both deltas, CI-lower clause, intrinsic-set-only denylist) were calibrated on synthetic worlds with the estimator that EXECUTE will use (PERM=500/BOOT=1000 documented approximation of the frozen 10000; no Web outcomes; DESIGN-local script, deleted before freeze; EXECUTE re-verifies at full size):

| synthetic world | result (300 replications) | branch selected |
|---|---|---|
| `PC98` planted-stationary rho=0.98 | S1 294/300 (power 0.98 ≥ 0.80) | S1_EXTENDED regime |
| `PC92` planted-stationary rho=0.92 | S1 277/300 (0.923, reported) | S1_EXTENDED regime |
| `NC_EXCHANGE` independent anchor/lag | S1 0/300 (FP 0.0 ≤ 0.05) | S0 300/300 |
| `BREAK_EARLY` durable intrinsic change by 1800 | S1 0/300 | S0 300/300 |
| `BREAK_LATE` break only at 3600 | S1 0/300, HELD 300/300 | S1_HELD 300/300 |

Both science directions and the HELD middle are arithmetically reachable (one recovery among n=3 gives FA=0.333 > 0.20; persistence ≥ 0.80 needs at most the observed stability). This calibrates the estimator, null and rule; it asserts nothing about real endpoints. (DESIGN-local calibration script sha256 `fa3f87b1f9b6d97077f01af39c9150c01310633f129c34703685e4aebfd9e8b6`, deleted before freeze.)

## 7. Attainability certificate (pre-freeze, non-outcome-bearing)

DESIGN-local probes (DESIGN-local probe script sha256 `d8d676d0a22b89d66fa715bae7d4f668cfa3e317f03deef2175bb32a6bf1bf44`; scripts deleted before freeze; EXECUTE re-verifies every floor from its own data):

- **Egress/enumeration:** single NIC (`eth0`, RFC-1918), one default route, no `*PROXY*` env, IPv6 link-local only. Public IP `135.119.238.192` (Boydton, VA, US) agreed by 3/3 echo services (httpbin, ipify, ifconfig.me); ASN-service reachable. Only the `E_BLOCKED` certificate branch is reachable; `E_PROVISIONED` is excluded as a live science branch with this evidence.
- **Universe reachability:** 12/12 fixed-subset endpoints returned classifiable responses (4× HTTP 403 — the classifier's 403 arm is exercisable here; 8× 200/202). S1's full-57 census independently showed 6 stable T0 intrinsic barriers on this egress class, so `n_t0_intrinsic ≥ 3` / `n_t0_barrier ≥ 3` are certified reachable.
- **Oracle liveness:** all 7 oracle hosts respond live (HTTP 429 ×2, DNS-fail ×1, HTTP 403 ×1, HTTP 200 ×3) — controls can fire.
- **Body retention:** subset bodies 0.5 KB–450 KB; the 262144-byte window covers classification needs exactly; gzipped raw fits the 30 MB budget.
- **Certificate verdict: SATISFIED** for the single-path extended ladder. If EXECUTE cannot re-verify the floors, the packet is `MEASUREMENT_INVALID` (the operational analogue of PARK), with the egress receipts preserved regardless.

## 8. Freeze binding

`freeze_artifacts = []` (`NOT_APPLICABLE`). No pre-existing mutable local code, task bank, dataset or fixture determines the interpretation: every interpretation-determining constant (57-endpoint universe, challenge regex + classifier, 262144-byte window, extended sweep protocol, strata, thresholds, seeds, branch precedence, egress-certificate procedure) is embedded verbatim in `spec.json` and this file. EXECUTE authors the collection/analysis code strictly as a literal realization of these frozen constants (stdlib only; must not import `research/runtime` lane modules); its hash is recorded in `provenance.json`. DESIGN-local probe/calibration material was deleted before freeze and is not an interpretation dependency.

## 9. Parent handoff accounting (EXP-RUNTIME-38835192343, PARK)

Preserved distinctions: **established** — localhost repair functionally sound (108/108, contamination 0/432), shipped-counter premise exact, priced pattern 10 WIN / 2 MARGINAL / 0 LOSS with P1/P3-L2 straddles (CIBF uppers 1.00441/1.00442), stop trigger fired at N=36; **rejected** — robust LOSS, uncorrected-CI gating, treatment-identity/drift failures; **unknown** — MARGINAL-cell resolution on unfunded substrates, residual-vs-asymmetry separability, off-localhost transfer, B3 economics; **do_not_assume** — no 12-cell SUPPORTS reading, no shipped-counter empirical win, no residual upgrade, CIBF-only gating, no off-substrate transfer, no N* amortization, no B3 pricing, no third N increase. This design complies with every item: it contains zero localhost timing work and funds no N increase.

## 10. Intel dependency accounting

`dependencies: ["intel"]` is discharged as follows (not re-tested): the citable Intel evidence is EXP-INTEL-38194362040 (`FALSIFIES` — no credential-free local class clears the minimal multi-step bar) and the mandate's representation prior (observation-representation failures masquerade as reasoning failures). The shared instrument lesson is implemented here as `NC_CLASSIFIER_REPRODUCIBILITY` with full-window body retention (§2.1) — verify the instrument channel before any mechanism claim — which is strictly stronger than S1's hash-only storage and answers the Graph audit lesson on missing bodies. No LLM observation is involved (stdlib bytes only); Intel's ELEMENTS/tree probe is not duplicated.

## 11. Self-attack log (DESIGN defects considered and closed)

- **Unreachable provision branch:** excluded `E_PROVISIONED` as a live science branch after the probe proved a single-path structure; the halt clause covers environment change without authorizing improvisation.
- **Empty HELD branch:** closed by the `BREAK_LATE` calibration row (300/300 HELD).
- **Ceiling baselines:** closed by calibration separation (PC98 0.98 vs NC 0.0) on the exact extended rule.
- **Insensitive egress control:** the certificate is a census (enumeration + agreement), not a statistical test; disagreement/rotation fail closed to INVALID, never to science.
- **Duplicate-of-S1:** the 0–1800 prefix is a deliberate independent replication (fresh lane/code/seeds + exact-recompute bodies); the new information is the 3600 extension, the egress receipts, and the replication itself. A pure-1800 rerun was rejected as a duplicate.
- **Single-vantage substitution trap:** this packet does not answer the Physics vantage question and claims nothing about cross-vantage transfer; E_BLOCKED *is* the vantage answer for this environment (exact blocker), which PARKs rather than substitutes.
- **Mid-run egress rotation:** fail-closed INVALID with raw preserved (§3).
- **Tor-as-second-egress:** excluded a priori with construct-confound reasons (§3), not silently ignored.
- **Dropped induced probe:** explicit (§3); S1's Q3 stands unchallenged.
- **Scope inflation:** one claim id; Physics/graph/product consume via evidence_refs/handoff only (§5 ceiling).

## 12. Validity threats and representation loss

V1 egress-confound: `TRANSPORT_ERROR` conflates endpoint state with vantage blocking (S1's invisioncommunity DNS case); disclosed, bounded to this vantage, gated by anchor floors. V2 time-of-day: one window; horizon claims are window-bounded. V3 challenge-marker window: JS-only challenges invisible to stdlib bytes are declared out of scope (shared with S1). V4 3600-slip: guarded by the 3300 s actual floor. V5 storage: bodies capped by window + gzip; exactness preserved for classification. Representation loss: everything except the frozen stored fields is discarded (full DOM/TLS-handshake/timing internals); the result is valid only for the frozen classifier's level of description.

## 13. Product consequences

Positive (`S1_EXTENDED`/`S1_HELD`): quantified `DENYLIST_HORIZON` (≥3600 censored, or bounded in (1800,3600]) becomes the dead-end policy's re-probe interval; the freshness-guard calibration consumes the horizon with stated FA/FR. `E_BLOCKED` receipts let Physics proceed-or-park Q2/Q3 honestly. Negative (`S0_BREAK`): static denylist not amortizable through 1800 s here — re-observe before use; horizon bounded with breaking class. No promotion in any branch (Runtime lane; experiment-local code only).

## 14. Cost

~314 HTTP requests worst-case ~340; ~80 min wall; ~30 MB gzipped raw; 0 model calls; no browser/credentials/packages. Smallest decisive batch: the certificate runs first and the ladder is a single continuous session (no repeats, no N increases).

## 15. Legacy non-duplication (record)

`LEGACY: NO_MATCH` — method and zero-hit evidence in `spec.json:legacy_check`. The R2 parent S1 is replicated (prefix) and extended (3600 + egress + bodies), never identically repeated.
