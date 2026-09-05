# PREREGISTRATION — INTEL LANE, PROGRAM `intel-benchmark-audit`, CYCLE 1

**Experiment ID:** EXP-INTEL-33528832113
**Lane:** Intel
**Date:** 2026-09-01
**Status:** DESIGN ONLY (no outcome-bearing measurements)

---

## 1. Question

Which publicly available web-agent benchmarks contain multi-step stateful task structures that could serve as stronger testbeds for SPIDER's cross-site inheritance (C-CROSSSITE) and LLM-inheritance (C-LLM-INHERIT) claims than the current 2-site (quotes/books) corpus?

## 2. Motivation

### 2.1 Current limitation

ALL graph experiments (G-H1 through G-H9) use only 2 small structured sites:
- quotes.toscrape.com
- books.toscrape.com

This means:
- **C-CROSSSITE** ("reusable mechanisms transfer across website holdout") cannot be tested on general web structure -- there is no "other site" to hold out.
- **C-LLM-INHERIT** ("a real LLM agent benefits from SPIDER beyond strong memory/instruction baselines") can only be demonstrated on toy sites, limiting product credibility.
- **C-PRODUCT-ECON** ("SPIDER saves total cost per successful task") has no evidence on realistic task complexity.

### 2.2 What Intel can contribute

The Intel lane's charter is to "find, reproduce and stress-test datasets, baselines and prior art only when they can alter a live SPIDER claim or experimental design." This experiment directly serves that charter by determining whether external benchmarks exist that could alter the C-CROSSSITE and C-LLM-INHERIT experiment designs.

### 2.3 Prior art (pre-2.0 codex)

The pre-2.0 codex references Mind2Web, WebArena, and other benchmarks only as citation context -- never as integrated testbeds. No prior Intel experiment has systematically audited these benchmarks for structural compatibility with SPIDER's fragment-reuse model.

## 3. Hypothesis

At least one public web-agent benchmark satisfies all of:
- (S1) Tasks span ≥2 page transitions (multi-step)
- (S2) Trajectory data is publicly downloadable or reproducible
- (S3) Task structure includes stateful interactions (form fills, login, session-dependent actions)
- (S4) Environment is self-hostable or has API replay
- (S5) Task diversity covers ≥3 distinct website types

## 4. Search strategy

### 4.1 Identification (exhaustive, not selective)

Search terms:
- "web agent benchmark" / "web agent dataset"
- "browser automation benchmark"
- "web navigation benchmark"
- "webagent benchmark" / "webagent dataset"
- Specific known benchmarks: Mind2Web, WebArena, VisualWebArena, WorkArena, AgentBench, MiniWoB++, WebShop, Mind2Web, QWeb,url.NAV, ARES, AssistantBench

Search sources:
- GitHub topics: web-agent, web-benchmark, browser-agent
- Papers With Code: Web Navigation category
- arXiv searches (2022-2026)
- Semantic Scholar / Google Scholar forward citations of Mind2Web and WebArena

### 4.2 Structural assessment (predeclared criteria)

For each identified benchmark, assess:

| Criterion | Definition | How to verify |
|-----------|-----------|---------------|
| S1: Multi-step | Tasks require ≥2 page transitions to complete | Check task descriptions, trajectory length statistics |
| S2: Trajectory access | Trajectory data is downloadable OR the environment replays identically | Check dataset hosting (HuggingFace, GitHub releases, Zenodo) or replay documentation |
| S3: Stateful interactions | Tasks involve form fills, login, session state, or dynamic content | Check action vocabulary, task examples |
| S4: Self-hostable/replayable | Environment can be self-hosted OR API responses can be replayed | Check Dockerfile, docker-compose, replay server, or mock infrastructure |
| S5: Website diversity | Tasks span ≥3 distinct website types (e-commerce, wiki, social, news, etc.) | Check per-site task counts, website categorization |

### 4.3 Scoring

