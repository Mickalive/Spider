# EXP-RUNTIME-36129163700 preregistration

- **Lane:** runtime
- **Claim:** `C-MEAS-VALID` (measurement-validity claim only; no registry promotion is authorized by this packet)
- **Mode:** DESIGN / pre-freeze. No outcome-bearing measurement was run while writing this preregistration.
- **Primary substrate:** the accepted two-worker, shared-WAL, stable-header plain-HTTP fixture from `EXP-RUNTIME-36100549580`; this experiment does not silently replace it with the rejected private-helper composite from `EXP-RUNTIME-36106663091`.
- **Durability rule:** an executable capability is durable only if its frozen scope is present at `HEAD` with matching content. A worktree-only or content-addressed reference is not durable evidence.

## 1. Inherited scientific boundary

The parent handoff is inherited as context, not as an automatic agenda. The exact parent is `EXP-RUNTIME-36106663091` with SHA-256 `213c6c57a9a089b2159cc0e9ce1819f0165b84a498119ab180cf537d737f87ce`; the Director mandate supersedes its mandatory-browser-preflight disposition.

- **Established:** the accepted distributed shared-WAL plain-HTTP substrate is a bounded prerequisite (`EXP-RUNTIME-36100549580`); a private-helper Playwright path is not an admissible capability gate.
- **Rejected:** do not repeat the full C1-C8 browser composite or restore `playwright._impl`/private path access as a precondition.
- **Unknown:** public Chromium launchability, the same-run ledger/contract, downstream lane reachability and HEAD durability remain unestablished.
- **Do not assume:** contradictory Frontier/Intel availability records are not resolved by narrative; a browser failure is not a Part A negative; an uncommitted file is not durable; and C availability does not unblock a lane until that lane preregisters and honors the required scope.

The frozen validity-control identities are `V-SUBSTRATE-CERTIFICATE`, `V-CAPTURE-STABILITY`, `V-AUTH-SESSION-BOUNDARY`, `V-A-MATRIX-COMPLETE`, `V-RECOMPUTE`, `V-B-PUBLIC-API`, `V-B-REAL-CAPTURE`, `V-C-LEDGER-SCHEMA`, `V-DUR-HEAD` and `V-SECRET-REDACTION`. Each is reported as `PASS`, `FAIL` or `UNKNOWN` with an exact evidence reference; a `FAIL` or `UNKNOWN` follows the frozen failure class rather than being converted into a scientific negative.

## 2. Bound question and hypotheses

### 2.1 Director question

Under an explicitly non-vetoing execution order:

1. **Part A (primary):** does the already-certified distributed stable-header shared-WAL plain-HTTP substrate produce a complete intervention-validity matrix in which each valid-auth positive intervention (a valid-auth write and an induced representation drift) is detected, while each matched null (read-only, invalid-auth, expired-auth and deleted-session) leaves the shared WAL byte vector unchanged, with arm-specific sensitivity, specificity and non-degenerate confidence intervals; and
2. **Part B (independent capability):** can a real Chromium, reached only through the public Playwright API at the canonical executable when available, operate at a real `1280x720` viewport, produce nonempty DOM and `Accessibility.getFullAXTree` evidence, and perform a reversible valid-auth SPA write with matched null WAL controls; and
3. **Part C (contract and durability):** can one same-run machine-readable capability ledger and one-command substrate bring-up contract make the relevant capabilities fail closed and preregisterable by Graph, Product, Physics and Frontier, while distinguishing an uncommitted reference from a HEAD-durable implementation.

The browser result is a subordinate, non-vetoing capability result. A browser failure cannot erase or falsify a valid Part A result.

### 2.2 Hypotheses

- **H1-A-INTERVENTION-VALIDITY:** if the session/write boundary, shared-WAL capture and substrate certificate are valid, each positive arm will have point sensitivity at least `0.90` and a two-sided 95% Wilson lower bound at least `0.80`; each null arm will have point specificity at least `0.90` and a two-sided 95% Wilson lower bound at least `0.80`.
- **H2-B-PUBLIC-CHROMIUM-CAPABILITY:** all public-API, real-browser, viewport, DOM/AX, real SPA interaction and reversible-write gates pass. This is a single-run capability hypothesis, not a browser-generalization claim.
- **H3-C-FAIL-CLOSED-CONTRACT:** the same-run ledger and one-command contract enumerate required versus advisory capabilities, exact substrate facts, evidence, freshness and one smallest unblocking action for every unavailable required component. The contract is available for a declared scope only when that scope's gates pass.
- **H4-DURABILITY:** the executable capability scope is present at `HEAD` with matching content. An uncommitted implementation cannot satisfy this hypothesis and is labeled `REFERENCE_ONLY`.

