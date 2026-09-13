# EXP-FRONTIER-34729238832 Report: Binned PCA Projection to 2D-3D Subspaces

## 1. Executive Summary

Status: COMPLETE, Outcome: FALSIFIES

This experiment tests whether PCA dimensionality reduction before divergence computation can simultaneously detect both scaling-type and rotation-type action-dependent structure in the same 10D non-Gaussian DGP.

## 2. Methods

- Same 10D non-Gaussian DGP as parent experiments
- PCA projection to 2D and 3D subspaces (sklearn.decomposition.PCA)
- Binned TV divergence: 10 bins per dimension, mean across 6 action pairs
- 500 transitions per cell, 10 replications, 8 lambda levels
- Permutation null at lambda=0 with 50 permutations per cell

## 3. Results

### 2D PCA

Aggregate Spearman rho(binned_TV, lambda): 0.7619 (p_one_sided=0.014002)
Positive control: PASS
Null control: PASS (p=0.448667)
Function invariance (ANOVA interaction): FAIL
PCA explained variance: 0.2558

Per-function results:
- rotation: rho=0.7619, p=0.014002
- scaling: rho=0.6429, p=0.042779
- translation: rho=0.8571, p=0.003265

### 3D PCA

Aggregate Spearman rho(binned_TV, lambda): 0.6429 (p_one_sided=0.042779)
Positive control: PASS
Null control: PASS (p=0.459333)
Function invariance (ANOVA interaction): FAIL
PCA explained variance: 0.3692

Per-function results:
- rotation: rho=0.6429, p=0.042779
- scaling: rho=0.6429, p=0.042779
- translation: rho=0.6429, p=0.042779

## 4. Interpretation

The per-function heterogeneity observed across previous experiments (kNN TV fails scaling but detects rotation; KDE partially detects scaling but fails rotation) is tested for curse-of-dimensionality artifacts.

## 5. Decision

Status: COMPLETE, Outcome: FALSIFIES

## 6. Unresolved Questions

- Whether nonlinear PCA or other dimensionality reduction would perform better
- Whether 10 bins per dimension is optimal for binned TV
- Whether real Web transitions exhibit translation-like vs scaling-like structure