# EXP-RUNTIME-34439061845 Preregistration

## 1. Experiment Identity

- **Experiment ID**: EXP-RUNTIME-34439061845
- **Lane**: Runtime
- **Claim**: C-MEAS-VALID (Measurement substrate is intervention-valid)
- **Date**: 2026-09-10
- **Status**: DESIGN — NOT YET FROZEN
- **Parent**: EXP-RUNTIME-34300004597 (Keycloak ecological validity, C-MEAS-VALID survives narrowly)

## 2. Scientific Question

Does the WWW-Authenticate header discrimination pattern observed on Keycloak /userinfo — where no_auth returns 'Bearer realm=...' (no error fields) while error states return 'Bearer realm=..., error=invalid_token, error_description=...' — transfer to other Keycloak endpoints (/token with password grant, /token with client_credentials grant, /introspect)?

## 3. Motivation

Parent experiment EXP-RUNTIME-34300004597 established:
- WWW-Authenticate is the true discriminating header on Keycloak /userinfo (discrimination 0.833 == full vector)
- Cache-Control error-type variation is falsified on Keycloak (V4 tautology confirmed)
- expired_token and invalid_token are indistinguishable by ANY observable
- 3 distinct fingerprints (not 4): valid 5e7fae, no_auth 61c534, expired==invalid 196af3

The parent's next question: "Does WWW-Authenticate header variation transfer to other OAuth/OIDC providers (Auth0, Okta)?"

This experiment takes the first step toward answering that question by testing transfer within Keycloak across different endpoints. This is the smallest high-information experiment: it uses the same Keycloak deployment, same auth states, and same measurement pipeline, but tests whether the discrimination pattern is endpoint-specific or Keycloak-level.

**Rationale**: If WWW-Authenticate discrimination is /userinfo-specific, then the product recommendation is limited to that endpoint. If it transfers to /token and /introspect, the mechanism is broader and more useful for product architecture. Testing within Keycloak first (before external IdPs) is necessary because: (1) it uses existing infrastructure, (2) it controls for IdP implementation differences, (3) a negative result within Keycloak would falsify the endpoint-transfer hypothesis without needing external setup.

## 4. Hypotheses

### H1: WWW-Authenticate Transfer
WWW-Authenticate-only discrimination > 0 on at least 2 of 3 additional endpoints (/token password, /token client_credentials, /introspect).

### H2: Full-Vector Discrimination
Full-vector discrimination > 0.5 on at least 2 of 3 additional endpoints.

### H3: Positive Control
WWW-Authenticate-only discrimination > 0 on /userinfo (replicates parent result).

### H4: Expired-Invalid Indistinguishability
expired_token and invalid_token produce identical fingerprints on all 4 endpoints.

## 5. Endpoints

### 5.1 /userinfo (GET) — Positive Control
- URL: `http://127.0.0.1:18080/realms/spider-test/protocol/openid-connect/userinfo`
- Method: GET
- Auth: Bearer token in Authorization header
- Expected behavior: identical to parent (WWW-Authenticate varies by auth state)

### 5.2 /token (POST, password grant) — Test Endpoint 1
- URL: `http://127.0.0.1:18080/realms/spider-test/protocol/openid-connect/token`
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Body: `grant_type=password&client_id=spider-client&client_secret=spider-secret-12345&username=alice&password=alice123&scope=openid`
- Auth states:
  - no_auth: omit Authorization header (Keycloak may still process form body)
  - valid_token: include Authorization: Bearer <token> (redundant but consistent)
  - expired_token: include Authorization: Bearer <expired_jwt>
  - invalid_token: include Authorization: Bearer <malformed_string>
- Expected: Keycloak may ignore Authorization header for password grant (form body provides credentials). If so, all states return same response → discrimination = 0. This is informative: it means password grant is credential-based, not token-based.

### 5.3 /token (POST, client_credentials grant) — Test Endpoint 2
- URL: `http://127.0.0.1:18080/realms/spider-test/protocol/openid-connect/token`
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Body: `grant_type=client_credentials&client_id=spider-client&client_secret=spider-secret-12345`
- Auth states:
  - no_auth: omit Authorization header
  - valid_token: include Authorization: Bearer <token>
  - expired_token: include Authorization: Bearer <expired_jwt>
  - invalid_token: include Authorization: Bearer <malformed_string>