### 2.3 Falsifiers and stopping boundaries

For Part A, a valid falsification in this setting occurs only when all validity gates pass and an arm misses its frozen threshold. A substrate launch failure, missing raw file, unstable capture, absent session/auth implementation, missing cell or recomputation disagreement is `BLOCKED` or `MEASUREMENT_INVALID`, not a falsifier. A valid HTTP error with complete pre/post captures is a scored observation, not missing data.

For Part B, an absent public executable, import, launch, DOM/AX surface or action is `UNAVAILABLE`; a fabricated substitute is `MEASUREMENT_INVALID`. For Part C, a required capability failure or HEAD mismatch is a contract/durability result, not a scientific negative. No result in this preregistration self-promotes the claim.

## 3. Frozen substrate and state contract

### 3.1 Owned processes and files

The execution harness owns only the following names for this run and acquires a run lock before starting:

| item | frozen value |
|---|---|
| upstreams | `127.0.0.1:19860`, `127.0.0.1:19861` |
| gunicorn | version `23.0.0`, one worker per upstream, WSGI app `run_experiment:create_app` from this experiment directory (the planned executable is `research/experiments/EXP-RUNTIME-36129163700/run_experiment.py`) |
| nginx | `127.0.0.1:19851`, exclusive config `/tmp/single.db.nginx.conf` |
| cache/temp | `/tmp/single.db.cache`, `/tmp/single.db.temp` |
| shared database | `/tmp/single.db` in SQLite WAL mode |
| derived files | `/tmp/single.db-wal` (gating), `/tmp/single.db-shm` (diagnostic only) |
| nginx semantics | one upstream per declared port, `hash $request_uri consistent`, `proxy_cache`, authorization bypass, `X-Worker-Pid` |
| run lock | `/tmp/spider-runtime-EXP-RUNTIME-36129163700.lock` |

Bring-up is idempotent. It must refuse to kill unrelated processes, replace a foreign config, or overwrite a foreign lock. Teardown removes only owned PID files, temp/cache/config/database paths and the lock after all artifacts are hashed. The measured SQLite connection uses `PRAGMA wal_autocheckpoint=0`; the measured WAL must not be checkpointed or compacted between pre/post captures.

### 3.2 Readiness certificate

Before any Part A action, collect the deterministic real-cache probe. Target `n_total=910` and `n_non304=850`; the hard floors are:

- `n_non304 >= 800` total and `>=400` on each upstream endpoint;
- distinct `X-Worker-Pid >= 2` for 200 responses;
- per-URI stickiness `>=0.90` over more than 10 distinct URIs;
- no missing worker header on any 200 response;
- the configured hash, cache, authorization-bypass and TLS/plain-HTTP properties match the contract.

The Frontier proposal of ten distinct workers is a stricter diagnostic proposal, not a silently substituted acceptance floor. If the accepted minimum is not met, Part A is `BLOCKED`/`MEASUREMENT_INVALID`, never a scientific negative.

### 3.3 Controlled write surface

The experiment may add only its own controlled route and schema material; it must not edit a frozen parent packet. The planned routes are:

- `GET /runtime/read` — authenticated read-only projection;
- `POST /runtime/write` — accepts only `op=set_marker` or `op=set_representation`, validates HS256 signature and expiry, checks the `sid` against a live `sessions` row, and then updates the single experiment row;
- `GET /runtime/browser` — a real static browser control surface used only by Part B.

The proposed single row is `runtime_probe(id INTEGER PRIMARY KEY CHECK(id=1), marker TEXT NOT NULL, representation TEXT NOT NULL, revision INTEGER NOT NULL, updated_at REAL NOT NULL)`. The exact schema, route implementation and source paths must be recorded in the pre-run manifest before the first outcome-bearing request. A route that cannot enforce the live-session check is not a valid substrate for Part A.

All fixture creation, session insertion/deletion, marker planting and restore occur outside the measured pre/post interval. The pre-capture is taken only after setup is quiesced. Unique values include the run ID and episode ID; no value is reused across arms.

