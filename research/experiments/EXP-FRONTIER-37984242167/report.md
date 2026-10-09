# EXECUTE Report — EXP-FRONTIER-37984242167

**Lane:** frontier
**Stage:** EXECUTE
**Status:** BLOCKED (result.json `status=BLOCKED`, `outcome=NOT_APPLICABLE`)
**Run:** github_run_id 38003276774 (attempt 1), branch `lab2/frontier`, base `c6edd08c`, HEAD `165a2970`
**Date:** 2026-10-09

---

## 1. Executive summary

This EXECUTE did **not** produce a web measurement, because the frozen design is **unsatisfiable as frozen**: the frozen `spec.json` admits **zero** target-pool seeds, **zero** confirmed DEEP items and **zero** confirmed hosts, and its pre-freeze control certificate is `all_verified=false` with no evidence refs. The primary metric's denominator is therefore `0` and the frozen falsifier cannot be evaluated in **either** direction. Running probes now would construct the sampling frame *after* freeze — a mutation of the frozen design — so no confirmatory result is possible under this frozen transaction, and none was fabricated.

This is a **design/control-plane defect record**, not a scientific negative. No claim status changes. The smallest unblocking action is a re-opened DESIGN for the same Director mandate that completes the pool and certificate *before* a new freeze.

Status `BLOCKED` is distinct from:

- a scientific **FALSIFIES** (no measurement was made);
- **MEASUREMENT_INVALID** (no measurement was taken, so there is nothing invalid to disqualify);
- a network/infrastructure failure (outbound TCP 443 connectivity to candidate hosts succeeded — see §5).

---

## 2. What the frozen design required before freeze (its own rules)

The frozen documents are explicit that the experiment's input identity and a live attainability certificate were **DESIGN-time, pre-freeze obligations**:

| Requirement | Where stated |
|---|---|
| "Target pool of seed URLs is **frozen at DESIGN time** (recorded in `spec.json.target_pool`). Pool MUST contain DEEP (hop>=3) items on >=2 distinct hosts/engines **confirmed by a separate hop-confirmation crawl** (BFS, depth 6, budget 250) **during DESIGN**." | `spec.json.measurement_validity.VN-V2` |
| "ADMISSION_GATE_V2: frozen pool must have >=10 admitted DEEP items total ... with >=2 distinct hosts/engines each having >=3 admitted DEEP items. **Verified during DESIGN and recorded in pre_freeze_control_certificate.**" | `spec.json.decision_rule.admission_gate` |
| "Pre-freeze control certificate recorded in `spec.json.pre_freeze_control_certificate` with live evidence references proving: (a) pool admits DEEP items on >=2 hosts/engines, (b) at least one discovery channel is probeable on at least one host, (c) null control yields zero reachable URLs. **Freeze proceeds only if all three verified.**" | `spec.json.measurement_validity.VN-V9` |
| "Pool construction (During DESIGN, Before Freeze) ... **Pool freeze:** The set of seeds, admitted DEEP items, and their hop depths are frozen in `spec.json.target_pool.confirmed_deep_items`." | `prereg.md` §6.1 |
| "**Freeze proceeds ONLY if all three are verified.** If any fails, DESIGN must revise pool/channels or report INCONCLUSIVE." | `prereg.md` §14 |
| "[Unresolved open design decisions] **All must be resolved and frozen in `spec.json` before `freeze.json` is created.**" | `prereg.md` §18 |

The parent handoff carries the same dependency, verbatim: *"A MULTI-HOST, MULTI-ENGINE TARGET POOL THAT ACTUALLY CONTAINS DEEP (hop>=3) STATE ITEMS ON AT LEAST TWO DISTINCT HOSTS/ENGINES, confirmed during DESIGN before freeze ... A PRE-FREEZE CONTROL CERTIFICATE RECORDED INSIDE spec.json WITH LIVE EVIDENCE REFERENCES before freeze.json exists."*

---

## 3. What the frozen record actually contains (RAW EVIDENCE)

All of the following are direct observations of the frozen files (OBS-FROZEN-01…06 in `result.json`); hashes of `request.json`/`spec.json`/`prereg.md` match `freeze.json` exactly, so this is the true frozen record:

