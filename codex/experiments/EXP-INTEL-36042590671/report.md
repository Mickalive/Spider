# EXECUTE report — EXP-INTEL-36042590671 (lane=intel, claim C-CROSSSITE)

## Status: COMPLETE | Outcome: MIXED

Frozen decision rule applied per prereg §8 (three-way after MEASUREMENT_INVALID gating).

### Key measurements (fresh live CDP probe, 1280x720, CDP Accessibility.getFullAXTree)

| Metric | Value | Gate | Pass |
|---|---|---|---|
| M_CONSTRUCTIBLE_FAMILIES | 4 ([136, 145, 196, 222]) | >=10 | False |
| M_AX_MEDIAN (canonical) | 716 | >10 | True |
| M_DOM_MEDIAN (canonical) | 203748 | >=2000 | True |
| M_SHA_STABILITY_TRUE | True (n=12) | 12/12 TRUE | True |
| M_SHA_MUTATION_SENSITIVITY | True (n=12) | 12/12 !=TRUE | True |
| M_MANIFEST_SHA_WEBARA | d652756608146633... byte-identical x2 fresh | d6527566... | True |
| M_WEBGYM_DIVERSE_ETLD | UNAVAILABLE (HF 401 x2) | >=50 | n/a |
| M_WEBGYM_SWEEP_RANGE | UNAVAILABLE | >=0.05 | n/a |
| M_PARAM_PREVALENCE (PC-C) | 0.8958 (expect 0.8958 +-0.05) | within tolerance | True |

### MV gating
{
  "MV1_DURABLE_ATTEMPTS": true,
  "MV2_BYTE_IDENTITY": true,
  "MV3_SAMPLED_DIVERSE_50": "UNAVAILABLE_HF_401_LOGGED",
  "MV4_THRESHOLD_SWEEP": "UNAVAILABLE_HF_401_LOGGED",
  "MV5_CONSTRUCTIBILITY": true,
  "MV5_WEBGYM_SAMPLE_LOGGED": true,
  "MV6_PARAM_PREVALENCE_PC_C": true
}

### Decision detail
{
  "mv_gating": {
    "MV1_DURABLE_ATTEMPTS": true,
    "MV2_BYTE_IDENTITY": true,
    "MV3_SAMPLED_DIVERSE_50": "UNAVAILABLE_HF_401_LOGGED",
    "MV4_THRESHOLD_SWEEP": "UNAVAILABLE_HF_401_LOGGED",
    "MV5_CONSTRUCTIBILITY": true,
    "MV5_WEBGYM_SAMPLE_LOGGED": true,
    "MV6_PARAM_PREVALENCE_PC_C": true
  },
  "src_ghcr_success": false,
  "src_docker_success": true,
  "byte_identical_webarena_sha": true,
  "sampled_diverse_ge50": null,
  "sweep_ok": null,
  "param_ok": true,
  "union_constructible_ge10": false,
  "union_constructible_families": [
    136,
    145,
    196,
    222
  ],
  "rule": "frozen three-way: (A) INVALID if MV gating fails; (B) SURVIVES if A passes and all H_A subgates; (C) FALSIFIED if union<=4 AND (diverse<50 OR sweep<0.05), MIXED if any module passes"
}

### Observations
- Fresh live CDP probe (1280x720 CDP Accessibility.getFullAXTree) on canonical families 136/145/196/222 succeeded: 12 product-page captures, canonical AX median 716, DOM median 203748.
- SHA stability (before==after) True; mutation sensitivity True on 12 captures.
- Constructible product families (anchoring true + SHA both directions): [136, 145, 196, 222] (n=4) - frozen gate >=10.
- WebGym 292k/127k manifests UNAVAILABLE: HF 401 x2 genuine attempts logged; per frozen MV3/MV4/MV5 exception, diverse/sweep clauses are UNAVAILABLE not falsified.
- PC-C synthetic parameterization harness reproduces 0.8958 within tolerance (10000 fields, 8958 param slots).
- Deterministic samples S1==S2=True on primary census; WebGym census sample attempt logged (ERROR due empty family list) per MV5 on EACH census.
- Docker Hub digest match TRUE (sha256:3e8cb9b945ea9...).

### Validity notes
- HF_TOKEN absent in environment; WebGym-derived clauses (diverse eTLD+1, B=2000 duplication CI, threshold sweep 0.818/0.9479, manifest SHA, param prevalence on real manifest) are UNAVAILABLE after 2+ genuine 401 attempts each with timeout>=300s configured. Per frozen MV3/MV4 exceptions UNAVAILABLE is not falsification and does not trigger MEASUREMENT_INVALID for those clauses alone.
- MV6 prevalence clause: WebGym manifest missing (HF 401) is treated as UNAVAILABLE per the MV3/MV5 exception pattern for WebGym-derived clauses; PC-C synthetic harness (must reproduce 0.8958 within tolerance) passed, satisfying the prevalence control requirement. If the audit requires a real-manifest prevalence, smallest repair is HF_TOKEN provisioning.
- Fresh live CDP probe: this experiment captured its own AX trees at 1280x720 via CDP Accessibility.getFullAXTree; no prior experiment captures were reused (prereg do-not-assume #63).
- Canonical product URLs derived from the pinned census family_product_urls (resolved via get_task_start_url __SHOPPING__ expansion).
- Single-source durability: Docker Hub digest verified (SRC_DOCKER_SUCCESS); GHCR 403/404 UNAVAILABLE after attempts logged; cross-source equality explicitly UNAVAILABLE not assumed equal (MV2).
- Bounded ceiling: constructibility measured on attempted censuses (pinned 812 + WebGym UNAVAILABLE); result is bounded, not global impossibility (prereg do-not-assume #64).

### Unresolved
- WebGym 292k/127k sampled diverse census requires HF_TOKEN provisioning; smallest unblocking action identified by Director.
- Whether GHCR BrowserGym 0.14.3 digest is cross-verifiable (UNAVAILABLE this run, Docker single-source suffices per prior audit).
- Real-manifest parameterization prevalence 0.8958 remains unmeasured (PC-C synthetic passes as control).

### Product consequence
Positive (SURVIVES): sampled census replaces exhaustive 567MB LFS; Graph/Physics banks unblocked.
Negative (FALSIFIED/MIXED): pinned WebArena 812 yields 4 constructible families (136,145,196,222); WebGym diverse UNAVAILABLE (HF 401); sampled census does NOT replace exhaustive LFS on these censuses. Next orthogonal census via independent eTLD+1 hosting or HF_TOKEN provisioning.
