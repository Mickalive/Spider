# EXP-RUNTIME-36084499865 — H1-STABLE-HEADER-SINGLE-NODE

**Status:** MEASUREMENT_INVALID
**Outcome:** INCONCLUSIVE
**Lane:** runtime
**Claim:** C-MEAS-VALID

## Controls


## Metrics


## Validity Notes

- sudo available: nginx master started as root with user www-data workers; cache/temp dirs chowned www-data.
- SYNTHETIC_MUTATION_OR_NONCE_PRESENT: uuid.uuid4() found in code

## Interpretation

Stable-header representation: uuid4 per-response nonce replaced with deterministic HMAC-SHA256(TESTBED_SECRET, auth_state)[:16] token. Same auth state produces identical Set-Cookie, ensuring same-state Jaccard == 1.0. Header-only Jaccard and full-vector fingerprints computed on stable headers MINUS {Content-Length,ETag,W-ETag,Range} lowercased sorted keys preserving natural Cache-Control/Vary/stable Set-Cookie token.

## Unresolved
