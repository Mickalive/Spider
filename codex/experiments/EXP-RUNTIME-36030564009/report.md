# EXP-RUNTIME-36030564009 — Minimal Single-Node Honesty Gate REOPEN

**Status:** MEASUREMENT_INVALID
**Outcome:** INCONCLUSIVE
**Lane:** runtime
**Claim:** C-MEAS-VALID
**Director mandate:** REOPEN, cognitive_reset=true

## Controls

| V-NGINX-CONFIG-OK | PASS |  |  |
| V-FLASK-LISTENING | PASS |  |  |

## Metrics


## Validity Notes

- HEALTH_GATE_FAILED: nginx+Flask did not respond 200+X-Worker-Pid within 30s
- NGINX_ERROR_LOG:  "127.0.0.1:19851"
2026/09/24 17:02:08 [crit] 54143#54143: *47 open() "/var/lib/nginx/proxy/4/02/0000000024" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"
2026/09/24 17:02:09 [crit] 54143#54143: *49 open() "/var/lib/nginx/proxy/5/02/0000000025" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"
2026/09/24 17:02:10 [crit] 54143#54143: *51 open() "/var/lib/nginx/proxy/6/02/0000000026" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"
2026/09/24 17:02:11 [crit] 54143#54143: *53 open() "/var/lib/nginx/proxy/7/02/0000000027" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"
2026/09/24 17:02:12 [crit] 54143#54143: *55 open() "/var/lib/nginx/proxy/8/02/0000000028" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"
2026/09/24 17:02:13 [crit] 54143#54143: *57 open() "/var/lib/nginx/proxy/9/02/0000000029" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"
2026/09/24 17:02:14 [crit] 54143#54143: *59 open() "/var/lib/nginx/proxy/0/03/0000000030" failed (13: Permission denied) while reading upstream, client: 127.0.0.1, server: localhost, request: "GET /health HTTP/1.1", upstream: "http://127.0.0.1:19860/health", host: "127.0.0.1:19851"


## Unresolved

- None

## Recomputation Check
0 mismatches (greedy decompression, header-only Jaccard, Pearson, CramersV, rho_shuffled, full-vector bootstrap recomputed)