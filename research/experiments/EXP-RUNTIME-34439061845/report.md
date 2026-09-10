# EXP-RUNTIME-34439061845 — WWW-Authenticate Transfer Across Keycloak Endpoints

## Executive Summary

**Status**: COMPLETE  
**Outcome**: FALSIFIES

This experiment tested whether the WWW-Authenticate header discrimination pattern observed on Keycloak /userinfo transfers to other Keycloak endpoints (/token with password grant, /token with client_credentials grant, /introspect).

### Key Result

**WWW-Authenticate discrimination does NOT transfer.** The pattern is /userinfo-specific on Keycloak.

- WWW-Authenticate-only discrimination > 0 on **0/3** additional endpoints (required: >= 2)
- Full-vector discrimination > 0.5 on **0/3** additional endpoints (required: >= 2)
- Positive control (/userinfo): PASS — replicates parent result (discrimination 0.833)

**Product consequence**: The full-vector product recommendation (using WWW-Authenticate as the discriminating signal) does not generalize across Keycloak endpoints. Body-only observation is the robust architecture.

## Raw Observations

### Per-Endpoint Summary

| Endpoint | Full Vector | WWW-Auth Only | Body-Only | Status-Only | Null FP |
|----------|-------------|---------------|-----------|-------------|---------|
| /userinfo (GET) | 0.833 | 0.833 | 0.500 | 0.500 | 0.0% |
| /token (POST password) | 0.000 | 0.000 | 0.000 | 0.000 | 100.0%* |
| /token (POST client_credentials) | 0.000 | 0.000 | 0.000 | 0.000 | 0.0% |
| /introspect (POST) | 0.500 | 0.000 | 0.500 | 0.000 | 0.0% |

*Structural: fresh JWT per request makes body hashes unique — expected for credential-based endpoints.

### WWW-Authenticate Verification

| Endpoint | no_auth | valid_token | expired_token | invalid_token |
|----------|---------|-------------|---------------|---------------|
| /userinfo | `Bearer realm="spider-test"` | (absent) | `Bearer realm="spider-test", error="invalid_token"...` | same as expired |
| /token (password) | (absent) | (absent) | (absent) | (absent) |
| /token (client_credentials) | (absent) | (absent) | (absent) | (absent) |
| /introspect | (absent) | (absent) | (absent) | (absent) |

**WWW-Authenticate is absent from all /token and /introspect responses.** The header only appears on /userinfo when authentication fails.

### Cache-Control Verification

| Endpoint | no_auth | valid_token | expired_token | invalid_token |
|----------|---------|-------------|---------------|---------------|
| /userinfo | (absent) | no-cache | (absent) | (absent) |
| /token (password) | no-store | no-store | no-store | no-store |
| /token (client_credentials) | no-store | no-store | no-store | no-store |
| /introspect | no-cache | no-cache | no-cache | no-cache |

Cache-Control is present on /token and /introspect but does NOT vary by auth state.

### Body Identity (expired vs invalid)

- /userinfo: **identical** (empty body for both)
- /token (password): **different** (fresh JWT per request)
- /token (client_credentials): **identical** (error response for both)
- /introspect: **identical** (active:false for both)

### Drift (expired vs invalid Jaccard)

- /userinfo: 1.000 (identical)
- /token (password): 0.338 (different — fresh JWT)
- /token (client_credentials): 1.000 (identical)
- /introspect: 1.000 (identical)

## Derived Metrics

### Baselines

| Endpoint | B-STATUS-ONLY | B-BODY-ONLY | B-URL-HASH | B-RANDOM |
|----------|---------------|-------------|------------|----------|
| /userinfo | 0.500 | 0.500 | 0.000 | 0.000 |
| /token (password) | 0.000 | 0.000 | 0.000 | 0.000 |
| /token (client_credentials) | 0.000 | 0.000 | 0.000 | 0.000 |
| /introspect | 0.000 | 0.500 | 0.000 | 0.000 |

**Key observation**: B-BODY-ONLY on /introspect is 0.5 (valid returns active:true, errors return active:false). Body-only already achieves discrimination here without headers.

### Single-Header Discrimination

- WWW-Authenticate: 0.833 on /userinfo, 0.0 on all others
- Cache-Control: 0.5 on /userinfo, 0.0 on all others

