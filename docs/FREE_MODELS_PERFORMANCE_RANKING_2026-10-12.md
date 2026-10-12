# SPIDER free-model quality ranking — 12 October 2026

**Status: provisional EXTERNAL prior, NOT measured SPIDER quality.** Do not
present the sorted list as a statistically established ranking of the twelve
models. There are no comparable completed and audited SPIDER task samples
for the new free-tier configurations. The most recent Factory public probe
(2026-10-12, run 38273833911) tested all twelve, certified **zero** READY
responses, and safely parked research. Unit-test/CI success is distinct
from real free-agent scientific throughput.

## Two distinct kinds of evidence

1. **Availability / price**: [official OpenCode Zen pricing]
   (https://opencode.ai/docs/en/zen/) confirms the twelve configured
   general text-agent models have *Free* input and output prices.
   Promotional access and pricing may change; no paid fallback is allowed.
2. **General intelligence, independent but not the same free OpenCode
   deployment**: [Artificial Analysis Muse Spark 1.3 (Xhigh)]
   (https://artificialanalysis.ai/models/comparisons/muse-spark-1-3-xhigh-vs-muse-spark-1-2)
   scores 45; [Ling 3.1 Flash vs MiMo V2.6 Flash]
   (https://artificialanalysis.ai/models/comparisons/ling-3-1-flash-vs-mimo-v2-6-flash)
   score 41 vs 38. These are NOT matched-context SPIDER free-endpoint
   results: reasoning modes, providers and runtime may differ.
3. **Agentic coding, direct free OpenCode endpoints but very small sample**:
   [independent community test on 8 October 2026]
   (https://www.reddit.com/r/opencode/comments/1x0kuv2/which_free_opencode_models_are_fast_reliable/)
   uses two Q&A items and one real code-fix with pytest (420-second cutoff).
   Its author explicitly warns that **one repository/task run cannot
   establish reliability**.

## Observed small-sample community task ranking

| Model (currently zero-priced) | Community code-agent score / 100 | Confidence |
|---|---:|---|
| MiMo V2.6 Flash | 100 | low (one task bank) |
| Muse Spark 1.3 Contributor | 99 | low |
| Space Bunny | 95 | low |
| LongCat 2.5 Preview | 92 | low |
| Ling 3.1 Flash | 91 | low |
| Nemotron 3 Ultra | 70 | low |
| Nemotron 3.5 Lightning | 20 | low |
| Exo | 0 | *not evidence of intrinsic ability*: unavailable/timeout |
| Ling 3.0 Flash Fin | 0 | *not evidence of intrinsic ability*: unavailable/timeout |
| Step 5 Preview | unknown | not included in this comparison |
| MiMo V2.5 | unknown | not included in this comparison |
| Big Pickle | unknown | undisclosed/stealth underlying model |

The scores are from the linked user's scoring rule, not accuracy percentages,
not a scientific full-task ranking and not measurements from SPIDER. An
unavailable model stays in the free fallback list and is not permanently
classified as low-ability by an incidental provider incident.

## Actual routing in the repo

`config/models.json` is the sole source of allowed paid/free identities,
ranking sources and per-role priority. All **12** verified-zero-price models
remain eligible for every role, rather than a misleading universally-best
model assignment.

- **Research / Global Director:** Muse Spark 1.3 → Ling 3.1 → MiMo V2.6,
  privileging measured general-reasoning evaluations.
- **Coding / execution:** MiMo V2.6 → Muse Spark 1.3 → Space Bunny → LongCat
  2.5 → Ling 3.1, provisionally using the direct OpenCode code-agent test.
- **Audit / independent design review:** Ling 3.1 → Muse Spark 1.3 → MiMo
  V2.6, with a strict exclusion of the producing model.
- **Scout:** Ling 3.1 → Muse Spark 1.3 → MiMo V2.6; for reconnaissance,
  general reasoning and speed matter, not only coding.
- **Unknown-performance tail:** Step 5, MiMo V2.5, Big Pickle, Exo and other
  remaining verified-free models stay available as fallback. Their relative
  order is a **policy tie-break**, not a claimed empirical difference.

The global provider preflight attempts models in the provisional
reasoning-performance order. Once **one** free candidate actually responds
with a verified exact probe, that **known reachable** model is promoted to
the front of each role's execution candidates; among unprobed alternatives,
the relevant role's quality order governs. This ensures offline rankings
never outrank *real* provider availability. A reviewer always excludes the
producer even when the healthy free model is shared.

## What would constitute a real SPIDER-specific leaderboard?

At least multiple independently verifiable tasks per role/model, under
comparable prompts, identical environment/timeouts and blocked paid models.
Record safe task success, tool-use errors, wall clock, source-verified
output validity and retained tokens. Distinguish no-access/no-credential
from model errors and from genuine capability failures. Compute stratified
task success and confidence intervals; *do not infer quality from probe
availability*, a single Q&A, or aggregate claims of intelligence.

Until those matched experiments exist, this is an **evidence-aware provisional
order**, not a reliable definitive per-model performance ranking.

## Key unrelated blocker

All twelve previously returned `NO_ATTESTED_OUTPUT`, provider unavailability
or timeout during the first live broad probe. The earlier `Invalid
credential` responses are not fixed by sorting models. Live free-agent
research must resume only when credentials/provider respond successfully.
The CI health gate may report success while legitimately parked.