- RECOMMENDED: S1+S2+S3+S4 ≥ 3
- STRONGLY RECOMMENDED: S1+S2+S3+S4+S5 = 5
- NOT RECOMMENDED: S1+S2+S3+S4 < 3

## 5. Known candidates (must be assessed, not skipped)

These benchmarks are known to exist and MUST be included in the audit. They may NOT be excluded after seeing their properties:

1. **Mind2Web** (2023) -- cross-task, cross-website; 2000+ tasks; 137 websites
2. **WebArena** (2024) -- 812 long-horizon tasks; 4 real websites; full replay
3. **VisualWebArena** (2024) -- visual variant; 910 tasks; 4 websites
4. **WorkArena** (2024) -- ServiceNow tasks; not web-browsing per se
5. **AgentBench** (2023) -- multi-environment; includes web browsing subset
6. **WebShop** (2022) -- simulated e-commerce; 12K instructions
7. **MiniWoB++** (2018) -- simulated mini-tasks; 100+ task types
8. **QWeb** (2024) -- question-driven web navigation
9. **AssistantBench** (2024) -- real-world web assistant tasks
10. **AWM** (2024) -- web manipulation benchmark

Any additional benchmarks discovered during search must also be assessed.

## 6. Deliverable

A ranked table:

| Rank | Benchmark | Year | # Tasks | S1 | S2 | S3 | S4 | S5 | Total | Verdict | Integration notes |
|------|-----------|------|---------|----|----|----|----|----|----|---------|-------------------|

Plus:
- Per-benchmark notes on what makes it compatible or incompatible with SPIDER's fragment-reuse model
- Recommended integration priority for C-CROSSSITE and C-LLM-INHERIT
- Any benchmarks that are close (S1+S2+S3+S4 = 2) but blocked by a single missing capability

## 7. Validity threats

- **Search incompleteness:** The web-agent benchmark landscape is fast-moving (2022-2026). New benchmarks may have appeared after the last codex update. Mitigation: use multiple search sources; acknowledge search date.
- **Access claims may be stale:** A benchmark that was publicly available at time of paper may have had its server shut down. Mitigation: verify access claims by checking actual repositories, not just paper text.
- **Structural compatibility ≠ experimental suitability:** A benchmark may score 5/5 on structural criteria but still be unsuitable for SPIDER (e.g., tasks too simple, too complex, or requiring capabilities SPIDER doesn't have). Mitigation: this audit identifies candidates; suitability requires a separate experiment.
- **SPIDER fragment-reuse model is not formalized:** The criteria S1-S5 are proxies for "could SPIDER's fragment mechanism work here." They are not guarantees. Mitigation: flag uncertain cases.

## 8. What this experiment is NOT

- This is NOT an experiment on SPIDER's capabilities. No SPIDER code runs.
- This is NOT a claim that any benchmark is "better" than the current 2-site corpus in general.
- This is NOT a commitment to integrate any benchmark. Integration requires a separate experiment.
- This is NOT a literature review. It is a structured audit with predeclared criteria.

## 9. Decision consequences

### If ≥1 STRONGLY RECOMMENDED benchmark is found:
- Graph lane: consider designing C-CROSSSITE experiment on the recommended benchmark instead of (or in addition to) the 2-site corpus
- Product lane: consider designing C-LLM-INHERIT experiment on the recommended benchmark
- Intel lane: subsequent cycle could attempt reproduction/stress-test of the recommended benchmark

### If ≥1 RECOMMENDED but no STRONGLY RECOMMENDED:
- Same as above but with caveat that one structural dimension is missing
- Identify which dimension is missing and whether it blocks SPIDER specifically

### If zero RECOMMENDED:
- C-CROSSSITE and C-LLM-INHERIT remain bounded to 2-site corpus
- Product lane must decide: build a diverse testbed in-house, or accept permanent scope limitation
- Intel lane: next cycle could audit whether building an in-house testbed is feasible

---

*This preregistration is frozen before any outcome data is collected.*
*No benchmark structural properties have been inspected prior to this design.*
