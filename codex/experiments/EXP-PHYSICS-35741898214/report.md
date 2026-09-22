# EXP-PHYSICS-35741898214 — Experiment Report

## Status: MEASUREMENT_INVALID

**Experiment ID:** EXP-PHYSICS-35741898214  
**Lane:** physics  
**Claim:** C-CROSSSITE (Reusable mechanisms transfer across website holdout)  
**Director Mandate:** PIVOT (SUPERSEDE) — `allocation.action=PIVOT`, `claim_id=C-CROSSSITE`, `parent_handoff_disposition=SUPERSEDE`, `cognitive_reset=true`  
**Frozen at:** 2026-09-22T14:44:05.232158+00:00  

---

## Summary

This experiment was designed to test whether TF-IDF→k-means parameterized mechanism clusters from task+action text transfer across true website/family holdouts by ≥0.10 beyond shuffled null, without site-identity leakage. The experiment is **MEASUREMENT_INVALID** because the required datasets are unavailable.

---

## Critical Finding: Required Datasets Unavailable

### Mind2Web — Official Splits Not Available

- **Dataset:** `osunlp/Mind2Web`
- **Revision:** `17ece8eb89862368edc0cc806acee6fca5163474`
- **Available splits:** `['train']` only (1009 tasks, 73 websites)
- **Required splits:** `train`, `test_website`, `test_domain`
- **Source:** HuggingFace Hub (unauthenticated requests)

Per spec.json falsifier: *"MEASUREMENT_INVALID if ... official Mind2Web splits are not available (synthetic 60/40 shuffle rejected per EXP-INTEL-35725763380 REVISE)"*  
Per prereg.md: *"If HF dataset revision lacks 3-way splits, record MEASUREMENT_INVALID with dataset_revision hash"*

### WebArena-Verified v2 — Data Not Available

- **Repository:** `web-arena/web-arena-verified`
- **Status:** 404 on HuggingFace; not found on GitHub
- **Expected data:** 192 shopping tasks, 49 intent_templates, 36 families (per EXP-INTEL-35697055679 census replication)

Per spec.json falsifier: *"MEASUREMENT_INVALID if ... WebArena cross-store overlap is invoked on WebArena-Verified v2"* and prereg.md requires family-level holdout on this dataset.

---

## Pipeline Verification (Completed)

Despite dataset unavailability, the TF-IDF→k-means pipeline was verified operational:

| Parameter | Value |
|---|---|
| Dataset | osunlp/Mind2Web train (1009 tasks, 73 websites) |
| k | 50 (min(50, floor(1009/20))) |
| TF-IDF vocab size | 1655 |
| n_clusters | 50 |
| Max cluster fraction | 10.7% (no collapse >40%) |
| Leakage tokens in top 100 | None |
| Text cleaning | URLs/domains/shop names removed via regex |

The pipeline is confirmed functional. The null distribution (proxy website-label shuffle, 100 shuffles) is degenerate (all overlap=1.0) because k-means assigns test tasks to existing train clusters, confirming the null cannot be properly estimated without official holdout structure.

---

## Prior Evidence Context

### EXP-INTEL-35697055679 (MIXED, audit PASS)
- WebArena-Verified v2 defines exactly **one shopping store**
- Cross-store overlap is vacuous null (not 0.0)
- Parameterization prevalence: 0.8958
- Duplication fraction: 0.9479

### EXP-INTEL-35725763380 (REVISE)
- WebArena census replicated exactly (192 tasks, 49 templates, 36 families)
- AX consistency unmeasured (ax_consistency=null)
- Mind2Web cross-website overlap measurement is **methodologically non-compliant**:
  1. Coarse 33-mechanism heuristic vs frozen TF-IDF→k-means k=min(50,unique_tasks/20)
  2. Synthetic 60/40 website shuffle replacing official train/test_website/test_domain splits
  3. 73/3 vs spec 137/31 divergence

---

## Validity Assessment

**Status:** MEASUREMENT_INVALID — substrate unavailability  
**Not a scientific negative.** This is an infrastructure/dataset failure, not evidence against the hypothesis. The C-CROSSSITE claim remains HYPOTHESIS.

The experiment design is sound (spec.json, prereg.md, freeze.json all frozen and consistent), but the required datasets for the primary measurement are unavailable from their specified sources. The pipeline is verified operational but cannot produce valid holdout overlap measurements.

---

## Consequences

### If datasets become available:
- Re-run with official Mind2Web splits (test_website, test_domain) and WebArena-Verified v2 family holdout
- 1000 website-label shuffles with k/2 and 2k sensitivity
- Full C1/C2/C3/PC/NC/SENS decision rule application

### If datasets remain unavailable:
- C-CROSSSITE remains HYPOTHESIS with narrowed ceiling
- Frontier/Graph should test richer mechanism definitions (DOM/AX patterns, learned embeddings, state-conditioned actions)
- Product lane keeps C-CROSSSITE bounded to 2-site corpus or within-store reuse only
- The director mandate PIVOT decision stands: true website-holdout test is the correct next_gate for C-CROSSSITE

---

## Reproducibility

```bash
# Load Mind2Web
python3 -c "from datasets import load_dataset; ds = load_dataset('osunlp/Mind2Web')"
# Dataset revision: 17ece8eb89862368edc0cc806acee6fca5163474
# Only train split available

# TF-IDF->k-means pipeline (verified)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
# k = min(50, floor(n_unique_train_tasks / 20))
# Vectorizer: max_features=5000, min_df=2, max_df=0.9, ngram_range=(1,2), stop_words='english'
# KMeans: n_clusters=k, init='k-means++', n_init=10, random_state=42
```

---

## References

- spec.json: `research/experiments/EXP-PHYSICS-35741898214/spec.json`
- prereg.md: `research/experiments/EXP-PHYSICS-35741898214/prereg.md`
- freeze.json: `research/experiments/EXP-PHYSICS-35741898214/freeze.json`
- request.json: `research/experiments/EXP-PHYSICS-35741898214/request.json`
- pipeline_results.json: `research/experiments/EXP-PHYSICS-35741898214/pipeline_results.json`
- EXP-INTEL-35697055679 codex: claim_state.json
- EXP-INTEL-35725763380 codex: claim_state.json
- Parent handoff: `research/experiments/EXP-PHYSICS-35697037202/handoff.json`
