# Experiment Report — EXP-INTEL-36103378878

## Status: COMPLETE | Outcome: MIXED

## Executive Summary

This experiment tested whether an orthogonal diverse census via independent eTLD+1 hosting (and/or HF_TOKEN-provisioned WebGym 292k) could deliver discriminating diverse-site evidence for closing the C-CROSSSITE tunnel.

**Key finding:** The orthogonal hosting approach (Branch B) creates 10 distinct eTLD+1 hosts with heterogeneous DOM templates, but these are minimal HTML pages (300-400 bytes, DOM textContent 67-107) that fail the DOM>=2000 constructibility gate. The canonical Magento family (magento_136) passes all liveness gates. The overall outcome is **MIXED**.

## Measurement Results

### Branch A: HF_TOKEN WebGym 292k
- **Status:** UNAVAILABLE
- **HF_TOKEN present:** False
- **Attempts:** 2x404 on `https://huggingface.co/api/datasets/ServiceNow/WebGym/refs/main`
- **Smallest-next-action:** scope (ServiceNow/WebGym read-scope, OpenEnv/WebGym), quota (unknown), mirror (unknown)
- **Gate result:** UNAVAILABLE (not falsified per MV6)

### Branch B: Orthogonal Independent eTLD+1 Hosting
- **Sites created:** 10 distinct hostnames with heterogeneous DOM templates
  - tech_store, book_store, fashion_store, home_store, sports_store, pet_store, toy_store, garden_store, auto_store, music_store
- **Distinct eTLD+1 via tldextract:** 10 ✓
- **AX tree nodes:** 20 per site (>10 ✓)
- **DOM textContent:** 67-107 per site (<2000 ✗)
- **Jaccard max:** 0.1111 (<0.30 ✓)
- **Jaccard gap vs shuffled:** 0.0202 (<0.20 ✗)
- **Threshold sweep range:** 0.0521 (>=0.05 ✓)
- **Canonical delta (fulltree vs truncated):** 0.6667 (>=0.20 ✓)
- **Real constructible families (DOM>=2000):** 1 (magento_136) ✗

### Durable Pins
- **Docker image:** `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945...` verified via docker pull (status 0) ✓
- **Container:** `spider-intel-36103378878-shopping` running at `localhost:7770` ✓
- **Canonical family (magento_136):** AX=1430, DOM=56764, SHA changed on mutation ✓
- **Hard258:** Verified from parent experiment ✓

### Blind Baselines
- **Stagehand HIT/MISS:** HIT=1.0, FA=0.0 on bounded substrate (14 families) ✓
- **DSM/TraceCompiler:** precision=1.0, alias_gain=0.8571 ✓

## Gate Evaluation

| Gate | Expected | Observed | Pass |
|------|----------|----------|------|
| Jaccard<0.30 | max<0.30 | 0.1111 | ✓ |
| Jaccard gap>=0.20 | gap>=0.20 | 0.0202 | ✗ |
| Threshold sweep range>=0.05 | range>=0.05 | 0.0521 | ✓ |
| Delta>=0.20 (canonical) | delta>=0.20 | 0.6667 | ✓ |
| AX>10, mean>15, std>5 | median>10 | 20, 148, 425 | ✓ |
| DOM>=2000 | median>=2000 | 77 | ✗ |
| >=10 real constructible | >=10 | 1 | ✗ |
| SHA before==after TRUE | TRUE | TRUE | ✓ |
| HF_TOKEN UNAVAILABLE logged | smallest-next-action | documented | ✓ |
| Docker digest verified | 64-char match | verified | ✓ |

## Decision Rule Application

Per the frozen three-way decision rule:
- **(A) MEASUREMENT_INVALID:** Not triggered. All MV1-MV2/MV4-MV5/MV7-MV8 gating checks passed (>=2 attempts per source, SHA verified, pip freeze non-empty, grammar hash live, body regex present, deterministic sampling executed, shared manifest published, provenance complete).
- **(B) SURVIVES_CURRENT_TEST:** Not triggered. Branch B fails the DOM>=2000 gate and the >=10 real constructible families gate. Branch A is UNAVAILABLE.
- **(C) MIXED:** Applied. Branch B partially passes (Jaccard<0.30, delta>=0.20, AX gates pass) but fails critical constructibility gates. Branch A is UNAVAILABLE. Single primary branch partial pass → MIXED.

## Conclusion

The experiment demonstrates that:
1. Orthogonal independent eTLD+1 hosting can create distinct hostnames with different templates
2. These sites fail the DOM>=2000 constructibility gate because they are minimal HTML pages
3. The canonical Magento family passes all liveness and constructibility gates
4. The true website holdout (C-CROSSSITE next_gate) remains blocked pending either:
   - More complex orthogonal hosting sites with full product-subtree DOM (2000+ textContent)
   - HF_TOKEN provisioned WebGym 292k diverse census
   - Truly independent external eTLD+1 hosting beyond synthetic domains

C-CROSSSITE remains HYPOTHESIS at 4-family real + 10-synthetic ceiling.

## Artifacts

All artifacts are stored at `research/experiments/EXP-INTEL-36103378878/artifacts/`:
- Raw: attempt logs (HF, GitHub, GHCR, Docker Hub, orthogonal hosting, Stagehand, DSM), AX captures
- Derived: census, Jaccard matrix, shared manifest, AX results (orthogonal and canonical)

## Provenance

- Request hash: `f8950754ed776156e0a6a9478984c6fac1268f67ece7e97546ff507f97fbbff`
- Spec hash: `dd5f0be8a227065134282172f1fd58fbc0281be1d2413eea02745d75fecc3ebd`
- Prereg hash: `4fa78552b70b14447d8dd3789a6a3faf3c6e8e5cd20e05ea19dea64fe1aaaa8c`
- Pip freeze: 245 lines, sha `2392b35d67f4b40a71abf68df16d81c1`
- Grammar hash: `273eafbcb817e8981f843581a724594665cabdd357b318c701251929ee9c83de`
- Docker image: `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945ea9b1c94ab26dba53e8d12dd0406abbf4bf686fd3bb2b6a5908feb`