- Expected: client_credentials grant uses client authentication (client_id/secret in body), not user tokens. Authorization header may be ignored → discrimination may be 0. This is informative.

### 5.4 /introspect (POST) — Test Endpoint 3
- URL: `http://127.0.0.1:18080/realms/spider-test/protocol/openid-connect/token/introspect`
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Body: `token=<token>&client_id=spider-client&client_secret=spider-secret-12345`
- Auth states:
  - no_auth: omit Authorization header (body contains token to introspect)
  - valid_token: body contains valid token
  - expired_token: body contains expired JWT
  - invalid_token: body contains malformed string
- Expected: introspect returns JSON with `active: true/false`. Body varies by validity. Authorization header is for client authentication, not user token → may be ignored.

## 6. Auth States (Frozen from Parent)

| State | Token Source | Expected Status |
|-------|-------------|----------------|
| no_auth | None (no Authorization header) | 401 |
| valid_token | Keycloak direct access grant (alice) | 200 |
| expired_token | Locally-signed HS256 JWT (exp=1h ago) | 401 |
| invalid_token | String "not-a-real-jwt-token" | 401 |

Note: expired_token is NOT truly Keycloak-issued (V6 state construction leakage from parent). Keycloak treats it as invalid_signature, same as invalid_token.

## 7. Sample Size

- 4 endpoints x 4 states x 10 reps = 160 total requests
- Per endpoint: 40 requests (4 states x 10 reps)
- Seed: 44 (for comparability with parent)
- Inter-request jitter: 0-200ms (same as parent)
- Randomized request order per endpoint block

## 8. Measures

### 8.1 Primary Metric
- **www_authenticate_only_discrimination**: discrimination score using only WWW-Authenticate header value as fingerprint
- Per-endpoint: full_vector_discrimination, www_auth_only_discrimination

### 8.2 Baselines (per endpoint)
- B-STATUS-ONLY, B-BODY-ONLY, B-URL-HASH, B-RANDOM
- Cache-Control-only discrimination
- Set-Cookie-only discrimination

### 8.3 Controls
- C_NULL_FP_RATE: overall false positive rate < 5%
- C_POSITIVE_DISCRIMINATION: full-vector discrimination > 0.5 per endpoint
- C_WWW_AUTH_VARIATION: WWW-Authenticate-only discrimination > 0 per endpoint
- C_BODY_IDENTITY_EXPIRED_INVALID: expired == invalid body hash per endpoint
- C_DRIFT_EXPIRED_VS_INVALID: Jaccard < 0.5 per endpoint

## 9. Null Models

### 9.1 Shuffle Null
Permute auth state labels across requests. WWW-Authenticate-only discrimination should be ~0.

### 9.2 Random Fingerprint Null
B-RANDOM: random 256-bit fingerprints. Expected discrimination ~0.

### 9.3 URL Hash Null
B-URL-HASH: all requests to same URL. Expected discrimination 0.0.

## 10. Statistical Tests

### 10.1 Primary Test
- Count endpoints where WWW-Authenticate-only discrimination > 0
- Decision: >= 2 of 3 additional endpoints with discrimination > 0 → SURVIVES

### 10.2 Per-Endpoint Discrimination
- Full-vector discrimination > 0.5 for each endpoint
- Bootstrap 95% CI for discrimination score per endpoint

### 10.3 Expired-Invalid Identity
- Jaccard similarity between expired_token and invalid_token fingerprints per endpoint
- Jaccard == 1.0 (identical) on all endpoints

## 11. Controls

### 11.1 Positive Control (userinfo)
- WWW-Authenticate-only discrimination > 0 on /userinfo
- Replicates parent result; verifies pipeline correctness

### 11.2 Null Control (B-RANDOM)
- B-RANDOM discrimination ~ 0.0
- Verifies measurement pipeline stability

### 11.3 Endpoint Sensitivity Control
- If /token password grant ignores Authorization header, all states return same response → discrimination = 0
- This is NOT a failure; it is informative: password grant is credential-based, not token-based
- Document this as a structural observation, not a scientific negative