- `spec.json.target_pool.seeds` = `[]`
- `spec.json.target_pool.confirmed_deep_items` = `[]`
- `spec.json.target_pool.confirmed_deep_hosts` = `[]`
- `spec.json.pre_freeze_control_certificate.all_verified` = `false`, `verified_at` = `null`, `pool_deep_items_confirmed` = `false`, `pool_deep_hosts_confirmed` = `false`, `discovery_channel_probe_verified` = `false`, `null_control_verified` = `false`, `evidence_refs` = `[]`
- `spec.json.pre_freeze_control_certificate.note` itself says: "Must be completed during DESIGN with live evidence before freeze.json is created."
- `prereg.md` §18's open design decisions (final seed list, synthetic-item identifier format, search query-parameter mapping, JSON-LD vocabulary, sitemap.gz handling, redirect accounting, engine definition) were never resolved in the frozen spec.
- `freeze.json` contains only the three canonical hashes; it binds **no** pool, seed-list, raw-crawl or certificate artifact anywhere in the repository. A repo-wide search found pre-freeze-certificate evidence only in the *parent* packet (EXP-FRONTIER-37950626378), which is a different experiment with a different pool.

---

## 4. Interpretation: why the falsifier is unreachable in BOTH directions

Under the frozen decision rule:

```
discovery_reachable_fraction =
  count(DEEP items reachable in <=K GETs via ANY channel) / count(admitted DEEP items in frozen pool)

SUPPORTS  : fraction >= 0.50 on >= 2 distinct hosts/engines
FALSIFIES : fraction <  0.50 on >= 2 distinct hosts/engines
```

As frozen, `count(admitted DEEP items) = 0`, so:

- the primary fraction is `0/0` — **undefined**, not `0`;
- `discovery_reachable_fraction_per_engine` is undefined for every host (there are no hosts);
- `engines_meeting_threshold` cannot be counted;
- therefore **neither** the SUPPORTS nor the FALSIFIES branch is arithmetically reachable. This is precisely the "empty-accept-region / unsatisfiable-predicate" failure class flagged in the Director mandate's agent priors — the falsifier is satisfiable in neither direction until a pinned, DEEP-bearing pool exists.
- The `INCONCLUSIVE` mapping in the frozen decision rule ("admission gate fails (pool has <10 admitted DEEP items total)") also cannot be cleanly triggered, because the gate's prerequisite inputs were never recorded. Explicitly encoding this receipt as `NOT_APPLICABLE` is the honest option: no branch of the rule is meaningful on an empty sampling frame.

**Arithmetic sanity check of my claim:** if I had *constructed* a pool of N items after freeze and reported any fraction, that fraction would rest on an unfrozen sampling frame — the audit would (correctly) flag `MEASUREMENT_INVALID` and the sample would be wasted. Constructing nothing and blocking is the only way to keep the frozen transaction intact.

---

## 5. Environment: the blocker is not infrastructure

A TCP 443 connectivity probe (4 s timeout, no HTTP request) succeeded against `doc.rust-lang.org`, `www.gnu.org`, `quotes.toscrape.com`, and `example.com` (OBS-ENV-01). Python 3.12.15 is available. So the credential-free GET-only substrate *would* be usable; the experiment is blocked by the unsatisfiable frozen design, **not** by the network. No live HTTP probe was sent for this experiment (OBS-ENV-01 was TCP-only), because any discovery/channel/crawl traffic would constitute post-freeze pool construction (VN-B7).

---

## 6. Controls and baselines (all UNKNOWN, none run)

The four frozen control identifiers are preserved in `result.json.controls` with expected behavior, observed behavior, `result=UNKNOWN` and evidence refs:

| Control | Expected (frozen) | Observed |
|---|---|---|
| `PC_DISCOVERY_CHANNEL_REACHABILITY` | >=1 channel live-probeable on >=1 pool host with evidence in the certificate | not run; no pool host; certificate empty |
| `NC_SYNTHETIC_UNREACHABLE_ITEM` | 0 reachable URLs for synthetic items per channel | not run; synthetic identifiers never frozen |
| `B_LINK_FOLLOWING_BFS` | hop depths match DESIGN confirmation crawl | no crawl recorded; item set empty |
| `B_PERSISTED_PATH_REACQUISITION` | RACQ_PATH ~ hop+1 (parent) | carried reference only; not re-measurable |
| `B_DIRECT_URL_REPLAY` | RACQ_URL = 1 GET (parent) | carried reference only; not re-measurable |

