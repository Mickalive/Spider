# SPIDER — product status, without research jargon (12 October 2026)

## One-sentence product proposition

A Web agent solves a workflow once, SPIDER records the validated reusable
**procedure** (not ephemeral answers or credentials), and another agent skips
re-discovery when the task's prerequisites still hold.

## What a user can actually run TODAY

**On main:** an importable Python **mechanism kernel** under `src/spider/`,
with tests: observe, conservative literal distill, store, guarded parameter
resolution, postcondition verification and invalidate. It does not itself
browse websites or call a language model. It is a component, not a SaaS.

**On unmerged draft PR #42:** a browser integration prototype. Real headless
Chromium visits a controlled local portal; two recorded visits can be compiled
into an ID-parameterized read-only procedure, stored and reused on unseen IDs.
A test bank fetches actual GitHub Releases pages, checks them against official
API results and reports a PyPI challenge without bypassing it. The optional
Browser Use LLM and real Stagehand v4 cache paths **are coded, not run in a
live credentialed trial**. The source is not production-approved.

**Not yet:** a install-and-forget site SDK, safe generic capture from arbitrary
agent traces, robust authentication/session handling, developer onboarding,
cross-site resilience, priced economic evidence or independent Product-lane
promotion. No claimed >=20% savings. These missing features cannot be
replaced by counting research experiments or passing CI.

## Zero-money constraint

Research uses only manually allowed OpenCode promotional/free models. These
may expire or be throttled; the research runner must fail closed and never
fall back to paid model IDs. A free model does NOT guarantee zero operational
resources: GitHub Actions minutes and wall-clock time are real budgets.

The Browser Use / Stagehand adapters in draft PR #42 currently use optional
provider/browser credentials that **may charge**. They do not automatically
become free merely because OpenCode research agents are free. They must remain
**disabled** until replaced by a demonstrably free adapter or explicitly
authorized otherwise. The user's present constraint is **no paid APIs**.

## One decisive next implementation, not another factory

1. Demonstrate a genuinely capable FREE agent that browses a nontrivial,
   read-only site and exports a validated trajectory. Do not fake the first
   agent with a hand-authored fixture API.
2. Convert that observed trajectory into a guarded procedure; repeat with
   unseen parameters. Fallback only when the mechanism cannot safely apply.
3. Compare the same free agent COLD vs instruction/retrieval vs SPIDER and
   compiled workflow/API competitors on two independent, non-ceiling families.
4. Measure wall-clock, tokens, browser calls, safe success and cost-in-compute;
   do NOT assume paid dollars or claim economic savings from synthetic prices.
5. If the simplest cached/compiled baseline ties SPIDER, simplify or pivot.
   Graph/fractal hypotheses stay research until a discriminating ablation.

In short: **SPIDER has a working product kernel and a tested prototype, not a
working customer product.** The next milestone is real end-to-end inheritance
by a FREE browser-capable agent on an external task.