## 4. Part A: primary intervention-validity matrix

### 4.1 Arms and sample size

The independent unit is one pre-registered episode, not one HTTP row, retry or repeated request. There are exactly 20 episodes per arm, for 120 measured episodes total. The order is a seeded balanced permutation of all arm/episode IDs with seed `36129163700`; the raw order is archived before scoring. No retries or imputations are permitted.

| stable arm ID | assigned intervention | ground truth | expected HTTP boundary | independent required evidence |
|---|---|---|---|---|
| `P-WRITE` | valid HS256 token, live `sid`, `POST /runtime/write`, `op=set_marker`, unique value | positive write | 2xx | logical marker readback equals planted value and pre-state differs; WAL vector is recorded separately |
| `P-DRIFT` | valid HS256 token, live `sid`, `POST /runtime/write`, `op=set_representation`, unique value | induced representation drift | 2xx | logical representation readback equals planted value, pre-state differs and real response fingerprint changes; WAL vector is recorded separately |
| `N-READ` | valid HS256 token, live `sid`, `GET /runtime/read` | no-write null | 2xx read | no state change, no WAL change, no representation fingerprint change |
| `N-INVALID` | same write request with an invalid bearer token | auth-rejection null | 401 | no state change and no WAL change; accepted write is a false positive |
| `N-EXPIRED` | correctly signed but expired bearer token | auth-rejection null | 401 | no state change and no WAL change; accepted write is a false positive |
| `N-DELETED` | correctly signed token whose `sid` row was deleted during setup | session-rejection null | 401/403 | no state change and no WAL change; accepted write is a false positive |

A successful response is not by itself proof of a valid intervention. The detector receives raw pre/post observations and the planted readback, but not the arm label, expected status or hypothesis. The arm label is joined only after the detector output is written.

### 4.2 Raw evidence per episode

Write one immutable JSONL record per episode before deriving metrics. The record must contain:

- run ID, experiment ID, arm ID, episode ID and seeded order index;
- UTC start/end times and request path/operation;
- token class and session ID **as a redacted reference**, never a bearer secret;
- HTTP status, canonical body bytes and stable-header subset;
- pre/post `/tmp/single.db` and `/tmp/single.db-wal` byte lengths and SHA-256 values;
- pre/post `/tmp/single.db-shm` size and hash as a diagnostic;
- pre/post logical marker, representation, revision, session presence and planted-value readback;
- capture quiescence and fixture-cleanup markers;
- exception, timeout and transport outcome, or explicit `null` fields plus a reason.

A pre-capture and post-capture are not interchangeable. The raw file bytes used for a hash are retained or their content-addressed hashes are recorded under the packet's artifact rules. No derived metric is written over raw evidence.

### 4.3 Independent ground truth and detector

The ground truth label is assigned by the action script before the request, not inferred from a hash. A positive is considered detected only when:

- the logical readback equals the unique planted value;
- the pre-state differs from the post-state; and
- the response is an accepted 2xx response.

For `P-DRIFT`, the response fingerprint must also differ from the pre-response fingerprint. The WAL vector change is a separately reported side-effect observation, not the sole positive label, so a detector cannot be tautologically defined as “the WAL hash changed.” For each null, a false positive is any of:

- logical state changes;
- the main-plus-WAL vector changes; or
- for `N-READ`, the response fingerprint changes.

An unauthorized write returning 2xx is also a false positive for `N-INVALID`, `N-EXPIRED` and `N-DELETED`. A complete but unexpected 5xx/timeout in a positive arm is a valid false negative; a missing capture is not.

The response fingerprint is SHA-256 over status, canonical body and sorted stable headers after excluding `Date`, `Server`, `X-Worker-Pid`, `X-Cache`, `Age`, `Content-Length`, `ETag`, `W-ETag` and `Range`. The detector and an independent recomputation must agree bit-for-bit.

### 4.4 Metrics and decision

For each arm, report numerator, denominator, point rate and a two-sided 95% Wilson interval (`z=1.959963984540054`). Also report pooled sensitivity/specificity descriptively, but pooled values cannot override a failed individual arm. The primary estimand is the conjunction of all six arm-specific results.

