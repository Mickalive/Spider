# EXP-RUNTIME-36293257855 — COMPLETE / SUPPORTS

**Lane:** runtime  
**Claim:** C-MEAS-VALID  
**Transport:** real Chromium via public Playwright 1.63.0 API; real button clicks only  
**Authorship:** intervention surface and scorer in separate modules

## Result

- status: **COMPLETE**, outcome: **SUPPORTS**
- per-arm point rates: `{"P-WRITE": 1.0, "P-DRIFT": 1.0, "N-READ": 1.0, "N-INVALID": 1.0, "N-EXPIRED": 1.0, "N-DELETED": 1.0}`
- positive control (P-WRITE) sensitivity: 1.0
- null-control specificities: `{"N-READ": 1.0, "N-INVALID": 1.0, "N-EXPIRED": 1.0, "N-DELETED": 1.0}`
- independent recomputation zero_mismatches: True
- capability ledger required scopes pass: True

## Observations

- Matrix: 120/120 episodes completed via real Chromium; 120/120 scored by the arm-blind detector.
- Per-arm point rates: {"P-WRITE": 1.0, "P-DRIFT": 1.0, "N-READ": 1.0, "N-INVALID": 1.0, "N-EXPIRED": 1.0, "N-DELETED": 1.0}
- Positive control P-WRITE sensitivity=1.0; null-control specificities={"N-READ": 1.0, "N-INVALID": 1.0, "N-EXPIRED": 1.0, "N-DELETED": 1.0}.
- Capture stability: 10/10 byte-identical no-action pairs.
- Capability ledger required scopes pass=True; recompute zero_mismatches=True.
- Reversible restore pass=True.

## Validity notes

- sudo available: nginx master as root, www-data workers.
- Transport is real Chromium via the public Playwright API only; fixture admin/health calls use stdlib urllib and occur outside the measured interval.
- Representation drift (P-DRIFT) is planted via the controlled endpoint, not environmental; recorded as an unresolved scope bound.
- A byte-equality WAL oracle cannot distinguish 'no write' from 'write then byte-revert inside the capture interval'; bounded by the 10/10 stability control.

## Unresolved

- Whether the oracle's discrimination transfers to a non-planted environmental cache/worker drift rather than a planted set_representation drift.
- Whether a successful run leads any downstream lane to actually preregister this substrate as a precondition (publication is not adoption).
- Whether the registered claim ceiling should be widened to production auth middleware, TLS, HTTP/2 or real sites; none of these was measured.

## Decision rule

SUPPORTS requires all six arms point>=0.90, Wilson 95% lower bound>=0.80 and non-degenerate intervals, positive control sensitivity=1.0, null control specificity=1.0, independent recomputation zero_mismatches=true and all required capability-ledger scopes PASS.
