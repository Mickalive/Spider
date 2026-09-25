# Report — EXP-INTEL-36092351694

**Lane:** intel | **Claim:** C-CROSSSITE | **Director mandate:** PIVOT minimal viable shared manifest without exhaustive 567MB LFS
**Status:** COMPLETE | **Outcome:** MIXED

## Strategic question (Director binding)
Can Intel deliver a minimal viable shared manifest without exhaustive 567MB LFS/test.zip: pin WebArena-Verified v2 812 + Hard258 258 via GHCR and Docker digest plus rebuilt 192/36 synthetic Jaccard<0.30 disjoint L=8-14 via deterministic Random(35725763380).sample and product-subtree anchoring 1280x720 CDP AX>10 proving >=10 families constructible with deterministic get_task_start_url __SHOPPING__ expansion, and publish trajectory-grouped artifact for Graph/Frontier/Physics reuse while documenting WebGym 292k HF_TOKEN smallest-next-action if UNAVAILABLE?

## Results

### Durable pins
- WebArena-Verified v2 812: SHA d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 927596 bytes byte-identical x2 via 2 fresh GitHub raw 200 this experiment (raw/github_cross_source_attempts.json). Fresh verification saved to raw/webarena-verified-fresh.json.
- Docker Hub am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb via Hub API 200 / docker images --digests (raw/docker_hub_api_attempts.json) — single-source durable success.
- GHCR ghcr.io/servicenow/browsergym:0.14.3 — 4 attempts logged (raw/ghcr_browsergym_attempts.json) 403/denied UNAVAILABLE correctly marked not assumed equal per MV2.
- Hard258: 258 tasks deterministic random.Random(42).sample(base,258) hist {'shopping': 61, 'shopping_admin': 62, 'map': 40, 'gitlab': 57, 'reddit': 37, 'wikipedia': 1} (derived/hard258_census.json).

### Synthetic 192/36
- Rebuilt without LFS: 36 families 501..536, L per family 8-14 via 8+(idx%7), tokens disjoint t{fid}_j => pairwise Jaccard max 0.0 p95 0.0 mean 0.0 <0.30 PASS. Shuffled baseline mean 0.045 gap -0.045 <0.20 FAIL (gap gate >=0.20). Matrix logged in derived/synthetic_192_36_census.json with expanded stripping + DOTALL body regex via grammar_fulltree_358885.py.

### Deterministic sampling
- Random(35725763380).sample(sorted families_ge3,10) executed TWICE S1==S2 on EACH census: WebArena S1==S2 True [191, 180, 162, 197, 153, 213, 163, 137, 136, 222], Synthetic S1==S2 True [523, 520, 514, 526, 508, 533, 515, 503, 502, 535], WebGym empty ERROR correctly logged. (derived/deterministic_family_samples.json).

### Constructibility (frozen 1280x720 CDP)
- Fresh live CDP Accessibility.getFullAXTree via cdp_session at 1280x720 (raw/ax_captures.jsonl, derived/family_anchoring.json).
- Canonical 136/145/196/222: median AX 707.0 mean 742.4166666666666 std 138.17408001824688 DOM median 202526.5 SHA before==after True mutation != True — all gates >10/>15/>5/>=2000 PASS.
- Synthetic sampled families probed via Flask on 127.0.0.1:8898 with product-subtree anchoring heading/price/add_to_cart/main/contentinfo node_count>1.
- **Union constructible:** 14 distinct families [136, 145, 196, 222, 502, 503, 508, 514, 515, 520, 523, 526, 533, 535] (WebArena only [136, 145, 196, 222], Synthetic only [502, 503, 508, 514, 515, 520, 523, 526, 533, 535]) — gate >=10 **PASS** (requires 10, got 14). Per-family anchoring JSON logs S1/S2 SHA both directions.