`A=SUPPORTS` only if all 20 episodes per arm are complete, all validity gates pass, each positive sensitivity has point `>=0.90` and lower bound `>=0.80`, each null specificity has point `>=0.90` and lower bound `>=0.80`, and each interval has `ci_hi>ci_lo`. A deterministic zero-width interval, missing arm or missing interval is not accepted as non-degenerate evidence. A valid threshold failure is `A=FALSIFIES` in the exact setting. A capture/auth/recompute failure is `A=MEASUREMENT_INVALID`; an unstartable substrate is `A=BLOCKED`.

## 5. Part B: standalone public-Chromium capability

Part B is executed only after Part A raw evidence is complete and copied to an immutable artifact. Browser provisioning is not allowed to prevent or alter Part A execution.

1. Resolve the public Playwright executable through `sync_playwright().start().chromium.executable_path`; record the returned path, package version, executable hash and whether it is the canonical path `/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`. If the public property is absent, the only permitted equivalent is public `p.chromium.launch()` with no private path access; its public launch receipt and browser version must be independently recorded. If neither public route can be verified, record B as `UNAVAILABLE`.
2. Launch through the public `launch(executable_path=...)` API when a public executable path is available, or the recorded public equivalent when it is not, with a fresh context whose viewport and window size are exactly `1280x720`. No `playwright._impl`, private helper, alternate browser or synthetic fallback is allowed.
3. Navigate the real page to the served `/runtime/browser` surface. Capture `page.content()`, a real CDP DOM snapshot, and `Accessibility.getFullAXTree`; record DOM/AX byte lengths, hashes, node counts, viewport values and browser errors.
4. Use actual page controls, not `page.request` or direct server calls, to issue one valid-auth SPA write. Record pre/post logical state, response/body fingerprint and main-plus-WAL vector. Then use the actual control to restore the planted value; record the restore and its WAL vector.
5. Repeat one read-only, invalid-auth, expired-auth and deleted-session control through the same real browser interaction path. Each null must preserve the WAL vector and logical state; an accepted unauthorized action is `B=AVAILABLE` only if the null-control gate is still passed by the frozen detector.

`B=AVAILABLE` requires all steps, real captures, reversible restore and four nulls. Any missing browser/dependency/launch/DOM/AX/action is `B=UNAVAILABLE`, with exact artifact path and one smallest action such as installing the recorded package or making the canonical executable available. A synthetic DOM/AX/WAL substitute is `MEASUREMENT_INVALID`. B is a single capability result; no browser-generalization confidence interval is claimed.

## 6. Part C: one-command capability ledger and contract

The proposed exact bring-up command is:

```text
python -m research.runtime.bringup --config research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json --ledger research/experiments/EXP-RUNTIME-36129163700/artifacts/capability_ledger.json
```

The command must be idempotent, acquire the run lock, use only the frozen ports/config/WAL/schema above, and return a non-zero status for a failed required scope. It must not install packages, mutate credentials, start unrelated services or kill unrelated processes. If a dependency is absent, it records the absence and the smallest sanctioned action rather than silently installing or fabricating a result.

The ledger is one same-run JSON object with at least:

- `schema_version`, `ledger_id`, `experiment_id`, `run_id`, `base_sha`, `HEAD_sha`, timestamps and worktree status;
- `required_scope` and explicit `required_for_runtime_A`, `required_for_browser_B`, `required_for_downstream_lane` flags;
- statuses `AVAILABLE`, `UNAVAILABLE`, `ERROR`, `NOT_APPLICABLE` or `UNKNOWN`;
- `CAP-PYTHON-DEPENDENCIES`, `CAP-CHROMIUM-LAUNCH`, `CAP-BROWSERGYM-IMPORT`, `CAP-AGENTLAB-IMPORT`, `CAP-POLICY-MODEL-CREDENTIAL`, `CAP-HF-REACHABILITY`, `CAP-GHCR-REACHABILITY`, `CAP-DISTRIBUTED-SUBSTRATE`, `CAP-WAL-SCHEMA`, `CAP-HEALTH-GATE`, `CAP-N-NON304-FLOOR` and `CAP-X-WORKER-PID-FLOOR` records;
- exact command, timeout, exit status, package/version, executable path, endpoint, port, WAL path/schema, health floor, evidence path/hash, freshness, secret-redaction status and one `smallest_unblock_action` for every unavailable required item.