UNKNOWN (not FAIL) is deliberate: the pass criteria were never given the chance to run, and the frozen design assigned those runs to DESIGN pre-freeze. The parent baselines remain valid *inherited context* for the parent's own pool and cannot be substituted for this experiment's missing pool (parent DEEP band is single-host/single-engine mdBook and is explicitly rejected as a substitute by the parent handoff dependencies).

---

## 7. Why prior EXECUTE attempts failed (receipts, not measurements)

The packet directory contains `failure.json` (github_run_id 37996033047, category `EXECUTION_FAILURE`, `retryable=false`, `stage exited with code 1`, fingerprint `2ec9912af1c82b8c55d55e90`) and `model_execute.json` (status=failure, category=substantive), plus `execution_checkpoint.json` (pre_execute_sha `c6edd08c`). Lane state records `consecutive_failures=2`, `last_failure_retryable=false`. None of these receipts contain raw/derived evidence, consistent with the same satisfiability blocker. They are prior receipts; they are not scientific evidence (parent handoff `do_not_assume`, same principle).

This attempt produces the canonical stage outputs (`result.json`, `report.md`, `provenance.json`) so that AUDIT and DIRECTOR have a durable, machine-valid packet instead of another bare failure receipt.

---

## 8. Claim consequences

**None.** No measurement was made:

- `C-RESIDUAL-NOVELTY`: retains its Codex effective status (latest effective event EXP-PRODUCT-37989728440). Its acquisition-phase sub-question — can site-native discovery reach deep items in O(1) GETs — remains unmeasured. No support/falsification is claimed here.
- `C-WEB-DYNAMICS`: retains its Codex effective status (EXP-PHYSICS-37973239386). The discovery-mechanism question is adjacent but not this claim's measurement, and nothing here touches its epistemic state.

The only durable decision-relevant fact this packet adds: **the frozen transaction for this mandate is unsatisfiable and must be re-designed (pool + certificate) before any confirmatory run**, and the factory's freeze governance permitted a VN-V9/§14 gate violation that this receipt makes explicit and verifiable.

---

## 9. Validity disclosures

- `result.json.metrics` contains stable frozen metric identifiers with explicit `null`/`{}` values plus a `*_reason` companion; the contract semantics `null = explicitly unknown/not available` apply, and every null is explained.
- `result.json.observations` contains direct observations of the frozen files and of the TCP-only environment probe; no web-outcome observation exists because none was collected.
- `result.json.artifacts` pins the frozen inputs and prior receipts by sha256.
- The frozen experiment metrics are quantitative in nature; their absence here is a measurement-block, not a non-quantitative experiment. This is explained in the metrics themselves and in VN-B1/VN-B4.
- No representation of Web observation space was created or lost (VN-B12): the only analyzed representation is the frozen packet content itself, losslessly.

## 10. Smallest unblocking actions (also in `result.json.unresolved`)

1. **Re-open DESIGN** for the same Director mandate (`CONTINUE` on C-RESIDUAL-NOVELTY discovery question): curate candidate seeds, run the frozen hop-confirmation crawl (static same-host `<a>`, depth<=6, budget 250), admit >=10 DEEP items with >=2 hosts/engines each >=3, verify >=1 discovery channel and the null control live, populate `spec.json.target_pool` and `spec.json.pre_freeze_control_certificate` with evidence refs, then re-freeze. A design-contract-v2 design with `freeze_eligibility` checks (decision_rule_reachability, baseline_identifiability, control_sensitivity, treatment_liveness, freeze_artifacts_bound) would make this defect class impossible to freeze.
2. Alternatively, the Global Research Director may prefer the explicitly recorded maintenance/invalidation axis (re-validation GETs/bytes + stale-replay false-accept vs re-derivation), which is a different design and also requires a proper frozen input set.
3. Governance follow-up (non-scientific): determine why the deterministic freezer committed a v1 packet whose own pre-freeze gate (VN-V9/prereg §14) was unfulfilled, so the next occurrence is caught at DESIGN or freeze time.