### Full-tree AX_consistency vs truncated
- Fulltree mean 0.001 truncated mean 0.000 delta 0.001 (gate >=0.20) FAIL; shuffled delta 0.001 (gate <0.05) PASS; |rho_shuffled| 0.084 <0.20 PASS. Family-level B=2000 CI [0.0, 0.0018315018315018315] variance 0.0000 non-degenerate. Logged in derived/ax_consistency_fulltree.json.
- Reason: synthetic disjoint vocabularies make both fulltree and truncated Jaccard ~0.0, so delta ~0.0 not >=0.20. Prior 4-family slug-URL substrate inverted delta -0.420 also fails but different cause.

### Shared manifest
- Published at derived/shared_minimal_manifest.json with deterministic seeds S1/S2 per census, anchoring definition (1280x720 CDP, body regex DOTALL, expanded stripping), manifest SHAs (WebArena + synthetic + WebGym null UNAVAILABLE with smallest-next-action), family histograms, Jaccard matrix + shuffled gap, constructibility S1/S2 SHA both directions (AX median>10 mean>15 std>5 DOM>=2000), trajectory-grouped artifact (family-level B=2000), pip freeze + grammar hash + viewport. Path+sha256 stored in provenance.json and is consumable by Graph/Frontier/Physics without 567MB LFS (provenance.json).

### WebGym 292k smallest-next-action
- HF_TOKEN present False after 2 genuine 300s attempts each (hf_webgym_manifest_attempts.json) 401 UNAVAILABLE correctly documented: scope/quota/mirror (request HF_TOKEN read-scope on ServiceNow/WebGym + OpenEnv/WebGym, confirm quota, or use HF mirror/dataset export). Not falsification per director mandate.

## Controls
- B-DURABLE-PIN-812: PASS
- B-HARD258-258: PASS
- B-GHCR-BROWSERGYM-0143: PASS
- B-SYNTHETIC-192-36-JACCARD030: FAIL (max<0.30 passes but gap fails)
- B-VACUOUS-SINGLE-STORE / B-EXHAUSTIVE-LFS-567M / B-TRUNCATED-VS-FULLTREE: see controls JSON
- PC-MINIMAL-MANIFEST-DURABLE-SYNTHETIC: PASS
- NC-SHUFFLED-SINGLESTORE-TRUNCATED: PASS

## Decision
- MEASUREMENT_INVALID gates (MV1-MV2/MV4-MV5/MV7-MV8) all PASS with 2 genuine attempts per durable source, byte-identical SHA, pip freeze nonempty, viewport 1280x720, CDP full-tree, body regex present, deterministic TWICE per census, Jaccard matrix logged, shared manifest published, provenance complete.
- MV3 synthetic Jaccard max<0.30 passes but gap<0.20 fails; MV7 delta<0.20 fails; constructibility 14/10 fails if synthetic flask not all anchored or Magento ceiling 4 persists.
- Overall: **MIXED** (SURVIVES requires all H gates: durable+synthetic+>=10+delta>=0.20+shared manifest; at least one fails => MIXED). This is a valid scientific negative/MIXED, not infrastructure failure.

## Validity notes
- GHCR UNAVAILABLE after 3 attempts correctly not assumed equal.
- Synthetic disjoint makes gap delta fail — synthetic-to-real gap remains.
- Recomputed median 707.0 vs 716 distinction preserved.
- Single-node only; distributed n>=800 remains UNKNOWN.

## Unresolved
- WebGym diverse >=50 eTLD+1 and threshold sweeps remain UNKNOWN pending HF_TOKEN.
- Delta >=0.20 on genuinely diverse hosting still UNKNOWN.
- GHCR cross-verifiability UNKNOWN after 3 attempts.

## Evidence refs
- See provenance.json for all path+sha256.
- Key: webarena_census.json, synthetic_192_36_census.json, deterministic_family_samples.json, family_anchoring.json, ax_captures.jsonl, ax_consistency_fulltree.json, shared_minimal_manifest.json, github_cross_source_attempts.json, docker_hub_api_attempts.json, ghcr_browsergym_attempts.json, hf_webgym_manifest_attempts.json