## 12. Validity Threats

### 12.1 Authorization Header Ignoring
Keycloak may ignore the Authorization header for /token (password/client_credentials grant) because authentication is via form body (client_id/secret, username/password). If so, all auth states return identical responses → discrimination = 0. This is expected behavior, not measurement failure.

### 12.2 Endpoint-Specific Error Formats
Different Keycloak endpoints may return different error JSON structures, HTTP status codes, or header patterns. The experiment documents these differences rather than assuming uniformity.

### 12.3 Sample Size
N=40 per endpoint is sufficient for the primary threshold test (discrimination > 0.5) but limited for subtle differences. Bootstrap CI reported for each endpoint.

### 12.4 Body Variation Across Endpoints
/token returns access_token JSON for valid state; /introspect returns active:true/false JSON. Body-only discrimination may be higher on these endpoints than on /userinfo. This is informative: it shows which endpoints have natural body discrimination.

### 12.5 Expired Token Construction
expired_token is locally-signed HS256, not truly Keycloak-issued. Keycloak treats it as invalid_signature, same as invalid_token. This is the same constraint as the parent experiment.

## 13. Decision Rules

### 13.1 SURVIVES_CURRENT_TEST
If ALL of:
1. WWW-Authenticate-only discrimination > 0 on >= 2 of 3 additional endpoints (/token password, /token client_credentials, /introspect)
2. Full-vector discrimination > 0.5 on >= 2 of 3 additional endpoints
3. Null FP < 5%
4. Positive control passes (WWW-Authenticate discrimination > 0 on /userinfo)
5. No pipeline errors

### 13.2 FALSIFIED-IN-SETTING
If ANY of:
1. WWW-Authenticate-only discrimination == 0 on ALL 3 additional endpoints
2. Full-vector discrimination <= 0.5 on ALL 3 additional endpoints
3. Positive control fails (WWW-Authenticate discrimination == 0 on /userinfo)

### 13.3 MEASUREMENT_INVALID
If:
1. Null FP > 5%
2. Pipeline errors prevent computation
3. Keycloak deployment fails

## 14. Expected Outcomes

### 14.1 Positive Result (SURVIVES_CURRENT_TEST)
- WWW-Authenticate discrimination is a Keycloak-level behavior, not /userinfo-specific
- Product recommendation to use WWW-Authenticate as discriminating signal generalizes across Keycloak endpoints
- External agents using Keycloak can rely on WWW-Authenticate regardless of endpoint
- Does NOT test cross-IdP transfer (Auth0, Okta) — that remains unknown

### 14.2 Negative Result (FALSIFIED-IN-SETTING)
- WWW-Authenticate discrimination is /userinfo-specific
- Product recommendation limited to /userinfo endpoint
- Body-only observation (which already achieves discrimination on /token via access_token presence) is the robust architecture for other endpoints
- Does NOT falsify C-MEAS-VALID entirely — only this specific transfer test

### 14.3 Mixed Result
- WWW-Authenticate discriminates on some endpoints but not others
- Product recommendation is endpoint-dependent
- Document which endpoints support WWW-Authenticate discrimination

## 15. Analysis Plan

1. **Deploy Keycloak**: Same Docker deployment as parent (port 18080, realm spider-test)
2. **Test /userinfo**: Replicate parent result (positive control)
3. **Test /token (password)**: 4 states x 10 reps, document response patterns
4. **Test /token (client_credentials)**: 4 states x 10 reps, document response patterns
5. **Test /introspect**: 4 states x 10 reps, document response patterns
6. **Compute discrimination**: Full vector, single-header, baselines per endpoint
7. **Evaluate decision rule**: Count endpoints with WWW-Authenticate discrimination > 0
8. **Document structural observations**: Which endpoints ignore Authorization header, which have natural body discrimination

## 16. Deviation Policy

Any deviation from this preregistration will be labeled EXPLORATORY and cannot support confirmatory claims. A new confirmatory claim requires a new preregistration.

## 17. Freeze Statement

This preregistration is frozen BEFORE any analysis code is written or any outcome data is inspected. The experiment will be executed exactly as described here.
