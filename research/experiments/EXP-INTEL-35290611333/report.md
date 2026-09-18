# EXP-INTEL-35290611333 — Literature Synthesis Report

## Experiment Summary

**Question**: Does a formal systematic search of psychometrics, econometrics, and meta-analysis literature on aggregation methods yield additional relevant prior art for SPIDER's density metric recipe choice problem, beyond the IR micro/macro/weighted framework identified in EXP-INTEL-35280397316?

**Outcome**: **SURVIVES_CURRENT_TEST** — All four frozen decision-rule conditions pass.

## Decision Rule Evaluation

### PC1: At least 2 well-documented aggregation recipe choice problems found in psychometrics or econometrics

**PASS** — 7 problems found across psychometrics (3) and econometrics (4).

**Psychometric examples:**
1. **Kane & Case (2003)**: Weighted composite scores for mixed-format tests (MC vs FR section weighting). Different weights produce different composites that answer different scientific questions — directly analogous to SPIDER's micro/macro/weighted recipes.
2. **PMC5978518**: Composite score construction from multiple measures (GPA + test scores + essays for medical admissions). The choice of weights reflects different judgments about relative importance.
3. **PMC11588849**: Sum score vs weighted score vs average score debate in Classical Test Theory (CTT). The field has extensively studied when each aggregation recipe is appropriate.

**Econometric examples:**
1. **OECD Handbook (2008)**: Arithmetic mean vs geometric mean vs weighted product for composite indicators. The "non-aggregators" school objects to aggregation because of "the arbitrary nature of the weighting process."
2. **Munda (2005)**: Social choice theory applied to aggregation rule selection for composite indicators.
3. **Dobbie (2013)**: Robustness/sensitivity of weighting and aggregation in composite indices.
4. **Zhou et al. (2009)**: Information loss perspective on data aggregation — different aggregation methods preserve different information.

### PC2: At least 1 principled method found that addresses MIXED outcome handling

**PASS** — 3 principled methods found.

1. **OECD sensitivity analysis framework (COINr)**: Systematically varies aggregation methods and weights, quantifies ranking stability via dominance pairs and confidence intervals, reports robustness bounds rather than choosing one recipe. This directly addresses the MIXED outcome problem — what to do when different aggregation methods give conflicting results.

2. **Social choice theory (Munda 2005)**: Provides formally grounded framework for aggregation rule selection under uncertainty about weights. When different recipes give conflicting conclusions, social choice theory offers axiomatic criteria for selecting among them.

3. **Robust meta-analytic metrics (Mathur & VanderWeele 2021)**: Reports proportion-above-threshold for heterogeneous effects. When the pooled estimate is significant but individual effects vary (MIXED outcome), this framework quantifies how many effects exceed a meaningful threshold.

### F1: No relevant prior art found

**NOT TRIGGERED** — Rich relevant art found across all three fields (12 sources included from 30 screened).

### F2: All found methods are weaker than existing IR framework

**NOT TRIGGERED** — Found methods strengthen and extend the IR framework:
- OECD sensitivity analysis is more systematic than IR micro/macro/weighted
- Social choice theory provides formal axiomatic grounding
- Meta-analytic heterogeneity quantification provides principled variance decomposition

## Key Findings

### 1. Cross-Field Convergence on Recipe Choice Ambiguity

The most important finding is that aggregation recipe choice ambiguity is not an IR-specific curiosity but a **general measurement phenomenon** documented across three independent fields:

- **Psychometrics**: composite score construction (sum vs weighted vs average)
- **Econometrics**: composite indicator construction (arithmetic vs geometric vs weighted product)
- **Meta-analysis**: effect size pooling (fixed vs random effects)
- **IR** (parent experiment): micro/macro/weighted averaging of precision/recall/F1

This convergent evidence strengthens the IR analogy from interpretive mapping to cross-field convergent evidence.

### 2. Principled Resolution Methods Beyond IR

The literature provides resolution methods that go beyond the IR micro/macro/weighted framework:

1. **Sensitivity analysis** (OECD/COINr): Systematically test robustness by varying aggregation methods and weights. Report ranking stability, dominance pairs, and confidence intervals. This is more principled than simply binding recipes to questions.

2. **Social choice theory** (Munda 2005): Apply axiomatic criteria from social choice theory to select aggregation rules. This provides formal theoretical grounding for recipe selection.

3. **Heterogeneity quantification** (Higgins & Thompson 2002): Use I-squared and tau-squared to quantify how much variance is due to methodological choices vs genuine effect heterogeneity.

### 3. Direct Applicability to MIXED Outcomes

The OECD sensitivity analysis framework directly addresses the MIXED outcome problem:

- When different aggregation methods produce conflicting results, **report the robustness bounds** rather than choosing one recipe
- Quantify **ranking stability** via dominance pairs (percentage of entity pairs whose ranking is invariant to aggregation choice)
- Provide **confidence intervals** on rankings that incorporate aggregation uncertainty

This is exactly what SPIDER needs for the MIXED outcome decision rule amendment.

## Claim Ceiling

This experiment provides theoretical grounding for recipe selection. The findings:

1. **Strengthen** the IR analogy with convergent evidence from three independent fields
2. **Provide** alternative resolution frameworks (sensitivity analysis, social choice theory, heterogeneity quantification)
3. **Inform** the MIXED outcome decision-rule amendment (sensitivity analysis framework)

However, the claim ceiling is bounded:
- Literature synthesis only; no new empirical measurement
- SPIDER-to-field applicability mappings are interpretive analogies, not established results
- The empirical question of which recipe is correct for SPIDER's density metric remains unresolved

## Inherited State Update

### Established (newly strengthened)
- Recipe choice ambiguity is a **general measurement phenomenon** documented across psychometrics, econometrics, meta-analysis, and IR (convergent cross-field evidence)
- Principled resolution methods exist across fields: recipe-as-question-binding, sensitivity reporting, micro/macro/weighted framework, **plus** OECD sensitivity analysis, social choice theory, and heterogeneity quantification

### Established (unchanged from parent)
- Recipe reversal is genuine (canonical per-iteration C2 FALSE vs per-task weighted C2 TRUE)
- Recipe choice is MATERIAL determinant of C-MEAS-VALID conclusion
- Canonical per-iteration p=0.5 recipe remains principled choice for C-MEAS-VALID

### Unknown (newly identified)
- Whether OECD sensitivity analysis framework can be operationalized for SPIDER's density metric
- Whether social choice theory axioms apply to SPIDER's recipe selection context
- Whether meta-analytic heterogeneity methods can quantify variance attributable to recipe choice

### Unknown (unchanged from parent)
- Whether C2 FALSE and C2 TRUE reversal both hold on full-DOM enumeration
- Whether IR framework is OPTIMAL resolution framework
- Cross-site generalization
- Spec decision-rule amendment for MIXED outcomes

### Do Not Assume (unchanged from parent)
- SPIDER-to-IR applicability mapping is established result (it is interpretive analogy)
- Non-systematic search captured all relevant prior art
- FALSIFIED conclusion generalizes to full-DOM
- Per-iteration recipe is universally canonical
- Density metric is entirely useless
- Recipe choice is nuisance parameter
- C-MEAS-VALID status changed from this experiment