The component probes are fixed as follows: Python dependencies use an isolated subprocess with `sys.executable`, an import/`find_spec` check and a short timeout; BrowserGym and AgentLab use the same isolated import check and never receive a synthetic success; the policy-model capability records only configured environment-key presence and a redacted reference, never a token; HF and GHCR use bounded read-only HTTP reachability requests with explicit timeout, status code and latency, without downloading a model; browser launchability is the Part B public API probe; distributed health is the two-worker readiness certificate. A timeout, import exception, missing executable or non-2xx reachability result is recorded as `UNAVAILABLE`/`ERROR` with its evidence, never silently upgraded to `AVAILABLE`.

For this experiment's `runtime.A` scope, browser, AgentLab, model-credential, HF and GHCR probes are advisory unless explicitly selected as required by the invoking lane. A downstream lane may require them in its own preregistration, but absence of an optional item cannot veto Part A. A ledger/contract failure is `BLOCKED` or `UNAVAILABLE` for the affected scope, never a falsification.

## 7. Durability and contradiction resolution

After artifacts are written, compare every executable path in the frozen durability scope with `HEAD`. The scope is exactly `research/experiments/EXP-RUNTIME-36129163700/run_experiment.py` and `research/runtime/bringup.py`; the declarative `research/experiments/EXP-RUNTIME-36129163700/bringup_contract.json` is hash-recorded as well:

```text
git show HEAD:<path> must exist and have the same content hash as the measured worktree file.
```

An untracked generated file, a file present only in the worktree, a local diff or a content-addressed export is `REFERENCE_ONLY`; it cannot be measured as durable. The absence of a required executable at HEAD yields `DURABILITY=UNSATISFIABLE`, not a scientific falsification. Under the lane no-commit rule, the smallest sanctioned repair is to use an implementation already at HEAD or have an authorized commit/merge workflow apply the change, then start a new run. This experiment does not make a commit.

The capability ledger must also expose the contradictory inherited observations (Frontier's unavailable package report versus Intel's installed-package/Chromium evidence) as same-run component records, with raw evidence and exact statuses. It may resolve availability, but it may not erase the historical distinction between an unavailable observation and a valid negative.

## 8. Execution order, artifacts and analysis

The frozen order is:

1. acquire the run lock and create the pre-run manifest;
2. start the owned substrate and run the minimum health/readiness checks needed by A;
3. run the Part A matrix and preserve raw JSONL before any derived computation;
4. run the B probe independently; B failure is recorded without changing A;
5. run the full C contract/ledger, including optional capability records;
6. hash all artifacts, perform the HEAD/worktree durability check, write derived metrics and report, and clean up owned resources.

Required stable artifact identities and exact paths are:

- `A-EPISODE-LEDGER` — `artifacts/A-EPISODE-LEDGER.jsonl` — raw ordered episode JSONL;
- `A-WAL-VECTOR-BEFORE-AFTER` — `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl` — raw capture metadata and hashes;
- `A-RESPONSE-FINGERPRINTS` — `artifacts/A-RESPONSE-FINGERPRINTS.jsonl` — raw status/body/header fingerprints;
- `A-DERIVED-METRICS` — `artifacts/A-DERIVED-METRICS.json` — recomputed arm metrics and Wilson intervals;
- `A-CAPTURE-STABILITY` — `artifacts/A-CAPTURE-STABILITY.jsonl` — ten no-action pairs;
- `B-PLAYWRIGHT-CAPABILITY` — `artifacts/B-PLAYWRIGHT-CAPABILITY.json` — public executable and launch receipt;
- `B-DOM-AX-CAPTURE` — `artifacts/B-DOM-AX-CAPTURE.json` — real DOM/AX artifacts;
- `B-WAL-EVIDENCE` — `artifacts/B-WAL-EVIDENCE.jsonl` — browser write/restore/null captures;
- `C-CAPABILITY-LEDGER` — `artifacts/capability_ledger.json` — same-run ledger;
- `C-BRINGUP-CONTRACT` — `artifacts/C-BRINGUP-CONTRACT.json` — exact command/config/contract receipt;
- `D-DURABILITY-CHECK` — `artifacts/D-DURABILITY-CHECK.json` — HEAD/worktree comparison and reference-only disposition.

The report must keep raw evidence, observations, derived measurements, interpretation and unresolved validity threats in separate sections. A missing metric is `null`, an unobserved control is `UNKNOWN`, and no unavailable observation is silently imputed as a null success. No outcome is frozen or measured by this DESIGN packet.