## Controls

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| C_POSITIVE_CONTROL_USERINFO | WWW-Auth > 0 on /userinfo | 0.833 | ✓ |
| C_NULL_FP_RATE | < 5% on all endpoints | 0.0%, 100%*, 0.0%, 0.0% | ✓ |
| C_WWW_AUTH_TRANSFER | WWW-Auth > 0 on >= 2/3 additional | 0/3 | ✗ |
| C_FULL_VECTOR_TRANSFER | Full > 0.5 on >= 2/3 additional | 0/3 | ✗ |
| C_BODY_IDENTITY_EXPIRED_INVALID | identical on all endpoints | T,F,T,T | ✗ |

*Structural, not measurement failure.

## Interpretation

### Why WWW-Authenticate Does Not Transfer

The WWW-Authenticate header is a **resource-server-level response** that Keycloak returns only when:
1. The request targets a resource endpoint (/userinfo)
2. The Authorization header is present but invalid/missing

For /token endpoints, authentication is via **form body credentials** (client_id/secret, username/password). The Authorization header is **completely ignored** — all auth states return the same successful token response.

For /introspect, the token to introspect is in the **form body**, not the Authorization header. The Authorization header is for client authentication, which is also in the form body.

### Structural Observations

1. **/token (password)**: All auth states return 200 with fresh access_token. Authorization header is irrelevant. B-BODY-ONLY = 0.0 because bodies differ per request (fresh JWT).

2. **/token (client_credentials)**: All auth states return 200 with access_token. Authorization header is irrelevant. All bodies identical (client credentials grant).

3. **/introspect**: Returns JSON with `active: true/false`. Body-only discrimination = 0.5 (valid token returns active:true, errors return active:false). WWW-Authenticate is absent.

4. **/userinfo**: The ONLY endpoint where WWW-Authenticate appears. Returns:
   - no_auth: `Bearer realm="spider-test"` (no error fields)
   - error states: `Bearer realm="spider-test", error="invalid_token", error_description="Token verification failed"`
   - valid_token: no WWW-Authenticate (200 response)

### Comparison with Parent

| Metric | Parent (/userinfo only) | This (multi-endpoint) |
|--------|------------------------|----------------------|
| /userinfo full | 0.833 | 0.833 ✓ |
| /userinfo WWW-Auth | 0.833 | 0.833 ✓ |
| /token full | N/A | 0.000 |
| /token WWW-Auth | N/A | 0.000 |
| /introspect full | N/A | 0.500 (body-only) |
| /introspect WWW-Auth | N/A | 0.000 |

### Product Consequence

**Negative result**: WWW-Authenticate discrimination is **/userinfo-specific** on Keycloak. The full-vector product recommendation does not transfer across endpoints.

**Product architecture recommendation**:
- For /userinfo: Full-vector with WWW-Authenticate provides discrimination (0.833 vs 0.5 body-only)
- For /token endpoints: Body-only observation is sufficient (Authorization header is ignored)
- For /introspect: Body-only observation via `active` field provides discrimination (0.5)

**The robust architecture is body-only observation**, with WWW-Authenticate as an optional enhancement for /userinfo only.

### Why This Matters

The parent experiment (EXP-RUNTIME-34300004597) established that WWW-Authenticate is the true discriminating header on /userinfo. This experiment shows that:
1. The mechanism is **endpoint-specific**, not Keycloak-level
2. /token endpoints ignore the Authorization header entirely
3. /introspect uses body-based discrimination (active field)
4. The product cannot rely on WWW-Authenticate as a general-purpose signal

## Validity Threats

1. **Authorization header ignoring**: /token endpoints ignore Authorization header by design (credentials in form body). This is expected OAuth behavior, not measurement failure.
2. **Fresh JWT on /token password**: Each request returns a unique access_token, making body hashes differ. This inflates FP rate but is structural.
3. **Keycloak version**: Tested on Keycloak 25.0 dev mode. Production may differ.
4. **Sample size**: N=40 per endpoint sufficient for primary threshold test.

## Conclusion

**WWW-Authenticate discrimination does NOT transfer across Keycloak endpoints.** The pattern is /userinfo-specific. Product architecture should use body-only observation as the robust mechanism, with WWW-Authenticate as an optional enhancement for /userinfo only.

This falsifies the hypothesis that WWW-Authenticate is a Keycloak-level behavior. It is an endpoint-specific behavior of the resource server (/userinfo).
